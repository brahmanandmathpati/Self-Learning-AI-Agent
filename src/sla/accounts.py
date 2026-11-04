"""Dashboard sign-in accounts: email + password, "remember me" tokens and password-reset tokens.

Passwords are never stored. Each one is turned into a salted PBKDF2-SHA256 hash (200,000 rounds) and only the
hash and the random salt are saved. Tokens (remember-me cookies, reset links) are random 256-bit strings; only
their SHA-256 hash is stored, so a copy of the database cannot be used to sign in.

Storage:
* default: a small SQLite file (``runs/users.db``, git-ignored, separate from the experiment database);
* optional: any PostgreSQL database (for example a free Supabase project) when a ``postgresql://`` URL is given,
  so accounts survive restarts of Streamlit Community Cloud. Needs the ``psycopg`` package.
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
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ITERATIONS = 200_000
MIN_PASSWORD = 8
_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

_TABLES = """
CREATE TABLE IF NOT EXISTS users (
    user_id     {pk},
    email       TEXT NOT NULL UNIQUE,
    name        TEXT NOT NULL,
    pw_hash     TEXT NOT NULL,
    salt        TEXT NOT NULL,
    iterations  INTEGER NOT NULL,
    created_at  TEXT NOT NULL,
    last_login  TEXT
);
CREATE TABLE IF NOT EXISTS tokens (
    token_hash  TEXT PRIMARY KEY,
    user_id     INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    kind        TEXT NOT NULL,
    expires_at  TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
"""
REMEMBER_DAYS = 30
RESET_MINUTES = 30


class AccountError(ValueError):
    """A sign-up or sign-in problem that is safe to show to the user."""


@dataclass(frozen=True)
class Account:
    user_id: int
    email: str
    name: str


def _now_dt() -> datetime:
    return datetime.now(timezone.utc)


def _now() -> str:
    return _now_dt().isoformat(timespec="seconds")


def _hash(password: str, salt: bytes, iterations: int = ITERATIONS) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations).hex()


def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def normalise_email(email: str) -> str:
    return (email or "").strip().lower()


def _check_password(password: str) -> None:
    if len(password or "") < MIN_PASSWORD:
        raise AccountError(f"Password must be at least {MIN_PASSWORD} characters.")


class AccountStore:
    """Create and check accounts and tokens. Pass a file path (SQLite) or a ``postgresql://`` URL."""

    def __init__(self, target: str | Path) -> None:
        self.target = str(target)
        self.postgres = self.target.startswith(("postgres://", "postgresql://"))
        if self.postgres:
            try:
                import psycopg  # noqa: F401
            except ImportError as exc:  # pragma: no cover - depends on the install
                raise AccountError("A PostgreSQL accounts URL needs the 'psycopg' package.") from exc
        else:
            Path(self.target).parent.mkdir(parents=True, exist_ok=True)
        pk = "SERIAL PRIMARY KEY" if self.postgres else "INTEGER PRIMARY KEY AUTOINCREMENT"
        with self._connect() as con:
            for stmt in _TABLES.format(pk=pk).split(";"):
                if stmt.strip():
                    con.execute(stmt)

    # ------------------------------------------------------------------ connections (SQLite or PostgreSQL)
    @contextmanager
    def _connect(self) -> Iterator[Any]:
        if self.postgres:
            import psycopg
            from psycopg.rows import dict_row
            con = psycopg.connect(self.target, row_factory=dict_row, connect_timeout=10)
        else:
            con = sqlite3.connect(self.target, timeout=30)
            con.row_factory = sqlite3.Row
            con.execute("PRAGMA foreign_keys = ON")
        try:
            yield _Cursor(con, self.postgres)
            con.commit()
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()

    def _integrity_errors(self) -> tuple[type[BaseException], ...]:
        if self.postgres:
            import psycopg
            return (psycopg.errors.UniqueViolation,)
        return (sqlite3.IntegrityError,)

    # ------------------------------------------------------------------ accounts
    def create(self, email: str, name: str, password: str) -> Account:
        email, name = normalise_email(email), (name or "").strip()
        if not _EMAIL.match(email):
            raise AccountError("Please enter a valid email address.")
        if not name or len(name) > 60:
            raise AccountError("Please enter your name (up to 60 characters).")
        _check_password(password)
        salt = secrets.token_bytes(16)
        try:
            with self._connect() as con:
                row = con.one(
                    "INSERT INTO users (email, name, pw_hash, salt, iterations, created_at) VALUES (?, ?, ?, ?, ?, ?)"
                    " RETURNING user_id", (email, name, _hash(password, salt), salt.hex(), ITERATIONS, _now()))
        except self._integrity_errors() as exc:
            raise AccountError("An account with this email already exists. Please log in instead.") from exc
        return Account(int(row["user_id"]), email, name)

    def verify(self, email: str, password: str) -> Account | None:
        """Return the account when the email and password match, otherwise ``None``."""
        row = self._row_by_email(email)
        if row is None:
            _hash(password or "", b"timing-equaliser")  # same work either way, so timing does not reveal emails
            return None
        candidate = _hash(password or "", bytes.fromhex(row["salt"]), int(row["iterations"]))
        if not hmac.compare_digest(candidate, row["pw_hash"]):
            return None
        with self._connect() as con:
            con.run("UPDATE users SET last_login = ? WHERE user_id = ?", (_now(), row["user_id"]))
        return Account(int(row["user_id"]), row["email"], row["name"])

    def by_email(self, email: str) -> Account | None:
        row = self._row_by_email(email)
        return Account(int(row["user_id"]), row["email"], row["name"]) if row else None

    def _row_by_email(self, email: str) -> dict | None:
        with self._connect() as con:
            return con.one("SELECT * FROM users WHERE email = ?", (normalise_email(email),))

    def set_password(self, user_id: int, password: str) -> None:
        _check_password(password)
        salt = secrets.token_bytes(16)
        with self._connect() as con:
            con.run("UPDATE users SET pw_hash = ?, salt = ?, iterations = ? WHERE user_id = ?",
                    (_hash(password, salt), salt.hex(), ITERATIONS, user_id))
            con.run("DELETE FROM tokens WHERE user_id = ?", (user_id,))  # sign out everywhere after a reset

    def count(self) -> int:
        with self._connect() as con:
            return int(con.one("SELECT COUNT(*) AS n FROM users", ())["n"])

    # ------------------------------------------------------------------ tokens (remember-me, password reset)
    def issue_token(self, user_id: int, kind: str) -> str:
        """Create a random token; only its hash is stored. ``kind`` is 'remember' (30 days) or 'reset' (30 min)."""
        ttl = timedelta(days=REMEMBER_DAYS) if kind == "remember" else timedelta(minutes=RESET_MINUTES)
        token = secrets.token_urlsafe(32)
        with self._connect() as con:
            con.run("DELETE FROM tokens WHERE expires_at < ?", (_now(),))
            con.run("INSERT INTO tokens (token_hash, user_id, kind, expires_at, created_at) VALUES (?, ?, ?, ?, ?)",
                    (_token_hash(token), user_id, kind, (_now_dt() + ttl).isoformat(timespec="seconds"), _now()))
        return token

    def account_for_token(self, token: str, kind: str, consume: bool = False) -> Account | None:
        """The account a valid, unexpired token belongs to. ``consume`` deletes it (single-use reset links)."""
        if not isinstance(token, str) or not token:
            return None
        th = _token_hash(token)
        with self._connect() as con:
            row = con.one("SELECT u.user_id, u.email, u.name, t.expires_at FROM tokens t JOIN users u "
                          "ON u.user_id = t.user_id WHERE t.token_hash = ? AND t.kind = ?", (th, kind))
            if row is None:
                return None
            if row["expires_at"] < _now():
                con.run("DELETE FROM tokens WHERE token_hash = ?", (th,))
                return None
            if consume:
                con.run("DELETE FROM tokens WHERE token_hash = ?", (th,))
        return Account(int(row["user_id"]), row["email"], row["name"])

    def revoke_token(self, token: str) -> None:
        if isinstance(token, str) and token:
            with self._connect() as con:
                con.run("DELETE FROM tokens WHERE token_hash = ?", (_token_hash(token),))


class _Cursor:
    """Tiny wrapper so the same SQL (with ``?`` placeholders) runs on SQLite and PostgreSQL."""

    def __init__(self, con: Any, postgres: bool) -> None:
        self.con, self.postgres = con, postgres

    def _sql(self, sql: str) -> str:
        return sql.replace("?", "%s") if self.postgres else sql

    def execute(self, sql: str, params: tuple = ()) -> Any:
        return self.con.execute(self._sql(sql), params)

    def run(self, sql: str, params: tuple = ()) -> None:
        self.execute(sql, params)

    def one(self, sql: str, params: tuple = ()) -> dict | None:
        row = self.execute(sql, params).fetchone()
        return dict(row) if row is not None else None
