import math

import numpy as np
import pytest
from gymnasium.spaces import Discrete

from sla.utils.errors import ValidationError
from sla.utils.validation import (
    safe_run_name,
    validate_env_name,
    validate_episode_count,
    validate_seeds,
    validate_transition,
)


def test_seeds_deduplicated_in_order():
    assert validate_seeds([3, 1, 3, 0]) == [3, 1, 0]


@pytest.mark.parametrize("bad", [[], [-1], [1.5], [True], ["2"]])
def test_bad_seeds(bad):
    with pytest.raises(ValidationError):
        validate_seeds(bad)


def test_env_name():
    assert validate_env_name("CartPole-v1") == "CartPole-v1"
    with pytest.raises(ValidationError):
        validate_env_name("cartpole")


@pytest.mark.parametrize("bad", [0, -5, 100_001, 2.0, "10", None])
def test_bad_episode_counts(bad):
    with pytest.raises(ValidationError):
        validate_episode_count(bad)


def test_safe_run_name():
    assert safe_run_name("../../etc/passwd") == "etc_passwd"
    assert safe_run_name("My run #1") == "My_run_1"
    with pytest.raises(ValidationError):
        safe_run_name("///")




SPACE = Discrete(2)


def test_valid_transition_passes():
    validate_transition(np.zeros(4), 1, 1.0, np.ones(4), SPACE, (0.0, 1.0))


@pytest.mark.parametrize("state,action,reward,next_state", [
    (np.array([0, math.nan, 0, 0]), 0, 1.0, np.zeros(4)),
    (np.zeros(4), 0, 1.0, np.array([math.inf, 0, 0, 0])),
    (np.zeros(4), 5, 1.0, np.zeros(4)),
    (np.zeros(4), 0, math.nan, np.zeros(4)),
    (np.zeros(4), 0, "1", np.zeros(4)),
    (np.zeros(4), 0, 7.0, np.zeros(4)),
])
def test_bad_transitions_rejected(state, action, reward, next_state):
    with pytest.raises(ValidationError):
        validate_transition(state, action, reward, next_state, SPACE, (0.0, 1.0))
