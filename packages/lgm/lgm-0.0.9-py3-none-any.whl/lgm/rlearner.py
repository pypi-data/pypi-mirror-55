import torch
from functools import partial
from torch import tensor
from .optimizer import adam_opt
from .utils import ALL_CALLBACKS, param_getter, listify, CancelTrainException, CancelEpochException, CancelBatchException
from .callbacks import TrainEvalCallback, ProgressCallback, Plotter, SendToDeviceCallback, AvgStatsCallback, SaveModelCallback

class RLearner():
    """
    THIS IS JUST A STUB (for now, mostly copied from learner.py) FOR A REINFORCEMENT LEARNER CLASS
    -- we replace model with agent and data with env (environment)
    -- restructure this in a way partly inspired by rl_glue code from the Coursera RL specialization
    """
    def __init__(self, agent, env, loss_func, opt_func=adam_opt(), lr=1e-2,
                 splitter=param_getter, metrics=None, callbacks=None,
                 callback_funcs=None, device=None, reset_opt=False,
                 model_name=None, path_str=None):
        raise NotImplementedError
