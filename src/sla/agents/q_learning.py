"""Tabular Q-learning.

Q-table: one row per state, one column per action. Each value is the agent's
estimate of the total future reward for taking that action in that state.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from sla.agents.base import Agent, Transition
from sla.agents.schedules import LinearSchedule
from sla.utils.io_helpers import ensure_dir, read_json, write_json


def q_learning_update(q: np.ndarray, s: int, a: int, r: float, s_next: int, terminated: bool,
                      alpha: float, gamma: float) -> float:
    """Apply one Bellman update in place and return the TD error.

    target   = r                          if the episode really ended (terminated)
             = r + gamma * max_a' Q[s', a'] otherwise (including time-limit truncation)
    Q[s, a] += alpha * (target - Q[s, a])
    """
    target = r if terminated else r + gamma * float(np.max(q[s_next]))
    td_error = target - float(q[s, a])
    q[s, a] += alpha * td_error
    return td_error


class QLearningAgent(Agent):
    name = "q_learning"

    def __init__(self, n_states: int, n_actions: int, learning_rate: float = 0.1, gamma: float = 0.99,
                 epsilon_schedule: LinearSchedule | None = None, seed: int = 0) -> None:
        self.n_states = n_states
        self.n_actions = n_actions
        self.alpha = learning_rate
        self.gamma = gamma
        self.schedule = epsilon_schedule or LinearSchedule(1.0, 0.05, 10_000)
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.q = np.zeros((n_states, n_actions), dtype=np.float64)
        self.steps = 0

    @property
    def epsilon(self) -> float:
        return self.schedule.value(self.steps)

    def greedy_action(self, state: int) -> int:
        row = self.q[int(state)]
        best = np.flatnonzero(row == row.max())  # break ties randomly (all zeros at the start)
        return int(self.rng.choice(best))

    def act(self, obs: Any, explore: bool = True) -> int:
        if explore and self.rng.random() < self.epsilon:
            return int(self.rng.integers(self.n_actions))
        return self.greedy_action(int(obs))

    def update(self, transition: Transition) -> dict[str, float]:
        td = q_learning_update(self.q, int(transition.state), transition.action, transition.reward,
                               int(transition.next_state), transition.terminated, self.alpha, self.gamma)
        self.steps += 1
        return {"td_error": td}

    def save(self, path: Path) -> None:
        folder = ensure_dir(path)
        np.save(folder / "q_table.npy", self.q)
        write_json(folder / "meta.json", {
            "agent": self.name, "n_states": self.n_states, "n_actions": self.n_actions,
            "learning_rate": self.alpha, "gamma": self.gamma, "seed": self.seed, "steps": self.steps,
            "schedule": {"start": self.schedule.start, "end": self.schedule.end, "duration": self.schedule.duration},
            "rng_state": self.rng.bit_generator.state,
        })

    @classmethod
    def load(cls, path: Path) -> QLearningAgent:
        folder = Path(path)
        meta = read_json(folder / "meta.json")
        agent = cls(meta["n_states"], meta["n_actions"], meta["learning_rate"], meta["gamma"],
                    LinearSchedule(**meta["schedule"]), meta["seed"])
        agent.q = np.load(folder / "q_table.npy")
        agent.steps = meta["steps"]
        agent.rng.bit_generator.state = meta["rng_state"]
        return agent
