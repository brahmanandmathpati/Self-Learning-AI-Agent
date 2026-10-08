"""Evaluation must never learn and must be repeatable."""

import numpy as np

from sla.agents.q_learning import QLearningAgent
from sla.agents.random_agent import RandomAgent
from sla.evaluation.evaluate import EVAL_SEED_BASE, TEST_SEED_BASE, evaluate_agent
from sla.utils.seeding import episode_seed


def test_evaluation_does_not_change_q_table():
    agent = QLearningAgent(16, 4, seed=0)
    agent.q[:] = np.random.default_rng(0).random(agent.q.shape)
    before = agent.q.copy()
    rng_state = agent.rng.bit_generator.state
    res = evaluate_agent(agent, "FrozenLake-v1", {"is_slippery": False}, 10)
    assert np.array_equal(before, agent.q) and agent.steps == 0  # no update() was called
    assert agent.rng.bit_generator.state == rng_state           # not even the exploration RNG moved
    assert len(res.lengths) == 10 and res.median_return in (0.0, 1.0)


def test_random_baseline_repeatable():
    a = evaluate_agent(RandomAgent(2, seed=0), "CartPole-v1", n_episodes=10)
    b = evaluate_agent(RandomAgent(2, seed=0), "CartPole-v1", n_episodes=10)
    assert a.returns == b.returns and a.n_episodes == 10


def test_success_rate_frozenlake_perfect_policy():
    class GoRightDown:
        """Right, right, down, down, down, right reaches the goal on the 4x4 map without holes."""
        plan = [2, 2, 1, 1, 1, 2]

        def __init__(self):
            self.i = 0

        def act(self, obs, explore=True):
            a = self.plan[self.i % len(self.plan)]
            self.i += 1
            return a

    res = evaluate_agent(GoRightDown(), "FrozenLake-v1", {"is_slippery": False}, n_episodes=3)
    assert res.success_rate == 1.0 and res.mean_return == 1.0


def test_eval_and_test_seeds_never_overlap_training_seeds():
    largest_training_seed = episode_seed(99, 99_999)
    assert EVAL_SEED_BASE > largest_training_seed and TEST_SEED_BASE > EVAL_SEED_BASE + 1_000_000
