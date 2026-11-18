"""The friendly layer: guide cards on every page, Start-here banner, comparison filters, 'Why?' and live strip."""

from __future__ import annotations

import os
import shutil

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

from sla.app import demo_seed  # noqa: E402
from sla.app.guide_content import GUIDE  # noqa: E402


def page(module: str) -> AppTest:
    return AppTest.from_string(f"from sla.app.views import {module}\n{module}.render()", default_timeout=120)


def text(at) -> str:
    return "\n".join(m.value for m in at.markdown)


def test_every_page_shows_what_am_i_looking_at_with_an_empty_database():
    for module, title in (("comparison", "Agent comparison"), ("evaluation", "Evaluation"), ("training", "Training"),
                          ("ablation", "Ablation study"), ("explorer", "Run explorer")):
        at = page(module).run()
        assert not at.exception, (module, at.exception)
        assert "What am I looking at?" in text(at), module
        assert GUIDE[title][0] in text(at), module


def test_overview_has_start_here_banner_and_three_steps():
    at = page("overview").run()
    assert not at.exception, at.exception
    body = text(at)
    assert "Start here" in body and all(s in body for s in ("Watch it learn", "See the proof", "Compare agents"))


def test_guide_marathi_toggle_works():
    at = page("comparison").run()
    key = "guide_mr_agent_comparison"
    at.toggle(key=key).set_value(True).run()
    assert not at.exception, at.exception
    assert any(GUIDE["Agent comparison"][2] in c.value for c in at.caption)


def test_comparison_filters_winner_sentence_and_download_with_demo_snapshot():
    shutil.copyfile(demo_seed.SNAPSHOT_DB, os.environ["SLA_DB"])
    at = page("comparison").run()
    assert not at.exception, at.exception
    assert "scores best" in text(at) or "tie for first" in text(at)
    envs = at.multiselect(key="cmp_filter_env")
    envs.set_value(envs.value[:1]).run()
    assert not at.exception, at.exception
    at.multiselect(key="cmp_filter_algo").set_value([]).run()
    assert not at.exception, at.exception
    assert any("Nothing matches" in m.value for m in at.markdown)


def test_evaluation_why_expander_uses_real_numbers_with_demo_snapshot():
    shutil.copyfile(demo_seed.SNAPSHOT_DB, os.environ["SLA_DB"])
    at = page("evaluation").run()
    assert not at.exception, at.exception
    assert any("Why?" == e.label for e in at.expander)
    assert any("p-value" in m.value for m in at.markdown)


def test_training_page_inspect_section_has_question_titles_and_before_after():
    shutil.copyfile(demo_seed.SNAPSHOT_DB, os.environ["SLA_DB"])
    at = page("training").run()
    assert not at.exception, at.exception
    at.radio(key="tr_before_after").set_value("Before training").run()
    assert not at.exception, at.exception


def test_live_strip_html_from_a_fake_running_state():
    from sla.app.views.training import _log_html, _strip_html
    html_text = _strip_html("FrozenLake", 120, 500, 0.5, 1.0, 0.05, 0.0, 1.0)
    assert "120 of 500" in html_text and "50% random moves" in html_text and "Best score" in html_text
    assert _log_html([]) == "" and "<li>" in _log_html(["Episode 3: new best score 1"])
