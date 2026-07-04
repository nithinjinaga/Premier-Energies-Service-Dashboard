#!/usr/bin/env python3
"""
Premier Energies After-Sales Dashboard — Builder

HOW TO USE:
1. Run ingest.py first to produce data.json
2. Then run this script: python build_dashboard.py
3. Outputs index.html (dashboard UI) — data.json is fetched at runtime

TO ADD A NEW MONTH:
- Update the MONTHS and MLABEL constants in the HTML template below (search for const MONTHS)
- The data itself comes from ingest.py, not this file

INSTALL REQUIREMENT:
No extra packages needed beyond standard Python
"""

with open("favicon_b64.txt", encoding="utf-8") as f:
    favicon_b64 = f.read().strip()

with open("header_b64.txt", encoding="utf-8") as f:
    header_b64 = f.read().strip()

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dashboard 2026</title>
<link rel="icon" type="image/png" href="data:image/png;base64,__FAVICON__">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
:root{
  --bg:#f5f5f7; --panel:#ffffff; --panel2:#f5f5f7; --line:#e5e5e7;
  --txt:#1d1d1f; --txt2:#86868b; --accent:#0071e3; --accent2:#ff9500;
  --good:#34c759; --bad:#ff3b30; --warn:#ff9500;
  --c0:#3266ad;--c1:#e87f3a;--c2:#34c759;--c3:#ff3b30;--c4:#af52de;--c5:#ff6482;--c6:#00c7be;--c7:#ff9500;
  --radius:12px; --gap:16px;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--txt);font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:14px;padding:20px;line-height:1.5}
.wrap{max-width:1600px;margin:0 auto}
header{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px;margin-bottom:var(--gap)}
header h1{font-size:22px;font-weight:600}
header .sub{color:var(--txt2);font-size:13px;margin-top:2px}
.months{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.mbtn{padding:8px 16px;border:1px solid var(--line);background:var(--panel);color:var(--txt2);border-radius:8px;cursor:pointer;font-size:13px;font-weight:500;transition:.15s}
.mbtn.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.mbtn:hover{border-color:var(--accent)}
.mode-toggle{display:inline-flex;border:1px solid var(--line);border-radius:8px;overflow:hidden;margin-right:6px;font-size:12px}
.mode-toggle span{padding:6px 12px;cursor:pointer;color:var(--txt2);transition:.15s;user-select:none}
.mode-toggle span.active{background:var(--accent);color:#fff}
.filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;background:var(--panel);padding:16px;border-radius:var(--radius);margin-bottom:var(--gap);border:1px solid var(--line)}
.fg{display:flex;flex-direction:column;gap:4px}
.fg label{font-size:11px;color:var(--txt2);text-transform:uppercase;letter-spacing:.5px;font-weight:600}
.fg select{padding:8px 10px;background:var(--panel);color:var(--txt);border:1px solid #d2d2d7;border-radius:8px;font-size:13px;cursor:pointer}
.fg select:focus{outline:none;border-color:var(--accent)}
.resetbtn{align-self:flex-end;padding:8px 14px;background:var(--panel);color:var(--accent);border:1px solid #d2d2d7;border-radius:8px;cursor:pointer;font-size:13px;height:36px;font-weight:500}
.resetbtn:hover{background:#f0f0f2}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:var(--gap);margin-bottom:var(--gap)}
.kpi{background:var(--panel);padding:20px;border-radius:var(--radius);border:1px solid var(--line);position:relative;overflow:hidden}
.kpi::before{content:'';position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--accent)}
.kpi.amber::before{background:var(--accent2)}
.kpi.red::before{background:var(--bad)}
.kpi .label{font-size:12px;color:var(--txt2);text-transform:uppercase;letter-spacing:.5px;font-weight:600;margin-bottom:8px}
.kpi .val{font-size:30px;font-weight:600;letter-spacing:-1px}
.kpi .note{font-size:12px;color:var(--txt2);margin-top:4px}
.section-title{font-size:15px;font-weight:600;color:var(--txt);margin:8px 0 12px}
.grid{display:grid;gap:var(--gap);margin-bottom:var(--gap)}
.g2{grid-template-columns:repeat(auto-fit,minmax(440px,1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(320px,1fr))}
.card{background:var(--panel);padding:20px;border-radius:var(--radius);border:1px solid var(--line)}
.card h3{font-size:13px;font-weight:600;margin-bottom:4px}
.card .hint{font-size:11px;color:var(--txt2);margin-bottom:14px}
.card.span2{grid-column:span 2}
.chartbox{position:relative;height:300px}
.chartbox.tall{height:340px}
.toptrend{border:1px solid var(--accent);box-shadow:0 0 0 1px rgba(0,113,227,.15)}
.badges{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.badge{padding:5px 12px;border-radius:20px;font-size:12px;font-weight:600;display:flex;align-items:center;gap:6px;color:#fff}
.badge .rank{background:rgba(255,255,255,.3);border-radius:50%;width:18px;height:18px;display:flex;align-items:center;justify-content:center;font-size:11px}
.b0{background:var(--c0)}.b1{background:var(--c1)}.b2{background:var(--c2)}
table{width:100%;border-collapse:collapse;font-size:12.5px}
thead th{text-align:left;padding:8px 10px;background:var(--panel2);border-bottom:1px solid var(--line);color:var(--txt2);font-size:11px;text-transform:uppercase;letter-spacing:.3px;cursor:pointer;white-space:nowrap;user-select:none;font-weight:600}
thead th:hover{color:var(--txt)}
tbody td{padding:8px 10px;border-bottom:1px solid #f0f0f2}
tbody tr:hover{background:#fafafa}
.pill{padding:2px 9px;border-radius:6px;font-size:11px;font-weight:600}
.pill.closed{background:#f0fff4;color:var(--good)}
.pill.wip{background:#fff8f0;color:var(--warn)}
.tablebar{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;flex-wrap:wrap;gap:8px}
.tablebar input{padding:8px 12px;background:var(--panel);border:1px solid #d2d2d7;border-radius:8px;color:var(--txt);font-size:13px;min-width:240px}
.pager{display:flex;gap:8px;align-items:center;margin-top:12px;justify-content:flex-end;color:var(--txt2);font-size:12px}
.pager button{padding:5px 12px;background:var(--panel);border:1px solid #d2d2d7;border-radius:8px;color:var(--accent);cursor:pointer}
.pager button:disabled{opacity:.4;cursor:not-allowed}
.tableScroll{overflow-x:auto}
footer{color:var(--txt2);font-size:11px;text-align:center;padding:16px 0}
.note-box{background:#fff8f0;border:1px solid #ffd9a8;border-radius:8px;padding:10px 14px;font-size:12px;color:#86868b;margin-bottom:var(--gap)}
.heatmap{height:340px;overflow:auto}
.heatmap table{border-collapse:separate;border-spacing:3px}
.heatmap th{background:transparent;text-transform:none;letter-spacing:0;cursor:default;font-size:11px;padding:4px 6px;color:var(--txt2);text-align:center;vertical-align:bottom}
.heatmap th.rowlbl{text-align:right;white-space:nowrap;font-weight:600;color:var(--txt)}
.heatmap td{padding:0;border:none}
.heatmap .cell{min-width:54px;height:40px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:600;transition:.15s}
.heatmap .cell:hover{outline:2px solid var(--accent)}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div>
      <h1><img src="data:image/png;base64,__HEADER_LOGO__" alt="Premier Energies" style="height:32px;vertical-align:middle;margin-right:14px"> AFTER SALES SERVICE DASHBOARD</h1>
      <div class="sub">Field service &amp; module defect tracking · Jan–Jun 2026</div>
    </div>
    <div class="months" id="months"></div>
  </header>

  <div class="note-box" id="march-note" style="display:none">
    Note: March includes a large single-site inspection block (Ayana, ~178K modules, all "No Issue"). KPIs and charts exclude that block from defect calculations so charts stay readable.
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

  <div class="kpis">
    <div class="kpi"><div class="label">Modules Serviced (Closed)</div><div class="val" id="k-closed">0</div><div class="note" id="k-closed-note"></div></div>
    <div class="kpi amber"><div class="label">Closure Rate</div><div class="val" id="k-closure">0%</div><div class="note" id="k-closure-note"></div></div>
    <div class="kpi red"><div class="label">Avg TAT (days)</div><div class="val" id="k-tat">0</div><div class="note" id="k-tat-note"></div></div>
    <div class="kpi"><div class="label">Open (WIP)</div><div class="val" id="k-wip">0</div><div class="note" id="k-wip-note">awaiting resolution</div></div>
  </div>

  <div class="card toptrend" style="margin-bottom:var(--gap)">
    <h3>Top 3 Problems — Trend</h3>
    <div class="hint">The 3 largest defect types for the current month selection, tracked across all months. Recalculates as you change filters.</div>
    <div class="badges" id="top3badges"></div>
    <div class="chartbox tall"><canvas id="chTop3"></canvas></div>
  </div>

  <div class="section-title">Defect Breakdown</div>
  <div class="grid g2">
    <div class="card"><h3>Defects by Category</h3><div class="hint">Excludes "No Issue". Where to focus process-improvement effort.</div><div class="chartbox"><canvas id="chCat"></canvas></div></div>
    <div class="card"><h3>Top Defect Sub-categories (Pareto)</h3><div class="hint">80/20 view — the few defect types driving most of the volume.</div><div class="chartbox"><canvas id="chPareto"></canvas></div></div>
  </div>

  <div class="section-title">Segments</div>
  <div class="grid g3">
    <div class="card"><h3>By Customer Type</h3><div class="hint">Which segments generate defect load.</div><div class="chartbox"><canvas id="chCust"></canvas></div></div>
    <div class="card"><h3>By Manufacturing Plant</h3><div class="hint">Defect attribution by plant.</div><div class="chartbox"><canvas id="chPlant"></canvas></div></div>
    <div class="card"><h3>Status (Closed vs WIP)</h3><div class="hint">Resolution progress.</div><div class="chartbox"><canvas id="chStatus"></canvas></div></div>
  </div>

  <div class="grid g2">
    <div class="card"><h3>Top States by Defects</h3><div class="hint">Geographic concentration — where to position field teams.</div><div class="chartbox tall"><canvas id="chState"></canvas></div></div>
    <div class="card"><h3>Defect Resolution Timeline</h3><div class="hint">Average TAT (days) per month — is resolution speed improving?</div><div class="chartbox tall"><canvas id="chTATtrend"></canvas></div></div>
  </div>

  <div class="section-title">Production &amp; Customer Analysis</div>
  <div class="grid g2">
    <div class="card"><h3>Top Defects by Production Batch</h3><div class="hint">Defect category mix per manufacturing plant — which defect dominates each batch.</div><div class="chartbox tall"><canvas id="chBatch"></canvas></div></div>
    <div class="card"><h3>Customer × Defect Heatmap</h3><div class="hint">Defect concentration by customer type. Darker = more defects.</div><div id="heatmap" class="heatmap"></div></div>
  </div>

  <div class="section-title">Volume &amp; Trend</div>
  <div class="grid g2">
    <div class="card"><h3>Monthly Closed vs WIP</h3><div class="hint">Resolution progress per month — closed and open modules.</div><div class="chartbox"><canvas id="chMonthly"></canvas></div></div>
    <div class="card"><h3>Defect Category Trend</h3><div class="hint">How each category moves month to month.</div><div class="chartbox"><canvas id="chCatTrend"></canvas></div></div>
  </div>

  <div class="section-title">Module-level Records</div>
  <div class="card">
    <div class="tablebar">
      <div class="hint" id="tcount" style="margin:0"></div>
      <input id="search" placeholder="Search serial, site, complaint no…">
    </div>
    <div class="tableScroll">
      <table id="tbl">
        <thead><tr>
          <th data-k="month">Month</th><th data-k="serial">Serial</th><th data-k="project">Site</th>
          <th data-k="customer_type">Customer</th><th data-k="state">State</th>
          <th data-k="category">Category</th><th data-k="subcategory">Sub-category</th>
          <th data-k="plant">Plant</th><th data-k="status">Status</th>
          <th data-k="complaint_no">Complaint No.</th>
        </tr></thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>
    <div class="pager"><span id="pginfo"></span>
      <input type="number" id="pgjump" min="1" style="width:54px;padding:5px 6px;border:1px solid #d2d2d7;border-radius:6px;text-align:center" placeholder="#">
      <button id="pgjumpbtn">Go</button>
      <button id="prev">Prev</button><button id="next">Next</button></div>
  </div>

</div>

<div id="loading" style="position:fixed;inset:0;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:9999">
  <div style="position:relative;width:96px;height:96px;margin-bottom:20px">
    <img src="data:image/png;base64,__FAVICON__" style="position:absolute;inset:0;width:100%;height:100%;object-fit:contain;filter:grayscale(1) opacity(0.2)">
    <div style="position:absolute;left:0;right:0;bottom:0;height:0%;overflow:hidden;transition:height .3s" id="logo-fill">
      <img src="data:image/png;base64,__FAVICON__" style="position:absolute;bottom:0;left:0;width:96px;height:96px;object-fit:contain">
    </div>
  </div>
  <div style="font-size:15px;color:var(--txt);font-weight:600;margin-bottom:6px">Loading dashboard…</div>
  <div id="load-pct" style="font-size:13px;color:var(--txt2)">0%</div>
</div>
<script>
let RAW = [];
const MONTHS = ["2026-01","2026-02","2026-03","2026-04","2026-05","2026-06"];
const MLABEL = {"2026-01":"Jan-26","2026-02":"Feb-26","2026-03":"Mar-26","2026-04":"Apr-26","2026-05":"May-26","2026-06":"Jun-26"};
const CAT_ORDER = ["Junction Box Defects","Ribbon Soldering Issue","Cell and Module Defects","Physical and External Damage","Transit Damage","Aesthetic","No Issue","Inspection"];
const COLORS = ['#3266ad','#e87f3a','#34c759','#ff3b30','#af52de','#ff6482','#00c7be','#ff9500'];
Chart.defaults.color='#86868b';Chart.defaults.borderColor='#e5e5e7';Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif";

// ---------- state ----------
let selMonths = new Set(MONTHS);
const state={customer:'All',custname:'All',category:'All',subcat:'All',stateF:'All',status:'All',plant:'All',resolution:'All'};
let sortK='month',sortDir=1,page=0,search='',lastPages=1;
const PAGE=50;
const charts={};

const isDefect=r=>r.category!=='No Issue'&&!(r.category==='Inspection'&&r.subcategory!=='Issue Found');
const W=r=>r.weight||1;

// ---------- maps built after data loads ----------
const SUBMAP={};
const CUST_TYPE_TO_NAME={};
const CUST_NAME_TO_TYPE={};

// ---------- month buttons ----------
let monthMode='single';
const monthsEl=document.getElementById('months');
function renderMonthBtns(){
  monthsEl.innerHTML='';
  const tog=document.createElement('div');
  tog.className='mode-toggle';
  ['Single','Compare'].forEach(label=>{
    const s=document.createElement('span');
    s.textContent=label;
    const key=label.toLowerCase();
    if(monthMode===key) s.classList.add('active');
    s.onclick=()=>{monthMode=key;if(key==='single'){selMonths=new Set(MONTHS);}refresh();};
    tog.appendChild(s);
  });
  monthsEl.appendChild(tog);
  const all=document.createElement('button');
  all.className='mbtn'+(selMonths.size===MONTHS.length?' active':'');
  all.textContent='All';
  all.onclick=()=>{selMonths=new Set(MONTHS);refresh();};
  monthsEl.appendChild(all);
  MONTHS.forEach(m=>{
    const b=document.createElement('button');
    b.className='mbtn'+(selMonths.has(m)?' active':'');
    b.textContent=MLABEL[m];
    b.onclick=()=>{
      if(monthMode==='single'){
        selMonths=new Set([m]);
      } else {
        if(selMonths.has(m)) selMonths.delete(m); else selMonths.add(m);
        if(selMonths.size===0) selMonths.add(m);
      }
      refresh();
    };
    monthsEl.appendChild(b);
  });
}

// ---------- filter population ----------
function fill(id,vals,cur){
  const s=document.getElementById(id);
  s.innerHTML='';
  ['All',...vals].forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;if(v===cur)o.selected=true;s.appendChild(o);});
}
const HIDE_NA=v=>!/^(n\/?a|na)$/i.test(v);
function uniq(key,filter){const vals=[...new Set(RAW.map(r=>r[key]).filter(Boolean))].sort();return filter?vals.filter(filter):vals;}
function populateFilters(){
  populateCustCascade();
  fill('f-category',CAT_ORDER.filter(c=>c!=='No Issue'&&RAW.some(r=>r.category===c)),state.category);
  populateSub();
  fill('f-state',uniq('state',HIDE_NA),state.stateF);
  fill('f-status',uniq('status'),state.status);
  fill('f-plant',uniq('plant',HIDE_NA),state.plant);
  fill('f-resolution',uniq('resolution',HIDE_NA),state.resolution);
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

// ---------- filtering ----------
function monthFiltered(){ return RAW.filter(r=>selMonths.has(r.month)); }
function applyAll(rows){
  return rows.filter(r=>
    (state.customer==='All'||r.customer_type===state.customer)&&
    (state.custname==='All'||r.complaint_by===state.custname)&&
    (state.category==='All'||r.category===state.category)&&
    (state.subcat==='All'||r.subcategory===state.subcat)&&
    (state.stateF==='All'||r.state===state.stateF)&&
    (state.status==='All'||r.status===state.status)&&
    (state.plant==='All'||r.plant===state.plant)&&
    (state.resolution==='All'||r.resolution===state.resolution)
  );
}
// for KPIs we want inspected (incl No Issue) under non-defect filters;
// when a defect category/subcat filter is active, inspected==defects naturally.
function sumW(rows){return rows.reduce((a,r)=>a+W(r),0);}

// ---------- aggregation helpers ----------
function groupSum(rows,key){const m={};rows.forEach(r=>{m[r[key]]=(m[r[key]]||0)+W(r);});return m;}

// ---------- chart factory ----------
function mkBar(id,labels,data,opts={}){
  if(charts[id])charts[id].destroy();
  charts[id]=new Chart(document.getElementById(id),{type:opts.horizontal?'bar':'bar',
    data:{labels,datasets:[{data,backgroundColor:opts.colors||COLORS[0],borderRadius:4,maxBarThickness:46}]},
    options:{indexAxis:opts.horizontal?'y':'x',responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>' '+c.parsed[opts.horizontal?'x':'y'].toLocaleString()}}},
      scales:{x:{grid:{display:!opts.horizontal},ticks:{autoSkip:false}},y:{beginAtZero:true,ticks:{precision:0}}}}});
}
function mkDonut(id,labels,data){
  if(charts[id])charts[id].destroy();
  charts[id]=new Chart(document.getElementById(id),{type:'doughnut',
    data:{labels,datasets:[{data,backgroundColor:COLORS,borderColor:'#ffffff',borderWidth:2}]},
    options:{responsive:true,maintainAspectRatio:false,cutout:'58%',
      plugins:{legend:{position:'right',labels:{boxWidth:12,padding:8,font:{size:11}}},
      tooltip:{callbacks:{label:c=>' '+c.label+': '+c.parsed.toLocaleString()}}}}});
}
function mkStacked(id,labels,datasets){
  if(charts[id])charts[id].destroy();
  charts[id]=new Chart(document.getElementById(id),{type:'bar',
    data:{labels,datasets},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:'top',labels:{boxWidth:12,font:{size:11}}}},
      scales:{x:{stacked:true},y:{stacked:true,beginAtZero:true,ticks:{precision:0}}}}});
}
function mkLines(id,labels,datasets){
  if(charts[id])charts[id].destroy();
  charts[id]=new Chart(document.getElementById(id),{type:'line',
    data:{labels,datasets},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{position:'top',labels:{boxWidth:14,font:{size:12}}}},
      scales:{y:{beginAtZero:true,ticks:{precision:0}}},
      elements:{line:{tension:.3,borderWidth:3},point:{radius:4,hoverRadius:6}}}});
}

// ---------- main refresh ----------
function refresh(){
  renderMonthBtns();
  document.getElementById('march-note').style.display=selMonths.has('2026-03')?'block':'none';
  populateSub();

  const mrows=monthFiltered();
  const filtered=applyAll(mrows);              // respects all dropdowns
  const defects=filtered.filter(isDefect);
  const selM=MONTHS.filter(m=>selMonths.has(m));

  // KPIs
  const closed=sumW(filtered.filter(r=>/closed/i.test(r.status)));
  const wip=sumW(filtered.filter(r=>/wip/i.test(r.status)));
  const total=closed+wip;
  const closureRate=total?Math.round(closed/total*1000)/10:0;
  const durations=filtered.filter(r=>r.settle_days&&r.settle_days>0);
  const avgTAT=durations.length?Math.round(durations.reduce((a,r)=>a+(r.settle_days*W(r)),0)/sumW(durations)*10)/10:0;

  document.getElementById('k-closed').textContent=closed.toLocaleString();
  document.getElementById('k-closed-note').textContent=[...selMonths].sort().map(m=>MLABEL[m]).join(', ');
  document.getElementById('k-closure').textContent=closureRate+'%';
  const closureNote=document.getElementById('k-closure-note');
  closureNote.textContent=closed.toLocaleString()+' closed of '+total.toLocaleString();
  closureNote.style.color=closureRate>=90?'var(--good)':closureRate>=70?'var(--warn)':'var(--bad)';
  document.getElementById('k-tat').textContent=avgTAT;
  const tatNote=document.getElementById('k-tat-note');
  tatNote.textContent=avgTAT<=30?'Within 30-day SOP':'Exceeds 30-day SOP';
  tatNote.style.color=avgTAT<=30?'var(--good)':'var(--bad)';
  document.getElementById('k-wip').textContent=wip.toLocaleString();
  const wipNote=document.getElementById('k-wip-note');
  wipNote.textContent=wip>0?wip.toLocaleString()+' modules still open':'All resolved';
  wipNote.style.color=wip===0?'var(--good)':wip>100?'var(--bad)':'var(--warn)';

  // ---- Top 3 problems (by subcategory, current selection) ----
  const subSum=groupSum(defects,'subcategory');
  const top3=Object.entries(subSum).sort((a,b)=>b[1]-a[1]).slice(0,3).map(x=>x[0]);
  const badgesEl=document.getElementById('top3badges');badgesEl.innerHTML='';
  top3.forEach((s,i)=>{const d=document.createElement('div');d.className='badge b'+i;
    d.innerHTML=`<span class="rank">${i+1}</span>${s} · ${subSum[s].toLocaleString()}`;badgesEl.appendChild(d);});
  // trend of those top3 across selected months (respecting non-month filters)
  const baseForTrend=applyAll(RAW).filter(isDefect);
  if(selM.length===1){
    const t3vals=top3.map(s=>sumW(baseForTrend.filter(r=>r.month===selM[0]&&r.subcategory===s)));
    mkBar('chTop3',top3,t3vals,{colors:top3.map((_,i)=>COLORS[i])});
  } else {
    const t3data=top3.map((s,i)=>({label:s,borderColor:COLORS[i],backgroundColor:COLORS[i]+'33',
      data:selM.map(m=>sumW(baseForTrend.filter(r=>r.month===m&&r.subcategory===s)))}));
    mkLines('chTop3',selM.map(m=>MLABEL[m]),t3data.length?t3data:[{label:'No defects',data:selM.map(()=>0),borderColor:COLORS[0]}]);
  }

  // ---- Defects by category ----
  const catSum=groupSum(defects,'category');
  const catLabels=CAT_ORDER.filter(c=>c!=='No Issue'&&catSum[c]);
  mkBar('chCat',catLabels,catLabels.map(c=>catSum[c]),{colors:catLabels.map((_,i)=>COLORS[i%COLORS.length])});

  // ---- Pareto of subcategories ----
  const ps=Object.entries(subSum).sort((a,b)=>b[1]-a[1]).slice(0,12);
  mkBar('chPareto',ps.map(x=>x[0]),ps.map(x=>x[1]),{horizontal:true,colors:'#f59e0b'});

  // ---- Monthly closed vs WIP ----
  const allByM=applyAll(RAW);
  const closedByM=selM.map(m=>sumW(allByM.filter(r=>r.month===m&&/closed/i.test(r.status))));
  const wipByM=selM.map(m=>sumW(allByM.filter(r=>r.month===m&&/wip/i.test(r.status))));
  mkStacked('chMonthly',selM.map(m=>MLABEL[m]),[
    {label:'Closed',data:closedByM,backgroundColor:COLORS[0],borderRadius:4},
    {label:'WIP',data:wipByM,backgroundColor:COLORS[1],borderRadius:4},
  ]);

  // ---- Category trend (stacked across months) ----
  const trendBase=applyAll(RAW).filter(isDefect);
  const ctDatasets=catLabels.map((c,i)=>({label:c,backgroundColor:COLORS[i%COLORS.length],borderRadius:3,
    data:selM.map(m=>sumW(trendBase.filter(r=>r.month===m&&r.category===c)))}));
  mkStacked('chCatTrend',selM.map(m=>MLABEL[m]),ctDatasets);

  // ---- Customer type ----
  const cust=groupSum(defects,'customer_type');
  const ce=Object.entries(cust).sort((a,b)=>b[1]-a[1]);
  mkBar('chCust',ce.map(x=>x[0]),ce.map(x=>x[1]),{colors:'#8b5cf6'});

  // ---- Plant ----
  const plant=groupSum(defects.filter(r=>HIDE_NA(r.plant)),'plant');
  const pe=Object.entries(plant).sort((a,b)=>b[1]-a[1]);
  mkDonut('chPlant',pe.map(x=>x[0]),pe.map(x=>x[1]));

  // ---- Status ----
  const st=groupSum(defects,'status');
  mkDonut('chStatus',Object.keys(st),Object.values(st));

  // ---- States ----
  const stt=Object.entries(groupSum(defects,'state')).sort((a,b)=>b[1]-a[1]).slice(0,10);
  mkBar('chState',stt.map(x=>x[0]),stt.map(x=>x[1]),{horizontal:true,colors:'#14b8a6'});

  // ---- Defect resolution timeline (avg TAT per month) ----
  const tatByM=selM.map(m=>{
    const mr=applyAll(RAW).filter(r=>r.month===m&&r.settle_days&&r.settle_days>0);
    if(!mr.length)return 0;
    return Math.round(mr.reduce((a,r)=>a+(r.settle_days*W(r)),0)/sumW(mr)*10)/10;
  });
  mkLines('chTATtrend',selM.map(m=>MLABEL[m]),[
    {label:'Avg TAT (days)',borderColor:COLORS[0],backgroundColor:COLORS[0]+'33',data:tatByM,fill:true},
    {label:'30-day SOP',borderColor:'#ff3b30',borderDash:[6,4],data:selM.map(()=>30),pointRadius:0,fill:false}
  ]);

  // ---- Top defects by production batch (plant × category stacked) ----
  const batchPlants=Object.entries(groupSum(defects.filter(r=>HIDE_NA(r.plant)),'plant'))
    .sort((a,b)=>b[1]-a[1]).map(x=>x[0]);
  const batchDatasets=catLabels.map((c,i)=>({label:c,backgroundColor:COLORS[i%COLORS.length],borderRadius:3,
    data:batchPlants.map(p=>sumW(defects.filter(r=>r.plant===p&&r.category===c)))}));
  mkStacked('chBatch',batchPlants,batchDatasets.length?batchDatasets:[{label:'No defects',data:batchPlants.map(()=>0),backgroundColor:COLORS[0]}]);

  // ---- Customer × defect heatmap ----
  buildHeatmap(defects,catLabels);

  renderTable(defects);
}

// ---------- heatmap ----------
function buildHeatmap(defects,catLabels){
  const custs=Object.entries(groupSum(defects,'customer_type')).sort((a,b)=>b[1]-a[1]).map(x=>x[0]);
  const grid={};let maxV=0;
  custs.forEach(cu=>{grid[cu]={};catLabels.forEach(c=>{
    const v=sumW(defects.filter(r=>r.customer_type===cu&&r.category===c));
    grid[cu][c]=v;if(v>maxV)maxV=v;});});
  const el=document.getElementById('heatmap');
  if(!custs.length||!catLabels.length){el.innerHTML='<div class="hint">No data for current selection.</div>';return;}
  let html='<table><thead><tr><th></th>';
  catLabels.forEach(c=>{html+=`<th>${c}</th>`;});
  html+='</tr></thead><tbody>';
  custs.forEach(cu=>{
    html+=`<tr><th class="rowlbl">${cu}</th>`;
    catLabels.forEach(c=>{
      const v=grid[cu][c];
      const t=maxV?v/maxV:0;
      const bg=v?`rgba(50,102,173,${(0.12+t*0.85).toFixed(2)})`:'#f5f5f7';
      const fg=t>0.55?'#fff':'var(--txt)';
      html+=`<td><div class="cell" style="background:${bg};color:${fg}" title="${cu} · ${c}: ${v.toLocaleString()}">${v?v.toLocaleString():''}</div></td>`;
    });
    html+='</tr>';
  });
  html+='</tbody></table>';
  el.innerHTML=html;
}

// ---------- table ----------
function renderTable(defects){
  let rows=defects.filter(r=>!r.is_aggregate);
  if(search){const q=search.toLowerCase();
    rows=rows.filter(r=>(r.serial+' '+r.project+' '+r.complaint_no+' '+r.subcategory).toLowerCase().includes(q));}
  rows.sort((a,b)=>{const x=(a[sortK]||'') ,y=(b[sortK]||'');return (x>y?1:x<y?-1:0)*sortDir;});
  const total=rows.length,pages=Math.max(1,Math.ceil(total/PAGE));
  if(page>=pages)page=pages-1;
  const slice=rows.slice(page*PAGE,page*PAGE+PAGE);
  const tb=document.getElementById('tbody');tb.innerHTML='';
  slice.forEach(r=>{const tr=document.createElement('tr');
    const stcls=/wip/i.test(r.status)?'wip':'closed';
    tr.innerHTML=`<td>${MLABEL[r.month]}</td><td>${r.serial||'—'}</td><td>${r.project}</td>
      <td>${r.customer_type}</td><td>${r.state}</td><td>${r.category}</td><td>${r.subcategory}</td>
      <td>${r.plant}</td><td><span class="pill ${stcls}">${r.status}</span></td><td>${r.complaint_no||'—'}</td>`;
    tb.appendChild(tr);});
  document.getElementById('tcount').textContent=total.toLocaleString()+' defect records';
  document.getElementById('pginfo').textContent=`Page ${page+1} of ${pages}`;
  document.getElementById('prev').disabled=page===0;
  document.getElementById('next').disabled=page>=pages-1;
  lastPages=pages;
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
document.getElementById('reset').onclick=()=>{Object.assign(state,{customer:'All',custname:'All',category:'All',subcat:'All',stateF:'All',status:'All',plant:'All',resolution:'All'});selMonths=new Set(MONTHS);monthMode='single';page=0;populateFilters();refresh();};
document.getElementById('search').oninput=e=>{search=e.target.value;page=0;refresh();};
document.querySelectorAll('#tbl thead th').forEach(th=>th.onclick=()=>{const k=th.dataset.k;if(sortK===k)sortDir*=-1;else{sortK=k;sortDir=1;}refresh();});
document.getElementById('prev').onclick=()=>{if(page>0){page--;refresh();}};
document.getElementById('next').onclick=()=>{page++;refresh();};
function jumpToPage(){
  const v=parseInt(document.getElementById('pgjump').value,10);
  if(!v||v<1)return;
  page=Math.min(Math.max(v,1),lastPages)-1;
  document.getElementById('pgjump').value='';
  refresh();
}
document.getElementById('pgjumpbtn').onclick=jumpToPage;
document.getElementById('pgjump').onkeydown=e=>{if(e.key==='Enter')jumpToPage();};

// ---------- init ----------
(async()=>{
  try{
    const resp=await fetch('data.json');
    const total=+resp.headers.get('content-length')||0;
    const reader=resp.body.getReader();
    const chunks=[];let loaded=0;
    const fill=document.getElementById('logo-fill');
    const pct=document.getElementById('load-pct');
    while(true){
      const{done,value}=await reader.read();
      if(done)break;
      chunks.push(value);loaded+=value.length;
      if(total){const p=Math.round(loaded/total*100);fill.style.height=p+'%';pct.textContent=p+'%';}
    }
    fill.style.height='100%';pct.textContent='Building charts…';
    const blob=new Blob(chunks);
    const text=await blob.text();
    RAW=JSON.parse(text);
    RAW.forEach(r=>{ if(r.category!=='No Issue'){ (SUBMAP[r.category]=SUBMAP[r.category]||new Set()).add(r.subcategory);} });
    RAW.forEach(r=>{
      if(r.customer_type&&r.complaint_by){
        (CUST_TYPE_TO_NAME[r.customer_type]=CUST_TYPE_TO_NAME[r.customer_type]||new Set()).add(r.complaint_by);
        (CUST_NAME_TO_TYPE[r.complaint_by]=CUST_NAME_TO_TYPE[r.complaint_by]||new Set()).add(r.customer_type);
      }
    });
    document.getElementById('loading').style.display='none';
    populateFilters();
    refresh();
  }catch(err){
    document.getElementById('loading').innerHTML='<div style="color:var(--bad)">Failed to load data: '+err.message+'</div>';
  }
})();
</script>
</body>
</html>"""

out = HTML.replace("__FAVICON__", favicon_b64).replace("__HEADER_LOGO__", header_b64)
with open("index.html", "w", encoding="utf-8") as f:
    f.write(out)
print("Dashboard written: index.html (fetches data.json at runtime)")
