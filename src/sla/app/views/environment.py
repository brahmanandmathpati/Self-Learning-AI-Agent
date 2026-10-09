"""Environments: what the agent sees, what it can do and how it is rewarded."""

from __future__ import annotations

import numpy as np
import streamlit as st

from sla import settings
from sla.app import data
from sla.app.charts.figures import frozenlake_map
from sla.app.components.chart_card import chart_card
from sla.app.components.metric_card import metric_card
from sla.app.components.ui import empty_state, hero, section
from sla.app.state import services

ARROWS = ["←", "↓", "→", "↑"]


def _env_cards(items: list[tuple[str, str, str, str]]) -> None:
    st.markdown('<div class="sla-env-row">' + "".join(metric_card(label, value, sub, icon=ic, count=False)
                                                      for label, value, sub, ic in items) + "</div>",
                unsafe_allow_html=True)


@st.cache_data(ttl=300, show_spinner=False)
def _policy_cached(db: str, ver: tuple) -> tuple[list[str] | None, np.ndarray | None, str | None]:
    return _frozenlake_policy(services())


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
    hero("Environments", "Two Gymnasium tasks: a grid solved with a Q-table and a control task solved with a DQN.",
         eyebrow="Reference")
    tab_fl, tab_cp = st.tabs(["FrozenLake-v1 · tabular Q-learning", "CartPole-v1 · Deep Q-Network"])
    with tab_fl:
        _env_cards([
            ("Goal", "Walk from START to GOAL without falling into a hole", "4×4 frozen lake", "target"),
            ("State space", "16 squares", "the agent's cell on the grid · Discrete(16)", "eye"),
            ("Action space", "4 moves", "left · down · right · up · Discrete(4)", "move"),
            ("Reward", "+1 at the goal, 0 otherwise", "sparse; ends at goal, hole or 100 steps", "gift"),
        ])
        st.write("")
        left, right = st.columns([2, 3], gap="medium")
        desc = ["SFFF", "FHFH", "FFFH", "HFFG"]
        arrows, values, run_id = _policy_cached(str(settings.db_path()), data.version())
        with left:
            chart_card(frozenlake_map(desc, arrows, values), "Learned policy" if run_id else "Map",
                       "arrows = preferred move after training" if run_id else None, key="env_fl")
            if run_id:
                st.caption(f"Arrows = greedy action argmax_a Q(s, a) learned by run {run_id}; V = max_a Q(s, a).")
            else:
                st.caption("Train Q-learning on the non-slippery map to see the learned policy drawn on the grid.")
        with right:
            st.markdown("""
| | |
|---|---|
| **Episode ends** | goal reached or fell in a hole **H** (terminated), or 100 steps (truncated) |
| **Our setting** | non-slippery map by default (`is_slippery: false`); slippery is optional |
| **Algorithm** | Tabular Q-learning with ε-greedy exploration |
""")
            st.latex(r"Q(s,a) \leftarrow Q(s,a) + \alpha\,[\,r + \gamma \max_{a'} Q(s',a') - Q(s,a)\,]")
            st.caption("At a terminal step there is no next state, so the target is just r (no bootstrap).")
    with tab_cp:
        _env_cards([
            ("Goal", "Keep the pole upright and the cart on the track", "balance as long as possible", "target"),
            ("State space", "4 numbers", "cart position · velocity · pole angle · angular velocity · Box(4)", "eye"),
            ("Action space", "2 pushes", "push the cart left or right · Discrete(2)", "move"),
            ("Reward", "+1 per step balanced", "ends at > 12° or off-track; 500 steps = success", "gift"),
        ])
        st.write("")
        left, right = st.columns([2, 3], gap="medium")
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
