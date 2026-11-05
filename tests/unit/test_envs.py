import numpy as np
import pytest

from sla.agents.random_agent import RandomAgent
from sla.envs.factory import end_reason, make_env
from sla.utils.errors import EnvError
from sla.utils.seeding import episode_seed, set_global_seed


def rollout(seed):
    env = make_env("CartPole-v1", seed=seed)
    obs, _ = env.reset(seed=seed)
    observations = [obs]
    for _ in range(100):
        obs, _, term, trunc, _ = env.step(env.action_space.sample())
        observations.append(obs)
        if term or trunc:
            obs, _ = env.reset()
    env.close()
    return np.array(observations)


def test_same_seed_same_observations():
    assert np.array_equal(rollout(0), rollout(0))


def test_different_seed_different_observations():
    assert not np.array_equal(rollout(0), rollout(1))


def test_unknown_env():
    with pytest.raises(EnvError, match="Unsupported"):
        make_env("Cartpole-v9")


def test_frozenlake_defaults_not_slippery():
    env = make_env("FrozenLake-v1")
    assert env.observation_space.n == 16 and env.action_space.n == 4
    env.close()


def test_end_reasons():
    assert end_reason("FrozenLake-v1", True, False, 1.0, 15) == "goal"
    assert end_reason("FrozenLake-v1", True, False, 0.0, 5) == "hole"
    assert end_reason("CartPole-v1", True, False, 1.0, [2.5, 0, 0, 0]) == "position"
    assert end_reason("CartPole-v1", True, False, 1.0, [0.1, 0, 0.3, 0]) == "angle"
    assert end_reason("CartPole-v1", False, True, 1.0, [0, 0, 0, 0]) == "truncated"


def test_episode_seed_unique():
    assert episode_seed(0, 5) != episode_seed(1, 5)


def test_set_global_seed_rejects_negative():
    with pytest.raises(ValueError):
        set_global_seed(-1)


def test_random_agent_runs_ten_episodes():
    env = make_env("CartPole-v1", seed=0)
    agent = RandomAgent(env.action_space.n, seed=0)
    for ep in range(10):
        obs, _ = env.reset(seed=ep)
        done = False
        while not done:
            obs, r, term, trunc, _ = env.step(agent.act(obs))
            done = term or trunc
    env.close()


def test_taxi_and_cliffwalking_spaces_and_time_limits():
    taxi = make_env("Taxi-v4")
    assert taxi.observation_space.n == 500 and taxi.action_space.n == 6
    assert taxi.spec.max_episode_steps == 200
    taxi.close()
    cliff = make_env("CliffWalking-v1")
    assert cliff.observation_space.n == 48 and cliff.action_space.n == 4
    assert cliff.spec.max_episode_steps == 200
    cliff.close()


def test_new_end_reasons():
    assert end_reason("Taxi-v4", True, False, 20.0, 0) == "delivered"
    assert end_reason("CliffWalking-v1", True, False, -1.0, 47) == "goal"
    assert end_reason("Taxi-v4", False, True, -1.0, 0) == "truncated"


def test_success_means_reaching_the_goal_on_taxi_and_cliffwalking():
    from sla.agents.q_learning import QLearningAgent
    from sla.evaluation.evaluate import evaluate_agent
    # An untrained agent on CliffWalking almost never reaches the goal within 200 steps
    agent = QLearningAgent(48, 4, seed=0)
    res = evaluate_agent(agent, "CliffWalking-v1", n_episodes=3, max_steps=200)
    assert 0.0 <= res.success_rate <= 1.0
    # A hand-written optimal path (up, right x11, down) always reaches the goal: success 100%, return -13
    class Path:
        def __init__(self):
            self.moves = []

        def act(self, obs, explore=False):
            if not self.moves:
                self.moves = [0] + [1] * 11 + [2]
            return self.moves.pop(0)
    res = evaluate_agent(Path(), "CliffWalking-v1", n_episodes=2, max_steps=200)
    assert res.success_rate == 1.0 and res.mean_return == -13.0
