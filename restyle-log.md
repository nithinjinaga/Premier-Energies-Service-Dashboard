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

## 7. Token discipline check (machine-verified)

Python scan of the generated `index.html` `<style>` block: after stripping comments and
excluding `:root{}` token blocks (including the per-breakpoint token *overrides*, which only
redefine tokens), there are **zero `#hex` literals and zero raw `px` values** in the remaining
CSS. JS contains no raw color hex either. 78 tokens defined in `:root`.

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
- `14/15`: single month (Mar-2026: Ayana note visible, KPI scope narrows) and 3-month multi-select.
- `00-side-by-side.png`: our 1440 build vs the reference (its own 1440 design frame, downscaled)
  — same rail/topbar/card language and proportions.

## 10. Open judgment calls

- No scrollspy in the rail (static active state) — noted §5.
- Chart colors stay index-keyed; design.md §10.5 (category-order stability bug) is documented
  there and intentionally not touched in a restyle pass.
- c6 yellow left non-AA (dead slot); documented, not darkened.
- Chart animation disabled (§6) — a behavior-visible but purely presentational change; revert
  by deleting one line if the team wants entrance motion back.
- Reference's trend chips (±15.5% green/red pills) are Phase-2 (needs prior-period math); not in
  scope, so KPI notes carry the semantic color instead.
