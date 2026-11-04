"""Send the password-reset email through any SMTP server (Gmail app password, Brevo, Mailgun, …).

Configured with an ``[smtp]`` section in ``.streamlit/secrets.toml`` (see ``secrets.toml.example``). Without it,
``smtp_enabled()`` is False and the dialog says honestly that email reset is not set up on this site.
"""

from __future__ import annotations

import smtplib
import ssl
from email.message import EmailMessage

import streamlit as st

REQUIRED = ("host", "port", "username", "password", "sender")


def _smtp() -> dict:
    try:
        return dict(st.secrets.get("smtp", {}))
    except Exception:  # noqa: BLE001 - no secrets file is the normal local case
        return {}


def smtp_enabled() -> bool:
    cfg = _smtp()
    return all(cfg.get(k) for k in REQUIRED)


def reset_message(to: str, name: str, link: str, sender: str) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = "Reset your Self-Learning AI Agent password"
    msg["From"], msg["To"] = sender, to
    msg.set_content(
        f"Hi {name},\n\nSomeone (hopefully you) asked to reset the password for your Self-Learning AI Agent "
        f"account.\n\nOpen this link within 30 minutes to choose a new password:\n{link}\n\n"
        "If you did not ask for this, you can ignore this email — your password stays the same.\n")
    return msg


def send_reset(to: str, name: str, link: str) -> None:
    cfg = _smtp()
    msg = reset_message(to, name, link, cfg["sender"])
    port = int(cfg["port"])
    ctx = ssl.create_default_context()
    if port == 465:
        with smtplib.SMTP_SSL(cfg["host"], port, context=ctx, timeout=20) as s:
            s.login(cfg["username"], cfg["password"])
            s.send_message(msg)
    else:
        with smtplib.SMTP(cfg["host"], port, timeout=20) as s:
            s.starttls(context=ctx)
            s.login(cfg["username"], cfg["password"])
            s.send_message(msg)


def app_url() -> str:
    """Public base URL of the app (``[smtp] app_url`` if given, else the URL the visitor is using)."""
    from sla.app.routes import base_url
    url = _smtp().get("app_url") or base_url()
    return url if url.endswith("/") else url + "/"
