"""Project-wide exception classes.

Every module raises one of these instead of a bare Exception, so callers
(CLI, UI, pipeline) can show a clear message for each kind of failure.
"""


class SLAError(Exception):
    """Base class for all errors raised by the sla package."""


class ConfigError(SLAError):
    """A configuration file or value is missing or invalid."""


class ValidationError(SLAError):
    """User input or a runtime value failed validation."""


class EnvError(SLAError):
    """An environment could not be created or behaved unexpectedly."""


class CheckpointError(SLAError):
    """A checkpoint could not be saved or loaded."""


class StoreError(SLAError):
    """The SQLite episode store could not be read or written."""


class LLMError(SLAError):
    """The optional local LLM (Ollama) is unavailable or returned an error."""


class TrainingError(SLAError):
    """Training was stopped by a safety limit or a learning guard."""
