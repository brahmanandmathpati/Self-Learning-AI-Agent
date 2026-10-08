import numpy as np
import pytest

torch = pytest.importorskip("torch")

from sla.agents.base import Transition  # noqa: E402
from sla.agents.dqn import DQNAgent, compute_td_target  # noqa: E402
from sla.agents.networks import QNetwork  # noqa: E402
from sla.memory.replay_buffer import Batch  # noqa: E402
from sla.training.config import DQNConfig  # noqa: E402

pytestmark = pytest.mark.torch


def test_td_target_hand_calculation():
    r = np.array([1.0, 1.0])
    next_max = np.array([10.0, 10.0])
    term = np.array([0.0, 1.0])  # second transition really ended
    assert np.allclose(compute_td_target(r, next_max, term, 0.9), [10.0, 1.0])


def test_network_output_shape():
    net = QNetwork(4, 2, 16)
    assert net(torch.zeros(5, 4)).shape == (5, 2)


def make_batch(n=32):
    rng = np.random.default_rng(0)
    return Batch(rng.normal(size=(n, 4)).astype(np.float32), rng.integers(0, 2, n).astype(np.int64),
                 np.ones(n, dtype=np.float32), rng.normal(size=(n, 4)).astype(np.float32),
                 np.zeros(n, dtype=np.float32))


def test_loss_decreases_on_fixed_batch():
    # Frozen target network => a fixed regression problem, so the loss must fall.
    agent = DQNAgent(4, 2, DQNConfig(hidden_size=32, target_update_every=10_000), learning_rate=1e-3, seed=0)
    batch = make_batch()
    first = agent.train_step(batch)
    for _ in range(100):
        last = agent.train_step(batch)
    assert last < first


def test_target_net_frozen_between_syncs():
    cfg = DQNConfig(hidden_size=16, batch_size=8, learning_starts=8, target_update_every=500)
    agent = DQNAgent(4, 2, cfg, seed=0)
    before = [p.clone() for p in agent.target.parameters()]
    for i in range(499):
        agent.update(Transition(np.zeros(4), i % 2, 1.0, np.ones(4), False, False))
    assert all(torch.equal(a, b) for a, b in zip(before, agent.target.parameters()))
    agent.update(Transition(np.zeros(4), 0, 1.0, np.ones(4), False, False))  # step 500 -> sync
    assert all(torch.equal(a, b) for a, b in zip(agent.online.parameters(), agent.target.parameters()))


def test_save_load_same_greedy_actions(tmp_path):
    agent = DQNAgent(4, 2, DQNConfig(hidden_size=16), seed=0)
    agent.train_step(make_batch())
    agent.save(tmp_path / "d")
    clone = DQNAgent.load(tmp_path / "d")
    states = np.random.default_rng(1).normal(size=(100, 4))
    assert [agent.act(s, explore=False) for s in states] == [clone.act(s, explore=False) for s in states]
