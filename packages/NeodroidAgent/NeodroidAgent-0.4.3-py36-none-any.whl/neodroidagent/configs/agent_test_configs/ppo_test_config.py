#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from torch.nn import MSELoss

from neodroidagent.architectures.distributional.normal import MultiDimensionalNormalMLP
from neodroidagent.architectures.experimental.merged import MergedInputMLP
from .base_continous_test_config import *

__author__ = 'Christian Heider Nielsen'
'''
Description: Config for training
Author: Christian Heider Nielsen
'''

# General

CONFIG_NAME = __name__
import pathlib

CONFIG_FILE_PATH = pathlib.Path(__file__)

CONNECT_TO_RUNNING = False
RENDER_ENVIRONMENT = True
TEST_INTERVAL = 1000

INITIAL_OBSERVATION_PERIOD = 0

STEPS = 20

MEMORY_CAPACITY = STEPS
BATCH_SIZE = 64

TARGET_UPDATE_INTERVAL = 1000
TARGET_UPDATE_TAU = 1.0
MAX_GRADIENT_NORM = None

GAE_TAU = 0.95
DISCOUNT_FACTOR = 0.95

REACHED_HORIZON_PENALTY = -10.

# CRITIC_LOSS = F.smooth_l1_loss
CRITIC_LOSS = MSELoss

PPO_EPOCHS = 4

SEED = 66

VALUE_REG_COEF = 0.5
ENTROPY_REG_COEF = 1.0

SURROGATE_CLIPPING_VALUE = 0.2  # initial probability ratio clipping range
SURROGATE_CLIP_FUNC = lambda a:SURROGATE_CLIPPING_VALUE * (1. - a)  # clip range schedule function

# Architecture
ACTOR_ARCH_SPEC = GDKC(MultiDimensionalNormalMLP,
                       NOD(**{
                         'input_shape':            None,  # Obtain from environment
                         'hidden_layers':          None,
                         'hidden_layer_activation':torch.relu,
                         'output_shape':           None,  # Obtain from environment
                         }))

CRITIC_ARCH_SPEC = GDKC(MergedInputMLP,
                        NOD(**{
                          'input_shape':            None,  # Obtain from environment
                          'hidden_layers':          None,
                          'hidden_layer_activation':torch.relu,
                          'output_shape':           None,  # Obtain from environment
                          }))

ACTOR_OPTIMISER_SPEC = GDKC(constructor=torch.optim.Adam,
                            kwargs=NOD(lr=3e-4)
                            )

CRITIC_OPTIMISER_SPEC = GDKC(constructor=torch.optim.Adam,
                             kwargs=NOD(lr=3e-3,
                                        weight_decay=3e-2),
                             )

LR_FUNC = lambda a:CRITIC_OPTIMISER_SPEC.kwargs['lr'] * (1. - a)
