"""Shared, thread-safe state for the Vision Lab.

The live webcam callback (streamlit-webrtc) runs in its own thread, so samples, the learner and the latest prediction
live in one ``LiveState`` object guarded by a lock. It is kept in ``st.session_state`` — one per browser session — and
holds landmark numbers only. Images are never stored unless the user ticks "save images" (then they go to
``runs/vision_images/``, which is git-ignored and removed by "Delete my data").
"""

from __future__ import annotations

import importlib.util
import shutil
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import streamlit as st

from sla import settings
from sla.vision.features import normalise
from sla.vision.learners import KNNLearner, MLPLearner

DEFAULT_CLASSES = ["👍 Thumbs up", "👎 Thumbs down", "✋ Open palm", "✊ Fist"]
MIN_PER_CLASS = 10
RECORD_EVERY_S = 0.2  # at most 5 samples per second while recording


def available() -> bool:
    """True when the optional vision packages (mediapipe, OpenCV) are installed."""
    return all(importlib.util.find_spec(m) is not None for m in ("mediapipe", "cv2"))


def webrtc_available() -> bool:
    return all(importlib.util.find_spec(m) is not None for m in ("streamlit_webrtc", "av"))


@st.cache_resource(show_spinner="Loading the hand model (first time only)…")
def detector():
    from sla.vision.hands import HandDetector
    return HandDetector()


def images_dir() -> Path:
    return settings.run_root() / "vision_images"


@dataclass
class Prediction:
    label: str | None
    proba: dict[str, float]
    at: float
    hand: bool = False  # a hand was found (label can still be None when nothing has been learned yet)


@dataclass
class LiveState:
    classes: list[str] = field(default_factory=lambda: list(DEFAULT_CLASSES))
    X: list[np.ndarray] = field(default_factory=list)
    y: list[str] = field(default_factory=list)
    src: list[str] = field(default_factory=list)
    knn: KNNLearner = field(default_factory=KNNLearner)
    mlp: MLPLearner | None = None
    use_mlp: bool = False
    recording: str | None = None
    save_images: bool = False
    last: Prediction | None = None
    recent: deque = field(default_factory=lambda: deque(maxlen=8))  # recent labels, for stable gesture detection
    frame_ms: deque = field(default_factory=lambda: deque(maxlen=60))
    frame_times: deque = field(default_factory=lambda: deque(maxlen=30))
    _last_rec: float = 0.0
    det: object = None  # the HandDetector, set from the script thread (the webcam thread must not touch st.cache)
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    # ------------------------------------------------------------------ data
    def add(self, x: np.ndarray, label: str, source: str) -> None:
        with self.lock:
            self.X.append(np.asarray(x, dtype=np.float32))
            self.y.append(label)
            self.src.append(source)
            self.knn.add(x, label)
            self.mlp = None  # the network must be retrained to include the new sample

    def counts(self) -> dict[str, int]:
        with self.lock:
            return {c: self.y.count(c) for c in self.classes}

    def arrays(self) -> tuple[np.ndarray, list[str]]:
        with self.lock:
            return (np.vstack(self.X) if self.X else np.zeros((0, 42), np.float32)), list(self.y)

    def ready(self) -> bool:
        """At least two classes with MIN_PER_CLASS samples each."""
        return sum(n >= MIN_PER_CLASS for n in self.counts().values()) >= 2

    def clear(self) -> None:
        with self.lock:
            self.X, self.y, self.src = [], [], []
            self.knn, self.mlp, self.last = KNNLearner(), None, None
            self.recent.clear()
        shutil.rmtree(images_dir(), ignore_errors=True)

    def load(self, X: np.ndarray, y: list[str], classes: list[str]) -> None:
        with self.lock:
            self.X = [np.asarray(r, dtype=np.float32) for r in X]
            self.y, self.src = list(y), ["saved model"] * len(y)
            self.classes = list(dict.fromkeys(list(classes) + sorted(set(y))))
            self.knn = KNNLearner().fit(np.asarray(X, dtype=np.float32), list(y))
            self.mlp = None

    def train_mlp(self) -> MLPLearner:
        X, y = self.arrays()
        model = MLPLearner().fit(X, y)
        with self.lock:
            self.mlp = model
        return model

    # ------------------------------------------------------------------ prediction
    def predict(self, x: np.ndarray) -> dict[str, float]:
        with self.lock:
            model = self.mlp if (self.use_mlp and self.mlp is not None) else self.knn
            return model.predict_proba(x) if model.classes else {}

    def stable_gesture(self, min_conf: float = 0.7, frames: int = 4) -> str | None:
        """The gesture shown in the last ``frames`` predictions (all the same, confident, and recent)."""
        with self.lock:
            items = list(self.recent)[-frames:]
        if len(items) < frames or time.time() - items[-1][2] > 1.0:
            return None
        labels = {lbl for lbl, conf, _ in items}
        if len(labels) == 1 and all(conf >= min_conf for _, conf, _ in items):
            return labels.pop()
        return None

    def fps(self) -> float:
        with self.lock:
            t = list(self.frame_times)
        return (len(t) - 1) / (t[-1] - t[0]) if len(t) > 1 and t[-1] > t[0] else 0.0

    def mean_ms(self) -> float:
        with self.lock:
            return float(np.mean(self.frame_ms)) if self.frame_ms else 0.0

    # ------------------------------------------------------------------ one frame (webcam, snapshot or upload)
    def process(self, rgb: np.ndarray, source: str = "webcam", record: bool = True) -> tuple[np.ndarray, Prediction]:
        """Detect the hand, predict, optionally record a sample, and return the annotated frame."""
        from sla.vision.hands import draw
        det = self.det if self.det is not None else detector()
        t0 = time.perf_counter()
        hands = det.detect(rgb)
        out, pred = rgb, Prediction(None, {}, time.time())
        if hands:
            hand = hands[0]
            x = normalise(hand.landmarks, hand.handedness)
            proba = self.predict(x)
            label = next(iter(proba), None)
            pred = Prediction(label, proba, time.time(), hand=True)
            now = time.time()
            if record and self.recording and now - self._last_rec >= RECORD_EVERY_S:
                self._last_rec = now
                self.add(x, self.recording, source)
                if self.save_images:
                    self._save_image(rgb, self.recording)
            tag = f"{label} {proba[label]:.0%}" if label else ("recording…" if self.recording else "hand")
            out = draw(rgb, hand, tag)
        with self.lock:
            self.last = pred
            if pred.label:
                self.recent.append((pred.label, pred.proba[pred.label], pred.at))
            self.frame_ms.append((time.perf_counter() - t0) * 1000)
            self.frame_times.append(time.time())
        return out, pred

    def _save_image(self, rgb: np.ndarray, label: str) -> None:
        import cv2
        folder = images_dir() / "".join(ch if ch.isalnum() else "_" for ch in label).strip("_")
        folder.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(folder / f"{time.time_ns()}.jpg"), cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))


def state() -> LiveState:
    if "vision_live" not in st.session_state:
        st.session_state["vision_live"] = LiveState()
    return st.session_state["vision_live"]


# ---------------------------------------------------------------------- WebRTC (live video)
def ice_servers() -> list[dict]:
    """STUN by default; TURN from secrets so the webcam also connects on Streamlit Community Cloud.

    ``[webrtc] cloudflare_key_id`` + ``cloudflare_api_token`` (free Cloudflare TURN), or ``[webrtc] ice_servers``
    as a list of {urls, username, credential}.
    """
    try:
        cfg = dict(st.secrets.get("webrtc", {}))
    except Exception:  # noqa: BLE001
        cfg = {}
    if cfg.get("ice_servers"):
        return list(cfg["ice_servers"])
    if cfg.get("cloudflare_key_id") and cfg.get("cloudflare_api_token"):
        try:
            return _cloudflare_ice(cfg["cloudflare_key_id"], cfg["cloudflare_api_token"])
        except Exception:  # noqa: BLE001 - fall back to STUN; the snapshot mode still works
            pass
    return [{"urls": ["stun:stun.l.google.com:19302"]}]


@st.cache_data(ttl=3600, show_spinner=False)
def _cloudflare_ice(key_id: str, token: str) -> list[dict]:
    import requests
    r = requests.post(f"https://rtc.live.cloudflare.com/v1/turn/keys/{key_id}/credentials/generate-ice-servers",
                      headers={"Authorization": f"Bearer {token}"}, json={"ttl": 7200}, timeout=10)
    r.raise_for_status()
    return r.json()["iceServers"]


def frame_callback(live: LiveState):
    """The per-frame function streamlit-webrtc calls in its worker thread."""
    import av

    def callback(frame):
        rgb = frame.to_ndarray(format="rgb24")
        out, _ = live.process(rgb, "webcam")
        return av.VideoFrame.from_ndarray(out, format="rgb24")
    return callback
