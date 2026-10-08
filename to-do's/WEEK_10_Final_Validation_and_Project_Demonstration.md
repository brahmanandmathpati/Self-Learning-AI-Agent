# WEEK 10 — Final Validation and Project Demonstration

**Project:** Self-Learning AI Agent · **Team:** Brahmanand Mathpati, Atharv Gundale, Vedant Biradar, Somesh Badwane
**Source:** *Self_Learning_AI_Agent_10_Week_Master_Plan* (v1.0) · **Interfaces:** `docs/design.md` (tag `w2-design-freeze`)

---

## SECTION 1 — WEEK OVERVIEW

| Item | Details |
|---|---|
| Week number | 10 of 10 |
| Week title | Final Validation and Project Demonstration |
| Main objective | Validate the final system one last time (regression check against the Week-8 results), release **`v1.0`**, finish the report, slides, demo video and evidence pack, and prepare every member for the **viva** with mock sessions. Somesh adds one small independent enhancement (CSV export). |
| Expected outcome | `results/regression_check.md` shows the re-checked scores match `results/manifest.csv`; tag `v1.0` + GitHub Release; `report/final_report.docx` (and PDF); `slides/final.pptx`; demo video link; `demo/demo_script.md`; `demo/evidence/`; `docs/viva_questions.md`; final `docs/contributions.md`; CSV export on the Results page with 3 tests. |
| Required knowledge | Everything; presentation skills; answering questions about your own module and the whole system. |
| Required tools | Same venv; free screen recorder (OBS Studio — open source, GPL) for the demo video; free video hosting (unlisted YouTube or Google Drive link) — the video is **not** committed to Git (`*.mp4` is git-ignored). No new Python dependency. |
| Prerequisites from previous weeks | Week 9: `v0.9-rc`, reviewed report chapters, figures, user guide, licences, contributions draft, slide draft. |
| Approximate workload | 11 h per member. |
| Technical dependencies | Somesh's CSV export merged by **Day 3**; regression check passed by **Day 4**; `v1.0` tagged on **Day 4** (after that: documentation changes only). Report and slides final by **Day 6**. |
| Definition of Done | CI green on `v1.0`; regression check "ALL MATCH" (or every mismatch explained and fixed); the full demo runs from a fresh clone of `v1.0` with Ollama off; every member has completed two mock vivas; final report numbers match `results/`. |

**In simple words:** no new features (except one tiny, safe one). We check everything still gives the same answers, freeze version 1.0, and practise explaining it.

---

## SECTION 2 — WHAT WE ARE BUILDING THIS WEEK

1. **Items:** `scripts/regression_check.py`, `results/regression_check.md`, `demo/demo_script.md` (Brahmanand) · final code review, `v1.0` tag and release, `docs/viva_questions.md`, mock vivas (Atharv) · `report/final_report.docx` + PDF, `demo/evidence/` (Vedant) · `src/sla/ui/export.py` + CSV button on the Results page + `tests/unit/test_export.py`, demo video, `slides/final.pptx`, final `docs/contributions.md` (Somesh).
2. **Why:** the examiner sees the demo, the report and the viva answers. A regression check guarantees the demo shows the same system that produced the report's numbers.
3. **Connection:** this closes the project; the tag `v1.0` is what you submit.
4. **If missing:** a demo that crashes, a report number nobody can reproduce, or a member who cannot explain their module costs marks.
5. **Final output:**
   ```text
   $ python scripts/regression_check.py
          label  seed  run_id  manifest_mean  recheck_mean  same
   dqn_cartpole     0  ...               ...           ...  True
   ...
   ALL MATCH
   $ git tag --list
   w2-design-freeze  v0.8-experiments  v0.9-rc  v1.0
   ```

**Analogy:** a pilot's final pre-flight checklist — every switch checked, the same aircraft that was tested, then take-off (the demo).

**Stack note:** the CSV export uses only pandas (already a dependency) and Streamlit's built-in `st.download_button`. It does not touch training or evaluation code, so the Week-8 results remain valid.

---

## SECTION 3 — DAILY EXECUTION PLAN

### Day 1 — Final plan; regression script; enhancement starts (1.5 h)
- **Daily objective:** list every remaining item with an owner and deadline; start the safe enhancement.
- **Assigned members:** all; Atharv final-review lead.
- **Individual tasks:** Brahmanand: `regression_check.py` (SLA-10-BM-1 steps 1–2). Atharv: final review checklist (SLA-10-AG-1 step 1); draft `viva_questions.md` (SLA-10-AG-2 step 1). Vedant: merge report chapters into one document (SLA-10-VB-1 step 1). Somesh: `export.py` + tests (SLA-10-SB-1 steps 1–3).
- **Required commands:**
  ```bash
  git checkout main && git pull && pytest
  ```
- **Expected files:** `scripts/regression_check.py`, `src/sla/ui/export.py`, `tests/unit/test_export.py`.
- **GitHub activity:** issues #101–#108; milestone "v1.0".
- **Completion checklist:** - [ ] all remaining items have owners

### Day 2 — Regression check; export button (1.5 h)
- **Daily objective:** re-checked scores match the manifest; CSV export works.
- **Assigned members:** Brahmanand (runs regression on the laptop(s) that hold the final run folders), Somesh (button on the Results page → PR #101, reviewer Vedant), Atharv (code review pass 1), Vedant (report formatting).
- **Individual tasks:** SLA-10-BM-1 steps 3–5 · SLA-10-SB-1 steps 4–6.
- **Required commands:**
  ```bash
  python scripts/regression_check.py --manifest results/manifest.csv
  pytest tests/unit/test_export.py tests/ui -v
  ```
- **Completion checklist:** - [ ] regression result recorded · - [ ] export PR open

### Day 3 — Mock viva 1; merge export (1.5 h)
- **Daily objective:** first mock viva for every member; enhancement merged.
- **Assigned members:** Atharv runs mock viva 1 (each member 10 min: 3 questions on own module, 2 on the whole system); others observe and note weak answers.
- **Individual tasks:** SLA-10-AG-2 step 2 · SLA-10-SB-1 step 7 (merge).
- **Completion checklist:** - [ ] mock viva 1 done · - [ ] #101 merged

### Day 4 — Tag v1.0; demo script; evidence (1.5 h)
- **Daily objective:** final release; demo rehearsed once.
- **Assigned members:** Atharv (final checks + tag + release), Brahmanand (demo script + first rehearsal), Vedant (evidence pack), Somesh (records demo video draft following the script).
- **Individual tasks:** SLA-10-AG-1 steps 2–5 · SLA-10-BM-2 steps 1–3 · SLA-10-VB-2 · SLA-10-SB-2 steps 1–2.
- **Required commands:**
  ```bash
  git checkout main && git pull && pytest
  git tag -a v1.0 -m "Final submission: Self-Learning AI Agent"
  git push origin v1.0
  ```
- **Completion checklist:** - [ ] `v1.0` tagged · - [ ] release published · - [ ] demo rehearsed

### Day 5 — Mock viva 2; fresh-clone demo (1.5 h)
- **Daily objective:** second mock viva (harder questions, a guest if possible: another student or a teacher); demo from a fresh clone of `v1.0`.
- **Assigned members:** all.
- **Individual tasks:** SLA-10-AG-2 step 3 · SLA-10-BM-2 step 4.
- **Required commands:** `git clone --branch v1.0 https://github.com/<org>/self-learning-ai-agent.git sla-v1` and the Week-9 clean-install steps.
- **Completion checklist:** - [ ] mock viva 2 done · - [ ] fresh-clone demo works offline

### Day 6 — Final report, slides, video, contributions (2.5 h)
- **Daily objective:** all submission files final.
- **Assigned members:** Vedant (final report + PDF), Somesh (final slides, final video, contributions numbers regenerated on `v1.0`), Brahmanand + Atharv (proof-read the full report; check 10 random numbers against `results/`).
- **Individual tasks:** SLA-10-VB-1 steps 2–4 · SLA-10-SB-2 steps 3–4 · SLA-10-SB-3.
- **Completion checklist:** - [ ] report final · - [ ] slides final · - [ ] video link in README · - [ ] contributions final

### Day 7 — Final review and dress rehearsal (1 h)
- **Daily objective:** full presentation rehearsal with timing; final Section-12 review; submission checklist.
- **Completion checklist:** - [ ] Section 13 complete · - [ ] submission package ready

---

## SECTION 4 — INDIVIDUAL MEMBER TASKS

### Brahmanand Mathpati

**Task ID:** SLA-10-BM-1
**Task Title:** Final regression check
**Priority:** P1
**Estimated Duration:** 5 h (testing 3, integration 1, docs 1)
**Dependencies:** final run folders (Week 8) on the laptop(s) that produced them; `results/manifest.csv`
**Assigned Member:** Brahmanand Mathpati

1. **What:** `scripts/regression_check.py` and `results/regression_check.md`.
2. **Why:** proves the code you will demo and submit still produces **exactly** the reported numbers from the same checkpoints and test seeds.
3. **Files:** as item 1.
4. **Functions:** `main()` — for each manifest row: load the run's `config.yaml`, evaluate `checkpoints/best` on `TEST_SEED_BASE` with 100 episodes, compare with `final_mean`.
5. **Inputs:** `--manifest`, `--episodes` (must be 100 as in Week 8).
6. **Outputs:** table with `manifest_mean`, `recheck_mean`, `same`; "ALL MATCH" or "MISMATCH".
7. **Steps:**
   1. Write the script (Section 5.1).
   2. Run it on a small test manifest first (Section 5.1 dry run).
   3. Run it on each laptop holding final run folders (paths in `run_dir` are relative to the repo folder of that laptop).
   4. Also run the full test suite on the same commit.
   5. Write `results/regression_check.md` with the copied output, commit sha and laptop. If anything mismatches: stop, find the cause (code change after `v0.8-experiments`? different library version?), fix, re-run — and document it.
8. **Commands:**
   ```bash
   git checkout -b test/brahmanand-102-regression-check
   python scripts/regression_check.py --manifest results/manifest.csv
   pytest
   git add scripts/regression_check.py results/regression_check.md
   git commit -m "test: final regression check against recorded results"
   git push -u origin test/brahmanand-102-regression-check
   ```
9. **Tests:** the script itself is the check; plus `pytest`.
10. **Expected result:** "ALL MATCH" — or documented, explained differences. Never edit the manifest to make them match.
11. **Common errors:** `FileNotFoundError` for a run folder → run on the laptop that has it (or copy the run folder over); tiny float differences on a different laptop for DQN → note the laptop; same-laptop results must match.
12. **Branch:** `test/brahmanand-102-regression-check`
13. **Commit:** `test: final regression check against recorded results`
14. **PR title:** `test: final regression check (SLA-10-BM-1)`
15. **Acceptance:** result document merged before `v1.0`; reviewer: Atharv.

**Task ID:** SLA-10-BM-2
**Task Title:** Demo script and rehearsals
**Priority:** P1
**Estimated Duration:** 6 h (integration 3, docs 2, rehearsal 1)
**Dependencies:** `v1.0`
**Assigned Member:** Brahmanand Mathpati

1. **What:** `demo/demo_script.md` — a minute-by-minute live demo (~8 minutes) with a backup plan.
2. **Why:** a planned demo never surprises you; the backup plan covers laptop or network problems.
3. **Files:** `demo/demo_script.md`.
4. **Functions:** uses `sla` commands and the dashboard.
5. **Inputs:** a fresh clone of `v1.0`; a pre-trained run folder as backup.
6. **Outputs:** script + rehearsal notes (time taken, what went wrong).
7. **Steps:** write (template Section 5.1) → rehearse on Day 4 → fresh-clone rehearsal on Day 5 → final timing on Day 7.
8. **Commands:** branch `docs/brahmanand-103-demo-script`; commit `docs(demo): add live demo script`.
9. **Tests:** two complete rehearsals within 8 minutes.
10. **Expected result:** demo runs offline with Ollama off; backup used at most once in rehearsals.
11. **Common errors:** training CartPole live (too slow) — train FrozenLake live and show a pre-trained DQN run; screen resolution too small for the projector — zoom the browser to 125 %.
12. **Branch:** `docs/brahmanand-103-demo-script`
13. **Commit:** `docs(demo): add live demo script`
14. **PR title:** `docs: demo script (SLA-10-BM-2)`
15. **Acceptance:** team approves after Day-5 rehearsal; reviewer: Vedant.

### Atharv Gundale

**Task ID:** SLA-10-AG-1
**Task Title:** Final code review and `v1.0` release
**Priority:** P1
**Estimated Duration:** 6 h (testing 2, integration 3, docs 1)
**Dependencies:** regression check (#102); export merged (#101)
**Assigned Member:** Atharv Gundale

1. **What:** final review checklist (Section 5.2), `CHANGELOG.md` `[v1.0]` section, tag `v1.0`, GitHub Release.
2. **Why:** a single, clearly identified final version for submission.
3. **Files:** `CHANGELOG.md`.
4. **Functions:** —
5. **Inputs:** merged PRs since `v0.9-rc`; CI status; regression result.
6. **Outputs:** tag, release with notes and links (report PDF, slides, video, results).
7. **Steps:** run checklist → fix small issues via PRs (docs only, or bug fixes with tests — and then re-run the regression) → CHANGELOG → tag → Release (not pre-release).
8. **Commands:**
   ```bash
   git checkout -b docs/atharv-104-release-v1
   ruff check . && pytest
   git log v0.9-rc..main --oneline          # what changed since the release candidate
   git add CHANGELOG.md
   git commit -m "docs: changelog for v1.0"
   git push -u origin docs/atharv-104-release-v1
   # after merge:  git tag -a v1.0 -m "Final submission" && git push origin v1.0
   ```
9. **Tests:** CI green on the tagged commit.
10. **Expected result:** `v1.0` release visible on GitHub.
11. **Common errors:** tagging before the last PR merged (tag the merge commit on `main`); tagging a red CI commit.
12. **Branch:** `docs/atharv-104-release-v1`
13. **Commit:** `docs: changelog for v1.0`
14. **PR title:** `docs: v1.0 release notes (SLA-10-AG-1)`
15. **Acceptance:** checklist complete; reviewer: Brahmanand.

**Task ID:** SLA-10-AG-2
**Task Title:** Viva question bank and two mock vivas
**Priority:** P1
**Estimated Duration:** 5 h (mentoring/sessions 3, docs 2)
**Dependencies:** final report draft
**Assigned Member:** Atharv Gundale

1. **What:** `docs/viva_questions.md` (40+ questions: per module + whole system + results + ethics/limitations, with short answers pointing to files) and two mock vivas.
2. **Why:** every member must answer questions about their own work **and** the overall system. Atharv guides; each member writes the answers for their own module.
3. **Files:** `docs/viva_questions.md`.
4. **Functions:** —
5. **Inputs:** report, module docs, results.
6. **Outputs:** question bank; notes on weak answers after each mock.
7. **Steps:** draft question list (Section 5.2) → each member writes answers for own section → mock viva 1 (Day 3) → update answers → mock viva 2 (Day 5).
8. **Commands:** branch `docs/atharv-105-viva-questions`; commit `docs: viva question bank`.
9. **Tests:** each member answers 5 random questions without notes in mock 2.
10. **Expected result:** all members pass mock 2 by team judgement.
11. **Common errors:** Atharv writing everyone's answers — members must write their own.
12. **Branch:** `docs/atharv-105-viva-questions`
13. **Commit:** `docs: viva question bank`
14. **PR title:** `docs: viva questions (SLA-10-AG-2)`
15. **Acceptance:** each section approved by its owner; reviewer: Vedant.

### Vedant Biradar

**Task ID:** SLA-10-VB-1
**Task Title:** Final report
**Priority:** P1
**Estimated Duration:** 8 h (testing/number checks 2, integration 2, docs 4)
**Dependencies:** chapters from Week 9; regression check
**Assigned Member:** Vedant Biradar

1. **What:** `report/final_report.docx` and an exported PDF (attached to the GitHub Release; PDF committed only if the team agrees on size).
2. **Why:** the main written assessment.
3. **Files:** `report/final_report.docx`.
4. **Functions:** —
5. **Inputs:** `report/chapters_*.docx`, figures, appendices (user guide, contributions, licences, test report, clean-install test, regression check).
6. **Outputs:** one consistent document (fonts, numbering, references, table of contents).
7. **Steps:** merge chapters (Day 1) → apply college format → number check: 10 random numbers verified against `results/` by Brahmanand and Atharv (Day 6) → export PDF → attach to the release.
8. **Commands:** branch `docs/vedant-106-final-report`; commit `docs(report): final report`.
9. **Tests:** 10-number check; every figure/table referenced in the text; every reference cited.
10. **Expected result:** final PDF ready on Day 6.
11. **Common errors:** chapter styles differ (use one template's styles); broken cross-references after merging (update fields before export).
12. **Branch:** `docs/vedant-106-final-report`
13. **Commit:** `docs(report): final report`
14. **PR title:** `docs: final report (SLA-10-VB-1)`
15. **Acceptance:** 10-number check passed; team sign-off; reviewer: Brahmanand.

**Task ID:** SLA-10-VB-2
**Task Title:** Evidence pack
**Priority:** P2
**Estimated Duration:** 3 h (integration 2, docs 1)
**Dependencies:** results, CI, releases
**Assigned Member:** Vedant Biradar

1–15. **What** `demo/evidence/README.md` + small files: links to the CI run on `v1.0`, the GitHub Releases (`v0.9-rc`, `v1.0`), the merged-PR list, `results/` files, screenshots, the demo video link · **Why** lets an examiner verify claims quickly · **Files** `demo/evidence/` · **Inputs** GitHub links, `results/` · **Outputs** an index (Section 5.3) · **Steps** collect links → write index → each member checks their links · **Commands** branch `docs/vedant-106-evidence`, commit `docs(demo): evidence pack index` · **Tests** every link opens · **Expected** index merged before Day 6 · **Common errors** linking to private files (the repo must be accessible to examiners, or include exported copies) · **Branch** `docs/vedant-106-evidence` · **Commit** as above · **PR** `docs: evidence pack (SLA-10-VB-2)` · **Acceptance** reviewer Atharv.

### Somesh Badwane

**Task ID:** SLA-10-SB-1
**Task Title:** Independent enhancement: CSV export of results
**Priority:** P2
**Estimated Duration:** 5 h (learning 1, coding 2, testing 2)
**Dependencies:** your Results page (W7); your `safe_run_name` (W4)
**Assigned Member:** Somesh Badwane — **planned and coded by you alone**; Vedant reviews; ask Atharv only after 30 minutes stuck.

**0. Learn first (~1 h):** `DataFrame.merge` (joining two tables on a column, `how="left"` keeps every left row), `DataFrame.to_csv(index=False)`, bytes vs text (`.encode("utf-8")`), `st.download_button`.

1. **What:** `src/sla/ui/export.py` (`results_to_csv`, `export_filename`), a `# region W10` block at the end of `ui/pages/2_Results.py`, `tests/unit/test_export.py`.
2. **Why:** users (and the report author) can download a run's data to open in a spreadsheet. It shows you can design, build and test a feature independently.
3. **Files:** create `ui/export.py`, `tests/unit/test_export.py`; modify `ui/pages/2_Results.py`.
4. **Functions:** `results_to_csv(episodes, evals=None) -> bytes`; `export_filename(run_id) -> str`.
5. **Inputs:** episodes DataFrame; optional evals DataFrame; run id.
6. **Outputs:** CSV bytes with columns `episode, total_reward, …, eval_mean, eval_std`; a safe file name like `run_1_results.csv`.
7. **Steps:**
   1. Write a 5-line plan in the issue (#101): inputs, output, columns, file name, tests.
   2. Write `results_to_csv` — reject an empty table with `ValueError`; rename eval columns so they join on `episode`.
   3. Write `export_filename` using **your** `safe_run_name` from Week 4.
   4. Write 3 tests (Section 5.4) and run them.
   5. Add the W10 region to the Results page (download button).
   6. Run `pytest tests/unit/test_export.py tests/ui -v` and try the button in `sla dashboard`.
   7. PR #101 → Vedant → merge by Day 3.
8. **Commands:**
   ```bash
   git checkout main && git pull
   git checkout -b feat/somesh-101-csv-export
   pytest tests/unit/test_export.py tests/ui -v
   ruff check src/sla/ui tests/unit/test_export.py
   git add src/sla/ui/export.py src/sla/ui/pages/2_Results.py tests/unit/test_export.py
   git commit -m "feat(ui): download a run's results as CSV"
   git push -u origin feat/somesh-101-csv-export
   ```
9. **Tests:** CSV has episode and eval columns with the right values; empty episodes rejected; file name is safe.
10. **Expected result:** `3 passed`; UI tests still pass; button downloads a CSV.
11. **Common errors:** `KeyError: 'checkpoint_episode'` → evals table has different column names, print `evals.columns`; eval values on the wrong row → evals store the 0-based episode index, the same as `episode`, so join directly; ruff `E402` for the import in the middle of the page → keep the `# noqa: E402` comment (Streamlit pages run top to bottom).
12. **Branch:** `feat/somesh-101-csv-export`
13. **Commit:** `feat(ui): download a run's results as CSV`
14. **PR title:** `feat: CSV export on Results page (SLA-10-SB-1)`
15. **Acceptance:** tests pass; works in the dashboard; does not change any file outside `ui/` and its test; reviewer: Vedant.

**Task ID:** SLA-10-SB-2
**Task Title:** Demo video and final slides
**Priority:** P1
**Estimated Duration:** 4 h (integration 2, docs 2)
**Dependencies:** demo script (Brahmanand); slide draft (W9)
**Assigned Member:** Somesh Badwane

1–15. **What** a 4–6 minute screen recording following `demo/demo_script.md` (OBS Studio, free) uploaded as an unlisted video or Drive link, `demo/demo_video_link.md` with the link, and `slides/final.pptx` · **Why** a backup if the live demo fails, and the final presentation · **Files** `demo/demo_video_link.md`, `slides/final.pptx` · **Inputs** script, figures, final table, team comments on the draft · **Outputs** video link + final deck · **Steps** record draft (Day 4) → team feedback → final recording (Day 6) → update slides with final numbers (copy from `results/final_table.md`) → add link to README · **Commands** branch `docs/somesh-107-video-slides`, commit `docs: demo video link and final slides` · **Tests** video plays from the link in a private browser window; slide numbers match `results/` · **Expected** both ready Day 6 · **Common errors** committing the `.mp4` (it is git-ignored — share a link); personal notifications visible in the recording (turn them off) · **Branch** `docs/somesh-107-video-slides` · **Commit** `docs: demo video link and final slides` · **PR** `docs: video + final slides (SLA-10-SB-2)` · **Acceptance** team approves; reviewer Brahmanand.

**Task ID:** SLA-10-SB-3
**Task Title:** Final contribution record
**Priority:** P2
**Estimated Duration:** 2 h (docs 2)
**Dependencies:** `v1.0`
**Assigned Member:** Somesh Badwane

1–15. **What** regenerate the numbers in `docs/contributions.md` on `v1.0` with the Week-9 commands · **Why** final, verifiable record · **Files** `docs/contributions.md` · **Inputs** `git shortlog`, `gh pr list` · **Outputs** updated table with the commit sha used · **Steps** run commands → update table → all 4 members approve · **Commands** Week-9 Section 5.6 · **Tests** numbers reproducible · **Expected** 4 approvals · **Common errors** editing numbers by hand · **Branch** `docs/somesh-108-contributions-final` · **Commit** `docs: final contribution record` · **PR** `docs: final contributions (SLA-10-SB-3)` · **Acceptance** reviewer Atharv.

**Independent practice exercise (viva preparation):** explain your CSV export to a teammate in 2 minutes without notes: what problem it solves, the two functions, how the join works, and the three tests.

---

## SECTION 5 — COMPLETE TECHNICAL IMPLEMENTATION

### 5.1 Regression check and demo script (Brahmanand)

`scripts/regression_check.py`
```python
"""Regression check before v1.0: re-evaluate every final run and compare with the manifest (Brahmanand, W10).

Run:  python scripts/regression_check.py --manifest results/manifest.csv
Same code + same checkpoint + same test seeds must give the same score as recorded in Week 8.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from sla.evaluation.evaluate import TEST_SEED_BASE, evaluate_checkpoint
from sla.utils.config import load_config


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="results/manifest.csv")
    parser.add_argument("--episodes", type=int, default=100, help="must match the Week-8 final evaluation")
    args = parser.parse_args()
    manifest = pd.read_csv(args.manifest)
    rows = []
    for r in manifest.itertuples():
        run_dir = Path(r.run_dir)
        cfg = load_config(run_dir / "config.yaml")
        res = evaluate_checkpoint(run_dir / "checkpoints" / "best", cfg.env_name, cfg.env_kwargs, args.episodes,
                                  seed_base=TEST_SEED_BASE)
        rows.append({"label": r.label, "seed": r.seed, "run_id": r.run_id, "manifest_mean": r.final_mean,
                     "recheck_mean": res.mean_return, "same": abs(res.mean_return - r.final_mean) < 1e-6})
    table = pd.DataFrame(rows)
    print(table.to_string(index=False))
    print("ALL MATCH" if table["same"].all() else "MISMATCH - investigate before tagging v1.0")


if __name__ == "__main__":
    main()
```

**Dry run first** (on any laptop, takes about a minute): make a small FrozenLake manifest and check it:
```bash
python scripts/run_final_experiments.py --config configs/frozenlake_q.yaml --label dryrun --seeds 0 --manifest runs/dryrun_manifest.csv
python scripts/regression_check.py --manifest runs/dryrun_manifest.csv      # expect: ALL MATCH
```

`results/regression_check.md` template:
```markdown
# Regression check (commit <sha>, laptop <name>, date <date>)
Command: python scripts/regression_check.py --manifest results/manifest.csv
<copied output table>
Result: ALL MATCH / mismatches explained below
pytest on the same commit: <N passed, M skipped>
```

`demo/demo_script.md` template (~8 minutes):
```markdown
# Live demo script (v1.0)
Before: laptop charged, notifications off, Wi-Fi OFF, Ollama not running, terminal + browser zoom 125 %,
        fresh clone of v1.0 installed, backup run folder copied to runs/ (pre-trained DQN), video link ready.
| Time | Who | Action | What the audience sees | Backup if it fails |
|---|---|---|---|---|
| 0:00 | Brahmanand | Problem and idea (1 slide) | - | - |
| 1:00 | Brahmanand | `sla --help` | the commands | screenshot slide |
| 1:30 | Somesh | `sla dashboard` -> Train FrozenLake, 300 episodes | spinner, then score, plots, note | video 0:40-1:30 |
| 3:00 | Somesh | Results page: curve, eval, end reasons, CSV download | learning curve rising | screenshots |
| 4:00 | Vedant | Reflection page: grounded note, rating | note + "grounded" badge | screenshot |
| 5:00 | Atharv | Results page: pre-trained DQN run; `results/final_table.md`, ablation | final numbers from files | slide |
| 6:30 | Brahmanand | `sla evaluate --checkpoint <backup run>/checkpoints/best` | same score as in the table | slide |
| 7:30 | All | Limitations + questions | - | - |
```

### 5.2 Final review and viva questions (Atharv)

Final review checklist (paste into issue #104 and tick):
```markdown
- [ ] CI green on main; `ruff check .` clean
- [ ] `pytest` passes locally on 2 laptops (one Windows if available)
- [ ] regression check: ALL MATCH (results/regression_check.md)
- [ ] no secrets/keys in the repo (search for "key", "token", "password"); `.env` not committed
- [ ] no large files committed (runs/, *.pt, *.db, *.mp4 absent)
- [ ] README: quickstart, commands, results link, demo video link, licence, team
- [ ] module names in docs = names in src/ (no renamed modules)
- [ ] CHANGELOG [v1.0] section written from merged PRs
- [ ] licences doc complete; Ollama documented as optional
- [ ] tag v1.0 on the final merge commit; GitHub Release with report PDF, slides, links
```

`docs/viva_questions.md` structure (owners write the answers for their sections; each answer names a file):
```markdown
# Viva question bank
## Whole system (everyone)
1. What problem does the project solve, and what does "self-learning" mean here?
2. Draw the architecture and follow one training step through the modules.
3. How do you know the agent learned? (protocol, test seeds, baselines, 5 seeds)
4. What are the main limitations?
5. Why is the cost Rs 0, and what runs offline?
## Agent, runner, checkpoints, pipeline (Brahmanand)
6. Why callbacks? 7. How is resume exact? 8. What does metrics.json contain and why the git sha?
## Learning: Q-learning, DQN, guards, ablation (Atharv)
9. Write the Q-learning update. 10. Why replay and a target network? 11. Terminated vs truncated?
12. What did the ablation show? 13. Divergence vs regression?
## Memory, evaluation, reflection (Vedant)
14. Short-term vs long-term memory. 15. The three seed ranges. 16. How grounding stops hallucinated numbers.
17. What do the CI and p-value in the final table mean?
## Validation, plots, UI, export (Somesh)
18. Why check bool before int? 19. What does the rolling mean show? 20. How does the Train page call the pipeline?
21. How does the CSV export join evaluation scores? 22. Which UI bug did you fix and how is it tested?
## Ethics and honesty
23. How did you make sure no result was invented or cherry-picked?
24. Why is the LLM optional, and what happens when it gives a wrong number?
(extend to 40+ questions; add the follow-up questions asked in mock vivas)
```

### 5.3 Evidence pack (Vedant)

`demo/evidence/README.md` template:
```markdown
# Evidence pack (v1.0)
| Claim | Evidence | Link / file |
|---|---|---|
| Code is tested | CI run on v1.0; test report | <CI link>; results/test_report.md |
| Agent learns (vs baseline) | final table, 5 seeds, test seeds | results/final_table.md; results/manifest.csv |
| Results reproducible | regression check | results/regression_check.md |
| Components matter | ablation | results/ablation/summary.csv; docs/notes/ablation_notes.md |
| Runs offline, Rs 0 | clean-install test; licences | docs/clean_install_test.md; docs/licences.md |
| Team contributions | merged PRs and commits | docs/contributions.md; <PR list link> |
| Working demo | video | demo/demo_video_link.md |
```

### 5.4 CSV export (Somesh)

**Lesson:**
```python
import pandas as pd
left = pd.DataFrame({"episode": [0, 1, 2], "total_reward": [1.0, 2.0, 3.0]})
right = pd.DataFrame({"episode": [2], "eval_mean": [9.0]})
left.merge(right, on="episode", how="left")
#    episode  total_reward  eval_mean
# 0        0           1.0        NaN     <- no evaluation at this episode (stays empty)
# 1        1           2.0        NaN
# 2        2           3.0        9.0
left.to_csv(index=False)                  # 'episode,total_reward\n0,1.0\n...'  (text)
left.to_csv(index=False).encode("utf-8")  # the same as bytes - what a download button needs
```
Mini-exercises: (a) merge two small tables of your own with `how="left"` and `how="inner"` — what is the difference? (b) save a DataFrame to `test.csv` and open it in a spreadsheet program.

`src/sla/ui/export.py`
```python
"""CSV export for the Results page (owner: Somesh, Week 10 independent enhancement)."""

from __future__ import annotations

import pandas as pd

from sla.utils.validation import safe_run_name


def results_to_csv(episodes: pd.DataFrame, evals: pd.DataFrame | None = None) -> bytes:
    """One CSV: every episode row, with the evaluation score joined on the matching episode."""
    if episodes.empty:
        raise ValueError("No episodes to export")
    table = episodes.copy()
    if evals is not None and not evals.empty:
        ev = evals[["checkpoint_episode", "mean_return", "std_return"]].rename(
            columns={"checkpoint_episode": "episode", "mean_return": "eval_mean", "std_return": "eval_std"})
        table = table.merge(ev, on="episode", how="left")
    return table.to_csv(index=False).encode("utf-8")


def export_filename(run_id: str) -> str:
    return f"{safe_run_name(run_id)}_results.csv"
```

**Line by line:** `if episodes.empty: raise ValueError(...)` — an empty export would only confuse users · `episodes.copy()` — never change the caller's table · `rename(columns=...)` turns `checkpoint_episode` into `episode` so the two tables can be joined · `merge(..., how="left")` keeps every episode and fills evaluation columns only where an evaluation happened · `export_filename` reuses your `safe_run_name`, so a strange run id cannot create a dangerous file name.

`tests/unit/test_export.py`
```python
import pandas as pd
import pytest

from sla.ui.export import export_filename, results_to_csv


def test_csv_contains_episodes_and_eval_columns():
    episodes = pd.DataFrame({"episode": [0, 1, 2], "total_reward": [1.0, 2.0, 3.0]})
    evals = pd.DataFrame({"checkpoint_episode": [2], "mean_return": [9.0], "std_return": [1.0]})
    text = results_to_csv(episodes, evals).decode("utf-8")
    lines = text.strip().splitlines()
    assert lines[0] == "episode,total_reward,eval_mean,eval_std" and lines[3] == "2,3.0,9.0,1.0"


def test_empty_episodes_rejected():
    with pytest.raises(ValueError):
        results_to_csv(pd.DataFrame())


def test_filename_is_safe():
    assert export_filename("../run 1") == "run_1_results.csv"
```

`src/sla/ui/pages/2_Results.py` — add this region at the **end** of the Week-7 file:
```python
from sla.ui.export import export_filename, results_to_csv  # noqa: E402

st.download_button("Download results as CSV", data=results_to_csv(episodes, evals),
                   file_name=export_filename(run_id), mime="text/csv")
```

Complete `2_Results.py` after Week 10:
```python
"""Results page: learning curves and evaluation for a chosen run (owner: Somesh, Weeks 7 and 10)."""

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

# region W10: CSV export (Somesh's independent enhancement)
from sla.ui.export import export_filename, results_to_csv  # noqa: E402

st.download_button("Download results as CSV", data=results_to_csv(episodes, evals),
                   file_name=export_filename(run_id), mime="text/csv")
# endregion
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
├── demo/
│   ├── evidence/   [NEW · Vedant]
│   ├── demo_script.md   [NEW · Brahmanand]
│   └── demo_video_link.md   [NEW · Somesh]
├── docs/
│   ├── modules/
│   │   ├── agent.md
│   │   ├── learning.md
│   │   ├── memory_evaluation_reflection.md
│   │   └── ui.md
│   ├── notes/
│   │   ├── ablation_notes.md
│   │   ├── dqn_debug_checklist.md
│   │   ├── dqn_explained.md
│   │   ├── q_learning_by_hand.md
│   │   └── week6_results.md
│   ├── screenshots/
│   ├── architecture.md
│   ├── clean_install_test.md
│   ├── contributions.md   [MODIFIED · Somesh]
│   ├── data_handling.md
│   ├── design.md
│   ├── evaluation_protocol.md
│   ├── feasibility.md
│   ├── hardware_audit.md
│   ├── learning_plans.md
│   ├── licences.md
│   ├── literature_review.md
│   ├── nfr.md
│   ├── report_outline.md
│   ├── requirements.md
│   ├── synopsis_draft.md
│   ├── synopsis_outline.md
│   ├── tech_stack.md
│   ├── use_cases.md
│   ├── user_guide.md
│   └── viva_questions.md   [NEW · Atharv]
├── report/
│   ├── figures/
│   ├── chapter_4.docx   [MODIFIED · Atharv]
│   ├── chapters_1-3.docx   [MODIFIED · Brahmanand]
│   ├── chapters_5-6.docx   [MODIFIED · Vedant]
│   └── final_report.docx   [NEW · Vedant]
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
│   ├── regression_check.md   [NEW · Brahmanand]
│   └── test_report.md
├── scripts/
│   ├── failure_analysis.py
│   ├── hardware_check.py
│   ├── make_tables.py
│   ├── measure_performance.py
│   ├── quick_frozenlake_check.py
│   ├── regression_check.py   [NEW · Brahmanand]
│   ├── run_ablation.py
│   ├── run_baseline.py
│   └── run_final_experiments.py
├── slides/
│   ├── draft.pptx
│   └── final.pptx   [NEW · Somesh]
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
│       │   │   ├── 2_Results.py   [MODIFIED · Somesh]
│       │   │   └── 3_Reflection.py
│       │   ├── __init__.py
│       │   ├── app.py
│       │   ├── common.py
│       │   ├── export.py   [NEW · Somesh]
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
│   │   ├── test_export.py   [NEW · Somesh]
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
├── CHANGELOG.md   [MODIFIED · Atharv]
├── CONTRIBUTING.md
├── pyproject.toml
└── README.md   [MODIFIED · Atharv → Brahmanand]
```

Legend: [NEW] created this week · [MODIFIED] changed this week · no tag = carried over unchanged from an earlier week. `runs/` (training outputs) and `.venv/` exist on your laptop but are git-ignored, so they are not shown.

---

## SECTION 7 — GITHUB COLLABORATION PROCEDURE

13-step flow as every week. After `v1.0` is tagged (Day 4), only documentation PRs are merged.

| # | Title | Owner | Branch | Reviewer | Merge by |
|---|---|---|---|---|---|
| 101 | CSV export (independent enhancement) | Somesh | `feat/somesh-101-csv-export` | Vedant | **Day 3** |
| 102 | Final regression check | Brahmanand | `test/brahmanand-102-regression-check` | Atharv | **Day 4** |
| 103 | Demo script | Brahmanand | `docs/brahmanand-103-demo-script` | Vedant | Day 5 |
| 104 | Final review + v1.0 release | Atharv | `docs/atharv-104-release-v1` | Brahmanand | **Day 4** |
| 105 | Viva question bank | Atharv (+ all) | `docs/atharv-105-viva-questions` | Vedant | Day 5 |
| 106 | Final report + evidence pack | Vedant | `docs/vedant-106-final-report`, `docs/vedant-106-evidence` | Brahmanand / Atharv | Day 6 |
| 107 | Demo video + final slides | Somesh | `docs/somesh-107-video-slides` | Brahmanand | Day 6 |
| 108 | Final contributions | Somesh | `docs/somesh-108-contributions-final` | Atharv | Day 6 |

**Publishing the final release:** Releases → Draft a new release → tag `v1.0` → title "v1.0 — Final submission" → paste CHANGELOG `[v1.0]` → attach `final_report.pdf` and `final.pptx` → Publish (not a pre-release).

---

## SECTION 8 — WEEKLY INTEGRATION PROCEDURE

| Item | This week |
|---|---|
| What to integrate | CSV export into the Results page; regression result into the release; report + slides + video + evidence into the release. |
| Integrator | **Atharv** (final review lead). |
| Interfaces that must match | `results_to_csv(episodes, evals)` uses `query_episodes` / `query_evals` columns; regression script uses manifest columns `run_dir`, `final_mean`, `label`, `seed`, `run_id`. |
| Tests that must pass | all, including `test_export.py` and UI tests; regression check. |
| Detect failures | regression "MISMATCH"; UI test failure after the export region; demo fails on a fresh clone. |
| Debug | `git log v0.8-experiments..v1.0 -- src/` shows every code change since the experiments; check each one could not affect training/evaluation. |

**Integration checklist**
- [ ] Export merged; only `ui/` files and its test changed
- [ ] Regression check: ALL MATCH
- [ ] `v1.0` tagged on a green commit; release published
- [ ] Fresh clone of `v1.0` demo works offline with Ollama off
- [ ] Report, slides, video link, evidence pack attached/linked

---

## SECTION 9 — TESTING AND VALIDATION

| Type | This week | Command |
|---|---|---|
| Unit | `test_export` (3) + all earlier unit tests | `pytest tests/unit -v` |
| UI | 5 AppTest tests (Results page now has the export region) | `pytest tests/ui -v` |
| Regression | re-evaluate every final run on test seeds | `python scripts/regression_check.py` |
| End-to-end | fresh clone of `v1.0`, offline | Week-9 clean-install procedure |
| Demo | two timed rehearsals | `demo/demo_script.md` |

**RL rules (final):** the demo and report use only the recorded final runs (test seeds, frozen policy, no learning during evaluation, compared with baselines); a live demo run is labelled "live example", never presented as a result; no number is changed to match expectations.

---

## SECTION 10 — COMMON PROBLEMS AND SOLUTIONS

| Problem | Possible Cause | How to Check | Solution |
|---|---|---|---|
| Regression MISMATCH on the same laptop | code changed after `v0.8-experiments` affecting evaluation | `git log v0.8-experiments..HEAD -- src/` | revert or fix; re-run affected experiments on a new tag; document |
| Small DQN difference on another laptop | CPU/library floating-point differences | run on the original laptop | record laptop; same-laptop check is the reference |
| `run_dir` not found | final runs live on another laptop | path in manifest | run there, or copy that run folder to the same relative path |
| Download button missing | region added inside an `st.stop()` branch | read page | put the region at the very end of the page |
| Demo laptop has no internet | expected | — | the core system is offline; Ollama off; use local backup run |
| Projector shows tiny text | resolution | — | browser zoom 125 %, terminal font 16 pt |
| Report PDF numbering broken | fields not updated | print preview | update all fields before exporting |
| Mock viva answers vague | not tied to files | ask "show me where" | every answer names a file or a result |

---

## SECTION 11 — WEEKLY DELIVERABLES

| Deliverable | Owner | File/Location | Verification | Status |
|---|---|---|---|---|
| Regression check | Brahmanand | `scripts/regression_check.py`, `results/regression_check.md` | ALL MATCH | [ ] |
| Demo script | Brahmanand | `demo/demo_script.md` | 2 rehearsals ≤ 8 min | [ ] |
| Final review + `v1.0` | Atharv | `CHANGELOG.md`, tag `v1.0`, GitHub Release | checklist complete | [ ] |
| Viva question bank + 2 mocks | Atharv (+ all) | `docs/viva_questions.md` | all members pass mock 2 | [ ] |
| Final report | Vedant | `report/final_report.docx` (+ PDF on release) | 10-number check | [ ] |
| Evidence pack | Vedant | `demo/evidence/` | all links open | [ ] |
| CSV export | Somesh | `src/sla/ui/export.py`, `2_Results.py` (W10), `tests/unit/test_export.py` | 3 tests; works in UI | [ ] |
| Demo video + final slides | Somesh | `demo/demo_video_link.md`, `slides/final.pptx` | link plays; numbers match | [ ] |
| Final contributions | Somesh | `docs/contributions.md` | 4 approvals | [ ] |

---

## SECTION 12 — WEEKLY REVIEW MEETING

**Agenda:** dress rehearsal (presentation + demo, timed) · regression result · release check · report sign-off · viva readiness · submission checklist.

**Questions:**
1. Brahmanand: what does the regression check prove, and what would you do if one row did not match?
2. Atharv: which commit is `v1.0`, and what changed since `v0.9-rc`?
3. Vedant: pick any number in the final report — show its source file and commit.
4. Somesh: demonstrate the CSV export and explain how the evaluation scores are joined to episodes.
5. If the live demo fails, what is the backup at each step?
6. What are the three main limitations, and what is the most valuable future work?
7. Each member: explain one module you did **not** write.
8. Is anything in the submission not backed by a file in the repository?

---

## SECTION 13 — WEEK COMPLETION CHECKLIST

- [ ] All assigned tasks completed
- [ ] Code and documents pushed to feature branches
- [ ] Pull requests reviewed and merged (export and regression before `v1.0`)
- [ ] All tests pass locally and in CI on `v1.0`
- [ ] Final system integrated; fresh-clone offline demo works
- [ ] Documentation final (README, report, slides, user guide, contributions, CHANGELOG)
- [ ] Final demonstration rehearsed and delivered
- [ ] Remaining limitations recorded in the report

---

## SECTION 14 — NEXT WEEK HANDOFF

This is the final week; the "handoff" is to the examiners and to future students.

- **Submitted:** tag `v1.0` (code, configs, tests, docs, `results/`), GitHub Release (report PDF, slides), demo video link, evidence pack.
- **Files a future team would start from:** `README.md`, `docs/user_guide.md`, `docs/modules/*.md`, `docs/design.md`, `CONTRIBUTING.md`, `docs/viva_questions.md`.
- **Possible future work (from the report):** more environments (e.g. LunarLander via Gymnasium Box2D — free), Double/Dueling DQN, more seeds, a learning-rate study, LLM-note evaluation with more raters — each would start from the callback-based runner without changing it.
- **Risks after submission:** keep the repository accessible until results are announced; do not force-push or delete tags.
