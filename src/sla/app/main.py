"""Streamlit entry point: ``sla dashboard`` or ``streamlit run src/sla/app/main.py``."""

from __future__ import annotations

import functools
import html
import sys
from pathlib import Path

# Make "sla" importable when the package is not pip-installed (e.g. Streamlit Community Cloud).
_SRC = Path(__file__).resolve().parents[2]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import streamlit as st  # noqa: E402

from sla.app import data, demo_seed  # noqa: E402
from sla.app.components.states import error_state  # noqa: E402
from sla.app.components.status_badge import badge  # noqa: E402
from sla.app.styles.theme import inject_css  # noqa: E402
from sla.app.views import (  # noqa: E402
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

ASSETS = Path(__file__).resolve().parent / "assets"

st.set_page_config(page_title="Self-Learning AI Agent · Lab", page_icon=str(ASSETS / "icon.svg"), layout="wide",
                   initial_sidebar_state="expanded")
inject_css()
st.logo(str(ASSETS / "logo.svg"), icon_image=str(ASSETS / "icon.svg"), size="large")


@st.cache_resource(show_spinner=False)
def _seed_demo() -> bool:
    """Once per server process: give the hosted app the committed results snapshot (see demo_seed)."""
    return demo_seed.seed_if_needed()


_seed_demo()


def safe(render):
    """Show a friendly error card instead of a traceback; details stay in the log / developer expander."""
    @functools.wraps(render)
    def wrapper() -> None:
        try:
            render()
        except Exception as exc:  # noqa: BLE001 - Streamlit control-flow exceptions are BaseException
            error_state("Unable to load this page.",
                        "the experiment database could not be read, or a stored run is incomplete.",
                        "reload the page; if it persists, check that runs/sla.db exists and run `sla init-db`.", exc)
    return wrapper


PAGES = {
    "Dashboard": [
        st.Page(safe(overview.render), title="Overview", icon=":material/space_dashboard:", url_path="overview",
                default=True),
        st.Page(safe(training.render), title="Training", icon=":material/model_training:", url_path="training"),
    ],
    "Analysis": [
        st.Page(safe(comparison.render), title="Agent comparison", icon=":material/compare_arrows:",
                url_path="comparison"),
        st.Page(safe(evaluation.render), title="Evaluation", icon=":material/fact_check:", url_path="evaluation"),
        st.Page(safe(ablation.render), title="Ablation", icon=":material/science:", url_path="ablation"),
        st.Page(safe(explorer.render), title="Run explorer", icon=":material/manage_search:", url_path="runs"),
        st.Page(safe(reflection.render), title="Reflection", icon=":material/psychology:", url_path="reflection"),
    ],
    "Reference": [
        st.Page(safe(environment.render), title="Environments", icon=":material/grid_on:", url_path="environments"),
        st.Page(safe(about.render), title="About", icon=":material/info:", url_path="about"),
    ],
}


def _row(label: str, value: str) -> str:
    v = html.escape(value)
    return f'<div class="row"><span>{html.escape(label)}</span><b title="{v}">{v}</b></div>'


def sidebar_status() -> None:
    ver = data.version()
    if not ver:
        st.markdown(f'<div class="sla-side"><div class="ttl">SYSTEM</div>{badge("failed", "Database unavailable")}'
                    '<div style="margin-top:.4rem;color:var(--muted)">Run <code>sla init-db</code>.</div></div>',
                    unsafe_allow_html=True)
        return
    ov = data.overview()
    latest = ov["latest_run"]
    state = "running" if ov["running_runs"] else "idle"
    state_badge = badge(state, {"running": "Training", "completed": "Completed", "idle": "Idle",
                                "stopped": "Stopped", "failed": "Failed"}[state])
    algo = {"q_learning": "Q-learning", "dqn": "DQN"}.get(latest["algorithm"], "—") if latest else "—"
    st.markdown(
        f'<div class="sla-side"><div class="ttl">SYSTEM</div>'
        f'<div style="display:flex;gap:.35rem;flex-wrap:wrap;margin:.15rem 0 .45rem">{badge("online", "Online")}'
        f'{state_badge}</div>'
        + _row("Database", f"{ov['runs']} runs · {ov['experiments']} exps")
        + _row("Episodes", f"{ov['episodes_logged']:,}")
        + _row("Environment", latest["env"] if latest else "—")
        + _row("Algorithm", algo)
        + _row("Current run", latest["run_id"] if latest else "—")
        + "</div>", unsafe_allow_html=True)


nav = st.navigation(PAGES)
with st.sidebar:
    try:
        sidebar_status()
        snap = demo_seed.snapshot_info()
        if snap:
            c = snap.get("counts", {})
            st.markdown(f'<div class="sla-side" style="margin-top:.5rem"><div class="ttl">DATA</div>'
                        f'<div style="color:var(--secondary)">Includes a read-only snapshot of real runs '
                        f'from the project laptop: {c.get("experiments", 0)} experiments · {c.get("runs", 0)} '
                        f'runs · {c.get("episodes", 0):,} episodes. New runs you start here are added on '
                        f'top until the app restarts.</div></div>', unsafe_allow_html=True)
    except Exception as exc:  # noqa: BLE001
        error_state("Status unavailable", "the database could not be read.", "run `sla init-db`.", exc)
    st.caption("Q-learning · DQN · held-out evaluation")
nav.run()
