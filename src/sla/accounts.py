"""Dashboard sign-in accounts: email + password, stored in their own small SQLite file.

Passwords are never stored. Each one is turned into a salted PBKDF2-SHA256 hash (200,000 rounds) and only the
hash and the random salt are saved. The accounts file lives in ``runs/`` (git-ignored), separate from the
experiment database, so the results snapshot and the experiments are never touched by sign-ups.
"""

from __future__ import annotations

import hashlib
import hmac
import re
import secrets
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ITERATIONS = 200_000
MIN_PASSWORD = 8
_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    email       TEXT NOT NULL UNIQUE,
    name        TEXT NOT NULL,
    pw_hash     TEXT NOT NULL,
    salt        TEXT NOT NULL,
    iterations  INTEGER NOT NULL,
    created_at  TEXT NOT NULL,
    last_login  TEXT
);
"""


class AccountError(ValueError):
    """A sign-up or sign-in problem that is safe to show to the user."""


@dataclass(frozen=True)
class Account:
    user_id: int
    email: str
    name: str


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _hash(password: str, salt: bytes, iterations: int = ITERATIONS) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations).hex()


def normalise_email(email: str) -> str:
    return (email or "").strip().lower()


class AccountStore:
    """Create and check accounts. Every call opens a short-lived connection (safe for Streamlit reruns)."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as con:
            con.executescript(_SCHEMA)

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        con = sqlite3.connect(self.path, timeout=30)
        con.row_factory = sqlite3.Row
        try:
            with con:  # commit on success, roll back on error
                yield con
        finally:
            con.close()

    def create(self, email: str, name: str, password: str) -> Account:
        email, name = normalise_email(email), (name or "").strip()
        if not _EMAIL.match(email):
            raise AccountError("Please enter a valid email address.")
        if not name or len(name) > 60:
            raise AccountError("Please enter your name (up to 60 characters).")
        if len(password or "") < MIN_PASSWORD:
            raise AccountError(f"Password must be at least {MIN_PASSWORD} characters.")
        salt = secrets.token_bytes(16)
        try:
            with self._connect() as con:
                cur = con.execute(
                    "INSERT INTO users (email, name, pw_hash, salt, iterations, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (email, name, _hash(password, salt), salt.hex(), ITERATIONS, _now()))
                user_id = int(cur.lastrowid)
        except sqlite3.IntegrityError as exc:
            raise AccountError("An account with this email already exists. Please sign in instead.") from exc
        return Account(user_id, email, name)

    def verify(self, email: str, password: str) -> Account | None:
        """Return the account when the email and password match, otherwise ``None``."""
        email = normalise_email(email)
        with self._connect() as con:
            row = con.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if row is None:
            _hash(password or "", b"timing-equaliser")  # same work either way, so timing does not reveal emails
            return None
        candidate = _hash(password or "", bytes.fromhex(row["salt"]), int(row["iterations"]))
        if not hmac.compare_digest(candidate, row["pw_hash"]):
            return None
        with self._connect() as con:
            con.execute("UPDATE users SET last_login = ? WHERE user_id = ?", (_now(), row["user_id"]))
        return Account(int(row["user_id"]), row["email"], row["name"])

    def count(self) -> int:
        with self._connect() as con:
            return int(con.execute("SELECT COUNT(*) FROM users").fetchone()[0])
