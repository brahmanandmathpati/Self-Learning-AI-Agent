# Architecture

## Layers

| Layer | Package | Responsibility |
|---|---|---|
| Frontend | `sla.app` | Streamlit pages (`pages/`), reusable components (`components/`), Plotly figures (`charts/`), design tokens and CSS (`styles/`). No business logic. |
| Application | `sla.services`, `sla.cli` | `TrainingService`, `EvaluationService`, `ExperimentService`, `ReflectionService`, `CheckpointService`; the CLI and the dashboard both call these. |
| Pipeline | `sla.training.pipeline`, `sla.evaluation.ablation` | `train_run`, `resume_run`, `run_baseline`, `run_experiment`, `run_ablation`: the only way results are produced. |
| RL engine | `sla.training.runner`, `sla.agents`, `sla.memory`, `sla.envs` | The episode loop, the agents (random, Q-learning, DQN), the replay buffer and the seeded environments. |
| Persistence | `sla.database`, `sla.checkpoints` | SQLite experiment database; checkpoints on disk (paths stored in SQLite). |
| Evaluation | `sla.evaluation` | Frozen-policy evaluation, metrics, Welch's t-test, bootstrap CIs, static plots. |
| Reflection | `sla.reflection` | Grounded facts, deterministic template, optional Ollama client, number validation, ratings. |

## The training loop and callbacks

`run_training()` is the only place an agent learns. For every step it calls `agent.act(state, explore=True)`, `env.step(action)` and `agent.update(transition)`. Everything else plugs in as a callback (in this order, built by `pipeline.default_callbacks`):

1. `DatabaseCallback` – registers the run (seed, config, git SHA, run folder), logs every episode, records the final status.
2. `InitialEvalCallback` – evaluates the untrained policy on the test seeds ("before learning").
3. `TransitionValidationCallback` – rejects NaN/inf states, illegal actions and out-of-range rewards.
4. `CheckpointCallback` – saves `checkpoints/ep_XXXXXX` every `checkpoint_every` episodes, keeps the last 3, updates `latest.json`.
5. `PeriodicEvalCallback` – every `eval_every` episodes evaluates the frozen policy on validation seeds and saves `checkpoints/best`.
6. `RegressionMonitor` – flags sustained drops in validation score (training continues; the best checkpoint is kept).
7. `DivergenceGuard` – stops training if Q-values or the loss become NaN/inf or explode.
8. `ProgressCallback` (dashboard only) – live metrics; a stop request ends the run as `stopped`.

After training, `final_evaluation()` loads the **best** checkpoint (chosen on validation seeds) and evaluates it on the **test** seeds; only these numbers are reported.

## Agents

| Agent | File | Key points |
|---|---|---|
| Random | `agents/random_agent.py` | Seeded uniform actions; the "no learning" baseline. |
| Q-learning | `agents/q_learning.py` | `q_learning_update()` implements the Bellman update; terminal steps do not bootstrap; random tie-breaking. |
| DQN | `agents/dqn.py`, `agents/networks.py` | MLP Q-network, target network (`target_update_every`), replay buffer, Huber loss, Adam/AdamW, gradient clipping, ε-greedy (`agents/schedules.py`), ablation flags `replay_enabled` / `target_net_enabled`. |

## Database schema (SQLite, `database/store.py`)

Versioned with `PRAGMA user_version`; `Database.migrate()` applies newer entries of `MIGRATIONS` on open. WAL mode lets the dashboard read while a run is writing.

| Table | Contents |
|---|---|
| `experiments` | multi-seed / ablation groups: kind, env, algorithm, config, seeds, status, summary statistics (JSON), git SHA |
| `runs` | run_id, experiment, env, algorithm, seed, variant, config, run folder, git SHA, status, stop reason, episodes, latest/best checkpoint paths, start/end time, error |
| `episodes` | per-episode reward, length, ε, mean loss, end reason, wall time |
| `metrics` | named run-level metrics (test scores, divergence stops, regression flags) |
| `evaluations` | `initial` / `validation` / `test` evaluations: mean, std, median, success rate, mean length, seed base, checkpoint, all returns |
| `ablation_results` | variant × seed test scores linked to runs |
| `reflections`, `feedback` | notes with their facts and grounding report; user ratings |

Model weights and replay buffers stay on disk; SQLite stores their paths.

## Dashboard design system

Dark surface `#1a1a19` on a `#0d0d0d` page; ink `#ffffff` / `#c3c2b7` / muted `#898781`. Categorical slots in fixed order (validated for colour-vision deficiency on the dark surface): blue `#3987e5`, orange `#d95926`, aqua `#199e70`; the random baseline is always neutral grey. Status colours (good/warning/serious/critical) always come with an icon and label. Charts use a single y-axis, thin lines, a recessive grid and hover tooltips.

## Folder and module mapping to the project handbook

The handbook used `agent/`, `learning/`, `pipeline.py` and `ui/`; the repository uses the layout from the original scaffold: `agents/` (all agents, networks and ε schedule), `training/` (runner, callbacks, guards, pipeline, config), `checkpoints/`, `database/` (replaces `memory/episode_store.py`), `services/` and `app/` (replaces `ui/`).
