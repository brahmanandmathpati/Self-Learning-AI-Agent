# Self-Learning AI Agent — 10-Week Execution Handbook

**Team:** Brahmanand Mathpati · Atharv Gundale · Vedant Biradar · Somesh Badwane
**Budget:** ₹0 — free and open-source tools only; no paid APIs; no mandatory cloud; the core AI works without Ollama or any LLM.

## What is in this package

| File | Use it for |
|---|---|
| `WEEK_01_Project_Discovery_and_Requirements.md` … `WEEK_10_Final_Validation_and_Project_Demonstration.md` | The plan for each week. Every file has the same 14 sections: overview · what we build · Day 1–7 plan · member tasks (Task ID, 15 items each) · complete code · folder tree (new/modified files marked) · GitHub procedure · integration · testing · problems & solutions · deliverables · review meeting · completion checklist · next-week handoff. |
| `MASTER_TASK_TRACKER.md` | All 72 tasks with IDs, owners, priorities, hours (11 h per member per week) and dependencies, generated from the weekly files. |
| `GITHUB_WORKFLOW.md` | Branch protection, naming, the 13-step PR flow, reviews, CI, conflicts, tags and releases. |
| `PROJECT_PROGRESS_TRACKER.md` | Weekly status, Definitions of Done, deliverable ticks, results log, risks, hours log. |
| `TEAM_RESPONSIBILITY_MATRIX.md` | RACI chart for every module, test area, experiment, document and process. |
| `reference-implementation/` | The complete code the handbook embeds (final state after Week 10), so you can compare your work file by file. `handbook_snippets/` holds the earlier versions of files that change across weeks (CLI in Weeks 3/5/6, pipeline in Week 6, Results page in Week 7). |

## How to use it

1. On Day 1 of each week, everyone reads Sections 1–4 of that week's file; the integration captain creates the GitHub issues from Section 7.
2. Type the code yourself from Section 5 (or compare with `reference-implementation/`). Typing it and reading the explanations is how you learn it for the viva.
3. Never rename a module or file — later weeks import them by these exact names.
4. Record only numbers that the project's scripts actually produce. Targets in the handbook are labelled as targets; example outputs use placeholders such as `x.xx`.

## Verification status of the reference code (be aware)

- Checked in the authoring sandbox: 139 tests passed with the Python, NumPy, pandas and SciPy parts, `ruff check .` is clean, and the CLI and scripts were smoke-run end to end on FrozenLake.
- **Not executed in the authoring sandbox:** PyTorch-based code (DQN, its tests and the smoke test) and Streamlit pages/UI tests — those packages could not be installed there. They are written against the documented APIs and run in CI. In Week 3–4 your CI and laptops are the first real run: if anything fails, fix it with a normal PR and a test.
- No experiment results are included. The results tables are produced by your runs in Weeks 6–8.

## Stack additions flagged in the handbook

- `src/sla/reflection/reflect.py` — a small module added to the master plan's file list to join facts → LLM/template → grounding → storage (Week 7). It adds no library.
- `scripts/regression_check.py` — a Week-10 script that re-evaluates final checkpoints and compares them with the manifest. It uses only existing project functions.
- Everything else uses the dependencies already listed in the master plan (`pyproject.toml`): Gymnasium, NumPy, pandas, SciPy, Matplotlib, PyYAML, psutil, requests, Streamlit, PyTorch CPU, pytest, pytest-cov, ruff. Ollama with `qwen2.5:1.5b` (Apache-2.0) is **optional**.
