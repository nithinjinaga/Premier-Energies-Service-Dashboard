# Restyle log — token-accurate SaaS redesign

Branch `trial-1` worktree. Visual reference: `design reference/Shopeers dashboard — editable.png`
(primary) and `dashboard-overview.png` (secondary). Spec basis: `design.md` (token hypothesis),
`dashdesign.md` (1×-scale reading), `plan.md` (DOM contract §0.3).
Product changes live in `build_dashboard.py` only; `index.html` is regenerated from it
(`python build_dashboard.py`) and data logic / interactions are unchanged.

## 1. Scale — design.md vs dashdesign.md

The Shopeers PNG is 1878×1284. Two rival readings: `design.md` guessed ÷1.3 (≈1440 design
viewport); `dashdesign.md` divided by 2 (939 viewport). Pixel measurement settles it:

| artifact | PNG px | ÷1.3 (design.md) | ÷2 (dashdesign.md) |
|---|---|---|---|
| rail width | 316 | **243 px** | 158 px |
| topbar height | 74 | **57 px** | 37 px |
| nav item label cap height | 12 | **~13 px font** | ~8.5 px font |
| export button height | 47 | **~36 px** | ~23.5 px |
| KPI value cap height | 28 | **~30 px font** | ~19.5 px font |
| page-title cap height | 23 | **~25 px font** | ~16 px font |

÷2 yields 8px nav labels, 23px buttons, 22px search fields — unusable. ÷1.3 lands every
artifact on standard SaaS sizing. **÷1.3 confirmed; dashdesign.md's 939 reading rejected.**
Also verified at runtime: our build at a true 1440 viewport reproduces the reference's rail /
topbar proportions almost exactly (see `screenshots/00-side-by-side.png`).

## 2. Palette — sampled vs adopted

Sampled directly from the PNG (dominant-color / saturated-dominant / darkest-pixel sampling,
full-res). design.md values confirmed nearly exactly: canvas `#f5f7f9`, card `#ffffff`,
subtle `#fafafc`, border `#eeeef1`, grid `#f1f3f6`, text-1 `#191b1e`, text-2 `#5b5d62`,
text-3 `#85858f`, primary `#2861ff`, primary-50 `#eff4ff`, success-tone `#43ba8b`,
gauge `#42c78b`, danger `#eb4776`, chip tints `#eaf8f1` / `#fceaf0`.

Adopted corrections (all for WCAG, hues kept):

| token | sampled | adopted | reason |
|---|---|---|---|
| `--text-3` | `#85858f` | `#6e7076` | 3.65:1 on white fails AA 4.5:1 for 11–14px labels |
| `--success` (text) | `#43ba8b` | `#147a58` | only 2.2:1 on its own tint |
| `--success-tone` (chart fill) | `#43ba8b` | `#2ea276` | 2.43:1 < 3:1 graphics rule |
| `--danger` (text) | `#eb4776` | `#d93064` | 3.4:1 fails AA as text |
| `--c3` (chart fill) | — | `#eb4776` kept | 3.69:1, passes graphics rule |
| `--warning` (chart/accent) | `#ff8a3d` | `#ea6a10` | 2.35:1 → 3.20:1 |
| `--warn-text` (WIP pill) | `#ff8a3d` | `#b45309` | text on warning-50 tint needs 4.5:1 |
| active nav label | primary | `--primary-600 #1f4fe0` | 4.49:1 on primary-50 is a hair under 4.5 — 5.86:1 |
| `--c5` teal | `#14b8c4` | `#0f9aa5` | 2.42:1 → 3.39:1 |
| `--c1` | `#e87f3a` (old) | `#ea6a10` | slot re-mapped to AA-passing orange |

Undocumented tokens added: `--primary-100 #d6e2ff` (note-box border), `--bg-muted #eeeef0`
(rank chips), `--border-strong #e2e3e6` (selects/buttons).

## 3. Measured-vs-token disagreements

- Topbar: measured 57 → token `56px` (4px-grid rounding).
- Page title: measured cap ≈ 25px em → token `26px` (design.md said 26; kept 26).
- gauge-off: empty-arc sample gave `#f3f4f6`; kept design.md's `#d2d3d6` (sample likely hit
  the blank inner region, not tick ink). Gauge isn't used in our UI (status is a donut),
  so the value is inert.
- Slot `--c6` yellow kept at `#f5b400` **as documented dead slot** — no rendered chart reaches
  SLOT 6 ("No Issue" never runs a defect chart), and yellow cannot reach 3:1 on white without
  turning brown. Flagged rather than darkened.

## 4. Typography

- **Inter** 400/500/600/700 via Google Fonts (`display=swap`), system-webkit fallback stack in
  `--font`.
- License note: Inter is SIL OFL 1.1 — free for commercial use, self-host or Google-host both
  fine. Adobe/Monotype alternates (Source Sans, Helvetica Now) were considered but add
  licensing/config cost for zero visual gain here; the choice is one line (`--font`) if the
  brand later mandates a typeface.
- Scale: display 36 / h1 26 / KPI value 30 / h2–h3 16–15 / body 14 / small–chip 12 / micro 11.
  Micro labels uppercase, +0.04em tracking (the reference's table headers, pill labels, rail
  "MENU" all speak this way).

## 5. Layout & markup changes (presentational only)

- New left rail (243px, flat white, border-right): brand mark + "Premier Energies", `MENU`
  micro-label, 7 lucide-style inline SVG jump-links to `#sec-*` anchors, `DATA THROUGH Aug 2026`
  footer. Hidden ≤768px (no drawer — body doesn't scroll-lock under it, mobile keeps topbar
  brand). `active` state is static on Overview — **shortcut: no scrollspy**, upgrade if the page
  ever grows beyond one screen group.
- New sticky topbar: right cluster holds the existing month tools (`#months`, all JS-built
  classes kept: `.mbtn/.hdr-search/.cal-btn/.month-pop`); brand mark appears on mobile only.
- Body split `.main > .topbar + main.page`; section anchor ids added on pagehead/section labels.
- KPI cards: colored left accent bars removed; icon slot added top-right (inline SVG, primary
  color). Semantic color moved to the note lines (JS-set, tokens).
- Top-3 badges: solid colorful pills → white strip cells with 2px left rule in slot colors +
  neutral rank circle (reference "Customers" strip language). Classes `b0/b1/b2/.rank` kept,
  JS fill untouched.
- `note-box` re-skinned amber→info-blue (primary-50) to match the reference's banner language.
- Loading screen moved from inline styles to classes; ids kept.
- Filter bar: single surface card, uppercase micro labels, `--h-ctl` selects.
- Micro-updates to static copy: subtitle date range extended to "Dec 2024–Aug 2026" to match the
  actual dataset (was stale "Jul 2026"); new empty-state row is new copy.

## 6. JS changes (styling-path only)

- `getComputedStyle` helpers `V(name)` / `A(name, alpha)`; `COLORS[i]` now resolve `--c0..--c7`;
  `Chart.defaults` color/border/family come from tokens (canvas can't use `var()` directly).
- Semantic chart rule (design.md §10.1): Closed→`--success`, WIP→`--warning` everywhere
  (`chMonthly` stacks, `chStatus` donut gets explicit mapped colors; status pill mapping in the
  table was already regex-driven and stays).
- Old inline hexes replaced: pareto `#f59e0b`→`--c1`, cust violet `#8b5cf6`→`--c4`, state teal
  `#14b8a6`→`--c5`, TAT SOP dashed `#ff3b30`→`--danger`, heatmap `rgba(50,102,173,α)`→
  `A('--c0',α)`, empty-cell `#f5f5f7`→`var(--bg-app)`, `var(--good/--bad/--warn)`→
  `--success/--danger/--warn-text`.
- `Chart.defaults.animation=false`: time-based easing never advances under headless/virtual-time
  capture and adds no value on a dense ops dashboard (also makes screenshots deterministic).
- `document.fonts.ready` redraw removed — Inter loads before the 15MB parse finishes; the
  redraw only re-triggered chart animations.
- New: empty-state row ("No records match these filters") when a filter combo yields nothing;
  previously the table went blank with no explanation.
- `old var(--txt/--txt2/--good/--warn/--bad)` users migrated to the new token names.

**Elevate pass additions**

- **Token resolver fix:** unregistered custom properties are not converted by
  `getComputedStyle` — `getPropertyValue('--c0')` returns the raw `#2861ff`, so the previous
  digit-parse in `A()` produced invalid `rgba(2861,undefined,…)` strings (Chart.js silently
  dropped them; heatmap tints were weaker than designed). `A()` now resolves tokens through a
  cached offscreen probe element (`rgb(40,97,255)`), used by alpha fills and the new
  `grads()` gradient factory.
- **KPI trend chips** (the reference's signature element): each KPI card gets a `▲/▼ ±x.x%` pill
  vs the prior period. Rule: the selection must be one contiguous run of months, and the prior
  period is the run of the same length immediately before it (Feb-26 → Jan-26;
  Jan–Mar-26 → Oct–Dec-25). Default view (all 21 months) and gappy selections show no chip —
  no baseline, no fabricated number. Below the value, the note reads `vs. <prev value> · <period>`;
  single-month selections otherwise keep the month-name note. Direction→color is per-metric
  (closed/rate: up=good; TAT/WIP: down=good). Prior KPIs re-run the same aggregation formulas on
  the same static filters — no interaction/methodology change to the current-period numbers.
- **Donut center totals:** inline Chart.js plugin draws the slice sum + caption (`MODULES` /
  `DEFECTS`) in the doughnut hole, token-fed colors.
- **Gradient fills:** `grads()` builds token-tinted vertical ramps (horizontal when `indexAxis:y`)
  for `chCat/chPareto/chState/chCust/chTop3` bars, per-slot for multi-slot charts, and a soft
  fade for the TAT area fill. Donuts stay flat (reference language).
- **mkStacked cap:** single-month stacked pillars blew out full-width; datasets now carry
  `maxBarThickness:38`.
- **Hero card:** `chTop3` box is its own height token (`--h-hero`, 340/260/250px per tier) and
  the card carries `--shadow-2`; top-3 badge rank dots pick their slot color via `--rk`.

## 7. Token discipline check (machine-verified)

Python scan of the generated `index.html` `<style>` block: after stripping comments and
excluding `:root{}` token blocks (including the per-breakpoint token *overrides*, which only
redefine tokens), there are **zero `#hex` literals and zero raw `px` values** in the remaining
CSS. JS contains no raw color hex either. 79 tokens defined in `:root`.

## 8. WCAG AA — actual pairs used (computed)

| pair | ratio | verdict |
|---|---|---|
| text-1 #191b1e / white | 17.26 | AA |
| text-2 #5b5d62 / white | 6.59 | AA |
| text-3 #6e7076 / white · canvas · subtle | 4.95 · 4.61 · 4.75 | AA |
| primary #2861ff / white | 4.95 | AA |
| white / primary (buttons, month chips) | 4.95 | AA |
| primary-600 / primary-50 (active nav) | 5.86 | AA |
| success #147a58 / white · success-50 (Closed pill) | 5.31 · 4.85 | AA |
| danger #d93064 / white (KPI aside notes) | 4.61 | AA |
| warn-text #b45309 / warning-50 (WIP pill) | 4.61 | AA |
| text-2 / primary-50 (note banner) | 5.98 | AA |
| chart slots vs white (graphics ≥3:1) | c0 4.95 · c1 3.20 · c2 3.21 · c3 3.69 · c4 4.23 · c5 3.39 · c7 3.01 | AA-L |
| — c6 #f5b400 | 1.84 | n/a (dead slot, see §3) |
| text-4 #a3a3ab | — | decorative/disabled only; placeholders use text-3 |

## 9. Visual verification (screenshots/, headless Chrome + Playwright)

Live previews: worktree build on **:8020**, current main build on **:8021** (`frontend/`) for A/B.
Chrome's headless viewport floors at 512px, so ≤768/≤480 tiers were shot with Playwright's real
emulation (`04b-w400.png`).

- `01-default-full.png` (1600): every section, all charts populated with live data.
- `02-default-fold.png`: above-the-fold composition vs reference language.
- `03/04` & `04b`: 700px / 400px tiers — rail hidden, brand in topbar, toggled filters,
  1–2-col KPIs, stacked charts.
- `05–12`: each of the 8 filters applied singly — selects visibly set (e.g. `cust=C&I`,
  `status=Closed` read back from the live page) and every KPI/chart/table re-filtered.
- `13-no-result.png`: empty axes + "No records match these filters" row.
- `14/15`: single month (Feb-2026: prior-period chips visible, `vs. 4,700 · Jan-26`) and
  3-month multi-select (chips vs Oct–Dec-25).
- `00-side-by-side.png`: our 1440 build vs the reference (its own 1440 design frame, downscaled)
  — same rail/topbar/card language and proportions. `00b-side-by-side-939.png` keeps the
  viewport-width-matched full-page variant.

## 10. Open judgment calls

- No scrollspy in the rail (static active state) — noted §5.
- Chart colors stay index-keyed; design.md §10.5 (category-order stability bug) is documented
  there and intentionally not touched in a restyle pass.
- c6 yellow left non-AA (dead slot); documented, not darkened.
- Chart animation disabled (§6) — a behavior-visible but purely presentational change; revert
  by deleting one line if the team wants entrance motion back.
- Trend chips: implemented (§6 Elevate pass) with the contiguous-block prior-period rule; hidden
  rather than invented when no comparable prior period exists (default all-months view).

## 11. Liquid Glass redesign pass (branch `liquid-glass`, off `trial-1`)

Apple-grade "premium SaaS" reskin per approved prototype
(`Temp/opencode/brainstorm/content/prototype-v2.html`, glass intensity −20%).
Data logic, all 8 filters, month multi-select, Ayana exclusion, chips, no-result and
mobile behavior are untouched — this pass changes tokens, presentational CSS, and one
theme-manager JS addition in `build_dashboard.py`.

### 11.1 Dual theme

- Tokens split: `:root` = light (unchanged palette except `--bg-app:#f5f5f7`),
  `html[data-theme='dark']` overrides ~40 color tokens (`--bg-app:#101014`, text
  `#f5f5f7`/`#b8b8c0`/`#8e8e97`, brightened semantic and chart slots for dark AA/graphics).
- Theme = `localStorage('pe-theme')` else `prefers-color-scheme`; system changes propagate
  while no explicit choice is stored. Toggle button (sun/moon) in toolbar persists choice.
- Theme switch clears the `rgb()` resolution cache, re-derives `COLORS` + `Chart.defaults`
  from the new theme's tokens, and repaints via the normal `refresh()` path — charts stay
  token-fed, no per-theme chart code. `COLORS` became a `let` (was `const`).

### 11.2 Glass material (v2 values)

| token | light | dark |
|---|---|---|
| `--glass` / `--glass-2` | `rgba(255,255,255,.58/.48)` | `rgba(255,255,255,.056/.036)` |
| `--glass-brd` / `--glass-brd-2` | `rgba(0,0,0,.056/.04)` | `rgba(255,255,255,.105/.064)` |
| `--sheen` | white .74→.5 gradient | white .08→.028 gradient |
| `--shadow-card` | 0 1px 2px / 0 10px 30px black + inset sheen | 0 8px 28px black + inset sheen |

Blur 19px saturate(180%) (24px month popover, 14px table header) = tokens
`--blur/--blur-lg/--blur-sm`; floats/insets = `--edge:16px`, lift `--n-lift:-1px`.
All component glass values live in tokens; the glass skin block contains no raw px (§11.4).

### 11.3 Layout / components

- Floating glass rail (inset 16px, radius `--r-lg`), main offset `rail-w + 32`;
  floating sticky glass toolbar (top margin 16), month controls left, theme toggle right.
- Filters card, KPI cards, cards, rank badges, table header, pager, month popover — all glass;
  selects/chips/buttons use `--glass-2` fills + `--glass-brd-2` borders (native option lists
  forced opaque per theme for legibility).
- KPI icon accents per metric (`--k1..--k4`: blue/green/amber/orange) via nth-child, no markup change.
- Zebra + hover rows via `--row-tint`; reduced motion / reduced transparency / more-contrast
  media gates drop blur → solid surfaces.
- Motion: 450ms spring-ish theme cross-fade on body, hover lift −1px; all disabled under
  `prefers-reduced-motion`.

### 11.4 Token discipline (re-scanned)

Same scan as §7, excluding `:root` + `html[data-theme=…]` token scopes (incl. media-wrapped
overrides): **0 hex, 0 raw px** — 102 tokens across both themes (glass literals tokenized;
one intermediate build briefly had 47 raw-px leaks, fixed before commit).

### 11.5 Verification

Playwright (Chrome headless, real worktree build + `data.json`):
- Full regression re-run green: all 8 filters applied+Singly reset (each re-renders KPIs),
  Feb-26 single-month chips appear, `___none___` no-result state, theme toggle persists and
  repaints charts, dark/light/700px/400px shots.
- Computed-style spot-checks after tokenization: rail/KPI `blur(19px) saturate(180%)`,
  rail/topbar top 16px, active nav inset ring resolves with per-theme `--primary-100`.
- Dark AA notes: text-2 `#b8b8c0` ≈ 7.9:1 on `#101014` (AA); chart slots ≥3:1 vs card dark
  surfaces; `--primary` #0a84ff with white bold labels ~4.0:1 — large/bold UI text tier,
  matches Apple system blue precedent (documented; `-600` carries text-on-dark roles at 6+).

### 11.6 Prototype-match round 2 (user A/B feedback)

First build read denser than the prototype; second pass aligned the anatomy:

- **Page order**: `Overview` title + subtitle first, glass toolbar below (sticky through
  scroll). KPI row directly after toolbar; note band after; filters panel after the note.
- **KPI cards**: `--fs-kpi 38px` value, `--h-kpi 192px`, roomy padding, label text-2 600,
  icon = 36px tinted rounded-square (color-mix of per-metric accent `--k1..k4`),
  note text + trend chip share a bottom row (`.kpi .sub`). Grid = 4 columns ≥768.
- **Toolbar**: month pill (calendar glyph + range label + blue `N mo` count chip, opens the
  same popover), `All` quiet chip, expandable search, `N filters on` chip (green count badge,
  tap scrolls to filters), glass `Reset`, gold toggle knob (dark → slides right, light → left).
  Active month pill stays glass; accent lives only in the count chip.
- **Note band**: neutral glass strip with amber ⚠ glyph (was blue primary-50 box).
- **Rail**: gradient squircle brand mark (`--mark` + glow), 256px width, 48px nav rows with
  icon chips (`--chip-bg`), blue active chip.
- **Mojibake fix**: chip arrows ▲/▼ (and ≤ § · × ÷) were double-encoded on disk by an earlier
  PowerShell rewrite — restored; chips render proper glyphs.
- All new sizes tokenized (`--icon-badge/r/pad`, `--nav-s`, `--mark-s`, `--knob*`,
  `--h-nav-lg`, `--fs-nav`); scan still 0 raw px/hex (127 tokens).
- Verified: regression (8 filters, chips, no-result, March note, popover, `f-on` count, knob
  slide, light/dark/700/400 shots) + computed-style checks; no JS page errors.



### 11.7 Prototype v2 exact match (round 3)

Round 3 matches the approved prototype served live at :64734 byte-for-byte on
layout metrics. Spec = `brainstorm/content/prototype-v2.html`. User-confirmed
decisions: All+search fold into the month popover; filters = floating glass
panel; rail icons = literal plain squares (no glyphs); system-ui font.

- **Type**: h1 21px/800 (−.022em), sub 12px text-2, body system-ui (Inter dropped,
  no webfont), canvas chart fonts switched too.
- **Rail**: 216px, nav rows 12.5px/500 (8×10 pad, 9px radius), `--nav-ic` 16px
  currentColor squares (.5 / 1 active), active row = primary 16% bg + 28% inset
  ring, label 9.5px, brand name 13px, logo = repo `favicon.png` (30px, rounded).
- **Toolbar**: shared tool pill scale `--tool-fs 12px` @600, 7×12 pad; month chip
  5/10 radius 6 primary-50 + 26% inset ring; filters chip green `on` badge same
  size; knob flipped to prototype logic (dark = left gold, light = right blue
  `--knob-light`), knob 52×30 r15, grip 23px.
- **All + search**: removed from toolbar, live inside the month popover
  (search always-open, full width; popover keeps its own `All` chip).
- **KPI cards**: value 27px/800 (−.032em) 8/4 margins, label 11.5px, badge
  26px r8 (glyph = badge−2×6 pad), sub row 11px text-3 inline with chip
  (10.5px/700, 2×7, r7), card pad 16/16/12, no fixed height, grid gap 12,
  `.kpi-top` flex-start.
- **Note removed**: `#march-note` + JS month toggle + `.note-box` CSS deleted
  (user instruction overrides the prototype's one-liner).
- **Filters**: panel pulled from flow, `position:fixed` glass card under the
  toolbar (`--fpanel-w 880px`, `--fpanel-vacant 180px`), `display:none` until
  the `N filters on` chip toggles `.show` + aria-expanded; ESC and outside-click
  (in the existing popover `mousedown` gate) close it; 400px = full-width sheet.
  `filterToggle` button, its JS and CSS deleted.
- **Rhythm (desktop ≥48em)**: main frame 16px (left = rail + 32), `.page` pad 0
  (bottom 16), pagehead 4/8/12 + toolbar inset 16 both sides + 12px toolbar→KPIs
  gap, section titles 12/8, grid gap 12.
- **Deviations (all ≤2px or token-scale)**: brand pad 8/12/16 vs 6/10/14;
  mo-chip uses `--primary-50`/`--primary` tokens (identical dark, solid tint in
  light); KPI badge tint 15% vs prototype 16%; KPI sub keeps real computed
  note strings (mock's "▲ 98.7% vs Oct–Dec 25" is mock data); charts grid
  unchanged (real data, layout per existing hero/stat cards).
- **Mojibake**: python scan — none; ▲/▼/⇧ intact; ⚠ gone with the note.
- Scan: 0 raw px/hex violations, 147 tokens. Regression `pwglass2.js` green.

### 11.8 Hero photo background (round 4)
- Source: user-provided "Solar Energy Dashboard Landscape.png" (18 MB) → downscale
  1920w JPEG q82 (162 KB) → base64 → `hero_b64.txt`, embedded via `__HERO_BG__`
  (favicon pattern).
- `body{background:var(--hero-scrim),var(--hero-photo) var(--bg-app)}` — photo
  token root-only (`url(...) center/cover no-repeat fixed`), veil per theme:
  dark = rgba(11,13,17,.58→.80), light = rgba(246,249,252,.66→rgba(238,243,250,.80)).
- Rail + solid-surface fallbacks untouched; topbar/filters/popover glass already
  blur the photo. Verified: suite 40/40 (block H), scan 0 (149 tokens).
