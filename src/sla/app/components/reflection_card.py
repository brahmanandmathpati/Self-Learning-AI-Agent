"""Reflection 'learning insight' card and the data-source chips it is grounded in."""

from __future__ import annotations

import html
from typing import Any

import streamlit as st

from sla.app.components.icons import icon as svg_icon
from sla.app.components.status_badge import badge

# fact key -> label shown as a data source (only keys that exist in the facts are shown)
SOURCES = [
    ("first_window_mean", "Avg reward · first window"), ("last_window_mean", "Avg reward · last window"),
    ("best_episode_reward", "Best episode reward"), ("best_validation_mean", "Best validation score"),
    ("untrained_test_mean", "Untrained test score"), ("test_mean", "Evaluation score"),
    ("test_success_rate", "Test success rate"), ("random_baseline_mean", "Random baseline"),
    ("welch_p_value_vs_random", "Welch p vs random"), ("diff_vs_random_ci95", "95% CI of difference"),
    ("total_episodes", "Training episodes"), ("final_epsilon", "Final ε"), ("last_window_mean_loss", "Recent loss"),
    ("n_seeds", "Seeds in experiment"),
]


def _fmt(v: Any) -> str:
    if isinstance(v, (list, tuple)) and len(v) == 2:
        return f"[{float(v[0]):,.2f}, {float(v[1]):,.2f}]"
    if isinstance(v, float):
        return f"{v:,.4g}" if abs(v) < 0.01 and v != 0 else f"{v:,.2f}"
    return str(v)


def insight_card(text: str, passed: bool, source: str, meta: str) -> None:
    st.markdown(
        f'<div class="sla-insight"><div class="h"><div class="k">{svg_icon("spark", 15)} LEARNING INSIGHT</div>'
        f'<div>{badge("pass" if passed else "reject")} {badge("info", source)}</div></div>'
        f'<div class="body">{html.escape(text)}</div><div class="meta">{html.escape(meta)}</div></div>',
        unsafe_allow_html=True)


def data_sources(facts: dict[str, Any]) -> None:
    chips = "".join(f'<div class="sla-chip"><span class="ck">{html.escape(label)}</span>'
                    f'<span class="cv">{html.escape(_fmt(facts[k]))}</span></div>'
                    for k, label in SOURCES if facts.get(k) is not None)
    if chips:
        st.markdown(f'<div class="sla-chips">{chips}</div>', unsafe_allow_html=True)
