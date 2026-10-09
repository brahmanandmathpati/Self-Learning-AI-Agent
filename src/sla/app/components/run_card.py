"""Run summary header and readable key/value configuration (instead of raw JSON)."""

from __future__ import annotations

import html
from typing import Any

import streamlit as st

from sla.app.components.status_badge import badge

ALGO = {"q_learning": "Q-learning", "dqn": "DQN", "random": "Random"}


def algo_label(algorithm: str | None, variant: str | None = None) -> str:
    name = ALGO.get(algorithm or "", algorithm or "—")
    if variant and variant not in ("full",):
        name += f" · {variant}"
    return name


def flatten(cfg: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in cfg.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(flatten(v, key + "."))
        else:
            out[key] = v
    return out


def kv_grid(values: dict[str, Any]) -> None:
    cells = "".join(f'<div><div class="k">{html.escape(str(k))}</div><div class="v">{html.escape(str(v))}</div></div>'
                    for k, v in values.items())
    st.markdown(f'<div class="sla-kv">{cells}</div>', unsafe_allow_html=True)


def run_header(run: dict[str, Any]) -> None:
    st.markdown(
        f'<div class="sla-panel sla-anim" style="display:flex;flex-wrap:wrap;gap:.8rem;align-items:center;'
        f'justify-content:space-between"><div><div style="font-size:.7rem;letter-spacing:.16em;color:var(--muted);'
        f'font-weight:700">RUN ID</div><div class="mono" style="color:var(--ink);font-size:.95rem;'
        f'word-break:break-all">{html.escape(run["run_id"])}</div></div><div>{badge(run["status"])}</div></div>',
        unsafe_allow_html=True)
