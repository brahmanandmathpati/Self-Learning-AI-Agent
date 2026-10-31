"""Overview: live system status, headline KPIs and the latest run, all from the database."""

from __future__ import annotations

import streamlit as st

from sla.app import data
from sla.app.charts.figures import learning_curve, validation_curve
from sla.app.components.chart_card import chart_card
from sla.app.components.landing import actions, features, stack, steps
from sla.app.components.metric_card import card_grid, metric_card
from sla.app.components.motion import learning_loop, neural_flow
from sla.app.components.run_card import algo_label
from sla.app.components.section_header import hero, section
from sla.app.components.states import empty_state
from sla.app.components.status_badge import badge
from sla.app.styles.theme import AGENT_COLORS, SERIES

STATE_TEXT = {"running": "Training", "completed": "Completed", "idle": "Idle", "stopped": "Stopped", "failed": "Failed"}

STEPS = [("Observe", "The agent looks at the game: where it is, or how the pole is leaning."),
         ("Choose", "It picks a move — sometimes a random one, to explore."),
         ("Act", "The game reacts and gives a reward: points for good moves."),
         ("Learn", "It updates its scores so good moves are chosen more often.")]

FEATURES = [
    ("brain", "Learns from zero", "Starts with no knowledge and improves only from rewards — no hand rules."),
    ("cpu", "Deep Q-Network from scratch", "A small PyTorch neural network with replay memory and a target network."),
    ("check", "Fair, frozen tests", "Learning switched off, 100 new games per seed, compared with a random player."),
    ("flask", "Proof with statistics", "Five seeds, Welch's t-test and a 95% interval show the gain is not luck."),
    ("layers", "Ablation study", "Removes replay or the target network to show which parts really matter."),
    ("spark", "Explanations you can trust", "Plain-language notes where every number is checked against the database."),
]
STACK = ["Python", "PyTorch", "Gymnasium", "NumPy", "SciPy", "SQLite", "Streamlit", "Plotly", "pytest",
         "GitHub Actions"]


def _featured_run(latest: dict | None) -> dict | None:
    """Newest completed main run (not an ablation variant); falls back to the newest run of any kind."""
    runs = data.trained_runs()
    if runs.empty:
        return latest
    done = runs[runs["status"] == "completed"]
    main = done[done["variant"].fillna("").isin(["", "full"])] if "variant" in done else done
    pick = main if not main.empty else done
    return pick.iloc[0].to_dict() if not pick.empty else latest


def render() -> None:
    ov = data.overview()
    latest = ov["latest_run"]
    state = "running" if ov["running_runs"] else "idle"
    hero("An AI agent that learns from experience.",
         "It starts knowing nothing, learns two games from rewards alone, and proves it on games it has never seen.",
         badge("online", "System online") + badge(state, STATE_TEXT[state]), eyebrow="Self-Learning AI Agent",
         big=True, art=learning_loop(),
         actions=actions([("Start training", "training", "gold"), ("See the proof", "evaluation", "outline")]))
    section("At a glance", "Live numbers from the experiment database.", kicker="Results")

    featured = _featured_run(latest)
    detail = data.run_detail(featured["run_id"]) if featured else None
    ep = detail["episodes"] if detail else None
    tests = detail["evaluations"] if detail else None
    tests = tests[tests["kind"] == "test"] if tests is not None and not tests.empty else None
    best = float(ep["total_reward"].max()) if ep is not None and not ep.empty else None
    avg = float(ep["total_reward"].tail(50).mean()) if ep is not None and not ep.empty else None
    test_mean = float(tests.iloc[-1]["mean_return"]) if tests is not None and not tests.empty else None
    algo = algo_label(featured["algorithm"]) if featured else None
    who = f"{algo} on {featured['env']}, seed {featured['seed']}" if featured else ""
    card_grid([
        metric_card("Training runs", ov["runs"], f"{ov['completed_runs']} completed · {ov['failed_runs']} failed",
                    "{:,}", icon="runs", accent=SERIES[0]),
        metric_card("Best reward", best, f"best episode · {who}", icon="trophy",
                    accent="#f5b83d"),
        metric_card("Average reward", avg, f"last 50 training episodes (ε > 0) · {who}",
                    icon="avg", accent=SERIES[2]),
        metric_card("Evaluation score", test_mean,
                    f"held-out test mean, ε = 0 · {who}" if test_mean is not None else "no test yet",
                    icon="check", accent=SERIES[0]),
        metric_card("Episodes", ov["episodes_logged"], "logged across all runs", "{:,}", icon="layers",
                    accent=SERIES[1]),
        metric_card("Environment", featured["env"] if featured else None,
                    f"{algo} · seed {featured['seed']}" if featured else None, icon="globe", accent=SERIES[2]),
    ], min_width=150)

    section("How it works", "The same four steps repeat thousands of times.", kicker="The learning loop")
    steps(STEPS)
    section("What makes it different", kicker="Features")
    features(FEATURES)

    section("Featured run", "The newest completed training run. Reward should rise as the agent improves.",
            badge(featured["status"]) if featured else "", kicker="Learning curve")
    if featured is None:
        empty_state("No experiment data yet.", "sla train --config configs/frozenlake_qlearning.yaml",
                    "Run your first training experiment on the Training page to see learning results here.")
    else:
        color = AGENT_COLORS.get(algo or "", SERIES[0])
        trend = data.learning_trend(detail["episodes"])
        if trend:
            word = {"improving": "▲ Improving", "flat": "■ Flat", "declining": "▼ Declining"}[trend[0]]
            st.caption(f"Training trend: **{word}** — {trend[1]}")
        left, right = st.columns([3, 2], gap="medium")
        with left:
            chart_card(learning_curve(detail["episodes"], color=color, height=320), "Reward per episode",
                       featured["run_id"], key="ov_curve")
        with right:
            vals = detail["evaluations"]
            vals = vals[vals["kind"] == "validation"] if not vals.empty else vals
            if vals.empty:
                empty_state("No validation checks for this run.", next_step="Validation runs every few episodes "
                            "during training; random baselines have none.")
            else:
                chart_card(validation_curve(vals, color=color, height=320), "Frozen-policy validation",
                           "greedy return (ε = 0) during training", key="ov_val")

    section("Inside the agent", "An illustration of how the network turns what it sees into a choice.",
            kicker="Architecture")
    st.markdown('<div class="sla-panel sla-flow"><div>' + neural_flow() + '</div><div><p style="margin-top:0">'
                'The agent sees a <b>state</b>, passes it through a small neural network, and gets one '
                '<b>score</b> for each possible move. It picks the best score, receives a reward, and adjusts the '
                'network so good moves score higher next time. FrozenLake uses a simple score table instead of a '
                'network.</p></div></div>',
                unsafe_allow_html=True)
    section("Built with", kicker="Tech stack")
    stack(STACK)
