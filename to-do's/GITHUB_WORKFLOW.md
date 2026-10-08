# GITHUB WORKFLOW — Self-Learning AI Agent

How the four of us use Git and GitHub for all 10 weeks. Every weekly handbook (Section 7) follows these rules. GitHub, GitHub Actions (free minutes on public repositories and the free plan), the `gh` CLI and Git are all free — **₹0**.

**Team:** Brahmanand Mathpati (BM) · Atharv Gundale (AG, repository admin) · Vedant Biradar (VB) · Somesh Badwane (SB)
**Repository:** `self-learning-ai-agent` · **Default branch:** `main` (protected)

---

## 1. Golden rules

1. **Nobody pushes to `main` directly.** All changes arrive through a pull request (PR) with at least one approving review and green CI.
2. **One issue → one branch → one PR.** Small PRs (ideally under ~300 changed lines) are reviewed faster and break less.
3. **Owners own modules.** Only the module owner changes a module's public functions (see `TEAM_RESPONSIBILITY_MATRIX.md`). Others open an issue or ask.
4. **Never rename modules or files** listed in the handbook. Later weeks import them by these exact names.
5. **Tests with code.** Every new function gets a test; tests never need internet or Ollama.
6. **Results are produced by scripts, never typed by hand.** A result PR states the command, commit and laptop.
7. **No secrets, no large files.** `.env`, `runs/`, `*.db`, `*.pt`, `*.npz`, `*.mp4` are git-ignored — check `git status` before `git add`.
8. **Never fake activity.** Do not create empty commits, back-date commits or inflate PR counts. The contribution record (Week 9–10) is generated from the real history.

---

## 2. One-time setup (Week 1, Atharv; everyone does step 3–4)

1. Create the repository; add `README.md`, `.gitignore`, `.env.example`, `.github/PULL_REQUEST_TEMPLATE.md` (Week-1 handbook, Section 5).
2. **Settings → Branches → Add rule for `main`:** require a pull request before merging · require 1 approval · dismiss stale approvals when new commits are pushed · require status checks to pass (`CI / test`, after Week 3) · do not allow bypassing.
3. Each member:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "the-email-on-your-github-account@example.com"   # same e-mail always
   git clone https://github.com/<org>/self-learning-ai-agent.git
   cd self-learning-ai-agent
   ```
4. Authenticate once: GitHub Desktop, Git Credential Manager, or `gh auth login` (all free).
5. **Labels:** `week-1` … `week-10`, `agent`, `learning`, `memory`, `evaluation`, `ui`, `docs`, `bug`, `P1`, `P2`, `blocked`.
6. **Milestones:** `W1` … `W10` (due date = Day 7 of each week), plus `v1.0`.
7. **Project board** columns: Backlog → This week → In progress → In review → Done.

---

## 3. Naming conventions

| Thing | Pattern | Example |
|---|---|---|
| Issue number | `week × 10 + sequence` (planned in each handbook's Section 7) | #42 = Week 4, item 2 |
| Branch | `<type>/<member>-<issue#>-<short-name>` | `feat/brahmanand-42-agent-runner` |
| Branch types | `feat` (feature) · `fix` (bug) · `test` · `docs` · `refactor` · `chore` · `exp` (experiment results) · `spike` (throw-away research) | `exp/atharv-81-final-experiments` |
| Commit message | Conventional Commits: `<type>(<scope>): <summary>` | `feat(memory): add SQLite episode store and store callback` |
| PR title | `<type>: <summary> (<Task ID>)` | `feat: SQLite episode store (SLA-05-VB-1)` |
| Task ID | `SLA-<week>-<member>-<n>` | `SLA-07-SB-2` |
| Tags | `w2-design-freeze`, `v0.8-experiments`, `v0.9-rc`, `v1.0` | — |

GitHub issue numbers are assigned automatically. If yours differ from the handbook's plan, keep the handbook's Task ID in the title and use the real number in branches and `Closes #…`.

---

## 4. The 13-step workflow (every task, every week)

| # | Step | Command / action |
|---|---|---|
| 1 | **Create the issue** | GitHub → Issues → New: title `<Task ID> <title>`, description = Section 4 items 1, 7, 15 from the handbook |
| 2 | **Assign** | assignee = owner; labels `week-N`, area, priority; milestone `WN`; board → *This week* |
| 3 | **Create the branch** | `git checkout main && git pull && git checkout -b feat/<member>-<issue#>-<name>` |
| 4 | **Pull the latest code** | `git pull` (on `main`) before branching; during long tasks: `git fetch origin && git rebase origin/main` |
| 5 | **Implement** | follow the handbook's Section 5 code and Section 4 steps |
| 6 | **Test locally** | `ruff check .` and `pytest` (or the narrower command in Section 4 item 8) |
| 7 | **Stage** | `git status` → `git add <specific files>` (avoid `git add .` unless you checked `git status`) |
| 8 | **Commit** | `git commit -m "feat(scope): summary"` — small, focused commits |
| 9 | **Push** | `git push -u origin <branch>` (first time), then `git push` |
| 10 | **Open the PR** | fill the template; `Closes #<issue>`; reviewer (handbook Section 7); labels; milestone; board → *In review* |
| 11 | **Review** | reviewer reads code + tests, runs them if unsure, comments within 24 h |
| 12 | **Fix comments** | change on the same branch → commit → push (PR updates automatically); reply to each comment |
| 13 | **Merge** | after approval + green CI: **Squash and merge**; delete the branch; board → *Done*; everyone `git pull` |

### The PR template (already in `.github/PULL_REQUEST_TEMPLATE.md`)
```markdown
## What does this PR do?
Closes #<issue number>
## Why?   (task ID)
## How was it tested?
- [ ] pytest passes locally   - [ ] ruff check . passes locally   - [ ] New tests added for new code
## Checklist
- [ ] Only my own module's files changed (or the owner approved)
- [ ] README / docs updated if behaviour changed
- [ ] No secrets, large files, runs/ or .env committed
```

---

## 5. Reviews

| Who reviews whom (default) | Weeks |
|---|---|
| Atharv reviews Somesh | 1–3 (then mentoring continues) |
| Vedant reviews Somesh | 4–10 |
| Brahmanand ↔ Atharv review each other's core code | all |
| Each handbook's Section 7 table names the reviewer per PR | — |

**Reviewer checklist:** does it do what the issue asks? · tests cover the new behaviour (including a bad input)? · names match the handbook (no renamed modules or functions)? · no unrelated changes? · clear errors (`SLAError` subclasses) and no `print` in library code? · for results: command, commit and laptop stated; numbers come from files?

**Kind, specific comments:** "Line 42: `int(state)` is needed because FrozenLake returns a NumPy int — see test X" beats "wrong". Approve when it is correct, not when it is perfect. Atharv guides — he does not rewrite other members' PRs.

---

## 6. Continuous integration (`.github/workflows/ci.yml`, Week 3)

Runs on every PR and every push to `main`: Python 3.11 → install PyTorch CPU + project → `ruff check .` → `pytest -m "not smoke" --cov=sla` → smoke tests (`pytest -m smoke`, allowed to be empty before Week 5). A red CI blocks merging. If CI fails:

1. Open the failed job → read the first red error.
2. Reproduce locally with the same command.
3. Fix on your branch and push. Never merge with a red CI "because it works on my laptop".

---

## 7. Keeping your branch up to date and solving conflicts

```bash
git checkout feat/<your-branch>
git fetch origin
git rebase origin/main            # replay your commits on top of the newest main
# conflict? open the file, keep the right lines, delete the <<<<<<< ======= >>>>>>> markers
git add <file> && git rebase --continue
pytest                            # always re-test after a rebase
git push --force-with-lease       # only on YOUR OWN branch, never on main
```
Beginners may use `git merge origin/main` instead of rebase — also fine (no force-push needed).

**Files that often conflict:** `tests/conftest.py` (one region per owner: W4 Brahmanand, W5 Vedant), `src/sla/cli.py` (only Brahmanand edits it), `README.md` (one PR at a time; Brahmanand coordinates). Binary files (`.docx`, `.pptx`, `.png`) cannot be merged — one owner edits each.

---

## 8. Dependencies between PRs

When your work needs someone else's unmerged PR (e.g. DQN needs the replay buffer):
1. Ask for the dependency to be merged first (each handbook marks these "**merge by Day N**").
2. Meanwhile, write your code against the agreed interface (`docs/design.md`).
3. After their merge: `git rebase origin/main`, run tests, push.
Do **not** copy their unmerged code into your branch.

---

## 9. Experiments, tags and releases

- **Experiment PRs (`exp/…`)** contain configs, result CSV/Markdown and notes — not code changes. The description states: command, `git rev-parse --short HEAD`, laptop (from `scripts/hardware_check.py`).
- **Tags:** `w2-design-freeze` (interfaces frozen) · `v0.8-experiments` (code that produced the final results) · `v0.9-rc` (release candidate) · `v1.0` (submission).
  ```bash
  git checkout main && git pull
  git tag -a v1.0 -m "Final submission"
  git push origin v1.0
  ```
- After `v0.8-experiments`, a change to training/evaluation code means affected experiments are **re-run** on a new tag.
- **Releases:** GitHub → Releases → Draft new release → choose tag → paste CHANGELOG section → `v0.9-rc` as pre-release, `v1.0` as full release with report PDF and slides attached.

---

## 10. Weekly rhythm

| Day | GitHub activity |
|---|---|
| Day 1 | Issues for the week created and assigned; board updated; dependencies agreed |
| Days 2–5 | Branches, PRs, reviews within 24 h; dependency PRs merged first |
| Day 6 | All PRs merged; `main` green; everyone pulls and runs `pytest` |
| Day 7 | Review meeting: demo from a fresh `git pull`; tick the week in `PROJECT_PROGRESS_TRACKER.md` |

---

## 11. Emergency fixes

| Situation | What to do |
|---|---|
| Committed a secret | Remove it, **rotate/revoke the secret** (we use none, but check), tell Atharv; rewriting history needs the whole team |
| Committed `runs/` or a large file | `git rm -r --cached runs && git commit -m "chore: untrack runs"`; check `.gitignore` |
| Broke `main` after a merge | Revert the PR on GitHub (**Revert** button) → new PR → fix properly on a branch |
| Lost local work | `git reflog` shows recent states; ask Atharv before any `reset --hard` |
| "detached HEAD" after checking out a tag | normal; `git checkout main` to return |
