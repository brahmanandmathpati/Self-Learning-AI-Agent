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
