# design.md — Self-Learning AI Agent website

Design specification for the project website (Streamlit app, `src/sla/app/`).
**Inspiration:** the colour palette and the "case-study" storytelling style of the Dribbble shot
*Case Study: Website Design for EternaCloud* by tubik (<https://dribbble.com/shots/26682683-Case-Study-Website-Design-for-EternaCloud>).
We use it only as a mood reference: the palette below was read from the shot's published colour list, and nothing
else (logo, copy, illustrations, layouts) is copied. Our own product, content and components stay ours.

> Honest note: the shot's large images could not be opened from the build environment, so the *layout* guidance in
> Section 5 is our interpretation of a "case study" page (problem → approach → proof), not a pixel match.

---

## 1. Design idea in one line

**A calm, premium "deep violet" look that makes a hard topic (reinforcement learning) feel clear and trustworthy** —
dark, confident hero sections; pale lilac pages for reading; one warm coral accent for the moments that matter
(results, warnings, call-to-action).

Principles:

1. **Proof first.** Every page shows a real number or chart from the results database before any explanation.
2. **Plain words.** Beginner-level copy, one idea per card, a practice example at the end of each learning page.
3. **Honest states.** Missing data says `NOT MEASURED YET` / `NOT RUN`, never a fake value.
4. **Quiet motion.** Short fade-ups only; everything off under `prefers-reduced-motion`.
5. **Colour = identity.** An agent keeps the same colour on every chart and badge on every page.

---

## 2. Colour tokens

Palette from the reference (7 colours), given roles for our app. Contrast ratios are computed (WCAG 2.1).

| Token | Hex | Role | Notes |
|---|---|---|---|
| `--void` | `#040207` | Darkest background, hero text on light | 19.3 : 1 on `--mist` |
| `--mist` | `#F9F6FA` | Page background (light mode) | Replaces ivory `#FAF8F4` |
| `--plum` | `#41234E` | Dark panels, headings on light, footer | 12.4 : 1 on `--mist` |
| `--lavender` | `#AF98E4` | Soft accents, chips, borders, glow on dark | 8.3 : 1 on `--void`; **never as text on light** (2.3 : 1) |
| `--indigo` | `#4632C9` | Primary action, links, focus ring | 7.7 : 1 on `--mist`; white text on it 8.2 : 1 |
| `--coral` | `#C96B4B` | Highlight: key result, "new", warm CTA | 3.4 : 1 on `--mist` → use for large text / icons / fills only |
| `--orchid` | `#9965E8` | Secondary accent, AI/learning elements | 5.3 : 1 on `--void`; on light use only as fill or ≥18 px text |

Derived tokens (computed from the above, keep the same names in CSS):

| Token | Value | Use |
|---|---|---|
| `--surface` | `#FFFFFF` | Cards on `--mist` |
| `--surface-2` | `#F1EBF6` | Bands, table stripes, code background |
| `--ink` | `#040207` | Headings |
| `--body` | `#41234E` at 85 % → `#5A4763` | Paragraph text (≥ 7 : 1) |
| `--muted` | `#6B5B73` | Captions (5.8 : 1 on `--mist`) |
| `--border` | `rgba(65,35,78,.12)` | Card outline |
| `--coral-text` | `#B4562F` | Coral when it must be **text** on light (4.5 : 1) |
| `--glow` | `radial-gradient(600px 300px at 80% 0%, rgba(153,101,232,.35), transparent 70%)` | Hero glow |

Status colours (always with an icon + word, never colour alone):
good `#15803D` · warning `#B45309` · serious `#C2410C` · critical `#B91C1C` · info `--indigo`.

### 2.1 Agent and chart colours (identity follows the entity)

Charts keep **colour-blind-safe, high-separation** hues; the reference palette is used for chrome, not for data.
Do not change these between pages.

| Entity | Colour | Why |
|---|---|---|
| Q-learning | `#3987E5` | Existing blue; keeps old screenshots valid |
| SARSA | `#D95926` | Existing orange |
| Expected SARSA | `#8B5CF6` | Near `--orchid`; reads as "family of SARSA" |
| DQN | `#199E70` | Distinct green for the neural agent |
| Random baseline | `#94A3B8` | Neutral grey = "no learning" |
| Ablation: full / no replay / no target | `#3987E5` / `#D95926` / `#199E70` | Same as `VARIANT_COLORS` |

Rules: max 4 series per chart; always a legend; thin lines for seeds, thick line for the mean; no rainbow scales;
gridlines at 7 % opacity.

### 2.2 Dark and light

* **Reading pages** (Training, Evaluation, Comparison, Runs) = light: `--mist` page, white cards.
* **Story pages** (Overview hero, About, footer) = dark: `--void` → `--plum` gradient with the lavender glow.
* Dark panels never contain charts with grey seed lines unless the line colour is lightened (`#CBD5E1`).

---

## 3. Typography

| Role | Font | Size / weight | Notes |
|---|---|---|---|
| Display / hero | **Playfair Display** (already loaded) | 44–56 px / 600, tracking −0.02 em | Keeps the project's editorial voice |
| Section title | Playfair Display | 28–32 px / 600 | |
| Card title | **Inter** | 18 px / 600 | |
| Body | Inter | 16 px / 400, line-height 1.65 | Max line width 68 characters |
| Caption / eyebrow | Inter | 12 px / 600, uppercase, +0.18 em | Eyebrow has a 28 px line before it (existing `.eyebrow`) |
| Numbers (metrics) | Inter, `font-variant-numeric: tabular-nums` | 40–56 px / 700 | Big result numbers |
| Code / paths / seeds | JetBrains Mono | 13 px | |

Optional swap if a more "tech" feel is wanted: Mona Sans or Space Grotesk for display. Keep Playfair for the report PDF.

---

## 4. Shape, space, depth

* **Spacing unit:** 4 px. Scale: 4 · 8 · 12 · 16 · 24 · 32 · 48 · 72 · 96.
* **Radius:** cards 20 px, hero panels 28 px, buttons and chips fully rounded (999 px), inputs 12 px, avatars circle.
* **Shadows:** `0 1px 2px rgba(4,2,7,.05), 0 12px 32px -16px rgba(65,35,78,.28)`; large cards add a second layer.
  On dark panels use a 1 px `rgba(175,152,228,.25)` outline instead of a shadow.
* **Container:** max width 1200 px; 24 px side gutter on phones; sections separated by 72–96 px.
* **Grid:** 12 columns desktop, 6 tablet, 1 phone. Metric cards 4-up → 2-up → 1-up.

---

## 5. Page structure ("case-study" rhythm)

Every main page follows **Problem → Approach → Proof → Next step**, the same rhythm as a design case study.

### 5.1 Overview (home)

1. **Hero (dark):** eyebrow `FINAL-YEAR B.TECH PROJECT`, Playfair title "An AI agent that learns from experience",
   one-line promise, two buttons (primary `Watch it learn` → Training, secondary `Read the results`),
   right side: a live mini learning curve from the stored FrozenLake run.
2. **Proof strip (light):** four metric cards — FrozenLake success 1.000 vs 0.012 · CartPole 425.92 vs 22.58 ·
   Taxi / CliffWalking best returns · 242 tests. Each card links to its page.
3. **Challenge:** "Most 'AI agents' never learn" — 3 short cards (real learning, fair test, statistics).
4. **How it works:** 4-step horizontal flow (Play → Learn → Test fairly → Explain), each with a small icon.
5. **Games & learners:** a 4 × 3 matrix (FrozenLake, Taxi, CliffWalking, CartPole × Q-learning, SARSA, Expected SARSA, DQN) with
   dots showing what has been run; hovering shows the real result.
6. **Vision Lab teaser:** dark panel with the gesture photo and a "Try it" button.
7. **Team + college block**, then **FAQ**, then **footer** (dark `--plum`).

### 5.2 Environments
Tabs per game. Each tab: left = short story and rules table; right = the learned-path map with arrows; below = the
Q-learning vs SARSA vs Expected SARSA path cards (gold path squares, cliff squares in `--surface-2` with `CLIFF` label).

### 5.3 Training
Left rail (form): game, learner, episodes, α, γ, ε; right: live chart + reflection card. The **Start** button is
`--indigo`; the **Stop** button is outlined. Show the "stopping the page stops the run" warning in a `warning` banner.

### 5.4 Comparison / Evaluation / Ablation
Winner banner uses `--coral` fill with dark text ("LEARNING VERIFIED"); tie states use a lavender banner
("Tied — no ranking claimed"). Statistics in a compact table; plain-words sentence under every table.

### 5.5 Vision Lab
Four tabs (live, photo, video, results). Empty results show a `NOT RUN` card in lavender, never a score.

### 5.6 About / Report
Architecture diagram on a dark panel, team cards, college details, link to the PDF report.

---

## 6. Components

| Component | Spec |
|---|---|
| **Button – primary** | `--indigo` fill, white text, pill, 44 px high, hover lifts 2 px and brightens 6 % |
| **Button – secondary** | White fill, 1 px `--border`, `--ink` text, pill |
| **Button – on dark** | `--lavender` fill, `--void` text |
| **Metric card** | White, radius 20, 1 px border; label (caption), number (Inter 700, tabular), delta line with ▲/▼ + word, tiny sparkline |
| **Run card** | Title (agent · game), status badge, seed chips, mini curve, buttons `Open` / `Share` |
| **Status badge** | Pill with icon: ✔ completed (good), ⏸ stopped (warning), ✖ failed (critical), ● running (info) |
| **Chip** | Radius 999, `rgba(175,152,228,.18)` fill, `--plum` text |
| **Callout** | Left 4 px bar: indigo = tip, coral = key result, amber = caution; icon + title |
| **Reflection card** | Lavender-tinted card with "Explained in plain words" label and a "grounded" check (every number matches the data) |
| **Empty / error state** | Icon, one sentence of what happened, one button for what to do (e.g. "The hand-tracking model could not start on this server.") |
| **Team card** | 84 px avatar with gold ring (kept from the current design), name, role, GitHub and LinkedIn icon buttons; hide a link when it is missing |
| **Tabs** | Underline style, active tab `--indigo` with a 2 px bar; scroll horizontally on phones |
| **Policy map** | Grid cells 44 px, arrows in `--ink`, walked path cells filled `#F5ECD7`, goal `#CFF5E7`, cliff/hole `--surface-2` |
| **Table** | Header `--surface-2`, 1 px row borders, numbers right-aligned and tabular |

The gold (`#C9A24B`) from the current theme survives only as the **avatar ring and the walked-path fill**, so old
screenshots and the report remain consistent; the primary brand colour moves from gold/indigo to the plum–indigo pair.

---

## 7. Motion

* Entrance: 10 px fade-up, 450 ms, `cubic-bezier(.2,.7,.2,1)`, 60 ms stagger (existing `sla-up`).
* Hero glow drifts slowly (20 s ease-in-out, 8 px); pause when the tab is hidden.
* Numbers count up once when they enter the viewport (600 ms) — but the final text is in the DOM from the start.
* Charts: draw lines left → right over 700 ms on first view only.
* `@media (prefers-reduced-motion: reduce)` → no transforms, no count-up, no glow drift.

---

## 8. Accessibility

* Text contrast ≥ 4.5 : 1 (large text ≥ 3 : 1). `--lavender` and `--coral` are never used for small text on light.
* Visible focus: 2 px `--indigo` ring with 2 px offset (on dark: `--lavender`).
* Colour is never the only signal: statuses and winners carry an icon and a word; chart series have direct labels or a legend.
* Touch targets ≥ 44 px; layout works at 360 px width with no horizontal page scroll.
* Images have alt text; decorative glows are CSS only.
* Every number in generated notes must exist in the data (grounding check) — a design rule as much as a code rule.

---

## 9. Voice and content

* Short sentences, everyday words, one idea per card, a "plain words" line under every table or chart.
* Say what was measured, how many seeds, and on which held-out games.
* No exaggerated claims; unknown = `NOT MEASURED YET`; ties are called ties.
* No AI/assistant attribution anywhere in the UI or repository.

---

## 10. Implementation notes (Streamlit)

Where to change things (all in `src/sla/app/`):

| File | Change |
|---|---|
| `styles/theme.py` | Replace `INK`, `GOLD`, `INDIGO` tokens and the `:root` variables with the Section 2 tokens; keep `SERIES`, `AGENT_COLORS`, `VARIANT_COLORS` |
| `.streamlit/config.toml` | `primaryColor = "#4632C9"`, `backgroundColor = "#F9F6FA"`, `secondaryBackgroundColor = "#F1EBF6"`, `textColor = "#040207"` |
| `components/landing.py` | Dark hero, proof strip, games × learners matrix, footer on `--plum` |
| `components/section_header.py`, `motion.py` | Eyebrow, Playfair titles, count-up and glow (respect reduced motion) |
| `charts/figures.py` | Plotly template with Section 2.1 colours, 7 % grid, transparent background, Inter 12 px |
| `views/*.py` | Follow the Section 5 rhythm; keep all copy beginner-friendly |

Streamlit limits to remember: no true full-bleed sections (use a wrapper `div` with negative margins), fonts must
come from Google Fonts imports, and anything sticky needs CSS only (no JS). Test at 1440, 1024 and 390 px, with and
without data, as a guest and as a signed-in user.

### Design tokens as CSS

```css
:root {
  --void:#040207; --mist:#F9F6FA; --plum:#41234E; --lavender:#AF98E4;
  --indigo:#4632C9; --coral:#C96B4B; --orchid:#9965E8;
  --surface:#FFFFFF; --surface-2:#F1EBF6; --ink:#040207; --body:#5A4763; --muted:#6B5B73;
  --border:rgba(65,35,78,.12); --coral-text:#B4562F;
  --radius:20px; --radius-lg:28px; --ease:cubic-bezier(.2,.7,.2,1);
  --shadow:0 1px 2px rgba(4,2,7,.05), 0 12px 32px -16px rgba(65,35,78,.28);
  --serif:"Playfair Display", Georgia, serif;
}
@media (prefers-reduced-motion: reduce){ *{animation:none!important; transition:none!important} }
```

---

## 11. Rollout checklist

1. Branch from `main`, e.g. `feat/violet-redesign` (merge by pull request; never push to `main`).
2. Update tokens in `theme.py` and `config.toml`; check all pages in light mode.
3. Rebuild the Overview hero and proof strip; verify numbers come from the database snapshot.
4. Restyle charts with the shared template; confirm agent colours did not change.
5. Run the UI tests (`tests/ui/`) and take new screenshots at three widths.
6. Update README and the report screenshots; mention the design reference once (Section 0 credit).
7. Reboot the Streamlit Cloud app after the merge so the new theme loads.

*Reference credit: palette and case-study mood inspired by tubik's "Case Study: Website Design for EternaCloud" on Dribbble.*

## 11. Mission Control skin (branch `feat/mission-control`)

A dark "control room" look layered on the violet system. Only UI files change: `styles/mission.py` (new skin and motion),
`styles/theme.py` (colour tokens, white surfaces to variables), `components/motion.py` (SVG colours), `assets/logo.svg`,
`charts/figures.py` (grid-map and confusion-matrix colours) and `.streamlit/config.toml` (dark base). No logic, data or
number changes.

| Token | Value | Use |
|---|---|---|
| page / card | `#0B0D14` / `#121624` | background, surfaces |
| text / secondary / muted | `#E6E9F2` / `#B4BBD0` / `#8A93AD` | all at least 5:1 on the surfaces (WCAG AA) |
| cyan / lime / amber | `#22D3EE` / `#A3E635` / `#F59E0B` | actions and Q-learning / success and SARSA / warnings, NOT RUN and DQN |

Fonts: Space Grotesk (headings), Inter (body), JetBrains Mono (numbers).

Motion (all CSS, all off under `prefers-reduced-motion`): drifting grid, pulsing live dots, count-up numbers (existing),
hover lift with sweep and glow, rotating signal on the orbit, glowing "learning verified" badge, charts that draw their
line and grow their bars, a scan line over each new chart, shine on primary buttons.

Not done (would need new logic or data, so out of scope for a UI-only change): the "watch the agent play" replay and the
Problem / Approach / Proof / Next step page framing.

Screenshots: `docs/redesign/mission_*.jpg` (before: `after_*.jpg` from the violet round).
