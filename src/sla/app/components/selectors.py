"""Run and experiment pickers shared by several pages."""

from __future__ import annotations

import pandas as pd
import streamlit as st


def run_label(row: pd.Series) -> str:
    variant = f" · {row['variant']}" if isinstance(row.get("variant"), str) and row["variant"] else ""
    return f"{row['algorithm']} · {row['env']} · seed {row['seed']}{variant} · {row['status']} — {row['run_id']}"


def run_selector(runs: pd.DataFrame, key: str, label: str = "Run") -> str | None:
    if runs.empty:
        return None
    labels = {row["run_id"]: run_label(row) for _, row in runs.iterrows()}
    ids = list(labels)
    default = st.session_state.get("selected_run")
    index = ids.index(default) if default in ids else 0
    chosen = st.selectbox(label, ids, index=index, format_func=labels.get, key=key)
    st.session_state["selected_run"] = chosen
    return chosen


def experiment_selector(experiments: pd.DataFrame, key: str, label: str = "Experiment") -> int | None:
    if experiments.empty:
        return None
    labels = {int(r["experiment_id"]): f"#{int(r['experiment_id'])} · {r['name']} · {r['status']} · {r['created_at']}"
              for _, r in experiments.iterrows()}
    ids = list(labels)
    completed = [int(r["experiment_id"]) for _, r in experiments.iterrows() if r["status"] == "completed"]
    index = ids.index(completed[0]) if completed else 0  # newest finished experiment by default
    return st.selectbox(label, ids, index=index, format_func=labels.get, key=key)
