"""Compute grounded facts about a run from the database.

The LLM never computes numbers. It only receives these facts, and the grounding validator
checks that every number it writes appears here (within a small tolerance).
"""

from __future__ import annotations

import json
from typing import Any

from sla.database.store import Database
from sla.utils.errors import StoreError


def _r(value: Any, nd: int = 2) -> float | None:
    return None if value is None else round(float(value), nd)


def compute_facts(db: Database, run_id: str, window: int = 50) -> dict[str, Any]:
    run = db.get_run(run_id)
    if run is None:
        raise StoreError(f"Run {run_id!r} not found")
    episodes = db.query_episodes(run_id)
    if episodes.empty:
        raise StoreError(f"Run {run_id!r} has no training episodes (baseline runs cannot be reflected on)")
    window = max(1, min(window, len(episodes)))
    windows = []
    for start in range(0, len(episodes), window):
        chunk = episodes.iloc[start:start + window]
        reasons = chunk["end_reason"].value_counts()
        windows.append({
            "episodes": f"{start + 1}-{start + len(chunk)}",
            "mean_return": _r(chunk["total_reward"].mean()),
            "top_end_reason": str(reasons.index[0]) if not reasons.empty else "unknown",
        })
    first, last = windows[0]["mean_return"], windows[-1]["mean_return"]
    facts: dict[str, Any] = {
        "run_id": run_id,
        "env": run["env"],
        "agent": run["algorithm"],
        "seed": int(run["seed"]),
        "total_episodes": int(len(episodes)),
        "window": window,
        "first_window_mean": first,
        "last_window_mean": last,
        "change": _r(last - first),
        "best_window_mean": max(w["mean_return"] for w in windows),
        "mean_reward_all_episodes": _r(episodes["total_reward"].mean()),
        "best_episode_reward": _r(episodes["total_reward"].max()),
        "end_reasons": {str(k): int(v) for k, v in episodes["end_reason"].value_counts().items()},
        "windows": windows,
    }
    eps = episodes["epsilon"].dropna()
    if not eps.empty:
        facts["final_epsilon"] = _r(eps.iloc[-1])
    losses = episodes["mean_loss"].dropna()
    if not losses.empty:
        facts["last_window_mean_loss"] = _r(losses.tail(window).mean(), 4)
    vals = db.query_evaluations(run_id, "validation")
    if not vals.empty:
        best = vals.loc[vals["mean_return"].idxmax()]
        facts["best_validation_mean"] = _r(best["mean_return"])
        facts["best_validation_after_episode"] = int(best["episode"]) + 1
    initial = db.query_evaluations(run_id, "initial")
    if not initial.empty:
        facts["untrained_test_mean"] = _r(initial.iloc[-1]["mean_return"])
    test = db.query_evaluations(run_id, "test")
    if not test.empty:
        row = test.iloc[-1]
        facts["test_mean"] = _r(row["mean_return"])
        facts["test_std"] = _r(row["std_return"])
        facts["test_success_rate"] = _r(row["success_rate"])
        facts["test_episodes"] = int(row["n_episodes"])
    if run.get("experiment_id"):
        exp = db.get_experiment(int(run["experiment_id"]))
        summary = (exp or {}).get("summary") or {}
        if summary.get("baseline_test_means"):
            means = summary["baseline_test_means"]
            facts["random_baseline_mean"] = _r(sum(means) / len(means))
        cmp = summary.get("trained_vs_random")
        if cmp:
            facts["welch_p_value_vs_random"] = _r(cmp["p_value"], 4)
            facts["diff_vs_random_ci95"] = [_r(cmp["diff_ci_low"]), _r(cmp["diff_ci_high"])]
            facts["n_seeds"] = int(cmp["n_a"])
    return json.loads(json.dumps(facts))  # plain JSON types only
