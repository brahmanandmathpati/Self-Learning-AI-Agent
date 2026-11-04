"""Hand detection with MediaPipe's Hand Landmarker (21 points per hand), run locally on the CPU.

The model file (~7.8 MB) is downloaded once from Google's public model storage into ``runs/models/`` (git-ignored)
and reused. Images are processed in memory; nothing is uploaded anywhere.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from sla import settings
from sla.vision.features import CONNECTIONS

MODEL_URL = ("https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/"
             "hand_landmarker.task")


def model_path() -> Path:
    return settings.run_root() / "models" / "hand_landmarker.task"


def ensure_model() -> Path:
    """Download the hand model once (atomic write) and return its path."""
    path = model_path()
    if path.is_file() and path.stat().st_size > 1_000_000:
        return path
    import requests
    path.parent.mkdir(parents=True, exist_ok=True)
    resp = requests.get(MODEL_URL, timeout=60)
    resp.raise_for_status()
    tmp = path.with_suffix(".part")
    tmp.write_bytes(resp.content)
    tmp.replace(path)
    return path


@dataclass
class Hand:
    landmarks: np.ndarray  # (21, 3) in image coordinates 0..1
    handedness: str        # "Left" | "Right" (as seen by the camera)
    score: float


class HandDetector:
    """Thread-safe wrapper (the webcam callback runs in its own thread)."""

    def __init__(self, max_hands: int = 1, min_confidence: float = 0.5) -> None:
        from mediapipe.tasks import python as mp_python
        from mediapipe.tasks.python import vision
        options = vision.HandLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=str(ensure_model())),
            running_mode=vision.RunningMode.IMAGE, num_hands=max_hands,
            min_hand_detection_confidence=min_confidence, min_hand_presence_confidence=min_confidence)
        self._landmarker = vision.HandLandmarker.create_from_options(options)
        self._lock = threading.Lock()
        self.last_ms = 0.0

    def detect(self, rgb: np.ndarray, max_side: int = 480) -> list[Hand]:
        """Find hands in an RGB uint8 image (H, W, 3). Big frames are shrunk first (landmarks are relative 0..1,
        so the result does not change, but detection is faster)."""
        import mediapipe as mp
        h, w = rgb.shape[:2]
        if max(h, w) > max_side:
            import cv2
            s = max_side / max(h, w)
            rgb = cv2.resize(rgb, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
        img = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb, dtype=np.uint8))
        t0 = time.perf_counter()
        with self._lock:
            res = self._landmarker.detect(img)
        self.last_ms = (time.perf_counter() - t0) * 1000
        hands = []
        for lms, hd in zip(res.hand_landmarks, res.handedness):
            pts = np.array([[p.x, p.y, p.z] for p in lms], dtype=np.float32)
            hands.append(Hand(pts, hd[0].category_name, float(hd[0].score)))
        return hands


def draw(rgb: np.ndarray, hand: Hand, label: str | None = None, color=(201, 162, 75)) -> np.ndarray:
    """Draw the 21-point skeleton (gold) and an optional label onto a copy of the image."""
    import cv2
    out = rgb.copy()
    h, w = out.shape[:2]
    pts = [(int(x * w), int(y * h)) for x, y, _ in hand.landmarks]
    for a, b in CONNECTIONS:
        cv2.line(out, pts[a], pts[b], color, 2, cv2.LINE_AA)
    for p in pts:
        cv2.circle(out, p, 4, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(out, p, 4, (79, 70, 229), 1, cv2.LINE_AA)
    label = "".join(ch for ch in (label or "") if ord(ch) < 128).strip()  # OpenCV cannot draw emoji
    if label:
        x0, y0 = min(p[0] for p in pts), max(0, min(p[1] for p in pts) - 12)
        cv2.putText(out, label, (x0, y0), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (15, 23, 42), 4, cv2.LINE_AA)
        cv2.putText(out, label, (x0, y0), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    return out
