"""Agent comparison: Random vs Q-learning vs DQN on held-out test seeds."""

from __future__ import annotations

import streamlit as st

from sla.app.charts.figures import group_bars, mean_curves
from sla.app.components.ui import empty_state, hero, section
from sla.app.state import services
from sla.app.styles.theme import AGENT_COLORS

LABELS = {"q_learning": "Q-learning", "dqn": "DQN"}


def render() -> None:
    svc = services()
    hero("Agent comparison", "Every number is a frozen-policy score on held-out test seeds; dots are individual seeds.")
    table = svc.experiments.comparison_table()
    if table.empty:
        empty_state("No test evaluations yet. Run a multi-seed experiment to compare agents with the random baseline.",
                    "sla pipeline --config configs/frozenlake_qlearning.yaml --seeds 0 1 2 3 4")
        return
    points = svc.experiments.test_results()
    for env in sorted(table["env"].unique()):
        section(env, "Bar = mean over seeds · whisker = std across seeds · dot = one seed's test mean")
        t = table[table["env"] == env]
        pts = points[points["env"] == env]
        left, right = st.columns([2, 3])
        with left:
            st.plotly_chart(group_bars(t, "label", "mean", "std", AGENT_COLORS, pts, height=330), width="stretch")
        with right:
            show = t.rename(columns={"label": "Agent", "mean": "Mean test return", "std": "Std across seeds",
                                     "n": "Seeds", "success_rate": "Success rate"})[
                ["Agent", "Mean test return", "Std across seeds", "Seeds", "Success rate"]]
            st.dataframe(show, hide_index=True, width="stretch",
                         column_config={"Success rate": st.column_config.ProgressColumn(format="percent",
                                                                                         min_value=0, max_value=1)})
            runs = svc.experiments.trained_runs()
            runs = runs[(runs["env"] == env) & (runs["variant"].isna())] if not runs.empty else runs
            curves: dict[str, list] = {}
            for _, r in runs.iterrows():
                curves.setdefault(LABELS.get(r["algorithm"], r["algorithm"]), []).append(
                    svc.db.query_episodes(r["run_id"]))
            if curves:
                st.plotly_chart(mean_curves(curves, AGENT_COLORS, title="Training curves (mean and range over runs)",
                                            height=260), width="stretch")
