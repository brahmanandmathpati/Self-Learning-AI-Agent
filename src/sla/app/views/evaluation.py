"""Evaluation: 5-seed results, trained vs random, before vs after, Welch's t-test and bootstrap CI."""

from __future__ import annotations

import statistics

import pandas as pd
import streamlit as st

from sla.app import data
from sla.app.charts.figures import before_after, group_bars
from sla.app.components.chart_card import chart_card
from sla.app.components.selectors import experiment_selector
from sla.app.components.ui import NOT_RUN, card_grid, empty_state, fmt_num, hero, metric_card, section, verdict
from sla.app.styles.theme import AGENT_COLORS

LABELS = {"q_learning": "Q-learning", "dqn": "DQN"}


def _supports(cmp: dict | None) -> bool:
    """A comparison supports learning only if it is significant AND its bootstrap CI lies above zero."""
    return bool(cmp) and bool(cmp.get("significant_0_05")) and float(cmp["diff_ci_low"]) > 0


def _evidence(summary: dict) -> tuple[str, str]:
    vs_r, vs_u = summary.get("trained_vs_random"), summary.get("trained_vs_untrained")
    if not vs_r:
        return "notrun", "Needs at least 2 trained seeds and 2 random-baseline seeds."
    checks = [("beats the random agent", _supports(vs_r))]
    if vs_u:
        checks.append(("beats its own untrained start", _supports(vs_u)))
    if all(ok for _, ok in checks):
        return "verified", ("Trained policy " + " and ".join(c for c, _ in checks) +
                            f" on held-out test seeds (Welch p = {vs_r['p_value']:.3g}, 95% CI of the gain "
                            f"[{vs_r['diff_ci_low']:.2f}, {vs_r['diff_ci_high']:.2f}] excludes 0).")
    failed = [c for c, ok in checks if not ok]
    return "insufficient", ("Not shown: the trained policy " + " / ".join(failed) +
                            " with p < 0.05 and a confidence interval above 0. More seeds or training may help.")


def _cmp_card(title: str, cmp: dict | None) -> str:
    if not cmp:
        return metric_card(title, None, "needs ≥ 2 seeds in each group", icon="flask")
    ok = _supports(cmp)
    return metric_card(title, f"{cmp['diff']:+,.2f}",
                       f"bootstrap 95% CI [{cmp['diff_ci_low']:.2f}, {cmp['diff_ci_high']:.2f}] · Welch p = "
                       f"{cmp['p_value']:.3g}", icon="flask", accent="#22c55e" if ok else "#f5b83d",
                       delta="✓ significant" if cmp.get("significant_0_05") else "✕ not significant",
                       delta_negative=not cmp.get("significant_0_05"))


def render() -> None:
    hero("Evaluation", "Frozen policy (ε = 0, no updates) on held-out test seeds that training never used.",
         eyebrow="Proof of learning")
    exps = data.experiments("pipeline")
    if exps.empty:
        empty_state("No multi-seed experiment has been run yet.",
                    "sla pipeline --config configs/cartpole_dqn.yaml --seeds 0 1 2 3 4",
                    "Run a multi-seed experiment from the Training page to get statistics here.")
        return
    exp_id = experiment_selector(exps, key="eval_exp")
    exp = data.experiment(exp_id)
    summary = exp.get("summary") or {}
    if exp["status"] != "completed" or not summary:
        empty_state(f"Experiment #{exp_id} is {exp['status']}.", next_step="Statistics appear when it completes.",
                    glyph="clock", tag=str(exp["status"]).upper())
        return
    label = LABELS.get(exp["algorithm"], exp["algorithm"])
    trained = summary.get("trained_test_means", [])
    baseline = summary.get("baseline_test_means", [])
    ci = summary.get("trained_mean_ci95")
    kind, detail = _evidence(summary)
    verdict(kind, detail)
    card_grid([
        metric_card(f"Mean reward · {label}", statistics.fmean(trained) if trained else None,
                    f"{len(trained)} seeds · test episodes, ε = 0", icon="trophy", accent="#3987e5"),
        metric_card("Median reward", statistics.median(trained) if trained else None, "median of per-seed means",
                    icon="avg"),
        metric_card("Standard deviation", statistics.stdev(trained) if len(trained) > 1 else None, "across seeds",
                    icon="len"),
        metric_card("95% confidence interval", f"[{ci[0]:,.2f}, {ci[1]:,.2f}]" if ci else None,
                    "bootstrap CI of the trained mean", icon="target"),
        metric_card("Random baseline", statistics.fmean(baseline) if baseline else None,
                    f"{len(baseline)} seeds · same test seeds", icon="dice", accent="#8a94a6"),
    ])
    card_grid([_cmp_card("Welch's t-test · trained − random", summary.get("trained_vs_random")),
               _cmp_card("Before → after · trained − untrained", summary.get("trained_vs_untrained"))], min_width=280)

    runs = exp["runs"]
    tests = data.evaluations("test")
    tests = tests[tests["experiment_id"] == exp_id] if not tests.empty else tests
    initial = data.evaluations("initial")
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
    st.dataframe(df.rename(columns={"seed": "Seed", "initial": "Untrained", "trained": "Trained mean",
                                    "trained_std": "Trained std", "median": "Median", "success": "Success rate",
                                    "length": "Mean length", "random": "Random", "run_id": "Run"}),
                 hide_index=True, width="stretch",
                 column_config={"Success rate": st.column_config.ProgressColumn(format="percent", min_value=0,
                                                                                 max_value=1)})
    before_ok = not df.empty and df["initial"].notna().all() and df["trained"].notna().all()

    section("Before vs after · trained vs random", "Same held-out test seeds for every policy.")
    rows = []
    if trained:
        rows.append({"label": label, "mean": pd.Series(trained).mean(), "std": pd.Series(trained).std()})
    if baseline:
        rows.append({"label": "Random", "mean": pd.Series(baseline).mean(), "std": pd.Series(baseline).std()})
    pts = pd.DataFrame([{"label": label, "mean_return": v} for v in trained]
                       + [{"label": "Random", "mean_return": v} for v in baseline])
    c0, c1 = st.columns(2, gap="medium")
    with c0:
        if before_ok:
            chart_card(before_after(df, height=320), "Before vs after learning", "same test seeds, one line per seed",
                       key="ev_ba")
        else:
            empty_state("Before/after needs the untrained evaluation for every seed.")
    with c1:
        chart_card(group_bars(pd.DataFrame(rows), "label", "mean", "std", AGENT_COLORS, pts, height=320),
                   "Trained vs random", "mean ± std · dots are seeds", key="ev_bars")
    section("Statistical tests", "Welch's t-test and bootstrap 95% confidence intervals over seeds.")
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
