"""SARSA and Expected SARSA: update rules, the 'next action is really played' rule, save/load, configs."""

import numpy as np
import pytest

from sla.agents.base import Transition
from sla.agents.sarsa import ExpectedSarsaAgent, SarsaAgent, epsilon_greedy_probs, expected_sarsa_update, sarsa_update
from sla.agents.schedules import LinearSchedule
from sla.training.config import config_from_dict
from sla.utils.errors import ConfigError


def test_sarsa_update_uses_the_chosen_next_action():
    q = np.zeros((3, 2))
    q[1] = [10.0, 2.0]
    td = sarsa_update(q, 0, 0, -1.0, 1, 1, False, alpha=0.5, gamma=0.9)
    # target = -1 + 0.9 * Q[1, 1] = 0.8  (not the max 10.0 that Q-learning would use)
    assert td == pytest.approx(0.8)
    assert q[0, 0] == pytest.approx(0.4)


def test_sarsa_update_does_not_bootstrap_at_terminal():
    q = np.full((2, 2), 5.0)
    sarsa_update(q, 0, 1, 1.0, 1, 0, True, alpha=1.0, gamma=0.9)
    assert q[0, 1] == pytest.approx(1.0)


def test_epsilon_greedy_probs_sum_to_one_and_share_ties():
    p = epsilon_greedy_probs(np.array([1.0, 3.0, 3.0, 0.0]), 0.2)
    assert p.sum() == pytest.approx(1.0)
    assert p[1] == pytest.approx(0.05 + 0.4) and p[2] == pytest.approx(0.05 + 0.4) and p[0] == pytest.approx(0.05)


def test_expected_sarsa_update_worked_example():
    q = np.zeros((2, 2))
    q[1] = [4.0, 0.0]
    # epsilon 0.5: P(best) = 0.25 + 0.5 = 0.75, P(other) = 0.25 -> expected value = 0.75 * 4 = 3
    td = expected_sarsa_update(q, 0, 1, 1.0, 1, False, alpha=1.0, gamma=1.0, epsilon=0.5)
    assert td == pytest.approx(4.0)
    assert q[0, 1] == pytest.approx(4.0)


def test_expected_sarsa_with_zero_epsilon_equals_q_learning_target():
    q = np.zeros((2, 3))
    q[1] = [1.0, 7.0, 2.0]
    expected_sarsa_update(q, 0, 0, 0.0, 1, False, alpha=1.0, gamma=1.0, epsilon=0.0)
    assert q[0, 0] == pytest.approx(7.0)


def test_sarsa_plays_the_action_it_planned():
    agent = SarsaAgent(4, 3, 0.5, 0.9, LinearSchedule(0.5, 0.5, 1), seed=3)
    for _ in range(50):
        agent.update(Transition(0, 1, -1.0, 2, False, False))
        planned = agent._next
        assert planned is not None and planned[0] == 2
        assert agent.act(2, explore=True) == planned[1]
        assert agent._next is None


def test_sarsa_clears_the_plan_at_episode_end_and_on_truncation():
    agent = SarsaAgent(4, 2, seed=0)
    agent.update(Transition(0, 0, 0.0, 1, False, True))
    assert agent._next is None
    agent.update(Transition(0, 0, 0.0, 1, False, False))
    agent.end_episode()
    assert agent._next is None


def test_greedy_evaluation_ignores_the_plan():
    agent = SarsaAgent(3, 2, seed=0)
    agent.q[1] = [0.0, 5.0]
    agent._next = (1, 0)
    assert agent.act(1, explore=False) == 1


@pytest.mark.parametrize("cls", [SarsaAgent, ExpectedSarsaAgent])
def test_save_and_load_keep_the_table(tmp_path, cls):
    agent = cls(5, 2, 0.3, 0.95, LinearSchedule(1.0, 0.1, 100), seed=7)
    for i in range(20):
        agent.update(Transition(i % 5, i % 2, 1.0, (i + 1) % 5, i % 4 == 3, False))
    agent.save(tmp_path / "a")
    back = cls.load(tmp_path / "a")
    assert back.name == cls.name and back.steps == agent.steps
    assert np.array_equal(back.q, agent.q)


@pytest.mark.parametrize("agent", ["sarsa", "expected_sarsa", "q_learning"])
def test_tabular_agents_are_rejected_on_cartpole(agent):
    with pytest.raises(ConfigError, match="countable states"):
        config_from_dict({"env_name": "CartPole-v1", "agent": agent})


def test_dqn_is_rejected_on_a_grid_game():
    with pytest.raises(ConfigError, match="dqn"):
        config_from_dict({"env_name": "Taxi-v4", "agent": "dqn"})
