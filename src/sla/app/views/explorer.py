"""Run explorer: configuration, metrics, evaluations, checkpoints and logs of one run."""

from __future__ import annotations

import streamlit as st

from sla.app.charts.figures import learning_curve
from sla.app.components.selectors import run_selector
from sla.app.components.ui import badge, card_row, empty_state, hero, metric_card
from sla.app.state import services
from sla.utils.errors import SLAError


def render() -> None:
    svc = services()
    hero("Run explorer", "Every run is reproducible: seed, config, git commit, checkpoints and logs are recorded.")
    runs = svc.experiments.runs()
    if runs.empty:
        empty_state("No runs stored yet.", "sla train --config configs/frozenlake_qlearning.yaml")
        return
    f1, f2, f3 = st.columns(3)
    env = f1.multiselect("Environment", sorted(runs["env"].unique()))
    algo = f2.multiselect("Algorithm", sorted(runs["algorithm"].unique()))
    status = f3.multiselect("Status", sorted(runs["status"].unique()))
    view = runs
    if env:
        view = view[view["env"].isin(env)]
    if algo:
        view = view[view["algorithm"].isin(algo)]
    if status:
        view = view[view["status"].isin(status)]
    if view.empty:
        empty_state("No runs match these filters.")
        return
    run_id = run_selector(view, key="explorer_run")
    d = svc.experiments.run_detail(run_id)
    run = d["run"]
    st.markdown(f"{badge(run['status'])} &nbsp; <code>{run_id}</code>", unsafe_allow_html=True)
    test = d["evaluations"][d["evaluations"]["kind"] == "test"] if not d["evaluations"].empty else d["evaluations"]
    card_row([
        metric_card("Environment", run["env"]), metric_card("Algorithm", run["algorithm"], run.get("variant") or None),
        metric_card("Seed", run["seed"], None, "{}"),
        metric_card("Episodes", run["episodes_completed"], run.get("stopped_reason"), "{:,}"),
        metric_card("Test mean", float(test.iloc[-1]["mean_return"]) if not test.empty else None,
                    f"± {test.iloc[-1]['std_return']:.2f}" if not test.empty else "not evaluated"),
    ])
    st.caption(f"Started {run['started_at']} · ended {run.get('ended_at') or '—'} · git {run.get('git_sha') or 'n/a'}"
               f" · folder {run.get('run_dir') or '—'}")
    if run.get("error"):
        st.error(run["error"])

    tabs = st.tabs(["Curves", "Evaluations", "Configuration", "Checkpoints", "Metrics", "Log"])
    with tabs[0]:
        if d["episodes"].empty:
            empty_state("This run has no training episodes (random baselines are evaluated, not trained).")
        else:
            st.plotly_chart(learning_curve(d["episodes"], title="Training reward"), width="stretch")
    with tabs[1]:
        if d["evaluations"].empty:
            empty_state("No evaluations recorded.")
        else:
            cols = ["kind", "episode", "mean_return", "std_return", "median_return", "success_rate", "mean_length",
                    "n_episodes", "seed_base", "checkpoint", "created_at"]
            st.dataframe(d["evaluations"][cols], hide_index=True, width="stretch")
        if run.get("run_dir") and run["episodes_completed"]:
            c1, c2, c3 = st.columns([1, 1, 2])
            which = c1.selectbox("Checkpoint", ["best", "latest"], key="exp_ck")
            n = c2.number_input("Test episodes", 5, 1000, 100, step=5, key="exp_n")
            if c3.button("Evaluate frozen policy now", type="primary"):
                try:
                    with st.spinner("Evaluating on held-out test seeds (ε = 0, no learning)…"):
                        res, folder = svc.evaluation.evaluate_run(run["run_dir"], which, int(n))
                    st.success(f"{folder.name}: mean {res.mean_return:.2f} ± {res.std_return:.2f}, "
                               f"success {res.success_rate:.0%} — stored in the database.")
                except (SLAError, OSError) as exc:
                    st.error(str(exc))
    with tabs[2]:
        st.json(run["config"])
    with tabs[3]:
        cks = svc.checkpoints.list(run["run_dir"]) if run.get("run_dir") else None
        if cks is None or cks.empty:
            empty_state("No checkpoints on disk for this run.")
        else:
            st.dataframe(cks, hide_index=True, width="stretch")
            st.caption(f"Latest: {run.get('latest_checkpoint') or '—'} · Best (validation-selected): "
                       f"{run.get('best_checkpoint') or '—'}")
            if run["status"] in ("stopped", "failed"):
                st.info(f"Resume from the terminal: sla train --resume {run['run_dir']}")
    with tabs[4]:
        if d["metrics"].empty:
            empty_state("No run-level metrics recorded.")
        else:
            st.dataframe(d["metrics"], hide_index=True, width="stretch")
    with tabs[5]:
        st.code(d["log_tail"] or "No log file found.", language="text")
