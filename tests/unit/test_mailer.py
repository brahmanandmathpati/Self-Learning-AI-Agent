"""Password-reset email: content and the 'not configured' default."""

import pytest

pytest.importorskip("streamlit")

from sla.app import mailer  # noqa: E402


def test_reset_message_contains_link_and_expiry():
    msg = mailer.reset_message("a@b.co", "Asha", "https://example.app/?reset=abc", "Lab <lab@example.app>")
    body = msg.get_content()
    assert msg["To"] == "a@b.co" and "reset" in msg["Subject"].lower()
    assert "https://example.app/?reset=abc" in body and "30 minutes" in body


def test_smtp_is_off_without_secrets():
    assert mailer.smtp_enabled() is False
