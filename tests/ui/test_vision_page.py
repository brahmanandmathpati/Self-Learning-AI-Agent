"""Vision Lab page: renders without a camera, consent gate, view-only saving for guests, gesture → reward buttons."""

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

GUEST = {"name": "Guest", "email": "", "kind": "guest"}
MEMBER = {"name": "Asha Rao", "email": "asha@example.com", "kind": "member"}


def _page(user=None):
    at = AppTest.from_string("from sla.app.views import vision\nvision.render()", default_timeout=90)
    if user:
        at.session_state["sla_user"] = user
    return at.run()


def _md(at):
    return " ".join(m.value for m in at.markdown)


def test_page_renders_without_camera_and_waits_for_consent():
    at = _page()
    assert not at.exception, at.exception
    text = _md(at)
    assert "Privacy first" in text
    if "extra packages" in text:  # vision packages not installed on this machine
        return
    assert "The camera is off." in text  # nothing starts before consent
    assert "Not enough samples to measure yet." in text  # no invented accuracy


@pytest.mark.parametrize("user,locked", [(GUEST, True), (MEMBER, False)])
def test_saving_models_needs_a_member(user, locked):
    at = _page(user)
    assert not at.exception, at.exception
    if "extra packages" in _md(at):
        pytest.skip("vision packages not installed")
    assert ("save and load gesture models" in _md(at)) is locked


def test_reward_buttons_update_the_agent():
    at = _page(MEMBER)
    if "extra packages" in _md(at):
        pytest.skip("vision packages not installed")
    next(b for b in at.button if b.label.startswith("👍 Good move")).click().run()
    assert not at.exception, at.exception
    agent = at.session_state["vl_agent"]
    assert agent.q.max() > 0 and agent.steps + len(agent.history) >= 1
