#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import torch

from neodroidagent.architectures import SingleHeadMLP
from neodroidagent.architectures.experimental.merged import SingleHeadMergedInputMLP
from neodroidagent.memory import TransitionBuffer
from neodroidagent.utilities.exploration import OrnsteinUhlenbeckProcess
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
ENVIRONMENT_NAME = 'Pendulum-v0'

# Optimiser
OPTIMISER_TYPE = torch.optim.Adam
OPTIMISER_LEARNING_RATE = 0.00025
OPTIMISER_WEIGHT_DECAY = 1e-5
OPTIMISER_ALPHA = 0.95
DISCOUNT_FACTOR = 0.95
TARGET_UPDATE_TAU = 3e-3
RENDER_FREQUENCY = 5
RENDER_ENVIRONMENT = True

STATE_TYPE = torch.float
VALUE_TYPE = torch.float
ACTION_TYPE = torch.float

EVALUATION_FUNCTION = F.smooth_l1_loss

BATCH_SIZE = 64

ACTOR_OPTIMISER_SPEC = GDKC(constructor=OPTIMISER_TYPE,
                            kwargs=dict(lr=3e-4)
                            )

CRITIC_OPTIMISER_SPEC = GDKC(constructor=OPTIMISER_TYPE,
                             kwargs=dict(lr=3e-3,
                                         weight_decay=0.01),
                             )

RANDOM_PROCESS_THETA = 0.15
RANDOM_PROCESS_SIGMA = 0.2
RANDOM_PROCESS = GDKC(constructor=OrnsteinUhlenbeckProcess,
                      kwargs=dict(theta=RANDOM_PROCESS_THETA,
                                  sigma=RANDOM_PROCESS_SIGMA)
                      )

MEMORY = TransitionBuffer(REPLAY_MEMORY_SIZE)

ACTION_CLIPPING = False
SIGNAL_CLIPPING = False

ROLLOUTS = 1000

# Architecture
ACTOR_ARCH_SPEC = GDKC(SingleHeadMLP,
                       NOD(**{
                         'input_shape':      None,  # Obtain from environment
                         # 'hidden_layers' : [256],
                         'output_activation':torch.tanh,
                         'output_shape':     None,  # Obtain from environment
                         }))

CRITIC_ARCH_SPEC = GDKC(SingleHeadMergedInputMLP,
                        NOD(**{
                          'input_shape': None,  # Obtain from environment
                          # 'hidden_layers' : [256],
                          'output_shape':None,  # Obtain from environment
                          }))
