import numpy as np
import pytest

from sla.memory.replay_buffer import ReplayBuffer


def fill(buf, n):
    for i in range(n):
        buf.push([i, i, i, i], i % 2, float(i), [i + 1] * 4, i % 5 == 0)


def test_wraps_around_after_capacity():
    buf = ReplayBuffer(10, 4)
    fill(buf, 15)
    assert len(buf) == 10
    assert set(buf.rewards.tolist()) == set(float(i) for i in range(5, 15))


def test_sample_shapes_and_dtypes():
    buf = ReplayBuffer(100, 4, seed=0)
    fill(buf, 50)
    b = buf.sample(32)
    assert b.states.shape == (32, 4) and b.states.dtype == np.float32
    assert b.actions.shape == (32,) and b.actions.dtype == np.int64
    assert b.terminated.dtype == np.float32


def test_seeded_sampling_repeats():
    a, b = ReplayBuffer(100, 4, seed=1), ReplayBuffer(100, 4, seed=1)
    fill(a, 60)
    fill(b, 60)
    assert np.array_equal(a.sample(16).rewards, b.sample(16).rewards)


def test_sample_errors():
    buf = ReplayBuffer(10, 4)
    with pytest.raises(ValueError):
        buf.sample(1)
    fill(buf, 3)
    with pytest.raises(ValueError):
        buf.sample(4)


def test_latest_is_newest():
    buf = ReplayBuffer(5, 4)
    fill(buf, 7)
    assert buf.latest().rewards[0] == 6.0


def test_save_and_load(tmp_path):
    buf = ReplayBuffer(20, 4, seed=0)
    fill(buf, 12)
    buf.save(tmp_path / "r.npz")
    other = ReplayBuffer(20, 4)
    other.load_from(tmp_path / "r.npz")
    assert len(other) == 12 and np.array_equal(other.states[:12], buf.states[:12])
