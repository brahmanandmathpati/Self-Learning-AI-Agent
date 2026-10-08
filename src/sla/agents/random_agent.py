"""Random agent: the "before learning" baseline."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from sla.agents.base import Agent
from sla.utils.io_helpers import ensure_dir, read_json, write_json


class RandomAgent(Agent):
    """Picks every action uniformly at random and never learns."""

    name = "random"

    def __init__(self, n_actions: int, seed: int = 0) -> None:
        if n_actions <= 0:
            raise ValueError("n_actions must be > 0")
        self.n_actions = n_actions
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def act(self, obs: Any, explore: bool = True) -> int:
        return int(self.rng.integers(self.n_actions))

    def save(self, path: Path) -> None:
        folder = ensure_dir(path)
        write_json(folder / "meta.json", {"agent": self.name, "n_actions": self.n_actions,
                                          "seed": self.seed, "rng_state": self.rng.bit_generator.state})

    @classmethod
    def load(cls, path: Path) -> RandomAgent:
        meta = read_json(Path(path) / "meta.json")
        agent = cls(meta["n_actions"], meta["seed"])
        agent.rng.bit_generator.state = meta["rng_state"]
        return agent
