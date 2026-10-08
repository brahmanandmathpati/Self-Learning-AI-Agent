# WEEK 01 — Project Discovery and Requirements

**Project:** Self-Learning AI Agent · **Team:** Brahmanand Mathpati, Atharv Gundale, Vedant Biradar, Somesh Badwane
**Source:** *Self_Learning_AI_Agent_10_Week_Master_Plan* (v1.0) · **Budget:** ₹0 software (laptops and internet assumed)

> How to use this file: read Sections 1–2 together on Day 1 (30 minutes). Then each member jumps to their own part of Section 4 and follows the daily plan in Section 3. Code and file contents are in Section 5.

---

## SECTION 1 — WEEK OVERVIEW

| Item | Details |
|---|---|
| Week number | 1 of 10 |
| Week title | Project Discovery and Requirements |
| Main objective | Agree exactly what we will build, check every laptop, install the tools and set up a GitHub workflow everyone can use. |
| Expected outcome | A written, testable requirements list; MVP vs optional features; a working GitHub repository with branch protection; every member has opened at least one pull request (PR); a hardware audit of all 4 laptops. |
| Required knowledge | None in advance. This week teaches: what reinforcement learning (RL) is, what "self-learning" means in this project, basic Git and GitHub. |
| Required tools | Python 3.10–3.12, VS Code (+ Python extension), Git, a free GitHub account, a web browser. |
| Prerequisites from previous weeks | None — this is the first week. |
| Approximate workload | 11 hours per member (44 team-hours). Day 1–5: ~1.5 h/day · Day 6: ~2.5 h · Day 7: 1 h review. |
| Technical dependencies | Atharv must create the repository on Day 1 before others can push. Brahmanand's requirement IDs (Day 3) are used by Vedant's NFR document. |
| Definition of Done | (1) `docs/requirements.md` merged, every requirement has a verification method; (2) all 4 members merged one PR; (3) `docs/hardware_audit.md` lists 4 laptops; (4) `main` is protected (no direct pushes); (5) Week-1 review meeting held and notes saved. |

**In simple words:** before writing any AI code, we decide *what success looks like* and make sure everyone's laptop and GitHub account work. A team that skips this week usually wastes weeks 3–5 on "it works on my laptop" problems and arguments about scope.

### The project in one paragraph (memorise this)
Our agent starts with **zero knowledge** of a task. It repeatedly tries the task in a simulated environment (FrozenLake-v1, then CartPole-v1), gets a **reward** after every step, and **updates a Q-table or neural-network weights** so it does better next time. We prove learning by evaluating a **frozen** copy of the trained agent (no exploration, no updates) on **fixed test seeds**, across **5 training seeds**, and comparing it with a random agent and with its own untrained state. A chatbot, stored chat history or changed prompts do **not** count as learning.

---

## SECTION 2 — WHAT WE ARE BUILDING THIS WEEK

1. **What we develop:** not code yet — the *foundation*: requirements, scope, team workflow, repository, laptop audit. Somesh writes the project's first Python script (`scripts/hardware_check.py`).
2. **Why it is necessary:** examiners ask "what exactly did you promise and did you deliver it?". Numbered requirements (REQ-01, REQ-02, …) each with a test let us answer that with evidence in Week 8.
3. **How it connects to the full agent:** every later module (environment, agent, memory, evaluation, UI) is built to satisfy a REQ from this week. The hardware audit decides whether the optional local LLM (Ollama) is possible.
4. **What happens if this is missing:** scope creep (people start building chatbots or LunarLander), untestable claims ("it learns well"), merge chaos on `main`, and laptops that cannot install PyTorch discovered in Week 4.
5. **Final output of the week:** a GitHub repository like this, with 4 merged PRs and a filled task board:

```text
self-learning-ai-agent/
├── .github/PULL_REQUEST_TEMPLATE.md
├── docs/ requirements.md, use_cases.md, nfr.md, feasibility.md, learning_plans.md, hardware_audit.md, ...
├── scripts/hardware_check.py
├── .gitignore  .env.example  README.md
```

**Analogy:** building a house. This week we draw the plan, check the land and buy the tools. Nobody lays bricks before the plan is signed.

### What "Reinforcement Learning" means (5-minute explanation for everyone)
- **Agent:** the learner (our program).
- **Environment:** the world it acts in (e.g. FrozenLake: a 4×4 frozen lake with holes).
- **State:** what the agent sees now (e.g. "I am on square 6").
- **Action:** what it can do (left, down, right, up).
- **Reward:** a number after each action (FrozenLake: +1 for reaching the goal, 0 otherwise).
- **Policy:** the agent's rule for choosing actions.
- **Learning:** changing the policy so that total reward goes up over many attempts (episodes).

---

## SECTION 3 — DAILY EXECUTION PLAN

> Times are per member. "Async" = do it alone at your own time; "Sync" = together (call or in person).

### Day 1 — Kick-off and repository (1.5 h)
- **Daily objective:** everyone understands the project; repository exists.
- **Assigned members:** all (sync 45 min), then Atharv (repo), others (install tools).
- **Individual tasks:**
  - All: read Sections 1–2 and the Notion page together; agree the one-paragraph description above.
  - Atharv: SLA-01-AG-1 steps 1–4 (create repo, protect `main`, add collaborators).
  - Brahmanand, Vedant, Somesh: install Python, Git, VS Code (Section 5.1); create a GitHub account if needed and send the username to Atharv.
- **Detailed execution procedure:** Section 5.1 (installs) and Section 4 → SLA-01-AG-1.
- **Required commands:**
  ```bash
  python --version     # Mac/Linux: python3 --version   -> 3.10, 3.11 or 3.12
  git --version
  git config --global user.name "Your Name"
  git config --global user.email "you@example.com"
  ```
- **Expected files:** none locally yet; the GitHub repo `self-learning-ai-agent` exists online.
- **Expected output:** each member has accepted the GitHub invitation.
- **Testing steps:** each member opens the repo URL in a browser and can see it.
- **GitHub activity:** Atharv creates repo + labels + project board.
- **Completion checklist:** - [ ] all tools installed · - [ ] all invitations accepted

### Day 2 — First clone, first branch, first PR (1.5 h)
- **Daily objective:** everyone can clone, branch, commit, push and open a PR.
- **Assigned members:** all; Atharv runs a 30-min Git session (SLA-01-AG-1 step 6).
- **Individual tasks:** each member adds their name and role to `docs/team.md` through their own PR (practice PR). Somesh starts Python basics (Section 5.6).
- **Required commands:**
  ```bash
  git clone https://github.com/<team-account>/self-learning-ai-agent.git
  cd self-learning-ai-agent
  git checkout -b docs/<yourname>-11-team-entry
  # edit docs/team.md in VS Code, then:
  git add docs/team.md
  git commit -m "docs(team): add <yourname> to team list"
  git push -u origin docs/<yourname>-11-team-entry
  ```
- **Expected files:** `docs/team.md` (one line per member).
- **Expected output:** 4 open PRs; Atharv reviews and merges them one by one.
- **Testing steps:** after merging, everyone runs `git checkout main && git pull` and sees all 4 names.
- **GitHub activity:** 4 PRs, 4 reviews, 4 merges. The 2nd–4th PR may hit a **merge conflict** on `docs/team.md` — good practice; fix it with Section 7.
- **Completion checklist:** - [ ] my PR merged · - [ ] I resolved or watched a conflict being resolved

### Day 3 — Requirements and use cases (1.5 h)
- **Daily objective:** first draft of requirements and use cases.
- **Assigned members:** Brahmanand (requirements), Vedant (use cases), Atharv (feasibility), Somesh (hardware script start).
- **Individual tasks:** SLA-01-BM-1 steps 1–3 · SLA-01-VB-1 steps 1–2 · SLA-01-AG-2 steps 1–2 · SLA-01-SB-1 steps 1–4.
- **Expected files:** `docs/requirements.md` (draft), `docs/use_cases.md` (draft), `docs/feasibility.md` (draft), `scripts/hardware_check.py` (first version).
- **Expected output:** drafts pushed to feature branches (not merged yet).
- **Testing steps:** Brahmanand checks every REQ has a "Verification" column filled.
- **GitHub activity:** draft PRs opened (mark as "Draft" on GitHub).
- **Completion checklist:** - [ ] drafts pushed

### Day 4 — Non-functional requirements, MVP scope, learning plans (1.5 h)
- **Daily objective:** NFRs measurable; MVP vs optional list agreed; learning plans written.
- **Assigned members:** Vedant (NFRs), Brahmanand (MVP list), Atharv (Python assessment + learning plans), Somesh (finish script, run it).
- **Individual tasks:** SLA-01-VB-1 steps 3–5 · SLA-01-BM-1 steps 4–6 · SLA-01-AG-2 steps 3–5 · SLA-01-SB-1 steps 5–8.
- **Required commands (Somesh):** `pip install psutil` then `python scripts/hardware_check.py --name somesh`.
- **Expected files:** `docs/nfr.md`, `docs/learning_plans.md`, `hardware_somesh.json` (local only, git-ignored).
- **Expected output:** script prints laptop details without error.
- **Testing steps:** Somesh runs the script twice; output identical. Atharv reviews the script.
- **GitHub activity:** Somesh opens his PR "Add hardware audit script".
- **Completion checklist:** - [ ] NFR table has numbers · - [ ] script reviewed

### Day 5 — Hardware audit on all laptops, Q-learning by hand (1.5 h)
- **Daily objective:** all 4 laptops audited; everyone understands one Q-learning update.
- **Assigned members:** all run Somesh's script; Brahmanand writes the worked example; Atharv explains it (20 min sync).
- **Individual tasks:** SLA-01-SB-1 step 9 (collect results into `docs/hardware_audit.md`) · SLA-01-BM-2.
- **Required commands (everyone):**
  ```bash
  git checkout main && git pull
  pip install psutil
  python scripts/hardware_check.py --name <yourname>
  ```
  Send your printed output to Somesh in the team chat.
- **Expected files:** `docs/hardware_audit.md`, `docs/notes/q_learning_by_hand.md`.
- **Expected output:** a 4-row hardware table; a 3-step worked Q-learning example.
- **Testing steps:** compare each laptop with the minimum (4 cores, 8 GB RAM, 5 GB disk). Any laptop below → note it as a risk (it can still run the MVP, see master plan §5.2).
- **GitHub activity:** 2 PRs (hardware audit, worked example).
- **Completion checklist:** - [ ] 4 laptops audited · - [ ] everyone can explain the Q-update in one sentence

### Day 6 — Finalise and merge (2.5 h)
- **Daily objective:** all Week-1 documents final and merged; synopsis outline started.
- **Assigned members:** all.
- **Individual tasks:** address review comments; Brahmanand writes `docs/synopsis_outline.md` (SLA-01-BM-1 step 7); Atharv sets up the project board columns and creates Week-2 issues (Section 7).
- **Expected files:** all Week-1 files listed in Section 11.
- **Expected output:** every Week-1 PR merged; board shows Week-2 issues in "Not Started".
- **Testing steps:** `git checkout main && git pull` → check every file in Section 6 exists.
- **GitHub activity:** reviews and merges.
- **Completion checklist:** - [ ] no open Week-1 PRs (except intentionally postponed)

### Day 7 — Weekly review (1 h, sync)
- **Daily objective:** demonstrate, review and plan Week 2.
- **Assigned members:** all; Atharv chairs (integration captain W1).
- **Individual tasks:** run the agenda in Section 12; tick Section 13; record blockers in `PROJECT_PROGRESS_TRACKER.md`.
- **Expected output:** meeting notes saved as `docs/meetings/week01.md`.
- **Completion checklist:** - [ ] Section 13 complete

---

## SECTION 4 — INDIVIDUAL MEMBER TASKS

### Brahmanand Mathpati

**Task ID:** SLA-01-BM-1
**Task Title:** Requirements document and MVP scope
**Priority:** P1 (must have)
**Estimated Duration:** 6 h (learning 1, writing 4, review 1)
**Dependencies:** Notion page; Day-1 kick-off
**Assigned Member:** Brahmanand Mathpati

1. **What exactly to build:** `docs/requirements.md` — numbered functional requirements (REQ-01 …) and the MVP vs optional feature list; plus `docs/synopsis_outline.md`.
2. **Why it is needed:** every test in Week 8 must point to a requirement; the examiner checks promises against delivery.
3. **Which file:** create `docs/requirements.md`, `docs/synopsis_outline.md`.
4. **Function/class:** none (documentation task).
5. **Inputs:** Notion page sections FR1–FR5 and NFR table; master plan §2.
6. **Outputs:** a Markdown table: ID · Requirement · Priority (MVP/Optional) · Verification method · Planned test ID · Owner.
7. **Step-by-step procedure:**
   1. Copy the template in Section 5.2 into `docs/requirements.md`.
   2. Fill one row per requirement; split vague ones ("agent learns") into measurable ones ("frozen-policy mean return on test seeds is higher than random, Welch p < 0.05").
   3. For each row write the *verification method* (unit test, integration test, experiment, demo, review).
   4. Write the MVP vs optional table (Section 5.2 part B).
   5. Check every MVP row has an owner.
   6. Ask Vedant to reference your REQ IDs in `docs/use_cases.md`.
   7. Create `docs/synopsis_outline.md` with the 25 synopsis headings (from the synopsis file) and one bullet each.
8. **Commands:**
   ```bash
   git checkout main && git pull
   git checkout -b docs/brahmanand-12-requirements
   git add docs/requirements.md docs/synopsis_outline.md
   git commit -m "docs(requirements): add numbered requirements and MVP scope"
   git push -u origin docs/brahmanand-12-requirements
   ```
9. **Tests to write:** none (document). Peer check instead: Vedant tries to write a test idea for 3 random REQs; if he cannot, the REQ is too vague.
10. **Expected result:** ≥ 15 REQs; each has a verification method and planned test ID.
11. **Common errors and fixes:** vague words ("fast", "good") → replace with numbers; REQs about optional features marked MVP → move to optional.
12. **Branch:** `docs/brahmanand-12-requirements`
13. **Commit message:** `docs(requirements): add numbered requirements and MVP scope`
14. **PR title:** `docs: requirements and MVP scope (SLA-01-BM-1)`
15. **Acceptance criteria:** every REQ has a verification method; scope approved by all 4 at the Day-7 review; reviewer: Atharv.

**Task ID:** SLA-01-BM-2
**Task Title:** Hand-computed Q-learning example
**Priority:** P2
**Estimated Duration:** 5 h (learning 2, writing 1, reviewing teammates' Week-1 PRs 2)
**Dependencies:** none
**Assigned Member:** Brahmanand Mathpati

1. **What:** `docs/notes/q_learning_by_hand.md` with three Q-learning updates computed by hand on a 2-state example.
2. **Why:** in Week 4 your unit test `test_update_matches_hand_calculation` checks the code against these exact numbers.
3. **File:** create `docs/notes/q_learning_by_hand.md`.
4. **Function/class:** none yet (the code arrives in Week 4: `q_learning_update`).
5. **Inputs:** the formula `Q(s,a) ← Q(s,a) + α [r + γ·max Q(s′,·) − Q(s,a)]`.
6. **Outputs:** a table with each step's numbers (Section 5.3).
7. **Steps:** copy Section 5.3, redo every number yourself with a calculator, add one more update of your own.
8. **Commands:** branch `docs/brahmanand-13-q-learning-by-hand`, commit, push, PR (same pattern as above).
9. **Tests:** Atharv checks the arithmetic.
10. **Expected result:** all three updates correct; explanation in your own words.
11. **Common errors:** forgetting that a *terminal* step has no `γ·max Q(s′)` term.
12. **Branch:** `docs/brahmanand-13-q-learning-by-hand`
13. **Commit:** `docs(notes): add hand-computed Q-learning example`
14. **PR title:** `docs: Q-learning worked example (SLA-01-BM-2)`
15. **Acceptance:** numbers verified by Atharv; Brahmanand explains it at the Day-7 review.

### Atharv Gundale

**Task ID:** SLA-01-AG-1
**Task Title:** Repository, branch protection, labels, board and PR template
**Priority:** P1
**Estimated Duration:** 5 h (setup 2, Git session 1, reviews 2)
**Dependencies:** GitHub usernames from all members
**Assigned Member:** Atharv Gundale

1. **What:** the GitHub repository `self-learning-ai-agent` with `README.md`, `.gitignore`, `.env.example`, `.github/PULL_REQUEST_TEMPLATE.md`, labels, milestones W1–W10 and a project board.
2. **Why:** a protected `main` and a PR template stop broken code from reaching everyone.
3. **Files:** create the four files in Section 5.4.
4. **Function/class:** none.
5. **Inputs:** members' GitHub usernames.
6. **Outputs:** repo URL; 3 collaborators added; `main` protected.
7. **Steps:**
   1. GitHub → New repository → name `self-learning-ai-agent`, Public (or Private), add README, MIT licence.
   2. Settings → Collaborators → add Brahmanand, Vedant, Somesh (Write access).
   3. Settings → Branches → Add branch ruleset for `main`: require a pull request, require 1 approval, block force pushes. (Status checks are added in Week 3 when CI exists.)
   4. Issues → Labels: create `week-1` … `week-10`, `agent`, `learning`, `memory`, `evaluation`, `ui`, `docs`, `bug`, `P1`, `P2`, `blocked`.
   5. Issues → Milestones: `W1 — Requirements` … `W10 — Release v1.0` with Friday due dates.
   6. Projects → New project (Board) → columns: Not Started · In Progress · Blocked · In Review · Completed.
   7. Commit the files from Section 5.4 through a PR (yes, even you use a PR).
   8. Run a 30-minute Git session on Day 2: clone → branch → commit → push → PR → review → merge.
8. **Commands:**
   ```bash
   git clone https://github.com/<team-account>/self-learning-ai-agent.git
   cd self-learning-ai-agent
   git checkout -b chore/atharv-11-repo-setup
   # create .gitignore, .env.example, .github/PULL_REQUEST_TEMPLATE.md (Section 5.4)
   git add .gitignore .env.example .github/PULL_REQUEST_TEMPLATE.md README.md
   git commit -m "chore(repo): add gitignore, env example and PR template"
   git push -u origin chore/atharv-11-repo-setup
   ```
9. **Tests:** try `git push origin main` directly from a test commit — GitHub must reject it.
10. **Expected result:** direct push rejected with "protected branch" message.
11. **Common errors:** collaborators not accepting the invite (check spam); ruleset not targeting `main` (check "Target branches").
12. **Branch:** `chore/atharv-11-repo-setup`
13. **Commit:** `chore(repo): add gitignore, env example and PR template`
14. **PR title:** `chore: repository setup (SLA-01-AG-1)`
15. **Acceptance:** all 4 members opened a PR; direct pushes to `main` are blocked; reviewer: Brahmanand.

**Task ID:** SLA-01-AG-2
**Task Title:** Zero-cost feasibility note, Python assessment and learning plans
**Priority:** P1
**Estimated Duration:** 6 h (learning/research 2, writing 2, mentoring Somesh 1, review 1)
**Dependencies:** SLA-01-AG-1
**Assigned Member:** Atharv Gundale

1. **What:** `docs/feasibility.md` (RL-first design, each tool with licence and ₹0 cost) and `docs/learning_plans.md` (one plan per member, based on a short Python assessment).
2. **Why:** proves the ₹0 claim early; makes sure Somesh is taught alongside his tasks rather than left behind.
3. **Files:** `docs/feasibility.md`, `docs/learning_plans.md`.
4. **Function/class:** none.
5. **Inputs:** master plan §4 (learning plan) and §5 (stack and licences).
6. **Outputs:** two Markdown files (templates in Section 5.5).
7. **Steps:**
   1. Copy the stack table from the master plan §5 into `docs/feasibility.md`; add a column "Verified on (date)".
   2. Write the 10-question Python assessment (Section 5.5) and ask each member to answer it alone (20 min, no internet).
   3. Score it; write each member's learning plan (topics, week, practice task, proof).
   4. 1-hour setup session with Somesh: install Python + VS Code + Git, create venv, run `hello.py`, explain the terminal.
   5. Record assumptions: ₹0 = software only.
8. **Commands:** branch `docs/atharv-14-feasibility`, then add, commit, push, PR.
9. **Tests:** every tool row has a licence and source link.
10. **Expected result:** feasibility note approved; 4 learning plans.
11. **Common errors:** listing tools we will not use (keep the list minimal); forgetting model licences (Qwen2.5-3B is non-commercial; we use 1.5B, Apache-2.0).
12. **Branch:** `docs/atharv-14-feasibility`
13. **Commit:** `docs(feasibility): add zero-cost stack and learning plans`
14. **PR title:** `docs: feasibility and learning plans (SLA-01-AG-2)`
15. **Acceptance:** every tool has licence + ₹0 cost; each member agrees with their plan; reviewer: Brahmanand.

### Vedant Biradar

**Task ID:** SLA-01-VB-1
**Task Title:** Use cases, non-functional requirements and evaluation questions
**Priority:** P1
**Estimated Duration:** 11 h (research 3, writing 5, review/integration 3)
**Dependencies:** REQ IDs from SLA-01-BM-1 (Day 3)
**Assigned Member:** Vedant Biradar

1. **What:** `docs/use_cases.md` (4 use cases) and `docs/nfr.md` (measurable non-functional requirements + evaluation questions).
2. **Why:** NFRs become our performance and reliability tests in Week 8; evaluation questions shape the Week-6 protocol you own.
3. **Files:** `docs/use_cases.md`, `docs/nfr.md`.
4. **Function/class:** none.
5. **Inputs:** Notion NFR table; Brahmanand's REQ list.
6. **Outputs:** templates in Section 5.2 part C and D.
7. **Steps:**
   1. Write 4 use cases: UC-1 train an agent; UC-2 view proof of learning; UC-3 read the explanation; UC-4 rate the explanation. Each: actor, trigger, steps, result, related REQs.
   2. NFR table: Category · Requirement · Measure (number + unit) · How measured · Week tested.
   3. List the evaluation questions (Section 5.2 part D).
   4. Read: experience replay sections of Lin (1992) and Mnih et al. (2015); write 5 bullet notes in `docs/nfr.md` "Background".
   5. Cross-check with Brahmanand that every NFR has a REQ or vice versa.
8. **Commands:** branch `docs/vedant-15-use-cases-nfr`, add, commit, push, PR.
9. **Tests:** each NFR has a number and a measurement method (peer check by Atharv).
10. **Expected result:** 4 use cases, ≥ 8 NFRs, ≥ 5 evaluation questions.
11. **Common errors:** NFRs without numbers ("should be fast") — write "training of 500 CartPole episodes finishes in under 60 minutes on the weakest laptop".
12. **Branch:** `docs/vedant-15-use-cases-nfr`
13. **Commit:** `docs(nfr): add use cases and measurable non-functional requirements`
14. **PR title:** `docs: use cases and NFRs (SLA-01-VB-1)`
15. **Acceptance:** all NFRs measurable; use cases map to REQ IDs; reviewer: Atharv.

### Somesh Badwane

**Task ID:** SLA-01-SB-1
**Task Title:** Hardware audit script — your first Python program
**Priority:** P1
**Estimated Duration:** 11 h (learning 5, coding 3, testing 1, review 1, documentation 1)
**Dependencies:** repository from SLA-01-AG-1 (Day 1); Python installed
**Assigned Member:** Somesh Badwane

**0. Learn first (prerequisite concepts, ~5 h spread over Days 1–4):** Section 5.6 teaches, with tiny examples: variables and data types, `print` and f-strings, `if/else`, functions, dictionaries, importing modules, running a script from the terminal. Do every mini-exercise there before starting step 3 below.

1. **What exactly to build:** `scripts/hardware_check.py`, a script that prints and saves your laptop's OS, Python version, CPU cores, RAM, free disk and whether an NVIDIA GPU tool is present, and warns if the laptop is below the project minimum. Then `docs/hardware_audit.md` with a table for all 4 laptops.
2. **Why it is needed:** the team must know before Week 4 whether every laptop can train the DQN and whether the optional local LLM is possible.
3. **Files:** create `scripts/hardware_check.py` and `docs/hardware_audit.md`.
4. **Functions to implement:** `bytes_to_gb(num_bytes)`, `total_ram_gb()`, `collect_info()`, `check_minimum(info)`, `main()`.
5. **Inputs:** a `--name` argument typed in the terminal (e.g. `--name somesh`).
6. **Outputs:** printed lines and a file `hardware_<name>.json` (this file is git-ignored — it stays on your laptop).
7. **Step-by-step procedure:**
   1. Finish the Section 5.6 exercises.
   2. In VS Code: File → Open Folder → `self-learning-ai-agent`.
   3. Create the folder `scripts` and the file `scripts/hardware_check.py`.
   4. Type the code from Section 5.7 **by hand** (do not copy-paste) — typing it teaches you the syntax. Read the line-by-line explanation under the code as you go.
   5. Install psutil: `pip install psutil` (it reads RAM size).
   6. Run `python scripts/hardware_check.py --name somesh`.
   7. Compare the output with your laptop's Settings → About page.
   8. Run it without psutil installed on someone else's laptop if possible: the RAM line should show `None` instead of crashing.
   9. Collect the 4 outputs from the team chat into `docs/hardware_audit.md` (template in Section 5.7).
8. **Commands:**
   ```bash
   git checkout main
   git pull
   git checkout -b feat/somesh-16-hardware-check
   pip install psutil
   python scripts/hardware_check.py --name somesh
   git add scripts/hardware_check.py docs/hardware_audit.md
   git commit -m "feat(scripts): add hardware audit script"
   git push -u origin feat/somesh-16-hardware-check
   ```
9. **Tests to write:** this week, manual tests (automated tests start next week): run the script on all 4 laptops; run with a wrong argument (`python scripts/hardware_check.py`) and check the friendly error "the following arguments are required: --name".
10. **Expected successful result:**
    ```text
                        os: Windows 11
            python_version: 3.11.9
              python_64bit: True
                 cpu_cores: 8
                    ram_gb: 15.7
              free_disk_gb: 120.4
     nvidia_gpu_tool_found: False
                  warnings: []

    Saved to hardware_somesh.json
    ```
    (Your numbers will differ.)
11. **Common errors and fixes:** see the table at the end of Section 5.7.
12. **GitHub branch name:** `feat/somesh-16-hardware-check`
13. **Suggested commit message:** `feat(scripts): add hardware audit script`
14. **Pull request title:** `feat: hardware audit script (SLA-01-SB-1)`
15. **Acceptance criteria:** runs without error on all 4 laptops; `docs/hardware_audit.md` has 4 rows; in the review, Somesh explains every line of the script to Atharv.

**How to create your pull request (step by step):** after `git push`, GitHub prints a link "Create a pull request for …" — open it (or go to the repo page and click the yellow **Compare & pull request** button). Title: as above. The description box already contains our template: fill "What", "Closes #16", tick the boxes you did. On the right: **Reviewers → Atharv**, **Assignees → yourself**, **Labels → week-1, P1**, **Milestone → W1**. Click **Create pull request**. When Atharv leaves comments, change the code on the same branch, then `git add`, `git commit -m "fix: address review comments"`, `git push` — the PR updates automatically.

**Independent practice exercise (30 min, not submitted):** add a function `cpu_name()` that returns `platform.processor()` and print it as an extra line. Then make the script print `OK — this laptop meets the minimum` in green-free plain text when `warnings` is empty.

---

## SECTION 5 — COMPLETE TECHNICAL IMPLEMENTATION

### 5.1 Installing the tools (everyone)

| Tool | Windows | Mac | Ubuntu |
|---|---|---|---|
| Python 3.11 or 3.12 | python.org/downloads → tick **"Add python.exe to PATH"** | python.org installer | `sudo apt install python3 python3-venv python3-pip` |
| Git | git-scm.com/downloads (defaults) | run `git --version` → install prompt | `sudo apt install git` |
| VS Code | code.visualstudio.com + Python extension (Microsoft) | same | same |

Why Python 3.11/3.12: PyTorch CPU wheels are reliably available for them; very new Python versions sometimes have no PyTorch build yet.

### 5.2 Requirements templates (Brahmanand, Vedant)

**Part A — `docs/requirements.md` (functional requirements, start with these and refine):**

```markdown
# Requirements — Self-Learning AI Agent

| ID | Requirement | Priority | Verification | Planned test | Owner |
|---|---|---|---|---|---|
| REQ-01 | Create seeded FrozenLake-v1 and CartPole-v1 environments; same seed gives identical observations | MVP | Unit test | T-01, test_envs.py | Brahmanand |
| REQ-02 | Reject unsupported environment names with a clear error | MVP | Unit test | T-02 | Brahmanand |
| REQ-03 | Load and validate run settings from a YAML file; invalid values give an error naming the key | MVP | Unit test | T-03, test_config.py | Somesh |
| REQ-04 | Random-action baseline agent | MVP | Unit test + experiment | test_agents.py | Brahmanand |
| REQ-05 | Tabular Q-learning agent whose update matches a hand calculation | MVP | Unit test | T-04 | Brahmanand |
| REQ-06 | Q-learning reaches the FrozenLake 4x4 (non-slippery) goal in greedy evaluation for 5 seeds (target) | MVP | Experiment | T-05 | Brahmanand |
| REQ-07 | Training loop stops at step, episode and wall-clock limits | MVP | Unit/integration test | T-06 | Brahmanand |
| REQ-08 | DQN with replay buffer and target network, written by the team in PyTorch | MVP | Unit tests | T-07, T-08 | Atharv |
| REQ-09 | Replay buffer: fixed capacity, overwrite oldest, seeded random sampling | MVP | Unit test | T-09 | Vedant |
| REQ-10 | Persist every run and episode in SQLite; data survives restart | MVP | Integration test | T-10, T-11 | Vedant |
| REQ-11 | Save checkpoints and resume training from the latest one | MVP | Integration test | T-13 | Brahmanand |
| REQ-12 | Evaluate a frozen policy (epsilon = 0, no updates) on fixed test seeds | MVP | Unit test | test_evaluate.py | Vedant |
| REQ-13 | Trained agent beats random agent across 5 seeds (Welch t-test, bootstrap CI) | MVP | Experiment | T-15, T-16 | Atharv |
| REQ-14 | Stop training on NaN/exploding values; keep best checkpoint; flag regressions | MVP | Unit test | T-17 | Atharv |
| REQ-15 | Validate every transition (finite numbers, valid action, reward in range) | MVP | Unit test | T-20 | Somesh |
| REQ-16 | Plot learning curves from stored episodes | MVP | Unit test | test_plots.py | Somesh |
| REQ-17 | Streamlit UI: start a run, view curves, read and rate notes | MVP | UI test + demo | T-21 | Somesh |
| REQ-18 | Plain-language note grounded in logged numbers; template fallback without any LLM | MVP | Unit test | T-18, T-19 | Vedant |
| REQ-19 | Local LLM (Ollama) explanation | Optional | Demo | — | Vedant |
| REQ-20 | Ablation: full vs no-replay vs no-target-network | MVP | Experiment | ablation.csv | Atharv |
| REQ-21 | Everything runs offline after install, ₹0 software | MVP | Clean install test | T-24 | Atharv |
```

**Part B — MVP vs optional (also in `docs/requirements.md`):**

```markdown
## Scope
| Minimum viable product (must ship) | Optional (only after MVP exit criteria pass) |
|---|---|
| FrozenLake + CartPole environments, random baseline | LunarLander-v3 |
| Tabular Q-learning, DQN + replay + target network | Double DQN, prioritised replay |
| SQLite store, checkpoints, resume | Hosted demo on Streamlit Community Cloud |
| Frozen-policy evaluation, 5 seeds, statistics, ablation | stable-baselines3 reference run |
| CLI + Streamlit UI, template explanation note | Local LLM (Ollama) note |
```

**Part C — `docs/use_cases.md` (one example, write UC-2…UC-4 the same way):**

```markdown
## UC-1 Train an agent
- **Actor:** student / examiner
- **Trigger:** clicks "Start training" in the UI or runs `sla train --config configs/frozenlake_q.yaml`
- **Steps:** 1) config validated 2) environment created with seed 3) agent trains for N episodes 4) episodes stored 5) checkpoints saved 6) final evaluation on test seeds
- **Result:** run id, final mean return ± std, learning-curve plot
- **Related requirements:** REQ-01, 03, 05, 07, 10, 11, 12, 17
```

**Part D — `docs/nfr.md` (start with these):**

```markdown
| Category | Requirement | Measure | How measured | Week |
|---|---|---|---|---|
| Reproducibility | Same seed and config give identical episode returns | 100% identical | test_runner.py::test_same_seed_same_returns | 4 |
| Compute | 600 CartPole DQN episodes on the weakest laptop | < 60 min, CPU only | scripts/measure_performance.py | 8 |
| Memory | Peak RAM during DQN training | < 2 GB | scripts/measure_performance.py | 8 |
| Offline | Train, evaluate, UI, template note with internet off | All work | T-24 | 9 |
| Cost | Software cost | ₹0 | docs/licences.md | 9 |
| Transparency | Every algorithm line explainable by its owner | Mock viva ≥ 8/10 | Week-10 mock viva | 10 |
| Honesty | Every reported number traceable to a run folder and git commit | 100% of table rows | results/manifest.csv | 8 |
| Reliability | Training resumes after a forced stop | Resumes at next episode | T-13 | 5 |

## Evaluation questions (Vedant owns the answers in Week 6)
1. Does the frozen trained policy score higher than the random agent on unseen test seeds?
2. Does it score higher than its own untrained version (checkpoint 0)?
3. Is the improvement consistent across 5 training seeds (confidence interval excludes 0)?
4. Does the improvement survive saving, closing the program and reloading?
5. Does removing the replay buffer or target network change the result (ablation)?
```

### 5.3 Q-learning by hand (Brahmanand) — `docs/notes/q_learning_by_hand.md`

```markdown
# Q-learning by hand

Update rule: Q(s,a) ← Q(s,a) + α · [ r + γ · max_a' Q(s',a') − Q(s,a) ]
If the step is terminal (the episode really ended): target = r (no γ·max term).

Setup: 2 states (0, 1), 2 actions (0, 1), α = 0.5, γ = 0.9.
Start: Q = [[0, 0], [0, 1.0]]   (row = state, column = action)

| Step | s | a | r | s' | terminal? | target | TD error = target − Q(s,a) | new Q(s,a) |
|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 1 | 0 | 1 | no  | 0 + 0.9 × max(0, 1.0) = 0.9 | 0.9 − 0 = 0.9 | 0 + 0.5 × 0.9 = 0.45 |
| 2 | 0 | 1 | 0 | 1 | no  | 0.9 | 0.9 − 0.45 = 0.45 | 0.45 + 0.5 × 0.45 = 0.675 |
| 3 | 1 | 0 | 1 | 0 | yes | 1 (terminal: no γ term) | 1 − 0 = 1 | 0 + 0.5 × 1 = 0.5 |

Q after step 3 = [[0, 0.675], [0.5, 1.0]]
In words: each update moves the old guess part of the way (α) towards "reward now + discounted best guess later".
```

### 5.4 Repository files (Atharv)

`.gitignore`
```text
# Python
__pycache__/
*.py[cod]
*.egg-info/
.venv/
venv/
.pytest_cache/
.ruff_cache/
.coverage
htmlcov/

# Secrets and local settings
.env

# Training outputs (large, machine-specific)
runs/
*.pt
*.npz
*.db
!results/**/*.db

# Hardware audit files (personal)
hardware_*.json

# Editors / OS
.vscode/
.idea/
.DS_Store
Thumbs.db

# Media (keep the final demo video out of git; attach it to the GitHub release)
*.mp4
```

`.env.example` — the project needs **no** API keys; this only documents optional local settings.
```text
# Copy this file to .env and change values if needed. Never commit .env.
# The project needs NO API keys. These are optional local settings.
SLA_DB=runs/episodes.db
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:1.5b
```

`.github/PULL_REQUEST_TEMPLATE.md`
```markdown
## What does this PR do?
<!-- One or two sentences. -->

Closes #<issue number>

## Why?
<!-- Which requirement / task ID (e.g. SLA-04-BM) does this complete? -->

## How was it tested?
- [ ] `pytest` passes locally
- [ ] `ruff check .` passes locally
- [ ] New tests added for new code
<!-- Paste the command output or a screenshot. For experiments, attach the plot. -->

## Checklist
- [ ] Only my own module's files changed (or the owner approved)
- [ ] README / docs updated if behaviour changed
- [ ] No secrets, large files, `runs/` or `.env` committed
```

`README.md` (Week-1 stub; Brahmanand expands it in Weeks 3, 5 and 9):

```markdown
# Self-Learning AI Agent
Final-year B.Tech CSE project: an agent that learns FrozenLake and CartPole from rewards
(tabular Q-learning and a Deep Q-Network), with proof of learning across 5 seeds.
Status: Week 1 — requirements. See docs/requirements.md.
```

### 5.5 Feasibility and learning plans (Atharv)

`docs/feasibility.md` must contain the stack table from master plan §5 (purpose · choice · licence · why) plus this statement: *"₹0 refers to software and services. It assumes the team already has laptops, electricity and internet access."*

10-question Python assessment (20 minutes, alone):
1. What does `print(type(3.0))` print? 2. Write a function `square(x)` that returns x². 3. Difference between a list and a tuple? 4. Get the value of key `"seed"` from `cfg = {"seed": 0}`. 5. Loop over `[1, 2, 3]` and print each doubled. 6. What does `try/except` do? 7. How do you read a text file? 8. What is a virtual environment for? 9. What is a class? 10. What does `git commit` do (vs `git push`)?

`docs/learning_plans.md` row format: Member · Score · Topics (week) · Practice task · Proof (merged PR/test).

### 5.6 Python basics for Somesh (do these before writing the script)

Create `practice/basics.py` on your laptop (do **not** commit the `practice/` folder) and run each block with `python practice/basics.py`.

```python
# 1. Variables and types: a variable is a labelled box holding a value.
name = "Somesh"          # str  (text)
cores = 8                # int  (whole number)
ram_gb = 15.7            # float (decimal number)
is_64bit = True          # bool (True or False)
print(name, cores, ram_gb, is_64bit)
print(type(ram_gb))      # <class 'float'>

# 2. f-strings: put variables inside text with {}.
print(f"{name} has {cores} CPU cores and {ram_gb} GB RAM")

# 3. if / else: run code only when a condition is True.
if ram_gb < 8:
    print("Warning: less than 8 GB RAM")
else:
    print("RAM is fine")

# 4. Functions: a named, reusable block. 'return' sends a value back.
def bytes_to_gb(num_bytes):
    return round(num_bytes / (1024 ** 3), 1)

print(bytes_to_gb(17_179_869_184))   # 16.0

# 5. Dictionaries: key -> value pairs (like a small table).
info = {"os": "Windows", "cpu_cores": 8}
info["ram_gb"] = 15.7                 # add a new key
for key, value in info.items():       # loop over pairs
    print(key, "=", value)

# 6. Lists: an ordered collection you can append to.
warnings = []
warnings.append("Fewer than 4 cores")
print(len(warnings), warnings)

# 7. Modules: code written by others that you import.
import platform
print(platform.system(), platform.python_version())
```

Mini-exercises (10 min each): (a) write `def is_enough_ram(gb): ...` returning True if gb ≥ 8; (b) make a dict for your phone (brand, storage_gb) and print it with an f-string; (c) create a list of 3 numbers and print their sum with `sum()`.

Free resources: the official Python tutorial (docs.python.org/3/tutorial) chapters 3–5; "Python for Everybody" (py4e.com) chapters 1–4.

### 5.7 `scripts/hardware_check.py` (Somesh)

```python
"""Hardware audit (owner: Somesh, Week 1).

Run:  python scripts/hardware_check.py --name somesh
It prints your laptop details and saves them to hardware_<name>.json.
"""

import argparse
import json
import os
import platform
import shutil
import sys


def bytes_to_gb(num_bytes):
    """Convert bytes to gigabytes, rounded to 1 decimal place."""
    return round(num_bytes / (1024 ** 3), 1)


def total_ram_gb():
    """Total RAM in GB, or None if psutil is not installed yet."""
    try:
        import psutil
    except ImportError:
        return None
    return bytes_to_gb(psutil.virtual_memory().total)


def collect_info():
    disk = shutil.disk_usage(os.path.abspath(os.sep))
    return {
        "os": f"{platform.system()} {platform.release()}",
        "python_version": platform.python_version(),
        "python_64bit": sys.maxsize > 2 ** 32,
        "cpu_cores": os.cpu_count(),
        "ram_gb": total_ram_gb(),
        "free_disk_gb": bytes_to_gb(disk.free),
        "nvidia_gpu_tool_found": shutil.which("nvidia-smi") is not None,
    }


def check_minimum(info):
    """Return a list of warnings when the laptop is below the project minimum."""
    warnings = []
    if info["cpu_cores"] is not None and info["cpu_cores"] < 4:
        warnings.append("Fewer than 4 CPU cores: training will be slower.")
    if info["ram_gb"] is not None and info["ram_gb"] < 8:
        warnings.append("Less than 8 GB RAM: skip the optional Ollama model.")
    if info["free_disk_gb"] < 5:
        warnings.append("Less than 5 GB free disk: free some space before installing.")
    if not info["python_64bit"]:
        warnings.append("Python is 32-bit: install 64-bit Python 3.10+.")
    return warnings


def main():
    parser = argparse.ArgumentParser(description="Print and save laptop details")
    parser.add_argument("--name", required=True, help="your first name, e.g. somesh")
    args = parser.parse_args()

    info = collect_info()
    info["warnings"] = check_minimum(info)
    for key, value in info.items():
        print(f"{key:>22}: {value}")

    file_name = f"hardware_{args.name.lower()}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2)
    print(f"\nSaved to {file_name}")


if __name__ == "__main__":
    main()
```

**Line-by-line explanation:**
- `import argparse, json, os, platform, shutil, sys` — standard-library modules (they come with Python): `argparse` reads `--name` from the terminal, `json` saves the file, `os`/`platform`/`shutil`/`sys` read system details.
- `def bytes_to_gb(num_bytes)` — RAM and disk are reported in bytes; dividing by 1024³ gives gigabytes; `round(..., 1)` keeps one decimal.
- `def total_ram_gb()` — `try: import psutil` … `except ImportError: return None`: if psutil is not installed, we return `None` instead of crashing. This pattern (try/except) is how robust programs handle missing pieces.
- `def collect_info()` — builds one dictionary with every detail. `shutil.disk_usage(os.path.abspath(os.sep))` measures the main drive; `sys.maxsize > 2**32` is True on 64-bit Python; `shutil.which("nvidia-smi")` checks if NVIDIA's tool exists (a hint that an NVIDIA GPU is present — we do **not** need a GPU).
- `def check_minimum(info)` — compares with the project minimum and collects warning sentences in a list.
- `def main()` — reads `--name`, collects info, prints each key aligned with `f"{key:>22}"` (right-aligned in 22 characters), and saves `hardware_<name>.json`.
- `if __name__ == "__main__": main()` — runs `main()` only when you run this file directly, not when another file imports it.

**`docs/hardware_audit.md` template:**

```markdown
# Hardware audit (Week 1)

| Member | OS | Python | 64-bit | CPU cores | RAM (GB) | Free disk (GB) | NVIDIA tool | Warnings |
|---|---|---|---|---|---|---|---|---|
| Brahmanand | | | | | | | | |
| Atharv | | | | | | | | |
| Vedant | | | | | | | | |
| Somesh | | | | | | | | |

**Decision:** weakest laptop = ____ ; local LLM benchmark in Week 2 will run on it.
```

**Somesh's troubleshooting table:**

| Error | Why | Fix |
|---|---|---|
| `'python' is not recognized` | Python not on PATH | Reinstall with "Add python.exe to PATH" ticked; open a new terminal |
| `ModuleNotFoundError: No module named 'psutil'` | psutil not installed | `pip install psutil` (or accept `ram_gb: None`) |
| `error: the following arguments are required: --name` | forgot the argument | `python scripts/hardware_check.py --name somesh` |
| `IndentationError` | mixed spaces/tabs | VS Code: bottom bar "Spaces: 4"; re-indent the block |
| `SyntaxError: invalid syntax` near `f"` | missing quote or bracket | check every `(` has a `)` and every `"` has a pair |

---

## SECTION 6 — PROJECT FOLDER STRUCTURE

Expected repository at the end of Week 1:

```text
self-learning-ai-agent/
├── .github/
│   └── PULL_REQUEST_TEMPLATE.md   [NEW · Atharv]
├── docs/
│   ├── notes/
│   │   └── q_learning_by_hand.md   [NEW · Brahmanand]
│   ├── feasibility.md   [NEW · Atharv]
│   ├── hardware_audit.md   [NEW · Somesh]
│   ├── learning_plans.md   [NEW · Atharv]
│   ├── nfr.md   [NEW · Vedant]
│   ├── requirements.md   [NEW · Brahmanand]
│   ├── synopsis_outline.md   [NEW · Brahmanand]
│   └── use_cases.md   [NEW · Vedant]
├── scripts/
│   └── hardware_check.py   [NEW · Somesh]
├── .env.example   [NEW · Atharv]
├── .gitignore   [NEW · Atharv]
└── README.md   [NEW · Atharv → Brahmanand]
```

Legend: [NEW] created this week · [MODIFIED] changed this week · no tag = carried over unchanged from an earlier week. `runs/` (training outputs) and `.venv/` exist on your laptop but are git-ignored, so they are not shown.

Also created this week (team list from Day 2): `docs/team.md` and meeting notes `docs/meetings/week01.md`.

---

## SECTION 7 — GITHUB COLLABORATION PROCEDURE

1. **Create a GitHub issue** (Issues → New): title = task title, body = acceptance criteria, e.g. *"SLA-01-SB-1 Hardware audit script — Acceptance: runs on 4 laptops; table has 4 rows."*
2. **Assign the issue** to the owner; add labels `week-1`, `P1`, milestone `W1`; move it to **In Progress** on the board.
3. **Create a feature branch** named `<type>/<member>-<issue#>-<short-name>`.
4. **Pull latest changes** first:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feat/somesh-16-hardware-check
   ```
5. **Implement** the task.
6. **Run tests** (from Week 2: `pytest`; this week: run your script/check your document).
7. **Stage:** `git add scripts/hardware_check.py docs/hardware_audit.md` (add files by name; avoid `git add .` until you trust your `.gitignore`).
8. **Commit:** `git commit -m "feat(scripts): add hardware audit script"`.
9. **Push:** `git push -u origin feat/somesh-16-hardware-check`.
10. **Open a pull request** to `main`; write `Closes #16` in the description so the issue closes on merge.
11. **Request code review** from the reviewer named in Section 4.
12. **Fix review comments** on the same branch; push again.
13. **Merge after approval** (Squash and merge), then delete the branch and update locally:
    ```bash
    git checkout main && git pull
    git branch -d feat/somesh-16-hardware-check
    ```

**Week-1 issues to create (Atharv, Day 1):** #11 Repository setup (AG) · #12 Requirements and MVP scope (BM) · #13 Q-learning by hand (BM) · #14 Feasibility and learning plans (AG) · #15 Use cases and NFRs (VB) · #16 Hardware audit script (SB) · #17 Hardware audit table (SB).

**Merge conflicts — what they are and how to fix them:** a conflict happens when two branches change the same lines of the same file (Day 2's `docs/team.md` will do this on purpose). Git marks the file:
```text
<<<<<<< HEAD
| Atharv | Technical lead |
=======
| Vedant | Memory & evaluation |
>>>>>>> docs/vedant-11-team-entry
```
Fix: keep both lines (delete the `<<<<<<<`, `=======`, `>>>>>>>` markers), then:
```bash
git checkout docs/vedant-11-team-entry
git pull origin main          # brings in the conflict
# edit the file in VS Code ("Accept Both Changes"), save
git add docs/team.md
git commit -m "fix: resolve merge conflict in team list"
git push
```
**Avoid conflicts:** one owner per file; pull `main` every morning; small PRs; never commit directly to `main` (it is blocked anyway).

---

## SECTION 8 — WEEKLY INTEGRATION PROCEDURE

| Item | This week |
|---|---|
| Modules to connect | Documents, not code: REQ IDs (Brahmanand) ↔ use cases/NFRs (Vedant) ↔ feasibility (Atharv) ↔ hardware audit (Somesh). |
| Integrator | Atharv (integration captain, Week 1). |
| Interfaces that must match | Every use case and NFR references valid REQ IDs; hardware table columns match `hardware_check.py` keys. |
| Tests that must pass | Manual: script runs on 4 laptops; every REQ has a verification method. |
| Detecting failures | A REQ ID mentioned in `use_cases.md` that does not exist in `requirements.md`; a laptop missing from the audit. |
| Debugging | Search: in VS Code press Ctrl+Shift+F, type `REQ-`, compare lists. |

**Integration checklist**
- [ ] All REQ IDs referenced elsewhere exist
- [ ] MVP list matches master plan §2
- [ ] Hardware table complete; weakest laptop identified
- [ ] All Week-1 PRs merged into `main`

---

## SECTION 9 — TESTING AND VALIDATION

- **Unit/integration tests:** none yet (first automated tests: Week 2, Somesh's `test_io_helpers.py`).
- **Input validation:** `hardware_check.py` refuses to run without `--name` (argparse handles it).
- **Error handling:** script runs even without psutil (RAM shows `None`).
- **Reproducibility check:** run the script twice; output must be identical.
- **Document validation:** reviewer checks each REQ is *measurable* and has a *verification method*.
- **RL evaluation rules (agree now, used from Week 6):** training and evaluation are separate; evaluation uses fixed seeds that training never uses; no learning during evaluation (epsilon = 0, no updates); compare trained vs untrained; record only actual measurements — targets are labelled "target".

---

## SECTION 10 — COMMON PROBLEMS AND SOLUTIONS

| Problem | Possible Cause | How to Check | Solution |
|---|---|---|---|
| `python` opens Microsoft Store (Windows) | App execution alias | Settings → Apps → Advanced app settings → App execution aliases | Turn off python.exe / python3.exe aliases |
| Push rejected: "protected branch" | Pushing to `main` | `git branch` shows `* main` | Create a feature branch; push it; open a PR |
| `Permission denied (publickey)` | Cloning with SSH URL without keys | URL starts with `git@` | Use the `https://` URL |
| Invitation link expired | Not accepted within 7 days | Repo shows 404 | Atharv re-sends the invite |
| Merge conflict in `docs/team.md` | Two PRs edited same lines | GitHub says "This branch has conflicts" | Section 7 conflict steps |
| `pip` not found | pip not on PATH | `python -m pip --version` | Use `python -m pip install ...` |
| Different results of hardware script on same laptop | Disk space changed | Compare `free_disk_gb` only | Normal; other values must match |

---

## SECTION 11 — WEEKLY DELIVERABLES

| Deliverable | Owner | File/Location | Verification | Status |
|---|---|---|---|---|
| Requirements + MVP scope | Brahmanand | `docs/requirements.md` | Every REQ has verification; approved at review | [ ] |
| Synopsis outline | Brahmanand | `docs/synopsis_outline.md` | 25 headings present | [ ] |
| Q-learning worked example | Brahmanand | `docs/notes/q_learning_by_hand.md` | Atharv verified numbers | [ ] |
| Repo, protection, labels, board, PR template | Atharv | GitHub + `.github/`, `.gitignore`, `.env.example` | Direct push to `main` rejected | [ ] |
| Feasibility + learning plans | Atharv | `docs/feasibility.md`, `docs/learning_plans.md` | Licence + ₹0 per tool; 4 plans | [ ] |
| Use cases + NFRs | Vedant | `docs/use_cases.md`, `docs/nfr.md` | NFRs measurable; mapped to REQs | [ ] |
| Hardware audit script | Somesh | `scripts/hardware_check.py` | Runs on 4 laptops | [ ] |
| Hardware audit table | Somesh | `docs/hardware_audit.md` | 4 rows filled | [ ] |
| Week-1 meeting notes | Atharv | `docs/meetings/week01.md` | Saved after Day 7 | [ ] |

---

## SECTION 12 — WEEKLY REVIEW MEETING

**Agenda (60 min):** 1) demo: each member shows their merged PR (5 min each) · 2) completed vs pending tasks · 3) blockers · 4) document quality · 5) GitHub status (open PRs, board) · 6) integration status (REQ cross-references) · 7) Week-2 dependencies and issue assignment.

**Review questions:**
1. Can each member state the project in one sentence, including what does *not* count as learning?
2. Which REQ is the hardest to verify, and how will we verify it?
3. Is any MVP item actually optional (or vice versa)?
4. Which laptop is weakest, and can it run PyTorch CPU and (optionally) Ollama?
5. Did every member open, update and merge a PR without help?
6. Can Brahmanand explain the terminal-step rule in the Q-update?
7. Which Week-2 task is blocked by something unfinished this week?
8. Somesh: explain what `try/except ImportError` does in your script.

---

## SECTION 13 — WEEK COMPLETION CHECKLIST

- [ ] All assigned tasks completed (SLA-01-BM-1/2, AG-1/2, VB-1, SB-1)
- [ ] Code and documents pushed to feature branches
- [ ] Pull requests reviewed and merged
- [ ] Hardware script tested on all 4 laptops
- [ ] Documents cross-referenced (REQ IDs)
- [ ] `main` protected; project board set up; Week-2 issues created
- [ ] Weekly review held; notes saved
- [ ] Blockers recorded in `PROJECT_PROGRESS_TRACKER.md`

---

## SECTION 14 — NEXT WEEK HANDOFF

- **Must be ready before Week 2:** merged `docs/requirements.md`, `docs/nfr.md`, `docs/hardware_audit.md`; GitHub workflow working for all members.
- **Files Week 2 depends on:** `docs/requirements.md` (architecture must satisfy every MVP REQ); `docs/hardware_audit.md` (Atharv's LLM benchmark runs on the weakest laptop); `docs/learning_plans.md` (Somesh's Week-2 topics).
- **Coordination:** Brahmanand + Atharv + Vedant co-write `docs/design.md` (interfaces) in Week 2 — book a 1-hour call on Week-2 Day 2. Somesh needs the `src/sla/utils/` folder layout from Atharv on Week-2 Day 1.
- **Remaining technical risks:** a laptop below the minimum (mitigation: Colab fallback for long runs); members unfamiliar with Git (mitigation: Atharv pairs with them on the first Week-2 PR).
