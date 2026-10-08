"""Shared pytest fixtures."""

import pytest

from sla.database.store import Database
from sla.training.config import config_from_dict


@pytest.fixture
def fl_cfg(tmp_path):
    """A small FrozenLake Q-learning config that trains in about a second."""
    return config_from_dict({
        "env_name": "FrozenLake-v1", "env_kwargs": {"is_slippery": False}, "agent": "q_learning",
        "episodes": 300, "seed": 0, "learning_rate": 0.5, "gamma": 0.95, "epsilon_decay_steps": 1500,
        "max_steps_per_episode": 100, "eval_every": 100, "eval_episodes": 5, "checkpoint_every": 100,
        "run_root": str(tmp_path / "runs"),
    })


@pytest.fixture
def db(tmp_path):
    """A fresh SQLite database in a temporary folder."""
    return Database(tmp_path / "test.db")


@pytest.fixture(autouse=True)
def _isolated_paths(tmp_path, monkeypatch):
    """Never let a test touch the real runs/ folder or database."""
    monkeypatch.setenv("SLA_DB", str(tmp_path / "env.db"))
    monkeypatch.setenv("SLA_RUN_ROOT", str(tmp_path / "runs"))
