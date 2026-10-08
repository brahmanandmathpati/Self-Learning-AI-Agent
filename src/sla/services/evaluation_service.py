"""Evaluate stored checkpoints and compute statistics (no training happens here)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sla.checkpoints.manager import load_checkpoint, resolve_checkpoint
from sla.database.store import Database
from sla.evaluation.evaluate import TEST_SEED_BASE, EvalResult, evaluate_agent
from sla.evaluation.stats import bootstrap_ci, compare_groups
from sla.training.config import load_config
from sla.utils.errors import CheckpointError


class EvaluationService:
    def __init__(self, db: Database) -> None:
        self.db = db

    def evaluate_run(self, run_dir: str | Path, checkpoint: str = "best", episodes: int = 100,
                     record: bool = True) -> tuple[EvalResult, Path]:
        """Frozen-policy evaluation (epsilon = 0, no updates) of a run's checkpoint on the test seeds."""
        run_dir = Path(run_dir)
        if not (run_dir / "config.yaml").is_file():
            raise CheckpointError(f"{run_dir} is not a run folder (config.yaml missing)")
        cfg = load_config(run_dir / "config.yaml")
        folder = resolve_checkpoint(run_dir, checkpoint)
        agent, info = load_checkpoint(folder)
        res = evaluate_agent(agent, cfg.env_name, cfg.env_kwargs, episodes, seed_base=TEST_SEED_BASE,
                             max_steps=cfg.max_steps_per_episode)
        if record and self.db.get_run(run_dir.name) is not None:
            self.db.log_evaluation(run_dir.name, "test", res, episode=int(info["episode"]),
                                   seed_base=TEST_SEED_BASE, checkpoint=str(folder))
        return res, folder

    @staticmethod
    def compare(trained: list[float], baseline: list[float]) -> dict[str, Any]:
        return compare_groups(trained, baseline, "trained", "random")

    @staticmethod
    def mean_ci(values: list[float]) -> tuple[float, float]:
        return bootstrap_ci(values)
