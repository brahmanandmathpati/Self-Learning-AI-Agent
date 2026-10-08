"""Ablation: Full DQN vs no replay vs no target network, from stored runs."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from sla.app.charts.figures import group_bars, mean_curves
from sla.app.components.selectors import experiment_selector
from sla.app.components.ui import NOT_RUN, empty_state, hero, section
from sla.app.state import services
from sla.app.styles.theme import VARIANT_COLORS, VARIANT_LABELS


def render() -> None:
    svc = services()
    hero("Ablation study", "Remove one DQN component at a time and measure the held-out test score.")
    exps = svc.experiments.experiments("ablation")
    if exps.empty:
        empty_state("No ablation has been run yet.",
                    "sla ablation --config configs/cartpole_dqn.yaml --seeds 0 1 2 3 4")
        return
    exp_id = experiment_selector(exps, key="abl_exp")
    df, stats = svc.experiments.ablation(exp_id)
    if df.empty:
        empty_state(f"Ablation #{exp_id} has no finished runs yet.")
        return
    labels = {k: VARIANT_LABELS[k] for k in VARIANT_LABELS}
    colors = {VARIANT_LABELS[k]: v for k, v in VARIANT_COLORS.items()}
    df = df.assign(label=df["variant"].map(labels))
    agg = df.groupby("label", sort=False)["final_mean"].agg(mean="mean", std="std", n="count").reset_index()
    order = [VARIANT_LABELS[v] for v in VARIANT_LABELS if VARIANT_LABELS[v] in set(agg["label"])]
    agg = agg.set_index("label").loc[order].reset_index()

    left, right = st.columns([2, 3])
    with left:
        pts = df.rename(columns={"final_mean": "mean_return"})
        st.plotly_chart(group_bars(agg, "label", "mean", "std", colors, pts, title="Held-out test return by variant",
                                   height=340), width="stretch")
    with right:
        curves = {}
        for _, r in df.iterrows():
            if r["run_id"]:
                curves.setdefault(r["label"], []).append(svc.db.query_episodes(r["run_id"]))
        st.plotly_chart(mean_curves(curves, colors, title="Training reward (mean and range over seeds)", height=340),
                        width="stretch")

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
    section("Per-run results")
    st.dataframe(df[["label", "seed", "final_mean", "final_std", "success_rate", "run_id"]].rename(
        columns={"label": "Variant", "seed": "Seed", "final_mean": "Test mean", "final_std": "Test std",
                 "success_rate": "Success rate", "run_id": "Run"}), hide_index=True, width="stretch")
