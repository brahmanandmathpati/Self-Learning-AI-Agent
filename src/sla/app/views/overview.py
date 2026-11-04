"""Overview / landing page: hero, live numbers, how it works, features, live run, proof, architecture, team, FAQ."""

from __future__ import annotations

import html

import streamlit as st

from sla.app import auth, data, demo_seed, routes
from sla.app.charts.figures import learning_curve, validation_curve
from sla.app.components.chart_card import chart_card
from sla.app.components.landing import TEAM, architecture, faq, features, results_table, stack, steps, team
from sla.app.components.metric_card import card_grid, metric_card
from sla.app.components.motion import learning_loop, neural_flow
from sla.app.components.run_card import algo_label
from sla.app.components.section_header import section, sparks, words
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
    ("eye", "Vision Lab", "Teach it hand gestures live from your webcam, photos or videos — and reward it with a 👍."),
]
FAQ = [
    ("What is reinforcement learning?",
     "Learning by trial and error. The agent tries moves, gets **rewards** for good ones, and slowly prefers the moves "
     "that earn more reward — like a puppy learning a trick for treats."),
    ("Is this a chatbot?",
     "No. A chatbot answers from fixed knowledge. This agent changes its own numbers (a score table or a small "
     "neural network) from experience, and its game scores go up."),
    ("How do you prove it really learned?",
     "Learning is switched off and the agent plays games it has never seen, 5 times with different seeds. It is "
     "compared with its untrained self and a random player using Welch's t-test and a 95% confidence interval."),
    ("Why two games?",
     "FrozenLake has 16 squares, so a simple score table works (Q-learning). CartPole has endless situations, so a "
     "neural network is needed (DQN)."),
    ("Does the AI explanation make up numbers?",
     "No. Every number in a written insight is checked against facts computed from the database; a note with a "
     "number that is not in the facts is rejected."),
    ("Does the Vision Lab store my face?",
     "No. The camera picture is processed in memory to find 21 hand points, and only those numbers are kept. Pictures "
     "are saved only if you tick “save images”, and “Delete my data” removes everything."),
    ("Do I need an account?",
     "No. You can look at every page as a visitor. Log in (or sign up) to start training, write insights and "
     "rate them."),
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


def _hero(ov: dict) -> None:
    """Native hero (page links keep the session alive): headline, value line, live chips, two CTAs, loop art."""
    state = "running" if ov["running_runs"] else "idle"
    user = auth.current_user()
    first = user["name"].split()[0] if user and user["kind"] != "guest" else ""
    chips = badge("online", "System online") + badge(state, STATE_TEXT[state])
    if user and user["kind"] == "guest":
        chips += badge("info", "Guest · view only")
    eyebrow = f"Welcome back, {html.escape(first)}" if first else "Self-Learning AI Agent"
    with st.container(key="hero"):
        st.markdown(sparks(), unsafe_allow_html=True)
        left, right = st.columns([1.65, 1], vertical_alignment="center")
        with left:
            st.markdown(f'<div class="sla-hero-copy"><div class="eyebrow">{eyebrow}</div>'
                        f'<h1>{words("An AI agent that learns from experience.")}</h1>'
                        '<p>It starts knowing nothing, learns two games from rewards alone, and proves it on games '
                        f'it has never seen.</p><div class="chips">{chips}</div></div>', unsafe_allow_html=True)
            with st.container(horizontal=True, key="hero_cta"):
                routes.link("training", "Start training →", "gold", "hero")
                routes.link("evaluation", "See the proof", "outline", "hero")
        with right:
            st.markdown(f'<div class="sla-hero-art">{learning_loop()}</div>', unsafe_allow_html=True)


def _status_line(ov: dict) -> None:
    """What used to be the sidebar 'System' and 'Data' cards, as one quiet line."""
    latest = ov["latest_run"]
    parts = [f"<b>{ov['runs']}</b> runs", f"<b>{ov['experiments']}</b> experiments",
             f"<b>{ov['episodes_logged']:,}</b> episodes"]
    if latest:
        parts.append(f"latest run <code>{html.escape(str(latest['run_id']))}</code>")
    snap = demo_seed.snapshot_info()
    note = (" · includes a read-only snapshot of real runs from the project laptop; new runs started here are "
            "added on top until the app restarts") if snap else ""
    st.markdown(f'<p class="sla-status">Database: {" · ".join(parts)}{note}.</p>', unsafe_allow_html=True)


def _proof() -> None:
    """Real results from completed experiments: trained vs random with Welch p, plus the ablation means."""
    rows = []
    exps = data.experiments("pipeline")
    for _, e in (exps.iterrows() if not exps.empty else []):
        exp = data.experiment(int(e["experiment_id"]))
        summ = (exp or {}).get("summary") or {}
        cmp = summ.get("trained_vs_random")
        if not exp or exp.get("status") != "completed" or not cmp:
            continue
        rows.append((html.escape(str(exp.get("env") or "—")), algo_label(exp.get("algorithm") or ""),
                     f"{cmp['mean_trained']:,.2f}", f"{cmp['mean_random']:,.2f}",
                     f"{cmp['diff']:+,.2f} <small>[{cmp['diff_ci_low']:,.2f}, {cmp['diff_ci_high']:,.2f}]</small>",
                     f"{cmp['p_value']:.2g}"))
    if not rows:
        empty_state("No completed multi-seed experiment yet.",
                    "sla pipeline --config configs/frozenlake_qlearning.yaml --seeds 0 1 2 3 4",
                    "Run a multi-seed experiment to see trained-vs-random statistics here.", glyph="flask")
    else:
        results_table(rows)
    abl = data.experiments("ablation")
    if not abl.empty:
        df, _ = data.ablation(int(abl.iloc[0]["experiment_id"]))
        if not df.empty:
            means = df.groupby("variant")["final_mean"].mean()
            names = {"full": "Full DQN", "no_replay": "No replay memory", "no_target": "No target network"}
            chips = " · ".join(f"<b>{names.get(k, k)}</b> {v:,.2f}" for k, v in means.items())
            st.markdown(f'<p class="sla-status">Ablation (mean test return, CartPole): {chips}. Removing either '
                        'part makes the agent much worse.</p>', unsafe_allow_html=True)
    with st.container(horizontal=True, key="proof_cta"):
        routes.link("evaluation", "See the full evaluation", "outline", "proof")
        routes.link("ablation", "Open the ablation study", "outline", "abl")


def _cta_band() -> None:
    with st.container(key="ctaband"):
        st.markdown('<div class="sla-cta-copy"><div class="eyebrow">Get started</div>'
                    '<h2>Train your first agent in under a minute.</h2>'
                    '<p>A FrozenLake Q-learning run finishes in well under a minute on a laptop CPU.</p></div>',
                    unsafe_allow_html=True)
        with st.container(horizontal=True, key="cta_actions"):
            if auth.can_act():
                routes.link("training", "Start training →", "gold", "band")
            else:
                st.button("Sign up — it's free", key="band_signup", type="primary", on_click=auth.open_auth,
                          args=("Sign up",))
                routes.link("training", "Look around first", "outline", "band")


def render() -> None:
    ov = data.overview()
    latest = ov["latest_run"]
    _hero(ov)

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
    _status_line(ov)

    section("How it works", "The same four steps repeat thousands of times.", kicker="The learning loop")
    steps(STEPS)
    section("What makes it different", kicker="Features")
    features(FEATURES)
    routes.link("vision", "Teach the agent with your hands →", "outline", "vision")

    section("Live from the lab", "The newest completed training run. Reward should rise as the agent improves.",
            badge(featured["status"]) if featured else "", kicker="Live demo")
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
            chart_card(learning_curve(detail["episodes"], color=color, height=300), "Reward per episode",
                       featured["run_id"], key="ov_curve")
        with right:
            vals = detail["evaluations"]
            vals = vals[vals["kind"] == "validation"] if not vals.empty else vals
            if vals.empty:
                empty_state("No validation checks for this run.", next_step="Validation runs every few episodes "
                            "during training; random baselines have none.")
            else:
                chart_card(validation_curve(vals, color=color, height=300), "Frozen-policy validation",
                           "greedy return (ε = 0) during training", key="ov_val")
        routes.link("runs", "Open the full dashboard →", "outline", "live")

    section("Proof, not promises", "Held-out test results from completed experiments (5 seeds each).",
            kicker="Results")
    _proof()

    section("How it is built", "Each layer has one job and talks only to the layer below it.", kicker="Architecture")
    a, b = st.columns([1, 1.15], gap="large", vertical_alignment="center")
    a.markdown(architecture(), unsafe_allow_html=True)
    b.markdown('<div class="sla-panel sla-flowbox">' + neural_flow() + '<p>The agent sees a <b>state</b>, a small '
               'neural network gives one <b>score</b> per move, it picks the best, gets a reward, and adjusts the '
               'network. FrozenLake uses a simple score table instead.</p></div>', unsafe_allow_html=True)
    stack(STACK)

    section("The team", "Four final-year B.Tech CSE (AI) students, one shared codebase.", kicker="People")
    team(TEAM)
    section("Questions", kicker="FAQ")
    faq(FAQ)
    _cta_band()
