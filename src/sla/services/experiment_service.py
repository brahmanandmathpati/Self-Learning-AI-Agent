"""Read-side service: everything the dashboard and CLI need to inspect stored experiments."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from sla.database.store import Database


class ExperimentService:
    def __init__(self, db: Database) -> None:
        self.db = db

    # --------------------------------------------------------------- overview
    def overview(self) -> dict[str, Any]:
        """Headline numbers; every value is None when no data exists (the UI shows NOT RUN)."""
        counts = self.db.counts()
        runs = self.db.list_runs()
        trained = runs[runs["algorithm"] != "random"] if not runs.empty else runs
        latest = trained.iloc[0].to_dict() if not trained.empty else None
        test = self.db.query_evaluations(kind="test")
        test_trained = test[test["algorithm"] != "random"] if not test.empty else test
        latest_test = test_trained.iloc[-1] if not test_trained.empty else None
        episodes_total = counts["episodes"]
        best_reward = avg_reward = None
        if latest is not None:
            ep = self.db.query_episodes(latest["run_id"])
            if not ep.empty:
                best_reward = float(ep["total_reward"].max())
                avg_reward = float(ep["total_reward"].tail(50).mean())
        return {
            "experiments": counts["experiments"],
            "runs": counts["runs"],
            "completed_runs": int((runs["status"] == "completed").sum()) if not runs.empty else 0,
            "running_runs": int((runs["status"] == "running").sum()) if not runs.empty else 0,
            "failed_runs": int((runs["status"] == "failed").sum()) if not runs.empty else 0,
            "episodes_logged": episodes_total,
            "latest_run": latest,
            "latest_best_reward": best_reward,
            "latest_avg_reward_last50": avg_reward,
            "latest_test_mean": float(latest_test["mean_return"]) if latest_test is not None else None,
            "latest_test_label": (f"{latest_test['algorithm']} on {latest_test['env']}, seed {latest_test['seed']}"
                                  if latest_test is not None else None),
            "reflections": counts["reflections"],
        }

    # ------------------------------------------------------------------ runs
    def runs(self, include_baseline: bool = True) -> pd.DataFrame:
        runs = self.db.list_runs()
        if not include_baseline and not runs.empty:
            runs = runs[runs["variant"].fillna("") != "baseline"]
        return runs

    def trained_runs(self) -> pd.DataFrame:
        runs = self.db.list_runs()
        return runs[runs["episodes_completed"] > 0] if not runs.empty else runs

    def run_detail(self, run_id: str) -> dict[str, Any] | None:
        run = self.db.get_run(run_id)
        if run is None:
            return None
        log_tail = None
        if run.get("run_dir"):
            log_file = Path(run["run_dir"]) / "run.log"
            if log_file.is_file():
                log_tail = "\n".join(log_file.read_text(encoding="utf-8", errors="replace").splitlines()[-60:])
        return {"run": run, "episodes": self.db.query_episodes(run_id),
                "evaluations": self.db.query_evaluations(run_id), "metrics": self.db.query_metrics(run_id),
                "reflections": self.db.query_reflections(run_id), "log_tail": log_tail}

    # ------------------------------------------------------------ comparison
    def test_results(self, pipeline_only: bool = True) -> pd.DataFrame:
        """One row per run with a held-out test evaluation (latest per run), incl. random baselines.

        By default only runs that belong to a completed multi-seed experiment are used, so one-off demo runs
        and ablation variants do not change the headline comparison.
        """
        test = self.db.query_evaluations(kind="test")
        if test.empty:
            return test
        if pipeline_only:
            exps = self.db.list_experiments("pipeline")
            done = set(exps.loc[exps["status"] == "completed", "experiment_id"]) if not exps.empty else set()
            test = test[test["experiment_id"].isin(done)]
            if test.empty:
                return test
        test = test.sort_values("eval_id").groupby("run_id", as_index=False).last()
        test["label"] = test.apply(_label, axis=1)
        return test

    def comparison_table(self) -> pd.DataFrame:
        """Mean / std / n over seeds of the test means, per environment and agent label."""
        test = self.test_results()
        if test.empty:
            return test
        grouped = test.groupby(["env", "label"])["mean_return"]
        table = grouped.agg(mean="mean", std="std", n="count").reset_index()
        succ = test.groupby(["env", "label"])["success_rate"].mean().reset_index(name="success_rate")
        return table.merge(succ, on=["env", "label"])

    # ----------------------------------------------------------- experiments
    def experiments(self, kind: str | None = None) -> pd.DataFrame:
        return self.db.list_experiments(kind)

    def experiment(self, experiment_id: int) -> dict[str, Any] | None:
        exp = self.db.get_experiment(experiment_id)
        if exp is None:
            return None
        exp["runs"] = self.db.list_runs(experiment_id)
        return exp

    def ablation(self, experiment_id: int) -> tuple[pd.DataFrame, pd.DataFrame]:
        from sla.evaluation.ablation import ablation_statistics
        df = self.db.query_ablation(experiment_id)
        return df, ablation_statistics(df)

    def learning_curves(self, run_ids: list[str]) -> dict[str, pd.DataFrame]:
        return {rid: self.db.query_episodes(rid) for rid in run_ids}


def _label(row: pd.Series) -> str:
    if row["algorithm"] == "random":
        return "Random"
    name = {"q_learning": "Q-learning", "dqn": "DQN"}.get(row["algorithm"], row["algorithm"])
    variant = row.get("variant")
    if isinstance(variant, str) and variant and variant not in ("full", "baseline"):
        name += f" ({variant})"
    return name


def returns_of(row: pd.Series) -> list[float]:
    return json.loads(row["returns_json"] or "[]")
