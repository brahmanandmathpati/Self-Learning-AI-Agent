"""Sign-in accounts: hashing, validation and duplicate handling."""

import sqlite3

import pytest

from sla.accounts import AccountError, AccountStore


@pytest.fixture
def store(tmp_path):
    return AccountStore(tmp_path / "users.db")


def test_create_and_verify(store):
    acc = store.create("Asha@Example.com ", "Asha", "correct-horse")
    assert acc.email == "asha@example.com"
    assert store.verify("asha@example.com", "correct-horse") == acc
    assert store.verify("ASHA@example.com", "correct-horse") == acc


def test_wrong_password_and_unknown_email(store):
    store.create("a@b.co", "A", "password1")
    assert store.verify("a@b.co", "password2") is None
    assert store.verify("nobody@b.co", "password1") is None


def test_password_is_never_stored_in_plain_text(store, tmp_path):
    store.create("a@b.co", "A", "plain-secret-123")
    with sqlite3.connect(tmp_path / "users.db") as con:
        row = con.execute("SELECT pw_hash, salt FROM users").fetchone()
    assert "plain-secret-123" not in row[0] and len(row[0]) == 64 and len(row[1]) == 32


def test_same_password_gets_different_hashes(store, tmp_path):
    store.create("a@b.co", "A", "same-password")
    store.create("c@d.co", "C", "same-password")
    with sqlite3.connect(tmp_path / "users.db") as con:
        hashes = {r[0] for r in con.execute("SELECT pw_hash FROM users")}
    assert len(hashes) == 2


@pytest.mark.parametrize("email,name,pw", [("not-an-email", "A", "password1"), ("a@b.co", "", "password1"),
                                          ("a@b.co", "A", "short")])
def test_validation(store, email, name, pw):
    with pytest.raises(AccountError):
        store.create(email, name, pw)


def test_duplicate_email_rejected(store):
    store.create("a@b.co", "A", "password1")
    with pytest.raises(AccountError, match="already exists"):
        store.create("A@B.CO", "Other", "password2")
    assert store.count() == 1


def test_remember_token_round_trip_and_revoke(store):
    acc = store.create("a@b.co", "A", "password1")
    token = store.issue_token(acc.user_id, "remember")
    assert store.account_for_token(token, "remember") == acc
    assert store.account_for_token(token, "reset") is None  # a remember token is not a reset token
    store.revoke_token(token)
    assert store.account_for_token(token, "remember") is None


def test_tokens_are_stored_only_as_hashes(store, tmp_path):
    acc = store.create("a@b.co", "A", "password1")
    token = store.issue_token(acc.user_id, "remember")
    with sqlite3.connect(tmp_path / "users.db") as con:
        stored = con.execute("SELECT token_hash FROM tokens").fetchone()[0]
    assert stored != token and len(stored) == 64


def test_reset_token_is_single_use_and_new_password_works(store):
    acc = store.create("a@b.co", "A", "password1")
    remember = store.issue_token(acc.user_id, "remember")
    reset = store.issue_token(acc.user_id, "reset")
    assert store.account_for_token(reset, "reset", consume=True) == acc
    assert store.account_for_token(reset, "reset") is None
    store.set_password(acc.user_id, "brand-new-pass")
    assert store.verify("a@b.co", "password1") is None
    assert store.verify("a@b.co", "brand-new-pass") == acc
    assert store.account_for_token(remember, "remember") is None  # a reset signs out every device


def test_expired_token_is_rejected(store, tmp_path):
    acc = store.create("a@b.co", "A", "password1")
    token = store.issue_token(acc.user_id, "reset")
    with sqlite3.connect(tmp_path / "users.db") as con:
        con.execute("UPDATE tokens SET expires_at = '2000-01-01T00:00:00+00:00'")
    assert store.account_for_token(token, "reset") is None


def test_old_accounts_file_is_upgraded(tmp_path):
    path = tmp_path / "old.db"
    with sqlite3.connect(path) as con:  # the first version had only the users table
        con.execute("CREATE TABLE users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL UNIQUE, "
                    "name TEXT NOT NULL, pw_hash TEXT NOT NULL, salt TEXT NOT NULL, iterations INTEGER NOT NULL, "
                    "created_at TEXT NOT NULL, last_login TEXT)")
    s = AccountStore(path)
    acc = s.create("a@b.co", "A", "password1")
    assert s.account_for_token(s.issue_token(acc.user_id, "remember"), "remember") == acc
