#!/usr/bin/env python3
"""
Premier Energies After-Sales — multi-month ingestion.

HOW TO USE:
1. Place this file in the same folder as your monthly Excel files
2. Run: python ingest.py
3. It will produce data.json in the same folder
4. Then run build_dashboard.py to generate the HTML

TO ADD A NEW MONTH:
- Add a new line to SOURCES list below
- Format: ("filename.xlsx", "Sheet Name", "YYYY-MM", eval_col_index, serial_col_index, action_col_index)
- Feb/Mar use eval_idx=12, serial_idx=14, action_idx=20
- Apr/May onwards use eval_idx=13, serial_idx=15, action_idx=21 (due to extra column inserted)

INSTALL REQUIREMENT:
pip install openpyxl
"""
import json
import os
from datetime import datetime
from openpyxl import load_workbook

# ── ADD NEW MONTHS HERE ──────────────────────────────────────────────────────
SOURCES = [
    ("Jan 26 - Daily & Monthly Analyzed Report.xlsx",   "Monthly Report Jan-26",         "2026-01", 13, 15, 21),
    ("Feb 26 - Daily & Monthly Analyzed Report.xlsx",   "Monthly Report Feb-26",         "2026-02", 12, 14, 20),
    ("Mar 26 - Daily & Monthly Analyzed Report.xlsx",   "Monthly Report Mar-26",          "2026-03", 12, 14, 20),
    ("April 26 - Daily & Monthly AnalyzedReport.xlsx",  "Monthly Report April-26 ",       "2026-04", 13, 15, 21),
    ("May 26 - Daily & Monthly Analyzed Report.xlsx",   "Monthly Report May-26 Cleaned",  "2026-05", 13, 15, 21),
    ("June 26 - Daily & Monthly Analyzed Report.xlsx",  " Monthly Report June-26",        "2026-06", 13, 15, 21),
    # ("Jun_26_-_Daily___Monthly_Analyzed_Report.xlsx", "Monthly Report Jun-26",          "2026-06", 13, 15, 21),
]
# ─────────────────────────────────────────────────────────────────────────────

def col_map(eval_idx):
    shift = 1 if eval_idx == 13 else 0
    return {
        "received_date": 0,
        "complaint_by":  2,
        "customer_type": 3,
        "project":       4,
        "status":        5,
        "complaint_no":  8,
        "reported_problem": 9,
        "location":      10,
        "state":         11,
        "evaluation":    eval_idx,
        "wp":            13 + shift,
        "serial":        14 + shift,
        "make_year":     15 + shift,
        "make_month":    16 + shift,
        "module_type":   17 + shift,
        "plant":         18 + shift,
        "action":        20 + shift,
        "resolution":    21 + shift,
        "settle_date":   22 + shift,
        "settle_days":   23 + shift,
        "visit_date":    25 + shift,
    }

# ── DEFECT NORMALIZATION MAP ─────────────────────────────────────────────────
# Format: "raw value in lowercase" -> ("Category", "Subcategory")
HIER = {
    # Junction Box Defects
    "cold soldering":               ("Junction Box Defects", "JB Cold Soldering"),
    "jb issue":                     ("Junction Box Defects", "JB Issue"),
    "jb issue - theft case":        ("Junction Box Defects", "JB Issue"),
    "jb deattached":                ("Junction Box Defects", "JB Issue"),
    "low generation":               ("Junction Box Defects", "JB Issue"),
    "jb burn & glass broken":       ("Junction Box Defects", "JB Issue"),
    "jb burn":                      ("Junction Box Defects", "JB Issue"),
    "jb remove":                    ("Junction Box Defects", "JB Issue"),
    "jb deattach":                  ("Junction Box Defects", "JB Issue"),
    "jb remove by extranal":        ("Junction Box Defects", "JB Issue"),
    "external connection fault":    ("Junction Box Defects", "JB Issue"),
    "jb & cable damege":            ("Junction Box Defects", "JB Issue"),
    # Ribbon Soldering Issue
    "tab lead burn":                ("Ribbon Soldering Issue", "Tab Lead Burn"),
    "improper ribbon soldering":    ("Ribbon Soldering Issue", "Improper Ribbon Soldering"),
    "backsheet burn":               ("Ribbon Soldering Issue", "Backsheet Burn"),
    "back sheet burn":              ("Ribbon Soldering Issue", "Backsheet Burn"),
    "string cold soldering":        ("Ribbon Soldering Issue", "String Cold Soldering"),
    "improper or poor soldering":   ("Ribbon Soldering Issue", "Improper Ribbon Soldering"),
    "sub string short circuit":     ("Ribbon Soldering Issue", "String Cold Soldering"),
    # Cell and Module Defects
    "hotspot":                      ("Cell and Module Defects", "Hotspot"),
    "multiple hotspot":             ("Cell and Module Defects", "Hotspot"),
    "cell crack":                   ("Cell and Module Defects", "Cell Crack"),
    "cell chip":                    ("Cell and Module Defects", "Cell Chip"),
    "cell contamination":           ("Cell and Module Defects", "Cell Contamination"),
    "module burn":                  ("Cell and Module Defects", "Module Burn"),
    "burn module":                  ("Cell and Module Defects", "Module Burn"),
    "burning":                      ("Cell and Module Defects", "Module Burn"),
    "burn modules & glass breakage at shorter side": ("Cell and Module Defects", "Module Burn"),
    "string busbar open":           ("Cell and Module Defects", "String Busbar Open"),
    "transparent backsheet melt down": ("Cell and Module Defects", "Transparent Backsheet Melt Down"),
    "air entrapment during the lamination process": ("Cell and Module Defects", "Air Entrapment during Lamination"),
    "forign particle - cell piece": ("Cell and Module Defects", "Foreign Particle - Cell Piece"),
    "foreign particle - cell piece":("Cell and Module Defects", "Foreign Particle - Cell Piece"),
    "burn spot":                    ("Cell and Module Defects", "Burn Spot"),
    "burn marks":                   ("Cell and Module Defects", "Burn Spot"),
    "burn marks visible":           ("Cell and Module Defects", "Burn Spot"),
    "cell damage":                  ("Cell and Module Defects", "Cell Crack"),
    "cell broken":                  ("Cell and Module Defects", "Cell Crack"),
    # Physical and External Damage
    "glass breakage":               ("Physical and External Damage", "Glass Breakage"),
    "glass broken":                 ("Physical and External Damage", "Glass Breakage"),
    "glass broken/burning":         ("Physical and External Damage", "Glass Breakage"),
    "broken":                       ("Physical and External Damage", "Glass Breakage"),
    "burn marks visible & glass brokage":       ("Physical and External Damage", "Glass Breakage"),
    "glass breakage and visible burn marks":    ("Physical and External Damage", "Glass Breakage"),
    "glass brakage & burn marks":               ("Physical and External Damage", "Glass Breakage"),
    "backsheet burn & glass broken":            ("Physical and External Damage", "Glass Breakage"),
    "back glass broken":                        ("Physical and External Damage", "Glass Breakage"),
    "front glass broken":                       ("Physical and External Damage", "Glass Breakage"),
    "front glass broken  & burning":            ("Physical and External Damage", "Glass Breakage"),
    "both side glass broken & burning":         ("Physical and External Damage", "Glass Breakage"),
    "both side glass broken":                   ("Physical and External Damage", "Glass Breakage"),
    "back glass broken & jb burning":           ("Physical and External Damage", "Glass Breakage"),
    "back glass broken with jb deattached":     ("Physical and External Damage", "Glass Breakage"),
    "back glass broken & burning":              ("Physical and External Damage", "Glass Breakage"),
    "glass breakage with burn spot":            ("Physical and External Damage", "Glass Breakage"),
    "module breakage":                          ("Physical and External Damage", "Module Breakage"),
    "module breakage & burn":                   ("Physical and External Damage", "Module Breakage"),
    "jb tampered & glass breakage":             ("Physical and External Damage", "Glass Breakage"),
    "backsheet scratches":          ("Physical and External Damage", "Backsheet Scratches"),
    "backsheet scratch":            ("Physical and External Damage", "Backsheet Scratches"),
    "mc4 connectors damaged":       ("Physical and External Damage", "MC4 Connectors Damaged"),
    "frame damage":                 ("Physical and External Damage", "Frame Damage"),
    "frame issue":                  ("Physical and External Damage", "Frame Damage"),
    "slight frame bow":             ("Physical and External Damage", "Frame Damage"),
    "frame bow":                    ("Physical and External Damage", "Frame Damage"),
    "damage & burning":             ("Physical and External Damage", "Other Physical Damage"),
    "module damaged":               ("Physical and External Damage", "Other Physical Damage"),
    "module broken":                ("Physical and External Damage", "Other Physical Damage"),
    "hit mark observed":            ("Physical and External Damage", "Other Physical Damage"),
    "externel force applied":       ("Physical and External Damage", "Other Physical Damage"),
    "external force applied":       ("Physical and External Damage", "Other Physical Damage"),
    "damage":                       ("Physical and External Damage", "Other Physical Damage"),
    "broken module":                ("Physical and External Damage", "Other Physical Damage"),
    "frame broken":                 ("Physical and External Damage", "Frame Damage"),
    # Transit Damage
    "transit breakage":             ("Transit Damage", "Transit Breakage"),
    "transit damage":               ("Transit Damage", "Transit Breakage"),
    # Natural Disaster
    "natural disaster":             ("Physical and External Damage", "Natural Disaster"),
    # Aesthetic
    "aesthetic":                    ("Aesthetic", "Aesthetic"),
    "cleaning issue":               ("Aesthetic", "Aesthetic"),
    "asthetic issue":               ("Aesthetic", "Aesthetic"),
    # No Issue
    "no issue":                     ("No Issue", "No Issue"),
    "no issue found":               ("No Issue", "No Issue"),
    "not found":                    ("No Issue", "No Issue"),
    "no hotspot":                   ("No Issue", "No Issue"),
}
# ─────────────────────────────────────────────────────────────────────────────

def norm_serial(v):
    if v is None: return ""
    s = str(v).strip()
    return "" if s.lower() in ("n/a", "na", "none", "nan", "") else s

def clean(v):
    return "" if v is None else str(v).strip()

def fmt_date(v):
    if v is None: return ""
    s = str(v)
    return s.split(" ")[0] if " " in s else s

def calc_tat(received_raw, settle_raw):
    if received_raw is None or settle_raw is None:
        return None
    try:
        if isinstance(received_raw, datetime):
            d1 = received_raw
        else:
            d1 = datetime.strptime(str(received_raw).split(" ")[0], "%Y-%m-%d")
        if isinstance(settle_raw, datetime):
            d2 = settle_raw
        else:
            d2 = datetime.strptime(str(settle_raw).split(" ")[0], "%Y-%m-%d")
        diff = (d2 - d1).days
        return diff if diff >= 0 else None
    except (ValueError, TypeError):
        return None

unmapped = {}
rows = []

for fname, sheet, month, eval_idx, serial_idx, action_idx in SOURCES:
    if not os.path.exists(fname):
        print(f"WARNING: {fname} not found — skipping")
        continue
    print(f"Reading {fname} → sheet '{sheet}'...")
    wb = load_workbook(fname, read_only=True)
    ws = wb[sheet]
    cm = col_map(eval_idx)
    agg = {}

    for row in ws.iter_rows(min_row=2, values_only=True):
        v = list(row)
        if len(v) <= cm["serial"]: continue
        raw_eval = clean(v[cm["evaluation"]])
        if not raw_eval and not norm_serial(v[cm["serial"]]): continue

        key_eval = raw_eval.lower()
        mapped = HIER.get(key_eval)
        serial = norm_serial(v[cm["serial"]])

        if mapped is None:
            unmapped[raw_eval] = unmapped.get(raw_eval, 0) + 1
            category, subcat = ("Unmapped", raw_eval)
        else:
            category, subcat = mapped

        rec = {
            "month":         month,
            "serial":        serial,
            "complaint_by":  clean(v[cm["complaint_by"]]) or "Unknown",
            "customer_type": clean(v[cm["customer_type"]]) or "Unknown",
            "project":       clean(v[cm["project"]]) or "Unknown",
            "state":         clean(v[cm["state"]]) or "Unknown",
            "status":        clean(v[cm["status"]]) or "Unknown",
            "plant":         clean(v[cm["plant"]]) or "Unknown",
            "module_type":   clean(v[cm["module_type"]]) or "Unknown",
            "evaluation_raw":raw_eval,
            "category":      category,
            "subcategory":   subcat,
            "complaint_no":  clean(v[cm["complaint_no"]]),
            "action":        clean(v[cm["action"]]),
            "resolution":    clean(v[cm["resolution"]]),
            "wp":            clean(v[cm["wp"]]),
            "make_year":     clean(v[cm["make_year"]]),
            "location":      clean(v[cm["location"]]),
            "settle_days":   calc_tat(v[cm["received_date"]], v[cm["settle_date"]]),
            "visit_date":    fmt_date(v[cm["visit_date"]]),
            "received_date": fmt_date(v[cm["received_date"]]),
            "weight":        1,
        }

        # Collapse large blank-serial No-Issue blocks into single aggregate rows
        if category == "No Issue" and not serial:
            akey = (rec["month"], rec["project"], rec["customer_type"],
                    rec["state"], rec["plant"], rec["module_type"])
            if akey not in agg:
                agg[akey] = dict(rec)
                agg[akey]["weight"] = 0
                agg[akey]["is_aggregate"] = True
            agg[akey]["weight"] += 1
        else:
            rec["is_aggregate"] = False
            rows.append(rec)

    for akey, arec in agg.items():
        if arec["weight"] >= 50:
            rows.append(arec)
        else:
            base = dict(arec)
            w = base.pop("weight")
            base["weight"] = 1
            base["is_aggregate"] = False
            for _ in range(w):
                rows.append(dict(base))
    wb.close()

print(f"\nTotal embedded rows: {len(rows):,}")
print(f"True module count (weighted): {sum(r['weight'] for r in rows):,}")

if unmapped:
    print("\n!! UNMAPPED values — add these to HIER dict before building dashboard:")
    for k, c in sorted(unmapped.items(), key=lambda x: -x[1]):
        print(f"   '{k}': {c} occurrences")
else:
    print("All evaluation values mapped cleanly.")

from collections import Counter
mc = Counter()
for r in rows:
    mc[r["month"]] += r["weight"]
print("\nPer-month counts:")
for m in sorted(mc):
    print(f"   {m}: {mc[m]:,}")

with open("data.json", "w") as f:
    json.dump(rows, f, separators=(",", ":"))
print("\nWrote data.json — now run build_dashboard.py")
