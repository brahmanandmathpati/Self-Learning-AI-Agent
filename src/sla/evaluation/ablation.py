"""Ablation study: remove one part of the DQN and measure the effect.

Variants: full DQN, no replay (learn only from the newest transition),
no target network (bootstrap from the online network).
"""

from __future__ import annotations

import copy
from dataclasses import replace
from typing import Any

import pandas as pd

from sla.training.config import RunConfig, validate_config

VARIANTS: dict[str, dict[str, Any]] = {
    "full": {"replay_enabled": True, "target_net_enabled": True},
    "no_replay": {"replay_enabled": False, "target_net_enabled": True},
    "no_target": {"replay_enabled": True, "target_net_enabled": False},
}


def make_variant_config(base: RunConfig, variant: str, seed: int) -> RunConfig:
    if variant not in VARIANTS:
        raise ValueError(f"Unknown variant {variant!r}; choose from {sorted(VARIANTS)}")
    if base.agent != "dqn":
        raise ValueError("Ablation is only defined for the DQN agent")
    cfg = copy.deepcopy(base)
    cfg.dqn = replace(cfg.dqn, **VARIANTS[variant])
    cfg.seed = seed
    return validate_config(cfg)


def run_ablation(base: RunConfig, seeds: list[int], db: Any, variants: list[str] | None = None,
                 final_eval_episodes: int = 100, progress: Any = None) -> tuple[int, pd.DataFrame, pd.DataFrame]:
    """Train every variant on every seed with the standard pipeline and store the results.

    Returns (experiment_id, per-run table, statistics table comparing 'full' with each other variant).
    """
    from sla.training.pipeline import git_sha, train_run

    variants = variants or list(VARIANTS)
    exp_id = db.create_experiment(f"DQN ablation on {base.env_name}", "ablation", base.env_name, base.agent,
                                  base.to_dict(), list(seeds), git_sha())
    rows = []
    try:
        for variant in variants:
            for seed in seeds:
                cfg = make_variant_config(base, variant, seed)
                out = train_run(cfg, db, final_eval_episodes, exp_id, variant=variant, progress=progress,
                                initial_eval=False)
                db.log_ablation(exp_id, variant, seed, out.run_id, out.final_eval.mean_return,
                                out.final_eval.std_return, out.final_eval.success_rate)
                rows.append({"variant": variant, "seed": seed, "run_id": out.run_id,
                             "final_mean": out.final_eval.mean_return, "final_std": out.final_eval.std_return,
                             "success_rate": out.final_eval.success_rate})
        df = pd.DataFrame(rows)
        summary = ablation_statistics(df)
        db.finish_experiment(exp_id, "completed", {"comparisons": summary.to_dict(orient="records")})
    except BaseException as exc:
        db.finish_experiment(exp_id, "failed" if isinstance(exc, Exception) else "stopped")
        raise
    return exp_id, df, summary


def ablation_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Welch t-test and bootstrap CI of 'full' against every other variant (needs >= 2 seeds per group)."""
    from sla.evaluation.stats import compare_groups
    rows = []
    if df.empty or "full" not in set(df["variant"]):
        return pd.DataFrame(rows)
    full = df.loc[df["variant"] == "full", "final_mean"].tolist()
    for variant in [v for v in df["variant"].unique() if v != "full"]:
        other = df.loc[df["variant"] == variant, "final_mean"].tolist()
        if len(full) >= 2 and len(other) >= 2:
            rows.append({"comparison": f"full vs {variant}", **compare_groups(full, other, "full", variant)})
    return pd.DataFrame(rows)
