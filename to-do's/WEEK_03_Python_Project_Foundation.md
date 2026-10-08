# WEEK 03 — Python Project Foundation

**Project:** Self-Learning AI Agent · **Team:** Brahmanand Mathpati, Atharv Gundale, Vedant Biradar, Somesh Badwane
**Source:** *Self_Learning_AI_Agent_10_Week_Master_Plan* (v1.0) · **Interfaces:** `docs/design.md` (frozen, tag `w2-design-freeze`)

---

## SECTION 1 — WEEK OVERVIEW

| Item | Details |
|---|---|
| Week number | 3 of 10 |
| Week title | Python Project Foundation |
| Main objective | Turn the design into a real, installable Python package that **every member can install, run and test**, with CI checking every pull request. |
| Expected outcome | `pip install -e ".[dev]"` and `pytest` work on all four laptops; GitHub Actions runs ruff + pytest on every PR; seeded environments; a random agent plays CartPole; YAML configs load and are validated; shared logging and error classes; a `sla` command exists (skeleton). |
| Required knowledge | Week-2 Python (files, JSON, exceptions, pytest). New: packages and `pyproject.toml`, editable installs, Gymnasium `reset()`/`step()`, random seeds, logging, dataclasses, YAML, abstract base classes, argparse. |
| Required tools | Python 3.10–3.12 venv, VS Code, Git; packages from `pyproject.toml`; PyTorch CPU (installed now so Week 4 is not blocked). |
| Prerequisites from previous weeks | Frozen `docs/design.md`; `src/sla/utils/io_helpers.py` merged; `docs/tech_stack.md` versions. |
| Approximate workload | 11 h per member. |
| Technical dependencies | Atharv's `pyproject.toml` + skeleton (Day 2) → everyone installs. Vedant's `errors.py` (Day 3) → Somesh's `config.py` and Brahmanand's `factory.py` import it. |
| Definition of Done | CI green on `main`; branch protection requires the CI check; all four members show `pytest` passing locally (screenshot in their PR); `RandomAgent` runs 10 CartPole episodes through the `Agent` interface; invalid YAML raises `ConfigError` naming the key. |

**In simple words:** we build the "workshop" — folders, tools, safety checks — so that from next week everyone can build real AI parts quickly and safely.

---

## SECTION 2 — WHAT WE ARE BUILDING THIS WEEK

1. **Modules:** package skeleton + `pyproject.toml` + CI (Atharv) · `utils/errors.py`, `utils/logging_setup.py` (Vedant) · `utils/config.py` + YAML configs (Somesh) · `utils/seeding.py`, `envs/factory.py`, `agent/base.py`, `agent/random_agent.py`, `cli.py` skeleton (Brahmanand).
2. **Why:** without a package, imports break on some laptops; without CI, broken code reaches `main`; without seeds, results cannot be reproduced; without validation, a typo like `gamma: 1.5` silently ruins an experiment.
3. **Connection:** every later module imports `sla.utils.*`, creates environments with `make_env`, and implements `Agent`. The random agent is the "before learning" baseline used until Week 10.
4. **If missing:** "works on my laptop" bugs, irreproducible numbers, and week-long debugging of config typos.
5. **Final output:**
   ```text
   $ pytest
   ...............................................  [100%]
   47 passed in 3.1s
   $ sla --version
   sla 0.1.0
   ```
   (Exact test count depends on how many tests you add.)

**Analogy:** a kitchen before cooking: shelves labelled (package), a smoke alarm (CI), measuring cups that always measure the same (seeds), a recipe card checked for impossible quantities (config validation).

### Gymnasium in 10 lines (everyone)
```python
import gymnasium as gym
env = gym.make("CartPole-v1")
state, info = env.reset(seed=0)          # start an episode; seed => same start every time
done = False
while not done:
    action = env.action_space.sample()   # random action: 0 = push left, 1 = push right
    state, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated       # terminated: pole fell / cart left; truncated: 500-step limit
env.close()
```

---

## SECTION 3 — DAILY EXECUTION PLAN

### Day 1 — Install PyTorch CPU and Gymnasium; study (1.5 h)
- **Objective:** every laptop can import the core libraries.
- **Members:** all.
- **Tasks:** activate venv; install the libraries below; Atharv starts SLA-03-AG-1; Vedant studies `logging`; Somesh studies dataclasses/YAML (Section 5.6); Brahmanand studies Gymnasium API and `abc`.
- **Commands:**
  ```bash
  git checkout main && git pull
  # activate .venv (see Week 2)
  python -m pip install --upgrade pip
  pip install torch --index-url https://download.pytorch.org/whl/cpu     # Mac: pip install torch
  pip install "gymnasium[classic-control]" numpy pandas scipy matplotlib pyyaml psutil requests streamlit pytest pytest-cov ruff
  python -c "import torch, gymnasium; print(torch.__version__, gymnasium.__version__)"
  ```
- **Expected output:** two version numbers, no error.
- **Testing:** run the 10-line Gymnasium example above.
- **GitHub:** Atharv creates issues #31–#38.
- **Checklist:** - [ ] imports work on my laptop

### Day 2 — Package skeleton, pyproject, CI (1.5 h)
- **Objective:** Atharv's skeleton merged; everyone installs the package in editable mode.
- **Members:** Atharv (implements), others review and install.
- **Tasks:** SLA-03-AG-1 steps 1–6.
- **Commands (everyone after merge):**
  ```bash
  git checkout main && git pull
  pip install -e ".[dev]"
  python -c "import sla; print(sla.__version__)"
  pytest            # Somesh's 5 tests from Week 2 now run without PYTHONPATH
  ```
- **Expected files:** `pyproject.toml`, `src/sla/*/__init__.py`, `.github/workflows/ci.yml`, `CONTRIBUTING.md`.
- **Expected output:** `0.1.0`; 5 tests pass.
- **GitHub:** CI runs on Atharv's PR (Actions tab shows a green tick).
- **Checklist:** - [ ] editable install works for all four

### Day 3 — Errors, logging, seeding, factory (1.5 h)
- **Objective:** shared building blocks.
- **Members:** Vedant (errors, logging), Brahmanand (seeding, factory), Somesh (config start), Atharv (pairing).
- **Tasks:** SLA-03-VB-1 steps 1–5 (merge errors.py by end of day) · SLA-03-BM-1 steps 1–4 · SLA-03-SB-1 steps 1–4.
- **Testing:** `pytest tests/unit/test_logging.py tests/unit/test_envs.py -v`.
- **GitHub:** Vedant's PR merged first (others depend on `sla.utils.errors`).
- **Checklist:** - [ ] errors.py merged

### Day 4 — Agent interface, random agent, config validation (1.5 h)
- **Objective:** `Agent` base class + `RandomAgent`; `load_config` validating every field.
- **Members:** Brahmanand, Somesh; Atharv 1-h pairing with Somesh (pytest parametrize + merge conflict practice).
- **Tasks:** SLA-03-BM-1 steps 5–8 · SLA-03-SB-1 steps 5–9.
- **Testing:** `pytest tests/unit/test_agents.py tests/unit/test_config.py -v`.
- **Checklist:** - [ ] random agent plays 10 CartPole episodes in a test

### Day 5 — CLI skeleton, README, coverage (1.5 h)
- **Objective:** `sla --version` works; README "Run" section; first coverage report.
- **Members:** Brahmanand (CLI skeleton + README), Vedant (CONTRIBUTING error rules), Atharv (CI status check rule), Somesh (finish tests).
- **Commands:** `sla --version` · `pytest --cov=sla --cov-report=term-missing`.
- **Checklist:** - [ ] coverage report printed

### Day 6 — Reviews, merges, everyone runs everything (2.5 h)
- **Objective:** all Week-3 PRs merged; each member posts a screenshot of `pytest` passing on their own laptop.
- **Members:** all.
- **Tasks:** review each other's PRs (see reviewers in Section 4); fix comments; Atharv adds "Require status checks: CI / test" to the `main` ruleset.
- **Checklist:** - [ ] 4 screenshots in the PRs · - [ ] CI required on `main`

### Day 7 — Weekly review (1 h)
- **Objective:** live demo: fresh clone → install → `pytest` → random agent episode. Vedant chairs.
- **Checklist:** - [ ] Section 13 complete

---

## SECTION 4 — INDIVIDUAL MEMBER TASKS

### Brahmanand Mathpati

**Task ID:** SLA-03-BM-1
**Task Title:** Seeding, environment factory, Agent interface, random agent, CLI skeleton
**Priority:** P1
**Estimated Duration:** 11 h (learning 2, coding 5, testing 2, integration/review 1, docs 1)
**Dependencies:** SLA-03-AG-1 (package), SLA-03-VB-1 (`EnvError`)
**Assigned Member:** Brahmanand Mathpati

1. **What:** `src/sla/utils/seeding.py`, `src/sla/envs/factory.py`, `src/sla/agent/base.py`, `src/sla/agent/random_agent.py`, `src/sla/cli.py` (skeleton), tests `tests/unit/test_envs.py`, `tests/unit/test_agents.py`, `tests/unit/test_cli_help.py`; README "Run" section.
2. **Why:** every experiment starts with `make_env` and an `Agent`; seeding makes results reproducible.
3. **Files:** as above (Section 5.3).
4. **Functions/classes:** `set_global_seed(seed)`, `episode_seed(base_seed, episode)`, `make_env(name, seed, render_mode, **kwargs)`, `end_reason(...)`, `Transition`, `Agent`, `RandomAgent`, `build_parser()`, `main()`.
5. **Inputs:** environment name, seed; for agents an observation.
6. **Outputs:** a Gymnasium env; integer actions; `EnvError` for unsupported names.
7. **Steps:**
   1. Create `seeding.py` (Section 5.3.1). Explain in a code comment why `episode_seed` makes resume exact.
   2. Create `factory.py` (5.3.2). FrozenLake defaults to the 4×4 **non-slippery** map so Q-learning can be checked against expectations first.
   3. Write `test_envs.py` (5.3.5): same seed → same observations; different seeds → different; unknown env → `EnvError`; `end_reason` cases.
   4. Run `pytest tests/unit/test_envs.py -v`.
   5. Create `agent/base.py` exactly as frozen in `docs/design.md` §B.
   6. Create `agent/random_agent.py` with save/load (it must continue the same random sequence after loading).
   7. Write `test_agents.py`; run it.
   8. Create the CLI skeleton `src/sla/cli.py` (5.3.6); check `sla --version`.
   9. Add a "Run the tests" section to README.
8. **Commands:**
   ```bash
   git checkout main && git pull
   git checkout -b feat/brahmanand-31-envs-agent-base
   pytest tests/unit/test_envs.py tests/unit/test_agents.py -v
   ruff check src tests
   sla --version
   git add src/sla/utils/seeding.py src/sla/envs/factory.py src/sla/agent/base.py src/sla/agent/random_agent.py src/sla/cli.py tests/unit/test_envs.py tests/unit/test_agents.py tests/unit/test_cli_help.py README.md
   git commit -m "feat(envs): add seeded environment factory, agent interface and random agent"
   git push -u origin feat/brahmanand-31-envs-agent-base
   ```
9. **Tests:** `test_envs.py` (8 tests), `test_agents.py` (2 tests) — Section 5.3.5.
10. **Expected result:** all pass; `sla --version` prints `sla 0.1.0`.
11. **Common errors:** `gymnasium.error.NameNotFound` → typo in env id (`CartPole-v1`, capital C and P); observations differ for the same seed → you reset without `seed=`; `TypeError: Can't instantiate abstract class` → a subclass forgot `act`, `save` or `load`.
12. **Branch:** `feat/brahmanand-31-envs-agent-base`
13. **Commit:** `feat(envs): add seeded environment factory, agent interface and random agent`
14. **PR title:** `feat: environment factory, Agent interface, random agent, CLI skeleton (SLA-03-BM-1)`
15. **Acceptance:** tests pass in CI; random agent runs 10 CartPole episodes through the interface; reviewer: Vedant.

### Atharv Gundale

**Task ID:** SLA-03-AG-1
**Task Title:** Package skeleton, `pyproject.toml`, CI and coding standards
**Priority:** P1
**Estimated Duration:** 11 h (learning 1, coding 4, testing 2, integration/review/mentoring 3, docs 1)
**Dependencies:** `docs/tech_stack.md`
**Assigned Member:** Atharv Gundale

1. **What:** `pyproject.toml`, all `src/sla/<package>/__init__.py` files, `.github/workflows/ci.yml`, `CONTRIBUTING.md`; CI required on `main`; 1-h pairing with Somesh.
2. **Why:** one install command for everyone; automatic checks on every PR.
3. **Files:** Section 5.1.
4. **Function/class:** none (configuration).
5. **Inputs:** stack pins from Week 2.
6. **Outputs:** installable package `sla`; CI workflow.
7. **Steps:**
   1. Create the empty `__init__.py` files for `envs, agent, learning, memory, evaluation, reflection, ui` (Somesh already created `sla/` and `sla/utils/`).
   2. Write `pyproject.toml` (5.1.1). PyTorch is **not** a pip dependency there because the CPU wheel comes from a different index; README and CI install it explicitly.
   3. Write `ci.yml` (5.1.2).
   4. Write `CONTRIBUTING.md` (5.1.3).
   5. Push and confirm the Actions run is green.
   6. Deliberately push a commit with a failing test on a test branch → CI red → delete the branch. Screenshot both for the PR.
   7. Ruleset: require status check "test" before merging.
   8. Pairing with Somesh: `pytest.mark.parametrize`, then create and resolve a merge conflict together.
8. **Commands:**
   ```bash
   git checkout -b chore/atharv-32-package-ci
   pip install -e ".[dev]"
   ruff check .
   pytest
   git add pyproject.toml src/sla/*/__init__.py .github/workflows/ci.yml CONTRIBUTING.md
   git commit -m "chore(build): add pyproject, package skeleton and CI"
   git push -u origin chore/atharv-32-package-ci
   ```
9. **Tests:** CI on the PR; the deliberate-failure demonstration.
10. **Expected result:** green CI; every member's `pip install -e ".[dev]"` succeeds.
11. **Common errors:** `ModuleNotFoundError: sla` in CI → missing `[tool.setuptools.packages.find] where = ["src"]`; CI cannot find torch → the CPU index step is missing.
12. **Branch:** `chore/atharv-32-package-ci`
13. **Commit:** `chore(build): add pyproject, package skeleton and CI`
14. **PR title:** `chore: package skeleton, pyproject and CI (SLA-03-AG-1)`
15. **Acceptance:** CI fails on a failing test and passes otherwise; all members installed; reviewer: Brahmanand.

### Vedant Biradar

**Task ID:** SLA-03-VB-1
**Task Title:** Shared error classes and logging
**Priority:** P1
**Estimated Duration:** 11 h (learning 2, coding 4, testing 3, integration 1, docs 1)
**Dependencies:** SLA-03-AG-1
**Assigned Member:** Vedant Biradar

1. **What:** `src/sla/utils/errors.py`, `src/sla/utils/logging_setup.py`, `tests/unit/test_logging.py`, error-handling rules in `CONTRIBUTING.md`.
2. **Why:** one error family lets the CLI and UI show friendly messages (`except SLAError`); one log format with the run id makes debugging multi-seed experiments possible.
3. **Files:** Section 5.2.
4. **Classes/functions:** `SLAError`, `ConfigError`, `ValidationError`, `EnvError`, `CheckpointError`, `StoreError`, `LLMError`, `TrainingError`; `setup_logging(run_id, log_file, level)`, `get_logger(name)`.
5. **Inputs:** run id, optional log-file path.
6. **Outputs:** log lines like `2026-11-02 10:15:01 | INFO    | run=cartpole_dqn_s0_... | sla.agent.runner | Run ... started`.
7. **Steps:** 1) create `errors.py` and merge it **on Day 3** (others import it); 2) create `logging_setup.py`; 3) tests: log file created and contains the run id; error classes inherit from `SLAError`; 4) call `setup_logging` twice in a test to check handlers are replaced (no duplicate lines); 5) add the rules to CONTRIBUTING.
8. **Commands:**
   ```bash
   git checkout -b feat/vedant-33-errors-logging
   pytest tests/unit/test_logging.py -v
   git add src/sla/utils/errors.py src/sla/utils/logging_setup.py tests/unit/test_logging.py CONTRIBUTING.md
   git commit -m "feat(utils): add error hierarchy and run-aware logging"
   git push -u origin feat/vedant-33-errors-logging
   ```
9. **Tests:** Section 5.2.3.
10. **Expected result:** tests pass; others can `from sla.utils.errors import ConfigError`.
11. **Common errors:** duplicate log lines → handlers added twice (that is why `setup_logging` removes old handlers); `KeyError: 'run_id'` in formatter → the filter adding `run_id` is missing on a handler.
12. **Branch:** `feat/vedant-33-errors-logging`
13. **Commit:** `feat(utils): add error hierarchy and run-aware logging`
14. **PR title:** `feat: errors and logging (SLA-03-VB-1)`
15. **Acceptance:** used by the env factory and config loader; tests pass; reviewer: Atharv.

### Somesh Badwane

**Task ID:** SLA-03-SB-1
**Task Title:** YAML configuration loader with validation (your first class)
**Priority:** P1
**Estimated Duration:** 11 h (learning 3, coding 4, testing 2, review 1, docs 1)
**Dependencies:** SLA-03-AG-1 (install), SLA-03-VB-1 (`ConfigError`)
**Assigned Member:** Somesh Badwane

**0. Learn first (Section 5.6, ~3 h):** type hints; `@dataclass`; default values and `field(default_factory=...)`; YAML format; `raise` with a clear message; `pytest.mark.parametrize`.

1. **What:** `src/sla/utils/config.py` (dataclasses `DQNConfig`, `RunConfig`; functions `validate_config`, `config_from_dict`, `load_config`, `save_config`), four YAML files in `configs/`, and `tests/unit/test_config.py` (≥ 8 tests).
2. **Why:** every run starts from a config. A typo such as `gamma: 1.5` or `episodez: 100` must stop the run with a clear message instead of silently producing wrong results.
3. **Files:** `src/sla/utils/config.py`, `configs/frozenlake_q.yaml`, `configs/frozenlake_random.yaml`, `configs/cartpole_random.yaml`, `configs/cartpole_dqn.yaml` (values from `docs/design.md` §F), `tests/unit/test_config.py`.
4. **Classes/functions:** see 1.
5. **Inputs:** a YAML file path.
6. **Outputs:** a `RunConfig` object; `ConfigError("Invalid config value for 'gamma': must be in (0, 1], got 1.5")` for bad values.
7. **Step-by-step:**
   1. Section 5.6 exercises.
   2. Create the `configs/` folder and the four YAML files (Section 5.4) — type them; notice indentation matters in YAML.
   3. Create `config.py` (Section 5.5). Type it in three parts: (a) the two dataclasses, (b) `_is_int`, `_is_number`, `_check`, `validate_config`, (c) `config_from_dict`, `load_config`, `save_config`.
   4. After part (a), try in Python: `from sla.utils.config import RunConfig; print(RunConfig())`.
   5. After part (b), try: `validate_config(RunConfig(gamma=1.5))` — you should see `ConfigError`.
   6. Write the tests (Section 5.5). `parametrize` runs one test function for 8 different bad values.
   7. Run `pytest tests/unit/test_config.py -v`.
   8. Run ruff: `ruff check src/sla/utils/config.py`.
   9. Open your PR with a screenshot of the passing tests.
8. **Commands:**
   ```bash
   git checkout main && git pull
   git checkout -b feat/somesh-34-config-loader
   python -c "from sla.utils.config import load_config; print(load_config('configs/cartpole_dqn.yaml'))"
   pytest tests/unit/test_config.py -v
   ruff check src/sla/utils/config.py
   git add src/sla/utils/config.py configs/ tests/unit/test_config.py
   git commit -m "feat(utils): add YAML config loader with validation"
   git push -u origin feat/somesh-34-config-loader
   ```
9. **Tests:** valid file loads; repo configs valid; missing file; invalid YAML; 8 parametrised bad values; unknown key; bad DQN value; save-and-reload round trip.
10. **Expected result:** `16 passed` (8 parametrised cases count separately).
11. **Common errors:** `yaml.scanner.ScannerError` → wrong indentation in YAML (use 2 spaces, never tabs); `TypeError: __init__() got an unexpected keyword argument` → a key in YAML that is not a dataclass field (our `config_from_dict` catches this first as "Unknown config key"); test expects `ConfigError` but got `TypeError` → you passed a string where a number is needed before validation (check `_is_number`).
12. **Branch:** `feat/somesh-34-config-loader`
13. **Commit:** `feat(utils): add YAML config loader with validation`
14. **PR title:** `feat: YAML config loader with validation (SLA-03-SB-1)`
15. **Acceptance:** invalid config raises `ConfigError` naming the key; ≥ 8 tests pass; Somesh explains `@dataclass` and `field(default_factory=dict)` in review; reviewer: Atharv.

**Independent practice exercise:** add a check that `eval_episodes` is at most 1000 and write a parametrised test for 1000 (OK) and 1001 (error). Discuss with Atharv whether it belongs in the project (decide together; do not merge without agreement).

---

## SECTION 5 — COMPLETE TECHNICAL IMPLEMENTATION

### 5.1 Build and CI (Atharv)

**5.1.1 `pyproject.toml`**
```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "sla"
version = "0.1.0"
description = "Self-Learning AI Agent: tabular Q-learning and DQN that learn from reward"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
authors = [
  { name = "Brahmanand Mathpati" },
  { name = "Atharv Gundale" },
  { name = "Vedant Biradar" },
  { name = "Somesh Badwane" },
]
dependencies = [
  "gymnasium[classic-control]>=1.0",
  "numpy>=1.26",
  "pandas>=2.1",
  "scipy>=1.11",
  "matplotlib>=3.8",
  "pyyaml>=6.0",
  "psutil>=5.9",
  "requests>=2.31",
  "streamlit>=1.36",
  # PyTorch is installed separately (CPU build), see README / Week 3.
]

[project.optional-dependencies]
dev = ["pytest>=8", "pytest-cov>=5", "ruff>=0.5"]

[project.scripts]
sla = "sla.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"
markers = [
  "smoke: short end-to-end training runs (slower)",
  "torch: tests that need PyTorch",
]

[tool.ruff]
line-length = 120
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W", "B"]
ignore = ["B905"]
```

**5.1.2 `.github/workflows/ci.yml`** (the last step runs tests marked `smoke`; until Week 5 none exist, pytest returns exit code 5 "no tests collected", which the step allows.)
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip
      - name: Install PyTorch (CPU) and the project
        run: |
          python -m pip install --upgrade pip
          pip install torch --index-url https://download.pytorch.org/whl/cpu
          pip install -e ".[dev]"
      - name: Lint
        run: ruff check .
      - name: Unit and integration tests (without slow smoke runs)
        run: pytest -m "not smoke" --cov=sla --cov-report=term-missing
      - name: Smoke training run (exit code 5 = no smoke tests yet, allowed before Week 5)
        run: pytest -m smoke || test $? -eq 5
```

**5.1.3 `CONTRIBUTING.md`**
```markdown
# Contributing

## Daily routine
1. `git checkout main && git pull`
2. `git checkout -b feat/<name>-<issue#>-<short-name>`
3. Write code + tests. Run `ruff check .` and `pytest`.
4. `git add <files>` → `git commit -m "feat(scope): summary"` → `git push -u origin <branch>`
5. Open a pull request, fill the template, request your reviewer.

## Coding conventions
- Python 3.10+, type hints on public functions, a docstring on every module and public function.
- Raise errors from `sla.utils.errors` (ConfigError, ValidationError, EnvError, CheckpointError, StoreError, LLMError, TrainingError), never a bare `Exception`.
- Log with `get_logger(__name__)` from `sla.utils.logging_setup`; never `print` inside library code (CLI and scripts may print).
- Only the module owner changes a module's public functions. Interfaces are frozen on Mondays.
- Every new function gets a test. Tests must not need internet or Ollama.

## Commit messages (Conventional Commits)
`feat(agent): add epsilon-greedy policy` · `fix(memory): close sqlite connection` · `test(utils): cover bad seeds` · `docs(readme): add quickstart`
```

Empty package files (create each with no content):
```text
src/sla/envs/__init__.py
src/sla/agent/__init__.py
src/sla/learning/__init__.py
src/sla/memory/__init__.py
src/sla/evaluation/__init__.py
src/sla/reflection/__init__.py
src/sla/ui/__init__.py
```
`src/sla/__init__.py` (replace Somesh's empty file):
```python
"""Self-Learning AI Agent (sla).

An agent that starts with no knowledge of its task and improves by learning from
environment rewards (tabular Q-learning on FrozenLake, DQN on CartPole).
"""

__version__ = "0.1.0"
```

### 5.2 Errors and logging (Vedant)

**5.2.1 `src/sla/utils/errors.py`**
```python
"""Project-wide exception classes (owner: Vedant).

Every module raises one of these instead of a bare Exception, so callers
(CLI, UI, pipeline) can show a clear message for each kind of failure.
"""


class SLAError(Exception):
    """Base class for all errors raised by the sla package."""


class ConfigError(SLAError):
    """A configuration file or value is missing or invalid."""


class ValidationError(SLAError):
    """User input or a runtime value failed validation."""


class EnvError(SLAError):
    """An environment could not be created or behaved unexpectedly."""


class CheckpointError(SLAError):
    """A checkpoint could not be saved or loaded."""


class StoreError(SLAError):
    """The SQLite episode store could not be read or written."""


class LLMError(SLAError):
    """The optional local LLM (Ollama) is unavailable or returned an error."""


class TrainingError(SLAError):
    """Training was stopped by a safety limit or a learning guard."""
```

**5.2.2 `src/sla/utils/logging_setup.py`**
```python
"""Logging helpers (owner: Vedant).

Usage:
    from sla.utils.logging_setup import setup_logging, get_logger
    setup_logging(run_id="cartpole_dqn_s0", log_file=Path("runs/x/run.log"))
    log = get_logger(__name__)
    log.info("training started")
"""

from __future__ import annotations

import logging
from pathlib import Path

LOG_FORMAT = "%(asctime)s | %(levelname)-7s | run=%(run_id)s | %(name)s | %(message)s"
_ROOT = "sla"


class _RunIdFilter(logging.Filter):
    """Adds the current run id to every log record."""

    def __init__(self, run_id: str) -> None:
        super().__init__()
        self.run_id = run_id

    def filter(self, record: logging.LogRecord) -> bool:
        record.run_id = self.run_id
        return True


def setup_logging(run_id: str = "-", log_file: Path | None = None, level: str = "INFO") -> logging.Logger:
    """Configure the package logger once per run.

    Logs go to the console and, if ``log_file`` is given, to that file too.
    Calling it again replaces the previous handlers (safe in tests and the UI).
    """
    logger = logging.getLogger(_ROOT)
    logger.setLevel(level.upper())
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()
    for flt in list(logger.filters):
        logger.removeFilter(flt)

    formatter = logging.Formatter(LOG_FORMAT)
    run_filter = _RunIdFilter(run_id)

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.addFilter(run_filter)
    logger.addHandler(console)

    if log_file is not None:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.addFilter(run_filter)
        logger.addHandler(file_handler)

    logger.propagate = False
    return logger


def get_logger(name: str) -> logging.Logger:
    """Return a child logger of the package logger, e.g. ``sla.agent.runner``."""
    if not name.startswith(_ROOT):
        name = f"{_ROOT}.{name}"
    return logging.getLogger(name)
```

**5.2.3 `tests/unit/test_logging.py`**
```python
from sla.utils.errors import ConfigError, SLAError
from sla.utils.logging_setup import get_logger, setup_logging


def test_log_file_has_run_id(tmp_path):
    log_file = tmp_path / "run.log"
    setup_logging("run_42", log_file)
    get_logger("test").info("hello")
    text = log_file.read_text(encoding="utf-8")
    assert "run=run_42" in text and "hello" in text


def test_errors_are_sla_errors():
    assert issubclass(ConfigError, SLAError)
    assert str(ConfigError("bad gamma")) == "bad gamma"


def test_setup_twice_does_not_duplicate_lines(tmp_path):
    log_file = tmp_path / "run.log"
    setup_logging("a", log_file)
    setup_logging("a", log_file)
    get_logger("x").info("once")
    assert log_file.read_text(encoding="utf-8").count("once") == 1
```


### 5.3 Seeding, environments, agents, CLI (Brahmanand)

**5.3.1 `src/sla/utils/seeding.py`**
```python
"""Global random seeding (owner: Brahmanand).

Seeding makes runs reproducible: the same seed gives the same results.
"""

from __future__ import annotations

import os
import random

import numpy as np


def set_global_seed(seed: int) -> None:
    """Seed Python, NumPy and (if installed) PyTorch."""
    if not isinstance(seed, int) or seed < 0:
        raise ValueError(f"seed must be a non-negative int, got {seed!r}")
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
    except ImportError:  # PyTorch is optional until Week 4
        return
    torch.manual_seed(seed)


def episode_seed(base_seed: int, episode: int) -> int:
    """Seed used for env.reset() in a given episode.

    Using base_seed * 100_000 + episode means every episode starts from a known
    state, so a resumed run continues exactly where it stopped.
    """
    return base_seed * 100_000 + episode
```

**5.3.2 `src/sla/envs/factory.py`**
```python
"""Environment factory (owner: Brahmanand, Week 3).

All code creates environments through ``make_env`` so seeding and error
messages are handled in one place.
"""

from __future__ import annotations

from typing import Any

import gymnasium as gym

from sla.utils.errors import EnvError

SUPPORTED_ENVS: dict[str, dict[str, Any]] = {
    # name: default keyword arguments passed to gymnasium.make
    "FrozenLake-v1": {"map_name": "4x4", "is_slippery": False},
    "CartPole-v1": {},
}

CARTPOLE_X_LIMIT = 2.4  # Gymnasium ends a CartPole episode when |x| > 2.4


def make_env(name: str, seed: int | None = None, render_mode: str | None = None,
             **kwargs: Any) -> gym.Env:
    """Create a supported Gymnasium environment.

    Args:
        name: "FrozenLake-v1" or "CartPole-v1".
        seed: if given, seeds the action space so random actions repeat.
        render_mode: None, "human" (window) or "rgb_array" (frames for GIFs).
        **kwargs: overrides for the defaults in SUPPORTED_ENVS.
    """
    if name not in SUPPORTED_ENVS:
        raise EnvError(f"Unsupported environment {name!r}. Supported: {sorted(SUPPORTED_ENVS)}")
    options = {**SUPPORTED_ENVS[name], **kwargs}
    try:
        env = gym.make(name, render_mode=render_mode, **options)
    except Exception as exc:  # gymnasium raises several error types
        raise EnvError(f"Could not create {name} with options {options}: {exc}") from exc
    if seed is not None:
        env.action_space.seed(seed)
    return env


def end_reason(env_name: str, terminated: bool, truncated: bool, reward: float,
               state: Any) -> str:
    """Explain why an episode ended, for logs and failure analysis.

    FrozenLake: "goal", "hole" or "truncated".
    CartPole:   "position" (cart left the track), "angle" (pole fell) or "truncated".
    """
    if truncated and not terminated:
        return "truncated"
    if not terminated:
        return "running"
    if env_name == "FrozenLake-v1":
        return "goal" if reward > 0 else "hole"
    if env_name == "CartPole-v1":
        x = float(state[0])
        return "position" if abs(x) > CARTPOLE_X_LIMIT else "angle"
    return "terminated"
```

**5.3.3 `src/sla/agent/base.py`** (exactly the frozen interface)
```python
"""The Agent interface every agent implements (owner: Brahmanand, Week 3).

Frozen in Week 2 (docs/design.md). Do not change signatures without a team
decision, because the runner, checkpoints and evaluator depend on them.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Transition:
    """One step of experience: what the agent saw, did and got."""

    state: Any
    action: int
    reward: float
    next_state: Any
    terminated: bool
    truncated: bool


class Agent(ABC):
    """Base class for RandomAgent, QLearningAgent and DQNAgent."""

    name: str = "base"

    @abstractmethod
    def act(self, obs: Any, explore: bool = True) -> int:
        """Choose an action. explore=False means greedy (used for evaluation)."""

    def update(self, transition: Transition) -> dict[str, float]:
        """Learn from one transition. Returns stats such as {"loss": 0.12}."""
        return {}

    def end_episode(self) -> None:
        """Called by the runner after every episode (optional hook)."""
        return None

    @property
    def epsilon(self) -> float | None:
        """Current exploration rate, or None if the agent does not explore."""
        return None

    @abstractmethod
    def save(self, path: Path) -> None:
        """Save everything needed to continue later into the folder ``path``."""

    @classmethod
    @abstractmethod
    def load(cls, path: Path) -> Agent:
        """Re-create an agent from a folder written by ``save``."""
```

**5.3.4 `src/sla/agent/random_agent.py`**
```python
"""Random agent: the "before learning" baseline (owner: Brahmanand, Week 3)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np

from sla.agent.base import Agent
from sla.utils.io_helpers import ensure_dir, read_json, write_json


class RandomAgent(Agent):
    """Picks every action uniformly at random and never learns."""

    name = "random"

    def __init__(self, n_actions: int, seed: int = 0) -> None:
        if n_actions <= 0:
            raise ValueError("n_actions must be > 0")
        self.n_actions = n_actions
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def act(self, obs: Any, explore: bool = True) -> int:
        return int(self.rng.integers(self.n_actions))

    def save(self, path: Path) -> None:
        folder = ensure_dir(path)
        write_json(folder / "meta.json", {"agent": self.name, "n_actions": self.n_actions,
                                          "seed": self.seed, "rng_state": self.rng.bit_generator.state})

    @classmethod
    def load(cls, path: Path) -> RandomAgent:
        meta = read_json(Path(path) / "meta.json")
        agent = cls(meta["n_actions"], meta["seed"])
        agent.rng.bit_generator.state = meta["rng_state"]
        return agent
```

**5.3.5 Tests** — `tests/unit/test_envs.py`
```python
import numpy as np
import pytest

from sla.agent.random_agent import RandomAgent
from sla.envs.factory import end_reason, make_env
from sla.utils.errors import EnvError
from sla.utils.seeding import episode_seed, set_global_seed


def rollout(seed):
    env = make_env("CartPole-v1", seed=seed)
    obs, _ = env.reset(seed=seed)
    observations = [obs]
    for _ in range(100):
        obs, _, term, trunc, _ = env.step(env.action_space.sample())
        observations.append(obs)
        if term or trunc:
            obs, _ = env.reset()
    env.close()
    return np.array(observations)


def test_same_seed_same_observations():
    assert np.array_equal(rollout(0), rollout(0))


def test_different_seed_different_observations():
    assert not np.array_equal(rollout(0), rollout(1))


def test_unknown_env():
    with pytest.raises(EnvError, match="Unsupported"):
        make_env("Cartpole-v9")


def test_frozenlake_defaults_not_slippery():
    env = make_env("FrozenLake-v1")
    assert env.observation_space.n == 16 and env.action_space.n == 4
    env.close()


def test_end_reasons():
    assert end_reason("FrozenLake-v1", True, False, 1.0, 15) == "goal"
    assert end_reason("FrozenLake-v1", True, False, 0.0, 5) == "hole"
    assert end_reason("CartPole-v1", True, False, 1.0, [2.5, 0, 0, 0]) == "position"
    assert end_reason("CartPole-v1", True, False, 1.0, [0.1, 0, 0.3, 0]) == "angle"
    assert end_reason("CartPole-v1", False, True, 1.0, [0, 0, 0, 0]) == "truncated"


def test_episode_seed_unique():
    assert episode_seed(0, 5) != episode_seed(1, 5)


def test_set_global_seed_rejects_negative():
    with pytest.raises(ValueError):
        set_global_seed(-1)


def test_random_agent_runs_ten_episodes():
    env = make_env("CartPole-v1", seed=0)
    agent = RandomAgent(env.action_space.n, seed=0)
    for ep in range(10):
        obs, _ = env.reset(seed=ep)
        done = False
        while not done:
            obs, r, term, trunc, _ = env.step(agent.act(obs))
            done = term or trunc
    env.close()
```

`tests/unit/test_agents.py`
```python
from sla.agent.random_agent import RandomAgent


def test_random_agent_actions_in_range():
    agent = RandomAgent(4, seed=0)
    actions = {agent.act(None) for _ in range(200)}
    assert actions <= {0, 1, 2, 3} and len(actions) == 4


def test_random_agent_save_load_continues_same_sequence(tmp_path):
    agent = RandomAgent(3, seed=7)
    agent.act(None)
    agent.save(tmp_path / "ck")
    clone = RandomAgent.load(tmp_path / "ck")
    assert [agent.act(None) for _ in range(20)] == [clone.act(None) for _ in range(20)]
```

**5.3.6 `src/sla/cli.py` — Week-3 skeleton.** Weeks 5–7 add command blocks; each block appends a function to `PARSER_BUILDERS`, so the bottom of this file never changes.
```python
"""Command-line interface: `sla <command>` (owner: Brahmanand).

Week 3 skeleton: the parser and main() exist; commands are added in Weeks 5-7
by appending a "parser builder" function to PARSER_BUILDERS.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable

from sla.utils.errors import SLAError

PARSER_BUILDERS: list[Callable[[argparse._SubParsersAction], None]] = []
DEFAULT_DB = "runs/episodes.db"


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

`tests/unit/test_cli_help.py`:
```python
"""Week 3 (Brahmanand): the CLI skeleton exists and prints help."""

from sla.cli import build_parser, main


def test_no_command_prints_help(capsys):
    assert main([]) == 1
    assert "usage: sla" in capsys.readouterr().out


def test_parser_name():
    assert build_parser().prog == "sla"
```

Expected:
```text
$ sla --version
sla 0.1.0
$ sla
usage: sla [-h] [--version] {} ...      (no commands yet; exit code 1)
```

**README addition (Brahmanand):**
````markdown
## Development setup
```bash
python -m venv .venv && source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -e ".[dev]"
pytest && ruff check .
```
````

### 5.4 YAML configs (Somesh)

`configs/frozenlake_q.yaml`
```yaml
# Tabular Q-learning on FrozenLake 4x4 (non-slippery first; set is_slippery: true later)
env_name: FrozenLake-v1
env_kwargs:
  map_name: 4x4
  is_slippery: false
agent: q_learning
episodes: 2000
seed: 0
gamma: 0.99
learning_rate: 0.1          # alpha in the Q-learning update
epsilon_start: 1.0
epsilon_end: 0.05
epsilon_decay_steps: 10000  # environment steps
max_steps_per_episode: 100
max_wall_clock_s: 600
eval_every: 100
eval_episodes: 20
checkpoint_every: 500
run_root: runs
```

`configs/frozenlake_random.yaml`
```yaml
# Random baseline on FrozenLake 4x4 (no learning)
env_name: FrozenLake-v1
env_kwargs:
  map_name: 4x4
  is_slippery: false
agent: random
episodes: 200
seed: 0
max_steps_per_episode: 100
eval_every: 100
eval_episodes: 20
checkpoint_every: 100
run_root: runs
```

`configs/cartpole_random.yaml`
```yaml
# Random baseline on CartPole-v1 (no learning)
env_name: CartPole-v1
agent: random
episodes: 200
seed: 0
max_steps_per_episode: 500
eval_every: 100
eval_episodes: 20
checkpoint_every: 100
run_root: runs
```

`configs/cartpole_dqn.yaml` (values from `docs/design.md` §F; Atharv tunes them in Week 6)
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

### 5.5 `src/sla/utils/config.py` and tests (Somesh)

```python
"""Run configuration: load a YAML file into checked dataclasses (owner: Somesh, Week 3).

Example YAML (configs/frozenlake_q.yaml):

    env_name: FrozenLake-v1
    env_kwargs: {is_slippery: false}
    agent: q_learning
    episodes: 2000
    seed: 0
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from typing import Any

import yaml

from sla.utils.errors import ConfigError

ALLOWED_ENVS = ("FrozenLake-v1", "CartPole-v1")
ALLOWED_AGENTS = ("random", "q_learning", "dqn")


@dataclass
class DQNConfig:
    """Settings used only when agent == 'dqn'."""

    hidden_size: int = 128
    batch_size: int = 64
    buffer_size: int = 50_000
    learning_starts: int = 1_000
    train_freq: int = 1
    target_update_every: int = 500
    grad_clip: float = 10.0
    replay_enabled: bool = True
    target_net_enabled: bool = True


@dataclass
class RunConfig:
    """Everything needed to start one training run."""

    env_name: str = "FrozenLake-v1"
    agent: str = "q_learning"
    episodes: int = 1000
    seed: int = 0
    env_kwargs: dict[str, Any] = field(default_factory=dict)
    gamma: float = 0.99
    learning_rate: float = 0.1
    epsilon_start: float = 1.0
    epsilon_end: float = 0.05
    epsilon_decay_steps: int = 10_000
    max_steps_per_episode: int = 500
    max_wall_clock_s: float = 3_600.0
    eval_every: int = 50
    eval_episodes: int = 20
    checkpoint_every: int = 50
    run_root: str = "runs"
    dqn: DQNConfig = field(default_factory=DQNConfig)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _check(condition: bool, key: str, message: str) -> None:
    if not condition:
        raise ConfigError(f"Invalid config value for '{key}': {message}")


def validate_config(cfg: RunConfig) -> RunConfig:
    """Raise ConfigError (naming the bad key) if any value is wrong."""
    _check(cfg.env_name in ALLOWED_ENVS, "env_name", f"must be one of {ALLOWED_ENVS}, got {cfg.env_name!r}")
    _check(cfg.agent in ALLOWED_AGENTS, "agent", f"must be one of {ALLOWED_AGENTS}, got {cfg.agent!r}")
    positive_ints = ("episodes", "max_steps_per_episode", "eval_every", "eval_episodes", "checkpoint_every",
                     "epsilon_decay_steps")
    for key in positive_ints:
        value = getattr(cfg, key)
        _check(_is_int(value) and value > 0, key, f"must be a positive integer, got {value!r}")
    _check(_is_int(cfg.seed) and cfg.seed >= 0, "seed", f"must be an integer >= 0, got {cfg.seed!r}")
    _check(_is_number(cfg.gamma) and 0 < cfg.gamma <= 1, "gamma", f"must be in (0, 1], got {cfg.gamma!r}")
    _check(_is_number(cfg.learning_rate) and cfg.learning_rate > 0, "learning_rate",
           f"must be > 0, got {cfg.learning_rate!r}")
    for key in ("epsilon_start", "epsilon_end"):
        value = getattr(cfg, key)
        _check(_is_number(value) and 0 <= value <= 1, key, f"must be in [0, 1], got {value!r}")
    _check(cfg.epsilon_end <= cfg.epsilon_start, "epsilon_end", "must be <= epsilon_start")
    _check(_is_number(cfg.max_wall_clock_s) and cfg.max_wall_clock_s > 0, "max_wall_clock_s", "must be > 0")
    _check(isinstance(cfg.env_kwargs, dict), "env_kwargs", "must be a mapping")
    d = cfg.dqn
    for key in ("hidden_size", "batch_size", "buffer_size", "learning_starts", "train_freq", "target_update_every"):
        value = getattr(d, key)
        _check(_is_int(value) and value > 0, f"dqn.{key}", f"must be a positive integer, got {value!r}")
    _check(d.batch_size <= d.buffer_size, "dqn.batch_size", "must be <= dqn.buffer_size")
    _check(_is_number(d.grad_clip) and d.grad_clip > 0, "dqn.grad_clip", "must be > 0")
    return cfg


def config_from_dict(data: dict[str, Any]) -> RunConfig:
    """Build a RunConfig from a plain dict, rejecting unknown keys."""
    if not isinstance(data, dict):
        raise ConfigError("Config must be a mapping of key: value pairs")
    allowed = {f.name for f in fields(RunConfig)}
    unknown = set(data) - allowed
    if unknown:
        raise ConfigError(f"Unknown config key(s): {sorted(unknown)}")
    data = dict(data)
    dqn_data = data.pop("dqn", None) or {}
    if not isinstance(dqn_data, dict):
        raise ConfigError("Invalid config value for 'dqn': must be a mapping")
    dqn_allowed = {f.name for f in fields(DQNConfig)}
    dqn_unknown = set(dqn_data) - dqn_allowed
    if dqn_unknown:
        raise ConfigError(f"Unknown dqn key(s): {sorted(dqn_unknown)}")
    try:
        cfg = RunConfig(**data, dqn=DQNConfig(**dqn_data))
    except TypeError as exc:  # pragma: no cover - defensive
        raise ConfigError(str(exc)) from exc
    return validate_config(cfg)


def load_config(path: str | Path) -> RunConfig:
    """Read a YAML file and return a validated RunConfig."""
    file_path = Path(path)
    if not file_path.is_file():
        raise ConfigError(f"Config file not found: {file_path}")
    try:
        data = yaml.safe_load(file_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ConfigError(f"Config file {file_path} is not valid YAML: {exc}") from exc
    return config_from_dict(data)


def save_config(cfg: RunConfig, path: str | Path) -> Path:
    """Write a RunConfig back to YAML (used to copy the config into each run folder)."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(yaml.safe_dump(cfg.to_dict(), sort_keys=False), encoding="utf-8")
    return file_path
```

**Explanation for Somesh:**
- `@dataclass` automatically writes `__init__`, `__repr__` and `__eq__` for a class that mainly stores values. `RunConfig(episodes=10)` creates one with all other fields at their defaults.
- `env_kwargs: dict[str, Any] = field(default_factory=dict)` — a list/dict default must use `default_factory`, otherwise every config would share **the same** dict object.
- `dqn: DQNConfig = field(default_factory=DQNConfig)` — a config inside a config (the `dqn:` block in YAML).
- `_is_int` rejects `True`/`False` because in Python `True` is technically the integer 1.
- `_check(condition, key, message)` raises one consistent error format, so the message always names the bad key.
- `config_from_dict` rejects unknown keys (catches typos like `episodez`), builds `DQNConfig` from the nested `dqn` mapping, then validates.
- `yaml.safe_load` reads YAML safely (never use `yaml.load` on untrusted files).
- `save_config` writes a copy of the config into each run folder so every result can be reproduced later.

`tests/unit/test_config.py`
```python
import pytest

from sla.utils.config import RunConfig, config_from_dict, load_config, save_config
from sla.utils.errors import ConfigError


def write(tmp_path, text):
    path = tmp_path / "cfg.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def test_loads_valid_file(tmp_path):
    cfg = load_config(write(tmp_path, "env_name: CartPole-v1\nagent: dqn\nepisodes: 10\n"))
    assert cfg.env_name == "CartPole-v1" and cfg.episodes == 10 and cfg.dqn.batch_size == 64


def test_repo_configs_are_valid():
    for name in ["frozenlake_q", "frozenlake_random", "cartpole_random", "cartpole_dqn"]:
        assert isinstance(load_config(f"configs/{name}.yaml"), RunConfig)


def test_missing_file(tmp_path):
    with pytest.raises(ConfigError, match="not found"):
        load_config(tmp_path / "nope.yaml")


def test_invalid_yaml(tmp_path):
    with pytest.raises(ConfigError, match="not valid YAML"):
        load_config(write(tmp_path, "episodes: [1, 2\n"))


@pytest.mark.parametrize("key,value", [
    ("gamma", 1.5), ("gamma", 0), ("learning_rate", -0.1), ("episodes", 0),
    ("episodes", "many"), ("env_name", "Pong-v5"), ("agent", "ppo"), ("seed", -1),
])
def test_bad_values_name_the_key(key, value):
    with pytest.raises(ConfigError, match=key):
        config_from_dict({key: value})


def test_unknown_key_rejected():
    with pytest.raises(ConfigError, match="Unknown config key"):
        config_from_dict({"episodez": 10})


def test_bad_dqn_value():
    with pytest.raises(ConfigError, match="dqn.batch_size"):
        config_from_dict({"agent": "dqn", "env_name": "CartPole-v1", "dqn": {"batch_size": 0}})


def test_save_and_reload(tmp_path):
    cfg = config_from_dict({"env_name": "CartPole-v1", "agent": "dqn", "dqn": {"hidden_size": 64}})
    again = load_config(save_config(cfg, tmp_path / "copy.yaml"))
    assert again == cfg
```

### 5.6 Python lessons for Somesh (Week 3)

```python
# Type hints: describe what a function expects and returns (Python does not enforce them; tools like ruff/IDEs use them)
def scale(value: float, factor: float = 2.0) -> float:
    return value * factor

# Dataclass: a class for storing data, with __init__ written for you
from dataclasses import dataclass, field

@dataclass
class Student:
    name: str
    marks: list[int] = field(default_factory=list)   # each Student gets its OWN list
    year: int = 4

s = Student("Somesh")
s.marks.append(90)
print(s)                     # Student(name='Somesh', marks=[90], year=4)

# YAML: indentation-based text format. Read it into Python dicts/lists:
import yaml
text = """
episodes: 100
dqn:
  batch_size: 64
"""
data = yaml.safe_load(text)
print(data["dqn"]["batch_size"])     # 64

# parametrize: one test, many inputs
import pytest

@pytest.mark.parametrize("value,expected", [(1, 2.0), (2.5, 5.0)])
def test_scale(value, expected):
    assert scale(value) == expected
```
Mini-exercises: (a) dataclass `Laptop(name, ram_gb, cores=4)`; (b) YAML with a nested `owner:` block, load it, print the nested value; (c) parametrised test for `is_enough_ram` from Week 1 with 3 cases.

---

## SECTION 6 — PROJECT FOLDER STRUCTURE

```text
self-learning-ai-agent/
├── .github/
│   ├── workflows/
│   │   └── ci.yml   [NEW · Atharv]
│   └── PULL_REQUEST_TEMPLATE.md
├── configs/
│   ├── cartpole_dqn.yaml   [NEW · Somesh → Atharv]
│   ├── cartpole_random.yaml   [NEW · Somesh]
│   ├── frozenlake_q.yaml   [NEW · Somesh]
│   └── frozenlake_random.yaml   [NEW · Somesh]
├── docs/
│   ├── notes/
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
│   └── hardware_check.py
├── spikes/
│   └── llm_benchmark.py
├── src/
│   └── sla/
│       ├── agent/
│       │   ├── __init__.py   [NEW · Atharv]
│       │   ├── base.py   [NEW · Brahmanand]
│       │   └── random_agent.py   [NEW · Brahmanand]
│       ├── envs/
│       │   ├── __init__.py   [NEW · Atharv]
│       │   └── factory.py   [NEW · Brahmanand]
│       ├── evaluation/
│       │   └── __init__.py   [NEW · Atharv]
│       ├── learning/
│       │   └── __init__.py   [NEW · Atharv]
│       ├── memory/
│       │   └── __init__.py   [NEW · Atharv]
│       ├── reflection/
│       │   └── __init__.py   [NEW · Atharv]
│       ├── ui/
│       │   └── __init__.py   [NEW · Atharv]
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── config.py   [NEW · Somesh]
│       │   ├── errors.py   [NEW · Vedant]
│       │   ├── io_helpers.py
│       │   ├── logging_setup.py   [NEW · Vedant]
│       │   └── seeding.py   [NEW · Brahmanand]
│       ├── __init__.py
│       └── cli.py   [NEW · Brahmanand]
├── tests/
│   └── unit/
│       ├── test_agents.py   [NEW · Brahmanand]
│       ├── test_cli_help.py   [NEW · Brahmanand]
│       ├── test_config.py   [NEW · Somesh]
│       ├── test_envs.py   [NEW · Brahmanand]
│       ├── test_io_helpers.py
│       └── test_logging.py   [NEW · Vedant]
├── .env.example
├── .gitignore
├── CONTRIBUTING.md   [NEW · Atharv + Vedant]
├── pyproject.toml   [NEW · Atharv]
└── README.md   [MODIFIED · Atharv → Brahmanand]
```

Legend: [NEW] created this week · [MODIFIED] changed this week · no tag = carried over unchanged from an earlier week. `runs/` (training outputs) and `.venv/` exist on your laptop but are git-ignored, so they are not shown.

---

## SECTION 7 — GITHUB COLLABORATION PROCEDURE

Standard flow (issue → assign → branch → pull → implement → test → stage → commit → push → PR → review → fix → merge). **New this week:** CI must be green before "Merge" is allowed.

| # | Title | Owner | Reviewer | Branch |
|---|---|---|---|---|
| 31 | Env factory, Agent interface, random agent, CLI skeleton | Brahmanand | Vedant | `feat/brahmanand-31-envs-agent-base` |
| 32 | Package skeleton, pyproject, CI | Atharv | Brahmanand | `chore/atharv-32-package-ci` |
| 33 | Errors and logging | Vedant | Atharv | `feat/vedant-33-errors-logging` |
| 34 | YAML config loader | Somesh | Atharv | `feat/somesh-34-config-loader` |

**Merge order (avoids broken imports):** #32 (Day 2) → #33 (Day 3) → #31 and #34 (Day 4–6).

**When CI fails on your PR:** click "Details" next to the red ✗ → read the first red line → reproduce locally (`ruff check .` or `pytest -x`) → fix → commit → push. Never merge red.

**Keeping your branch up to date with `main` (rebase):**
```bash
git checkout feat/somesh-34-config-loader
git fetch origin
git rebase origin/main         # replay your commits on top of the latest main
# if conflicts: fix files, then
git add <file> && git rebase --continue
git push --force-with-lease    # safe force-push for YOUR feature branch only
```

---

## SECTION 8 — WEEKLY INTEGRATION PROCEDURE

| Item | This week |
|---|---|
| Modules that connect | `factory.py` ← `errors.EnvError`; `config.py` ← `errors.ConfigError`; `random_agent.py` ← `io_helpers` (Week 2) and `agent/base.py`; `cli.py` ← `errors.SLAError`. |
| Integrator | Vedant (captain W3) checks the merge order and runs the full suite after each merge. |
| Interfaces that must match | `Agent` signatures = `docs/design.md` §B; `RunConfig` fields include everything the runner (W4) needs: `episodes, seed, max_steps_per_episode, max_wall_clock_s, eval_every, checkpoint_every, run_root, env_kwargs, dqn`. |
| Tests that must pass | Full `pytest` + `ruff check .` locally and in CI. |
| Detect failures | `ImportError` in CI after a merge; tests passing alone but failing together (shared state). |
| Debug | `pytest -x -vv` stops at the first failure; `pip show sla` checks the editable install; `python -c "import sla, sys; print(sla.__file__)"` must point into `src/`. |

**Integration checklist**
- [ ] `pip install -e ".[dev]"` works on all 4 laptops
- [ ] Full test suite green locally and in CI
- [ ] `load_config("configs/cartpole_dqn.yaml")` returns a `RunConfig` with `dqn.batch_size == 64`
- [ ] `make_env("CartPole-v1", seed=0)` + `RandomAgent` run an episode
- [ ] `sla --version` works

---

## SECTION 9 — TESTING AND VALIDATION

- **Unit tests:** `test_io_helpers` (W2), `test_logging`, `test_envs`, `test_agents`, `test_config`.
- **Integration test (informal):** random agent through the env factory for 10 episodes.
- **Input validation:** `ConfigError` for unknown keys, wrong types, out-of-range values; `EnvError` for unknown environments.
- **Error handling:** CLI catches `SLAError` and prints `Error: ...` with exit code 1.
- **Reproducibility:** `test_same_seed_same_observations`; random agent save/load continues the same sequence.
- **Commands:**
  ```bash
  pytest -v
  pytest --cov=sla --cov-report=term-missing
  ruff check .
  ```
- **Expected conditions:** 0 failures; coverage of `sla/utils/config.py` ≥ 90%.

---

## SECTION 10 — COMMON PROBLEMS AND SOLUTIONS

| Problem | Possible Cause | How to Check | Solution |
|---|---|---|---|
| `pip install -e .` fails: "does not appear to be a Python project" | Not in repo root | `ls pyproject.toml` | `cd` into the repo |
| `ERROR: No matching distribution found for torch` | Python too new / 32-bit | `python --version`; `python -c "import sys; print(sys.maxsize > 2**32)"` | Install 64-bit Python 3.11 and recreate `.venv` |
| `ModuleNotFoundError: No module named 'sla'` | venv not active / not installed | `pip show sla` | Activate `.venv`; `pip install -e ".[dev]"` |
| `ModuleNotFoundError: gymnasium` in CI | Dependency missing in pyproject | CI log | Add to `dependencies`; push |
| Same seed, different observations | `reset()` without `seed=` | Read the test | Pass `seed=` to the first `reset` |
| `yaml.scanner.ScannerError` | Tabs or wrong indentation | Error shows line | 2 spaces per level |
| Duplicate log lines | Handlers added twice | Count lines in log | Use `setup_logging` (removes old handlers) |
| CI green locally red on GitHub | Different Python version / missing file not committed | `git status` | Commit the file; match Python 3.11 |
| Ruff `F401 imported but unused` | Leftover import | Ruff message shows line | Delete it or run `ruff check --fix` |

---

## SECTION 11 — WEEKLY DELIVERABLES

| Deliverable | Owner | File/Location | Verification | Status |
|---|---|---|---|---|
| Package + pyproject | Atharv | `pyproject.toml`, `src/sla/*/__init__.py` | Editable install on 4 laptops | [ ] |
| CI workflow + required check | Atharv | `.github/workflows/ci.yml` | Fails on failing test; required on `main` | [ ] |
| Contribution guide | Atharv + Vedant | `CONTRIBUTING.md` | Reviewed | [ ] |
| Errors + logging | Vedant | `utils/errors.py`, `utils/logging_setup.py` | `test_logging.py` passes | [ ] |
| Seeding + env factory | Brahmanand | `utils/seeding.py`, `envs/factory.py` | `test_envs.py` passes | [ ] |
| Agent interface + random agent | Brahmanand | `agent/base.py`, `agent/random_agent.py` | `test_agents.py` passes | [ ] |
| CLI skeleton | Brahmanand | `src/sla/cli.py` | `sla --version` | [ ] |
| Config loader + 4 configs | Somesh | `utils/config.py`, `configs/*.yaml` | `test_config.py` ≥ 8 tests pass | [ ] |

---

## SECTION 12 — WEEKLY REVIEW MEETING

**Agenda:** live fresh-clone demo · pending tasks · blockers · code quality (ruff, docstrings, type hints) · test results and coverage · PR status · integration status · Week-4 dependencies.

**Questions:**
1. What exactly does `pip install -e .` do, and why "editable"?
2. Why is PyTorch installed separately from `pyproject.toml` dependencies?
3. What is the difference between `terminated` and `truncated` in `env.step`?
4. Why does `episode_seed` use `base_seed * 100_000 + episode`?
5. What happens if the YAML says `episodes: "many"`? Show it live.
6. Which error class should the replay buffer raise on a bad argument, and which should the store raise?
7. Somesh: why `field(default_factory=dict)` instead of `= {}`?
8. Did CI block at least one broken PR this week? What did we learn?

---

## SECTION 13 — WEEK COMPLETION CHECKLIST

- [ ] All assigned tasks completed
- [ ] Code pushed to feature branches
- [ ] Pull requests reviewed (named reviewers)
- [ ] Tests passed locally and in CI
- [ ] Modules integrated (imports between members' modules work)
- [ ] Documentation updated (README dev setup, CONTRIBUTING)
- [ ] Weekly demonstration completed (fresh clone → pytest → random episode)
- [ ] Blockers recorded

---

## SECTION 14 — NEXT WEEK HANDOFF

- **Ready before Week 4:** `RunConfig`, `make_env`, `Agent`, `Transition`, `set_global_seed`, `episode_seed`, errors, logging — all merged and green.
- **Week-4 dependencies:** the runner (Brahmanand) uses `RunConfig`, `make_env`, `end_reason`, `save_config`, `get_logger`; Q-learning and DQN implement `Agent`; the replay buffer (Vedant) is used inside the DQN (Atharv) — Vedant must merge it by Week-4 Day 3.
- **Coordination:** Brahmanand and Atharv agree on Day 1 of Week 4 that `build_agent(cfg, env)` lives in `agent/runner.py` and imports the DQN lazily (so FrozenLake runs do not need PyTorch).
- **Risks:** PyTorch import failures on one laptop (that member runs DQN tests in CI or Colab); flaky tests due to shared folders (always use `tmp_path`).
