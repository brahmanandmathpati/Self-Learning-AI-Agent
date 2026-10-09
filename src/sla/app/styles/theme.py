# ruff: noqa: E501  (CSS block)
"""Design system for the dashboard: tokens + global CSS ("AI Learning Laboratory", dark).

Colour roles
- SERIES are the validated categorical chart colours (identity follows the entity, never its rank).
- STATUS colours are always paired with an icon/label, never used alone.
Motion
- Every animation is CSS-only and switched off under ``prefers-reduced-motion``.
"""

from __future__ import annotations

import streamlit as st

INK = {
    "page": "#070a12", "surface": "#0e1320", "surface_2": "#141b2b", "primary": "#f4f7fb",
    "secondary": "#b6c0d2", "muted": "#7d879c", "grid": "rgba(148,163,184,0.10)", "axis": "rgba(148,163,184,0.22)",
    "border": "rgba(148,163,184,0.14)",
}
ACCENT = "#5b9cf0"
SERIES = ["#3987e5", "#d95926", "#199e70"]
STATUS = {"good": "#22c55e", "warning": "#f5b83d", "serious": "#f08a5d", "critical": "#ef5350", "info": ACCENT}
AGENT_COLORS = {"Q-learning": SERIES[0], "DQN": SERIES[1], "Random": "#8a94a6"}
VARIANT_COLORS = {"full": SERIES[0], "no_replay": SERIES[1], "no_target": SERIES[2]}
VARIANT_LABELS = {"full": "Full DQN", "no_replay": "No replay", "no_target": "No target network"}

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
:root {{
  --page:{INK['page']}; --surface:{INK['surface']}; --surface2:{INK['surface_2']}; --border:{INK['border']};
  --ink:{INK['primary']}; --secondary:{INK['secondary']}; --muted:{INK['muted']}; --accent:{ACCENT};
  --blue:{SERIES[0]}; --orange:{SERIES[1]}; --aqua:{SERIES[2]};
  --good:{STATUS['good']}; --warn:{STATUS['warning']}; --bad:{STATUS['critical']};
  --radius:14px; --ease:cubic-bezier(.2,.7,.2,1);
}}
html, body, [class*="css"], .stMarkdown, button, input, textarea, select {{
  font-family: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif; }}
code, pre, .mono {{ font-family: "JetBrains Mono", ui-monospace, monospace !important; }}

/* ---------- canvas ---------- */
.stApp {{ background:
  radial-gradient(1200px 600px at 85% -10%, rgba(57,135,229,.14), transparent 60%),
  radial-gradient(900px 500px at -10% 110%, rgba(25,158,112,.08), transparent 60%), var(--page); }}
.stApp::before {{ content:""; position:fixed; inset:0; pointer-events:none; z-index:0; opacity:.35;
  background-image: linear-gradient(rgba(148,163,184,.05) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(148,163,184,.05) 1px, transparent 1px);
  background-size: 44px 44px; mask-image: radial-gradient(ellipse at 50% 0%, #000 30%, transparent 75%);
  animation: sla-drift 60s linear infinite; }}
@keyframes sla-drift {{ from {{ background-position:0 0, 0 0; }} to {{ background-position:44px 44px, 44px 44px; }} }}
header[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ padding-top: 2.2rem; padding-bottom: 4rem; max-width: 1360px; position:relative; z-index:1; }}
h1, h2, h3, h4 {{ letter-spacing: -0.015em; color: var(--ink); }}
p, li {{ color: var(--secondary); }}

/* ---------- entrance motion ---------- */
@keyframes sla-up {{ from {{ opacity:0; transform: translateY(8px); }} to {{ opacity:1; transform:none; }} }}
.sla-anim, .sla-hero, .sla-card, .sla-panel, .sla-section, .sla-empty, .sla-insight {{
  animation: sla-up .45s var(--ease) both; }}
.sla-grid > *:nth-child(2) {{ animation-delay:.04s; }} .sla-grid > *:nth-child(3) {{ animation-delay:.08s; }}
.sla-grid > *:nth-child(4) {{ animation-delay:.12s; }} .sla-grid > *:nth-child(5) {{ animation-delay:.16s; }}
.sla-grid > *:nth-child(6) {{ animation-delay:.20s; }}

/* ---------- hero ---------- */
.sla-hero {{ position:relative; overflow:hidden; display:flex; align-items:flex-end; justify-content:space-between;
  gap:1.2rem; padding: 1.5rem 1.6rem; border:1px solid var(--border); border-radius: 18px; margin-bottom: 1.3rem;
  background: linear-gradient(135deg, rgba(57,135,229,.16), rgba(14,19,32,.85) 55%), var(--surface); }}
.sla-hero::after {{ content:""; position:absolute; right:-80px; top:-120px; width:340px; height:340px; border-radius:50%;
  background: radial-gradient(circle, rgba(91,156,240,.22), transparent 65%); pointer-events:none; }}
.sla-hero .eyebrow {{ font-size:.72rem; letter-spacing:.22em; text-transform:uppercase; color:var(--accent);
  font-weight:600; margin-bottom:.45rem; }}
.sla-hero h1 {{ font-size: 1.75rem; margin: 0; font-weight: 750; line-height:1.15; }}
.sla-hero.big h1 {{ font-size: 2.35rem; letter-spacing:-.025em; }}
.sla-hero p {{ margin: .45rem 0 0 0; color: var(--secondary); font-size: .97rem; max-width: 760px; }}
.sla-hero .right {{ display:flex; flex-wrap:wrap; justify-content:flex-end; gap:.45rem; z-index:1; }}

/* ---------- cards ---------- */
.sla-grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap:.75rem; margin:.2rem 0 .6rem; }}
.sla-card {{ position:relative; border:1px solid var(--border); border-radius: var(--radius); padding: .95rem 1.05rem;
  background: linear-gradient(180deg, rgba(255,255,255,.035), rgba(255,255,255,.01)), var(--surface);
  transition: transform .2s var(--ease), border-color .2s, box-shadow .2s; height:100%; }}
.sla-card:hover {{ transform: translateY(-2px); border-color: rgba(91,156,240,.45);
  box-shadow: 0 10px 30px -12px rgba(57,135,229,.45); }}
.sla-card .label {{ display:flex; align-items:center; gap:.45rem; color: var(--muted); font-size: .72rem;
  text-transform: uppercase; letter-spacing: .09em; font-weight:600; }}
.sla-card .label .ic {{ width:1.55rem; height:1.55rem; border-radius:8px; display:inline-flex; align-items:center;
  justify-content:center; background: rgba(91,156,240,.12); color: var(--accent); font-size:.85rem; }}
.sla-card .value {{ font-size: 1.6rem; font-weight: 700; margin-top: .45rem; line-height: 1.15; color: var(--ink);
  font-variant-numeric: tabular-nums; letter-spacing:-.02em; }}
.sla-card .sub {{ color: var(--muted); font-size: .78rem; margin-top: .3rem; line-height:1.35; }}
.sla-card .value.sm {{ font-size:1.15rem; }}
.sla-card .value.notrun {{ color: var(--muted); font-size: 1rem; font-weight: 650; letter-spacing: .08em; }}
.sla-card.accent::before {{ content:""; position:absolute; left:0; top:12px; bottom:12px; width:3px; border-radius:3px;
  background: var(--card-accent, var(--accent)); }}
.sla-card .delta {{ display:inline-block; margin-top:.35rem; font-size:.74rem; font-weight:600; padding:.05rem .45rem;
  border-radius:6px; background: rgba(34,197,94,.12); color: var(--good); }}
.sla-card .delta.neg {{ background: rgba(239,83,80,.12); color: var(--bad); }}

/* count-up (integers only; the real value is always the final state) */
@property --sla-n {{ syntax:'<integer>'; inherits:false; initial-value:0; }}
.sla-count {{ counter-reset: n var(--sla-n); animation: sla-count 1.1s var(--ease) both; }}
.sla-count::after {{ content: counter(n); }}
@keyframes sla-count {{ from {{ --sla-n: 0; }} }}

/* ---------- panels / containers ---------- */
.sla-panel {{ border:1px solid var(--border); border-radius: var(--radius); background: var(--surface); padding:1rem 1.1rem; }}
div[class*="st-key-card"] {{ border:1px solid var(--border); border-radius: var(--radius); padding: .9rem 1rem .4rem;
  background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.005)), var(--surface);
  animation: sla-up .45s var(--ease) both; }}
.stMarkdown p.sla-chart-title {{ font-size:.92rem !important; font-weight:650; color:var(--ink); margin:0 !important; line-height:1.3; }}
.stMarkdown p.sla-chart-sub {{ font-size:.76rem !important; color:var(--muted); margin:.1rem 0 .1rem !important; line-height:1.35; }}

/* ---------- badges & live dots ---------- */
.sla-badge {{ display:inline-flex; align-items:center; gap:.45rem; padding: .28rem .72rem; border-radius: 999px;
  font-size: .74rem; font-weight: 650; letter-spacing:.06em; text-transform:uppercase; border:1px solid var(--border);
  background: rgba(255,255,255,.04); color: var(--ink); white-space:nowrap; }}
.sla-dot {{ width:.5rem; height:.5rem; border-radius:50%; display:inline-block; background: var(--c, var(--muted));
  box-shadow: 0 0 0 0 var(--c); }}
.sla-dot.pulse {{ animation: sla-pulse 1.8s ease-out infinite; }}
@keyframes sla-pulse {{ 0% {{ box-shadow: 0 0 0 0 color-mix(in srgb, var(--c) 70%, transparent); }}
  70% {{ box-shadow: 0 0 0 .5rem transparent; }} 100% {{ box-shadow: 0 0 0 0 transparent; }} }}

/* ---------- section header ---------- */
.sla-section {{ display:flex; align-items:flex-end; justify-content:space-between; gap:1rem; margin: 1.7rem 0 .7rem; }}
.sla-section h3 {{ margin: 0; font-size: 1.12rem; font-weight: 700; display:flex; align-items:center; gap:.55rem; }}
.sla-section h3::before {{ content:""; width:.55rem; height:.55rem; border-radius:3px; background: var(--accent);
  box-shadow: 0 0 12px var(--accent); }}
.sla-section p {{ margin: .25rem 0 0 0; color: var(--muted); font-size: .84rem; }}

/* ---------- verdict ---------- */
.sla-verdict {{ display:flex; gap:1rem; align-items:center; border-radius: var(--radius); padding: 1rem 1.2rem;
  border:1px solid color-mix(in srgb, var(--c) 45%, transparent);
  background: linear-gradient(90deg, color-mix(in srgb, var(--c) 16%, transparent), transparent 70%), var(--surface);
  animation: sla-up .45s var(--ease) both; margin: .3rem 0 .9rem; }}
.sla-verdict .icon {{ width:2.6rem; height:2.6rem; flex:none; border-radius:12px; display:flex; align-items:center;
  justify-content:center; font-size:1.25rem; font-weight:800; color: var(--c);
  background: color-mix(in srgb, var(--c) 16%, transparent); }}
.sla-verdict .t {{ font-size:.95rem; font-weight:800; letter-spacing:.12em; color: var(--c); }}
.sla-verdict .d {{ font-size:.85rem; color: var(--secondary); margin-top:.15rem; }}

/* ---------- rank / comparison ---------- */
.sla-rank {{ display:inline-flex; align-items:center; justify-content:center; min-width:1.9rem; height:1.9rem;
  padding:0 .4rem; border-radius:9px; font-weight:800; font-size:.85rem; background: rgba(255,255,255,.06);
  color: var(--secondary); }}
.sla-rank.first {{ background: linear-gradient(135deg, #f5b83d, #d98a1a); color:#1b1206; }}
.sla-cmp-head {{ display:flex; align-items:center; justify-content:space-between; gap:.6rem; }}
.sla-cmp-name {{ display:flex; align-items:center; gap:.55rem; font-weight:700; color: var(--ink); font-size:1rem; }}
.sla-swatch {{ width:.7rem; height:.7rem; border-radius:3px; background: var(--c); display:inline-block; }}
.sla-bar {{ height:.45rem; border-radius:99px; background: rgba(255,255,255,.06); overflow:hidden; margin-top:.6rem; }}
.sla-bar > span {{ display:block; height:100%; border-radius:99px; background: var(--c);
  transform-origin:left; animation: sla-grow .9s var(--ease) both; }}
@keyframes sla-grow {{ from {{ transform: scaleX(0); }} }}
.sla-why {{ font-size:.8rem; color: var(--muted); margin-top:.55rem; line-height:1.45; }}

/* ---------- progress (live training) ---------- */
.sla-progress {{ border:1px solid var(--border); border-radius: var(--radius); background: var(--surface);
  padding:.85rem 1rem; margin-bottom:.8rem; }}
.sla-progress .row {{ display:flex; justify-content:space-between; align-items:center; gap:1rem; font-size:.82rem;
  color: var(--secondary); }}
.sla-progress .track {{ height:.55rem; border-radius:99px; background: rgba(255,255,255,.06); overflow:hidden; margin-top:.6rem; }}
.sla-progress .fill {{ height:100%; border-radius:99px; transition: width .4s var(--ease);
  background: linear-gradient(90deg, var(--blue), var(--aqua)); background-size: 200% 100%; position:relative; }}
.sla-progress .fill.live {{ background-image: linear-gradient(90deg, var(--blue), var(--aqua)),
  repeating-linear-gradient(45deg, rgba(255,255,255,.18) 0 8px, transparent 8px 16px);
  background-blend-mode: overlay; animation: sla-stripes 1s linear infinite; }}
@keyframes sla-stripes {{ to {{ background-position: 0 0, 32px 0; }} }}

/* ---------- skeleton ---------- */
.sla-skel {{ border-radius: var(--radius); height: var(--h, 90px); border:1px solid var(--border);
  background: linear-gradient(90deg, var(--surface) 25%, var(--surface2) 37%, var(--surface) 63%);
  background-size: 400% 100%; animation: sla-shimmer 1.4s ease infinite; }}
@keyframes sla-shimmer {{ 0% {{ background-position: 100% 50%; }} 100% {{ background-position: 0 50%; }} }}

/* ---------- empty / error ---------- */
.sla-empty {{ border:1px dashed rgba(148,163,184,.28); border-radius: var(--radius); padding: 1.6rem 1.4rem;
  text-align:center; background: rgba(255,255,255,.015); }}
.sla-empty .glyph {{ width:2.8rem; height:2.8rem; margin:0 auto .7rem; border-radius:14px; display:flex;
  align-items:center; justify-content:center; font-size:1.3rem; color: var(--accent); background: rgba(91,156,240,.10); }}
.sla-empty .tag {{ font-size:.7rem; font-weight:700; letter-spacing:.18em; color: var(--muted); }}
.sla-empty .what {{ color: var(--ink); font-weight:650; margin-top:.35rem; font-size:.98rem; }}
.sla-empty .next {{ color: var(--secondary); font-size:.86rem; margin-top:.3rem; }}
.sla-empty code {{ display:inline-block; margin-top:.7rem; font-size:.78rem; padding:.3rem .6rem; border-radius:8px;
  background: rgba(255,255,255,.05); border:1px solid var(--border); color: var(--secondary); }}
.sla-error {{ border:1px solid rgba(239,83,80,.4); border-radius: var(--radius); padding:1.1rem 1.2rem;
  background: linear-gradient(90deg, rgba(239,83,80,.10), transparent 70%), var(--surface); }}
.sla-error .t {{ color:#ff8a87; font-weight:700; }}
.sla-error .r {{ color: var(--secondary); font-size:.86rem; margin-top:.35rem; }}

/* ---------- insight (reflection) ---------- */
.sla-insight {{ position:relative; border-radius: 16px; padding: 1.2rem 1.3rem 1.1rem; border:1px solid rgba(91,156,240,.35);
  background: linear-gradient(135deg, rgba(57,135,229,.14), rgba(14,19,32,.9) 60%), var(--surface); }}
.sla-insight .h {{ display:flex; align-items:center; justify-content:space-between; gap:.6rem; flex-wrap:wrap; }}
.sla-insight .k {{ font-size:.72rem; font-weight:800; letter-spacing:.2em; color: var(--accent); display:flex; gap:.5rem;
  align-items:center; }}
.sla-insight .body {{ color: var(--ink); font-size:.98rem; line-height:1.7; margin-top:.75rem; }}
.sla-insight .meta {{ color: var(--muted); font-size:.76rem; margin-top:.8rem; }}
.sla-chips {{ display:flex; flex-wrap:wrap; gap:.45rem; margin-top:.5rem; }}
.sla-chip {{ display:inline-flex; flex-direction:column; gap:.05rem; padding:.45rem .7rem; border-radius:10px;
  border:1px solid var(--border); background: rgba(255,255,255,.03); min-width: 7.5rem; }}
.sla-chip .ck {{ font-size:.66rem; letter-spacing:.08em; text-transform:uppercase; color: var(--muted); font-weight:600; }}
.sla-chip .cv {{ font-size:.92rem; color: var(--ink); font-weight:650; font-variant-numeric: tabular-nums; }}

/* ---------- key/value ---------- */
.sla-kv {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap:.5rem; }}
.sla-kv div {{ border:1px solid var(--border); border-radius:10px; padding:.5rem .7rem; background: rgba(255,255,255,.02); }}
.sla-kv .k {{ font-size:.68rem; letter-spacing:.08em; text-transform:uppercase; color: var(--muted); font-weight:600; }}
.sla-kv .v {{ font-size:.88rem; color: var(--ink); font-family:"JetBrains Mono", monospace; word-break: break-all; }}

/* ---------- environment cards ---------- */
.sla-env-row {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:.7rem; }}
.sla-env-row .sla-card .value {{ font-size:1rem; font-weight:600; line-height:1.45; }}

/* ---------- streamlit widgets ---------- */
section[data-testid="stSidebar"] {{ background: linear-gradient(180deg, #0a0f1a, #070a12); border-right: 1px solid var(--border); }}
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] {{ border-radius:10px; transition: background .15s; }}
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] {{
  background: linear-gradient(90deg, rgba(57,135,229,.22), rgba(57,135,229,.04)); }}
.sla-side {{ border:1px solid var(--border); border-radius:12px; padding:.75rem .85rem; background: rgba(255,255,255,.025);
  font-size:.8rem; }}
.sla-side .row {{ display:flex; justify-content:space-between; align-items:center; gap:.5rem; padding:.28rem 0;
  color: var(--secondary); }}
.sla-side .row b {{ color: var(--ink); font-weight:600; text-align:right; overflow:hidden; text-overflow:ellipsis;
  white-space:nowrap; max-width: 60%; }}
.sla-side .ttl {{ font-size:.66rem; letter-spacing:.18em; color: var(--muted); font-weight:700; margin-bottom:.25rem; }}
.sla-brand {{ display:flex; align-items:center; gap:.65rem; margin:.1rem 0 .2rem; }}
.sla-brand .t {{ font-weight:750; color: var(--ink); font-size:.98rem; line-height:1.15; }}
.sla-brand .s {{ font-size:.7rem; color: var(--muted); letter-spacing:.06em; }}
div[data-testid="stForm"] {{ border:1px solid var(--border); border-radius: var(--radius); background: var(--surface); }}
div[data-testid="stDataFrame"] {{ border:1px solid var(--border); border-radius: 12px; overflow:hidden; }}
div[data-testid="stExpander"] details {{ border:1px solid var(--border) !important; border-radius:12px !important;
  background: var(--surface); }}
button[data-baseweb="tab"] {{ font-weight:600; }}
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {{
  background: linear-gradient(135deg, #3987e5, #2f6fd0); border:0; box-shadow: 0 8px 22px -10px rgba(57,135,229,.8);
  transition: transform .15s var(--ease), box-shadow .15s; }}
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover {{
  transform: translateY(-1px); box-shadow: 0 12px 26px -10px rgba(57,135,229,.95); }}
div[data-testid="stPlotlyChart"] {{ border-radius: 10px; }}

/* ---------- responsive ---------- */
@media (max-width: 900px) {{
  .sla-hero {{ flex-direction:column; align-items:flex-start; }}
  .sla-hero .right {{ align-items:flex-start; }}
  .sla-hero.big h1 {{ font-size: 1.8rem; }}
  .block-container {{ padding-left: 1rem; padding-right: 1rem; }}
}}
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{ animation: none !important; transition: none !important; }}
}}
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
