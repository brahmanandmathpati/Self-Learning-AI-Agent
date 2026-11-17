# ruff: noqa: E501
"""Mission Control skin: dark control-room look + motion (see docs/design.md, section "Mission Control").

Plain (non-f) string, appended after the base CSS. UI only: colours, glow, motion. Every animation lives under
``prefers-reduced-motion: no-preference`` and is switched off otherwise. Text colours keep WCAG AA contrast on the
#0B0D14 / #121624 surfaces.
"""

MISSION_FONTS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
</style>"""

MISSION_CSS = """
<style>
@property --sla-ang { syntax: '<angle>'; inherits: false; initial-value: 0deg; }

/* ================= Mission Control: tokens ================= */
:root {
  --page:#0B0D14; --band:#121624; --surface:#121624; --surface2:#171C2E; --mist:#0B0D14;
  --ink:#E6E9F2; --secondary:#B4BBD0; --muted:#8A93AD; --border:#232A40; --hair:rgba(34,211,238,.28);
  --cyan:#22D3EE; --lime:#A3E635; --amber:#F59E0B; --rose:#F87171;
  --indigo:#22D3EE; --indigo-soft:rgba(34,211,238,.12); --accent:#22D3EE;
  --gold:#22D3EE; --gold-d:#22D3EE; --gold-soft:rgba(34,211,238,.12); --lavender:#67E8F9; --orchid:#22D3EE;
  --coral:#F59E0B; --coral-text:#F59E0B; --avatar-ring:#22D3EE;
  --good:#A3E635; --warn:#F59E0B; --bad:#F87171;
  --blue:#22D3EE; --orange:#F59E0B; --aqua:#A3E635;
  --radius:14px; --glow:0 0 24px rgba(34,211,238,.33);
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 14px 34px -18px rgba(0,0,0,.8);
  --shadow-lg:0 2px 4px rgba(0,0,0,.4), 0 24px 48px -20px rgba(0,0,0,.9);
  --serif:"Space Grotesk","Inter",system-ui,sans-serif;
}
html, body, [class*="css"], .stMarkdown, button, input, textarea, select { font-family:"Inter",system-ui,sans-serif; }
h1, h2, h3, h4, .sla-hero-copy h1, .sla-card .label, .sla-kicker { font-family:"Space Grotesk","Inter",sans-serif; }
h1, h2, h3, h4 { color:var(--ink); letter-spacing:-.02em; }
p, li { color:var(--secondary); }
a { color:var(--cyan); }
:focus-visible { outline:2px solid var(--cyan) !important; outline-offset:2px; }
::selection { background:rgba(34,211,238,.35); color:#fff; }

/* ================= canvas: grid + aurora ================= */
.stApp { background:
  radial-gradient(900px 520px at 88% -10%, rgba(34,211,238,.13), transparent 62%),
  radial-gradient(800px 480px at -8% 110%, rgba(163,230,53,.07), transparent 62%), var(--page); color:var(--ink); }
.stApp::before { content:""; position:fixed; inset:0; z-index:0; pointer-events:none; opacity:.55;
  background-image:linear-gradient(rgba(34,211,238,.055) 1px, transparent 1px),
    linear-gradient(90deg, rgba(34,211,238,.055) 1px, transparent 1px);
  background-size:44px 44px; -webkit-mask-image:radial-gradient(ellipse at 50% 20%, #000 20%, transparent 78%);
  mask-image:radial-gradient(ellipse at 50% 20%, #000 20%, transparent 78%); }
.block-container { position:relative; }
header[data-testid="stHeader"] { background:rgba(11,13,20,.78); border-bottom:1px solid var(--border);
  backdrop-filter:saturate(160%) blur(14px); -webkit-backdrop-filter:saturate(160%) blur(14px); }
section[data-testid="stSidebar"] { background:#0E111B; border-right:1px solid var(--border); }
section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] {
  background:rgba(34,211,238,.12); box-shadow:inset 2px 0 0 var(--cyan); }

/* ================= surfaces ================= */
.sla-card, .sla-panel, .sla-insight, .sla-step, .sla-feature, .sla-member,
.sla-proof, .sla-lock, .sla-error, .sla-pred, .sla-side, div[data-testid="stForm"], .sla-progress {
  background:linear-gradient(180deg, rgba(23,28,46,.92), rgba(18,22,36,.92)); border:1px solid var(--border);
  border-radius:var(--radius); color:var(--secondary); box-shadow:var(--shadow);
  transition:transform .25s var(--ease), border-color .25s, box-shadow .25s; }
.sla-card:hover, .sla-step:hover, .sla-feature:hover, .sla-member:hover, .sla-insight:hover {
  transform:translateY(-3px); border-color:rgba(34,211,238,.55);
  box-shadow:var(--shadow-lg), 0 0 28px -8px rgba(34,211,238,.45); }
.sla-card .label { color:var(--muted); text-transform:uppercase; letter-spacing:.12em; font-size:.7rem; font-weight:600; }
.sla-card .label .ic { background:rgba(34,211,238,.12); color:var(--cyan); }
.sla-card .value, .sla-count { font-family:"JetBrains Mono",ui-monospace,monospace; color:var(--ink);
  text-shadow:0 0 18px rgba(34,211,238,.35); font-variant-numeric:tabular-nums; }
.sla-card .value.notrun { color:var(--amber); text-shadow:none; font-size:1.05rem; letter-spacing:.08em; }
.sla-card .sub { color:var(--muted); }
.sla-card .delta { color:var(--lime); background:rgba(163,230,53,.12); }
.sla-card .delta.neg { color:var(--rose); background:rgba(248,113,113,.12); }
.sla-card.accent::before { background:var(--card-accent, var(--cyan)); box-shadow:0 0 14px var(--card-accent, var(--cyan)); }
.sla-kicker, .sla-hero .eyebrow, .sla-insight .k, .sla-side .ttl, .sla-auth-brand .eyebrow, .sla-step .n { color:var(--cyan); }
.sla-section { border-top-color:var(--border); }
.sla-section h2, .sla-section h3 { color:var(--ink); }
.sla-badge, .sla-chip { background:rgba(34,211,238,.08); color:var(--cyan); border:1px solid rgba(34,211,238,.35); }
.sla-empty { background:rgba(18,22,36,.7); border:1px dashed rgba(34,211,238,.4); color:var(--secondary); }
.sla-empty .glyph { background:rgba(245,158,11,.14); color:var(--amber); }
.sla-rank.first { background:var(--amber); color:#0B0D14; }
.sla-progress { background:#1B2136; }
.sla-progress .fill { background:linear-gradient(90deg, var(--cyan), var(--lime)); box-shadow:0 0 12px rgba(34,211,238,.6); }
.sla-verdict { background:rgba(163,230,53,.09); border:1px solid rgba(163,230,53,.5); color:var(--lime); }
.sla-verdict .t { color:var(--lime); font-family:"JetBrains Mono",monospace; }
.sla-member .av { border:2px solid var(--cyan); box-shadow:0 0 18px rgba(34,211,238,.35); }
.sla-member .links a { color:var(--cyan); }
code, pre, .mono { color:#A5F3FC; background:rgba(34,211,238,.08) !important; }

.sla-why, .sla-chart-title, .sla-chart-sub { background:none !important; border:0 !important; box-shadow:none !important; color:var(--secondary); }
.sla-chart-title { color:var(--ink); }
.sla-kv div { background:rgba(34,211,238,.06); border-color:var(--border); color:var(--secondary); }
.sla-stack span { background:rgba(34,211,238,.07); border-color:rgba(34,211,238,.3); color:var(--ink); }
input, textarea, div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="textarea"] { background:#0E111B !important; color:var(--ink) !important; }
div[data-baseweb="input"], div[data-baseweb="select"] > div { border-color:var(--border) !important; }
div[data-baseweb="popover"] ul, div[data-baseweb="menu"] { background:#121624 !important; }
label, [data-testid="stWidgetLabel"] p { color:var(--secondary) !important; }

/* ================= hero ================= */
div.st-key-hero, .sla-hero, .sla-hero.big { border:1px solid rgba(34,211,238,.28); border-radius:20px;
  background:radial-gradient(620px 320px at 84% 0%, rgba(34,211,238,.22), transparent 70%),
    radial-gradient(500px 300px at 0% 100%, rgba(163,230,53,.10), transparent 70%),
    linear-gradient(135deg, #0B0D14 0%, #101528 60%, #131A30 100%);
  box-shadow:0 30px 60px -34px rgba(0,0,0,.9), inset 0 0 0 1px rgba(255,255,255,.02); }
div.st-key-hero::before { background:rgba(34,211,238,.18); } div.st-key-hero::after { background:rgba(163,230,53,.10); }
.sla-hero-copy .eyebrow, .sla-hero-copy .eyebrow::before { color:var(--cyan); }
.sla-hero-copy .eyebrow::before, .sla-hero .eyebrow::before { background:var(--cyan); }
.sla-hero-copy h1, .sla-hero.big h1 { color:var(--ink); font-size:3.3rem; }
.sla-hero-copy .w.gold { background:linear-gradient(100deg, #22D3EE 0%, #E6FBFF 45%, #A3E635 100%);
  background-size:220% 100%; -webkit-background-clip:text; background-clip:text; color:transparent; }
.sla-hero-copy p, .sla-hero.big p { color:#C3CADC; }
div.st-key-hero .sla-badge { background:rgba(34,211,238,.08); color:var(--cyan); border-color:rgba(34,211,238,.35); }
div.st-key-hero .sla-hero-art svg text { fill:var(--ink); }
div.st-key-hero .sla-hero-art .sla-core { fill:#101528; stroke:var(--cyan); }
div.st-key-hero .sla-hero-art svg circle[fill="#FFFFFF"], .sla-loop circle[fill="#FFFFFF"] { fill:#0B0D14; }
.sla-loop .sla-ring, .sla-loop .sla-ring2 { stroke:rgba(34,211,238,.35); }
.sla-loop text, .sla-net text { fill:#B4BBD0 !important; }
.sla-net line { stroke:rgba(34,211,238,.45); }
.sla-net circle { fill:#0B0D14; }

/* ================= buttons ================= */
.sla-btn.gold, div[class*="st-key-cta_gold"] [data-testid="stPageLink"] a, div.st-key-hero div[class*="st-key-cta_gold"] [data-testid="stPageLink"] a,
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primaryFormSubmit"], .stFormSubmitButton > button[kind="primary"] {
  background:linear-gradient(135deg, #22D3EE, #67E8F9); color:#06222A !important; border:0; font-weight:700;
  box-shadow:0 0 0 1px rgba(34,211,238,.5), 0 10px 28px -10px rgba(34,211,238,.75); position:relative; overflow:hidden;
  transition:transform .2s var(--ease), box-shadow .2s, filter .2s; }
.sla-btn.gold, div[class*="st-key-cta_gold"] [data-testid="stPageLink"] a span, div[class*="st-key-cta_gold"] [data-testid="stPageLink"] a p,
div.st-key-hero div[class*="st-key-cta_gold"] [data-testid="stPageLink"] a span, div.st-key-hero div[class*="st-key-cta_gold"] [data-testid="stPageLink"] a p,
.stButton > button[kind="primary"] p, .stFormSubmitButton > button[kind^="primary"] p { color:#06222A !important; }
.sla-btn.gold:hover, div[class*="st-key-cta_gold"] [data-testid="stPageLink"] a:hover, .stButton > button[kind="primary"]:hover {
  transform:translateY(-2px); filter:brightness(1.06); box-shadow:0 0 0 1px #22D3EE, 0 14px 34px -8px rgba(34,211,238,.9); color:#06222A; }
.sla-btn.outline, div[class*="st-key-cta_outline"] [data-testid="stPageLink"] a, div.st-key-hero div[class*="st-key-cta_outline"] [data-testid="stPageLink"] a,
.stButton > button:not([kind="primary"]) { background:rgba(34,211,238,.05); color:var(--ink); border:1px solid rgba(34,211,238,.4); }
div[class*="st-key-cta_outline"] [data-testid="stPageLink"] a span, div[class*="st-key-cta_outline"] [data-testid="stPageLink"] a p,
div.st-key-hero div[class*="st-key-cta_outline"] [data-testid="stPageLink"] a span, div.st-key-hero div[class*="st-key-cta_outline"] [data-testid="stPageLink"] a p { color:var(--ink) !important; }
.stButton > button:not([kind="primary"]):hover, div[class*="st-key-cta_outline"] [data-testid="stPageLink"] a:hover {
  border-color:var(--cyan); background:rgba(34,211,238,.12); transform:translateY(-1px); }

/* ================= tabs / inputs / charts ================= */
button[data-baseweb="tab"] { color:var(--muted); } button[data-baseweb="tab"][aria-selected="true"] { color:var(--cyan); }
div[data-baseweb="tab-highlight"] { background:var(--cyan) !important; box-shadow:0 0 12px var(--cyan); }
div[data-baseweb="tab-border"] { background:var(--border) !important; }
details, [data-testid="stExpander"] { border-color:var(--border) !important; background:rgba(18,22,36,.6); border-radius:12px; }
div[data-testid="stAlert"] { background:rgba(18,22,36,.85); border:1px solid var(--border); color:var(--secondary); }
.js-plotly-plot .hoverlayer .hovertext path { fill:#121624 !important; stroke:#22D3EE !important; }
.js-plotly-plot .hoverlayer .hovertext text { fill:#E6E9F2 !important; }
.js-plotly-plot .annotation-text-g text { fill:#E6E9F2 !important; opacity:1 !important; }
.js-plotly-plot .xtick text, .js-plotly-plot .ytick text, .js-plotly-plot .legendtext { fill:#B4BBD0 !important; }
.js-plotly-plot .gridlayer path, .js-plotly-plot .zerolinelayer path { stroke:rgba(138,147,173,.16) !important; }
.sla-footer { background:linear-gradient(135deg, #0E111B, #121A30); border:1px solid var(--border); color:#B4BBD0; border-radius:20px; }
.sla-footer .brand { color:var(--ink); } .sla-footer a { color:var(--cyan); } .sla-footer a:hover { color:#fff; }

/* ================= motion (opt-in) ================= */
@keyframes mc-dot { 0% { box-shadow:0 0 0 0 rgba(34,211,238,.7); } 70%,100% { box-shadow:0 0 0 9px rgba(34,211,238,0); } }
@keyframes mc-grid { to { background-position:44px 44px, 44px 44px; } }
@keyframes mc-sweep { 0% { transform:translateX(-120%); } 60%,100% { transform:translateX(220%); } }
@keyframes mc-spin { to { --sla-ang:360deg; } }
@keyframes mc-draw { from { stroke-dashoffset:5000; } to { stroke-dashoffset:0; } }
@keyframes mc-bar { from { transform:scaleY(0); } to { transform:scaleY(1); } }
@keyframes mc-fade { from { opacity:0; } to { opacity:1; } }
@keyframes mc-glow { 0%,100% { box-shadow:0 0 0 1px rgba(163,230,53,.4), 0 0 10px rgba(163,230,53,.15); }
  50% { box-shadow:0 0 0 1px rgba(163,230,53,.8), 0 0 26px rgba(163,230,53,.45); } }
@keyframes mc-scan { 0% { top:-2px; opacity:0; } 10% { opacity:.8; } 90% { opacity:.8; } 100% { top:100%; opacity:0; } }
@keyframes mc-float { 50% { transform:translateY(-6px); } }
@keyframes mc-flicker { 0%,100% { opacity:1; } 92% { opacity:1; } 94% { opacity:.55; } 96% { opacity:1; } }

@media (prefers-reduced-motion: no-preference) {
  .stApp::before { animation:mc-grid 14s linear infinite; }
  .sla-kicker::before, .sla-hero .eyebrow::after, .sla-status .dot, .sla-dot { animation:mc-dot 1.8s ease-out infinite; }
  .sla-kicker::before { content:""; display:inline-block; width:8px; height:8px; border-radius:50%; background:var(--cyan);
    margin-right:.55rem; vertical-align:middle; }
  .sla-hero .eyebrow::after { content:""; width:8px; height:8px; border-radius:50%; background:var(--lime); }
  .sla-card:not(.static)::after { content:""; position:absolute; inset:0; pointer-events:none; width:40%;
    background:linear-gradient(100deg, transparent, rgba(34,211,238,.10), transparent); transform:translateX(-120%); }
  .sla-card { position:relative; overflow:hidden; }
  .sla-card:hover::after { animation:mc-sweep 1.1s var(--ease); }
  div.st-key-hero, .sla-hero { position:relative; }
  div.st-key-hero::before, div.st-key-hero::after { animation:mc-float 7s ease-in-out infinite; }
  .sla-verdict { animation:mc-glow 2.6s ease-in-out infinite; }
  .sla-verdict .t { animation:mc-flicker 6s linear infinite; }
  .sla-member .av { animation:mc-glow 4s ease-in-out infinite; }
  .sla-btn.gold::after, .stButton > button[kind="primary"]::after, div[class*="st-key-cta_gold"] [data-testid="stPageLink"] a::after {
    content:""; position:absolute; top:0; bottom:0; width:40%; left:0; pointer-events:none;
    background:linear-gradient(100deg, transparent, rgba(255,255,255,.28), transparent); transform:translateX(-120%);
    animation:mc-sweep 3.6s ease-in-out infinite; }
  /* charts draw themselves; bars grow from the baseline */
  .js-plotly-plot .scatterlayer .trace path.js-line { stroke-dasharray:5000; animation:mc-draw 1.8s var(--ease) both; }
  .js-plotly-plot .scatterlayer .trace .fills path, .js-plotly-plot .scatterlayer .trace .js-fill { animation:mc-fade 1.6s .5s both; }
  .js-plotly-plot .scatterlayer .trace .points path { animation:mc-fade .6s 1.2s both; }
  .js-plotly-plot .barlayer .points path { transform-box:fill-box; transform-origin:50% 100%; animation:mc-bar .9s var(--ease) both; }
  .js-plotly-plot .heatmaplayer { animation:mc-fade .9s both; }
  div[data-testid="stPlotlyChart"] { position:relative; }
  div[data-testid="stPlotlyChart"]::after { content:""; position:absolute; left:0; right:0; height:2px; top:-2px; pointer-events:none;
    background:linear-gradient(90deg, transparent, rgba(34,211,238,.7), transparent); animation:mc-scan 2.6s ease-out 1 both; }
  /* spinner */
  div[data-testid="stSpinner"] i, div[data-testid="stSpinner"] svg { filter:drop-shadow(0 0 6px var(--cyan)); }
  /* rotating neon edge on the active run card */
  .sla-card.live { background:linear-gradient(var(--surface), var(--surface)) padding-box,
      conic-gradient(from var(--sla-ang), #22D3EE, #A3E635, #22D3EE) border-box; border:1px solid transparent;
    animation:mc-spin 5s linear infinite; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation:none !important; transition:none !important; scroll-behavior:auto !important; }
  .sla-card:hover, .sla-step:hover, .sla-feature:hover, .sla-member:hover { transform:none; }
}

/* ================= 360px phones ================= */
@media (max-width:480px) {
  div.st-key-hero { padding:1.6rem 1.1rem; border-radius:16px; }
  .sla-hero-copy h1, .sla-hero.big h1 { font-size:2.1rem; }
  .block-container { padding-left:.9rem; padding-right:.9rem; }
  .sla-card:hover { transform:none; }
  div.st-key-hero_cta { flex-wrap:wrap; gap:.5rem; }
  div.st-key-hero [data-testid="stPageLink"] a { padding:.55rem .9rem; font-size:.88rem; white-space:nowrap; }
}
</style>
"""
