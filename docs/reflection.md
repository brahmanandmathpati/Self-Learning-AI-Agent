# Reflection layer and grounding validator

Owner: Somesh Badwane (reflection layer, grounding validator, dashboard and demo).

After a run finishes, the agent can write a short plain-English note about how it did. The rule that matters most is
that **the note may never invent a number**. This page explains how the code in `src/sla/reflection/` enforces that.

## The pipeline in one line

`facts -> LLM or template -> grounding check -> store`

1. **Facts** (`stats.py`, `compute_facts`): numbers are read from the experiment database for one run (agent, game,
   episodes, mean reward per window, change between first and last window).
2. **Write the note** (`reflect.py`, `reflect`):
   - With the optional LLM switched on, `llm_client.py` asks a local Ollama model to write the note from the facts.
   - Without it, `fallback.py` (`template_note`) builds a fixed sentence template that uses only values from the facts.
     This works with no LLM at all.
3. **Grounding check** (`grounding.py`, `check_grounding`): every number in the note must also appear in the facts.
4. **Store**: the note, its facts and the grounding report are saved in the `reflections` table. If an LLM note fails
   the check, the template note is shown instead and the rejected LLM note is kept for transparency.

## How the grounding check works

- `extract_numbers` pulls every number out of the text, for example "mean 23.5 over 1,000 episodes" gives 23.5 and 1000.
- `fact_numbers` collects every number found anywhere in the facts, including numbers inside strings like "1-50".
- Any number in the note that is not in the facts is listed as `unsupported` and the note fails (`passed = False`).
- Small whole numbers from 0 to 10 are always allowed, so phrases like "two seeds" or "step 3" do not fail.

## Practice example

Facts: mean reward was 0.10 in the first window and 0.94 in the last window.

- Note A: "Reward rose from 0.10 to 0.94." Every number is in the facts, so it passes.
- Note B: "Reward rose from 0.10 to 0.99." The number 0.99 is not in the facts, so it is listed as unsupported and the
  note fails.

Try it: would "It improved by 0.84" pass? (Hint: check whether 0.84 is in the facts.)

## Where to look

| What | File |
|---|---|
| Facts for a run | `src/sla/reflection/stats.py` |
| Template note (no LLM) | `src/sla/reflection/fallback.py` |
| Optional Ollama client | `src/sla/reflection/llm_client.py` |
| Grounding validator | `src/sla/reflection/grounding.py` |
| Pipeline entry point | `src/sla/reflection/reflect.py` |
| User ratings of notes | `src/sla/reflection/feedback.py` |
