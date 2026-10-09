"""Page hero and section headers."""

from __future__ import annotations

import html

import streamlit as st


def hero(title: str, subtitle: str, right_html: str = "", eyebrow: str = "AI Learning Laboratory",
         big: bool = False) -> None:
    eb = f'<div class="eyebrow">{html.escape(eyebrow)}</div>' if eyebrow else ""
    st.markdown(f'<div class="sla-hero{" big" if big else ""}"><div>{eb}<h1>{html.escape(title)}</h1>'
                f'<p>{html.escape(subtitle)}</p></div><div class="right">{right_html}</div></div>',
                unsafe_allow_html=True)


def section(title: str, caption: str | None = None, right_html: str = "") -> None:
    cap = f"<p>{html.escape(caption)}</p>" if caption else ""
    st.markdown(f'<div class="sla-section"><div><h3>{html.escape(title)}</h3>{cap}</div><div>{right_html}</div></div>',
                unsafe_allow_html=True)
