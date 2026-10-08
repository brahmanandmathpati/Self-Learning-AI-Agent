"""Deterministic template note: works with no LLM at all and uses only values from the facts."""

from __future__ import annotations

from typing import Any


def template_note(facts: dict[str, Any]) -> str:
    """Build a plain-English summary using only values from ``facts``."""
    lines = [
        f"The {facts['agent']} agent trained on {facts['env']} for {facts['total_episodes']} episodes.",
        (f"Mean training reward was {facts['first_window_mean']} in episodes {facts['windows'][0]['episodes']} "
         f"and {facts['last_window_mean']} in episodes {facts['windows'][-1]['episodes']} "
         f"(change: {facts['change']})."),
    ]
    if facts["change"] > 0:
        lines.append("Training reward went up, which is consistent with learning.")
    elif facts["change"] < 0:
        lines.append("Training reward went down; check the learning curve and settings.")
    else:
        lines.append("Training reward did not change between the first and last windows.")
    if "untrained_test_mean" in facts and "test_mean" in facts:
        lines.append(f"On held-out test seeds the untrained policy scored {facts['untrained_test_mean']} "
                     f"and the trained policy scored {facts['test_mean']} (std {facts['test_std']}).")
    elif "test_mean" in facts:
        lines.append(f"On held-out test seeds the trained policy scored {facts['test_mean']} "
                     f"(std {facts['test_std']}).")
    if "random_baseline_mean" in facts:
        lines.append(f"The random baseline averaged {facts['random_baseline_mean']} on the same seeds.")
    if "welch_p_value_vs_random" in facts:
        low, high = facts["diff_vs_random_ci95"]
        lines.append(f"Across {facts['n_seeds']} seeds, Welch's t-test against random gave p = "
                     f"{facts['welch_p_value_vs_random']} and the bootstrap interval for the difference "
                     f"was {low} to {high}.")
    if "best_validation_mean" in facts:
        lines.append(f"The best validation score was {facts['best_validation_mean']} "
                     f"after episode {facts['best_validation_after_episode']}.")
    reasons = facts.get("end_reasons", {})
    if reasons:
        top = max(reasons, key=reasons.get)
        lines.append(f"The most common way episodes ended was '{top}' ({reasons[top]} episodes).")
    return " ".join(lines)
