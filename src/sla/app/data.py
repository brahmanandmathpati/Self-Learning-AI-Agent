"""Cached, read-only data access for the dashboard.

Every cached function takes a ``version`` token built from cheap row counts, so the cache is reused across
Streamlit reruns and refreshed automatically as soon as a run, episode, evaluation or note is written.
Cached values are copies (``st.cache_data``), so pages may modify them freely.
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from sla import settings
from sla.app.state import services

TTL = 120  # seconds; the version token handles freshness, the TTL only bounds memory


def version() -> tuple[int, ...]:
    """Cheap change token (COUNT(*) of the main tables). Empty tuple if the database is unavailable."""
    try:
        return tuple(services().db.counts().values())
    except Exception:  # noqa: BLE001 - the caller shows a friendly error state
        return ()


def _db() -> str:
    return str(settings.db_path())


@st.cache_data(ttl=TTL, show_spinner=False)
def _overview(db: str, ver: tuple) -> dict[str, Any]:
    return services().experiments.overview()


@st.cache_data(ttl=TTL, show_spinner=False)
def _runs(db: str, ver: tuple) -> pd.DataFrame:
    return services().experiments.runs()


@st.cache_data(ttl=TTL, show_spinner=False)
def _trained_runs(db: str, ver: tuple) -> pd.DataFrame:
    return services().experiments.trained_runs()


@st.cache_data(ttl=TTL, show_spinner=False, max_entries=64)
def _episodes(db: str, ver: tuple, run_id: str) -> pd.DataFrame:
    return services().db.query_episodes(run_id)


@st.cache_data(ttl=TTL, show_spinner=False, max_entries=32)
def _run_detail(db: str, ver: tuple, run_id: str) -> dict[str, Any] | None:
    return services().experiments.run_detail(run_id)


@st.cache_data(ttl=TTL, show_spinner=False)
def _comparison(db: str, ver: tuple) -> tuple[pd.DataFrame, pd.DataFrame]:
    exp = services().experiments
    return exp.comparison_table(), exp.test_results()


@st.cache_data(ttl=TTL, show_spinner=False)
def _experiments(db: str, ver: tuple, kind: str | None) -> pd.DataFrame:
    return services().experiments.experiments(kind)


@st.cache_data(ttl=TTL, show_spinner=False, max_entries=32)
def _experiment(db: str, ver: tuple, exp_id: int) -> dict[str, Any] | None:
    return services().experiments.experiment(exp_id)


@st.cache_data(ttl=TTL, show_spinner=False, max_entries=16)
def _ablation(db: str, ver: tuple, exp_id: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    return services().experiments.ablation(exp_id)


@st.cache_data(ttl=TTL, show_spinner=False)
def _evaluations(db: str, ver: tuple, kind: str | None) -> pd.DataFrame:
    return services().db.query_evaluations(kind=kind)


def overview() -> dict[str, Any]:
    return _overview(_db(), version())


def runs() -> pd.DataFrame:
    return _runs(_db(), version())


def trained_runs() -> pd.DataFrame:
    return _trained_runs(_db(), version())


def episodes(run_id: str) -> pd.DataFrame:
    return _episodes(_db(), version(), run_id)


def run_detail(run_id: str) -> dict[str, Any] | None:
    return _run_detail(_db(), version(), run_id)


def comparison() -> tuple[pd.DataFrame, pd.DataFrame]:
    return _comparison(_db(), version())


def experiments(kind: str | None = None) -> pd.DataFrame:
    return _experiments(_db(), version(), kind)


def experiment(exp_id: int) -> dict[str, Any] | None:
    return _experiment(_db(), version(), int(exp_id))


def ablation(exp_id: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    return _ablation(_db(), version(), int(exp_id))


def evaluations(kind: str | None = None) -> pd.DataFrame:
    return _evaluations(_db(), version(), kind)


def learning_trend(ep: pd.DataFrame) -> tuple[str, str] | None:
    """Training-reward trend from real episodes: first 20% vs last 20% (needs >= 20 episodes).

    Returns (state, text) with state in {"improving", "flat", "declining"}; this describes the training
    curve only - proof of learning comes from the frozen-policy evaluation.
    """
    if ep is None or len(ep) < 20:
        return None
    k = max(5, len(ep) // 5)
    first, last = float(ep["total_reward"].head(k).mean()), float(ep["total_reward"].tail(k).mean())
    scale = max(abs(first), abs(last), 1e-9)
    change = last - first
    if change > 0.05 * scale:
        state = "improving"
    elif change < -0.05 * scale:
        state = "declining"
    else:
        state = "flat"
    return state, f"avg reward {first:,.2f} (first {k} episodes) → {last:,.2f} (last {k})"
