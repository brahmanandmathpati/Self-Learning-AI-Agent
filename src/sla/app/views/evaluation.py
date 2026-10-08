"""Evaluation: 5-seed results, trained vs random, before vs after, Welch's t-test and bootstrap CI."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from sla.app.charts.figures import before_after, group_bars
from sla.app.components.selectors import experiment_selector
from sla.app.components.ui import NOT_RUN, card_row, empty_state, fmt_num, hero, metric_card, section
from sla.app.state import services
from sla.app.styles.theme import AGENT_COLORS

LABELS = {"q_learning": "Q-learning", "dqn": "DQN"}


def _stats_card(title: str, cmp: dict | None) -> str:
    if not cmp:
        return metric_card(title, None, "needs ≥ 2 seeds in each group")
    sig = "significant at 0.05" if cmp.get("significant_0_05") else "not significant at 0.05"
    return metric_card(title, f"{cmp['diff']:+.2f}",
                       f"95% CI [{cmp['diff_ci_low']:.2f}, {cmp['diff_ci_high']:.2f}] · "
                       f"Welch p = {cmp['p_value']:.3g} · {sig}")


def render() -> None:
    svc = services()
    hero("Evaluation", "Frozen policy (ε = 0, no updates) on held-out test seeds that training never used.")
    exps = svc.experiments.experiments("pipeline")
    if exps.empty:
        empty_state("No multi-seed experiment has been run yet.",
                    "sla pipeline --config configs/cartpole_dqn.yaml --seeds 0 1 2 3 4")
        return
    exp_id = experiment_selector(exps, key="eval_exp")
    exp = svc.experiments.experiment(exp_id)
    summary = exp.get("summary") or {}
    if exp["status"] != "completed" or not summary:
        empty_state(f"Experiment #{exp_id} is {exp['status']} — statistics appear when it completes.")
        return
    label = LABELS.get(exp["algorithm"], exp["algorithm"])
    trained = summary.get("trained_test_means", [])
    baseline = summary.get("baseline_test_means", [])
    ci = summary.get("trained_mean_ci95")
    card_row([
        metric_card(f"{label} mean (test)", sum(trained) / len(trained) if trained else None,
                    f"{len(trained)} training seeds" + (f" · 95% CI [{ci[0]:.2f}, {ci[1]:.2f}]" if ci else "")),
        metric_card("Random baseline mean", sum(baseline) / len(baseline) if baseline else None,
                    f"{len(baseline)} seeds, same test seeds"),
        _stats_card("Trained − random", summary.get("trained_vs_random")),
        _stats_card("Trained − untrained (before/after)", summary.get("trained_vs_untrained")),
    ])

    runs = exp["runs"]
    tests = svc.db.query_evaluations(kind="test")
    tests = tests[tests["experiment_id"] == exp_id] if not tests.empty else tests
    initial = svc.db.query_evaluations(kind="initial")
    initial = initial[initial["experiment_id"] == exp_id] if not initial.empty else initial

    section("Per-seed results", "One row per training seed; the random baseline uses the same held-out seeds.")
    per_seed = []
    for _, r in runs[runs["algorithm"] != "random"].iterrows():
        t = tests[tests["run_id"] == r["run_id"]]
        i = initial[initial["run_id"] == r["run_id"]]
        b = tests[(tests["algorithm"] == "random") & (tests["seed"] == r["seed"])]
        per_seed.append({
            "seed": int(r["seed"]), "initial": float(i.iloc[-1]["mean_return"]) if not i.empty else None,
            "trained": float(t.iloc[-1]["mean_return"]) if not t.empty else None,
            "trained_std": float(t.iloc[-1]["std_return"]) if not t.empty else None,
            "median": float(t.iloc[-1]["median_return"]) if not t.empty else None,
            "success": float(t.iloc[-1]["success_rate"]) if not t.empty else None,
            "length": float(t.iloc[-1]["mean_length"]) if not t.empty else None,
            "random": float(b.iloc[-1]["mean_return"]) if not b.empty else None, "run_id": r["run_id"]})
    df = pd.DataFrame(per_seed)
    left, right = st.columns([3, 2])
    with left:
        st.dataframe(df.rename(columns={"seed": "Seed", "initial": "Untrained", "trained": "Trained mean",
                                        "trained_std": "Trained std", "median": "Median", "success": "Success rate",
                                        "length": "Mean length", "random": "Random", "run_id": "Run"}),
                     hide_index=True, width="stretch",
                     column_config={"Success rate": st.column_config.ProgressColumn(format="percent", min_value=0,
                                                                                     max_value=1)})
    with right:
        if not df.empty and df["initial"].notna().all() and df["trained"].notna().all():
            st.plotly_chart(before_after(df, title="Before vs after learning (same test seeds)"), width="stretch")
        else:
            empty_state("Before/after needs the untrained evaluation for every seed.")

    section("Trained vs random", "Bars: mean of per-seed test means ± std; dots: seeds.")
    rows = []
    if trained:
        rows.append({"label": label, "mean": pd.Series(trained).mean(), "std": pd.Series(trained).std()})
    if baseline:
        rows.append({"label": "Random", "mean": pd.Series(baseline).mean(), "std": pd.Series(baseline).std()})
    pts = pd.DataFrame([{"label": label, "mean_return": v} for v in trained]
                       + [{"label": "Random", "mean_return": v} for v in baseline])
    c1, c2 = st.columns([2, 3])
    with c1:
        st.plotly_chart(group_bars(pd.DataFrame(rows), "label", "mean", "std", AGENT_COLORS, pts, height=320),
                        width="stretch")
    with c2:
        stats = []
        for name, key in (("Trained vs random", "trained_vs_random"), ("Trained vs untrained", "trained_vs_untrained")):
            c = summary.get(key)
            stats.append({"Comparison": name,
                          "Difference": fmt_num(c["diff"]) if c else NOT_RUN,
                          "Bootstrap 95% CI": f"[{c['diff_ci_low']:.2f}, {c['diff_ci_high']:.2f}]" if c else NOT_RUN,
                          "Welch t": fmt_num(c["t"]) if c else NOT_RUN,
                          "p-value": f"{c['p_value']:.4g}" if c else NOT_RUN,
                          "n": f"{c['n_a']} vs {c['n_b']}" if c else NOT_RUN})
        st.dataframe(pd.DataFrame(stats), hide_index=True, width="stretch")
        st.caption("Welch's t-test does not assume equal variances. With only a few seeds, read the bootstrap "
                   "interval alongside the p-value. If both groups have zero variance the test is undefined; "
                   "it is then reported as p = 0 (perfect separation) or p = 1 (identical).")
