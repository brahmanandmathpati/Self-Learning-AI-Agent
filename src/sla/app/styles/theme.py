
"""Design system: tokens + global CSS — "deep violet" theme (see docs/design.md).

Palette (CSS variables in :root): lilac-mist background, void/plum headings, indigo actions, lavender and orchid
accents, one coral highlight (see docs/design.md). SERIES are the categorical chart colours (identity follows the
entity, never its rank). Status colours are always paired with an icon/label. Every animation is CSS-only and
switched off under ``prefers-reduced-motion``.
"""

from __future__ import annotations

import streamlit as st

from sla.app.styles.mission import MISSION_CSS, MISSION_FONTS

INK = {
    "page": "#0B0D14", "surface": "#121624", "surface_2": "#171C2E", "primary": "#E6E9F2",
    "secondary": "#B4BBD0", "muted": "#8A93AD", "grid": "rgba(138,147,173,0.16)", "axis": "rgba(138,147,173,0.32)",
    "border": "#232A40",
}
GOLD = "#C9A24B"  # kept only for the team-avatar ring and walked-path fill
VOID, MIST, PLUM, LAVENDER, CORAL, ORCHID = "#040207", "#F9F6FA", "#41234E", "#AF98E4", "#C96B4B", "#9965E8"
INDIGO = "#4632C9"
ACCENT = INDIGO
SERIES = ["#22D3EE", "#F59E0B", "#A3E635"]  # Mission Control: cyan / amber / lime
STATUS = {"good": "#A3E635", "warning": "#F59E0B", "serious": "#FB923C", "critical": "#F87171", "info": "#22D3EE"}
AGENT_COLORS = {"Q-learning": SERIES[0], "DQN": SERIES[1], "SARSA": SERIES[2], "Expected SARSA": "#A78BFA",
                "Random": "#8A93AD"}
VARIANT_COLORS = {"full": SERIES[0], "no_replay": SERIES[1], "no_target": SERIES[2]}
VARIANT_LABELS = {"full": "Full DQN", "no_replay": "No replay", "no_target": "No target network"}

CSS = f"""
<style>
@import
  url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
:root {{
  --page:{INK['page']}; --band:#F1EBF6; --surface:#FFFFFF; --surface2:{INK['surface_2']};
  --ink:{INK['primary']}; --secondary:{INK['secondary']}; --muted:{INK['muted']};
  --border:{INK['border']}; --hair:rgba(175,152,228,.45);
  --gold:#AF98E4; --gold-d:#4632C9; --gold-soft:#EDE7FA; --indigo:{INDIGO}; --indigo-soft:#EDE7FA;
  --void:{VOID}; --mist:{MIST}; --plum:{PLUM}; --lavender:{LAVENDER};
   --coral:{CORAL}; --orchid:{ORCHID}; --coral-text:#B4562F; --avatar-ring:#C9A24B; --accent:{INDIGO};
  --blue:{SERIES[0]}; --orange:{SERIES[1]}; --aqua:{SERIES[2]};
  --good:{STATUS['good']}; --warn:{STATUS['warning']}; --bad:{STATUS['critical']};
  --radius:20px; --ease:cubic-bezier(.2,.7,.2,1);
  --shadow: 0 1px 2px rgba(4,2,7,.05), 0 12px 32px -16px rgba(65,35,78,.28);
  --shadow-lg: 0 2px 4px rgba(4,2,7,.05), 0 22px 44px -18px rgba(65,35,78,.38);
  --serif: "Playfair Display", "Cormorant Garamond", Georgia, serif;
}}
html, body, [class*="css"], .stMarkdown, button, input, textarea, select {{ font-family: "Inter", system-ui,
  -apple-system, "Segoe UI", sans-serif; }}
code, pre, .mono {{ font-family: "JetBrains Mono", ui-monospace, monospace !important; }}

/* ---------- canvas ---------- */
.stApp {{ background: radial-gradient(1100px 520px at 90% -8%, #EAE0FA 0%, transparent 60%),
  radial-gradient(900px 480px at -5% 105%, #EFEEFB 0%, transparent 60%), var(--page); color: var(--ink); }}
header[data-testid="stHeader"] {{ background: rgba(249,246,250,.78); backdrop-filter: saturate(160%) blur(14px);
  -webkit-backdrop-filter: saturate(160%) blur(14px); border-bottom: 1px solid var(--hair); }}
.block-container {{ padding-top: 4.6rem; padding-bottom: 2rem; max-width: 1200px; }}
h1, h2, h3, h4 {{ color: var(--ink); letter-spacing: -0.01em; }}
p, li {{ color: var(--secondary); line-height: 1.65; }}
a {{ color: var(--indigo); }}
:focus-visible {{ outline: 2px solid var(--indigo) !important; outline-offset: 2px; border-radius: 6px; }}

/* ---------- entrance motion (staggered fade-up) ---------- */
@keyframes sla-up {{ from {{ opacity:0; transform: translateY(10px); }} to {{ opacity:1; transform:none; }} }}
.sla-anim, .sla-hero, .sla-card, .sla-panel, .sla-section, .sla-empty, .sla-insight, .sla-step, .sla-feature,
  .sla-member {{
  animation: sla-up .45s var(--ease) both; }}
.sla-grid > *:nth-child(2), .sla-steps > *:nth-child(2) {{ animation-delay:.06s; }}
.sla-grid > *:nth-child(3), .sla-steps > *:nth-child(3) {{ animation-delay:.12s; }}
.sla-grid > *:nth-child(4), .sla-steps > *:nth-child(4) {{ animation-delay:.18s; }}
.sla-grid > *:nth-child(5) {{ animation-delay:.24s; }} .sla-grid > *:nth-child(6) {{ animation-delay:.30s; }}

/* ---------- hero ---------- */
.sla-hero {{ position:relative; overflow:hidden; display:flex; align-items:center; justify-content:space-between;
  gap:1.5rem;
  padding: 2rem 2.2rem; border:1px solid var(--hair); border-radius: 24px; margin-bottom: 1.6rem;
  background: linear-gradient(135deg, var(--surface) 0%, #151B30 100%); box-shadow: var(--shadow); }}
.sla-hero .eyebrow {{ font-size:.72rem; letter-spacing:.24em; text-transform:uppercase; color: var(--gold-d);
  font-weight:600;
  margin-bottom:.6rem; display:flex; align-items:center; gap:.6rem; }}
.sla-hero .eyebrow::before {{ content:""; width:28px; height:1px; background: var(--gold); }}
.sla-hero h1 {{ font-family: var(--serif); font-size: 2.1rem; margin: 0; font-weight: 600; line-height:1.12;
  color: var(--ink); }}
.sla-hero.big {{ padding: 2.8rem 2.6rem; }}
.sla-hero.big h1 {{ font-size: 3.1rem; letter-spacing:-.02em; }}
.sla-hero p {{ margin: .7rem 0 0 0; color: var(--secondary); font-size: 1.05rem; max-width: 640px; }}
.sla-hero .right {{ display:flex; flex-wrap:wrap; gap:.5rem; z-index:1; }}
.sla-hero .art {{ width: 230px; height: 230px; flex: none; z-index:1; }}
.sla-actions {{ display:flex; flex-wrap:wrap; gap:.7rem; margin-top:1.3rem; }}
.sla-btn {{ position:relative; overflow:hidden; display:inline-flex; align-items:center; gap:.5rem;
  padding:.72rem 1.25rem;
  border-radius: 999px; font-weight:600; font-size:.92rem; text-decoration:none !important;
  transition: transform .2s var(--ease), box-shadow .2s; }}
.sla-btn.gold {{ background: linear-gradient(135deg, #AF98E4, var(--gold) 55%, #4632C9); color: #FFFFFF !important;
  box-shadow: 0 8px 20px -10px rgba(70,50,201,.8); }}
.sla-btn.outline {{ background: var(--surface); color: var(--ink) !important; border: 1px solid rgba(65,35,78,.16); }}
.sla-btn:hover {{ transform: translateY(-1px); box-shadow: var(--shadow-lg); }}
.sla-btn::after {{ content:""; position:absolute; inset:0;
  background: linear-gradient(110deg, transparent 30%, rgba(255,255,255,.55) 48%, transparent 66%);
  transform: translateX(-120%); transition: transform .7s var(--ease); }}
.sla-btn:hover::after {{ transform: translateX(120%); }}

/* ---------- cards ---------- */
.sla-grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap:1rem;
  margin:.2rem 0 .8rem; }}
.sla-card {{ position:relative; border:1px solid var(--border); border-radius: var(--radius); padding: 1.15rem 1.2rem;
  background: var(--surface); box-shadow: var(--shadow);
  transition: transform .25s var(--ease), box-shadow .25s, border-color .25s; height:100%; }}
.sla-card:hover {{ transform: translateY(-3px); box-shadow: var(--shadow-lg); border-color: var(--hair); }}
.sla-card .label {{ display:flex; align-items:center; gap:.5rem; color: var(--muted); font-size: .7rem;
  text-transform: uppercase;
  letter-spacing: .12em; font-weight:600; }}
.sla-card .label .ic {{ width:1.7rem; height:1.7rem; border-radius:9px; display:inline-flex; align-items:center;
  justify-content:center;
  background: var(--gold-soft); color: var(--gold-d); font-size:.85rem; font-weight:700; }}
.sla-card .value {{ font-family: var(--serif); font-size: 1.85rem; font-weight: 600; margin-top: .5rem;
  line-height: 1.15; color: var(--ink);
  font-variant-numeric: lining-nums tabular-nums; }}
.sla-card .value.sm {{ font-size:1.25rem; }}
.sla-card .sub {{ color: var(--muted); font-size: .8rem; margin-top: .35rem; line-height:1.45; }}
.sla-card .value.notrun {{ font-family: "Inter", sans-serif; color: var(--muted); font-size: .95rem;
  font-weight: 650; letter-spacing: .1em; }}
.sla-card.accent::before {{ content:""; position:absolute; left:0; top:16px; bottom:16px; width:3px;
  border-radius:3px; background: var(--card-accent, var(--gold)); }}
.sla-card .delta {{ display:inline-block; margin-top:.4rem; font-size:.74rem; font-weight:600; padding:.1rem .5rem;
  border-radius:6px;
  background: #E8F5EC; color: var(--good); }}
.sla-card .delta.neg {{ background: #FCEBEB; color: var(--bad); }}
@property --sla-n {{ syntax:'<integer>'; inherits:false; initial-value:0; }}
.sla-count {{ counter-reset: n var(--sla-n); animation: sla-count 1.2s var(--ease) both; }}
.sla-count::after {{ content: counter(n); }}
@keyframes sla-count {{ from {{ --sla-n: 0; }} }}

/* ---------- panels / chart containers ---------- */
.sla-panel {{ border:1px solid var(--border); border-radius: var(--radius); background: var(--surface);
  padding:1.2rem 1.3rem; box-shadow: var(--shadow); }}
div[class*="st-key-card"] {{ border:1px solid var(--border); border-radius: var(--radius);
  padding: 1rem 1.1rem .5rem; background: var(--surface);
  box-shadow: var(--shadow); animation: sla-up .45s var(--ease) both; }}
.stMarkdown p.sla-chart-title {{ font-size:.95rem !important; font-weight:650; color:var(--ink); margin:0 !important;
  line-height:1.3; }}
.stMarkdown p.sla-chart-sub {{ font-size:.76rem !important; color:var(--muted); margin:.1rem 0 .1rem !important;
  line-height:1.35; }}

/* ---------- badges ---------- */
.sla-badge {{ display:inline-flex; align-items:center; gap:.45rem; padding: .3rem .75rem; border-radius: 999px;
  font-size: .72rem; font-weight: 650;
  letter-spacing:.08em; text-transform:uppercase; border:1px solid rgba(65,35,78,.10); background: var(--surface);
  color: var(--ink); white-space:nowrap; }}
.sla-dot {{ width:.5rem; height:.5rem; border-radius:50%; display:inline-block; background: var(--c, var(--muted)); }}
.sla-dot.pulse {{ animation: sla-pulse 1.8s ease-out infinite; }}
@keyframes sla-pulse {{ 0% {{ box-shadow: 0 0 0 0 color-mix(in srgb, var(--c) 55%, transparent);
  }} 70% {{ box-shadow: 0 0 0 .5rem transparent; }}
  100% {{ box-shadow: 0 0 0 0 transparent; }} }}

/* ---------- section header ---------- */
.sla-section {{ display:flex; align-items:flex-end; justify-content:space-between; gap:1rem; margin: 2.4rem 0 1rem;
  padding-top: 1.2rem; border-top: 1px solid var(--hair); }}
.sla-section h3 {{ margin: 0; font-family: var(--serif); font-size: 1.55rem; font-weight: 600; }}
.sla-section p {{ margin: .3rem 0 0 0; color: var(--muted); font-size: .9rem; }}
.sla-kicker {{ font-size:.68rem; letter-spacing:.24em; text-transform:uppercase; color: var(--gold-d);
  font-weight:600; margin-bottom:.35rem; }}

/* ---------- how it works ---------- */
.sla-steps {{ display:grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; position:relative; }}
.sla-steps::before {{ content:""; position:absolute; top: 26px; left: 12%; right: 12%; height:1px;
  background: linear-gradient(90deg, transparent, var(--gold), var(--gold), transparent); }}
.sla-step {{ position:relative; text-align:center; padding: 0 .6rem; }}
.sla-step .n {{ position:relative; z-index:1; width:52px; height:52px; margin:0 auto .8rem; border-radius:50%;
  display:flex; align-items:center;
  justify-content:center; font-family: var(--serif); font-size:1.25rem; font-weight:600; color: var(--gold-d);
  background: var(--surface);
  border:1px solid var(--hair); box-shadow: var(--shadow); }}
.sla-step h4 {{ margin:0 0 .3rem; font-size:1rem; font-weight:650; }}
.sla-step p {{ margin:0; font-size:.86rem; }}

/* ---------- features ---------- */
.sla-feature {{ border:1px solid var(--border); border-radius: var(--radius); background: var(--surface);
  padding:1.3rem 1.35rem; box-shadow: var(--shadow);
  transition: transform .25s var(--ease), box-shadow .25s, border-color .25s; height:100%; }}
.sla-feature:hover {{ transform: translateY(-4px); box-shadow: var(--shadow-lg); border-color: var(--hair); }}
.sla-feature .fi {{ width:2.4rem; height:2.4rem; border-radius:12px; display:flex; align-items:center;
  justify-content:center;
  background: var(--indigo-soft); color: var(--indigo); margin-bottom:.8rem; }}
.sla-feature h4 {{ margin:0 0 .35rem; font-size:1.02rem; font-weight:650; }}
.sla-feature p {{ margin:0; font-size:.87rem; }}

/* ---------- chips / tech stack ---------- */
.sla-stack {{ display:flex; flex-wrap:wrap; gap:.55rem; }}
.sla-stack span {{ padding:.4rem .85rem; border-radius:999px; background: var(--surface); border:1px solid var(--hair);
  font-size:.84rem; font-weight:500; color: var(--ink); }}

/* ---------- team ---------- */
.sla-team {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(210px,1fr)); gap:1rem; }}
.sla-member {{ border:1px solid var(--border); border-radius: var(--radius); background: var(--surface);
  padding:1.5rem 1.2rem;
  text-align:center; box-shadow: var(--shadow);
  transition: transform .25s var(--ease), box-shadow .25s; }}
.sla-member:hover {{ transform: translateY(-3px); box-shadow: var(--shadow-lg); }}
.sla-member .av {{ width:76px; height:76px; margin:0 auto .9rem; border-radius:50%; display:flex; align-items:center;
  justify-content:center;
  font-family: var(--serif); font-size:1.6rem; font-weight:600; color: var(--gold-d);
  background: linear-gradient(135deg, #F6F2FC, var(--gold-soft));
  border:1px solid var(--hair); }}
.sla-member h4 {{ margin:0; font-size:1.05rem; font-weight:650; }}
.sla-member .role {{ font-size:.84rem; color: var(--secondary); margin:.35rem 0 .7rem; line-height:1.5; }}
.sla-member .links {{ font-size:.8rem; color: var(--muted); }}
.sla-member .links a {{ color: var(--indigo, #4F46E5); font-weight:600; text-decoration:none; }}
.sla-member .links .todo {{ font-style: italic; }}
.sla-member .av {{ width:84px; height:84px; border:2px solid var(--avatar-ring);
  box-shadow: 0 0 0 4px var(--surface), 0 6px 18px -8px rgba(65,35,78,.35); }}
.sla-college {{ text-align:center; font-size:.84rem !important; color: var(--muted); margin:1.4rem auto 0;
  max-width:820px; line-height:1.7; padding-top:1rem; border-top:1px solid var(--hair); }}
.sla-college b {{ font-family: var(--serif); color: var(--ink); font-size:1rem; font-weight:600; }}

/* ---------- footer ---------- */
.sla-footer {{ margin-top: 3rem; padding: 1.6rem 0 .4rem; border-top: 1px solid var(--hair); display:flex;
  flex-wrap:wrap; justify-content:space-between;
  gap:1rem; font-size:.85rem; color: var(--muted); }}
.sla-footer a {{ color: var(--secondary); text-decoration:none; margin-right:1.1rem; }}
.sla-footer a:hover {{ color: var(--gold-d); }}
.sla-footer .brand {{ font-family: var(--serif); font-size:1.05rem; color: var(--ink); }}

/* ---------- verdict ---------- */
.sla-verdict {{ display:flex; gap:1rem; align-items:center; border-radius: var(--radius); padding: 1.1rem 1.3rem;
  background: var(--surface); box-shadow: var(--shadow);
  border:1px solid color-mix(in srgb, var(--c) 35%, transparent); animation: sla-up .45s var(--ease) both;
  margin: .3rem 0 1rem; }}
.sla-verdict .icon {{ width:2.7rem; height:2.7rem; flex:none; border-radius:12px; display:flex; align-items:center;
  justify-content:center; font-size:1.25rem;
  font-weight:800; color: var(--c); background: color-mix(in srgb, var(--c) 12%, white); }}
.sla-verdict .t {{ font-size:.92rem; font-weight:700; letter-spacing:.14em; color: var(--c); }}
.sla-verdict .d {{ font-size:.88rem; color: var(--secondary); margin-top:.15rem; }}

/* ---------- comparison ---------- */
.sla-rank {{ display:inline-flex; align-items:center; justify-content:center; min-width:1.9rem; height:1.9rem;
  padding:0 .4rem; border-radius:9px;
  font-weight:700; font-size:.85rem; background: var(--surface2); color: var(--secondary); }}
.sla-rank.first {{ background: linear-gradient(135deg, #AF98E4, var(--gold)); color:#FFFFFF; }}
.sla-cmp-head {{ display:flex; align-items:center; justify-content:space-between; gap:.6rem; }}
.sla-cmp-name {{ display:flex; align-items:center; gap:.55rem; font-weight:650; color: var(--ink); font-size:1rem; }}
.sla-swatch {{ width:.7rem; height:.7rem; border-radius:3px; background: var(--c); display:inline-block; }}
.sla-bar {{ height:.45rem; border-radius:99px; background: var(--surface2); overflow:hidden; margin-top:.7rem; }}
.sla-bar > span {{ display:block; height:100%; border-radius:99px; background: var(--c); transform-origin:left;
  animation: sla-grow .9s var(--ease) both; }}
@keyframes sla-grow {{ from {{ transform: scaleX(0); }} }}
.sla-why {{ font-size:.82rem; color: var(--muted); margin-top:.6rem; line-height:1.5; }}

/* ---------- progress / skeleton ---------- */
.sla-progress {{ border:1px solid var(--border); border-radius: var(--radius); background: var(--surface);
  padding:.9rem 1.1rem;
  margin-bottom:.9rem; box-shadow: var(--shadow); }}
.sla-progress .row {{ display:flex; justify-content:space-between; align-items:center; gap:1rem; font-size:.84rem;
  color: var(--secondary); flex-wrap:wrap; }}
.sla-progress .track {{ height:.5rem; border-radius:99px; background: var(--surface2); overflow:hidden;
  margin-top:.7rem; }}
.sla-progress .fill {{ height:100%; border-radius:99px; transition: width .4s var(--ease);
  background: linear-gradient(90deg, var(--gold), #AF98E4); }}
.sla-progress .fill.live {{ background-image: linear-gradient(90deg, var(--gold), #AF98E4),
  repeating-linear-gradient(45deg, rgba(255,255,255,.45) 0 8px, transparent 8px 16px);
  background-blend-mode: overlay; animation: sla-stripes 1s linear infinite; }}
@keyframes sla-stripes {{ to {{ background-position: 0 0, 32px 0; }} }}
.sla-skel {{ border-radius: var(--radius); height: var(--h, 90px); border:1px solid var(--border);
  background: linear-gradient(90deg, var(--surface) 25%, var(--surface2) 37%, var(--surface) 63%);
  background-size: 400% 100%;
  animation: sla-shimmer 1.4s ease infinite; }}
@keyframes sla-shimmer {{ 0% {{ background-position: 100% 50%; }} 100% {{ background-position: 0 50%; }} }}

/* ---------- empty / error ---------- */
.sla-empty {{ border:1px dashed rgba(70,50,201,.45); border-radius: var(--radius); padding: 1.8rem 1.4rem;
  text-align:center; background: rgba(255,255,255,.7); }}
.sla-empty .glyph {{ width:3rem; height:3rem; margin:0 auto .8rem; border-radius:14px; display:flex;
  align-items:center; justify-content:center;
  color: var(--gold-d); background: var(--gold-soft); }}
.sla-empty .tag {{ font-size:.68rem; font-weight:700; letter-spacing:.2em; color: var(--muted); }}
.sla-empty .what {{ color: var(--ink); font-weight:650; margin-top:.35rem; font-size:1rem; }}
.sla-empty .next {{ color: var(--secondary); font-size:.88rem; margin-top:.3rem; }}
.sla-empty code {{ display:inline-block; margin-top:.8rem; font-size:.78rem; padding:.35rem .65rem;
  border-radius:8px; background: var(--surface2);
  border:1px solid var(--border); color: var(--ink); }}
.sla-error {{ border:1px solid rgba(185,28,28,.3); border-radius: var(--radius); padding:1.1rem 1.2rem;
  background:#FEF6F6; }}
.sla-error .t {{ color: var(--bad); font-weight:700; }}
.sla-error .r {{ color: var(--secondary); font-size:.88rem; margin-top:.35rem; }}

/* ---------- insight (reflection) ---------- */
.sla-insight {{ border-radius: 20px; padding: 1.4rem 1.5rem 1.2rem; border:1px solid var(--hair);
  background: linear-gradient(135deg, var(--surface), #151B30); box-shadow: var(--shadow); }}
.sla-insight .h {{ display:flex; align-items:center; justify-content:space-between; gap:.6rem; flex-wrap:wrap; }}
.sla-insight .k {{ font-size:.72rem; font-weight:700; letter-spacing:.22em; color: var(--gold-d); display:flex;
  gap:.5rem; align-items:center; }}
.sla-insight .body {{ color: var(--ink); font-size:1rem; line-height:1.75; margin-top:.8rem; }}
.sla-insight .meta {{ color: var(--muted); font-size:.78rem; margin-top:.8rem; }}
.sla-chips {{ display:flex; flex-wrap:wrap; gap:.5rem; margin-top:.5rem; }}
.sla-chip {{ display:inline-flex; flex-direction:column; gap:.05rem; padding:.5rem .75rem; border-radius:12px;
  border:1px solid var(--border); background: var(--surface); min-width:7.5rem; box-shadow: var(--shadow); }}
.sla-chip .ck {{ font-size:.64rem; letter-spacing:.1em; text-transform:uppercase; color: var(--muted);
  font-weight:600; }}
.sla-chip .cv {{ font-size:.95rem; color: var(--ink); font-weight:650; font-variant-numeric: tabular-nums; }}

/* ---------- key/value ---------- */
.sla-kv {{ display:grid; grid-template-columns: repeat(auto-fill, minmax(190px, 1fr)); gap:.55rem; }}
.sla-kv div {{ border:1px solid var(--border); border-radius:12px; padding:.55rem .75rem; background: var(--surface); }}
.sla-kv .k {{ font-size:.66rem; letter-spacing:.1em; text-transform:uppercase; color: var(--muted); font-weight:600; }}
.sla-kv .v {{ font-size:.86rem; color: var(--ink); font-family:"JetBrains Mono", monospace; word-break: break-all; }}
.sla-env-row {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:.8rem; }}
.sla-env-row .sla-card .value {{ font-family:"Inter",sans-serif; font-size:1rem; font-weight:600; line-height:1.45; }}

/* ---------- sidebar & widgets ---------- */
section[data-testid="stSidebar"] {{ background: #FBF8FD; border-right: 1px solid var(--hair); }}
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] {{ border-radius:10px; transition: background .15s; }}
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] {{
  background: var(--gold-soft); }}
.sla-side {{ border:1px solid var(--border); border-radius:14px; padding:.8rem .9rem; background: var(--surface);
  font-size:.8rem; box-shadow: var(--shadow); }}
.sla-side .row {{ display:flex; justify-content:space-between; align-items:center; gap:.5rem; padding:.28rem 0;
  color: var(--secondary); }}
.sla-side .row b {{ color: var(--ink); font-weight:600; text-align:right; overflow:hidden; text-overflow:ellipsis;
  white-space:nowrap; max-width: 60%; }}
.sla-side .ttl {{ font-size:.64rem; letter-spacing:.2em; color: var(--gold-d); font-weight:700; margin-bottom:.25rem; }}
div[data-testid="stForm"] {{ border:1px solid var(--border); border-radius: var(--radius); background: var(--surface);
  box-shadow: var(--shadow); }}
div[data-testid="stDataFrame"] {{ border:1px solid var(--border); border-radius: 14px; overflow:hidden; }}
div[data-testid="stExpander"] details {{ border:1px solid var(--border) !important; border-radius:14px !important;
  background: var(--surface); }}
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primaryFormSubmit"],
  .stFormSubmitButton > button[kind="primary"] {{ background: linear-gradient(135deg, #AF98E4, var(--gold) 55%,
  #4632C9);
  color:#FFFFFF; border:0; border-radius:999px; font-weight:600; box-shadow: 0 8px 20px -10px rgba(70,50,201,.8);
  transition: transform .15s var(--ease), box-shadow .15s; }}
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primaryFormSubmit"]:hover,
  .stFormSubmitButton > button[kind="primary"]:hover {{ transform: translateY(-1px); color:#FFFFFF;
  box-shadow: var(--shadow-lg); }}
.stButton > button[kind="primary"] p, .stFormSubmitButton > button[kind^="primary"] p {{ color:#FFFFFF;
  font-weight:600; }}

/* ---------- motion graphics (decorative) ---------- */
.sla-loop {{ width:100%; height:100%; overflow:visible; }}
.sla-ring {{ fill:none; stroke: var(--gold); stroke-width:.7; stroke-dasharray:2 3; opacity:.7;
  transform-origin:50px 50px; animation: sla-rot 40s linear infinite; }}
.sla-ring2 {{ fill:none; stroke: var(--indigo); stroke-width:1; opacity:.45; stroke-dasharray:40 130;
  transform-origin:50px 50px; animation: sla-rot 6s linear infinite reverse; }}
@keyframes sla-rot {{ to {{ transform: rotate(360deg); }} }}
.sla-signal {{ filter: drop-shadow(0 0 3px rgba(175,152,228,.9)); }}
.sla-node circle {{ animation: sla-blink 2.2s ease-in-out infinite; animation-delay: inherit; }}
@keyframes sla-blink {{ 0%,100% {{ stroke-width:1.4; }} 50% {{ stroke-width:2.6; }} }}
.sla-net {{ width:100%; height:auto; max-height:230px; }}
.sla-edge {{ stroke: rgba(70,50,201,.30); stroke-width:.8; stroke-dasharray: 3 9;
  animation: sla-flow 3s linear infinite; }}
@keyframes sla-flow {{ to {{ stroke-dashoffset: -24; }} }}
.sla-neuron {{ animation: sla-fire 2.4s ease-in-out infinite; }}
@keyframes sla-fire {{ 0%,100% {{ fill:#0B0D14; }} 45% {{ fill:#1B2A3A; }} }}
.sla-flow {{ display:grid; grid-template-columns: 1.1fr 1fr; gap:1.2rem; align-items:center; }}

/* ---------- responsive ---------- */
@media (max-width: 900px) {{
  .sla-hero {{ flex-direction:column; align-items:flex-start; padding:1.6rem 1.3rem; }}
  .sla-hero.big {{ padding:1.8rem 1.4rem; }} .sla-hero.big h1 {{ font-size: 2.2rem; }}
  .sla-hero .art {{ width:180px; height:180px; align-self:center; }}
  .sla-steps {{ grid-template-columns: 1fr 1fr; row-gap:1.5rem; }} .sla-steps::before {{ display:none; }}
  .sla-flow {{ grid-template-columns: 1fr; }}
  .block-container {{ padding-left: 1rem; padding-right: 1rem; }}
}}
@media (max-width: 480px) {{ .sla-steps {{ grid-template-columns: 1fr; }} .sla-hero.big h1 {{ font-size: 1.85rem; }} }}
/* ---------- sign-in screen, guest lock, user card ---------- */
.sla-auth-brand .eyebrow {{ font-size:.72rem; letter-spacing:.24em; text-transform:uppercase; color: var(--gold-d);
  font-weight:600; display:flex; align-items:center; gap:.6rem; }}
.sla-auth-brand .eyebrow::before {{ content:""; width:28px; height:1px; background: var(--gold); }}
.sla-auth-brand h1 {{ font-family: var(--serif); font-size: 2.7rem; line-height:1.1; font-weight:600; margin:.6rem 0 0;
  animation: sla-up .7s var(--ease) both; }}
.sla-auth-brand h1 .gold {{ color: var(--gold-d); }}
.sla-auth-brand p {{ font-size:1.02rem; max-width: 470px; animation: sla-up .7s var(--ease) .15s both; }}
.sla-auth-art {{ width: 210px; height: 210px; margin: .4rem 0 .6rem; }}
.sla-auth-list {{ list-style:none; padding:0; margin:0; display:grid; gap:.55rem; }}
.sla-auth-list li {{ display:flex; gap:.6rem; align-items:flex-start; color: var(--secondary); font-size:.9rem; }}
.sla-auth-list li svg {{ flex:none; margin-top:.2rem; color: var(--gold-d); }}
div[class*="st-key-card_auth"] {{ padding: 1.6rem 1.6rem 1rem; border:1px solid var(--hair);
  box-shadow: var(--shadow-lg);
  border-top: 3px solid var(--gold); }}
.sla-auth-head h3 {{ font-family: var(--serif); font-size:1.6rem; font-weight:600; margin:0; }}
.sla-auth-head p {{ margin:.2rem 0 .4rem; color: var(--muted); font-size:.9rem; }}
.sla-or {{ display:flex; align-items:center; gap:.8rem; color: var(--muted); font-size:.75rem; letter-spacing:.2em;
  text-transform:uppercase; margin:.5rem 0 .6rem; }}
.sla-or::before, .sla-or::after {{ content:""; flex:1; height:1px; background: var(--hair); }}
.sla-lock {{ display:flex; gap:.6rem; align-items:center; padding:.7rem 1rem; border-radius:14px;
  border:1px dashed rgba(70,50,201,.55); background: #F8F5FD; color: var(--secondary); font-size:.9rem; }}
.sla-lock svg {{ color: var(--gold-d); flex:none; }}
.sla-me {{ display:flex; gap:.7rem; align-items:center; margin-bottom:.5rem; }}
.sla-me .av {{ width:2.4rem; height:2.4rem; flex:none; border-radius:50%; display:flex; align-items:center;
  justify-content:center; font-family: var(--serif); font-weight:600; color: var(--gold-d);
  background: linear-gradient(135deg,#F6F2FC,var(--gold-soft)); border:1px solid var(--hair); }}
.sla-me b {{ display:block; color: var(--ink); font-size:.9rem; line-height:1.2; }}
.sla-me small {{ display:block; color: var(--muted); font-size:.72rem; overflow:hidden; text-overflow:ellipsis;
  white-space:nowrap; max-width: 11rem; }}
.sla-me .kind {{ display:inline-block; margin:.15rem 0; font-size:.62rem; font-weight:700; letter-spacing:.12em;
  text-transform:uppercase; padding:.1rem .45rem; border-radius:99px; background: var(--gold-soft);
  color: var(--gold-d); }}
.sla-me .kind.guest {{ background: var(--indigo-soft); color: var(--indigo); }}
@media (max-width: 900px) {{ .sla-auth-brand h1 {{ font-size: 2rem; }} .sla-auth-art {{ display:none; }} }}

/* ================= v3: top navbar, auth corner, landing sections ================= */
header[data-testid="stHeader"] {{ height: 3.75rem; }}
header[data-testid="stHeader"] a, header[data-testid="stHeader"] button {{ font-weight: 500; }}
/* top-right corner: Log in / Sign up or the avatar menu */
div.st-key-topauth {{ position: fixed; top: .62rem; right: 3.6rem; z-index: 1000002; width: auto !important;
  gap: .5rem; }}
div.st-key-topauth .stButton > button[kind="tertiary"] {{ color: var(--ink); font-weight: 600; padding: .4rem .8rem; }}
div.st-key-topauth .stButton > button[kind="tertiary"]:hover {{ color: var(--gold-d); }}
div.st-key-topauth .stButton > button[kind="primary"] {{ padding: .42rem 1.1rem; min-height: 2.3rem; }}
div.st-key-topauth [data-testid="stPopover"] > div > button, div.st-key-topauth [data-testid="stPopoverButton"] {{
  width: 2.5rem; height: 2.5rem; min-height: 2.5rem; padding: 0; border-radius: 50%; border: 1px solid var(--hair);
  background: linear-gradient(135deg, #F6F2FC, var(--gold-soft)); color: var(--gold-d); font-family: var(--serif);
  font-weight: 600; box-shadow: var(--shadow); }}
div.st-key-topauth [data-testid="stPopoverButton"] svg, div.st-key-topauth [data-testid="stPopover"] button svg {{
  display: none; }}
div[data-testid="stPopoverBody"] {{ border-radius: 16px; border: 1px solid var(--hair); min-width: 260px; }}
/* log-in dialog */
div[data-testid="stDialog"] div[role="dialog"] {{ border-radius: 22px; border-top: 3px solid var(--gold);
  box-shadow: 0 30px 80px -30px rgba(65,35,78,.45); animation: sla-pop .28s var(--ease) both; }}
@keyframes sla-pop {{ from {{ opacity: 0; transform: translateY(10px) scale(.98); }} to {{ opacity: 1;
  transform: none; }} }}
div[data-testid="stDialog"] h2, div[data-testid="stDialog"] [data-testid="stHeading"] {{ font-family: var(--serif); }}
/* hero (native container so page links keep the session) */
div.st-key-hero {{ position: relative; overflow: hidden; padding: 2.6rem 2.6rem 2.3rem; border: 1px solid var(--hair);
  border-radius: 24px; margin-bottom: 1.2rem; box-shadow: var(--shadow);
  background: linear-gradient(135deg, var(--surface) 0%, #151B30 100%); }}
div.st-key-hero::before, div.st-key-hero::after {{ content: ""; position: absolute; border-radius: 50%;
  filter: blur(48px);
  pointer-events: none; }}
div.st-key-hero::before {{ width: 360px; height: 360px; right: -80px; top: -120px; background: rgba(175,152,228,.28);
  animation: sla-blob 14s ease-in-out infinite alternate; }}
div.st-key-hero::after {{ width: 300px; height: 300px; left: 30%; bottom: -170px; background: rgba(70,50,201,.14);
  animation: sla-blob 18s ease-in-out infinite alternate-reverse; }}
div.st-key-hero > div {{ position: relative; z-index: 1; }}
.sla-hero-copy .eyebrow {{ font-size: .72rem; letter-spacing: .24em; text-transform: uppercase; color: var(--gold-d);
  font-weight: 600; display: flex; align-items: center; gap: .6rem; }}
.sla-hero-copy .eyebrow::before {{ content: ""; width: 28px; height: 1px; background: var(--gold); }}
.sla-hero-copy h1 {{ font-family: var(--serif); font-size: 3.2rem; line-height: 1.08; letter-spacing: -.02em;
  font-weight: 600; margin: .7rem 0 0; color: var(--ink); padding: 0; }}
.sla-hero-copy .w {{ display: inline-block; opacity: 0; transform: translateY(.45em); filter: blur(6px);
  animation: sla-word .8s var(--ease) forwards; }}
.sla-hero-copy .w.gold {{ background: linear-gradient(100deg, var(--gold-d) 0%, #AF98E4 40%, var(--gold-d) 60%,
  #4632C9 100%); background-size: 220% 100%; -webkit-background-clip: text; background-clip: text; color: transparent;
  animation: sla-word .8s var(--ease) forwards, sla-sheen 5s ease-in-out 1.6s infinite; }}
.sla-hero-copy p {{ font-size: 1.08rem; max-width: 600px; margin: .8rem 0 .9rem;
  animation: sla-up .7s var(--ease) .55s both; }}
.sla-hero-copy .chips {{ display: flex; flex-wrap: wrap; gap: .5rem; animation: sla-up .7s var(--ease) .7s both; }}
.sla-hero-art {{ width: 100%; max-width: 250px; aspect-ratio: 1; margin: 0 auto; }}
div.st-key-hero_cta {{ gap: .7rem; margin-top: .6rem; animation: sla-up .7s var(--ease) .85s both; }}
/* pill links (st.page_link) */
div[class*="st-key-cta_"] {{ width: auto !important; flex: 0 0 auto !important; }}
div.st-key-hero_cta, div.st-key-proof_cta, div.st-key-cta_actions {{ justify-content: flex-start !important;
  flex-wrap: wrap !important; }}
div.st-key-topauth [data-testid="stPopover"] [data-testid="stIconMaterial"],
div.st-key-topauth [data-testid="stPopover"] button > div > div:last-child:not(:first-child) {{ display: none; }}
div.st-key-topauth [data-testid="stPopover"] button {{ justify-content: center; min-width: 2.5rem; }}
div[class*="st-key-cta_"] [data-testid="stPageLink"] a, div[class*="st-key-cta_"] a.sla-btn {{ position: relative;
  overflow: hidden; display: inline-flex; padding: .55rem 1.25rem; border-radius: 999px; text-decoration: none;
  transition: transform .2s var(--ease), box-shadow .2s; }}
div[class*="st-key-cta_gold"] [data-testid="stPageLink"] a {{
  background: linear-gradient(135deg, #AF98E4, var(--gold) 55%, #4632C9);
  box-shadow: 0 8px 20px -10px rgba(70,50,201,.8);
  animation: sla-glow 3.2s ease-in-out 1.5s infinite; }}
div[class*="st-key-cta_gold"] [data-testid="stPageLink"] a span,
  div[class*="st-key-cta_gold"] [data-testid="stPageLink"] a p {{
  color: #FFFFFF !important; font-weight: 600; }}
div[class*="st-key-cta_outline"] [data-testid="stPageLink"] a {{ background: var(--surface);
  border: 1px solid rgba(65,35,78,.16); }}
div[class*="st-key-cta_outline"] [data-testid="stPageLink"] a span,
  div[class*="st-key-cta_outline"] [data-testid="stPageLink"] a p {{
  color: var(--ink) !important; font-weight: 600; }}
div[class*="st-key-cta_"] [data-testid="stPageLink"] a:hover {{ transform: translateY(-1px);
  box-shadow: var(--shadow-lg); }}
div[class*="st-key-cta_"] [data-testid="stPageLink"] a::after {{ content: ""; position: absolute; inset: 0;
  background: linear-gradient(110deg, transparent 30%, rgba(255,255,255,.55) 48%, transparent 66%);
  transform: translateX(-120%); transition: transform .7s var(--ease); }}
div[class*="st-key-cta_"] [data-testid="stPageLink"] a:hover::after {{ transform: translateX(120%); }}
div.st-key-proof_cta, div.st-key-cta_actions {{ gap: .7rem; }}
/* status line, proof table, architecture */
.sla-status {{ font-size: .86rem; color: var(--muted); margin: .2rem 0 0; }}
.sla-status b {{ color: var(--ink); }}
.sla-proof {{ border: 1px solid var(--border); border-radius: var(--radius); background: var(--surface);
  box-shadow: var(--shadow);
  overflow-x: auto; margin-bottom: .7rem; }}
.sla-proof table {{ width: 100%; border-collapse: collapse; font-size: .92rem; }}
.sla-proof th {{ text-align: left; font-size: .68rem; letter-spacing: .14em; text-transform: uppercase;
  color: var(--gold-d);
  padding: .85rem 1rem; border-bottom: 1px solid var(--hair); white-space: nowrap; }}
.sla-proof td {{ padding: .8rem 1rem; border-bottom: 1px solid var(--border); color: var(--ink);
  font-variant-numeric: tabular-nums; white-space: nowrap; }}
.sla-proof tr:last-child td {{ border-bottom: 0; }}
.sla-proof td small {{ color: var(--muted); }}
.sla-arch {{ display: grid; gap: .5rem; }}
.sla-arch .lay {{ position: relative; display: flex; justify-content: space-between; gap: 1rem; align-items: center;
  padding: .7rem 1rem; border-radius: 14px; background: var(--surface); border: 1px solid var(--border);
  box-shadow: var(--shadow);
  animation: sla-up .5s var(--ease) both; }}
.sla-arch .lay:nth-child(4) {{ border-color: var(--hair); background: #F8F5FD; }}
.sla-arch .lay b {{ font-size: .92rem; color: var(--ink); }}
.sla-arch .lay span {{ font-size: .8rem; color: var(--muted); text-align: right; }}
.sla-arch .lay:not(:last-child)::after {{ content: ""; position: absolute; left: 50%; bottom: -.5rem; width: 1px;
  height: .5rem; background: var(--gold); }}
.sla-flowbox p {{ font-size: .9rem; margin: .6rem 0 0; }}
/* FAQ */
div[data-testid="stExpander"] details summary p {{ font-weight: 600; color: var(--ink); }}
div[data-testid="stExpander"] details:hover {{ border-color: var(--hair) !important; }}
/* final call-to-action band */
div.st-key-ctaband {{ margin-top: 2.6rem; padding: 2.4rem 2.6rem; border-radius: 24px; position: relative;
  overflow: hidden;
  background: radial-gradient(600px 300px at 90% 0%, rgba(175,152,228,.35), transparent 70%), linear-gradient(135deg,
  #0F172A, #1E293B);
  border: 1px solid rgba(175,152,228,.4); box-shadow: var(--shadow-lg); }}
.sla-cta-copy .eyebrow {{ font-size: .7rem; letter-spacing: .24em; text-transform: uppercase; color: #AF98E4;
  font-weight: 600; }}
.sla-cta-copy h2 {{ font-family: var(--serif); color: #FFFFFF; font-size: 2rem; font-weight: 600; margin: .4rem 0 .3rem;
  padding: 0; }}
.sla-cta-copy p {{ color: #CBD5E1; margin: 0 0 .9rem; }}
div.st-key-ctaband div[class*="st-key-cta_outline"] [data-testid="stPageLink"] a {{ background: transparent;
  border-color: rgba(255,255,255,.35); }}
div.st-key-ctaband div[class*="st-key-cta_outline"] [data-testid="stPageLink"] a span,
div.st-key-ctaband div[class*="st-key-cta_outline"] [data-testid="stPageLink"] a p {{ color: #FFFFFF !important; }}
/* phones and small tablets: the corner moves into the page flow */
@media (max-width: 768px) {{
  div.st-key-topauth {{ position: static; margin: -.4rem 0 .6rem; justify-content: flex-end; }}
  div.st-key-hero {{ padding: 1.6rem 1.3rem; }}
  .sla-hero-copy h1 {{ font-size: 2.1rem; }}
  .sla-hero-art {{ max-width: 190px; }}
  div.st-key-ctaband {{ padding: 1.8rem 1.4rem; }}
  .sla-cta-copy h2 {{ font-size: 1.5rem; }}
  .sla-arch .lay {{ flex-direction: column; align-items: flex-start; gap: .1rem; }}
  .sla-arch .lay span {{ text-align: left; }}
}}

/* ---------- next steps: team photos, share card, cookie helper ---------- */
.sla-member .av {{ overflow: hidden; }}
.sla-member .av img {{ width: 100%; height: 100%; object-fit: cover; border-radius: 50%; display: block; }}
.sla-share {{ display: flex; flex-direction: column; gap: .2rem; margin-bottom: .4rem; }}
.sla-share b {{ font-family: var(--serif); font-size: 1.15rem; font-weight: 600; color: var(--ink); }}
.sla-share span {{ color: var(--muted); font-size: .86rem; }}
div.st-key-cookiejar {{ position: absolute; width: 0; height: 0; overflow: hidden; }}

/* ---------- Vision Lab: live prediction panel and the FrozenLake board ---------- */
.sla-pred {{ border: 1px solid var(--border); border-radius: var(--radius); background: var(--surface);
  padding: 1rem 1.1rem;
  box-shadow: var(--shadow); }}
.sla-pred.empty {{ color: var(--muted); font-size: .9rem; }}
.sla-pred .top {{ font-family: var(--serif); font-size: 1.6rem; font-weight: 600; color: var(--ink);
  margin-bottom: .5rem; }}
.sla-pred .row {{ display: grid; grid-template-columns: 8.5rem 1fr 2.6rem; gap: .5rem; align-items: center;
  font-size: .82rem;
  color: var(--secondary); margin-top: .3rem; }}
.sla-pred .bar {{ height: .45rem; border-radius: 99px; background: var(--surface2); overflow: hidden; }}
.sla-pred .bar i {{ display: block; height: 100%; border-radius: 99px;
  background: linear-gradient(90deg, var(--gold), #AF98E4);
  transition: width .3s var(--ease); }}
.sla-pred .row b {{ color: var(--ink); text-align: right; font-variant-numeric: tabular-nums; }}
.sla-lake {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: .4rem; max-width: 360px; margin: .6rem 0; }}
.sla-lake .cell {{ position: relative; aspect-ratio: 1; border-radius: 12px; display: flex; align-items: center;
  justify-content: center; font-size: 1.3rem; color: var(--ink); background: #F1F5F9;
  border: 1px solid var(--border); }}
.sla-lake .cell.hole {{ background: #CBD5E1; font-size: .7rem; letter-spacing: .1em; color: #334155; }}
.sla-lake .cell.goal {{ background: #A7F3D0; font-size: .7rem; letter-spacing: .1em; }}
.sla-lake .cell.here {{ outline: 2px solid var(--gold); background: #F8F5FD;
  animation: sla-lit-cell 1.6s ease-in-out infinite; }}
@keyframes sla-lit-cell {{ 50% {{ box-shadow: 0 0 0 6px rgba(175,152,228,.18); }} }}
.sla-lake .prop {{ position: absolute; right: .3rem; bottom: .15rem; font-size: .9rem; color: var(--gold-d); }}

.stButton > button[kind="primary"]:disabled, .stFormSubmitButton > button[kind^="primary"]:disabled {{
  opacity: .45; box-shadow: none; cursor: not-allowed; animation: none; }}

/* ================= motion v2 — luxury touch-up (all decorative, CSS-only) ================= */
/* ambient drifting light behind the whole app */
.stApp {{ isolation: isolate; }}
.stApp::before {{ content:""; position:fixed; inset:-20%; z-index:-1; pointer-events:none;
  background: radial-gradient(520px 380px at 20% 30%, rgba(175,152,228,.10), transparent 70%),
  radial-gradient(560px 420px at 80% 70%, rgba(70,50,201,.07), transparent 70%);
  animation: sla-drift 26s ease-in-out infinite alternate; }}
@keyframes sla-drift {{ 0% {{ transform: translate3d(0,0,0) scale(1); }}
  50% {{ transform: translate3d(4%,-3%,0) scale(1.06); }} 100% {{ transform: translate3d(-3%,4%,0) scale(1); }} }}

/* hero: aurora blobs, gold sparks, word-by-word headline, gold sheen */
.sla-hero.big::before, .sla-hero.big::after {{ content:""; position:absolute; border-radius:50%; filter: blur(48px);
  pointer-events:none; z-index:0; }}
.sla-hero.big::before {{ width:360px; height:360px; right:-80px; top:-120px; background: rgba(175,152,228,.28);
  animation: sla-blob 14s ease-in-out infinite alternate; }}
.sla-hero.big::after {{ width:300px; height:300px; left:30%; bottom:-170px; background: rgba(70,50,201,.14);
  animation: sla-blob 18s ease-in-out infinite alternate-reverse; }}
@keyframes sla-blob {{ to {{ transform: translate(-40px, 30px) scale(1.15); }} }}
.sla-hero > div:not(.sla-sparks) {{ position:relative; z-index:1; }}
.sla-hero .w {{ display:inline-block; opacity:0; transform: translateY(.45em); filter: blur(6px);
  animation: sla-word .8s var(--ease) forwards; }}
@keyframes sla-word {{ to {{ opacity:1; transform:none; filter:none; }} }}
.sla-hero.big h1 .gold {{ background: linear-gradient(100deg, var(--gold-d) 0%, #AF98E4 40%, var(--gold-d) 60%,
  #4632C9 100%); background-size: 220% 100%; -webkit-background-clip:text; background-clip:text; color:transparent;
  animation: sla-word .8s var(--ease) forwards, sla-sheen 5s ease-in-out 1.6s infinite; }}
@keyframes sla-sheen {{ 0%,100% {{ background-position: 100% 0; }} 50% {{ background-position: 0 0; }} }}
.sla-hero p, .sla-hero .right, .sla-actions {{ animation: sla-up .7s var(--ease) both; }}
.sla-hero p {{ animation-delay: .55s; }} .sla-hero .right {{ animation-delay: .7s; }}
.sla-actions {{ animation-delay: .85s; }}
.sla-sparks {{ position:absolute; inset:0; pointer-events:none; z-index:0; }}
.sla-sparks i {{ position:absolute; bottom:-10px; width:4px; height:4px; border-radius:50%;
  background: radial-gradient(circle, #F3DFA6, var(--gold)); box-shadow: 0 0 8px rgba(175,152,228,.8); opacity:0;
  animation: sla-rise var(--d, 9s) linear infinite; animation-delay: var(--t, 0s); }}
@keyframes sla-rise {{ 0% {{ opacity:0; transform: translate(0,0) scale(.6); }} 15% {{ opacity:.9; }}
  100% {{ opacity:0; transform: translate(var(--x, 20px), -340px) scale(1.1); }} }}

/* gold CTA: idle glow + arrow nudge */
.sla-btn.gold {{ animation: sla-glow 3.2s ease-in-out 1.5s infinite; }}
@keyframes sla-glow {{ 0%,100% {{ box-shadow: 0 8px 20px -10px rgba(70,50,201,.8); }}
  50% {{ box-shadow: 0 10px 30px -8px rgba(175,152,228,.95), 0 0 0 4px rgba(175,152,228,.12); }} }}
.sla-btn .arr {{ display:inline-block; transition: transform .25s var(--ease); }}
.sla-btn:hover .arr {{ transform: translateX(4px); }}
.sla-btn:active {{ transform: translateY(0) scale(.98); }}

/* learning loop: sweeping progress arc, breathing core, halos */
.sla-arc {{ fill:none; stroke: url(#slaGold); stroke-width:1.6; stroke-linecap:round; stroke-dasharray: 264;
  stroke-dashoffset: 264; transform-origin:50px 50px; transform: rotate(-90deg);
  animation: sla-arc 4s var(--ease) infinite; }}
@keyframes sla-arc {{ 0% {{ stroke-dashoffset:264; }} 70% {{ stroke-dashoffset:0; opacity:1; }}
  100% {{ stroke-dashoffset:0; opacity:0; }} }}
.sla-core {{ transform-origin:50px 50px; animation: sla-breathe 4s ease-in-out infinite; }}
@keyframes sla-breathe {{ 0%,100% {{ transform: scale(1); opacity:.9; }} 50% {{ transform: scale(1.06); opacity:1; }} }}
.sla-halo {{ fill:none; stroke-width:.8; transform-box: fill-box; transform-origin:center; opacity:0;
  animation: sla-halo 4s ease-out infinite; }}
@keyframes sla-halo {{ 0% {{ transform: scale(1); opacity:.7; }} 60%,100% {{ transform: scale(2.6); opacity:0; }} }}
.sla-loop {{ filter: drop-shadow(0 10px 24px rgba(70,50,201,.18)); }}

/* section headers: gold hairline draws in */
.sla-section {{ border-top-color: transparent; position:relative; }}
.sla-section::before {{ content:""; position:absolute; left:0; right:0; top:-1px; height:1px;
  background: linear-gradient(90deg, var(--gold), rgba(175,152,228,.35) 40%, transparent);
  transform-origin:left; animation: sla-draw 1.1s var(--ease) both; }}
@keyframes sla-draw {{ from {{ transform: scaleX(0); }} }}

/* KPI cards: shine line on top, icon float */
.sla-card::after {{ content:""; position:absolute; left:18px; right:18px; top:0; height:2px; border-radius:2px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent); opacity:0; transform: scaleX(.3);
  transition: opacity .3s, transform .5s var(--ease); }}
.sla-card:hover::after {{ opacity:1; transform: scaleX(1); }}
.sla-card:hover .label .ic {{ animation: sla-bob 1.2s ease-in-out infinite; }}
@keyframes sla-bob {{ 50% {{ transform: translateY(-3px); }} }}

/* how it works: line draws, a pulse travels along it, numbers light up in turn */
.sla-steps::before {{ transform-origin:left; animation: sla-draw 1.4s var(--ease) .2s both; }}
.sla-steps::after {{ content:""; position:absolute; top:23px; left:12%; width:7px; height:7px; border-radius:50%;
  background: var(--gold); box-shadow: 0 0 10px 2px rgba(175,152,228,.7);
  animation: sla-travel 5s ease-in-out infinite; }}
@keyframes sla-travel {{ 0% {{ left:12%; opacity:0; }} 10% {{ opacity:1; }} 90% {{ opacity:1; }}
  100% {{ left:88%; opacity:0; }} }}
.sla-step .n {{ animation: sla-lit 5s ease-in-out infinite; }}
.sla-step:nth-child(2) .n {{ animation-delay: 1.25s; }} .sla-step:nth-child(3) .n {{ animation-delay: 2.5s; }}
.sla-step:nth-child(4) .n {{ animation-delay: 3.75s; }}
@keyframes sla-lit {{ 0%,30%,100% {{ background: var(--surface); color: var(--gold-d); }}
  10% {{ background: linear-gradient(135deg,#AF98E4,var(--gold)); color:#FFFFFF;
  box-shadow: 0 0 0 6px rgba(175,152,228,.15), var(--shadow); }} }}
.sla-step:hover .n {{ transform: scale(1.08); transition: transform .25s var(--ease); }}

/* features: gold gradient border on hover, icon turns gold and tilts */
.sla-feature {{ position:relative; }}
.sla-feature::before {{ content:""; position:absolute; inset:0; border-radius: inherit; padding:1px;
  background: linear-gradient(135deg, var(--gold), rgba(175,152,228,0) 45%, rgba(70,50,201,.45));
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude; opacity:0; transition: opacity .35s; pointer-events:none; }}
.sla-feature:hover::before {{ opacity:1; }}
.sla-feature .fi {{ transition: transform .35s var(--ease), background .35s, color .35s; }}
.sla-feature:hover .fi {{ transform: rotate(-8deg) scale(1.08); background: var(--gold-soft); color: var(--gold-d); }}

/* tech chips + team */
.sla-stack span {{ transition: transform .2s var(--ease), background .2s, box-shadow .2s;
  animation: sla-up .5s var(--ease) both; }}
.sla-stack span:hover {{ transform: translateY(-2px); background: var(--gold-soft); box-shadow: var(--shadow); }}
.sla-member .av {{ position:relative; }}
.sla-member .av::before {{ content:""; position:absolute; inset:-5px; border-radius:50%;
  background: conic-gradient(from 0deg, var(--gold), transparent 30%, var(--indigo) 55%, transparent 75%, var(--gold));
  -webkit-mask: radial-gradient(circle, transparent 61%, #000 62%);
  mask: radial-gradient(circle, transparent 61%, #000 62%);
  opacity:.35; animation: sla-rot 8s linear infinite; }}
.sla-member:hover .av::before {{ opacity:1; animation-duration: 2.5s; }}

@media (max-width: 900px) {{ .sla-steps::after {{ display:none; }}
  .sla-hero.big::before {{ width:220px; height:220px; }} }}
/* scroll-reveal where the browser supports scroll-driven animations */
@supports (animation-timeline: view()) {{
  .sla-feature, .sla-member, .sla-step, .sla-panel, div[class*="st-key-card"] {{
    animation: sla-up linear both; animation-timeline: view(); animation-range: entry 0% entry 140px; }}
}}
@media (prefers-reduced-motion: reduce) {{ *, *::before, *::after {{ animation: none !important;
  transition: none !important; }}
  .sla-hero .w {{ opacity:1; transform:none; filter:none; }} .sla-arc {{ stroke-dashoffset:0; }} }}
/* ================= violet redesign (docs/design.md) ================= */
html, body, .stApp {{ font-size: 16px; }}
h1, h2, h3 {{ font-family: var(--serif); }}
.stApp {{ background: radial-gradient(1000px 480px at 92% -8%, rgba(153,101,232,.16) 0%, transparent 62%),
  radial-gradient(900px 480px at -6% 108%, rgba(175,152,228,.20) 0%, transparent 62%), var(--mist); }}
header[data-testid="stHeader"] {{ border-bottom: 1px solid var(--border); }}
:focus-visible {{ outline: 2px solid var(--indigo) !important; outline-offset: 2px; }}
a {{ color: var(--indigo); }}
.sla-card {{ border-radius: 20px; }}
.sla-card .label .ic {{ background: #EDE7FA; color: var(--indigo); }}
.sla-card.accent::before {{ background: var(--card-accent, var(--orchid)); }}
.sla-kicker, .sla-hero .eyebrow, .sla-insight .k, .sla-side .ttl, .sla-auth-brand .eyebrow {{ color: var(--indigo); }}
.sla-badge {{ background: var(--surface); border-color: var(--border); }}
.sla-section {{ border-top-color: var(--border); }}
.sla-step .n {{ color: var(--indigo); }}
.sla-rank.first {{ background: var(--coral-text); color: #fff; }}
.sla-progress .fill {{ background: linear-gradient(90deg, var(--indigo), var(--orchid)); }}
.sla-empty {{ border-color: rgba(70,50,201,.35); }}
.sla-empty .glyph {{ background: #EDE7FA; color: var(--indigo); }}
.sla-verdict .t {{ letter-spacing: .14em; }}
.sla-lock {{ border-color: rgba(70,50,201,.35); }}

/* buttons: indigo pills */
.sla-btn.gold, div[class*="st-key-cta_gold"] [data-testid="stPageLink"] a,
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primaryFormSubmit"],
.stFormSubmitButton > button[kind="primary"] {{ background: var(--indigo); color: #fff !important; border: 0;
  box-shadow: 0 10px 24px -12px rgba(70,50,201,.75); }}
.sla-btn.gold, div[class*="st-key-cta_gold"] [data-testid="stPageLink"] a span,
div[class*="st-key-cta_gold"] [data-testid="stPageLink"] a p, .stButton > button[kind="primary"] p,
.stFormSubmitButton > button[kind^="primary"] p {{ color: #fff !important; }}
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind^="primary"]:hover
   {{ color:#fff; filter: brightness(1.08); }}
.sla-btn.outline, div[class*="st-key-cta_outline"] [data-testid="stPageLink"] a
   {{ background: var(--surface); border:1px solid var(--border); }}
div[data-testid="stDialog"] div[role="dialog"] {{ border-top-color: var(--indigo); }}
div[class*="st-key-card_auth"] {{ border-top-color: var(--indigo); }}

/* dark hero */
div.st-key-hero {{ border: 1px solid rgba(175,152,228,.25); border-radius: 28px; padding: 3rem 2.8rem 2.6rem;
  background: radial-gradient(600px 300px at 82% 0%, rgba(153,101,232,.38), transparent 70%),
  linear-gradient(135deg, #040207 0%, #1E0F27 45%, #41234E 100%);
  box-shadow: 0 30px 60px -30px rgba(65,35,78,.7); }}
div.st-key-hero::before {{ background: rgba(153,101,232,.30); }}
div.st-key-hero::after {{ background: rgba(175,152,228,.16); }}
.sla-hero-copy .eyebrow {{ color: var(--lavender); }}
.sla-hero-copy .eyebrow::before {{ background: var(--lavender); }}
.sla-hero-copy h1 {{ color: var(--mist); font-size: 3.4rem; }}
.sla-hero-copy .w.gold {{ background: linear-gradient(100deg, #AF98E4 0%, #F9F6FA 45%, #9965E8 100%);
  background-size: 220% 100%; -webkit-background-clip: text; background-clip: text; color: transparent; }}
.sla-hero-copy p {{ color: rgba(249,246,250,.82); }}
div.st-key-hero .sla-badge
   {{ background: rgba(249,246,250,.08); color: var(--mist); border-color: rgba(175,152,228,.35); }}
div.st-key-hero .sla-hero-art svg text {{ fill: var(--mist); }}
div.st-key-hero .sla-hero-art .sla-core {{ fill: #41234E; stroke: #AF98E4; }}
div.st-key-hero .sla-hero-art svg circle[fill="#FFFFFF"] {{ fill: #F9F6FA; }}
div.st-key-hero [data-testid="stPageLink"] a {{ transition: transform .2s var(--ease); }}
div.st-key-hero div[class*="st-key-cta_gold"] [data-testid="stPageLink"] a
   {{ background: var(--lavender); box-shadow: none; }}
div.st-key-hero div[class*="st-key-cta_gold"] [data-testid="stPageLink"] a span,
div.st-key-hero div[class*="st-key-cta_gold"] [data-testid="stPageLink"] a p {{ color: var(--void) !important; }}
div.st-key-hero div[class*="st-key-cta_outline"] [data-testid="stPageLink"] a
   {{ background: transparent; border-color: rgba(249,246,250,.4); }}
div.st-key-hero div[class*="st-key-cta_outline"] [data-testid="stPageLink"] a span,
div.st-key-hero div[class*="st-key-cta_outline"] [data-testid="stPageLink"] a p {{ color: var(--mist) !important; }}
.sla-hero {{ border-radius: 28px; border-color: rgba(175,152,228,.3); }}
.sla-hero.big {{ background: linear-gradient(135deg, #040207 0%, #41234E 100%); }}
.sla-hero.big h1, .sla-hero.big .eyebrow {{ color: var(--mist); }}
.sla-hero.big .eyebrow::before {{ background: var(--lavender); }}
.sla-hero.big p {{ color: rgba(249,246,250,.82); }}

/* dark footer */
.sla-footer {{ margin-top: 3.5rem; padding: 1.8rem 2rem; border: 0; border-radius: 28px;
  background: linear-gradient(135deg, #1E0F27, var(--plum)); color: rgba(249,246,250,.75); }}
.sla-footer .brand {{ color: var(--mist); }}
.sla-footer a {{ color: var(--lavender); }} .sla-footer a:hover {{ color: #fff; }}

/* team avatar: gold ring kept, lilac tint */
.sla-member .av {{ border: 2px solid var(--avatar-ring); }}
.sla-member .links a {{ color: var(--indigo); }}
section[data-testid="stSidebar"] {{ background: #FBF8FD; }}
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] {{ background: #EDE7FA; }}

/* 360px phones */
@media (max-width: 480px) {{
  div.st-key-hero {{ padding: 1.8rem 1.2rem 1.6rem; border-radius: 22px; }}
  .sla-hero-copy h1 {{ font-size: 2.2rem; }}
  .sla-footer {{ padding: 1.3rem 1.1rem; border-radius: 20px; }}
  .block-container {{ padding-left: .9rem; padding-right: .9rem; }}
}}
</style>
"""


def inject_css() -> None:
    st.markdown(MISSION_FONTS + CSS + MISSION_CSS, unsafe_allow_html=True)
