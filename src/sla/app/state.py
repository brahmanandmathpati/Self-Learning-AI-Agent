"""Cached access to the service layer for every page."""

from __future__ import annotations

import streamlit as st

from sla import settings
from sla.services import Services, get_services


@st.cache_resource(show_spinner=False)
def _services(db_path: str) -> Services:
    return get_services(db_path)


def services() -> Services:
    return _services(str(settings.db_path()))
