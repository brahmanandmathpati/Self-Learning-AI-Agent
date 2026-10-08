"""Grounding validator: reject notes that contain numbers not found in the facts."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any

NUMBER_RE = re.compile(r"-?\d+(?:\.\d+)?")
# Small whole numbers ("two seeds", "step 3") are allowed without a matching fact.
ALWAYS_ALLOWED = {float(n) for n in range(0, 11)}


@dataclass
class GroundingReport:
    passed: bool
    numbers_found: list[float] = field(default_factory=list)
    unsupported: list[float] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def extract_numbers(text: str) -> list[float]:
    """All numbers in a text, e.g. 'mean 23.5 over 1,000 episodes' -> [23.5, 1000.0]."""
    cleaned = re.sub(r"(?<=\d),(?=\d{3})", "", text)
    return [float(m) for m in NUMBER_RE.findall(cleaned)]


def fact_numbers(facts: Any) -> set[float]:
    """Every number that appears anywhere in the facts (including inside strings like '1-50')."""
    found: set[float] = set()
    if isinstance(facts, bool):
        return found
    if isinstance(facts, (int, float)):
        found.add(float(facts))
        found.add(abs(float(facts)))
    elif isinstance(facts, str):
        found.update(abs(v) for v in extract_numbers(facts))
    elif isinstance(facts, dict):
        for value in facts.values():
            found |= fact_numbers(value)
    elif isinstance(facts, (list, tuple)):
        for value in facts:
            found |= fact_numbers(value)
    return found


def check_grounding(text: str, facts: dict[str, Any], tolerance: float = 0.01) -> GroundingReport:
    """Pass only if every number in ``text`` matches a fact within ``tolerance`` (relative)."""
    allowed = fact_numbers(facts) | ALWAYS_ALLOWED
    numbers = extract_numbers(text)
    unsupported = []
    for number in numbers:
        value = abs(number)
        if not any(abs(value - f) <= tolerance * max(1.0, abs(f)) for f in allowed):
            unsupported.append(number)
    return GroundingReport(passed=not unsupported, numbers_found=numbers, unsupported=unsupported)
