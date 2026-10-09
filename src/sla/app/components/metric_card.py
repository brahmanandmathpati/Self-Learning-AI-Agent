"""KPI / metric cards. ``None`` renders as NOT RUN - never a made-up number."""

from __future__ import annotations

import html
from collections.abc import Sequence

import streamlit as st

from sla.app.components.icons import icon as svg_icon

NOT_RUN = "NOT RUN"


def _value_html(value: object, fmt: str, count: bool) -> str:
    if value is None:
        return f'<div class="value notrun">{NOT_RUN}</div>'
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        text = fmt.format(value)
        # count-up only for small whole numbers whose formatted text is the bare integer
        if count and isinstance(value, int) and 0 <= value < 10_000 and text == str(value):
            return (f'<div class="value"><span class="sla-count" style="--sla-n:{value}" role="text" '
                    f'aria-label="{value}"></span></div>')
        return f'<div class="value">{html.escape(text)}</div>'
    text = str(value)
    return f'<div class="value{" sm" if len(text) > 10 else ""}">{html.escape(text)}</div>'


def metric_card(label: str, value: object, sub: str | None = None, fmt: str = "{:,.2f}", icon: str | None = None,
                accent: str | None = None, delta: str | None = None, delta_negative: bool = False,
                count: bool = True) -> str:
    """Card HTML: label (+ optional icon), value, optional delta chip and sub-text."""
    ic = f'<span class="ic">{svg_icon(icon, 14)}</span>' if icon else ""
    sub_html = f'<div class="sub">{html.escape(sub)}</div>' if sub else ""
    delta_html = (f'<div class="delta{" neg" if delta_negative else ""}">{html.escape(delta)}</div>'
                  if delta else "")
    cls = "sla-card accent" if accent else "sla-card"
    style = f' style="--card-accent:{accent}"' if accent else ""
    return (f'<div class="{cls}"{style}><div class="label">{ic}{html.escape(label)}</div>'
            f"{_value_html(value, fmt, count)}{delta_html}{sub_html}</div>")


def card_grid(cards: Sequence[str], min_width: int = 150) -> None:
    """Responsive grid of cards (wraps on narrow screens)."""
    st.markdown(f'<div class="sla-grid" style="grid-template-columns:repeat(auto-fit,minmax({min_width}px,1fr))">'
                + "".join(cards) + "</div>", unsafe_allow_html=True)


def card_row(cards: Sequence[str]) -> None:
    """Backwards-compatible alias used by older views."""
    card_grid(cards)
