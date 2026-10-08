# PROJECT PROGRESS TRACKER — Self-Learning AI Agent

One page to see where the project stands. Update it at every **Day-7 weekly review** (Atharv owns the file; each owner ticks their own deliverables). Objectives, Definitions of Done and deliverables are copied from Section 1 and Section 11 of each weekly handbook.

**Status values:** Not started · In progress · Done · Blocked (write the blocker in Section 4).

## 1. Overview

| Week | Title | Handbook file | Milestone tag | Status | Deliverables done | Review date |
|---|---|---|---|---|---|---|
| 1 | Project Discovery and Requirements | `WEEK_01_Project_Discovery_and_Requirements.md` | — | Not started | 0 / 9 | |
| 2 | Research and System Architecture | `WEEK_02_Research_and_System_Architecture.md` | `w2-design-freeze` | Not started | 0 / 8 | |
| 3 | Python Project Foundation | `WEEK_03_Python_Project_Foundation.md` | — | Not started | 0 / 8 | |
| 4 | Core AI Agent Development | `WEEK_04_Core_AI_Agent_Development.md` | — | Not started | 0 / 9 | |
| 5 | Memory and State Management | `WEEK_05_Memory_and_State_Management.md` | — | Not started | 0 / 8 | |
| 6 | Self-Learning and Reward Mechanism | `WEEK_06_Self_Learning_and_Reward_Mechanism.md` | — | Not started | 0 / 9 | |
| 7 | UI and Full System Integration | `WEEK_07_UI_and_Full_System_Integration.md` | — | Not started | 0 / 8 | |
| 8 | Testing and Performance Improvement | `WEEK_08_Testing_and_Performance_Improvement.md` | `v0.8-experiments` | Not started | 0 / 10 | |
| 9 | Documentation and Release Candidate | `WEEK_09_Documentation_and_Release_Candidate.md` | `v0.9-rc` | Not started | 0 / 12 | |
| 10 | Final Validation and Project Demonstration | `WEEK_10_Final_Validation_and_Project_Demonstration.md` | `v1.0` | Not started | 0 / 9 | |

## 2. Week by week

### Week 01 — Project Discovery and Requirements

**Objective:** Agree exactly what we will build, check every laptop, install the tools and set up a GitHub workflow everyone can use.

**Definition of Done:** (1) `docs/requirements.md` merged, every requirement has a verification method; (2) all 4 members merged one PR; (3) `docs/hardware_audit.md` lists 4 laptops; (4) `main` is protected (no direct pushes); (5) Week-1 review meeting held and notes saved.

| Deliverable | Owner | File/Location | Done |
|---|---|---|---|
| Requirements + MVP scope | Brahmanand | `docs/requirements.md` | [ ] |
| Synopsis outline | Brahmanand | `docs/synopsis_outline.md` | [ ] |
| Q-learning worked example | Brahmanand | `docs/notes/q_learning_by_hand.md` | [ ] |
| Repo, protection, labels, board, PR template | Atharv | GitHub + `.github/`, `.gitignore`, `.env.example` | [ ] |
| Feasibility + learning plans | Atharv | `docs/feasibility.md`, `docs/learning_plans.md` | [ ] |
| Use cases + NFRs | Vedant | `docs/use_cases.md`, `docs/nfr.md` | [ ] |
| Hardware audit script | Somesh | `scripts/hardware_check.py` | [ ] |
| Hardware audit table | Somesh | `docs/hardware_audit.md` | [ ] |
| Week-1 meeting notes | Atharv | `docs/meetings/week01.md` | [ ] |

- [ ] All tests pass in CI on `main` at the end of the week
- [ ] Weekly demo done from a fresh `git pull`
- [ ] Section 13 completion checklist of the handbook ticked

Review notes (what went well / what to change / blockers carried over):

> 

### Week 02 — Research and System Architecture

**Objective:** Learn the RL theory we need, choose the smallest Python stack, and **freeze the architecture and module interfaces** so four people can code in parallel from Week 3.

**Definition of Done:** `docs/design.md` merged and **signed off by all four** (interfaces frozen); `docs/architecture.md` + `docs/tech_stack.md` merged; LLM decision recorded with numbers; `docs/literature_review.md` merged; synopsis draft sections exist; `tests/unit/test_io_helpers.py` passes.

| Deliverable | Owner | File/Location | Done |
|---|---|---|---|
| Frozen interfaces | Brahmanand (+ all) | `docs/design.md` | [ ] |
| Synopsis draft sections 1–4 | Brahmanand | `docs/synopsis_draft.md` | [ ] |
| Architecture diagrams | Atharv | `docs/architecture.md` | [ ] |
| Tech stack + LLM decision | Atharv | `docs/tech_stack.md` | [ ] |
| LLM benchmark spike | Atharv | `spikes/llm_benchmark.py` | [ ] |
| Literature review | Vedant | `docs/literature_review.md` | [ ] |
| Memory/evaluation design | Vedant | `docs/design.md` §G | [ ] |
| JSON/folder helpers + tests | Somesh | `src/sla/utils/io_helpers.py`, `tests/unit/test_io_helpers.py` | [ ] |

- [ ] All tests pass in CI on `main` at the end of the week
- [ ] Weekly demo done from a fresh `git pull`
- [ ] Section 13 completion checklist of the handbook ticked

Review notes (what went well / what to change / blockers carried over):

> 

### Week 03 — Python Project Foundation

**Objective:** Turn the design into a real, installable Python package that **every member can install, run and test**, with CI checking every pull request.

**Definition of Done:** CI green on `main`; branch protection requires the CI check; all four members show `pytest` passing locally (screenshot in their PR); `RandomAgent` runs 10 CartPole episodes through the `Agent` interface; invalid YAML raises `ConfigError` naming the key.

| Deliverable | Owner | File/Location | Done |
|---|---|---|---|
| Package + pyproject | Atharv | `pyproject.toml`, `src/sla/*/__init__.py` | [ ] |
| CI workflow + required check | Atharv | `.github/workflows/ci.yml` | [ ] |
| Contribution guide | Atharv + Vedant | `CONTRIBUTING.md` | [ ] |
| Errors + logging | Vedant | `utils/errors.py`, `utils/logging_setup.py` | [ ] |
| Seeding + env factory | Brahmanand | `utils/seeding.py`, `envs/factory.py` | [ ] |
| Agent interface + random agent | Brahmanand | `agent/base.py`, `agent/random_agent.py` | [ ] |
| CLI skeleton | Brahmanand | `src/sla/cli.py` | [ ] |
| Config loader + 4 configs | Somesh | `utils/config.py`, `configs/*.yaml` | [ ] |

- [ ] All tests pass in CI on `main` at the end of the week
- [ ] Weekly demo done from a fresh `git pull`
- [ ] Section 13 completion checklist of the handbook ticked

Review notes (what went well / what to change / blockers carried over):

> 

### Week 04 — Core AI Agent Development

**Objective:** Build the **training loop** and the **first agent that genuinely learns** (tabular Q-learning on FrozenLake), and write — and unit-test — the DQN, the replay buffer and the exploration schedule.

**Definition of Done:** All Week-4 tests pass in CI; `scripts/quick_frozenlake_check.py` shows Q-learning reaching the goal in its greedy episode for all 5 seeds on non-slippery FrozenLake (the **target** — record what you actually get); DQN unit tests pass (TD target, loss decreases, target frozen, save/load); runner stops at step and wall-clock limits.

| Deliverable | Owner | File/Location | Done |
|---|---|---|---|
| Safety limits | Brahmanand | `src/sla/agent/safety.py` | [ ] |
| Training loop + callbacks | Brahmanand | `src/sla/agent/runner.py`, `tests/conftest.py` | [ ] |
| Tabular Q-learning | Brahmanand | `src/sla/learning/q_learning.py` | [ ] |
| FrozenLake quick check | Brahmanand | `scripts/quick_frozenlake_check.py` | [ ] |
| Epsilon schedule | Atharv | `src/sla/learning/schedules.py` | [ ] |
| Q-network + DQN | Atharv | `src/sla/learning/networks.py`, `dqn.py` | [ ] |
| DQN notes + session | Atharv | `docs/notes/dqn_explained.md` | [ ] |
| Replay buffer | Vedant | `src/sla/memory/replay_buffer.py` | [ ] |
| Validation + summary | Somesh | `src/sla/utils/validation.py`, `summary.py` | [ ] |

- [ ] All tests pass in CI on `main` at the end of the week
- [ ] Weekly demo done from a fresh `git pull`
- [ ] Section 13 completion checklist of the handbook ticked

Review notes (what went well / what to change / blockers carried over):

> 

### Week 05 — Memory and State Management

**Objective:** Give the agent a **memory that survives**: every episode goes into a SQLite database (long-term memory), training can be **stopped and resumed exactly** from checkpoints, and the first **learning-curve plots** are drawn from stored data. First real DQN runs on CartPole (pilot).

**Definition of Done:** All Week-5 tests pass in CI; `test_resumed_run_matches_uninterrupted_run` passes (resume is exact); `test_retrieval_accuracy_1000_rows` passes; `sla train --config configs/frozenlake_q.yaml` creates a run folder with checkpoints and rows in `runs/episodes.db`; learning-curve PNG produced from the database; DQN pilot results recorded **as observed** (no invented numbers).

| Deliverable | Owner | File/Location | Done |
|---|---|---|---|
| Checkpoints + resume | Brahmanand | `src/sla/agent/checkpoint.py` | [ ] |
| CLI train/resume/prune | Brahmanand | `src/sla/cli.py` | [ ] |
| README command-line section | Brahmanand | `README.md` | [ ] |
| Episode store + callback | Vedant | `src/sla/memory/episode_store.py`, `tests/conftest.py` | [ ] |
| Retention + data doc | Vedant | `src/sla/memory/retention.py`, `docs/data_handling.md` | [ ] |
| Learning-curve plots | Somesh | `src/sla/evaluation/plots.py` | [ ] |
| DQN smoke test | Atharv | `tests/integration/test_dqn_smoke.py` | [ ] |
| Pilot runs + debug checklist | Atharv | `docs/notes/dqn_debug_checklist.md` | [ ] |

- [ ] All tests pass in CI on `main` at the end of the week
- [ ] Weekly demo done from a fresh `git pull`
- [ ] Section 13 completion checklist of the handbook ticked

Review notes (what went well / what to change / blockers carried over):

> 

### Week 06 — Self-Learning and Reward Mechanism

**Objective:** Make "self-learning" **measurable and safe**: a frozen-policy **evaluator** on held-out seeds, automatic **best-checkpoint** selection, **guards** that stop divergence and flag regressions, **validation** of every reward/transition, and the first honest **5-seed** results compared with a **random baseline**.

**Definition of Done:** All tests pass in CI including `test_eval_and_test_seeds_never_overlap_training_seeds`, `test_evaluation_does_not_change_q_table`, `test_corrupted_transition_stops_training`; `metrics.json` written for each run; baseline CSV produced; 5-seed result table (trained vs random vs untrained DQN) filled **only with numbers produced by the scripts**.

| Deliverable | Owner | File/Location | Done |
|---|---|---|---|
| Train-and-evaluate pipeline | Brahmanand | `src/sla/pipeline.py` | [ ] |
| CLI `train` (evaluates) + `evaluate` | Brahmanand | `src/sla/cli.py` | [ ] |
| Baselines | Brahmanand | `scripts/run_baseline.py`, `results/baseline/baseline.csv` | [ ] |
| Guards | Atharv | `src/sla/learning/guards.py` | [ ] |
| Five-seed results + config log | Atharv | `docs/notes/week6_results.md`, `configs/cartpole_dqn.yaml` | [ ] |
| Evaluator + protocol | Vedant | `src/sla/evaluation/evaluate.py`, `docs/evaluation_protocol.md` | [ ] |
| Metrics | Vedant | `src/sla/evaluation/metrics.py` | [ ] |
| Transition validation | Somesh | `src/sla/utils/validation.py` (W6) | [ ] |
| Note rating helper | Somesh | `src/sla/ui/feedback.py` | [ ] |

- [ ] All tests pass in CI on `main` at the end of the week
- [ ] Weekly demo done from a fresh `git pull`
- [ ] Section 13 completion checklist of the handbook ticked

Review notes (what went well / what to change / blockers carried over):

> 

### Week 07 — UI and Full System Integration

**Objective:** Join everything into **one working system**: a one-call pipeline (train → evaluate → plots → explanation note), a **Streamlit dashboard** (Train, Results, Reflection pages), **grounded reflection notes** (template by default, optional local LLM), and **statistics + ablation** to prove which DQN parts matter.

**Definition of Done:** All tests pass in CI (`test_cli.py`, `test_pipeline_e2e.py` W7, `test_reflection.py`, `test_stats.py`, `test_ablation.py`, `tests/ui/test_pages.py`); dashboard demo on 2 laptops; the project runs fully **with Ollama switched off**; ablation pilot numbers recorded as produced.

| Deliverable | Owner | File/Location | Done |
|---|---|---|---|
| Full pipeline | Brahmanand | `src/sla/pipeline.py` (W7) | [ ] |
| CLI pipeline/reflect/dashboard | Brahmanand | `src/sla/cli.py`, `tests/integration/test_cli.py` | [ ] |
| Statistics | Atharv | `src/sla/evaluation/stats.py` | [ ] |
| Ablation code + pilot | Atharv | `src/sla/evaluation/ablation.py`, `scripts/run_ablation.py` | [ ] |
| Grounded reflection | Vedant | `src/sla/reflection/*.py` | [ ] |
| Dashboard shell | Somesh | `src/sla/ui/common.py`, `app.py` | [ ] |
| Dashboard pages + tests | Somesh | `src/sla/ui/pages/*.py`, `tests/ui/test_pages.py` | [ ] |
| Fresh-clone integration test | All | GitHub issues labelled `bug` | [ ] |

- [ ] All tests pass in CI on `main` at the end of the week
- [ ] Weekly demo done from a fresh `git pull`
- [ ] Section 13 completion checklist of the handbook ticked

Review notes (what went well / what to change / blockers carried over):

> 

### Week 08 — Testing and Performance Improvement

**Objective:** Produce the **final, traceable results** and prove the system is **reliable**: freeze the code, run the final 5-seed experiments and the full ablation, generate every table from files (never by hand), analyse failures, measure speed/memory, prove learning survives a restart, and harden the UI.

**Definition of Done:** All tests pass in CI; coverage report attached to `results/test_report.md`; every number in `results/final_table.md` regenerates from `results/manifest.csv` by running `scripts/make_tables.py`; persistence test passes; performance measured on every member's laptop with hardware details; no fabricated or hand-edited numbers.

| Deliverable | Owner | File/Location | Done |
|---|---|---|---|
| Code-freeze tag | Atharv | tag `v0.8-experiments` | [ ] |
| Final experiments + manifest | Atharv | `scripts/run_final_experiments.py`, `results/manifest.csv` | [ ] |
| Generated results table | Atharv | `scripts/make_tables.py`, `results/final_table.md` | [ ] |
| Five-seed ablation | Atharv | `results/ablation/summary.csv`, `docs/notes/ablation_notes.md` | [ ] |
| Failure analysis | Brahmanand | `scripts/failure_analysis.py`, `results/failure_analysis.md` | [ ] |
| Persistence test | Brahmanand | `tests/integration/test_persistence.py` | [ ] |
| Performance | Vedant | `scripts/measure_performance.py`, `results/performance.md` | [ ] |
| Test report | Vedant | `results/test_report.md` | [ ] |
| Reflection evaluation | Vedant + Somesh | `results/reflection_eval.md` | [ ] |
| UI tests + fixes | Somesh | `tests/ui/test_pages.py`, `src/sla/ui/pages/*` | [ ] |

- [ ] All tests pass in CI on `main` at the end of the week
- [ ] Weekly demo done from a fresh `git pull`
- [ ] Section 13 completion checklist of the handbook ticked

Review notes (what went well / what to change / blockers carried over):

> 

### Week 09 — Documentation and Release Candidate

**Objective:** Turn the working system and its results into a **complete, examinable package**: final README, module documentation, user guide, licences, contribution record, report chapters 1–6, slide draft, and a **release candidate** (`v0.9-rc`) proven to install and run on a clean machine **without internet after installation** and without Ollama.

**Definition of Done:** `v0.9-rc` tagged on a commit where CI is green **and** the clean-install test passed; every number in the report chapters is copied from a file in `results/` (with the file named in the text or caption); every member's contribution record comes from real Git/GitHub data.

| Deliverable | Owner | File/Location | Done |
|---|---|---|---|
| Final README | Brahmanand | `README.md` | [ ] |
| Agent module doc | Brahmanand | `docs/modules/agent.md` | [ ] |
| Report outline + ch 1–3 | Brahmanand | `docs/report_outline.md`, `report/chapters_1-3.docx` | [ ] |
| Clean-install offline test | Atharv (+ Somesh) | `docs/clean_install_test.md` | [ ] |
| CHANGELOG + `v0.9-rc` | Atharv | `CHANGELOG.md`, tag, pre-release | [ ] |
| Licences + learning doc | Atharv | `docs/licences.md`, `docs/modules/learning.md` | [ ] |
| Report ch 4 | Atharv | `report/chapter_4.docx` | [ ] |
| Report ch 5–6 + figures | Vedant | `report/chapters_5-6.docx`, `report/figures/` | [ ] |
| Memory/eval/reflection doc | Vedant | `docs/modules/memory_evaluation_reflection.md` | [ ] |
| User guide + UI doc + screenshots | Somesh | `docs/user_guide.md`, `docs/modules/ui.md`, `docs/screenshots/` | [ ] |
| Contribution record | Somesh | `docs/contributions.md` | [ ] |
| Slide draft | Somesh | `slides/draft.pptx` | [ ] |

- [ ] All tests pass in CI on `main` at the end of the week
- [ ] Weekly demo done from a fresh `git pull`
- [ ] Section 13 completion checklist of the handbook ticked

Review notes (what went well / what to change / blockers carried over):

> 

### Week 10 — Final Validation and Project Demonstration

**Objective:** Validate the final system one last time (regression check against the Week-8 results), release **`v1.0`**, finish the report, slides, demo video and evidence pack, and prepare every member for the **viva** with mock sessions. Somesh adds one small independent enhancement (CSV export).

**Definition of Done:** CI green on `v1.0`; regression check "ALL MATCH" (or every mismatch explained and fixed); the full demo runs from a fresh clone of `v1.0` with Ollama off; every member has completed two mock vivas; final report numbers match `results/`.

| Deliverable | Owner | File/Location | Done |
|---|---|---|---|
| Regression check | Brahmanand | `scripts/regression_check.py`, `results/regression_check.md` | [ ] |
| Demo script | Brahmanand | `demo/demo_script.md` | [ ] |
| Final review + `v1.0` | Atharv | `CHANGELOG.md`, tag `v1.0`, GitHub Release | [ ] |
| Viva question bank + 2 mocks | Atharv (+ all) | `docs/viva_questions.md` | [ ] |
| Final report | Vedant | `report/final_report.docx` (+ PDF on release) | [ ] |
| Evidence pack | Vedant | `demo/evidence/` | [ ] |
| CSV export | Somesh | `src/sla/ui/export.py`, `2_Results.py` (W10), `tests/unit/test_export.py` | [ ] |
| Demo video + final slides | Somesh | `demo/demo_video_link.md`, `slides/final.pptx` | [ ] |
| Final contributions | Somesh | `docs/contributions.md` | [ ] |

- [ ] All tests pass in CI on `main` at the end of the week
- [ ] Weekly demo done from a fresh `git pull`
- [ ] Section 13 completion checklist of the handbook ticked

Review notes (what went well / what to change / blockers carried over):

> 

## 3. Key results log (copy only from files produced by the project's scripts)

| Date | What | Value (copied) | Source file | Commit | Recorded by |
|---|---|---|---|---|---|
| | e.g. FrozenLake Q-learning, mean test return over 5 seeds | | `results/final_table.md` | | |

Pilot numbers (Weeks 4–7) are written as **pilot** and never reused as final results.

## 4. Blockers and risks

| # | Date | Blocker / risk | Impact | Owner | Action | Status |
|---|---|---|---|---|---|---|
| R1 | W1 | DQN may learn slowly on CPU-only laptops | final runs take long | Atharv | split seeds across laptops, run overnight | open |
| R2 | W1 | PyTorch install problems on a laptop | DQN tests skipped locally | Atharv | CPU wheel; CI always runs them | open |
| R3 | W1 | Beginner ramp-up (Somesh) | slower early tasks | Atharv | lessons + pairing; tasks grow gradually | open |
| R4 | W1 | Optional LLM unavailable or too slow | no LLM notes | Vedant | template notes always work; LLM optional | open |
| R5 | W1 | Writing takes longer than coding | late report | Brahmanand | start outline in Week 8, chapters in Week 9 | open |

## 5. Hours log (actual vs planned 11 h per member per week)

| Week | Brahmanand | Atharv | Vedant | Somesh | Notes |
|---|---|---|---|---|---|
| 1 | / 11 | / 11 | / 11 | / 11 | |
| 2 | / 11 | / 11 | / 11 | / 11 | |
| 3 | / 11 | / 11 | / 11 | / 11 | |
| 4 | / 11 | / 11 | / 11 | / 11 | |
| 5 | / 11 | / 11 | / 11 | / 11 | |
| 6 | / 11 | / 11 | / 11 | / 11 | |
| 7 | / 11 | / 11 | / 11 | / 11 | |
| 8 | / 11 | / 11 | / 11 | / 11 | |
| 9 | / 11 | / 11 | / 11 | / 11 | |
| 10 | / 11 | / 11 | / 11 | / 11 | |

Write the hours you actually spent — honest numbers help plan the next week.
