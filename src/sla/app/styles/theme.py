"""Design tokens and global CSS for the dashboard (dark theme, validated categorical palette)."""

from __future__ import annotations

import streamlit as st

# Chart chrome & ink (dark surface) - see docs/architecture.md "Dashboard design system".
INK = {
    "page": "#0d0d0d", "surface": "#1a1a19", "surface_2": "#222220", "primary": "#ffffff",
    "secondary": "#c3c2b7", "muted": "#898781", "grid": "#2c2c2a", "axis": "#383835",
    "border": "rgba(255,255,255,0.10)",
}
# Categorical slots, fixed order (validated all-pairs for 3 slots on the dark surface).
SERIES = ["#3987e5", "#d95926", "#199e70"]
STATUS = {"good": "#0ca30c", "warning": "#fab219", "serious": "#ec835a", "critical": "#d03b3b"}
# Identity colours follow the entity, never its rank.
AGENT_COLORS = {"Q-learning": SERIES[0], "DQN": SERIES[1], "Random": INK["muted"]}
VARIANT_COLORS = {"full": SERIES[0], "no_replay": SERIES[1], "no_target": SERIES[2]}
VARIANT_LABELS = {"full": "Full DQN", "no_replay": "No replay", "no_target": "No target network"}

CSS = f"""
<style>
:root {{ --surface: {INK['surface']}; --border: {INK['border']}; --muted: {INK['muted']};
        --secondary: {INK['secondary']}; }}
html, body, [class*="css"] {{ font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }}
.block-container {{ padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1400px; }}
h1, h2, h3 {{ letter-spacing: -0.01em; }}
.sla-hero {{ display:flex; align-items:center; justify-content:space-between; gap:1rem;
  padding: 1.1rem 1.3rem; border:1px solid var(--border); border-radius: 14px;
  background: linear-gradient(135deg, rgba(57,135,229,0.16), rgba(25,158,112,0.06) 60%, transparent);
  margin-bottom: 1.1rem; }}
.sla-hero h1 {{ font-size: 1.55rem; margin: 0; font-weight: 650; }}
.sla-hero p {{ margin: .25rem 0 0 0; color: var(--secondary); font-size: .93rem; }}
.sla-card {{ border:1px solid var(--border); border-radius: 12px; background: var(--surface);
  padding: .9rem 1rem; height: 100%; }}
.sla-card .label {{ color: var(--muted); font-size: .76rem; text-transform: uppercase; letter-spacing: .06em; }}
.sla-card .value {{ font-size: 1.55rem; font-weight: 650; margin-top: .2rem; line-height: 1.2; }}
.sla-card .sub {{ color: var(--secondary); font-size: .8rem; margin-top: .25rem; }}
.sla-card .value.notrun {{ color: var(--muted); font-size: 1.05rem; font-weight: 600; letter-spacing: .04em; }}
.sla-badge {{ display:inline-flex; align-items:center; gap:.35rem; padding: .15rem .6rem; border-radius: 999px;
  font-size: .76rem; font-weight: 600; border:1px solid var(--border); background: rgba(255,255,255,0.04); }}
.sla-badge .dot {{ width:.5rem; height:.5rem; border-radius:50%; display:inline-block; }}
.sla-section {{ margin: 1.4rem 0 .6rem 0; }}
.sla-section h3 {{ margin: 0; font-size: 1.08rem; font-weight: 650; }}
.sla-section p {{ margin: .2rem 0 0 0; color: var(--muted); font-size: .85rem; }}
.sla-empty {{ border:1px dashed var(--border); border-radius: 12px; padding: 1.4rem; text-align:center;
  color: var(--secondary); background: rgba(255,255,255,0.02); }}
.sla-empty b {{ color: #fff; letter-spacing: .05em; }}
.sla-empty code {{ font-size: .82rem; }}
.sla-note {{ border-left: 3px solid {SERIES[0]}; background: var(--surface); padding: .8rem 1rem;
  border-radius: 0 10px 10px 0; line-height: 1.55; }}
div[data-testid="stMetric"] {{ background: var(--surface); border:1px solid var(--border); border-radius:12px;
  padding:.7rem .9rem; }}
section[data-testid="stSidebar"] {{ border-right: 1px solid var(--border); }}
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
