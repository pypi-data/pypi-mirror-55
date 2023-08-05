#!/usr/local/bin/python
# coding: utf-8
from typing import Any

import numpy
from torch import nn
from torch.utils.data import DataLoader

from draugr.torch_utilities.to_tensor import to_tensor
from draugr.writers import MockWriter
from draugr.writers.writer import Writer
from neodroid.environments.unity_environment.vector_unity_environment import VectorUnityEnvironment
from neodroid.utilities.unity_specifications import EnvironmentSnapshot
from neodroidagent.agents.torch_agents.model_free.actor_critic import ActorCriticAgent
from neodroidagent.utilities.signal.advantage_estimation import torch_compute_gae
from neodroidagent.utilities.signal.experimental.discounting import discount_signal
from neodroidagent.utilities.specifications import AdvantageDiscountedTransition, ValuedTransition
from neodroidagent.utilities.training.mini_batch_iter import AdvDisDataset

__author__ = 'Christian Heider Nielsen'

import torch
from tqdm import tqdm
import torch.nn.functional as F


class PPOAgent(ActorCriticAgent):
  '''
  PPO, Proximal Policy Optimization method


'''

  # region Private

  def __init__(self,
               discount_factor=0.95,
               gae_tau=0.15,
               actor_lr=4e-4,
               critic_lr=4e-4,
               entropy_reg_coef=1e-2,
               value_reg_coef=5e-1,
               mini_batches=32,
               copy_percentage=1.0,
               update_target_interval=1000,
               max_grad_norm=0.5,
               solved_threshold=-200,
               test_interval=1000,
               early_stop=False,
               rollouts=10000,
               surrogate_clipping_value=3e-1,
               ppo_optimisation_epochs=6,
               state_type=torch.float,
               value_type=torch.float,
               action_type=torch.long,
               exploration_epsilon_start=0.99,
               exploration_epsilon_end=0.05,
               exploration_epsilon_decay=10000,
               **kwargs) -> None:
    '''

    :param discount_factor:
    :param gae_tau:
    :param actor_lr:
    :param critic_lr:
    :param entropy_reg_coef:
    :param value_reg_coef:
    :param mini_batches:
    :param copy_percentage:
    :param update_target_interval:
    :param max_grad_norm:
    :param solved_threshold:
    :param test_interval:
    :param early_stop:
    :param rollouts:
    :param surrogate_clipping_value:
    :param ppo_optimisation_epochs:
    :param state_type:
    :param value_type:
    :param action_type:
    :param exploration_epsilon_start:
    :param exploration_epsilon_end:
    :param exploration_epsilon_decay:
    :param kwargs:
    '''
    super().__init__(**kwargs)

    self._discount_factor = discount_factor
    self._gae_tau = gae_tau
    # self._reached_horizon_penalty = -10.
    self._actor_lr = actor_lr
    self._critic_lr = critic_lr
    self._entropy_reg_coef = entropy_reg_coef
    self._value_reg_coef = value_reg_coef
    self._mini_batches = mini_batches
    self._target_update_tau = copy_percentage
    self._update_target_interval = update_target_interval
    self._max_grad_norm = max_grad_norm
    self._solved_threshold = solved_threshold
    self._test_interval = test_interval
    self._early_stop = early_stop
    self._rollouts = rollouts
    self._surrogate_clipping_value = surrogate_clipping_value
    self._ppo_optimisation_epochs = ppo_optimisation_epochs
    self._state_type = state_type
    self._value_type = value_type
    self._action_type = action_type
    # TODO: ExplorationSpec
    # params for epsilon greedy
    self._exploration_epsilon_start = exploration_epsilon_start
    self._exploration_epsilon_end = exploration_epsilon_end
    self._exploration_epsilon_decay = exploration_epsilon_decay

    (self._actor,
     self._target_actor,
     self._critic,
     self._target_critic,
     self._actor_optimiser,
     self._critic_optimiser) = None, None, None, None, None, None

  # endregion

  # region Protected

  def _optimise(self, cost, **kwargs):

    self._actor_optimiser.zero_grad()
    self._critic_optimiser.zero_grad()
    cost.backward(retain_graph=True)

    if self._max_grad_norm is not None:
      nn.utils.clip_grad_norm(self._actor.parameters(), self._max_grad_norm)
      nn.utils.clip_grad_norm(self._critic.parameters(), self._max_grad_norm)

    self._actor_optimiser.step()
    self._critic_optimiser.step()

  def _sample_model(self, state, *args, **kwargs):
    '''
      continuous
        randomly sample from normal distribution, whose mean and variance come from policy network.
        [batch, action_size]

      :param state:
      :type state:
      :param continuous:
      :type continuous:
      :param kwargs:
      :type kwargs:
      :return:
      :rtype:
    '''

    model_input = to_tensor(state,
                            device=self._device,
                            dtype=self._state_type)

    distribution = self._actor(model_input)

    with torch.no_grad():
      action = distribution.sample().detach().to('cpu').numpy()

    value_estimate = self._critic(model_input, action)

    action_log_prob = distribution.log_prob(action)

    return (action,
            action_log_prob,
            value_estimate,
            distribution)

  def _update_targets(self) -> None:
    self._update_target(target_model=self._target_actor,
                        source_model=self._actor,
                        copy_percentage=self._target_update_tau)

    self._update_target(target_model=self._target_critic,
                        source_model=self._critic,
                        copy_percentage=self._target_update_tau)

  def _update(self,
              transitions=None,
              *args,
              metric_writer: Writer = MockWriter(),
              **kwargs) -> None:

    adv_trans = self.back_trace_advantages(transitions)
    dataset = AdvDisDataset(adv_trans)
    loader = DataLoader(dataset,
                        batch_size=len(dataset) // self._mini_batches,
                        shuffle=True)
    for i in range(self._ppo_optimisation_epochs):
      for mini_batch in loader:
        loss, new_log_probs, old_log_probs = self.evaluate(mini_batch)
        self._optimise(loss)

    if self._update_i % self._update_target_interval == 0:
      self._update_targets()

  # endregion

  # region Public

  def take_n_steps(self,
                   initial_state: EnvironmentSnapshot,
                   environment: VectorUnityEnvironment,
                   n: int = 100,
                   *,
                   train: bool = False,
                   **kwargs) -> Any:
    state = initial_state.observables

    accumulated_signal = []

    snapshot = None
    transitions = []
    terminated = False
    T = tqdm(range(1, n + 1),
             f'Step #{self._sample_i} - {0}/{n}',
             leave=False)
    for t in T:
      # T.set_description(f'Step #{self._step_i} - {t}/{n}')
      self._sample_i += 1
      action, action_prob, value_estimates, *_ = self.sample(state)

      snapshot = environment.react(action)

      successor_state, signal, terminated = (snapshot.observables, snapshot.signal, snapshot.terminated)

      transitions.append(ValuedTransition(state,
                                          action,
                                          action_prob,
                                          value_estimates,
                                          signal,
                                          successor_state,
                                          terminated,
                                          )
                         )

      state = successor_state

      accumulated_signal += signal

      if numpy.array(terminated).all():
        # TODO: support individual reset of environments vector
        snapshot = environment.reset()
        state, signal, terminated = (snapshot.observables, snapshot.signal, snapshot.terminated)

    return transitions, accumulated_signal, terminated, snapshot

  def back_trace_advantages(self, transitions):

    value_estimates = to_tensor(transitions.value_estimate, device=self._device)
    sig = to_tensor(transitions.signal)
    value_estimates = value_estimates.view(value_estimates.shape[0], -1)

    advantages = torch_compute_gae(signals=sig,
                                   values=value_estimates,
                                   non_terminals=transitions.non_terminal,
                                   discount_factor=self._discount_factor,
                                   tau=self._gae_tau
                                   )

    discounted_signal = discount_signal(sig.transpose(0, 1).detach().to('cpu').numpy(),
                                        self._discount_factor).transpose()

    i = 0
    advantage_memories = []
    for step in zip(*transitions):
      step = ValuedTransition(*step)
      advantage_memories.append(AdvantageDiscountedTransition(step.state,
                                                              step.action,
                                                              step.successor_state,
                                                              step.terminal,
                                                              step.action_prob,
                                                              value_estimates,
                                                              discounted_signal[i],
                                                              advantages[i]
                                                              )
                                )
      i += 1

    return AdvantageDiscountedTransition(*zip(*advantage_memories))

  def evaluate(self,
               batch: AdvantageDiscountedTransition,
               discrete: bool = False,
               **kwargs):
    # region Tensorise

    states = to_tensor(batch.state, device=self._device)
    value_estimates = to_tensor(batch.value_estimate, device=self._device)
    advantages = to_tensor(batch.advantage, device=self._device)
    discounted_returns = to_tensor(batch.discounted_return, device=self._device)
    action_log_probs_old = to_tensor(batch.action_prob, device=self._device)

    # endregion

    *_, action_log_probs_new, distribution = self._sample_model(states)

    if discrete:
      actions = to_tensor(batch.action, device=self._device)
      action_log_probs_old = action_log_probs_old.gather(-1, actions)
      action_log_probs_new = action_log_probs_new.gather(-1, actions)

    ratio = (action_log_probs_new - action_log_probs_old).exp()
    # Generated action probs from (new policy) and (old policy).
    # Values of [0..1] means that actions less likely with the new policy,
    # while values [>1] mean action a more likely now
    surrogate = ratio * advantages
    clamped_ratio = torch.clamp(ratio,
                                min=1. - self._surrogate_clipping_value,
                                max=1. + self._surrogate_clipping_value)
    surrogate_clipped = clamped_ratio * advantages  # (L^CLIP)

    policy_loss = torch.min(surrogate, surrogate_clipped).mean()
    entropy_loss = distribution.entropy().mean() * self._entropy_reg_coef
    policy_loss -= entropy_loss

    value_error = F.mse_loss(value_estimates, discounted_returns) * self._value_reg_coef
    collective_cost = policy_loss + value_error

    return collective_cost, policy_loss, value_error,

  # endregion


# region Test
def ppo_test(rollouts=None, skip: bool = True):
  from neodroidagent.sessions.session_entry_point import session_entry_point
  from neodroidagent.procedures.training import StepWise
  from neodroidagent.sessions.single_agent.parallel import ParallelSession
  import neodroidagent.configs.agent_test_configs.ppo_test_config as C

  if rollouts:
    C.ROLLOUTS = rollouts

  session_entry_point(PPOAgent,
                      C,
                      session=ParallelSession(
                        StepWise,
                        environment=C.ENVIRONMENT_NAME,
                        auto_reset_on_terminal_state=True),
                      parse_args=False,
                      skip_confirmation=skip)


def ppo_run(rollouts=None, skip: bool = True):
  from neodroidagent.sessions.session_entry_point import session_entry_point
  from neodroidagent.procedures.training.step_wise import StepWise
  from neodroidagent.sessions.single_agent.parallel import ParallelSession
  import neodroidagent.configs.agent_test_configs.ppo_test_config as C

  if rollouts:
    C.ROLLOUTS = rollouts

  session_entry_point(PPOAgent,
                      C,
                      session=ParallelSession(
                        StepWise,
                        auto_reset_on_terminal_state=True, connect_to_running=True),
                      parse_args=False,
                      skip_confirmation=skip)


if __name__ == '__main__':
  ppo_test()
# ppo_run()

# endregion
