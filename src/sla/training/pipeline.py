"""Training pipelines: one run, a resumed run, a random baseline and a multi-seed experiment.

Every entry point (CLI, scripts, services used by the dashboard) goes through these functions,
so all results are produced and stored the same way.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

from sla.checkpoints.manager import CheckpointCallback, best_checkpoint, load_checkpoint, resume_training
from sla.database.store import Database
from sla.evaluation.evaluate import EVAL_SEED_BASE, TEST_SEED_BASE, EvalResult, PeriodicEvalCallback, evaluate_agent
from sla.training.callbacks import DatabaseCallback, InitialEvalCallback, ProgressCallback
from sla.training.config import RunConfig, load_config
from sla.training.guards import DivergenceGuard, RegressionMonitor
from sla.training.runner import Callback, RunResult, make_run_id, run_training
from sla.utils.io_helpers import write_json
from sla.utils.logging_setup import get_logger
from sla.utils.validation import TransitionValidationCallback

log = get_logger(__name__)


def git_sha() -> str | None:
    """Short commit id of the code that produced a result (None outside a git repo)."""
    try:
        out = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True,
                             timeout=5, check=True)
        return out.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


@dataclass
class RunOutcome:
    """Everything one training run produced."""

    train: RunResult
    final_eval: EvalResult
    checkpoint: str
    initial_eval: EvalResult | None = None

    @property
    def run_id(self) -> str:
        return self.train.run_id


@dataclass
class ExperimentOutcome:
    experiment_id: int
    runs: list[RunOutcome] = field(default_factory=list)
    baseline: list[EvalResult] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)


def default_callbacks(cfg: RunConfig, db: Database, experiment_id: int | None = None, variant: str | None = None,
                      progress: Any = None, initial_eval_episodes: int | None = None) -> list[Callback]:
    """Standard plug-ins, in the order they must run."""
    callbacks: list[Callback] = [DatabaseCallback(db, git_sha(), experiment_id, variant)]
    if initial_eval_episodes:
        callbacks.append(InitialEvalCallback(db, initial_eval_episodes, TEST_SEED_BASE))
    callbacks += [
        TransitionValidationCallback(cfg.env_name),
        CheckpointCallback(cfg.checkpoint_every, db=db),
        PeriodicEvalCallback(cfg.eval_every, cfg.eval_episodes, db, EVAL_SEED_BASE),
        RegressionMonitor(),   # must come after PeriodicEvalCallback (reads the newest score)
        DivergenceGuard(),
    ]
    if progress is not None:
        callbacks.append(ProgressCallback(progress))
    return callbacks


def final_evaluation(run_dir: Path, cfg: RunConfig, db: Database, run_id: str,
                     n_episodes: int = 100) -> tuple[EvalResult, str]:
    """Evaluate the best checkpoint (validation-selected) on the held-out test seeds and store it."""
    folder = best_checkpoint(run_dir)
    agent, info = load_checkpoint(folder)
    result = evaluate_agent(agent, cfg.env_name, cfg.env_kwargs, n_episodes, seed_base=TEST_SEED_BASE,
                            max_steps=cfg.max_steps_per_episode)
    db.log_evaluation(run_id, "test", result, episode=int(info["episode"]), seed_base=TEST_SEED_BASE,
                      checkpoint=str(folder))
    for name in ("mean_return", "std_return", "median_return", "success_rate", "mean_length"):
        db.log_metric(run_id, f"test_{name}", float(getattr(result, name)))
    return result, str(folder)


def _finish(cfg: RunConfig, db: Database, train: RunResult, final_eval_episodes: int,
            initial: EvalResult | None) -> RunOutcome:
    final, used = final_evaluation(train.run_dir, cfg, db, train.run_id, final_eval_episodes)
    write_json(train.run_dir / "metrics.json", {
        "run_id": train.run_id, "env": cfg.env_name, "algorithm": cfg.agent, "seed": cfg.seed,
        "episodes_completed": train.episodes_completed, "stopped_reason": train.stopped_reason,
        "initial_eval": initial.to_dict() if initial else None,
        "final_eval": {**final.to_dict(), "checkpoint": used, "seed_base": TEST_SEED_BASE},
        "git_sha": git_sha(),
    })
    log.info("Run %s: final test mean %.2f ± %.2f", train.run_id, final.mean_return, final.std_return)
    return RunOutcome(train, final, used, initial)


def train_run(cfg: RunConfig, db: Database, final_eval_episodes: int = 100, experiment_id: int | None = None,
              variant: str | None = None, progress: Any = None, initial_eval: bool = True,
              run_id: str | None = None) -> RunOutcome:
    """Train one seed with all callbacks, then evaluate the best checkpoint on the test seeds."""
    run_id = run_id or make_run_id(cfg)
    if variant:
        run_id = f"{run_id}_{variant}"
    run_dir = Path(cfg.run_root) / run_id
    from sla.utils.logging_setup import setup_logging
    setup_logging(run_id, run_dir / "run.log")
    callbacks = default_callbacks(cfg, db, experiment_id, variant, progress,
                                  final_eval_episodes if initial_eval else None)
    try:
        train = run_training(cfg, callbacks, run_dir=run_dir, run_id=run_id)
        initial = next((cb for cb in callbacks if isinstance(cb, InitialEvalCallback)), None)
        return _finish(cfg, db, train, final_eval_episodes, initial.result if initial else None)
    except BaseException as exc:  # BaseException: also a Streamlit rerun/stop or Ctrl+C
        if db.get_run(run_id) is not None:
            _mark_interrupted(db, run_id, exc)
        raise


def resume_run(run_dir: str | Path, db: Database, final_eval_episodes: int = 100, progress: Any = None) -> RunOutcome:
    """Continue a run from its latest checkpoint (same run id), then re-run the final evaluation."""
    run_dir = Path(run_dir)
    cfg = load_config(run_dir / "config.yaml")
    existing = db.get_run(run_dir.name)
    callbacks = default_callbacks(cfg, db, existing["experiment_id"] if existing else None,
                                  existing["variant"] if existing else None, progress)
    try:
        train = resume_training(run_dir, callbacks)
        return _finish(cfg, db, train, final_eval_episodes, None)
    except BaseException as exc:
        if db.get_run(run_dir.name) is not None:
            _mark_interrupted(db, run_dir.name, exc)
        raise


def _mark_interrupted(db: Database, run_id: str, exc: BaseException) -> None:
    """Failed for errors; stopped (resumable from the latest checkpoint) for interrupts."""
    if isinstance(exc, Exception):
        db.finish_run(run_id, "failed", error=f"{type(exc).__name__}: {exc}")
    else:
        db.finish_run(run_id, "stopped", stopped_reason="interrupted")


def run_baseline(cfg: RunConfig, seeds: list[int], db: Database, n_episodes: int = 100,
                 experiment_id: int | None = None) -> list[EvalResult]:
    """Random-action baseline on the same held-out test seeds as the trained agents. Nothing is trained."""
    from sla.agents.random_agent import RandomAgent
    from sla.envs.factory import make_env
    env = make_env(cfg.env_name, **cfg.env_kwargs)
    n_actions = int(env.action_space.n)
    env.close()
    results = []
    sha = git_sha()
    for seed in seeds:
        base_cfg = replace(cfg, agent="random", seed=seed)
        run_id = f"{make_run_id(base_cfg)}_baseline"
        db.start_run(run_id, cfg.env_name, "random", seed, base_cfg.to_dict(), None, sha, experiment_id, "baseline")
        res = evaluate_agent(RandomAgent(n_actions, seed=seed), cfg.env_name, cfg.env_kwargs, n_episodes,
                             seed_base=TEST_SEED_BASE, max_steps=cfg.max_steps_per_episode)
        db.log_evaluation(run_id, "test", res, seed_base=TEST_SEED_BASE)
        db.finish_run(run_id, "completed", 0, "baseline")
        results.append(res)
    return results


def summarize_experiment(trained: list[float], baseline: list[float], initial: list[float]) -> dict[str, Any]:
    """Statistics comparing trained agents with the random baseline and with their own untrained start."""
    from sla.evaluation.stats import bootstrap_ci, compare_groups
    summary: dict[str, Any] = {"n_seeds": len(trained), "trained_test_means": trained,
                               "baseline_test_means": baseline, "initial_test_means": initial}
    if len(trained) >= 2:
        low, high = bootstrap_ci(trained)
        summary["trained_mean_ci95"] = [low, high]
    if len(trained) >= 2 and len(baseline) >= 2:
        summary["trained_vs_random"] = compare_groups(trained, baseline, "trained", "random")
    if len(trained) >= 2 and len(initial) >= 2:
        summary["trained_vs_untrained"] = compare_groups(trained, initial, "trained", "untrained")
    return summary


def run_experiment(cfg: RunConfig, seeds: list[int], db: Database, final_eval_episodes: int = 100,
                   with_baseline: bool = True, progress: Any = None, name: str | None = None) -> ExperimentOutcome:
    """Train every seed, evaluate on test seeds, run the random baseline and store the statistics."""
    exp_id = db.create_experiment(name or f"{cfg.agent} on {cfg.env_name}", "pipeline", cfg.env_name, cfg.agent,
                                  cfg.to_dict(), list(seeds), git_sha())
    outcome = ExperimentOutcome(exp_id)
    try:
        for seed in seeds:
            seed_cfg = replace(cfg, seed=seed)
            outcome.runs.append(train_run(seed_cfg, db, final_eval_episodes, exp_id, progress=progress))
        if with_baseline:
            outcome.baseline = run_baseline(cfg, list(seeds), db, final_eval_episodes, exp_id)
        outcome.summary = summarize_experiment(
            [r.final_eval.mean_return for r in outcome.runs], [b.mean_return for b in outcome.baseline],
            [r.initial_eval.mean_return for r in outcome.runs if r.initial_eval is not None])
        db.finish_experiment(exp_id, "completed", outcome.summary)
    except BaseException as exc:
        db.finish_experiment(exp_id, "failed" if isinstance(exc, Exception) else "stopped", outcome.summary or None)
        raise
    return outcome

