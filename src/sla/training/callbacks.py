"""Runner callbacks that connect training to the database, the UI and the evaluator."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from sla.training.runner import Callback, EpisodeInfo, RunContext, RunResult


class DatabaseCallback(Callback):
    """Registers the run, logs every episode and marks the run finished."""

    def __init__(self, db: Any, git_sha: str | None = None, experiment_id: int | None = None,
                 variant: str | None = None) -> None:
        self.db = db
        self.git_sha = git_sha
        self.experiment_id = experiment_id
        self.variant = variant

    def on_run_start(self, ctx: RunContext) -> None:
        self.db.start_run(ctx.run_id, ctx.cfg.env_name, ctx.cfg.agent, ctx.cfg.seed, ctx.cfg.to_dict(),
                          str(ctx.run_dir), self.git_sha, self.experiment_id, self.variant)

    def on_episode_end(self, ctx: RunContext, info: EpisodeInfo) -> bool:
        self.db.log_episode(ctx.run_id, info)
        return False

    def on_run_end(self, ctx: RunContext, result: RunResult) -> None:
        status = "completed" if result.stopped_reason == "completed" else "stopped"
        self.db.finish_run(ctx.run_id, status, result.episodes_completed, result.stopped_reason)
        if ctx.extra.get("stop_reason") == "divergence":
            self.db.log_metric(ctx.run_id, "divergence_stop", 1.0, result.episodes_completed)
        flags = ctx.extra.get("regression_flags", [])
        if flags:
            self.db.log_metric(ctx.run_id, "regression_flags", float(len(flags)))


class InitialEvalCallback(Callback):
    """Evaluates the untrained agent once, before the first episode ("before learning" score)."""

    def __init__(self, db: Any, n_episodes: int, seed_base: int) -> None:
        self.db = db
        self.n_episodes = n_episodes
        self.seed_base = seed_base
        self.result: Any = None

    def on_run_start(self, ctx: RunContext) -> None:
        if ctx.extra.get("start_episode", 0) > 0:
            return  # resumed run: the initial score was recorded the first time
        from sla.evaluation.evaluate import evaluate_agent
        res = evaluate_agent(ctx.agent, ctx.cfg.env_name, ctx.cfg.env_kwargs, self.n_episodes, self.seed_base,
                             max_steps=ctx.cfg.max_steps_per_episode)
        ctx.extra["initial_eval"] = res
        self.result = res
        if self.db is not None:
            self.db.log_evaluation(ctx.run_id, "initial", res, episode=None, seed_base=self.seed_base)


class ProgressCallback(Callback):
    """Calls ``fn(info, ctx)`` after every episode; ``fn`` may return True to stop training (UI stop button)."""

    def __init__(self, fn: Callable[[EpisodeInfo, RunContext], bool | None]) -> None:
        self.fn = fn

    def on_episode_end(self, ctx: RunContext, info: EpisodeInfo) -> bool:
        if self.fn(info, ctx):
            ctx.extra["stop_reason"] = "user"
            return True
        return False
