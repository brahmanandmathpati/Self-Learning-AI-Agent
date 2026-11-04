"""Top-right Log in / Sign up, the auth dialog, guest (view-only) mode and member access."""

from pathlib import Path

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest  # noqa: E402

MAIN = str(Path(__file__).resolve().parents[2] / "src" / "sla" / "app" / "main.py")
GUEST = {"name": "Guest", "email": "", "kind": "guest"}
MEMBER = {"name": "Asha Rao", "email": "asha@example.com", "kind": "member"}


def _app():
    return AppTest.from_file(MAIN, default_timeout=60).run()


def _button(at, label, skip_key=None):
    return next(b for b in at.button if b.label == label and b.key != skip_key)


def _text(at, label):
    return next(t for t in at.text_input if t.label == label)


def _md(at):
    return " ".join(m.value for m in at.markdown)


def test_visitor_sees_the_dashboard_and_auth_buttons():
    at = _app()
    assert not at.exception, at.exception
    assert "At a glance" in _md(at)  # no forced sign-in screen any more
    labels = {b.label for b in at.button}
    assert {"Log in", "Sign up"} <= labels
    assert "Continue with Google" not in labels  # hidden until [auth] secrets are configured


def test_sign_up_in_the_dialog_then_log_in_again():
    at = _app()
    _button(at, "Sign up").click().run()
    _text(at, "Your name").input("Asha Rao")
    _text(at, "Email").input("asha@example.com")
    _text(at, "Password (at least 8 characters)").input("correct-horse")
    _text(at, "Confirm password").input("correct-horse")
    _button(at, "Create account").click().run()
    assert not at.exception, at.exception
    assert at.session_state["sla_user"]["kind"] == "member"
    assert "Welcome back, Asha" in _md(at)

    again = _app()  # a new visit: log in with the saved account (email is case-insensitive)
    _button(again, "Log in").click().run()
    _text(again, "Email").input("ASHA@example.com")
    _text(again, "Password").input("correct-horse")
    _button(again, "Log in", skip_key="nav_login").click().run()
    assert again.session_state["sla_user"]["email"] == "asha@example.com"


def test_wrong_password_shows_error():
    at = _app()
    _button(at, "Log in").click().run()
    _text(at, "Email").input("nobody@example.com")
    _text(at, "Password").input("wrong-password")
    _button(at, "Log in", skip_key="nav_login").click().run()
    assert any("not correct" in e.value for e in at.error)
    assert "sla_user" not in at.session_state


def test_continue_as_guest_is_view_only():
    at = _app()
    _button(at, "Log in").click().run()
    _button(at, "Continue as guest").click().run()
    assert not at.exception, at.exception
    assert at.session_state["sla_user"]["kind"] == "guest"
    assert "Guest · view only" in _md(at)


@pytest.mark.parametrize("user,locked", [(None, True), (GUEST, True), (MEMBER, False)])
def test_training_is_locked_unless_member(user, locked):
    at = AppTest.from_string("from sla.app.views import training\ntraining.render()", default_timeout=60)
    if user:
        at.session_state["sla_user"] = user
    at.run()
    assert not at.exception, at.exception
    assert ("View-only mode" in _md(at)) is locked
    assert _button(at, "Start training").disabled is locked


def test_overview_has_all_landing_sections():
    at = _app()
    text = _md(at)
    for title in ("At a glance", "How it works", "What makes it different", "Live from the lab",
                  "Proof, not promises", "How it is built", "The team", "Questions",
                  "Train your first agent in under a minute."):
        assert title in text, title
    assert len(at.expander) >= 6  # FAQ


def _store():
    import os

    from sla.accounts import AccountStore
    return AccountStore(os.environ["SLA_USERS_DB"])


def test_keep_me_signed_in_issues_a_remember_token():
    _store().create("keep@example.com", "Keep Me", "password1")
    at = _app()
    _button(at, "Log in").click().run()
    _text(at, "Email").input("keep@example.com")
    _text(at, "Password").input("password1")
    _button(at, "Log in", skip_key="nav_login").click().run()
    token = at.session_state["sla_remember_token"]
    assert _store().account_for_token(token, "remember").email == "keep@example.com"


def test_forgot_password_says_when_email_is_not_set_up():
    at = _app()
    _button(at, "Log in").click().run()
    _button(at, "Forgot password?").click().run()
    assert not at.exception, at.exception
    assert any("not set up" in i.value for i in at.info)


def test_reset_link_lets_the_user_choose_a_new_password():
    store = _store()
    acc = store.create("reset@example.com", "Re Set", "old-password")
    token = store.issue_token(acc.user_id, "reset")
    at = AppTest.from_file(MAIN, default_timeout=60)
    at.query_params["reset"] = token
    at.run()
    _text(at, "New password (at least 8 characters)").input("new-password-1")
    _text(at, "Confirm new password").input("new-password-1")
    _button(at, "Save new password").click().run()
    assert not at.exception, at.exception
    assert at.session_state["sla_user"]["email"] == "reset@example.com"
    assert store.verify("reset@example.com", "old-password") is None
    assert store.verify("reset@example.com", "new-password-1") is not None
    assert store.account_for_token(token, "reset") is None  # single use


def test_run_explorer_offers_a_share_link():
    import os
    from dataclasses import replace

    from sla.database.store import Database
    from sla.training.config import config_from_dict
    from sla.training.pipeline import run_experiment
    cfg = config_from_dict({"env_name": "FrozenLake-v1", "env_kwargs": {"is_slippery": False},
                            "agent": "q_learning", "episodes": 60, "seed": 0, "eval_every": 30,
                            "eval_episodes": 3, "checkpoint_every": 30, "run_root": os.environ["SLA_RUN_ROOT"]})
    run_experiment(replace(cfg), [0], Database(os.environ["SLA_DB"]), final_eval_episodes=3)
    at = AppTest.from_string("from sla.app.views import explorer\nexplorer.render()", default_timeout=60).run()
    assert not at.exception, at.exception
    assert "Share this run" in _md(at)
    assert any("runs?run=" in c.value for c in at.code)
