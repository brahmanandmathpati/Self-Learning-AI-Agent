"""Service layer used by the CLI and the Streamlit dashboard (the UI holds no business logic)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sla import settings
from sla.database.store import Database
from sla.services.checkpoint_service import CheckpointService
from sla.services.evaluation_service import EvaluationService
from sla.services.experiment_service import ExperimentService
from sla.services.reflection_service import ReflectionService
from sla.services.training_service import TrainingService


@dataclass
class Services:
    db: Database
    experiments: ExperimentService
    training: TrainingService
    evaluation: EvaluationService
    reflection: ReflectionService
    checkpoints: CheckpointService


def get_services(db_path: str | Path | None = None) -> Services:
    db = Database(db_path or settings.db_path())
    return Services(db, ExperimentService(db), TrainingService(db), EvaluationService(db),
                    ReflectionService(db), CheckpointService())
