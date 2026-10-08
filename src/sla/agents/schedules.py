"""Exploration schedules."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LinearSchedule:
    """Goes from ``start`` to ``end`` in a straight line over ``duration`` steps, then stays at ``end``."""

    start: float
    end: float
    duration: int

    def __post_init__(self) -> None:
        if self.duration <= 0:
            raise ValueError("duration must be > 0")

    def value(self, step: int) -> float:
        fraction = min(max(step, 0) / self.duration, 1.0)
        return self.start + fraction * (self.end - self.start)
