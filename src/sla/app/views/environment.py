"""Environments: what the agent sees, what it can do and how it is rewarded."""

from __future__ import annotations

import numpy as np
import streamlit as st

from sla.app.charts.figures import frozenlake_map
from sla.app.components.ui import empty_state, hero, section
from sla.app.state import services

ARROWS = ["←", "↓", "→", "↑"]


def _frozenlake_policy(svc) -> tuple[list[str] | None, np.ndarray | None, str | None]:
    """Greedy arrows and state values from the best checkpoint of the newest Q-learning run."""
    runs = svc.experiments.trained_runs()
    runs = runs[(runs["algorithm"] == "q_learning") & (runs["status"] == "completed")] if not runs.empty else runs
    for _, r in runs.iterrows():
        cfg = svc.db.get_run(r["run_id"])["config"]
        if cfg.get("env_kwargs", {}).get("is_slippery", True) is False and r["run_dir"]:
            try:
                from sla.checkpoints.manager import best_checkpoint, load_checkpoint
                agent, _ = load_checkpoint(best_checkpoint(r["run_dir"]))
                return [ARROWS[int(np.argmax(row))] for row in agent.q], agent.q.max(axis=1), r["run_id"]
            except Exception:  # noqa: BLE001 - checkpoint missing on this machine
                continue
    return None, None, None


def render() -> None:
    svc = services()
    hero("Environments", "Two Gymnasium tasks: a grid solved with a Q-table and a control task solved with a DQN.")
    tab_fl, tab_cp = st.tabs(["FrozenLake-v1 · tabular Q-learning", "CartPole-v1 · Deep Q-Network"])
    with tab_fl:
        left, right = st.columns([2, 3])
        desc = ["SFFF", "FHFH", "FFFH", "HFFG"]
        arrows, values, run_id = _frozenlake_policy(svc)
        with left:
            st.plotly_chart(frozenlake_map(desc, arrows, values), width="stretch")
            if run_id:
                st.caption(f"Arrows = greedy action argmax_a Q(s, a) learned by run {run_id}; V = max_a Q(s, a).")
            else:
                st.caption("Train Q-learning on the non-slippery map to see the learned policy drawn on the grid.")
        with right:
            st.markdown("""
| | |
|---|---|
| **State space** | `Discrete(16)` — the agent's cell on the 4×4 grid |
| **Action space** | `Discrete(4)` — 0 left, 1 down, 2 right, 3 up |
| **Reward** | +1 for reaching the goal **G**, 0 otherwise (sparse) |
| **Episode ends** | goal reached or fell in a hole **H** (terminated), or 100 steps (truncated) |
| **Our setting** | non-slippery map by default (`is_slippery: false`); slippery is optional |
| **Algorithm** | Tabular Q-learning with ε-greedy exploration |
""")
            st.latex(r"Q(s,a) \leftarrow Q(s,a) + \alpha\,[\,r + \gamma \max_{a'} Q(s',a') - Q(s,a)\,]")
            st.caption("At a terminal step there is no next state, so the target is just r (no bootstrap).")
    with tab_cp:
        left, right = st.columns([2, 3])
        with left:
            try:
                import gymnasium as gym
                env = gym.make("CartPole-v1", render_mode="rgb_array")
                env.reset(seed=0)
                st.image(env.render(), caption="CartPole-v1 (rendered by Gymnasium)", width="stretch")
                env.close()
            except Exception:  # noqa: BLE001 - pygame not installed: show text only
                empty_state("Rendering needs pygame (pip install pygame); the environment itself works without it.")
        with right:
            st.markdown("""
| | |
|---|---|
| **State space** | `Box(4)` — cart position, cart velocity, pole angle, pole angular velocity |
| **Action space** | `Discrete(2)` — push the cart left (0) or right (1) |
| **Reward** | +1 for every step the pole stays up |
| **Episode ends** | pole angle > 12° or cart leaves the track (terminated), or 500 steps (truncated) |
| **Success** | an episode return of 500 (the full time limit) |
| **Algorithm** | DQN: MLP 4→128→128→2, replay buffer, target network, Huber loss, gradient clipping |
""")
            st.latex(r"y = r + \gamma\,(1 - \text{terminated})\,\max_{a'} Q_{\text{target}}(s', a')")
            st.caption("Truncation at 500 steps is not a failure, so the target still bootstraps.")
    section("Seeds", "Training, validation and test seeds never overlap.")
    st.markdown("- **Training resets:** `seed × 100 000 + episode`\n"
                "- **Validation (picks the best checkpoint):** `10 000 000 + i`\n"
                "- **Test (reported results only):** `20 000 000 + i`")
