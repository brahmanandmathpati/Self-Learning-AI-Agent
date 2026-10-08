"""About: objective, architecture, technology, team, limitations and future work."""

from __future__ import annotations

import streamlit as st

from sla import __version__
from sla.app.components.ui import hero, section

ARCH = """
digraph G {
  rankdir=TB; bgcolor="transparent"; nodesep=0.35; ranksep=0.35;
  node [shape=box, style="rounded,filled", fillcolor="#1a1a19",
  color="#383835", fontcolor="#ffffff", fontname="Helvetica", fontsize=11]; edge [color="#898781"];
  UI [label="Streamlit dashboard\\n(app/pages, components, charts)"];
  CLI [label="CLI  sla ..."];
  SVC [label="Service layer\\nTraining · Evaluation · Experiment\\nReflection · Checkpoint"];
  PIPE [label="Training pipeline\\n(train_run, run_experiment,\\nrun_ablation)"];
  RUN [label="Runner + callbacks\\n(the only place learning happens)", fillcolor="#173a63"];
  ENV [label="Gymnasium env\\nFrozenLake / CartPole"];
  AG [label="Agents\\nRandom · Q-learning · DQN"];
  BUF [label="Replay buffer"];
  CK [label="Checkpoints\\n(best / latest)"];
  DB [label="SQLite\\nexperiments · runs · episodes\\nmetrics · evaluations\\nablation · reflections", shape=cylinder];
  EV [label="Evaluation\\nfrozen policy · stats"];
  RF [label="Reflection\\nfacts → template / Ollama\\n→ number check"];
  UI -> SVC; CLI -> SVC; SVC -> PIPE; PIPE -> RUN; RUN -> ENV [dir=both]; RUN -> AG [dir=both];
  AG -> BUF [dir=both]; RUN -> CK; RUN -> DB; PIPE -> EV; EV -> DB; CK -> EV; SVC -> RF; RF -> DB; SVC -> DB;
}
"""


def render() -> None:
    hero("About the project", f"Final-year B.Tech CSE (AI) project · version {__version__}")
    section("Objective")
    st.markdown("Build an agent that **starts with no trained policy and measurably improves through reinforcement "
                "learning** — and prove it with held-out evaluation, statistics and an ablation study. Learning "
                "happens only in the Q-table or network weights; LLM text, chat history or prompt changes are "
                "*not* counted as learning.")
    section("Architecture")
    st.graphviz_chart(ARCH, width="stretch")
    c1, c2 = st.columns(2)
    with c1:
        section("Technology stack")
        st.markdown("| Layer | Technology |\n|---|---|\n| Frontend | Streamlit, Plotly |\n"
                    "| Application | Python service layer + CLI (argparse) |\n"
                    "| RL | Gymnasium, NumPy, PyTorch (CPU) |\n"
                    "| Statistics | SciPy (Welch's t-test), bootstrap CI |\n| Database | SQLite (versioned schema) |\n"
                    "| Explanation | Template + optional local Ollama (qwen2.5:1.5b) |\n"
                    "| Quality | pytest, ruff, GitHub Actions |")
        section("Team")
        st.markdown("- Brahmanand Mathpati\n- Atharv Gundale\n- Vedant Biradar\n- Somesh Badwane")
    with c2:
        section("Limitations")
        st.markdown("- Two small benchmark tasks; bounded single-task learning, not general intelligence.\n"
                    "- 5 seeds give wide confidence intervals; results vary across hardware.\n"
                    "- CartPole DQN results are sensitive to hyper-parameters.\n"
                    "- The LLM explains results; it does not learn and is never required.")
        section("Future work")
        st.markdown("- Double / dueling DQN and prioritised replay.\n- Harder environments (e.g. LunarLander).\n"
                    "- More seeds and hyper-parameter sweeps.\n- Live training in a background worker.")
