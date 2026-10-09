"""Empty, error, loading and verdict states."""

from __future__ import annotations

import html
import logging
import traceback

import streamlit as st

from sla.app.components.icons import icon as svg_icon
from sla.app.components.metric_card import NOT_RUN
from sla.app.styles.theme import STATUS

log = logging.getLogger("sla.app")


def empty_state(what: str, command: str | None = None, next_step: str | None = None, glyph: str = "inbox",
                tag: str = NOT_RUN) -> None:
    """What is missing + what to do next (+ an optional terminal command)."""
    nxt = f'<div class="next">{html.escape(next_step)}</div>' if next_step else ""
    cmd = f"<code>{html.escape(command)}</code>" if command else ""
    st.markdown(f'<div class="sla-empty"><div class="glyph">{svg_icon(glyph, 20)}</div>'
                f'<div class="tag">{html.escape(tag)}</div><div class="what">{html.escape(what)}</div>{nxt}{cmd}</div>',
                unsafe_allow_html=True)


def error_state(title: str, cause: str, action: str, exc: BaseException | None = None) -> None:
    """Friendly error card; full details are logged and available in a collapsed developer section."""
    st.markdown(f'<div class="sla-error"><div class="t">{svg_icon("alert", 16)} &nbsp;{html.escape(title)}</div>'
                f'<div class="r"><b>Possible cause:</b> {html.escape(cause)}</div>'
                f'<div class="r"><b>Recommended action:</b> {html.escape(action)}</div></div>', unsafe_allow_html=True)
    if exc is not None:
        log.exception("%s", title, exc_info=exc)
        with st.expander("Developer details"):
            st.code("".join(traceback.format_exception(type(exc), exc, exc.__traceback__))[-4000:], language="text")


def skeleton(n: int = 4, height: int = 92) -> str:
    return ('<div class="sla-grid">' + "".join(f'<div class="sla-skel" style="--h:{height}px"></div>'
                                               for _ in range(n)) + "</div>")


VERDICT = {
    "verified": (STATUS["good"], "✓", "LEARNING VERIFIED"),
    "insufficient": (STATUS["warning"], "!", "INSUFFICIENT EVIDENCE"),
    "notrun": ("#7d879c", "–", NOT_RUN),
}


def verdict(kind: str, detail: str) -> None:
    color, ic, title = VERDICT[kind]
    st.markdown(f'<div class="sla-verdict" style="--c:{color}"><div class="icon">{ic}</div><div>'
                f'<div class="t">{title}</div><div class="d">{html.escape(detail)}</div></div></div>',
                unsafe_allow_html=True)
