"""Streamlit entry point: ``sla dashboard`` or ``streamlit run src/sla/app/main.py``."""

from __future__ import annotations

import streamlit as st

from sla.app.state import services
from sla.app.styles.theme import inject_css
from sla.app.views import (
    ablation,
    about,
    comparison,
    environment,
    evaluation,
    explorer,
    overview,
    reflection,
    training,
)

st.set_page_config(page_title="Self-Learning AI Agent", page_icon="🧠", layout="wide",
                   initial_sidebar_state="expanded")
inject_css()

PAGES = {
    "Dashboard": [
        st.Page(overview.render, title="Overview", icon=":material/space_dashboard:", url_path="overview",
                default=True),
        st.Page(training.render, title="Training", icon=":material/model_training:", url_path="training"),
    ],
    "Analysis": [
        st.Page(comparison.render, title="Agent comparison", icon=":material/compare_arrows:", url_path="comparison"),
        st.Page(evaluation.render, title="Evaluation", icon=":material/fact_check:", url_path="evaluation"),
        st.Page(ablation.render, title="Ablation", icon=":material/science:", url_path="ablation"),
        st.Page(explorer.render, title="Run explorer", icon=":material/manage_search:", url_path="runs"),
        st.Page(reflection.render, title="Reflection", icon=":material/psychology:", url_path="reflection"),
    ],
    "Reference": [
        st.Page(environment.render, title="Environments", icon=":material/grid_on:", url_path="environments"),
        st.Page(about.render, title="About", icon=":material/info:", url_path="about"),
    ],
}

nav = st.navigation(PAGES)
with st.sidebar:
    st.markdown("### 🧠 Self-Learning AI Agent")
    st.caption("Reinforcement learning that measurably improves: Q-learning · DQN · held-out evaluation")
    try:
        counts = services().db.counts()
        st.caption(f"Database: {counts['runs']} runs · {counts['experiments']} experiments · "
                   f"{counts['episodes']:,} episodes logged")
    except Exception as exc:  # noqa: BLE001 - show the problem instead of a blank page
        st.error(f"Database unavailable: {exc}")
nav.run()
