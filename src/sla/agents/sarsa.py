"""SARSA and Expected SARSA: two table-based relatives of Q-learning.

All three keep the same Q-table (one row per state, one column per action). They differ only in the
"target" — the guess of how good the next situation is:

* Q-learning      target = r + γ · max_a' Q(s', a')                 (assumes the best move next; off-policy)
* SARSA           target = r + γ · Q(s', a')                        (uses the move it will really make next)
* Expected SARSA  target = r + γ · Σ_a' π(a' | s') · Q(s', a')       (average over the ε-greedy policy)

SARSA's name comes from the five things one update uses: State, Action, Reward, next State, next Action.
Because SARSA and Expected SARSA learn the value of the policy they actually follow (exploration included),
they prefer safer routes when random moves are dangerous — CliffWalking shows this clearly.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from sla.agents.base import Transition
from sla.agents.q_learning import QLearningAgent


def sarsa_update(q: np.ndarray, s: int, a: int, r: float, s_next: int, a_next: int, terminated: bool,
                 alpha: float, gamma: float) -> float:
    """One SARSA update in place; returns the TD error. No bootstrap at a real terminal state."""
    target = r if terminated else r + gamma * float(q[s_next, a_next])
    td_error = target - float(q[s, a])
    q[s, a] += alpha * td_error
    return td_error


def epsilon_greedy_probs(row: np.ndarray, epsilon: float) -> np.ndarray:
    """Probability of each action under ε-greedy; ties for the best action share the greedy part."""
    n = row.shape[0]
    probs = np.full(n, epsilon / n, dtype=np.float64)
    best = np.flatnonzero(row == row.max())
    probs[best] += (1.0 - epsilon) / best.size
    return probs


def expected_sarsa_update(q: np.ndarray, s: int, a: int, r: float, s_next: int, terminated: bool,
                          alpha: float, gamma: float, epsilon: float) -> float:
    """One Expected SARSA update in place; returns the TD error."""
    if terminated:
        target = r
    else:
        row = q[s_next]
        target = r + gamma * float(np.dot(epsilon_greedy_probs(row, epsilon), row))
    td_error = target - float(q[s, a])
    q[s, a] += alpha * td_error
    return td_error


class SarsaAgent(QLearningAgent):
    """On-policy TD control. The next action is chosen during ``update`` and then really played by ``act``."""

    name = "sarsa"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._next: tuple[int, int] | None = None  # (next state, the action already chosen for it)

    def _choose(self, state: int) -> int:
        if self.rng.random() < self.epsilon:
            return int(self.rng.integers(self.n_actions))
        return self.greedy_action(state)

    def act(self, obs: Any, explore: bool = True) -> int:
        if explore and self._next is not None and self._next[0] == int(obs):
            action = self._next[1]
            self._next = None
            return action
        return super().act(obs, explore)

    def update(self, transition: Transition) -> dict[str, float]:
        s, s_next = int(transition.state), int(transition.next_state)
        self.steps += 1  # the next action uses the exploration rate of the next step
        if transition.terminated:
            td = sarsa_update(self.q, s, transition.action, transition.reward, s_next, 0, True, self.alpha,
                              self.gamma)
            self._next = None
        else:
            a_next = self._choose(s_next)
            td = sarsa_update(self.q, s, transition.action, transition.reward, s_next, a_next, False, self.alpha,
                              self.gamma)
            # after a time-limit cut the episode ends anyway, so the chosen action is never played
            self._next = None if transition.truncated else (s_next, a_next)
        return {"td_error": td}

    def end_episode(self) -> None:
        self._next = None


class ExpectedSarsaAgent(QLearningAgent):
    """Like SARSA, but averages over every next action using the ε-greedy probabilities (lower variance)."""

    name = "expected_sarsa"

    def update(self, transition: Transition) -> dict[str, float]:
        td = expected_sarsa_update(self.q, int(transition.state), transition.action, transition.reward,
                                   int(transition.next_state), transition.terminated, self.alpha, self.gamma,
                                   self.epsilon)
        self.steps += 1
        return {"td_error": td}
