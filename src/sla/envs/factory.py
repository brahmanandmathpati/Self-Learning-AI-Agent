"""Environment factory.

All code creates environments through ``make_env`` so seeding and error
messages are handled in one place.
"""

from __future__ import annotations

from typing import Any

import gymnasium as gym

from sla.utils.errors import EnvError

SUPPORTED_ENVS: dict[str, dict[str, Any]] = {
    # name: default keyword arguments passed to gymnasium.make
    "FrozenLake-v1": {"map_name": "4x4", "is_slippery": False},
    "CartPole-v1": {},
}

CARTPOLE_X_LIMIT = 2.4  # Gymnasium ends a CartPole episode when |x| > 2.4


def make_env(name: str, seed: int | None = None, render_mode: str | None = None,
             **kwargs: Any) -> gym.Env:
    """Create a supported Gymnasium environment.

    Args:
        name: "FrozenLake-v1" or "CartPole-v1".
        seed: if given, seeds the action space so random actions repeat.
        render_mode: None, "human" (window) or "rgb_array" (frames for GIFs).
        **kwargs: overrides for the defaults in SUPPORTED_ENVS.
    """
    if name not in SUPPORTED_ENVS:
        raise EnvError(f"Unsupported environment {name!r}. Supported: {sorted(SUPPORTED_ENVS)}")
    options = {**SUPPORTED_ENVS[name], **kwargs}
    try:
        env = gym.make(name, render_mode=render_mode, **options)
    except Exception as exc:  # gymnasium raises several error types
        raise EnvError(f"Could not create {name} with options {options}: {exc}") from exc
    if seed is not None:
        env.action_space.seed(seed)
    return env


def end_reason(env_name: str, terminated: bool, truncated: bool, reward: float,
               state: Any) -> str:
    """Explain why an episode ended, for logs and failure analysis.

    FrozenLake: "goal", "hole" or "truncated".
    CartPole:   "position" (cart left the track), "angle" (pole fell) or "truncated".
    """
    if truncated and not terminated:
        return "truncated"
    if not terminated:
        return "running"
    if env_name == "FrozenLake-v1":
        return "goal" if reward > 0 else "hole"
    if env_name == "CartPole-v1":
        x = float(state[0])
        return "position" if abs(x) > CARTPOLE_X_LIMIT else "angle"
    return "terminated"
