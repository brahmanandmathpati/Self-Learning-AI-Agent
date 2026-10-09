"""Reflection: grounded plain-language notes, the facts behind them, and validation status."""

from __future__ import annotations

import json

import streamlit as st

from sla.app import data
from sla.app.components.reflection_card import data_sources, insight_card
from sla.app.components.selectors import run_selector
from sla.app.components.ui import badge, empty_state, error_state, hero, section
from sla.app.state import services
from sla.utils.errors import SLAError

SOURCE = {"llm": "Local LLM (Ollama)", "template": "Template"}


@st.cache_data(ttl=30, show_spinner=False)
def _llm_online() -> bool:
    return services().reflection.llm_available()


def render() -> None:
    svc = services()
    online = _llm_online()
    hero("Reflection", "An AI research assistant that explains a run in plain words — written only from computed "
         "facts, with every number checked against them.", eyebrow="Learning insight",
         right_html=badge("online", "Ollama online") if online else badge("offline", "Ollama offline · template mode"))
    runs = data.trained_runs()
    if runs.empty:
        empty_state("No reflection available yet.", "sla train --config configs/frozenlake_qlearning.yaml",
                    "Train an agent first — reflection needs logged episodes.", glyph="brain")
        return
    run_id = run_selector(runs, key="refl_run")
    try:
        facts = svc.reflection.facts(run_id)
    except SLAError as exc:
        error_state("Unable to compute facts for this run.", str(exc), "Pick a run that finished training.")
        return

    c1, c2 = st.columns([3, 1], vertical_alignment="center")
    with c1:
        use_llm = st.toggle("Write with the local LLM (Ollama)", value=False, disabled=not online,
                            help="Optional. Without Ollama the deterministic template writes the note.")
        if not online:
            st.caption("Ollama is not reachable from this server, so notes are written by the template — "
                       "they use exactly the same facts.")
    with c2:
        generate = st.button("Generate insight", type="primary", width="stretch")
    if generate:
        with st.spinner("Writing the note and checking every number against the facts…"):
            result = svc.reflection.generate(run_id, use_llm=use_llm)
        if result.rejected:
            st.warning("The LLM note was rejected because it used numbers that are not in the facts: "
                       f"{result.rejected.report.unsupported}. The template note is shown instead.")
        st.toast(f"Note #{result.shown.note_id} saved ({SOURCE.get(result.shown.source, result.shown.source)}).")

    notes = svc.reflection.notes(run_id)
    if notes.empty:
        empty_state("No insight for this run yet.", next_step="Press “Generate insight” to write one.", glyph="spark")
    else:
        n = notes.iloc[0]
        insight_card(n["note_text"], bool(n["grounding_passed"]), SOURCE.get(n["source"], n["source"]),
                     f"Note #{n['note_id']} · {n['created_at']}")
        report = json.loads(n["grounding_report"] or "{}")
        if report.get("unsupported"):
            st.caption(f"Unsupported numbers: {report['unsupported']}")

    section("Data sources", "The facts this explanation may use — computed from the stored episodes and evaluations.")
    data_sources(facts)
    with st.expander("All facts (JSON)"):
        st.json(facts, expanded=False)

    if not notes.empty:
        if len(notes) > 1:
            with st.expander(f"Earlier notes ({len(notes) - 1})"):
                for _, m in notes.iloc[1:].iterrows():
                    st.markdown(f"{badge('pass' if m['grounding_passed'] else 'reject')} &nbsp; "
                                f"<span style='color:var(--muted)'>#{m['note_id']} · "
                                f"{SOURCE.get(m['source'], m['source'])} · {m['created_at']}</span>",
                                unsafe_allow_html=True)
                    st.write(m["note_text"])
        section("Rate an insight",
                "Ratings evaluate the explanation layer only — they never change what the agent learns.")
        with st.form("rate"):
            a, b = st.columns(2)
            note_id = a.selectbox("Note", notes["note_id"].tolist())
            accurate = b.radio("Accurate?", ["Yes", "No"], horizontal=True) == "Yes"
            useful = st.slider("Usefulness", 1, 5, 3)
            comment = st.text_input("Comment (optional, max 500 characters)")
            if st.form_submit_button("Save rating"):
                try:
                    svc.reflection.rate(int(note_id), accurate, int(useful), comment)
                    st.success("Rating saved.")
                except SLAError as exc:
                    st.error(str(exc))
