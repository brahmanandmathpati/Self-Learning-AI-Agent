"""Frozen-policy evaluation.

Evaluation rules:
  * explore=False (no random actions, epsilon is not used),
  * agent.update() is never called, so nothing is learned,
  * fixed evaluation seeds that are never used for training.
"""

from __future__ import annotations

import copy
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from sla.agents.base import Agent
from sla.checkpoints.manager import load_checkpoint, save_checkpoint
from sla.envs.factory import make_env
from sla.training.runner import Callback, EpisodeInfo, RunContext
from sla.utils.logging_setup import get_logger

log = get_logger(__name__)

# Training uses reset seeds seed*100_000 + episode (see sla.utils.seeding.episode_seed),
# so evaluation seeds start far above that range and never overlap with training.
EVAL_SEED_BASE = 10_000_000   # "validation" seeds: periodic evaluation + picking the best checkpoint
TEST_SEED_BASE = 20_000_000   # "test" seeds: final evaluation only, never used to pick checkpoints
SUCCESS_THRESHOLDS = {"FrozenLake-v1": 1.0, "CartPole-v1": 500.0}


@dataclass
class EvalResult:
    mean_return: float
    std_return: float
    success_rate: float
    n_episodes: int
    returns: list[float] = field(default_factory=list)
    median_return: float = 0.0
    mean_length: float = 0.0
    lengths: list[int] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_agent(agent: Agent, env_name: str, env_kwargs: dict[str, Any] | None = None,
                   n_episodes: int = 100, seed_base: int = EVAL_SEED_BASE,
                   max_steps: int = 10_000) -> EvalResult:
    """Run the agent greedily for ``n_episodes`` and return the scores.

    The episodes are played by a deep copy of the agent with exploration off and ``update()`` never
    called, so the training agent (weights, Q-table, replay buffer, RNG state, step counters) is untouched.
    """
    if n_episodes <= 0:
        raise ValueError("n_episodes must be > 0")
    policy = copy.deepcopy(agent)
    env = make_env(env_name, **(env_kwargs or {}))
    returns: list[float] = []
    lengths: list[int] = []
    try:
        for i in range(n_episodes):
            state, _ = env.reset(seed=seed_base + i)
            total, steps, done = 0.0, 0, False
            while not done and steps < max_steps:
                action = policy.act(state, explore=False)
                state, reward, terminated, truncated, _ = env.step(action)
                total += float(reward)
                steps += 1
                done = terminated or truncated
            returns.append(total)
            lengths.append(steps)
    finally:
        env.close()
    arr = np.asarray(returns)
    threshold = SUCCESS_THRESHOLDS.get(env_name, float("inf"))
    return EvalResult(float(arr.mean()), float(arr.std()), float(np.mean(arr >= threshold)),
                      n_episodes, returns, float(np.median(arr)), float(np.mean(lengths)), lengths)


def evaluate_checkpoint(folder: Path, env_name: str, env_kwargs: dict[str, Any] | None = None,
                        n_episodes: int = 100, seed_base: int = EVAL_SEED_BASE) -> EvalResult:
    agent, _ = load_checkpoint(folder)
    return evaluate_agent(agent, env_name, env_kwargs, n_episodes, seed_base)


class PeriodicEvalCallback(Callback):
    """Every ``every`` episodes: evaluate the frozen policy, store the score, keep the best checkpoint."""

    def __init__(self, every: int, n_episodes: int = 20, db: Any = None,
                 seed_base: int = EVAL_SEED_BASE) -> None:
        self.every = every
        self.n_episodes = n_episodes
        self.db = db
        self.seed_base = seed_base
        self.best_mean = -float("inf")

    def on_run_start(self, ctx: RunContext) -> None:
        ctx.extra.setdefault("eval_history", [])
        best_file = ctx.run_dir / "checkpoints" / "best" / "checkpoint.json"
        if best_file.exists():  # resuming: remember the previous best
            from sla.utils.io_helpers import read_json
            self.best_mean = float(read_json(best_file).get("eval_mean", -float("inf")))

    def on_episode_end(self, ctx: RunContext, info: EpisodeInfo) -> bool:
        if (info.episode + 1) % self.every != 0:
            return False
        res = evaluate_agent(ctx.agent, ctx.cfg.env_name, ctx.cfg.env_kwargs, self.n_episodes, self.seed_base)
        ctx.extra["eval_history"].append((info.episode, res.mean_return))
        ctx.extra["last_eval"] = res
        if self.db is not None:
            self.db.log_evaluation(ctx.run_id, "validation", res, episode=info.episode, seed_base=self.seed_base)
        log.info("Eval after episode %d: mean %.2f ± %.2f", info.episode, res.mean_return, res.std_return)
        if res.mean_return > self.best_mean:
            self.best_mean = res.mean_return
            best = save_checkpoint(ctx.agent, ctx.run_dir / "checkpoints" / "best", info.episode,
                                   {"eval_mean": res.mean_return})
            if self.db is not None:
                self.db.set_checkpoints(ctx.run_id, best=str(best))
        return False
