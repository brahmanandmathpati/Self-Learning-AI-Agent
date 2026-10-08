"""Readable training summaries."""

from __future__ import annotations

from collections.abc import Sequence


def rolling_mean(values: Sequence[float], window: int) -> list[float]:
    """Mean of the last ``window`` values at each position (shorter at the start)."""
    if window <= 0:
        raise ValueError("window must be > 0")
    out: list[float] = []
    total = 0.0
    for i, v in enumerate(values):
        total += float(v)
        if i >= window:
            total -= float(values[i - window])
        out.append(total / min(i + 1, window))
    return out


def format_episode_summary(episode: int, returns: Sequence[float], window: int = 50,
                           epsilon: float | None = None) -> str:
    """One line such as: 'Episode   100 | return   23.0 | mean(50)   18.4 | eps 0.62'."""
    if not returns:
        raise ValueError("returns must not be empty")
    mean = rolling_mean(returns, window)[-1]
    line = f"Episode {episode:>5} | return {returns[-1]:>7.1f} | mean({window}) {mean:>7.2f}"
    if epsilon is not None:
        line += f" | eps {epsilon:.2f}"
    return line
