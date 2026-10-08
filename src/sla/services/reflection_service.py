"""Grounded reflection notes and their ratings."""

from __future__ import annotations

from typing import Any

from sla.database.store import Database
from sla.reflection.llm_client import OllamaClient
from sla.reflection.reflect import ReflectionResult, reflect
from sla.reflection.stats import compute_facts


class ReflectionService:
    def __init__(self, db: Database) -> None:
        self.db = db

    def facts(self, run_id: str) -> dict[str, Any]:
        return compute_facts(self.db, run_id)

    def generate(self, run_id: str, use_llm: bool = False, client: OllamaClient | None = None) -> ReflectionResult:
        return reflect(self.db, run_id, use_llm=use_llm, client=client)

    @staticmethod
    def llm_available() -> bool:
        return OllamaClient().is_available()

    def notes(self, run_id: str | None = None):
        return self.db.query_reflections(run_id)

    def rate(self, note_id: int, accurate: bool, usefulness: int, comment: str | None = None) -> int:
        from sla.reflection.feedback import save_rating
        return save_rating(self.db, note_id, accurate, usefulness, comment)
