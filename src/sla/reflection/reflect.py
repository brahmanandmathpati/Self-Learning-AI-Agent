"""Reflection service: facts -> LLM or template -> grounding check -> store.

Addition to the master plan: this small module joins the four reflection
files so the pipeline and UI call one function.
"""

from __future__ import annotations

from dataclasses import dataclass

from sla.database.store import Database
from sla.reflection.fallback import template_note
from sla.reflection.grounding import GroundingReport, check_grounding
from sla.reflection.llm_client import OllamaClient, build_prompt
from sla.reflection.stats import compute_facts
from sla.utils.errors import LLMError
from sla.utils.logging_setup import get_logger

log = get_logger(__name__)


@dataclass
class Note:
    note_id: int
    text: str
    source: str  # "llm" or "template"
    report: GroundingReport


@dataclass
class ReflectionResult:
    shown: Note               # the note to display (always grounded)
    rejected: Note | None     # an LLM note that failed grounding, kept for transparency


def reflect(db: Database, run_id: str, use_llm: bool = False,
            client: OllamaClient | None = None) -> ReflectionResult:
    facts = compute_facts(db, run_id)
    rejected = None
    if use_llm:
        client = client or OllamaClient()
        try:
            text = client.generate(build_prompt(facts))
            report = check_grounding(text, facts)
            note_id = db.add_reflection(run_id, facts, text, "llm", report.passed, report.to_dict())
            note = Note(note_id, text, "llm", report)
            if report.passed:
                return ReflectionResult(note, None)
            log.warning("LLM note rejected: unsupported numbers %s", report.unsupported)
            rejected = note
        except LLMError as exc:
            log.warning("LLM unavailable (%s); using template note", exc)
    text = template_note(facts)
    report = check_grounding(text, facts)
    note_id = db.add_reflection(run_id, facts, text, "template", report.passed, report.to_dict())
    return ReflectionResult(Note(note_id, text, "template", report), rejected)
