# WEEK 05 — Memory and State Management

**Project:** Self-Learning AI Agent · **Team:** Brahmanand Mathpati, Atharv Gundale, Vedant Biradar, Somesh Badwane
**Source:** *Self_Learning_AI_Agent_10_Week_Master_Plan* (v1.0) · **Interfaces:** `docs/design.md` (tag `w2-design-freeze`)

---

## SECTION 1 — WEEK OVERVIEW

| Item | Details |
|---|---|
| Week number | 5 of 10 |
| Week title | Memory and State Management |
| Main objective | Give the agent a **memory that survives**: every episode goes into a SQLite database (long-term memory), training can be **stopped and resumed exactly** from checkpoints, and the first **learning-curve plots** are drawn from stored data. First real DQN runs on CartPole (pilot). |
| Expected outcome | `sla train`, `sla resume`, `sla prune` work from the terminal; `runs/episodes.db` holds runs and episodes; a resumed run gives the **same numbers** as an uninterrupted run; Somesh's plots draw a learning curve from the database; Atharv has 3 pilot CartPole runs with honest notes. |
| Required knowledge | Week-4 runner and `Callback` idea; SQL basics (`CREATE TABLE`, `INSERT`, `SELECT`, foreign keys); file paths; JSON; pandas DataFrames (read-only use); matplotlib basics (Somesh). |
| Required tools | Same venv. **No new dependency:** `sqlite3` is in the Python standard library; pandas and matplotlib were already in `pyproject.toml` (Week 3). Optional free viewer: *DB Browser for SQLite* (open source) to look inside the database. |
| Prerequisites from previous weeks | Week 4 merged: `runner.py` (`Callback`, `EpisodeInfo`, `RunContext`, `RunResult`), agents with `save/load`, `replay_buffer.py` with `save/load_from`, `summary.rolling_mean`, CI green. |
| Approximate workload | 11 h per member. |
| Technical dependencies | Vedant's `episode_store.py` merged by **Day 3** (CLI and plots read from it). Brahmanand's `checkpoint.py` merged by **Day 3** (CLI imports it). `sla train` merged by **Day 4** (Atharv's pilot runs use it). |
| Definition of Done | All Week-5 tests pass in CI; `test_resumed_run_matches_uninterrupted_run` passes (resume is exact); `test_retrieval_accuracy_1000_rows` passes; `sla train --config configs/frozenlake_q.yaml` creates a run folder with checkpoints and rows in `runs/episodes.db`; learning-curve PNG produced from the database; DQN pilot results recorded **as observed** (no invented numbers). |

**In simple words:** last week the agent learned, but forgot everything when the program closed. This week we give it a diary (the database) and a "save game" button (checkpoints).

---

## SECTION 2 — WHAT WE ARE BUILDING THIS WEEK

1. **Modules:** `agent/checkpoint.py` + first real `cli.py` (Brahmanand) · `memory/episode_store.py` + `memory/retention.py` (Vedant) · `evaluation/plots.py` (Somesh) · DQN smoke test + pilot runs + debug checklist (Atharv).
2. **Why:** a final-year project must show *evidence*. Without stored episodes there are no learning curves; without checkpoints a laptop crash at episode 550 of 600 wastes an hour; without resume the "self-learning over time" claim cannot be demonstrated.
3. **Connection:** both the store and checkpoints are **callbacks** — they plug into the Week-4 runner without changing it. Week 6 adds evaluation callbacks the same way; Week 7's UI reads only from the store.
4. **If missing:** no plots, no evaluation history, no reflection facts (Week 7), no dashboard.
5. **Final output:**
   ```text
   $ sla train --config configs/frozenlake_q.yaml
   Run id: frozenlake_q_learning_s0_20261105-181202  (completed, 2000 episodes)
   Mean training reward of the last 50 episodes: 0.9x
   Folder: runs/frozenlake_q_learning_s0_20261105-181202
   $ ls runs/frozenlake_q_learning_s0_20261105-181202/checkpoints
   ep_000999  ep_001499  ep_001999  latest.json
   ```
   (Your run id, time stamp and reward will differ — record what you actually see.)

**Analogy:** the replay buffer (Week 4) is short-term memory — what happened a few minutes ago. The SQLite store is long-term memory — a diary of every episode ever played. A checkpoint is a "save game" — the agent's brain at one moment.

### Where data goes
```text
run_training ──► StoreCallback ──────► runs/episodes.db   (runs, episodes; later evals, reflections, feedback)
             └─► CheckpointCallback ─► runs/<run_id>/checkpoints/ep_000499/ (agent files + checkpoint.json)
                                       runs/<run_id>/checkpoints/latest.json
plots.py ◄── EpisodeStore.query_episodes(run_id)  (pandas DataFrame)
```

---

## SECTION 3 — DAILY EXECUTION PLAN

### Day 1 — Agree the data contract (1.5 h)
- **Daily objective:** everyone knows the database tables and the checkpoint folder layout before coding.
- **Assigned members:** all (Vedant leads 30 min on the schema; Brahmanand 15 min on checkpoint layout; Atharv is integration captain this week).
- **Individual tasks:** Vedant: `SCHEMA` + `start_run` / `log_episode` (SLA-05-VB-1 steps 1–3). Brahmanand: `save_checkpoint` / `load_checkpoint` (SLA-05-BM-1 steps 1–2). Atharv: write `docs/notes/dqn_debug_checklist.md` skeleton (SLA-05-AG-1 step 1). Somesh: matplotlib and pandas lesson (Section 5.5) — exercises (a)–(c).
- **Required commands:**
  ```bash
  git checkout main && git pull
  pip install -e ".[dev]"
  pytest -q                        # all Week-4 tests must still pass
  python -c "import sqlite3; print(sqlite3.sqlite_version)"
  ```
- **Expected files:** `src/sla/memory/episode_store.py` (draft), `src/sla/agent/checkpoint.py` (draft).
- **Expected output:** agreed callback order written in the issue #51 comment: `StoreCallback` first, then `CheckpointCallback`.
- **Testing steps:** none yet (design day).
- **GitHub activity:** issues #51–#58 created and assigned (Section 7).
- **Completion checklist:** - [ ] schema agreed · - [ ] callback order agreed · - [ ] issues assigned

### Day 2 — Store and checkpoints, first tests (1.5 h)
- **Daily objective:** store survives reopen; checkpoints save and load an agent.
- **Assigned members:** Vedant (store + tests), Brahmanand (checkpoint callback), Somesh (`plot_learning_curve`), Atharv (reviews store schema).
- **Individual tasks:** SLA-05-VB-1 steps 4–6 · SLA-05-BM-1 steps 3–4 · SLA-05-SB-1 steps 1–3.
- **Required commands:** `pytest tests/unit/test_episode_store.py -v`
- **Expected files:** `tests/unit/test_episode_store.py`, `tests/conftest.py` (W5 region), `src/sla/evaluation/plots.py`.
- **Expected output:** `test_run_and_episodes_persist_after_reopen` passes.
- **GitHub activity:** PR #53 (store) opened.
- **Completion checklist:** - [ ] store PR open · - [ ] checkpoint callback saves folders

### Day 3 — Resume and merge the dependencies (1.5 h)
- **Daily objective:** store and checkpoint merged; resume gives identical numbers.
- **Assigned members:** Brahmanand (resume + `test_resume.py`), Vedant (retention + data handling doc), Atharv (reviews checkpoint PR — checks DQN buffer and optimizer are saved), Somesh (plot tests).
- **Individual tasks:** SLA-05-BM-1 steps 5–7 · SLA-05-VB-2 steps 1–3 · SLA-05-SB-1 steps 4–6.
- **Required commands:**
  ```bash
  pytest tests/integration/test_resume.py -v
  pytest tests/unit/test_plots.py -v
  ```
- **Expected output:** `2 passed` in `test_resume.py`.
- **GitHub activity:** PRs #51 (checkpoint + resume) and #53 (store) **merged**.
- **Completion checklist:** - [ ] resume exact · - [ ] store merged

### Day 4 — Command-line interface (1.5 h)
- **Daily objective:** `sla train`, `sla resume`, `sla prune` work.
- **Assigned members:** Brahmanand (CLI), Vedant (retention PR), Somesh (plots PR → Vedant review), Atharv (first CartPole pilot run once CLI is merged).
- **Individual tasks:** SLA-05-BM-2 steps 1–5 · SLA-05-VB-2 step 4 · SLA-05-AG-1 step 2.
- **Required commands:**
  ```bash
  sla train --config configs/frozenlake_q.yaml
  sla resume --run runs/<run_id>          # after interrupting a second run with Ctrl+C
  sla prune --older-than 30               # dry run, deletes nothing
  ```
- **Expected files:** `src/sla/cli.py` (Week-5 version), README "Command line" section.
- **Expected output:** run folder with `checkpoints/` and `config.yaml`; `runs/episodes.db` exists.
- **GitHub activity:** PR #52 (CLI) merged; #55 (plots) under review.
- **Completion checklist:** - [ ] `sla train` works on all 4 laptops

### Day 5 — DQN pilot and smoke test (1.5 h)
- **Daily objective:** first real DQN training on CartPole; failures recorded honestly.
- **Assigned members:** Atharv (pilot runs + smoke test), Brahmanand (pairs with Atharv on any runner/checkpoint issue), Vedant (checks the pilot rows in the database), Somesh (plots a pilot run's learning curve).
- **Individual tasks:** SLA-05-AG-1 steps 3–6.
- **Required commands:**
  ```bash
  sla train --config configs/cartpole_dqn.yaml --seed 0
  pytest -m smoke -v                       # runs test_dqn_smoke (needs torch)
  ```
- **Expected output:** 3 pilot runs; for each, the last-50 mean training reward written in `docs/notes/dqn_debug_checklist.md` exactly as printed.
- **Completion checklist:** - [ ] 3 pilot runs recorded · - [ ] smoke test passes locally

### Day 6 — Merge, plot from the database, interrupt test (2.5 h)
- **Daily objective:** all PRs merged; everyone proves resume on their own laptop.
- **Assigned members:** all.
- **Individual tasks:** each member: start `sla train --config configs/frozenlake_q.yaml`, press Ctrl+C around episode 1200, run `sla resume --run ...`, confirm it continues from the last checkpoint. Somesh draws the learning curve of his own run (Section 5.5 example). Vedant opens the database in DB Browser for SQLite and shows the team the tables.
- **Required commands:** `git checkout main && git pull && pytest`
- **Expected output:** 4 learning-curve PNGs (one per laptop) in each member's local `runs/` (not committed).
- **Completion checklist:** - [ ] all PRs merged · - [ ] interrupt/resume done on 4 laptops

### Day 7 — Weekly review (1 h)
- **Daily objective:** demo on fresh `main`: train → interrupt → resume → plot; Section 12 agenda.
- **Completion checklist:** - [ ] Section 13 complete

---

## SECTION 4 — INDIVIDUAL MEMBER TASKS

### Brahmanand Mathpati

**Task ID:** SLA-05-BM-1
**Task Title:** Checkpoints and exact resume
**Priority:** P1
**Estimated Duration:** 6 h (learning 1, coding 3, testing 1, integration 1)
**Dependencies:** Week-4 runner; agents' `save/load`; Vedant's `ReplayBuffer.save/load_from`
**Assigned Member:** Brahmanand Mathpati

1. **What:** `src/sla/agent/checkpoint.py` — `save_checkpoint`, `load_checkpoint`, `latest_checkpoint`, `CheckpointCallback(every, keep_last=3)`, `resume_training(run_dir, callbacks)`.
2. **Why:** "save game" for the agent: protects long CartPole runs, lets Week 6 pick the **best** checkpoint, and lets Week 8 prove a reloaded agent behaves identically.
3. **Files:** create `agent/checkpoint.py`, `tests/integration/test_resume.py`.
4. **Functions/classes:** as item 1 (exact code in Section 5.1).
5. **Inputs:** a trained agent, a folder, the episode number; for resume: a run folder containing `config.yaml` and `checkpoints/latest.json`.
6. **Outputs:** `checkpoints/ep_000499/` (episodes count from 0; agent files + `checkpoint.json` with agent class name and episode), `checkpoints/latest.json`; a continued `RunResult`.
7. **Steps:**
   1. Write `save_checkpoint` / `load_checkpoint` — `checkpoint.json` stores the agent name so `load_checkpoint` knows which class to rebuild (`_agent_class`).
   2. Unit-check by hand in a Python shell: train Q-learning 50 episodes, save, load, compare `agent.q`.
   3. Write `CheckpointCallback`: save every `every` episodes and at the end; keep only the newest `keep_last` folders (`_cleanup`) so the disk does not fill up.
   4. Write `latest_checkpoint` (reads `latest.json`; raises `CheckpointError` with a clear message if missing).
   5. Write `resume_training`: load config + latest checkpoint, call `run_training(..., agent=agent, run_id=..., start_episode=episode)`. Because every episode resets with `episode_seed(seed, episode)` (Week 4), the resumed episodes see exactly the same start states.
   6. Write `tests/integration/test_resume.py` (2 tests).
   7. Run; open PR #51.
8. **Commands:**
   ```bash
   git checkout main && git pull
   git checkout -b feat/brahmanand-51-checkpoint-resume
   pytest tests/integration/test_resume.py -v
   ruff check src tests
   git add src/sla/agent/checkpoint.py tests/integration/test_resume.py
   git commit -m "feat(agent): add checkpoints and exact resume"
   git push -u origin feat/brahmanand-51-checkpoint-resume
   ```
9. **Tests:** resume continues the episode count; a run stopped after 100 episodes and resumed to 150 has **identical** returns to an uninterrupted 150-episode run.
10. **Expected result:** `2 passed`.
11. **Common errors:** resumed run differs → agent RNG state not saved (check `meta.json` has `rng_state`) or ε step counter reset; `CheckpointError: no latest.json` → the run was stopped before the first checkpoint (lower `checkpoint_every` for testing); Windows path errors → always use `pathlib.Path`, never string `+ "/"`.
12. **Branch:** `feat/brahmanand-51-checkpoint-resume`
13. **Commit:** `feat(agent): add checkpoints and exact resume`
14. **PR title:** `feat: checkpoints and resume (SLA-05-BM-1)`
15. **Acceptance:** exact-resume test passes in CI; reviewer: Atharv (checks DQN optimizer, step counters and buffer are restored).

**Task ID:** SLA-05-BM-2
**Task Title:** Command-line interface: `sla train`, `sla resume`, `sla prune`
**Priority:** P1
**Estimated Duration:** 5 h (coding 2, testing 1, integration 1, docs 1)
**Dependencies:** SLA-05-BM-1; Vedant's store (#53) and retention (#54)
**Assigned Member:** Brahmanand Mathpati

1. **What:** replace the Week-3 CLI skeleton with the **Week-5 version** of `src/sla/cli.py` (Section 5.2): `_load_cfg`, `_callbacks`, `cmd_train`, `cmd_resume`, `cmd_prune`, `add_w5_parsers`.
2. **Why:** one consistent way for the team, the examiner and the Week-7 UI to start training.
3. **Files:** modify `src/sla/cli.py`, `README.md` (new "Command line" section).
4. **Functions:** as item 1; `build_parser` and `main` stay exactly as in Week 3 — new commands are added through the `PARSER_BUILDERS` list, so Weeks 6 and 7 only *append*.
5. **Inputs:** `--config`, optional `--seed`, `--episodes`, `--db`; `--run` for resume; `--older-than`, `--yes` for prune.
6. **Outputs:** printed run id, stop reason, mean of the last 50 training episodes, run folder.
7. **Steps:**
   1. Pull `main` after #51 and #53 are merged.
   2. Copy the Week-5 `cli.py` from Section 5.2; read the region markers `# region W5` / `# endregion`.
   3. Run `sla --help`, `sla train --help`.
   4. Train FrozenLake once; interrupt a second run; resume it.
   5. Add the "Command line" section to README (command table: train / resume / prune with one example each).
   6. Open PR #52; open PR #58 for README if you prefer a separate docs PR.
8. **Commands:**
   ```bash
   git checkout -b feat/brahmanand-52-cli-train-resume
   sla --help
   sla train --config configs/frozenlake_q.yaml --episodes 300
   pytest tests/unit/test_cli_help.py -v
   git add src/sla/cli.py README.md
   git commit -m "feat(cli): add train, resume and prune commands"
   git push -u origin feat/brahmanand-52-cli-train-resume
   ```
9. **Tests:** `test_cli_help.py` (Week 3) still passes; manual train/resume/prune run recorded in the PR description. Full CLI integration tests come in Week 7 (`test_cli.py`).
10. **Expected result:** `sla --help` lists `train`, `resume`, `prune`.
11. **Common errors:** `sla: command not found` → run `pip install -e .` again in the venv; `Error: ...` with exit code 1 → this is our clean `SLAError` message, read it (e.g. a bad config key); `--seed` ignored → `_load_cfg` must override before `validate_config`.
12. **Branch:** `feat/brahmanand-52-cli-train-resume`
13. **Commit:** `feat(cli): add train, resume and prune commands`
14. **PR title:** `feat: CLI train/resume/prune (SLA-05-BM-2)`
15. **Acceptance:** all three commands run on 4 laptops (Day 6); README section merged; reviewer: Vedant.

### Atharv Gundale

**Task ID:** SLA-05-AG-1
**Task Title:** CartPole DQN pilot runs, smoke test and debug checklist
**Priority:** P1
**Estimated Duration:** 11 h (learning 1, coding 5, testing 2, integration 2, docs 1)
**Dependencies:** Week-4 DQN; Brahmanand's `sla train` (#52, Day 4)
**Assigned Member:** Atharv Gundale (integration captain, Week 5)

1. **What:** `tests/integration/test_dqn_smoke.py`; 3 pilot runs of `configs/cartpole_dqn.yaml` (seeds 0, 1, 2); `docs/notes/dqn_debug_checklist.md`.
2. **Why:** unit tests prove the parts work; only a real run shows whether the DQN *learns*. Problems found now (Week 5) leave a week to fix them before the baseline (Week 6).
3. **Files:** `tests/integration/test_dqn_smoke.py`, `docs/notes/dqn_debug_checklist.md`.
4. **Functions/classes:** uses `run_training`, `DQNAgent.last_loss`, `last_max_q`.
5. **Inputs:** `configs/cartpole_dqn.yaml` (600 episodes, lr 0.0005).
6. **Outputs:** pilot table (seed, episodes, last-50 mean training reward, wall-clock minutes, notes) in the checklist file.
7. **Steps:**
   1. Write the checklist skeleton (Section 5.3 outline).
   2. After #52 is merged, run seed 0; watch the summary line every `eval_every` episodes.
   3. Run seeds 1 and 2; time each run (`time sla train ...` on Linux/macOS; note start/end on Windows).
   4. Write `test_dqn_smoke.py`: 40 episodes with `learning_starts = 200`; it only checks that 40 episodes are stored and the logged losses are finite — **no performance claim**.
   5. Fill the pilot table with what you actually observed, including bad runs. If a run does not learn, write which checklist item you investigated.
   6. Mentor: explain to Somesh what a learning curve should look like for CartPole (noisy, rising) vs FrozenLake (0/1 rewards).
8. **Commands:**
   ```bash
   git checkout -b test/atharv-56-dqn-smoke
   sla train --config configs/cartpole_dqn.yaml --seed 0
   pytest -m smoke -v
   git add tests/integration/test_dqn_smoke.py docs/notes/dqn_debug_checklist.md
   git commit -m "test(dqn): add DQN smoke test and pilot debug checklist"
   git push -u origin test/atharv-56-dqn-smoke
   ```
9. **Tests:** `test_dqn_smoke_run` (markers `smoke` and `torch`; skipped automatically without PyTorch).
10. **Expected result:** smoke test passes in CI's smoke step; pilot table filled honestly. CartPole DQN often needs a few hundred episodes before rewards rise — a pilot that has not reached 500 is normal and is *not* a failure of the week.
11. **Common errors:** reward stuck near 10–20 → `learning_starts` larger than total steps, or ε never decays; loss explodes → check `grad_clip`, lr; very slow → check `train_freq` and that PyTorch uses CPU threads (`torch.get_num_threads()`).
12. **Branch:** `test/atharv-56-dqn-smoke`
13. **Commit:** `test(dqn): add DQN smoke test and pilot debug checklist`
14. **PR title:** `test: DQN smoke test + pilot notes (SLA-05-AG-1)`
15. **Acceptance:** smoke test green; 3 pilot runs recorded with real numbers; reviewer: Brahmanand.

### Vedant Biradar

**Task ID:** SLA-05-VB-1
**Task Title:** SQLite episode store (long-term memory)
**Priority:** P1
**Estimated Duration:** 7 h (learning 1, coding 3, testing 2, integration 1)
**Dependencies:** `EpisodeInfo` field names (Week-4 runner); design §G
**Assigned Member:** Vedant Biradar

1. **What:** `src/sla/memory/episode_store.py` — `SCHEMA`, `EpisodeStore` (write: `start_run`, `log_episode`, `log_eval`, `add_reflection`, `add_feedback`, `delete_run`; read: `list_runs`, `get_run`, `query_episodes`, `query_evals`, `query_reflections`, `get_reflection`, `query_feedback`) and `StoreCallback`.
2. **Why:** every later feature reads from here: plots (this week), evaluation history (Week 6), reflection facts and feedback (Week 7), dashboard (Week 7).
3. **Files:** `memory/episode_store.py`, `tests/unit/test_episode_store.py`, `tests/conftest.py` (add the W5 region with the `store` fixture).
4. **Functions/classes:** as item 1 (Section 5.4). The tables for evals, reflections and feedback are created **now**, so later weeks never change the schema.
5. **Inputs:** run metadata, `EpisodeInfo` objects, evaluation results, notes, ratings.
6. **Outputs:** `runs/episodes.db`; pandas DataFrames for reading.
7. **Steps:**
   1. Learn: `sqlite3.connect`, parameter placeholders `?` (never f-strings in SQL — prevents SQL injection), `PRAGMA foreign_keys = ON`, `ON DELETE CASCADE`.
   2. Write `SCHEMA` (5 tables + indexes) exactly as Section 5.4.
   3. Write `_connect` as a context manager (commits on success, rolls back on error, always closes).
   4. Write the write methods, then the read methods.
   5. Write `StoreCallback` (`on_run_start` → `start_run`; `on_episode_end` → `log_episode`).
   6. Add the `store` fixture (W5 region of `tests/conftest.py`) and write 6 tests.
   7. PR #53 by Day 2; merge Day 3.
8. **Commands:**
   ```bash
   git checkout -b feat/vedant-53-episode-store
   pytest tests/unit/test_episode_store.py -v --cov=sla.memory.episode_store --cov-report=term-missing
   git add src/sla/memory/episode_store.py tests/unit/test_episode_store.py tests/conftest.py
   git commit -m "feat(memory): add SQLite episode store and store callback"
   git push -u origin feat/vedant-53-episode-store
   ```
9. **Tests:** data persists after reopening; 1000 episodes written and read back exactly; foreign key enforced; evals/reflections/feedback round trip; delete cascades; prune dry run deletes nothing.
10. **Expected result:** `6 passed`; coverage ≥ 85 %.
11. **Common errors:** `sqlite3.OperationalError: database is locked` → a connection left open (always use `with self._connect()`); foreign keys silently ignored → `PRAGMA foreign_keys = ON` must run on *every* connection; `IntegrityError: UNIQUE` → the same run id started twice.
12. **Branch:** `feat/vedant-53-episode-store`
13. **Commit:** `feat(memory): add SQLite episode store and store callback`
14. **PR title:** `feat: SQLite episode store (SLA-05-VB-1)`
15. **Acceptance:** tests pass in CI; Brahmanand's CLI and Somesh's plots use it; reviewer: Atharv.

**Task ID:** SLA-05-VB-2
**Task Title:** Retention (pruning old runs) and data-handling document
**Priority:** P2
**Estimated Duration:** 4 h (coding 2, testing 1, docs 1)
**Dependencies:** SLA-05-VB-1
**Assigned Member:** Vedant Biradar

1. **What:** `src/sla/memory/retention.py` (`find_old_runs`, `prune_runs(..., dry_run=True)`) and `docs/data_handling.md`.
2. **Why:** keeps laptops from filling up; documents what data we store (no personal data, only numbers and optional comments).
3. **Files:** `memory/retention.py`, `docs/data_handling.md` (test is in `test_episode_store.py`: `test_prune_dry_run_deletes_nothing`).
4. **Functions:** `find_old_runs(store, older_than_days) -> list[str]`; `prune_runs(store, older_than_days, run_root, dry_run=True) -> list[str]`.
5. **Inputs:** age in days.
6. **Outputs:** list of run ids that would be (or were) deleted; database rows and run folders removed only when `dry_run=False`.
7. **Steps:** write both functions → add the dry-run test → write the doc (outline Section 5.4) → PR #54.
8. **Commands:** branch `feat/vedant-54-retention`; `pytest tests/unit/test_episode_store.py -k prune -v`; commit; push.
9. **Tests:** dry run deletes nothing.
10. **Expected result:** `sla prune --older-than 30` prints "Would delete …" and deletes nothing.
11. **Common errors:** deleting the folder before the DB row → if the DB delete fails you have orphan rows; we delete the DB row first, then the folder.
12. **Branch:** `feat/vedant-54-retention`
13. **Commit:** `feat(memory): add dry-run-first retention for old runs`
14. **PR title:** `feat: retention + data handling doc (SLA-05-VB-2)`
15. **Acceptance:** dry run is the default; doc reviewed by Brahmanand.

### Somesh Badwane

**Task ID:** SLA-05-SB-1
**Task Title:** Learning-curve plots from stored data
**Priority:** P2
**Estimated Duration:** 11 h (learning 2, coding 5, testing 2, review 1, docs 1)
**Dependencies:** your `rolling_mean` (Week 4); Vedant's store (#53) for the real-data demo
**Assigned Member:** Somesh Badwane

**0. Learn first (Section 5.5, ~2 h):** what a pandas DataFrame is (a table with named columns), reading one column (`df["total_reward"]`), matplotlib's `Figure` object (`fig = Figure(); ax = fig.subplots()`), labels and saving with `fig.savefig`, and why we use `Figure` directly instead of `pyplot` (it never opens a window, so it works in tests, CI and Streamlit).

1. **What:** `src/sla/evaluation/plots.py` — `plot_learning_curve`, `plot_seed_band`, `plot_eval_curve`.
2. **Why:** the learning curve is the single most important picture in the report and the viva — it *shows* the agent improving. Week 7's dashboard calls your functions directly.
3. **Files:** create `evaluation/plots.py`, `tests/unit/test_plots.py`.
4. **Functions:** as item 1; each returns a matplotlib `Figure` and optionally saves a PNG.
5. **Inputs:** DataFrames from `EpisodeStore.query_episodes` (columns `episode`, `total_reward`, …) and `query_evals`.
6. **Outputs:** `Figure` objects; PNG files when `out_path` is given.
7. **Steps:**
   1. Do the Section 5.5 exercises.
   2. Write `plot_learning_curve` first: raw rewards in light colour, `rolling_mean` on top, axis labels, title, legend.
   3. Add the check that rejects an empty DataFrame or one without the needed columns (`ValueError` with a clear message).
   4. Write `plot_seed_band` (mean line + min–max shaded band over seeds) and `plot_eval_curve`.
   5. Write 4 tests using `tmp_path` (the files must exist and have labels).
   6. When Vedant's store is merged, plot your own FrozenLake run (Section 5.5 example); share the PNG in the team chat (do **not** commit PNGs from `runs/`).
   7. Open PR #55; reviewer Vedant.
8. **Commands:**
   ```bash
   git checkout main && git pull
   git checkout -b feat/somesh-55-plots
   pytest tests/unit/test_plots.py -v
   ruff check src/sla/evaluation tests/unit
   git add src/sla/evaluation/plots.py tests/unit/test_plots.py
   git commit -m "feat(evaluation): add learning-curve, seed-band and eval plots"
   git push -u origin feat/somesh-55-plots
   ```
9. **Tests:** learning curve saved with labels; bad DataFrame rejected; seed band; eval curve.
10. **Expected result:** `4 passed`.
11. **Common errors:** `TclError: no display` / a window pops up during tests → you used `pyplot`; build a `matplotlib.figure.Figure` directly as in Section 5.5; `ValueError: df must contain ...` → wrong column name, print `df.columns`; `FileNotFoundError` on save → the parent folder is missing (the code creates it with `mkdir(parents=True)`).
12. **Branch:** `feat/somesh-55-plots`
13. **Commit:** `feat(evaluation): add learning-curve, seed-band and eval plots`
14. **PR title:** `feat: learning-curve plots (SLA-05-SB-1)`
15. **Acceptance:** tests pass; a real learning curve drawn from `runs/episodes.db` shown in the Day-7 demo; reviewer: Vedant.

**How to make the PR:** as in Weeks 1–4; label `week-5`, reviewer Vedant, `Closes #55`. In the description paste the `pytest` output and attach your learning-curve PNG as an image (drag it into the PR text box).

**Independent practice exercise:** add an optional `ylabel` argument to a *copy* of `plot_learning_curve` in a scratch file, and draw your FrozenLake run with the label "Reached goal (1) or not (0)". Show Atharv; do not commit.

---

## SECTION 5 — COMPLETE TECHNICAL IMPLEMENTATION

### 5.1 Checkpoints and resume (Brahmanand)

`src/sla/agent/checkpoint.py` — key ideas: (1) `checkpoint.json` records which agent class to rebuild; (2) `latest.json` always points at the newest checkpoint; (3) `keep_last=3` deletes older folders; (4) `resume_training` passes `start_episode` to the unchanged Week-4 runner.
```python
"""Checkpoints: save and resume training (owner: Brahmanand, Week 5).

Layout inside a run folder:
    runs/<run_id>/checkpoints/ep_000049/   (meta.json + agent files)
    runs/<run_id>/checkpoints/latest.json  {"episode": 49, "path": "ep_000049"}
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sla.agent.base import Agent
from sla.agent.runner import Callback, EpisodeInfo, RunContext, RunResult, run_training
from sla.utils.config import load_config
from sla.utils.errors import CheckpointError
from sla.utils.io_helpers import read_json, write_json
from sla.utils.logging_setup import get_logger

log = get_logger(__name__)


def _agent_class(name: str) -> type[Agent]:
    if name == "random":
        from sla.agent.random_agent import RandomAgent
        return RandomAgent
    if name == "q_learning":
        from sla.learning.q_learning import QLearningAgent
        return QLearningAgent
    if name == "dqn":
        from sla.learning.dqn import DQNAgent
        return DQNAgent
    raise CheckpointError(f"Unknown agent type in checkpoint: {name!r}")


def save_checkpoint(agent: Agent, folder: Path, episode: int, extra: dict[str, Any] | None = None) -> Path:
    """Save the agent plus a small checkpoint.json describing it."""
    folder = Path(folder)
    try:
        agent.save(folder)
        write_json(folder / "checkpoint.json", {"agent": agent.name, "episode": episode, **(extra or {})})
    except OSError as exc:
        raise CheckpointError(f"Could not save checkpoint to {folder}: {exc}") from exc
    return folder


def load_checkpoint(folder: Path) -> tuple[Agent, dict[str, Any]]:
    """Return (agent, checkpoint_info) from a checkpoint folder."""
    folder = Path(folder)
    if not (folder / "checkpoint.json").is_file():
        raise CheckpointError(f"No checkpoint found at {folder}")
    info = read_json(folder / "checkpoint.json")
    try:
        agent = _agent_class(info["agent"]).load(folder)
    except (OSError, KeyError, ValueError) as exc:
        raise CheckpointError(f"Checkpoint at {folder} is incomplete or corrupt: {exc}") from exc
    return agent, info


def latest_checkpoint(run_dir: Path) -> Path:
    """Folder of the most recent checkpoint in a run."""
    pointer = Path(run_dir) / "checkpoints" / "latest.json"
    if not pointer.is_file():
        raise CheckpointError(f"No checkpoints in {run_dir}")
    return pointer.parent / read_json(pointer)["path"]


class CheckpointCallback(Callback):
    """Saves a checkpoint every ``every`` episodes and at the end of the run."""

    def __init__(self, every: int, keep_last: int = 3) -> None:
        if every <= 0:
            raise ValueError("every must be > 0")
        self.every = every
        self.keep_last = keep_last
        self.saved: list[Path] = []

    def _save(self, ctx: RunContext, episode: int) -> None:
        name = f"ep_{episode:06d}"
        folder = save_checkpoint(ctx.agent, ctx.run_dir / "checkpoints" / name, episode)
        write_json(ctx.run_dir / "checkpoints" / "latest.json", {"episode": episode, "path": name})
        self.saved.append(folder)
        log.info("Saved checkpoint %s", folder)
        self._cleanup()

    def _cleanup(self) -> None:
        """Keep only the newest ``keep_last`` periodic checkpoints (best/ is never deleted)."""
        import shutil
        while len(self.saved) > self.keep_last:
            old = self.saved.pop(0)
            shutil.rmtree(old, ignore_errors=True)

    def on_episode_end(self, ctx: RunContext, info: EpisodeInfo) -> bool:
        if (info.episode + 1) % self.every == 0:
            self._save(ctx, info.episode)
        return False

    def on_run_end(self, ctx: RunContext, result: RunResult) -> None:
        last_episode = result.episodes_completed - 1
        if last_episode >= 0 and (last_episode + 1) % self.every != 0:
            self._save(ctx, last_episode)


def resume_training(run_dir: Path, callbacks: list[Callback] | None = None) -> RunResult:
    """Continue a run from its latest checkpoint, keeping the same run id and folder."""
    run_dir = Path(run_dir)
    cfg = load_config(run_dir / "config.yaml")
    agent, info = load_checkpoint(latest_checkpoint(run_dir))
    start = int(info["episode"]) + 1
    if start >= cfg.episodes:
        raise CheckpointError(f"Run {run_dir.name} already finished all {cfg.episodes} episodes")
    log.info("Resuming %s from episode %d", run_dir.name, start)
    return run_training(cfg, callbacks, agent=agent, run_dir=run_dir, run_id=run_dir.name,
                        start_episode=start)
```

`tests/integration/test_resume.py`
```python
from sla.agent.checkpoint import CheckpointCallback, latest_checkpoint, load_checkpoint, resume_training
from sla.agent.runner import Callback, run_training
from sla.memory.episode_store import StoreCallback


class StopAt(Callback):
    def __init__(self, episode):
        self.episode = episode

    def on_episode_end(self, ctx, info):
        return info.episode >= self.episode


def test_resume_continues_episode_count(fl_cfg, store):
    fl_cfg.episodes = 200
    first = run_training(fl_cfg, [StoreCallback(store), CheckpointCallback(50), StopAt(119)])
    assert first.episodes_completed == 120
    ck, info = load_checkpoint(latest_checkpoint(first.run_dir))
    assert info["episode"] == 119
    resumed = resume_training(first.run_dir, [StoreCallback(store), CheckpointCallback(50)])
    assert resumed.episodes_completed == 200 and len(resumed.returns) == 80
    assert len(store.query_episodes(first.run_id)) == 200


def test_resumed_run_matches_uninterrupted_run(fl_cfg, store, tmp_path):
    """Q-learning + per-episode reset seeds: stop/resume gives the same returns as one long run."""
    fl_cfg.episodes = 150
    full = run_training(fl_cfg, run_dir=tmp_path / "full")
    part = run_training(fl_cfg, [CheckpointCallback(50), StopAt(99)], run_dir=tmp_path / "part")
    rest = resume_training(part.run_dir, [CheckpointCallback(50)])
    assert part.returns + rest.returns == full.returns
```

### 5.2 CLI — Week-5 version (Brahmanand)

Save this as `src/sla/cli.py` (it **replaces** the Week-3 skeleton). Week 6 changes `_callbacks` and `cmd_train` and appends an `evaluate` region; Week 7 appends a third region. `build_parser` and `main` never change again.
```python
"""Command-line interface: `sla <command>` (owner: Brahmanand).

Week 5 version: train, resume, prune.
"""

from __future__ import annotations

import argparse
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
    """Week 5 version: store every episode and save checkpoints."""
    from sla.agent.checkpoint import CheckpointCallback
    from sla.memory.episode_store import StoreCallback
    return [StoreCallback(store), CheckpointCallback(cfg.checkpoint_every)]


def cmd_train(args: argparse.Namespace) -> int:
    from sla.agent.runner import run_training
    from sla.memory.episode_store import EpisodeStore
    from sla.utils.logging_setup import setup_logging
    cfg = _load_cfg(args)
    setup_logging()
    result = run_training(cfg, _callbacks(cfg, EpisodeStore(args.db)))
    last = result.returns[-50:]
    print(f"Run id: {result.run_id}  ({result.stopped_reason}, {result.episodes_completed} episodes)")
    print(f"Mean training reward of the last {len(last)} episodes: {sum(last) / len(last):.2f}")
    print(f"Folder: {result.run_dir}")
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

README "Command line" section to add:
```markdown
## Command line
| Command | What it does | Example |
|---|---|---|
| `sla train` | train an agent from a YAML config | `sla train --config configs/frozenlake_q.yaml --seed 0` |
| `sla resume` | continue a stopped run from its latest checkpoint | `sla resume --run runs/<run_id>` |
| `sla prune` | list (or with `--yes` delete) runs older than N days | `sla prune --older-than 30` |
```

### 5.3 DQN smoke test and debug checklist (Atharv)

`tests/integration/test_dqn_smoke.py`
```python
"""Week 5 (Atharv): a short DQN run on CartPole must finish, log and stay finite."""

import math

import pytest

pytest.importorskip("torch")

from sla.agent.runner import run_training  # noqa: E402
from sla.memory.episode_store import StoreCallback  # noqa: E402
from sla.utils.config import load_config  # noqa: E402

pytestmark = [pytest.mark.smoke, pytest.mark.torch]


def test_dqn_smoke_run(tmp_path, store):
    cfg = load_config("configs/cartpole_dqn.yaml")
    cfg.episodes = 40
    cfg.run_root = str(tmp_path / "runs")
    cfg.dqn.learning_starts = 200
    result = run_training(cfg, [StoreCallback(store)])
    episodes = store.query_episodes(result.run_id)
    assert len(episodes) == 40
    losses = episodes["mean_loss"].dropna()
    assert not losses.empty and all(math.isfinite(v) for v in losses)
```

`docs/notes/dqn_debug_checklist.md` outline:
```markdown
# DQN debug checklist (CartPole)
## Pilot runs (fill with observed values only)
| Seed | Episodes | Last-50 mean training reward | Minutes | Notes |
|---|---|---|---|---|
| 0 | | | | |
| 1 | | | | |
| 2 | | | | |
## If the agent does not learn, check in this order
1. Is epsilon decaying? (print agent.epsilon every 50 episodes)
2. Has training started? total steps > learning_starts?
3. Is the loss finite and not exploding? (agent.last_loss)
4. Is max Q growing without limit? (agent.last_max_q > 1e4 -> divergence)
5. Is the target network syncing? (target_update_every)
6. Terminated vs truncated: truncation at 500 steps must NOT zero the target.
7. Learning rate: try 0.0005 -> 0.00025 (change one thing at a time, note it here).
## Changes tried (date, change, result)
```

### 5.4 Episode store and retention (Vedant)

`src/sla/memory/episode_store.py` — five tables (`runs`, `episodes`, `evals`, `reflections`, `feedback`) with foreign keys and `ON DELETE CASCADE`; every SQL statement uses `?` placeholders.
```python
"""SQLite episode store: the agent's long-term memory (owner: Vedant, Week 5).

One database file (default runs/episodes.db) holds every run, episode,
evaluation, reflection note and user rating. Always use parameterised SQL
("?" placeholders), never string formatting, to avoid SQL injection.
"""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from sla.agent.runner import Callback, EpisodeInfo, RunContext
from sla.utils.errors import StoreError

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    run_id      TEXT PRIMARY KEY,
    env         TEXT NOT NULL,
    agent       TEXT NOT NULL,
    seed        INTEGER NOT NULL,
    config_json TEXT NOT NULL,
    git_sha     TEXT,
    started_at  TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS episodes (
    run_id      TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    episode     INTEGER NOT NULL,
    total_reward REAL NOT NULL,
    length      INTEGER NOT NULL,
    epsilon     REAL,
    mean_loss   REAL,
    end_reason  TEXT,
    wall_time_s REAL,
    PRIMARY KEY (run_id, episode)
);
CREATE TABLE IF NOT EXISTS evals (
    run_id      TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    checkpoint_episode INTEGER NOT NULL,
    mean_return REAL NOT NULL,
    std_return  REAL NOT NULL,
    success_rate REAL,
    n_episodes  INTEGER NOT NULL,
    created_at  TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS reflections (
    note_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id      TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    facts_json  TEXT NOT NULL,
    note_text   TEXT NOT NULL,
    source      TEXT NOT NULL,
    grounding_passed INTEGER NOT NULL,
    grounding_report TEXT,
    created_at  TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    note_id     INTEGER NOT NULL REFERENCES reflections(note_id) ON DELETE CASCADE,
    accurate    INTEGER NOT NULL,
    usefulness  INTEGER NOT NULL,
    comment     TEXT,
    created_at  TEXT NOT NULL
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class EpisodeStore:
    def __init__(self, db_path: str | Path = "runs/episodes.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as con:
            con.executescript(SCHEMA)

    @contextmanager
    def _connect(self):
        try:
            con = sqlite3.connect(self.db_path, timeout=10)
        except sqlite3.Error as exc:
            raise StoreError(f"Cannot open database {self.db_path}: {exc}") from exc
        con.execute("PRAGMA foreign_keys = ON")
        con.row_factory = sqlite3.Row
        try:
            yield con
            con.commit()
        except sqlite3.Error as exc:
            con.rollback()
            raise StoreError(f"Database error in {self.db_path}: {exc}") from exc
        finally:
            con.close()

    # ----- writing --------------------------------------------------------
    def start_run(self, run_id: str, env: str, agent: str, seed: int, config: dict[str, Any],
                  git_sha: str | None = None) -> None:
        with self._connect() as con:
            con.execute("INSERT OR IGNORE INTO runs VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (run_id, env, agent, seed, json.dumps(config), git_sha, _now()))

    def log_episode(self, run_id: str, info: EpisodeInfo) -> None:
        with self._connect() as con:
            con.execute("INSERT OR REPLACE INTO episodes VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (run_id, info.episode, info.total_reward, info.length, info.epsilon,
                         info.mean_loss, info.end_reason, info.wall_time_s))

    def log_eval(self, run_id: str, checkpoint_episode: int, mean_return: float, std_return: float,
                 success_rate: float | None, n_episodes: int) -> None:
        with self._connect() as con:
            con.execute("INSERT INTO evals VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (run_id, checkpoint_episode, mean_return, std_return, success_rate, n_episodes, _now()))

    def add_reflection(self, run_id: str, facts: dict[str, Any], note_text: str, source: str,
                       grounding_passed: bool, grounding_report: dict[str, Any] | None = None) -> int:
        with self._connect() as con:
            cur = con.execute(
                "INSERT INTO reflections (run_id, facts_json, note_text, source, grounding_passed, "
                "grounding_report, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (run_id, json.dumps(facts), note_text, source, int(grounding_passed),
                 json.dumps(grounding_report or {}), _now()))
            return int(cur.lastrowid)

    def add_feedback(self, note_id: int, accurate: bool, usefulness: int, comment: str | None) -> int:
        with self._connect() as con:
            cur = con.execute(
                "INSERT INTO feedback (note_id, accurate, usefulness, comment, created_at) VALUES (?, ?, ?, ?, ?)",
                (note_id, int(accurate), usefulness, comment, _now()))
            return int(cur.lastrowid)

    def delete_run(self, run_id: str) -> None:
        with self._connect() as con:
            con.execute("DELETE FROM runs WHERE run_id = ?", (run_id,))

    # ----- reading --------------------------------------------------------
    def _df(self, sql: str, params: tuple = ()) -> pd.DataFrame:
        with self._connect() as con:
            return pd.read_sql_query(sql, con, params=params)

    def list_runs(self) -> pd.DataFrame:
        return self._df("SELECT * FROM runs ORDER BY started_at DESC")

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        with self._connect() as con:
            row = con.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
        return dict(row) if row else None

    def query_episodes(self, run_id: str) -> pd.DataFrame:
        return self._df("SELECT * FROM episodes WHERE run_id = ? ORDER BY episode", (run_id,))

    def query_evals(self, run_id: str) -> pd.DataFrame:
        return self._df("SELECT * FROM evals WHERE run_id = ? ORDER BY checkpoint_episode", (run_id,))

    def query_reflections(self, run_id: str | None = None) -> pd.DataFrame:
        if run_id is None:
            return self._df("SELECT * FROM reflections ORDER BY note_id DESC")
        return self._df("SELECT * FROM reflections WHERE run_id = ? ORDER BY note_id DESC", (run_id,))

    def get_reflection(self, note_id: int) -> dict[str, Any] | None:
        with self._connect() as con:
            row = con.execute("SELECT * FROM reflections WHERE note_id = ?", (note_id,)).fetchone()
        return dict(row) if row else None

    def query_feedback(self, note_id: int | None = None) -> pd.DataFrame:
        if note_id is None:
            return self._df("SELECT * FROM feedback ORDER BY feedback_id")
        return self._df("SELECT * FROM feedback WHERE note_id = ? ORDER BY feedback_id", (note_id,))


class StoreCallback(Callback):
    """Runner callback: records the run and every episode in the store."""

    def __init__(self, store: EpisodeStore, git_sha: str | None = None) -> None:
        self.store = store
        self.git_sha = git_sha

    def on_run_start(self, ctx: RunContext) -> None:
        self.store.start_run(ctx.run_id, ctx.cfg.env_name, ctx.cfg.agent, ctx.cfg.seed,
                             ctx.cfg.to_dict(), self.git_sha)

    def on_episode_end(self, ctx: RunContext, info: EpisodeInfo) -> bool:
        self.store.log_episode(ctx.run_id, info)
        return False
```

`src/sla/memory/retention.py`
```python
"""Data retention: delete old runs on purpose, never by accident (owner: Vedant, Week 5)."""

from __future__ import annotations

import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

from sla.memory.episode_store import EpisodeStore


def find_old_runs(store: EpisodeStore, older_than_days: int) -> list[str]:
    if older_than_days < 0:
        raise ValueError("older_than_days must be >= 0")
    cutoff = datetime.now(timezone.utc) - timedelta(days=older_than_days)
    runs = store.list_runs()
    old = []
    for _, row in runs.iterrows():
        started = datetime.fromisoformat(row["started_at"])
        if started < cutoff:
            old.append(row["run_id"])
    return old


def prune_runs(store: EpisodeStore, older_than_days: int, run_root: str | Path = "runs",
               dry_run: bool = True) -> list[str]:
    """Return the runs that are (or would be) deleted.

    With dry_run=True (the default) nothing is deleted; the list shows what
    *would* be removed so the user can check first.
    """
    targets = find_old_runs(store, older_than_days)
    if dry_run:
        return targets
    for run_id in targets:
        store.delete_run(run_id)  # ON DELETE CASCADE removes episodes, evals, notes, feedback
        folder = Path(run_root) / run_id
        if folder.is_dir():
            shutil.rmtree(folder)
    return targets
```

`tests/conftest.py` — add this W5 region **below** Brahmanand's W4 region (one owner per region avoids merge conflicts):
```python
@pytest.fixture
def store(tmp_path):
    from sla.memory.episode_store import EpisodeStore
    return EpisodeStore(tmp_path / "test.db")
```

`tests/unit/test_episode_store.py`
```python
import pytest

from sla.agent.runner import EpisodeInfo
from sla.memory.episode_store import EpisodeStore
from sla.memory.retention import prune_runs
from sla.utils.errors import StoreError


def info(ep, reward=1.0):
    return EpisodeInfo(ep, reward, 10, 0.5, None, "hole", 0.01)


def test_run_and_episodes_persist_after_reopen(tmp_path):
    db = tmp_path / "e.db"
    s = EpisodeStore(db)
    s.start_run("r1", "FrozenLake-v1", "q_learning", 0, {"a": 1})
    for ep in range(10):
        s.log_episode("r1", info(ep, float(ep)))
    again = EpisodeStore(db)  # like restarting the program
    df = again.query_episodes("r1")
    assert len(df) == 10 and df["total_reward"].tolist() == [float(i) for i in range(10)]


def test_retrieval_accuracy_1000_rows(store):
    store.start_run("r", "CartPole-v1", "dqn", 1, {})
    for ep in range(1000):
        store.log_episode("r", info(ep, ep * 0.5))
    df = store.query_episodes("r")
    assert (df["total_reward"] == df["episode"] * 0.5).all() and len(df) == 1000


def test_foreign_key_enforced(store):
    with pytest.raises(StoreError):
        store.log_episode("no_such_run", info(0))


def test_evals_reflections_feedback(store):
    store.start_run("r", "CartPole-v1", "dqn", 0, {})
    store.log_eval("r", 49, 20.0, 3.0, 0.0, 20)
    note = store.add_reflection("r", {"x": 1}, "text", "template", True)
    store.add_feedback(note, True, 4, "nice")
    assert len(store.query_evals("r")) == 1
    assert store.get_reflection(note)["note_text"] == "text"
    assert store.query_feedback(note)["usefulness"].tolist() == [4]


def test_delete_cascades(store):
    store.start_run("r", "CartPole-v1", "dqn", 0, {})
    store.log_episode("r", info(0))
    store.delete_run("r")
    assert store.query_episodes("r").empty


def test_prune_dry_run_deletes_nothing(store, tmp_path):
    store.start_run("old", "CartPole-v1", "dqn", 0, {})
    targets = prune_runs(store, older_than_days=0, run_root=tmp_path, dry_run=True)
    assert targets == ["old"] and store.get_run("old") is not None
    prune_runs(store, older_than_days=0, run_root=tmp_path, dry_run=False)
    assert store.get_run("old") is None
```

`docs/data_handling.md` outline:
```markdown
# Data handling
- What we store: run settings, per-episode numbers, evaluation numbers, explanation notes, optional ratings/comments.
- What we do NOT store: personal data, passwords, API keys (none are used).
- Where: runs/episodes.db (SQLite, local only) and runs/<run_id>/ (checkpoints, logs). Both git-ignored.
- Retention: `sla prune --older-than N` (dry run by default; `--yes` deletes DB rows first, then folders).
- Backups: copy runs/episodes.db before final experiments (Week 8).
- Comments are cleaned (length limit, control characters removed) before saving (Week 6, Somesh).
```

### 5.5 Plots (Somesh)

**Lesson (read before coding):**
```python
import pandas as pd
df = pd.DataFrame({"episode": [0, 1, 2], "total_reward": [0.0, 1.0, 1.0]})  # a small table
df["total_reward"]            # one column (a "Series")
df["total_reward"].mean()     # 0.666...
list(df.columns)              # ['episode', 'total_reward']

from matplotlib.figure import Figure   # the object-oriented API: never opens a window
fig = Figure(figsize=(6, 4))  # fig = the whole picture
ax = fig.subplots()           # ax = one chart inside it
ax.plot([0, 1, 2], [0, 1, 1], label="reward")
ax.set_xlabel("Episode"); ax.set_ylabel("Reward"); ax.legend()
fig.savefig("example.png")   # write a PNG file
```
Mini-exercises: (a) make a DataFrame with 5 episodes and print the mean of the last 3 rewards (`.tail(3)`); (b) plot `y = x*x` for x in 0..9 with labels; (c) plot two lines on the same `ax` with a legend.

`src/sla/evaluation/plots.py`
```python
"""Learning-curve plots (owner: Somesh, Week 5).

Uses matplotlib's object-oriented Figure API (no pyplot), so it works the same
in scripts, tests and Streamlit without opening windows.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib.figure import Figure

from sla.utils.summary import rolling_mean


def plot_learning_curve(df: pd.DataFrame, window: int = 50, title: str = "Learning curve",
                        out_path: str | Path | None = None) -> Figure:
    """Plot reward per episode (faint) and its rolling mean (bold).

    ``df`` needs the columns 'episode' and 'total_reward' (as returned by
    EpisodeStore.query_episodes).
    """
    if df.empty or not {"episode", "total_reward"} <= set(df.columns):
        raise ValueError("df must contain non-empty 'episode' and 'total_reward' columns")
    fig = Figure(figsize=(8, 4.5))
    ax = fig.subplots()
    ax.plot(df["episode"], df["total_reward"], alpha=0.3, label="reward per episode")
    ax.plot(df["episode"], rolling_mean(df["total_reward"].tolist(), window), linewidth=2,
            label=f"rolling mean ({window})")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Total reward")
    ax.set_title(title)
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    if out_path is not None:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=120)
    return fig


def plot_seed_band(curves: dict[int, pd.DataFrame], window: int = 50, title: str = "Learning curve (all seeds)",
                   out_path: str | Path | None = None) -> Figure:
    """Mean rolling reward across seeds with a min–max band."""
    if not curves:
        raise ValueError("curves must not be empty")
    length = min(len(df) for df in curves.values())
    if length == 0:
        raise ValueError("every curve needs at least one episode")
    smoothed = np.array([rolling_mean(df["total_reward"].tolist()[:length], window) for df in curves.values()])
    x = np.arange(length)
    fig = Figure(figsize=(8, 4.5))
    ax = fig.subplots()
    ax.plot(x, smoothed.mean(axis=0), linewidth=2, label=f"mean over {len(curves)} seeds")
    ax.fill_between(x, smoothed.min(axis=0), smoothed.max(axis=0), alpha=0.25, label="min–max")
    ax.set_xlabel("Episode")
    ax.set_ylabel(f"Rolling mean reward ({window})")
    ax.set_title(title)
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    if out_path is not None:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=120)
    return fig


def plot_eval_curve(evals: pd.DataFrame, title: str = "Frozen-policy evaluation",
                    out_path: str | Path | None = None) -> Figure:
    """Evaluation mean ± std at each checkpoint (columns from EpisodeStore.query_evals)."""
    if evals.empty:
        raise ValueError("evals is empty")
    fig = Figure(figsize=(8, 4.5))
    ax = fig.subplots()
    ax.errorbar(evals["checkpoint_episode"], evals["mean_return"], yerr=evals["std_return"],
                marker="o", capsize=3)
    ax.set_xlabel("Training episode")
    ax.set_ylabel("Mean evaluation return")
    ax.set_title(title)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    if out_path is not None:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=120)
    return fig
```

**Line by line (key parts):** `from matplotlib.figure import Figure` (no `pyplot`) makes the module safe in tests, CI and Streamlit · the first `if` raises a `ValueError` with a clear message when the table is empty or a column is missing (a clear message beats a `KeyError`) · `alpha=0.3` makes raw rewards faint so the rolling mean stands out · the seed band shades the area between the lowest and highest seed at each episode · `if out_path is not None:` saves only when asked, and the function always *returns* the figure so Streamlit can show it with `st.pyplot(fig)` in Week 7.

`tests/unit/test_plots.py`
```python
import pandas as pd
import pytest

from sla.evaluation.plots import plot_eval_curve, plot_learning_curve, plot_seed_band


@pytest.fixture
def df():
    return pd.DataFrame({"episode": range(100), "total_reward": [i % 10 for i in range(100)]})


def test_learning_curve_saved_with_labels(df, tmp_path):
    out = tmp_path / "plots" / "curve.png"
    fig = plot_learning_curve(df, window=10, title="test", out_path=out)
    ax = fig.axes[0]
    assert out.exists() and out.stat().st_size > 0
    assert ax.get_xlabel() == "Episode" and ax.get_ylabel() == "Total reward" and ax.get_title() == "test"


def test_learning_curve_rejects_bad_df():
    with pytest.raises(ValueError):
        plot_learning_curve(pd.DataFrame({"x": [1]}))


def test_seed_band(df, tmp_path):
    fig = plot_seed_band({0: df, 1: df}, window=5, out_path=tmp_path / "band.png")
    assert (tmp_path / "band.png").exists() and len(fig.axes) == 1


def test_eval_curve(tmp_path):
    evals = pd.DataFrame({"checkpoint_episode": [49, 99], "mean_return": [10.0, 50.0], "std_return": [2.0, 5.0]})
    plot_eval_curve(evals, out_path=tmp_path / "eval.png")
    assert (tmp_path / "eval.png").exists()
```

Plot your own run from the database (run in a Python shell after Day 4; do not commit the PNG):
```python
from sla.memory.episode_store import EpisodeStore
from sla.evaluation.plots import plot_learning_curve
store = EpisodeStore("runs/episodes.db")
run_id = store.list_runs()["run_id"].iloc[-1]      # newest run
plot_learning_curve(store.query_episodes(run_id), window=50, title=run_id, out_path="runs/my_curve.png")
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
│   │   ├── dqn_debug_checklist.md   [NEW · Atharv]
│   │   ├── dqn_explained.md
│   │   └── q_learning_by_hand.md
│   ├── architecture.md
│   ├── data_handling.md   [NEW · Vedant]
│   ├── design.md
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
├── scripts/
│   ├── hardware_check.py
│   └── quick_frozenlake_check.py
├── spikes/
│   └── llm_benchmark.py
├── src/
│   └── sla/
│       ├── agent/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── checkpoint.py   [NEW · Brahmanand]
│       │   ├── random_agent.py
│       │   ├── runner.py
│       │   └── safety.py
│       ├── envs/
│       │   ├── __init__.py
│       │   └── factory.py
│       ├── evaluation/
│       │   ├── __init__.py
│       │   └── plots.py   [NEW · Somesh]
│       ├── learning/
│       │   ├── __init__.py
│       │   ├── dqn.py
│       │   ├── networks.py
│       │   ├── q_learning.py
│       │   └── schedules.py
│       ├── memory/
│       │   ├── __init__.py
│       │   ├── episode_store.py   [NEW · Vedant]
│       │   ├── replay_buffer.py
│       │   └── retention.py   [NEW · Vedant]
│       ├── reflection/
│       │   └── __init__.py
│       ├── ui/
│       │   └── __init__.py
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
│       └── cli.py   [MODIFIED · Brahmanand]
├── tests/
│   ├── integration/
│   │   ├── test_dqn_smoke.py   [NEW · Atharv]
│   │   ├── test_resume.py   [NEW · Brahmanand]
│   │   └── test_runner.py
│   ├── unit/
│   │   ├── test_agents.py
│   │   ├── test_cli_help.py
│   │   ├── test_config.py
│   │   ├── test_dqn.py
│   │   ├── test_envs.py
│   │   ├── test_episode_store.py   [NEW · Vedant]
│   │   ├── test_io_helpers.py
│   │   ├── test_logging.py
│   │   ├── test_plots.py   [NEW · Somesh]
│   │   ├── test_q_learning.py
│   │   ├── test_replay_buffer.py
│   │   ├── test_safety.py
│   │   ├── test_schedules.py
│   │   ├── test_summary.py
│   │   └── test_validation.py
│   └── conftest.py   [MODIFIED · Brahmanand → Vedant]
├── .env.example
├── .gitignore
├── CONTRIBUTING.md
├── pyproject.toml
└── README.md   [MODIFIED · Atharv → Brahmanand]
```

Legend: [NEW] created this week · [MODIFIED] changed this week · no tag = carried over unchanged from an earlier week. `runs/` (training outputs) and `.venv/` exist on your laptop but are git-ignored, so they are not shown.

---

## SECTION 7 — GITHUB COLLABORATION PROCEDURE

13-step flow as every week (issue → assign → branch → pull → implement → test → stage → commit → push → PR → review → fix → merge). Week-5 issues:

| # | Title | Owner | Branch | Reviewer | Merge by |
|---|---|---|---|---|---|
| 51 | Checkpoints and exact resume | Brahmanand | `feat/brahmanand-51-checkpoint-resume` | Atharv | **Day 3** |
| 52 | CLI train / resume / prune | Brahmanand | `feat/brahmanand-52-cli-train-resume` | Vedant | **Day 4** |
| 53 | SQLite episode store | Vedant | `feat/vedant-53-episode-store` | Atharv | **Day 3** |
| 54 | Retention + data handling doc | Vedant | `feat/vedant-54-retention` | Brahmanand | Day 5 |
| 55 | Learning-curve plots | Somesh | `feat/somesh-55-plots` | Vedant | Day 6 |
| 56 | DQN smoke test + checklist | Atharv | `test/atharv-56-dqn-smoke` | Brahmanand | Day 6 |
| 58 | README command-line section | Brahmanand | (in #52 or `docs/brahmanand-58-readme-cli`) | Somesh | Day 6 |

**Rule for `tests/conftest.py`:** Brahmanand owns the W4 region, Vedant the W5 region. If both edit the file in the same week, the second PR rebases (`git rebase origin/main`) and keeps both regions.

**What must never be committed:** `runs/`, `*.db`, `*.pt`, `*.npz` — `.gitignore` (Week 1) already blocks them. Check with `git status` before `git add`.

---

## SECTION 8 — WEEKLY INTEGRATION PROCEDURE

| Item | This week |
|---|---|
| Modules to connect | runner ↔ `StoreCallback` + `CheckpointCallback`; checkpoints ↔ every agent's `save/load` (+ replay buffer); CLI ↔ config, runner, store, checkpoint, retention; plots ↔ store DataFrames + `rolling_mean`. |
| Integrator | **Atharv** (integration captain, Week 5). |
| Interfaces that must match | `Callback.on_run_start(ctx)`, `on_episode_end(ctx, info) -> bool`; `EpisodeInfo` fields → `episodes` table columns; `checkpoint.json` keys (`agent`, `episode`); `query_episodes` columns `episode`, `total_reward`, `length`, `epsilon`, `mean_loss`, `end_reason`, `wall_time_s`. |
| Callback order | `[StoreCallback, CheckpointCallback]` (Week 6 extends the list in `pipeline.default_callbacks`). |
| Tests that must pass | all, especially `test_resume.py`, `test_episode_store.py`, `test_plots.py`; smoke step in CI. |
| Detect failures | resumed returns differ from the uninterrupted run; `database is locked`; plots fail with `KeyError` on a column. |
| Debug | compare `checkpoint.json` and `latest.json` by eye; open `runs/episodes.db` in DB Browser for SQLite; `pytest path::test -x -vv`. |

**Integration checklist**
- [ ] `sla train` writes rows to the DB **and** checkpoints for Q-learning and DQN
- [ ] `sla resume` continues the episode numbering (no duplicate episode rows)
- [ ] Plot drawn from a real stored run
- [ ] Runner file unchanged this week (`git log -- src/sla/agent/runner.py` shows no Week-5 commit)
- [ ] CI green on `main`

---

## SECTION 9 — TESTING AND VALIDATION

| Type | Tests this week | Command |
|---|---|---|
| Unit | `test_episode_store` (6), `test_plots` (4) | `pytest tests/unit -v` |
| Integration | `test_resume` (2) | `pytest tests/integration/test_resume.py -v` |
| Smoke (needs torch) | `test_dqn_smoke` | `pytest -m smoke -v` |
| Data persistence | persist-after-reopen; 1000-row retrieval accuracy; cascade delete | in `test_episode_store.py` |
| Reproducibility | resumed run == uninterrupted run | `test_resumed_run_matches_uninterrupted_run` |
| Error handling | missing checkpoint → `CheckpointError`; bad DataFrame → `ValueError` | tests + manual CLI run |
| Performance | not measured yet (Week 8); note pilot wall-clock minutes only | — |

**RL rules applied this week:** pilot numbers are **training** rewards with exploration on — label them "training reward", never "accuracy" or "final result". The frozen-policy evaluation on separate seeds comes in Week 6. Record every pilot run, including ones that failed.

---

## SECTION 10 — COMMON PROBLEMS AND SOLUTIONS

| Problem | Possible Cause | How to Check | Solution |
|---|---|---|---|
| `sqlite3.OperationalError: database is locked` | connection not closed; DB open in DB Browser with unsaved changes | close DB Browser; search code for `sqlite3.connect` outside `_connect` | always `with self._connect() as con:`; close the viewer |
| Resumed run gives different numbers | RNG or step counter not saved | compare `meta.json` before/after | save `rng_state`, `steps`; reset env with `episode_seed` |
| `CheckpointError: no checkpoint found` | run stopped before first checkpoint | `ls runs/<id>/checkpoints` | lower `checkpoint_every` or train longer |
| Disk filling with checkpoints | `keep_last` not applied | count `ep_*` folders | `CheckpointCallback(every, keep_last=3)` |
| Duplicate episode rows after resume | resume restarted at episode 0 | `SELECT MAX(episode) FROM episodes WHERE run_id=?` | pass `start_episode` from `checkpoint.json` |
| Plot test opens a window / fails in CI | `pyplot` used instead of `Figure` | search for `pyplot` in `plots.py` | build `Figure()` directly (Section 5.5) |
| `sla: command not found` | package not installed in active venv | `which sla` / `where sla` | activate venv; `pip install -e ".[dev]"` |
| DQN pilot reward stays ~20 | not training yet / ε stuck | print `agent.epsilon`, total steps | check `learning_starts`, `epsilon_decay_steps` |
| Accidentally committed `runs/` | `.gitignore` edited | `git status` | `git rm -r --cached runs && git commit` |

---

## SECTION 11 — WEEKLY DELIVERABLES

| Deliverable | Owner | File/Location | Verification | Status |
|---|---|---|---|---|
| Checkpoints + resume | Brahmanand | `src/sla/agent/checkpoint.py` | `test_resume.py` 2 passed | [ ] |
| CLI train/resume/prune | Brahmanand | `src/sla/cli.py` | commands run on 4 laptops | [ ] |
| README command-line section | Brahmanand | `README.md` | merged | [ ] |
| Episode store + callback | Vedant | `src/sla/memory/episode_store.py`, `tests/conftest.py` | 6 tests pass | [ ] |
| Retention + data doc | Vedant | `src/sla/memory/retention.py`, `docs/data_handling.md` | dry-run test | [ ] |
| Learning-curve plots | Somesh | `src/sla/evaluation/plots.py` | 4 tests; real plot demoed | [ ] |
| DQN smoke test | Atharv | `tests/integration/test_dqn_smoke.py` | CI smoke step green | [ ] |
| Pilot runs + debug checklist | Atharv | `docs/notes/dqn_debug_checklist.md` | 3 runs with observed numbers | [ ] |

---

## SECTION 12 — WEEKLY REVIEW MEETING

**Agenda:** demo on fresh `main` (train → Ctrl+C → resume → plot from DB) · completed/pending tasks · blockers · code quality · test results · PRs · integration status · Week-6 dependencies.

**Questions:**
1. Brahmanand: why does a resumed run give *exactly* the same returns? Which two things make it possible?
2. What is inside `checkpoint.json` and `latest.json`, and why keep only 3 checkpoints?
3. Vedant: why use `?` placeholders instead of f-strings in SQL?
4. What does `ON DELETE CASCADE` do when we prune a run?
5. Somesh: why does `plots.py` use `Figure` instead of `pyplot`? What does the rolling mean show that raw rewards do not?
6. Atharv: what did the 3 pilot CartPole runs show? Which checklist item did you investigate first?
7. Short-term vs long-term memory in our agent — which module is which?
8. Which new callbacks arrive next week, and where will the callback list live?

---

## SECTION 13 — WEEK COMPLETION CHECKLIST

- [ ] All assigned tasks completed
- [ ] Code pushed to feature branches
- [ ] Pull requests reviewed and merged (#51, #53 first)
- [ ] All tests pass locally and in CI (including smoke step)
- [ ] Store, checkpoints and CLI integrated; runner unchanged
- [ ] README command-line section and `docs/data_handling.md` merged
- [ ] Weekly demonstration completed
- [ ] Blockers recorded (e.g. DQN pilot not learning yet)

---

## SECTION 14 — NEXT WEEK HANDOFF

- **Ready before Week 6:** merged `checkpoint.py`, `episode_store.py` (with `log_eval` and the `evals` table), `retention.py`, `plots.py` (including `plot_eval_curve`), Week-5 `cli.py`, DQN pilot notes.
- **Files Week 6 depends on:** `CheckpointCallback` (best-checkpoint saving builds on it), `EpisodeStore.log_eval` (periodic evaluation), `cli._callbacks` / `cmd_train` (replaced in Week 6), `configs/cartpole_dqn.yaml` (Atharv tunes it using the pilot notes).
- **Coordination:** Vedant (evaluator) and Atharv (guards) both read evaluation results — `RegressionMonitor` must run **after** `PeriodicEvalCallback`. Brahmanand moves the callback list into `pipeline.default_callbacks`. Somesh's transition validator becomes a callback too.
- **Risks:** DQN may still not learn reliably — Week 6 Day 1–2 is reserved for Atharv to apply the checklist before the 5-seed runs; database grows during experiments — use `sla prune` (dry run first).
