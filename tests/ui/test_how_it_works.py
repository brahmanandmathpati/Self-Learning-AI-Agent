"""The 'How it works' page: guest view, demo snapshot, demo switch and the Marathi-English helper."""

from __future__ import annotations

import html
import os
import shutil

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

from sla.app import demo_seed  # noqa: E402
from sla.app.how_content import SECTIONS, TEXT  # noqa: E402
from sla.app.views.how_it_works import DEMO_LABEL  # noqa: E402


def page():
    return AppTest.from_string("from sla.app.views import how_it_works\nhow_it_works.render()", default_timeout=120)


def markdown_text(at) -> str:
    return "\n".join(m.value for m in at.markdown)


def test_guest_sees_the_page_with_an_empty_database():
    at = page().run()  # no login: a guest
    assert not at.exception, at.exception
    assert "How it works" in markdown_text(at)
    assert any(DEMO_LABEL in c.value for c in at.caption)


def test_page_renders_with_the_demo_snapshot():
    shutil.copyfile(demo_seed.SNAPSHOT_DB, os.environ["SLA_DB"])
    at = page().run()
    assert not at.exception, at.exception
    text = markdown_text(at)
    assert "Where the data lives" in text and "Current verdict" in text


def test_demo_switch_and_slider_work():
    at = page().run()
    at.radio(key="how_mode").set_value("Before training").run()
    assert not at.exception, at.exception
    at.radio(key="how_mode").set_value("After training").run()
    at.slider(key="how_eps").set_value(50).run()
    assert not at.exception, at.exception


def test_marathi_toggle_switches_every_helper_line_and_survives_two_toggles():
    at = page().run()
    assert not any(html.escape(TEXT["mr"][k]) in markdown_text(at) for k in SECTIONS)
    at.toggle(key="how_mr").set_value(True).run()
    assert not at.exception, at.exception
    text = markdown_text(at)
    assert all(html.escape(TEXT["mr"][k]) in text for k in SECTIONS)
    at.toggle(key="how_mr").set_value(False).run()
    assert not at.exception, at.exception
    at.toggle(key="how_mr").set_value(True).run()
    assert not at.exception, at.exception


def test_calculator_starts_with_the_documented_example():
    at = page().run()
    code = "\n".join(c.value for c in at.code)
    assert "new Q = old Q + α × (target − old Q)" in code and "= 0.1" in code
