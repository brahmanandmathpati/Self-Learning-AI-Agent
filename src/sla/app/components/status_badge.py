"""Status badges: an icon/dot + a text label (status is never shown by colour alone)."""

from __future__ import annotations

import html

from sla.app.styles.theme import INK, STATUS

# kind -> (colour, label, pulsing dot?)
_STYLE = {
    "completed": (STATUS["good"], "Completed", False),
    "running": (STATUS["warning"], "Training", True),
    "live": (STATUS["good"], "Live", True),
    "stopped": (STATUS["serious"], "Stopped", False),
    "failed": (STATUS["critical"], "Failed", False),
    "pass": (STATUS["good"], "Grounded", False),
    "reject": (STATUS["critical"], "Rejected", False),
    "online": (STATUS["good"], "Online", True),
    "offline": (INK["muted"], "Offline", False),
    "idle": (STATUS["info"], "Idle", False),
    "info": (STATUS["info"], "Info", False),
}
_ICON = {"completed": "✓", "pass": "✓", "failed": "✕", "reject": "✕", "stopped": "■"}


def badge(kind: str, text: str | None = None) -> str:
    """Pill with a coloured dot (pulsing for live states) and a text label."""
    color, label, pulse = _STYLE.get(kind, (INK["muted"], kind.title(), False))
    mark = _ICON.get(kind)
    dot = (f'<span style="color:{color};font-weight:800">{mark}</span>' if mark else
           f'<span class="sla-dot{" pulse" if pulse else ""}" style="--c:{color}"></span>')
    return f'<span class="sla-badge">{dot}{html.escape(text or label)}</span>'


def run_state(status: str | None) -> str:
    """Human label for the overall training state."""
    if status == "running":
        return "running"
    if status == "completed":
        return "completed"
    if status in ("stopped", "failed"):
        return status
    return "idle"
