"""Agent comparison: Random vs Q-learning, SARSA, Expected SARSA and DQN on held-out test seeds.

Uses completed multi-seed experiments only.
"""

from __future__ import annotations

import streamlit as st

from sla import friendly
from sla.app import data
from sla.app.charts.figures import group_bars, mean_curves
from sla.app.components.chart_card import chart_card
from sla.app.components.comparison_card import comparison_card
from sla.app.components.metric_card import card_grid
from sla.app.components.section_header import hero, section
from sla.app.components.states import empty_state
from sla.app.styles.theme import AGENT_COLORS
from sla.catalog import ALGO_LABELS

LABELS = ALGO_LABELS
WHY = {
    "Q-learning": "Keeps a table of action values for every square and updates it from each reward.",
    "SARSA": "Like Q-learning, but learns from the move it really makes next, so it plays it safe while exploring.",
    "Expected SARSA": "Averages over every possible next move (weighted by how likely it is) — steadier updates.",
    "DQN": "A neural network estimates action values; replay memory and a target network keep learning stable.",
    "Random": "Picks actions by chance — the score you get with no learning at all.",
}


def render() -> None:
    hero("Agent comparison", "Frozen-policy scores on held-out test seeds from completed multi-seed experiments.",
         eyebrow="Analysis")
    table, points = data.comparison()
    if table.empty:
        empty_state("No test evaluations to compare yet.",
                    "sla pipeline --config configs/frozenlake_qlearning.yaml --seeds 0 1 2 3 4",
                    "Run a multi-seed experiment (Training → Multi-seed) — it also runs the random baseline.")
        return
    runs = data.trained_runs()
    envs = sorted(table["env"].unique())
    algos = sorted(table["label"].unique())
    f1, f2 = st.columns(2)
    pick_env = f1.multiselect("Game", envs, default=envs, key="cmp_filter_env")
    pick_algo = f2.multiselect("Algorithm", algos, default=algos, key="cmp_filter_algo")
    table = table[table["env"].isin(pick_env) & table["label"].isin(pick_algo)]
    if table.empty:
        empty_state("Nothing matches these filters.", next_step="Choose at least one game and one algorithm.")
        return
    st.download_button("Download this table (CSV)", table.to_csv(index=False).encode("utf-8"),
                       "comparison.csv", "text/csv", key="cmp_csv")
    for env in sorted(table["env"].unique()):
        t = table[table["env"] == env].sort_values("mean", ascending=False).reset_index(drop=True)
        pts = points[points["env"] == env]
        best = float(t["mean"].max())
        rnd = t[t["label"] == "Random"]
        rnd_mean = float(rnd["mean"].iloc[0]) if not rnd.empty else None
        top = t.iloc[0]
        tied = [str(x) for x in t.loc[(t["mean"] - best).abs() < 1e-9, "label"]]
        if len(tied) > 1:
            names = ", ".join(tied[:-1]) + " and " + tied[-1]
            summary = f"{names} tie for first with a mean test return of {best:,.2f}"
        else:
            summary = f"{top['label']} ranks first with a mean test return of {top['mean']:,.2f}"
        if rnd_mean is not None and top["label"] != "Random":
            summary += f", {top['mean'] - rnd_mean:+,.2f} versus the random agent"
        winner = friendly.winner_sentence(str(env), list(zip(t["label"], t["mean"])))
        section(env, winner or summary + ".")
        st.caption("Why do they differ? " + " ".join(
            f"{lab}: {WHY[lab.split(' (')[0]]}" for lab in t["label"] if lab.split(" (")[0] in WHY))
        cards = []
        for i, r in t.iterrows():
            delta = None
            if rnd_mean is not None and r["label"] != "Random":
                delta = f"{r['mean'] - rnd_mean:+,.2f} vs random"
            std = "—" if r["std"] != r["std"] else f"± {r['std']:,.2f}"  # NaN check (1 seed)
            cards.append(comparison_card(
                r["label"], AGENT_COLORS.get(r["label"], "#8a94a6"), i + 1, float(r["mean"]), best,
                "mean test return", f"{std} across {int(r['n'])} seeds · success {r['success_rate']:.0%}",
                WHY.get(r["label"].split(" (")[0], ""), delta, delta_negative=bool(delta and delta.startswith("-"))))
        card_grid(cards, min_width=240)
        left, right = st.columns([2, 3], gap="medium")
        with left:
            chart_card(group_bars(t, "label", "mean", "std", AGENT_COLORS, pts, height=320), "Test return by agent",
                       "bar = mean over seeds · whisker = std · dot = one seed", key=f"cmp_bar_{env}")
        with right:
            ids = set(pts["run_id"])
            sel = runs[runs["run_id"].isin(ids)] if not runs.empty else runs
            curves: dict[str, list] = {}
            for _, r in sel.iterrows():
                curves.setdefault(LABELS.get(r["algorithm"], r["algorithm"]), []).append(data.episodes(r["run_id"]))
            if curves:
                chart_card(mean_curves(curves, AGENT_COLORS, height=320), "Training curves",
                           "mean and min–max range over seeds", key=f"cmp_curve_{env}")
            else:
                empty_state("No training curves for these runs.")
