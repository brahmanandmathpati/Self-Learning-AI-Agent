"""'What am I looking at?' card and the Help / glossary popover shown at the top of every page."""

from __future__ import annotations

import html

import streamlit as st

from sla.app import routes
from sla.app.guide_content import FALLBACK, GUIDE, HELP_TITLE
from sla.app.how_content import GLOSSARY


def guide_for(title: str) -> tuple[str, str, str]:
    return GUIDE.get(title, FALLBACK)


def what_am_i_looking_at(title: str) -> None:
    """A short card: what the page is, what to look for, and an optional Roman-Marathi line."""
    what, look, mr = guide_for(title)
    key = "guide_mr_" + "".join(c if c.isalnum() else "_" for c in title.lower())
    with st.container(key=f"guide_{key}"):
        st.markdown(f'<div class="sla-guide" role="note"><b>What am I looking at?</b><p>{html.escape(what)}</p>'
                    f'<p><b>What to look for:</b> {html.escape(look)}</p></div>', unsafe_allow_html=True)
        if st.toggle("Marathi helper line", key=key, help="Short Roman-Marathi hint (technical words stay English)."):
            st.caption(mr)


def help_popover() -> None:
    """Persistent glossary: every term from the How-it-works page, plus a link to the full explanation."""
    with st.popover(HELP_TITLE, use_container_width=False):
        for term, meaning in GLOSSARY:
            st.markdown(f"**{term}** — {meaning}")
        routes.link("how", "Read the full explanation →", "outline", "help")


def page_header_extras(title: str) -> None:
    """Called by hero(): help button + guide card (the How page is its own guide, so it only gets the button)."""
    help_popover()
    if title != "How it works":
        what_am_i_looking_at(title)
