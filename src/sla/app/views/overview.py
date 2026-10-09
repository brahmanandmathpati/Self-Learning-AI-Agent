"""Overview: live system status, headline KPIs and the latest run, all from the database."""

from __future__ import annotations

import streamlit as st

from sla.app import data
from sla.app.charts.figures import learning_curve, validation_curve
from sla.app.components.chart_card import chart_card
from sla.app.components.metric_card import card_grid, metric_card
from sla.app.components.run_card import algo_label
from sla.app.components.section_header import hero, section
from sla.app.components.states import empty_state
from sla.app.components.status_badge import badge, run_state
from sla.app.styles.theme import AGENT_COLORS, SERIES

STATE_TEXT = {"running": "Training", "completed": "Completed", "idle": "Idle", "stopped": "Stopped", "failed": "Failed"}

PILLARS = [
    ("Learning lives in the values",
     "The Q-table (FrozenLake) or the network weights (CartPole) change after every reward."),
    ("Frozen evaluation", "ε = 0 and no updates, on test seeds the agent never trained on."),
    ("Before vs after", "The untrained and the trained policy play exactly the same test seeds."),
    ("Against chance", "Trained agents vs a random agent: Welch's t-test and bootstrap 95% CI over 5 seeds."),
    ("Ablation", "Removing replay or the target network shows which DQN parts matter."),
]


def render() -> None:
    ov = data.overview()
    latest = ov["latest_run"]
    state = "running" if ov["running_runs"] else run_state(latest["status"] if latest else None)
    hero("SELF-LEARNING AI AGENT",
         "An AI agent that learns from experience — and proves it on games it has never seen.",
         badge("online", "System online") + badge(state, STATE_TEXT[state]), eyebrow="AI Learning Laboratory",
         big=True)

    algo = algo_label(latest["algorithm"]) if latest else None
    card_grid([
        metric_card("Training runs", ov["runs"], f"{ov['completed_runs']} completed · {ov['failed_runs']} failed",
                    "{:,}", icon="runs", accent=SERIES[0]),
        metric_card("Best reward", ov["latest_best_reward"], "best episode · latest run", icon="trophy",
                    accent="#f5b83d"),
        metric_card("Average reward", ov["latest_avg_reward_last50"], "last 50 episodes · latest run (ε > 0)",
                    icon="avg", accent=SERIES[2]),
        metric_card("Evaluation score", ov["latest_test_mean"],
                    f"test mean, ε = 0 · {ov['latest_test_label']}" if ov["latest_test_label"] else "no test yet",
                    icon="check", accent=SERIES[0]),
        metric_card("Episodes", ov["episodes_logged"], "logged across all runs", "{:,}", icon="layers",
                    accent=SERIES[1]),
        metric_card("Environment", latest["env"] if latest else None, f"{algo} · seed {latest['seed']}" if latest
                    else None, icon="globe", accent=SERIES[2]),
    ], min_width=150)

    section("Latest run", "Training reward should rise as the policy improves; validation uses the frozen policy.",
            badge(latest["status"]) if latest else "")
    if latest is None:
        empty_state("No experiment data yet.", "sla train --config configs/frozenlake_qlearning.yaml",
                    "Run your first training experiment on the Training page to see learning results here.")
    else:
        detail = data.run_detail(latest["run_id"])
        color = AGENT_COLORS.get(algo or "", SERIES[0])
        trend = data.learning_trend(detail["episodes"])
        if trend:
            word = {"improving": "▲ Improving", "flat": "■ Flat", "declining": "▼ Declining"}[trend[0]]
            st.caption(f"Training trend: **{word}** — {trend[1]}")
        left, right = st.columns([3, 2], gap="medium")
        with left:
            chart_card(learning_curve(detail["episodes"], color=color, height=320), "Reward per episode",
                       latest["run_id"], key="ov_curve")
        with right:
            vals = detail["evaluations"]
            vals = vals[vals["kind"] == "validation"] if not vals.empty else vals
            if vals.empty:
                empty_state("No validation checks for this run.", next_step="Validation runs every few episodes "
                            "during training; random baselines have none.")
            else:
                chart_card(validation_curve(vals, color=color, height=320), "Frozen-policy validation",
                           "greedy return (ε = 0) during training", key="ov_val")

    section("How learning is proven here")
    st.markdown('<div class="sla-grid" style="grid-template-columns:repeat(auto-fit,minmax(170px,1fr))">' + "".join(
        f'<div class="sla-card"><div class="label"><span class="ic">{i}</span>{t}</div>'
        f'<div class="sub" style="font-size:.84rem;color:var(--secondary)">{d}</div></div>'
        for i, (t, d) in enumerate(PILLARS, 1)) + "</div>", unsafe_allow_html=True)
