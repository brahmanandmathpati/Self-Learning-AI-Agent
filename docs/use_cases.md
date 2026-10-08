# Use Cases — Self-Learning AI Agent
**Owner:** Vedant Biradar · **Task:** SLA-01-VB-1 · **Week:** 1  

Each use case lists the actor, what starts it, the steps, the result, and the requirements (REQ IDs from docs/requirements.md) it depends on.

---

## UC-1 Train an agent
- **Actor:** student / examiner
- **Trigger:** clicks "Start training" in the UI or runs `sla train --config configs/frozenlake_q.yaml`
- **Steps:**
  1. The config file is validated.
  2. The environment is created with a seed.
  3. The agent trains for N episodes.
  4. Every episode is stored in the database.
  5. Checkpoints are saved during training.
  6. A final evaluation runs on fixed test seeds.
- **Result:** a run id, the final mean return ± std, and a learning-curve plot.
- **Related requirements:** REQ-01, REQ-03, REQ-05, REQ-07, REQ-10, REQ-11, REQ-12, REQ-17

---

## UC-2 View proof of learning
- **Actor:** student / examiner
- **Trigger:** opens a finished run in the UI (or runs the evaluation command) and asks "did the agent really learn?"
- **Steps:**
  1. The system loads the saved (frozen) trained policy.
  2. It evaluates that policy on fixed test seeds with epsilon = 0 and no updates.
  3. It evaluates the random-agent baseline and the untrained checkpoint (checkpoint 0) on the same seeds.
  4. It repeats this for 5 training seeds.
  5. It shows the comparison table, the statistics (Welch t-test, bootstrap confidence interval) and the learning curves.
- **Result:** a clear table and plot showing trained vs random vs untrained, with the statistical result.
- **Related requirements:** REQ-04, REQ-12, REQ-13, REQ-16, REQ-17, REQ-20

---

## UC-3 Read the explanation
- **Actor:** student / examiner
- **Trigger:** clicks "Explain this run" on a finished run in the UI.
- **Steps:**
  1. The system reads the logged numbers of the run (returns, epsilon, loss, evaluation results).
  2. It builds a plain-language note based only on those logged numbers.
  3. If the optional local LLM (Ollama) is available, it uses it to word the note; otherwise it uses the template fallback.
  4. The note is shown next to the learning curve.
- **Result:** a short note in plain language whose numbers all match the stored run.
- **Related requirements:** REQ-10, REQ-17, REQ-18, REQ-19 (optional)

---

## UC-4 Rate the explanation
- **Actor:** student / examiner
- **Trigger:** clicks a rating (for example 1-5) under an explanation note.
- **Steps:**
  1. The user picks a rating, and optionally writes a comment.
  2. The system saves the rating with the run id and the note.
  3. The UI confirms that the rating was saved.
- **Result:** the rating is stored and still there after restarting the program.
- **Related requirements:** REQ-10, REQ-17, REQ-18