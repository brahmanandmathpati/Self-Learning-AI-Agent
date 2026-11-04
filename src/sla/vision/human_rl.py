"""Human-in-the-loop reinforcement learning: the user's gestures are the reward signal.

The agent plays FrozenLake (4×4, non-slippery) one step at a time. Before each step it proposes a move; the user
answers with a gesture (👍 = +1, 👎 = −1). The agent takes the move and updates its Q-table with the HUMAN reward
(instead of the game's reward):  Q(s,a) ← Q(s,a) + α · (r_human + γ · max Q(s′) − Q(s,a)).
Episodes are logged to the experiment database as Q-learning runs with variant = "human_feedback", so they appear in
the Run explorer. Reaching the goal is recorded (end_reason = "goal") to show whether the feedback taught the agent.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from types import SimpleNamespace

import numpy as np

ACTIONS = ["← left", "↓ down", "→ right", "↑ up"]
ARROWS = ["←", "↓", "→", "↑"]
MAP = ["SFFF", "FHFH", "FFFH", "HFFG"]


@dataclass
class HumanFeedbackAgent:
    alpha: float = 0.5
    gamma: float = 0.9
    epsilon: float = 0.1
    seed: int = 0
    max_steps: int = 50
    q: np.ndarray = field(default_factory=lambda: np.zeros((16, 4)))
    state: int = 0
    proposal: int | None = None
    episode: int = 0
    steps: int = 0
    total: float = 0.0
    history: list[dict] = field(default_factory=list)  # one row per finished episode
    run_id: str | None = None

    def __post_init__(self) -> None:
        import gymnasium as gym
        self.env = gym.make("FrozenLake-v1", desc=MAP, is_slippery=False)
        self.rng = np.random.default_rng(self.seed)
        self.state, _ = self.env.reset(seed=self.seed)
        self._t0 = time.perf_counter()
        self.propose()

    # -------------------------------------------------------------- acting
    def propose(self) -> int:
        """Pick the next move: best known action (random tie-break), or a random one with probability ε."""
        if self.rng.random() < self.epsilon:
            a = int(self.rng.integers(4))
        else:
            row = self.q[self.state]
            a = int(self.rng.choice(np.flatnonzero(row == row.max())))
        self.proposal = a
        return a

    def feedback(self, reward: float) -> dict:
        """Apply the human reward to the proposed move, take the move, and propose the next one."""
        a = self.proposal if self.proposal is not None else self.propose()
        s = self.state
        s2, env_r, terminated, truncated, _ = self.env.step(a)
        target = reward + (0.0 if terminated else self.gamma * float(self.q[s2].max()))
        self.q[s, a] += self.alpha * (target - self.q[s, a])
        self.steps += 1
        self.total += reward
        self.state = int(s2)
        info = {"state": s, "action": a, "reward": reward, "next_state": int(s2), "done": False}
        if terminated or truncated or self.steps >= self.max_steps:
            end = "goal" if env_r > 0 else ("hole" if terminated else "max_steps")
            info.update(done=True, end_reason=end)
            self._finish_episode(end)
        self.propose()
        return info

    def reset_episode(self, end_reason: str = "reset") -> None:
        if self.steps:
            self._finish_episode(end_reason)
        else:
            self.state, _ = self.env.reset()
            self.propose()

    def _finish_episode(self, end_reason: str) -> None:
        self.episode += 1
        self.history.append({"episode": self.episode, "total_reward": self.total, "length": self.steps,
                             "end_reason": end_reason, "wall_time_s": time.perf_counter() - self._t0})
        self.steps, self.total = 0, 0.0
        self._t0 = time.perf_counter()
        self.state, _ = self.env.reset()

    # -------------------------------------------------------------- views
    def greedy_policy(self) -> list[str]:
        """Arrow per square for the current Q-table ('·' where nothing has been learned yet)."""
        out = []
        for s in range(16):
            cell = MAP[s // 4][s % 4]
            if cell in "HG":
                out.append(cell)
            elif not self.q[s].any():
                out.append("·")
            else:
                out.append(ARROWS[int(self.q[s].argmax())])
        return out

    # -------------------------------------------------------------- persistence (experiment database)
    def save(self, db, final: bool = True) -> str:
        """Write this session to the database as a run with variant 'human_feedback'; returns the run id."""
        if self.run_id is None:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
            self.run_id = f"frozenlake_human_feedback_s{self.seed}_{stamp}"
            db.start_run(self.run_id, "FrozenLake-v1", "q_learning", self.seed,
                         {"agent": "q_learning", "reward": "human gestures", "alpha": self.alpha, "gamma": self.gamma,
                          "epsilon": self.epsilon, "map": MAP, "is_slippery": False}, variant="human_feedback")
        for row in self.history:
            db.log_episode(self.run_id, SimpleNamespace(epsilon=self.epsilon, mean_loss=None, **row))
        if final:
            db.finish_run(self.run_id, "completed", episodes_completed=len(self.history),
                          stopped_reason="session ended by user")
        return self.run_id
