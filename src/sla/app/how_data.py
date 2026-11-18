"""Row counts for the "How it works" page (cached with the same version token as the other pages)."""

from __future__ import annotations

import streamlit as st

from sla.app import data
from sla.app.state import services

TABLES = ("experiments", "runs", "episodes", "metrics", "evaluations", "ablation_results", "reflections")


@st.cache_data(ttl=data.TTL, show_spinner=False)
def _counts(db: str, ver: tuple) -> dict[str, int]:
    with services().db._connect() as con:
        return {t: int(con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]) for t in TABLES}


def table_counts() -> dict[str, int]:
    return _counts(data._db(), data.version())
