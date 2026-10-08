"""The Agent interface every agent implements.

Every agent implements this interface. Do not change signatures without a team
decision, because the runner, checkpoints and evaluator depend on them.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Transition:
    """One step of experience: what the agent saw, did and got."""

    state: Any
    action: int
    reward: float
    next_state: Any
    terminated: bool
    truncated: bool


class Agent(ABC):
    """Base class for RandomAgent, QLearningAgent and DQNAgent."""

    name: str = "base"

    @abstractmethod
    def act(self, obs: Any, explore: bool = True) -> int:
        """Choose an action. explore=False means greedy (used for evaluation)."""

    def update(self, transition: Transition) -> dict[str, float]:
        """Learn from one transition. Returns stats such as {"loss": 0.12}."""
        return {}

    def end_episode(self) -> None:
        """Called by the runner after every episode (optional hook)."""
        return None

    @property
    def epsilon(self) -> float | None:
        """Current exploration rate, or None if the agent does not explore."""
        return None

    @abstractmethod
    def save(self, path: Path) -> None:
        """Save everything needed to continue later into the folder ``path``."""

    @classmethod
    @abstractmethod
    def load(cls, path: Path) -> Agent:
        """Re-create an agent from a folder written by ``save``."""
