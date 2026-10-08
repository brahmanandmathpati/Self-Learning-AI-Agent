"""The training loop.

``run_training`` is the only place where an agent learns. Other features
(storage, checkpoints, evaluation, guards, validation) plug in as callbacks,
so this file rarely needs to change.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

from sla.agents.base import Agent, Transition
from sla.envs.factory import end_reason, make_env
from sla.training.config import RunConfig, save_config
from sla.training.safety import SafetyLimits, check_finite
from sla.utils.logging_setup import get_logger
from sla.utils.seeding import episode_seed, set_global_seed
from sla.utils.summary import format_episode_summary

log = get_logger(__name__)


@dataclass
class EpisodeInfo:
    episode: int
    total_reward: float
    length: int
    epsilon: float | None
    mean_loss: float | None
    end_reason: str
    wall_time_s: float


@dataclass
class RunContext:
    cfg: RunConfig
    run_id: str
    run_dir: Path
    env: Any
    agent: Agent
    start_time: float
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class RunResult:
    run_id: str
    run_dir: Path
    returns: list[float]
    lengths: list[int]
    episodes_completed: int
    stopped_reason: str  # "completed", "wall_clock", "divergence", "user" or "callback"


class Callback:
    """Base class for runner plug-ins. Override only the methods you need."""

    def on_run_start(self, ctx: RunContext) -> None: ...

    def on_step(self, ctx: RunContext, transition: Transition) -> None: ...

    def on_episode_end(self, ctx: RunContext, info: EpisodeInfo) -> bool:
        """Return True to stop training early."""
        return False

    def on_run_end(self, ctx: RunContext, result: RunResult) -> None: ...


def make_run_id(cfg: RunConfig) -> str:
    env_short = cfg.env_name.split("-")[0].lower()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{env_short}_{cfg.agent}_s{cfg.seed}_{stamp}"


def build_agent(cfg: RunConfig, env: Any) -> Agent:
    """Create the agent named in the config for this environment."""
    n_actions = int(env.action_space.n)
    if cfg.agent == "random":
        from sla.agents.random_agent import RandomAgent
        return RandomAgent(n_actions, seed=cfg.seed)
    from sla.agents.schedules import LinearSchedule
    schedule = LinearSchedule(cfg.epsilon_start, cfg.epsilon_end, cfg.epsilon_decay_steps)
    if cfg.agent == "q_learning":
        from sla.agents.q_learning import QLearningAgent
        if not hasattr(env.observation_space, "n"):
            raise ValueError("Tabular Q-learning needs a discrete observation space (e.g. FrozenLake)")
        return QLearningAgent(int(env.observation_space.n), n_actions, cfg.learning_rate,
                              cfg.gamma, schedule, seed=cfg.seed)
    if cfg.agent == "dqn":
        from sla.agents.dqn import DQNAgent
        obs_dim = int(np.prod(env.observation_space.shape))
        return DQNAgent(obs_dim, n_actions, cfg.dqn, cfg.gamma, cfg.learning_rate, schedule, seed=cfg.seed)
    raise ValueError(f"Unknown agent {cfg.agent!r}")


def run_training(cfg: RunConfig, callbacks: list[Callback] | None = None, agent: Agent | None = None,
                 run_dir: Path | None = None, run_id: str | None = None,
                 start_episode: int = 0) -> RunResult:
    """Train ``agent`` (or a new one from ``cfg``) for episodes start_episode .. cfg.episodes-1."""
    callbacks = callbacks or []
    set_global_seed(cfg.seed)
    run_id = run_id or make_run_id(cfg)
    run_dir = Path(run_dir) if run_dir else Path(cfg.run_root) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    save_config(cfg, run_dir / "config.yaml")

    env = make_env(cfg.env_name, seed=cfg.seed, **cfg.env_kwargs)
    agent = agent or build_agent(cfg, env)
    limits = SafetyLimits.from_config(cfg)
    ctx = RunContext(cfg, run_id, run_dir, env, agent, time.monotonic(), {"start_episode": start_episode})
    for cb in callbacks:
        cb.on_run_start(ctx)

    returns: list[float] = []
    lengths: list[int] = []
    stopped = "completed"
    log.info("Run %s: %s on %s, episodes %d..%d", run_id, cfg.agent, cfg.env_name,
             start_episode, cfg.episodes - 1)

    for episode in range(start_episode, cfg.episodes):
        ep_start = time.monotonic()
        state, _ = env.reset(seed=episode_seed(cfg.seed, episode))
        total, steps, losses = 0.0, 0, []
        terminated = truncated = False
        reward = 0.0
        while not (terminated or truncated):
            action = agent.act(state, explore=True)
            next_state, reward, terminated, truncated, _ = env.step(action)
            reward = check_finite(reward, "reward")
            steps += 1
            if limits.step_limit_reached(steps) and not terminated:
                truncated = True
            transition = Transition(state, int(action), reward, next_state, bool(terminated), bool(truncated))
            for cb in callbacks:
                cb.on_step(ctx, transition)
            stats = agent.update(transition)
            if "loss" in stats:
                losses.append(check_finite(stats["loss"], "loss"))
            total += reward
            state = next_state
        agent.end_episode()
        info = EpisodeInfo(episode, total, steps, agent.epsilon,
                           float(np.mean(losses)) if losses else None,
                           end_reason(cfg.env_name, terminated, truncated, reward, state),
                           time.monotonic() - ep_start)
        returns.append(total)
        lengths.append(steps)
        if (episode + 1) % max(1, cfg.eval_every) == 0:
            log.info(format_episode_summary(episode, returns, window=50, epsilon=agent.epsilon))
        stop_requested = False
        for cb in callbacks:
            if cb.on_episode_end(ctx, info):
                stop_requested = True
        if stop_requested:
            stopped = str(ctx.extra.get("stop_reason", "callback"))
            break
        if limits.wall_clock_exceeded(ctx.start_time):
            stopped = "wall_clock"
            log.warning("Wall-clock limit of %.0f s reached; stopping", limits.max_wall_clock_s)
            break

    env.close()
    result = RunResult(run_id, run_dir, returns, lengths, start_episode + len(returns), stopped)
    for cb in callbacks:
        cb.on_run_end(ctx, result)
    log.info("Run %s finished (%s) after %d episodes", run_id, stopped, result.episodes_completed)
    return result
