"""Plotly figures with one shared visual language (thin marks, recessive grid, single y-axis)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from sla.app.styles.theme import AGENT_COLORS, INK, SERIES, VARIANT_COLORS, VARIANT_LABELS
from sla.utils.summary import rolling_mean


def _layout(fig: go.Figure, title: str | None = None, x: str = "", y: str = "", height: int = 340,
            legend: bool = True) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(size=13, color=INK["primary"]), x=0, xanchor="left") if title else None,
        height=height, margin=dict(l=6, r=6, t=38 if title else 10, b=6),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family='Inter, system-ui, -apple-system, "Segoe UI", sans-serif', color=INK["secondary"], size=12),
        hovermode="x unified" if fig.data and fig.data[0].type == "scatter" else "closest",
        hoverlabel=dict(bgcolor="#141b2b", bordercolor="rgba(91,156,240,.5)", font_color=INK["primary"],
                        font_family="Inter, sans-serif"),
        showlegend=legend, transition=dict(duration=300, easing="cubic-in-out"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11),
                    bgcolor="rgba(0,0,0,0)", itemclick="toggle", itemdoubleclick="toggleothers"),
        dragmode="zoom",
    )
    axis = dict(gridcolor=INK["grid"], zerolinecolor=INK["axis"], linecolor=INK["axis"], showline=False,
                tickfont=dict(color=INK["muted"], size=11), title_font=dict(color=INK["muted"], size=11),
                showspikes=True, spikecolor="rgba(148,163,184,.35)", spikethickness=1, spikedash="dot",
                spikemode="across")
    fig.update_xaxes(title_text=x, **axis)
    fig.update_yaxes(title_text=y, **axis)
    return fig


def learning_curve(episodes: pd.DataFrame, window: int = 50, color: str = SERIES[0], title: str | None = None,
                   height: int = 340) -> go.Figure:
    """Reward per episode (faint) and its rolling mean (bold)."""
    fig = go.Figure()
    if not episodes.empty:
        x = episodes["episode"] + 1
        y = episodes["total_reward"]
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="Reward per episode", line=dict(width=1, color=color),
                                 opacity=0.28, hovertemplate="%{y:.2f}"))
        fig.add_trace(go.Scatter(x=x, y=rolling_mean(y.tolist(), window), mode="lines",
                                 name=f"Moving average ({window})", line=dict(width=2.4, color=color),
                                 fill="tozeroy", fillcolor=_alpha(color, 0.08), hovertemplate="%{y:.2f}"))
    return _layout(fig, title, "Episode", "Total reward", height)


def single_series(episodes: pd.DataFrame, column: str, label: str, color: str = SERIES[0], title: str | None = None,
                  window: int | None = None, height: int = 260) -> go.Figure:
    fig = go.Figure()
    data = episodes.dropna(subset=[column]) if not episodes.empty else episodes
    if not data.empty:
        y = data[column].tolist()
        if window:
            y = rolling_mean(y, window)
        fig.add_trace(go.Scatter(x=data["episode"] + 1, y=y, mode="lines", name=label,
                                 line=dict(width=2, color=color), fill="tozeroy", fillcolor=_alpha(color, 0.07),
                                 hovertemplate="%{y:.4g}"))
    return _layout(fig, title, "Episode", label, height, legend=False)


def validation_curve(evals: pd.DataFrame, color: str = SERIES[0], title: str | None = None,
                     height: int = 260) -> go.Figure:
    fig = go.Figure()
    if not evals.empty:
        x = evals["episode"] + 1
        fig.add_trace(go.Scatter(x=x, y=evals["mean_return"], mode="lines+markers", name="Validation mean",
                                 line=dict(width=2, color=color), marker=dict(size=8),
                                 error_y=dict(type="data", array=evals["std_return"], thickness=1, width=0,
                                              color=color),
                                 hovertemplate="mean %{y:.2f}"))
    return _layout(fig, title, "Training episode", "Greedy return (ε = 0)", height, legend=False)


def mean_curves(curves: dict[str, list[pd.DataFrame]], colors: dict[str, str], window: int = 50,
                title: str | None = None, height: int = 340) -> go.Figure:
    """Mean rolling reward over seeds per group, with a min-max band."""
    fig = go.Figure()
    for label, frames in curves.items():
        frames = [f for f in frames if not f.empty]
        if not frames:
            continue
        n = min(len(f) for f in frames)
        mat = np.array([rolling_mean(f["total_reward"].tolist()[:n], window) for f in frames])
        x = np.arange(1, n + 1)
        color = colors.get(label, INK["muted"])
        fig.add_trace(go.Scatter(x=np.concatenate([x, x[::-1]]),
                                 y=np.concatenate([mat.max(axis=0), mat.min(axis=0)[::-1]]),
                                 fill="toself", fillcolor=_alpha(color, 0.14), line=dict(width=0),
                                 hoverinfo="skip", showlegend=False))
        fig.add_trace(go.Scatter(x=x, y=mat.mean(axis=0), mode="lines", name=f"{label} ({len(frames)} seeds)",
                                 line=dict(width=2.2, color=color), hovertemplate="%{y:.2f}"))
    return _layout(fig, title, "Episode", f"Reward (moving average {window})", height)


def group_bars(df: pd.DataFrame, label_col: str, mean_col: str, std_col: str | None, colors: dict[str, str],
               points: pd.DataFrame | None = None, point_col: str = "mean_return", title: str | None = None,
               y_title: str = "Mean test return", height: int = 340) -> go.Figure:
    """Bars of the across-seed mean (± std) with each seed drawn as a dot."""
    fig = go.Figure()
    for _, row in df.iterrows():
        label = row[label_col]
        color = colors.get(label, INK["muted"])
        err = dict(type="data", array=[row[std_col]] if std_col and pd.notna(row[std_col]) else [0],
                   thickness=1.2, width=6, color=INK["secondary"])
        fig.add_trace(go.Bar(x=[label], y=[row[mean_col]], name=label, marker=dict(color=color, line=dict(width=0)),
                             error_y=err, width=0.55, hovertemplate=f"{label}<br>mean %{{y:.2f}}<extra></extra>"))
        if points is not None and not points.empty:
            pts = points[points[label_col] == label][point_col]
            fig.add_trace(go.Scatter(x=[label] * len(pts), y=pts, mode="markers", showlegend=False,
                                     marker=dict(size=9, color=INK["primary"],
                                                 line=dict(width=2, color=INK["surface"])),
                                     hovertemplate="seed result %{y:.2f}<extra></extra>"))
    fig.update_layout(barmode="group", bargap=0.35)
    return _layout(fig, title, "", y_title, height, legend=False)


def before_after(per_seed: pd.DataFrame, title: str | None = None, height: int = 320) -> go.Figure:
    """Slope chart: untrained vs trained test score for each seed."""
    fig = go.Figure()
    for _, r in per_seed.iterrows():
        fig.add_trace(go.Scatter(x=["Untrained (before)", "Trained (after)"], y=[r["initial"], r["trained"]],
                                 mode="lines+markers", name=f"seed {int(r['seed'])}",
                                 line=dict(width=2, color=SERIES[0]), marker=dict(size=9),
                                 hovertemplate=f"seed {int(r['seed'])}: %{{y:.2f}}<extra></extra>"))
    fig = _layout(fig, title, "", "Mean test return", height, legend=False)
    fig.update_layout(hovermode="closest")
    return fig


def frozenlake_map(desc: list[str], arrows: list[str] | None = None, values: np.ndarray | None = None,
                   height: int = 360) -> go.Figure:
    """FrozenLake grid; optional greedy-policy arrows and state values from a trained Q-table."""
    n = len(desc)
    kinds = {"S": 0.15, "F": 0.15, "H": 0.0, "G": 1.0}
    z = [[kinds[c] for c in row] for row in desc]
    colors = [[0, "#0a1322"], [0.14, "#0a1322"], [0.15, "#1a2840"], [0.99, "#1a2840"], [1.0, "#0e5c43"]]
    fig = go.Figure(go.Heatmap(z=z, colorscale=colors, showscale=False, hoverinfo="skip", xgap=3, ygap=3))
    names = {"S": "START", "H": "HOLE", "G": "GOAL", "F": ""}
    for i, row in enumerate(desc):
        for j, c in enumerate(row):
            text = names[c]
            k = i * n + j
            if arrows and c in "SF":
                text = f"{arrows[k]}" + (f"<br><span style='font-size:10px'>V={values[k]:.2f}</span>"
                                         if values is not None else "")
            fig.add_annotation(x=j, y=i, text=text, showarrow=False,
                               font=dict(color=INK["primary"], size=18 if arrows and c in "SF" else 11))
    fig.update_yaxes(autorange="reversed", showticklabels=False, showgrid=False, zeroline=False)
    fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False, scaleanchor="y")
    return _layout(fig, None, "", "", height, legend=False)


def _alpha(hex_color: str, a: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{a})"


__all__ = ["AGENT_COLORS", "VARIANT_COLORS", "VARIANT_LABELS", "learning_curve", "single_series", "validation_curve",
           "mean_curves", "group_bars", "before_after", "frozenlake_map"]
