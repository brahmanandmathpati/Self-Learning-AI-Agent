"""Plain-Python helpers behind the website's "How it works" page.

Nothing here imports Streamlit, the database, Gymnasium or PyTorch, so everything is cheap to import and easy to
unit-test. The numbers it returns are computed with the project's own functions
(``q_learning_update`` and ``LinearSchedule``) instead of being typed in by hand.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from sla.agents.q_learning import q_learning_update
from sla.agents.schedules import LinearSchedule

# --------------------------------------------------------------------------- the Q-learning update


@dataclass(frozen=True)
class QUpdate:
    """One Q-learning update, with every intermediate number so the page can show the arithmetic."""

    old_q: float
    reward: float
    best_next_q: float
    terminated: bool
    alpha: float
    gamma: float
    target: float
    td_error: float
    new_q: float


def q_update(old_q: float, reward: float, best_next_q: float, terminated: bool, alpha: float,
             gamma: float) -> QUpdate:
    """Apply the project's ``q_learning_update`` to a tiny 2-state table and return all the numbers."""
    q = np.array([[old_q], [best_next_q]], dtype=np.float64)  # row 0 = this state, row 1 = the next state
    td_error = q_learning_update(q, 0, 0, reward, 1, terminated, alpha, gamma)
    target = reward if terminated else reward + gamma * best_next_q
    return QUpdate(old_q, reward, best_next_q, terminated, alpha, gamma, float(target), float(td_error),
                   float(q[0, 0]))


def describe_update(u: QUpdate) -> list[str]:
    """The three lines of arithmetic shown under the calculator."""
    if u.terminated:
        target = f"target = r = {u.reward:.4g}  (the game ended, so there is no next state)"
    else:
        target = (f"target = r + γ × best next Q = {u.reward:.4g} + {u.gamma:.4g} × {u.best_next_q:.4g} "
                  f"= {u.target:.4g}")
    error = f"error = target − old Q = {u.target:.4g} − {u.old_q:.4g} = {u.td_error:.4g}"
    new = f"new Q = old Q + α × error = {u.old_q:.4g} + {u.alpha:.4g} × {u.td_error:.4g} = {u.new_q:.4g}"
    return [target, error, new]


# --------------------------------------------------------------------------- epsilon


def epsilon_curve(start: float, end: float, duration: int, points: int = 121) -> tuple[list[int], list[float]]:
    """Epsilon over environment steps, from the real ``LinearSchedule``; runs a little past the end of the decay."""
    schedule = LinearSchedule(start, end, duration)
    last = int(duration * 1.3)
    steps = [round(i * last / (points - 1)) for i in range(points)]
    return steps, [schedule.value(s) for s in steps]


def epsilon_at(start: float, end: float, duration: int, step: int) -> float:
    return LinearSchedule(start, end, duration).value(step)


# --------------------------------------------------------------------------- the FrozenLake demo

LAKE_MAP = ("SFFF", "FHFH", "FFFH", "HFFG")  # the standard 4x4 map; the project uses it with is_slippery: false
ACTION_ARROWS = ("←", "↓", "→", "↑")  # Gymnasium order: left, down, right, up
N_STATES = len(LAKE_MAP) * len(LAKE_MAP[0])
N_ACTIONS = len(ACTION_ARROWS)


def lake_step(state: int, action: int) -> tuple[int, float, bool]:
    """One move on the non-slippery map: (next state, reward, terminated). Same rules as FrozenLake-v1."""
    cols = len(LAKE_MAP[0])
    row, col = divmod(state, cols)
    if action == 0:
        col = max(col - 1, 0)
    elif action == 1:
        row = min(row + 1, len(LAKE_MAP) - 1)
    elif action == 2:
        col = min(col + 1, cols - 1)
    else:
        row = max(row - 1, 0)
    nxt = row * cols + col
    cell = LAKE_MAP[row][col]
    return nxt, (1.0 if cell == "G" else 0.0), cell in "HG"


@dataclass(frozen=True)
class LakeDemo:
    """Q-table after every episode (index 0 = before any training) plus per-episode success and epsilon."""

    q_by_episode: np.ndarray  # shape (episodes + 1, 16, 4)
    success: np.ndarray  # shape (episodes,), 1.0 if the episode reached the goal
    epsilon: np.ndarray  # shape (episodes,), epsilon at the start of each episode


def run_lake_demo(episodes: int, alpha: float, gamma: float, eps_start: float, eps_end: float, eps_steps: int,
                  max_steps: int = 100, seed: int = 0) -> LakeDemo:
    """Tabular Q-learning on the 4x4 lake with the same update and epsilon schedule as the real agent.

    This is a small separate loop (no Gymnasium, no database, no checkpoints), so it is an *illustration* of the
    algorithm, not a stored result. The same seed always gives the same tables.
    """
    rng = np.random.default_rng(seed)
    schedule = LinearSchedule(eps_start, eps_end, eps_steps)
    q = np.zeros((N_STATES, N_ACTIONS))
    snapshots = np.zeros((episodes + 1, N_STATES, N_ACTIONS))
    success = np.zeros(episodes)
    eps_log = np.zeros(episodes)
    steps = 0
    for ep in range(episodes):
        state, eps_log[ep] = 0, schedule.value(steps)
        for _ in range(max_steps):
            if rng.random() < schedule.value(steps):
                action = int(rng.integers(N_ACTIONS))
            else:
                action = int(rng.choice(np.flatnonzero(q[state] == q[state].max())))  # random tie-break
            nxt, reward, terminated = lake_step(state, action)
            q_learning_update(q, state, action, reward, nxt, terminated, alpha, gamma)
            steps += 1
            state = nxt
            if terminated:
                success[ep] = reward
                break
        snapshots[ep + 1] = q
    return LakeDemo(snapshots, success, eps_log)


def policy_arrows(q: np.ndarray) -> list[str]:
    """Best move per square as an arrow ("·" where the agent has learned nothing yet)."""
    return [ACTION_ARROWS[int(np.argmax(row))] if row.max() > 0 else "·" for row in q]


def best_values(q: np.ndarray) -> np.ndarray:
    return q.max(axis=1)


def greedy_walk(q: np.ndarray, max_steps: int = 100) -> tuple[bool, list[int]]:
    """Follow the table with epsilon = 0 (learning off). Returns (reached the goal, squares visited)."""
    state, path = 0, [0]
    for _ in range(max_steps):
        state, reward, terminated = lake_step(state, int(np.argmax(q[state])))
        path.append(state)
        if terminated:
            return reward > 0, path
    return False, path


def random_success_rate(games: int = 500, max_steps: int = 100, seed: int = 0) -> float:
    """Share of games a purely random player wins (the 'before training' state, all-zero table)."""
    rng = np.random.default_rng(seed)
    wins = 0
    for _ in range(games):
        state = 0
        for _ in range(max_steps):
            state, reward, terminated = lake_step(state, int(rng.integers(N_ACTIONS)))
            if terminated:
                wins += int(reward > 0)
                break
    return wins / games


def moving_average(values: np.ndarray, window: int = 50) -> np.ndarray:
    """Trailing mean (shorter windows at the start), same length as ``values``."""
    if len(values) == 0:
        return np.zeros(0)
    csum = np.cumsum(np.insert(values.astype(float), 0, 0.0))
    idx = np.arange(1, len(values) + 1)
    lo = np.maximum(idx - window, 0)
    return (csum[idx] - csum[lo]) / (idx - lo)


# --------------------------------------------------------------------------- sizes used in the explanations


def dqn_parameter_count(hidden: int, inputs: int = 4, outputs: int = 2) -> int:
    """Weights + biases of the inputs -> hidden -> hidden -> outputs network."""
    return (inputs * hidden + hidden) + (hidden * hidden + hidden) + (hidden * outputs + outputs)


# --------------------------------------------------------------------------- practice questions for the review


def practice_questions(alpha: float, gamma: float, eps_start: float, eps_end: float, eps_steps: int,
                       target_update: int, test_seed_base: int) -> list[tuple[str, str]]:
    """Six (question, answer) pairs. Every answer is computed here, not typed in, so it can never drift."""
    q1 = q_update(0.2, 1.0, 0.0, True, alpha, gamma)
    q2 = q_update(0.5, 0.0, 0.8, False, alpha, gamma)
    step = max(eps_steps // 5, 1)
    eps = epsilon_at(eps_start, eps_end, eps_steps, step)
    cells = N_STATES * N_ACTIONS
    return [
        (f"Q = 0.2. The move ends the game at the goal (reward 1). α = {alpha:g}. What is the new Q?",
         "\n\n".join(describe_update(q1))),
        (f"Q = 0.5, reward 0, best next Q = 0.8, the game continues. α = {alpha:g}, γ = {gamma:g}. New Q?",
         "\n\n".join(describe_update(q2))),
        (f"ε falls from {eps_start:g} to {eps_end:g} over {eps_steps:,} steps. What is ε after {step:,} steps?",
         f"ε = {eps_start:g} − ({eps_start:g} − {eps_end:g}) × {step:,} / {eps_steps:,} = **{eps:.4g}**"),
        (f"The target network is copied every {target_update:,} gradient steps. How many copies in "
         f"{4 * target_update:,} steps?", f"{4 * target_update:,} ÷ {target_update:,} = **4**"),
        ("Which reset seed does test game number 7 use?",
         f"{test_seed_base:,} + 7 = **{test_seed_base + 7:,}**"),
        ("How many numbers are in the FrozenLake Q-table?",
         f"{N_STATES} squares × {N_ACTIONS} moves = **{cells}**"),
    ]
