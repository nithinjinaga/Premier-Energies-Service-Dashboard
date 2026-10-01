# design.md — Visual Specification

Premier Energies · After Sales Service Dashboard — SaaS redesign

---

## 0. Source & confidence

| Source | File (on `main`) | Role |
|---|---|---|
| Shopeers dashboard (Figma frame `15:5`) | `design reference/Shopeers dashboard — editable.png` (1878×1284) | **Primary reference** — layout, sidebar, cards, colours, type |
| Dashboard Overview | `design reference/dashboard-overview.png` (2880×2124) | Secondary — sidebar section labels, progress-bar list, segmented toggle, status pills |
| Vesta Investment | `design reference/investment-dashboard.png` (2880×1950) | Secondary — tabs, KPI row of 5, legend-in-header chart |

**How values were obtained.** The Figma API was rate-limited (Starter plan), so nothing here came from Figma's
inspect data. Every value was extracted from the exported PNGs:

- **Colours** — sampled pixel values (dominant colour per region). Tag: **[Measured]**. Anti-aliasing can shift a
  hex by 1–3 units; flat fills (backgrounds, buttons, chips) are reliable.
- **Sizes** — measured in PNG pixels, then converted to CSS px with an assumed scale factor of **÷1.3**
  (PNG 1878 px wide ≈ 1440 px design viewport). Tag: **[Estimated]**. The scale factor itself is a **guess** —
  it is chosen because a 316 px sidebar and 34 px page title are oversized for a 1× SaaS UI. All CSS values are
  rounded to a 4 px grid, which is a design decision, not a measurement.
- **Font family** — not identifiable from pixels with certainty. **[Guessing]**

> **Italic text in the Shopeers PNG**: every string in the export is rendered italic, including numbers and table
> cells. That is almost certainly a font-substitution artefact of the "editable" export (a missing font replaced by
> an italic face), not a design intent. **[Likely]** This spec uses **upright** text.

---

## 1. Design tokens

### 1.1 Colours

```css
:root{
  /* Surfaces */
  --bg-app:        #f5f7f9;  /* page canvas behind cards            [Measured] */
  --bg-surface:    #ffffff;  /* cards, sidebar, top bar             [Measured] */
  --bg-subtle:     #fafafc;  /* search field, icon buttons          [Measured] */
  --bg-muted:      #eeeef0;  /* inactive bars, skeletons            [Measured] */
  --bg-frame:      #e7eaee;  /* outer frame gutter (optional)       [Measured] */

  /* Borders */
  --border:        #eeeef1;  /* card border, sidebar/topbar divider, table row divider [Measured] */
  --border-strong: #e2e3e6;  /* inputs, secondary buttons           [Estimated] */
  --grid:          #f1f3f6;  /* chart gridlines                     [Measured] */

  /* Text */
  --text-1:        #191b1e;  /* headings, values, nav labels        [Measured] */
  --text-2:        #5b5d62;  /* table body text                     [Measured] */
  --text-3:        #85858f;  /* labels, table headers, axis ticks, "vs last period" [Measured] */
  --text-4:        #a3a3ab;  /* placeholders, disabled              [Measured] */

  /* Brand / primary */
  --primary:       #2861ff;  /* Export button, active nav text, chart line, icons [Measured] */
  --primary-600:   #1f4fe0;  /* hover (derived, -10% L)             [Estimated] */
  --primary-50:    #eff4ff;  /* active nav background               [Measured] */
  --primary-25:    #f4f7ff;  /* area-chart fill end                 [Measured] */
  --primary-bar:   #4e7cff;  /* highlighted bar                     [Measured] */

  /* Semantic */
  --success:       #43ba8b;  /* up-trend text                       [Measured] */
  --success-50:    #eaf8f1;  /* up-trend chip bg, count badge bg    [Measured] */
  --success-strong:#3aa583;  /* positive money value in table       [Measured] */
  --danger:        #eb4776;  /* down-trend text                     [Measured] */
  --danger-50:     #fceaf0;  /* down-trend chip bg                  [Measured] */
  --warning:       #ff8a3d;  /* accent orange (bar stroke)          [Estimated — measured tint #ffac76] */
  --warning-50:    #fff3ea;  /*                                     [Estimated] */
  --gauge-on:      #42c78b;  /* gauge filled ticks                  [Measured] */
  --gauge-off:     #d2d3d6;  /* gauge empty ticks                   [Measured] */

  /* Overlay */
  --tooltip-bg:    #191b1e;
  --focus-ring:    0 0 0 3px rgba(40,97,255,.25);
}
```

**Premier brand note.** The current dashboard primary is Apple blue `#0071e3`. Shopeers primary `#2861ff` is close in
hue; switching is low-risk. If Premier Energies has a brand colour guideline, substitute it for `--primary` and
re-derive `-50 / -25` tints — the rest of the palette is neutral and survives the swap.

### 1.2 Chart palette (categorical, 8 slots)

The data has up to 8 defect categories, so 8 distinguishable hues are required. Shopeers shows only 3 (blue / green /
orange); the rest are extended in the same saturation band. **[Estimated]**

| Slot | Hex | Used for (default order = `CAT_ORDER`) |
|---|---|---|
| 0 | `#2861ff` | Junction Box Defects |
| 1 | `#ff8a3d` | Ribbon Soldering Issue |
| 2 | `#43ba8b` | Cell and Module Defects |
| 3 | `#eb4776` | Physical and External Damage |
| 4 | `#8b5cf6` | Transit Damage |
| 5 | `#14b8c4` | Aesthetic |
| 6 | `#f5b400` | No Issue (normally excluded) |
| 7 | `#94949d` | Inspection |

Rule: **semantic colours (success / danger) must not be reused for neutral categories in the same chart** where a
red/green reading could be mistaken for good/bad. Slot 2 (green) and 3 (pink) are acceptable in category charts
because those charts carry no good/bad meaning — but never use them in Closed-vs-WIP charts (see §10).

### 1.3 Typography

**Family:** `Inter` (Google Fonts, weights 400/500/600/700), fallback
`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`. The reference glyphs (single-storey `a` absent,
open apertures, tabular-looking numerals) are consistent with Inter. **[Guessing]**

Enable tabular numbers on every numeric element: `font-variant-numeric: tabular-nums;`

| Token | Use | PNG px (cap-based) | CSS size / line-height | Weight | Colour |
|---|---|---|---|---|---|
| `--fs-display` | Hero number in Top-3 card ("$446.7K" slot) | ~46 | 36 / 44 | 700 | text-1 |
| `--fs-h1` | Page title ("Dashboard") | ~34 | 26 / 32 | 700 | text-1 |
| `--fs-kpi` | KPI value | ~40 | 30 / 36 | 700 | text-1 |
| `--fs-h2` | Card title ("Total Profit") | ~21 | 16 / 24 | 600 | text-1 |
| `--fs-h3` | KPI label ("Page Views"), sub-card title | ~20 | 15 / 22 | 500 | text-1 |
| `--fs-body` | Nav items, table cells, buttons | ~17 | 14 / 20 | 500 (nav, buttons) / 400 (cells) | text-1 / text-2 |
| `--fs-small` | Hints, "vs last period", axis ticks, sub-nav | ~14 | 12 / 16 | 400 | text-3 |
| `--fs-micro` | Table header, section label (MENU / TEAMS) | ~13 | 11 / 16, `letter-spacing:.04em`, UPPERCASE | 500 | text-3 |
| `--fs-chip` | Trend chip, count badge | ~15 | 12 / 16 | 600 | semantic |

Letter-spacing: `-0.02em` on display / h1 / kpi; `0` elsewhere.

### 1.4 Spacing scale (4 px base)

`--s-1:4px  --s-2:8px  --s-3:12px  --s-4:16px  --s-5:20px  --s-6:24px  --s-8:32px  --s-10:40px`

| Measurement | PNG px | CSS |
|---|---|---|
| Content padding (sidebar edge → first card) | 42–44 | 32 |
| Gap between KPI cards | 32 | 24 |
| Gap between rows / columns of cards | 30–42 | 24 |
| Card inner padding | 30–34 | 24 |
| KPI label → value | ~30 | 16 |
| KPI value → "vs" line | ~40 | 20 |
| Nav item vertical pitch | 58 | 44 (height) + 0 gap |
| Sidebar horizontal padding | 12 (to active bg) / 30 (to icon) | 12 / 20 |
| Icon → label in nav | 14 | 12 |

### 1.5 Radius

| Token | PNG px | CSS | Used on |
|---|---|---|---|
| `--r-xl` | ~26–28 | 20 | Cards (KPI + content) |
| `--r-lg` | ~16 | 12 | Inner sub-card (Customers strip), popovers |
| `--r-md` | ~12 | 10 | Nav items, inputs, secondary buttons, table thumbnails |
| `--r-sm` | ~8 | 6 | Trend chips, heatmap cells, bars (`borderRadius` 6) |
| `--r-pill` | full | 999 | Export button, search field, date pill, count badge, status pills, icon buttons (circle) |

### 1.6 Shadows / elevation

The reference is **flat**: cards separate from the canvas by a 1 px `--border` plus the `#f5f7f9` canvas contrast. No
visible drop shadow on resting cards. **[Measured — no shadow pixels found around KPI cards]**

```css
--shadow-0: none;                                             /* resting card */
--shadow-1: 0 1px 2px rgba(16,24,40,.04);                     /* inputs, pills */
--shadow-2: 0 4px 16px rgba(16,24,40,.06);                    /* card hover */
--shadow-3: 0 12px 32px rgba(16,24,40,.12);                   /* popovers, dropdowns, drawer */
```
`--shadow-2/3` are not in the reference (static image can't show hover) — **[Estimated]**.

---

## 2. Layout

### 2.1 App shell (desktop ≥ 1280 px)

```
┌───────────────┬──────────────────────────────────────────────────────────────┐
│ Sidebar 240   │ Top bar 64  (search ........................ icon btns)      │
│ (fixed,       ├──────────────────────────────────────────────────────────────┤
│  full height) │ Page header 56: Title ....... [date pill|range ▾] [Filters] [Export] │
│               │ Filter bar (collapsible)                                     │
│               │ KPI row: 4 × equal cards                                     │
│               │ Content grid: 12 col, gap 24                                 │
│               │   ┌──────────── 8 col ────────────┐ ┌──── 4 col ────┐        │
│               │   │ Top-3 hero card               │ │ Closure gauge │        │
│               │   └───────────────────────────────┘ └───────────────┘        │
│               │   ...                                                        │
└───────────────┴──────────────────────────────────────────────────────────────┘
```

- **Sidebar**: `position:fixed; left:0; top:0; bottom:0; width:240px; background:#fff; border-right:1px solid var(--border)`.
- **Main**: `margin-left:240px; background:var(--bg-app); min-height:100vh`.
- **Content container**: `padding:24px 32px 40px; max-width:1600px` (left-aligned, not centred — reference keeps
  content flush to the sidebar). [Estimated]
- **Grid**: `display:grid; grid-template-columns:repeat(12,minmax(0,1fr)); gap:24px`.
- Main/side column ratio in reference: 878 : 524 px ≈ **8 : 4** (≈ 63 / 37). [Measured]

### 2.2 Section anchors

Each logical group from the current page becomes a section with `id` and `scroll-margin-top:80px` (top bar + 16) so
sidebar jump-links land below the sticky top bar.

---

## 3. Navigation

### 3.1 Sidebar

| Part | Spec |
|---|---|
| Logo block | height 64 (aligned to top bar), padding 0 20, logo image 28 px tall + wordmark text 18/600 OR existing Premier header PNG at 28 px height. Collapse button right: 28×28 icon button, icon 18, colour text-3. Bottom border 1 px `--border`. |
| Section label | `--fs-micro`, text-3, padding 20 20 8 (from Overview ref: MENU / TEAMS / HELP) |
| Nav item | height 44, padding 0 12, margin 0 12, radius 10, gap 12, icon 20 px stroke 1.75 colour text-1, label `--fs-body` 500 text-1 |
| Nav item – hover | bg `--bg-subtle`, 150 ms |
| Nav item – active | bg `--primary-50`, icon + label `--primary`, weight 600 [Measured] |
| Count badge | right-aligned, height 22, padding 0 8, radius pill, bg `--success-50`, text `--success` 12/600 (ref "46") |
| Group (collapsible) | chevron 16 px right; children indented 48 px with a 1 px `--border` vertical guide line at x=28 (ref "Finances") |
| Divider | 1 px `--border`, margin 12 |
| Footer block | pinned to bottom (`margin-top:auto`), items same as nav |

**Proposed nav content (single-page → jump links):**

| Icon (Lucide name) | Label | Target |
|---|---|---|
| `layout-dashboard` | Overview | `#sec-overview` (KPIs + Top 3 + closure) |
| `alert-triangle` | Defect Breakdown | `#sec-defects` |
| `users` | Segments | `#sec-segments` |
| `map-pin` | Geography & TAT | `#sec-geo` |
| `factory` | Production | `#sec-production` |
| `trending-up` | Volume & Trend | `#sec-trend` |
| `table` | Module Records | `#sec-records` — badge = record count |
| *(footer)* `calendar` | Data through **Aug-26** | static info, not a link |
| *(footer)* `help-circle` | How to read this | optional: opens existing "note" content |

No Orders / Products / Settings / user-avatar items — they would be dead links.

### 3.2 Top bar

| Part | Spec |
|---|---|
| Container | height 64, bg #fff, bottom border 1 px `--border`, padding 0 32, `position:sticky; top:0; z-index:40` |
| Search field | width 340 (PNG 338→ 260–340), height 40, radius pill, bg `--bg-subtle`, border 1 px `--border`, icon 18 text-3 at left 14, placeholder text-4 `--fs-body` 400, right hint chip "⌘K" 11/500 text-3 |
| Icon buttons (right) | 40×40 circle, bg `--bg-subtle`, border 1 px `--border`, icon 20 text-1. Reference has theme / bell / avatar — **omit** unless a real function exists. |

### 3.3 Page header row

- Title left: `--fs-h1`, text-1. Subtitle under it (optional): "Field service & module defect tracking", `--fs-small`
  text-3.
- Right cluster, gap 12, height 40 each:
  - **Date/range pill (split button)**: bg #fff, border 1 px `--border`, radius pill. Left segment: calendar icon 18 +
    label "Dec 2024 – Aug 2026" (`--fs-body` 500). 1 px divider. Right segment: "All months ▾".
  - **Filters button** (secondary): icon `sliders-horizontal` + "Filters" + active-count badge (primary-50 bg,
    primary text) when any filter ≠ All.
  - **Export button** (primary): bg `--primary`, text #fff 14/600, icon `download` 18, padding 0 20, radius pill.
    [Measured colour]

---

## 4. Buttons

| Variant | Default | Hover | Active (pressed) | Focus-visible | Disabled |
|---|---|---|---|---|---|
| Primary | bg primary, #fff | bg primary-600 | `transform:scale(.98)` | focus-ring | opacity .45, cursor not-allowed |
| Secondary | bg #fff, border `--border-strong`, text-1 | bg bg-subtle | scale .98 | focus-ring | opacity .45 |
| Ghost / icon | transparent, text-3 | bg bg-subtle, text-1 | — | focus-ring | opacity .45 |
| Toggle (segmented, from Overview ref) | container bg bg-subtle radius 10 padding 4; option 32 h radius 8 text-3 | text-1 | selected: bg #fff, text-1 600, shadow-1 | focus-ring | — |
| Chip (month chip in picker) | bg bg-subtle, border `--border`, radius 10, 36 h | border primary | selected: bg primary, #fff | focus-ring | — |

Sizes: `sm` 32 h / 12 px text, `md` 40 h / 14 px, `lg` 44 h / 15 px. Icon-to-label gap 8.

---

## 5. Forms

| Element | Spec |
|---|---|
| Select (filter) | height 40, radius 10, bg #fff, border 1 px `--border-strong`, padding 0 36 0 12, text `--fs-body` 500 text-1, custom chevron 16 at right 12 (`appearance:none`) |
| Select label | `--fs-micro` text-3, margin-bottom 6 |
| Select – active value ≠ All | border primary, bg primary-50/40, text primary — makes applied filters visible at a glance |
| Text input (search) | as §3.2 |
| Number input (pager jump) | 32 h, width 56, radius 8, centred |
| Focus | border primary + focus-ring, no default outline |
| Filter bar container | card (`--r-xl`, border, padding 16 24), grid `repeat(4,1fr)` gap 12 16; footer row right-aligned: "Reset filters" ghost button + active-filter count |
| Applied-filter chips (optional) | under header: pill 28 h, bg primary-50, text primary 12/600, × icon 14 |

---

## 6. Cards

### 6.1 KPI card (reference: "Page Views")

| Property | Value |
|---|---|
| Size | fluid (¼ of row), min-height 128 (PNG 168) |
| Padding | 24 |
| Bg / border / radius | #fff / 1 px `--border` / 20 |
| Row 1 | label `--fs-h3` 500 text-1 left; icon 22 px `--primary` right (eye/users/pointer/inbox in ref) |
| Row 2 (margin-top 16) | value `--fs-kpi` 700 + trend chip, gap 12, baseline-aligned |
| Trend chip | height 24, padding 0 8, radius 6, 12/600, ▲/▼ glyph 8 px; up = success on success-50, down = danger on danger-50 |
| Row 3 (margin-top 20) | `--fs-small` text-3 ("vs. 14,653 last period") |
| Hover | border `--border-strong`, shadow-2, 200 ms |

**Mapping to Premier KPIs** (icons from Lucide):

| Card | Icon | Value | Chip (Phase 2) | Row 3 |
|---|---|---|---|---|
| Modules Serviced (Closed) | `check-circle-2` | `k-closed` | Δ% vs previous equal-length period | single-month label or "Selected period" |
| Closure Rate | `percent` | `k-closure` | Δ **pp** (percentage points) | "x closed of y" |
| Avg TAT (days) | `timer` | `k-tat` | Δ days — **inverted polarity**: decrease = green | "Within / Exceeds 30-day SOP" coloured |
| Open (WIP) | `inbox` | `k-wip` | Δ count — **inverted polarity** | "n modules still open" |

Phase 1 (no new logic): chip slot shows the existing status text (e.g. "Within SOP") as a semantic chip; Row 3 shows the
existing note.

### 6.2 Content card (reference: "Total Profit", "Most Day Active")

| Property | Value |
|---|---|
| Padding | 28 24 24 (PNG 34/30) |
| Header | title `--fs-h2` 600 text-1 left; right: overflow "•••" ghost icon button 32×32 (ref) or segmented toggle / legend |
| Hint | `--fs-small` text-3, margin-top 4 (keep current hint copy — it carries business meaning) |
| Header → body | 20 |
| Chart box height | 280 default, 320 tall (current 300/340 — slightly reduced to absorb the extra padding) |

### 6.3 Hero card (reference: "Total Profit" layout)

Two-column inside the card: left 30 % = big number + chip + caption; right 70 % = chart. Below, an inset
sub-card ("Customers" strip): radius 12, border 1 px `--border`, padding 20 24, 3 equal columns each with
a coloured left rule (2 px, full height) and a 6 px coloured bar along the bottom — colours primary / success /
warning in ref. [Measured]

**Premier mapping:** Top-3 Problems. Big number = total defects of the #1 sub-category; chip = its share of all
defects; chart = existing `chTop3`. The 3-column strip replaces the current coloured badges: rank, sub-category
name, count, bar coloured with chart slot 0/1/2 so the legend and the series match.

### 6.4 Gauge card (reference: "Repeat Customer Rate")

Semicircle, 32 radial ticks, filled ticks `--gauge-on`, empty `--gauge-off`; centre value `--fs-display`, caption
"On track for 80% target" `--fs-small` text-3; secondary button "Show details" (sm, centred).

**Premier mapping:** Closure Rate vs **90 % target** (the 90 % threshold already exists in the code's colour logic).
Chart.js doughnut with `circumference:180, rotation:-90` reproduces the arc; ticked style needs a small plugin or a
dashed `borderDash`-segment trick — Phase 2, a solid arc is acceptable in Phase 1.

### 6.5 Progress-list card (from Overview ref "Top Products")

Row: name 15/600 text-1 + subline 13 text-3 left, value 15/700 right; 8 px bar under, radius pill, track `--bg-muted`,
fill colour. Row gap 20. Candidate use: **Top States by Defects** (10 rows) instead of a horizontal bar chart — more
readable, no axis needed.

---

## 7. Tables (reference: "Best Selling Products")

| Part | Spec |
|---|---|
| Container | inside card; table bar above: count left (`--fs-small` text-3), search right (as §3.2, width 280) |
| Header row | no fill (ref) — height 40, `--fs-micro` text-3 UPPERCASE, bottom border 1 px `--border`. Sort indicator ↑/↓ 12 px after label on sorted column, text-1 on sorted column |
| Body row | height 56 (PNG 88 ⇒ 68 — reduced to 56 for density, 9 columns × 50 rows) |
| Cell | padding 0 16, `--fs-body` 400 text-2; first column (Month) 500 text-1 |
| Row divider | 1 px **dashed** `--border` (ref uses dashed) |
| Row hover | bg `#fafbfc` |
| Status pill | height 24, padding 0 10, radius pill, 12/600. Closed = success on success-50; WIP = `#c26a00` on warning-50; (Overview ref "Processing" = primary on primary-50 if another status appears) |
| Serial / Complaint No. | `font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size:13px` — IDs scan faster in mono |
| Sticky header | keep `position:sticky; top:0`, bg #fff |
| Pager | right-aligned, 32 h controls: "Page 1 of 40" text-3, jump input, Prev/Next secondary sm buttons |
| Empty state | centred icon `search-x` 32 text-4 + "No records match these filters" 14/500 text-2 + "Reset filters" ghost button |

### 7.1 Heatmap (table-based)

Cells 40 h min-width 56, radius 6, gap 4. Scale from `#eff4ff` (low) to `#2861ff` (high) — i.e. primary tints
instead of current `#3266ad`. Text flips to #fff above 55 % intensity (keep current rule). Empty cell `--bg-app`.
Row labels 13/600 text-1 right-aligned; column labels 12/500 text-3, wrapped, bottom-aligned.

---

## 8. Charts (Chart.js 4 global defaults)

| Property | Value |
|---|---|
| Font | Inter 12, colour text-3 |
| Gridlines | y only, `--grid`, `drawBorder:false`, dashed `[4,4]` (ref shows dashed) |
| X axis | no grid, ticks text-3, `maxRotation:0`, autoSkip on time axes |
| Legend | top-right in card header, `usePointStyle:true, pointStyle:'circle', boxWidth:8`, 12 text-2 |
| Tooltip | bg `--tooltip-bg`, radius 8, padding 10 12, title 12/500 #fff at 70 %, body 13/600 #fff, no caret border, `displayColors` dot style circle |
| Line | width 2.5, tension .35, points hidden (`radius:0`), `hoverRadius:5` with white 2 px border |
| Area fill | vertical gradient `rgba(40,97,255,.18)` → `rgba(40,97,255,0)` (ref Total Profit) |
| Comparison / target line | 1.5 px dashed `[6,4]` `#c7c9ce` (ref dashed "previous period") — use for 30-day SOP line (keep red only if SOP breach must be alarming: `--danger` at 60 %) |
| Bars | `borderRadius:6`, `borderSkipped:false`, `maxBarThickness:40`, `categoryPercentage:.7` |
| Highlight bar pattern (ref "Most Day Active") | all bars `--bg-muted`, max bar `--primary-bar`, value label above max bar 13/600 text-1 — use for **Defects by Category** and **Customer Type** |
| Donut | `cutout:'72%'`, `borderWidth:0`, `spacing:2`, centre label (total) via plugin, legend right ≥ 768 / bottom < 768 |
| Stacked bars | `borderRadius:4` on top dataset only; gap 0 between stacks |
| Animation | see plan.md §7 |

---

## 9. States

| State | Treatment |
|---|---|
| Loading (initial) | Keep logo-fill loader but restyle: bg `--bg-app`, logo 64, progress bar 160×4 radius pill primary below, % text-3 12 |
| Loading (cards, optional) | skeleton blocks `--bg-muted` with shimmer 1.2 s; only if refresh becomes async later |
| Empty chart | centred `--fs-small` text-3 "No defects for this selection" inside chart box |
| Error | card with `alert-circle` danger 24, message 14 text-1, "Retry" secondary button (reloads) |
| Hover | cards: border-strong + shadow-2; rows: bg; buttons: per §4 |
| Focus-visible | `--focus-ring` on every interactive element; never remove outline without replacement |
| Active filter | select gets primary border/bg (§5) + count badge on Filters button |
| Selected month(s) | date pill label changes; calendar chip `.sel` = primary |
| Disabled | opacity .45, `cursor:not-allowed` |
| Note banner (March Ayana block) | info alert: bg primary-50, border 1 px `#d6e2ff`, icon `info` primary, text 13 text-2, radius 12 |

---

## 10. Semantic rules specific to this dashboard

1. **Closed = success green, WIP = warning orange** everywhere (KPI, status pill, Closed-vs-WIP chart, status donut).
   Currently Closed is blue `#3266ad` in charts but green in pills — inconsistent.
2. **Lower-is-better metrics** (Avg TAT, Open WIP): a decrease renders green ▼, an increase red ▲.
3. **Closure Rate thresholds** stay: ≥ 90 % success, ≥ 70 % warning, else danger.
4. **TAT threshold** stays: ≤ 30 days success, else danger.
5. Category colours are fixed by category name (not by sort position), so "Transit Damage" is the same colour in
   every chart. The current code assigns colours by index after filtering, which can shift colours when a category
   drops out — flagged in plan.md.

---

## 11. Responsive behaviour

| Breakpoint | Sidebar | Top bar | KPI grid | Content grid | Charts | Table |
|---|---|---|---|---|---|---|
| ≥ 1440 | 240 expanded | full search 340 | 4 col | 8/4 and 6/6 rows | 280 / 320 h | full |
| 1280–1439 | 240 | search 280 | 4 col | same | same | full |
| 1024–1279 | **72 px icon rail** (labels hidden, tooltips on hover) | search 240 | 4 col | 8/4 → stays; 6/6 stays | 260 / 300 | horizontal scroll if needed |
| 768–1023 | **off-canvas drawer** 280 w, opened by hamburger in top bar, scrim `rgba(16,24,40,.4)` | hamburger + search icon (expands) | 2 col | all cards 12 col | 260 / 280 | h-scroll, sticky first column |
| 480–767 | drawer | hamburger, title, search icon | 2 col, KPI value 24 | 12 col | 240 / 260, donut legend bottom | h-scroll |
| < 480 | drawer | as above | 1 col | 12 col | 220 / 240 | h-scroll; hide Sub-category & Plant columns |

Page header at < 768: title on its own line; right cluster wraps to full-width row, Export becomes icon-only 40×40.
Filter bar at < 768: hidden behind the Filters button → bottom sheet (full width, max-height 80vh, radius 20 20 0 0,
selects 1 col 44 h for touch). Content padding: 32 → 24 (≤1023) → 16 (≤767) → 12 (≤479).

Touch targets ≥ 44×44 below 1024 px.

---

## 12. Component dimension summary (CSS px)

| Component | W × H | Radius |
|---|---|---|
| Sidebar | 240 × 100vh (rail 72) | 0 |
| Top bar | fluid × 64 | 0 |
| Nav item | 216 × 44 | 10 |
| Search field | 340 × 40 | pill |
| Icon button | 40 × 40 | pill |
| Primary / secondary button md | auto × 40 | pill (header) / 10 (in-card) |
| Date pill | auto × 40 | pill |
| KPI card | ¼ row × ≥128 | 20 |
| Content card | grid span × auto | 20 |
| Trend chip | auto × 24 | 6 |
| Count badge | auto × 22 | pill |
| Status pill | auto × 24 | pill |
| Filter select | fluid × 40 (44 touch) | 10 |
| Month popover | 340 × auto | 12 |
| Table row | fluid × 56 | 0 |
| Heatmap cell | ≥56 × 40 | 6 |
| Chart box | fluid × 280 / 320 | — |
| Tooltip | auto, padding 10 12 | 8 |
