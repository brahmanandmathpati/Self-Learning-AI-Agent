import numpy as np
import pytest

from sla.agents.base import Transition
from sla.agents.q_learning import QLearningAgent, q_learning_update
from sla.agents.schedules import LinearSchedule


def test_update_matches_hand_calculation():
    # Worked example from docs/q_learning_by_hand.md: alpha=0.5, gamma=0.9, r=0, Q[s'] best = 1.0
    q = np.zeros((2, 2))
    q[1] = [0.0, 1.0]
    td = q_learning_update(q, s=0, a=1, r=0.0, s_next=1, terminated=False, alpha=0.5, gamma=0.9)
    assert td == pytest.approx(0.9)
    assert q[0, 1] == pytest.approx(0.45)


def test_terminal_does_not_bootstrap():
    q = np.zeros((2, 2))
    q[1] = [5.0, 5.0]
    q_learning_update(q, 0, 0, r=1.0, s_next=1, terminated=True, alpha=1.0, gamma=0.9)
    assert q[0, 0] == pytest.approx(1.0)


def test_greedy_picks_best_action():
    agent = QLearningAgent(4, 3, epsilon_schedule=LinearSchedule(0.0, 0.0, 1))
    agent.q[2] = [0.1, 0.9, 0.3]
    assert agent.act(2, explore=False) == 1


def test_update_increments_steps_and_epsilon_decays():
    agent = QLearningAgent(4, 2, epsilon_schedule=LinearSchedule(1.0, 0.0, 10))
    for _ in range(5):
        agent.update(Transition(0, 0, 0.0, 1, False, False))
    assert agent.steps == 5 and agent.epsilon == pytest.approx(0.5)


def test_save_load_same_q_and_actions(tmp_path):
    agent = QLearningAgent(16, 4, seed=3)
    agent.q = np.random.default_rng(0).random((16, 4))
    agent.save(tmp_path / "q")
    clone = QLearningAgent.load(tmp_path / "q")
    assert np.array_equal(agent.q, clone.q)
    assert [agent.act(s, explore=False) for s in range(16)] == [clone.act(s, explore=False) for s in range(16)]
