# WEEK 06 — Self-Learning and Reward Mechanism

**Project:** Self-Learning AI Agent · **Team:** Brahmanand Mathpati, Atharv Gundale, Vedant Biradar, Somesh Badwane
**Source:** *Self_Learning_AI_Agent_10_Week_Master_Plan* (v1.0) · **Interfaces:** `docs/design.md` (tag `w2-design-freeze`)

---

## SECTION 1 — WEEK OVERVIEW

| Item | Details |
|---|---|
| Week number | 6 of 10 |
| Week title | Self-Learning and Reward Mechanism |
| Main objective | Make "self-learning" **measurable and safe**: a frozen-policy **evaluator** on held-out seeds, automatic **best-checkpoint** selection, **guards** that stop divergence and flag regressions, **validation** of every reward/transition, and the first honest **5-seed** results compared with a **random baseline**. |
| Expected outcome | `sla train` now trains → evaluates periodically → keeps the best checkpoint → runs a final test evaluation and writes `metrics.json`; `sla evaluate --checkpoint ...` works; `results/baseline/baseline.csv` exists; 5 seeds of Q-learning (FrozenLake) and DQN (CartPole) trained with results recorded as observed. |
| Required knowledge | Week-2 theory: reward signal, return, exploration vs exploitation, why train and test must be separate (over-fitting to seeds). Week-5 callbacks, store, checkpoints. Basic statistics: mean, standard deviation, success rate. |
| Required tools | Same venv; no new dependency. |
| Prerequisites from previous weeks | Week 5 merged: `checkpoint.py`, `episode_store.py` (with `log_eval`, `evals` table), `plots.py`, Week-5 `cli.py`, DQN pilot notes. |
| Approximate workload | 11 h per member (5-seed DQN runs can run unattended overnight — start them early). |
| Technical dependencies | Vedant's `evaluate.py` merged by **Day 2** (pipeline, guards and baseline import it). Atharv's `guards.py` and Somesh's `TransitionValidationCallback` merged by **Day 3** (pipeline imports them). Brahmanand's `pipeline.py` merged by **Day 4** (5-seed runs use the new `sla train`). |
| Definition of Done | All tests pass in CI including `test_eval_and_test_seeds_never_overlap_training_seeds`, `test_evaluation_does_not_change_q_table`, `test_corrupted_transition_stops_training`; `metrics.json` written for each run; baseline CSV produced; 5-seed result table (trained vs random vs untrained DQN) filled **only with numbers produced by the scripts**. |

**In simple words:** until now we looked at training rewards, which include random exploration moves. This week we add an "exam": the agent plays with no randomness and no learning, on levels it never trained on. Only exam scores count as results.

---

## SECTION 2 — WHAT WE ARE BUILDING THIS WEEK

1. **Modules:** `evaluation/evaluate.py` + `evaluation/metrics.py` (Vedant) · `learning/guards.py` (Atharv) · `utils/validation.py` W6 part + `ui/feedback.py` (Somesh) · `pipeline.py` + `cli.py` changes + `scripts/run_baseline.py` (Brahmanand).
2. **Why:** a learning curve alone can mislead (exploration noise, lucky seeds). Examiners will ask "how do you know it learned?" — the answer is: *frozen-policy evaluation on held-out seeds, compared with an untrained baseline, over 5 seeds*.
3. **Connection:** all new pieces are **callbacks** collected in one place, `pipeline.default_callbacks`; the runner still does not change. Week 7 builds the full pipeline, statistics and UI on top.
4. **If missing:** no trustworthy numbers for the report; a diverging DQN could silently waste a night of training.
5. **Final output:**
   ```text
   $ sla train --config configs/frozenlake_q.yaml --seed 0
   Run id: frozenlake_q_learning_s0_20261112-190405  (completed, 2000 episodes)
   Final evaluation: mean x.xx ± x.xx, success xx% over 100 test episodes
   Folder: runs/frozenlake_q_learning_s0_20261112-190405
   $ python scripts/run_baseline.py --seeds 0 1 2 3 4 --with-untrained-dqn
   (prints a table of random / untrained-DQN scores and saves results/baseline/baseline.csv)
   ```
   The `x` values are placeholders — write in what *your* run prints.

**Analogy:** training is practice with a coach shouting hints (exploration); evaluation is the exam — no hints, no learning during the exam, and the questions (seeds) were never seen in practice.

### The three seed ranges (never overlap)
```text
training resets   seed*100_000 + episode     e.g. seed 4, episode 1999  -> 401_999
validation (eval) EVAL_SEED_BASE + i         10_000_000 ... 10_000_019  (pick the best checkpoint)
test (final)      TEST_SEED_BASE + i         20_000_000 ... 20_000_099  (report these numbers only)
```

### Callback order (in `pipeline.default_callbacks`)
```text
StoreCallback -> TransitionValidationCallback -> CheckpointCallback -> PeriodicEvalCallback
             -> RegressionMonitor (needs the newest eval score) -> DivergenceGuard
```

---

## SECTION 3 — DAILY EXECUTION PLAN

### Day 1 — Evaluation protocol and DQN fixes (1.5 h)
- **Daily objective:** everyone agrees *how* results are measured before any result is produced.
- **Assigned members:** all (Vedant presents the protocol, 30 min). Brahmanand is integration captain.
- **Individual tasks:** Vedant: `docs/evaluation_protocol.md` + `evaluate_agent` (SLA-06-VB-1 steps 1–3). Atharv: apply the Week-5 debug checklist to the pilot runs; write `is_diverging` / `detect_regression` (SLA-06-AG-1 steps 1–2). Brahmanand: `run_baseline.py` skeleton (SLA-06-BM-2 step 1). Somesh: lesson on NaN/infinity and `math.isfinite` (Section 5.4).
- **Required commands:**
  ```bash
  git checkout main && git pull && pip install -e ".[dev]" && pytest -q
  ```
- **Expected files:** `docs/evaluation_protocol.md`, `src/sla/evaluation/evaluate.py` (draft), `src/sla/learning/guards.py` (draft).
- **Expected output:** protocol agreed (seed ranges, 100 test episodes, success thresholds FrozenLake 1.0 / CartPole 500).
- **GitHub activity:** issues #61–#69 created.
- **Completion checklist:** - [ ] protocol agreed · - [ ] issues assigned

### Day 2 — Evaluator merged (1.5 h)
- **Daily objective:** frozen-policy evaluation works and is merged.
- **Assigned members:** Vedant (evaluator tests → PR #61 merged), Atharv (guard callbacks), Somesh (`validate_transition`), Brahmanand (reviews #61).
- **Individual tasks:** SLA-06-VB-1 steps 4–6 · SLA-06-AG-1 steps 3–4 · SLA-06-SB-1 steps 1–3.
- **Required commands:** `pytest tests/unit/test_evaluate.py -v`
- **Expected output:** `test_evaluation_does_not_change_q_table` passes.
- **GitHub activity:** #61 merged.
- **Completion checklist:** - [ ] evaluator merged

### Day 3 — Guards, validation, metrics merged (1.5 h)
- **Daily objective:** every piece the pipeline needs is on `main`.
- **Assigned members:** Atharv (#64 guards), Somesh (#68 transition validation), Vedant (#62 metrics), Brahmanand (`pipeline.py`).
- **Individual tasks:** SLA-06-AG-1 steps 5–6 · SLA-06-SB-1 steps 4–6 · SLA-06-VB-2 · SLA-06-BM-1 steps 1–3.
- **Required commands:**
  ```bash
  pytest tests/unit/test_guards.py tests/unit/test_metrics.py tests/unit/test_validation.py -v
  pytest tests/integration/test_transition_validation.py -v
  ```
- **GitHub activity:** #62, #64, #68 merged.
- **Completion checklist:** - [ ] guards merged · - [ ] validation merged · - [ ] metrics merged

### Day 4 — Pipeline and new `sla train` (1.5 h)
- **Daily objective:** `sla train` trains + evaluates + writes `metrics.json`; `sla evaluate` exists.
- **Assigned members:** Brahmanand (pipeline + CLI), Somesh (feedback module), Vedant (reviews pipeline), Atharv (starts 5-seed FrozenLake runs right after merge).
- **Individual tasks:** SLA-06-BM-1 steps 4–7 · SLA-06-SB-2 steps 1–3.
- **Required commands:**
  ```bash
  pytest tests/integration/test_pipeline_e2e.py -v
  sla train --config configs/frozenlake_q.yaml --seed 0
  sla evaluate --checkpoint runs/<run_id>/checkpoints/best
  ```
- **Expected output:** `runs/<run_id>/metrics.json` and `checkpoints/best/`.
- **GitHub activity:** #66 merged.
- **Completion checklist:** - [ ] new `sla train` works on 4 laptops

### Day 5 — Baselines and 5-seed runs (1.5 h + unattended runs)
- **Daily objective:** baseline CSV and the 5-seed training runs started.
- **Assigned members:** Brahmanand (baseline), Atharv (5-seed DQN — split seeds across laptops if slow: Atharv 0–1, Brahmanand 2, Vedant 3, Somesh 4), Vedant (checks `evals` rows), Somesh (feedback tests → PR #69).
- **Individual tasks:** SLA-06-BM-2 steps 2–4 · SLA-06-AG-2 steps 1–3 · SLA-06-SB-2 steps 4–6.
- **Required commands:**
  ```bash
  python scripts/run_baseline.py --seeds 0 1 2 3 4 --episodes 100 --with-untrained-dqn
  for s in 0 1 2 3 4; do sla train --config configs/frozenlake_q.yaml --seed $s; done
  sla train --config configs/cartpole_dqn.yaml --seed 0      # one seed per laptop
  ```
  (Windows PowerShell loop: `foreach ($s in 0..4) { sla train --config configs/frozenlake_q.yaml --seed $s }`)
- **Completion checklist:** - [ ] baseline CSV · - [ ] all 10 runs started

### Day 6 — Results table and merge (2.5 h)
- **Daily objective:** all PRs merged; the first honest results table written.
- **Assigned members:** all.
- **Individual tasks:** each member sends Atharv the `metrics.json` of the runs on their laptop; Atharv fills the table in `docs/notes/week6_results.md` (Section 5.2 template); Vedant checks that every number in it matches a `metrics.json` file; Somesh plots the eval curve of one DQN run with `plot_eval_curve`.
- **Expected output:** table with trained (test seeds) vs random vs untrained DQN, 5 seeds, mean ± std.
- **Completion checklist:** - [ ] all PRs merged · - [ ] results cross-checked by Vedant

### Day 7 — Weekly review (1 h)
- **Daily objective:** demo `sla train` → `sla evaluate` on fresh `main`; walk through the results table; Section 12 agenda.
- **Completion checklist:** - [ ] Section 13 complete

---

## SECTION 4 — INDIVIDUAL MEMBER TASKS

### Brahmanand Mathpati

**Task ID:** SLA-06-BM-1
**Task Title:** Train-and-evaluate pipeline, new `sla train`, `sla evaluate`
**Priority:** P1
**Estimated Duration:** 7 h (learning 1, coding 3, testing 1, integration 2 — integration captain)
**Dependencies:** `evaluate.py` (#61), `guards.py` (#64), `TransitionValidationCallback` (#68)
**Assigned Member:** Brahmanand Mathpati

1. **What:** `src/sla/pipeline.py` (Week-6 part: `git_sha`, `default_callbacks`, `final_evaluation`, `train_and_evaluate`); in `src/sla/cli.py` replace `_callbacks` and `cmd_train`, add `--eval-episodes` to `train`, and add the `# region W6: evaluate` block (`cmd_evaluate`, `add_w6_parsers`).
2. **Why:** one function that every entry point (CLI, scripts, UI) calls, so all results are produced the same way.
3. **Files:** create `pipeline.py`, `tests/integration/test_pipeline_e2e.py`; modify `cli.py`.
4. **Functions:** as item 1 (Section 5.1).
5. **Inputs:** `RunConfig`, `EpisodeStore`, number of final test episodes.
6. **Outputs:** `RunResult`, `EvalResult`; `runs/<run_id>/metrics.json` (run id, env, agent, seed, episodes, stop reason, final evaluation with checkpoint used and seed base, git commit).
7. **Steps:**
   1. Pull `main` after #61, #64, #68.
   2. Write `default_callbacks` in the order of Section 2 (comment why `RegressionMonitor` is after `PeriodicEvalCallback`).
   3. Write `final_evaluation`: use `checkpoints/best` if it exists, otherwise the latest checkpoint; always on `TEST_SEED_BASE`.
   4. Write `train_and_evaluate`; write `metrics.json` with `git_sha()` so every result can be traced to a commit.
   5. Update `cli.py` (Section 5.1 — complete Week-6 file).
   6. Write `test_pipeline_e2e.py` (W6 region).
   7. Run all tests; PR #66.
8. **Commands:**
   ```bash
   git checkout -b feat/brahmanand-66-pipeline-evaluate
   pytest tests/integration/test_pipeline_e2e.py tests/unit/test_cli_help.py -v
   sla --help                                   # now lists evaluate
   git add src/sla/pipeline.py src/sla/cli.py tests/integration/test_pipeline_e2e.py
   git commit -m "feat(pipeline): train, evaluate on test seeds and save metrics.json"
   git push -u origin feat/brahmanand-66-pipeline-evaluate
   ```
9. **Tests:** `test_train_and_evaluate_writes_metrics` (metrics file, best checkpoint, one eval row per `eval_every`).
10. **Expected result:** `1 passed` (the W7 test is added next week).
11. **Common errors:** `metrics.json` reports a training score → make sure `final_evaluation` uses `TEST_SEED_BASE`; `RegressionMonitor` never fires → it is listed before `PeriodicEvalCallback`; `git_sha` crashes without git → it already returns `None` on `OSError`.
12. **Branch:** `feat/brahmanand-66-pipeline-evaluate`
13. **Commit:** `feat(pipeline): train, evaluate on test seeds and save metrics.json`
14. **PR title:** `feat: train-and-evaluate pipeline + sla evaluate (SLA-06-BM-1)`
15. **Acceptance:** e2e test green; `sla evaluate` reproduces the `metrics.json` final score for the same checkpoint (same seeds → same number); reviewer: Vedant.

**Task ID:** SLA-06-BM-2
**Task Title:** Baseline script (random agent and untrained DQN)
**Priority:** P1
**Estimated Duration:** 4 h (coding 1, testing 1, integration 1, docs 1)
**Dependencies:** `evaluate.py` (#61)
**Assigned Member:** Brahmanand Mathpati

1. **What:** `scripts/run_baseline.py`.
2. **Why:** "the agent learned" only means something compared with an agent that did **not** learn: a random agent, and the same DQN network before training.
3. **Files:** `scripts/run_baseline.py`; output `results/baseline/baseline.csv` (committed — it is a small result file, and the command that made it is in the PR).
4. **Functions:** `untrained_dqn(cfg_path, seed)`, `main()`.
5. **Inputs:** `--seeds`, `--episodes`, `--with-untrained-dqn`, `--out`.
6. **Outputs:** CSV rows `env, agent, seed, mean_return, std_return, success_rate`; printed summary.
7. **Steps:** write the script (Section 5.1) → run it → paste the printed table into the PR → commit the CSV.
8. **Commands:**
   ```bash
   git checkout -b feat/brahmanand-67-baseline
   python scripts/run_baseline.py --seeds 0 1 2 3 4 --episodes 100 --with-untrained-dqn
   git add scripts/run_baseline.py results/baseline/baseline.csv
   git commit -m "feat(scripts): add random and untrained-DQN baselines"
   git push -u origin feat/brahmanand-67-baseline
   ```
9. **Tests:** run twice → identical CSV (fixed seeds).
10. **Expected result:** 15 rows (2 envs × 5 seeds random + 5 untrained DQN).
11. **Common errors:** `ModuleNotFoundError: torch` → run without `--with-untrained-dqn` on that laptop and let a laptop with PyTorch produce the final CSV.
12. **Branch:** `feat/brahmanand-67-baseline`
13. **Commit:** `feat(scripts): add random and untrained-DQN baselines`
14. **PR title:** `feat: baselines (SLA-06-BM-2)`
15. **Acceptance:** CSV reproducible; reviewer: Atharv.

### Atharv Gundale

**Task ID:** SLA-06-AG-1
**Task Title:** Divergence guard and regression monitor
**Priority:** P1
**Estimated Duration:** 5 h (learning 1, coding 2, testing 2)
**Dependencies:** `PeriodicEvalCallback` writes `ctx.extra["eval_history"]` (#61)
**Assigned Member:** Atharv Gundale

1. **What:** `src/sla/learning/guards.py` — `is_diverging`, `detect_regression`, `DivergenceGuard`, `RegressionMonitor`.
2. **Why:** self-learning can go wrong: Q-values can explode (divergence) or the policy can get worse after being good (regression / "catastrophic forgetting"). Guards stop the first and flag the second; the best checkpoint is always kept.
3. **Files:** `learning/guards.py`, `tests/unit/test_guards.py`.
4. **Functions/classes:** `is_diverging(max_abs_q, loss, q_limit=1e4)`; `detect_regression(history, drop_fraction=0.2, patience=3)`; the two callbacks.
5. **Inputs:** `agent.last_max_q`, `agent.last_loss`; the evaluation history list.
6. **Outputs:** `True` to stop (divergence; `stop_reason = "divergence"`); a list of flagged episodes in `ctx.extra["regression_flags"]` (training continues).
7. **Steps:** pure functions first → 3 tests → callbacks → PR #64 by Day 3.
8. **Commands:**
   ```bash
   git checkout -b feat/atharv-64-guards
   pytest tests/unit/test_guards.py -v
   git add src/sla/learning/guards.py tests/unit/test_guards.py
   git commit -m "feat(learning): add divergence guard and regression monitor"
   git push -u origin feat/atharv-64-guards
   ```
9. **Tests:** divergence detected for NaN loss / huge Q; regression after 3 drops ≥ 20 % below the best; no regression when scores recover.
10. **Expected result:** `3 passed`.
11. **Common errors:** guard stops Q-learning → Q-learning has no `last_max_q`, `getattr(..., None)` must return `None` and `is_diverging(None, None)` is `False`.
12. **Branch:** `feat/atharv-64-guards`
13. **Commit:** `feat(learning): add divergence guard and regression monitor`
14. **PR title:** `feat: training guards (SLA-06-AG-1)`
15. **Acceptance:** tests pass; reviewer: Brahmanand.

**Task ID:** SLA-06-AG-2
**Task Title:** 5-seed training runs and DQN configuration tuning
**Priority:** P1
**Estimated Duration:** 6 h (coding 3 [config + run scripts], integration 2, docs 1) + unattended run time
**Dependencies:** new `sla train` (#66, Day 4)
**Assigned Member:** Atharv Gundale

1. **What:** run 5 seeds × {FrozenLake Q-learning, CartPole DQN}; tune `configs/cartpole_dqn.yaml` **only if** the pilot notes show a problem; write `docs/notes/week6_results.md`.
2. **Why:** one seed can be lucky. Five seeds show whether learning is reliable.
3. **Files:** `configs/cartpole_dqn.yaml` (modified only with a reason), `docs/notes/week6_results.md`.
4. **Functions:** uses `sla train`, `metrics.json`.
5. **Inputs:** configs; seeds 0–4.
6. **Outputs:** 10 run folders with `metrics.json`; results note.
7. **Steps:**
   1. Before Day 4: decide config changes from the debug checklist. Change **one value at a time**, write each change and its reason in the YAML comment and in `dqn_debug_checklist.md`.
   2. Freeze the config **before** the 5-seed runs. Tuning on the test seeds is not allowed — choose settings using training/validation curves only.
   3. Run the 10 runs (split across laptops, Day 5 plan).
   4. Fill the table (Section 5.2) by copying from each `metrics.json`; Vedant cross-checks.
   5. Write 3–5 sentences of honest observations (e.g. "seed 3 reached 500 only at the end", "seed 2 was flagged for regression at episode 449").
8. **Commands:**
   ```bash
   git checkout -b exp/atharv-65-five-seed-runs
   for s in 0 1 2 3 4; do sla train --config configs/cartpole_dqn.yaml --seed $s; done
   python -c "import json,glob; [print(p, json.load(open(p))['final_eval']['mean_return']) for p in sorted(glob.glob('runs/*/metrics.json'))]"
   git add configs/cartpole_dqn.yaml docs/notes/week6_results.md
   git commit -m "exp: five-seed results and tuned DQN config"
   git push -u origin exp/atharv-65-five-seed-runs
   ```
9. **Tests:** `pytest tests/unit/test_config.py` (the repo configs must still validate).
10. **Expected result:** a table where every number traces back to a `metrics.json`. Target from the master plan: trained DQN clearly above the untrained DQN and random baselines on test seeds — **report whatever you get**, including seeds that did not learn.
11. **Common errors:** mixing training reward with test score in the table; changing the config after seeing test results (this is "peeking" — record and re-run all seeds if you must change it).
12. **Branch:** `exp/atharv-65-five-seed-runs`
13. **Commit:** `exp: five-seed results and tuned DQN config`
14. **PR title:** `exp: Week-6 five-seed results (SLA-06-AG-2)`
15. **Acceptance:** Vedant confirms every number; config change log present; reviewer: Vedant.

### Vedant Biradar

**Task ID:** SLA-06-VB-1
**Task Title:** Frozen-policy evaluator, best checkpoint and evaluation protocol
**Priority:** P1
**Estimated Duration:** 8 h (learning 1, coding 4, testing 2, docs 1)
**Dependencies:** Week-5 checkpoints and store
**Assigned Member:** Vedant Biradar

1. **What:** `src/sla/evaluation/evaluate.py` — `EVAL_SEED_BASE`, `TEST_SEED_BASE`, `SUCCESS_THRESHOLDS`, `EvalResult`, `evaluate_agent`, `evaluate_checkpoint`, `PeriodicEvalCallback`; `docs/evaluation_protocol.md`.
2. **Why:** the single source of truth for every reported number.
3. **Files:** `evaluation/evaluate.py`, `tests/unit/test_evaluate.py`, `docs/evaluation_protocol.md`.
4. **Functions/classes:** as item 1 (Section 5.3).
5. **Inputs:** an agent (or checkpoint folder), env name/kwargs, number of episodes, seed base.
6. **Outputs:** `EvalResult(mean_return, std_return, success_rate, n_episodes, returns)`; rows in the `evals` table; `checkpoints/best/` with `eval_mean`.
7. **Steps:**
   1. Write the protocol doc (Section 5.3 outline).
   2. Write `evaluate_agent`: `explore=False`, never call `update()`, `env.reset(seed=seed_base + i)`.
   3. Write `evaluate_checkpoint`.
   4. Write `PeriodicEvalCallback`: every `every` episodes evaluate on validation seeds, log to store, save `checkpoints/best` when the score improves; on resume, read the previous best from `best/checkpoint.json`.
   5. Write 4 tests.
   6. PR #61 — **merge by Day 2**.
8. **Commands:**
   ```bash
   git checkout -b feat/vedant-61-evaluator
   pytest tests/unit/test_evaluate.py -v --cov=sla.evaluation.evaluate --cov-report=term-missing
   git add src/sla/evaluation/evaluate.py tests/unit/test_evaluate.py docs/evaluation_protocol.md
   git commit -m "feat(evaluation): add frozen-policy evaluator with held-out seeds"
   git push -u origin feat/vedant-61-evaluator
   ```
9. **Tests:** evaluation does not change the Q-table; random baseline repeatable; perfect FrozenLake policy gets success 100 %; evaluation/test seeds never overlap training seeds.
10. **Expected result:** `4 passed`.
11. **Common errors:** evaluation changes the agent → you called `act(..., explore=True)` or `update()`; scores differ run to run → missing `seed=` in `env.reset`.
12. **Branch:** `feat/vedant-61-evaluator`
13. **Commit:** `feat(evaluation): add frozen-policy evaluator with held-out seeds`
14. **PR title:** `feat: frozen-policy evaluator (SLA-06-VB-1)`
15. **Acceptance:** tests pass; protocol reviewed by the whole team on Day 1; reviewer: Brahmanand.

**Task ID:** SLA-06-VB-2
**Task Title:** Learning metrics
**Priority:** P2
**Estimated Duration:** 3 h (coding 1, testing 1, review 1)
**Dependencies:** none
**Assigned Member:** Vedant Biradar

1. **What:** `src/sla/evaluation/metrics.py` — `summarize`, `success_rate`, `episodes_to_threshold`, `first_last_fraction`, `area_under_curve`.
2. **Why:** numbers that describe *how fast* and *how much* the agent improved (used by reflection facts and the report in Weeks 7–9).
3. **Files:** `evaluation/metrics.py`, `tests/unit/test_metrics.py`.
4. **Functions:** as item 1.
5. **Inputs:** list of returns.
6. **Outputs:** floats / dicts; `episodes_to_threshold` returns `None` when never reached.
7. **Steps:** write → 6 tests with hand-checked answers → PR #62.
8. **Commands:** branch `feat/vedant-62-metrics`; `pytest tests/unit/test_metrics.py -v`; commit `feat(evaluation): add learning metrics`; push.
9. **Tests:** summary, success rate, known answer for episodes-to-threshold, first/last fraction, AUC, empty input raises.
10. **Expected result:** `6 passed`.
11. **Common errors:** off-by-one in `episodes_to_threshold` (window end vs start) — the test fixes the convention.
12. **Branch:** `feat/vedant-62-metrics`
13. **Commit:** `feat(evaluation): add learning metrics`
14. **PR title:** `feat: learning metrics (SLA-06-VB-2)`
15. **Acceptance:** tests pass; reviewer: Somesh (Somesh reviews a teammate's code for the first time — Vedant explains each function).

### Somesh Badwane

**Task ID:** SLA-06-SB-1
**Task Title:** Transition validation (reward and state checks during training)
**Priority:** P1
**Estimated Duration:** 6 h (learning 2, coding 2, testing 2)
**Dependencies:** your Week-4 `validation.py`; Week-4 runner `Callback.on_step`
**Assigned Member:** Somesh Badwane

**0. Learn first (Section 5.4, ~1 h):** what NaN and infinity are, `math.isfinite`, `np.isfinite` on arrays, Gymnasium action spaces (`space.contains(a)`), and how a callback's `on_step` sees every transition.

1. **What:** the W6 region of `src/sla/utils/validation.py` — `validate_transition`, `REWARD_RANGES`, `TransitionValidationCallback`.
2. **Why:** the reward is the only teacher the agent has. A broken reward (NaN, wrong range) would silently teach nonsense; your check stops training at once with a clear message.
3. **Files:** modify `utils/validation.py` and `tests/unit/test_validation.py` (add W6 regions); create `tests/integration/test_transition_validation.py`.
4. **Functions/classes:** as item 1.
5. **Inputs:** state, action, reward, next state, action space, expected reward range.
6. **Outputs:** nothing when valid; `ValidationError` naming the problem otherwise; `checked` counter.
7. **Steps:**
   1. Exercises in Section 5.4.
   2. Add the new imports at the top of `validation.py` (`math`, `numpy as np`) — see the full file in Section 5.4.
   3. Write `validate_transition` below the W4 region, inside `# region W6`.
   4. Add the W6 tests (parametrized bad transitions).
   5. Write `TransitionValidationCallback` and the integration test (a fake callback corrupts the reward → training must stop with `ValidationError`).
   6. PR #68 by Day 3; reviewer Vedant.
8. **Commands:**
   ```bash
   git checkout main && git pull
   git checkout -b feat/somesh-68-transition-validation
   pytest tests/unit/test_validation.py tests/integration/test_transition_validation.py -v
   ruff check src/sla/utils tests
   git add src/sla/utils/validation.py tests/unit/test_validation.py tests/integration/test_transition_validation.py
   git commit -m "feat(utils): validate every transition during training"
   git push -u origin feat/somesh-68-transition-validation
   ```
9. **Tests:** valid transition passes; NaN state, out-of-space action, bool/str/NaN/out-of-range reward rejected; every transition of a 10-episode run is checked; corrupted reward stops training.
10. **Expected result:** all validation tests pass (W4 + W6) plus `2 passed` in the integration test.
11. **Common errors:** `True` accepted as a reward → check `bool` first (same lesson as Week 4); NumPy `float32` reward rejected → include `np.floating` in the `isinstance` check; ruff F401 "imported but unused" → you added an import you do not use yet.
12. **Branch:** `feat/somesh-68-transition-validation`
13. **Commit:** `feat(utils): validate every transition during training`
14. **PR title:** `feat: transition validation (SLA-06-SB-1)`
15. **Acceptance:** tests pass; Brahmanand's `default_callbacks` uses your callback; reviewer: Vedant.

**Task ID:** SLA-06-SB-2
**Task Title:** Feedback storage helper (ratings for explanation notes)
**Priority:** P2
**Estimated Duration:** 5 h (coding 3, testing 1, docs 1)
**Dependencies:** Vedant's store (`add_feedback`, `get_reflection`, `query_feedback` — Week 5)
**Assigned Member:** Somesh Badwane

1. **What:** `src/sla/ui/feedback.py` — `clean_comment`, `save_rating`, `ratings_summary`.
2. **Why:** in Week 7 users rate each explanation note (accurate? useful 1–5?). Your module validates and stores those ratings; the Week-8 reflection evaluation reads them.
3. **Files:** `ui/feedback.py`, `tests/unit/test_feedback.py`.
4. **Functions:** as item 1.
5. **Inputs:** note id, accurate (bool), usefulness (1–5), optional comment.
6. **Outputs:** new feedback id; summary dict `{count, accurate_share, mean_usefulness}`.
7. **Steps:** write `clean_comment` (removes control characters, max 500 characters) → `save_rating` with validation → `ratings_summary` → 5 tests → PR #69.
8. **Commands:**
   ```bash
   git checkout -b feat/somesh-69-feedback
   pytest tests/unit/test_feedback.py -v
   git add src/sla/ui/feedback.py tests/unit/test_feedback.py
   git commit -m "feat(ui): validate and store note ratings"
   git push -u origin feat/somesh-69-feedback
   ```
9. **Tests:** save and summary; invalid ratings rejected; unknown note rejected; comment cleaning; empty summary.
10. **Expected result:** `5 passed`.
11. **Common errors:** `IntegrityError: FOREIGN KEY` → note id does not exist (your `get_reflection` check should catch it first with a clear message).
12. **Branch:** `feat/somesh-69-feedback`
13. **Commit:** `feat(ui): validate and store note ratings`
14. **PR title:** `feat: note rating helper (SLA-06-SB-2)`
15. **Acceptance:** tests pass; reviewer: Vedant.

**How to make the PR:** as before; label `week-6`; in the description explain in 2 sentences *why* the reward must be validated (practice for the viva).

**Independent practice exercise:** write `validate_probability(p)` that accepts finite floats in [0, 1] (not bools, not NaN). 5 parametrized tests. Show Vedant; do not commit.

---

## SECTION 5 — COMPLETE TECHNICAL IMPLEMENTATION

### 5.1 Pipeline, CLI changes, baselines (Brahmanand)

`src/sla/pipeline.py` — **Week-6 version** (Week 7 appends a second region; nothing here changes):
```python
"""One-call pipelines used by the CLI, scripts and the Streamlit UI (owner: Brahmanand).

Week 6: default_callbacks + train_and_evaluate.
Week 7 adds run_pipeline (logging to file, plots and reflection) — see the Week-7 handbook.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from sla.agent.checkpoint import CheckpointCallback, latest_checkpoint, load_checkpoint
from sla.agent.runner import Callback, RunResult, run_training
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
```

`src/sla/cli.py` — **complete Week-6 version.** Compared with Week 5: (1) `_callbacks` now returns `pipeline.default_callbacks` (used by `resume`); (2) `cmd_train` calls `train_and_evaluate` and prints the **test** score; (3) `train` gets `--eval-episodes`; (4) new region W6 with `evaluate`.
```python
"""Command-line interface: `sla <command>` (owner: Brahmanand).

Week 6 version: train (now evaluates), resume, prune, evaluate.
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

`tests/integration/test_pipeline_e2e.py` — Week-6 version:
```python
import json

from sla.pipeline import train_and_evaluate
```
```python
def test_train_and_evaluate_writes_metrics(fl_cfg, store):
    train, final = train_and_evaluate(fl_cfg, store, final_eval_episodes=10)
    metrics = json.loads((train.run_dir / "metrics.json").read_text())
    assert metrics["final_eval"]["n_episodes"] == 10
    assert (train.run_dir / "checkpoints" / "best" / "checkpoint.json").exists()
    assert len(store.query_evals(train.run_id)) == fl_cfg.episodes // fl_cfg.eval_every
```

`scripts/run_baseline.py`
```python
"""Baselines: random agent (and optionally the untrained DQN), 5 seeds (owner: Brahmanand, Week 6).

Run:  python scripts/run_baseline.py --seeds 0 1 2 3 4 --episodes 100
Output: results/baseline/baseline.csv and a printed table. Nothing is trained.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from sla.agent.random_agent import RandomAgent
from sla.envs.factory import make_env
from sla.evaluation.evaluate import TEST_SEED_BASE, evaluate_agent
from sla.utils.config import load_config

BASELINE_CONFIGS = ["configs/frozenlake_random.yaml", "configs/cartpole_random.yaml"]


def untrained_dqn(cfg_path: str, seed: int):
    """A DQN with random initial weights and no training: the 'before learning' network."""
    from sla.agent.runner import build_agent
    cfg = load_config(cfg_path)
    cfg.seed = seed
    env = make_env(cfg.env_name, **cfg.env_kwargs)
    agent = build_agent(cfg, env)
    env.close()
    return cfg, agent


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    parser.add_argument("--episodes", type=int, default=100, help="evaluation episodes per seed")
    parser.add_argument("--with-untrained-dqn", action="store_true", help="needs PyTorch")
    parser.add_argument("--out", default="results/baseline/baseline.csv")
    args = parser.parse_args()

    rows = []
    for cfg_path in BASELINE_CONFIGS:
        cfg = load_config(cfg_path)
        env = make_env(cfg.env_name, **cfg.env_kwargs)
        n_actions = int(env.action_space.n)
        env.close()
        for seed in args.seeds:
            res = evaluate_agent(RandomAgent(n_actions, seed=seed), cfg.env_name, cfg.env_kwargs,
                                 args.episodes, seed_base=TEST_SEED_BASE)
            rows.append({"env": cfg.env_name, "agent": "random", "seed": seed,
                         "mean_return": res.mean_return, "std_return": res.std_return,
                         "success_rate": res.success_rate})
    if args.with_untrained_dqn:
        for seed in args.seeds:
            cfg, agent = untrained_dqn("configs/cartpole_dqn.yaml", seed)
            res = evaluate_agent(agent, cfg.env_name, cfg.env_kwargs, args.episodes, seed_base=TEST_SEED_BASE)
            rows.append({"env": cfg.env_name, "agent": "dqn_untrained", "seed": seed,
                         "mean_return": res.mean_return, "std_return": res.std_return,
                         "success_rate": res.success_rate})

    df = pd.DataFrame(rows)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    summary = df.groupby(["env", "agent"])["mean_return"].agg(["mean", "std", "count"]).round(2)
    print(summary.to_string())
    print(f"\nSaved {len(df)} rows to {out}")


if __name__ == "__main__":
    main()
```

### 5.2 Guards and results note (Atharv)

`src/sla/learning/guards.py`
```python
"""Learning safeguards (owner: Atharv, Week 6).

DivergenceGuard stops training when Q-values or the loss explode.
RegressionMonitor flags (but does not stop) when evaluation drops well
below the best score for several evaluations in a row.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from sla.agent.runner import Callback, EpisodeInfo, RunContext
from sla.utils.logging_setup import get_logger

log = get_logger(__name__)


def is_diverging(max_abs_q: float | None, loss: float | None, q_limit: float = 1e4) -> bool:
    """True if Q-values or loss are NaN/inf, or Q-values are absurdly large."""
    for value in (max_abs_q, loss):
        if value is not None and not math.isfinite(value):
            return True
    return max_abs_q is not None and max_abs_q > q_limit


def detect_regression(history: Sequence[float], drop_fraction: float = 0.2, patience: int = 3) -> bool:
    """True if the last ``patience`` scores are all below (1 - drop_fraction) * best earlier score."""
    if len(history) <= patience:
        return False
    best = max(history[:-patience])
    if best <= 0:
        return False
    limit = (1.0 - drop_fraction) * best
    return all(score < limit for score in history[-patience:])


class DivergenceGuard(Callback):
    def __init__(self, q_limit: float = 1e4) -> None:
        self.q_limit = q_limit

    def on_episode_end(self, ctx: RunContext, info: EpisodeInfo) -> bool:
        max_q = getattr(ctx.agent, "last_max_q", None)
        loss = getattr(ctx.agent, "last_loss", None)
        if is_diverging(max_q, loss, self.q_limit):
            ctx.extra["stop_reason"] = "divergence"
            log.error("Divergence at episode %d (max|Q|=%s, loss=%s); stopping", info.episode, max_q, loss)
            return True
        return False


class RegressionMonitor(Callback):
    """Must be listed after PeriodicEvalCallback so it sees the newest score."""

    def __init__(self, drop_fraction: float = 0.2, patience: int = 3) -> None:
        self.drop_fraction = drop_fraction
        self.patience = patience
        self._seen = 0

    def on_episode_end(self, ctx: RunContext, info: EpisodeInfo) -> bool:
        history = ctx.extra.get("eval_history", [])
        if len(history) == self._seen:
            return False
        self._seen = len(history)
        scores = [score for _, score in history]
        if detect_regression(scores, self.drop_fraction, self.patience):
            ctx.extra.setdefault("regression_flags", []).append(info.episode)
            log.warning("Regression flagged at episode %d (best checkpoint is kept)", info.episode)
        return False
```

`tests/unit/test_guards.py`
```python
import math

from sla.learning.guards import detect_regression, is_diverging


def test_divergence():
    assert is_diverging(math.nan, None)
    assert is_diverging(None, math.inf)
    assert is_diverging(1e9, 0.1)
    assert not is_diverging(50.0, 0.1)
    assert not is_diverging(None, None)


def test_regression_detected_after_three_drops():
    assert detect_regression([100, 200, 150, 150, 150], drop_fraction=0.2, patience=3)


def test_no_regression_when_recovering():
    assert not detect_regression([100, 200, 150, 150, 190], 0.2, 3)
    assert not detect_regression([100, 200], 0.2, 3)
```

`configs/cartpole_dqn.yaml` — values at the start of Week 6 (change only with a written reason):
```yaml
# DQN on CartPole-v1. Starting values; Atharv tunes them in Week 6.
env_name: CartPole-v1
agent: dqn
episodes: 600
seed: 0
gamma: 0.99
learning_rate: 0.0005
epsilon_start: 1.0
epsilon_end: 0.05
epsilon_decay_steps: 10000
max_steps_per_episode: 500
max_wall_clock_s: 3600
eval_every: 50
eval_episodes: 20
checkpoint_every: 50
run_root: runs
dqn:
  hidden_size: 128
  batch_size: 64
  buffer_size: 50000
  learning_starts: 1000
  train_freq: 1
  target_update_every: 500
  grad_clip: 10.0
  replay_enabled: true
  target_net_enabled: true
```

`docs/notes/week6_results.md` template (copy numbers from `metrics.json` / `baseline.csv` only):
```markdown
# Week-6 results (test seeds 20_000_000+, 100 episodes, epsilon = 0, no learning)
Commit: <git sha from metrics.json>     Config: configs/cartpole_dqn.yaml (unchanged / changed: ...)
| Env | Agent | Seed 0 | Seed 1 | Seed 2 | Seed 3 | Seed 4 | Mean ± std over seeds |
|---|---|---|---|---|---|---|---|
| FrozenLake-v1 | random | | | | | | |
| FrozenLake-v1 | q_learning (trained) | | | | | | |
| CartPole-v1 | random | | | | | | |
| CartPole-v1 | dqn (untrained) | | | | | | |
| CartPole-v1 | dqn (trained, best checkpoint) | | | | | | |
Observations (honest, 3-5 sentences):
Regression flags / divergence stops (run id, episode):
```

### 5.3 Evaluator, metrics and protocol (Vedant)

`src/sla/evaluation/evaluate.py`
```python
"""Frozen-policy evaluation (owner: Vedant, Week 6).

Evaluation rules:
  * explore=False (no random actions, epsilon is not used),
  * agent.update() is never called, so nothing is learned,
  * fixed evaluation seeds that are never used for training.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from sla.agent.base import Agent
from sla.agent.checkpoint import load_checkpoint, save_checkpoint
from sla.agent.runner import Callback, EpisodeInfo, RunContext
from sla.envs.factory import make_env
from sla.utils.logging_setup import get_logger

log = get_logger(__name__)

# Training uses reset seeds seed*100_000 + episode (see sla.utils.seeding.episode_seed),
# so evaluation seeds start far above that range and never overlap with training.
EVAL_SEED_BASE = 10_000_000   # "validation" seeds: periodic evaluation + picking the best checkpoint
TEST_SEED_BASE = 20_000_000   # "test" seeds: final evaluation only, never used to pick checkpoints
SUCCESS_THRESHOLDS = {"FrozenLake-v1": 1.0, "CartPole-v1": 500.0}


@dataclass
class EvalResult:
    mean_return: float
    std_return: float
    success_rate: float
    n_episodes: int
    returns: list[float] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_agent(agent: Agent, env_name: str, env_kwargs: dict[str, Any] | None = None,
                   n_episodes: int = 100, seed_base: int = EVAL_SEED_BASE,
                   max_steps: int = 10_000) -> EvalResult:
    """Run the agent greedily for ``n_episodes`` and return the scores. No learning happens."""
    if n_episodes <= 0:
        raise ValueError("n_episodes must be > 0")
    env = make_env(env_name, **(env_kwargs or {}))
    returns: list[float] = []
    try:
        for i in range(n_episodes):
            state, _ = env.reset(seed=seed_base + i)
            total, steps, done = 0.0, 0, False
            while not done and steps < max_steps:
                action = agent.act(state, explore=False)
                state, reward, terminated, truncated, _ = env.step(action)
                total += float(reward)
                steps += 1
                done = terminated or truncated
            returns.append(total)
    finally:
        env.close()
    arr = np.asarray(returns)
    threshold = SUCCESS_THRESHOLDS.get(env_name, float("inf"))
    return EvalResult(float(arr.mean()), float(arr.std()), float(np.mean(arr >= threshold)),
                      n_episodes, returns)


def evaluate_checkpoint(folder: Path, env_name: str, env_kwargs: dict[str, Any] | None = None,
                        n_episodes: int = 100, seed_base: int = EVAL_SEED_BASE) -> EvalResult:
    agent, _ = load_checkpoint(folder)
    return evaluate_agent(agent, env_name, env_kwargs, n_episodes, seed_base)


class PeriodicEvalCallback(Callback):
    """Every ``every`` episodes: evaluate the frozen policy, store the score, keep the best checkpoint."""

    def __init__(self, every: int, n_episodes: int = 20, store: Any = None,
                 seed_base: int = EVAL_SEED_BASE) -> None:
        self.every = every
        self.n_episodes = n_episodes
        self.store = store
        self.seed_base = seed_base
        self.best_mean = -float("inf")

    def on_run_start(self, ctx: RunContext) -> None:
        ctx.extra.setdefault("eval_history", [])
        best_file = ctx.run_dir / "checkpoints" / "best" / "checkpoint.json"
        if best_file.exists():  # resuming: remember the previous best
            from sla.utils.io_helpers import read_json
            self.best_mean = float(read_json(best_file).get("eval_mean", -float("inf")))

    def on_episode_end(self, ctx: RunContext, info: EpisodeInfo) -> bool:
        if (info.episode + 1) % self.every != 0:
            return False
        res = evaluate_agent(ctx.agent, ctx.cfg.env_name, ctx.cfg.env_kwargs, self.n_episodes, self.seed_base)
        ctx.extra["eval_history"].append((info.episode, res.mean_return))
        ctx.extra["last_eval"] = res
        if self.store is not None:
            self.store.log_eval(ctx.run_id, info.episode, res.mean_return, res.std_return,
                                res.success_rate, res.n_episodes)
        log.info("Eval after episode %d: mean %.2f ± %.2f", info.episode, res.mean_return, res.std_return)
        if res.mean_return > self.best_mean:
            self.best_mean = res.mean_return
            save_checkpoint(ctx.agent, ctx.run_dir / "checkpoints" / "best", info.episode,
                            {"eval_mean": res.mean_return})
        return False
```

`tests/unit/test_evaluate.py`
```python
"""Week 6 (Vedant): evaluation must never learn and must be repeatable."""

import numpy as np

from sla.agent.random_agent import RandomAgent
from sla.evaluation.evaluate import EVAL_SEED_BASE, TEST_SEED_BASE, evaluate_agent
from sla.learning.q_learning import QLearningAgent
from sla.utils.seeding import episode_seed


def test_evaluation_does_not_change_q_table():
    agent = QLearningAgent(16, 4, seed=0)
    agent.q[:] = np.random.default_rng(0).random(agent.q.shape)
    before = agent.q.copy()
    evaluate_agent(agent, "FrozenLake-v1", {"is_slippery": False}, 10)
    assert np.array_equal(before, agent.q) and agent.steps == 0  # no update() was called


def test_random_baseline_repeatable():
    a = evaluate_agent(RandomAgent(2, seed=0), "CartPole-v1", n_episodes=10)
    b = evaluate_agent(RandomAgent(2, seed=0), "CartPole-v1", n_episodes=10)
    assert a.returns == b.returns and a.n_episodes == 10


def test_success_rate_frozenlake_perfect_policy():
    class GoRightDown:
        """Right, right, down, down, down, right reaches the goal on the 4x4 map without holes."""
        plan = [2, 2, 1, 1, 1, 2]

        def __init__(self):
            self.i = 0

        def act(self, obs, explore=True):
            a = self.plan[self.i % len(self.plan)]
            self.i += 1
            return a

    res = evaluate_agent(GoRightDown(), "FrozenLake-v1", {"is_slippery": False}, n_episodes=3)
    assert res.success_rate == 1.0 and res.mean_return == 1.0


def test_eval_and_test_seeds_never_overlap_training_seeds():
    largest_training_seed = episode_seed(99, 99_999)
    assert EVAL_SEED_BASE > largest_training_seed and TEST_SEED_BASE > EVAL_SEED_BASE + 1_000_000
```

`src/sla/evaluation/metrics.py`
```python
"""Metrics computed from lists of episode returns (owner: Vedant, Week 6)."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def summarize(returns: Sequence[float]) -> dict[str, float]:
    arr = np.asarray(returns, dtype=np.float64)
    if arr.size == 0:
        raise ValueError("returns must not be empty")
    return {"mean": float(arr.mean()), "std": float(arr.std()), "median": float(np.median(arr)),
            "min": float(arr.min()), "max": float(arr.max()), "n": int(arr.size)}


def success_rate(returns: Sequence[float], threshold: float) -> float:
    """Share of episodes whose return reached ``threshold``."""
    arr = np.asarray(returns, dtype=np.float64)
    if arr.size == 0:
        raise ValueError("returns must not be empty")
    return float(np.mean(arr >= threshold))


def episodes_to_threshold(returns: Sequence[float], threshold: float, window: int = 20) -> int | None:
    """First episode index at which the rolling mean (over ``window``) reaches ``threshold``; None if never."""
    arr = np.asarray(returns, dtype=np.float64)
    if window <= 0:
        raise ValueError("window must be > 0")
    if arr.size < window:
        return None
    rolling = np.convolve(arr, np.ones(window) / window, mode="valid")
    hits = np.flatnonzero(rolling >= threshold)
    return int(hits[0] + window - 1) if hits.size else None


def first_last_fraction(returns: Sequence[float], fraction: float = 0.05) -> tuple[float, float]:
    """Mean return of the first and the last ``fraction`` of episodes (at least one episode each)."""
    arr = np.asarray(returns, dtype=np.float64)
    if arr.size == 0:
        raise ValueError("returns must not be empty")
    if not 0 < fraction <= 0.5:
        raise ValueError("fraction must be in (0, 0.5]")
    k = max(1, int(round(arr.size * fraction)))
    return float(arr[:k].mean()), float(arr[-k:].mean())


def area_under_curve(returns: Sequence[float]) -> float:
    """Average return over all training episodes: higher means faster and better learning."""
    arr = np.asarray(returns, dtype=np.float64)
    if arr.size == 0:
        raise ValueError("returns must not be empty")
    return float(arr.mean())
```

`tests/unit/test_metrics.py`
```python
import pytest

from sla.evaluation.metrics import (
    area_under_curve,
    episodes_to_threshold,
    first_last_fraction,
    success_rate,
    summarize,
)


def test_summarize():
    s = summarize([1, 2, 3])
    assert s["mean"] == 2 and s["median"] == 2 and s["n"] == 3


def test_success_rate():
    assert success_rate([500, 200, 500, 500], 500) == 0.75


def test_episodes_to_threshold_known_answer():
    returns = [0] * 10 + [10] * 10
    assert episodes_to_threshold(returns, threshold=10, window=5) == 14
    assert episodes_to_threshold([1, 1, 1], threshold=5, window=2) is None


def test_first_last_fraction():
    first, last = first_last_fraction(list(range(100)), 0.05)
    assert first == pytest.approx(2.0) and last == pytest.approx(97.0)


def test_auc():
    assert area_under_curve([0, 10]) == 5


def test_empty_raises():
    with pytest.raises(ValueError):
        summarize([])
```

`docs/evaluation_protocol.md` outline:
```markdown
# Evaluation protocol
1. Training: epsilon-greedy, learning on, reset seeds seed*100_000 + episode.
2. Validation (during training): every eval_every episodes, eval_episodes greedy episodes on
   seeds 10_000_000 + i. Used ONLY to choose checkpoints/best.
3. Test (after training): best checkpoint, 100 greedy episodes on seeds 20_000_000 + i.
   These are the ONLY numbers reported as results.
4. During validation and test: explore=False, agent.update() is never called.
5. Success: FrozenLake return >= 1.0 (goal reached); CartPole return >= 500 (full episode).
6. Every result is reported over 5 training seeds (0-4) as mean +- std, next to the random and
   untrained-DQN baselines from scripts/run_baseline.py.
7. Every number in the report must trace to a metrics.json / CSV file and a git commit.
8. Never change hyper-parameters after looking at test results.
```

### 5.4 Transition validation and feedback (Somesh)

**Lesson (read before coding):**
```python
import math
import numpy as np
x = float("nan")           # "not a number" - e.g. 0.0/0.0 in NumPy
y = float("inf")           # infinity
math.isfinite(1.5)         # True
math.isfinite(x)           # False
x == x                     # False!  NaN is not even equal to itself
np.isfinite(np.array([1.0, np.nan, 2.0]))   # array([ True, False,  True])
np.all(np.isfinite(np.array([1.0, 2.0])))   # True only if EVERY value is finite

from gymnasium.spaces import Discrete
space = Discrete(2)        # actions 0 and 1
space.contains(1)          # True
space.contains(5)          # False
```
Mini-exercises: (a) write `all_finite(values)` for a list using a loop and `math.isfinite`; (b) check which of `[0, 1, 2, -1]` are inside `Discrete(2)`; (c) explain in one sentence why `x == x` is `False` for NaN.

`src/sla/utils/validation.py` — **complete file after Week 6** (your W4 region is unchanged; the new imports `math` and `numpy` are at the top):
```python
"""Input and transition validation (owner: Somesh).

Week 4: run-request helpers (seeds, env names, episode counts, safe names).
Week 6: transition validation used during training.
"""

from __future__ import annotations

import math
import re
from collections.abc import Iterable
from typing import Any

import numpy as np

from sla.utils.config import ALLOWED_ENVS
from sla.utils.errors import ValidationError

# region W4: run-request validation
MAX_EPISODES = 100_000
_SAFE_NAME = re.compile(r"[^A-Za-z0-9_-]+")


def validate_seeds(seeds: Iterable[Any]) -> list[int]:
    """Return seeds as a list of unique non-negative ints, keeping their order."""
    result: list[int] = []
    for seed in seeds:
        if isinstance(seed, bool) or not isinstance(seed, int):
            raise ValidationError(f"Seed must be an integer, got {seed!r}")
        if seed < 0:
            raise ValidationError(f"Seed must be >= 0, got {seed}")
        if seed not in result:
            result.append(seed)
    if not result:
        raise ValidationError("At least one seed is required")
    return result


def validate_env_name(name: str) -> str:
    """Accept only the environments this project supports."""
    if name not in ALLOWED_ENVS:
        raise ValidationError(f"Unsupported environment {name!r}. Choose one of {ALLOWED_ENVS}")
    return name


def validate_episode_count(episodes: Any) -> int:
    """Episodes must be an int between 1 and MAX_EPISODES."""
    if isinstance(episodes, bool) or not isinstance(episodes, int):
        raise ValidationError(f"Episodes must be an integer, got {episodes!r}")
    if not 1 <= episodes <= MAX_EPISODES:
        raise ValidationError(f"Episodes must be between 1 and {MAX_EPISODES}, got {episodes}")
    return episodes


def safe_run_name(name: str, max_length: int = 60) -> str:
    """Turn any text into a safe folder name: letters, digits, '_' and '-' only."""
    cleaned = _SAFE_NAME.sub("_", name.strip()).strip("_")
    if not cleaned:
        raise ValidationError("Run name is empty after removing unsafe characters")
    return cleaned[:max_length]
# endregion


# region W6: transition validation
def _is_finite_array(value: Any) -> bool:
    arr = np.asarray(value, dtype=np.float64)
    return bool(np.all(np.isfinite(arr)))


def validate_transition(state: Any, action: Any, reward: Any, next_state: Any,
                        action_space: Any, reward_range: tuple[float, float] | None = None) -> None:
    """Raise ValidationError if a transition looks corrupted.

    Checks: states contain only finite numbers, the action is inside the action
    space, and the reward is a finite number inside ``reward_range`` (if given).
    """
    if not _is_finite_array(state):
        raise ValidationError(f"State contains NaN or infinity: {state!r}")
    if not _is_finite_array(next_state):
        raise ValidationError(f"Next state contains NaN or infinity: {next_state!r}")
    if not action_space.contains(action):
        raise ValidationError(f"Action {action!r} is not inside the action space {action_space}")
    if isinstance(reward, bool) or not isinstance(reward, (int, float, np.floating, np.integer)):
        raise ValidationError(f"Reward must be a number, got {reward!r}")
    if not math.isfinite(float(reward)):
        raise ValidationError(f"Reward is NaN or infinite: {reward!r}")
    if reward_range is not None:
        low, high = reward_range
        if not low <= float(reward) <= high:
            raise ValidationError(f"Reward {reward} is outside the expected range [{low}, {high}]")


# Expected reward per step for each environment (used by the runner callback).
REWARD_RANGES: dict[str, tuple[float, float]] = {
    "FrozenLake-v1": (0.0, 1.0),
    "CartPole-v1": (0.0, 1.0),
}


class TransitionValidationCallback:
    """Runner callback that validates every transition (see sla.agent.runner.Callback)."""

    def __init__(self, env_name: str) -> None:
        self.reward_range = REWARD_RANGES.get(env_name)
        self.checked = 0

    def on_run_start(self, ctx: Any) -> None:
        self.checked = 0

    def on_step(self, ctx: Any, transition: Any) -> None:
        validate_transition(transition.state, transition.action, transition.reward,
                            transition.next_state, ctx.env.action_space, self.reward_range)
        self.checked += 1

    def on_episode_end(self, ctx: Any, info: Any) -> bool:
        return False

    def on_run_end(self, ctx: Any, result: Any) -> None:
        return None
# endregion
```

**Line by line (W6 part):** `_is_finite_array` converts any state (an int for FrozenLake, 4 floats for CartPole) to a NumPy array and checks every value · `action_space.contains(action)` asks Gymnasium itself whether the action is legal · the reward check rejects bools first, then non-numbers, then NaN/infinity, then values outside `REWARD_RANGES` · the callback's `on_step` runs for **every** step and counts how many it checked — the integration test compares that count with the total episode lengths.

`tests/unit/test_validation.py` — complete file after Week 6:
```python
import math

import numpy as np
import pytest
from gymnasium.spaces import Discrete

from sla.utils.errors import ValidationError
from sla.utils.validation import (
    safe_run_name,
    validate_env_name,
    validate_episode_count,
    validate_seeds,
    validate_transition,
)


# region W4: run-request validation
def test_seeds_deduplicated_in_order():
    assert validate_seeds([3, 1, 3, 0]) == [3, 1, 0]


@pytest.mark.parametrize("bad", [[], [-1], [1.5], [True], ["2"]])
def test_bad_seeds(bad):
    with pytest.raises(ValidationError):
        validate_seeds(bad)


def test_env_name():
    assert validate_env_name("CartPole-v1") == "CartPole-v1"
    with pytest.raises(ValidationError):
        validate_env_name("cartpole")


@pytest.mark.parametrize("bad", [0, -5, 100_001, 2.0, "10", None])
def test_bad_episode_counts(bad):
    with pytest.raises(ValidationError):
        validate_episode_count(bad)


def test_safe_run_name():
    assert safe_run_name("../../etc/passwd") == "etc_passwd"
    assert safe_run_name("My run #1") == "My_run_1"
    with pytest.raises(ValidationError):
        safe_run_name("///")


# endregion


# region W6: transition validation
SPACE = Discrete(2)


def test_valid_transition_passes():
    validate_transition(np.zeros(4), 1, 1.0, np.ones(4), SPACE, (0.0, 1.0))


@pytest.mark.parametrize("state,action,reward,next_state", [
    (np.array([0, math.nan, 0, 0]), 0, 1.0, np.zeros(4)),
    (np.zeros(4), 0, 1.0, np.array([math.inf, 0, 0, 0])),
    (np.zeros(4), 5, 1.0, np.zeros(4)),
    (np.zeros(4), 0, math.nan, np.zeros(4)),
    (np.zeros(4), 0, "1", np.zeros(4)),
    (np.zeros(4), 0, 7.0, np.zeros(4)),
])
def test_bad_transitions_rejected(state, action, reward, next_state):
    with pytest.raises(ValidationError):
        validate_transition(state, action, reward, next_state, SPACE, (0.0, 1.0))
# endregion
```

`tests/integration/test_transition_validation.py`
```python
"""Week 6 (Somesh): the runner validates every transition through a callback."""

import math

import pytest

from sla.agent.runner import Callback, run_training
from sla.utils.errors import ValidationError
from sla.utils.validation import TransitionValidationCallback


def test_every_transition_is_checked(fl_cfg):
    fl_cfg.episodes = 10
    cb = TransitionValidationCallback(fl_cfg.env_name)
    result = run_training(fl_cfg, [cb])
    assert cb.checked == sum(result.lengths)


class CorruptReward(Callback):
    """Pretends the environment returned a broken reward."""

    def on_step(self, ctx, transition):
        transition.reward = math.nan


def test_corrupted_transition_stops_training(fl_cfg):
    fl_cfg.episodes = 5
    with pytest.raises(ValidationError, match="NaN"):
        run_training(fl_cfg, [CorruptReward(), TransitionValidationCallback(fl_cfg.env_name)])
```

`src/sla/ui/feedback.py`
```python
"""Saving user ratings of reflection notes (owner: Somesh, Week 6).

Ratings are used ONLY to evaluate the explanation layer. They never change
what the agent learns.
"""

from __future__ import annotations

import re
from typing import Any

from sla.memory.episode_store import EpisodeStore
from sla.utils.errors import ValidationError

MAX_COMMENT_LENGTH = 500
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def clean_comment(comment: str | None) -> str | None:
    """Strip spaces and control characters; empty comments become None."""
    if comment is None:
        return None
    if not isinstance(comment, str):
        raise ValidationError("Comment must be text")
    text = _CONTROL_CHARS.sub("", comment).strip()
    if len(text) > MAX_COMMENT_LENGTH:
        raise ValidationError(f"Comment is too long ({len(text)} characters, max {MAX_COMMENT_LENGTH})")
    return text or None


def save_rating(store: EpisodeStore, note_id: int, accurate: bool, usefulness: int,
                comment: str | None = None) -> int:
    """Validate and store one rating. Returns the new feedback id."""
    if isinstance(note_id, bool) or not isinstance(note_id, int) or note_id <= 0:
        raise ValidationError(f"note_id must be a positive integer, got {note_id!r}")
    if not isinstance(accurate, bool):
        raise ValidationError("accurate must be True or False")
    if isinstance(usefulness, bool) or not isinstance(usefulness, int) or not 1 <= usefulness <= 5:
        raise ValidationError(f"usefulness must be an integer from 1 to 5, got {usefulness!r}")
    if store.get_reflection(note_id) is None:
        raise ValidationError(f"Note {note_id} does not exist")
    return store.add_feedback(note_id, accurate, usefulness, clean_comment(comment))


def ratings_summary(store: EpisodeStore) -> dict[str, Any]:
    df = store.query_feedback()
    if df.empty:
        return {"count": 0, "accurate_share": None, "mean_usefulness": None}
    return {"count": int(len(df)), "accurate_share": round(float(df["accurate"].mean()), 2),
            "mean_usefulness": round(float(df["usefulness"].mean()), 2)}
```

`tests/unit/test_feedback.py`
```python
import pytest

from sla.ui.feedback import clean_comment, ratings_summary, save_rating
from sla.utils.errors import ValidationError


@pytest.fixture
def note_id(store):
    store.start_run("r", "CartPole-v1", "dqn", 0, {})
    return store.add_reflection("r", {}, "note", "template", True)


def test_save_and_summary(store, note_id):
    save_rating(store, note_id, True, 5, "  clear  ")
    save_rating(store, note_id, False, 3)
    assert ratings_summary(store) == {"count": 2, "accurate_share": 0.5, "mean_usefulness": 4.0}
    assert store.query_feedback(note_id)["comment"].tolist()[0] == "clear"


@pytest.mark.parametrize("kwargs", [
    {"accurate": "yes", "usefulness": 3}, {"accurate": True, "usefulness": 0},
    {"accurate": True, "usefulness": 6}, {"accurate": True, "usefulness": 2.5},
])
def test_invalid_ratings(store, note_id, kwargs):
    with pytest.raises(ValidationError):
        save_rating(store, note_id, **kwargs)


def test_unknown_note(store):
    with pytest.raises(ValidationError, match="does not exist"):
        save_rating(store, 999, True, 3)


def test_comment_cleaning():
    assert clean_comment("ok\x00\x07 ") == "ok"
    assert clean_comment("   ") is None
    with pytest.raises(ValidationError):
        clean_comment("x" * 501)


def test_empty_summary(store):
    assert ratings_summary(store)["count"] == 0
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
│   ├── cartpole_dqn.yaml   [MODIFIED · Somesh → Atharv]
│   ├── cartpole_random.yaml
│   ├── frozenlake_q.yaml
│   └── frozenlake_random.yaml
├── docs/
│   ├── notes/
│   │   ├── dqn_debug_checklist.md
│   │   ├── dqn_explained.md
│   │   ├── q_learning_by_hand.md
│   │   └── week6_results.md   [NEW · Atharv]
│   ├── architecture.md
│   ├── data_handling.md
│   ├── design.md
│   ├── evaluation_protocol.md   [NEW · Vedant]
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
│       └── baseline.csv   [NEW · Brahmanand]
├── scripts/
│   ├── hardware_check.py
│   ├── quick_frozenlake_check.py
│   └── run_baseline.py   [NEW · Brahmanand]
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
│       │   ├── evaluate.py   [NEW · Vedant]
│       │   ├── metrics.py   [NEW · Vedant]
│       │   └── plots.py
│       ├── learning/
│       │   ├── __init__.py
│       │   ├── dqn.py
│       │   ├── guards.py   [NEW · Atharv]
│       │   ├── networks.py
│       │   ├── q_learning.py
│       │   └── schedules.py
│       ├── memory/
│       │   ├── __init__.py
│       │   ├── episode_store.py
│       │   ├── replay_buffer.py
│       │   └── retention.py
│       ├── reflection/
│       │   └── __init__.py
│       ├── ui/
│       │   ├── __init__.py
│       │   └── feedback.py   [NEW · Somesh]
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   ├── errors.py
│       │   ├── io_helpers.py
│       │   ├── logging_setup.py
│       │   ├── seeding.py
│       │   ├── summary.py
│       │   └── validation.py   [MODIFIED · Somesh]
│       ├── __init__.py
│       ├── cli.py   [MODIFIED · Brahmanand]
│       └── pipeline.py   [NEW · Brahmanand]
├── tests/
│   ├── integration/
│   │   ├── test_dqn_smoke.py
│   │   ├── test_pipeline_e2e.py   [NEW · Brahmanand]
│   │   ├── test_resume.py
│   │   ├── test_runner.py
│   │   └── test_transition_validation.py   [NEW · Somesh]
│   ├── unit/
│   │   ├── test_agents.py
│   │   ├── test_cli_help.py
│   │   ├── test_config.py
│   │   ├── test_dqn.py
│   │   ├── test_envs.py
│   │   ├── test_episode_store.py
│   │   ├── test_evaluate.py   [NEW · Vedant]
│   │   ├── test_feedback.py   [NEW · Somesh]
│   │   ├── test_guards.py   [NEW · Atharv]
│   │   ├── test_io_helpers.py
│   │   ├── test_logging.py
│   │   ├── test_metrics.py   [NEW · Vedant]
│   │   ├── test_plots.py
│   │   ├── test_q_learning.py
│   │   ├── test_replay_buffer.py
│   │   ├── test_safety.py
│   │   ├── test_schedules.py
│   │   ├── test_summary.py
│   │   └── test_validation.py   [MODIFIED · Somesh]
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

13-step flow as every week. Week-6 issues:

| # | Title | Owner | Branch | Reviewer | Merge by |
|---|---|---|---|---|---|
| 61 | Frozen-policy evaluator + protocol | Vedant | `feat/vedant-61-evaluator` | Brahmanand | **Day 2** |
| 62 | Learning metrics | Vedant | `feat/vedant-62-metrics` | Somesh | Day 3 |
| 64 | Divergence guard + regression monitor | Atharv | `feat/atharv-64-guards` | Brahmanand | **Day 3** |
| 65 | Five-seed results + DQN config | Atharv | `exp/atharv-65-five-seed-runs` | Vedant | Day 6 |
| 66 | Pipeline + `sla evaluate` | Brahmanand | `feat/brahmanand-66-pipeline-evaluate` | Vedant | **Day 4** |
| 67 | Baselines | Brahmanand | `feat/brahmanand-67-baseline` | Atharv | Day 5 |
| 68 | Transition validation | Somesh | `feat/somesh-68-transition-validation` | Vedant | **Day 3** |
| 69 | Note rating helper | Somesh | `feat/somesh-69-feedback` | Vedant | Day 6 |

**Experiment branches (`exp/…`)** contain configs and result notes, not code changes. A result PR must say in its description: the command used, the commit (`git rev-parse --short HEAD`) and the laptop it ran on.

---

## SECTION 8 — WEEKLY INTEGRATION PROCEDURE

| Item | This week |
|---|---|
| Modules to connect | runner ↔ six callbacks via `pipeline.default_callbacks`; evaluator ↔ checkpoints + store (`log_eval`); guards ↔ `ctx.extra["eval_history"]` and DQN `last_loss/last_max_q`; CLI ↔ pipeline; baseline ↔ evaluator. |
| Integrator | **Brahmanand** (integration captain, Weeks 6–7). |
| Interfaces that must match | `PeriodicEvalCallback` writes `ctx.extra["eval_history"]` as `(episode, mean)` tuples; `RegressionMonitor` reads it; `best/checkpoint.json` has `eval_mean`; `metrics.json` key `final_eval` (used by Week-8 scripts). |
| Tests that must pass | all; especially `test_pipeline_e2e.py`, `test_evaluate.py`, `test_transition_validation.py`. |
| Detect failures | `metrics.json` missing; eval rows count ≠ episodes / `eval_every`; `sla evaluate` score ≠ `metrics.json` score for the same checkpoint. |
| Debug | query the `evals` table (`EpisodeStore("runs/episodes.db").query_evals(run_id)` in Python, or DB Browser for SQLite); read the warnings printed in the terminal ("Regression flagged", "Divergence"). |

**Integration checklist**
- [ ] `sla train` writes `metrics.json` and `checkpoints/best/` for both agents
- [ ] `sla resume` still works (now with all six callbacks)
- [ ] `sla evaluate` reproduces the final score
- [ ] Runner unchanged this week
- [ ] CI green on `main`

---

## SECTION 9 — TESTING AND VALIDATION

| Type | Tests this week | Command |
|---|---|---|
| Unit | `test_evaluate` (4), `test_metrics` (6), `test_guards` (3), `test_validation` (W6 part), `test_feedback` (5) | `pytest tests/unit -v` |
| Integration | `test_pipeline_e2e` (W6), `test_transition_validation` (2) | `pytest tests/integration -v` |
| Input/reward validation | NaN/inf/out-of-range rewards, illegal actions, bad ratings/comments | as above |
| Reproducibility | baseline CSV identical on re-run; `sla evaluate` = `metrics.json` | manual, recorded in PRs |
| Model evaluation | 5 seeds, test seeds, trained vs random vs untrained DQN | `docs/notes/week6_results.md` |

**RL rules applied this week (mandatory):**
1. Training and evaluation are separate code paths; evaluation never calls `update()` and uses `explore=False`.
2. Evaluation seeds are fixed and never overlap training seeds (tested).
3. Validation seeds choose the checkpoint; test seeds produce the reported number — never the other way round.
4. Trained agents are always compared with the untrained/random baseline.
5. No result is invented, rounded up, or copied from a paper. A seed that failed stays in the table.

---

## SECTION 10 — COMMON PROBLEMS AND SOLUTIONS

| Problem | Possible Cause | How to Check | Solution |
|---|---|---|---|
| Final score much lower than training reward on FrozenLake | slippery map or greedy policy loops until the step limit | `end_reason` counts in DB | check `is_slippery: false`; train longer |
| `sla evaluate` score differs from `metrics.json` | different checkpoint or seed base | compare checkpoint folder and `seed_base` in `metrics.json` | use `checkpoints/best`; `TEST_SEED_BASE` |
| Training stopped with `divergence` | lr too high, target network off | terminal log, `agent.last_max_q` | lower lr; keep `target_net_enabled: true` |
| Many "Regression flagged" warnings | noisy eval with few episodes | `evals` table | normal for DQN; best checkpoint is kept; consider `eval_episodes: 20` |
| `ValidationError: Reward ... outside the expected range` | wrong `REWARD_RANGES` entry or env wrapper | print the reward | fix the range only if the env really gives that reward |
| DQN 5-seed runs too slow | CPU-only laptop | minutes per 50 episodes in log | split seeds across laptops; run overnight; never reduce test episodes |
| `torch` missing on one laptop | install problem | `python -c "import torch"` | that laptop runs FrozenLake + baseline without `--with-untrained-dqn` |
| Results table has a number nobody can find | typed by hand | Vedant's cross-check | regenerate from `metrics.json` (Week-8 script automates this) |

---

## SECTION 11 — WEEKLY DELIVERABLES

| Deliverable | Owner | File/Location | Verification | Status |
|---|---|---|---|---|
| Train-and-evaluate pipeline | Brahmanand | `src/sla/pipeline.py` | `test_pipeline_e2e` (W6) | [ ] |
| CLI `train` (evaluates) + `evaluate` | Brahmanand | `src/sla/cli.py` | `sla evaluate` = `metrics.json` | [ ] |
| Baselines | Brahmanand | `scripts/run_baseline.py`, `results/baseline/baseline.csv` | reproducible CSV | [ ] |
| Guards | Atharv | `src/sla/learning/guards.py` | 3 tests | [ ] |
| Five-seed results + config log | Atharv | `docs/notes/week6_results.md`, `configs/cartpole_dqn.yaml` | Vedant cross-check | [ ] |
| Evaluator + protocol | Vedant | `src/sla/evaluation/evaluate.py`, `docs/evaluation_protocol.md` | 4 tests | [ ] |
| Metrics | Vedant | `src/sla/evaluation/metrics.py` | 6 tests | [ ] |
| Transition validation | Somesh | `src/sla/utils/validation.py` (W6) | unit + integration tests | [ ] |
| Note rating helper | Somesh | `src/sla/ui/feedback.py` | 5 tests | [ ] |

---

## SECTION 12 — WEEKLY REVIEW MEETING

**Agenda:** demo (`sla train` → `metrics.json` → `sla evaluate`) · results table walk-through · completed/pending · blockers · code quality · tests · PRs · integration · Week-7 dependencies.

**Questions:**
1. Vedant: name the three seed ranges and what each is allowed to be used for.
2. Why is evaluating on the training seeds misleading?
3. Why does `final_evaluation` use the *best* checkpoint, and why is choosing it with test seeds forbidden?
4. Atharv: what is the difference between divergence and regression, and why does only one of them stop training?
5. Somesh: show the test where a NaN reward stops training. Why is the reward the most important value to validate?
6. Brahmanand: why does `RegressionMonitor` come after `PeriodicEvalCallback`?
7. Does the trained DQN beat the untrained DQN on all 5 seeds? If not, which seed and why might that be?
8. Where does each number in the results table come from (file + commit)?

---

## SECTION 13 — WEEK COMPLETION CHECKLIST

- [ ] All assigned tasks completed
- [ ] Code pushed to feature branches
- [ ] Pull requests reviewed and merged (#61, #64, #68 before #66)
- [ ] All tests pass locally and in CI
- [ ] Six callbacks integrated through `default_callbacks`; runner unchanged
- [ ] `docs/evaluation_protocol.md` and `docs/notes/week6_results.md` merged
- [ ] Weekly demonstration completed
- [ ] Blockers recorded (e.g. seeds that did not learn)

---

## SECTION 14 — NEXT WEEK HANDOFF

- **Ready before Week 7:** `pipeline.train_and_evaluate`, `evaluate.py`, `metrics.py`, `guards.py`, transition validation, `feedback.py`, baseline CSV, frozen `configs/cartpole_dqn.yaml`, Week-6 results note.
- **Files Week 7 depends on:** `pipeline.py` (Week 7 appends `run_pipeline`), `metrics.py` (reflection facts), `evaluate.py` + `pipeline.train_and_evaluate` (ablation), `feedback.py` (Reflection page), `plots.py` (Results page), the `reflections` table (Vedant).
- **Coordination:** Somesh starts Streamlit pages in Week 7 — Atharv pairs with him (2 × 45 min). Vedant's `reflect()` signature must be agreed with Brahmanand on Week-7 Day 1 (`reflect(store, run_id, use_llm, client)`).
- **Risks:** DQN results may vary a lot across seeds — the Week-7 statistics (Welch t-test, bootstrap CI) will show this honestly; Ollama is **optional** — every Week-7 feature must work without it.
