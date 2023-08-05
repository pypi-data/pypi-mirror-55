import os
import re
import time
import torch
from torch import nn
import matplotlib.pyplot as plt
from functools import partial
from fastprogress import master_bar
from fastprogress import progress_bar
from fastprogress.fastprogress import format_time
from IPython.core.debugger import set_trace
from pathlib import Path
from types import SimpleNamespace
from .datasets import URLs
from .utils import ALL_CALLBACKS, camel2snake, listify, cos_1cycle_anneal, combine_scheds, create_phases
from .utils import CancelTrainException


# this enables us to plot tensors
torch.Tensor.ndim = property(lambda x: len(x.shape))

# to be used with the DebugCallback
callback_types = SimpleNamespace(**{o:o for o in ALL_CALLBACKS})

def print_details(o):
    "print function to be used with the DebugCallback"
    print('parameter groups: ', len(o.opt.param_groups), '\n',
           'hyperparam dicts:', '\n',
           '\n'.join([('dict ' + str(i) + ': ' + str(hyper))
                      for i, hyper in enumerate(o.opt.hypers)]))
    raise CancelTrainException()

class Callback():
    """
    Base Callback class, can be called like a function with attr names as args,
    where attrs are methods (e.g., begin_fit, after_batch etc.) to be called at
    relevant points in the train-eval loop.
    The learn (i.e., learner) argument is the learner, which will incorporate the
    callback as one of its attributes.
    _order keeps track of the priority of the callbacks so that they can be
    called in order of priority.
    __getattr__ percolates attrs from inside the learn object up to the callback.
    The name property converts the callback name from camel to snake; the name
    is then percolated up to the learner and becomes one of its attributes.
    """
    _order = 0
    def set_learner(self, learn):
        self.learn=learn
    def __getattr__(self, k):
        return getattr(self.learn, k)

    @property
    def name(self):
        name = re.sub(r'Callback$', '', self.__class__.__name__)
        return camel2snake(name or 'callback')

    def __call__(self, callback_name):
        f = getattr(self, callback_name, None)
        if f and f():
            return True
        return False

class TrainEvalCallback(Callback):
    """
    Callback to do basic training and evaluation.
    """
    def begin_fit(self):
        self.learn.n_epochs = 0.
        self.learn.n_iter = 0

    def after_batch(self):
        if not self.in_train: return
        self.learn.n_epochs += 1./self.iters
        self.learn.n_iter   += 1

    def begin_epoch(self):
        self.learn.n_epochs = self.epoch
        self.model.train()
        self.learn.in_train = True

    def begin_validate(self):
        self.model.eval()
        self.learn.in_train = False

class AvgStats():
    def __init__(self, metrics, in_train):
        self.metrics = listify(metrics)
        self.in_train = in_train
        # dictionary to record metrics for plotting
        self.metrics_dict = {'loss':[]}
        for metric in self.metrics:
            self.metrics_dict[metric.__name__] = []

    def reset(self):
        self.tot_loss = 0.
        self.count = 0
        self.tot_metrics = [0.] * len(self.metrics)

    @property
    def all_stats(self):
        return [self.tot_loss.item()] + self.tot_metrics
    @property
    def avg_stats(self):
        return [statistic/self.count for statistic in self.all_stats]

    def __repr__(self):
        if not self.count: return ""
        return f"{'train' if self.in_train else 'valid'}: {self.avg_stats}"

    def accumulate(self, learn):
        batch_size = learn.xb.shape[0]
        self.tot_loss += learn.loss * batch_size
        self.metrics_dict['loss'].append(learn.loss.detach().cpu().item())
        self.count += batch_size
        for i, metric in enumerate(self.metrics):
            current_statistic = metric(learn.pred, learn.yb)
            self.tot_metrics[i] += current_statistic * batch_size
            self.metrics_dict[metric.__name__].append(current_statistic.detach().cpu().item())

class AvgStatsCallback(Callback):
    # _order = -1
    def __init__(self, metrics):
        self.train_stats = AvgStats(metrics, True)
        self.valid_stats = AvgStats(metrics, False)

    def begin_fit(self):
        met_names = ['loss'] + [m.__name__ for m in self.train_stats.metrics]
        names = ['epoch'] + [f'train_{n}' for n in met_names] + [
            f'valid_{n}' for n in met_names] + ['time']
        self.logger(names)

    def begin_epoch(self):
        self.train_stats.reset()
        self.valid_stats.reset()
        self.start_time = time.time()

    def after_loss(self):
        stats = self.train_stats if self.in_train else self.valid_stats
        with torch.no_grad():
            stats.accumulate(self.learn)

    def after_epoch(self):
        stats = [str(self.epoch)]
        for stat in [self.train_stats, self.valid_stats]:
            stats += [f'{v:.6f}' for v in stat.avg_stats]
        stats += [format_time(time.time() - self.start_time)]
        # We use the logger function of the `Learner` here, which
        # can be customized to write in a file or in a progress bar
        self.logger(stats)

    # def after_fit(self):
        # self.train_metrics_dict.update(self.train_stats.metrics_dict)
        # self.valid_metrics_dict.update(self.valid_stats.metrics_dict)


class ProgressCallback(Callback):
    _order=-1
    def begin_fit(self):
        # set master bar (for epochs) when we start fitting
        self.mbar = master_bar(range(self.epochs))
        # initialize mbar
        self.mbar.on_iter_begin()
        # replace logger (default: printing) with mbar
        self.learn.logger = partial(self.mbar.write, table=True)

    def after_fit(self):
        # tell mbar we're done
        self.mbar.on_iter_end()

    def after_batch(self):
        # update progress bar after every batch
        self.pb.update(self.iter)

    def begin_epoch(self):
        # set progress bar at the beginning of every training epoch
        self.set_pb()

    def begin_validate(self):
        # set progress bar at the beginning of validation
        self.set_pb()

    def set_pb(self):
        self.pb = progress_bar(self.dl, parent=self.mbar, auto_update=False)
        self.mbar.update(self.epoch)

class TestCallback(Callback):
    """
    Callback to quickly test the model works. Has to follow TrainEvalCallback.
    """
    _order = 1
    def after_step(self):
        if self.n_iter>=10:
            print("ran {} batches successfully".format(self.n_iter))
            raise CancelTrainException()

class CudaCallback(Callback):
    def begin_fit(self):
        self.model.cuda()

    def begin_batch(self):
        self.learn.xb = self.xb.cuda()
        self.learn.yb = self.yb.cuda()

class Plotter(Callback):
    """
    Recording functions for everything but the lr are relegated to
    AvgStatsCallback, which in turn leverages the metrics_dict in AvgStats.
    The Plotter callback additional records lr and provides plotting
    functionality
    """
    _order = 0
    def begin_fit(self):
        self.lrs = []

    def after_batch(self):
        if not self.in_train: return
        # plot the lr for the last layer group
        self.lrs.append(self.opt.hypers[-1]['lr'])

    def plot_lr(self):
        plt.plot(self.lrs)
        plt.xlabel('iteration')
        plt.ylabel('learning rate')

    def plot_lr_finder(self, skip_last=0):
        losses = self.avg_stats.train_stats.metrics_dict['loss']
        n = len(losses)-skip_last
        plt.xscale('log')
        plt.plot(self.lrs[:n], losses[:n])
        plt.xlabel('log learning rate')
        plt.ylabel('loss')

    def plot_stats(self, stats):
        metrics = stats.keys()
        ncols = 2
        if len(metrics) % ncols == 0:
            nrows = len(metrics) // ncols
        else:
            nrows = len(metrics) // ncols + 1
        _, axes = plt.subplots(nrows=nrows, ncols=ncols)
        for ax, metric in zip([*axes], metrics):
            ax.plot(stats[metric])
            ax.set_xlabel('iteration')
            ax.set_ylabel(metric)
        plt.tight_layout()


    def plot_train_stats(self):
        self.plot_stats(self.avg_stats.train_stats.metrics_dict)

    def plot_valid_stats(self):
        self.plot_stats(self.avg_stats.valid_stats.metrics_dict)

class LR_Find(Callback):
    _order = 1
    def __init__(self, max_iter=100, min_lr=1e-6, max_lr=10):
        self.max_iter = max_iter
        self.min_lr = min_lr
        self.max_lr = max_lr
        self.best_loss = 1e9

    def begin_batch(self):
        if not self.in_train: return
        pos = self.n_iter/self.max_iter
        lr = self.min_lr * (self.max_lr/self.min_lr) ** pos
        for pg in self.opt.hypers: pg['lr'] = lr

    def after_step(self):
        if self.n_iter>=self.max_iter or self.loss>self.best_loss*10:
            self.plotter.plot_lr_finder(3)
            raise CancelTrainException()
        if self.loss < self.best_loss:
            self.best_loss = self.loss

class GradientClipping(Callback):
    """
    Checks after the backward pass if the norm (sum of squares) of the
    gradients is greater than the number clip; if they are, they get
    divided (scaled down) so that they're smaller than clip.
    """

    def __init__(self, clip=None):
        self.clip = clip

    def after_backward(self):
        if self.clip:
            nn.utils.clip_grad_norm_(self.learn.model.parameters(), self.clip)

class ParamScheduler(Callback):
    """
    assumes there are as many scheduling functions as there are param groups
    (if only one function is passed, it is cloned for each param group).
    the scheduling functions are then used to set the value of the parameter
    pname in each param group based on the current position in the training loop.
    """
    _order = 1
    def __init__(self, pname, sched_funcs):
        self.pname = pname
        self.sched_funcs = listify(sched_funcs)

    def begin_batch(self):
        if not self.in_train: return
        fs = self.sched_funcs
        if len(fs)==1:
            fs = fs*len(self.opt.param_groups)
        pos = self.n_epochs/self.epochs
        for f, h in zip(fs, self.opt.hypers):
            h[self.pname] = f(pos)

def sched_1cycle(lrs, pct_start=0.3, mom_start=0.95, mom_mid=0.85, mom_end=0.95):
    lrs = listify(lrs)
    phases = create_phases(pct_start)
    sched_lr = [combine_scheds(phases, cos_1cycle_anneal(lr*1e-1, lr, lr*1e-5))
                for lr in lrs]
    sched_mom = combine_scheds(phases, cos_1cycle_anneal(mom_start, mom_mid, mom_end))
    return [ParamScheduler('lr', sched_lr), ParamScheduler('mom', sched_mom)]

class RNNTrainer(Callback):
    """
    Adds two L2 penalties on activations (not weights).
    Activation Regularization (AR): ensures activations are not too high.
    Temporal Activation Regularization (TAR): ensures activations don't change
    radically from timestep to timestep.
    """
    def __init__(self, alpha, beta):
        # parameter for Activation Regularization (AR)
        self.alpha = alpha
        # parameter for Temporal Activation Regularization (TAR)
        self.beta = beta

    def after_pred(self):
        # Save the extra outputs for later and only returns the true output.
        self.raw_out = self.pred[1]
        self.out = self.pred[2]
        self.learn.pred = self.pred[0]

    def after_loss(self):
        # Activation Regularization (AR): we add to the loss an L2 penalty
        # on the last activations of the AWD LSTM (with dropout applied)
        if self.alpha != 0.:
            self.learn.loss += self.alpha * self.out[-1].float().pow(2).mean()
        # Temporal Activation Regularization (TAR): we add to the loss an L2
        # penalty on the difference between two consecutive (in terms of
        # words) raw outputs
        if self.beta != 0.:
            h = self.raw_out[-1]
            if len(h)>1:
                self.learn.loss += self.beta * (h[:,1:] - h[:,:-1]).float().pow(2).mean()

    def begin_epoch(self):
        # Shuffle the texts at the beginning of the epoch
        if hasattr(self.dl.dataset, "batchify"):
            self.dl.dataset.batchify()

class DebugCallback(Callback):
    """
    Overrides __call__ itself to ensure we debug callback callback_name.
    When callback_name is called, it call the function func if it's provided,
    otherwise, it calls the debugger (set_trace).
    example usage: callbacks = [DebugCallback(callback_types.after_batch, print_details)]
    """
    _order = 999
    def __init__(self, callback_name, func=None):
        self.callback_name = callback_name
        self.func = func

    def __call__(self, callback_name):
        if callback_name == self.callback_name:
            if self.func:
                self.func(self.learn)
            else:
                set_trace()

class SaveModelCallback(Callback):
    def __init__(self, model_name, path_str=None):
        self.model_name = model_name
        if path_str and isinstance(path_str, str):
            self.abs_path = URLs.LOCAL_PATH/path_str
        else:
            self.abs_path = URLs.LOCAL_PATH

    def after_epoch(self):
        torch.save(self.model.state_dict(),
                   self.abs_path/(self.model_name + '_' + str(int(self.n_epochs-1)) + '.pth'))

    def after_fit(self):
        torch.save(self.model.state_dict(),
                   self.abs_path/(self.model_name + '_final.pth'))
