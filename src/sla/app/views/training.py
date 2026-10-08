"""Training: start a run (or a multi-seed experiment) and watch the metrics live."""

from __future__ import annotations

from dataclasses import replace

import pandas as pd
import streamlit as st

from sla.app.charts.figures import learning_curve, single_series
from sla.app.components.selectors import run_selector
from sla.app.components.ui import card_row, empty_state, hero, metric_card, section
from sla.app.state import services
from sla.app.styles.theme import AGENT_COLORS, SERIES
from sla.utils.errors import SLAError

LABELS = {"q_learning": "Q-learning", "dqn": "DQN"}


def _live_panel(cfg, total_episodes: int):
    """Placeholders updated from the training callback."""
    prog = st.progress(0.0, text="Starting…")
    cards = st.empty()
    chart = st.empty()
    rows: list[dict] = []
    color = AGENT_COLORS.get(LABELS.get(cfg.agent, ""), SERIES[0])

    def on_episode(info, ctx) -> bool:
        rows.append({"episode": info.episode, "total_reward": info.total_reward, "length": info.length,
                     "epsilon": info.epsilon, "mean_loss": info.mean_loss})
        done = info.episode + 1
        prog.progress(min(done / total_episodes, 1.0), text=f"{ctx.run_id} · episode {done:,} / {total_episodes:,}")
        if done % max(1, total_episodes // 60) == 0 or done == total_episodes:
            df = pd.DataFrame(rows)
            last = df.tail(50)
            cards.markdown(
                "<div style='display:grid;grid-template-columns:repeat(5,1fr);gap:.6rem'>"
                + metric_card("Episode", done, None, "{:,}")
                + metric_card("Reward", info.total_reward)
                + metric_card("Moving avg (50)", float(last["total_reward"].mean()))
                + metric_card("Epsilon", info.epsilon, None, "{:.3f}")
                + (metric_card("Loss", "n/a", "tabular Q-learning has no network") if cfg.agent != "dqn"
                   else metric_card("Loss", "warming up", "filling the replay buffer") if info.mean_loss is None
                   else metric_card("Loss", info.mean_loss, None, "{:.4f}"))
                + "</div>", unsafe_allow_html=True)
            chart.plotly_chart(learning_curve(df, window=min(50, max(5, len(df) // 5)), color=color, height=300),
                               width="stretch", key=f"live_{ctx.run_id}_{done}")
        return False
    return on_episode


def render() -> None:
    svc = services()
    hero("Training", "Configure an agent, start training and watch reward, ε, loss and episode length update live.")

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
                card_row([
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

    section("Inspect a training run", "Charts are read from the SQLite database.")
    runs = svc.experiments.trained_runs()
    if runs.empty:
        empty_state("No training runs yet.", "sla train --config configs/frozenlake_qlearning.yaml")
        return
    run_id = run_selector(runs, key="train_run")
    ep = svc.db.query_episodes(run_id)
    algo = svc.db.get_run(run_id)["algorithm"]
    color = AGENT_COLORS.get(LABELS.get(algo, ""), SERIES[0])
    st.plotly_chart(learning_curve(ep, color=color, title="Reward and moving average"), width="stretch")
    a, b, c = st.columns(3)
    a.plotly_chart(single_series(ep, "epsilon", "Epsilon", SERIES[2], "Exploration (ε)"), width="stretch")
    if ep["mean_loss"].notna().any():
        b.plotly_chart(single_series(ep, "mean_loss", "Loss", SERIES[1], "Huber loss (moving avg 20)", window=20),
                       width="stretch")
    else:
        with b:
            empty_state("No loss for tabular Q-learning (it has no network).")
    c.plotly_chart(single_series(ep, "length", "Steps", SERIES[0], "Episode length (moving avg 20)", window=20),
                   width="stretch")
