import pytest

from sla.reflection.feedback import clean_comment, ratings_summary, save_rating
from sla.utils.errors import ValidationError


@pytest.fixture
def note_id(db):
    db.start_run("r", "CartPole-v1", "dqn", 0, {})
    return db.add_reflection("r", {}, "note", "template", True)


def test_save_and_summary(db, note_id):
    save_rating(db, note_id, True, 5, "  clear  ")
    save_rating(db, note_id, False, 3)
    assert ratings_summary(db) == {"count": 2, "accurate_share": 0.5, "mean_usefulness": 4.0}
    assert db.query_feedback(note_id)["comment"].tolist()[0] == "clear"


@pytest.mark.parametrize("kwargs", [
    {"accurate": "yes", "usefulness": 3}, {"accurate": True, "usefulness": 0},
    {"accurate": True, "usefulness": 6}, {"accurate": True, "usefulness": 2.5},
])
def test_invalid_ratings(db, note_id, kwargs):
    with pytest.raises(ValidationError):
        save_rating(db, note_id, **kwargs)


def test_unknown_note(db):
    with pytest.raises(ValidationError, match="does not exist"):
        save_rating(db, 999, True, 3)


def test_comment_cleaning():
    assert clean_comment("ok\x00\x07 ") == "ok"
    assert clean_comment("   ") is None
    with pytest.raises(ValidationError):
        clean_comment("x" * 501)


def test_empty_summary(db):
    assert ratings_summary(db)["count"] == 0
