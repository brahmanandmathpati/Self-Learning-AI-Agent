"""Experience replay buffer.

A fixed-size circular memory of transitions. When it is full, the oldest
transition is overwritten. ``sample`` returns a random mini-batch so the DQN
learns from a mix of old and new experience (Lin, 1992; Mnih et al., 2015).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, NamedTuple

import numpy as np


class Batch(NamedTuple):
    states: np.ndarray       # shape (B, obs_dim), float32
    actions: np.ndarray      # shape (B,), int64
    rewards: np.ndarray      # shape (B,), float32
    next_states: np.ndarray  # shape (B, obs_dim), float32
    terminated: np.ndarray   # shape (B,), float32 (1.0 = episode really ended)


class ReplayBuffer:
    def __init__(self, capacity: int, obs_dim: int, seed: int = 0) -> None:
        if capacity <= 0 or obs_dim <= 0:
            raise ValueError("capacity and obs_dim must be > 0")
        self.capacity = capacity
        self.obs_dim = obs_dim
        self.rng = np.random.default_rng(seed)
        self.states = np.zeros((capacity, obs_dim), dtype=np.float32)
        self.actions = np.zeros(capacity, dtype=np.int64)
        self.rewards = np.zeros(capacity, dtype=np.float32)
        self.next_states = np.zeros((capacity, obs_dim), dtype=np.float32)
        self.terminated = np.zeros(capacity, dtype=np.float32)
        self.pos = 0   # where the next transition will be written
        self.size = 0  # how many slots are filled

    def __len__(self) -> int:
        return self.size

    def push(self, state: Any, action: int, reward: float, next_state: Any, terminated: bool) -> None:
        i = self.pos
        self.states[i] = np.asarray(state, dtype=np.float32).reshape(self.obs_dim)
        self.actions[i] = int(action)
        self.rewards[i] = float(reward)
        self.next_states[i] = np.asarray(next_state, dtype=np.float32).reshape(self.obs_dim)
        self.terminated[i] = 1.0 if terminated else 0.0
        self.pos = (self.pos + 1) % self.capacity
        self.size = min(self.size + 1, self.capacity)

    def sample(self, batch_size: int) -> Batch:
        if self.size == 0:
            raise ValueError("Cannot sample from an empty buffer")
        if batch_size > self.size:
            raise ValueError(f"batch_size {batch_size} is larger than buffer size {self.size}")
        idx = self.rng.choice(self.size, size=batch_size, replace=False)
        return Batch(self.states[idx], self.actions[idx], self.rewards[idx],
                     self.next_states[idx], self.terminated[idx])

    def latest(self) -> Batch:
        """The most recent transition as a batch of one (used by the no-replay ablation)."""
        if self.size == 0:
            raise ValueError("Buffer is empty")
        i = (self.pos - 1) % self.capacity
        idx = np.array([i])
        return Batch(self.states[idx], self.actions[idx], self.rewards[idx],
                     self.next_states[idx], self.terminated[idx])

    def save(self, path: str | Path) -> None:
        np.savez_compressed(path, states=self.states[: self.size], actions=self.actions[: self.size],
                            rewards=self.rewards[: self.size], next_states=self.next_states[: self.size],
                            terminated=self.terminated[: self.size],
                            meta=np.array([self.capacity, self.obs_dim, self.pos, self.size]))

    def load_from(self, path: str | Path) -> None:
        data = np.load(path)
        capacity, obs_dim, pos, size = (int(v) for v in data["meta"])
        if capacity != self.capacity or obs_dim != self.obs_dim:
            raise ValueError("Saved buffer has a different capacity or obs_dim")
        self.states[:size] = data["states"]
        self.actions[:size] = data["actions"]
        self.rewards[:size] = data["rewards"]
        self.next_states[:size] = data["next_states"]
        self.terminated[:size] = data["terminated"]
        self.pos, self.size = pos, size
