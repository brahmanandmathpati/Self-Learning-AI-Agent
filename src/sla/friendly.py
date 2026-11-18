"""Plain-language helpers for the website's friendly layer (no Streamlit, database or PyTorch imports).

They turn raw numbers (epsilon, test means) into short sentences, so every sentence shown on a page is computed from
real data instead of being typed in.
"""

from __future__ import annotations

from collections.abc import Sequence

# Share of the epsilon decay (start -> end) at which the phase label changes.
PHASE_CUTS = (0.35, 0.9)

PHASES = {
    "exploring": "Exploring (mostly random moves)",
    "learning": "Learning (mixing random and best-known moves)",
    "exploiting": "Mostly using what it learned",
}


def epsilon_in_words(eps: float | None) -> str:
    """'30% random moves, 70% best-known moves' for an epsilon value."""
    if eps is None:
        return "not available"
    random_pct = round(100 * min(max(float(eps), 0.0), 1.0))
    return f"{random_pct}% random moves, {100 - random_pct}% best-known moves"


def phase_for(eps: float, start: float, end: float) -> tuple[str, str]:
    """(key, label) of the training phase, from how far epsilon has fallen between its start and end value."""
    span = float(start) - float(end)
    if span <= 1e-12:  # a fixed exploration rate (for example CliffWalking)
        progress = 1.0 if float(eps) < 0.5 else 0.0
    else:
        progress = min(max((float(start) - float(eps)) / span, 0.0), 1.0)
    key = "exploring" if progress < PHASE_CUTS[0] else "learning" if progress < PHASE_CUTS[1] else "exploiting"
    return key, PHASES[key]


def phase_change_event(previous: str | None, key: str, episode: int) -> str | None:
    """A log line when the phase changes (None for the first episode or when nothing changed)."""
    if previous is None or previous == key:
        return None
    return f"Episode {episode:,}: now {PHASES[key].lower()}"


def best_score_event(episode: int, reward: float, best_so_far: float | None) -> tuple[str | None, float]:
    """(log line, new best). A line is returned only when ``reward`` beats the best score seen so far."""
    if best_so_far is None or reward > best_so_far:
        if best_so_far is None:
            return None, float(reward)
        return f"Episode {episode:,}: new best score {reward:,.4g}", float(reward)
    return None, float(best_so_far)


def winner_sentence(env: str, rows: Sequence[tuple[str, float]], random_label: str = "Random") -> str | None:
    """One sentence about the best agent on a game, from (label, mean test return) pairs. None if there is no data."""
    rows = [(str(label), float(mean)) for label, mean in rows if mean == mean]  # drop NaN
    if not rows:
        return None
    best = max(mean for _, mean in rows)
    tied = [label for label, mean in rows if abs(mean - best) < 1e-9]
    rnd = next((mean for label, mean in rows if label == random_label), None)
    if len(tied) > 1:
        names = ", ".join(tied[:-1]) + " and " + tied[-1]
        lead = f"On {env}, {names} tie for first with a mean test score of {best:,.2f}"
    else:
        lead = f"On {env}, {tied[0]} scores best with a mean test score of {best:,.2f}"
    if rnd is None or tied == [random_label]:
        return lead + "."
    if rnd > 0:
        return lead + f", about {best / rnd:,.1f} times the random agent's {rnd:,.2f}."
    return lead + f", compared with {rnd:,.2f} for the random agent."


def before_after_sentence(before: float | None, after: float | None, what: str = "mean test score") -> str:
    """Before vs after training in one sentence (the numbers come from stored evaluations)."""
    if before is None or after is None:
        return "Not available yet: run a training run with a final test."
    change = after - before
    word = "improved" if change > 0 else "did not improve" if change == 0 else "got worse"
    return f"The {what} {word}: {before:,.2f} before training, {after:,.2f} after ({change:+,.2f})."


def verdict_why(p_value: float | None, ci_low: float | None, ci_high: float | None) -> list[str]:
    """Two plain-language lines that explain a p-value and a confidence interval with the real numbers."""
    if p_value is None or ci_low is None or ci_high is None:
        return ["Not available: the statistics need at least two trained seeds and two baseline seeds."]
    return [
        f"p-value {p_value:.3g}: if training had no real effect, a gap this big would show up about "
        f"{p_value * 1000:.1f} times in 1,000 repeats (below 0.05 counts as significant).",
        f"95% confidence interval [{ci_low:,.2f}, {ci_high:,.2f}]: the true gain very likely lies in this range; "
        "when the whole range is above 0 the gain is real, not luck.",
    ]
