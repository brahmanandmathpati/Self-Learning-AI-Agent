"""Streamlit entry point: ``sla dashboard`` or ``streamlit run src/sla/app/main.py``."""

from __future__ import annotations

import functools
import sys
from pathlib import Path

# Make "sla" importable when the package is not pip-installed (e.g. Streamlit Community Cloud).
_SRC = Path(__file__).resolve().parents[2]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import streamlit as st  # noqa: E402

from sla.app import auth, demo_seed, routes  # noqa: E402
from sla.app.components.landing import footer  # noqa: E402
from sla.app.components.states import error_state  # noqa: E402
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

st.set_page_config(page_title="Self-Learning AI Agent — learns from experience",
                   page_icon=str(ASSETS / "icon.svg"), layout="wide",
                   initial_sidebar_state="collapsed")
inject_css()
st.logo(str(ASSETS / "logo.svg"), size="large")


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


_OVERVIEW = st.Page(safe(overview.render), title="Overview", icon=":material/space_dashboard:", url_path="overview",
                    default=True)
_TRAINING = st.Page(safe(training.render), title="Training", icon=":material/model_training:", url_path="training")
_ANALYSIS = [
    st.Page(safe(comparison.render), title="Agent comparison", icon=":material/compare_arrows:", url_path="comparison"),
    st.Page(safe(evaluation.render), title="Evaluation", icon=":material/fact_check:", url_path="evaluation"),
    st.Page(safe(ablation.render), title="Ablation", icon=":material/science:", url_path="ablation"),
    st.Page(safe(explorer.render), title="Run explorer", icon=":material/manage_search:", url_path="runs"),
    st.Page(safe(reflection.render), title="Reflection", icon=":material/psychology:", url_path="reflection"),
]
_ENVS = st.Page(safe(environment.render), title="Environments", icon=":material/grid_on:", url_path="environments")
_ABOUT = st.Page(safe(about.render), title="About", icon=":material/info:", url_path="about")
# Top navbar: Overview · Training · Environments · About · Analysis ▾ ("" = pages without a dropdown).
PAGES = {"": [_OVERVIEW, _TRAINING, _ENVS, _ABOUT], "Analysis": _ANALYSIS}
routes.register({"overview": _OVERVIEW, "training": _TRAINING, "environments": _ENVS, "about": _ABOUT,
                 "comparison": _ANALYSIS[0], "evaluation": _ANALYSIS[1], "ablation": _ANALYSIS[2],
                 "runs": _ANALYSIS[3], "reflection": _ANALYSIS[4]})

nav = st.navigation(PAGES, position="top")
auth.topbar()
nav.run()
footer()
