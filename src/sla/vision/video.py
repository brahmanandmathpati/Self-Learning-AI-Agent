"""Sample frames from a short uploaded video (default 5 frames per second, at most 30 seconds)."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import numpy as np

MAX_SECONDS = 30


def sample_times(duration_s: float, fps: float = 5.0, max_seconds: float = MAX_SECONDS) -> list[float]:
    """Timestamps (seconds) to sample: every 1/fps seconds up to min(duration, max_seconds)."""
    end = min(max(duration_s, 0.0), max_seconds)
    n = int(end * fps + 1e-9)
    return [round(i / fps, 6) for i in range(n)]


def frames(path: str | Path, fps: float = 5.0, max_seconds: float = MAX_SECONDS,
           max_side: int = 640) -> Iterator[tuple[float, np.ndarray]]:
    """Yield (time_s, RGB frame) pairs. Large frames are shrunk so the longest side is ``max_side``."""
    import cv2
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise ValueError("could not open the video (try an .mp4 file)")
    try:
        src_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        count = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
        duration = count / src_fps if count > 0 else max_seconds
        for t in sample_times(duration, fps, max_seconds):
            cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
            ok, bgr = cap.read()
            if not ok:
                break
            h, w = bgr.shape[:2]
            s = max_side / max(h, w)
            if s < 1:
                bgr = cv2.resize(bgr, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
            yield t, cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    finally:
        cap.release()
