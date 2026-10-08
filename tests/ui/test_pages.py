"""Every dashboard page must render, both with an empty database and with real stored runs."""

from dataclasses import replace
from pathlib import Path

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

PAGES = ["overview", "training", "comparison", "evaluation", "ablation", "explorer", "reflection", "environment",
         "about"]


def page(name):
    return AppTest.from_string(f"from sla.app.views import {name}\n{name}.render()", default_timeout=60)


@pytest.mark.parametrize("name", PAGES)
def test_page_renders_with_empty_database(name):
    at = page(name).run()
    assert not at.exception, at.exception


@pytest.fixture
def filled_db(fl_cfg, tmp_path):
    import os

    from sla.database.store import Database
    from sla.training.pipeline import run_experiment
    db = Database(os.environ["SLA_DB"])
    run_experiment(replace(fl_cfg, episodes=150), [0, 1], db, final_eval_episodes=5)
    return db


@pytest.mark.parametrize("name", PAGES)
def test_page_renders_with_data(name, filled_db):
    at = page(name).run()
    assert not at.exception, at.exception


def test_overview_shows_not_run_when_empty():
    at = page("overview").run()
    assert any("NOT RUN" in m.value for m in at.markdown)


def test_main_app_navigation_renders():
    main = Path(__file__).resolve().parents[2] / "src" / "sla" / "app" / "main.py"
    at = AppTest.from_file(str(main), default_timeout=60).run()
    assert not at.exception, at.exception
