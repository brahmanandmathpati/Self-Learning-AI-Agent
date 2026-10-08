# WEEK 08 — Testing and Performance Improvement

**Project:** Self-Learning AI Agent · **Team:** Brahmanand Mathpati, Atharv Gundale, Vedant Biradar, Somesh Badwane
**Source:** *Self_Learning_AI_Agent_10_Week_Master_Plan* (v1.0) · **Interfaces:** `docs/design.md` (tag `w2-design-freeze`)

---

## SECTION 1 — WEEK OVERVIEW

| Item | Details |
|---|---|
| Week number | 8 of 10 |
| Week title | Testing and Performance Improvement |
| Main objective | Produce the **final, traceable results** and prove the system is **reliable**: freeze the code, run the final 5-seed experiments and the full ablation, generate every table from files (never by hand), analyse failures, measure speed/memory, prove learning survives a restart, and harden the UI. |
| Expected outcome | Tag `v0.8-experiments`; `results/manifest.csv` (one row per final run with git commit); `results/final_table.md`; `results/ablation/summary.csv`; `results/failure_analysis.md`; `results/performance.md`; `results/test_report.md`; `results/reflection_eval.md`; `test_persistence.py` passing; UI bugs from Week 7 fixed with tests. |
| Required knowledge | All previous weeks; reading test coverage reports; basic profiling ideas (time, memory); how to describe results honestly (mean ± std, CI, limitations). |
| Required tools | Same venv; `psutil` (already a dependency since Week 3) for memory; `pytest-cov` (dev extra since Week 3). No new dependency. |
| Prerequisites from previous weeks | Week 7 merged: full pipeline, CLI, reflection, stats, ablation code, dashboard; open `bug` issues list. |
| Approximate workload | 11 h per member + unattended overnight runs. |
| Technical dependencies | Code freeze tag `v0.8-experiments` on **Day 1** (only bug fixes after it, each with a test). Final experiments finish by **Day 4** (tables, failure analysis and reflection evaluation read their outputs). |
| Definition of Done | All tests pass in CI; coverage report attached to `results/test_report.md`; every number in `results/final_table.md` regenerates from `results/manifest.csv` by running `scripts/make_tables.py`; persistence test passes; performance measured on every member's laptop with hardware details; no fabricated or hand-edited numbers. |

**In simple words:** this is "exam week" for the project itself. We stop adding features, run the real experiments once, carefully, and make sure anyone can repeat them.

---

## SECTION 2 — WHAT WE ARE BUILDING THIS WEEK

1. **Modules/scripts:** `scripts/run_final_experiments.py`, `scripts/make_tables.py`, full ablation run (Atharv) · `scripts/failure_analysis.py`, `tests/integration/test_persistence.py` (Brahmanand) · `scripts/measure_performance.py`, test report, reflection evaluation (Vedant) · UI hardening, new UI tests, bug fixes, reflection rating study (Somesh).
2. **Why:** the report (Week 9) and viva (Week 10) need numbers that are final, reproducible and honest; a project that crashes in the demo loses marks regardless of its results.
3. **Connection:** Week 9 writes the report from the files produced here; Week 10 re-runs the regression check and demo on the same tag.
4. **If missing:** results typed by hand cannot be defended; unknown performance limits surprise you during the demo.
5. **Final output (shape only — your numbers will differ):**
   ```text
   $ python scripts/make_tables.py
          label            env  n_seeds  mean  std_across_seeds  git_sha  ci95_low  ci95_high  random_mean  p_value_vs_random
   dqn_cartpole    CartPole-v1        5   ...               ...  a1b2c3d       ...        ...          ...                ...
   q_frozenlake  FrozenLake-v1        5   ...               ...  a1b2c3d       ...        ...          ...                ...
   ```

**Analogy:** a scientist's lab notebook — every result has the date, the exact recipe (commit + config) and the raw data next to it.

### Result traceability chain
```text
git tag v0.8-experiments ─► run_final_experiments.py ─► runs/<run_id>/metrics.json
                                                     └► results/manifest.csv (label, run_id, seed, git_sha, final_mean, ...)
results/manifest.csv + results/baseline/baseline.csv ─► make_tables.py ─► results/final_table.md / .csv
```

---

## SECTION 3 — DAILY EXECUTION PLAN

### Day 1 — Code freeze and run plan (1.5 h)
- **Daily objective:** a frozen, tagged commit and a written plan of which laptop runs what.
- **Assigned members:** all; **Vedant** is integration captain (testing week).
- **Individual tasks:** Atharv: write `run_final_experiments.py` (SLA-08-AG-1 steps 1–2) and the run plan table in issue #81. Brahmanand: `test_persistence.py` (SLA-08-BM-2 steps 1–2). Vedant: run the full test suite with coverage, list gaps (SLA-08-VB-2 step 1). Somesh: triage the Week-7 `bug` issues with Vedant (SLA-08-SB-1 step 1).
- **Required commands:**
  ```bash
  git checkout main && git pull && pytest --cov=sla --cov-report=term-missing
  git tag -a v0.8-experiments -m "Code freeze for final experiments"   # Atharv, after CI is green
  git push origin v0.8-experiments
  ```
- **Expected output:** tag on GitHub; run plan (laptop × config × seeds) in issue #81.
- **GitHub activity:** issues #81–#89 created; tag pushed.
- **Completion checklist:** - [ ] CI green · - [ ] tag pushed · - [ ] run plan agreed

### Day 2 — Start final experiments (1.5 h + overnight)
- **Daily objective:** all final runs started on the tagged commit.
- **Assigned members:** everyone runs their share (example plan: Atharv DQN seeds 0–1 + ablation `no_replay`; Brahmanand DQN seed 2 + ablation `no_target`; Vedant DQN seeds 3–4; Somesh FrozenLake seeds 0–4 + baseline).
- **Individual tasks:** SLA-08-AG-1 step 3 · SLA-08-AG-2 step 1.
- **Required commands:**
  ```bash
  git fetch --tags && git checkout v0.8-experiments          # "detached HEAD" is expected here
  python scripts/run_final_experiments.py --config configs/frozenlake_q.yaml --label q_frozenlake --seeds 0 1 2 3 4
  python scripts/run_final_experiments.py --config configs/cartpole_dqn.yaml --label dqn_cartpole --seeds 3 4
  ```
- **Expected output:** each laptop has its own `results/manifest.csv` rows (merged on Day 4).
- **Completion checklist:** - [ ] all runs started

### Day 3 — Persistence, performance, UI tests (1.5 h)
- **Daily objective:** reliability evidence while experiments run.
- **Assigned members:** Brahmanand (persistence test → PR #85), Vedant (`measure_performance.py`), Somesh (new UI tests, first bug fix), Atharv (`make_tables.py`).
- **Individual tasks:** SLA-08-BM-2 steps 3–4 · SLA-08-VB-1 steps 1–3 · SLA-08-SB-1 steps 2–4 · SLA-08-AG-1 step 4.
- **Required commands:**
  ```bash
  git checkout main && git pull                              # code work happens on main-based branches
  pytest tests/integration/test_persistence.py -v
  python scripts/measure_performance.py --config configs/cartpole_dqn.yaml --episodes 100
  ```
- **Completion checklist:** - [ ] persistence test green · - [ ] performance measured on 1 laptop

### Day 4 — Collect results, build tables (1.5 h)
- **Daily objective:** one manifest, one generated table.
- **Assigned members:** Atharv (merges manifest rows; runs `make_tables.py`), Vedant (checks every row against its `metrics.json`), Brahmanand (failure analysis on the best DQN checkpoints), Somesh (bug fix 2).
- **Individual tasks:** SLA-08-AG-1 steps 5–6 · SLA-08-BM-1 steps 1–3 · SLA-08-SB-1 step 5.
- **Required commands:**
  ```bash
  python scripts/make_tables.py --manifest results/manifest.csv --baseline results/baseline/baseline.csv
  python scripts/failure_analysis.py --checkpoint runs/<run_id>/checkpoints/best --episodes 100
  ```
- **Completion checklist:** - [ ] `final_table.md` generated · - [ ] cross-check done

### Day 5 — Ablation results, reflection evaluation (1.5 h)
- **Daily objective:** ablation statistics; reflection notes rated.
- **Assigned members:** Atharv (ablation summary), Vedant + Somesh (reflection evaluation: generate notes for every final run, rate them blind), Brahmanand (writes `results/failure_analysis.md`).
- **Individual tasks:** SLA-08-AG-2 steps 2–4 · SLA-08-VB-3 · SLA-08-SB-2 · SLA-08-BM-1 step 4.
- **Required commands:**
  ```bash
  python scripts/run_ablation.py --config configs/cartpole_dqn.yaml --seeds 0 1 2 3 4
  for id in $(python -c "import pandas as pd; print(' '.join(pd.read_csv('results/manifest.csv').run_id))"); do sla reflect --run-id $id; done
  ```
- **Completion checklist:** - [ ] ablation summary · - [ ] notes rated

### Day 6 — Reports and remaining fixes (2.5 h)
- **Daily objective:** all result documents written; performance on all 4 laptops; all PRs merged.
- **Assigned members:** all.
- **Individual tasks:** Vedant: `results/test_report.md` + `results/performance.md` (SLA-08-VB-1 step 4, SLA-08-VB-2 steps 2–4). Somesh: bug fix 3 + merge. Atharv: `results/final_table.md` PR. Everyone: run `measure_performance.py` and `hardware_check.py` on their laptop and send the output to Vedant.
- **Completion checklist:** - [ ] 5 result documents merged · - [ ] all PRs merged · - [ ] CI green

### Day 7 — Weekly review (1 h)
- **Daily objective:** present the final table, ablation, failure analysis and performance; agree what the report claims (and does not claim). Section 12 agenda.
- **Completion checklist:** - [ ] Section 13 complete

---

## SECTION 4 — INDIVIDUAL MEMBER TASKS

### Brahmanand Mathpati

**Task ID:** SLA-08-BM-1
**Task Title:** Failure analysis of the trained agents
**Priority:** P1
**Estimated Duration:** 5 h (coding 2, testing 1, integration 1, docs 1)
**Dependencies:** final experiment checkpoints (Day 2–4); `envs.end_reason` (W3)
**Assigned Member:** Brahmanand Mathpati

1. **What:** `scripts/failure_analysis.py` and `results/failure_analysis.md`.
2. **Why:** a mean score hides *how* the agent fails. Counting episode endings (pole angle, cart position, truncated = survived; hole vs goal on FrozenLake) shows what the agent learned and what it did not.
3. **Files:** as item 1.
4. **Functions:** `main()` — loads a checkpoint, runs greedy episodes on test seeds, counts `end_reason`.
5. **Inputs:** `--checkpoint`, `--episodes`.
6. **Outputs:** printed counts per reason; your written analysis.
7. **Steps:** write the script (Section 5.1) → run on the best checkpoint of every final DQN seed and one FrozenLake seed → write the doc (template in Section 5.1) with the printed counts copied exactly → PR #84.
8. **Commands:**
   ```bash
   git checkout -b feat/brahmanand-84-failure-analysis
   python scripts/failure_analysis.py --checkpoint runs/<run_id>/checkpoints/best --episodes 100
   git add scripts/failure_analysis.py results/failure_analysis.md
   git commit -m "feat(scripts): add failure analysis of evaluation episodes"
   git push -u origin feat/brahmanand-84-failure-analysis
   ```
9. **Tests:** run twice → same counts (fixed test seeds).
10. **Expected result:** counts that add up to the number of episodes for each checkpoint.
11. **Common errors:** using a training checkpoint instead of `best`; analysing on training seeds (the script uses `TEST_SEED_BASE`).
12. **Branch:** `feat/brahmanand-84-failure-analysis`
13. **Commit:** `feat(scripts): add failure analysis of evaluation episodes`
14. **PR title:** `feat: failure analysis (SLA-08-BM-1)`
15. **Acceptance:** doc lists run ids and copied counts; reviewer: Vedant.

**Task ID:** SLA-08-BM-2
**Task Title:** Persistence test — learning survives a restart
**Priority:** P1
**Estimated Duration:** 6 h (coding 1, testing 3, integration 2)
**Dependencies:** checkpoints (W5), evaluator (W6)
**Assigned Member:** Brahmanand Mathpati

1. **What:** `tests/integration/test_persistence.py`.
2. **Why:** "self-learning" means knowledge is kept. This test proves that a saved agent, reloaded — even in a **new Python process** — has the same Q-table and the same evaluation score.
3. **Files:** as item 1.
4. **Functions:** `test_reloaded_agent_has_same_q_table_and_score`, `test_new_process_gets_same_score` (uses `subprocess` + `sys.executable`).
5. **Inputs:** a short FrozenLake training run (`fl_cfg`).
6. **Outputs:** pass/fail.
7. **Steps:** write test 1 (same process) → write test 2 (child process prints the score; compare) → run 3 times → PR #85.
8. **Commands:**
   ```bash
   git checkout -b test/brahmanand-85-persistence
   pytest tests/integration/test_persistence.py -v
   git add tests/integration/test_persistence.py
   git commit -m "test: prove learned agent survives save, exit and reload"
   git push -u origin test/brahmanand-85-persistence
   ```
9. **Tests:** the two tests.
10. **Expected result:** `2 passed`.
11. **Common errors:** child process cannot import `sla` → pass `sys.executable` (the venv's Python); path problems on Windows → pass paths as `str(path)`.
12. **Branch:** `test/brahmanand-85-persistence`
13. **Commit:** `test: prove learned agent survives save, exit and reload`
14. **PR title:** `test: persistence across processes (SLA-08-BM-2)`
15. **Acceptance:** green in CI; reviewer: Atharv.

### Atharv Gundale

**Task ID:** SLA-08-AG-1
**Task Title:** Final experiments with manifest, and generated results table
**Priority:** P1
**Estimated Duration:** 6 h (coding 2, testing 2, integration 1, docs 1) + overnight runs
**Dependencies:** `run_pipeline` (W7), `stats.bootstrap_ci`/`compare_groups` (W7), baseline CSV (W6)
**Assigned Member:** Atharv Gundale

1. **What:** `scripts/run_final_experiments.py`, `scripts/make_tables.py`, `results/manifest.csv`, `results/final_table.md` (+ `.csv`).
2. **Why:** every reported number must trace to a run folder and commit; tables are generated, never typed.
3. **Files:** as item 1.
4. **Functions:** `run_final_experiments.main()` appends one row per seed (fields `label, run_id, env, agent, seed, git_sha, final_mean, final_std, success_rate, episodes_completed, stopped_reason, run_dir`); `make_tables.main()` groups by label/env, adds std across seeds, bootstrap CI and p-value vs random.
5. **Inputs:** configs, labels, seeds; manifest + baseline CSV.
6. **Outputs:** manifest; final table (CSV + Markdown).
7. **Steps:**
   1. Write `run_final_experiments.py` (Section 5.2).
   2. Agree the run plan; tag `v0.8-experiments`.
   3. Run your share on the tag.
   4. Write `make_tables.py`.
   5. Merge the 4 laptops' manifest rows into one `results/manifest.csv` (copy rows; never edit numbers). Vedant cross-checks against `metrics.json`.
   6. Generate `final_table.md`; PR #81/#82.
8. **Commands:**
   ```bash
   git checkout main && git pull && git checkout -b exp/atharv-81-final-experiments
   python scripts/make_tables.py
   git add scripts/run_final_experiments.py scripts/make_tables.py results/manifest.csv results/final_table.md results/final_table.csv
   git commit -m "exp: final five-seed results generated from manifest"
   git push -u origin exp/atharv-81-final-experiments
   ```
9. **Tests:** run `make_tables.py` twice → identical output; every manifest `git_sha` equals the tag's commit (`git rev-parse --short v0.8-experiments`).
10. **Expected result:** a table regenerable by anyone from the repo. Write whatever the runs produced — including a seed that did not learn.
11. **Common errors:** mixed commits in the manifest (`git_sha` column lists two values) → a laptop ran on `main` instead of the tag; re-run those seeds on the tag. `to_markdown` ImportError → the script falls back to plain text (no new dependency needed).
12. **Branch:** `exp/atharv-81-final-experiments`
13. **Commit:** `exp: final five-seed results generated from manifest`
14. **PR title:** `exp: final results (SLA-08-AG-1)`
15. **Acceptance:** Vedant confirms every row; table regenerates; reviewer: Vedant.

**Task ID:** SLA-08-AG-2
**Task Title:** Full 5-seed ablation and its interpretation
**Priority:** P1
**Estimated Duration:** 5 h (testing 2, integration 2, docs 1) + overnight runs
**Dependencies:** ablation code (W7); code freeze
**Assigned Member:** Atharv Gundale

1. **What:** run `scripts/run_ablation.py` with 5 seeds on the tag; commit `results/ablation/ablation.csv` and `summary.csv`; write a short interpretation in `docs/notes/ablation_notes.md`.
2. **Why:** shows whether replay and the target network each matter in *our* setting.
3. **Files:** `results/ablation/*.csv`, `docs/notes/ablation_notes.md`.
4. **Functions:** `run_ablation`, `compare_groups`.
5. **Inputs:** `configs/cartpole_dqn.yaml`, seeds 0–4, variants `full`, `no_replay`, `no_target`.
6. **Outputs:** per-run CSV; summary with difference CI and p-value.
7. **Steps:** split variants across laptops (`--variants no_replay` etc. and different `--out-dir`) → combine the CSV rows → re-run the summary on the combined file (or run all variants on one laptop overnight) → interpret.
8. **Commands:**
   ```bash
   python scripts/run_ablation.py --config configs/cartpole_dqn.yaml --seeds 0 1 2 3 4 --variants full no_replay --out-dir results/ablation
   git add results/ablation docs/notes/ablation_notes.md
   git commit -m "exp: five-seed ablation of replay and target network"
   ```
9. **Tests:** summary rows exist for both comparisons; n = 5 per group.
10. **Expected result:** whatever the data shows. If a component does **not** make a significant difference, say so — that is a valid finding.
11. **Common errors:** comparing variants trained on different commits; claiming significance when the CI includes 0.
12. **Branch:** `exp/atharv-83-ablation`
13. **Commit:** `exp: five-seed ablation of replay and target network`
14. **PR title:** `exp: ablation results (SLA-08-AG-2)`
15. **Acceptance:** interpretation reviewed by Brahmanand; reviewer: Brahmanand.

### Vedant Biradar

**Task ID:** SLA-08-VB-1
**Task Title:** Performance measurement
**Priority:** P1
**Estimated Duration:** 4 h (coding 2, testing 1, docs 1)
**Dependencies:** `hardware_check.py` (W1, Somesh); runner
**Assigned Member:** Vedant Biradar (integration captain, Week 8)

1. **What:** `scripts/measure_performance.py` and `results/performance.md`.
2. **Why:** NFRs from Week 1 (e.g. training time on a student laptop, UI responsiveness) must be checked with measurements, on real hardware.
3. **Files:** as item 1.
4. **Functions:** `main()` — training time, steps per second, action-selection latency, peak RAM (`psutil`).
5. **Inputs:** `--config`, `--episodes`, `--run-root`.
6. **Outputs:** printed measurements; table of 4 laptops in the doc.
7. **Steps:** write script → run on your laptop → collect 3 teammates' outputs + `hardware_check.py` → write the doc comparing with the NFR targets → PR #86.
8. **Commands:**
   ```bash
   git checkout -b feat/vedant-86-performance
   python scripts/hardware_check.py
   python scripts/measure_performance.py --config configs/cartpole_dqn.yaml --episodes 100
   python scripts/measure_performance.py --config configs/frozenlake_q.yaml --episodes 2000
   git add scripts/measure_performance.py results/performance.md
   git commit -m "feat(scripts): measure training speed, latency and memory"
   git push -u origin feat/vedant-86-performance
   ```
9. **Tests:** run twice; numbers similar (timing varies — report it as approximate).
10. **Expected result:** a 4-laptop table with CPU/RAM next to each measurement.
11. **Common errors:** measuring while other programs run (close the browser); comparing laptops without their specs.
12. **Branch:** `feat/vedant-86-performance`
13. **Commit:** `feat(scripts): measure training speed, latency and memory`
14. **PR title:** `feat: performance measurement (SLA-08-VB-1)`
15. **Acceptance:** NFRs marked met / not met honestly; reviewer: Atharv.

**Task ID:** SLA-08-VB-2
**Task Title:** Test report with coverage
**Priority:** P1
**Estimated Duration:** 4 h (testing 3, docs 1)
**Dependencies:** all tests merged
**Assigned Member:** Vedant Biradar

1. **What:** `results/test_report.md`.
2. **Why:** the report's testing chapter needs a summary of what is tested, how, and what is not.
3. **Files:** as item 1.
4. **Functions:** —
5. **Inputs:** `pytest` and coverage output.
6. **Outputs:** table per test file (purpose, count, pass), coverage per package, known gaps.
7. **Steps:** run `pytest --cov=sla --cov-report=term-missing -m "not smoke"` and `pytest -m smoke` → fill the template (Section 5.3) with copied output → list untested lines and why → PR #87.
8. **Commands:**
   ```bash
   pytest --cov=sla --cov-report=term-missing -m "not smoke" | tee test_output.txt
   pytest -m smoke -v
   ```
9. **Tests:** n/a (this is the report of tests).
10. **Expected result:** report with copied numbers; target from master plan: core modules (`agent`, `learning`, `memory`, `evaluation`) ≥ 80 % — report the real figure.
11. **Common errors:** pasting coverage from an old run; forgetting the smoke and UI tests.
12. **Branch:** `docs/vedant-87-test-report`
13. **Commit:** `docs(results): add test report with coverage`
14. **PR title:** `docs: test report (SLA-08-VB-2)`
15. **Acceptance:** numbers match a CI run linked in the PR; reviewer: Brahmanand.

**Task ID:** SLA-08-VB-3
**Task Title:** Reflection evaluation (with Somesh)
**Priority:** P2
**Estimated Duration:** 3 h (testing 1, integration 1, docs 1)
**Dependencies:** final runs; reflection (W7); feedback (W6)
**Assigned Member:** Vedant Biradar (lead), Somesh Badwane

1. **What:** `results/reflection_eval.md` — grounding pass rate for template notes (and LLM notes if Ollama is available on any laptop), plus the team's ratings.
2. **Why:** the reflection feature must be evaluated like any other component.
3. **Files:** as item 1.
4. **Functions:** `sla reflect`, `ratings_summary`, `query_reflections`.
5. **Inputs:** final run ids from the manifest.
6. **Outputs:** table: run id, source, grounding passed, rating summary.
7. **Steps:** generate notes → each member rates notes for runs they did **not** train (Reflection page) → export counts with a short Python snippet → write doc (template in Section 5.3).
8. **Commands:** `sla reflect --run-id <id>` (and `--llm` if Ollama installed).
9. **Tests:** counts in the doc match the database.
10. **Expected result:** honest pass rate and ratings; if Ollama was not used, write "LLM notes not evaluated (optional component not installed)".
11. **Common errors:** rating your own run's note (bias).
12. **Branch:** `docs/vedant-88-reflection-eval`
13. **Commit:** `docs(results): evaluate reflection notes`
14. **PR title:** `docs: reflection evaluation (SLA-08-VB-3)`
15. **Acceptance:** reviewer: Brahmanand.

### Somesh Badwane

**Task ID:** SLA-08-SB-1
**Task Title:** UI hardening: new UI tests and three bug fixes
**Priority:** P1
**Estimated Duration:** 9 h (learning 1, coding 4, testing 3, review 1)
**Dependencies:** your Week-7 pages; Week-7 `bug` issues
**Assigned Member:** Somesh Badwane

**0. Learn first (~1 h):** how to reproduce a bug before fixing it; writing a test that fails *first* and passes after the fix ("regression test"); reading an `AppTest` result (`at.exception`, `at.selectbox[0].value`, `at.info`, `at.error`).

1. **What:** two new tests in `tests/ui/test_pages.py` (`test_reflection_page_without_runs`, `test_results_page_with_a_stored_run`) and up to **3 bug fixes** from the Week-7 issues, each with its own test where possible.
2. **Why:** the dashboard is what examiners touch; each fixed bug with a test can never come back silently.
3. **Files:** modify `tests/ui/test_pages.py`, and the page files the bugs are in (`ui/pages/1_Train.py`, `2_Results.py`, `3_Reflection.py`).
4. **Functions:** pages; tests.
5. **Inputs:** bug reports (steps to reproduce).
6. **Outputs:** fixed pages; 5 UI tests in total.
7. **Steps:**
   1. With Vedant, choose 3 bugs (most visible first). If fewer than 3 were filed, run the **UI check list** below and file what you find. Do not invent bugs.
   2. Add the two new tests (Section 5.4); run them.
   3. For each bug: reproduce → write a failing test (or exact manual steps if a test is not possible) → fix → test passes → one PR per bug (`fix/somesh-89-<short-name>`).
   4. Ask Vedant to review each fix; Atharv only if you are stuck for more than 30 minutes.
   5. Update the issue with "Fixed in #PR".
   **UI check list:** empty database on each page · a run with 0 evaluations · very long run id · episodes = 1 · non-numeric characters in the comment box · 501-character comment · switching environment after choosing an agent · refreshing during training.
8. **Commands:**
   ```bash
   git checkout main && git pull
   git checkout -b test/somesh-89-ui-tests
   pytest tests/ui -v
   git add tests/ui/test_pages.py
   git commit -m "test(ui): cover reflection page and results page with data"
   git push -u origin test/somesh-89-ui-tests
   ```
9. **Tests:** 5 UI tests + one test per bug where possible.
10. **Expected result:** `5 passed` in `tests/ui`; up to 3 bug issues closed.
11. **Common errors:** the test passes before the fix (then it does not test the bug — change it); fixing two bugs in one PR (hard to review — split).
12. **Branches:** `test/somesh-89-ui-tests`, `fix/somesh-89-<short-name>` (one per bug)
13. **Commits:** `test(ui): cover reflection page and results page with data` · `fix(ui): <what was wrong>`
14. **PR titles:** `test: more UI tests (SLA-08-SB-1)` · `fix: <bug title> (SLA-08-SB-1)`
15. **Acceptance:** tests pass in CI; each fix linked to its issue; reviewer: Vedant.

**Task ID:** SLA-08-SB-2
**Task Title:** Blind rating of reflection notes
**Priority:** P3
**Estimated Duration:** 2 h (testing 1, docs 1)
**Dependencies:** SLA-08-VB-3
**Assigned Member:** Somesh Badwane

1. **What:** rate the notes of runs you did not train on the Reflection page; write 3 sentences in `results/reflection_eval.md` about what made a note useful or not.
2. **Why:** a user's view of the feature — and you built the rating form.
3–15. **Files** `results/reflection_eval.md` (Vedant's PR) · **Inputs** notes · **Outputs** ratings in DB · **Steps** open `sla dashboard` → Reflection → rate → write sentences · **Commands** `sla dashboard` · **Tests** your ratings appear in `ratings_summary` · **Expected** summary count increases · **Common errors** rating the same note twice · **Branch/Commit/PR** included in Vedant's `docs/vedant-88-reflection-eval` (commit your sentences there) · **Acceptance** Vedant confirms counts.

**Independent practice exercise:** pick one function you wrote earlier (`clean_comment`, `rolling_mean` or `safe_run_name`). Try to break it with 5 unusual inputs in a Python shell (empty string, emoji, very long text, `None`, numbers). Write down what happened; if one is a real bug, file an issue.

---

## SECTION 5 — COMPLETE TECHNICAL IMPLEMENTATION

### 5.1 Failure analysis and persistence (Brahmanand)

`scripts/failure_analysis.py`
```python
"""Failure analysis: how did evaluation episodes end? (owner: Brahmanand, Week 8)

Run:  python scripts/failure_analysis.py --checkpoint runs/<run_id>/checkpoints/best --episodes 100
CartPole episodes end by "angle" (pole fell), "position" (cart left the track)
or "truncated" (survived to the time limit). Output: a count per reason.
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from sla.agent.checkpoint import load_checkpoint
from sla.envs.factory import end_reason, make_env
from sla.evaluation.evaluate import TEST_SEED_BASE
from sla.utils.config import load_config


def classify_episodes(agent, env_name: str, env_kwargs: dict, n_episodes: int,
                      seed_base: int = TEST_SEED_BASE) -> Counter:
    env = make_env(env_name, **env_kwargs)
    reasons: Counter = Counter()
    for i in range(n_episodes):
        state, _ = env.reset(seed=seed_base + i)
        terminated = truncated = False
        reward = 0.0
        while not (terminated or truncated):
            state, reward, terminated, truncated, _ = env.step(agent.act(state, explore=False))
        reasons[end_reason(env_name, terminated, truncated, reward, state)] += 1
    env.close()
    return reasons


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--episodes", type=int, default=100)
    args = parser.parse_args()
    folder = Path(args.checkpoint)
    cfg = load_config(folder.parent.parent / "config.yaml")
    agent, info = load_checkpoint(folder)
    reasons = classify_episodes(agent, cfg.env_name, cfg.env_kwargs, args.episodes)
    print(f"Checkpoint {folder} (episode {info['episode']}), {args.episodes} test episodes:")
    for reason, count in reasons.most_common():
        print(f"  {reason:>10}: {count:>4}  ({count / args.episodes:.0%})")


if __name__ == "__main__":
    main()
```

`results/failure_analysis.md` template:
```markdown
# Failure analysis (best checkpoints, 100 test episodes each, commit <sha>)
| Run id | Env | angle | position | truncated (survived) | hole | goal | other |
|---|---|---|---|---|---|---|---|
Observations (copy counts exactly; 3-6 sentences):
What this tells us about the learned policy:
Limitations:
```

`tests/integration/test_persistence.py`
```python
"""Week 8 (Brahmanand): learning survives saving, exiting and reloading in a new process."""

import subprocess
import sys

import numpy as np

from sla.agent.checkpoint import CheckpointCallback, latest_checkpoint, load_checkpoint
from sla.agent.runner import run_training
from sla.evaluation.evaluate import evaluate_agent


def test_reloaded_agent_has_same_q_table_and_score(fl_cfg):
    result = run_training(fl_cfg, [CheckpointCallback(100)])
    agent, _ = load_checkpoint(latest_checkpoint(result.run_dir))
    again, _ = load_checkpoint(latest_checkpoint(result.run_dir))
    assert np.array_equal(agent.q, again.q)
    a = evaluate_agent(agent, fl_cfg.env_name, fl_cfg.env_kwargs, 20)
    b = evaluate_agent(again, fl_cfg.env_name, fl_cfg.env_kwargs, 20)
    assert a.mean_return == b.mean_return


def test_new_process_gets_same_score(fl_cfg):
    result = run_training(fl_cfg, [CheckpointCallback(100)])
    folder = latest_checkpoint(result.run_dir)
    agent, _ = load_checkpoint(folder)
    here = evaluate_agent(agent, fl_cfg.env_name, fl_cfg.env_kwargs, 20).mean_return
    code = (
        "from sla.agent.checkpoint import load_checkpoint;"
        "from sla.evaluation.evaluate import evaluate_agent;"
        f"a,_=load_checkpoint(r'{folder}');"
        f"print(evaluate_agent(a,'{fl_cfg.env_name}',{fl_cfg.env_kwargs!r},20).mean_return)"
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert float(out.stdout.strip()) == here
```

### 5.2 Final experiments and tables (Atharv)

`scripts/run_final_experiments.py`
```python
"""Final 5-seed experiments on a tagged commit, recorded in a manifest (owner: Atharv, Week 8).

Run:  python scripts/run_final_experiments.py --config configs/cartpole_dqn.yaml --label dqn_cartpole
Every finished run appends one row to results/manifest.csv, so each number in the
report can be traced to its run folder and git commit.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from sla.pipeline import git_sha, run_pipeline
from sla.utils.config import load_config

FIELDS = ["label", "run_id", "env", "agent", "seed", "git_sha", "final_mean", "final_std",
          "success_rate", "episodes_completed", "stopped_reason", "run_dir"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--label", required=True, help="name used in the results table, e.g. dqn_cartpole")
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    parser.add_argument("--db", default="runs/episodes.db")
    parser.add_argument("--manifest", default="results/manifest.csv")
    args = parser.parse_args()

    manifest = Path(args.manifest)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    new_file = not manifest.exists()
    sha = git_sha()
    for seed in args.seeds:
        cfg = load_config(args.config)
        cfg.seed = seed
        res = run_pipeline(cfg, args.db, final_eval_episodes=100)
        row = {"label": args.label, "run_id": res.train.run_id, "env": cfg.env_name, "agent": cfg.agent,
               "seed": seed, "git_sha": sha, "final_mean": res.final_eval.mean_return,
               "final_std": res.final_eval.std_return, "success_rate": res.final_eval.success_rate,
               "episodes_completed": res.train.episodes_completed,
               "stopped_reason": res.train.stopped_reason, "run_dir": str(res.train.run_dir)}
        with manifest.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            if new_file:
                writer.writeheader()
                new_file = False
            writer.writerow(row)
        print(f"{args.label} seed {seed}: {row['final_mean']:.2f} ± {row['final_std']:.2f} -> {manifest}")


if __name__ == "__main__":
    main()
```

`scripts/make_tables.py` — note the `git_sha` column: if it ever shows two values, runs came from different commits.
```python
"""Build the final results tables from the manifest — never type numbers by hand (owner: Atharv, Week 8).

Run:  python scripts/make_tables.py --manifest results/manifest.csv --baseline results/baseline/baseline.csv
Output: results/final_table.csv and results/final_table.md
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from sla.evaluation.stats import bootstrap_ci, compare_groups


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="results/manifest.csv")
    parser.add_argument("--baseline", default="results/baseline/baseline.csv")
    parser.add_argument("--out", default="results/final_table")
    args = parser.parse_args()

    runs = pd.read_csv(args.manifest)
    rows = []
    for (label, env), group in runs.groupby(["label", "env"]):
        scores = group["final_mean"].tolist()
        row = {"label": label, "env": env, "n_seeds": len(scores),
               "mean": round(float(pd.Series(scores).mean()), 2),
               "std_across_seeds": round(float(pd.Series(scores).std(ddof=1)), 2) if len(scores) > 1 else None,
               "git_sha": ",".join(sorted(group["git_sha"].fillna("unknown").astype(str).unique()))}
        if len(scores) >= 2:
            low, high = bootstrap_ci(scores)
            row["ci95_low"], row["ci95_high"] = round(low, 2), round(high, 2)
        if Path(args.baseline).exists():
            base = pd.read_csv(args.baseline)
            base_scores = base[(base["env"] == env) & (base["agent"] == "random")]["mean_return"].tolist()
            if len(scores) >= 2 and len(base_scores) >= 2:
                cmp = compare_groups(scores, base_scores, "agent", "random")
                row["random_mean"] = round(cmp["mean_random"], 2)
                row["p_value_vs_random"] = round(cmp["p_value"], 4)
        rows.append(row)

    table = pd.DataFrame(rows)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(out.with_suffix(".csv"), index=False)
    try:
        markdown = table.to_markdown(index=False)  # needs the optional 'tabulate' package
    except ImportError:
        markdown = "```\n" + table.to_string(index=False) + "\n```"
    out.with_suffix(".md").write_text(markdown, encoding="utf-8")
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()
```

`docs/notes/ablation_notes.md` template:
```markdown
# Ablation (5 seeds, commit <sha>, results/ablation/summary.csv)
| Comparison | mean full | mean variant | diff | 95% CI of diff | p-value |
(copy from summary.csv)
Interpretation: a CI that excludes 0 suggests a real difference; with 5 seeds treat p-values with care.
```

### 5.3 Performance, test report, reflection evaluation (Vedant)

`scripts/measure_performance.py`
```python
"""Performance measurement: speed and memory on this laptop (owner: Vedant, Week 8).

Run:  python scripts/measure_performance.py --config configs/cartpole_dqn.yaml --episodes 100
Prints training time, steps per second, action-selection latency and peak RAM.
Always report results together with the laptop details (scripts/hardware_check.py).
"""

from __future__ import annotations

import argparse
import platform
import time

import numpy as np
import psutil

from sla.agent.runner import Callback, run_training
from sla.utils.config import load_config


class RamSampler(Callback):
    """Records the process memory after every episode."""

    def __init__(self) -> None:
        self.process = psutil.Process()
        self.peak_mb = 0.0

    def on_episode_end(self, ctx, info) -> bool:
        self.peak_mb = max(self.peak_mb, self.process.memory_info().rss / 2 ** 20)
        return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--episodes", type=int, default=100)
    parser.add_argument("--run-root", default="runs/perf")
    args = parser.parse_args()

    cfg = load_config(args.config)
    cfg.episodes = args.episodes
    cfg.run_root = args.run_root
    sampler = RamSampler()
    start = time.perf_counter()
    result = run_training(cfg, [sampler])
    seconds = time.perf_counter() - start
    steps = sum(result.lengths)

    from sla.agent.runner import build_agent
    from sla.envs.factory import make_env
    env = make_env(cfg.env_name, **cfg.env_kwargs)
    agent = build_agent(cfg, env)
    obs, _ = env.reset(seed=0)
    timings = []
    for _ in range(1000):
        t0 = time.perf_counter()
        agent.act(obs, explore=False)
        timings.append((time.perf_counter() - t0) * 1000)
    env.close()

    print(f"Machine: {platform.processor() or platform.machine()}, {psutil.cpu_count(logical=False)} cores, "
          f"{psutil.virtual_memory().total / 2 ** 30:.1f} GB RAM")
    print(f"Training: {result.episodes_completed} episodes, {steps} steps in {seconds:.1f} s "
          f"({steps / seconds:.0f} steps/s)")
    print(f"Action selection: median {np.median(timings):.3f} ms, p95 {np.percentile(timings, 95):.3f} ms")
    print(f"Peak RAM during training: {sampler.peak_mb:.0f} MB")


if __name__ == "__main__":
    main()
```

`results/test_report.md` template:
```markdown
# Test report (commit <sha>, CI run <link>)
| Test file | What it checks | Tests | Result |
|---|---|---|---|
Coverage by package (copied from pytest --cov):
Smoke tests (torch): <result>       UI tests (Streamlit AppTest): <result>
Not covered and why:
Bugs found during testing (issue numbers) and their status:
```

`results/performance.md` template:
```markdown
# Performance (approximate; laptops differ)
| Member | CPU | RAM | Config | Episodes | Train time (s) | Steps/s | Act latency (ms) | Peak RAM (MB) |
NFR check: <target from docs/nfr.md> -> met / not met
```

`results/reflection_eval.md` — counting snippet (run in a Python shell):
```python
from sla.memory.episode_store import EpisodeStore
from sla.ui.feedback import ratings_summary
store = EpisodeStore("runs/episodes.db")
notes = store.query_reflections()
print(notes.groupby("source")["grounding_passed"].agg(["count", "mean"]))
print(ratings_summary(store))
```

### 5.4 UI hardening (Somesh)

`tests/ui/test_pages.py` — complete file after Week 8 (the last two tests are new):
```python
"""Streamlit UI tests with AppTest (owner: Somesh; started Week 7, extended in Week 8)."""

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402


@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    monkeypatch.setenv("SLA_DB", str(tmp_path / "ui.db"))
    import importlib

    import sla.ui.common as common
    importlib.reload(common)


def test_home_page_without_runs():
    at = AppTest.from_file("src/sla/ui/app.py").run()
    assert not at.exception
    assert any("No runs yet" in info.value for info in at.info)


def test_results_page_without_runs():
    at = AppTest.from_file("src/sla/ui/pages/2_Results.py").run()
    assert not at.exception


def test_train_page_renders_form():
    at = AppTest.from_file("src/sla/ui/pages/1_Train.py").run()
    assert not at.exception
    assert at.number_input[0].value == 300


# Week 8 (Somesh): pages with real data and the empty Reflection page.
def test_reflection_page_without_runs():
    at = AppTest.from_file("src/sla/ui/pages/3_Reflection.py").run()
    assert not at.exception


def test_results_page_with_a_stored_run(fl_cfg):
    import sla.ui.common as common
    from sla.agent.runner import run_training
    from sla.memory.episode_store import StoreCallback

    fl_cfg.episodes = 20
    result = run_training(fl_cfg, [StoreCallback(common.get_store())])
    at = AppTest.from_file("src/sla/ui/pages/2_Results.py").run()
    assert not at.exception
    assert at.selectbox[0].value == result.run_id
```

**Line by line (new tests):** `test_reflection_page_without_runs` checks the page stops politely when the database is empty · in `test_results_page_with_a_stored_run`, `fl_cfg` is Brahmanand's small FrozenLake config fixture; `common.get_store()` uses the temporary database set by the `isolated_db` fixture; after a 20-episode run, the Results page must load without an exception and pre-select that run.

**Bug-fix PR description template:**
```markdown
Fixes #<issue>
**Bug:** <what the user saw>
**Steps to reproduce:** 1. ... 2. ...
**Cause:** <one sentence>
**Fix:** <one sentence>
**Test:** <test name> fails before, passes after
```

---

## SECTION 6 — PROJECT FOLDER STRUCTURE

```text
self-learning-ai-agent/
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── configs/
│   ├── cartpole_dqn.yaml
│   ├── cartpole_random.yaml
│   ├── frozenlake_q.yaml
│   └── frozenlake_random.yaml
├── docs/
│   ├── notes/
│   │   ├── ablation_notes.md   [NEW · Atharv]
│   │   ├── dqn_debug_checklist.md
│   │   ├── dqn_explained.md
│   │   ├── q_learning_by_hand.md
│   │   └── week6_results.md
│   ├── architecture.md
│   ├── data_handling.md
│   ├── design.md
│   ├── evaluation_protocol.md
│   ├── feasibility.md
│   ├── hardware_audit.md
│   ├── learning_plans.md
│   ├── literature_review.md
│   ├── nfr.md
│   ├── requirements.md
│   ├── synopsis_draft.md
│   ├── synopsis_outline.md
│   ├── tech_stack.md
│   └── use_cases.md
├── results/
│   ├── ablation/
│   │   ├── ablation.csv   [NEW · Atharv]
│   │   └── summary.csv   [NEW · Atharv]
│   ├── baseline/
│   │   └── baseline.csv   [MODIFIED · Brahmanand]
│   ├── failure_analysis.md   [NEW · Brahmanand]
│   ├── final_table.csv   [NEW · Atharv]
│   ├── final_table.md   [NEW · Atharv]
│   ├── manifest.csv   [NEW · Atharv]
│   ├── performance.md   [NEW · Vedant]
│   ├── reflection_eval.md   [NEW · Vedant + Somesh]
│   └── test_report.md   [NEW · Vedant]
├── scripts/
│   ├── failure_analysis.py   [NEW · Brahmanand]
│   ├── hardware_check.py
│   ├── make_tables.py   [NEW · Atharv]
│   ├── measure_performance.py   [NEW · Vedant]
│   ├── quick_frozenlake_check.py
│   ├── run_ablation.py
│   ├── run_baseline.py
│   └── run_final_experiments.py   [NEW · Atharv]
├── spikes/
│   └── llm_benchmark.py
├── src/
│   └── sla/
│       ├── agent/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── checkpoint.py
│       │   ├── random_agent.py
│       │   ├── runner.py
│       │   └── safety.py
│       ├── envs/
│       │   ├── __init__.py
│       │   └── factory.py
│       ├── evaluation/
│       │   ├── __init__.py
│       │   ├── ablation.py
│       │   ├── evaluate.py
│       │   ├── metrics.py
│       │   ├── plots.py
│       │   └── stats.py
│       ├── learning/
│       │   ├── __init__.py
│       │   ├── dqn.py
│       │   ├── guards.py
│       │   ├── networks.py
│       │   ├── q_learning.py
│       │   └── schedules.py
│       ├── memory/
│       │   ├── __init__.py
│       │   ├── episode_store.py
│       │   ├── replay_buffer.py
│       │   └── retention.py
│       ├── reflection/
│       │   ├── __init__.py
│       │   ├── facts.py
│       │   ├── fallback.py
│       │   ├── grounding.py
│       │   ├── llm_client.py
│       │   └── reflect.py
│       ├── ui/
│       │   ├── pages/
│       │   │   ├── 1_Train.py   [MODIFIED · Somesh]
│       │   │   ├── 2_Results.py   [MODIFIED · Somesh]
│       │   │   └── 3_Reflection.py   [MODIFIED · Somesh]
│       │   ├── __init__.py
│       │   ├── app.py
│       │   ├── common.py
│       │   └── feedback.py
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   ├── errors.py
│       │   ├── io_helpers.py
│       │   ├── logging_setup.py
│       │   ├── seeding.py
│       │   ├── summary.py
│       │   └── validation.py
│       ├── __init__.py
│       ├── cli.py
│       └── pipeline.py
├── tests/
│   ├── integration/
│   │   ├── test_cli.py
│   │   ├── test_dqn_smoke.py
│   │   ├── test_persistence.py   [NEW · Brahmanand]
│   │   ├── test_pipeline_e2e.py
│   │   ├── test_resume.py
│   │   ├── test_runner.py
│   │   └── test_transition_validation.py
│   ├── ui/
│   │   └── test_pages.py   [MODIFIED · Somesh]
│   ├── unit/
│   │   ├── test_ablation.py
│   │   ├── test_agents.py
│   │   ├── test_cli_help.py
│   │   ├── test_config.py
│   │   ├── test_dqn.py
│   │   ├── test_envs.py
│   │   ├── test_episode_store.py
│   │   ├── test_evaluate.py
│   │   ├── test_feedback.py
│   │   ├── test_guards.py
│   │   ├── test_io_helpers.py
│   │   ├── test_logging.py
│   │   ├── test_metrics.py
│   │   ├── test_plots.py
│   │   ├── test_q_learning.py
│   │   ├── test_reflection.py
│   │   ├── test_replay_buffer.py
│   │   ├── test_safety.py
│   │   ├── test_schedules.py
│   │   ├── test_stats.py
│   │   ├── test_summary.py
│   │   └── test_validation.py
│   └── conftest.py
├── .env.example
├── .gitignore
├── CONTRIBUTING.md
├── pyproject.toml
└── README.md
```

Legend: [NEW] created this week · [MODIFIED] changed this week · no tag = carried over unchanged from an earlier week. `runs/` (training outputs) and `.venv/` exist on your laptop but are git-ignored, so they are not shown.

---

## SECTION 7 — GITHUB COLLABORATION PROCEDURE

13-step flow as every week. During the code freeze, **only** `fix/…`, `test/…`, `docs/…` and `exp/…` branches are merged; no new features.

| # | Title | Owner | Branch | Reviewer | Merge by |
|---|---|---|---|---|---|
| 81 | Final experiments + manifest | Atharv | `exp/atharv-81-final-experiments` | Vedant | Day 5 |
| 82 | Generated results table | Atharv | (with #81) | Vedant | Day 5 |
| 83 | Five-seed ablation | Atharv | `exp/atharv-83-ablation` | Brahmanand | Day 6 |
| 84 | Failure analysis | Brahmanand | `feat/brahmanand-84-failure-analysis` | Vedant | Day 6 |
| 85 | Persistence test | Brahmanand | `test/brahmanand-85-persistence` | Atharv | Day 4 |
| 86 | Performance measurement | Vedant | `feat/vedant-86-performance` | Atharv | Day 6 |
| 87 | Test report | Vedant | `docs/vedant-87-test-report` | Brahmanand | Day 6 |
| 88 | Reflection evaluation | Vedant + Somesh | `docs/vedant-88-reflection-eval` | Brahmanand | Day 6 |
| 89 | UI tests + bug fixes | Somesh | `test/somesh-89-ui-tests`, `fix/somesh-89-*` | Vedant | Day 6 |

**Tags:** `v0.8-experiments` marks the code that produced the results. If a bug fix changes training or evaluation code after the tag, the affected experiments must be **re-run** on a new tag (`v0.8.1-experiments`) — write this in the PR.

**Checking out a tag:**
```bash
git fetch --tags
git checkout v0.8-experiments     # detached HEAD: you can run code but should not commit here
git checkout main                 # go back to normal work
```

---

## SECTION 8 — WEEKLY INTEGRATION PROCEDURE

| Item | This week |
|---|---|
| Modules to connect | final scripts ↔ `run_pipeline`; tables ↔ manifest + baseline + `stats`; failure analysis ↔ checkpoints + `end_reason`; reflection evaluation ↔ store + feedback. |
| Integrator | **Vedant** (integration captain, Week 8). |
| Interfaces that must match | manifest columns (`FIELDS` in `run_final_experiments.py`) used by `make_tables.py`; `metrics.json` `final_eval` keys; baseline CSV columns `env, agent, mean_return`. |
| Tests that must pass | all (unit, integration, UI, smoke); coverage recorded. |
| Detect failures | manifest row that does not match its `metrics.json`; table changes when regenerated; `git_sha` column with two values. |
| Debug | regenerate the table; compare row by row; check the tag with `git describe --tags`. |

**Integration checklist**
- [ ] All final runs on `v0.8-experiments` (single `git_sha` in the table)
- [ ] `make_tables.py` regenerates identical files
- [ ] Persistence test green in CI
- [ ] Performance on 4 laptops with specs
- [ ] UI tests: 5 passing; bug issues closed or documented

---

## SECTION 9 — TESTING AND VALIDATION

| Type | This week | Command |
|---|---|---|
| Unit / integration (all) | full suite + coverage | `pytest --cov=sla --cov-report=term-missing` |
| Persistence | same process + new process | `pytest tests/integration/test_persistence.py -v` |
| UI | 5 AppTest tests | `pytest tests/ui -v` |
| Performance | time, steps/s, latency, peak RAM | `python scripts/measure_performance.py ...` |
| Model evaluation | 5 seeds, test seeds, CI, p-value vs random | `run_final_experiments.py` + `make_tables.py` |
| Ablation | full vs no_replay vs no_target | `run_ablation.py` |
| Failure analysis | end-reason counts | `failure_analysis.py` |
| Reflection | grounding pass rate, ratings | `results/reflection_eval.md` |

**RL rules (final results):** train and evaluation separate; fixed test seeds; no learning during evaluation; trained vs untrained/random comparison in the same table; same protocol for all variants; **no invented, cherry-picked or hand-edited numbers** — a failed seed stays in.

---

## SECTION 10 — COMMON PROBLEMS AND SOLUTIONS

| Problem | Possible Cause | How to Check | Solution |
|---|---|---|---|
| `git_sha` shows two commits | some runs not on the tag | `git_sha` column | re-run those seeds on the tag |
| Laptop sleeps during overnight run | power settings | run stops, no final checkpoint | disable sleep; `sla resume --run ...` continues |
| Manifest rows duplicated | script run twice for a seed | count rows per label/seed | keep the run that matches the plan; note it in the PR |
| Coverage lower than expected | UI pages and scripts count | per-file report | report honestly; explain scripts are run manually |
| Persistence test fails only in CI | child process uses another Python | print `sys.executable` | always pass `sys.executable` |
| Results differ between laptops | different library versions / CPU math | `pip freeze` | same tag + same `pyproject`; small float differences are normal — report per-laptop runs as they are |
| AppTest selectbox value is not the new run | page lists runs in a different order | print `store.list_runs()` | assert the run id is in `at.selectbox[0].options` instead |
| Final DQN weaker than in Week 6 | randomness across seeds | compare per-seed scores | report the final numbers; discuss variance in the report |

---

## SECTION 11 — WEEKLY DELIVERABLES

| Deliverable | Owner | File/Location | Verification | Status |
|---|---|---|---|---|
| Code-freeze tag | Atharv | tag `v0.8-experiments` | visible on GitHub | [ ] |
| Final experiments + manifest | Atharv | `scripts/run_final_experiments.py`, `results/manifest.csv` | single `git_sha`; Vedant cross-check | [ ] |
| Generated results table | Atharv | `scripts/make_tables.py`, `results/final_table.md` | regenerates identically | [ ] |
| Five-seed ablation | Atharv | `results/ablation/summary.csv`, `docs/notes/ablation_notes.md` | n = 5 per variant | [ ] |
| Failure analysis | Brahmanand | `scripts/failure_analysis.py`, `results/failure_analysis.md` | counts copied | [ ] |
| Persistence test | Brahmanand | `tests/integration/test_persistence.py` | 2 passed in CI | [ ] |
| Performance | Vedant | `scripts/measure_performance.py`, `results/performance.md` | 4 laptops + specs | [ ] |
| Test report | Vedant | `results/test_report.md` | matches CI run | [ ] |
| Reflection evaluation | Vedant + Somesh | `results/reflection_eval.md` | counts match DB | [ ] |
| UI tests + fixes | Somesh | `tests/ui/test_pages.py`, `src/sla/ui/pages/*` | 5 UI tests; issues closed | [ ] |

---

## SECTION 12 — WEEKLY REVIEW MEETING

**Agenda:** final table (regenerate it live) · ablation · failure analysis · performance · test report · open bugs · what the report will claim and what it will not.

**Questions:**
1. Atharv: regenerate `final_table.md` live. Where does each number come from?
2. Does the trained agent beat random/untrained on the test seeds? Is the CI clear of zero? Any seed that failed?
3. What did the ablation show? If a component made no clear difference, how will we explain it?
4. Brahmanand: how do CartPole episodes end for the best checkpoints, and what does that say about the policy?
5. What does the persistence test prove that the resume test (Week 5) does not?
6. Vedant: which NFRs are met and which are not, on which laptop?
7. Somesh: describe one bug you fixed: how did you reproduce it, and which test now protects it?
8. Which limitations must the report state honestly?

---

## SECTION 13 — WEEK COMPLETION CHECKLIST

- [ ] All assigned tasks completed
- [ ] Code pushed to feature branches
- [ ] Pull requests reviewed and merged (no features after the freeze)
- [ ] All tests pass locally and in CI; coverage recorded
- [ ] Results integrated: manifest → table; ablation; failure analysis; performance
- [ ] Result documents merged in `results/`
- [ ] Weekly demonstration completed
- [ ] Blockers and limitations recorded

---

## SECTION 14 — NEXT WEEK HANDOFF

- **Ready before Week 9:** `results/` folder complete (manifest, final table, ablation, failure analysis, performance, test report, reflection evaluation); green CI on `main`; tag `v0.8-experiments`.
- **Files Week 9 depends on:** every file in `results/` (report chapters 5–6), `docs/design.md` + `docs/architecture.md` (chapter 4), `docs/requirements.md` + `docs/literature_review.md` (chapters 1–3), UI screenshots (user guide), `pyproject.toml` (licences).
- **Coordination:** report chapters are split by owner (Week 9): Brahmanand 1–3, Atharv 4, Vedant 5–6, Somesh user guide/contributions/slides. Agree the report template (fonts, figure numbering) on Week-9 Day 1.
- **Risks:** writing takes longer than coding — start Day 1; any late code change after the tag forces a re-run — avoid unless it is a real bug.
