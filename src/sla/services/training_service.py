"""Write-side service: start, resume and stop training from the CLI or the dashboard."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

from sla import settings
from sla.database.store import Database
from sla.training.config import RunConfig, load_config, validate_config
from sla.training.pipeline import ExperimentOutcome, RunOutcome, resume_run, run_baseline, run_experiment, train_run

PRESETS: dict[tuple[str, str], str] = {
    ("FrozenLake-v1", "q_learning"): "frozenlake_qlearning.yaml",
    ("FrozenLake-v1", "random"): "frozenlake_random.yaml",
    ("CartPole-v1", "dqn"): "cartpole_dqn.yaml",
    ("CartPole-v1", "random"): "cartpole_random.yaml",
}


class TrainingService:
    def __init__(self, db: Database) -> None:
        self.db = db

    @staticmethod
    def algorithms_for(env_name: str) -> list[str]:
        return [algo for (env, algo) in PRESETS if env == env_name and algo != "random"]

    @staticmethod
    def preset(env_name: str, algorithm: str) -> RunConfig:
        try:
            name = PRESETS[(env_name, algorithm)]
        except KeyError as exc:
            raise ValueError(f"No preset config for {algorithm} on {env_name}") from exc
        cfg = load_config(settings.config_dir() / name)
        return replace(cfg, run_root=str(settings.run_root()))

    def train(self, cfg: RunConfig, final_eval_episodes: int = 100, progress: Any = None) -> RunOutcome:
        return train_run(validate_config(cfg), self.db, final_eval_episodes, progress=progress)

    def experiment(self, cfg: RunConfig, seeds: list[int], final_eval_episodes: int = 100,
                   with_baseline: bool = True, progress: Any = None) -> ExperimentOutcome:
        return run_experiment(validate_config(cfg), seeds, self.db, final_eval_episodes, with_baseline, progress)

    def resume(self, run_dir: str | Path, final_eval_episodes: int = 100, progress: Any = None) -> RunOutcome:
        return resume_run(run_dir, self.db, final_eval_episodes, progress)

    def baseline(self, cfg: RunConfig, seeds: list[int], n_episodes: int = 100):
        return run_baseline(cfg, seeds, self.db, n_episodes)
