# WEEK 04 — Core AI Agent Development

**Project:** Self-Learning AI Agent · **Team:** Brahmanand Mathpati, Atharv Gundale, Vedant Biradar, Somesh Badwane
**Source:** *Self_Learning_AI_Agent_10_Week_Master_Plan* (v1.0) · **Interfaces:** `docs/design.md` (tag `w2-design-freeze`)

---

## SECTION 1 — WEEK OVERVIEW

| Item | Details |
|---|---|
| Week number | 4 of 10 |
| Week title | Core AI Agent Development |
| Main objective | Build the **training loop** and the **first agent that genuinely learns** (tabular Q-learning on FrozenLake), and write — and unit-test — the DQN, the replay buffer and the exploration schedule. |
| Expected outcome | `run_training()` trains any agent with safety limits and plug-in callbacks; Q-learning reaches the FrozenLake goal; DQN + replay buffer pass their unit tests; Somesh's validation and summary helpers are used by the runner. |
| Required knowledge | Week-2 RL theory: Q-table, ε-greedy, Bellman update, terminated vs truncated, DQN, replay buffer, target network. Python: classes, dataclasses, NumPy arrays; PyTorch basics (Atharv). |
| Required tools | Project venv with `pip install -e ".[dev]"` and PyTorch CPU (installed in Week 3). |
| Prerequisites from previous weeks | Week 3 merged: `config.py`, `errors.py`, `logging_setup.py`, `seeding.py`, `envs/factory.py`, `agent/base.py`, `random_agent.py`, CI green. |
| Approximate workload | 11 h per member. |
| Technical dependencies | Atharv's `schedules.py` merged by **Day 2** (Q-learning imports it). Somesh's `summary.py` merged by **Day 3** (runner imports it). Vedant's `replay_buffer.py` merged by **Day 3** (DQN imports it). |
| Definition of Done | All Week-4 tests pass in CI; `scripts/quick_frozenlake_check.py` shows Q-learning reaching the goal in its greedy episode for all 5 seeds on non-slippery FrozenLake (the **target** — record what you actually get); DQN unit tests pass (TD target, loss decreases, target frozen, save/load); runner stops at step and wall-clock limits. |

**In simple words:** this is the week the agent first *learns*. By Friday we watch a Q-table start at all zeros and end up knowing the safe path across the frozen lake.

---

## SECTION 2 — WHAT WE ARE BUILDING THIS WEEK

1. **Modules:** `agent/runner.py` + `agent/safety.py` + `learning/q_learning.py` (Brahmanand) · `learning/schedules.py`, `learning/networks.py`, `learning/dqn.py` (Atharv) · `memory/replay_buffer.py` (Vedant) · `utils/validation.py` (run-request part) + `utils/summary.py` (Somesh).
2. **Why:** the runner is the heart of the system — the only place where the agent acts, gets reward and updates. Q-learning proves the loop works on a small problem before the harder DQN.
3. **Connection:** from Week 5 on, storage, checkpoints, evaluation, guards and validation all plug into the runner as **callbacks**, so `runner.py` does not change again.
4. **If missing:** nothing can be trained; every later week is blocked.
5. **Final output:**
   ```text
   $ python scripts/quick_frozenlake_check.py
   seed 0: training success (last 100 episodes) 0.9x | greedy episode reward 1.0
   ...
   seed 4: training success (last 100 episodes) 0.9x | greedy episode reward 1.0
   ```
   (Your exact numbers will differ. Training success is below 1.0 because ε-greedy still explores; the greedy episode shows what was learned.)

**Analogy:** the runner is a driving-school car; the agent is the learner driver. The car (runner) is the same whether the learner is a beginner (random agent), uses a notebook of rules (Q-table) or has a trained intuition (neural network).

### How the pieces fit (one step)
```text
state ──► agent.act(state, explore=True) ──► action ──► env.step(action)
  ▲                                                        │
  │      Transition(state, action, reward, next_state, terminated, truncated)
  │                                                        ▼
  └─────────── agent.update(transition)  ◄── callbacks.on_step(transition)
```

---

## SECTION 3 — DAILY EXECUTION PLAN

### Day 1 — Small building blocks first (1.5 h)
- **Daily objective:** tiny dependencies merged early so nobody waits later.
- **Assigned members:** all.
- **Individual tasks:** Atharv: `schedules.py` + `test_schedules.py` (SLA-04-AG-1 steps 1–2) and opens PR. Vedant: replay buffer steps 1–3. Brahmanand: `safety.py` + `test_safety.py` (SLA-04-BM-1 steps 1–2). Somesh: learning part of SLA-04-SB-1 (comprehensions, default arguments).
- **Required commands:**
  ```bash
  git checkout main && git pull
  pip install -e ".[dev]"          # picks up any dependency changes
  pytest -q                         # everything from Week 3 must still pass
  ```
- **Expected files:** `src/sla/learning/schedules.py`, `src/sla/agent/safety.py` (+ tests).
- **Expected output:** `pytest tests/unit/test_schedules.py tests/unit/test_safety.py` passes.
- **GitHub activity:** PRs #41 (safety), #45 (schedules) opened.
- **Completion checklist:** - [ ] schedules PR open · - [ ] safety PR open

### Day 2 — Q-learning and replay buffer (1.5 h)
- **Daily objective:** Q-learning update matches the Week-1 hand calculation; buffer tested.
- **Assigned members:** Brahmanand (Q-learning), Vedant (buffer tests), Atharv (networks.py; review schedules → merge), Somesh (validation functions).
- **Individual tasks:** SLA-04-BM-2 steps 1–4 · SLA-04-VB-1 steps 4–6 · SLA-04-AG-1 step 3 · SLA-04-SB-1 steps 1–4.
- **Expected files:** `learning/q_learning.py`, `tests/unit/test_q_learning.py`, `tests/unit/test_replay_buffer.py`, `learning/networks.py`, `utils/validation.py`.
- **Testing steps:** `pytest tests/unit/test_q_learning.py -v` — `test_update_matches_hand_calculation` must give 0.45.
- **GitHub activity:** schedules PR merged (Q-learning depends on it).
- **Completion checklist:** - [ ] hand-calculation test passes

### Day 3 — Summary helper, buffer merged, DQN agent (1.5 h)
- **Daily objective:** dependencies for runner and DQN merged.
- **Assigned members:** Somesh (summary.py + tests → PR), Vedant (buffer PR merged), Atharv (dqn.py), Brahmanand (reviews Somesh, starts runner).
- **Individual tasks:** SLA-04-SB-1 steps 5–8 · SLA-04-VB-1 step 7 · SLA-04-AG-1 steps 4–5 · SLA-04-BM-1 step 3.
- **Expected files:** `utils/summary.py`, `learning/dqn.py`.
- **GitHub activity:** PRs #47 (buffer) and #48 (validation + summary) merged after review.
- **Completion checklist:** - [ ] buffer merged · - [ ] summary merged

### Day 4 — Runner (1.5 h)
- **Daily objective:** `run_training` works with the random agent and Q-learning.
- **Assigned members:** Brahmanand (runner), Atharv (DQN tests), Vedant (reviews DQN's buffer use), Somesh (helps test runner with a bad seed list).
- **Individual tasks:** SLA-04-BM-1 steps 4–7 · SLA-04-AG-1 step 6.
- **Required commands:**
  ```bash
  pytest tests/integration/test_runner.py -v
  python scripts/quick_frozenlake_check.py
  ```
- **Expected output:** 4 runner tests pass; quick check prints 5 lines.
- **Completion checklist:** - [ ] runner tests green

### Day 5 — DQN maths session and integration (1.5 h)
- **Daily objective:** whole team understands the DQN update; DQN tests merged.
- **Assigned members:** Atharv leads a 45-min session (Section 5.4 notes); others review PRs.
- **Individual tasks:** SLA-04-AG-2 · everyone reads `docs/notes/dqn_explained.md`.
- **Testing steps:** each member hand-computes one TD target from the session sheet.
- **Completion checklist:** - [ ] session done · - [ ] DQN tests pass in CI

### Day 6 — Merge, tune, measure (2.5 h)
- **Daily objective:** all Week-4 PRs merged; Q-learning check run on all 4 laptops.
- **Assigned members:** all.
- **Individual tasks:** fix review comments; Brahmanand tries `is_slippery: true` and records the result honestly in the PR description; Somesh and Vedant run `quick_frozenlake_check.py` on their laptops.
- **Required commands:** `git checkout main && git pull && pytest && python scripts/quick_frozenlake_check.py`
- **Completion checklist:** - [ ] all PRs merged · - [ ] results recorded

### Day 7 — Weekly review (1 h)
- **Daily objective:** live demo: fresh `main`, run the quick check; Atharv explains a DQN update; Section 12 agenda.
- **Completion checklist:** - [ ] Section 13 complete

---

## SECTION 4 — INDIVIDUAL MEMBER TASKS

### Brahmanand Mathpati

**Task ID:** SLA-04-BM-1
**Task Title:** Training loop (runner) with safety limits and callbacks
**Priority:** P1
**Estimated Duration:** 6 h (learning 1, coding 3, testing 1, review 1)
**Dependencies:** Week-3 modules; `summary.py` (Somesh, Day 3); `schedules.py` (Atharv, Day 2)
**Assigned Member:** Brahmanand Mathpati

1. **What:** `src/sla/agent/safety.py` (`SafetyLimits`, `check_finite`) and `src/sla/agent/runner.py` (`EpisodeInfo`, `RunContext`, `RunResult`, `Callback`, `make_run_id`, `build_agent`, `run_training`).
2. **Why:** the single training loop used by every agent and every later feature.
3. **Files:** create `agent/safety.py`, `agent/runner.py`, `tests/unit/test_safety.py`, `tests/integration/test_runner.py`, `tests/conftest.py`.
4. **Functions/classes:** as listed in item 1 — exact code in Section 5.1.
5. **Inputs:** a `RunConfig`; optional callbacks, agent, run folder, run id, start episode.
6. **Outputs:** `RunResult` (returns per episode, lengths, stop reason); `runs/<run_id>/config.yaml`.
7. **Steps:**
   1. Write `safety.py` and `test_safety.py` (Section 5.1). Run the tests.
   2. Open PR #41.
   3. Write the dataclasses and `Callback` at the top of `runner.py`.
   4. Write `build_agent` (lazy imports: PyTorch is imported only when `agent == "dqn"`).
   5. Write `run_training` exactly in the order of the design's paper trace.
   6. Write `tests/conftest.py` (the `fl_cfg` fixture) and `tests/integration/test_runner.py`.
   7. Run all tests; open PR #42.
8. **Commands:**
   ```bash
   git checkout -b feat/brahmanand-42-agent-runner
   pytest tests/unit/test_safety.py tests/integration/test_runner.py -v
   ruff check src tests
   git add src/sla/agent/runner.py tests/conftest.py tests/integration/test_runner.py
   git commit -m "feat(agent): add training loop with callbacks and safety limits"
   git push -u origin feat/brahmanand-42-agent-runner
   ```
9. **Tests:** callbacks are called and can stop training; step limit truncates; same seed gives identical returns; Q-learning beats random on FrozenLake.
10. **Expected result:** `4 passed` in `test_runner.py`; `2 passed` in `test_safety.py`.
11. **Common errors:** forgetting `env.reset(seed=episode_seed(...))` → runs are not reproducible; reusing `state` instead of `next_state` → agent never moves forward; treating `truncated` as `terminated` in the Transition.
12. **Branches:** `feat/brahmanand-41-safety-limits`, `feat/brahmanand-42-agent-runner`
13. **Commits:** `feat(agent): add safety limits` · `feat(agent): add training loop with callbacks and safety limits`
14. **PR titles:** `feat: safety limits (SLA-04-BM-1a)` · `feat: training loop with callbacks (SLA-04-BM-1b)`
15. **Acceptance:** runner tests pass; runner stops at each limit; reviewer: Atharv.

**Task ID:** SLA-04-BM-2
**Task Title:** Tabular Q-learning agent and FrozenLake check
**Priority:** P1
**Estimated Duration:** 5 h (learning 1, coding 2, testing 1, docs 1)
**Dependencies:** `schedules.py` (Atharv, Day 2); Week-1 worked example
**Assigned Member:** Brahmanand Mathpati

1. **What:** `src/sla/learning/q_learning.py` (`q_learning_update`, `QLearningAgent`) and `scripts/quick_frozenlake_check.py`.
2. **Why:** first agent that genuinely learns; its numbers are checked against your Week-1 hand calculation.
3. **Files:** `learning/q_learning.py`, `tests/unit/test_q_learning.py`, `scripts/quick_frozenlake_check.py`.
4. **Functions/classes:** `q_learning_update(q, s, a, r, s_next, terminated, alpha, gamma) -> float`; `QLearningAgent(n_states, n_actions, learning_rate, gamma, epsilon_schedule, seed)` with `act`, `greedy_action`, `update`, `epsilon`, `save`, `load`.
5. **Inputs:** FrozenLake states (integers 0–15) and actions (0 left, 1 down, 2 right, 3 up).
6. **Outputs:** an updated Q-table (16 × 4 NumPy array).
7. **Steps:**
   1. Write `q_learning_update` first and its two tests (hand calculation; terminal does not bootstrap).
   2. Write `QLearningAgent`; note `greedy_action` breaks ties randomly — at the start the whole table is 0 and `argmax` would always pick action 0.
   3. Write save/load (Q-table as `.npy`, settings and RNG state in `meta.json`).
   4. Run the unit tests.
   5. After the runner is merged, run `scripts/quick_frozenlake_check.py`; paste the output in the PR.
   6. Change `configs/frozenlake_q.yaml` to `is_slippery: true` on your laptop only, run again, record the (usually much lower) result in the PR — then change it back. Slippery FrozenLake is hard; an honest lower number is fine.
8. **Commands:**
   ```bash
   git checkout -b feat/brahmanand-43-q-learning
   pytest tests/unit/test_q_learning.py -v
   python scripts/quick_frozenlake_check.py
   git add src/sla/learning/q_learning.py tests/unit/test_q_learning.py scripts/quick_frozenlake_check.py
   git commit -m "feat(learning): add tabular Q-learning agent"
   git push -u origin feat/brahmanand-43-q-learning
   ```
9. **Tests:** 5 tests in `test_q_learning.py` (Section 5.2).
10. **Expected result:** all tests pass; greedy episode reward 1.0 for each seed (target).
11. **Common errors:** `IndexError` → passing a NumPy array as state instead of an int (`int(state)`); agent never reaches the goal → ε decays too fast (check `epsilon_decay_steps`) or ties always pick 0.
12. **Branch:** `feat/brahmanand-43-q-learning`
13. **Commit:** `feat(learning): add tabular Q-learning agent`
14. **PR title:** `feat: tabular Q-learning (SLA-04-BM-2)`
15. **Acceptance:** hand-calculation test passes; FrozenLake result recorded honestly for 5 seeds; reviewer: Atharv.

### Atharv Gundale

**Task ID:** SLA-04-AG-1
**Task Title:** Exploration schedule, Q-network and DQN agent (unit-level)
**Priority:** P1
**Estimated Duration:** 9 h (learning 1, coding 5, testing 2, docs 1)
**Dependencies:** `agent/base.py` (W3); `replay_buffer.py` (Vedant, Day 3)
**Assigned Member:** Atharv Gundale

1. **What:** `learning/schedules.py` (`LinearSchedule`), `learning/networks.py` (`QNetwork`), `learning/dqn.py` (`compute_td_target`, `DQNAgent`).
2. **Why:** the DQN is the main learning component for CartPole.
3. **Files:** the three modules + `tests/unit/test_schedules.py`, `tests/unit/test_dqn.py`.
4. **Functions/classes:** `LinearSchedule.value(step)`; `QNetwork(obs_dim, n_actions, hidden_size)`; `DQNAgent` with `act`, `q_values`, `update`, `train_step`, `sync_target`, `save`, `load`.
5. **Inputs:** CartPole observations (4 floats), actions {0, 1}, `DQNConfig` from `utils/config.py`.
6. **Outputs:** loss values; updated network weights; checkpoints (`dqn.pt`, `meta.json`, optional `replay.npz`).
7. **Steps:**
   1. `schedules.py` + `test_schedules.py` → PR #45 on Day 1 (others depend on it).
   2. Merge it on Day 2 after Brahmanand's review.
   3. `networks.py` (4 → 128 → 128 → 2).
   4. `dqn.py`: acting (ε-greedy), `update` (push → train every `train_freq` once `learning_starts` reached → sync target every `target_update_every`), `train_step` (Huber loss, gradient clipping), ablation flags.
   5. Save/load including optimizer, step counters and RNG states.
   6. Write `tests/unit/test_dqn.py` (Section 5.3); run; PR #46.
8. **Commands:**
   ```bash
   git checkout -b feat/atharv-46-dqn
   pytest tests/unit/test_dqn.py -v
   git add src/sla/learning/networks.py src/sla/learning/dqn.py tests/unit/test_dqn.py
   git commit -m "feat(learning): add DQN agent with replay and target network"
   git push -u origin feat/atharv-46-dqn
   ```
9. **Tests:** TD target by hand; network output shape; loss falls on a fixed batch; target network unchanged for 499 steps and equal to online after step 500; save → load gives identical greedy actions.
10. **Expected result:** `5 passed` in `test_dqn.py`, `3 passed` in `test_schedules.py`.
11. **Common errors:** `RuntimeError: Index tensor must have the same number of dimensions` → `actions.unsqueeze(1)` before `gather`; loss NaN → forgot gradient clipping or used a huge learning rate; `torch.load` error with `weights_only` → save only state dicts (we do).
12. **Branches:** `feat/atharv-45-schedules`, `feat/atharv-46-dqn`
13. **Commits:** `feat(learning): add linear epsilon schedule` · `feat(learning): add DQN agent with replay and target network`
14. **PR titles:** `feat: epsilon schedule (SLA-04-AG-1a)` · `feat: DQN agent (SLA-04-AG-1b)`
15. **Acceptance:** all DQN unit tests pass in CI (no training to convergence yet — that is Week 6); reviewer: Brahmanand (schedules), Vedant (DQN — checks buffer use).

**Task ID:** SLA-04-AG-2
**Task Title:** DQN maths session and `docs/notes/dqn_explained.md`
**Priority:** P2
**Estimated Duration:** 2 h (mentoring/session 1, docs 1)
**Dependencies:** SLA-04-AG-1
**Assigned Member:** Atharv Gundale

1. **What:** a 45-minute team session + a 1–2 page note (outline in Section 5.4).
2. **Why:** every member must explain the DQN in the viva, not just Atharv.
3. **File:** `docs/notes/dqn_explained.md`.
4. **Function/class:** explains `compute_td_target`, `train_step`, `sync_target`.
5. **Inputs:** the code and the design §F.
6. **Outputs:** note + a 3-question quiz in the note.
7. **Steps:** write the note → run the session → each member computes one TD target → record answers.
8. **Commands:** branch `docs/atharv-49-dqn-notes`, add, commit, push, PR.
9. **Tests:** quiz answered correctly by all three members.
10. **Expected result:** everyone explains "why a target network" in one sentence.
11. **Common errors:** too much maths — use the CartPole example and numbers.
12. **Branch:** `docs/atharv-49-dqn-notes`
13. **Commit:** `docs(notes): explain DQN update for the team`
14. **PR title:** `docs: DQN explained (SLA-04-AG-2)`
15. **Acceptance:** note reviewed by Brahmanand; quiz done.

### Vedant Biradar

**Task ID:** SLA-04-VB-1
**Task Title:** Replay buffer
**Priority:** P1
**Estimated Duration:** 11 h (learning 2, coding 4, testing 3, integration 1, docs 1)
**Dependencies:** design §G
**Assigned Member:** Vedant Biradar

1. **What:** `src/sla/memory/replay_buffer.py` (`Batch`, `ReplayBuffer`) and `tests/unit/test_replay_buffer.py`.
2. **Why:** experience replay is one of the two DQN ideas that make deep RL stable; it is also our **short-term memory**.
3. **Files:** as above.
4. **Functions/classes:** `ReplayBuffer(capacity, obs_dim, seed)` with `push`, `sample`, `latest`, `__len__`, `save`, `load_from`.
5. **Inputs:** transitions (state, action, reward, next state, terminated).
6. **Outputs:** `Batch` of NumPy arrays with fixed dtypes (float32 states/rewards/terminated, int64 actions).
7. **Steps:**
   1. Learn: NumPy preallocated arrays and the "circular buffer" idea (write position wraps with `% capacity`).
   2. Create arrays in `__init__`.
   3. Write `push` (store at `pos`, then `pos = (pos + 1) % capacity`, `size = min(size + 1, capacity)`).
   4. Write `sample` with `rng.choice(size, batch, replace=False)`.
   5. Write `latest` (used by the no-replay ablation in Week 7) and `save/load_from` (used by checkpoints in Week 5).
   6. Write 6 tests (Section 5.5); run with coverage.
   7. Open PR #47; merge by Day 3 (DQN depends on it).
8. **Commands:**
   ```bash
   git checkout -b feat/vedant-47-replay-buffer
   pytest tests/unit/test_replay_buffer.py -v --cov=sla.memory.replay_buffer --cov-report=term-missing
   git add src/sla/memory/replay_buffer.py tests/unit/test_replay_buffer.py
   git commit -m "feat(memory): add circular replay buffer with seeded sampling"
   git push -u origin feat/vedant-47-replay-buffer
   ```
9. **Tests:** wrap-around after capacity; shapes and dtypes; seeded sampling repeats; errors on empty/oversized samples; `latest` is newest; save/load round trip.
10. **Expected result:** `6 passed`, coverage ≥ 90 % for the module.
11. **Common errors:** using a Python list and `pop(0)` (slow) — use arrays; sampling with replacement (allowed duplicates) — we use `replace=False`.
12. **Branch:** `feat/vedant-47-replay-buffer`
13. **Commit:** `feat(memory): add circular replay buffer with seeded sampling`
14. **PR title:** `feat: replay buffer (SLA-04-VB-1)`
15. **Acceptance:** ≥ 90 % coverage; tests pass in CI; reviewer: Atharv.

### Somesh Badwane

**Task ID:** SLA-04-SB-1
**Task Title:** Run-request validation and episode-summary printer
**Priority:** P2
**Estimated Duration:** 11 h (learning 3, coding 4, testing 2, review 1, docs 1)
**Dependencies:** `config.py` (your Week 3), `errors.py` (Vedant, Week 3)
**Assigned Member:** Somesh Badwane

**0. Learn first (Section 5.6, ~3 h):** `for` loops over lists, list comprehensions, `isinstance`, default arguments, `raise`, regular expressions (just one pattern), and *why* we check `bool` before `int` (in Python `True` is an `int`!).

1. **What:** in `src/sla/utils/validation.py`: `validate_seeds`, `validate_env_name`, `validate_episode_count`, `safe_run_name`; in `src/sla/utils/summary.py`: `rolling_mean`, `format_episode_summary`.
2. **Why:** the UI (Week 7) uses your validators so users cannot start a run with nonsense input; the runner prints your summary line every `eval_every` episodes; the plots (Week 5) use `rolling_mean`.
3. **Files:** create `utils/validation.py`, `utils/summary.py`, `tests/unit/test_validation.py`, `tests/unit/test_summary.py`.
4. **Functions:** as item 1 (exact code in Section 5.6).
5. **Inputs:** lists of seeds, environment names, episode counts, free text for names; lists of rewards.
6. **Outputs:** clean values or a `ValidationError` with a clear message; a summary string.
7. **Steps:**
   1. Do the Section 5.6 exercises.
   2. Create `validation.py` with the Week-4 part (Section 5.6). Read each line's explanation.
   3. Write the validation tests; use `@pytest.mark.parametrize` to test many bad inputs with one test function.
   4. Run them.
   5. Create `summary.py` and its tests.
   6. Run `pytest tests/unit/test_validation.py tests/unit/test_summary.py -v`.
   7. Open PR #48 by Day 3 (Brahmanand's runner imports `format_episode_summary`).
   8. Ask Brahmanand to show you where the runner calls your function.
8. **Commands:**
   ```bash
   git checkout main && git pull
   git checkout -b feat/somesh-48-validation-summary
   pytest tests/unit/test_validation.py tests/unit/test_summary.py -v
   ruff check src/sla/utils tests/unit
   git add src/sla/utils/validation.py src/sla/utils/summary.py tests/unit/test_validation.py tests/unit/test_summary.py
   git commit -m "feat(utils): add run-request validation and episode summary"
   git push -u origin feat/somesh-48-validation-summary
   ```
9. **Tests:** duplicates removed in order; bad seeds (`[]`, `[-1]`, `[1.5]`, `[True]`, `["2"]`) rejected; unknown env rejected; bad episode counts rejected; unsafe names cleaned (`"../../etc/passwd"` → `"etc_passwd"`); rolling mean; summary line format.
10. **Expected result:** about 20 test cases pass (parametrize makes each bad input its own case).
11. **Common errors:** `True` accepted as a seed → check `isinstance(seed, bool)` *before* `isinstance(seed, int)`; regex error → copy the pattern exactly; `ruff` says "line too long" → break the line inside brackets.
12. **Branch:** `feat/somesh-48-validation-summary`
13. **Commit:** `feat(utils): add run-request validation and episode summary`
14. **PR title:** `feat: run-request validation and summary (SLA-04-SB-1)`
15. **Acceptance:** tests pass; runner uses `format_episode_summary`; reviewer: **Vedant** (from this week Vedant reviews most of Somesh's PRs; Atharv keeps mentoring).

**How to make the PR:** same as Week 1–3; add label `week-4`, reviewer Vedant, link `Closes #48`.

**Independent practice exercise:** write `validate_learning_rate(value)` that accepts floats in (0, 1] and rejects everything else (including `True`). Write 4 parametrized tests. Show Atharv in your mentoring session; do not commit.

---

## SECTION 5 — COMPLETE TECHNICAL IMPLEMENTATION

### 5.1 Runner and safety (Brahmanand)

`src/sla/agent/safety.py`
```python
"""Safety limits for training (owner: Brahmanand, Week 4).

They stop runaway runs: too many steps, too much time, or broken numbers.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass

from sla.utils.errors import TrainingError


@dataclass
class SafetyLimits:
    max_steps_per_episode: int = 500
    max_episodes: int = 100_000
    max_wall_clock_s: float = 3_600.0

    @classmethod
    def from_config(cls, cfg) -> SafetyLimits:
        return cls(cfg.max_steps_per_episode, cfg.episodes, cfg.max_wall_clock_s)

    def wall_clock_exceeded(self, start_time: float) -> bool:
        return (time.monotonic() - start_time) > self.max_wall_clock_s

    def step_limit_reached(self, steps: int) -> bool:
        return steps >= self.max_steps_per_episode


def check_finite(value: float, name: str) -> float:
    """Raise TrainingError if ``value`` is NaN or infinite (e.g. a broken reward or loss)."""
    if not math.isfinite(float(value)):
        raise TrainingError(f"{name} is not a finite number: {value!r}")
    return float(value)
```

`src/sla/agent/runner.py` — the complete file. Important points: (1) each episode resets with `episode_seed(cfg.seed, episode)`, which makes resume exact in Week 5; (2) the runner forces `truncated=True` at the step limit; (3) `build_agent` imports Q-learning/DQN *inside* the function so FrozenLake runs work even on a laptop where PyTorch is broken; (4) any callback returning `True` stops training cleanly.
```python
"""The training loop (owner: Brahmanand, Week 4).

``run_training`` is the only place where an agent learns. Other features
(storage, checkpoints, evaluation, guards, validation) plug in as callbacks,
so this file does not need to change after Week 4.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

from sla.agent.base import Agent, Transition
from sla.agent.safety import SafetyLimits, check_finite
from sla.envs.factory import end_reason, make_env
from sla.utils.config import RunConfig, save_config
from sla.utils.logging_setup import get_logger
from sla.utils.seeding import episode_seed, set_global_seed
from sla.utils.summary import format_episode_summary

log = get_logger(__name__)


@dataclass
class EpisodeInfo:
    episode: int
    total_reward: float
    length: int
    epsilon: float | None
    mean_loss: float | None
    end_reason: str
    wall_time_s: float


@dataclass
class RunContext:
    cfg: RunConfig
    run_id: str
    run_dir: Path
    env: Any
    agent: Agent
    start_time: float
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class RunResult:
    run_id: str
    run_dir: Path
    returns: list[float]
    lengths: list[int]
    episodes_completed: int
    stopped_reason: str  # "completed", "wall_clock" or "callback"


class Callback:
    """Base class for runner plug-ins. Override only the methods you need."""

    def on_run_start(self, ctx: RunContext) -> None: ...

    def on_step(self, ctx: RunContext, transition: Transition) -> None: ...

    def on_episode_end(self, ctx: RunContext, info: EpisodeInfo) -> bool:
        """Return True to stop training early."""
        return False

    def on_run_end(self, ctx: RunContext, result: RunResult) -> None: ...


def make_run_id(cfg: RunConfig) -> str:
    env_short = cfg.env_name.split("-")[0].lower()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{env_short}_{cfg.agent}_s{cfg.seed}_{stamp}"


def build_agent(cfg: RunConfig, env: Any) -> Agent:
    """Create the agent named in the config for this environment."""
    n_actions = int(env.action_space.n)
    if cfg.agent == "random":
        from sla.agent.random_agent import RandomAgent
        return RandomAgent(n_actions, seed=cfg.seed)
    from sla.learning.schedules import LinearSchedule
    schedule = LinearSchedule(cfg.epsilon_start, cfg.epsilon_end, cfg.epsilon_decay_steps)
    if cfg.agent == "q_learning":
        from sla.learning.q_learning import QLearningAgent
        if not hasattr(env.observation_space, "n"):
            raise ValueError("Tabular Q-learning needs a discrete observation space (e.g. FrozenLake)")
        return QLearningAgent(int(env.observation_space.n), n_actions, cfg.learning_rate,
                              cfg.gamma, schedule, seed=cfg.seed)
    if cfg.agent == "dqn":
        from sla.learning.dqn import DQNAgent
        obs_dim = int(np.prod(env.observation_space.shape))
        return DQNAgent(obs_dim, n_actions, cfg.dqn, cfg.gamma, cfg.learning_rate, schedule, seed=cfg.seed)
    raise ValueError(f"Unknown agent {cfg.agent!r}")


def run_training(cfg: RunConfig, callbacks: list[Callback] | None = None, agent: Agent | None = None,
                 run_dir: Path | None = None, run_id: str | None = None,
                 start_episode: int = 0) -> RunResult:
    """Train ``agent`` (or a new one from ``cfg``) for episodes start_episode .. cfg.episodes-1."""
    callbacks = callbacks or []
    set_global_seed(cfg.seed)
    run_id = run_id or make_run_id(cfg)
    run_dir = Path(run_dir) if run_dir else Path(cfg.run_root) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    save_config(cfg, run_dir / "config.yaml")

    env = make_env(cfg.env_name, seed=cfg.seed, **cfg.env_kwargs)
    agent = agent or build_agent(cfg, env)
    limits = SafetyLimits.from_config(cfg)
    ctx = RunContext(cfg, run_id, run_dir, env, agent, time.monotonic())
    for cb in callbacks:
        cb.on_run_start(ctx)

    returns: list[float] = []
    lengths: list[int] = []
    stopped = "completed"
    log.info("Run %s: %s on %s, episodes %d..%d", run_id, cfg.agent, cfg.env_name,
             start_episode, cfg.episodes - 1)

    for episode in range(start_episode, cfg.episodes):
        ep_start = time.monotonic()
        state, _ = env.reset(seed=episode_seed(cfg.seed, episode))
        total, steps, losses = 0.0, 0, []
        terminated = truncated = False
        reward = 0.0
        while not (terminated or truncated):
            action = agent.act(state, explore=True)
            next_state, reward, terminated, truncated, _ = env.step(action)
            reward = check_finite(reward, "reward")
            steps += 1
            if limits.step_limit_reached(steps) and not terminated:
                truncated = True
            transition = Transition(state, int(action), reward, next_state, bool(terminated), bool(truncated))
            for cb in callbacks:
                cb.on_step(ctx, transition)
            stats = agent.update(transition)
            if "loss" in stats:
                losses.append(check_finite(stats["loss"], "loss"))
            total += reward
            state = next_state
        agent.end_episode()
        info = EpisodeInfo(episode, total, steps, agent.epsilon,
                           float(np.mean(losses)) if losses else None,
                           end_reason(cfg.env_name, terminated, truncated, reward, state),
                           time.monotonic() - ep_start)
        returns.append(total)
        lengths.append(steps)
        if (episode + 1) % max(1, cfg.eval_every) == 0:
            log.info(format_episode_summary(episode, returns, window=50, epsilon=agent.epsilon))
        stop_requested = False
        for cb in callbacks:
            if cb.on_episode_end(ctx, info):
                stop_requested = True
        if stop_requested:
            stopped = "callback"
            break
        if limits.wall_clock_exceeded(ctx.start_time):
            stopped = "wall_clock"
            log.warning("Wall-clock limit of %.0f s reached; stopping", limits.max_wall_clock_s)
            break

    env.close()
    result = RunResult(run_id, run_dir, returns, lengths, start_episode + len(returns), stopped)
    for cb in callbacks:
        cb.on_run_end(ctx, result)
    log.info("Run %s finished (%s) after %d episodes", run_id, stopped, result.episodes_completed)
    return result
```

`tests/conftest.py` (Week-4 part; Vedant adds the `store` fixture in Week 5):
```python
@pytest.fixture
def fl_cfg(tmp_path):
    """A small FrozenLake Q-learning config that trains in about a second."""
    return config_from_dict({
        "env_name": "FrozenLake-v1", "env_kwargs": {"is_slippery": False}, "agent": "q_learning",
        "episodes": 300, "seed": 0, "learning_rate": 0.5, "gamma": 0.95, "epsilon_decay_steps": 1500,
        "max_steps_per_episode": 100, "eval_every": 100, "eval_episodes": 5, "checkpoint_every": 100,
        "run_root": str(tmp_path / "runs"),
    })
```

Put this at the top of the file:
```python
"""Shared pytest fixtures."""

import pytest

from sla.utils.config import config_from_dict
```

`tests/unit/test_safety.py`
```python
import math
import time

import pytest

from sla.agent.safety import SafetyLimits, check_finite
from sla.utils.errors import TrainingError


def test_check_finite():
    assert check_finite(1.5, "reward") == 1.5
    with pytest.raises(TrainingError, match="reward"):
        check_finite(math.nan, "reward")


def test_limits():
    limits = SafetyLimits(max_steps_per_episode=50, max_episodes=10, max_wall_clock_s=0.01)
    assert limits.step_limit_reached(50) and not limits.step_limit_reached(49)
    start = time.monotonic()
    time.sleep(0.02)
    assert limits.wall_clock_exceeded(start)
```

`tests/integration/test_runner.py`
```python
import numpy as np

from sla.agent.runner import Callback, run_training


class Recorder(Callback):
    def __init__(self, stop_after=None):
        self.steps, self.episodes, self.stop_after = 0, [], stop_after

    def on_step(self, ctx, transition):
        self.steps += 1

    def on_episode_end(self, ctx, info):
        self.episodes.append(info)
        return self.stop_after is not None and len(self.episodes) >= self.stop_after


def test_q_learning_beats_random_on_frozenlake(fl_cfg, tmp_path):
    learned = run_training(fl_cfg, run_dir=tmp_path / "q")
    fl_cfg.agent = "random"
    random = run_training(fl_cfg, run_dir=tmp_path / "r")
    assert np.mean(learned.returns[-50:]) > np.mean(random.returns[-50:])


def test_callbacks_called_and_can_stop(fl_cfg):
    rec = Recorder(stop_after=5)
    result = run_training(fl_cfg, [rec])
    assert result.stopped_reason == "callback" and result.episodes_completed == 5
    assert rec.steps == sum(result.lengths)
    assert (result.run_dir / "config.yaml").exists()


def test_step_limit_truncates(fl_cfg):
    fl_cfg.max_steps_per_episode = 3
    fl_cfg.episodes = 20
    result = run_training(fl_cfg)
    assert max(result.lengths) <= 3


def test_same_seed_same_returns(fl_cfg, tmp_path):
    a = run_training(fl_cfg, run_dir=tmp_path / "a")
    b = run_training(fl_cfg, run_dir=tmp_path / "b")
    assert a.returns == b.returns
```

### 5.2 Q-learning (Brahmanand)

`src/sla/learning/q_learning.py`
```python
"""Tabular Q-learning (owner: Brahmanand, Week 4).

Q-table: one row per state, one column per action. Each value is the agent's
estimate of the total future reward for taking that action in that state.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from sla.agent.base import Agent, Transition
from sla.learning.schedules import LinearSchedule
from sla.utils.io_helpers import ensure_dir, read_json, write_json


def q_learning_update(q: np.ndarray, s: int, a: int, r: float, s_next: int, terminated: bool,
                      alpha: float, gamma: float) -> float:
    """Apply one Bellman update in place and return the TD error.

    target   = r                          if the episode really ended (terminated)
             = r + gamma * max_a' Q[s', a'] otherwise (including time-limit truncation)
    Q[s, a] += alpha * (target - Q[s, a])
    """
    target = r if terminated else r + gamma * float(np.max(q[s_next]))
    td_error = target - float(q[s, a])
    q[s, a] += alpha * td_error
    return td_error


class QLearningAgent(Agent):
    name = "q_learning"

    def __init__(self, n_states: int, n_actions: int, learning_rate: float = 0.1, gamma: float = 0.99,
                 epsilon_schedule: LinearSchedule | None = None, seed: int = 0) -> None:
        self.n_states = n_states
        self.n_actions = n_actions
        self.alpha = learning_rate
        self.gamma = gamma
        self.schedule = epsilon_schedule or LinearSchedule(1.0, 0.05, 10_000)
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.q = np.zeros((n_states, n_actions), dtype=np.float64)
        self.steps = 0

    @property
    def epsilon(self) -> float:
        return self.schedule.value(self.steps)

    def greedy_action(self, state: int) -> int:
        row = self.q[int(state)]
        best = np.flatnonzero(row == row.max())  # break ties randomly (all zeros at the start)
        return int(self.rng.choice(best))

    def act(self, obs: Any, explore: bool = True) -> int:
        if explore and self.rng.random() < self.epsilon:
            return int(self.rng.integers(self.n_actions))
        return self.greedy_action(int(obs))

    def update(self, transition: Transition) -> dict[str, float]:
        td = q_learning_update(self.q, int(transition.state), transition.action, transition.reward,
                               int(transition.next_state), transition.terminated, self.alpha, self.gamma)
        self.steps += 1
        return {"td_error": td}

    def save(self, path: Path) -> None:
        folder = ensure_dir(path)
        np.save(folder / "q_table.npy", self.q)
        write_json(folder / "meta.json", {
            "agent": self.name, "n_states": self.n_states, "n_actions": self.n_actions,
            "learning_rate": self.alpha, "gamma": self.gamma, "seed": self.seed, "steps": self.steps,
            "schedule": {"start": self.schedule.start, "end": self.schedule.end, "duration": self.schedule.duration},
            "rng_state": self.rng.bit_generator.state,
        })

    @classmethod
    def load(cls, path: Path) -> QLearningAgent:
        folder = Path(path)
        meta = read_json(folder / "meta.json")
        agent = cls(meta["n_states"], meta["n_actions"], meta["learning_rate"], meta["gamma"],
                    LinearSchedule(**meta["schedule"]), meta["seed"])
        agent.q = np.load(folder / "q_table.npy")
        agent.steps = meta["steps"]
        agent.rng.bit_generator.state = meta["rng_state"]
        return agent
```

`tests/unit/test_q_learning.py` — the first test uses the exact numbers from `docs/notes/q_learning_by_hand.md` (Week 1):
```python
import numpy as np
import pytest

from sla.agent.base import Transition
from sla.learning.q_learning import QLearningAgent, q_learning_update
from sla.learning.schedules import LinearSchedule


def test_update_matches_hand_calculation():
    # Worked example from Week 1: alpha=0.5, gamma=0.9, r=0, Q[s'] best = 1.0
    q = np.zeros((2, 2))
    q[1] = [0.0, 1.0]
    td = q_learning_update(q, s=0, a=1, r=0.0, s_next=1, terminated=False, alpha=0.5, gamma=0.9)
    assert td == pytest.approx(0.9)
    assert q[0, 1] == pytest.approx(0.45)


def test_terminal_does_not_bootstrap():
    q = np.zeros((2, 2))
    q[1] = [5.0, 5.0]
    q_learning_update(q, 0, 0, r=1.0, s_next=1, terminated=True, alpha=1.0, gamma=0.9)
    assert q[0, 0] == pytest.approx(1.0)


def test_greedy_picks_best_action():
    agent = QLearningAgent(4, 3, epsilon_schedule=LinearSchedule(0.0, 0.0, 1))
    agent.q[2] = [0.1, 0.9, 0.3]
    assert agent.act(2, explore=False) == 1


def test_update_increments_steps_and_epsilon_decays():
    agent = QLearningAgent(4, 2, epsilon_schedule=LinearSchedule(1.0, 0.0, 10))
    for _ in range(5):
        agent.update(Transition(0, 0, 0.0, 1, False, False))
    assert agent.steps == 5 and agent.epsilon == pytest.approx(0.5)


def test_save_load_same_q_and_actions(tmp_path):
    agent = QLearningAgent(16, 4, seed=3)
    agent.q = np.random.default_rng(0).random((16, 4))
    agent.save(tmp_path / "q")
    clone = QLearningAgent.load(tmp_path / "q")
    assert np.array_equal(agent.q, clone.q)
    assert [agent.act(s, explore=False) for s in range(16)] == [clone.act(s, explore=False) for s in range(16)]
```

`scripts/quick_frozenlake_check.py` — a temporary check until the proper evaluator exists (Week 6):
```python
"""Week-4 check (Brahmanand): does tabular Q-learning solve FrozenLake 4x4 for 5 seeds?

Run from the repo root:  python scripts/quick_frozenlake_check.py
(Proper evaluation code arrives in Week 6; this is a quick greedy check.)
"""

from sla.agent.runner import build_agent, run_training
from sla.envs.factory import make_env
from sla.utils.config import load_config
from sla.utils.logging_setup import setup_logging

setup_logging(level="WARNING")
for seed in range(5):
    cfg = load_config("configs/frozenlake_q.yaml")
    cfg.seed = seed
    env = make_env(cfg.env_name, **cfg.env_kwargs)
    agent = build_agent(cfg, env)
    result = run_training(cfg, agent=agent)          # the agent object keeps what it learned

    state, _ = env.reset(seed=123)                   # one greedy episode: explore=False, no update()
    total, done = 0.0, False
    while not done:
        state, reward, terminated, truncated, _ = env.step(agent.act(state, explore=False))
        total += reward
        done = terminated or truncated
    last100 = sum(result.returns[-100:]) / 100
    print(f"seed {seed}: training success (last 100 episodes) {last100:.2f} | greedy episode reward {total}")
```

### 5.3 Schedules, network, DQN (Atharv)

`src/sla/learning/schedules.py`
```python
"""Exploration schedules (owner: Atharv, Week 4)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LinearSchedule:
    """Goes from ``start`` to ``end`` in a straight line over ``duration`` steps, then stays at ``end``."""

    start: float
    end: float
    duration: int

    def __post_init__(self) -> None:
        if self.duration <= 0:
            raise ValueError("duration must be > 0")

    def value(self, step: int) -> float:
        fraction = min(max(step, 0) / self.duration, 1.0)
        return self.start + fraction * (self.end - self.start)
```

`tests/unit/test_schedules.py`
```python
import numpy as np
import pytest

from sla.learning.schedules import LinearSchedule


def test_linear_schedule():
    s = LinearSchedule(1.0, 0.1, 100)
    assert s.value(0) == 1.0
    assert np.isclose(s.value(50), 0.55)
    assert np.isclose(s.value(100), 0.1) and np.isclose(s.value(10_000), 0.1)


def test_negative_step_treated_as_zero():
    assert LinearSchedule(1.0, 0.0, 10).value(-5) == 1.0


def test_duration_must_be_positive():
    with pytest.raises(ValueError):
        LinearSchedule(1.0, 0.0, 0)
```

`src/sla/learning/networks.py`
```python
"""Neural network that estimates Q-values (owner: Atharv, Week 4)."""

from __future__ import annotations

import torch
from torch import nn


class QNetwork(nn.Module):
    """Small MLP: state (obs_dim numbers) -> one Q-value per action.

    For CartPole: 4 -> 128 -> 128 -> 2.
    """

    def __init__(self, obs_dim: int, n_actions: int, hidden_size: int = 128) -> None:
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(obs_dim, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, n_actions),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.layers(x)
```

`src/sla/learning/dqn.py` — read `update()` carefully: replay on → train on a random mini-batch; replay off (ablation) → train only on the newest transition; target network off (ablation) → bootstrap from the online network.
```python
"""Deep Q-Network agent (owner: Atharv, Week 4–6).

Key ideas (Mnih et al., 2015):
  * a neural network replaces the Q-table,
  * experience replay: learn from random mini-batches of past transitions,
  * a target network, copied every C steps, gives stable learning targets.
"""

from __future__ import annotations

import copy
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn.functional as F

from sla.agent.base import Agent, Transition
from sla.learning.networks import QNetwork
from sla.learning.schedules import LinearSchedule
from sla.memory.replay_buffer import Batch, ReplayBuffer
from sla.utils.config import DQNConfig
from sla.utils.io_helpers import ensure_dir, read_json, write_json


def compute_td_target(rewards, next_q_max, terminated, gamma: float):
    """y = r + gamma * (1 - terminated) * max_a' Q_target(s', a').

    Works with NumPy arrays and PyTorch tensors. Only *terminated* stops
    bootstrapping; a time-limit truncation still uses the next state's value.
    """
    return rewards + gamma * (1.0 - terminated) * next_q_max


class DQNAgent(Agent):
    name = "dqn"

    def __init__(self, obs_dim: int, n_actions: int, cfg: DQNConfig | None = None, gamma: float = 0.99,
                 learning_rate: float = 1e-3, epsilon_schedule: LinearSchedule | None = None,
                 seed: int = 0) -> None:
        self.obs_dim = obs_dim
        self.n_actions = n_actions
        self.cfg = cfg or DQNConfig()
        self.gamma = gamma
        self.learning_rate = learning_rate
        self.schedule = epsilon_schedule or LinearSchedule(1.0, 0.05, 10_000)
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        torch.manual_seed(seed)

        self.online = QNetwork(obs_dim, n_actions, self.cfg.hidden_size)
        self.target = copy.deepcopy(self.online)
        self.target.eval()
        self.optimizer = torch.optim.Adam(self.online.parameters(), lr=learning_rate)
        capacity = self.cfg.buffer_size if self.cfg.replay_enabled else 1
        self.buffer = ReplayBuffer(capacity, obs_dim, seed)

        self.steps = 0          # environment steps seen
        self.updates = 0        # gradient steps taken
        self.last_loss: float | None = None
        self.last_max_q: float | None = None

    # ----- acting ---------------------------------------------------------
    @property
    def epsilon(self) -> float:
        return self.schedule.value(self.steps)

    def q_values(self, obs: Any) -> np.ndarray:
        with torch.no_grad():
            x = torch.as_tensor(np.asarray(obs, dtype=np.float32).reshape(1, -1))
            return self.online(x).squeeze(0).numpy()

    def act(self, obs: Any, explore: bool = True) -> int:
        if explore and self.rng.random() < self.epsilon:
            return int(self.rng.integers(self.n_actions))
        return int(np.argmax(self.q_values(obs)))

    # ----- learning -------------------------------------------------------
    def update(self, transition: Transition) -> dict[str, float]:
        self.buffer.push(transition.state, transition.action, transition.reward,
                         transition.next_state, transition.terminated)
        self.steps += 1
        stats: dict[str, float] = {}
        if self.steps >= self.cfg.learning_starts and self.steps % self.cfg.train_freq == 0:
            if self.cfg.replay_enabled:
                if len(self.buffer) >= self.cfg.batch_size:
                    stats["loss"] = self.train_step(self.buffer.sample(self.cfg.batch_size))
            else:
                stats["loss"] = self.train_step(self.buffer.latest())
        if self.cfg.target_net_enabled and self.steps % self.cfg.target_update_every == 0:
            self.sync_target()
        return stats

    def train_step(self, batch: Batch) -> float:
        states = torch.as_tensor(batch.states)
        actions = torch.as_tensor(batch.actions).long()
        rewards = torch.as_tensor(batch.rewards)
        next_states = torch.as_tensor(batch.next_states)
        terminated = torch.as_tensor(batch.terminated)

        q = self.online(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        with torch.no_grad():
            bootstrap_net = self.target if self.cfg.target_net_enabled else self.online
            next_q_max = bootstrap_net(next_states).max(dim=1).values
            target = compute_td_target(rewards, next_q_max, terminated, self.gamma)
        loss = F.smooth_l1_loss(q, target)  # Huber loss

        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.online.parameters(), self.cfg.grad_clip)
        self.optimizer.step()

        self.updates += 1
        self.last_loss = float(loss.item())
        self.last_max_q = float(q.detach().abs().max().item())
        return self.last_loss

    def sync_target(self) -> None:
        self.target.load_state_dict(self.online.state_dict())

    # ----- saving ---------------------------------------------------------
    def save(self, path: Path, include_buffer: bool = True) -> None:
        folder = ensure_dir(path)
        torch.save({"online": self.online.state_dict(), "target": self.target.state_dict(),
                    "optimizer": self.optimizer.state_dict()}, folder / "dqn.pt")
        write_json(folder / "meta.json", {
            "agent": self.name, "obs_dim": self.obs_dim, "n_actions": self.n_actions,
            "cfg": asdict(self.cfg), "gamma": self.gamma, "learning_rate": self.learning_rate,
            "schedule": {"start": self.schedule.start, "end": self.schedule.end, "duration": self.schedule.duration},
            "seed": self.seed, "steps": self.steps, "updates": self.updates,
            "rng_state": self.rng.bit_generator.state,
            "buffer_rng_state": self.buffer.rng.bit_generator.state,
        })
        if include_buffer and len(self.buffer) > 0:
            self.buffer.save(folder / "replay.npz")

    @classmethod
    def load(cls, path: Path) -> DQNAgent:
        folder = Path(path)
        meta = read_json(folder / "meta.json")
        agent = cls(meta["obs_dim"], meta["n_actions"], DQNConfig(**meta["cfg"]), meta["gamma"],
                    meta["learning_rate"], LinearSchedule(**meta["schedule"]), meta["seed"])
        state = torch.load(folder / "dqn.pt", map_location="cpu", weights_only=True)
        agent.online.load_state_dict(state["online"])
        agent.target.load_state_dict(state["target"])
        agent.optimizer.load_state_dict(state["optimizer"])
        agent.steps, agent.updates = meta["steps"], meta["updates"]
        agent.rng.bit_generator.state = meta["rng_state"]
        agent.buffer.rng.bit_generator.state = meta["buffer_rng_state"]
        if (folder / "replay.npz").exists():
            agent.buffer.load_from(folder / "replay.npz")
        return agent
```

`tests/unit/test_dqn.py` — `pytest.importorskip("torch")` skips these tests (instead of failing) on a laptop without PyTorch; CI always has PyTorch, so they always run there.
```python
import numpy as np
import pytest

torch = pytest.importorskip("torch")

from sla.agent.base import Transition  # noqa: E402
from sla.learning.dqn import DQNAgent, compute_td_target  # noqa: E402
from sla.learning.networks import QNetwork  # noqa: E402
from sla.memory.replay_buffer import Batch  # noqa: E402
from sla.utils.config import DQNConfig  # noqa: E402

pytestmark = pytest.mark.torch


def test_td_target_hand_calculation():
    r = np.array([1.0, 1.0])
    next_max = np.array([10.0, 10.0])
    term = np.array([0.0, 1.0])  # second transition really ended
    assert np.allclose(compute_td_target(r, next_max, term, 0.9), [10.0, 1.0])


def test_network_output_shape():
    net = QNetwork(4, 2, 16)
    assert net(torch.zeros(5, 4)).shape == (5, 2)


def make_batch(n=32):
    rng = np.random.default_rng(0)
    return Batch(rng.normal(size=(n, 4)).astype(np.float32), rng.integers(0, 2, n).astype(np.int64),
                 np.ones(n, dtype=np.float32), rng.normal(size=(n, 4)).astype(np.float32),
                 np.zeros(n, dtype=np.float32))


def test_loss_decreases_on_fixed_batch():
    agent = DQNAgent(4, 2, DQNConfig(hidden_size=32, target_net_enabled=False), learning_rate=1e-2, seed=0)
    batch = make_batch()
    first = agent.train_step(batch)
    for _ in range(100):
        last = agent.train_step(batch)
    assert last < first


def test_target_net_frozen_between_syncs():
    cfg = DQNConfig(hidden_size=16, batch_size=8, learning_starts=8, target_update_every=500)
    agent = DQNAgent(4, 2, cfg, seed=0)
    before = [p.clone() for p in agent.target.parameters()]
    for i in range(499):
        agent.update(Transition(np.zeros(4), i % 2, 1.0, np.ones(4), False, False))
    assert all(torch.equal(a, b) for a, b in zip(before, agent.target.parameters()))
    agent.update(Transition(np.zeros(4), 0, 1.0, np.ones(4), False, False))  # step 500 -> sync
    assert all(torch.equal(a, b) for a, b in zip(agent.online.parameters(), agent.target.parameters()))


def test_save_load_same_greedy_actions(tmp_path):
    agent = DQNAgent(4, 2, DQNConfig(hidden_size=16), seed=0)
    agent.train_step(make_batch())
    agent.save(tmp_path / "d")
    clone = DQNAgent.load(tmp_path / "d")
    states = np.random.default_rng(1).normal(size=(100, 4))
    assert [agent.act(s, explore=False) for s in states] == [clone.act(s, explore=False) for s in states]
```

### 5.4 `docs/notes/dqn_explained.md` outline (Atharv)

```markdown
# DQN explained (team notes)
1. Problem: CartPole state = 4 real numbers -> a Q-table cannot list them all.
2. Idea: a small network Q_theta(s) outputs one Q-value per action (2 numbers for CartPole).
3. Acting: epsilon-greedy over Q_theta(s).
4. Learning from one mini-batch (64 transitions sampled from the replay buffer):
   target y = r + gamma * (1 - terminated) * max_a' Q_target(s', a')
   loss     = Huber(Q_theta(s, a), y)           -> gradient step, clip gradient norm at 10
5. Every 500 steps: Q_target <- Q_theta (copy weights).
6. Worked example: r = 1, gamma = 0.99, terminated = 0, max Q_target(s') = 20.0  ->  y = 1 + 0.99 * 20 = 20.8
                   r = 1, terminated = 1                                          ->  y = 1
7. Why replay? consecutive steps are almost identical; random batches break this correlation (Lin, 1992).
8. Why a target network? the target would otherwise move every step we learn (Mnih et al., 2015).
Quiz: (a) y for r=1, gamma=0.9, terminated=0, max=10?  (b) why does truncation still bootstrap?  (c) what happens if replay is off?
```

### 5.5 Replay buffer (Vedant)

`src/sla/memory/replay_buffer.py`
```python
"""Experience replay buffer (owner: Vedant, Week 4).

A fixed-size circular memory of transitions. When it is full, the oldest
transition is overwritten. ``sample`` returns a random mini-batch so the DQN
learns from a mix of old and new experience (Lin, 1992; Mnih et al., 2015).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, NamedTuple

import numpy as np


class Batch(NamedTuple):
    states: np.ndarray       # shape (B, obs_dim), float32
    actions: np.ndarray      # shape (B,), int64
    rewards: np.ndarray      # shape (B,), float32
    next_states: np.ndarray  # shape (B, obs_dim), float32
    terminated: np.ndarray   # shape (B,), float32 (1.0 = episode really ended)


class ReplayBuffer:
    def __init__(self, capacity: int, obs_dim: int, seed: int = 0) -> None:
        if capacity <= 0 or obs_dim <= 0:
            raise ValueError("capacity and obs_dim must be > 0")
        self.capacity = capacity
        self.obs_dim = obs_dim
        self.rng = np.random.default_rng(seed)
        self.states = np.zeros((capacity, obs_dim), dtype=np.float32)
        self.actions = np.zeros(capacity, dtype=np.int64)
        self.rewards = np.zeros(capacity, dtype=np.float32)
        self.next_states = np.zeros((capacity, obs_dim), dtype=np.float32)
        self.terminated = np.zeros(capacity, dtype=np.float32)
        self.pos = 0   # where the next transition will be written
        self.size = 0  # how many slots are filled

    def __len__(self) -> int:
        return self.size

    def push(self, state: Any, action: int, reward: float, next_state: Any, terminated: bool) -> None:
        i = self.pos
        self.states[i] = np.asarray(state, dtype=np.float32).reshape(self.obs_dim)
        self.actions[i] = int(action)
        self.rewards[i] = float(reward)
        self.next_states[i] = np.asarray(next_state, dtype=np.float32).reshape(self.obs_dim)
        self.terminated[i] = 1.0 if terminated else 0.0
        self.pos = (self.pos + 1) % self.capacity
        self.size = min(self.size + 1, self.capacity)

    def sample(self, batch_size: int) -> Batch:
        if self.size == 0:
            raise ValueError("Cannot sample from an empty buffer")
        if batch_size > self.size:
            raise ValueError(f"batch_size {batch_size} is larger than buffer size {self.size}")
        idx = self.rng.choice(self.size, size=batch_size, replace=False)
        return Batch(self.states[idx], self.actions[idx], self.rewards[idx],
                     self.next_states[idx], self.terminated[idx])

    def latest(self) -> Batch:
        """The most recent transition as a batch of one (used by the no-replay ablation)."""
        if self.size == 0:
            raise ValueError("Buffer is empty")
        i = (self.pos - 1) % self.capacity
        idx = np.array([i])
        return Batch(self.states[idx], self.actions[idx], self.rewards[idx],
                     self.next_states[idx], self.terminated[idx])

    def save(self, path: str | Path) -> None:
        np.savez_compressed(path, states=self.states[: self.size], actions=self.actions[: self.size],
                            rewards=self.rewards[: self.size], next_states=self.next_states[: self.size],
                            terminated=self.terminated[: self.size],
                            meta=np.array([self.capacity, self.obs_dim, self.pos, self.size]))

    def load_from(self, path: str | Path) -> None:
        data = np.load(path)
        capacity, obs_dim, pos, size = (int(v) for v in data["meta"])
        if capacity != self.capacity or obs_dim != self.obs_dim:
            raise ValueError("Saved buffer has a different capacity or obs_dim")
        self.states[:size] = data["states"]
        self.actions[:size] = data["actions"]
        self.rewards[:size] = data["rewards"]
        self.next_states[:size] = data["next_states"]
        self.terminated[:size] = data["terminated"]
        self.pos, self.size = pos, size
```

`tests/unit/test_replay_buffer.py`
```python
import numpy as np
import pytest

from sla.memory.replay_buffer import ReplayBuffer


def fill(buf, n):
    for i in range(n):
        buf.push([i, i, i, i], i % 2, float(i), [i + 1] * 4, i % 5 == 0)


def test_wraps_around_after_capacity():
    buf = ReplayBuffer(10, 4)
    fill(buf, 15)
    assert len(buf) == 10
    assert set(buf.rewards.tolist()) == set(float(i) for i in range(5, 15))


def test_sample_shapes_and_dtypes():
    buf = ReplayBuffer(100, 4, seed=0)
    fill(buf, 50)
    b = buf.sample(32)
    assert b.states.shape == (32, 4) and b.states.dtype == np.float32
    assert b.actions.shape == (32,) and b.actions.dtype == np.int64
    assert b.terminated.dtype == np.float32


def test_seeded_sampling_repeats():
    a, b = ReplayBuffer(100, 4, seed=1), ReplayBuffer(100, 4, seed=1)
    fill(a, 60)
    fill(b, 60)
    assert np.array_equal(a.sample(16).rewards, b.sample(16).rewards)


def test_sample_errors():
    buf = ReplayBuffer(10, 4)
    with pytest.raises(ValueError):
        buf.sample(1)
    fill(buf, 3)
    with pytest.raises(ValueError):
        buf.sample(4)


def test_latest_is_newest():
    buf = ReplayBuffer(5, 4)
    fill(buf, 7)
    assert buf.latest().rewards[0] == 6.0


def test_save_and_load(tmp_path):
    buf = ReplayBuffer(20, 4, seed=0)
    fill(buf, 12)
    buf.save(tmp_path / "r.npz")
    other = ReplayBuffer(20, 4)
    other.load_from(tmp_path / "r.npz")
    assert len(other) == 12 and np.array_equal(other.states[:12], buf.states[:12])
```

### 5.6 Validation and summary (Somesh)

**Lesson (read before coding):**
```python
# isinstance checks a value's type. Careful: bool is a subclass of int!
isinstance(5, int)       # True
isinstance(True, int)    # True  <- surprise! so check bool first:
isinstance(True, bool)   # True

# List comprehension: build a list in one line
squares = [x * x for x in range(5)]          # [0, 1, 4, 9, 16]
positives = [x for x in [-1, 2, 3] if x > 0]  # [2, 3]

# Default argument: used when the caller leaves it out
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}"
greet("Somesh")             # 'Hello, Somesh'

# re.sub replaces every match of a pattern
import re
re.sub(r"[^A-Za-z0-9_-]+", "_", "My run #1")  # 'My_run_1'  ([^...] means "NOT these characters")
```
Mini-exercises: (a) comprehension keeping only even numbers from `range(10)`; (b) function `clamp(x, low=0, high=1)`; (c) use `re.sub` to replace spaces with `-`.

`src/sla/utils/validation.py` — **Week-4 version** (the file header and imports you need now; Week 6 adds a second part to the same file):

```python
"""Input and transition validation (owner: Somesh).

Week 4: run-request helpers (seeds, env names, episode counts, safe names).
Week 6: transition validation used during training.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any

from sla.utils.config import ALLOWED_ENVS
from sla.utils.errors import ValidationError

# region W4: run-request validation
```
```python
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
```
```python
# endregion
```

**Line by line (validation):** `MAX_EPISODES = 100_000` — underscores make big numbers readable · `_SAFE_NAME = re.compile(...)` — a pre-compiled pattern of *unsafe* characters (the leading `_` means "private to this file") · `validate_seeds` loops, rejects bools/non-ints/negatives, skips duplicates with `if seed not in result`, and fails if the list ends empty · `validate_episode_count` uses a chained comparison `1 <= episodes <= MAX_EPISODES` · `safe_run_name` replaces unsafe runs of characters with `_`, strips leading/trailing `_`, and cuts to `max_length` — this stops names like `../../` from escaping the `runs/` folder.

`tests/unit/test_validation.py` — Week-4 version:
```python
import pytest

from sla.utils.errors import ValidationError
from sla.utils.validation import safe_run_name, validate_env_name, validate_episode_count, validate_seeds

# region W4: run-request validation
```
```python
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
```
```python
# endregion
```

`src/sla/utils/summary.py`
```python
"""Readable training summaries (owner: Somesh, Week 4)."""

from __future__ import annotations

from collections.abc import Sequence


def rolling_mean(values: Sequence[float], window: int) -> list[float]:
    """Mean of the last ``window`` values at each position (shorter at the start)."""
    if window <= 0:
        raise ValueError("window must be > 0")
    out: list[float] = []
    total = 0.0
    for i, v in enumerate(values):
        total += float(v)
        if i >= window:
            total -= float(values[i - window])
        out.append(total / min(i + 1, window))
    return out


def format_episode_summary(episode: int, returns: Sequence[float], window: int = 50,
                           epsilon: float | None = None) -> str:
    """One line such as: 'Episode   100 | return   23.0 | mean(50)   18.4 | eps 0.62'."""
    if not returns:
        raise ValueError("returns must not be empty")
    mean = rolling_mean(returns, window)[-1]
    line = f"Episode {episode:>5} | return {returns[-1]:>7.1f} | mean({window}) {mean:>7.2f}"
    if epsilon is not None:
        line += f" | eps {epsilon:.2f}"
    return line
```

**Line by line (summary):** `rolling_mean` keeps a running `total`; once more than `window` values are seen it subtracts the value leaving the window — so it is fast even for 10,000 episodes · `min(i + 1, window)` divides by the true count at the start · `format_episode_summary` uses format specs: `{episode:>5}` right-aligns in 5 characters, `{x:>7.2f}` shows 2 decimals in 7 characters.

`tests/unit/test_summary.py`
```python
import pytest

from sla.utils.summary import format_episode_summary, rolling_mean


def test_rolling_mean():
    assert rolling_mean([1, 2, 3, 4], 2) == [1.0, 1.5, 2.5, 3.5]


def test_rolling_mean_bad_window():
    with pytest.raises(ValueError):
        rolling_mean([1], 0)


def test_summary_line():
    line = format_episode_summary(9, [1.0] * 10, window=5, epsilon=0.5)
    assert "Episode     9" in line and "eps 0.50" in line and "1.00" in line
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
│   │   ├── dqn_explained.md   [NEW · Atharv]
│   │   └── q_learning_by_hand.md
│   ├── architecture.md
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
│   └── quick_frozenlake_check.py   [NEW · Brahmanand]
├── spikes/
│   └── llm_benchmark.py
├── src/
│   └── sla/
│       ├── agent/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── random_agent.py
│       │   ├── runner.py   [NEW · Brahmanand]
│       │   └── safety.py   [NEW · Brahmanand]
│       ├── envs/
│       │   ├── __init__.py
│       │   └── factory.py
│       ├── evaluation/
│       │   └── __init__.py
│       ├── learning/
│       │   ├── __init__.py
│       │   ├── dqn.py   [NEW · Atharv]
│       │   ├── networks.py   [NEW · Atharv]
│       │   ├── q_learning.py   [NEW · Brahmanand]
│       │   └── schedules.py   [NEW · Atharv]
│       ├── memory/
│       │   ├── __init__.py
│       │   └── replay_buffer.py   [NEW · Vedant]
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
│       │   ├── summary.py   [NEW · Somesh]
│       │   └── validation.py   [NEW · Somesh]
│       ├── __init__.py
│       └── cli.py
├── tests/
│   ├── integration/
│   │   └── test_runner.py   [NEW · Brahmanand]
│   ├── unit/
│   │   ├── test_agents.py
│   │   ├── test_cli_help.py
│   │   ├── test_config.py
│   │   ├── test_dqn.py   [NEW · Atharv]
│   │   ├── test_envs.py
│   │   ├── test_io_helpers.py
│   │   ├── test_logging.py
│   │   ├── test_q_learning.py   [NEW · Brahmanand]
│   │   ├── test_replay_buffer.py   [NEW · Vedant]
│   │   ├── test_safety.py   [NEW · Brahmanand]
│   │   ├── test_schedules.py   [NEW · Atharv]
│   │   ├── test_summary.py   [NEW · Somesh]
│   │   └── test_validation.py   [NEW · Somesh]
│   └── conftest.py   [NEW · Brahmanand → Vedant]
├── .env.example
├── .gitignore
├── CONTRIBUTING.md
├── pyproject.toml
└── README.md
```

Legend: [NEW] created this week · [MODIFIED] changed this week · no tag = carried over unchanged from an earlier week. `runs/` (training outputs) and `.venv/` exist on your laptop but are git-ignored, so they are not shown.

---

## SECTION 7 — GITHUB COLLABORATION PROCEDURE

Use the 13-step flow (issue → assign → branch → pull → implement → test → stage → commit → push → PR → review → fix → merge). Week-4 issues:

| # | Title | Owner | Branch | Reviewer | Merge by |
|---|---|---|---|---|---|
| 41 | Safety limits | Brahmanand | `feat/brahmanand-41-safety-limits` | Atharv | Day 2 |
| 42 | Training loop with callbacks | Brahmanand | `feat/brahmanand-42-agent-runner` | Atharv | Day 5 |
| 43 | Tabular Q-learning | Brahmanand | `feat/brahmanand-43-q-learning` | Atharv | Day 4 |
| 45 | Epsilon schedule | Atharv | `feat/atharv-45-schedules` | Brahmanand | **Day 2** |
| 46 | DQN agent | Atharv | `feat/atharv-46-dqn` | Vedant | Day 6 |
| 47 | Replay buffer | Vedant | `feat/vedant-47-replay-buffer` | Atharv | **Day 3** |
| 48 | Validation + summary | Somesh | `feat/somesh-48-validation-summary` | Vedant | **Day 3** |
| 49 | DQN notes | Atharv | `docs/atharv-49-dqn-notes` | Brahmanand | Day 6 |

**Working on a branch that depends on an unmerged PR** (e.g. Atharv's DQN needs Vedant's buffer on Day 3): wait for the merge, then update your branch:
```bash
git checkout feat/atharv-46-dqn
git fetch origin
git rebase origin/main          # replay your commits on top of the newest main
# if conflicts: fix files, then  git add <file>  and  git rebase --continue
git push --force-with-lease     # safe force-push of your own branch only
```
Never force-push `main` (it is protected).

---

## SECTION 8 — WEEKLY INTEGRATION PROCEDURE

| Item | This week |
|---|---|
| Modules to connect | runner ↔ `Agent` implementations (random, Q-learning, DQN); Q-learning ↔ `LinearSchedule`; DQN ↔ `ReplayBuffer` + `DQNConfig`; runner ↔ `summary.format_episode_summary`, `envs.end_reason`, `seeding.episode_seed`. |
| Integrator | **Brahmanand** (integration captain, Week 4). |
| Interfaces that must match | `Agent.update(transition) -> dict` (DQN returns `{"loss": x}` when it trains); `ReplayBuffer.push(s, a, r, s2, terminated)`; `LinearSchedule(start, end, duration).value(step)`; `build_agent(cfg, env)` names: `"random"`, `"q_learning"`, `"dqn"`. |
| Tests that must pass | `pytest` (all), especially `test_runner.py`, `test_dqn.py`, `test_replay_buffer.py`. |
| Detect failures | `TypeError: update() takes 2 positional arguments` (interface mismatch); `ImportError` on `sla.learning.schedules` (merge order); CI red after merging two PRs that each passed alone. |
| Debug | Run the failing test alone with `pytest path::test_name -x -vv`; add `print(type(state), state)` temporarily in the runner loop; compare with `docs/design.md`. |

**Integration checklist**
- [ ] `build_agent` creates all three agents (DQN only on CartPole)
- [ ] Runner works with random + Q-learning; `quick_frozenlake_check.py` prints 5 seeds
- [ ] DQN unit tests pass in CI with the merged buffer
- [ ] No module outside `agent/runner.py` changed the loop
- [ ] CI green on `main` after the last merge

---

## SECTION 9 — TESTING AND VALIDATION

| Type | Tests this week | Command |
|---|---|---|
| Unit | `test_safety`, `test_q_learning`, `test_schedules`, `test_dqn`, `test_replay_buffer`, `test_validation` (W4), `test_summary` | `pytest tests/unit -v` |
| Integration | `test_runner.py` (callbacks, step limit, reproducibility, learns vs random) | `pytest tests/integration -v` |
| Input validation | Somesh's validators (bad seeds, env names, episode counts, unsafe names) | `pytest tests/unit/test_validation.py` |
| Error handling | `check_finite` raises `TrainingError` on NaN reward/loss | `pytest tests/unit/test_safety.py` |
| Reproducibility | `test_same_seed_same_returns` — two runs, identical returns | in `test_runner.py` |
| Performance | not measured yet (Week 8) | — |

**RL rules applied this week:** the quick check separates training (`run_training`, ε-greedy, updates) from a greedy episode (`explore=False`, no `update()`); results from the check are *observations*, not final results — the proper evaluator with fixed test seeds arrives in Week 6. Record whatever numbers you actually see.

---

## SECTION 10 — COMMON PROBLEMS AND SOLUTIONS

| Problem | Possible Cause | How to Check | Solution |
|---|---|---|---|
| `ValueError: not enough values to unpack (expected 5, got 4)` | Old Gym API (4-value `step`) | `pip show gymnasium` | Use `gymnasium>=1.0` (pyproject pins it); never `import gym` |
| Q-learning stuck at reward 0 | Ties always choose action 0; ε decays too fast | print `agent.q` after training | Random tie-break (`greedy_action`); larger `epsilon_decay_steps` |
| `ModuleNotFoundError: sla.learning.schedules` | Atharv's PR not merged yet | `git log origin/main --oneline` | Wait for merge; `git rebase origin/main` |
| DQN loss becomes `nan` | lr too high / no clipping | print `agent.last_loss` | Keep `grad_clip: 10`, lr 5e-4 |
| `RuntimeError` in `gather` | actions not int64 or wrong shape | `batch.actions.dtype` | `torch.as_tensor(actions).long().unsqueeze(1)` |
| Tests pass alone but fail together | shared state / files | run `pytest -p no:randomly` | Use `tmp_path`; never write into the repo in tests |
| Runner never stops (CartPole) | step limit ignored | print `steps` | `limits.step_limit_reached(steps)` sets `truncated=True` |
| `torch` import is slow (5–10 s) | normal on first import | — | Fine; FrozenLake does not import torch (lazy import) |
| Merge conflict in `tests/conftest.py` | two people added fixtures | conflict banner | Keep both fixtures; one owner per region |

---

## SECTION 11 — WEEKLY DELIVERABLES

| Deliverable | Owner | File/Location | Verification | Status |
|---|---|---|---|---|
| Safety limits | Brahmanand | `src/sla/agent/safety.py` | `test_safety.py` passes | [ ] |
| Training loop + callbacks | Brahmanand | `src/sla/agent/runner.py`, `tests/conftest.py` | `test_runner.py` passes | [ ] |
| Tabular Q-learning | Brahmanand | `src/sla/learning/q_learning.py` | hand-calc test; quick check recorded | [ ] |
| FrozenLake quick check | Brahmanand | `scripts/quick_frozenlake_check.py` | output pasted in PR | [ ] |
| Epsilon schedule | Atharv | `src/sla/learning/schedules.py` | `test_schedules.py` | [ ] |
| Q-network + DQN | Atharv | `src/sla/learning/networks.py`, `dqn.py` | `test_dqn.py` in CI | [ ] |
| DQN notes + session | Atharv | `docs/notes/dqn_explained.md` | quiz answered | [ ] |
| Replay buffer | Vedant | `src/sla/memory/replay_buffer.py` | ≥ 90 % coverage | [ ] |
| Validation + summary | Somesh | `src/sla/utils/validation.py`, `summary.py` | tests pass; runner uses summary | [ ] |

---

## SECTION 12 — WEEKLY REVIEW MEETING

**Agenda:** demo (`git pull && pytest && python scripts/quick_frozenlake_check.py` on the projector) · completed/pending tasks · blockers · code quality (ruff, readability) · test results · PRs open/merged · integration status · Week-5 dependencies.

**Questions:**
1. Brahmanand: walk through one episode in `run_training` line by line.
2. Why does the runner call `env.reset(seed=episode_seed(...))` every episode, and what does that give us next week?
3. What happens to the Q-update when an episode is *terminated* vs *truncated*?
4. Atharv: compute a TD target for r = 1, γ = 0.99, terminated = 0, max Q = 20.
5. Vedant: what happens when the buffer is full, and why sample without replacement?
6. Somesh: why must the seed validator check `bool` before `int`? Show the test that proves it.
7. Did Q-learning reach the goal for all 5 seeds? What happened on slippery FrozenLake?
8. Which callback will each member add next week, and which runner object does it use?

---

## SECTION 13 — WEEK COMPLETION CHECKLIST

- [ ] All assigned tasks completed
- [ ] Code pushed to feature branches
- [ ] Pull requests reviewed and merged in dependency order (#45, #47, #48 first)
- [ ] All tests pass locally and in CI
- [ ] Runner integrated with all three agent types
- [ ] `docs/notes/dqn_explained.md` merged; README "Run" section mentions `quick_frozenlake_check.py`
- [ ] Weekly demonstration completed
- [ ] Blockers recorded

---

## SECTION 14 — NEXT WEEK HANDOFF

- **Ready before Week 5:** merged `runner.py` (with the `Callback` class), `q_learning.py`, `dqn.py` (with `save/load`), `replay_buffer.py` (with `save/load_from`), `summary.py`, `validation.py` (W4 part).
- **Files Week 5 depends on:** `agent/runner.py` (`Callback`, `EpisodeInfo`, `RunContext`), every agent's `save/load` (checkpoints), `EpisodeInfo` field names (SQLite store), `rolling_mean` (plots).
- **Coordination:** Brahmanand (checkpoints) and Vedant (store) both write callbacks — agree the order on Week-5 Day 1: `StoreCallback` first, then `CheckpointCallback`. Atharv needs Brahmanand's `sla train` (Week-5 Day 4) for his CartPole pilot runs.
- **Risks:** DQN untested on real training (Week 5 pilot); slippery FrozenLake much harder (documented, not a blocker); runner bugs found later would affect everyone — report them to Brahmanand immediately, never patch the runner in your own PR.
