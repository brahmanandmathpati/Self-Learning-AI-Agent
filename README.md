# Self-Learning AI Agent

> An agent that starts with **no trained policy**, interacts with an environment, and **measurably improves from reward** — tabular Q-learning on FrozenLake and a from-scratch Deep Q-Network on CartPole, with held-out evaluation, statistics, an ablation study, SQLite experiment tracking, grounded explanations and a Streamlit dashboard.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-CPU-orange)
![Gymnasium](https://img.shields.io/badge/Gymnasium-FrozenLake%20%7C%20CartPole-green)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-lightgrey)

Final-year B.Tech CSE (AI Specialization) project, 2023–2027.

---

## Problem statement

Most student "AI agents" are static: they prompt an LLM with fixed instructions and behave the same on day 1 and day 100. Chat history, prompt edits and better-worded LLM text are **not learning**. This project builds an agent whose **policy actually changes from experience** and proves the improvement with a rigorous protocol.

## How learning actually happens

The agent receives `(state, action, reward, next_state)` from the environment and updates its value estimates:

**Tabular Q-learning (FrozenLake-v1)**

```
Q(s, a) ← Q(s, a) + α [ r + γ · max_a' Q(s', a') − Q(s, a) ]       (target = r at a terminal step)
```

A worked example by hand is in [`docs/q_learning_by_hand.md`](docs/q_learning_by_hand.md); the unit test `test_update_matches_hand_calculation` checks the code against it.

**Deep Q-Network (CartPole-v1)** — written by us in PyTorch (no Stable-Baselines3):

```
batch  = replay_buffer.sample(B)                         # s, a, r, s', terminated
q      = online_net(s)[a]
target = r + γ · (1 − terminated) · max_a' target_net(s')[a']
loss   = Huber(q, target);  Adam/AdamW step;  clip grad-norm
every C gradient steps: target_net ← online_net
```

Truncation at the 500-step time limit is **not** terminal, so the target still bootstraps.

## How we prove it learned

| Evidence | How |
|---|---|
| Learning curve | training return per episode with a moving average, 5 seeds |
| Frozen-policy evaluation | ε = 0, no gradient / replay / target updates, on a deep copy of the agent |
| Held-out seeds | training resets `seed×100000+episode`; validation `10 000 000+i` (picks the best checkpoint); test `20 000 000+i` (reported numbers only) |
| Before / after | the **untrained** policy and the **trained** policy play the same test seeds |
| Against chance | trained vs random-action baseline: Welch's t-test + bootstrap 95% CI over seeds |
| Persistence | a checkpoint reloaded in a **new process** keeps its score (test) |
| Ablation | full DQN vs no replay vs no target network |

## Results

> Results are produced only by real runs and are stored in the SQLite database. Regenerate the tables with
> `python scripts/make_tables.py` — they are written to [`results/`](results/). Until experiments are run, the
> dashboard and the tables show **NOT RUN**.

| Agent | Environment | Held-out test return (mean ± std over 5 seeds) |
|---|---|---|
| Random baseline | FrozenLake-v1 4×4 | NOT RUN |
| Tabular Q-learning | FrozenLake-v1 4×4 | NOT RUN |
| Random baseline | CartPole-v1 | NOT RUN |
| DQN | CartPole-v1 | NOT RUN |
| DQN without replay / without target network | CartPole-v1 | NOT RUN |

---

## Architecture

```
            ┌──────────── Streamlit dashboard (src/sla/app) ─────┐      CLI: sla ...
            │ pages · components · charts (Plotly) · styles       │        │
            └──────────────────────────┬──────────────────────────┘        │
                                       ▼                                   ▼
              Service layer (src/sla/services): Training · Evaluation · Experiment · Reflection · Checkpoint
                                       │
              Training pipeline (training/pipeline.py): train_run · resume_run · run_experiment · run_baseline
                                       │                                         evaluation/ablation.py
   ┌──────── Runner + callbacks (training/runner.py) — the only place learning happens ────────┐
   │  Environment (envs/) ⇄ Agent (agents/: random, Q-learning, DQN) ⇄ Replay buffer (memory/)  │
   │  callbacks: database · initial eval · transition validation · checkpoints · validation     │
   │             eval (best checkpoint) · regression monitor · divergence guard · UI progress   │
   └──────────────┬───────────────────────────────┬────────────────────────────────────────────┘
                  ▼                               ▼
        SQLite (database/store.py)         Checkpoints on disk (checkpoints/manager.py)
        experiments · runs · episodes ·    runs/<run_id>/checkpoints/{ep_XXXXXX, best, latest.json}
        metrics · evaluations · ablation
        · reflections · feedback           Evaluation (evaluation/): frozen policy · metrics · stats
                  │
                  ▼
        Reflection (reflection/): facts → template or optional Ollama → number validation
```

Details: [`docs/architecture.md`](docs/architecture.md).

## Installation

Requirements: Python 3.10+ and a normal laptop CPU (no GPU needed).

```bash
git clone https://github.com/brahmanandmathpati/Self-Learning-AI-Agent.git
cd Self-Learning-AI-Agent
python -m venv .venv
source .venv/bin/activate                 # Windows: .venv\Scripts\activate
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -e ".[dev]"
sla init-db
```

Optional (explanations by a local LLM): install [Ollama](https://ollama.com) and `ollama pull qwen2.5:1.5b`. Everything works without it.

## Commands

| Command | What it does |
|---|---|
| `sla train --config configs/frozenlake_qlearning.yaml --seed 0` | Train one run (FrozenLake, a few seconds) |
| `sla train --config configs/cartpole_dqn.yaml --seed 0` | Train the DQN (minutes on CPU) |
| `sla train --resume runs/<run_id>` | Resume a stopped run from its latest checkpoint |
| `sla evaluate --run runs/<run_id> --episodes 100` | Frozen-policy evaluation of the best checkpoint on test seeds |
| `sla pipeline --config configs/cartpole_dqn.yaml --seeds 0 1 2 3 4` | 5 seeds + random baseline + Welch / bootstrap statistics |
| `sla ablation --config configs/cartpole_dqn.yaml --seeds 0 1 2 3 4` | Full DQN vs no replay vs no target network |
| `sla baseline --config configs/cartpole_random.yaml` | Random-action baseline only |
| `sla reflect --run runs/<run_id> [--llm]` | Grounded plain-language summary of a run |
| `sla runs` | List stored runs |
| `sla dashboard` | Launch the dashboard (http://localhost:8501) |

`python -m sla <command>` works too. Full reference: [`docs/usage.md`](docs/usage.md).

## Dashboard

`sla dashboard` opens a dark, multi-page experimentation dashboard: **Overview**, **Training** (start runs and watch reward, moving average, ε, loss and episode length live), **Agent comparison**, **Evaluation** (5-seed results, CI, Welch's t-test, before/after), **Ablation**, **Run explorer** (config, evaluations, checkpoints, logs), **Reflection** (notes, facts, validation status, ratings), **Environments** and **About**. Every number is read from the database; empty sections say NOT RUN.

<!-- Screenshots: add docs/screenshots/*.png after the first real experiments. -->

## Experiments and reproducibility

Every run records its seed, full config (hyper-parameters), environment, algorithm, start/end time, status, git commit SHA, checkpoint paths and metrics in SQLite, plus `config.yaml`, `metrics.json` and `run.log` in `runs/<run_id>/`. See [`docs/experiments.md`](docs/experiments.md) and [`docs/evaluation.md`](docs/evaluation.md).

## Reflection layer

1. `reflection/stats.py` computes facts from the database (window means, best validation score, untrained vs trained test score, random baseline, Welch p-value, bootstrap CI, ε, loss).
2. A deterministic template turns the facts into a note; optionally a local Ollama model writes it instead, receiving **only** the facts.
3. `reflection/grounding.py` extracts every number from the note and rejects it unless it matches a fact (±0.01). Rejected LLM notes are kept for transparency and the template is shown.

## Testing

```bash
pytest              # unit, integration and dashboard tests (no internet, no Ollama, no GPU)
pytest -m smoke     # short DQN training + resume
ruff check .
```

CI (GitHub Actions) runs lint, tests and the smoke run on every pull request.

## Project structure

```
configs/            YAML experiment configs (frozenlake_qlearning, cartpole_dqn, ablation_*, random, smoke)
src/sla/
  envs/             environment factory, seeding, end reasons
  agents/           base, random_agent, q_learning, networks, dqn, schedules (ε)
  memory/           replay_buffer
  checkpoints/      save / load / best / latest / resume
  training/         config, runner, callbacks, guards, safety, pipeline
  database/         SQLite schema, migrations and data access
  evaluation/       evaluate (frozen policy), metrics, stats, ablation, plots
  reflection/       stats (facts), grounding, fallback template, llm_client (Ollama), reflect, feedback
  services/         service layer used by the CLI and the dashboard
  app/              Streamlit dashboard: main, pages/, components/, charts/, styles/
  cli.py
scripts/            make_tables.py
tests/              unit/, integration/, ui/
docs/               architecture, setup, usage, training, evaluation, experiments, troubleshooting
results/            generated tables
runs/               run folders and the database (git-ignored)
```

## Limitations and future work

**Limitations**
- Two small benchmark tasks; bounded single-task learning only.
- DQN is sensitive to hyper-parameters and random seeds; 5 seeds give wide intervals.
- The reflection layer explains learning; it does not cause it.

**Future work**
- Double DQN and prioritised experience replay
- Harder environments such as LunarLander
- Using reflection notes to propose hyper-parameter changes that are then tested automatically

---

## Team

| Member | Main contribution |
| --- | --- |
| Brahma | Agent core: Q-learning, DQN, tuning, failure analysis |
| Atharv | Environment layer, training runner and CLI, CI, release |
| Vedant | Experience memory, evaluation harness, statistics, ablations |
| Somesh | Reflection layer, grounding validator, dashboard, demo |

---

## Acknowledgements

- [Gymnasium](https://gymnasium.farama.org/) for the environments
- Sutton & Barto, *Reinforcement Learning: An Introduction* (2nd ed.)
- Mnih et al., "Human-level control through deep reinforcement learning," *Nature*, 2015

## License

Apache-2.0 license
