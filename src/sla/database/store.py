"""SQLite experiment database: experiments, runs, episodes, metrics, evaluations, ablation results, reflections.

Large artefacts (model weights, replay buffers) stay on disk; the database stores their paths.
The schema is versioned with ``PRAGMA user_version`` and upgraded by ``MIGRATIONS`` on open.
"""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from sla.utils.errors import StoreError

DEFAULT_DB = "runs/sla.db"

MIGRATIONS: dict[int, str] = {
    1: """
CREATE TABLE experiments (
    experiment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    kind          TEXT NOT NULL,              -- pipeline | ablation | baseline | single
    env           TEXT,
    algorithm     TEXT,
    config_json   TEXT NOT NULL DEFAULT '{}',
    seeds_json    TEXT NOT NULL DEFAULT '[]',
    status        TEXT NOT NULL DEFAULT 'running',
    summary_json  TEXT,
    git_sha       TEXT,
    created_at    TEXT NOT NULL,
    finished_at   TEXT
);
CREATE TABLE runs (
    run_id            TEXT PRIMARY KEY,
    experiment_id     INTEGER REFERENCES experiments(experiment_id) ON DELETE SET NULL,
    env               TEXT NOT NULL,
    algorithm         TEXT NOT NULL,
    seed              INTEGER NOT NULL,
    variant           TEXT,
    config_json       TEXT NOT NULL,
    run_dir           TEXT,
    git_sha           TEXT,
    status            TEXT NOT NULL DEFAULT 'running',  -- running | completed | stopped | failed
    stopped_reason    TEXT,
    episodes_completed INTEGER NOT NULL DEFAULT 0,
    latest_checkpoint TEXT,
    best_checkpoint   TEXT,
    started_at        TEXT NOT NULL,
    ended_at          TEXT,
    error             TEXT
);
CREATE TABLE episodes (
    run_id       TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    episode      INTEGER NOT NULL,
    total_reward REAL NOT NULL,
    length       INTEGER NOT NULL,
    epsilon      REAL,
    mean_loss    REAL,
    end_reason   TEXT,
    wall_time_s  REAL,
    PRIMARY KEY (run_id, episode)
);
CREATE TABLE metrics (
    run_id    TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    name      TEXT NOT NULL,
    value     REAL,
    step      INTEGER,
    created_at TEXT NOT NULL
);
CREATE INDEX idx_metrics_run ON metrics(run_id, name);
CREATE TABLE evaluations (
    eval_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id       TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    kind         TEXT NOT NULL,              -- initial | validation | test
    episode      INTEGER,                    -- training episode the policy came from (NULL = untrained)
    mean_return  REAL NOT NULL,
    std_return   REAL NOT NULL,
    median_return REAL,
    success_rate REAL,
    mean_length  REAL,
    n_episodes   INTEGER NOT NULL,
    seed_base    INTEGER,
    checkpoint   TEXT,
    returns_json TEXT,
    created_at   TEXT NOT NULL
);
CREATE INDEX idx_eval_run ON evaluations(run_id, kind);
CREATE TABLE ablation_results (
    ablation_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id INTEGER NOT NULL REFERENCES experiments(experiment_id) ON DELETE CASCADE,
    variant       TEXT NOT NULL,
    seed          INTEGER NOT NULL,
    run_id        TEXT REFERENCES runs(run_id) ON DELETE SET NULL,
    final_mean    REAL NOT NULL,
    final_std     REAL NOT NULL,
    success_rate  REAL,
    created_at    TEXT NOT NULL
);
CREATE TABLE reflections (
    note_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id           TEXT NOT NULL REFERENCES runs(run_id) ON DELETE CASCADE,
    facts_json       TEXT NOT NULL,
    note_text        TEXT NOT NULL,
    source           TEXT NOT NULL,          -- llm | template
    grounding_passed INTEGER NOT NULL,
    grounding_report TEXT,
    created_at       TEXT NOT NULL
);
CREATE TABLE feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    note_id     INTEGER NOT NULL REFERENCES reflections(note_id) ON DELETE CASCADE,
    accurate    INTEGER NOT NULL,
    usefulness  INTEGER NOT NULL,
    comment     TEXT,
    created_at  TEXT NOT NULL
);
""",
}
SCHEMA_VERSION = max(MIGRATIONS)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _json(value: Any) -> str:
    return json.dumps(value, default=str)


class Database:
    """Thin data-access layer. Each call opens a short-lived connection (safe for Streamlit reruns)."""

    def __init__(self, path: str | Path = DEFAULT_DB) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.migrate()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        try:
            con = sqlite3.connect(self.path, timeout=30)
        except sqlite3.Error as exc:
            raise StoreError(f"Cannot open database {self.path}: {exc}") from exc
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        con.execute("PRAGMA synchronous = NORMAL")
        try:
            yield con
            con.commit()
        except sqlite3.Error as exc:
            con.rollback()
            raise StoreError(f"Database error: {exc}") from exc
        finally:
            con.close()

    # ---------------------------------------------------------------- schema
    def schema_version(self) -> int:
        with self._connect() as con:
            return int(con.execute("PRAGMA user_version").fetchone()[0])

    def migrate(self) -> int:
        """Apply every migration newer than the stored schema version."""
        with self._connect() as con:
            con.execute("PRAGMA journal_mode = WAL")  # readers (dashboard) never block the trainer
            current = int(con.execute("PRAGMA user_version").fetchone()[0])
            for version in sorted(v for v in MIGRATIONS if v > current):
                con.executescript(MIGRATIONS[version])
                con.execute(f"PRAGMA user_version = {version}")
        return self.schema_version()

    # ----------------------------------------------------------- experiments
    def create_experiment(self, name: str, kind: str, env: str | None = None, algorithm: str | None = None,
                          config: dict[str, Any] | None = None, seeds: list[int] | None = None,
                          git_sha: str | None = None) -> int:
        with self._connect() as con:
            cur = con.execute(
                "INSERT INTO experiments (name, kind, env, algorithm, config_json, seeds_json, git_sha, created_at)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (name, kind, env, algorithm, _json(config or {}), _json(seeds or []), git_sha, now()))
            return int(cur.lastrowid)

    def finish_experiment(self, experiment_id: int, status: str, summary: dict[str, Any] | None = None) -> None:
        with self._connect() as con:
            con.execute("UPDATE experiments SET status = ?, summary_json = ?, finished_at = ? WHERE experiment_id = ?",
                        (status, _json(summary) if summary is not None else None, now(), experiment_id))

    def get_experiment(self, experiment_id: int) -> dict[str, Any] | None:
        with self._connect() as con:
            row = con.execute("SELECT * FROM experiments WHERE experiment_id = ?", (experiment_id,)).fetchone()
        if row is None:
            return None
        exp = dict(row)
        exp["config"] = json.loads(exp.pop("config_json") or "{}")
        exp["seeds"] = json.loads(exp.pop("seeds_json") or "[]")
        exp["summary"] = json.loads(exp.pop("summary_json")) if exp.get("summary_json") else None
        return exp

    def list_experiments(self, kind: str | None = None) -> pd.DataFrame:
        sql = "SELECT * FROM experiments" + (" WHERE kind = ?" if kind else "") + " ORDER BY experiment_id DESC"
        return self._df(sql, (kind,) if kind else ())

    # ------------------------------------------------------------------ runs
    def start_run(self, run_id: str, env: str, algorithm: str, seed: int, config: dict[str, Any],
                  run_dir: str | None = None, git_sha: str | None = None, experiment_id: int | None = None,
                  variant: str | None = None) -> None:
        with self._connect() as con:
            con.execute(
                "INSERT INTO runs (run_id, experiment_id, env, algorithm, seed, variant, config_json, run_dir,"
                " git_sha, status, started_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'running', ?)"
                " ON CONFLICT(run_id) DO UPDATE SET status = 'running', ended_at = NULL, error = NULL",
                (run_id, experiment_id, env, algorithm, seed, variant, _json(config), run_dir, git_sha, now()))

    def finish_run(self, run_id: str, status: str, episodes_completed: int | None = None,
                   stopped_reason: str | None = None, error: str | None = None) -> None:
        with self._connect() as con:
            con.execute(
                "UPDATE runs SET status = ?, stopped_reason = COALESCE(?, stopped_reason),"
                " episodes_completed = COALESCE(?, episodes_completed), error = ?, ended_at = ? WHERE run_id = ?",
                (status, stopped_reason, episodes_completed, error, now(), run_id))

    def set_checkpoints(self, run_id: str, latest: str | None = None, best: str | None = None) -> None:
        with self._connect() as con:
            con.execute("UPDATE runs SET latest_checkpoint = COALESCE(?, latest_checkpoint),"
                        " best_checkpoint = COALESCE(?, best_checkpoint) WHERE run_id = ?", (latest, best, run_id))

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        with self._connect() as con:
            row = con.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,)).fetchone()
        if row is None:
            return None
        run = dict(row)
        run["config"] = json.loads(run.pop("config_json"))
        return run

    def list_runs(self, experiment_id: int | None = None) -> pd.DataFrame:
        sql = "SELECT * FROM runs" + (" WHERE experiment_id = ?" if experiment_id is not None else "")
        return self._df(sql + " ORDER BY started_at DESC", (experiment_id,) if experiment_id is not None else ())

    def delete_run(self, run_id: str) -> None:
        with self._connect() as con:
            con.execute("DELETE FROM runs WHERE run_id = ?", (run_id,))

    # -------------------------------------------------------------- episodes
    def log_episode(self, run_id: str, info: Any) -> None:
        with self._connect() as con:
            con.execute(
                "INSERT OR REPLACE INTO episodes (run_id, episode, total_reward, length, epsilon, mean_loss,"
                " end_reason, wall_time_s) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (run_id, info.episode, info.total_reward, info.length, info.epsilon, info.mean_loss,
                 info.end_reason, info.wall_time_s))
            con.execute("UPDATE runs SET episodes_completed = MAX(episodes_completed, ?) WHERE run_id = ?",
                        (info.episode + 1, run_id))

    def query_episodes(self, run_id: str) -> pd.DataFrame:
        return self._df("SELECT * FROM episodes WHERE run_id = ? ORDER BY episode", (run_id,))

    # --------------------------------------------------------------- metrics
    def log_metric(self, run_id: str, name: str, value: float | None, step: int | None = None) -> None:
        with self._connect() as con:
            con.execute("INSERT INTO metrics (run_id, name, value, step, created_at) VALUES (?, ?, ?, ?, ?)",
                        (run_id, name, value, step, now()))

    def query_metrics(self, run_id: str) -> pd.DataFrame:
        return self._df("SELECT name, value, step, created_at FROM metrics WHERE run_id = ? ORDER BY rowid",
                        (run_id,))

    # ----------------------------------------------------------- evaluations
    def log_evaluation(self, run_id: str, kind: str, result: Any, episode: int | None = None,
                       seed_base: int | None = None, checkpoint: str | None = None) -> int:
        with self._connect() as con:
            cur = con.execute(
                "INSERT INTO evaluations (run_id, kind, episode, mean_return, std_return, median_return,"
                " success_rate, mean_length, n_episodes, seed_base, checkpoint, returns_json, created_at)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (run_id, kind, episode, result.mean_return, result.std_return, result.median_return,
                 result.success_rate, result.mean_length, result.n_episodes, seed_base, checkpoint,
                 _json(list(result.returns)), now()))
            return int(cur.lastrowid)

    def query_evaluations(self, run_id: str | None = None, kind: str | None = None) -> pd.DataFrame:
        where, params = [], []
        if run_id is not None:
            where.append("e.run_id = ?")
            params.append(run_id)
        if kind is not None:
            where.append("e.kind = ?")
            params.append(kind)
        sql = ("SELECT e.*, r.env, r.algorithm, r.seed, r.variant, r.experiment_id FROM evaluations e"
               " JOIN runs r ON r.run_id = e.run_id" + (" WHERE " + " AND ".join(where) if where else "")
               + " ORDER BY e.eval_id")
        return self._df(sql, tuple(params))

    # -------------------------------------------------------------- ablation
    def log_ablation(self, experiment_id: int, variant: str, seed: int, run_id: str | None, final_mean: float,
                     final_std: float, success_rate: float | None = None) -> None:
        with self._connect() as con:
            con.execute(
                "INSERT INTO ablation_results (experiment_id, variant, seed, run_id, final_mean, final_std,"
                " success_rate, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (experiment_id, variant, seed, run_id, final_mean, final_std, success_rate, now()))

    def query_ablation(self, experiment_id: int | None = None) -> pd.DataFrame:
        sql = "SELECT * FROM ablation_results" + (" WHERE experiment_id = ?" if experiment_id is not None else "")
        return self._df(sql + " ORDER BY ablation_id", (experiment_id,) if experiment_id is not None else ())

    # ----------------------------------------------------------- reflections
    def add_reflection(self, run_id: str, facts: dict[str, Any], note_text: str, source: str,
                       grounding_passed: bool, grounding_report: dict[str, Any] | None = None) -> int:
        with self._connect() as con:
            cur = con.execute(
                "INSERT INTO reflections (run_id, facts_json, note_text, source, grounding_passed,"
                " grounding_report, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (run_id, _json(facts), note_text, source, int(grounding_passed), _json(grounding_report or {}),
                 now()))
            return int(cur.lastrowid)

    def query_reflections(self, run_id: str | None = None) -> pd.DataFrame:
        sql = "SELECT * FROM reflections" + (" WHERE run_id = ?" if run_id else "")
        return self._df(sql + " ORDER BY note_id DESC", (run_id,) if run_id else ())

    def get_reflection(self, note_id: int) -> dict[str, Any] | None:
        with self._connect() as con:
            row = con.execute("SELECT * FROM reflections WHERE note_id = ?", (note_id,)).fetchone()
        return dict(row) if row else None

    def add_feedback(self, note_id: int, accurate: bool, usefulness: int, comment: str | None) -> int:
        with self._connect() as con:
            cur = con.execute("INSERT INTO feedback (note_id, accurate, usefulness, comment, created_at)"
                              " VALUES (?, ?, ?, ?, ?)", (note_id, int(accurate), usefulness, comment, now()))
            return int(cur.lastrowid)

    def query_feedback(self, note_id: int | None = None) -> pd.DataFrame:
        sql = "SELECT * FROM feedback" + (" WHERE note_id = ?" if note_id is not None else "")
        return self._df(sql + " ORDER BY feedback_id", (note_id,) if note_id is not None else ())

    # --------------------------------------------------------------- helpers
    def counts(self) -> dict[str, int]:
        with self._connect() as con:
            return {t: int(con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]) for t in
                    ("experiments", "runs", "episodes", "evaluations", "ablation_results", "reflections")}

    def _df(self, sql: str, params: tuple = ()) -> pd.DataFrame:
        with self._connect() as con:
            return pd.read_sql_query(sql, con, params=params)
