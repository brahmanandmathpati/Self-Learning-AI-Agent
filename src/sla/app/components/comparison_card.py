"""Ranked agent / variant comparison cards."""

from __future__ import annotations

import html


def comparison_card(name: str, color: str, rank: int, value: float, best: float, value_label: str,
                    detail: str, why: str, delta: str | None = None, delta_negative: bool = False) -> str:
    """One ranked card; the bar length is ``value / best`` of the real stored means."""
    nd = 3 if abs(best) < 10 else 2
    width = 0 if best <= 0 else max(0.0, min(1.0, value / best)) * 100
    rk = f'<span class="sla-rank{" first" if rank == 1 else ""}" aria-label="rank {rank}">#{rank}</span>'
    dl = (f'<div class="delta{" neg" if delta_negative else ""}">{html.escape(delta)}</div>' if delta else "")
    return (f'<div class="sla-card"><div class="sla-cmp-head"><div class="sla-cmp-name">'
            f'<span class="sla-swatch" style="--c:{color}"></span>{html.escape(name)}</div>{rk}</div>'
            f'<div class="value">{value:,.{nd}f}</div>'
            f'<div class="sub">{html.escape(value_label)} · {html.escape(detail)}</div>'
            f'{dl}<div class="sla-bar"><span style="width:{width:.1f}%;--c:{color}"></span></div>'
            f'<div class="sla-why">{html.escape(why)}</div></div>')
