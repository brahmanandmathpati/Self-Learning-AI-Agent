"""Sign-in screen, guest (view-only) mode and member access."""

from pathlib import Path

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

MAIN = str(Path(__file__).resolve().parents[2] / "src" / "sla" / "app" / "main.py")
GUEST = {"name": "Guest", "email": "", "kind": "guest"}
MEMBER = {"name": "Asha Rao", "email": "asha@example.com", "kind": "member"}


def _button(at, label):
    return next(b for b in at.button if b.label == label)


def _text(at, label):
    return next(t for t in at.text_input if t.label == label)


def _md(at):
    return " ".join(m.value for m in at.markdown)


def test_sign_in_screen_comes_first():
    at = AppTest.from_file(MAIN, default_timeout=60).run()
    assert not at.exception, at.exception
    labels = {b.label for b in at.button}
    assert {"Sign in", "Create account", "Continue as guest"} <= labels
    assert "Continue with Google" not in labels  # hidden until [auth] secrets are configured


def test_guest_lands_on_overview_in_view_only_mode():
    at = AppTest.from_file(MAIN, default_timeout=60).run()
    _button(at, "Continue as guest").click().run()
    assert not at.exception, at.exception
    assert at.session_state["sla_user"]["kind"] == "guest"
    assert "Guest · view only" in _md(at)
    assert "At a glance" in _md(at)


def test_create_account_then_sign_in_again():
    at = AppTest.from_file(MAIN, default_timeout=60).run()
    _text(at, "Your name").input("Asha Rao")
    _text(at, "Email ").input("asha@example.com")
    _text(at, "Password (at least 8 characters)").input("correct-horse")
    _text(at, "Confirm password").input("correct-horse")
    _button(at, "Create account").click().run()
    assert not at.exception, at.exception
    assert at.session_state["sla_user"]["kind"] == "member"
    assert "Welcome back, Asha" in _md(at)

    again = AppTest.from_file(MAIN, default_timeout=60).run()  # a new visit: sign in with the saved account
    _text(again, "Email").input("ASHA@example.com")
    _text(again, "Password").input("correct-horse")
    _button(again, "Sign in").click().run()
    assert again.session_state["sla_user"]["email"] == "asha@example.com"


def test_wrong_password_shows_error():
    at = AppTest.from_file(MAIN, default_timeout=60).run()
    _text(at, "Email").input("nobody@example.com")
    _text(at, "Password").input("wrong-password")
    _button(at, "Sign in").click().run()
    assert any("not correct" in e.value for e in at.error)
    assert "sla_user" not in at.session_state


@pytest.mark.parametrize("user,locked", [(GUEST, True), (MEMBER, False)])
def test_training_is_locked_only_for_guests(user, locked):
    at = AppTest.from_string("from sla.app.views import training\ntraining.render()", default_timeout=60)
    at.session_state["sla_user"] = user
    at.run()
    assert not at.exception, at.exception
    assert ("Guest mode is view-only" in _md(at)) is locked
    assert _button(at, "Start training").disabled is locked
