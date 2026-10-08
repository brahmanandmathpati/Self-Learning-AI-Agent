"""Overview: project status and headline numbers from the database."""

from __future__ import annotations

import streamlit as st

from sla.app.charts.figures import learning_curve, validation_curve
from sla.app.components.ui import badge, card_row, empty_state, hero, metric_card, section
from sla.app.state import services
from sla.app.styles.theme import AGENT_COLORS


def render() -> None:
    svc = services()
    ov = svc.experiments.overview()
    latest = ov["latest_run"]
    status = badge(latest["status"]) if latest else badge("offline", "No runs yet")
    hero("Self-Learning AI Agent", "An agent that starts with no knowledge and improves only from reward — "
         "proven with frozen-policy evaluation on held-out seeds.", status)

    algo = {"q_learning": "Q-learning", "dqn": "DQN", "random": "Random"}.get(latest["algorithm"]) if latest else None
    card_row([
        metric_card("Current environment", latest["env"] if latest else None, "most recent training run"),
        metric_card("Current algorithm", algo, f"seed {latest['seed']}" if latest else None),
        metric_card("Training status", latest["status"].title() if latest else None,
                    f"{latest['episodes_completed']:,} episodes" if latest else None),
        metric_card("Experiments", ov["experiments"], "multi-seed / ablation", "{:,}"),
        metric_card("Completed runs", ov["completed_runs"], f"{ov['runs']} total · {ov['failed_runs']} failed", "{:,}"),
    ])
    st.write("")
    card_row([
        metric_card("Best episode reward", ov["latest_best_reward"], "latest run, training"),
        metric_card("Average reward (last 50)", ov["latest_avg_reward_last50"], "latest run, training (ε > 0)"),
        metric_card("Evaluation score", ov["latest_test_mean"],
                    f"latest test mean (ε = 0): {ov['latest_test_label']}" if ov["latest_test_label"] else None),
        metric_card("Episodes logged", ov["episodes_logged"], "all runs", "{:,}"),
        metric_card("Reflection notes", ov["reflections"], "grounded explanations", "{:,}"),
    ])

    section("Latest run", "Training reward rises as the policy improves; validation uses the frozen greedy policy.")
    if latest is None:
        empty_state("No experiment data available yet. Train an agent on the Training page or from the terminal.",
                    "sla train --config configs/frozenlake_qlearning.yaml")
        return
    detail = svc.experiments.run_detail(latest["run_id"])
    color = AGENT_COLORS.get(algo or "", AGENT_COLORS["Q-learning"])
    left, right = st.columns([3, 2])
    with left:
        st.plotly_chart(learning_curve(detail["episodes"], color=color, title=latest["run_id"]), width="stretch")
    with right:
        vals = detail["evaluations"]
        vals = vals[vals["kind"] == "validation"] if not vals.empty else vals
        if vals.empty:
            empty_state("No validation evaluations for this run.")
        else:
            st.plotly_chart(validation_curve(vals, color=color, title="Frozen-policy validation", height=340),
                            width="stretch")

    section("How learning is proven here")
    st.markdown(
        "1. **Learning happens in the values/weights** — the Q-table (FrozenLake) or the network (CartPole) changes "
        "after every reward.\n"
        "2. **Frozen evaluation** — ε = 0, no updates, on seeds the agent never trained on.\n"
        "3. **Before vs after** — the same seeds are played by the untrained and the trained policy.\n"
        "4. **Against chance** — trained agents are compared with a random-action baseline (Welch's t-test, "
        "bootstrap 95% CI) across 5 training seeds.\n"
        "5. **Ablation** — removing replay or the target network shows which DQN parts matter.")
