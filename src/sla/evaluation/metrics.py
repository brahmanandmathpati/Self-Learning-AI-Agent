"""Metrics computed from lists of episode returns."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def summarize(returns: Sequence[float]) -> dict[str, float]:
    arr = np.asarray(returns, dtype=np.float64)
    if arr.size == 0:
        raise ValueError("returns must not be empty")
    return {"mean": float(arr.mean()), "std": float(arr.std()), "median": float(np.median(arr)),
            "min": float(arr.min()), "max": float(arr.max()), "n": int(arr.size)}


def success_rate(returns: Sequence[float], threshold: float) -> float:
    """Share of episodes whose return reached ``threshold``."""
    arr = np.asarray(returns, dtype=np.float64)
    if arr.size == 0:
        raise ValueError("returns must not be empty")
    return float(np.mean(arr >= threshold))


def episodes_to_threshold(returns: Sequence[float], threshold: float, window: int = 20) -> int | None:
    """First episode index at which the rolling mean (over ``window``) reaches ``threshold``; None if never."""
    arr = np.asarray(returns, dtype=np.float64)
    if window <= 0:
        raise ValueError("window must be > 0")
    if arr.size < window:
        return None
    rolling = np.convolve(arr, np.ones(window) / window, mode="valid")
    hits = np.flatnonzero(rolling >= threshold)
    return int(hits[0] + window - 1) if hits.size else None


def first_last_fraction(returns: Sequence[float], fraction: float = 0.05) -> tuple[float, float]:
    """Mean return of the first and the last ``fraction`` of episodes (at least one episode each)."""
    arr = np.asarray(returns, dtype=np.float64)
    if arr.size == 0:
        raise ValueError("returns must not be empty")
    if not 0 < fraction <= 0.5:
        raise ValueError("fraction must be in (0, 0.5]")
    k = max(1, int(round(arr.size * fraction)))
    return float(arr[:k].mean()), float(arr[-k:].mean())


def area_under_curve(returns: Sequence[float]) -> float:
    """Average return over all training episodes: higher means faster and better learning."""
    arr = np.asarray(returns, dtype=np.float64)
    if arr.size == 0:
        raise ValueError("returns must not be empty")
    return float(arr.mean())
