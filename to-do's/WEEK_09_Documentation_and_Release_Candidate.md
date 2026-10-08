# WEEK 09 — Documentation and Release Candidate

**Project:** Self-Learning AI Agent · **Team:** Brahmanand Mathpati, Atharv Gundale, Vedant Biradar, Somesh Badwane
**Source:** *Self_Learning_AI_Agent_10_Week_Master_Plan* (v1.0) · **Interfaces:** `docs/design.md` (tag `w2-design-freeze`)

---

## SECTION 1 — WEEK OVERVIEW

| Item | Details |
|---|---|
| Week number | 9 of 10 |
| Week title | Documentation and Release Candidate |
| Main objective | Turn the working system and its results into a **complete, examinable package**: final README, module documentation, user guide, licences, contribution record, report chapters 1–6, slide draft, and a **release candidate** (`v0.9-rc`) proven to install and run on a clean machine **without internet after installation** and without Ollama. |
| Expected outcome | Tag `v0.9-rc` with a CHANGELOG; `docs/modules/*.md`, `docs/user_guide.md`, `docs/licences.md`, `docs/contributions.md`, `docs/clean_install_test.md`; report chapter drafts in `report/`; figures in `report/figures/`; `slides/draft.pptx`; screenshots in `docs/screenshots/`. |
| Required knowledge | The whole system; academic writing basics (claims need evidence, cite sources, state limitations); semantic versioning and Git tags; open-source licences (MIT, BSD, Apache-2.0). |
| Required tools | Free tools only: LibreOffice Writer/Impress (or the college's Word/PowerPoint, or Google Docs/Slides) for the report and slides; draw.io / diagrams.net (free) for diagrams; the `gh` CLI (free) or the GitHub website for the contribution record. **No new Python dependency.** |
| Prerequisites from previous weeks | Week 8 merged: everything in `results/`; tag `v0.8-experiments`; green CI. |
| Approximate workload | 11 h per member (mostly writing and review). |
| Technical dependencies | README and module docs merged by **Day 3** (user guide and report link to them). Clean-install test passed by **Day 5** (before tagging `v0.9-rc`). Report chapters exchanged for peer review on **Day 5**. |
| Definition of Done | `v0.9-rc` tagged on a commit where CI is green **and** the clean-install test passed; every number in the report chapters is copied from a file in `results/` (with the file named in the text or caption); every member's contribution record comes from real Git/GitHub data. |

**In simple words:** the code is finished. This week we explain it so well that an examiner — or a new student — can install it, run it and understand what we did and what we found, using only our documents.

**Version note:** the Python package version in `pyproject.toml` stays `0.1.0` (the first version of the package). The Git tags `v0.9-rc` and `v1.0` mark the project's milestones; the CHANGELOG explains both.

---

## SECTION 2 — WHAT WE ARE BUILDING THIS WEEK

1. **Documents:** final `README.md`, `docs/modules/agent.md`, report chapters 1–3 (Brahmanand) · `CHANGELOG.md`, `docs/licences.md`, `docs/clean_install_test.md`, `docs/modules/learning.md`, report chapter 4, tag `v0.9-rc` (Atharv) · report chapters 5–6, `docs/modules/memory_evaluation_reflection.md`, final diagrams (Vedant) · `docs/user_guide.md`, `docs/modules/ui.md`, `docs/contributions.md`, screenshots, `slides/draft.pptx` (Somesh).
2. **Why:** marks are given for the report, the viva and a reproducible demo — not only for code. Clear documents also prove each member understands their part.
3. **Connection:** Week 10 finalises the report and slides from these drafts and runs the final demo on `v1.0`.
4. **If missing:** examiners cannot verify results; the team cannot answer "how do I run it?"; a viva question on licences or limitations goes unanswered.
5. **Final output:**
   ```text
   $ git tag --list
   w2-design-freeze
   v0.8-experiments
   v0.9-rc
   $ ls docs/modules
   agent.md  learning.md  memory_evaluation_reflection.md  ui.md
   ```

**Analogy:** the code is the engine; this week we write the car's owner manual, the service record and the test-drive certificate.

### Report map (chapter → owner → source files)
```text
Ch 1 Introduction & problem        Brahmanand   docs/requirements.md, docs/synopsis_draft.md
Ch 2 Literature review             Brahmanand   docs/literature_review.md (Vedant, W2)
Ch 3 Requirements & feasibility    Brahmanand   docs/requirements.md, docs/nfr.md, docs/feasibility.md, docs/use_cases.md
Ch 4 Design & implementation       Atharv       docs/design.md, docs/architecture.md, docs/modules/*.md, src/
Ch 5 Testing & results             Vedant       results/*.md, results/*.csv, results/ablation/, docs/evaluation_protocol.md
Ch 6 Discussion, limitations,      Vedant       results/failure_analysis.md, results/reflection_eval.md, docs/notes/ablation_notes.md
     conclusion & future work
Appendices: user guide (Somesh), contributions (Somesh), licences (Atharv), test report (Vedant)
```

---

## SECTION 3 — DAILY EXECUTION PLAN

### Day 1 — Documentation plan and templates (1.5 h)
- **Daily objective:** everyone knows which document they own, the template, and the source files.
- **Assigned members:** all; Atharv integration captain (release week).
- **Individual tasks:** Brahmanand: report template (headings, fonts, figure/table numbering) in `docs/report_outline.md` (SLA-09-BM-2 step 1). Atharv: list dependencies and licences (SLA-09-AG-2 step 1). Vedant: list figures needed for chapters 5–6 (SLA-09-VB-1 step 1). Somesh: user-guide outline + start screenshots (SLA-09-SB-1 steps 1–2).
- **Required commands:**
  ```bash
  git checkout main && git pull && pytest -q
  pip list --format=freeze > installed_versions.txt      # for the licence list (not committed)
  ```
- **Expected files:** `docs/report_outline.md`.
- **GitHub activity:** issues #91–#99.
- **Completion checklist:** - [ ] owners and templates agreed

### Day 2 — README and module docs (1.5 h)
- **Daily objective:** each member documents their own modules.
- **Assigned members:** all (each writes one `docs/modules/*.md` — template Section 5.2).
- **Individual tasks:** SLA-09-BM-1 steps 1–3 · SLA-09-AG-2 step 2 · SLA-09-VB-2 · SLA-09-SB-1 step 3.
- **Expected files:** `README.md` (final), `docs/modules/*.md`.
- **Testing steps:** a teammate follows the README Quickstart on their laptop and notes every unclear step.
- **Completion checklist:** - [ ] 4 module docs drafted · - [ ] README reviewed by a teammate

### Day 3 — Merge docs; report chapters start (1.5 h)
- **Daily objective:** README + module docs merged; chapter drafting begins.
- **Assigned members:** all.
- **Individual tasks:** SLA-09-BM-2 step 2 (ch 1) · SLA-09-AG-3 step 1 (ch 4) · SLA-09-VB-1 step 2 (ch 5) · SLA-09-SB-2 (contributions record).
- **GitHub activity:** #91, #92 merged.
- **Completion checklist:** - [ ] docs merged

### Day 4 — Clean-install offline test; figures (1.5 h)
- **Daily objective:** prove the project installs and runs on a clean machine and works offline.
- **Assigned members:** Atharv leads; Somesh performs the test on his laptop (new user account or new folder) following only the README; Vedant produces final figures; Brahmanand writes ch 2–3.
- **Individual tasks:** SLA-09-AG-1 steps 1–4 · SLA-09-VB-1 step 3 · SLA-09-BM-2 step 3.
- **Required commands:** Section 5.3 procedure.
- **Expected output:** `docs/clean_install_test.md` filled with real results.
- **Completion checklist:** - [ ] clean-install test passed (or failures fixed and re-tested)

### Day 5 — Release candidate; peer review swap (1.5 h)
- **Daily objective:** tag `v0.9-rc`; every chapter reviewed by a different member.
- **Assigned members:** Atharv (CHANGELOG + tag), all (review swap: BM→AG's ch 4, AG→VB's ch 5–6, VB→BM's ch 1–3, SB reads the whole report as "a student who has never seen the project" and marks confusing sentences).
- **Individual tasks:** SLA-09-AG-1 steps 5–6.
- **Required commands:**
  ```bash
  git checkout main && git pull && pytest
  git tag -a v0.9-rc -m "Release candidate: code complete, docs drafted"
  git push origin v0.9-rc
  ```
- **GitHub activity:** GitHub Release (pre-release) created from `v0.9-rc` with CHANGELOG text.
- **Completion checklist:** - [ ] tag + pre-release · - [ ] review comments sent

### Day 6 — Fix review comments; slides draft (2.5 h)
- **Daily objective:** chapters revised; slide draft complete.
- **Assigned members:** all; Somesh leads slides with one slide input from each member.
- **Individual tasks:** SLA-09-SB-3 · everyone revises their chapter.
- **Expected files:** `report/chapters_1-3.docx`, `report/chapter_4.docx`, `report/chapters_5-6.docx`, `slides/draft.pptx`.
- **Completion checklist:** - [ ] chapters revised · - [ ] slides draft merged

### Day 7 — Weekly review (1 h)
- **Daily objective:** walk through the report and slide draft; practise 5 viva questions each; Section 12 agenda.
- **Completion checklist:** - [ ] Section 13 complete

---

## SECTION 4 — INDIVIDUAL MEMBER TASKS

### Brahmanand Mathpati

**Task ID:** SLA-09-BM-1
**Task Title:** Final README and agent module documentation
**Priority:** P1
**Estimated Duration:** 4 h (coding/doc examples 1, integration 1, docs 2)
**Dependencies:** all features merged; results files
**Assigned Member:** Brahmanand Mathpati

1. **What:** final `README.md`; `docs/modules/agent.md` (runner, callbacks, checkpoints, CLI, pipeline).
2. **Why:** README is the first thing examiners open; the module doc is the source for report chapter 4 and your viva answers.
3. **Files:** `README.md`, `docs/modules/agent.md`.
4. **Functions:** documents `run_training`, `Callback`, `CheckpointCallback`, `resume_training`, `train_and_evaluate`, `run_pipeline`, CLI commands.
5. **Inputs:** code, `results/final_table.md`.
6. **Outputs:** README with: what it is, quickstart, commands, project structure, results (link to `results/final_table.md` — copy numbers only from it), how to test, limitations, team, licence.
7. **Steps:** update README (Section 5.1) → write module doc (template Section 5.2) → teammate follows README on their laptop → fix unclear steps → PR #91.
8. **Commands:**
   ```bash
   git checkout -b docs/brahmanand-91-readme-final
   git add README.md docs/modules/agent.md
   git commit -m "docs: final README and agent module documentation"
   git push -u origin docs/brahmanand-91-readme-final
   ```
9. **Tests:** every command in README run once by a teammate on a clean venv.
10. **Expected result:** a teammate gets from clone to dashboard using only the README.
11. **Common errors:** README results that differ from `final_table.md`; outdated commands; broken relative links (check them on GitHub after pushing).
12. **Branch:** `docs/brahmanand-91-readme-final`
13. **Commit:** `docs: final README and agent module documentation`
14. **PR title:** `docs: final README + agent docs (SLA-09-BM-1)`
15. **Acceptance:** teammate test passed; reviewer: Somesh (fresh eyes).

**Task ID:** SLA-09-BM-2
**Task Title:** Report outline and chapters 1–3
**Priority:** P1
**Estimated Duration:** 7 h (docs 6, review 1)
**Dependencies:** Week-1/2 documents
**Assigned Member:** Brahmanand Mathpati

1. **What:** `docs/report_outline.md` (template + chapter map) and `report/chapters_1-3.docx`.
2. **Why:** introduction, literature and requirements set the examiner's expectations.
3. **Files:** as item 1.
4. **Functions:** —
5. **Inputs:** `docs/requirements.md`, `docs/literature_review.md`, `docs/nfr.md`, `docs/feasibility.md`, `docs/use_cases.md`, synopsis draft.
6. **Outputs:** chapter drafts with numbered figures/tables and references (consistent citation style, e.g. IEEE).
7. **Steps:** outline (Section 5.4) → chapter 1 → chapter 2 (summarise and cite sources from the literature review; never invent references) → chapter 3 → peer review by Vedant → revise.
8. **Commands:** `git checkout -b docs/brahmanand-93-report-ch1-3` · add · commit `docs(report): draft chapters 1-3` · push.
9. **Tests:** every reference exists and is cited in the text; every requirement in ch 3 has an ID matching `docs/requirements.md`.
10. **Expected result:** reviewed draft.
11. **Common errors:** copying text from papers (plagiarism — paraphrase and cite); claims without evidence.
12. **Branch:** `docs/brahmanand-93-report-ch1-3`
13. **Commit:** `docs(report): draft chapters 1-3`
14. **PR title:** `docs: report chapters 1–3 (SLA-09-BM-2)`
15. **Acceptance:** Vedant's review comments resolved; reviewer: Vedant.

### Atharv Gundale

**Task ID:** SLA-09-AG-1
**Task Title:** Release candidate `v0.9-rc`, CHANGELOG and clean-install offline test
**Priority:** P1
**Estimated Duration:** 5 h (testing 2, integration 2, docs 1)
**Dependencies:** README final (#91)
**Assigned Member:** Atharv Gundale (integration captain, Week 9)

1. **What:** `docs/clean_install_test.md` (procedure + real results), `CHANGELOG.md`, tag `v0.9-rc`, GitHub pre-release.
2. **Why:** proves the ₹0, offline-capable claim: after a one-time install, the core system needs no internet, no cloud and no LLM.
3. **Files:** `docs/clean_install_test.md`, `CHANGELOG.md`.
4. **Functions:** —
5. **Inputs:** README Quickstart.
6. **Outputs:** pass/fail per step with real timings; CHANGELOG; tag.
7. **Steps:**
   1. Prepare the procedure (Section 5.3).
   2. Somesh runs it on his laptop in a **new folder** (fresh clone, fresh venv); Atharv observes and records.
   3. After install, **switch Wi-Fi off** and run tests, a pipeline run, the dashboard and `sla reflect` (Ollama not running).
   4. Fix any failure (bug-fix PRs with tests), re-run.
   5. Write `CHANGELOG.md` (Section 5.3 template) from merged PRs (`gh pr list --state merged --limit 200`).
   6. Tag `v0.9-rc` on a green commit; create a GitHub pre-release.
8. **Commands:**
   ```bash
   git checkout -b docs/atharv-94-release-candidate
   gh pr list --state merged --limit 200 --json number,title,author > merged_prs.json   # not committed
   git add CHANGELOG.md docs/clean_install_test.md
   git commit -m "docs: changelog and clean-install offline test for v0.9-rc"
   git push -u origin docs/atharv-94-release-candidate
   ```
9. **Tests:** offline test steps all pass.
10. **Expected result:** filled `clean_install_test.md`; tag and pre-release on GitHub.
11. **Common errors:** testing in your usual venv (not clean); forgetting that PyTorch must be downloaded *during* install (internet needed once — say so).
12. **Branch:** `docs/atharv-94-release-candidate`
13. **Commit:** `docs: changelog and clean-install offline test for v0.9-rc`
14. **PR title:** `docs: v0.9-rc release notes + install test (SLA-09-AG-1)`
15. **Acceptance:** test passed on a clean setup; reviewer: Brahmanand.

**Task ID:** SLA-09-AG-2
**Task Title:** Licences and learning module documentation
**Priority:** P2
**Estimated Duration:** 2 h (docs 2)
**Dependencies:** `pyproject.toml`
**Assigned Member:** Atharv Gundale

1. **What:** `docs/licences.md`, `docs/modules/learning.md`.
2. **Why:** we must show every dependency is free and open source, and that the optional LLM model's licence allows our use.
3. **Files:** as item 1.
4. **Functions:** documents `QLearningAgent`, `DQNAgent`, `LinearSchedule`, `QNetwork`, guards.
5. **Inputs:** `pyproject.toml`, each package's licence (check on PyPI / the project's repository).
6. **Outputs:** licence table (Section 5.3).
7. **Steps:** verify each licence at the source → table → module doc → PR #95.
8. **Commands:** branch `docs/atharv-95-licences`; `pip show gymnasium numpy pandas` (shows `License:`); commit `docs: licences and learning module docs`.
9. **Tests:** every dependency in `pyproject.toml` (+ PyTorch, Ollama, the model) listed.
10. **Expected result:** complete table; project licence MIT (from `pyproject.toml`).
11. **Common errors:** copying a licence from memory — **verify** at the source; forgetting dev tools (pytest, ruff).
12. **Branch:** `docs/atharv-95-licences`
13. **Commit:** `docs: licences and learning module docs`
14. **PR title:** `docs: licences + learning docs (SLA-09-AG-2)`
15. **Acceptance:** reviewer: Vedant.

**Task ID:** SLA-09-AG-3
**Task Title:** Report chapter 4 — design and implementation
**Priority:** P1
**Estimated Duration:** 4 h (docs 3, review 1)
**Dependencies:** module docs (#92)
**Assigned Member:** Atharv Gundale

1. **What:** `report/chapter_4.docx`.
2. **Why:** explains architecture, data flow, algorithms and key design decisions (callbacks, seed ranges, grounding).
3–15. **Files** `report/chapter_4.docx` · **Inputs** `docs/design.md`, `docs/architecture.md`, `docs/modules/*.md`, Vedant's diagrams · **Outputs** chapter with architecture diagram, class/sequence diagram, algorithm boxes (Q-learning update, DQN update), short code excerpts (≤ 15 lines each) · **Steps** outline → write → insert diagrams → review by Brahmanand → revise · **Commands** branch `docs/atharv-97-report-ch4`, commit `docs(report): draft chapter 4` · **Tests** every module named exists in `src/` with that name · **Expected** reviewed draft · **Common errors** pasting whole files (use excerpts; full code is in the repo) · **Branch** `docs/atharv-97-report-ch4` · **Commit** `docs(report): draft chapter 4` · **PR** `docs: report chapter 4 (SLA-09-AG-3)` · **Acceptance** Brahmanand's comments resolved.

### Vedant Biradar

**Task ID:** SLA-09-VB-1
**Task Title:** Report chapters 5–6 and final figures
**Priority:** P1
**Estimated Duration:** 8 h (testing/figure generation 2, docs 5, review 1)
**Dependencies:** `results/` (W8)
**Assigned Member:** Vedant Biradar

1. **What:** `report/chapters_5-6.docx` (testing & results; discussion, limitations, conclusion, future work) and `report/figures/` (learning curves with seed bands, eval curves, ablation bar chart, architecture diagram export).
2. **Why:** the evidence chapters — they decide whether the project's claims are believed.
3. **Files:** as item 1.
4. **Functions:** `plot_seed_band`, `plot_eval_curve` (W5) to regenerate figures from the database.
5. **Inputs:** every file in `results/`; `runs/episodes.db` from the final runs.
6. **Outputs:** chapters where each table/figure caption names its source file, e.g. "Source: results/final_table.md (commit a1b2c3d)".
7. **Steps:**
   1. List figures/tables needed.
   2. Write chapter 5: protocol, test summary, final table, ablation, performance, reflection evaluation.
   3. Generate figures with the Section 5.5 script (from the database — not screenshots of old plots).
   4. Write chapter 6: what worked, what did not (failure analysis), limitations (5 seeds, two small environments, CPU only, template notes), future work.
   5. Peer review by Atharv → revise.
8. **Commands:**
   ```bash
   git checkout -b docs/vedant-98-report-ch5-6
   python make_report_figures.py         # Section 5.5 snippet saved locally (scratch file)
   git add report/chapters_5-6.docx report/figures
   git commit -m "docs(report): draft chapters 5-6 with generated figures"
   git push -u origin docs/vedant-98-report-ch5-6
   ```
9. **Tests:** pick 5 numbers at random from the chapters; find each in `results/` — all must match.
10. **Expected result:** reviewed draft; every figure regenerable.
11. **Common errors:** using pilot numbers (Weeks 5–7) instead of final ones; overclaiming ("the agent is intelligent") — describe exactly what was measured.
12. **Branch:** `docs/vedant-98-report-ch5-6`
13. **Commit:** `docs(report): draft chapters 5-6 with generated figures`
14. **PR title:** `docs: report chapters 5–6 (SLA-09-VB-1)`
15. **Acceptance:** 5-number spot check passes; reviewer: Atharv.

**Task ID:** SLA-09-VB-2
**Task Title:** Memory, evaluation and reflection module documentation
**Priority:** P2
**Estimated Duration:** 3 h (docs 2, integration 1)
**Dependencies:** none
**Assigned Member:** Vedant Biradar

1–15. **What** `docs/modules/memory_evaluation_reflection.md` (replay buffer, episode store schema, retention, evaluator + seed ranges, metrics, stats, reflection + grounding) · **Why** source for ch 4–5 and viva · **Files** as named · **Functions** all public functions of `memory/`, `evaluation/`, `reflection/` · **Inputs** code · **Outputs** doc following the Section 5.2 template · **Steps** template → write → Brahmanand reviews → PR #92 · **Commands** branch `docs/vedant-92-module-docs`, commit `docs(modules): memory, evaluation and reflection` · **Tests** every function named exists · **Expected** merged by Day 3 · **Common errors** describing planned features that were not built · **Branch** `docs/vedant-92-module-docs` · **Commit** as above · **PR** `docs: module docs (SLA-09-VB-2)` · **Acceptance** reviewer Brahmanand.

### Somesh Badwane

**Task ID:** SLA-09-SB-1
**Task Title:** User guide, UI module doc and screenshots
**Priority:** P1
**Estimated Duration:** 5 h (learning 1, docs 3, review 1)
**Dependencies:** README final (#91)
**Assigned Member:** Somesh Badwane

**0. Learn first (~1 h):** how to write instructions for a beginner (one action per step, show what they should see), Markdown images (`![caption](screenshots/train_page.png)`), taking clean screenshots (crop, no personal information visible).

1. **What:** `docs/user_guide.md`, `docs/modules/ui.md`, `docs/screenshots/*.png`.
2. **Why:** you built the dashboard; you are the best person to explain it. The user guide becomes a report appendix.
3. **Files:** as item 1.
4. **Functions:** documents the three pages, `common.py`, `feedback.py`.
5. **Inputs:** the running dashboard.
6. **Outputs:** step-by-step guide with screenshots: install, start dashboard, train, read results, generate/rate a note, common problems.
7. **Steps:** outline (Section 5.6) → screenshots of each page → write → ask Vedant (not a UI author) to follow it → fix → PR #99a.
8. **Commands:**
   ```bash
   git checkout main && git pull
   git checkout -b docs/somesh-99-user-guide
   sla dashboard
   git add docs/user_guide.md docs/modules/ui.md docs/screenshots
   git commit -m "docs: user guide and UI module documentation"
   git push -u origin docs/somesh-99-user-guide
   ```
9. **Tests:** Vedant completes "train → results → rate a note" using only the guide.
10. **Expected result:** guide merged with 4–6 screenshots.
11. **Common errors:** screenshots showing your username or other private windows; huge PNGs (crop; keep each under ~500 KB).
12. **Branch:** `docs/somesh-99-user-guide`
13. **Commit:** `docs: user guide and UI module documentation`
14. **PR title:** `docs: user guide (SLA-09-SB-1)`
15. **Acceptance:** Vedant's test passed; reviewer: Vedant.

**Task ID:** SLA-09-SB-2
**Task Title:** Contribution record from real Git/GitHub data
**Priority:** P2
**Estimated Duration:** 2 h (docs 2)
**Dependencies:** none
**Assigned Member:** Somesh Badwane

1. **What:** `docs/contributions.md` — per member: modules owned, merged PRs, reviews, documents.
2. **Why:** examiners ask "who did what?". The answer must come from the repository, not from memory — **never edit or inflate the numbers**.
3. **Files:** `docs/contributions.md`.
4. **Functions:** Git/GitHub commands (Section 5.6).
5. **Inputs:** `git shortlog`, `gh pr list`.
6. **Outputs:** table + links to PR lists.
7. **Steps:** run the commands → copy the output into the table → each member checks their row → PR #99b (finalised in Week 10).
8. **Commands:** see Section 5.6.
9. **Tests:** every member confirms their row in a PR comment.
10. **Expected result:** a table that anyone can regenerate with the same commands.
11. **Common errors:** commit counts differ because a member committed with a different e-mail — map e-mails with a `.mailmap` file or explain it in a note; do not change the numbers.
12. **Branch:** `docs/somesh-99-contributions`
13. **Commit:** `docs: contribution record from git history`
14. **PR title:** `docs: contributions (SLA-09-SB-2)`
15. **Acceptance:** all 4 members approve; reviewer: Atharv.

**Task ID:** SLA-09-SB-3
**Task Title:** Slide deck draft
**Priority:** P2
**Estimated Duration:** 4 h (coding 1 [figure export], docs 2, integration 1)
**Dependencies:** figures from Vedant; screenshots
**Assigned Member:** Somesh Badwane

1–15. **What** `slides/draft.pptx` (12–15 slides, structure in Section 5.6) · **Why** the viva presentation · **Files** `slides/draft.pptx` · **Inputs** one slide of content from each member, figures, screenshots, `results/final_table.md` · **Outputs** draft deck · **Steps** structure → collect inputs by Day 5 → build → team review Day 7 · **Commands** branch `docs/somesh-99-slides`, commit `docs(slides): first draft` · **Tests** every number on a slide is in `results/` · **Expected** draft reviewed · **Common errors** too much text (max ~30 words per slide); low-resolution figures · **Branch** `docs/somesh-99-slides` · **Commit** `docs(slides): first draft` · **PR** `docs: slide draft (SLA-09-SB-3)` · **Acceptance** team comments collected; reviewer Brahmanand.

**Independent practice exercise:** explain, in 5 sentences written for a first-year student, what happens when someone clicks "Start training" — from your page down to the runner and back. Use it as the first paragraph of `docs/modules/ui.md` if Vedant agrees it is correct.

---

## SECTION 5 — COMPLETE TECHNICAL IMPLEMENTATION

This week's "implementation" is documentation. No library or module is added or renamed.

### 5.1 Final README (Brahmanand)

`README.md` — reference final version (replace `<team-account>`; add the results lines **only** by copying from `results/final_table.md`):
```markdown
# Self-Learning AI Agent

An agent that starts with **no knowledge** of its task and improves by learning from rewards:
tabular **Q-learning** on FrozenLake-v1 and a **Deep Q-Network (DQN)** on CartPole-v1. Learning
is proven by evaluating a frozen copy of the policy on fixed test seeds across 5 training seeds.

> Results are added here only from logged runs (`results/final_table.md`).

## Quickstart
```bash
git clone https://github.com/<team-account>/self-learning-ai-agent.git
cd self-learning-ai-agent
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1    Mac/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install torch --index-url https://download.pytorch.org/whl/cpu   # Mac: pip install torch
pip install -e ".[dev]"
pytest
sla train --config configs/frozenlake_q.yaml
sla dashboard
```

## Commands
| Command | What it does |
|---|---|
| `sla train --config <yaml> [--seed N] [--episodes N]` | Train, then evaluate on test seeds |
| `sla resume --run runs/<run_id>` | Continue from the latest checkpoint |
| `sla evaluate --checkpoint runs/<run_id>/checkpoints/best` | Evaluate without learning |
| `sla pipeline --config <yaml> --seeds 0 1 2 3 4` | Train → evaluate → plots → note, per seed |
| `sla reflect --run-id <run_id> [--llm]` | Grounded explanation note |
| `sla prune --older-than 30 [--yes]` | Delete old runs (dry run by default) |
| `sla dashboard` | Streamlit UI |

## Team
Brahmanand Mathpati · Atharv Gundale · Vedant Biradar · Somesh Badwane — see `docs/contributions.md`.

## License
MIT
```

### 5.2 Module documentation template (everyone)

```markdown
# Module: <package> (owner: <name>)
## Purpose (2-3 sentences, plain English)
## Files
| File | Main classes/functions | Used by |
## How it works (numbered steps or a small diagram)
## Key design decisions (and why)
## Inputs and outputs (types, units, files written)
## Errors raised (SLAError subclasses and when)
## Tests (test files, what they prove)
## Limitations / future work
```

### 5.3 Release, licences, clean install (Atharv)

`docs/clean_install_test.md` procedure (fill the Result column with what actually happened):
```markdown
# Clean-install and offline test (v0.9-rc candidate commit <sha>)
Machine: <CPU, RAM, OS>   Tester: Somesh   Observer: Atharv   Date: <date>
| # | Step | Command | Expected | Result (pass/fail, time, notes) |
|---|---|---|---|---|
| 1 | Fresh clone in a new folder | git clone ... sla-clean && cd sla-clean | repo files present | |
| 2 | New virtual environment | python -m venv .venv ; activate | (.venv) in prompt | |
| 3 | Install PyTorch CPU (internet needed once) | pip install torch --index-url https://download.pytorch.org/whl/cpu | installs | |
| 4 | Install project | pip install -e ".[dev]" | installs | |
| 5 | Switch internet OFF; make sure Ollama is not running | - | - | |
| 6 | Tests | pytest | all pass (UI/smoke may skip if a package is missing) | |
| 7 | Pipeline | sla pipeline --config configs/frozenlake_q.yaml --seeds 0 | run folder, plots, template note | |
| 8 | Evaluate | sla evaluate --checkpoint runs/<id>/checkpoints/best | score printed | |
| 9 | Reflect without LLM | sla reflect --run-id <id> --llm | "LLM unavailable" warning, template note shown | |
| 10 | Dashboard | sla dashboard | opens at localhost:8501, train a 300-episode FrozenLake run | |
Conclusion: <one paragraph, honest>
```

`CHANGELOG.md` template ([Keep a Changelog](https://keepachangelog.com) style):
```markdown
# Changelog
## [v0.9-rc] - <date>
### Added
- Training runner with callbacks, safety limits, checkpoints and exact resume (#42, #51)
- Tabular Q-learning (FrozenLake) and DQN with replay buffer and target network (CartPole) (#43, #46, #47)
- SQLite episode store, retention, plots (#53, #54, #55)
- Frozen-policy evaluator, guards, transition validation, baselines (#61, #64, #68, #67)
- Full pipeline, CLI, grounded reflection (optional local LLM), statistics, ablation, Streamlit dashboard (#71-#78)
- Final experiments, tables, failure analysis, performance and test reports (#81-#89)
### Fixed
- <bug-fix PRs from Week 8, by number>
### Notes
- Package version in pyproject.toml remains 0.1.0; tags mark project milestones.
```
(Replace the issue numbers with the **actual merged PR numbers** from `gh pr list`; the numbers above follow this handbook's plan.)

`docs/licences.md` table — **verify every entry at the package's PyPI page or repository before merging** (licences can change between versions):
```markdown
| Component | Use | Licence (verify) | Cost |
|---|---|---|---|
| Python | language | PSF License | free |
| gymnasium | environments | MIT | free |
| numpy | arrays | BSD-3-Clause | free |
| pandas | tables | BSD-3-Clause | free |
| scipy | t-test | BSD-3-Clause | free |
| matplotlib | plots | Matplotlib License (PSF-based) | free |
| PyYAML | configs | MIT | free |
| psutil | memory measurement | BSD-3-Clause | free |
| requests | optional Ollama HTTP calls | Apache-2.0 | free |
| streamlit | dashboard | Apache-2.0 | free |
| torch (CPU) | DQN | BSD-3-Clause | free |
| pytest, pytest-cov | tests | MIT | free |
| ruff | lint | MIT | free |
| SQLite (stdlib sqlite3) | database | Public domain | free |
| Ollama (optional) | local LLM server | MIT | free |
| qwen2.5:1.5b (optional) | local LLM model | Apache-2.0 | free |
| This project | - | MIT (pyproject.toml) | free |
Note: larger Qwen2.5 variants (e.g. 3B) use a different, more restrictive licence - we do not use them.
```

### 5.4 Report outline (Brahmanand, with all)

`docs/report_outline.md`:
```markdown
# Report outline and rules
Front matter: title page, certificate, declaration, acknowledgement, abstract (<= 250 words), contents, lists of figures/tables.
Ch 1 Introduction: background, problem statement, objectives (from docs/requirements.md), scope, report organisation.
Ch 2 Literature review: RL basics, Q-learning, DQN (replay, target network), evaluation practice, LLM explanations + hallucination, gap.
Ch 3 Requirements & feasibility: FR/NFR tables with IDs, use cases, feasibility (technical, economic: Rs 0, operational).
Ch 4 Design & implementation: architecture, modules, data flow, algorithms, key decisions, tools.
Ch 5 Testing & results: protocol, test summary, final table, ablation, performance, reflection evaluation.
Ch 6 Discussion & conclusion: findings, failure analysis, limitations, future work, conclusion.
References (IEEE style). Appendices: user guide, contributions, licences, test report, clean-install test.
Rules: every number cites a results/ file; figures numbered "Fig. 5.2"; tables "Table 5.1"; no copied text; first person plural ("we").
```

### 5.5 Report figures (Vedant)

Save as a scratch script `make_report_figures.py` in the repo root (do not commit it — it only calls existing project functions):
```python
"""Regenerate report figures from the final runs (uses only existing project functions)."""
from pathlib import Path

import pandas as pd

from sla.evaluation.plots import plot_eval_curve, plot_seed_band
from sla.memory.episode_store import EpisodeStore

store = EpisodeStore("runs/episodes.db")
manifest = pd.read_csv("results/manifest.csv")
out = Path("report/figures")
for label, group in manifest.groupby("label"):
    curves = {int(r.seed): store.query_episodes(r.run_id) for r in group.itertuples()}
    plot_seed_band(curves, window=50, title=f"{label}: training reward, 5 seeds",
                   out_path=out / f"{label}_seed_band.png")
    first = group.iloc[0]
    plot_eval_curve(store.query_evals(first.run_id), title=f"{label}: validation score (seed {first.seed})",
                    out_path=out / f"{label}_eval_seed{first.seed}.png")
print("Figures written to", out)
```

### 5.6 User guide, contributions, slides (Somesh)

`docs/user_guide.md` outline:
```markdown
# User guide
1. What this program does (3 sentences)
2. Install (copy from README Quickstart) - what you should see after each step
3. Start the dashboard: `sla dashboard` -> browser opens at http://localhost:8501
4. Train an agent (screenshot): choose environment and agent, episodes, seed, click Start
5. Read the results (screenshot): learning curve, evaluation, how episodes ended
6. Read and rate an explanation (screenshot): what "grounded" means; rating form
7. Optional: the local LLM (Ollama) - the program works without it
8. Problems and solutions (table)
```

Contribution record commands (copy the output; do not edit numbers):
```bash
git checkout main && git pull
git shortlog -sne --no-merges main                        # commits per author (name + e-mail)
gh pr list --state merged --author <github-username> --limit 200 --json number,title | python -c "import json,sys; print(len(json.load(sys.stdin)))"
gh api "repos/<org>/self-learning-ai-agent/pulls?state=closed&per_page=100" --paginate --jq '.[].number' | wc -l   # total closed PRs
```
`docs/contributions.md` table:
```markdown
| Member | Modules owned (from handbook) | Merged PRs (gh) | Commits (git shortlog) | Main documents | Reviews given |
|---|---|---|---|---|---|
Generated on <date> from commit <sha> with the commands above.
```

Slide structure (12–15 slides): title · problem · objectives · background (RL in one picture) · architecture · Q-learning on FrozenLake · DQN on CartPole · memory & self-improvement (store, checkpoints, resume) · evaluation protocol · results table · ablation · reflection (grounded notes) · demo · limitations & future work · thank you / questions.

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
│   ├── modules/
│   │   ├── agent.md   [NEW · Brahmanand]
│   │   ├── learning.md   [NEW · Atharv]
│   │   ├── memory_evaluation_reflection.md   [NEW · Vedant]
│   │   └── ui.md   [NEW · Somesh]
│   ├── notes/
│   │   ├── ablation_notes.md
│   │   ├── dqn_debug_checklist.md
│   │   ├── dqn_explained.md
│   │   ├── q_learning_by_hand.md
│   │   └── week6_results.md
│   ├── screenshots/   [NEW · Somesh]
│   ├── architecture.md   [MODIFIED · Atharv]
│   ├── clean_install_test.md   [NEW · Atharv]
│   ├── contributions.md   [NEW · Somesh]
│   ├── data_handling.md
│   ├── design.md
│   ├── evaluation_protocol.md
│   ├── feasibility.md
│   ├── hardware_audit.md
│   ├── learning_plans.md
│   ├── licences.md   [NEW · Atharv]
│   ├── literature_review.md
│   ├── nfr.md
│   ├── report_outline.md   [NEW · Brahmanand + all]
│   ├── requirements.md
│   ├── synopsis_draft.md
│   ├── synopsis_outline.md
│   ├── tech_stack.md
│   ├── use_cases.md
│   └── user_guide.md   [NEW · Somesh]
├── report/
│   ├── figures/   [NEW · Vedant]
│   ├── chapter_4.docx   [NEW · Atharv]
│   ├── chapters_1-3.docx   [NEW · Brahmanand]
│   └── chapters_5-6.docx   [NEW · Vedant]
├── results/
│   ├── ablation/
│   │   ├── ablation.csv
│   │   └── summary.csv
│   ├── baseline/
│   │   └── baseline.csv
│   ├── failure_analysis.md
│   ├── final_table.csv
│   ├── final_table.md
│   ├── manifest.csv
│   ├── performance.md
│   ├── reflection_eval.md
│   └── test_report.md
├── scripts/
│   ├── failure_analysis.py
│   ├── hardware_check.py
│   ├── make_tables.py
│   ├── measure_performance.py
│   ├── quick_frozenlake_check.py
│   ├── run_ablation.py
│   ├── run_baseline.py
│   └── run_final_experiments.py
├── slides/
│   └── draft.pptx   [NEW · Somesh]
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
│       │   │   ├── 1_Train.py
│       │   │   ├── 2_Results.py
│       │   │   └── 3_Reflection.py
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
│   │   ├── test_persistence.py
│   │   ├── test_pipeline_e2e.py
│   │   ├── test_resume.py
│   │   ├── test_runner.py
│   │   └── test_transition_validation.py
│   ├── ui/
│   │   └── test_pages.py
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
├── CHANGELOG.md   [NEW · Atharv]
├── CONTRIBUTING.md
├── pyproject.toml
└── README.md   [MODIFIED · Atharv → Brahmanand]
```

Legend: [NEW] created this week · [MODIFIED] changed this week · no tag = carried over unchanged from an earlier week. `runs/` (training outputs) and `.venv/` exist on your laptop but are git-ignored, so they are not shown.

---

## SECTION 7 — GITHUB COLLABORATION PROCEDURE

13-step flow as every week (documentation PRs are reviewed like code). Week-9 issues:

| # | Title | Owner | Branch | Reviewer | Merge by |
|---|---|---|---|---|---|
| 91 | Final README + agent docs | Brahmanand | `docs/brahmanand-91-readme-final` | Somesh | **Day 3** |
| 92 | Module docs (memory/eval/reflection; learning; ui) | Vedant, Atharv, Somesh | `docs/vedant-92-module-docs` (+ in #95, #99) | Brahmanand | **Day 3** |
| 93 | Report chapters 1–3 | Brahmanand | `docs/brahmanand-93-report-ch1-3` | Vedant | Day 6 |
| 94 | CHANGELOG + clean-install test + `v0.9-rc` | Atharv | `docs/atharv-94-release-candidate` | Brahmanand | **Day 5** |
| 95 | Licences + learning docs | Atharv | `docs/atharv-95-licences` | Vedant | Day 3 |
| 97 | Report chapter 4 | Atharv | `docs/atharv-97-report-ch4` | Brahmanand | Day 6 |
| 98 | Report chapters 5–6 + figures | Vedant | `docs/vedant-98-report-ch5-6` | Atharv | Day 6 |
| 99 | User guide, contributions, slides, screenshots | Somesh | `docs/somesh-99-*` | Vedant / Atharv / Brahmanand | Day 6 |

**Binary files (`.docx`, `.pptx`, `.png`):** Git cannot merge them. Only the owner edits each file; reviewers comment in the PR (or in a shared copy) and the owner applies changes. Keep figures under ~500 KB each.

**Creating the pre-release on GitHub:** Releases → Draft a new release → choose tag `v0.9-rc` → title "v0.9-rc (release candidate)" → paste the CHANGELOG section → tick "Set as a pre-release" → Publish.

---

## SECTION 8 — WEEKLY INTEGRATION PROCEDURE

| Item | This week |
|---|---|
| What to connect | README ↔ user guide ↔ module docs (consistent commands and names); report chapters ↔ `results/` files; slides ↔ report figures. |
| Integrator | **Atharv** (integration captain, Week 9). |
| Consistency rules | module and file names exactly as in `src/` (never rename in docs); commands exactly as in `sla --help`; numbers exactly as in `results/`. |
| Checks | clean-install test; README followed by a teammate; 5-number spot check of chapters 5–6; `pytest` green on the tagged commit. |
| Detect problems | a command in a doc that fails; a figure that cannot be regenerated; two documents giving different numbers. |
| Fix | correct the doc (or, if the code is wrong, a bug-fix PR with a test — then re-check results that depend on it). |

**Integration checklist**
- [ ] Every command in README and user guide runs as written
- [ ] Every module name in docs exists in `src/sla/`
- [ ] Every number in the report matches `results/`
- [ ] Clean-install offline test passed
- [ ] `v0.9-rc` tagged on a green commit

---

## SECTION 9 — TESTING AND VALIDATION

| Type | This week | How |
|---|---|---|
| Regression | full test suite on the release candidate | `pytest` (CI on the tagged commit) |
| Installation | clean install + offline run without Ollama | `docs/clean_install_test.md` |
| Documentation | teammate follows README / user guide | recorded in PR comments |
| Result integrity | 5-number spot check per chapter | reviewer records the check in the PR |
| Licence check | every dependency verified at source | `docs/licences.md` |

**RL rules in writing:** report final (test-seed) numbers only, with mean ± std over 5 seeds and the baseline next to them; label pilot numbers as pilot if mentioned at all; state limitations (5 seeds, small environments, CPU-only, notes from a template unless an LLM was evaluated). Never write a result that is not in a file.

---

## SECTION 10 — COMMON PROBLEMS AND SOLUTIONS

| Problem | Possible Cause | How to Check | Solution |
|---|---|---|---|
| Clean install fails at PyTorch | Python version without a CPU wheel | `python --version` | use Python 3.10–3.12; follow pytorch.org selector |
| `pytest` fails on the clean machine only | file written into repo by a test; missing package | read failure | fix the test to use `tmp_path`; add missing dependency to `pyproject.toml` (flag it) |
| Two documents show different numbers | one copied from an old run | compare with `results/` | always copy from `results/`; regenerate figures |
| `.docx` merge conflict | two people edited | Git message "binary" | one owner per file; reviewer comments only |
| Figures blurry in the report | screenshots of plots | image size | regenerate with `make_report_figures.py` |
| Commit counts look unfair | different e-mails per member | `git shortlog -sne` | add `.mailmap`; explain; never edit numbers |
| Reference cannot be found | invented or wrong citation | search the title | remove or replace with a real, checked source |
| Writing behind schedule | started late | chapter word counts | outline first; write results/limitations before the introduction |

---

## SECTION 11 — WEEKLY DELIVERABLES

| Deliverable | Owner | File/Location | Verification | Status |
|---|---|---|---|---|
| Final README | Brahmanand | `README.md` | teammate followed it | [ ] |
| Agent module doc | Brahmanand | `docs/modules/agent.md` | names match `src/` | [ ] |
| Report outline + ch 1–3 | Brahmanand | `docs/report_outline.md`, `report/chapters_1-3.docx` | Vedant review | [ ] |
| Clean-install offline test | Atharv (+ Somesh) | `docs/clean_install_test.md` | all steps pass | [ ] |
| CHANGELOG + `v0.9-rc` | Atharv | `CHANGELOG.md`, tag, pre-release | visible on GitHub | [ ] |
| Licences + learning doc | Atharv | `docs/licences.md`, `docs/modules/learning.md` | verified at source | [ ] |
| Report ch 4 | Atharv | `report/chapter_4.docx` | Brahmanand review | [ ] |
| Report ch 5–6 + figures | Vedant | `report/chapters_5-6.docx`, `report/figures/` | 5-number spot check | [ ] |
| Memory/eval/reflection doc | Vedant | `docs/modules/memory_evaluation_reflection.md` | names match `src/` | [ ] |
| User guide + UI doc + screenshots | Somesh | `docs/user_guide.md`, `docs/modules/ui.md`, `docs/screenshots/` | Vedant followed it | [ ] |
| Contribution record | Somesh | `docs/contributions.md` | 4 approvals | [ ] |
| Slide draft | Somesh | `slides/draft.pptx` | team review | [ ] |

---

## SECTION 12 — WEEKLY REVIEW MEETING

**Agenda:** report walk-through (one chapter per owner, 5 min each) · slide draft · clean-install result · release candidate · open issues · Week-10 plan.

**Questions:**
1. Atharv: what exactly did the clean-install offline test prove, and what still needs internet?
2. Which licence does each major dependency use, and why can we use `qwen2.5:1.5b` but not the 3B model?
3. Vedant: pick a number from chapter 5 — show the file and commit it came from.
4. Brahmanand: what is our problem statement in one sentence, and which objective does each results table support?
5. What are our three most important limitations, and where are they written?
6. Somesh: how was `docs/contributions.md` produced, and how can an examiner verify it?
7. What would a new student find confusing in our README or user guide?
8. What is left for Week 10, and who owns each item?

---

## SECTION 13 — WEEK COMPLETION CHECKLIST

- [ ] All assigned tasks completed
- [ ] Documents pushed to `docs/…` branches
- [ ] Pull requests reviewed and merged
- [ ] All tests pass locally and in CI on the release-candidate commit
- [ ] Docs integrated and consistent with code and results
- [ ] Documentation updated (README, module docs, user guide, licences, CHANGELOG)
- [ ] Weekly demonstration (report + slides walk-through) completed
- [ ] Blockers recorded

---

## SECTION 14 — NEXT WEEK HANDOFF

- **Ready before Week 10:** `v0.9-rc` tag and pre-release; report chapters 1–6 (reviewed drafts); figures; user guide; licences; contributions draft; slide draft; clean-install record.
- **Files Week 10 depends on:** all `report/*.docx` (merged into `final_report.docx`), `slides/draft.pptx` (→ `final.pptx`), `docs/contributions.md` (final numbers), `results/` (regression comparison), `src/sla/ui/pages/2_Results.py` (Somesh's Week-10 enhancement).
- **Coordination:** Week 10 is the only week a small feature is added (Somesh's CSV export) — it must not touch training or evaluation code, so results stay valid. Mock vivas are scheduled by Atharv on Week-10 Days 3 and 5.
- **Risks:** last-minute code changes break the demo — after `v1.0` only documentation changes; report formatting takes time — leave a full day.
