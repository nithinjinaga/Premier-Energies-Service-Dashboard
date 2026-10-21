#!/usr/bin/env python3
"""
Premier Energies After-Sales Dashboard — Builder

HOW TO USE:
1. Run ingest.py first to produce data.db
2. Then run this script: python build_dashboard.py
3. Outputs ../frontend/index.html (dashboard UI) — data.db is fetched at runtime

TO ADD A NEW MONTH:
- Update the MONTHS and MLABEL constants in the HTML template below (search for const MONTHS)
- The data itself comes from ingest.py, not this file

INSTALL REQUIREMENT:
No extra packages needed beyond standard Python
"""

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

with open(os.path.join(BASE_DIR, "favicon_b64.txt"), encoding="utf-8") as f:
    favicon_b64 = f.read().strip()
with open(os.path.join(BASE_DIR, "hero_b64.txt"), encoding="utf-8") as f:
    hero_b64 = f.read().strip()

with open(os.path.join(BASE_DIR, "header_b64.txt"), encoding="utf-8") as f:
    header_b64 = f.read().strip()

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard 2026</title>
<link rel="icon" type="image/png" href="data:image/png;base64,__FAVICON__">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/sql.js@1.10.3/dist/sql-wasm.min.js"></script>
<style>
/* ==========================================================================
   Design tokens — sampled from design reference/Shopeers dashboard — editable.png
   Scale: PNG 1878px = 1440px design viewport (÷1.3). See restyle-log.md.
   ========================================================================== */
:root{
  /* surfaces — light theme */
  --bg-app:#f5f5f7;
  --bg-surface:#ffffff;
  --bg-subtle:#fafafc;
  --bg-muted:#eeeef0;
  /* glass material (Liquid Glass v2, dark-canvas intensity) */
  --glass:rgba(255,255,255,.58);
  --glass-2:rgba(255,255,255,.48);
  --glass-brd:rgba(0,0,0,.056);
  --glass-brd-2:rgba(0,0,0,.04);
  --sheen:linear-gradient(180deg,rgba(255,255,255,.74),rgba(255,255,255,.5));
  --shadow-card:0 1px 2px rgba(0,0,0,.05),0 10px 30px rgba(0,0,0,.07),inset 0 1px 0 rgba(255,255,255,.7);
  --row-tint:rgba(0,0,0,.02);
  /* borders */
  --border:#eeeef1;
  --border-strong:#e2e3e6;
  --grid:rgba(0,0,0,.05);
  /* text */
  --text-1:#191b1e;
  --text-2:#5b5d62;
  --text-3:#6e7076; /* sampled #85858f = 3.65:1 on white, AA fail — darkened, hue kept */
  --text-4:#a3a3ab; /* decorative/disabled only, never body text */
  /* brand */
  --primary:#2861ff;
  --primary-600:#1f4fe0;
  --primary-50:#eff4ff;
  --primary-100:#d6e2ff;
  --primary-bar:#4e7cff;
  /* semantic — text shades AA-checked; tint bgs as sampled */
  --success:#147a58;   /* sampled #43ba8b fails AA as text (2.2:1 on tint) */
  --success-tone:#2ea276; /* chart fill, ≥3:1 on white */
  --success-50:#eaf8f1;
  --danger:#d93064;    /* sampled #eb4776 fails AA as text on white */
  --danger-50:#fceaf0;
  --warn-text:#b45309; /* sampled orange fails AA as text */
  --warning:#ea6a10;   /* chart fill / accents, ≥3:1 */
  --warning-50:#fff3ea;
  /* misc viz */
  --gauge-on:#42c78b;
  --gauge-off:#d2d3d6;
  --tooltip-bg:#191b1e;
  /* KPI icon slots — per-metric accent (closed/rate/tat/wip) */
  --k1:#0071e3; --k2:#248a3d; --k3:#b25000; --k4:#8a3b12;
  /* 8 chart slots — category order CAT_ORDER; all ≥3:1 vs white except c6 (unused slot, see log) */
  --c0:#2861ff; --c1:#ea6a10; --c2:#2ea276; --c3:#eb4776;
  --c4:#8b5cf6; --c5:#0f9aa5; --c6:#f5b400; --c7:#94949d;
  /* type */
  --font:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  --fs-display:36px; --fs-h1:21px; --fs-kpi:27px; --fs-h2:16px; --fs-h3:15px; --fs-kpi-label:11.5px; --fs-kpi-sub:11px;
  --fs-body:14px; --fs-small:12px; --fs-micro:11px; --fs-chip:10.5px;
  /* spacing (4px scale) */
  --s-1:4px; --s-2:8px; --s-3:12px; --s-4:16px; --s-5:20px;
  --s-6:24px; --s-8:32px; --s-10:40px;
  /* radius */
  --r-xl:20px; --r-lg:12px; --r-md:10px; --r-sm:6px; --r-pill:999px;
  /* elevation — reference is flat; hover shadows estimated (static PNG) */
  --shadow-0:none;
  --shadow-1:0 1px 2px rgba(16,24,40,.04);
  --shadow-2:0 4px 16px rgba(16,24,40,.06);
  --shadow-3:0 12px 32px rgba(16,24,40,.12);
  --focus-ring:0 0 0 3px rgba(40,97,255,.25);
  /* component dims */
  --rail-w:216px;
  --topbar-h:56px;    /* sampled 57px */
  --h-nav:44px;
  --h-kpi:0px;
  --h-chart:280px;
  --h-chart-tall:300px;
  --h-hero:340px;
  --h-table:520px;
  --h-row:56px;
  --h-pill:24px;
  --h-ctl:38px;       /* filter select / reset height */
  --h-btn-sm:36px;
  --h-touch:44px;
  --w-page:1600px;
  --w-fg-min:120px;
  --w-kpi-min:220px;
  --w-g2:440px;
  --w-g3:320px;
  --w-badge-min:200px;
  --w-cell:56px;
  --w-pop:340px;
  --w-search-open:248px;
  --w-search-min:240px;
  --w-jump:56px;
  --logo:96px;        /* loading logo */
  --logo-s:30px;      /* rail/topbar brand mark */
  --bw:1px;
  --bw-2:2px;
  /* glass skin literals */
  --edge:16px; --blur:19px; --blur-sm:14px; --blur-lg:24px; --n-lift:-1px; --ring-inset:inset 0 0 0 1px var(--primary-100);
  /* prototype-match round 2 */
  --chip-bg:rgba(0,0,0,.05); --knob:linear-gradient(135deg,#ffd60a,#ff9f0a); --knob-w:52px; --knob-d:23px;
  --knob-h:30px; --knob-r:15px; --knob-oy:2.5px; --knob-ox:3px; --knob-slide:22px; --knob-light:linear-gradient(135deg,#4f8cff,#0a84ff); --tool-fs:12px; --tool-py:7px; --tool-px:12px; --mchip-py:5px; --mchip-px:10px;
  --mark:linear-gradient(135deg,#4d9bff,#0a84ff); --mark-glow:0 4px 14px rgba(10,132,255,.3);
  --icon-badge:26px; --icon-badge-m:26px; --icon-pad:6px; --icon-pad-m:6px; --icon-r:8px; --chip-r:7px; --chip-px:7px;
  --fs-nav:12.5px; --fs-label:9.5px; --fs-brand:13px; --fs-foot:10px; --nav-py:8px; --nav-px:10px; --nav-r:9px; --nav-ic:16px; --nav-ic-r:5px;
  --knob-shadow:0 2px 8px rgba(0,0,0,.35); --pad-tiny:2px; --fpanel-vacant:180px; --fpanel-w:880px; --hero-photo:url("data:image/jpeg;base64,__HERO_BG__") center/cover no-repeat fixed;
}

/* ---------- base ---------- */
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:var(--font);font-size:var(--fs-body);line-height:1.5;color:var(--text-1);background:var(--hero-photo) var(--bg-app);-webkit-font-smoothing:antialiased;transition:background .45s cubic-bezier(.34,1.3,.64,1),color .45s cubic-bezier(.34,1.3,.64,1)}
button,input,select{font-family:var(--font)}
:focus-visible{outline:none;box-shadow:var(--focus-ring)}
[id^="sec-"]{scroll-margin-top:calc(var(--topbar-h) + var(--s-4))}

/* ---------- left rail ---------- */
.rail{position:fixed;left:0;top:0;bottom:0;width:var(--rail-w);background:var(--bg-surface);border-right:var(--bw) solid var(--border);display:flex;flex-direction:column;z-index:30}
.rail-brand{display:flex;align-items:center;gap:var(--s-3);height:var(--topbar-h);padding:0 var(--s-5);border-bottom:var(--bw) solid var(--border);flex:none}
.rail-logo{width:var(--logo-s);height:var(--logo-s);object-fit:contain;flex:none}
.rail-name{font-size:var(--fs-h3);font-weight:600;letter-spacing:-.01em}
.rail-label{font-size:var(--fs-micro);font-weight:500;color:var(--text-3);text-transform:uppercase;letter-spacing:.04em;padding:var(--s-5) var(--s-5) var(--s-2)}
.rail-nav{display:flex;flex-direction:column;padding:0 var(--s-3)}
.rl{display:flex;align-items:center;gap:var(--s-3);height:var(--h-nav);padding:0 var(--s-3);border-radius:var(--r-md);color:var(--text-1);font-size:var(--fs-body);font-weight:500;text-decoration:none;transition:background .15s}
.rl svg{width:var(--s-5);height:var(--s-5);flex:none;color:var(--text-2)}
.rl:hover{background:var(--bg-subtle)}
.rl.active{background:var(--primary-50);color:var(--primary-600)}
.rl.active svg{color:var(--primary-600)}
.rail-foot{margin-top:auto;padding:var(--s-4) var(--s-5);border-top:var(--bw) solid var(--border)}
.rail-foot-k{font-size:var(--fs-micro);font-weight:500;color:var(--text-3);text-transform:uppercase;letter-spacing:.04em}
.rail-foot-v{font-size:var(--fs-h3);font-weight:600;color:var(--text-1)}

/* ---------- topbar + page canvas ---------- */
.main{margin-left:var(--rail-w);min-height:100vh}
.topbar{position:sticky;top:0;z-index:40;display:flex;align-items:center;justify-content:flex-end;gap:var(--s-3);min-height:var(--topbar-h);padding:0 var(--s-8);background:var(--bg-surface);border-bottom:var(--bw) solid var(--border)}
.topbar-brand{display:none;align-items:center;gap:var(--s-2);font-weight:600;font-size:var(--fs-h3)}
.topbar-brand img{width:var(--logo-s);height:var(--logo-s);object-fit:contain}
.topbar-end{display:flex;align-items:center}
.page{padding:var(--s-6) var(--s-8) var(--s-10);max-width:var(--w-page)}
.pagehead{margin-bottom:var(--s-5)}
.pagehead h1{font-size:var(--fs-h1);font-weight:800;letter-spacing:-.022em;line-height:1.25}
.pagehead .sub{color:var(--text-2);font-size:var(--fs-small);margin-top:var(--s-1)}

/* ---------- note banner (removed in prototype v2 match) ---------- */

/* ---------- filter bar ---------- */
.filters{display:flex;flex-wrap:wrap;gap:var(--s-3) var(--s-4);background:var(--bg-surface);padding:var(--s-4) var(--s-5);border-radius:var(--r-xl);border:var(--bw) solid var(--border);margin-bottom:var(--s-6);align-items:flex-end}
.fg{display:flex;flex-direction:column;gap:var(--s-2);flex:1;min-width:var(--w-fg-min)}
.fg label{font-size:var(--fs-micro);font-weight:500;color:var(--text-3);text-transform:uppercase;letter-spacing:.04em}
.fg select{height:var(--h-ctl);padding:0 var(--s-3);background:var(--bg-surface);color:var(--text-1);border:var(--bw) solid var(--border-strong);border-radius:var(--r-md);font-size:var(--fs-body);font-weight:500;cursor:pointer;transition:border-color .15s}
.fg select:focus{outline:none;border-color:var(--primary);box-shadow:var(--focus-ring)}
.resetbtn{height:var(--h-ctl);padding:0 var(--s-4);background:var(--bg-surface);color:var(--primary);border:var(--bw) solid var(--border-strong);border-radius:var(--r-md);cursor:pointer;font-size:var(--fs-body);font-weight:500;white-space:nowrap;transition:background .15s}
.resetbtn:hover{background:var(--bg-subtle)}

/* ---------- KPI cards ---------- */
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(var(--w-kpi-min),1fr));gap:var(--s-6);margin-bottom:var(--s-6)}
.kpi{background:var(--bg-surface);border:var(--bw) solid var(--border);border-radius:var(--r-xl);padding:var(--s-6);min-height:var(--h-kpi);transition:border-color .2s,box-shadow .2s}
.kpi:hover{border-color:var(--border-strong);box-shadow:var(--shadow-card)}
.kpi-top{display:flex;justify-content:space-between;align-items:center}
.kpi .label{font-size:var(--fs-h3);font-weight:500;color:var(--text-1)}
.kpi-icon{width:var(--s-5);height:var(--s-5);color:var(--primary);flex:none}
.kpi .val{font-size:var(--fs-kpi);font-weight:700;letter-spacing:-.02em;line-height:1.2;margin-top:var(--s-4);font-variant-numeric:tabular-nums}
.kpi .note{font-size:var(--fs-small);color:var(--text-3);margin-top:var(--s-5)}
.kpi .chip{display:none;margin-top:var(--s-3);height:var(--h-pill);padding:0 var(--s-2);border-radius:var(--r-pill);font-size:var(--fs-chip);font-weight:600;width:max-content;align-items:center;letter-spacing:.01em}
.kpi .chip.on{display:inline-flex}
.kpi .chip.good{background:var(--success-50);color:var(--success)}
.kpi .chip.bad{background:var(--danger-50);color:var(--danger)}

/* ---------- cards / grids ---------- */
.section-title{font-size:var(--fs-micro);font-weight:500;color:var(--text-3);text-transform:uppercase;letter-spacing:.04em;margin:var(--s-6) 0 var(--s-3)}
.grid{display:grid;gap:var(--s-6);margin-bottom:var(--s-6)}
.g2{grid-template-columns:repeat(auto-fit,minmax(var(--w-g2),1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(var(--w-g3),1fr))}
.card{background:var(--bg-surface);border:var(--bw) solid var(--border);border-radius:var(--r-xl);padding:var(--s-6);transition:border-color .2s,box-shadow .2s}
.card:hover{border-color:var(--border-strong);box-shadow:var(--shadow-card)}
.card h3{font-size:var(--fs-h2);font-weight:600;letter-spacing:-.01em}
.card .hint{font-size:var(--fs-small);color:var(--text-3);margin-top:var(--s-1);margin-bottom:var(--s-4)}
.card.span2{grid-column:span 2}
.chartbox{position:relative;height:var(--h-chart)}
.chartbox.tall{height:var(--h-chart-tall)}
.chartbox.hero{height:var(--h-hero)}
.toptrend{margin-bottom:var(--s-6)}

/* ---------- top-3 strip ---------- */
.badges{display:grid;grid-template-columns:repeat(auto-fit,minmax(var(--w-badge-min),1fr));gap:var(--s-3);margin-bottom:var(--s-4)}
.badge{display:flex;align-items:center;gap:var(--s-2);background:var(--bg-surface);border:var(--bw) solid var(--border);border-left:var(--bw-2) solid var(--c0);border-radius:var(--r-lg);padding:var(--s-3) var(--s-4);font-size:var(--fs-body);font-weight:500;color:var(--text-1)}
.badge.b1{border-left-color:var(--c1)}
.badge.b2{border-left-color:var(--c2)}
.badge .rank{width:var(--s-5);height:var(--s-5);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:var(--fs-micro);font-weight:700;color:var(--rk,var(--text-3));background:var(--bg-subtle);flex:none}
.badge b{font-weight:700;color:var(--text-1);font-variant-numeric:tabular-nums}

/* ---------- table ---------- */
table{width:100%;border-collapse:collapse;font-size:var(--fs-body)}
thead th{text-align:left;height:var(--s-10);padding:0 var(--s-4);color:var(--text-3);font-size:var(--fs-micro);font-weight:500;text-transform:uppercase;letter-spacing:.04em;border-bottom:var(--bw) solid var(--border);cursor:pointer;white-space:nowrap;user-select:none;background:var(--bg-surface)}
thead th:hover{color:var(--text-1)}
tbody td{padding:var(--s-3) var(--s-4);border-bottom:var(--bw) solid var(--border);color:var(--text-2);height:var(--h-row);font-variant-numeric:tabular-nums}
tbody td:first-child{color:var(--text-1);font-weight:500}
tbody tr:hover td{background:var(--bg-subtle)}
.empty{text-align:center;color:var(--text-3);padding:var(--s-8) 0;height:auto}
.pill{height:var(--h-pill);display:inline-flex;align-items:center;padding:0 var(--s-3);border-radius:var(--r-pill);font-size:var(--fs-chip);font-weight:600}
.pill.closed{background:var(--success-50);color:var(--success)}
.pill.wip{background:var(--warning-50);color:var(--warn-text)}
.tablebar{display:flex;justify-content:space-between;align-items:center;margin-bottom:var(--s-3);flex-wrap:wrap;gap:var(--s-2)}
.tablebar input{height:var(--s-10);padding:0 var(--s-4);background:var(--bg-subtle);border:var(--bw) solid var(--border);border-radius:var(--r-pill);color:var(--text-1);font-size:var(--fs-body);min-width:var(--w-search-min)}
.tablebar input:focus{outline:none;background:var(--bg-surface);border-color:var(--primary);box-shadow:var(--focus-ring)}
.tablebar input::placeholder{color:var(--text-3)}
.tablebar .hint{margin:0}
.tableScroll{overflow:auto;max-height:var(--h-table)}
.tableScroll thead{position:sticky;top:0;z-index:1}
.pager{display:flex;gap:var(--s-2);align-items:center;margin-top:var(--s-3);justify-content:flex-end;color:var(--text-3);font-size:var(--fs-small)}
.pager button{height:var(--s-8);padding:0 var(--s-3);background:var(--bg-surface);border:var(--bw) solid var(--border-strong);border-radius:var(--r-md);color:var(--text-1);cursor:pointer;font-size:var(--fs-small);font-weight:500;transition:background .15s}
.pager button:hover{background:var(--bg-subtle)}
.pager button:disabled{opacity:.45;cursor:not-allowed}
.pager-jump{height:var(--s-8);width:var(--w-jump);border:var(--bw) solid var(--border-strong);border-radius:var(--r-md);text-align:center;color:var(--text-1);background:var(--bg-surface);font-size:var(--fs-small)}

/* ---------- header tools (built by JS) ---------- */
.months{display:flex;gap:var(--s-2);align-items:center}
.mbtn{height:var(--h-btn-sm);padding:0 var(--s-4);border:var(--bw) solid var(--border);background:var(--bg-subtle);color:var(--text-1);border-radius:var(--r-md);cursor:pointer;font-size:var(--fs-small);font-weight:500;transition:background .15s,border-color .15s}
.mbtn:hover{border-color:var(--primary)}
.mbtn.active{background:var(--primary);border-color:var(--primary);color:var(--bg-surface)}
.hdr-search{display:flex;align-items:center;height:var(--s-10);border:var(--bw) solid var(--border);border-radius:var(--r-pill);background:var(--bg-subtle);overflow:hidden;width:var(--s-10);transition:width .28s cubic-bezier(.4,0,.2,1)}
.hdr-search.open{width:var(--w-search-open)}
.hdr-search-btn{flex:none;width:var(--s-10);height:calc(var(--s-10) - var(--s-1));display:flex;align-items:center;justify-content:center;background:transparent;border:none;cursor:pointer;color:var(--text-3);padding:0}
.hdr-search-btn.on{color:var(--primary)}
.hdr-search-input{flex:1;min-width:0;height:100%;border:none;outline:none;background:transparent;font-size:var(--fs-body);color:var(--text-1);padding:0 var(--s-3) 0 0}
.hdr-search-input::placeholder{color:var(--text-3)}
.cal-btn{width:var(--s-10);height:var(--s-10);display:flex;align-items:center;justify-content:center;border:var(--bw) solid var(--border);background:var(--bg-subtle);color:var(--text-3);border-radius:var(--r-pill);cursor:pointer;transition:.15s;padding:0;flex:none}
.cal-btn:hover{border-color:var(--primary);color:var(--text-1)}
.cal-btn.active{border-color:var(--glass-brd-2);background:var(--glass-2);color:var(--text-1)}
.month-pop{display:none;position:absolute;top:calc(var(--s-10) + var(--s-1));right:0;z-index:50;width:var(--w-pop);background:var(--bg-surface);border:var(--bw) solid var(--border);border-radius:var(--r-lg);box-shadow:var(--shadow-3);padding:var(--s-5)}
.month-pop.open{display:block}
.mp-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:var(--s-1)}
.mp-title{font-size:var(--fs-body);font-weight:600;color:var(--text-1)}
.mp-all{height:var(--s-8);padding:0 var(--s-4);border:var(--bw) solid var(--border-strong);background:var(--bg-surface);color:var(--text-2);border-radius:var(--r-md);cursor:pointer;font-size:var(--fs-small);font-weight:600;transition:.12s}
.mp-all:hover{border-color:var(--primary);color:var(--primary)}
.mp-all.active{background:var(--primary);color:var(--bg-surface);border-color:var(--primary)}
.mp-hint{font-size:var(--fs-micro);color:var(--text-3);margin-bottom:var(--s-4)}
.mp-year{margin-top:var(--s-4)}
.mp-year:first-of-type{margin-top:0}
.mp-year-lbl{font-size:var(--fs-micro);font-weight:600;color:var(--text-3);letter-spacing:.04em;text-transform:uppercase;margin-bottom:var(--s-2)}
.mp-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--s-2)}
.mp-chip{padding:var(--s-2) 0;text-align:center;border-radius:var(--r-md);cursor:pointer;font-size:var(--fs-small);font-weight:600;transition:.12s;border:var(--bw) solid var(--border);background:var(--bg-subtle);color:var(--text-1)}
.mp-chip:hover{border-color:var(--primary)}
.mp-chip.sel{border-color:var(--primary);background:var(--primary);color:var(--bg-surface)}
.mp-foot{margin-top:var(--s-4);padding-top:var(--s-3);border-top:var(--bw) solid var(--border);font-size:var(--fs-micro);color:var(--text-3)}
.mp-foot span{color:var(--text-1);font-weight:600}

/* ---------- heatmap ---------- */
.heatmap{height:var(--h-chart-tall);overflow:auto}
.heatmap table{border-collapse:separate;border-spacing:var(--s-1)}
.heatmap th{background:transparent;text-transform:none;letter-spacing:0;cursor:default;font-size:var(--fs-small);font-weight:500;padding:var(--s-1) var(--s-2);color:var(--text-3);text-align:center;vertical-align:bottom}
.heatmap th.rowlbl{text-align:right;white-space:nowrap;font-weight:600;color:var(--text-1)}
.heatmap td{padding:0;border:none;height:auto}
.heatmap .cell{min-width:var(--w-cell);height:var(--s-10);border-radius:var(--r-sm);display:flex;align-items:center;justify-content:center;font-size:var(--fs-small);font-weight:600;transition:.15s}
.heatmap .cell:hover{outline:var(--bw-2) solid var(--primary)}

/* ---------- loading ---------- */
.loading{position:fixed;inset:0;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:9999}
.loading-logo{position:relative;width:var(--logo);height:var(--logo);margin-bottom:var(--s-5)}
.loading-logo img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain}
.loading-dim{filter:grayscale(1) opacity(.2)}
.loading-fill{position:absolute;left:0;right:0;bottom:0;height:0%;overflow:hidden;transition:height .3s}
.loading-fill img{position:absolute;bottom:0;left:0;width:var(--logo);height:var(--logo);object-fit:contain}
.loading-title{font-size:var(--fs-h3);color:var(--text-1);font-weight:600;margin-bottom:var(--s-2)}
.loading-pct{font-size:var(--fs-small);color:var(--text-3)}

/* ---------- responsive: ≤768 (matches isMobile() threshold) ---------- */
@media (max-width:48em){
  :root{--topbar-h:52px;--fs-h1:20px;--fs-kpi:24px;--fs-h2:15px;--h-chart:240px;--h-chart-tall:260px;--h-kpi:0px;--h-hero:260px;--h-table:440px}
  .rail{display:none}
  .main{margin-left:0}
  .topbar{justify-content:space-between;padding:0 var(--s-4)}
  .topbar-brand{display:flex}
  .page{padding:var(--s-4)}
  .months{width:100%;gap:var(--s-2)}
  .mbtn{padding:var(--s-2) var(--s-3);font-size:var(--fs-small);flex:1;text-align:center;min-width:0}
  .fg{min-width:calc((100% - var(--s-3)) / 2)}
  .fg select{height:var(--h-touch);font-size:var(--fs-body)}
  .resetbtn{width:100%;text-align:center;height:var(--h-touch)}
  .kpis{grid-template-columns:1fr 1fr;gap:var(--s-3)}
  .kpi{padding:var(--s-4)}
  .kpi .val{margin-top:var(--s-2)}
  .g2,.g3{grid-template-columns:1fr}
  .card.span2{grid-column:span 1}
  .card{padding:var(--s-4)}
  .badges{grid-template-columns:1fr}
  .tablebar{flex-direction:column;align-items:stretch}
  .tablebar input{min-width:100%;height:var(--h-touch)}
  tbody td{font-size:var(--fs-small);padding:var(--s-2) var(--s-2)}
  .heatmap{overflow-x:auto;-webkit-overflow-scrolling:touch}
}

/* ---------- responsive: ≤480 ---------- */
@media (max-width:30em){
  :root{--fs-h1:18px;--fs-kpi:22px;--h-chart:230px;--h-chart-tall:250px;--h-hero:250px}
  .page{padding:var(--s-3)}
  .fg{min-width:100%}
  .kpis{grid-template-columns:1fr}
  .mp-grid{gap:var(--s-1)}
}

/* ==========================================================================
   LIQUID GLASS RESKIN — v2 (overrides cascade above in one block).
   Floating glass rail + toolbar, glass cards, dual theme. Data logic untouched.
   See restyle-log.md §Glass + prototype: brainstorm/content/prototype-v2.html
   ========================================================================== */
.rail{left:var(--edge);top:var(--edge);bottom:var(--edge);width:var(--rail-w);background:var(--glass);backdrop-filter:blur(var(--blur)) saturate(180%);-webkit-backdrop-filter:blur(var(--blur)) saturate(180%);border:var(--bw) solid var(--glass-brd-2);border-right:var(--bw) solid var(--glass-brd-2);border-radius:var(--r-lg);box-shadow:var(--shadow-card)}
.rail-brand{border-bottom:var(--bw) solid var(--glass-brd-2)}
.rl:hover{background:var(--glass-2)}
.rl.active{background:var(--primary-50);box-shadow:var(--ring-inset);color:var(--primary-600)}
.rl.active svg{color:var(--primary-600)}
.rail-foot{border-top:var(--bw) solid var(--glass-brd-2)}
@media (min-width:48em){
  .main{margin-left:calc(var(--rail-w) + var(--s-8));padding:0 var(--edge)}
  .topbar{position:sticky;top:var(--edge);margin:0 var(--edge) 0 var(--edge);padding:var(--s-2) var(--s-4);background:var(--glass);backdrop-filter:blur(var(--blur)) saturate(180%);-webkit-backdrop-filter:blur(var(--blur)) saturate(180%);border:var(--bw) solid var(--glass-brd-2);border-radius:var(--r-md);box-shadow:var(--shadow-card);justify-content:space-between}
  .topbar-end{flex:1;display:flex;justify-content:flex-start;align-items:center;gap:var(--s-3)}
  .topbar-end .tbl-btn.wide{margin-left:auto}
  [id^="sec-"]{scroll-margin-top:calc(var(--topbar-h) + var(--s-8))}
  .pagehead{padding-top:var(--s-5)}
}
@media (max-width:48em){
  .topbar{margin:0 var(--s-2);background:var(--glass);backdrop-filter:blur(var(--blur)) saturate(180%);-webkit-backdrop-filter:blur(var(--blur)) saturate(180%);border:var(--bw) solid var(--glass-brd-2);border-radius:var(--r-md);box-shadow:var(--shadow-card)}
  .topbar-end{gap:var(--s-2)}
  .tbl-btn{width:var(--h-touch);height:var(--h-touch)}
}
.filters{background:var(--glass);backdrop-filter:blur(var(--blur)) saturate(180%);-webkit-backdrop-filter:blur(var(--blur)) saturate(180%);border:var(--bw) solid var(--glass-brd);box-shadow:var(--shadow-card)}
.tablebar input{background:var(--glass-2);border:var(--bw) solid var(--glass-brd-2)}
.fg select{background:var(--glass-2);border:var(--bw) solid var(--glass-brd-2)}
.fg select option{background:var(--bg-surface);color:var(--text-1)}
.resetbtn{background:var(--glass-2);border:var(--bw) solid var(--glass-brd-2)}
.resetbtn:hover{background:var(--glass)}
.kpi,.card{background:var(--sheen);backdrop-filter:blur(var(--blur)) saturate(180%);-webkit-backdrop-filter:blur(var(--blur)) saturate(180%);border:var(--bw) solid var(--glass-brd);box-shadow:var(--shadow-card)}
.kpi:hover,.card:hover{transform:translateY(var(--n-lift));border-color:var(--glass-brd-2)}

.badge{background:var(--glass);border:var(--bw) solid var(--glass-brd)}
.badge .rank{background:var(--glass-2)}
thead th{background:var(--glass);backdrop-filter:blur(var(--blur-sm)) saturate(180%);-webkit-backdrop-filter:blur(var(--blur-sm)) saturate(180%)}
tbody tr:nth-child(even) td{background:var(--row-tint)}
tbody tr:hover td{background:var(--row-tint)}
.pager button{background:var(--glass-2);border:var(--bw) solid var(--glass-brd-2)}
.pager button:hover{background:var(--glass)}
.pager-jump{background:var(--glass-2);border:var(--bw) solid var(--glass-brd-2)}
.mbtn,.cal-btn{background:var(--glass-2);border:var(--bw) solid var(--glass-brd-2)}
.hdr-search{background:var(--glass-2);border:var(--bw) solid var(--glass-brd-2)}
.month-pop{background:var(--glass);backdrop-filter:blur(var(--blur-lg)) saturate(180%);-webkit-backdrop-filter:blur(var(--blur-lg)) saturate(180%);border:var(--bw) solid var(--glass-brd-2);box-shadow:var(--shadow-3)}


.mp-all,.mp-chip{background:var(--glass-2);border:var(--bw) solid var(--glass-brd-2)}
.mp-chip:hover{background:var(--glass)}
.loading{background:var(--bg-app)}
.kpis .kpi:nth-child(1) .kpi-icon{color:var(--k1)}
.kpis .kpi:nth-child(2) .kpi-icon{color:var(--k2)}
.kpis .kpi:nth-child(3) .kpi-icon{color:var(--k3)}
.kpis .kpi:nth-child(4) .kpi-icon{color:var(--k4)}
/* theme toggle — sun/moon pill */
.tbl-btn{flex:none;width:var(--s-10);height:var(--h-btn-sm);display:flex;align-items:center;justify-content:center;border:var(--bw) solid var(--glass-brd-2);background:var(--glass-2);border-radius:var(--r-pill);color:var(--text-2);cursor:pointer;transition:background .2s,border-color .2s;padding:0}
.tbl-btn:hover{border-color:var(--primary);color:var(--text-1)}
.tbl-btn svg{width:var(--s-4);height:var(--s-4);stroke:currentColor;fill:none;stroke-width:var(--bw-2);stroke-linecap:round;stroke-linejoin:round}
/* motion + accessibility gates */
@media (prefers-reduced-motion:reduce){
  *{transition:none!important;animation:none!important}
  html{scroll-behavior:auto}
}
@media (prefers-reduced-transparency:reduce){
  .rail,.topbar,.filters,.kpi,.card,.badge,.month-pop,thead th{backdrop-filter:none;-webkit-backdrop-filter:none}
  .rail,.topbar{background:var(--bg-surface);border-color:var(--border)}
  .filters,.month-pop{background:var(--bg-surface)}
}
@media (prefers-contrast:more){
  .rail,.topbar,.filters,.kpi,.card,.badge,.month-pop,thead th{backdrop-filter:none;-webkit-backdrop-filter:none}
  .rail,.topbar,.kpi,.card,.filters,.month-pop{background:var(--bg-surface);border:var(--bw) solid var(--border-strong)}
}
/* PROTOTYPE MATCH ROUND 2 — Overview head order, big KPI cards, pill toolbar
   ========================================================================== */
/* KPI cards — prototype v2 scale */
.kpi{padding:var(--s-4) var(--s-4) var(--s-3)}
.kpi .kpi-top{align-items:flex-start}
.kpi .label{font-size:var(--fs-kpi-label);font-weight:600;color:var(--text-2)}
.kpi .kpi-icon{width:var(--icon-badge);height:var(--icon-badge);box-sizing:border-box;padding:var(--icon-pad);border-radius:var(--icon-r);background:color-mix(in srgb,currentColor 15%,transparent);color:var(--k,var(--primary))}
.kpi .val{margin:var(--s-2) 0 var(--s-1);font-weight:800;letter-spacing:-.032em}
.kpi .sub{display:flex;align-items:center;gap:var(--s-2);margin-top:var(--s-1);min-height:0;font-size:var(--fs-kpi-sub)}
.kpi .sub .note{flex:1;margin-top:0;font-size:var(--fs-kpi-sub);color:var(--text-3)}
.kpi .sub .chip{margin-top:0;height:auto;padding:var(--pad-tiny) var(--chip-px);border-radius:var(--chip-r);font-weight:700}
/* layout rhythm — prototype v2: 16px frame, 12px block gaps (desktop) */
@media (min-width:48em){
  .main{margin:var(--edge);margin-left:calc(var(--rail-w) + var(--s-8));padding:0}
  .page{padding:0 0 var(--edge)}
  .pagehead{padding:var(--s-1) var(--s-2) var(--s-3);margin-bottom:0}
  .topbar{margin-bottom:var(--s-3)}
  .kpis{grid-template-columns:repeat(4,1fr);gap:var(--s-3);margin-bottom:var(--s-3)}
}
.section-title{margin:var(--s-3) 0 var(--s-2)}
.grid{gap:var(--s-3);margin-bottom:var(--s-3)}
/* nav rows — prototype v2: compact rows, bolted-square markers */
.rl{height:auto;padding:var(--nav-py) var(--nav-px);border-radius:var(--nav-r);font-size:var(--fs-nav);font-weight:500;color:var(--text-2)}
.rl svg{display:none}
.rl-ic{width:var(--nav-ic);height:var(--nav-ic);flex:none;border-radius:var(--nav-ic-r);background:currentColor;opacity:.5}
.rl.active{background:color-mix(in srgb,var(--primary) 16%,transparent);box-shadow:inset 0 0 0 var(--bw) color-mix(in srgb,var(--primary) 28%,transparent);color:var(--primary);font-weight:600}
.rl.active .rl-ic{opacity:1}
.rail-logo{width:var(--logo-s);height:var(--logo-s);flex:none;object-fit:contain;border-radius:var(--r-md)}
.rail-brand{height:auto;border-bottom:0;padding:var(--s-1) var(--s-3) var(--s-4)}
.rail-name{font-size:var(--fs-brand);font-weight:700}
.rail-label{padding:var(--s-3) var(--s-3) var(--s-2)}
.rail-foot-k{font-size:var(--fs-foot)}
.rail-foot-v{font-size:var(--fs-small);color:var(--text-2)}
/* toolbar pills — prototype v2 */
.cal-btn{display:inline-flex;align-items:center;gap:var(--s-2);width:auto;padding:var(--tool-py) var(--tool-px);font-size:var(--tool-fs);font-weight:600;color:var(--text-1)}
.cal-btn svg{width:var(--s-4);height:var(--s-4);color:var(--text-2);flex:none}
.cal-btn .rng{white-space:nowrap}
.cal-btn .mo-chip{padding:var(--mchip-py) var(--mchip-px);border-radius:var(--r-sm);background:var(--primary-50);color:var(--primary);font-size:var(--fs-micro);font-weight:600;white-space:nowrap;box-shadow:inset 0 0 0 var(--bw) color-mix(in srgb,var(--primary) 26%,transparent)}
/* search lives inside the month popover now (prototype v2: clean toolbar) */
.month-pop .hdr-search,.month-pop .hdr-search.open{width:100%}
.month-pop .hdr-search{margin-bottom:var(--s-2)}
.fchip{display:inline-flex;align-items:center;gap:var(--s-2);padding:var(--tool-py) var(--tool-px);border-radius:var(--r-md);background:var(--glass-2);border:var(--bw) solid var(--glass-brd-2);color:var(--text-2);font-size:var(--tool-fs);font-weight:600;cursor:pointer;white-space:nowrap;transition:background .2s,border-color .2s}
.fchip:hover{border-color:var(--primary);color:var(--text-1)}
.fchip svg{width:var(--s-4);height:var(--s-4);flex:none;fill:currentColor;stroke:none}
.fchip b{background:var(--success-50);color:var(--success);padding:var(--mchip-py) var(--mchip-px);border-radius:var(--r-sm);font-weight:600;font-size:var(--fs-micro)}
.fchip.zero b{background:var(--bg-muted);color:var(--text-3)}
.tbl-btn{width:auto;height:auto}
.tbl-btn.wide{padding:var(--tool-py) var(--tool-px);color:var(--text-1);font-weight:600;font-size:var(--tool-fs)}
.tbl-btn.knobbtn{width:var(--knob-w);height:var(--knob-h);border-radius:var(--knob-r);display:block;position:relative;padding:0;flex:none}
.knobbtn .knob{position:absolute;top:var(--knob-oy);left:var(--knob-ox);width:var(--knob-d);height:var(--knob-d);border-radius:50%;background:var(--knob);box-shadow:var(--knob-shadow);transition:transform .4s cubic-bezier(.34,1.4,.64,1),background .4s}
/* note band removed in prototype v2 match */
/* filters: on-demand floating panel (prototype v2) */
.filters{position:fixed;display:none;top:calc(var(--edge) + var(--topbar-h) + var(--s-3));right:var(--edge);left:auto;width:min(var(--fpanel-w),calc(100vw - var(--rail-w) - var(--s-8)));max-height:calc(100vh - var(--fpanel-vacant));overflow:auto;z-index:45;margin-bottom:0}
.filters.show{display:flex}
@media(max-width:48em){
  .filters{left:var(--edge);right:var(--edge);width:auto}
}
@media (max-width:48em){
  .kpi{padding:var(--s-4);min-height:0}
  .kpi .kpi-icon{width:var(--icon-badge-m);height:var(--icon-badge-m);padding:var(--icon-pad-m)}
  .fchip span{display:none}
  .cal-btn .rng{max-width:34vw;overflow:hidden;text-overflow:ellipsis}
  .topbar-end .tbl-btn.wide{display:none}
  .knobbtn{margin-left:auto}
  .topbar-end{flex-wrap:wrap;gap:var(--s-2)}
}
</style>
</head>
<body>
<aside class="rail" aria-label="Section navigation">
  <div class="rail-brand">
    <img class="rail-logo" src="data:image/png;base64,__FAVICON__" alt="">
    <span class="rail-name">Premier Energies</span>
  </div>
  <div class="rail-label">Menu</div>
  <nav class="rail-nav">
    <a class="rl active" href="#sec-overview"><div class="rl-ic" aria-hidden="true"></div>Overview</a>
    <a class="rl" href="#sec-defects"><div class="rl-ic" aria-hidden="true"></div>Defect Breakdown</a>
    <a class="rl" href="#sec-segments"><div class="rl-ic" aria-hidden="true"></div>Segments</a>
    <a class="rl" href="#sec-geo"><div class="rl-ic" aria-hidden="true"></div>Geography &amp; TAT</a>
    <a class="rl" href="#sec-production"><div class="rl-ic" aria-hidden="true"></div>Production</a>
    <a class="rl" href="#sec-trend"><div class="rl-ic" aria-hidden="true"></div>Volume &amp; Trend</a>
    <a class="rl" href="#sec-records"><div class="rl-ic" aria-hidden="true"></div>Records</a>
  </nav>
  <div class="rail-foot">
    <div class="rail-foot-k">Data through</div>
    <div class="rail-foot-v" id="data-through">Sep 2026</div>
  </div>
</aside>
<div class="main">
  <header class="pagehead" id="sec-overview">
    <h1>Overview</h1>
    <div class="sub" id="pagehead-sub">Field service &amp; module defect tracking · Dec 2024–Sep 2026</div>
  </header>
  <div class="topbar">
    <div class="topbar-brand"><img src="data:image/png;base64,__FAVICON__" alt="Premier Energies"></div>
    <div class="topbar-end"><div class="months" id="months"></div><button id="f-on" class="fchip" type="button" title="Show filters"><svg viewBox="0 0 24 24"><path d="M22 3H2l10 10v8l2-2v-6z"/></svg><span><b id="f-on-n">0</b> filters on</span></button><button id="rst-top" class="tbl-btn wide" type="button">Reset</button></div>
  </div>
  <main class="page">
    <div class="kpis">
      <div class="kpi"><div class="kpi-top"><div class="label" id="k-closed-label">Modules Serviced</div><svg class="kpi-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg></div><div class="val" id="k-closed">0</div><div class="sub"><div class="note" id="k-closed-note"></div><div class="chip" id="k-closed-chip"></div></div></div>
      <div class="kpi"><div class="kpi-top"><div class="label">Closure Rate</div><svg class="kpi-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" x2="5" y1="5" y2="19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/></svg></div><div class="val" id="k-closure">0%</div><div class="sub"><div class="note" id="k-closure-note"></div><div class="chip" id="k-closure-chip"></div></div></div>
      <div class="kpi"><div class="kpi-top"><div class="label">Avg TAT (days)</div><svg class="kpi-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="10" x2="14" y1="2" y2="2"/><line x1="12" x2="15" y1="14" y2="11"/><circle cx="12" cy="14" r="8"/></svg></div><div class="val" id="k-tat">0</div><div class="sub"><div class="note" id="k-tat-note"></div><div class="chip" id="k-tat-chip"></div></div></div>
      <div class="kpi"><div class="kpi-top"><div class="label">Open (WIP)</div><svg class="kpi-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg></div><div class="val" id="k-wip">0</div><div class="sub"><div class="note" id="k-wip-note">awaiting resolution</div><div class="chip" id="k-wip-chip"></div></div></div>
    </div>

    <div class="filters">
      <div class="fg"><label>Customer Type</label><select id="f-customer"></select></div>
      <div class="fg"><label>Customer Name</label><select id="f-custname"></select></div>
      <div class="fg"><label>Defect Category</label><select id="f-category"></select></div>
      <div class="fg"><label>Sub-category</label><select id="f-subcat"></select></div>
      <div class="fg"><label>State</label><select id="f-state"></select></div>
      <div class="fg"><label>Status</label><select id="f-status"></select></div>
      <div class="fg"><label>Manufacturing Plant</label><select id="f-plant"></select></div>
      <div class="fg"><label>Resolution Type</label><select id="f-resolution"></select></div>
      <button class="resetbtn" id="reset">Reset filters</button>
    </div>

    <div class="card toptrend">
      <h3>Top 3 Problems — Trend</h3>
      <div class="hint">The 3 largest defect types for the current month selection, tracked across all months. Recalculates as you change filters.</div>
      <div class="badges" id="top3badges"></div>
      <div class="chartbox hero"><canvas id="chTop3"></canvas></div>
    </div>

    <div class="section-title" id="sec-defects">Defect Breakdown</div>
    <div class="grid g2">
      <div class="card"><h3>Defects by Category</h3><div class="hint">Excludes "No Issue". Where to focus process-improvement effort.</div><div class="chartbox"><canvas id="chCat"></canvas></div></div>
      <div class="card"><h3>Top Defect Sub-categories (Pareto)</h3><div class="hint">80/20 view — the few defect types driving most of the volume.</div><div class="chartbox"><canvas id="chPareto"></canvas></div></div>
    </div>

    <div class="section-title" id="sec-segments">Segments</div>
    <div class="grid g3">
      <div class="card"><h3>By Customer Type</h3><div class="hint">Which segments generate defect load.</div><div class="chartbox"><canvas id="chCust"></canvas></div></div>
      <div class="card"><h3>By Manufacturing Plant</h3><div class="hint">Defect attribution by plant.</div><div class="chartbox"><canvas id="chPlant"></canvas></div></div>
      <div class="card"><h3>Status (Closed vs WIP)</h3><div class="hint">Resolution progress.</div><div class="chartbox"><canvas id="chStatus"></canvas></div></div>
    </div>

    <div class="section-title" id="sec-geo">Geography &amp; TAT</div>
    <div class="grid g2">
      <div class="card"><h3>Top States by Defects</h3><div class="hint">Geographic concentration — where to position field teams.</div><div class="chartbox tall"><canvas id="chState"></canvas></div></div>
      <div class="card"><h3>Defect Resolution Timeline</h3><div class="hint">Average TAT (days) per month — is resolution speed improving?</div><div class="chartbox tall"><canvas id="chTATtrend"></canvas></div></div>
    </div>

    <div class="section-title" id="sec-production">Production &amp; Customer Analysis</div>
    <div class="grid g2">
      <div class="card"><h3>Top Defects by Production Batch</h3><div class="hint">Defect category mix per manufacturing plant — which defect dominates each batch.</div><div class="chartbox tall"><canvas id="chBatch"></canvas></div></div>
      <div class="card"><h3>Customer × Defect Heatmap</h3><div class="hint">Defect concentration by customer type. Darker = more defects.</div><div id="heatmap" class="heatmap"></div></div>
    </div>

    <div class="section-title" id="sec-trend">Volume &amp; Trend</div>
    <div class="grid g2">
      <div class="card"><h3>Monthly Closed vs WIP</h3><div class="hint">Resolution progress per month — closed and open modules.</div><div class="chartbox"><canvas id="chMonthly"></canvas></div></div>
      <div class="card"><h3>Defect Category Trend</h3><div class="hint">How each category moves month to month.</div><div class="chartbox"><canvas id="chCatTrend"></canvas></div></div>
    </div>

    <div class="section-title" id="sec-records">Module-level Records</div>
    <div class="card">
      <div class="tablebar">
        <div class="hint" id="tcount" style="margin:0"></div>
        <input id="search" placeholder="Search serial, complaint no…">
      </div>
      <div class="tableScroll">
        <table id="tbl">
          <thead><tr>
            <th data-k="month">Month</th><th data-k="serial">Serial</th>
            <th data-k="customer_type">Customer</th><th data-k="state">State</th>
            <th data-k="category">Category</th><th data-k="subcategory">Sub-category</th>
            <th data-k="plant">Plant</th><th data-k="status">Status</th>
            <th data-k="complaint_no">Complaint No.</th>
          </tr></thead>
          <tbody id="tbody"></tbody>
        </table>
      </div>
      <div class="pager"><span id="pginfo"></span>
        <input type="number" id="pgjump" class="pager-jump" min="1" placeholder="#">
        <button id="pgjumpbtn">Go</button>
        <button id="prev">Prev</button><button id="next">Next</button></div>
    </div>

  </main>
</div>

<div class="loading" id="loading">
  <div class="loading-logo">
    <img src="data:image/png;base64,__FAVICON__" class="loading-dim" alt="">
    <div class="loading-fill" id="logo-fill"><img src="data:image/png;base64,__FAVICON__" alt=""></div>
  </div>
  <div class="loading-title">Loading dashboard…</div>
  <div class="loading-pct" id="load-pct">0%</div>
</div>
<script>
let DB=null;
const MONTHS = ["2024-12","2025-01","2025-02","2025-03","2025-04","2025-05","2025-06","2025-07","2025-08","2025-09","2025-10","2025-11","2025-12","2026-01","2026-02","2026-03","2026-04","2026-05","2026-06","2026-07","2026-08","2026-09"];
const MLABEL = {"2024-12":"Dec-24","2025-01":"Jan-25","2025-02":"Feb-25","2025-03":"Mar-25","2025-04":"Apr-25","2025-05":"May-25","2025-06":"Jun-25","2025-07":"Jul-25","2025-08":"Aug-25","2025-09":"Sep-25","2025-10":"Oct-25","2025-11":"Nov-25","2025-12":"Dec-25","2026-01":"Jan-26","2026-02":"Feb-26","2026-03":"Mar-26","2026-04":"Apr-26","2026-05":"May-26","2026-06":"Jun-26","2026-07":"Jul-26","2026-08":"Aug-26","2026-09":"Sep-26"};
// "Data through" + header range derive from MONTHS so they never go stale
const M2FULL=m=>MLABEL[m].replace('-',' 20');
document.getElementById('data-through').textContent=M2FULL(MONTHS[MONTHS.length-1]);
document.getElementById('pagehead-sub').textContent='Field service & module defect tracking · '+M2FULL(MONTHS[0])+'–'+M2FULL(MONTHS[MONTHS.length-1]);
const CAT_ORDER = ["Junction Box Defects","Ribbon Soldering Issue","Cell and Module Defects","Physical and External Damage","Transit Damage","Aesthetic","No Issue","Inspection"];
const ROOT=getComputedStyle(document.documentElement);
const V=n=>ROOT.getPropertyValue(n).trim();
// custom properties are not pre-converted; resolve via a probe element (cached)
const rgbCache={};let rgbProbe=null;
function rgb(n){
  if(rgbCache[n])return rgbCache[n];
  if(!rgbProbe){rgbProbe=document.createElement('i');
    rgbProbe.style.cssText='position:absolute;left:-9999px;width:0;height:0';
    document.body.appendChild(rgbProbe);}
  rgbProbe.style.color='var('+n+')';
  const m=getComputedStyle(rgbProbe).color.match(/\d+/g);
  return rgbCache[n]=m?m.slice(0,3).join(','):'40,97,255';
}
const A=(n,a)=>'rgba('+rgb(n)+','+a+')';
let COLORS=['--c0','--c1','--c2','--c3','--c4','--c5','--c6','--c7'].map(V);
Chart.defaults.color=V('--text-3');Chart.defaults.borderColor=V('--grid');Chart.defaults.font.family=V('--font');Chart.defaults.animation=false;
const isMobile=()=>window.innerWidth<=768;

// ---------- state ----------
let selMonths = new Set(MONTHS);
const state={customer:'All',custname:'All',category:'All',subcat:'All',stateF:'All',status:'All',plant:'All',resolution:'All'};
let sortK='month',sortDir=1,search='',page=0;
const PAGE=50;
let totalTableRows=0;
const charts={};

// ---------- SQL helpers ----------
const DEFECT_COND="category != 'No Issue' AND NOT (category = 'Inspection' AND subcategory != 'Issue Found')";
const HIDE_NA=v=>!/^(n\/?a|na)$/i.test(v);

function query(sql){const stmt=DB.prepare(sql);const rows=[];while(stmt.step())rows.push(stmt.getAsObject());stmt.free();return rows;}
function esc(s){return String(s).replace(/'/g,"''");}
function monthList(){return MONTHS.filter(m=>selMonths.has(m)).map(m=>"'"+m+"'").join(',');}
function buildWhere(opts){
  if(!opts)opts={};
  const c=['1=1'];
  if(opts.months!==false) c.push('month IN ('+monthList()+')');
  if(state.customer!=='All') c.push("customer_type='"+esc(state.customer)+"'");
  if(state.custname!=='All') c.push("complaint_by='"+esc(state.custname)+"'");
  if(state.category!=='All') c.push("category='"+esc(state.category)+"'");
  if(state.subcat!=='All') c.push("subcategory='"+esc(state.subcat)+"'");
  if(state.stateF!=='All') c.push("state='"+esc(state.stateF)+"'");
  if(state.status!=='All') c.push("status='"+esc(state.status)+"'");
  if(state.plant!=='All') c.push("plant='"+esc(state.plant)+"'");
  if(state.resolution!=='All') c.push("resolution='"+esc(state.resolution)+"'");
  if(opts.defects) c.push(DEFECT_COND);
  return ' WHERE '+c.join(' AND ');
}

// ---------- maps built after data loads ----------
const SUBMAP={};
const CUST_TYPE_TO_NAME={};
const CUST_NAME_TO_TYPE={};

// ---------- month picker + search ----------
const monthsEl=document.getElementById('months');
const CAL_SVG='<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"></rect><line x1="3" y1="9" x2="21" y2="9"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="16" y1="2" x2="16" y2="6"></line></svg>';
const SEARCH_SVG='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>';
let calOpen=false, hdrSearchOpen=false;
let hdrSearchWrap,hdrSearchBtn,hdrSearchInput,calBtnEl,monthPopEl,popAllEl,mpShowEl;
const monthChipEls={};

function summaryLabel(){
  const sel=MONTHS.filter(m=>selMonths.has(m));
  if(sel.length===MONTHS.length) return 'All months';
  if(sel.length===1) return MLABEL[sel[0]];
  return MLABEL[sel[0]].slice(0,3)+'–'+MLABEL[sel[sel.length-1]].slice(0,3)+' 26';
}

function setSearch(v){
  search=v;page=0;
  if(hdrSearchInput && hdrSearchInput.value!==v) hdrSearchInput.value=v;
  const low=document.getElementById('search'); if(low && low.value!==v) low.value=v;
  refresh();
}

function syncHeaderUI(){
  const allSel=selMonths.size===MONTHS.length;
  hdrSearchWrap.className='hdr-search'+(hdrSearchOpen?' open':'');
  hdrSearchBtn.classList.toggle('on',hdrSearchOpen);
  calBtnEl.className='cal-btn'+((calOpen||!allSel)?' active':'');
  calBtnEl.querySelector('.rng').textContent=allSel?'All months':summaryLabel();
  const cnt=calBtnEl.querySelector('.mo-chip');
  cnt.textContent=allSel?'':selMonths.size+' mo'; cnt.hidden=allSel;
  monthPopEl.classList.toggle('open',calOpen);
  popAllEl.classList.toggle('active',allSel);
  MONTHS.forEach(m=>monthChipEls[m]&&monthChipEls[m].classList.toggle('sel',selMonths.has(m)));
  const fN=[...document.querySelectorAll('.filters select')].filter(s=>s.value!=='All').length;
  const fEl=document.getElementById('f-on-n'); if(fEl)fEl.textContent=fN;
  const fc=document.getElementById('f-on'); if(fc)fc.classList.toggle('zero',!fN);
  mpShowEl.textContent=summaryLabel();
  if(hdrSearchInput && document.activeElement!==hdrSearchInput && hdrSearchInput.value!==search) hdrSearchInput.value=search;
}

function buildHeaderTools(){
  monthsEl.innerHTML='';
  monthsEl.style.position='relative';

  calBtnEl=document.createElement('button'); calBtnEl.type='button'; calBtnEl.className='cal-btn'; calBtnEl.title='Select month'; calBtnEl.innerHTML=CAL_SVG+'<span class="rng"></span><span class="mo-chip"></span>';
  calBtnEl.onclick=e=>{e.stopPropagation();calOpen=!calOpen;syncHeaderUI();};
  monthsEl.appendChild(calBtnEl);

  hdrSearchWrap=document.createElement('div'); hdrSearchWrap.className='hdr-search';
  hdrSearchBtn=document.createElement('button'); hdrSearchBtn.type='button'; hdrSearchBtn.className='hdr-search-btn'; hdrSearchBtn.innerHTML=SEARCH_SVG;
  hdrSearchInput=document.createElement('input'); hdrSearchInput.className='hdr-search-input'; hdrSearchInput.placeholder='Search serial, complaint no…';
  hdrSearchBtn.onclick=e=>{e.stopPropagation();hdrSearchOpen=!hdrSearchOpen;syncHeaderUI();if(hdrSearchOpen)setTimeout(()=>hdrSearchInput.focus(),60);};
  hdrSearchInput.oninput=e=>setSearch(e.target.value);
  hdrSearchWrap.appendChild(hdrSearchBtn); hdrSearchWrap.appendChild(hdrSearchInput);

  monthPopEl=document.createElement('div'); monthPopEl.className='month-pop';
  monthPopEl.onclick=e=>e.stopPropagation();
  const head=document.createElement('div'); head.className='mp-head';
  const ttl=document.createElement('span'); ttl.className='mp-title'; ttl.textContent='Select month'; head.appendChild(ttl);
  popAllEl=document.createElement('button'); popAllEl.type='button'; popAllEl.className='mp-all'; popAllEl.textContent='All';
  popAllEl.onclick=()=>{selMonths=new Set(MONTHS);refresh();};
  head.appendChild(popAllEl); monthPopEl.appendChild(head);
  const hint=document.createElement('div'); hint.className='mp-hint'; hint.innerHTML='Click a month · hold ⇧ Shift to compare several';
  monthPopEl.appendChild(hdrSearchWrap);
  monthPopEl.appendChild(hint);
  const SHORTM=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const years=[...new Set(MONTHS.map(m=>m.slice(0,4)))];
  years.forEach(yr=>{
    const grp=document.createElement('div'); grp.className='mp-year';
    const lbl=document.createElement('div'); lbl.className='mp-year-lbl'; lbl.textContent=yr; grp.appendChild(lbl);
    const grid=document.createElement('div'); grid.className='mp-grid';
    MONTHS.filter(m=>m.slice(0,4)===yr).forEach(m=>{
      const c=document.createElement('button'); c.type='button'; c.className='mp-chip'; c.textContent=SHORTM[parseInt(m.slice(5,7),10)-1];
      c.onclick=e=>{
        if(e.shiftKey){
          if(selMonths.has(m)){selMonths.delete(m); if(selMonths.size===0)selMonths.add(m);}
          else selMonths.add(m);
        } else selMonths=new Set([m]);
        refresh();
      };
      grid.appendChild(c); monthChipEls[m]=c;
    });
    grp.appendChild(grid); monthPopEl.appendChild(grp);
  });
  const foot=document.createElement('div'); foot.className='mp-foot'; foot.innerHTML='Showing: <span id="mp-showing"></span>'; monthPopEl.appendChild(foot);
  monthsEl.appendChild(monthPopEl);
  mpShowEl=foot.querySelector('#mp-showing');

  document.addEventListener('mousedown',e=>{
    if(calOpen && !monthPopEl.contains(e.target) && !calBtnEl.contains(e.target)){calOpen=false;syncHeaderUI();}
    if(hdrSearchOpen && !hdrSearchWrap.contains(e.target)){hdrSearchOpen=false;syncHeaderUI();}
    const fB=document.getElementById('f-on'),fP=document.querySelector('.filters');
    if(fP.classList.contains('show') && !fP.contains(e.target) && !fB.contains(e.target)){fP.classList.remove('show');fB.classList.remove('open');fB.setAttribute('aria-expanded','false');}
  },true);
}

// ---------- filter population ----------
function fill(id,vals,cur){
  const s=document.getElementById(id);
  s.innerHTML='';
  ['All',...vals].forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;if(v===cur)o.selected=true;s.appendChild(o);});
}
function uniq(col,filter){
  const vals=query("SELECT DISTINCT "+col+" FROM complaints WHERE "+col+" IS NOT NULL AND "+col+" != '' ORDER BY "+col).map(r=>r[col]);
  return filter?vals.filter(filter):vals;
}
function populateFilters(){
  populateCustCascade();
  const cats=query("SELECT DISTINCT category FROM complaints").map(r=>r.category);
  fill('f-category',CAT_ORDER.filter(c=>c!=='No Issue'&&cats.includes(c)),state.category);
  populateSub();
  fill('f-state',uniq('state',HIDE_NA),state.stateF);
  fill('f-status',uniq('status'),state.status);
  fill('f-plant',uniq('plant',HIDE_NA),state.plant);
  fill('f-resolution',uniq('resolution',v=>HIDE_NA(v)&&v!=='WIP'),state.resolution);
}
function populateSub(){
  let subs=[];
  if(state.category!=='All'&&SUBMAP[state.category]) subs=[...SUBMAP[state.category]].sort();
  else { const s=new Set(); Object.values(SUBMAP).forEach(set=>set.forEach(v=>s.add(v))); subs=[...s].sort(); }
  fill('f-subcat',subs,state.subcat);
}
function populateCustCascade(){
  let types, names;
  if(state.custname!=='All'&&CUST_NAME_TO_TYPE[state.custname]){
    types=[...CUST_NAME_TO_TYPE[state.custname]].sort();
  } else {
    types=uniq('customer_type');
  }
  if(state.customer!=='All'&&CUST_TYPE_TO_NAME[state.customer]){
    names=[...CUST_TYPE_TO_NAME[state.customer]].sort();
  } else {
    names=uniq('complaint_by');
  }
  fill('f-customer',types,state.customer);
  fill('f-custname',names,state.custname);
}

// prior period for KPI chips: the contiguous run of the same number of months
// immediately before the selection (hidden when selection spans gaps or hits the start)
function prevMonths(){
  const selM=MONTHS.filter(m=>selMonths.has(m));
  if(!selM.length)return null;
  const idx=selM.map(m=>MONTHS.indexOf(m));
  for(let i=1;i<idx.length;i++)if(idx[i]!==idx[i-1]+1)return null;
  const i0=idx[0];
  if(i0<idx.length)return null;
  const pidx=MONTHS.slice(i0-idx.length,i0);
  return {set:new Set(pidx),label:pidx.length===1?MLABEL[pidx[0]]:MLABEL[pidx[0]]+'–'+MLABEL[pidx[pidx.length-1]]};
}
// KPI trend chip: ▲/▼ % vs prior period, colored by whether the move is good
function chip(id,goodUp,cur,prev){
  const el=document.getElementById(id);
  if(prev==null||prev===0||!isFinite((cur-prev)/prev)){el.className='chip';el.textContent='';return;}
  const d=(cur-prev)/prev*100,up=d>=0,good=up===goodUp;
  el.className='chip on '+(good?'good':'bad');
  el.textContent=(up?'▲ ':'▼ ')+Math.abs(d).toFixed(1)+'%';
}
// ----------
/* vertical (or horizontal for indexAxis:y) token-tinted ramps for bars & area fills */
function grads(sctx,n,t1,t0){
  const c=(sctx&&sctx.chart&&sctx.chart.ctx)?sctx.chart.ctx:(sctx&&sctx.canvas?sctx.ctx:null);
  if(!c)return'rgba('+rgb(n)+','+t1+')';
  const horiz=sctx.chart&&sctx.chart.options&&sctx.chart.options.indexAxis==='y';
  const g=horiz?c.createLinearGradient(0,0,c.canvas.width,0):c.createLinearGradient(0,0,0,c.canvas.height);
  const r=rgb(n);
  g.addColorStop(0,'rgba('+r+','+t1+')');
  g.addColorStop(1,'rgba('+r+','+t0+')');
  return g;
}
// draws the running total in the doughnut hole + a small caption
const centerTxt={id:'ctr',afterDraw(c){
  const o=(c.config.options.plugins&&c.config.options.plugins.ctr)||{};
  const total=o.total||0;
  if(!total)return;
  const a=c.chartArea,x=(a.left+a.right)/2,y=(a.top+a.bottom)/2,ctx=c.ctx;
  ctx.save();
  ctx.textAlign='center';ctx.textBaseline='middle';
  ctx.font='700 20px system-ui, sans-serif';ctx.fillStyle=V('--text-1');
  ctx.fillText(total.toLocaleString(),x,y-7);
  ctx.font='600 10px system-ui, sans-serif';ctx.fillStyle=V('--text-3');
  ctx.fillText(o.label||'',x,y+13);
  ctx.restore();
}};
// ---------- chart factory ----------
function mkBar(id,labels,data,opts={}){
  if(charts[id])charts[id].destroy();
  charts[id]=new Chart(document.getElementById(id),{type:opts.horizontal?'bar':'bar',
    data:{labels,datasets:[{data,backgroundColor:opts.colors||COLORS[0],borderRadius:6,maxBarThickness:40}]},
    options:{indexAxis:opts.horizontal?'y':'x',responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>' '+c.parsed[opts.horizontal?'x':'y'].toLocaleString()}}},
      scales:{x:{grid:{display:!opts.horizontal},ticks:{autoSkip:false}},y:{beginAtZero:true,ticks:{precision:0}}}}});
}
function mkDonut(id,labels,data,cols,ctr){
  if(charts[id])charts[id].destroy();
  const mob=isMobile();
  charts[id]=new Chart(document.getElementById(id),{type:'doughnut',plugins:[centerTxt],
    data:{labels,datasets:[{data,backgroundColor:cols||COLORS,borderWidth:0}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'62%',
      plugins:{ctr:{total:ctr?data.reduce((a,b)=>a+b,0):0,label:ctr?ctr.label:''},
      legend:{position:mob?'bottom':'right',labels:{boxWidth:mob?10:12,padding:mob?6:8,font:{size:mob?10:11}}},
      tooltip:{callbacks:{label:c=>' '+c.label+': '+c.parsed.toLocaleString()}}}}});
}
function mkStacked(id,labels,datasets){
  if(charts[id])charts[id].destroy();
  const mob=isMobile();
  charts[id]=new Chart(document.getElementById(id),{type:'bar',
    data:{labels,datasets:datasets.map(d=>Object.assign({},d,{maxBarThickness:38}))},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:'top',labels:{boxWidth:mob?10:12,padding:mob?6:8,font:{size:mob?10:11}}}},
      scales:{x:{stacked:true,ticks:{font:{size:mob?10:12}}},y:{stacked:true,beginAtZero:true,ticks:{precision:0,font:{size:mob?10:12}}}}}});
}
function mkLines(id,labels,datasets){
  if(charts[id])charts[id].destroy();
  const mob=isMobile();
  charts[id]=new Chart(document.getElementById(id),{type:'line',
    data:{labels,datasets},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:'top',labels:{boxWidth:mob?10:14,padding:mob?6:8,font:{size:mob?10:12}}}},
      scales:{x:{ticks:{font:{size:mob?10:12}}},y:{beginAtZero:true,ticks:{precision:0,font:{size:mob?10:12}}}},
      elements:{line:{tension:.3,borderWidth:mob?2:3},point:{radius:mob?3:4,hoverRadius:mob?5:6}}}});
}

// ---------- main refresh ----------
function refresh(){
  syncHeaderUI();
  populateSub();
  const selM=MONTHS.filter(m=>selMonths.has(m));
  const w=buildWhere();
  const wd=buildWhere({defects:true});

  // KPIs
  const kpi=query("SELECT SUM(weight) as total,"+
    "SUM(CASE WHEN LOWER(status) LIKE '%closed%' THEN weight ELSE 0 END) as closed,"+
    "SUM(CASE WHEN LOWER(status) LIKE '%wip%' THEN weight ELSE 0 END) as wip,"+
    "ROUND(SUM(CASE WHEN settle_days>=0 THEN settle_days*weight ELSE 0 END)*1.0/"+
    "NULLIF(SUM(CASE WHEN settle_days>=0 THEN weight ELSE 0 END),0),1) as avg_tat"+
    " FROM complaints"+w)[0]||{};
  const total=kpi.total||0,closed=kpi.closed||0,wip=kpi.wip||0,avgTAT=kpi.avg_tat||0;
  const closureRate=total?Math.round(closed/total*1000)/10:0;

  // prior-period KPIs for the trend chips
  const pm=prevMonths();
  let pPrev=null;
  if(pm){
    const pIn=[...pm.set].map(m=>"'"+m+"'").join(',');
    const pv=query("SELECT SUM(weight) as t,"+
      "SUM(CASE WHEN LOWER(status) LIKE '%closed%' THEN weight ELSE 0 END) as c,"+
      "SUM(CASE WHEN LOWER(status) LIKE '%wip%' THEN weight ELSE 0 END) as w,"+
      "ROUND(SUM(CASE WHEN settle_days>=0 THEN settle_days*weight ELSE 0 END)*1.0/"+
      "NULLIF(SUM(CASE WHEN settle_days>=0 THEN weight ELSE 0 END),0),1) as avg_tat"+
      " FROM complaints"+buildWhere({months:false})+" AND month IN ("+pIn+")")[0]||{};
    pPrev={kVal:state.status==='All'?(pv.c||0):(pv.t||0),
      rate:(pv.t||0)?Math.round((pv.c||0)/(pv.t||0)*1000)/10:0,
      tat:pv.avg_tat||0, wip:pv.w||0, label:pm.label};
  }

  const kLabel=state.status==='All'?'Modules Serviced (Closed)':('Modules Serviced ('+state.status+')');
  document.getElementById('k-closed-label').textContent=kLabel;
  const kVal=state.status==='All'?closed:total;
  document.getElementById('k-closed').textContent=kVal.toLocaleString();
  document.getElementById('k-closed-note').textContent=pPrev
    ?('vs. '+pPrev.kVal.toLocaleString()+' · '+pPrev.label)
    :(selMonths.size===1?MLABEL[[...selMonths][0]]:'');
  chip('k-closed-chip',true,kVal,pPrev?pPrev.kVal:null);
  document.getElementById('k-closure').textContent=closureRate+'%';
  const closureNote=document.getElementById('k-closure-note');
  closureNote.textContent=closed.toLocaleString()+' closed of '+total.toLocaleString();
  closureNote.style.color=closureRate>=90?'var(--success)':closureRate>=70?'var(--warn-text)':'var(--danger)';
  chip('k-closure-chip',true,closureRate,pPrev?pPrev.rate:null);
  document.getElementById('k-tat').textContent=avgTAT;
  const tatNote=document.getElementById('k-tat-note');
  tatNote.textContent=avgTAT<=30?'Within 30-day SOP':'Exceeds 30-day SOP';
  tatNote.style.color=avgTAT<=30?'var(--success)':'var(--danger)';
  chip('k-tat-chip',false,avgTAT,pPrev?pPrev.tat:null);
  document.getElementById('k-wip').textContent=wip.toLocaleString();
  const wipNote=document.getElementById('k-wip-note');
  wipNote.textContent=wip>0?wip.toLocaleString()+' modules still open':'All resolved';
  wipNote.style.color=wip===0?'var(--success)':wip>100?'var(--danger)':'var(--warn-text)';
  chip('k-wip-chip',false,wip,pPrev?pPrev.wip:null);

  // ---- Top 3 problems ----
  const top3rows=query("SELECT subcategory,SUM(weight) as total FROM complaints"+wd+" GROUP BY subcategory ORDER BY total DESC LIMIT 3");
  const top3=top3rows.map(r=>r.subcategory);
  const badgesEl=document.getElementById('top3badges');badgesEl.innerHTML='';
  top3rows.forEach((r,i)=>{const d=document.createElement('div');d.className='badge b'+i;
    d.innerHTML=`<span class="rank" style="--rk:var(--c${i})">${i+1}</span>${r.subcategory} · <b>${r.total.toLocaleString()}</b>`;badgesEl.appendChild(d);});
  // trend of those top3 across selected months (respecting non-month filters)
  const wdTrend=buildWhere({defects:true,months:false});
  if(selM.length===1){
    const t3vals=top3.map(s=>{
      const r=query("SELECT SUM(weight) as t FROM complaints"+wdTrend+" AND month='"+selM[0]+"' AND subcategory='"+esc(s)+"'")[0];
      return r&&r.t?r.t:0;});
    mkBar('chTop3',top3,t3vals,{colors:s=>grads(s,'--c'+s.dataIndex,.95,.5)});
  } else {
    if(top3.length){
      const inList=top3.map(s=>"'"+esc(s)+"'").join(',');
      const trendRows=query("SELECT month,subcategory,SUM(weight) as total FROM complaints"+wdTrend+
        " AND subcategory IN ("+inList+") AND month IN ("+monthList()+") GROUP BY month,subcategory");
      const tm={};trendRows.forEach(r=>{if(!tm[r.subcategory])tm[r.subcategory]={};tm[r.subcategory][r.month]=r.total;});
      const t3data=top3.map((s,i)=>({label:s,borderColor:COLORS[i],backgroundColor:A('--c'+i,.2),
        data:selM.map(m=>(tm[s]&&tm[s][m])||0)}));
      mkLines('chTop3',selM.map(m=>MLABEL[m]),t3data);
    } else {
      mkLines('chTop3',selM.map(m=>MLABEL[m]),[{label:'No defects',data:selM.map(()=>0),borderColor:COLORS[0]}]);
    }
  }
  // ---- Defects by category ----
  const catRows=query("SELECT category,SUM(weight) as total FROM complaints"+wd+" GROUP BY category");
  const catMap={};catRows.forEach(r=>catMap[r.category]=r.total);
  const catLabels=CAT_ORDER.filter(c=>c!=='No Issue'&&catMap[c]);
  mkBar('chCat',catLabels,catLabels.map(c=>catMap[c]),{colors:s=>grads(s,'--c'+(s.dataIndex%COLORS.length),.95,.5)});
  // ---- Pareto ----
  const ps=query("SELECT subcategory,SUM(weight) as total FROM complaints"+wd+" GROUP BY subcategory ORDER BY total DESC LIMIT 12");
  mkBar('chPareto',ps.map(r=>r.subcategory),ps.map(r=>r.total),{horizontal:true,colors:s=>grads(s,'--c1',.95,.55)});

  // ---- Monthly closed vs WIP ----
  const monthlyRows=query("SELECT month,"+
    "SUM(CASE WHEN LOWER(status) LIKE '%closed%' THEN weight ELSE 0 END) as closed,"+
    "SUM(CASE WHEN LOWER(status) LIKE '%wip%' THEN weight ELSE 0 END) as wip"+
    " FROM complaints"+w+" GROUP BY month ORDER BY month");
  const mm={};monthlyRows.forEach(r=>mm[r.month]={closed:r.closed,wip:r.wip});
  mkStacked('chMonthly',selM.map(m=>MLABEL[m]),[
    {label:'Closed',data:selM.map(m=>(mm[m]&&mm[m].closed)||0),backgroundColor:V('--success'),borderRadius:4},
    {label:'WIP',data:selM.map(m=>(mm[m]&&mm[m].wip)||0),backgroundColor:V('--warning'),borderRadius:4}]);

  // ---- Category trend ----
  const ctRows=query("SELECT month,category,SUM(weight) as total FROM complaints"+wd+" GROUP BY month,category");
  const ctm={};ctRows.forEach(r=>{if(!ctm[r.category])ctm[r.category]={};ctm[r.category][r.month]=r.total;});
  const ctDatasets=catLabels.map((c,i)=>({label:c,backgroundColor:COLORS[i%COLORS.length],borderRadius:3,
    data:selM.map(m=>(ctm[c]&&ctm[c][m])||0)}));
  mkStacked('chCatTrend',selM.map(m=>MLABEL[m]),ctDatasets);

  // ---- Customer type ----
  const custRows=query("SELECT customer_type,SUM(weight) as total FROM complaints"+wd+" GROUP BY customer_type ORDER BY total DESC");
  mkBar('chCust',custRows.map(r=>r.customer_type),custRows.map(r=>r.total),{colors:s=>grads(s,'--c4',.95,.5)});
  // ---- Plant ----
  const plantRows=query("SELECT plant,SUM(weight) as total FROM complaints"+wd+
    " AND plant IS NOT NULL AND plant!='' AND LOWER(plant) NOT IN ('n/a','na') GROUP BY plant ORDER BY total DESC");
  mkDonut('chPlant',plantRows.map(r=>r.plant),plantRows.map(r=>r.total),null,{label:'MODULES'});
  // ---- Status ----
  const stRows=query("SELECT status,SUM(weight) as total FROM complaints"+wd+" GROUP BY status");
  mkDonut('chStatus',stRows.map(r=>r.status),stRows.map(r=>r.total),stRows.map(r=>/closed/i.test(r.status)?V('--success'):V('--warning')),{label:'DEFECTS'});
  // ---- States ----
  const stateRows=query("SELECT state,SUM(weight) as total FROM complaints"+wd+" GROUP BY state ORDER BY total DESC LIMIT 10");
  mkBar('chState',stateRows.map(r=>r.state),stateRows.map(r=>r.total),{horizontal:true,colors:s=>grads(s,'--c5',.95,.55)});
  // ---- TAT trend ----
  const tatRows=query("SELECT month,ROUND(SUM(CASE WHEN settle_days>=0 THEN settle_days*weight ELSE 0 END)*1.0/"+
    "NULLIF(SUM(CASE WHEN settle_days>=0 THEN weight ELSE 0 END),0),1) as avg_tat"+
    " FROM complaints"+w+" GROUP BY month ORDER BY month");
  const tatM={};tatRows.forEach(r=>tatM[r.month]=r.avg_tat||0);
  mkLines('chTATtrend',selM.map(m=>MLABEL[m]),[
    {label:'Avg TAT (days)',borderColor:COLORS[0],backgroundColor:s=>grads(s,'--c0',.3,.02),data:selM.map(m=>tatM[m]||0),fill:'origin'},
    {label:'30-day SOP',borderColor:V('--danger'),borderDash:[6,4],data:selM.map(()=>30),pointRadius:0,fill:false}]);
  // ---- Plant × category batch ----
  const batchRows=query("SELECT plant,category,SUM(weight) as total FROM complaints"+wd+
    " AND plant IS NOT NULL AND plant!='' AND LOWER(plant) NOT IN ('n/a','na') GROUP BY plant,category");
  const bpt={};batchRows.forEach(r=>bpt[r.plant]=(bpt[r.plant]||0)+r.total);
  const batchPlants=Object.entries(bpt).sort((a,b)=>b[1]-a[1]).map(x=>x[0]);
  const bm={};batchRows.forEach(r=>{if(!bm[r.category])bm[r.category]={};bm[r.category][r.plant]=r.total;});
  const batchDS=catLabels.map((c,i)=>({label:c,backgroundColor:COLORS[i%COLORS.length],borderRadius:3,
    data:batchPlants.map(p=>(bm[c]&&bm[c][p])||0)}));
  mkStacked('chBatch',batchPlants,batchDS.length?batchDS:[{label:'No defects',data:batchPlants.map(()=>0),backgroundColor:COLORS[0]}]);
  // ---- Customer × defect heatmap ----
  const heatRows=query("SELECT customer_type,category,SUM(weight) as total FROM complaints"+wd+" GROUP BY customer_type,category");
  const hct={};heatRows.forEach(r=>hct[r.customer_type]=(hct[r.customer_type]||0)+r.total);
  const custs=Object.entries(hct).sort((a,b)=>b[1]-a[1]).map(x=>x[0]);
  const hm={};let maxV=0;
  heatRows.forEach(r=>{if(!hm[r.customer_type])hm[r.customer_type]={};hm[r.customer_type][r.category]=r.total;if(r.total>maxV)maxV=r.total;});
  const hel=document.getElementById('heatmap');
  if(!custs.length||!catLabels.length){hel.innerHTML='<div class="hint">No data for current selection.</div>';}
  else{
    let html='<table><thead><tr><th></th>';
    catLabels.forEach(c=>{html+=`<th>${c}</th>`;});
    html+='</tr></thead><tbody>';
    custs.forEach(cu=>{
      html+=`<tr><th class="rowlbl">${cu}</th>`;
      catLabels.forEach(c=>{
        const v=(hm[cu]&&hm[cu][c])||0;
        const t=maxV?v/maxV:0;
        const bg=v?A('--c0',(0.12+t*0.85)):'var(--bg-app)';
        const fg=t>0.55?'var(--bg-surface)':'var(--text-1)';
        html+=`<td><div class="cell" style="background:${bg};color:${fg}" title="${cu} · ${c}: ${v.toLocaleString()}">${v?v.toLocaleString():''}</div></td>`;
      });
      html+='</tr>';
    });
    html+='</tbody></table>';
    hel.innerHTML=html;
  }

  renderTable();
}

// ---------- table ----------
function renderTable(){
  const SORT_COLS={month:1,serial:1,customer_type:1,state:1,category:1,subcategory:1,plant:1,status:1,complaint_no:1};
  const sortCol=SORT_COLS[sortK]?sortK:'month';
  const dir=sortDir===1?'ASC':'DESC';
  let searchCond='';
  if(search){const q=esc(search);searchCond=" AND (serial LIKE '%"+q+"%' OR project LIKE '%"+q+"%' OR complaint_no LIKE '%"+q+"%' OR subcategory LIKE '%"+q+"%')";}
  const base=" FROM complaints"+buildWhere()+" AND is_aggregate=0"+searchCond;
  totalTableRows=(query("SELECT COUNT(*) as cnt"+base)[0]||{}).cnt||0;
  const pages=Math.max(1,Math.ceil(totalTableRows/PAGE));
  if(page>=pages) page=Math.max(0,pages-1);
  const rows=query("SELECT month,serial,customer_type,state,category,subcategory,plant,status,complaint_no"+base+" ORDER BY "+sortCol+" "+dir+" LIMIT "+PAGE+" OFFSET "+(page*PAGE));
  const tb=document.getElementById('tbody');tb.innerHTML='';
  if(!rows.length){tb.innerHTML='<tr><td colspan="9" class="empty">No records match these filters</td></tr>';}
  rows.forEach(r=>{
    const tr=document.createElement('tr');
    const stcls=/wip/i.test(r.status)?'wip':'closed';
    tr.innerHTML=`<td>${MLABEL[r.month]||r.month}</td><td>${r.serial||'—'}</td>
      <td>${r.customer_type}</td><td>${r.state}</td><td>${r.category}</td><td>${r.subcategory}</td>
      <td>${r.plant}</td><td><span class="pill ${stcls}">${r.status}</span></td><td>${r.complaint_no||'—'}</td>`;
    tb.appendChild(tr);
  });
  document.querySelector('.tableScroll').scrollTop=0;
  document.getElementById('tcount').textContent=totalTableRows.toLocaleString()+' complaint records';
  document.getElementById('pginfo').textContent=`Page ${page+1} of ${pages}`;
  document.getElementById('prev').disabled=page===0;
  document.getElementById('next').disabled=page>=pages-1;
  document.getElementById('pgjump').max=pages;
}

// ---------- events ----------
document.getElementById('f-customer').onchange=e=>{state.customer=e.target.value;state.custname='All';page=0;populateCustCascade();refresh();};
document.getElementById('f-custname').onchange=e=>{state.custname=e.target.value;state.customer='All';page=0;populateCustCascade();refresh();};
document.getElementById('f-category').onchange=e=>{state.category=e.target.value;state.subcat='All';page=0;populateSub();refresh();};
document.getElementById('f-subcat').onchange=e=>{state.subcat=e.target.value;page=0;refresh();};
document.getElementById('f-state').onchange=e=>{state.stateF=e.target.value;page=0;refresh();};
document.getElementById('f-status').onchange=e=>{state.status=e.target.value;page=0;refresh();};
document.getElementById('f-plant').onchange=e=>{state.plant=e.target.value;page=0;refresh();};
document.getElementById('f-resolution').onchange=e=>{state.resolution=e.target.value;page=0;refresh();};
document.getElementById('reset').onclick=()=>{Object.assign(state,{customer:'All',custname:'All',category:'All',subcat:'All',stateF:'All',status:'All',plant:'All',resolution:'All'});selMonths=new Set(MONTHS);calOpen=false;hdrSearchOpen=false;search='';document.getElementById('search').value='';page=0;populateFilters();refresh();};
document.getElementById('rst-top').onclick=document.getElementById('reset').onclick;
document.getElementById('f-on').onclick=()=>{document.querySelector('.filters').scrollIntoView({behavior:'smooth',block:'center'});};
document.getElementById('search').oninput=e=>setSearch(e.target.value);
document.querySelectorAll('#tbl thead th').forEach(th=>th.onclick=()=>{const k=th.dataset.k;if(sortK===k)sortDir*=-1;else{sortK=k;sortDir=1;}renderTable();});
document.getElementById('prev').onclick=()=>{if(page>0){page--;renderTable();}};
document.getElementById('next').onclick=()=>{if((page+1)*PAGE<totalTableRows){page++;renderTable();}};
function jumpToPage(){const v=parseInt(document.getElementById('pgjump').value,10);if(!v||v<1)return;const pages=Math.ceil(totalTableRows/PAGE);page=Math.min(Math.max(v,1),pages)-1;document.getElementById('pgjump').value='';renderTable();}
document.getElementById('pgjumpbtn').onclick=jumpToPage;
document.getElementById('pgjump').onkeydown=e=>{if(e.key==='Enter')jumpToPage();};

// ---------- init ----------
(async()=>{
  try{
    const SQL=await initSqlJs({locateFile:f=>'https://cdn.jsdelivr.net/npm/sql.js@1.10.3/dist/'+f});
    const resp=await fetch('data.db');
    const total=+resp.headers.get('content-length')||0;
    const reader=resp.body.getReader();
    const chunks=[];let loaded=0;
    const logoFill=document.getElementById('logo-fill');
    const pct=document.getElementById('load-pct');
    while(true){
      const{done,value}=await reader.read();
      if(done)break;
      chunks.push(value);loaded+=value.length;
      if(total){const p=Math.round(loaded/total*100);logoFill.style.height=p+'%';pct.textContent=p+'%';}
    }
    logoFill.style.height='100%';pct.textContent='Building charts…';
    const buf=new Uint8Array(await new Blob(chunks).arrayBuffer());
    DB=new SQL.Database(buf);
    query("SELECT DISTINCT category,subcategory FROM complaints WHERE category!='No Issue'")
      .forEach(r=>(SUBMAP[r.category]=SUBMAP[r.category]||new Set()).add(r.subcategory));
    query("SELECT DISTINCT customer_type,complaint_by FROM complaints WHERE customer_type IS NOT NULL AND complaint_by IS NOT NULL AND customer_type!='' AND complaint_by!=''")
      .forEach(r=>{
        (CUST_TYPE_TO_NAME[r.customer_type]=CUST_TYPE_TO_NAME[r.customer_type]||new Set()).add(r.complaint_by);
        (CUST_NAME_TO_TYPE[r.complaint_by]=CUST_NAME_TO_TYPE[r.complaint_by]||new Set()).add(r.customer_type);
      });
    document.getElementById('loading').style.display='none';
    populateFilters();
    buildHeaderTools();
    refresh();
  }catch(err){
    document.getElementById('loading').innerHTML='<div style="color:var(--danger)">Failed to load data: '+err.message+'</div>';
  }
})();

// --- Filters: on-demand floating panel (prototype v2) ---
const ftBtn=document.getElementById('f-on');
const ftPanel=document.querySelector('.filters');
ftBtn.onclick=()=>{ftBtn.classList.toggle('open');ftPanel.classList.toggle('show');ftBtn.setAttribute('aria-expanded',ftPanel.classList.contains('show'));};
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&ftPanel.classList.contains('show')){ftPanel.classList.remove('show');ftBtn.classList.remove('open');ftBtn.setAttribute('aria-expanded','false');}});

// --- Re-render charts on resize (legend repositioning) ---
let resizeTimer;
window.addEventListener('resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>refresh(),250);});
</script>
</body>
</html>"""

out = HTML.replace("__FAVICON__", favicon_b64).replace("__HEADER_LOGO__", header_b64).replace("__HERO_BG__", hero_b64)
with open(os.path.join(FRONTEND_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(out)
print("Dashboard written: ../frontend/index.html (fetches data.db at runtime)")
