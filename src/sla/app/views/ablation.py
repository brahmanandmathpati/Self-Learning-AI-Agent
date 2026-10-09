"""Ablation: Full DQN vs no replay vs no target network, from stored runs."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from sla.app import data
from sla.app.charts.figures import group_bars, mean_curves
from sla.app.components.chart_card import chart_card
from sla.app.components.comparison_card import comparison_card
from sla.app.components.selectors import experiment_selector
from sla.app.components.ui import NOT_RUN, card_grid, empty_state, hero, section
from sla.app.styles.theme import VARIANT_COLORS, VARIANT_LABELS

WHY = {
    "Full DQN": "Replay memory + target network: learns from shuffled past experience against stable targets.",
    "No replay": "Learns only from the newest step, so consecutive, highly correlated samples drive every update.",
    "No target network": "The network chases its own moving predictions — targets shift after every update.",
}


def render() -> None:
    hero("Ablation study", "Remove one DQN component at a time and measure the held-out test score.",
         eyebrow="Which parts matter?")
    exps = data.experiments("ablation")
    if exps.empty:
        empty_state("No ablation has been run yet.",
                    "sla ablation --config configs/cartpole_dqn.yaml --seeds 0 1 2 3 4",
                    "Run the ablation from the terminal; results appear here automatically.", glyph="flask")
        return
    exp_id = experiment_selector(exps, key="abl_exp")
    df, stats = data.ablation(exp_id)
    if df.empty:
        empty_state(f"Ablation #{exp_id} has no finished runs yet.", next_step="Check back when its runs complete.",
                    glyph="clock")
        return
    labels = {k: VARIANT_LABELS[k] for k in VARIANT_LABELS}
    colors = {VARIANT_LABELS[k]: v for k, v in VARIANT_COLORS.items()}
    df = df.assign(label=df["variant"].map(labels))
    agg = df.groupby("label", sort=False)["final_mean"].agg(mean="mean", std="std", n="count").reset_index()
    order = [VARIANT_LABELS[v] for v in VARIANT_LABELS if VARIANT_LABELS[v] in set(agg["label"])]
    agg = agg.set_index("label").loc[order].reset_index()

    full_mean = float(agg.loc[agg["label"] == "Full DQN", "mean"].iloc[0]) if "Full DQN" in set(agg["label"]) else None
    ranked = agg.sort_values("mean", ascending=False).reset_index(drop=True)
    best = float(ranked["mean"].max())
    cards = []
    for i, r in ranked.iterrows():
        delta = None
        if full_mean is not None and r["label"] != "Full DQN":
            delta = f"{r['mean'] - full_mean:+,.2f} vs full DQN"
        std = "—" if r["std"] != r["std"] else f"± {r['std']:,.2f}"
        cards.append(comparison_card(r["label"], colors.get(r["label"], "#8a94a6"), i + 1, float(r["mean"]), best,
                                     "mean test return", f"{std} · {int(r['n'])} seeds", WHY.get(r["label"], ""),
                                     delta, delta_negative=bool(delta and delta.startswith("-"))))
    card_grid(cards, min_width=240)

    left, right = st.columns([2, 3], gap="medium")
    with left:
        pts = df.rename(columns={"final_mean": "mean_return"})
        chart_card(group_bars(agg, "label", "mean", "std", colors, pts, height=330), "Held-out test return by variant",
                   "bar = mean · whisker = std · dot = one seed", key="abl_bars")
    with right:
        curves = {}
        for _, r in df.iterrows():
            if r["run_id"]:
                curves.setdefault(r["label"], []).append(data.episodes(r["run_id"]))
        chart_card(mean_curves(curves, colors, height=330), "Training reward", "mean and min–max range over seeds",
                   key="abl_curves")

    section("Statistics", "Full DQN compared with each ablated variant (Welch's t-test, bootstrap 95% CI).")
    if stats.empty:
        st.info(f"{NOT_RUN}: statistics need at least 2 seeds per variant.")
    else:
        show = pd.DataFrame({
            "Comparison": stats["comparison"].str.replace("_", " "),
            "Full mean": stats.filter(like="mean_full").iloc[:, 0].round(2),
            "Variant mean": stats.apply(lambda r: r[[c for c in stats.columns if c.startswith("mean_")
                                                     and c != "mean_full"]].dropna().iloc[0], axis=1).round(2),
            "Difference": stats["diff"].round(2),
            "95% CI": stats.apply(lambda r: f"[{r['diff_ci_low']:.2f}, {r['diff_ci_high']:.2f}]", axis=1),
            "p-value": stats["p_value"].map(lambda p: f"{p:.4g}"),
            "Significant": stats["significant_0_05"].map({True: "✓ yes", False: "✕ no"}),
        })
        st.dataframe(show, hide_index=True, width="stretch")
    with st.expander("Per-run results"):
        st.dataframe(df[["label", "seed", "final_mean", "final_std", "success_rate", "run_id"]].rename(
            columns={"label": "Variant", "seed": "Seed", "final_mean": "Test mean", "final_std": "Test std",
                     "success_rate": "Success rate", "run_id": "Run"}), hide_index=True, width="stretch")
