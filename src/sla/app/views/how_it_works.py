"""How it works: the whole project, from a training command to a verified result, in plain words.

Read-only: every result number comes from the database or the YAML configs, never from this file. The one live
demo (FrozenLake Q-learning) runs in the visitor's session, is deterministic and never touches the database.
"""

from __future__ import annotations

import html

import pandas as pd
import streamlit as st

from sla.app import data, how_data, routes
from sla.app.charts.figures import group_bars, learning_curve
from sla.app.charts.how_figures import epsilon_chart, q_grid
from sla.app.components.chart_card import chart_card
from sla.app.components.landing import features, steps
from sla.app.components.metric_card import NOT_RUN, card_grid, metric_card
from sla.app.components.motion import neural_flow
from sla.app.components.ui import hero, note_box, section, verdict
from sla.app.how_content import (
    FILE_CHIPS,
    GLOSSARY,
    SAFETY_TEXT,
    START_TRAINING_STEPS,
    TABLE_NOTES,
    TEXT,
    limits_from_docs,
    resolve,
)
from sla.app.styles.theme import SERIES, VARIANT_COLORS, VARIANT_LABELS
from sla.app.views.evaluation import _evidence
from sla.evaluation.evaluate import EVAL_SEED_BASE, TEST_SEED_BASE
from sla.explain import (
    ACTION_ARROWS,
    LAKE_MAP,
    best_values,
    describe_update,
    dqn_parameter_count,
    epsilon_curve,
    greedy_walk,
    moving_average,
    policy_arrows,
    practice_questions,
    q_update,
    random_success_rate,
    run_lake_demo,
)
from sla.training.config import RunConfig, load_config
from sla.utils.seeding import episode_seed

MR_KEY = "how_mr"
DEMO_LABEL = "Illustrative demo, re-run in your browser session. Not a stored result."
DEMO_SEED = 0


# ------------------------------------------------------------------------------------------ small helpers
@st.cache_data(show_spinner=False)
def _config(name: str) -> RunConfig | None:
    """A YAML config from configs/, or None if the file cannot be read (the page then says 'not available')."""
    try:
        return load_config(resolve(f"configs/{name}"))
    except Exception:  # noqa: BLE001 - a missing or invalid file must never break the page
        return None


@st.cache_data(show_spinner=False)
def _lake_demo(episodes: int, alpha: float, gamma: float, eps_start: float, eps_end: float, eps_steps: int,
               seed: int):
    return run_lake_demo(episodes, alpha, gamma, eps_start, eps_end, eps_steps, seed=seed)


@st.cache_data(show_spinner=False)
def _random_rate(seed: int) -> float:
    return random_success_rate(seed=seed)


def _chips(key: str) -> None:
    """Small monospace chips with the files that implement this section (all checked by a unit test)."""
    items = "".join(f"<span><code>{html.escape(p)}</code></span>" for p in FILE_CHIPS.get(key, ()))
    if items:
        st.markdown(f'<div class="sla-stack" aria-label="Files for this section">{items}</div>',
                    unsafe_allow_html=True)


def _head(key: str, title: str, kicker: str) -> None:
    """Section header + file chips + the optional Roman-Marathi helper line."""
    section(title, TEXT["en"][key], kicker=kicker)
    _chips(key)
    if st.session_state.get(MR_KEY):
        note_box(TEXT["mr"][key])


def _cards(*cards: str) -> None:
    card_grid(list(cards), min_width=170)


# ------------------------------------------------------------------------------------------ the sections
def _big_picture(fl: RunConfig | None) -> None:
    _head("big_picture", "The big picture", "1 · Overview")
    items = [
        ("YAML config", "configs/*.yaml: game, algorithm, seed, episodes, learning settings."),
        ("CLI or website", "`sla train` in a terminal, or the Training page here."),
        ("Services", "services/: one entry point per feature (training, evaluation, reflection)."),
        ("Pipeline", "training/pipeline.py: single run, multi-seed experiment, baseline or ablation."),
        ("Runner", "training/runner.py: plays the episodes. The only place where learning happens."),
        ("Agent + environment", "agents/q_learning.py or agents/dqn.py, with envs/factory.py."),
        ("Checkpoints", "checkpoints/manager.py: save, resume and keep the best agent."),
        ("SQLite database", "database/store.py: every episode, test and note is stored."),
        ("Evaluation + statistics", "evaluation/ and stats.py: frozen tests, t-test, confidence interval."),
        ("This website", "app/: reads the database and draws the pages."),
    ]
    steps([(t, d.replace("`", "")) for t, d in items])
    st.caption("Diagram in words: config → CLI or website → services → pipeline → runner → agent + environment "
               "→ checkpoints → SQLite database → evaluation and statistics → this website.")
    note_box("The runner is the only place where learning happens. The website only reads.")


def _one_step(fl: RunConfig | None) -> None:
    _head("one_step", "One training step, in four moves", "2 · The learning loop")
    steps([("Observe", "The agent looks at the state, for example 'I am on square 5'."),
           ("Choose", "It picks a move: random with chance ε, otherwise the best move it knows."),
           ("Act", "The game moves and returns a reward and the new state."),
           ("Learn", "One number in the Q-table changes a little. Try the calculator below.")])
    alpha = fl.learning_rate if fl else 0.1
    gamma = fl.gamma if fl else 0.99
    st.markdown("**Q-learning update calculator** (starts with the example: old Q = 0, reward = 1, game ended)")
    c1, c2, c3 = st.columns(3)
    old_q = c1.number_input("Old Q", value=0.0, step=0.05, format="%.4f", key="how_oldq")
    reward = c2.number_input("Reward r", value=1.0, step=0.5, format="%.2f", key="how_r")
    best_next = c3.number_input("Best next Q", value=0.0, step=0.05, format="%.4f", key="how_next")
    c4, c5, c6 = st.columns(3)
    a = c4.number_input("α (learning rate)", value=float(alpha), min_value=0.0, max_value=1.0, step=0.05,
                        format="%.3f", key="how_alpha")
    g = c5.number_input("γ (discount)", value=float(gamma), min_value=0.0, max_value=1.0, step=0.01,
                        format="%.3f", key="how_gamma")
    ended = c6.checkbox("The game ended on this move", value=True, key="how_ended")
    u = q_update(float(old_q), float(reward), float(best_next), bool(ended), float(a), float(g))
    st.code("new Q = old Q + α × (target − old Q)\n" + "\n".join(describe_update(u)), language="text")
    _cards(metric_card("New Q", u.new_q, "the number written into the table", "{:.4f}", icon="check",
                       accent=SERIES[0]))


def _watch(fl: RunConfig | None) -> None:
    _head("watch", "Watch it learn", "3 · Q-learning on FrozenLake")
    if fl is None:
        st.info(f"{NOT_RUN}: configs/frozenlake_qlearning.yaml could not be read, so the demo is not available.")
        return
    st.caption(DEMO_LABEL)
    demo = _lake_demo(fl.episodes, fl.learning_rate, fl.gamma, fl.epsilon_start, fl.epsilon_end,
                      fl.epsilon_decay_steps, DEMO_SEED)
    mode = st.radio("Show the agent", ["Before training", "After training"], index=1, horizontal=True,
                    key="how_mode")
    ep = st.slider("Episodes trained", 0, fl.episodes, min(300, fl.episodes), key="how_eps",
                   disabled=mode == "Before training")
    before = mode == "Before training" or ep == 0
    q = demo.q_by_episode[0 if before else ep]
    left, right = st.columns(2, gap="medium")
    with left:
        chart_card(q_grid(list(LAKE_MAP), q, height=330), "Best move per square",
                   "arrow = best move · brightness and number = its Q value", key="how_grid")
    with right:
        if before:
            st.caption("Before training: all numbers are 0, so every move is a random guess.")
            _cards(metric_card("Success rate · random moves", _random_rate(DEMO_SEED), "share of games won",
                               "{:.1%}", icon="dice", accent=SERIES[1]))
        else:
            n = max(ep, 1)
            table = pd.DataFrame({"episode": range(n), "total_reward": demo.success[:n]})
            chart_card(learning_curve(table, 50, SERIES[0], height=240), "Success while training",
                       "1 = reached the goal · line = moving average of 50 episodes", key="how_succ")
            reached, path = greedy_walk(q)
            recent = float(moving_average(demo.success[:n])[-1])
            _cards(metric_card("Success · last 50 episodes", recent, "ε > 0, still exploring", "{:.0%}",
                               icon="avg", accent=SERIES[1]),
                   metric_card("Success · ε = 0, learning off", 1.0 if reached else 0.0,
                               f"greedy walk of {len(path) - 1} steps", "{:.0%}", icon="check", accent=SERIES[2]))
    arrows = policy_arrows(q)
    st.caption("Same code, only the numbers changed.")
    st.caption("Text version of the grid (square: best move): "
               + ", ".join(f"{i}: {a}" for i, a in enumerate(arrows) if LAKE_MAP[i // 4][i % 4] in "SF") + ". "
               + f"Highest Q value in the table: {float(best_values(q).max()):.3f}. Arrow key: "
               + " ".join(ACTION_ARROWS) + " = left, down, right, up.")


def _explore(fl: RunConfig | None) -> None:
    _head("explore", "Explore or exploit", "4 · Epsilon")
    if fl is None:
        st.info(f"{NOT_RUN}: the FrozenLake config could not be read, so the chart is not available.")
        return
    xs, ys = epsilon_curve(fl.epsilon_start, fl.epsilon_end, fl.epsilon_decay_steps)
    chart_card(epsilon_chart(xs, ys), "ε over training steps", "drawn from agents/schedules.py", key="how_eps_chart")
    st.caption(f"Chart in words: ε falls in a straight line from {fl.epsilon_start:g} to {fl.epsilon_end:g} over "
               f"{fl.epsilon_decay_steps:,} steps, then stays flat.")
    st.markdown("**ε (epsilon) is the chance of making a random move.** It starts high so the agent explores, and "
                "falls so it can use what it has learned. **At test time ε = 0**, so luck cannot help.")


def _dqn(cp: RunConfig | None) -> None:
    _head("dqn", "For big games: the DQN", "5 · Neural network learner")
    if cp is None:
        st.info(f"{NOT_RUN}: configs/cartpole_dqn.yaml could not be read, so these sizes are not available.")
        return
    d = cp.dqn
    st.markdown(f'<div class="sla-panel sla-flowbox">{neural_flow()}</div>', unsafe_allow_html=True)
    st.caption(f"Network: 4 state numbers → {d.hidden_size} → {d.hidden_size} → 2 scores (push left, push right); "
               f"{dqn_parameter_count(d.hidden_size):,} learnable numbers.")
    _cards(metric_card("Replay memory", d.buffer_size, "old moves kept", "{:,}", icon="db", accent=SERIES[0]),
           metric_card("Batch size", d.batch_size, "random moves per learning step", "{:,}", icon="layers"),
           metric_card("Target refresh", d.target_update_every, "gradient steps between copies", "{:,}",
                       icon="clock", accent=SERIES[1]),
           metric_card("Learning rate", cp.learning_rate, "Adam optimiser", "{:g}", icon="spark"),
           metric_card("Hidden width", d.hidden_size, "neurons per hidden layer", "{:,}", icon="cpu",
                       accent=SERIES[2]))
    steps([("Trick 1: replay memory", "Consecutive moves look almost the same, which makes learning shaky. "
                                      "Storing old moves and learning from random samples fixes that."),
           ("Trick 2: target network", "If the network chases its own changing answers it becomes unstable. A "
                                       "frozen copy gives steady targets.")])


def _prove(cp: RunConfig | None) -> None:
    _head("prove", "How we prove it learned", "6 · Fair testing")
    exps = data.experiments("pipeline")
    cart = exps[exps["env"] == "CartPole-v1"] if not exps.empty else exps
    summary: dict = {}
    seeds_text, games_text = NOT_RUN.lower(), NOT_RUN.lower()
    exp_id = None
    if not cart.empty:
        exp_id = int(cart.iloc[0]["experiment_id"])  # list_experiments is newest first
        exp = data.experiment(exp_id) or {}
        if exp.get("status") == "completed":
            summary = exp.get("summary") or {}
        seeds = len(summary.get("trained_test_means", []))
        seeds_text = str(seeds) if seeds else seeds_text
        tests = data.evaluations("test")
        tests = tests[tests["experiment_id"] == exp_id] if not tests.empty else tests
        if not tests.empty:
            games_text = f"{int(tests['n_episodes'].median())}"
    steps([("Training games", f"Reset seed = seed × {episode_seed(1, 0):,} + episode, so training never repeats."),
           ("Validation games", f"Seeds {EVAL_SEED_BASE:,} + i. Used to pick the best checkpoint."),
           ("Test games", f"Seeds {TEST_SEED_BASE:,} + i. Used once, for the final score."),
           ("Frozen agent", f"ε = 0, no learning. {seeds_text} seeds × {games_text} test games each."),
           ("Statistics", "Welch t-test and a bootstrap 95% interval compare it with a random player.")])
    st.markdown("**Verdict rule:** learning verified = p &lt; 0.05 **and** the confidence interval of the gain is "
                "above 0 (the same rule the Evaluation page uses).", unsafe_allow_html=True)
    if not summary:
        st.info(f"{NOT_RUN}: no completed CartPole experiment in the database yet, so there is no live verdict.")
    else:
        kind, detail = _evidence(summary)
        st.markdown("**Current verdict · latest CartPole experiment**")
        verdict(kind, detail)
    routes.link("evaluation", "Open the Evaluation page →", "outline", "how_eval_link")


def _data_tables() -> None:
    _head("data", "Where the data lives", "7 · SQLite")
    counts = how_data.table_counts()
    rows = [{"Table": t, "What it holds": note, "Rows": f"{counts[t]:,}" if t in counts else "not available"}
            for t, note in TABLE_NOTES]
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")


def _start_training(fl: RunConfig | None, cp: RunConfig | None) -> None:
    _head("start_training", "What happens when you press Start training", "8 · Step by step")
    steps([(f"{i}. {t}", f"{d} ({f})") for i, (t, d, f) in enumerate(START_TRAINING_STEPS, 1)])
    if fl and cp:
        st.markdown(f"**Validation interval** (from the configs): every {fl.eval_every} episodes on FrozenLake and "
                    f"every {cp.eval_every} on CartPole, {fl.eval_episodes} and {cp.eval_episodes} games each.")
    note_box(SAFETY_TEXT)


def _ablation() -> None:
    _head("ablation", "Why the two tricks matter (ablation)", "9 · Remove one part")
    exps = data.experiments("ablation")
    if exps.empty:
        st.info(f"{NOT_RUN}: no ablation has been run yet, so this chart is not available.")
        return
    df, _ = data.ablation(int(exps.iloc[0]["experiment_id"]))
    if df.empty:
        st.info(f"{NOT_RUN}: the latest ablation has no finished runs yet.")
        return
    labels = dict(VARIANT_LABELS)
    colors = {VARIANT_LABELS[k]: v for k, v in VARIANT_COLORS.items()}
    df = df.assign(label=df["variant"].map(labels))
    agg = df.groupby("label", sort=False)["final_mean"].agg(mean="mean", std="std", n="count").reset_index()
    pts = df.rename(columns={"final_mean": "mean_return"})
    chart_card(group_bars(agg, "label", "mean", "std", colors, pts, height=300), "Held-out test return by variant",
               "bar = mean · whisker = std · dot = one seed", key="how_abl")
    best = agg.loc[agg["mean"].idxmax()]
    st.caption("Chart in words: " + "; ".join(f"{r['label']} scored {r['mean']:,.2f}" for _, r in agg.iterrows())
               + f". The highest is {best['label']}.")
    routes.link("ablation", "Open the Ablation page →", "outline", "how_abl_link")


def _beyond() -> None:
    _head("beyond", "Beyond the games", "10 · Two more layers")
    features([("flask", "Reflection layer",
               "Facts from the database become a plain-language note. A number checker compares every number in "
               "the note with the facts; a note with a wrong number is rejected. (reflection/grounding.py)"),
              ("brain", "Vision Lab",
               "Hand points from a photo, video or webcam become 42 numbers, and a small learner recognises the "
               "gesture. Gestures can also act as rewards. (vision/hands.py, features.py, learners.py)")],
             min_width=280)
    routes.link("reflection", "Open Reflection →", "outline", "how_refl_link")
    routes.link("vision", "Open Vision Lab →", "outline", "how_vision_link")


def _limits() -> None:
    _head("limits", "What we do NOT claim", "11 · Honest limits")
    with st.container(border=True):
        st.markdown("\n".join(f"- {b}" for b in limits_from_docs()))


def _glossary_and_practice(fl: RunConfig | None, cp: RunConfig | None) -> None:
    _head("glossary", "Words you will hear, and practice", "12 · For the review")
    with st.expander("Words you will hear"):
        st.markdown("\n".join(f"- **{t}**: {d}" for t, d in GLOSSARY))
    if fl is None or cp is None:
        st.info(f"{NOT_RUN}: the configs could not be read, so the practice questions are not available.")
        return
    st.markdown("**Practice questions** (open an answer after you try it)")
    qs = practice_questions(fl.learning_rate, fl.gamma, fl.epsilon_start, fl.epsilon_end, fl.epsilon_decay_steps,
                            cp.dqn.target_update_every, TEST_SEED_BASE)
    for i, (question, answer) in enumerate(qs, 1):
        st.markdown(f"**Q{i}.** {question}")
        with st.expander(f"Answer {i}"):
            st.markdown(answer)


def _try_it(fl: RunConfig | None) -> None:
    _head("try_it", "Try it yourself", "13 · Run it")
    seed, eps = (fl.seed, fl.episodes) if fl else (0, 2000)
    st.code(f"sla train --config configs/frozenlake_qlearning.yaml --seed {seed} --episodes {eps}", language="bash")
    st.code("sla pipeline --config configs/cartpole_dqn.yaml --seeds 0 1 2 3 4", language="bash")
    st.code("sla ablation --config configs/cartpole_dqn.yaml --seeds 0 1 2 3 4", language="bash")
    st.code("streamlit run src/sla/app/main.py", language="bash")
    routes.link("training", "Open the Training page →", "gold", "how_train_link")
    routes.link("evaluation", "Open the Evaluation page →", "outline", "how_eval_link2")


def render() -> None:
    hero("How it works", "From a training command to a verified result: every step, with the real files and numbers.",
         eyebrow="Under the hood")
    st.toggle("Marathi-English helper lines", key=MR_KEY,
              help="Adds a one-line Roman-Marathi explanation under each section. English stays the default.")
    routes.link("overview", "← Back to the Overview", "outline", "how_back")
    fl, cp = _config("frozenlake_qlearning.yaml"), _config("cartpole_dqn.yaml")
    _big_picture(fl)
    _one_step(fl)
    _watch(fl)
    _explore(fl)
    _dqn(cp)
    _prove(cp)
    _data_tables()
    _start_training(fl, cp)
    _ablation()
    _beyond()
    _limits()
    _glossary_and_practice(fl, cp)
    _try_it(fl)
