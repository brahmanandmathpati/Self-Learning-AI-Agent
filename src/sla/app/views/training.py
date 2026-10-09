"""Training: start a run (or a multi-seed experiment) and watch the metrics live."""

from __future__ import annotations

import html
from dataclasses import replace

import pandas as pd
import streamlit as st

from sla.app import data
from sla.app.charts.figures import learning_curve, single_series
from sla.app.components.chart_card import PLOTLY_CONFIG, chart_card
from sla.app.components.selectors import run_selector
from sla.app.components.ui import badge, card_grid, empty_state, hero, metric_card, section, skeleton
from sla.app.state import services
from sla.app.styles.theme import AGENT_COLORS, SERIES
from sla.utils.errors import SLAError

LABELS = {"q_learning": "Q-learning", "dqn": "DQN"}


TREND = {"improving": ("▲ Improving", "#22c55e"), "flat": ("■ Flat", "#f5b83d"),
         "declining": ("▼ Declining", "#ef5350")}


def _progress_html(done: int, total: int, run_id: str, live: bool) -> str:
    pct = 100 * min(done / max(total, 1), 1.0)
    state = badge("live", "Live training") if live else badge("completed", "Finished")
    return (f'<div class="sla-progress"><div class="row"><span>{state}</span>'
            f'<span class="mono">{html.escape(run_id)}</span>'
            f'<span><b style="color:var(--ink)">{done:,}</b> / {total:,} episodes · {pct:.0f}%</span></div>'
            f'<div class="track"><div class="fill{" live" if live else ""}" '
            f'style="width:{pct:.1f}%"></div></div></div>')


def _live_cards(df: pd.DataFrame, info, agent: str) -> list[str]:
    last = df.tail(50)
    if agent != "dqn":
        loss = metric_card("Loss", "n/a", "tabular Q-learning has no network", icon="loss")
    elif info.mean_loss is None:
        loss = metric_card("Loss", "warming up", "filling the replay buffer", icon="loss")
    else:
        loss = metric_card("Loss", info.mean_loss, "Huber, this episode", "{:.4f}", icon="loss", accent=SERIES[1])
    return [
        metric_card("Episode", len(df), None, "{:,}", icon="layers", count=False),
        metric_card("Reward", info.total_reward, "this episode", icon="trophy", accent="#f5b83d"),
        metric_card("Moving average", float(last["total_reward"].mean()), f"last {len(last)} episodes", icon="avg",
                    accent=SERIES[2]),
        loss,
        metric_card("Epsilon", info.epsilon, "exploration rate", "{:.3f}", icon="dice"),
        metric_card("Episode length", info.length, "steps this episode", "{:,}", icon="len", count=False),
    ]


def _live_panel(cfg, total_episodes: int):
    """Placeholders updated from the training callback (throttled to ~60 redraws per run)."""
    head = st.empty()
    head.markdown(_progress_html(0, total_episodes, "starting…", True) + skeleton(6, 96), unsafe_allow_html=True)
    trend_ph = st.empty()
    chart = st.empty()
    small = st.empty()
    rows: list[dict] = []
    color = AGENT_COLORS.get(LABELS.get(cfg.agent, ""), SERIES[0])

    def on_episode(info, ctx) -> bool:
        rows.append({"episode": info.episode, "total_reward": info.total_reward, "length": info.length,
                     "epsilon": info.epsilon, "mean_loss": info.mean_loss})
        done = info.episode + 1
        if done % max(1, total_episodes // 60) == 0 or done == total_episodes or done == 1:
            df = pd.DataFrame(rows)
            live = done < total_episodes
            head.markdown(_progress_html(done, total_episodes, ctx.run_id, live)
                          + '<div class="sla-grid">' + "".join(_live_cards(df, info, cfg.agent)) + "</div>",
                          unsafe_allow_html=True)
            trend = data.learning_trend(df)
            if trend:
                word, c = TREND[trend[0]]
                trend_ph.markdown(f'<div class="sla-badge" style="margin:.2rem 0 .4rem"><span class="sla-dot pulse" '
                                  f'style="--c:{c}"></span>Is it learning? {word} · {html.escape(trend[1])}</div>',
                                  unsafe_allow_html=True)
            window = min(50, max(5, len(df) // 5))
            chart.plotly_chart(learning_curve(df, window=window, color=color, height=300), width="stretch",
                               config=PLOTLY_CONFIG, key=f"live_{ctx.run_id}_{done}")
            if done % max(1, total_episodes // 20) == 0 or done == total_episodes:
                with small.container():
                    a, b, c2 = st.columns(3)
                    a.plotly_chart(single_series(df, "epsilon", "Epsilon", SERIES[2], "Epsilon", height=200),
                                   width="stretch", config=PLOTLY_CONFIG, key=f"le_{ctx.run_id}_{done}")
                    if df["mean_loss"].notna().any():
                        b.plotly_chart(single_series(df, "mean_loss", "Loss", SERIES[1], "Loss", height=200),
                                       width="stretch", config=PLOTLY_CONFIG, key=f"ll_{ctx.run_id}_{done}")
                    c2.plotly_chart(single_series(df, "length", "Steps", SERIES[0], "Episode length", height=200),
                                    width="stretch", config=PLOTLY_CONFIG, key=f"ln_{ctx.run_id}_{done}")
        return False
    return on_episode


def render() -> None:
    svc = services()
    hero("Training", "Configure an agent, start training and watch reward, ε, loss and episode length update live.",
         eyebrow="Live learning")

    with st.form("train_form"):
        c1, c2, c3 = st.columns(3)
        env_name = c1.selectbox("Environment", ["FrozenLake-v1", "CartPole-v1"])
        algorithms = svc.training.algorithms_for(env_name)
        algorithm = c2.selectbox("Algorithm", algorithms, format_func=lambda a: LABELS.get(a, a))
        mode = c3.selectbox("Mode", ["Single run", "Multi-seed experiment (+ random baseline)"])
        preset = svc.training.preset(env_name, algorithm)
        c4, c5, c6, c7 = st.columns(4)
        episodes = c4.number_input("Episodes", 10, 100_000, preset.episodes, step=50)
        seed = c5.number_input("Seed (single run)", 0, 10_000, preset.seed)
        seeds_text = c6.text_input("Seeds (experiment)", "0 1 2 3 4")
        eval_eps = c7.number_input("Test episodes", 5, 1000, 100, step=5)
        with st.expander("Hyper-parameters"):
            h1, h2, h3, h4 = st.columns(4)
            lr = h1.number_input("Learning rate α", 1e-5, 1.0, float(preset.learning_rate), format="%.5f")
            gamma = h2.number_input("Discount γ", 0.5, 1.0, float(preset.gamma), format="%.3f")
            eps_end = h3.number_input("Final ε", 0.0, 1.0, float(preset.epsilon_end), format="%.3f")
            decay = h4.number_input("ε decay steps", 100, 1_000_000, preset.epsilon_decay_steps, step=500)
            slippery = None
            if env_name == "FrozenLake-v1":
                slippery = st.checkbox("Slippery ice (stochastic transitions)",
                                       bool(preset.env_kwargs.get("is_slippery", False)))
        submitted = st.form_submit_button("Start training", type="primary")
    if algorithm == "dqn":
        st.caption("DQN on CPU: roughly a few minutes for 600 episodes. Keep this tab open while it trains.")

    if submitted:
        try:
            cfg = replace(preset, episodes=int(episodes), seed=int(seed), learning_rate=float(lr), gamma=float(gamma),
                          epsilon_end=float(eps_end), epsilon_decay_steps=int(decay))
            if slippery is not None:
                cfg = replace(cfg, env_kwargs={**cfg.env_kwargs, "is_slippery": bool(slippery)})
            section("Live training")
            if mode.startswith("Single"):
                out = svc.training.train(cfg, int(eval_eps), progress=_live_panel(cfg, cfg.episodes))
                st.success(f"Run {out.run_id} finished ({out.train.stopped_reason}).")
                card_grid([
                    metric_card("Untrained test mean", out.initial_eval.mean_return if out.initial_eval else None,
                                "before learning, ε = 0"),
                    metric_card("Trained test mean", out.final_eval.mean_return,
                                f"± {out.final_eval.std_return:.2f} over {out.final_eval.n_episodes} test episodes"),
                    metric_card("Success rate", out.final_eval.success_rate * 100, "goal reached / full episode",
                                "{:.0f}%"),
                    metric_card("Checkpoint", "best", out.checkpoint),
                ])
                st.session_state["selected_run"] = out.run_id
            else:
                from sla.utils.validation import validate_seeds
                seeds = validate_seeds([int(s) for s in seeds_text.replace(",", " ").split()])
                total = cfg.episodes
                out = svc.training.experiment(cfg, seeds, int(eval_eps), True, progress=_live_panel(cfg, total))
                st.success(f"Experiment #{out.experiment_id} finished: {len(out.runs)} seeds + random baseline. "
                           "See the Evaluation page for statistics.")
        except (SLAError, ValueError) as exc:
            st.error(f"Could not train: {exc}")
        except ImportError as exc:
            st.error(f"A required package is missing: {exc}. Install PyTorch (CPU) for the DQN.")

    section("Inspect a training run",
            "Every chart is read from the SQLite database · drag to zoom, double-click to reset.")
    runs = data.trained_runs()
    if runs.empty:
        empty_state("No training runs yet.", "sla train --config configs/frozenlake_qlearning.yaml",
                    "Start a run with the form above — its curves will appear here.")
        return
    run_id = run_selector(runs, key="train_run")
    ep = data.episodes(run_id)
    run = svc.db.get_run(run_id)
    algo = run["algorithm"]
    color = AGENT_COLORS.get(LABELS.get(algo, ""), SERIES[0])
    last = ep.tail(50)
    loss = ep["mean_loss"].dropna()
    card_grid([
        metric_card("Episodes", len(ep), run["status"], "{:,}", icon="layers"),
        metric_card("Best reward", float(ep["total_reward"].max()) if not ep.empty else None, "single episode",
                    icon="trophy", accent="#f5b83d"),
        metric_card("Moving average", float(last["total_reward"].mean()) if not ep.empty else None,
                    f"last {len(last)} episodes", icon="avg", accent=SERIES[2]),
        metric_card("Loss", float(loss.tail(50).mean()) if not loss.empty else ("n/a" if algo != "dqn" else None),
                    "mean of last 50" if not loss.empty else "Q-learning has no network", "{:.4f}", icon="loss"),
        metric_card("Epsilon", float(ep["epsilon"].iloc[-1]) if not ep.empty else None, "final exploration rate",
                    "{:.3f}", icon="dice"),
        metric_card("Episode length", float(last["length"].mean()) if not ep.empty else None, "mean of last 50",
                    "{:,.1f}", icon="len"),
    ])
    trend = data.learning_trend(ep)
    if trend:
        word, c = TREND[trend[0]]
        st.markdown(f'<div class="sla-badge" style="margin:.3rem 0 .6rem"><span class="sla-dot" style="--c:{c}"></span>'
                    f'Training trend: {word} · {html.escape(trend[1])}</div>', unsafe_allow_html=True)
    chart_card(learning_curve(ep, color=color, height=330), "Reward vs episode",
               "faint = reward per episode · bold = moving average", key="tr_reward")
    a, b, c = st.columns(3, gap="medium")
    with a:
        chart_card(single_series(ep, "epsilon", "Epsilon", SERIES[2], height=230), "Exploration (ε)",
                   "probability of a random action", key="tr_eps")
    with b:
        if ep["mean_loss"].notna().any():
            chart_card(single_series(ep, "mean_loss", "Loss", SERIES[1], window=20, height=230), "Huber loss",
                       "moving average of 20", key="tr_loss")
        else:
            empty_state("No loss for tabular Q-learning.", next_step="Q-learning updates a table, not a network.",
                        glyph="loss", tag="NOT APPLICABLE")
    with c:
        chart_card(single_series(ep, "length", "Steps", SERIES[0], window=20, height=230), "Episode length",
                   "moving average of 20", key="tr_len")
