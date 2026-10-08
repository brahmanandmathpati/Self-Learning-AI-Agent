"""Learning safeguards.

DivergenceGuard stops training when Q-values or the loss explode.
RegressionMonitor flags (but does not stop) when evaluation drops well
below the best score for several evaluations in a row.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from sla.training.runner import Callback, EpisodeInfo, RunContext
from sla.utils.logging_setup import get_logger

log = get_logger(__name__)


def is_diverging(max_abs_q: float | None, loss: float | None, q_limit: float = 1e4) -> bool:
    """True if Q-values or loss are NaN/inf, or Q-values are absurdly large."""
    for value in (max_abs_q, loss):
        if value is not None and not math.isfinite(value):
            return True
    return max_abs_q is not None and max_abs_q > q_limit


def detect_regression(history: Sequence[float], drop_fraction: float = 0.2, patience: int = 3) -> bool:
    """True if the last ``patience`` scores are all below (1 - drop_fraction) * best earlier score."""
    if len(history) <= patience:
        return False
    best = max(history[:-patience])
    if best <= 0:
        return False
    limit = (1.0 - drop_fraction) * best
    return all(score < limit for score in history[-patience:])


class DivergenceGuard(Callback):
    def __init__(self, q_limit: float = 1e4) -> None:
        self.q_limit = q_limit

    def on_episode_end(self, ctx: RunContext, info: EpisodeInfo) -> bool:
        max_q = getattr(ctx.agent, "last_max_q", None)
        loss = getattr(ctx.agent, "last_loss", None)
        if is_diverging(max_q, loss, self.q_limit):
            ctx.extra["stop_reason"] = "divergence"
            log.error("Divergence at episode %d (max|Q|=%s, loss=%s); stopping", info.episode, max_q, loss)
            return True
        return False


class RegressionMonitor(Callback):
    """Must be listed after PeriodicEvalCallback so it sees the newest score."""

    def __init__(self, drop_fraction: float = 0.2, patience: int = 3) -> None:
        self.drop_fraction = drop_fraction
        self.patience = patience
        self._seen = 0

    def on_episode_end(self, ctx: RunContext, info: EpisodeInfo) -> bool:
        history = ctx.extra.get("eval_history", [])
        if len(history) == self._seen:
            return False
        self._seen = len(history)
        scores = [score for _, score in history]
        if detect_regression(scores, self.drop_fraction, self.patience):
            ctx.extra.setdefault("regression_flags", []).append(info.episode)
            log.warning("Regression flagged at episode %d (best checkpoint is kept)", info.episode)
        return False
