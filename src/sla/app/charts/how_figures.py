"""Charts used only by the "How it works" page (kept apart so the shared figures module stays untouched)."""

from __future__ import annotations

import numpy as np
import plotly.graph_objects as go

from sla.app.charts.figures import _alpha, _layout
from sla.app.styles.theme import INK, SERIES


def epsilon_chart(steps: list[int], eps: list[float], height: int = 280) -> go.Figure:
    """Epsilon (chance of a random move) over environment steps."""
    fig = go.Figure(go.Scatter(x=steps, y=eps, mode="lines", line=dict(color=SERIES[1], width=3), fill="tozeroy",
                               fillcolor=_alpha(SERIES[1], 0.12), name="epsilon",
                               hovertemplate="step %{x:,}<br>epsilon %{y:.3f}<extra></extra>"))
    fig.update_yaxes(range=[0, 1.05])
    return _layout(fig, None, "Environment steps", "ε (chance of a random move)", height, legend=False)


def q_grid(desc: list[str], q: np.ndarray, height: int = 360) -> go.Figure:
    """FrozenLake squares coloured by the best Q-value, with the greedy arrow; dark = nothing learned yet."""
    cols = len(desc[0])
    arrows = ("←", "↓", "→", "↑")
    z, notes = [], []
    for i, row in enumerate(desc):
        zr = []
        for j, c in enumerate(row):
            k = i * cols + j
            best = float(q[k].max())
            if c == "H":
                zr.append(-1.0)
            elif c == "G":
                zr.append(2.0)
            else:
                zr.append(min(max(best, 0.0), 1.0))
            notes.append((i, j, c, best, arrows[int(np.argmax(q[k]))] if best > 0 else "·"))
        z.append(zr)
    scale = [[0, "#3A2230"], [0.3333, "#1B2136"], [0.6667, SERIES[0]], [0.6668, "#2F5D1E"], [1, "#2F5D1E"]]
    fig = go.Figure(go.Heatmap(z=z, colorscale=scale, zmin=-1, zmax=2, showscale=False, hoverinfo="skip",
                               xgap=3, ygap=3))
    for i, j, c, best, arrow in notes:
        if c in "HG":
            text, color = ("HOLE" if c == "H" else "GOAL"), INK["primary"]
        else:
            text = f"{arrow}<br><span style='font-size:10px'>Q={best:.2f}</span>"
            color = "#0B1020" if best > 0.55 else INK["primary"]
        fig.add_annotation(x=j, y=i, text=text, showarrow=False, font=dict(color=color, size=15))
    fig.update_yaxes(autorange="reversed", showticklabels=False, showgrid=False, zeroline=False)
    fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False, scaleanchor="y")
    return _layout(fig, None, "", "", height, legend=False)
