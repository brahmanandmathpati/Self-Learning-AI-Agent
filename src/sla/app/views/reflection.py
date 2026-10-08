"""Reflection: grounded plain-language notes, the facts behind them, and validation status."""

from __future__ import annotations

import json

import streamlit as st

from sla.app.components.selectors import run_selector
from sla.app.components.ui import badge, empty_state, hero, note_box, section
from sla.app.state import services
from sla.utils.errors import SLAError


@st.cache_data(ttl=30, show_spinner=False)
def _llm_online() -> bool:
    return services().reflection.llm_available()


def render() -> None:
    svc = services()
    online = _llm_online()
    hero("Reflection", "Explanations are written only from computed facts; every number is checked against them.",
         badge("online" if online else "offline", "Ollama online" if online else "Ollama offline · template mode"))
    runs = svc.experiments.trained_runs()
    if runs.empty:
        empty_state("Train an agent first — reflection needs logged episodes.",
                    "sla train --config configs/frozenlake_qlearning.yaml")
        return
    run_id = run_selector(runs, key="refl_run")
    left, right = st.columns([3, 2])
    with right:
        section("Grounded facts", "The only input the explanation may use.")
        try:
            facts = svc.reflection.facts(run_id)
            st.json(facts, expanded=False)
        except SLAError as exc:
            st.error(str(exc))
            return
    with left:
        section("Generate an explanation")
        use_llm = st.toggle("Use local LLM (Ollama)", value=False, disabled=not online,
                            help="Optional. Without Ollama the deterministic template is used.")
        if st.button("Generate note", type="primary"):
            with st.spinner("Writing and fact-checking the note…"):
                result = svc.reflection.generate(run_id, use_llm=use_llm)
            if result.rejected:
                st.warning("The LLM note was rejected because it contained numbers that are not in the facts: "
                           f"{result.rejected.report.unsupported}. The template note is shown instead.")
            st.success(f"Note #{result.shown.note_id} saved ({result.shown.source}).")

        notes = svc.reflection.notes(run_id)
        if notes.empty:
            empty_state("No notes for this run yet.")
            return
        for _, n in notes.iterrows():
            kind = "pass" if n["grounding_passed"] else "reject"
            source = {"llm": "LLM", "template": "Template (fallback)"}.get(n["source"], n["source"])
            st.markdown(f"{badge(kind)} &nbsp; <span style='color:#898781'>#{n['note_id']} · {source} · "
                        f"{n['created_at']}</span>", unsafe_allow_html=True)
            note_box(n["note_text"])
            report = json.loads(n["grounding_report"] or "{}")
            if report.get("unsupported"):
                st.caption(f"Unsupported numbers: {report['unsupported']}")
            st.write("")

        section("Rate a note", "Ratings evaluate the explanation layer only — they never change what the agent learns.")
        with st.form("rate"):
            note_id = st.selectbox("Note", notes["note_id"].tolist())
            accurate = st.radio("Accurate?", ["Yes", "No"], horizontal=True) == "Yes"
            useful = st.slider("Usefulness", 1, 5, 3)
            comment = st.text_input("Comment (optional, max 500 characters)")
            if st.form_submit_button("Save rating"):
                try:
                    svc.reflection.rate(int(note_id), accurate, int(useful), comment)
                    st.success("Rating saved.")
                except SLAError as exc:
                    st.error(str(exc))
