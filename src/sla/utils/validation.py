"""Input and transition validation.

Run-request helpers (seeds, env names, episode counts, safe names) and
transition validation used during training.
"""

from __future__ import annotations

import math
import re
from collections.abc import Iterable
from typing import Any

import numpy as np

from sla.training.config import ALLOWED_ENVS
from sla.utils.errors import ValidationError

MAX_EPISODES = 100_000
_SAFE_NAME = re.compile(r"[^A-Za-z0-9_-]+")


def validate_seeds(seeds: Iterable[Any]) -> list[int]:
    """Return seeds as a list of unique non-negative ints, keeping their order."""
    result: list[int] = []
    for seed in seeds:
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise ValidationError(f"Seed must be an integer, got {seed!r}")
        if seed < 0:
            raise ValidationError(f"Seed must be >= 0, got {seed}")
        if seed not in result:
            result.append(seed)
    if not result:
        raise ValidationError("At least one seed is required")
    return result


def validate_env_name(name: str) -> str:
    """Accept only the environments this project supports."""
    if name not in ALLOWED_ENVS:
        raise ValidationError(f"Unsupported environment {name!r}. Choose one of {ALLOWED_ENVS}")
    return name


def validate_episode_count(episodes: Any) -> int:
    """Episodes must be an int between 1 and MAX_EPISODES."""
    if isinstance(episodes, bool) or not isinstance(episodes, int):
        raise ValidationError(f"Episodes must be an integer, got {episodes!r}")
    if not 1 <= episodes <= MAX_EPISODES:
        raise ValidationError(f"Episodes must be between 1 and {MAX_EPISODES}, got {episodes}")
    return episodes


def safe_run_name(name: str, max_length: int = 60) -> str:
    """Turn any text into a safe folder name: letters, digits, '_' and '-' only."""
    cleaned = _SAFE_NAME.sub("_", name.strip()).strip("_")
    if not cleaned:
        raise ValidationError("Run name is empty after removing unsafe characters")
    return cleaned[:max_length]


def _is_finite_array(value: Any) -> bool:
    arr = np.asarray(value, dtype=np.float64)
    return bool(np.all(np.isfinite(arr)))


def validate_transition(state: Any, action: Any, reward: Any, next_state: Any,
                        action_space: Any, reward_range: tuple[float, float] | None = None) -> None:
    """Raise ValidationError if a transition looks corrupted.

    Checks: states contain only finite numbers, the action is inside the action
    space, and the reward is a finite number inside ``reward_range`` (if given).
    """
    if not _is_finite_array(state):
        raise ValidationError(f"State contains NaN or infinity: {state!r}")
    if not _is_finite_array(next_state):
        raise ValidationError(f"Next state contains NaN or infinity: {next_state!r}")
    if not action_space.contains(action):
        raise ValidationError(f"Action {action!r} is not inside the action space {action_space}")
    if isinstance(reward, bool) or not isinstance(reward, (int, float, np.floating, np.integer)):
        raise ValidationError(f"Reward must be a number, got {reward!r}")
    if not math.isfinite(float(reward)):
        raise ValidationError(f"Reward is NaN or infinite: {reward!r}")
    if reward_range is not None:
        low, high = reward_range
        if not low <= float(reward) <= high:
            raise ValidationError(f"Reward {reward} is outside the expected range [{low}, {high}]")


# Expected reward per step for each environment (used by the runner callback).
REWARD_RANGES: dict[str, tuple[float, float]] = {
    "FrozenLake-v1": (0.0, 1.0),
    "CartPole-v1": (0.0, 1.0),
}


class TransitionValidationCallback:
    """Runner callback that validates every transition (see sla.training.runner.Callback)."""

    def __init__(self, env_name: str) -> None:
        self.reward_range = REWARD_RANGES.get(env_name)
        self.checked = 0

    def on_run_start(self, ctx: Any) -> None:
        self.checked = 0

    def on_step(self, ctx: Any, transition: Any) -> None:
        validate_transition(transition.state, transition.action, transition.reward,
                            transition.next_state, ctx.env.action_space, self.reward_range)
        self.checked += 1

    def on_episode_end(self, ctx: Any, info: Any) -> bool:
        return False

    def on_run_end(self, ctx: Any, result: Any) -> None:
        return None
