"""In-app links that keep the session (and therefore the sign-in) alive.

Plain HTML ``<a href>`` links reload the browser page, which starts a new Streamlit session and signs the user
out. ``main.py`` registers its ``st.Page`` objects here, and views link to them with ``st.page_link``. When a view
is rendered on its own (unit tests), no pages are registered and a plain link is used instead.
"""

from __future__ import annotations

import html
from urllib.parse import urlsplit

import streamlit as st

PAGES: dict[str, object] = {}


def register(pages: dict[str, object]) -> None:
    PAGES.update(pages)


def link(name: str, label: str, kind: str = "gold", key: str = "") -> None:
    """A pill-styled link to an app page. ``kind`` is 'gold' (main action) or 'outline'."""
    with st.container(key=f"cta_{kind}_{key or name}"):
        page = PAGES.get(name)
        if page is not None:
            st.page_link(page, label=label)
        else:
            st.markdown(f'<a class="sla-btn {kind}" href="{html.escape(name)}" target="_self">{html.escape(label)}</a>',
                        unsafe_allow_html=True)


LIVE = "https://self-learning-ai-agent-final-year-project.streamlit.app/"


def base_url() -> str:
    """scheme://host/ of the page the visitor is on (falls back to the live app address)."""
    try:
        url = st.context.url
        parts = urlsplit(url if isinstance(url, str) else "")
        if parts.scheme and parts.netloc:
            return f"{parts.scheme}://{parts.netloc}/"
    except Exception:  # noqa: BLE001 - st.context.url is unavailable in bare/test mode
        pass
    return LIVE
