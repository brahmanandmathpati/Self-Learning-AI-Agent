"""Checkpoints: save and resume training.

Layout inside a run folder:
    runs/<run_id>/checkpoints/ep_000049/   (meta.json + agent files)
    runs/<run_id>/checkpoints/latest.json  {"episode": 49, "path": "ep_000049"}
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sla.agents.base import Agent
from sla.training.config import load_config
from sla.training.runner import Callback, EpisodeInfo, RunContext, RunResult, run_training
from sla.utils.errors import CheckpointError
from sla.utils.io_helpers import read_json, write_json
from sla.utils.logging_setup import get_logger

log = get_logger(__name__)


def _agent_class(name: str) -> type[Agent]:
    if name == "random":
        from sla.agents.random_agent import RandomAgent
        return RandomAgent
    if name == "q_learning":
        from sla.agents.q_learning import QLearningAgent
        return QLearningAgent
    if name == "dqn":
        from sla.agents.dqn import DQNAgent
        return DQNAgent
    raise CheckpointError(f"Unknown agent type in checkpoint: {name!r}")


def save_checkpoint(agent: Agent, folder: Path, episode: int, extra: dict[str, Any] | None = None) -> Path:
    """Save the agent plus a small checkpoint.json describing it."""
    folder = Path(folder)
    try:
        agent.save(folder)
        write_json(folder / "checkpoint.json", {"agent": agent.name, "episode": episode, **(extra or {})})
    except OSError as exc:
        raise CheckpointError(f"Could not save checkpoint to {folder}: {exc}") from exc
    return folder


def load_checkpoint(folder: Path) -> tuple[Agent, dict[str, Any]]:
    """Return (agent, checkpoint_info) from a checkpoint folder."""
    folder = Path(folder)
    if not (folder / "checkpoint.json").is_file():
        raise CheckpointError(f"No checkpoint found at {folder}")
    info = read_json(folder / "checkpoint.json")
    try:
        agent = _agent_class(info["agent"]).load(folder)
    except (OSError, KeyError, ValueError) as exc:
        raise CheckpointError(f"Checkpoint at {folder} is incomplete or corrupt: {exc}") from exc
    return agent, info


def latest_checkpoint(run_dir: Path) -> Path:
    """Folder of the most recent checkpoint in a run."""
    pointer = Path(run_dir) / "checkpoints" / "latest.json"
    if not pointer.is_file():
        raise CheckpointError(f"No checkpoints in {run_dir}")
    return pointer.parent / read_json(pointer)["path"]


def best_checkpoint(run_dir: Path) -> Path:
    """Folder of the best checkpoint (highest validation score), falling back to the latest one."""
    best = Path(run_dir) / "checkpoints" / "best"
    return best if (best / "checkpoint.json").is_file() else latest_checkpoint(run_dir)


def resolve_checkpoint(run_dir: Path, which: str = "best") -> Path:
    """``which`` is 'best', 'latest' or a checkpoint folder name such as 'ep_000499'."""
    if which == "best":
        return best_checkpoint(run_dir)
    if which == "latest":
        return latest_checkpoint(run_dir)
    folder = Path(run_dir) / "checkpoints" / which
    if not (folder / "checkpoint.json").is_file():
        raise CheckpointError(f"No checkpoint {which!r} in {run_dir}")
    return folder


class CheckpointCallback(Callback):
    """Saves a checkpoint every ``every`` episodes and at the end of the run."""

    def __init__(self, every: int, keep_last: int = 3, db: Any = None) -> None:
        if every <= 0:
            raise ValueError("every must be > 0")
        self.db = db
        self.every = every
        self.keep_last = keep_last
        self.saved: list[Path] = []

    def _save(self, ctx: RunContext, episode: int) -> None:
        name = f"ep_{episode:06d}"
        folder = save_checkpoint(ctx.agent, ctx.run_dir / "checkpoints" / name, episode)
        write_json(ctx.run_dir / "checkpoints" / "latest.json", {"episode": episode, "path": name})
        self.saved.append(folder)
        if self.db is not None:
            self.db.set_checkpoints(ctx.run_id, latest=str(folder))
        log.info("Saved checkpoint %s", folder)
        self._cleanup()

    def _cleanup(self) -> None:
        """Keep only the newest ``keep_last`` periodic checkpoints (best/ is never deleted)."""
        import shutil
        while len(self.saved) > self.keep_last:
            old = self.saved.pop(0)
            shutil.rmtree(old, ignore_errors=True)

    def on_episode_end(self, ctx: RunContext, info: EpisodeInfo) -> bool:
        if (info.episode + 1) % self.every == 0:
            self._save(ctx, info.episode)
        return False

    def on_run_end(self, ctx: RunContext, result: RunResult) -> None:
        last_episode = result.episodes_completed - 1
        if last_episode >= 0 and (last_episode + 1) % self.every != 0:
            self._save(ctx, last_episode)


def resume_training(run_dir: Path, callbacks: list[Callback] | None = None) -> RunResult:
    """Continue a run from its latest checkpoint, keeping the same run id and folder."""
    run_dir = Path(run_dir)
    cfg = load_config(run_dir / "config.yaml")
    agent, info = load_checkpoint(latest_checkpoint(run_dir))
    start = int(info["episode"]) + 1
    if start >= cfg.episodes:
        raise CheckpointError(f"Run {run_dir.name} already finished all {cfg.episodes} episodes")
    log.info("Resuming %s from episode %d", run_dir.name, start)
    return run_training(cfg, callbacks, agent=agent, run_dir=run_dir, run_id=run_dir.name,
                        start_episode=start)
