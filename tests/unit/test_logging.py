from sla.utils.errors import ConfigError, SLAError
from sla.utils.logging_setup import get_logger, setup_logging


def test_log_file_has_run_id(tmp_path):
    log_file = tmp_path / "run.log"
    setup_logging("run_42", log_file)
    get_logger("test").info("hello")
    text = log_file.read_text(encoding="utf-8")
    assert "run=run_42" in text and "hello" in text


def test_errors_are_sla_errors():
    assert issubclass(ConfigError, SLAError)
    assert str(ConfigError("bad gamma")) == "bad gamma"


def test_setup_twice_does_not_duplicate_lines(tmp_path):
    log_file = tmp_path / "run.log"
    setup_logging("a", log_file)
    setup_logging("a", log_file)
    get_logger("x").info("once")
    assert log_file.read_text(encoding="utf-8").count("once") == 1
