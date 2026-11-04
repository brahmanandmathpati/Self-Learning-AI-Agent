"""Landing-style blocks: hero buttons, how-it-works steps, feature cards, tech chips, team cards, footer."""

from __future__ import annotations

import base64
import html
from collections.abc import Sequence
from pathlib import Path

import streamlit as st

from sla.app.components.icons import icon

GITHUB = "https://github.com/brahmanandmathpati/Self-Learning-AI-Agent"
LIVE = "https://self-learning-ai-agent-final-year-project.streamlit.app/"
REPORT = ""  # TODO: link to the hosted project report PDF (e.g. a GitHub release asset)
TEAM_PHOTOS = Path(__file__).resolve().parents[1] / "assets" / "team"


def _links(github: str = "", linkedin: str = "") -> str:
    """Profile links; a missing one shows a TODO so it is easy to spot and fill in."""
    out = []
    for label, url in (("GitHub", github), ("LinkedIn", linkedin)):
        out.append(f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{label}</a>' if url
                   else f'<span class="todo" title="TODO: add {label} link">{label}: TODO</span>')
    return " · ".join(out)


# (name, role, links). Photos: put <first-last>.jpg/.png/.webp in src/sla/app/assets/team/ (e.g. atharv-gundale.jpg).
TEAM = [
    ("Brahmanand Mathpati", "Agent core — Q-learning, DQN, tuning, failure analysis",
     _links("https://github.com/brahmanandmathpati", "https://www.linkedin.com/in/brahmanand-mathpati")),
    ("Atharv Gundale", "Environments, training runner and CLI, CI and release", _links()),
    ("Vedant Biradar", "Experience memory, evaluation, statistics, ablations", _links()),
    ("Somesh Badwane", "Reflection layer, grounding check, dashboard, demo", _links()),
]


def actions(buttons: Sequence[tuple[str, str, str]]) -> str:
    """HTML for buttons: (label, href, 'gold' | 'outline'). Internal pages open in the same tab."""
    out = []
    for label, href, kind in buttons:
        target = ' target="_blank" rel="noopener"' if href.startswith("http") else ' target="_self"'
        arrow = ' <span class="arr" aria-hidden="true">→</span>' if kind == "gold" else ""
        out.append(f'<a class="sla-btn {kind}" href="{html.escape(href)}"{target}>{html.escape(label)}{arrow}</a>')
    return '<div class="sla-actions">' + "".join(out) + "</div>"


def steps(items: Sequence[tuple[str, str]]) -> None:
    st.markdown('<div class="sla-steps">' + "".join(
        f'<div class="sla-step"><div class="n">{i}</div><h4>{html.escape(t)}</h4><p>{html.escape(d)}</p></div>'
        for i, (t, d) in enumerate(items, 1)) + "</div>", unsafe_allow_html=True)


def features(items: Sequence[tuple[str, str, str]], min_width: int = 250) -> None:
    grid = f'<div class="sla-grid" style="grid-template-columns:repeat(auto-fit,minmax({min_width}px,1fr))">'
    st.markdown(grid + "".join(
        f'<div class="sla-feature"><div class="fi">{icon(ic, 18)}</div><h4>{html.escape(t)}</h4>'
        f'<p>{html.escape(d)}</p></div>' for ic, t, d in items) + "</div>", unsafe_allow_html=True)


def stack(names: Sequence[str]) -> None:
    st.markdown('<div class="sla-stack">' + "".join(f"<span>{html.escape(n)}</span>" for n in names) + "</div>",
                unsafe_allow_html=True)


def photo(name: str) -> str:
    """Data-URI <img> for assets/team/<first-last>.(jpg|jpeg|png|webp), or "" when there is no photo."""
    slug = "-".join(name.lower().split())
    for ext, mime in (("jpg", "jpeg"), ("jpeg", "jpeg"), ("png", "png"), ("webp", "webp")):
        f = TEAM_PHOTOS / f"{slug}.{ext}"
        if f.is_file():
            data = base64.b64encode(f.read_bytes()).decode()
            return f'<img src="data:image/{mime};base64,{data}" alt="Photo of {html.escape(name)}">'
    return ""


def team(members: Sequence[tuple[str, str, str]]) -> None:
    """(name, role, links_html). Shows a photo from assets/team/ when present, otherwise the initials."""
    cards = []
    for name, role, links in members:
        face = photo(name) or "".join(p[0] for p in name.split()[:2]).upper()
        cards.append(f'<div class="sla-member"><div class="av" aria-hidden="true">{face}</div>'
                     f'<h4>{html.escape(name)}</h4>'
                     f'<div class="role">{html.escape(role)}</div><div class="links">{links}</div></div>')
    st.markdown('<div class="sla-team">' + "".join(cards) + "</div>", unsafe_allow_html=True)


def footer() -> None:
    report = (f'<a href="{REPORT}" target="_blank" rel="noopener">Project report</a>' if REPORT
              else '<span title="TODO: add the report link">Project report (link coming soon)</span>')
    st.markdown(
        f'<footer class="sla-footer"><div><div class="brand">Self-Learning AI Agent</div>'
        f'<div>Final-year B.Tech CSE (AI) project · © 2026 Brahmanand Mathpati, Atharv Gundale, '
        f'Vedant Biradar, Somesh Badwane</div></div>'
        f'<nav aria-label="Footer"><a href="{GITHUB}" target="_blank" rel="noopener">GitHub</a>'
        f'<a href="{LIVE}" target="_blank" rel="noopener">Live app</a>{report}</nav></footer>', unsafe_allow_html=True)


def results_table(rows: Sequence[tuple[str, str, str, str, str, str]]) -> None:
    """Proof table: (game, agent, trained, random, gain, p-value) — values come from stored experiments."""
    head = "".join(f"<th>{h}</th>" for h in ("Game", "Agent", "Trained", "Random", "Gain (95% CI)", "Welch p"))
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    st.markdown(f'<div class="sla-proof"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>',
                unsafe_allow_html=True)


_LAYERS = [("Dashboard &amp; CLI", "Streamlit pages · sla commands"),
           ("Services", "training · evaluation · reflection"),
           ("Training pipeline", "runs, experiments, ablations"), ("Runner", "the only place learning happens"),
           ("Agents ⇄ Environments", "Q-learning · DQN ⇄ FrozenLake · CartPole"),
           ("Vision Lab", "hand points → k-NN / small network · gestures as rewards"),
           ("SQLite + checkpoints", "every episode, test and note is stored")]


def architecture() -> str:
    """Layered architecture as a simple animated stack (decorative + informative)."""
    rows = "".join(f'<div class="lay" style="animation-delay:{i * 0.08:.2f}s"><b>{t}</b><span>{d}</span></div>'
                   for i, (t, d) in enumerate(_LAYERS))
    return f'<div class="sla-arch">{rows}</div>'


def faq(items: Sequence[tuple[str, str]]) -> None:
    for q, a in items:
        with st.expander(q):
            st.markdown(a)
