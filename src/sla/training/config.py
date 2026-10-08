"""Run configuration: load a YAML file into checked dataclasses.

Example YAML (configs/frozenlake_qlearning.yaml):

    env_name: FrozenLake-v1
    env_kwargs: {is_slippery: false}
    agent: q_learning
    episodes: 2000
    seed: 0
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from typing import Any

import yaml

from sla.utils.errors import ConfigError

ALLOWED_ENVS = ("FrozenLake-v1", "CartPole-v1")
ALLOWED_AGENTS = ("random", "q_learning", "dqn")


@dataclass
class DQNConfig:
    """Settings used only when agent == 'dqn'."""

    hidden_size: int = 128
    batch_size: int = 64
    buffer_size: int = 50_000
    learning_starts: int = 1_000
    train_freq: int = 1
    target_update_every: int = 500
    grad_clip: float = 10.0
    replay_enabled: bool = True
    target_net_enabled: bool = True
    optimizer: str = "adam"          # "adam" or "adamw"
    weight_decay: float = 0.0        # only used by AdamW


@dataclass
class RunConfig:
    """Everything needed to start one training run."""

    env_name: str = "FrozenLake-v1"
    agent: str = "q_learning"
    episodes: int = 1000
    seed: int = 0
    env_kwargs: dict[str, Any] = field(default_factory=dict)
    gamma: float = 0.99
    learning_rate: float = 0.1
    epsilon_start: float = 1.0
    epsilon_end: float = 0.05
    epsilon_decay_steps: int = 10_000
    max_steps_per_episode: int = 500
    max_wall_clock_s: float = 3_600.0
    eval_every: int = 50
    eval_episodes: int = 20
    checkpoint_every: int = 50
    run_root: str = "runs"
    dqn: DQNConfig = field(default_factory=DQNConfig)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _check(condition: bool, key: str, message: str) -> None:
    if not condition:
        raise ConfigError(f"Invalid config value for '{key}': {message}")


def validate_config(cfg: RunConfig) -> RunConfig:
    """Raise ConfigError (naming the bad key) if any value is wrong."""
    _check(cfg.env_name in ALLOWED_ENVS, "env_name", f"must be one of {ALLOWED_ENVS}, got {cfg.env_name!r}")
    _check(cfg.agent in ALLOWED_AGENTS, "agent", f"must be one of {ALLOWED_AGENTS}, got {cfg.agent!r}")
    positive_ints = ("episodes", "max_steps_per_episode", "eval_every", "eval_episodes", "checkpoint_every",
                     "epsilon_decay_steps")
    for key in positive_ints:
        value = getattr(cfg, key)
        _check(_is_int(value) and value > 0, key, f"must be a positive integer, got {value!r}")
    _check(_is_int(cfg.seed) and cfg.seed >= 0, "seed", f"must be an integer >= 0, got {cfg.seed!r}")
    _check(_is_number(cfg.gamma) and 0 < cfg.gamma <= 1, "gamma", f"must be in (0, 1], got {cfg.gamma!r}")
    _check(_is_number(cfg.learning_rate) and cfg.learning_rate > 0, "learning_rate",
           f"must be > 0, got {cfg.learning_rate!r}")
    for key in ("epsilon_start", "epsilon_end"):
        value = getattr(cfg, key)
        _check(_is_number(value) and 0 <= value <= 1, key, f"must be in [0, 1], got {value!r}")
    _check(cfg.epsilon_end <= cfg.epsilon_start, "epsilon_end", "must be <= epsilon_start")
    _check(_is_number(cfg.max_wall_clock_s) and cfg.max_wall_clock_s > 0, "max_wall_clock_s", "must be > 0")
    _check(isinstance(cfg.env_kwargs, dict), "env_kwargs", "must be a mapping")
    d = cfg.dqn
    for key in ("hidden_size", "batch_size", "buffer_size", "learning_starts", "train_freq", "target_update_every"):
        value = getattr(d, key)
        _check(_is_int(value) and value > 0, f"dqn.{key}", f"must be a positive integer, got {value!r}")
    _check(d.batch_size <= d.buffer_size, "dqn.batch_size", "must be <= dqn.buffer_size")
    _check(_is_number(d.grad_clip) and d.grad_clip > 0, "dqn.grad_clip", "must be > 0")
    _check(d.optimizer in ("adam", "adamw"), "dqn.optimizer", f"must be 'adam' or 'adamw', got {d.optimizer!r}")
    _check(_is_number(d.weight_decay) and d.weight_decay >= 0, "dqn.weight_decay", "must be >= 0")
    _check(isinstance(d.replay_enabled, bool), "dqn.replay_enabled", "must be true or false")
    _check(isinstance(d.target_net_enabled, bool), "dqn.target_net_enabled", "must be true or false")
    return cfg


def config_from_dict(data: dict[str, Any]) -> RunConfig:
    """Build a RunConfig from a plain dict, rejecting unknown keys."""
    if not isinstance(data, dict):
        raise ConfigError("Config must be a mapping of key: value pairs")
    allowed = {f.name for f in fields(RunConfig)}
    unknown = set(data) - allowed
    if unknown:
        raise ConfigError(f"Unknown config key(s): {sorted(unknown)}")
    data = dict(data)
    dqn_data = data.pop("dqn", None) or {}
    if not isinstance(dqn_data, dict):
        raise ConfigError("Invalid config value for 'dqn': must be a mapping")
    dqn_allowed = {f.name for f in fields(DQNConfig)}
    dqn_unknown = set(dqn_data) - dqn_allowed
    if dqn_unknown:
        raise ConfigError(f"Unknown dqn key(s): {sorted(dqn_unknown)}")
    try:
        cfg = RunConfig(**data, dqn=DQNConfig(**dqn_data))
    except TypeError as exc:  # pragma: no cover - defensive
        raise ConfigError(str(exc)) from exc
    return validate_config(cfg)


def load_config(path: str | Path) -> RunConfig:
    """Read a YAML file and return a validated RunConfig."""
    file_path = Path(path)
    if not file_path.is_file():
        raise ConfigError(f"Config file not found: {file_path}")
    try:
        data = yaml.safe_load(file_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ConfigError(f"Config file {file_path} is not valid YAML: {exc}") from exc
    return config_from_dict(data)


def save_config(cfg: RunConfig, path: str | Path) -> Path:
    """Write a RunConfig back to YAML (used to copy the config into each run folder)."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(yaml.safe_dump(cfg.to_dict(), sort_keys=False), encoding="utf-8")
    return file_path
