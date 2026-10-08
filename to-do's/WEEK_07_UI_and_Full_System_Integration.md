# WEEK 07 — UI and Full System Integration

**Project:** Self-Learning AI Agent · **Team:** Brahmanand Mathpati, Atharv Gundale, Vedant Biradar, Somesh Badwane
**Source:** *Self_Learning_AI_Agent_10_Week_Master_Plan* (v1.0) · **Interfaces:** `docs/design.md` (tag `w2-design-freeze`)

---

## SECTION 1 — WEEK OVERVIEW

| Item | Details |
|---|---|
| Week number | 7 of 10 |
| Week title | UI and Full System Integration |
| Main objective | Join everything into **one working system**: a one-call pipeline (train → evaluate → plots → explanation note), a **Streamlit dashboard** (Train, Results, Reflection pages), **grounded reflection notes** (template by default, optional local LLM), and **statistics + ablation** to prove which DQN parts matter. |
| Expected outcome | `sla pipeline --config ... --seeds 0 1 2 3 4` runs end to end; `sla dashboard` opens the UI; every explanation note passes the grounding check (no invented numbers); a small ablation pilot (full vs no_replay vs no_target) produces a CSV and statistics. |
| Required knowledge | Weeks 4–6 modules; Streamlit basics (Somesh, with Atharv); HTTP requests (Vedant, optional Ollama); statistics: mean, std, confidence interval, t-test idea (Atharv). |
| Required tools | Same venv. Streamlit and `requests` are already in `pyproject.toml` (Week 3). **Optional only:** Ollama (free, open source) with `qwen2.5:1.5b` (Apache-2.0 licence). Nothing in the project requires it; with Ollama absent, the template note is used. |
| Prerequisites from previous weeks | Week 6 merged: `pipeline.train_and_evaluate`, `evaluate.py`, `metrics.py`, `guards.py`, transition validation, `feedback.py`, Week-6 results note. |
| Approximate workload | 11 h per member. |
| Technical dependencies | Vedant's `reflect()` merged by **Day 3** (pipeline calls it). Brahmanand's `run_pipeline` merged by **Day 4** (Train page calls it). Somesh's `common.py` + `app.py` merged by **Day 3**. |
| Definition of Done | All tests pass in CI (`test_cli.py`, `test_pipeline_e2e.py` W7, `test_reflection.py`, `test_stats.py`, `test_ablation.py`, `tests/ui/test_pages.py`); dashboard demo on 2 laptops; the project runs fully **with Ollama switched off**; ablation pilot numbers recorded as produced. |

**Stack note (flagged addition):** `src/sla/reflection/reflect.py` is a small module **added to the master plan's file list** — it joins facts → LLM/template → grounding → store into one function so the CLI, pipeline and UI do not repeat that logic. No new library is added.

**In simple words:** until now everything worked from the terminal and only the team could use it. This week anyone can click "Start training", watch the result, and read a short explanation that is checked against the real numbers.

---

## SECTION 2 — WHAT WE ARE BUILDING THIS WEEK

1. **Modules:** `pipeline.run_pipeline` + CLI `pipeline / reflect / dashboard` (Brahmanand) · `evaluation/stats.py`, `evaluation/ablation.py`, `scripts/run_ablation.py` (Atharv) · `reflection/facts.py`, `grounding.py`, `fallback.py`, `llm_client.py`, `reflect.py` (Vedant) · `ui/common.py`, `ui/app.py`, `ui/pages/1_Train.py`, `2_Results.py`, `3_Reflection.py` (Somesh).
2. **Why:** examiners judge a working, demonstrable system. The reflection note answers "what did the agent learn?" in plain words; statistics and ablation answer "is the improvement real, and why?".
3. **Connection:** the UI only calls `run_pipeline`, `EpisodeStore` queries, `plots`, `reflect` and `feedback` — it contains no RL logic. Week 8 tests and measures this complete system.
4. **If missing:** no demo, no explanation feature, no evidence that replay/target network matter.
5. **Final output:**
   ```text
   $ sla pipeline --config configs/frozenlake_q.yaml --seeds 0 1
   [seed 0] frozenlake_q_learning_s0_...: final mean x.xx ± x.xx
     plot: runs/frozenlake_q_learning_s0_.../plots/learning_curve.png
     plot: runs/frozenlake_q_learning_s0_.../plots/eval_curve.png
     note (template): <a sentence built only from the run's facts>
   [seed 1] ...
   $ sla dashboard        # opens http://localhost:8501 in the browser
   ```
   (`x.xx` = whatever your run prints.)

**Analogy:** the pipeline is the kitchen, the dashboard is the restaurant menu and the reflection note is the waiter explaining the dish — and the grounding check makes sure the waiter never makes up ingredients.

### How a note is produced
```text
compute_facts(store, run_id)  ──► facts dict (numbers from the DB only)
      │
      ├─ use_llm and Ollama running? ──► LLM text ──► check_grounding(text, facts)
      │                                                 ├─ passed  → store + show (source "llm")
      │                                                 └─ failed  → store as rejected, fall back ↓
      └─ otherwise ───────────────────► template_note(facts) → check_grounding → store + show (source "template")
```

---

## SECTION 3 — DAILY EXECUTION PLAN

### Day 1 — Interfaces and Streamlit kick-off (1.5 h)
- **Daily objective:** agree the `reflect()` and `run_pipeline()` signatures; Somesh's first Streamlit page runs.
- **Assigned members:** all; Brahmanand integration captain; Atharv runs a 45-min Streamlit pairing session with Somesh.
- **Individual tasks:** Vedant: `compute_facts` + `extract_numbers` (SLA-07-VB-1 steps 1–2). Atharv: `stats.py` (SLA-07-AG-1 steps 1–2) and the pairing session. Brahmanand: `PipelineResult` + `run_pipeline` skeleton (SLA-07-BM-1 step 1). Somesh: Streamlit lesson (Section 5.4) and `common.py`.
- **Required commands:**
  ```bash
  git checkout main && git pull && pip install -e ".[dev]" && pytest -q
  streamlit hello                     # checks Streamlit works (Ctrl+C to stop)
  ```
- **Expected files:** `src/sla/reflection/facts.py`, `src/sla/evaluation/stats.py`, `src/sla/ui/common.py` (drafts).
- **Expected output:** signatures written in issue #71: `run_pipeline(cfg, db_path, final_eval_episodes, use_llm) -> PipelineResult`; `reflect(store, run_id, use_llm=False, client=None) -> ReflectionResult`.
- **GitHub activity:** issues #71–#78.
- **Completion checklist:** - [ ] signatures agreed · - [ ] Streamlit runs on Somesh's laptop

### Day 2 — Grounding, statistics, home page (1.5 h)
- **Daily objective:** notes can be checked; statistics tested; home page lists runs.
- **Assigned members:** Vedant (grounding + template), Atharv (stats tests → PR #73), Somesh (`app.py`), Brahmanand (reviews #73).
- **Individual tasks:** SLA-07-VB-1 steps 3–5 · SLA-07-AG-1 steps 3–4 · SLA-07-SB-1 steps 1–4.
- **Required commands:** `pytest tests/unit/test_stats.py -v` · `streamlit run src/sla/ui/app.py`
- **Completion checklist:** - [ ] stats merged · - [ ] home page shows runs from `runs/episodes.db`

### Day 3 — Reflection merged; ablation (1.5 h)
- **Daily objective:** `reflect()` on `main`; ablation code ready.
- **Assigned members:** Vedant (LLM client + `reflect` + tests → PR #75/#76), Atharv (ablation), Somesh (common + app PR #77 merged), Brahmanand (reviews #76).
- **Individual tasks:** SLA-07-VB-1 steps 6–8 · SLA-07-AG-2 steps 1–3 · SLA-07-SB-1 step 5.
- **Required commands:** `pytest tests/unit/test_reflection.py tests/unit/test_ablation.py -v`
- **GitHub activity:** #75, #76, #77 merged.
- **Completion checklist:** - [ ] reflection merged (works with Ollama off)

### Day 4 — Pipeline and CLI (1.5 h)
- **Daily objective:** `sla pipeline`, `sla reflect`, `sla dashboard` work.
- **Assigned members:** Brahmanand (pipeline + CLI + tests), Somesh (Train page), Atharv (reviews), Vedant (optional: try Ollama on his laptop).
- **Individual tasks:** SLA-07-BM-1 steps 2–6 · SLA-07-SB-2 steps 1–3.
- **Required commands:**
  ```bash
  pytest tests/integration/test_pipeline_e2e.py tests/integration/test_cli.py -v
  sla pipeline --config configs/frozenlake_q.yaml --seeds 0
  sla reflect --run-id <run_id>
  ```
- **GitHub activity:** #71 merged (#72 follows on Day 6).
- **Completion checklist:** - [ ] pipeline merged · - [ ] CLI tests green

### Day 5 — Results and Reflection pages; ablation pilot (1.5 h)
- **Daily objective:** all three UI pages work; ablation pilot runs.
- **Assigned members:** Somesh (pages + UI tests), Atharv (pilot: `--seeds 0 1 --episodes 150`), Vedant (reviews Somesh), Brahmanand (end-to-end check).
- **Individual tasks:** SLA-07-SB-2 steps 4–7 · SLA-07-AG-2 steps 4–5.
- **Required commands:**
  ```bash
  python scripts/run_ablation.py --config configs/cartpole_dqn.yaml --seeds 0 1 --episodes 150
  pytest tests/ui -v
  sla dashboard
  ```
- **Completion checklist:** - [ ] 3 pages work · - [ ] pilot CSV produced

### Day 6 — Full-system integration test (2.5 h)
- **Daily objective:** whole system works on a fresh clone, with Ollama **off**.
- **Assigned members:** all.
- **Individual tasks:** each member: fresh clone in a new folder → install → `pytest` → `sla pipeline --config configs/frozenlake_q.yaml --seeds 0 1` → `sla dashboard` → train from the UI → rate the note on the Reflection page. Record every problem as a GitHub issue labelled `bug` (they are Week-8 work if not fixed today).
- **Required commands:**
  ```bash
  git clone https://github.com/<org>/self-learning-ai-agent.git sla-fresh && cd sla-fresh
  python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
  pip install torch --index-url https://download.pytorch.org/whl/cpu
  pip install -e ".[dev]" && pytest
  ```
- **Completion checklist:** - [ ] fresh-clone test done on 4 laptops · - [ ] bugs filed

### Day 7 — Weekly review (1 h)
- **Daily objective:** full demo from the dashboard; Section 12 agenda.
- **Completion checklist:** - [ ] Section 13 complete

---

## SECTION 4 — INDIVIDUAL MEMBER TASKS

### Brahmanand Mathpati

**Task ID:** SLA-07-BM-1
**Task Title:** Full pipeline and CLI `pipeline / reflect / dashboard`
**Priority:** P1
**Estimated Duration:** 7 h (learning 1, coding 3, testing 1, integration 2 — integration captain)
**Dependencies:** `reflect()` (#76), `plots.py` (W5), `train_and_evaluate` (W6)
**Assigned Member:** Brahmanand Mathpati

1. **What:** append `# region W7: full pipeline` to `pipeline.py` (`PipelineResult`, `run_pipeline`); append `# region W7` to `cli.py` (`cmd_pipeline`, `cmd_reflect`, `cmd_dashboard`, `add_w7_parsers`).
2. **Why:** one call that produces everything a run needs (log file, metrics, plots, note) — used by the CLI and the Train page.
3. **Files:** modify `pipeline.py`, `cli.py`, `tests/integration/test_pipeline_e2e.py` (W7 region); create `tests/integration/test_cli.py`.
4. **Functions/classes:** as item 1 (Section 5.1).
5. **Inputs:** config, DB path, final test episodes, `use_llm` flag; CLI `--seeds`, `--llm`, `--run-id`.
6. **Outputs:** `PipelineResult(train, final_eval, plots, note_text, note_source)`; `runs/<id>/run.log`, `plots/learning_curve.png`, `plots/eval_curve.png`, `metrics.json`.
7. **Steps:**
   1. Add the new imports to `pipeline.py` (`dataclass`, `field`, `make_run_id`) and write `PipelineResult`.
   2. Write `run_pipeline`: make the run id first so the log file goes into the run folder; call `train_and_evaluate`; draw plots; call `reflect`.
   3. Add `import subprocess` to `cli.py` and the W7 region.
   4. Write the W7 e2e test (template note must pass grounding) and `test_cli.py` (train → evaluate → prune; bad config; missing checkpoint).
   5. Run all tests.
   6. PR #71 (pipeline, CLI and both test files).
8. **Commands:**
   ```bash
   git checkout -b feat/brahmanand-71-full-pipeline
   pytest tests/integration -v
   sla pipeline --config configs/frozenlake_q.yaml --seeds 0 1
   git add src/sla/pipeline.py src/sla/cli.py tests/integration/test_pipeline_e2e.py tests/integration/test_cli.py
   git commit -m "feat(pipeline): add full pipeline and pipeline/reflect/dashboard commands"
   git push -u origin feat/brahmanand-71-full-pipeline
   ```
9. **Tests:** `test_full_pipeline_with_template_note`; `test_train_evaluate_and_prune`; `test_bad_config_gives_clear_error`; `test_missing_checkpoint_error`.
10. **Expected result:** `2 passed` in e2e, `3 passed` in `test_cli.py`.
11. **Common errors:** `run.log` empty → `setup_logging` called after training starts; `sla dashboard` "No module named streamlit" → venv not active; plots missing → store had no episodes (wrong `db_path`).
12. **Branch:** `feat/brahmanand-71-full-pipeline`
13. **Commit:** `feat(pipeline): add full pipeline and pipeline/reflect/dashboard commands`
14. **PR title:** `feat: full pipeline + CLI (SLA-07-BM-1)`
15. **Acceptance:** fresh-clone Day-6 test passes on 4 laptops; reviewer: Atharv.

**Task ID:** SLA-07-BM-2
**Task Title:** Integration captain: fresh-clone system test, bug triage and README update
**Priority:** P1
**Estimated Duration:** 4 h (integration 3, docs 1)
**Dependencies:** SLA-07-BM-1; all Week-7 PRs merged
**Assigned Member:** Brahmanand Mathpati

1. **What:** lead the Day-6 fresh-clone test on all 4 laptops; turn every problem into a GitHub issue labelled `bug` with steps to reproduce and an owner; add `sla pipeline` and `sla dashboard` to the README command table.
2. **Why:** the integration captain makes sure the parts work *together* on every laptop, not just on the author's.
3. **Files:** `README.md` (command table); GitHub issues.
4. **Functions:** none new — exercises `run_pipeline`, the CLI and the dashboard.
5. **Inputs:** Day-6 test notes from all members.
6. **Outputs:** list of `bug` issues (each with owner and priority) linked in the Week-7 review; updated README.
7. **Steps:** prepare the Day-6 checklist (Section 3, Day 6) → run it with each member → file issues the same day → fix the ones in your own modules → update README → PR.
8. **Commands:**
   ```bash
   git checkout -b docs/brahmanand-72-readme-pipeline
   sla --help                      # copy the exact command names into the README table
   git add README.md
   git commit -m "docs: add pipeline and dashboard commands to README"
   git push -u origin docs/brahmanand-72-readme-pipeline
   ```
9. **Tests:** every README command runs on a fresh clone.
10. **Expected result:** all 4 laptops tested; every problem has an issue and an owner.
11. **Common errors:** fixing other members' bugs yourself — assign them to the module owner (Atharv guides; nobody does everyone's work).
12. **Branch:** `docs/brahmanand-72-readme-pipeline`
13. **Commit:** `docs: add pipeline and dashboard commands to README`
14. **PR title:** `docs: README pipeline/dashboard (SLA-07-BM-2)`
15. **Acceptance:** bug list reviewed at the Day-7 meeting; reviewer: Somesh.

### Atharv Gundale

**Task ID:** SLA-07-AG-1
**Task Title:** Statistics: Welch t-test and bootstrap confidence intervals
**Priority:** P1
**Estimated Duration:** 4 h (learning 1, coding 2, testing 1)
**Dependencies:** SciPy (already a dependency)
**Assigned Member:** Atharv Gundale

1. **What:** `src/sla/evaluation/stats.py` — `bootstrap_ci`, `bootstrap_diff_ci`, `welch_t_test`, `compare_groups`.
2. **Why:** with only 5 seeds, "A is better than B" needs a confidence interval and a test, not just two means.
3. **Files:** `evaluation/stats.py`, `tests/unit/test_stats.py`.
4. **Functions:** as item 1 (Section 5.2).
5. **Inputs:** two lists of per-seed final scores.
6. **Outputs:** `(low, high)` intervals; `(t, p)`; a dict with means, difference CI, p-value.
7. **Steps:** learn (Section 5.2 note) → write functions → 5 tests (Welch matches SciPy, CI contains mean, clear gap excludes 0, keys, too few values) → PR #73.
8. **Commands:**
   ```bash
   git checkout -b feat/atharv-73-stats
   pytest tests/unit/test_stats.py -v
   git add src/sla/evaluation/stats.py tests/unit/test_stats.py
   git commit -m "feat(evaluation): add bootstrap CIs and Welch t-test"
   git push -u origin feat/atharv-73-stats
   ```
9. **Tests:** 5 tests above.
10. **Expected result:** `5 passed`.
11. **Common errors:** `nan` p-value → fewer than 2 values per group (`compare_groups` and the bootstrap functions raise a clear `ValueError` instead); non-repeatable CI → pass `seed` to the bootstrap RNG.
12. **Branch:** `feat/atharv-73-stats`
13. **Commit:** `feat(evaluation): add bootstrap CIs and Welch t-test`
14. **PR title:** `feat: statistics helpers (SLA-07-AG-1)`
15. **Acceptance:** tests pass; reviewer: Brahmanand.

**Task ID:** SLA-07-AG-2
**Task Title:** Ablation study code and pilot; Streamlit mentoring
**Priority:** P1
**Estimated Duration:** 7 h (coding 2, testing 1, integration 3 [pairing with Somesh, pilot], docs 1)
**Dependencies:** SLA-07-AG-1; `train_and_evaluate` (W6); DQN flags `replay_enabled`, `target_net_enabled` (W4)
**Assigned Member:** Atharv Gundale

1. **What:** `src/sla/evaluation/ablation.py` (`VARIANTS`, `make_variant_config`, `run_ablation`), `scripts/run_ablation.py`; a 2-seed pilot; two 45-min pairing sessions with Somesh.
2. **Why:** an ablation removes one component at a time to show its contribution — the strongest evidence for *why* the agent learns.
3. **Files:** `evaluation/ablation.py`, `scripts/run_ablation.py`, `tests/unit/test_ablation.py`.
4. **Functions:** as item 1.
5. **Inputs:** base DQN config, seeds, variants.
6. **Outputs:** `results/ablation/ablation.csv` (one row per variant × seed) and `summary.csv` (full vs each variant with CI and p-value).
7. **Steps:**
   1. `make_variant_config` changes **only** its flag (test proves it); unknown variant / non-DQN agent rejected.
   2. `run_ablation` uses `pipeline.train_and_evaluate`, so every variant is evaluated exactly like normal runs.
   3. Script + tests → PR #74.
   4. Pilot with `--seeds 0 1 --episodes 150` (pilot only — numbers are **not** results; full 5-seed run is Week 8).
   5. Pairing: help Somesh with `st.form`, `st.session_state` questions and AppTest — guide, do not write his pages.
8. **Commands:**
   ```bash
   git checkout -b feat/atharv-74-ablation
   pytest tests/unit/test_ablation.py -v
   python scripts/run_ablation.py --config configs/cartpole_dqn.yaml --seeds 0 1 --episodes 150
   git add src/sla/evaluation/ablation.py scripts/run_ablation.py tests/unit/test_ablation.py
   git commit -m "feat(evaluation): add DQN ablation (no replay, no target network)"
   git push -u origin feat/atharv-74-ablation
   ```
9. **Tests:** variants change only their flag; unknown variant and wrong agent rejected.
10. **Expected result:** `2 passed`; pilot CSV printed (do **not** commit pilot CSVs).
11. **Common errors:** variants share one config object → use `copy.deepcopy` (already in the code); pilot too slow → fewer episodes for the pilot only.
12. **Branch:** `feat/atharv-74-ablation`
13. **Commit:** `feat(evaluation): add DQN ablation (no replay, no target network)`
14. **PR title:** `feat: ablation study (SLA-07-AG-2)`
15. **Acceptance:** tests pass; pilot ran; Somesh's UI PRs merged with Atharv's guidance; reviewer: Vedant.

### Vedant Biradar

**Task ID:** SLA-07-VB-1
**Task Title:** Grounded reflection (facts, grounding check, template, optional local LLM)
**Priority:** P1
**Estimated Duration:** 11 h (learning 1, coding 5, testing 2, integration 2, docs 1)
**Dependencies:** store `reflections` and `evals` tables (W5/W6)
**Assigned Member:** Vedant Biradar

1. **What:** `reflection/facts.py` (`compute_facts`), `grounding.py` (`extract_numbers`, `fact_numbers`, `check_grounding`, `GroundingReport`), `fallback.py` (`template_note`), `llm_client.py` (`OllamaClient`, `build_prompt`), `reflect.py` (`Note`, `ReflectionResult`, `reflect`).
2. **Why:** the "reflection" feature explains what the agent learned. Small LLMs can invent numbers, so every number in a note must appear in the facts (tolerance 0.01; small integers 0–10 allowed for words like "3 seeds"). The template note always works — the LLM is optional.
3. **Files:** the five modules + `tests/unit/test_reflection.py`.
4. **Functions/classes:** as item 1 (Section 5.3).
5. **Inputs:** store + run id; optional `OllamaClient`.
6. **Outputs:** a stored note (`source` = `llm` or `template`, grounding report) and `ReflectionResult(shown, rejected)`.
7. **Steps:**
   1. `compute_facts`: mean reward per window of 50 episodes, first/last/best window, change, end-reason counts, final ε, best/last evaluation score — numbers only from the DB, rounded to 2 decimals.
   2. `extract_numbers` with one regular expression; `fact_numbers` walks nested dicts/lists.
   3. `check_grounding` returns which numbers are unsupported.
   4. `template_note` builds sentences from facts (it must pass its own grounding check — tested).
   5. Test: a note with a planted wrong number is rejected.
   6. `OllamaClient` (timeout, retries, `temperature: 0`) and `build_prompt`.
   7. `reflect()` — LLM failure or grounding failure ⇒ template; rejected LLM note kept for transparency.
   8. Tests with a `FakeClient` (no network in tests) → PRs #75 (facts/grounding/template) and #76 (client + reflect).
8. **Commands:**
   ```bash
   git checkout -b feat/vedant-75-grounded-reflection
   pytest tests/unit/test_reflection.py -v
   git add src/sla/reflection tests/unit/test_reflection.py
   git commit -m "feat(reflection): add grounded notes with template fallback"
   git push -u origin feat/vedant-75-grounded-reflection
   # optional, on a laptop with Ollama installed:
   ollama pull qwen2.5:1.5b && sla reflect --run-id <run_id> --llm
   ```
9. **Tests:** number extraction; facts; missing run; template grounded; planted wrong number rejected; offline LLM → template; hallucinated LLM note rejected; grounded LLM note accepted.
10. **Expected result:** `8 passed` — with no network and no Ollama.
11. **Common errors:** tests try to reach `localhost:11434` → always inject `FakeClient`; "2026" in a note flagged as unsupported → do not put dates in notes; rounding mismatch (0.83 vs 0.833) → tolerance 0.01 and round facts to 2–3 decimals.
12. **Branches:** `feat/vedant-75-grounded-reflection`, `feat/vedant-76-llm-client`
13. **Commits:** `feat(reflection): add grounded notes with template fallback` · `feat(reflection): add optional local LLM client`
14. **PR titles:** `feat: grounded reflection (SLA-07-VB-1a)` · `feat: optional Ollama client (SLA-07-VB-1b)`
15. **Acceptance:** all tests pass offline; `sla reflect` works with Ollama off; reviewer: Brahmanand.

### Somesh Badwane

**Task ID:** SLA-07-SB-1
**Task Title:** Streamlit app shell: shared settings and home page
**Priority:** P1
**Estimated Duration:** 4 h (learning 1, coding 2, review 1)
**Dependencies:** store (W5); Streamlit lesson (Section 5.4)
**Assigned Member:** Somesh Badwane

**0. Learn first (Section 5.4, ~1 h, with Atharv):** a Streamlit script runs **top to bottom on every click**; `st.title`, `st.markdown`, `st.selectbox`, `st.form` + `st.form_submit_button`, `st.dataframe`, `st.info/st.error`, `st.stop()`; multipage apps (files in `pages/` appear in the sidebar); environment variables with `os.environ.get`.

1. **What:** `src/sla/ui/common.py` (`REPO_ROOT`, `CONFIG_DIR`, `DB_PATH`, `CONFIGS`, `agents_for`, `config_path`, `get_store`) and `src/sla/ui/app.py` (home page).
2. **Why:** every page needs the same database path and config list; keeping them in one file means one change fixes all pages. `SLA_DB` lets tests use a temporary database.
3. **Files:** create `ui/common.py`, `ui/app.py`.
4. **Functions:** as item 1.
5. **Inputs:** `SLA_DB` environment variable (optional).
6. **Outputs:** home page: project description + table of runs (or "No runs yet").
7. **Steps:** lesson → `common.py` → `app.py` → run `streamlit run src/sla/ui/app.py` → check with and without runs → PR #77 (reviewer Vedant).
8. **Commands:**
   ```bash
   git checkout main && git pull
   git checkout -b feat/somesh-77-ui-shell
   streamlit run src/sla/ui/app.py
   ruff check src/sla/ui
   git add src/sla/ui/common.py src/sla/ui/app.py
   git commit -m "feat(ui): add Streamlit home page and shared settings"
   git push -u origin feat/somesh-77-ui-shell
   ```
9. **Tests:** `test_home_page_without_runs` (written in SLA-07-SB-2).
10. **Expected result:** home page shows runs from `runs/episodes.db`.
11. **Common errors:** page blank → error shown in the terminal, read it; `ModuleNotFoundError: sla` → run from the repo folder with the venv active; wrong database → print `DB_PATH`.
12. **Branch:** `feat/somesh-77-ui-shell`
13. **Commit:** `feat(ui): add Streamlit home page and shared settings`
14. **PR title:** `feat: Streamlit shell (SLA-07-SB-1)`
15. **Acceptance:** runs list visible; reviewer: Vedant.

**Task ID:** SLA-07-SB-2
**Task Title:** Train, Results and Reflection pages + UI tests
**Priority:** P1
**Estimated Duration:** 7 h (learning 0.5, coding 4, testing 2, docs 0.5)
**Dependencies:** SLA-07-SB-1; `run_pipeline` (#71, Day 4); your Week-4 validators; your Week-6 `feedback.py`; your Week-5 plots
**Assigned Member:** Somesh Badwane

1. **What:** `ui/pages/1_Train.py`, `ui/pages/2_Results.py`, `ui/pages/3_Reflection.py`, `tests/ui/test_pages.py`.
2. **Why:** this is the part of the project examiners will click. It reuses **your own** earlier code: validators (W4), plots (W5), feedback (W6).
3. **Files:** as item 1.
4. **Functions:** pages are scripts (no functions); tests use Streamlit's `AppTest`.
5. **Inputs:** environment, agent, episodes, seed, optional LLM checkbox; run selection; rating form.
6. **Outputs:** training result with plots and note; learning curve + evaluation + end-reason chart; note display + rating saved via `save_rating`.
7. **Steps:**
   1. Train page: form → validate with `validate_episode_count`, `validate_seeds`, `validate_config` → `run_pipeline(cfg, DB_PATH, final_eval_episodes=50, use_llm=...)` inside `st.spinner` → show metrics, plots, note. Catch `SLAError` and `ImportError` and show friendly `st.error` messages.
   2. Results page: select a run, slider for the rolling window, `st.pyplot(plot_learning_curve(...))`, eval curve and table, end-reason bar chart.
   3. Reflection page: select run → show notes (source + grounding status) → rating form → `save_rating` → `ratings_summary`.
   4. UI tests with `AppTest` and a temporary `SLA_DB` (Section 5.4).
   5. PR #78 (reviewer Vedant; Atharv pairs if stuck).
8. **Commands:**
   ```bash
   git checkout -b feat/somesh-78-ui-pages
   pytest tests/ui -v
   sla dashboard
   git add src/sla/ui/pages tests/ui/test_pages.py
   git commit -m "feat(ui): add train, results and reflection pages"
   git push -u origin feat/somesh-78-ui-pages
   ```
9. **Tests:** home page without runs; results page without runs; train page renders the form with default 300 episodes.
10. **Expected result:** `3 passed` (skipped automatically if Streamlit is not installed).
11. **Common errors:** training restarts on every click → keep the training call inside `if submitted:`; `DuplicateWidgetID` → give each widget a unique label/key; long CartPole run "freezes" the page → expected (spinner shows); suggest FrozenLake for live demos; `AppTest` uses your real DB → the `isolated_db` fixture must set `SLA_DB` and reload `common`.
12. **Branch:** `feat/somesh-78-ui-pages`
13. **Commit:** `feat(ui): add train, results and reflection pages`
14. **PR title:** `feat: dashboard pages (SLA-07-SB-2)`
15. **Acceptance:** 3 UI tests pass; a teammate who did not write the pages can train and rate a note without help; reviewer: Vedant.

**How to make the PR:** as before; label `week-7`; attach two screenshots (Train result, Reflection page) to the PR description.

**Independent practice exercise:** in a scratch file `scratch_page.py` (not committed), make a Streamlit page with a number input "episodes" and a button that shows `st.success` when the number is between 1 and 1000 and `st.error` otherwise, using **your** `validate_episode_count` inside `try/except ValidationError`.

---

## SECTION 5 — COMPLETE TECHNICAL IMPLEMENTATION

### 5.1 Pipeline and CLI (Brahmanand)

`src/sla/pipeline.py` — **complete file after Week 7** (W6 region unchanged; new imports `dataclass`, `field`, `make_run_id`; new W7 region at the end):
```python
"""One-call pipelines used by the CLI, scripts and the Streamlit UI (owner: Brahmanand).

Week 6: default_callbacks + train_and_evaluate.
Week 7: run_pipeline (adds logging to file, plots, metrics.json and reflection).
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from sla.agent.checkpoint import CheckpointCallback, latest_checkpoint, load_checkpoint
from sla.agent.runner import Callback, RunResult, make_run_id, run_training
from sla.evaluation.evaluate import TEST_SEED_BASE, EvalResult, PeriodicEvalCallback, evaluate_agent
from sla.learning.guards import DivergenceGuard, RegressionMonitor
from sla.memory.episode_store import EpisodeStore, StoreCallback
from sla.utils.config import RunConfig
from sla.utils.io_helpers import write_json
from sla.utils.validation import TransitionValidationCallback


# region W6: train and evaluate
def git_sha() -> str | None:
    """Short commit id of the code that produced a result (None outside a git repo)."""
    try:
        out = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True,
                             timeout=5, check=True)
        return out.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def default_callbacks(cfg: RunConfig, store: EpisodeStore, validate: bool = True) -> list[Callback]:
    """Standard plug-ins, in the order they must run."""
    callbacks: list[Callback] = [StoreCallback(store, git_sha())]
    if validate:
        callbacks.append(TransitionValidationCallback(cfg.env_name))
    callbacks += [
        CheckpointCallback(cfg.checkpoint_every),
        PeriodicEvalCallback(cfg.eval_every, cfg.eval_episodes, store),
        RegressionMonitor(),   # must come after PeriodicEvalCallback
        DivergenceGuard(),
    ]
    return callbacks


def final_evaluation(run_dir: Path, cfg: RunConfig, n_episodes: int = 100) -> tuple[EvalResult, str]:
    """Evaluate the best checkpoint (or the latest one) on the held-out test seeds."""
    best = Path(run_dir) / "checkpoints" / "best"
    folder = best if (best / "checkpoint.json").exists() else latest_checkpoint(run_dir)
    agent, _ = load_checkpoint(folder)
    result = evaluate_agent(agent, cfg.env_name, cfg.env_kwargs, n_episodes, seed_base=TEST_SEED_BASE)
    return result, folder.name


def train_and_evaluate(cfg: RunConfig, store: EpisodeStore, final_eval_episodes: int = 100,
                       run_id: str | None = None, run_dir: Path | None = None) -> tuple[RunResult, EvalResult]:
    """Train with the default callbacks, then run the final test evaluation and save metrics.json."""
    train = run_training(cfg, default_callbacks(cfg, store), run_id=run_id, run_dir=run_dir)
    final, used = final_evaluation(train.run_dir, cfg, final_eval_episodes)
    write_json(train.run_dir / "metrics.json", {
        "run_id": train.run_id, "env": cfg.env_name, "agent": cfg.agent, "seed": cfg.seed,
        "episodes_completed": train.episodes_completed, "stopped_reason": train.stopped_reason,
        "final_eval": {**final.to_dict(), "checkpoint": used, "seed_base": TEST_SEED_BASE},
        "git_sha": git_sha(),
    })
    return train, final
# endregion


# region W7: full pipeline
@dataclass
class PipelineResult:
    train: RunResult
    final_eval: EvalResult
    plots: list[Path] = field(default_factory=list)
    note_text: str | None = None
    note_source: str | None = None


def run_pipeline(cfg: RunConfig, db_path: str | Path = "runs/episodes.db", final_eval_episodes: int = 100,
                 use_llm: bool = False) -> PipelineResult:
    """Train -> evaluate -> plots -> reflection note. Used by `sla pipeline` and the UI."""
    from sla.evaluation.plots import plot_eval_curve, plot_learning_curve
    from sla.reflection.reflect import reflect
    from sla.utils.logging_setup import setup_logging

    run_id = make_run_id(cfg)
    run_dir = Path(cfg.run_root) / run_id
    setup_logging(run_id, run_dir / "run.log")
    store = EpisodeStore(db_path)
    train, final = train_and_evaluate(cfg, store, final_eval_episodes, run_id=run_id, run_dir=run_dir)

    plots: list[Path] = []
    episodes = store.query_episodes(run_id)
    if not episodes.empty:
        path = run_dir / "plots" / "learning_curve.png"
        plot_learning_curve(episodes, title=f"{cfg.agent} on {cfg.env_name} (seed {cfg.seed})", out_path=path)
        plots.append(path)
    evals = store.query_evals(run_id)
    if not evals.empty:
        path = run_dir / "plots" / "eval_curve.png"
        plot_eval_curve(evals, out_path=path)
        plots.append(path)

    result = reflect(store, run_id, use_llm=use_llm)
    return PipelineResult(train, final, plots, result.shown.text, result.shown.source)
# endregion
```

`src/sla/cli.py` — the new W7 region (also add `import subprocess` to the imports at the top):
```python
def cmd_pipeline(args: argparse.Namespace) -> int:
    from sla.pipeline import run_pipeline
    from sla.utils.validation import validate_seeds
    base = _load_cfg(args)
    for seed in validate_seeds(args.seeds or [base.seed]):
        base.seed = seed
        res = run_pipeline(base, args.db, args.eval_episodes, use_llm=args.llm)
        print(f"[seed {seed}] {res.train.run_id}: final mean {res.final_eval.mean_return:.2f} "
              f"± {res.final_eval.std_return:.2f}")
        for plot in res.plots:
            print(f"  plot: {plot}")
        print(f"  note ({res.note_source}): {res.note_text}")
    return 0


def cmd_reflect(args: argparse.Namespace) -> int:
    from sla.memory.episode_store import EpisodeStore
    from sla.reflection.reflect import reflect
    result = reflect(EpisodeStore(args.db), args.run_id, use_llm=args.llm)
    if result.rejected:
        print(f"Rejected LLM note (unsupported numbers {result.rejected.report.unsupported}):")
        print(f"  {result.rejected.text}")
    print(f"Note #{result.shown.note_id} ({result.shown.source}): {result.shown.text}")
    return 0


def cmd_dashboard(args: argparse.Namespace) -> int:
    app = Path(__file__).resolve().parent / "ui" / "app.py"
    return subprocess.call([sys.executable, "-m", "streamlit", "run", str(app)])


def add_w7_parsers(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("pipeline", help="train -> evaluate -> plots -> reflection, for one or more seeds")
    p.add_argument("--config", required=True)
    p.add_argument("--seeds", type=int, nargs="+", help="e.g. --seeds 0 1 2 3 4")
    p.add_argument("--episodes", type=int)
    p.add_argument("--db", default=DEFAULT_DB)
    p.add_argument("--eval-episodes", type=int, default=100)
    p.add_argument("--llm", action="store_true", help="try the local Ollama model for the note")
    p.set_defaults(func=cmd_pipeline)

    p = sub.add_parser("reflect", help="write a grounded explanation note for a run")
    p.add_argument("--run-id", required=True)
    p.add_argument("--db", default=DEFAULT_DB)
    p.add_argument("--llm", action="store_true")
    p.set_defaults(func=cmd_reflect)

    p = sub.add_parser("dashboard", help="open the Streamlit dashboard")
    p.set_defaults(func=cmd_dashboard)


PARSER_BUILDERS.append(add_w7_parsers)
```

`src/sla/cli.py` — **complete final file** for checking (Weeks 5 + 6 + 7):
```python
"""Command-line interface: `sla <command>` (owner: Brahmanand).

Week 5: train, resume, prune.   Week 6: evaluate (and train now evaluates).
Week 7: pipeline, reflect, dashboard.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

from sla.utils.errors import SLAError

PARSER_BUILDERS: list[Callable[[argparse._SubParsersAction], None]] = []
DEFAULT_DB = "runs/episodes.db"


# region W5: train, resume, prune
def _load_cfg(args: argparse.Namespace):
    from sla.utils.config import load_config, validate_config
    cfg = load_config(args.config)
    if getattr(args, "seed", None) is not None:
        cfg.seed = args.seed
    if getattr(args, "episodes", None) is not None:
        cfg.episodes = args.episodes
    return validate_config(cfg)


def _callbacks(cfg, store):
    """Week 6 version: all standard callbacks (store, validation, checkpoints, evaluation, guards)."""
    from sla.pipeline import default_callbacks
    return default_callbacks(cfg, store)


def cmd_train(args: argparse.Namespace) -> int:
    """Week 6 version: train with all callbacks, then evaluate on the test seeds."""
    from sla.memory.episode_store import EpisodeStore
    from sla.pipeline import train_and_evaluate
    from sla.utils.logging_setup import setup_logging
    cfg = _load_cfg(args)
    setup_logging()
    train, final = train_and_evaluate(cfg, EpisodeStore(args.db), final_eval_episodes=args.eval_episodes)
    print(f"Run id: {train.run_id}  ({train.stopped_reason}, {train.episodes_completed} episodes)")
    print(f"Final evaluation: mean {final.mean_return:.2f} ± {final.std_return:.2f}, "
          f"success {final.success_rate:.0%} over {final.n_episodes} test episodes")
    print(f"Folder: {train.run_dir}")
    return 0


def cmd_resume(args: argparse.Namespace) -> int:
    from sla.agent.checkpoint import resume_training
    from sla.memory.episode_store import EpisodeStore
    from sla.utils.config import load_config
    from sla.utils.logging_setup import setup_logging
    run_dir = Path(args.run)
    setup_logging(run_dir.name, run_dir / "run.log")
    cfg = load_config(run_dir / "config.yaml")
    result = resume_training(run_dir, _callbacks(cfg, EpisodeStore(args.db)))
    print(f"Resumed {result.run_id}: now {result.episodes_completed} episodes ({result.stopped_reason})")
    return 0


def cmd_prune(args: argparse.Namespace) -> int:
    from sla.memory.episode_store import EpisodeStore
    from sla.memory.retention import prune_runs
    runs = prune_runs(EpisodeStore(args.db), args.older_than, args.run_root, dry_run=not args.yes)
    verb = "Deleted" if args.yes else "Would delete (dry run; add --yes to delete)"
    print(f"{verb} {len(runs)} run(s): {', '.join(runs) if runs else '-'}")
    return 0


def add_w5_parsers(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("train", help="train an agent from a YAML config")
    p.add_argument("--config", required=True, help="path to a YAML config, e.g. configs/frozenlake_q.yaml")
    p.add_argument("--seed", type=int, help="override the seed in the config")
    p.add_argument("--episodes", type=int, help="override the number of episodes")
    p.add_argument("--db", default=DEFAULT_DB, help="SQLite episode store")
    p.add_argument("--eval-episodes", type=int, default=100, help="final test-evaluation episodes")
    p.set_defaults(func=cmd_train)

    p = sub.add_parser("resume", help="continue a run from its latest checkpoint")
    p.add_argument("--run", required=True, help="run folder, e.g. runs/frozenlake_q_learning_s0_...")
    p.add_argument("--db", default=DEFAULT_DB)
    p.set_defaults(func=cmd_resume)

    p = sub.add_parser("prune", help="delete runs older than N days (dry run unless --yes)")
    p.add_argument("--older-than", type=int, required=True, help="age in days")
    p.add_argument("--db", default=DEFAULT_DB)
    p.add_argument("--run-root", default="runs")
    p.add_argument("--yes", action="store_true", help="really delete")
    p.set_defaults(func=cmd_prune)


PARSER_BUILDERS.append(add_w5_parsers)
# endregion


# region W6: evaluate
def cmd_evaluate(args: argparse.Namespace) -> int:
    from sla.evaluation.evaluate import TEST_SEED_BASE, evaluate_checkpoint
    from sla.utils.config import load_config
    folder = Path(args.checkpoint)
    config_path = Path(args.config) if args.config else folder.parent.parent / "config.yaml"
    cfg = load_config(config_path)
    res = evaluate_checkpoint(folder, cfg.env_name, cfg.env_kwargs, args.episodes, seed_base=TEST_SEED_BASE)
    print(f"{folder}: mean {res.mean_return:.2f} ± {res.std_return:.2f}, success {res.success_rate:.0%} "
          f"over {res.n_episodes} episodes (no learning, epsilon = 0)")
    return 0


def add_w6_parsers(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("evaluate", help="evaluate a saved checkpoint without learning")
    p.add_argument("--checkpoint", required=True, help="e.g. runs/<run_id>/checkpoints/best")
    p.add_argument("--config", help="config file (default: the run's config.yaml)")
    p.add_argument("--episodes", type=int, default=100)
    p.set_defaults(func=cmd_evaluate)


PARSER_BUILDERS.append(add_w6_parsers)
# endregion


# region W7: pipeline, reflect, dashboard
def cmd_pipeline(args: argparse.Namespace) -> int:
    from sla.pipeline import run_pipeline
    from sla.utils.validation import validate_seeds
    base = _load_cfg(args)
    for seed in validate_seeds(args.seeds or [base.seed]):
        base.seed = seed
        res = run_pipeline(base, args.db, args.eval_episodes, use_llm=args.llm)
        print(f"[seed {seed}] {res.train.run_id}: final mean {res.final_eval.mean_return:.2f} "
              f"± {res.final_eval.std_return:.2f}")
        for plot in res.plots:
            print(f"  plot: {plot}")
        print(f"  note ({res.note_source}): {res.note_text}")
    return 0


def cmd_reflect(args: argparse.Namespace) -> int:
    from sla.memory.episode_store import EpisodeStore
    from sla.reflection.reflect import reflect
    result = reflect(EpisodeStore(args.db), args.run_id, use_llm=args.llm)
    if result.rejected:
        print(f"Rejected LLM note (unsupported numbers {result.rejected.report.unsupported}):")
        print(f"  {result.rejected.text}")
    print(f"Note #{result.shown.note_id} ({result.shown.source}): {result.shown.text}")
    return 0


def cmd_dashboard(args: argparse.Namespace) -> int:
    app = Path(__file__).resolve().parent / "ui" / "app.py"
    return subprocess.call([sys.executable, "-m", "streamlit", "run", str(app)])


def add_w7_parsers(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("pipeline", help="train -> evaluate -> plots -> reflection, for one or more seeds")
    p.add_argument("--config", required=True)
    p.add_argument("--seeds", type=int, nargs="+", help="e.g. --seeds 0 1 2 3 4")
    p.add_argument("--episodes", type=int)
    p.add_argument("--db", default=DEFAULT_DB)
    p.add_argument("--eval-episodes", type=int, default=100)
    p.add_argument("--llm", action="store_true", help="try the local Ollama model for the note")
    p.set_defaults(func=cmd_pipeline)

    p = sub.add_parser("reflect", help="write a grounded explanation note for a run")
    p.add_argument("--run-id", required=True)
    p.add_argument("--db", default=DEFAULT_DB)
    p.add_argument("--llm", action="store_true")
    p.set_defaults(func=cmd_reflect)

    p = sub.add_parser("dashboard", help="open the Streamlit dashboard")
    p.set_defaults(func=cmd_dashboard)


PARSER_BUILDERS.append(add_w7_parsers)
# endregion


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sla", description="Self-Learning AI Agent")
    parser.add_argument("--version", action="version", version="sla 0.1.0")
    sub = parser.add_subparsers(dest="command")
    for builder in PARSER_BUILDERS:
        builder(sub)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    try:
        return int(args.func(args) or 0)
    except SLAError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

`tests/integration/test_pipeline_e2e.py` — complete file after Week 7:
```python
import json

from sla.pipeline import train_and_evaluate


# region W6: train and evaluate
def test_train_and_evaluate_writes_metrics(fl_cfg, store):
    train, final = train_and_evaluate(fl_cfg, store, final_eval_episodes=10)
    metrics = json.loads((train.run_dir / "metrics.json").read_text())
    assert metrics["final_eval"]["n_episodes"] == 10
    assert (train.run_dir / "checkpoints" / "best" / "checkpoint.json").exists()
    assert len(store.query_evals(train.run_id)) == fl_cfg.episodes // fl_cfg.eval_every


# endregion


# region W7: full pipeline
def test_full_pipeline_with_template_note(fl_cfg, tmp_path):
    from sla.pipeline import run_pipeline

    res = run_pipeline(fl_cfg, tmp_path / "p.db", final_eval_episodes=10, use_llm=False)
    assert res.note_source == "template" and res.note_text
    assert all(p.exists() for p in res.plots) and len(res.plots) == 2
    assert (res.train.run_dir / "run.log").exists()
# endregion
```

`tests/integration/test_cli.py`
```python
import yaml

from sla.cli import main


def small_config(tmp_path):
    cfg = {"env_name": "FrozenLake-v1", "env_kwargs": {"is_slippery": False}, "agent": "q_learning",
           "episodes": 100, "learning_rate": 0.5, "epsilon_decay_steps": 800, "max_steps_per_episode": 100,
           "eval_every": 50, "eval_episodes": 5, "checkpoint_every": 50, "run_root": str(tmp_path / "runs")}
    path = tmp_path / "cfg.yaml"
    path.write_text(yaml.safe_dump(cfg))
    return path


def test_train_evaluate_and_prune(tmp_path, capsys):
    cfg = small_config(tmp_path)
    db = str(tmp_path / "c.db")
    assert main(["train", "--config", str(cfg), "--db", db, "--eval-episodes", "5"]) == 0
    out = capsys.readouterr().out
    assert "Final evaluation" in out
    run_dir = next((tmp_path / "runs").iterdir())
    assert main(["evaluate", "--checkpoint", str(run_dir / "checkpoints" / "best"), "--episodes", "5"]) == 0
    assert main(["prune", "--older-than", "0", "--db", db, "--run-root", str(tmp_path / "runs")]) == 0
    assert "Would delete" in capsys.readouterr().out


def test_bad_config_gives_clear_error(tmp_path, capsys):
    bad = tmp_path / "bad.yaml"
    bad.write_text("gamma: 5\n")
    assert main(["train", "--config", str(bad)]) == 1
    assert "gamma" in capsys.readouterr().err


def test_missing_checkpoint_error(tmp_path, capsys):
    folder = tmp_path / "run" / "checkpoints" / "x"
    folder.mkdir(parents=True)
    (tmp_path / "run" / "config.yaml").write_text("agent: random\n")
    assert main(["evaluate", "--checkpoint", str(folder)]) == 1
    assert "No checkpoint" in capsys.readouterr().err
```

### 5.2 Statistics and ablation (Atharv)

**Note for the team:** *bootstrap CI* — resample the 5 seed scores with replacement 10,000 times, take the mean each time; the middle 95 % of those means is the interval. *Welch t-test* — compares two means without assuming equal variance; a small p-value (< 0.05) suggests the difference is unlikely to be chance. With 5 seeds both are rough — say so in the report.

`src/sla/evaluation/stats.py`
```python
"""Statistics for comparing agents across seeds (owner: Atharv, Week 7).

With only 5 seeds, report a mean, a 95% bootstrap confidence interval and a
Welch t-test (it does not assume equal variances) — never a single run.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from scipy import stats as sps


def bootstrap_ci(values: Sequence[float], n_boot: int = 10_000, ci: float = 0.95,
                 seed: int = 0) -> tuple[float, float]:
    """Confidence interval for the mean, by resampling with replacement."""
    arr = np.asarray(values, dtype=np.float64)
    if arr.size < 2:
        raise ValueError("Need at least 2 values for a confidence interval")
    rng = np.random.default_rng(seed)
    means = rng.choice(arr, size=(n_boot, arr.size), replace=True).mean(axis=1)
    alpha = (1.0 - ci) / 2.0
    return float(np.quantile(means, alpha)), float(np.quantile(means, 1.0 - alpha))


def bootstrap_diff_ci(a: Sequence[float], b: Sequence[float], n_boot: int = 10_000, ci: float = 0.95,
                      seed: int = 0) -> tuple[float, float]:
    """Confidence interval for mean(a) - mean(b)."""
    x, y = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    if x.size < 2 or y.size < 2:
        raise ValueError("Each group needs at least 2 values")
    rng = np.random.default_rng(seed)
    diffs = (rng.choice(x, size=(n_boot, x.size)).mean(axis=1)
             - rng.choice(y, size=(n_boot, y.size)).mean(axis=1))
    alpha = (1.0 - ci) / 2.0
    return float(np.quantile(diffs, alpha)), float(np.quantile(diffs, 1.0 - alpha))


def welch_t_test(a: Sequence[float], b: Sequence[float]) -> tuple[float, float]:
    """Return (t statistic, two-sided p-value) for mean(a) vs mean(b)."""
    result = sps.ttest_ind(np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64), equal_var=False)
    return float(result.statistic), float(result.pvalue)


def compare_groups(a: Sequence[float], b: Sequence[float], name_a: str = "A", name_b: str = "B") -> dict:
    """Everything needed for one row of the results table."""
    t, p = welch_t_test(a, b)
    low, high = bootstrap_diff_ci(a, b)
    return {f"mean_{name_a}": float(np.mean(a)), f"mean_{name_b}": float(np.mean(b)),
            "diff": float(np.mean(a) - np.mean(b)), "diff_ci_low": low, "diff_ci_high": high,
            "t": t, "p_value": p, "n_a": len(a), "n_b": len(b)}
```

`tests/unit/test_stats.py`
```python
import numpy as np
import pytest
from scipy import stats

from sla.evaluation.stats import bootstrap_ci, bootstrap_diff_ci, compare_groups, welch_t_test


def test_welch_matches_scipy():
    a, b = [10, 12, 11, 13, 12], [5, 6, 7, 5, 6]
    t, p = welch_t_test(a, b)
    ref = stats.ttest_ind(a, b, equal_var=False)
    assert t == pytest.approx(ref.statistic) and p == pytest.approx(ref.pvalue)


def test_bootstrap_ci_contains_mean():
    values = [10, 12, 11, 13, 12]
    low, high = bootstrap_ci(values, n_boot=2000)
    assert low <= np.mean(values) <= high


def test_diff_ci_excludes_zero_for_clear_gap():
    low, high = bootstrap_diff_ci([100, 101, 102, 103], [1, 2, 3, 4], n_boot=2000)
    assert low > 0


def test_compare_groups_keys():
    out = compare_groups([1, 2, 3], [1, 2, 4], "dqn", "random")
    assert {"mean_dqn", "mean_random", "p_value", "diff_ci_low"} <= set(out)


def test_too_few_values():
    with pytest.raises(ValueError):
        bootstrap_ci([1])
```

`src/sla/evaluation/ablation.py`
```python
"""Ablation study: remove one part of the DQN and measure the effect (owner: Atharv, Week 7).

Variants: full DQN, no replay (learn only from the newest transition),
no target network (bootstrap from the online network).
"""

from __future__ import annotations

import copy
from dataclasses import replace
from pathlib import Path
from typing import Any

import pandas as pd

from sla.utils.config import RunConfig, validate_config

VARIANTS: dict[str, dict[str, Any]] = {
    "full": {},
    "no_replay": {"replay_enabled": False},
    "no_target": {"target_net_enabled": False},
}


def make_variant_config(base: RunConfig, variant: str, seed: int) -> RunConfig:
    if variant not in VARIANTS:
        raise ValueError(f"Unknown variant {variant!r}; choose from {sorted(VARIANTS)}")
    if base.agent != "dqn":
        raise ValueError("Ablation is only defined for the DQN agent")
    cfg = copy.deepcopy(base)
    cfg.dqn = replace(cfg.dqn, **VARIANTS[variant])
    cfg.seed = seed
    return validate_config(cfg)


def run_ablation(base: RunConfig, seeds: list[int], db_path: str | Path = "runs/episodes.db",
                 variants: list[str] | None = None, final_eval_episodes: int = 100) -> pd.DataFrame:
    """Train every variant on every seed; return one row per (variant, seed)."""
    from sla.memory.episode_store import EpisodeStore
    from sla.pipeline import train_and_evaluate

    store = EpisodeStore(db_path)
    rows = []
    for variant in variants or list(VARIANTS):
        for seed in seeds:
            cfg = make_variant_config(base, variant, seed)
            train, final = train_and_evaluate(cfg, store, final_eval_episodes=final_eval_episodes)
            rows.append({"variant": variant, "seed": seed, "run_id": train.run_id,
                         "final_mean": final.mean_return, "final_std": final.std_return,
                         "success_rate": final.success_rate})
    return pd.DataFrame(rows)
```

`tests/unit/test_ablation.py`
```python
import pytest

from sla.evaluation.ablation import make_variant_config
from sla.utils.config import config_from_dict


def test_variants_change_only_their_flag():
    base = config_from_dict({"env_name": "CartPole-v1", "agent": "dqn"})
    no_replay = make_variant_config(base, "no_replay", seed=3)
    assert no_replay.dqn.replay_enabled is False and no_replay.dqn.target_net_enabled is True
    assert no_replay.seed == 3 and base.dqn.replay_enabled is True  # base untouched


def test_unknown_variant_and_wrong_agent():
    base = config_from_dict({"env_name": "CartPole-v1", "agent": "dqn"})
    with pytest.raises(ValueError):
        make_variant_config(base, "no_brain", 0)
    with pytest.raises(ValueError):
        make_variant_config(config_from_dict({}), "full", 0)
```

`scripts/run_ablation.py`
```python
"""Ablation study runner (owner: Atharv, Week 7; full 5-seed run in Week 8).

Run:  python scripts/run_ablation.py --config configs/cartpole_dqn.yaml --seeds 0 1 2 3 4
Output: results/ablation/ablation.csv and results/ablation/summary.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from sla.evaluation.ablation import VARIANTS, run_ablation
from sla.evaluation.stats import compare_groups
from sla.utils.config import load_config
from sla.utils.logging_setup import setup_logging


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/cartpole_dqn.yaml")
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    parser.add_argument("--episodes", type=int, help="override episodes (use small values for a pilot)")
    parser.add_argument("--variants", nargs="+", default=list(VARIANTS))
    parser.add_argument("--db", default="runs/episodes.db")
    parser.add_argument("--out-dir", default="results/ablation")
    args = parser.parse_args()

    setup_logging("ablation")
    base = load_config(args.config)
    if args.episodes:
        base.episodes = args.episodes
    df = run_ablation(base, args.seeds, args.db, args.variants)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "ablation.csv", index=False)

    rows = []
    full = df.loc[df["variant"] == "full", "final_mean"].tolist()
    for variant in args.variants:
        if variant == "full":
            continue
        other = df.loc[df["variant"] == variant, "final_mean"].tolist()
        if len(full) >= 2 and len(other) >= 2:
            rows.append({"comparison": f"full vs {variant}", **compare_groups(full, other, "full", variant)})
    summary = pd.DataFrame(rows)
    summary.to_csv(out / "summary.csv", index=False)
    print(df.to_string(index=False))
    if summary.empty:
        print("Need >= 2 seeds per variant for statistics.")
    else:
        print(summary.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
```

### 5.3 Reflection (Vedant)

`src/sla/reflection/facts.py`
```python
"""Compute facts about a run from the store (owner: Vedant, Week 7).

The LLM never computes numbers. It only receives these facts, and the
grounding validator checks that every number it writes appears here.
"""

from __future__ import annotations

from typing import Any

from sla.memory.episode_store import EpisodeStore
from sla.utils.errors import StoreError


def compute_facts(store: EpisodeStore, run_id: str, window: int = 50) -> dict[str, Any]:
    run = store.get_run(run_id)
    if run is None:
        raise StoreError(f"Run {run_id!r} not found")
    episodes = store.query_episodes(run_id)
    if episodes.empty:
        raise StoreError(f"Run {run_id!r} has no episodes yet")
    window = max(1, min(window, len(episodes)))
    windows = []
    for start in range(0, len(episodes), window):
        chunk = episodes.iloc[start:start + window]
        reasons = chunk["end_reason"].value_counts()
        windows.append({
            "episodes": f"{start + 1}-{start + len(chunk)}",
            "mean_return": round(float(chunk["total_reward"].mean()), 2),
            "top_end_reason": str(reasons.index[0]) if not reasons.empty else "unknown",
        })
    first, last = windows[0]["mean_return"], windows[-1]["mean_return"]
    facts: dict[str, Any] = {
        "run_id": run_id,
        "env": run["env"],
        "agent": run["agent"],
        "total_episodes": int(len(episodes)),
        "window": window,
        "first_window_mean": first,
        "last_window_mean": last,
        "change": round(last - first, 2),
        "best_window_mean": max(w["mean_return"] for w in windows),
        "end_reasons": {str(k): int(v) for k, v in episodes["end_reason"].value_counts().items()},
        "windows": windows,
    }
    eps = episodes["epsilon"].dropna()
    if not eps.empty:
        facts["final_epsilon"] = round(float(eps.iloc[-1]), 2)
    evals = store.query_evals(run_id)
    if not evals.empty:
        best = evals.loc[evals["mean_return"].idxmax()]
        facts["best_eval_mean"] = round(float(best["mean_return"]), 2)
        facts["best_eval_episode"] = int(best["checkpoint_episode"]) + 1
        facts["last_eval_mean"] = round(float(evals.iloc[-1]["mean_return"]), 2)
    return facts
```

`src/sla/reflection/grounding.py`
```python
"""Grounding validator: reject notes that contain numbers not found in the facts (owner: Vedant, Week 7)."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any

NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")
# Small whole numbers ("two seeds", "step 3") are allowed without a matching fact.
ALWAYS_ALLOWED = {float(n) for n in range(0, 11)}


@dataclass
class GroundingReport:
    passed: bool
    numbers_found: list[float] = field(default_factory=list)
    unsupported: list[float] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def extract_numbers(text: str) -> list[float]:
    """All numbers in a text, e.g. 'mean 23.5 over 1,000 episodes' -> [23.5, 1000.0]."""
    cleaned = re.sub(r"(?<=\d),(?=\d{3})", "", text)
    return [float(m) for m in NUMBER_RE.findall(cleaned)]


def fact_numbers(facts: Any) -> set[float]:
    """Every number that appears anywhere in the facts (including inside strings like '1-50')."""
    found: set[float] = set()
    if isinstance(facts, bool):
        return found
    if isinstance(facts, (int, float)):
        found.add(float(facts))
        found.add(abs(float(facts)))
    elif isinstance(facts, str):
        found.update(abs(v) for v in extract_numbers(facts))
    elif isinstance(facts, dict):
        for value in facts.values():
            found |= fact_numbers(value)
    elif isinstance(facts, (list, tuple)):
        for value in facts:
            found |= fact_numbers(value)
    return found


def check_grounding(text: str, facts: dict[str, Any], tolerance: float = 0.01) -> GroundingReport:
    """Pass only if every number in ``text`` matches a fact within ``tolerance`` (relative)."""
    allowed = fact_numbers(facts) | ALWAYS_ALLOWED
    numbers = extract_numbers(text)
    unsupported = []
    for number in numbers:
        value = abs(number)
        if not any(abs(value - f) <= tolerance * max(1.0, abs(f)) for f in allowed):
            unsupported.append(number)
    return GroundingReport(passed=not unsupported, numbers_found=numbers, unsupported=unsupported)
```

`src/sla/reflection/fallback.py`
```python
"""Rule-based template note: works with no LLM at all (owner: Vedant, Week 7)."""

from __future__ import annotations

from typing import Any


def template_note(facts: dict[str, Any]) -> str:
    """Build a plain-English summary using only values from ``facts``."""
    lines = [
        f"The {facts['agent']} agent trained on {facts['env']} for {facts['total_episodes']} episodes.",
        (f"Mean reward was {facts['first_window_mean']} in episodes {facts['windows'][0]['episodes']} "
         f"and {facts['last_window_mean']} in episodes {facts['windows'][-1]['episodes']} "
         f"(change: {facts['change']})."),
    ]
    if facts["change"] > 0:
        lines.append("Training reward went up, which is consistent with learning.")
    elif facts["change"] < 0:
        lines.append("Training reward went down; check the learning curve and settings.")
    else:
        lines.append("Training reward did not change between the first and last windows.")
    if "best_eval_mean" in facts:
        lines.append(f"The best frozen-policy evaluation scored {facts['best_eval_mean']} "
                     f"after episode {facts['best_eval_episode']}.")
    reasons = facts.get("end_reasons", {})
    if reasons:
        top = max(reasons, key=reasons.get)
        lines.append(f"The most common way episodes ended was '{top}' ({reasons[top]} episodes).")
    return " ".join(lines)
```

`src/sla/reflection/llm_client.py` — local Ollama only (`localhost`); no API key; no paid service.
```python
"""Optional local LLM client for Ollama (owner: Vedant, Week 7).

The core agent never depends on this file. If Ollama is not running, the
pipeline falls back to the template note.
"""

from __future__ import annotations

import json
import time
from typing import Any

import requests

from sla.utils.errors import LLMError

PROMPT_TEMPLATE = """You explain the results of a reinforcement-learning training run to students.
Write 3 to 5 short sentences in plain English.
Rules:
- Use ONLY numbers that appear in the FACTS below. Do not calculate new numbers.
- Do not invent results, causes or future predictions.
- If the change is positive, say the reward improved; if negative, say it fell.

FACTS (JSON):
{facts}
"""


def build_prompt(facts: dict[str, Any]) -> str:
    return PROMPT_TEMPLATE.format(facts=json.dumps(facts, indent=2))


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen2.5:1.5b",
                 timeout: float = 60.0, retries: int = 2) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.retries = retries

    def is_available(self) -> bool:
        try:
            return requests.get(f"{self.base_url}/api/tags", timeout=3).ok
        except requests.RequestException:
            return False

    def generate(self, prompt: str) -> str:
        payload = {"model": self.model, "prompt": prompt, "stream": False, "options": {"temperature": 0}}
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            try:
                resp = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=self.timeout)
                resp.raise_for_status()
                text = resp.json().get("response", "").strip()
                if not text:
                    raise LLMError("Ollama returned an empty response")
                return text
            except (requests.RequestException, ValueError, LLMError) as exc:
                last_error = exc
                time.sleep(min(2 ** attempt, 4))
        raise LLMError(f"Ollama request failed after {self.retries + 1} attempts: {last_error}")
```

`src/sla/reflection/reflect.py` (flagged addition, see Section 1)
```python
"""Reflection service: facts -> LLM or template -> grounding check -> store (owner: Vedant, Week 7).

Addition to the master plan: this small module joins the four reflection
files so the pipeline and UI call one function.
"""

from __future__ import annotations

from dataclasses import dataclass

from sla.memory.episode_store import EpisodeStore
from sla.reflection.facts import compute_facts
from sla.reflection.fallback import template_note
from sla.reflection.grounding import GroundingReport, check_grounding
from sla.reflection.llm_client import OllamaClient, build_prompt
from sla.utils.errors import LLMError
from sla.utils.logging_setup import get_logger

log = get_logger(__name__)


@dataclass
class Note:
    note_id: int
    text: str
    source: str  # "llm" or "template"
    report: GroundingReport


@dataclass
class ReflectionResult:
    shown: Note               # the note to display (always grounded)
    rejected: Note | None     # an LLM note that failed grounding, kept for transparency


def reflect(store: EpisodeStore, run_id: str, use_llm: bool = False,
            client: OllamaClient | None = None) -> ReflectionResult:
    facts = compute_facts(store, run_id)
    rejected = None
    if use_llm:
        client = client or OllamaClient()
        try:
            text = client.generate(build_prompt(facts))
            report = check_grounding(text, facts)
            note_id = store.add_reflection(run_id, facts, text, "llm", report.passed, report.to_dict())
            note = Note(note_id, text, "llm", report)
            if report.passed:
                return ReflectionResult(note, None)
            log.warning("LLM note rejected: unsupported numbers %s", report.unsupported)
            rejected = note
        except LLMError as exc:
            log.warning("LLM unavailable (%s); using template note", exc)
    text = template_note(facts)
    report = check_grounding(text, facts)
    note_id = store.add_reflection(run_id, facts, text, "template", report.passed, report.to_dict())
    return ReflectionResult(Note(note_id, text, "template", report), rejected)
```

`tests/unit/test_reflection.py`
```python
import pytest

from sla.agent.runner import EpisodeInfo
from sla.reflection.facts import compute_facts
from sla.reflection.fallback import template_note
from sla.reflection.grounding import check_grounding, extract_numbers
from sla.reflection.reflect import reflect
from sla.utils.errors import LLMError, StoreError


@pytest.fixture
def filled(store):
    store.start_run("r", "FrozenLake-v1", "q_learning", 0, {})
    for ep in range(100):
        reward = 1.0 if ep >= 50 else 0.0
        store.log_episode("r", EpisodeInfo(ep, reward, 6, 0.1, None, "goal" if reward else "hole", 0.0))
    store.log_eval("r", 99, 1.0, 0.0, 1.0, 20)
    return store


def test_extract_numbers():
    assert extract_numbers("mean 23.5 over 1,000 episodes, change -2") == [23.5, 1000.0, -2.0]


def test_facts(filled):
    facts = compute_facts(filled, "r", window=50)
    assert facts["first_window_mean"] == 0.0 and facts["last_window_mean"] == 1.0
    assert facts["windows"][1]["episodes"] == "51-100" and facts["best_eval_episode"] == 100


def test_facts_missing_run(store):
    with pytest.raises(StoreError):
        compute_facts(store, "nope")


def test_template_note_is_grounded(filled):
    facts = compute_facts(filled, "r")
    assert check_grounding(template_note(facts), facts).passed


def test_planted_wrong_number_rejected(filled):
    facts = compute_facts(filled, "r")
    report = check_grounding("The agent reached a mean reward of 87.3 after training.", facts)
    assert not report.passed and report.unsupported == [87.3]


class FakeClient:
    def __init__(self, text=None, fail=False):
        self.text, self.fail = text, fail

    def generate(self, prompt):
        if self.fail:
            raise LLMError("offline")
        return self.text


def test_reflect_falls_back_when_llm_offline(filled):
    result = reflect(filled, "r", use_llm=True, client=FakeClient(fail=True))
    assert result.shown.source == "template" and result.shown.report.passed and result.rejected is None


def test_reflect_rejects_hallucinated_llm_note(filled):
    result = reflect(filled, "r", use_llm=True, client=FakeClient("Reward rose to 999 points."))
    assert result.rejected is not None and result.rejected.source == "llm"
    assert result.shown.source == "template"
    assert len(filled.query_reflections("r")) == 2


def test_reflect_accepts_grounded_llm_note(filled):
    result = reflect(filled, "r", use_llm=True, client=FakeClient("Mean reward went from 0.0 to 1.0."))
    assert result.shown.source == "llm" and result.rejected is None
```

### 5.4 Dashboard (Somesh)

**Lesson (read with Atharv before coding):**
```python
# hello_page.py  ->  run with:  streamlit run hello_page.py
import streamlit as st

st.title("Hello")                              # big heading
name = st.text_input("Your name")              # returns what the user typed ("" at first)
with st.form("my_form"):                       # inputs inside a form are sent together
    n = st.number_input("Episodes", min_value=1, value=10)
    go = st.form_submit_button("Go")           # True only in the run right after the click
if go:                                         # the WHOLE script re-runs after every click,
    st.success(f"{name} asked for {n} episodes")  # so we check the button value
if n > 500:
    st.error("Too many for a demo")
    st.stop()                                  # stop drawing the rest of the page
st.dataframe({"episode": [0, 1], "reward": [0.0, 1.0]})   # an interactive table
```
Mini-exercises: (a) add a `st.selectbox` with "FrozenLake-v1" and "CartPole-v1" and print the choice; (b) show a `st.metric("Reward", 0.75)`; (c) explain to Atharv why `go` is `False` again after the next click.

`src/sla/ui/common.py`
```python
"""Shared helpers for the Streamlit pages (owner: Somesh, Week 7)."""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CONFIG_DIR = REPO_ROOT / "configs"
DB_PATH = os.environ.get("SLA_DB", str(REPO_ROOT / "runs" / "episodes.db"))

# Which default config to use for each (environment, agent) pair shown in the UI.
CONFIGS: dict[tuple[str, str], str] = {
    ("FrozenLake-v1", "random"): "frozenlake_random.yaml",
    ("FrozenLake-v1", "q_learning"): "frozenlake_q.yaml",
    ("CartPole-v1", "random"): "cartpole_random.yaml",
    ("CartPole-v1", "dqn"): "cartpole_dqn.yaml",
}


def agents_for(env_name: str) -> list[str]:
    return [agent for (env, agent) in CONFIGS if env == env_name]


def config_path(env_name: str, agent: str) -> Path:
    try:
        return CONFIG_DIR / CONFIGS[(env_name, agent)]
    except KeyError as exc:
        raise ValueError(f"No default config for {agent} on {env_name}") from exc


def get_store():
    from sla.memory.episode_store import EpisodeStore
    return EpisodeStore(DB_PATH)
```

**Line by line (common.py):** `Path(__file__).resolve().parents[3]` climbs from `src/sla/ui/common.py` up to the repo folder · `os.environ.get("SLA_DB", default)` uses a test database when the variable is set · `CONFIGS` maps (env, agent) to a YAML file so the UI only offers valid pairs · `agents_for` is a list comprehension over those pairs · `get_store` imports the store inside the function so the page loads fast.

`src/sla/ui/app.py`
```python
"""Streamlit home page (owner: Somesh, Week 7).

Run with:  streamlit run src/sla/ui/app.py   (or: sla dashboard)
"""

import streamlit as st

from sla.ui.common import get_store

st.set_page_config(page_title="Self-Learning AI Agent", layout="wide")
st.title("Self-Learning AI Agent")
st.markdown(
    "This agent starts with **no knowledge** of its task and improves by learning from rewards.\n\n"
    "* **Train** – start a run (Q-learning on FrozenLake, DQN on CartPole).\n"
    "* **Results** – learning curves and frozen-policy evaluation.\n"
    "* **Reflection** – a plain-language note grounded in the logged numbers, and a rating form."
)

store = get_store()
runs = store.list_runs()
st.subheader("Runs")
if runs.empty:
    st.info("No runs yet. Open the **Train** page in the sidebar to start one.")
else:
    st.dataframe(runs[["run_id", "env", "agent", "seed", "started_at"]], use_container_width=True)
```

`src/sla/ui/pages/1_Train.py`
```python
"""Train page: start a run from the browser (owner: Somesh, Week 7)."""

import streamlit as st

from sla.ui.common import DB_PATH, agents_for, config_path
from sla.utils.config import load_config, validate_config
from sla.utils.errors import SLAError
from sla.utils.validation import validate_episode_count, validate_seeds

st.title("Train an agent")

env_name = st.selectbox("Environment", ["FrozenLake-v1", "CartPole-v1"])
agent = st.selectbox("Agent", agents_for(env_name))
with st.form("train_form"):
    episodes = st.number_input("Episodes", min_value=1, max_value=100_000, value=300, step=50)
    seed = st.number_input("Seed", min_value=0, max_value=10_000, value=0, step=1)
    use_llm = st.checkbox("Use local Ollama model for the explanation (optional)", value=False)
    submitted = st.form_submit_button("Start training")

if submitted:
    try:
        cfg = load_config(config_path(env_name, agent))
        cfg.episodes = validate_episode_count(int(episodes))
        cfg.seed = validate_seeds([int(seed)])[0]
        validate_config(cfg)
    except SLAError as exc:
        st.error(f"Please fix the input: {exc}")
        st.stop()

    from sla.pipeline import run_pipeline

    with st.spinner(f"Training {agent} on {env_name} for {cfg.episodes} episodes... (keep this tab open)"):
        try:
            result = run_pipeline(cfg, DB_PATH, final_eval_episodes=50, use_llm=use_llm)
        except ImportError as exc:
            st.error(f"A required package is missing: {exc}. Did you install PyTorch (CPU)?")
            st.stop()
        except SLAError as exc:
            st.error(f"Training failed: {exc}")
            st.stop()

    st.success(f"Finished run {result.train.run_id} ({result.train.stopped_reason}).")
    col1, col2, col3 = st.columns(3)
    col1.metric("Final mean return (test seeds)", f"{result.final_eval.mean_return:.2f}")
    col2.metric("Std", f"{result.final_eval.std_return:.2f}")
    col3.metric("Success rate", f"{result.final_eval.success_rate:.0%}")
    for plot in result.plots:
        st.image(str(plot))
    st.info(f"Explanation ({result.note_source}): {result.note_text}")
```

`src/sla/ui/pages/2_Results.py` — Week-7 version (in Week 10 you add a CSV-download region at the end):
```python
"""Results page: learning curves and evaluation for a chosen run (owner: Somesh, Week 7)."""

import streamlit as st

from sla.evaluation.plots import plot_eval_curve, plot_learning_curve
from sla.ui.common import get_store

st.title("Results")
store = get_store()
runs = store.list_runs()
if runs.empty:
    st.info("No runs yet. Train an agent first.")
    st.stop()

run_id = st.selectbox("Run", runs["run_id"].tolist())
window = st.slider("Rolling-mean window", min_value=5, max_value=200, value=50, step=5)
episodes = store.query_episodes(run_id)
evals = store.query_evals(run_id)

if episodes.empty:
    st.warning("This run has no episodes logged.")
    st.stop()

st.pyplot(plot_learning_curve(episodes, window=window, title=run_id))
c1, c2, c3 = st.columns(3)
c1.metric("Episodes", len(episodes))
c2.metric("Mean reward (first 50)", f"{episodes['total_reward'].head(50).mean():.2f}")
c3.metric("Mean reward (last 50)", f"{episodes['total_reward'].tail(50).mean():.2f}")

st.subheader("Frozen-policy evaluation")
if evals.empty:
    st.caption("No evaluations logged for this run.")
else:
    st.pyplot(plot_eval_curve(evals))
    st.dataframe(evals, use_container_width=True)

st.subheader("How episodes ended")
st.bar_chart(episodes["end_reason"].value_counts())
```

`src/sla/ui/pages/3_Reflection.py`
```python
"""Reflection page: grounded notes and the rating form (owner: Somesh, Week 7)."""

import streamlit as st

from sla.reflection.reflect import reflect
from sla.ui.common import get_store
from sla.ui.feedback import ratings_summary, save_rating
from sla.utils.errors import SLAError

st.title("Reflection notes")
st.caption("Notes explain what the agent learned using only logged numbers. "
           "They never change the agent. Ratings help us judge the notes.")
store = get_store()
runs = store.list_runs()
if runs.empty:
    st.info("No runs yet.")
    st.stop()

run_id = st.selectbox("Run", runs["run_id"].tolist())
use_llm = st.checkbox("Try the local Ollama model", value=False)
if st.button("Generate a new note"):
    try:
        result = reflect(store, run_id, use_llm=use_llm)
        if result.rejected:
            st.warning("The LLM note was rejected because it contained numbers not found in the data: "
                       f"{result.rejected.report.unsupported}")
        st.success(f"Note #{result.shown.note_id} created ({result.shown.source}).")
    except SLAError as exc:
        st.error(str(exc))

notes = store.query_reflections(run_id)
for _, note in notes.iterrows():
    badge = "grounded" if note["grounding_passed"] else "REJECTED"
    with st.expander(f"Note #{note['note_id']} · {note['source']} · {badge}"):
        st.write(note["note_text"])

if not notes.empty:
    st.subheader("Rate a note")
    with st.form("rating"):
        note_id = st.selectbox("Note", notes["note_id"].tolist())
        accurate = st.radio("Is it accurate?", ["Yes", "No"], horizontal=True) == "Yes"
        usefulness = st.slider("How useful (1 = not, 5 = very)?", 1, 5, 3)
        comment = st.text_area("Comment (optional, max 500 characters)")
        if st.form_submit_button("Save rating"):
            try:
                save_rating(store, int(note_id), accurate, int(usefulness), comment)
                st.success("Thank you! Rating saved.")
            except SLAError as exc:
                st.error(str(exc))

st.caption(f"Ratings so far: {ratings_summary(store)}")
```

`tests/ui/test_pages.py`
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
│   └── baseline/
│       └── baseline.csv
├── scripts/
│   ├── hardware_check.py
│   ├── quick_frozenlake_check.py
│   ├── run_ablation.py   [NEW · Atharv]
│   └── run_baseline.py
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
│       │   ├── ablation.py   [NEW · Atharv]
│       │   ├── evaluate.py
│       │   ├── metrics.py
│       │   ├── plots.py
│       │   └── stats.py   [NEW · Atharv]
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
│       │   ├── facts.py   [NEW · Vedant]
│       │   ├── fallback.py   [NEW · Vedant]
│       │   ├── grounding.py   [NEW · Vedant]
│       │   ├── llm_client.py   [NEW · Vedant]
│       │   └── reflect.py   [NEW · Vedant]
│       ├── ui/
│       │   ├── pages/
│       │   │   ├── 1_Train.py   [NEW · Somesh]
│       │   │   ├── 2_Results.py   [NEW · Somesh]
│       │   │   └── 3_Reflection.py   [NEW · Somesh]
│       │   ├── __init__.py
│       │   ├── app.py   [NEW · Somesh]
│       │   ├── common.py   [NEW · Somesh]
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
│       ├── cli.py   [MODIFIED · Brahmanand]
│       └── pipeline.py   [MODIFIED · Brahmanand]
├── tests/
│   ├── integration/
│   │   ├── test_cli.py   [NEW · Brahmanand]
│   │   ├── test_dqn_smoke.py
│   │   ├── test_pipeline_e2e.py   [MODIFIED · Brahmanand]
│   │   ├── test_resume.py
│   │   ├── test_runner.py
│   │   └── test_transition_validation.py
│   ├── ui/
│   │   └── test_pages.py   [NEW · Somesh]
│   ├── unit/
│   │   ├── test_ablation.py   [NEW · Atharv]
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
│   │   ├── test_reflection.py   [NEW · Vedant]
│   │   ├── test_replay_buffer.py
│   │   ├── test_safety.py
│   │   ├── test_schedules.py
│   │   ├── test_stats.py   [NEW · Atharv]
│   │   ├── test_summary.py
│   │   └── test_validation.py
│   └── conftest.py
├── .env.example
├── .gitignore
├── CONTRIBUTING.md
├── pyproject.toml
└── README.md   [MODIFIED · Atharv → Brahmanand]
```

Legend: [NEW] created this week · [MODIFIED] changed this week · no tag = carried over unchanged from an earlier week. `runs/` (training outputs) and `.venv/` exist on your laptop but are git-ignored, so they are not shown.

---

## SECTION 7 — GITHUB COLLABORATION PROCEDURE

13-step flow as every week. Week-7 issues:

| # | Title | Owner | Branch | Reviewer | Merge by |
|---|---|---|---|---|---|
| 71 | Full pipeline + CLI commands | Brahmanand | `feat/brahmanand-71-full-pipeline` | Atharv | **Day 4** |
| 72 | README pipeline/dashboard + fresh-clone bug triage | Brahmanand | `docs/brahmanand-72-readme-pipeline` | Somesh | Day 6 |
| 73 | Statistics helpers | Atharv | `feat/atharv-73-stats` | Brahmanand | Day 2 |
| 74 | Ablation study | Atharv | `feat/atharv-74-ablation` | Vedant | Day 4 |
| 75 | Grounded reflection | Vedant | `feat/vedant-75-grounded-reflection` | Brahmanand | **Day 3** |
| 76 | Optional Ollama client + `reflect` | Vedant | `feat/vedant-76-llm-client` | Brahmanand | **Day 3** |
| 77 | Streamlit shell | Somesh | `feat/somesh-77-ui-shell` | Vedant | **Day 3** |
| 78 | Dashboard pages + UI tests | Somesh | `feat/somesh-78-ui-pages` | Vedant | Day 6 |

**Screenshots in PRs:** UI PRs must include screenshots; this is also how the report figures are collected (Week 9).

---

## SECTION 8 — WEEKLY INTEGRATION PROCEDURE

| Item | This week |
|---|---|
| Modules to connect | UI → `run_pipeline`, store queries, plots, `reflect`, `feedback`; pipeline → `train_and_evaluate`, plots, `reflect`; CLI → pipeline, reflect, Streamlit; ablation → `train_and_evaluate` + stats. |
| Integrator | **Brahmanand** (integration captain). |
| Interfaces that must match | `PipelineResult` fields used by `1_Train.py`; `ReflectionResult.shown.text/.source`; `query_reflections` columns used by `3_Reflection.py`; `save_rating(store, note_id, accurate, usefulness, comment)`; `run_ablation` output column `final_mean` used by the script. |
| Tests that must pass | all; `tests/ui` (Streamlit), `test_cli.py`, e2e. |
| Detect failures | UI shows a Python traceback; note shown with "grounding failed"; `sla pipeline` works but the Train page does not (different DB path). |
| Debug | run the page from the terminal and read the traceback; print `DB_PATH`; run `sla reflect --run-id ...` to separate UI bugs from reflection bugs. |

**Integration checklist**
- [ ] Fresh clone → install → `pytest` → `sla pipeline` → `sla dashboard` works on 4 laptops
- [ ] Everything works with Ollama **not installed**
- [ ] Train page run appears on Results and Reflection pages
- [ ] Rating saved and visible in the summary
- [ ] Runner unchanged; CI green on `main`

---

## SECTION 9 — TESTING AND VALIDATION

| Type | Tests this week | Command |
|---|---|---|
| Unit | `test_stats` (5), `test_ablation` (2), `test_reflection` (8) | `pytest tests/unit -v` |
| Integration | `test_pipeline_e2e` (2), `test_cli` (3) | `pytest tests/integration -v` |
| UI | `tests/ui/test_pages.py` (3, AppTest) | `pytest tests/ui -v` |
| LLM safety | planted wrong number rejected; hallucinated LLM note rejected; offline → template | in `test_reflection.py` |
| Input validation | UI uses W4 validators and W6 rating validation | UI tests + manual |
| Error handling | bad config → clear `Error:` and exit 1; missing checkpoint → `CheckpointError` | `test_cli.py` |

**RL rules applied this week:** the pipeline reports the **test-seed** score of the best checkpoint; ablation variants are evaluated with exactly the same protocol; pilot ablation numbers (2 seeds, 150 episodes) are labelled "pilot" and never used as results; notes may only contain numbers from the facts.

---

## SECTION 10 — COMMON PROBLEMS AND SOLUTIONS

| Problem | Possible Cause | How to Check | Solution |
|---|---|---|---|
| `streamlit: command not found` | venv not active | `which streamlit` | activate venv; `sla dashboard` |
| Page re-trains on every click | training code outside `if submitted:` | read page code | keep heavy work inside the button branch |
| UI shows no runs but CLI has runs | different DB path | print `DB_PATH` on the page | run from the repo folder; unset `SLA_DB` |
| `LLM unavailable` warning | Ollama not running (normal) | `curl http://localhost:11434/api/tags` | ignore (template used) or `ollama serve` |
| LLM note always rejected | model invents numbers or rounds differently | stored `grounding_report` | expected sometimes; template is shown; never relax the check to "make it pass" |
| Ollama very slow | CPU only, large model | time `sla reflect --llm` | use `qwen2.5:1.5b`; LLM stays optional |
| AppTest error `No module named sla` | tests not run from repo root | `pwd` | run `pytest` from the repo root |
| Ablation takes hours | 3 variants × 5 seeds × 600 episodes | estimate from one run | pilot with 2 seeds/150 episodes now; full run in Week 8 across laptops |
| Merge conflict in `cli.py` | two people edited it | conflict markers | only Brahmanand edits `cli.py` |

---

## SECTION 11 — WEEKLY DELIVERABLES

| Deliverable | Owner | File/Location | Verification | Status |
|---|---|---|---|---|
| Full pipeline | Brahmanand | `src/sla/pipeline.py` (W7) | e2e test | [ ] |
| CLI pipeline/reflect/dashboard | Brahmanand | `src/sla/cli.py`, `tests/integration/test_cli.py` | 3 CLI tests | [ ] |
| Statistics | Atharv | `src/sla/evaluation/stats.py` | 5 tests | [ ] |
| Ablation code + pilot | Atharv | `src/sla/evaluation/ablation.py`, `scripts/run_ablation.py` | 2 tests; pilot printed | [ ] |
| Grounded reflection | Vedant | `src/sla/reflection/*.py` | 8 tests offline | [ ] |
| Dashboard shell | Somesh | `src/sla/ui/common.py`, `app.py` | home page demo | [ ] |
| Dashboard pages + tests | Somesh | `src/sla/ui/pages/*.py`, `tests/ui/test_pages.py` | 3 UI tests; teammate test | [ ] |
| Fresh-clone integration test | All | GitHub issues labelled `bug` | 4 laptops | [ ] |

---

## SECTION 12 — WEEKLY REVIEW MEETING

**Agenda:** live demo (dashboard: train FrozenLake → results → reflection → rate) with Ollama off · completed/pending · bugs found on Day 6 · code quality · tests · PRs · integration · Week-8 plan.

**Questions:**
1. Brahmanand: what does `run_pipeline` produce, in what order, and why is the run id created before training?
2. Vedant: how does the grounding check decide a note is acceptable? Show the planted-wrong-number test.
3. What happens if Ollama is not installed? Prove it live.
4. Atharv: what does a bootstrap CI tell us, and why are 5 seeds a limitation?
5. What does each ablation variant remove, and what do we expect to happen?
6. Somesh: why does a Streamlit page re-run from the top on every click, and how did you stop training from restarting?
7. Which of your earlier functions (W4, W5, W6) does the dashboard reuse?
8. Which bugs from the fresh-clone test are still open, and who owns each?

---

## SECTION 13 — WEEK COMPLETION CHECKLIST

- [ ] All assigned tasks completed
- [ ] Code pushed to feature branches
- [ ] Pull requests reviewed and merged (#75, #76, #77 before #71/#78)
- [ ] All tests pass locally and in CI (including UI tests)
- [ ] Full system integrated and demonstrated with Ollama off
- [ ] README updated with `sla pipeline` and `sla dashboard`
- [ ] Weekly demonstration completed
- [ ] Bugs and blockers recorded as issues

---

## SECTION 14 — NEXT WEEK HANDOFF

- **Ready before Week 8:** complete system on `main`: `sla train/resume/prune/evaluate/pipeline/reflect/dashboard`; reflection; stats; ablation code; UI with 3 tests; open `bug` issues list.
- **Files Week 8 depends on:** `pipeline.train_and_evaluate` (final experiments), `ablation.run_ablation` + `stats.compare_groups` (full ablation), `metrics.json` format (tables), `checkpoint.load_checkpoint` (persistence test), `ui/pages/*` (UI hardening), `reflections`/`feedback` tables (reflection evaluation).
- **Coordination:** Week 8 runs long experiments — agree on Day 1 which laptop runs which seeds/variants and **freeze the code** (tag `v0.8-experiments`) before final runs so every result maps to one commit.
- **Risks:** experiment time (plan overnight runs); UI bugs found late (Somesh fixes them in Week 8 with tests); results may be weaker than hoped — report them as they are.
