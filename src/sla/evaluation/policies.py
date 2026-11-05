"""Learned grid policies for pictures: greedy move per square, its value, and the path the agent walks.

The website draws these on the FrozenLake and CliffWalking maps. They come from a real trained Q-table:
the best checkpoint of a stored run, or — on the hosted app, where checkpoints are not committed — from
``data/demo/policies.json``, which ``scripts/export_policies.py`` writes from those same checkpoints.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from sla import settings

POLICIES_FILE = settings.PROJECT_ROOT / "data" / "demo" / "policies.json"

FROZENLAKE_DESC = ["SFFF", "FHFH", "FFFH", "HFFG"]
CLIFF_DESC = ["F" * 12, "F" * 12, "F" * 12, "S" + "C" * 10 + "G"]
# Arrow for each action number (the two games number their moves differently)
ARROWS = {"FrozenLake-v1": ["←", "↓", "→", "↑"], "CliffWalking-v1": ["↑", "→", "↓", "←"]}
GRID_ENVS = ("FrozenLake-v1", "CliffWalking-v1")


def greedy(q: np.ndarray) -> tuple[list[int], list[float]]:
    """Best action and its value (max_a Q) for every state."""
    return [int(np.argmax(row)) for row in q], [float(row.max()) for row in q]


def walk(env_name: str, actions: list[int], max_steps: int = 60) -> list[int]:
    """Squares visited when always taking the greedy action from the start (deterministic maps only)."""
    desc = FROZENLAKE_DESC if env_name == "FrozenLake-v1" else CLIFF_DESC
    rows, cols = len(desc), len(desc[0])
    start = next(i * cols + j for i, r in enumerate(desc) for j, c in enumerate(r) if c == "S")
    # (row, col) change for each action number
    moves = ({0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)} if env_name == "FrozenLake-v1"
             else {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)})
    s, path = start, [start]
    for _ in range(max_steps):
        r, c = divmod(s, cols)
        dr, dc = moves[actions[s]]
        r, c = min(max(r + dr, 0), rows - 1), min(max(c + dc, 0), cols - 1)
        s = r * cols + c
        path.append(s)
        if desc[r][c] in "GHC":
            break
    return path


def from_checkpoint(run_dir: str | Path) -> tuple[list[int], list[float]]:
    from sla.checkpoints.manager import best_checkpoint, load_checkpoint
    agent, _ = load_checkpoint(best_checkpoint(Path(run_dir)))
    return greedy(agent.q)


def learned(db: Any, env_name: str, algorithm: str) -> dict[str, Any] | None:
    """Greedy policy of the newest completed run of ``algorithm`` on ``env_name`` (non-slippery FrozenLake).

    Tries the run's checkpoint first; falls back to the committed snapshot file. None if neither exists.
    """
    try:
        runs = db.list_runs()
    except Exception:  # noqa: BLE001 - the page shows a friendly empty state
        runs = None
    if runs is not None and not runs.empty:
        sel = runs[(runs["env"] == env_name) & (runs["algorithm"] == algorithm) & (runs["status"] == "completed")]
        for _, r in sel.iterrows():
            run = db.get_run(r["run_id"]) or {}
            if run.get("config", {}).get("env_kwargs", {}).get("is_slippery", False):
                continue
            if not r.get("run_dir") or r.get("variant") in ("human_feedback", "baseline"):
                continue
            try:
                actions, values = from_checkpoint(r["run_dir"])
                return {"env": env_name, "algorithm": algorithm, "run_id": r["run_id"], "actions": actions,
                        "values": values, "source": "checkpoint"}
            except Exception:  # noqa: BLE001 - checkpoint not on this machine
                continue
    for item in snapshot():
        if item["env"] == env_name and item["algorithm"] == algorithm:
            return {**item, "source": "snapshot"}
    return None


def snapshot(path: Path = POLICIES_FILE) -> list[dict[str, Any]]:
    try:
        return list(json.loads(path.read_text(encoding="utf-8")))
    except (OSError, ValueError):
        return []
