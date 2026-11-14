"""Environments: what the agent sees, what it can do and how it is rewarded — four Gymnasium games."""

from __future__ import annotations

import streamlit as st

from sla import settings
from sla.app import data
from sla.app.charts.figures import grid_map
from sla.app.components.chart_card import chart_card
from sla.app.components.metric_card import metric_card
from sla.app.components.ui import empty_state, hero, section
from sla.app.state import services
from sla.catalog import algo_label
from sla.evaluation.policies import ARROWS, CLIFF_DESC, FROZENLAKE_DESC, learned, walk

TAXI_MAP = """+---------+
|R: | : :G|
| : | : : |
| : : : : |
| | : | : |
|Y| : |B: |
+---------+"""


def _env_cards(items: list[tuple[str, str, str, str]]) -> None:
    st.markdown('<div class="sla-env-row">' + "".join(metric_card(label, value, sub, icon=ic, count=False)
                                                      for label, value, sub, ic in items) + "</div>",
                unsafe_allow_html=True)


@st.cache_data(ttl=300, show_spinner=False)
def _policy(db: str, ver: tuple, env_name: str, algorithm: str) -> dict | None:
    return learned(services().db, env_name, algorithm)


def _policy_map(env_name: str, algorithm: str, desc: list[str], key: str, height: int) -> None:
    pol = _policy(str(settings.db_path()), data.version(), env_name, algorithm)
    if pol is None:
        chart_card(grid_map(desc, height=height), "Map", None, key=key)
        st.caption(f"Train {algo_label(algorithm)} on this game to see its learned moves drawn on the grid.")
        return
    arrows = [ARROWS[env_name][a] for a in pol["actions"]]
    path = set(walk(env_name, pol["actions"]))
    chart_card(grid_map(desc, arrows, pol["values"], height=height, path=path),
               f"{algo_label(algorithm)} — learned path", "gold squares = the path it walks with ε = 0", key=key)
    src = "best checkpoint" if pol["source"] == "checkpoint" else "best checkpoint (saved snapshot)"
    st.caption(f"Arrows = argmax_a Q(s, a) from the {src} of run {pol['run_id']}; "
               f"path length {len(walk(env_name, pol['actions'])) - 1} steps.")


def _frozenlake() -> None:
    _env_cards([
        ("Goal", "Walk from START to GOAL without falling into a hole", "4×4 frozen lake", "target"),
        ("State space", "16 squares", "the agent's cell on the grid · Discrete(16)", "eye"),
        ("Action space", "4 moves", "left · down · right · up · Discrete(4)", "move"),
        ("Reward", "+1 at the goal, 0 otherwise", "sparse; ends at goal, hole or 100 steps", "gift"),
    ])
    st.write("")
    left, right = st.columns([2, 3], gap="medium")
    with left:
        algo = st.segmented_control("Agent", ["q_learning", "sarsa", "expected_sarsa"], default="q_learning",
                                    format_func=algo_label, key="env_fl_algo") or "q_learning"
        _policy_map("FrozenLake-v1", algo, FROZENLAKE_DESC, "env_fl", 360)
    with right:
        st.markdown("""
| | |
|---|---|
| **Episode ends** | goal reached or fell in a hole **H** (terminated), or 100 steps (truncated) |
| **Our setting** | non-slippery map by default (`is_slippery: false`); slippery is optional |
| **Algorithms** | Q-learning, SARSA and Expected SARSA (all keep a 16 × 4 Q-table) |
""")
        st.latex(r"Q(s,a) \leftarrow Q(s,a) + \alpha\,[\,r + \gamma \max_{a'} Q(s',a') - Q(s,a)\,]")
        st.caption("At a terminal step there is no next state, so the target is just r (no bootstrap).")


def _taxi() -> None:
    _env_cards([
        ("Goal", "Pick up the passenger and drop them at their destination", "5×5 city, 4 stops R · G · Y · B",
         "target"),
        ("State space", "500 situations", "taxi square (25) × passenger place (5) × destination (4) · Discrete(500)",
         "eye"),
        ("Action space", "6 actions", "south · north · east · west · pick up · drop off · Discrete(6)", "move"),
        ("Reward", "+20 delivery, −1 per step", "−10 for an illegal pick-up or drop-off; 200-step limit", "gift"),
    ])
    st.write("")
    left, right = st.columns([2, 3], gap="medium")
    with left:
        st.code(TAXI_MAP, language=None)
        st.caption("Gymnasium's Taxi map: | = wall the taxi cannot cross, R G Y B = the four stops.")
    with right:
        st.markdown("""
| | |
|---|---|
| **Episode ends** | passenger delivered to the right stop (terminated), or 200 steps (truncated) |
| **Success** | the passenger was delivered (the episode really ended, not cut off) |
| **Why it is harder** | 500 situations instead of 16, so the table needs many more games to fill in |
| **Algorithms** | Q-learning, SARSA and Expected SARSA (500 × 6 Q-table each) |
""")
        st.latex(r"\text{SARSA: } Q(s,a) \leftarrow Q(s,a) + \alpha\,[\,r + \gamma\,Q(s',a') - Q(s,a)\,]")
        st.caption("a′ is the move SARSA really makes next (exploring moves included) — that is the only change "
                   "from Q-learning.")


def _cliff() -> None:
    _env_cards([
        ("Goal", "Walk from START to GOAL along the cliff without falling", "4×12 grid", "target"),
        ("State space", "48 squares", "the agent's cell · Discrete(48)", "eye"),
        ("Action space", "4 moves", "up · right · down · left · Discrete(4)", "move"),
        ("Reward", "−1 per step, −100 off the cliff", "falling sends you back to START; 200-step limit", "gift"),
    ])
    st.write("")
    st.markdown("**Same game, same settings, different learning rule.** Exploration stays at 10%, so random moves "
                "near the edge are dangerous. Q-learning learns the shortest path right along the edge; SARSA, which "
                "learns from the moves it really makes, learns a safer path further away.")
    left, right = st.columns(2, gap="medium")
    with left:
        _policy_map("CliffWalking-v1", "q_learning", CLIFF_DESC, "env_cliff_q", 260)
    with right:
        _policy_map("CliffWalking-v1", "sarsa", CLIFF_DESC, "env_cliff_s", 260)
    with st.expander("Expected SARSA on the same map"):
        _policy_map("CliffWalking-v1", "expected_sarsa", CLIFF_DESC, "env_cliff_e", 260)
    st.latex(r"\text{Expected SARSA: } Q(s,a) \leftarrow Q(s,a) + \alpha\,[\,r + \gamma \sum_{a'} \pi(a'\mid s')\,"
             r"Q(s',a') - Q(s,a)\,]")
    st.caption("π is the ε-greedy policy: the best move with probability 1 − ε + ε/4, each other move ε/4.")


def _cartpole() -> None:
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


def render() -> None:
    hero("Environments", "Four Gymnasium games: three grids solved with a Q-table (Q-learning, SARSA, Expected "
         "SARSA) and one control task solved with a DQN.", eyebrow="Reference")
    tabs = st.tabs(["FrozenLake-v1", "Taxi-v4", "CliffWalking-v1", "CartPole-v1 · DQN"])
    for tab, draw in zip(tabs, (_frozenlake, _taxi, _cliff, _cartpole)):
        with tab:
            draw()
    section("Seeds", "Training, validation and test seeds never overlap.")
    st.markdown("- **Training resets:** `seed × 100 000 + episode`\n"
                "- **Validation (picks the best checkpoint):** `10 000 000 + i`\n"
                "- **Test (reported results only):** `20 000 000 + i`")
