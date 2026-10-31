"""Page hero and section headers."""

from __future__ import annotations

import html

import streamlit as st


def _words(title: str, gold_last: int = 1) -> str:
    """Headline split into words that fade up one after another; the last word(s) get a gold sheen."""
    words = title.split()
    out = []
    for i, w in enumerate(words):
        cls = "w gold" if i >= len(words) - gold_last else "w"
        out.append(f'<span class="{cls}" style="animation-delay:{0.08 + i * 0.09:.2f}s">{html.escape(w)}</span>')
    return " ".join(out)


def _sparks(n: int = 14) -> str:
    """Tiny gold particles rising through the hero (decorative)."""
    dots = "".join(
        f'<i style="left:{(i * 37) % 100}%;--d:{7 + (i * 5) % 6}s;--t:-{(i * 1.3) % 9:.1f}s;'
        f'--x:{(i % 5 - 2) * 14}px"></i>'
        for i in range(n))
    return f'<div class="sla-sparks" aria-hidden="true">{dots}</div>'


def hero(title: str, subtitle: str, right_html: str = "", eyebrow: str = "AI Learning Laboratory",
         big: bool = False, art: str = "", actions: str = "") -> None:
    eb = f'<div class="eyebrow">{html.escape(eyebrow)}</div>' if eyebrow else ""
    st.markdown(f'<div class="sla-hero{" big" if big else ""}">{_sparks() if big else ""}<div>{eb}'
                f'<h1>{_words(title) if big else html.escape(title)}</h1>'
                f'<p>{html.escape(subtitle)}</p><div class="right" '
                f'style="justify-content:flex-start;margin-top:.8rem">{right_html}</div>{actions}</div>'
                + (f'<div class="art">{art}</div>' if art else '') + '</div>',
                unsafe_allow_html=True)


def section(title: str, caption: str | None = None, right_html: str = "", kicker: str = "") -> None:
    cap = f"<p>{html.escape(caption)}</p>" if caption else ""
    kick = f'<div class="sla-kicker">{html.escape(kicker)}</div>' if kicker else ""
    st.markdown(f'<div class="sla-section"><div>{kick}<h3>{html.escape(title)}</h3>{cap}</div>'
                f'<div>{right_html}</div></div>',
                unsafe_allow_html=True)
