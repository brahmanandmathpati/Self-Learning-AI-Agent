"""Learning-curve plots.

Uses matplotlib's object-oriented Figure API (no pyplot), so it works the same
in scripts, tests and Streamlit without opening windows.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.figure import Figure

from sla.utils.summary import rolling_mean


def plot_learning_curve(df: pd.DataFrame, window: int = 50, title: str = "Learning curve",
                        out_path: str | Path | None = None) -> Figure:
    """Plot reward per episode (faint) and its rolling mean (bold).

    ``df`` needs the columns 'episode' and 'total_reward' (as returned by
    EpisodeStore.query_episodes).
    """
    if df.empty or not {"episode", "total_reward"} <= set(df.columns):
        raise ValueError("df must contain non-empty 'episode' and 'total_reward' columns")
    fig = Figure(figsize=(8, 4.5))
    ax = fig.subplots()
    ax.plot(df["episode"], df["total_reward"], alpha=0.3, label="reward per episode")
    ax.plot(df["episode"], rolling_mean(df["total_reward"].tolist(), window), linewidth=2,
            label=f"rolling mean ({window})")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Total reward")
    ax.set_title(title)
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    if out_path is not None:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=120)
    return fig


def plot_seed_band(curves: dict[int, pd.DataFrame], window: int = 50, title: str = "Learning curve (all seeds)",
                   out_path: str | Path | None = None) -> Figure:
    """Mean rolling reward across seeds with a min–max band."""
    if not curves:
        raise ValueError("curves must not be empty")
    length = min(len(df) for df in curves.values())
    if length == 0:
        raise ValueError("every curve needs at least one episode")
    smoothed = np.array([rolling_mean(df["total_reward"].tolist()[:length], window) for df in curves.values()])
    x = np.arange(length)
    fig = Figure(figsize=(8, 4.5))
    ax = fig.subplots()
    ax.plot(x, smoothed.mean(axis=0), linewidth=2, label=f"mean over {len(curves)} seeds")
    ax.fill_between(x, smoothed.min(axis=0), smoothed.max(axis=0), alpha=0.25, label="min–max")
    ax.set_xlabel("Episode")
    ax.set_ylabel(f"Rolling mean reward ({window})")
    ax.set_title(title)
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    if out_path is not None:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=120)
    return fig


def plot_eval_curve(evals: pd.DataFrame, title: str = "Frozen-policy evaluation",
                    out_path: str | Path | None = None) -> Figure:
    """Evaluation mean ± std at each checkpoint (columns from EpisodeStore.query_evals)."""
    if evals.empty:
        raise ValueError("evals is empty")
    fig = Figure(figsize=(8, 4.5))
    ax = fig.subplots()
    ax.errorbar(evals["checkpoint_episode"], evals["mean_return"], yerr=evals["std_return"],
                marker="o", capsize=3)
    ax.set_xlabel("Training episode")
    ax.set_ylabel("Mean evaluation return")
    ax.set_title(title)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    if out_path is not None:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=120)
    return fig
