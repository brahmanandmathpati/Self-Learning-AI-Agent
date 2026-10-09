"""Facade for the UI components (kept so existing imports keep working)."""

from __future__ import annotations

import html

import streamlit as st

from sla.app.components.metric_card import NOT_RUN, card_grid, card_row, metric_card
from sla.app.components.section_header import hero, section
from sla.app.components.states import empty_state, error_state, skeleton, verdict
from sla.app.components.status_badge import badge

__all__ = ["NOT_RUN", "badge", "card_grid", "card_row", "empty_state", "error_state", "fmt_num", "hero",
           "metric_card", "note_box", "section", "skeleton", "verdict"]


def note_box(text: str) -> None:
    st.markdown(f'<div class="sla-panel">{html.escape(text)}</div>', unsafe_allow_html=True)


def fmt_num(value: object, nd: int = 2) -> str:
    if value is None:
        return NOT_RUN
    try:
        return f"{float(value):,.{nd}f}"
    except (TypeError, ValueError):
        return str(value)
