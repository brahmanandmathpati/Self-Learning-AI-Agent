"""Saving user ratings of reflection notes.

Ratings are used ONLY to evaluate the explanation layer. They never change
what the agent learns.
"""

from __future__ import annotations

import re
from typing import Any

from sla.database.store import Database
from sla.utils.errors import ValidationError

MAX_COMMENT_LENGTH = 500
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def clean_comment(comment: str | None) -> str | None:
    """Strip spaces and control characters; empty comments become None."""
    if comment is None:
        return None
    if not isinstance(comment, str):
        raise ValidationError("Comment must be text")
    text = _CONTROL_CHARS.sub("", comment).strip()
    if len(text) > MAX_COMMENT_LENGTH:
        raise ValidationError(f"Comment is too long ({len(text)} characters, max {MAX_COMMENT_LENGTH})")
    return text or None


def save_rating(store: Database, note_id: int, accurate: bool, usefulness: int,
                comment: str | None = None) -> int:
    """Validate and store one rating. Returns the new feedback id."""
    if isinstance(note_id, bool) or not isinstance(note_id, int) or note_id <= 0:
        raise ValidationError(f"note_id must be a positive integer, got {note_id!r}")
    if not isinstance(accurate, bool):
        raise ValidationError("accurate must be True or False")
    if isinstance(usefulness, bool) or not isinstance(usefulness, int) or not 1 <= usefulness <= 5:
        raise ValidationError(f"usefulness must be an integer from 1 to 5, got {usefulness!r}")
    if store.get_reflection(note_id) is None:
        raise ValidationError(f"Note {note_id} does not exist")
    return store.add_feedback(note_id, accurate, usefulness, clean_comment(comment))


def ratings_summary(store: Database) -> dict[str, Any]:
    df = store.query_feedback()
    if df.empty:
        return {"count": 0, "accurate_share": None, "mean_usefulness": None}
    return {"count": int(len(df)), "accurate_share": round(float(df["accurate"].mean()), 2),
            "mean_usefulness": round(float(df["usefulness"].mean()), 2)}
