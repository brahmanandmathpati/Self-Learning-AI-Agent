"""Safety limits for training.

They stop runaway runs: too many steps, too much time, or broken numbers.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass

from sla.utils.errors import TrainingError


@dataclass
class SafetyLimits:
    max_steps_per_episode: int = 500
    max_episodes: int = 100_000
    max_wall_clock_s: float = 3_600.0

    @classmethod
    def from_config(cls, cfg) -> SafetyLimits:
        return cls(cfg.max_steps_per_episode, cfg.episodes, cfg.max_wall_clock_s)

    def wall_clock_exceeded(self, start_time: float) -> bool:
        return (time.monotonic() - start_time) > self.max_wall_clock_s

    def step_limit_reached(self, steps: int) -> bool:
        return steps >= self.max_steps_per_episode


def check_finite(value: float, name: str) -> float:
    """Raise TrainingError if ``value`` is NaN or infinite (e.g. a broken reward or loss)."""
    if not math.isfinite(float(value)):
        raise TrainingError(f"{name} is not a finite number: {value!r}")
    return float(value)
