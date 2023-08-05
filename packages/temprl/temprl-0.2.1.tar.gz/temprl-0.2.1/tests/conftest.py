# -*- coding: utf-8 -*-
"""This module contains the configurations for the tests."""
import logging
from enum import Enum
from typing import Optional

import gym
import numpy as np
from gym.spaces import Discrete, MultiDiscrete

logger = logging.getLogger(__name__)
logging.getLogger("temprl").setLevel(level=logging.INFO)


class GymTestEnv(gym.Env):
    """
    A class that implements a simple Gym environment.

    It is a chain-like environment:
    - the state space is the set of cells in a row;
    - the action space is {LEFT, RIGHT, NOP}.
    - a reward signal +1 is given if the right-most state is reached.
    - a reward signal -1 is given if an illegal move is done
      (i.e. LEFT in the left-most state of the chain).
    - the game ends when a time limit is reached or the agent reaches the right-most state.
    """

    class Action(Enum):
        """An enum to describe the available actions."""

        LEFT = -1
        NOP = 0
        RIGHT = 1

    def __init__(self, n_states: int = 2):
        """Initialize the Gym test environment."""
        assert n_states >= 2
        self._current_state = 0
        self._last_action = None  # type: Optional[int]
        self.n_states = n_states
        self.max_steps = self.n_states * 10

        self.observation_space = Discrete(self.n_states)
        self.actions = {self.Action.LEFT.value, self.Action.NOP.value, self.Action.RIGHT.value}
        self.action_space = Discrete(len(self.actions))
        self.counter = 0

    def step(self, action: int):
        """Do a step in the environment."""
        self.counter += 1
        action -= 1
        self._last_action = action
        reward = 0
        assert action in self.actions
        if self._current_state + action < 0:
            self._current_state = 0
            reward = -1
        elif self._current_state + action >= self.n_states:
            self._current_state = self.n_states - 1
            reward = -1
        else:
            self._current_state += action

        if self._current_state == self.n_states - 1:
            done = True
            reward = 1
        elif self.counter >= self.max_steps:
            done = True
        else:
            done = False

        return self._current_state, reward, done, {}

    def reset(self):
        """Reset the Gym env."""
        self._current_state = 0
        self.counter = 0
        self._last_action = None
        return self._current_state

    def render(self, mode='human'):
        """Render the current state of the environment."""
        print("Current state={}, action={}".format(self._current_state, self._last_action))


class GymTestObsWrapper(gym.ObservationWrapper):
    """
    This class is an observation wrapper for the GymTestEnv.

    It just makes the observation space an instance of MultiDiscrete
    rather than Discrete.
    """

    def __init__(self, n_states: int = 2):
        """Initialize the wrapper."""
        super().__init__(GymTestEnv(n_states))

        self.observation_space = MultiDiscrete((self.env.observation_space.n, ))

    def observation(self, observation):
        """Wrap the observation."""
        return np.asarray([observation])
