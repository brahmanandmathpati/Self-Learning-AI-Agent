"""Logging helpers.

Usage:
    from sla.utils.logging_setup import setup_logging, get_logger
    setup_logging(run_id="cartpole_dqn_s0", log_file=Path("runs/x/run.log"))
    log = get_logger(__name__)
    log.info("training started")
"""

from __future__ import annotations

import logging
from pathlib import Path

LOG_FORMAT = "%(asctime)s | %(levelname)-7s | run=%(run_id)s | %(name)s | %(message)s"
_ROOT = "sla"


class _RunIdFilter(logging.Filter):
    """Adds the current run id to every log record."""

    def __init__(self, run_id: str) -> None:
        super().__init__()
        self.run_id = run_id

    def filter(self, record: logging.LogRecord) -> bool:
        record.run_id = self.run_id
        return True


def setup_logging(run_id: str = "-", log_file: Path | None = None, level: str = "INFO") -> logging.Logger:
    """Configure the package logger once per run.

    Logs go to the console and, if ``log_file`` is given, to that file too.
    Calling it again replaces the previous handlers (safe in tests and the UI).
    """
    logger = logging.getLogger(_ROOT)
    logger.setLevel(level.upper())
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()
    for flt in list(logger.filters):
        logger.removeFilter(flt)

    formatter = logging.Formatter(LOG_FORMAT)
    run_filter = _RunIdFilter(run_id)

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    console.addFilter(run_filter)
    logger.addHandler(console)

    if log_file is not None:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.addFilter(run_filter)
        logger.addHandler(file_handler)

    logger.propagate = False
    return logger


def get_logger(name: str) -> logging.Logger:
    """Return a child logger of the package logger, e.g. ``sla.training.runner``."""
    if not name.startswith(_ROOT):
        name = f"{_ROOT}.{name}"
    return logging.getLogger(name)
