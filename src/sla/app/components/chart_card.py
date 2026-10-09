"""Charts inside a bordered card, with a consistent Plotly toolbar (zoom, pan, reset, download)."""

from __future__ import annotations

import html
import re

import plotly.graph_objects as go
import streamlit as st

PLOTLY_CONFIG = {
    "displaylogo": False, "responsive": True, "scrollZoom": False,
    "modeBarButtonsToRemove": ["lasso2d", "select2d", "autoScale2d", "toggleSpikelines"],
    "toImageButtonOptions": {"format": "png", "scale": 2},
}


def _key(text: str) -> str:
    return re.sub(r"[^a-z0-9_]+", "_", text.lower()).strip("_")[:60] or "chart"


def plot(fig: go.Figure, key: str | None = None) -> None:
    st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG, key=key)


def chart_card(fig: go.Figure, title: str | None = None, sub: str | None = None, key: str | None = None) -> None:
    """Render ``fig`` in a card. ``key`` must be unique on the page."""
    k = _key(key or title or "chart")
    with st.container(key=f"card_{k}"):
        if title:
            st.markdown(f'<p class="sla-chart-title">{html.escape(title)}</p>'
                        + (f'<p class="sla-chart-sub">{html.escape(sub)}</p>' if sub else ""), unsafe_allow_html=True)
        plot(fig, key=f"plot_{k}")
