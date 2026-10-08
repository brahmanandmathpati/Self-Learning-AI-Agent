"""Reusable UI components: hero header, metric cards, badges, section headers, empty states."""

from __future__ import annotations

import html
from collections.abc import Sequence

import streamlit as st

from sla.app.styles.theme import INK, STATUS

NOT_RUN = "NOT RUN"

_STATUS_STYLE = {
    "completed": (STATUS["good"], "✓", "Completed"),
    "running": (STATUS["warning"], "●", "Running"),
    "stopped": (STATUS["serious"], "■", "Stopped"),
    "failed": (STATUS["critical"], "✕", "Failed"),
    "pass": (STATUS["good"], "✓", "Grounded"),
    "reject": (STATUS["critical"], "✕", "Rejected"),
    "online": (STATUS["good"], "●", "Online"),
    "offline": (INK["muted"], "○", "Offline"),
}


def hero(title: str, subtitle: str, right_html: str = "") -> None:
    st.markdown(f'<div class="sla-hero"><div><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>'
                f"<div>{right_html}</div></div>", unsafe_allow_html=True)


def badge(kind: str, text: str | None = None) -> str:
    """Status badge HTML: an icon + label, never colour alone."""
    color, icon, label = _STATUS_STYLE.get(kind, (INK["muted"], "•", kind.title()))
    return (f'<span class="sla-badge"><span style="color:{color}">{icon}</span>'
            f"{html.escape(text or label)}</span>")


def metric_card(label: str, value: object, sub: str | None = None, fmt: str = "{:,.2f}") -> str:
    """Card HTML. ``None`` values render as NOT RUN - never a made-up number."""
    if value is None:
        value_html = f'<div class="value notrun">{NOT_RUN}</div>'
    else:
        text = fmt.format(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else str(value)
        value_html = f'<div class="value">{html.escape(text)}</div>'
    sub_html = f'<div class="sub">{html.escape(sub)}</div>' if sub else ""
    return f'<div class="sla-card"><div class="label">{html.escape(label)}</div>{value_html}{sub_html}</div>'


def card_row(cards: Sequence[str]) -> None:
    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        col.markdown(card, unsafe_allow_html=True)


def section(title: str, caption: str | None = None) -> None:
    cap = f"<p>{html.escape(caption)}</p>" if caption else ""
    st.markdown(f'<div class="sla-section"><h3>{html.escape(title)}</h3>{cap}</div>', unsafe_allow_html=True)


def empty_state(message: str, command: str | None = None) -> None:
    cmd = f"<div style='margin-top:.6rem'><code>{html.escape(command)}</code></div>" if command else ""
    st.markdown(f'<div class="sla-empty"><b>{NOT_RUN}</b><div style="margin-top:.4rem">{html.escape(message)}</div>'
                f"{cmd}</div>", unsafe_allow_html=True)


def note_box(text: str) -> None:
    st.markdown(f'<div class="sla-note">{html.escape(text)}</div>', unsafe_allow_html=True)


def fmt_num(value: object, nd: int = 2) -> str:
    if value is None:
        return NOT_RUN
    try:
        return f"{float(value):,.{nd}f}"
    except (TypeError, ValueError):
        return str(value)
