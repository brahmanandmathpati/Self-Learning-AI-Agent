# Use Cases — Self-Learning AI Agent

## UC-1: Train an Agent
- **Actor:** Student / Examiner
- **Trigger:** Clicks "Start training" in the UI or runs `sla train --config configs/frozenlake_q.yaml`
- **Steps:**
  1. System validates the configuration YAML.
  2. Seeded environment (CartPole-v1 or FrozenLake-v1) is initialized.
  3. Agent interacts with the environment and updates parameters for N episodes.
  4. Episode statistics (steps, return, epsilon, loss) are persisted to the SQLite store.
  5. Checkpoints are saved periodically and when a new best evaluation score is achieved.
  6. Final evaluation runs on unseen test seeds with frozen policy.
- **Result:** Run ID generated, training metrics saved, learning curve displayed.
- **Related Requirements:** REQ-01, REQ-03, REQ-05, REQ-07, REQ-08, REQ-10, REQ-11, REQ-12, REQ-17

## UC-2: View Proof of Learning
- **Actor:** Student / Examiner / Evaluator
- **Trigger:** Opens evaluation tab in UI or runs `sla evaluate --run-id <id>`
- **Steps:**
  1. System fetches frozen-policy evaluation logs across 5 independent seeds.
  2. Calculates mean return, standard deviation, and 95% bootstrap confidence intervals.
  3. Compares trained agent performance against the random-action baseline and untrained checkpoint (epoch 0).
  4. Performs Welch's t-test to check statistical significance (p < 0.05).
- **Result:** Formatted comparison table and confidence interval plots proving genuine learning.
- **Related Requirements:** REQ-04, REQ-12, REQ-13, REQ-16, REQ-17

## UC-3: Read Grounded Explanation
- **Actor:** Student / Examiner
- **Trigger:** Selects a completed training run and requests an explanation summary.
- **Steps:**
  1. System extracts factual performance metrics from the SQLite database.
  2. Generates a natural language summary (via local Ollama model or rule-based template).
  3. Grounding validator scans generated text to ensure every number matches recorded facts.
  4. If validation passes, displays note; if unverified claims/numbers exist, rejects note and falls back to template.
- **Result:** Trustworthy plain-language summary of what the agent learned without hallucinations.
- **Related Requirements:** REQ-18, REQ-19

## UC-4: Rate the Explanation
- **Actor:** User / Examiner
- **Trigger:** User reads the generated explanation and clicks a rating (1 to 5 stars + feedback).
- **Steps:**
  1. User submits rating and optional textual feedback via the Streamlit UI.
  2. Feedback handler validates input and appends the rating record to the SQLite database linked to the explanation ID.
- **Result:** User feedback stored persistently for qualitative analysis (does not alter RL policy).
- **Related Requirements:** REQ-10, REQ-17