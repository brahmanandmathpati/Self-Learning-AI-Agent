"""One place for the names of agents and environments shown to people (CLI, website, documents)."""

from __future__ import annotations

ALGO_LABELS: dict[str, str] = {
    "random": "Random",
    "q_learning": "Q-learning",
    "sarsa": "SARSA",
    "expected_sarsa": "Expected SARSA",
    "dqn": "DQN",
}

# Agents that keep a Q-table: they need a game with a small, countable number of states.
TABULAR_AGENTS: tuple[str, ...] = ("q_learning", "sarsa", "expected_sarsa")
# Games with countable states (Discrete observation space) and the one with continuous states.
TABULAR_ENVS: tuple[str, ...] = ("FrozenLake-v1", "Taxi-v4", "CliffWalking-v1")
CONTINUOUS_ENVS: tuple[str, ...] = ("CartPole-v1",)

ENV_LABELS: dict[str, str] = {
    "FrozenLake-v1": "FrozenLake",
    "Taxi-v4": "Taxi",
    "CliffWalking-v1": "CliffWalking",
    "CartPole-v1": "CartPole",
}


def algo_label(algorithm: str | None) -> str:
    return ALGO_LABELS.get(algorithm or "", algorithm or "—")


def env_label(env_name: str | None) -> str:
    return ENV_LABELS.get(env_name or "", env_name or "—")
