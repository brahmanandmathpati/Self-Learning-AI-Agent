# Self-Learning AI Agent

> A self-learning RL agent: a from-scratch Deep Q-Network with experience replay that learns CartPole by trial and error, with multi-seed evaluation and an LLM that explains what it learned.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-CPU-orange)
![Gymnasium](https://img.shields.io/badge/Gymnasium-CartPole--v1-green)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-lightgrey)

Final-year B.Tech CSE (AI Specialization) project, 2023–2027.

---

## What this project is

Most student "AI agents" are static: they prompt an LLM with fixed instructions and behave the same on day 1 and day 100. This agent is different. It **starts with zero knowledge of its task, learns by trial and error, and gets measurably better with experience.**

- **Learning happens in the weights.** A Deep Q-Network (written by us in PyTorch, not imported from a library) updates its weights from a reward signal.
- **It remembers its past attempts.** A replay buffer stores every transition, and the agent samples from it to learn from past steps again.
- **Improvement is proven, not claimed.** A frozen copy of the trained policy is evaluated across 5 random seeds and compared with a random-action baseline.
- **It explains itself.** An LLM layer (local, via Ollama) turns computed training statistics into a plain-language note. A validator rejects any note containing a number the logs don't support.

**Scope.** "Self-learning" here means learning one bounded task through repeated interaction. It is not general-purpose or continual multi-task learning.

---

## Results

> ⚠️ This table is filled only from real training runs. Every number links to a run folder listed in `results/manifest.csv`.

| Agent | Environment | Frozen-policy mean return (± std, 5 seeds) | Episodes to reach 195 |
| --- | --- | --- | --- |
| Random baseline | CartPole-v1 | _TBD_ | — |
| DQN (ours) | CartPole-v1 | _TBD_ | _TBD_ |
| DQN without replay (ablation) | CartPole-v1 | _TBD_ | _TBD_ |
| Tabular Q-learning (ours) | FrozenLake-v1 4×4 | _TBD_ (success rate) | — |

<!-- Add after Week 5: results/figures/learning_curve.png and demo/before_after.gif -->

---

## Architecture

```
┌──────────── Training runner (M4): config, seeds, checkpoints ────────────┐
│                                                                          │
│   Environment (M1)  ⇄   RL agent core (M2)   ⇄   Replay buffer (M3)      │
│   state, reward         ε-greedy action,         stores transitions,     │
│                         TD update of weights     samples mini-batches    │
└──────────────┬──────────────────────┬────────────────────────────────────┘
               │ episode rows         │ checkpoints
               ▼                      ▼
     Episode store (M3) ──►  Evaluation (M5) ──►  Reflection (M6) ──►  Dashboard (M6)
     SQLite log              frozen policy,        stats → LLM note,     curves, notes,
                             5 seeds vs baseline   numbers fact-checked  GIFs (Streamlit)
```

Only the top loop changes the agent's behaviour. The bottom row measures and explains learning; it never trains the agent.

| Module | Path | Responsibility |
| --- | --- | --- |
| M1 Environment layer | `src/sla/envs/` | Seeded Gymnasium environments, wrappers, rendering |
| M2 Agent core | `src/sla/agents/` | Random baseline, tabular Q-learning, DQN |
| M3 Experience memory | `src/sla/memory/` | Replay buffer; persistent SQLite episode log |
| M4 Training runner | `src/sla/training/`, `src/sla/cli.py` | Episode loop, configs, seeding, checkpoints, CLI |
| M5 Evaluation harness | `src/sla/evaluation/` | Frozen-policy evaluation, metrics, statistics, plots |
| M6 Reflection + dashboard | `src/sla/reflection/`, `src/sla/app/` | Grounded LLM notes; Streamlit UI; GIFs |

---

## Getting started

### Requirements

- Python 3.10 or newer
- A laptop CPU is enough; no GPU needed
- Optional: [Ollama](https://ollama.com) with a small model (e.g. `llama3.2:3b`) for the reflection layer

### Install

```bash
git clone https://github.com/<your-org>/self-learning-agent.git
cd self-learning-agent
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env             # only needed if you change defaults
```

Optional, for the reflection layer:

```bash
ollama pull llama3.2:3b
```

### Quickstart

Train, evaluate, write a reflection note and make plots in one command:

```bash
sla pipeline --config configs/cartpole_dqn.yaml --seeds 0 1 2 3 4
sla dashboard                     # opens the Streamlit dashboard
```

### Individual commands

| Command | What it does |
| --- | --- |
| `sla train --config configs/cartpole_dqn.yaml --seed 0` | Train one run; creates a folder in `runs/` |
| `sla train --resume runs/<run_dir>` | Resume a run from its latest checkpoint |
| `sla evaluate --run runs/<run_dir> --episodes 100` | Evaluate the frozen policy (ε = 0) |
| `sla reflect --run runs/<run_dir>` | Generate and fact-check a learning summary |
| `sla dashboard` | Launch the dashboard |
| `python scripts/run_baseline.py` | Random-agent baseline, 5 seeds |
| `python scripts/run_ablation.py` | Full DQN vs. no replay vs. no target network |
| `python scripts/make_tables.py` | Regenerate all results tables from run folders |

Each run folder holds a copy of its config, the git commit SHA, the SQLite episode log, checkpoints and `run.log`.

---

## How the agent learns

**Q-learning update** (tabular, FrozenLake):

```
Q(s, a) ← Q(s, a) + α [ r + γ · max_a' Q(s', a') − Q(s, a) ]
```

**DQN update** (CartPole):

```
batch  = replay_buffer.sample(B)                      # s, a, r, s', terminated
q      = online_net(s)[a]
target = r + γ · (1 − terminated) · max_a' target_net(s')[a']
loss   = Huber(q, target)
gradient step on online_net (grad-norm clip 10)
every C steps: target_net ← online_net
```

Truncation (hitting the 500-step time limit) is **not** treated as terminal, so the target still bootstraps.

| Hyper-parameter | Starting value |
| --- | --- |
| Learning rate (Adam) | 1e-3 |
| Discount γ | 0.99 |
| Batch size | 64 |
| Replay buffer size | 50,000 |
| Learning starts | 1,000 steps |
| Target network sync | every 500 steps |
| ε schedule | 1.0 → 0.05 over 10,000 steps |

Final tuned values are in `configs/cartpole_dqn.yaml`.

---

## How we prove it learns

We claim the agent learns only if all of the following hold:

1. **Learning curve:** training return rises across 5 seeds.
2. **Frozen-policy evaluation:** with ε = 0 and no updates, the trained policy beats the random baseline (Welch's t-test, n = 5 seeds).
3. **Before/after:** the last 5% of episodes score higher than the first 5%, with a bootstrap 95% confidence interval that excludes zero.
4. **Persistence:** the checkpoint, reloaded in a new process, keeps its score.
5. **Held-out seeds:** evaluation seeds are never used in training.
6. **Ablation:** we report what happens when the replay buffer or target network is removed.

What does **not** count as learning: better-worded LLM notes, stored history the policy never uses, or prompt changes between runs.

---

## Reflection layer

1. `stats.py` computes facts from the episode log (window means, failure causes, ε).
2. The LLM receives only those facts and writes a note.
3. `grounding.py` extracts every number in the note and rejects it if any number is not within ±1% of a fact.
4. The dashboard shows both accepted and rejected notes.

If Ollama is not running, a template note is generated from the facts instead, so the pipeline never crashes.

---

## Running tests

```bash
pytest                    # unit + integration tests
pytest -m smoke           # 2,000-step DQN smoke run
ruff check .              # lint
```

CI runs lint, tests and the smoke run on every pull request. The LLM is mocked in CI, so no API key or network is needed.

---

## Project structure

```
self-learning-agent/
├── configs/          experiment configs (YAML)
├── src/sla/
│   ├── envs/         factory.py, wrappers.py
│   ├── agents/       base.py, random_agent.py, q_learning.py, networks.py, dqn.py
│   ├── memory/       replay_buffer.py, episode_store.py
│   ├── training/     runner.py, config.py, checkpoint.py, seeding.py
│   ├── evaluation/   evaluate.py, metrics.py, stats.py, plots.py
│   ├── reflection/   stats.py, prompts.py, llm_client.py, grounding.py
│   ├── app/          dashboard.py, record.py
│   └── cli.py
├── scripts/          baseline, ablation and table scripts
├── tests/            mirrors src/sla/
├── docs/             requirements, design, related work, notes
├── results/          tables, figures, manifest.csv
└── runs/             raw run folders (git-ignored)
```

---

## Reproducibility

- All randomness (Python, NumPy, PyTorch, environment) is seeded from the config.
- Evaluation runs use deterministic PyTorch settings.
- Every reported number appears in `results/manifest.csv` with its run folder and git SHA.
- Results tables and figures are generated by scripts, never typed by hand.

---

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `box2d` fails to install on Windows | Only needed for LunarLander (optional). Use WSL or Colab. |
| `sla reflect` warns "Ollama offline" | Start Ollama (`ollama serve`) or accept the template note. |
| Results differ slightly between machines | Expected across hardware; compare means over 5 seeds. |
| Dashboard shows no runs | Check that `runs/` contains at least one finished run folder. |

---

## Limitations and future work

**Limitations**
- One simple environment (CartPole); bounded single-task learning only.
- DQN is sensitive to hyper-parameters and random seeds.
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

See `CONTRIBUTING.md` for the branch, commit and pull-request workflow.

---

## Acknowledgements

- [Gymnasium](https://gymnasium.farama.org/) for the environments
- Sutton & Barto, *Reinforcement Learning: An Introduction* (2nd ed.)
- Mnih et al., "Human-level control through deep reinforcement learning," *Nature*, 2015

## License

_Choose a license (e.g. MIT) and add a `LICENSE` file._
