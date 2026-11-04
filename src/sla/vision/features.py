"""Turn 21 hand landmarks into a 42-number feature vector that ignores where the hand is and how big it looks.

Steps: (1) mirror left hands so both hands look like right hands, (2) move the wrist to (0, 0), (3) divide by the
hand size (wrist → middle-finger knuckle distance, or the farthest point if that is tiny). Only x and y are used;
MediaPipe's z is noisy. The result depends on the *shape* of the hand, not on the camera, lighting or skin.
"""

from __future__ import annotations

import numpy as np

N_POINTS = 21
N_FEATURES = 2 * N_POINTS
WRIST, MIDDLE_MCP = 0, 9
# Pairs of landmark indices that form the hand skeleton (for drawing).
CONNECTIONS = [(0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (7, 8), (5, 9), (9, 10), (10, 11),
               (11, 12), (9, 13), (13, 14), (14, 15), (15, 16), (13, 17), (0, 17), (17, 18), (18, 19), (19, 20)]


def normalise(landmarks: np.ndarray, handedness: str = "Right") -> np.ndarray:
    """(21, 2|3) landmarks in image coordinates (0..1) → (42,) translation-, scale- and hand-invariant features."""
    pts = np.asarray(landmarks, dtype=np.float64)
    if pts.ndim != 2 or pts.shape[0] != N_POINTS or pts.shape[1] < 2:
        raise ValueError(f"expected {N_POINTS} landmarks with x, y; got shape {pts.shape}")
    xy = pts[:, :2].copy()
    if handedness.lower().startswith("l"):
        xy[:, 0] = -xy[:, 0]  # mirror a left hand so it matches a right hand
    xy -= xy[WRIST]
    scale = float(np.linalg.norm(xy[MIDDLE_MCP]))
    if scale < 1e-6:
        scale = float(np.linalg.norm(xy, axis=1).max())
    if scale < 1e-9:
        raise ValueError("degenerate hand: all landmarks at the same point")
    return (xy / scale).reshape(-1).astype(np.float32)
