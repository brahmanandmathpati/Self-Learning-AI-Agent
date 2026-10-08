# TEAM RESPONSIBILITY MATRIX (RACI) — Self-Learning AI Agent

**R** = Responsible (does the work) · **A** = Accountable (approves; exactly one per row) · **C** = Consulted (gives input before/during) · **I** = Informed (kept up to date)

**Team:** BM = Brahmanand Mathpati (core agent, runner, pipeline, CLI; integration captain W2, W4, W6, W7) · AG = Atharv Gundale (team guide, repository/CI, learning algorithms, statistics, releases; captain W1, W5, W9; W10 final-review lead) · VB = Vedant Biradar (memory, evaluation, reflection, testing lead; captain W3, W8; Somesh's reviewer from W4) · SB = Somesh Badwane (validation, plots, feedback, dashboard, user docs; beginner track with mentoring)

**Guiding principles**
- Atharv **guides** the team (reviews, pairing, unblocking) — he is not Responsible for other members' modules.
- Somesh is Responsible for real, gradually harder modules (validation → plots → feedback → dashboard → export), with Atharv/Vedant Consulted, never doing the work for him.
- Exactly one **A** per row; the A merges or signs off.

---

## 1. Code modules (`src/sla/`)

| Module / file | Week | BM | AG | VB | SB |
|---|---|---|---|---|---|
| `utils/io_helpers.py` | 2 | I | C | I | **R/A** |
| `utils/errors.py`, `utils/logging_setup.py` | 3 | C | C | **R/A** | I |
| `utils/config.py` + `configs/*.yaml` | 3 | C | C | I | **R/A** |
| `utils/seeding.py`, `envs/factory.py` | 3 | **R/A** | C | I | I |
| `agent/base.py`, `agent/random_agent.py` | 3 | **R/A** | C | C | I |
| `pyproject.toml`, package skeleton, CI | 3 | C | **R/A** | C | I |
| `agent/runner.py`, `agent/safety.py` | 4 | **R/A** | C | C | I |
| `learning/q_learning.py` | 4 | **R/A** | C | I | I |
| `learning/schedules.py`, `networks.py`, `dqn.py` | 4 | C | **R/A** | C | I |
| `memory/replay_buffer.py` | 4 | I | C | **R/A** | I |
| `utils/validation.py` (W4 run-request) | 4 | C | I | C | **R/A** |
| `utils/summary.py` | 4 | C | I | C | **R/A** |
| `agent/checkpoint.py` | 5 | **R/A** | C | C | I |
| `cli.py` (all regions) | 3, 5–7 | **R/A** | C | C | I |
| `memory/episode_store.py`, `memory/retention.py` | 5 | C | C | **R/A** | I |
| `evaluation/plots.py` | 5 | I | C | C | **R/A** |
| `pipeline.py` | 6–7 | **R/A** | C | C | I |
| `learning/guards.py` | 6 | C | **R/A** | C | I |
| `evaluation/evaluate.py`, `evaluation/metrics.py` | 6 | C | C | **R/A** | I |
| `utils/validation.py` (W6 transition) | 6 | C | I | C | **R/A** |
| `ui/feedback.py` | 6 | I | I | C | **R/A** |
| `evaluation/stats.py`, `evaluation/ablation.py` | 7 | C | **R/A** | C | I |
| `reflection/*` (facts, grounding, fallback, llm_client, reflect) | 7 | C | C | **R/A** | I |
| `ui/common.py`, `ui/app.py`, `ui/pages/*` | 7–8 | C | C (pairing) | C (review) | **R/A** |
| `ui/export.py` (independent enhancement) | 10 | I | I | C (review) | **R/A** |

## 2. Tests

| Test area | BM | AG | VB | SB |
|---|---|---|---|---|
| Unit tests for each module | R (own) | R (own) | R (own) | R (own) |
| `tests/conftest.py` W4 region / W5 region | **R/A** (W4) | I | **R/A** (W5) | I |
| Integration: runner, resume, pipeline, CLI, persistence | **R/A** | C | C | I |
| Integration: DQN smoke | C | **R/A** | I | I |
| Integration: transition validation | C | I | C | **R/A** |
| UI tests (`tests/ui/`) | I | C | C | **R/A** |
| Overall test strategy, coverage, test report | C | C | **R/A** | C |

## 3. Experiments and results

| Deliverable | BM | AG | VB | SB |
|---|---|---|---|---|
| Hand-computed Q-learning example (W1) | **R/A** | C | I | I |
| Hardware audit (W1) | I | C | I | **R/A** |
| LLM spike / benchmark (W2, optional component) | I | **R/A** | C | I |
| Baselines (W6) | **R/A** | C | C | I |
| Five-seed runs + DQN config tuning (W6) | R (seeds) | **R/A** | C (cross-check) | R (seeds) |
| Evaluation protocol (W6) | C | C | **R/A** | I |
| Final experiments + manifest + tables (W8) | R (seeds) | **R/A** | C (cross-check) | R (seeds) |
| Full ablation (W8) | R (variant) | **R/A** | C | I |
| Failure analysis (W8) | **R/A** | C | C | I |
| Performance measurement (W8) | R (own laptop) | R (own laptop) | **R/A** | R (own laptop) |
| Reflection evaluation (W8) | C | I | **R/A** | R |
| Regression check (W10) | **R/A** | C | C | I |

## 4. Documentation, report and presentation

| Deliverable | BM | AG | VB | SB |
|---|---|---|---|---|
| Requirements, synopsis outline/draft (W1–2) | **R/A** | C | C | I |
| Feasibility, learning plans (W1) | C | **R/A** | I | C |
| Use cases, NFRs (W1) | C | C | **R/A** | I |
| Design (`docs/design.md`) (W2) | **R/A** | R | R | C |
| Architecture, tech stack (W2) | C | **R/A** | C | I |
| Literature review (W2) | C | C | **R/A** | I |
| CONTRIBUTING.md (W3) | C | **R/A** | R | I |
| DQN notes + team session (W4) | I | **R/A** | I | I |
| Data handling doc (W5) | C | I | **R/A** | I |
| README (final) (W9) | **R/A** | C | C | C (fresh-eyes review) |
| Module docs (W9) | R (agent) | R (learning) | R (memory/eval/reflection) | R (ui); A: owner of each |
| Licences, CHANGELOG, clean-install test (W9) | C | **R/A** | I | R (tester) |
| Report ch 1–3 | **R/A** | I | C (review) | I |
| Report ch 4 | C (review) | **R/A** | C (diagrams) | I |
| Report ch 5–6 + figures | C | C (review) | **R/A** | I |
| Final report (W10) | C (number check) | C (number check) | **R/A** | C |
| User guide, screenshots (W9) | C | I | C (tester) | **R/A** |
| Contribution record (W9–10) | C (confirms) | C (confirms) | C (confirms) | **R/A** |
| Slides draft / final | C | C | C | **R/A** |
| Demo script (W10) | **R/A** | C | C | C |
| Demo video (W10) | C | I | I | **R/A** |
| Viva question bank + mock vivas (W10) | R (own answers) | **R/A** | R (own answers) | R (own answers) |
| Evidence pack (W10) | C | C | **R/A** | C |

## 5. Process and coordination

| Activity | BM | AG | VB | SB |
|---|---|---|---|---|
| Repository settings, branch protection, labels, board | I | **R/A** | I | I |
| CI workflow maintenance | C | **R/A** | C | I |
| Weekly issue creation and assignment | R (own) | **A** | R (own) | R (own) |
| Integration captain (merge order, `main` stays green) | **R/A** W2, W4, W6, W7 | **R/A** W1, W5, W9, W10 | **R/A** W3, W8 | I |
| Code reviews | R | R | R | R (from W6, guided) |
| Mentoring Somesh (lessons, pairing) | C | **R/A** | R (reviews from W4) | I |
| Weekly review meeting (agenda, notes) | R | **A** | R | R |
| Code freeze and tags (`v0.8-experiments`, `v0.9-rc`, `v1.0`) | C | **R/A** | C | I |
| Risk and blocker tracking | R | **A** | R | R |

If any assignment above differs from a weekly handbook, the weekly handbook's Section 4 and Section 8 take precedence for that week.
