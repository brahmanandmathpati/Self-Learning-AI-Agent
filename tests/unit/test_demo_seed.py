"""The hosted-app seeding copies the committed snapshot only when forced/hosted and no database exists."""

import sqlite3

import pytest

from sla.app import demo_seed


@pytest.fixture
def target(tmp_path, monkeypatch):
    db = tmp_path / "sub" / "sla.db"
    monkeypatch.setenv("SLA_DB", str(db))
    return db


def test_no_seed_by_default_locally(target, monkeypatch):
    monkeypatch.delenv("SLA_SEED_DEMO", raising=False)
    assert demo_seed.seed_if_needed() is False
    assert not target.exists()


@pytest.mark.skipif(not demo_seed.SNAPSHOT_DB.is_file(), reason="snapshot not present")
def test_seed_copies_snapshot_when_forced(target, monkeypatch):
    monkeypatch.setenv("SLA_SEED_DEMO", "1")
    assert demo_seed.seed_if_needed() is True
    with sqlite3.connect(target) as con:
        assert con.execute("SELECT COUNT(*) FROM experiments").fetchone()[0] > 0
    assert demo_seed.seed_if_needed() is False  # never overwrites an existing database


def test_seed_disabled_explicitly(target, monkeypatch):
    monkeypatch.setenv("SLA_SEED_DEMO", "0")
    assert demo_seed.seed_if_needed() is False
