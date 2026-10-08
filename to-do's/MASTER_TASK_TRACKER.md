# MASTER TASK TRACKER — Self-Learning AI Agent (10 weeks)

Generated from the ten weekly handbook files: task IDs, titles, owners, priorities, hours and dependencies match Section 4 of each week. Tick **Status** only when the task's *Acceptance* item (Section 4, item 15) is met and its PR is merged. Fill the PR column with the real PR number from GitHub.

**Task ID format:** `SLA-<week>-<member>-<n>` · BM = Brahmanand Mathpati · AG = Atharv Gundale · VB = Vedant Biradar · SB = Somesh Badwane · Priority P1 = must have, P2 = should have, P3 = nice to have.

## Hours per member per week (planned)

| Week | Title | BM | AG | VB | SB |
|---|---|---|---|---|---|
| 1 | Project Discovery and Requirements | 11 | 11 | 11 | 11 |
| 2 | Research and System Architecture | 11 | 11 | 11 | 11 |
| 3 | Python Project Foundation | 11 | 11 | 11 | 11 |
| 4 | Core AI Agent Development | 11 | 11 | 11 | 11 |
| 5 | Memory and State Management | 11 | 11 | 11 | 11 |
| 6 | Self-Learning and Reward Mechanism | 11 | 11 | 11 | 11 |
| 7 | UI and Full System Integration | 11 | 11 | 11 | 11 |
| 8 | Testing and Performance Improvement | 11 | 11 | 11 | 11 |
| 9 | Documentation and Release Candidate | 11 | 11 | 11 | 11 |
| 10 | Final Validation and Project Demonstration | 11 | 11 | 11 | 11 |
| **Total** | | **110** | **110** | **110** | **110** |

## Week 01 — Project Discovery and Requirements

| Task ID | Task | Owner | Priority | Hours | Dependencies | PR | Status |
|---|---|---|---|---|---|---|---|
| SLA-01-BM-1 | Requirements document and MVP scope | Brahmanand Mathpati | P1 | 6 | Notion page; Day-1 kick-off | # | [ ] |
| SLA-01-BM-2 | Hand-computed Q-learning example | Brahmanand Mathpati | P2 | 5 | none | # | [ ] |
| SLA-01-AG-1 | Repository, branch protection, labels, board and PR template | Atharv Gundale | P1 | 5 | GitHub usernames from all members | # | [ ] |
| SLA-01-AG-2 | Zero-cost feasibility note, Python assessment and learning plans | Atharv Gundale | P1 | 6 | SLA-01-AG-1 | # | [ ] |
| SLA-01-VB-1 | Use cases, non-functional requirements and evaluation questions | Vedant Biradar | P1 | 11 | REQ IDs from SLA-01-BM-1 (Day 3) | # | [ ] |
| SLA-01-SB-1 | Hardware audit script — your first Python program | Somesh Badwane | P1 | 11 | repository from SLA-01-AG-1 (Day 1); Python installed | # | [ ] |

## Week 02 — Research and System Architecture

| Task ID | Task | Owner | Priority | Hours | Dependencies | PR | Status |
|---|---|---|---|---|---|---|---|
| SLA-02-BM-1 | Agent, runner and CLI interface design | Brahmanand Mathpati | P1 | 6 | Week-1 requirements | # | [ ] |
| SLA-02-BM-2 | Synopsis draft — Introduction, Problem Statement, Existing and Proposed System | Brahmanand Mathpati | P2 | 5 | `docs/synopsis_outline.md` (Week 1) | # | [ ] |
| SLA-02-AG-1 | Architecture diagrams and technology-stack freeze | Atharv Gundale | P1 | 5 | Week-1 feasibility note | # | [ ] |
| SLA-02-AG-2 | DQN design choices and local-LLM benchmark | Atharv Gundale | P1 | 6 | `docs/hardware_audit.md` (weakest laptop) | # | [ ] |
| SLA-02-VB-1 | Literature review (8–10 genuine sources) | Vedant Biradar | P1 | 5 | none | # | [ ] |
| SLA-02-VB-2 | Memory schema, replay-buffer interface and evaluation rules | Vedant Biradar | P1 | 6 | Day-2 interface meeting | # | [ ] |
| SLA-02-SB-1 | JSON and file helpers with your first unit tests | Somesh Badwane | P2 | 11 | Week-1 repository; Day-1 virtual environment | # | [ ] |

## Week 03 — Python Project Foundation

| Task ID | Task | Owner | Priority | Hours | Dependencies | PR | Status |
|---|---|---|---|---|---|---|---|
| SLA-03-BM-1 | Seeding, environment factory, Agent interface, random agent, CLI skeleton | Brahmanand Mathpati | P1 | 11 | SLA-03-AG-1 (package), SLA-03-VB-1 (`EnvError`) | # | [ ] |
| SLA-03-AG-1 | Package skeleton, `pyproject.toml`, CI and coding standards | Atharv Gundale | P1 | 11 | `docs/tech_stack.md` | # | [ ] |
| SLA-03-VB-1 | Shared error classes and logging | Vedant Biradar | P1 | 11 | SLA-03-AG-1 | # | [ ] |
| SLA-03-SB-1 | YAML configuration loader with validation (your first class) | Somesh Badwane | P1 | 11 | SLA-03-AG-1 (install), SLA-03-VB-1 (`ConfigError`) | # | [ ] |

## Week 04 — Core AI Agent Development

| Task ID | Task | Owner | Priority | Hours | Dependencies | PR | Status |
|---|---|---|---|---|---|---|---|
| SLA-04-BM-1 | Training loop (runner) with safety limits and callbacks | Brahmanand Mathpati | P1 | 6 | Week-3 modules; `summary.py` (Somesh, Day 3); `schedules.py` (Atharv, Day 2) | # | [ ] |
| SLA-04-BM-2 | Tabular Q-learning agent and FrozenLake check | Brahmanand Mathpati | P1 | 5 | `schedules.py` (Atharv, Day 2); Week-1 worked example | # | [ ] |
| SLA-04-AG-1 | Exploration schedule, Q-network and DQN agent (unit-level) | Atharv Gundale | P1 | 9 | `agent/base.py` (W3); `replay_buffer.py` (Vedant, Day 3) | # | [ ] |
| SLA-04-AG-2 | DQN maths session and `docs/notes/dqn_explained.md` | Atharv Gundale | P2 | 2 | SLA-04-AG-1 | # | [ ] |
| SLA-04-VB-1 | Replay buffer | Vedant Biradar | P1 | 11 | design §G | # | [ ] |
| SLA-04-SB-1 | Run-request validation and episode-summary printer | Somesh Badwane | P2 | 11 | `config.py` (your Week 3), `errors.py` (Vedant, Week 3) | # | [ ] |

## Week 05 — Memory and State Management

| Task ID | Task | Owner | Priority | Hours | Dependencies | PR | Status |
|---|---|---|---|---|---|---|---|
| SLA-05-BM-1 | Checkpoints and exact resume | Brahmanand Mathpati | P1 | 6 | Week-4 runner; agents' `save/load`; Vedant's `ReplayBuffer.save/load_from` | # | [ ] |
| SLA-05-BM-2 | Command-line interface: `sla train`, `sla resume`, `sla prune` | Brahmanand Mathpati | P1 | 5 | SLA-05-BM-1; Vedant's store (#53) and retention (#54) | # | [ ] |
| SLA-05-AG-1 | CartPole DQN pilot runs, smoke test and debug checklist | Atharv Gundale | P1 | 11 | Week-4 DQN; Brahmanand's `sla train` (#52, Day 4) | # | [ ] |
| SLA-05-VB-1 | SQLite episode store (long-term memory) | Vedant Biradar | P1 | 7 | `EpisodeInfo` field names (Week-4 runner); design §G | # | [ ] |
| SLA-05-VB-2 | Retention (pruning old runs) and data-handling document | Vedant Biradar | P2 | 4 | SLA-05-VB-1 | # | [ ] |
| SLA-05-SB-1 | Learning-curve plots from stored data | Somesh Badwane | P2 | 11 | your `rolling_mean` (Week 4); Vedant's store (#53) for the real-data demo | # | [ ] |

## Week 06 — Self-Learning and Reward Mechanism

| Task ID | Task | Owner | Priority | Hours | Dependencies | PR | Status |
|---|---|---|---|---|---|---|---|
| SLA-06-BM-1 | Train-and-evaluate pipeline, new `sla train`, `sla evaluate` | Brahmanand Mathpati | P1 | 7 | `evaluate.py` (#61), `guards.py` (#64), `TransitionValidationCallback` (#68) | # | [ ] |
| SLA-06-BM-2 | Baseline script (random agent and untrained DQN) | Brahmanand Mathpati | P1 | 4 | `evaluate.py` (#61) | # | [ ] |
| SLA-06-AG-1 | Divergence guard and regression monitor | Atharv Gundale | P1 | 5 | `PeriodicEvalCallback` writes `ctx.extra["eval_history"]` (#61) | # | [ ] |
| SLA-06-AG-2 | 5-seed training runs and DQN configuration tuning | Atharv Gundale | P1 | 6 | new `sla train` (#66, Day 4) | # | [ ] |
| SLA-06-VB-1 | Frozen-policy evaluator, best checkpoint and evaluation protocol | Vedant Biradar | P1 | 8 | Week-5 checkpoints and store | # | [ ] |
| SLA-06-VB-2 | Learning metrics | Vedant Biradar | P2 | 3 | none | # | [ ] |
| SLA-06-SB-1 | Transition validation (reward and state checks during training) | Somesh Badwane | P1 | 6 | your Week-4 `validation.py`; Week-4 runner `Callback.on_step` | # | [ ] |
| SLA-06-SB-2 | Feedback storage helper (ratings for explanation notes) | Somesh Badwane | P2 | 5 | Vedant's store (`add_feedback`, `get_reflection`, `query_feedback` — Week 5) | # | [ ] |

## Week 07 — UI and Full System Integration

| Task ID | Task | Owner | Priority | Hours | Dependencies | PR | Status |
|---|---|---|---|---|---|---|---|
| SLA-07-BM-1 | Full pipeline and CLI `pipeline / reflect / dashboard` | Brahmanand Mathpati | P1 | 7 | `reflect()` (#76), `plots.py` (W5), `train_and_evaluate` (W6) | # | [ ] |
| SLA-07-BM-2 | Integration captain: fresh-clone system test, bug triage and README update | Brahmanand Mathpati | P1 | 4 | SLA-07-BM-1; all Week-7 PRs merged | # | [ ] |
| SLA-07-AG-1 | Statistics: Welch t-test and bootstrap confidence intervals | Atharv Gundale | P1 | 4 | SciPy (already a dependency) | # | [ ] |
| SLA-07-AG-2 | Ablation study code and pilot; Streamlit mentoring | Atharv Gundale | P1 | 7 | SLA-07-AG-1; `train_and_evaluate` (W6); DQN flags `replay_enabled`, `target_net_enabled` (W4) | # | [ ] |
| SLA-07-VB-1 | Grounded reflection (facts, grounding check, template, optional local LLM) | Vedant Biradar | P1 | 11 | store `reflections` and `evals` tables (W5/W6) | # | [ ] |
| SLA-07-SB-1 | Streamlit app shell: shared settings and home page | Somesh Badwane | P1 | 4 | store (W5); Streamlit lesson (Section 5.4) | # | [ ] |
| SLA-07-SB-2 | Train, Results and Reflection pages + UI tests | Somesh Badwane | P1 | 7 | SLA-07-SB-1; `run_pipeline` (#71, Day 4); your Week-4 validators; your Week-6 `feedback.py`; your Week-5 plots | # | [ ] |

## Week 08 — Testing and Performance Improvement

| Task ID | Task | Owner | Priority | Hours | Dependencies | PR | Status |
|---|---|---|---|---|---|---|---|
| SLA-08-BM-1 | Failure analysis of the trained agents | Brahmanand Mathpati | P1 | 5 | final experiment checkpoints (Day 2–4); `envs.end_reason` (W3) | # | [ ] |
| SLA-08-BM-2 | Persistence test — learning survives a restart | Brahmanand Mathpati | P1 | 6 | checkpoints (W5), evaluator (W6) | # | [ ] |
| SLA-08-AG-1 | Final experiments with manifest, and generated results table | Atharv Gundale | P1 | 6 | `run_pipeline` (W7), `stats.bootstrap_ci`/`compare_groups` (W7), baseline CSV (W6) | # | [ ] |
| SLA-08-AG-2 | Full 5-seed ablation and its interpretation | Atharv Gundale | P1 | 5 | ablation code (W7); code freeze | # | [ ] |
| SLA-08-VB-1 | Performance measurement | Vedant Biradar | P1 | 4 | `hardware_check.py` (W1, Somesh); runner | # | [ ] |
| SLA-08-VB-2 | Test report with coverage | Vedant Biradar | P1 | 4 | all tests merged | # | [ ] |
| SLA-08-VB-3 | Reflection evaluation (with Somesh) | Vedant Biradar | P2 | 3 | final runs; reflection (W7); feedback (W6) | # | [ ] |
| SLA-08-SB-1 | UI hardening: new UI tests and three bug fixes | Somesh Badwane | P1 | 9 | your Week-7 pages; Week-7 `bug` issues | # | [ ] |
| SLA-08-SB-2 | Blind rating of reflection notes | Somesh Badwane | P3 | 2 | SLA-08-VB-3 | # | [ ] |

## Week 09 — Documentation and Release Candidate

| Task ID | Task | Owner | Priority | Hours | Dependencies | PR | Status |
|---|---|---|---|---|---|---|---|
| SLA-09-BM-1 | Final README and agent module documentation | Brahmanand Mathpati | P1 | 4 | all features merged; results files | # | [ ] |
| SLA-09-BM-2 | Report outline and chapters 1–3 | Brahmanand Mathpati | P1 | 7 | Week-1/2 documents | # | [ ] |
| SLA-09-AG-1 | Release candidate `v0.9-rc`, CHANGELOG and clean-install offline test | Atharv Gundale | P1 | 5 | README final (#91) | # | [ ] |
| SLA-09-AG-2 | Licences and learning module documentation | Atharv Gundale | P2 | 2 | `pyproject.toml` | # | [ ] |
| SLA-09-AG-3 | Report chapter 4 — design and implementation | Atharv Gundale | P1 | 4 | module docs (#92) | # | [ ] |
| SLA-09-VB-1 | Report chapters 5–6 and final figures | Vedant Biradar | P1 | 8 | `results/` (W8) | # | [ ] |
| SLA-09-VB-2 | Memory, evaluation and reflection module documentation | Vedant Biradar | P2 | 3 | none | # | [ ] |
| SLA-09-SB-1 | User guide, UI module doc and screenshots | Somesh Badwane | P1 | 5 | README final (#91) | # | [ ] |
| SLA-09-SB-2 | Contribution record from real Git/GitHub data | Somesh Badwane | P2 | 2 | none | # | [ ] |
| SLA-09-SB-3 | Slide deck draft | Somesh Badwane | P2 | 4 | figures from Vedant; screenshots | # | [ ] |

## Week 10 — Final Validation and Project Demonstration

| Task ID | Task | Owner | Priority | Hours | Dependencies | PR | Status |
|---|---|---|---|---|---|---|---|
| SLA-10-BM-1 | Final regression check | Brahmanand Mathpati | P1 | 5 | final run folders (Week 8) on the laptop(s) that produced them; `results/manifest.csv` | # | [ ] |
| SLA-10-BM-2 | Demo script and rehearsals | Brahmanand Mathpati | P1 | 6 | `v1.0` | # | [ ] |
| SLA-10-AG-1 | Final code review and `v1.0` release | Atharv Gundale | P1 | 6 | regression check (#102); export merged (#101) | # | [ ] |
| SLA-10-AG-2 | Viva question bank and two mock vivas | Atharv Gundale | P1 | 5 | final report draft | # | [ ] |
| SLA-10-VB-1 | Final report | Vedant Biradar | P1 | 8 | chapters from Week 9; regression check | # | [ ] |
| SLA-10-VB-2 | Evidence pack | Vedant Biradar | P2 | 3 | results, CI, releases | # | [ ] |
| SLA-10-SB-1 | Independent enhancement: CSV export of results | Somesh Badwane | P2 | 5 | your Results page (W7); your `safe_run_name` (W4) | # | [ ] |
| SLA-10-SB-2 | Demo video and final slides | Somesh Badwane | P1 | 4 | demo script (Brahmanand); slide draft (W9) | # | [ ] |
| SLA-10-SB-3 | Final contribution record | Somesh Badwane | P2 | 2 | `v1.0` | # | [ ] |

## How to update this tracker

1. When you start a task, create/assign its GitHub issue and write the issue number next to the task in the PR column.
2. When the PR is merged and the acceptance item is met, change `[ ]` to `[x]` in a small `docs/` PR (or tick it in the GitHub project board and copy weekly).
3. Never tick a task whose tests are failing or whose results were not produced by the project's scripts.
