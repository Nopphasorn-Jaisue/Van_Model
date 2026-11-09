#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_app_en.py
===============================================================================
Cross-Faculty Shared Passenger Van Allocation Web Decision Support System
(MILP Engine v6 - English Edition)

Usage:
  python web_app_en.py --port 8081
Then open your browser at: http://localhost:8081
===============================================================================
"""

from __future__ import annotations
import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict

from van_allocation_engine import (
    AllocationConfig,
    get_v6_real_pending_preset,
    solve_van_allocation_milp,
    validate_web_request,
)

HTML_EN = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Cross-Faculty Shared Van Allocation DSS (MILP Engine v6 - English Edition)</title>
  <style>
    :root {
      --primary: #1e3a8a;
      --primary-light: #2563eb;
      --accent: #059669;
      --danger: #dc2626;
      --bg: #f8fafc;
      --card: #ffffff;
      --border: #e2e8f0;
      --text: #0f172a;
      --muted: #475569;
    }
    * { box-sizing: border-box; font-family: 'Segoe UI', Inter, Roboto, sans-serif; }
    body { margin: 0; background: var(--bg); color: var(--text); }
    header {
      background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
      color: #fff; padding: 20px 32px;
      display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;
      box-shadow: 0 2px 10px rgba(0,0,0,0.12);
    }
    header h1 { margin: 0; font-size: 1.35rem; }
    header p { margin: 4px 0 0; font-size: 0.9rem; opacity: 0.9; }
    .badge-bar { display: flex; gap: 8px; align-items: center; }
    .badge {
      background: rgba(255,255,255,0.18); padding: 6px 12px; border-radius: 999px;
      font-size: 0.82rem; font-weight: 600;
    }
    .container { max-width: 1320px; margin: 24px auto; padding: 0 20px; }
    .grid-top { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
    @media (max-width: 960px) { .grid-top { grid-template-columns: 1fr; } }
    .card {
      background: var(--card); border: 1px solid var(--border); border-radius: 12px;
      padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .card h2 { margin: 0 0 14px; font-size: 1.08rem; color: var(--primary); border-bottom: 2px solid #eff6ff; padding-bottom: 8px; }
    .form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
    .form-group { display: flex; flex-direction: column; gap: 4px; }
    .form-group label { font-size: 0.84rem; font-weight: 600; color: var(--muted); }
    .form-group input, .form-group select {
      padding: 8px 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.92rem;
    }
    .btn-row { display: flex; gap: 10px; margin-top: 14px; flex-wrap: wrap; }
    button {
      cursor: pointer; border: none; border-radius: 8px; padding: 10px 16px;
      font-weight: 600; font-size: 0.9rem; transition: 0.15s;
    }
    .btn-primary { background: var(--primary-light); color: #fff; }
    .btn-primary:hover { background: var(--primary); }
    .btn-success { background: var(--accent); color: #fff; }
    .btn-success:hover { background: #047857; }
    .btn-outline { background: #f1f5f9; color: var(--text); border: 1px solid var(--border); }
    .btn-outline:hover { background: #e2e8f0; }
    .kpi-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-bottom: 20px; }
    @media (max-width: 960px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }
    .kpi {
      background: var(--card); border: 1px solid var(--border); border-radius: 10px;
      padding: 14px 16px; border-left: 4px solid var(--primary-light);
    }
    .kpi .label { font-size: 0.78rem; color: var(--muted); font-weight: 600; text-transform: uppercase; }
    .kpi .val { font-size: 1.4rem; font-weight: 700; margin-top: 4px; color: var(--text); }
    .kpi .sub { font-size: 0.76rem; color: var(--accent); margin-top: 2px; }
    .alert {
      padding: 10px 14px; border-radius: 8px; margin-top: 12px; font-size: 0.88rem; display: none;
    }
    .alert-error { background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }
    .alert-ok { background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }
    table { width: 100%; border-collapse: collapse; font-size: 0.86rem; }
    th, td { padding: 10px 10px; border-bottom: 1px solid var(--border); text-align: left; }
    th { background: #f1f5f9; font-weight: 700; color: var(--primary); }
    .pill {
      display: inline-block; padding: 3px 8px; border-radius: 999px; font-size: 0.75rem; font-weight: 700;
    }
    .pill-ok { background: #d1fae5; color: #065f46; }
    .pill-no { background: #fee2e2; color: #991b1b; }
    .pill-loan { background: #dbeafe; color: #1e40af; }
    .pill-own { background: #f1f5f9; color: #334155; }
  </style>
</head>
<body>
  <header>
    <div>
      <h1>🚐 Cross-Faculty Shared Passenger Van Allocation DSS (MILP Engine v6)</h1>
      <p>Safety-Compliant Hours-of-Service Optimization (14h/day cap, 72h/14-day cap, 10h mandatory rest)</p>
    </div>
    <div class="badge-bar">
      <span class="badge">English Edition (EN)</span>
      <span class="badge">Solver: PuLP + COIN-OR CBC</span>
    </div>
  </header>

  <div class="container">
    <div class="grid-top">
      <!-- University Policy & HOS Parameters -->
      <div class="card">
        <h2>⚙️ 1. University Policy & Hours-of-Service (HOS) Configuration</h2>
        <div class="form-grid">
          <div class="form-group">
            <label>Standard Van Capacity (Seats/Van)</label>
            <input type="number" id="cfg_cap" value="11" min="1" max="40" />
          </div>
          <div class="form-group">
            <label>Max Daily Duty Cap (Hours/Day)</label>
            <input type="number" id="cfg_daily" value="14.0" step="0.5" min="4" max="24" />
          </div>
          <div class="form-group">
            <label>Max 14-Day Cumulative Cap (Hours/14d)</label>
            <input type="number" id="cfg_14d" value="72.0" step="1" min="20" max="140" />
          </div>
          <div class="form-group">
            <label>Min Mandatory Inter-Shift Rest (Hours)</label>
            <input type="number" id="cfg_rest" value="10.0" step="0.5" min="0" max="24" />
          </div>
          <div class="form-group" style="grid-column: span 2;">
            <label>Cross-Faculty Fleet Sharing Policy</label>
            <select id="cfg_sharing">
              <option value="true" selected>✅ Enable Cross-Faculty Pooling (Shared Pool — Recommended)</option>
              <option value="false">🔒 Disable Sharing (Siloed Policy — Home Faculty Vans Only)</option>
            </select>
          </div>
        </div>
        <div class="btn-row">
          <button class="btn-success" onclick="runSolve()">🚀 Run MILP Optimization</button>
          <button class="btn-outline" onclick="loadPreset()">🔄 Load Real Pending Queue (N = 10 Preset)</button>
        </div>
      </div>

      <!-- Add New Booking Request -->
      <div class="card">
        <h2>➕ 2. Add Booking Request (with Web Capacity Rule Validation TC66–TC69)</h2>
        <div class="form-grid">
          <div class="form-group">
            <label>Request ID</label>
            <input type="text" id="req_id" value="ICT_NEW_01" />
          </div>
          <div class="form-group">
            <label>Requester Faculty</label>
            <select id="req_fac">
              <option value="ICT">ICT (School of ICT)</option>
              <option value="SCI">SCI (School of Science)</option>
              <option value="SEEN">SEEN (School of Energy & Environment)</option>
            </select>
          </div>
          <div class="form-group">
            <label>Passenger Count</label>
            <input type="number" id="req_pax" value="8" min="1" max="50" />
          </div>
          <div class="form-group">
            <label>Requested Vans</label>
            <input type="number" id="req_vans" value="1" min="1" max="3" />
          </div>
          <div class="form-group">
            <label>Trip Scope</label>
            <select id="req_scope">
              <option value="1">Out-of-Province (Mandatory Driver)</option>
              <option value="0">In-Province</option>
            </select>
          </div>
          <div class="form-group">
            <label>Trip Work Duration (Hours)</label>
            <input type="number" id="req_hours" value="6.0" step="0.5" min="1" max="14" />
          </div>
        </div>
        <div class="btn-row">
          <button class="btn-primary" onclick="addRequest()">+ Validate Capacity & Add to Queue</button>
        </div>
        <div id="val_alert" class="alert"></div>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="kpi-grid">
      <div class="kpi">
        <div class="label">Requests Fulfilled</div>
        <div class="val" id="kpi_req">-</div>
        <div class="sub" id="kpi_status">Solver Status: Ready</div>
      </div>
      <div class="kpi">
        <div class="label">Passengers Served</div>
        <div class="val" id="kpi_pax">-</div>
        <div class="sub" id="kpi_pax_pct">-</div>
      </div>
      <div class="kpi">
        <div class="label">Cross-Faculty Loans</div>
        <div class="val" id="kpi_loans">-</div>
        <div class="sub">Borrowed only when home fleet busy</div>
      </div>
      <div class="kpi">
        <div class="label">Safety / HOS Violations</div>
        <div class="val" id="kpi_viol">0</div>
        <div class="sub">14h/day, 72h/14d & 10h rest enforced</div>
      </div>
      <div class="kpi">
        <div class="label">CBC Solve Time</div>
        <div class="val" id="kpi_time">-</div>
        <div class="sub">Global Optimal (0.0% MIP Gap)</div>
      </div>
    </div>

    <!-- Request-Level Results Table -->
    <div class="card">
      <h2>📋 3. Request-Level Van & Driver Allocation Schedule (Table 6 Replication)</h2>
      <div style="overflow-x:auto;">
        <table>
          <thead>
            <tr>
              <th>Request ID</th>
              <th>Faculty</th>
              <th>Passengers (Served/Req)</th>
              <th>Trip Scope</th>
              <th>Schedule Window</th>
              <th>Assigned Van (Driver)</th>
              <th>Cross-Faculty Loan</th>
              <th>Outcome</th>
              <th>Allocation Rationale</th>
            </tr>
          </thead>
          <tbody id="res_tbody"></tbody>
        </table>
      </div>
    </div>
  </div>

  <script>
    let currentState = { requests: [], vans: [], drivers: [], fixed_busy_blocks: [] };

    async function loadPreset() {
      const res = await fetch('/api/preset');
      currentState = await res.json();
      await runSolve();
    }

    async function addRequest() {
      const alertBox = document.getElementById('val_alert');
      const pax = parseInt(document.getElementById('req_pax').value || '0');
      const vans = parseInt(document.getElementById('req_vans').value || '1');
      const cap = parseInt(document.getElementById('cfg_cap').value || '11');

      const vRes = await fetch('/api/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ pax, requested_vans: vans, van_capacity: cap })
      });
      const vData = await vRes.json();
      alertBox.style.display = 'block';
      if (!vData.valid) {
        alertBox.className = 'alert alert-error';
        alertBox.textContent = '❌ ' + vData.msg_en;
        return;
      }
      alertBox.className = 'alert alert-ok';
      alertBox.textContent = '✅ ' + vData.msg_en + ' — Added to queue and re-optimized.';

      const reqId = document.getElementById('req_id').value.trim() || ('REQ_' + (currentState.requests.length + 1));
      const fac = document.getElementById('req_fac').value;
      const scope = parseInt(document.getElementById('req_scope').value);
      const hours = parseFloat(document.getElementById('req_hours').value || '6.0');
      currentState.requests.push({
        request_id: reqId,
        faculty: fac,
        pax: pax,
        max_vans: vans,
        is_out_of_province: scope,
        start_dt: '2026-07-05 08:00:00',
        end_dt: '2026-07-05 16:00:00',
        day_hours: { 12: hours },
        reason_th: 'คำขอที่เพิ่มใหม่จากหน้าเว็บ (ผ่านการตรวจสอบความจุและกฎ HOS)',
        reason_en: 'Newly added web request (validated against capacity & HOS rules)'
      });
      await runSolve();
    }

    async function runSolve() {
      const cfg = {
        van_capacity: parseInt(document.getElementById('cfg_cap').value || '11'),
        max_hours_per_day: parseFloat(document.getElementById('cfg_daily').value || '14.0'),
        max_hours_per_14d: parseFloat(document.getElementById('cfg_14d').value || '72.0'),
        min_rest_hours: parseFloat(document.getElementById('cfg_rest').value || '10.0'),
        allow_cross_faculty_sharing: document.getElementById('cfg_sharing').value === 'true'
      };
      const res = await fetch('/api/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...currentState, config: cfg })
      });
      const out = await res.json();
      document.getElementById('kpi_req').textContent = `${out.fully_assigned} / ${out.total_requests} (${out.fulfillment_rate_pct}%)`;
      document.getElementById('kpi_status').textContent = `Status: ${out.solver_status}`;
      document.getElementById('kpi_pax').textContent = `${out.total_pax_served} / ${out.total_pax_requested} pax`;
      document.getElementById('kpi_pax_pct').textContent = `${out.pax_fulfillment_pct}% served`;
      document.getElementById('kpi_loans').textContent = `${out.cross_faculty_loans} trips`;
      document.getElementById('kpi_viol').textContent = `${out.safety_violations}`;
      document.getElementById('kpi_time').textContent = `${out.solve_time_sec} s`;

      const tbody = document.getElementById('res_tbody');
      tbody.innerHTML = '';
      for (const a of out.assignments) {
        const tr = document.createElement('tr');
        const resStr = a.assigned_resources.length
          ? a.assigned_resources.map(r => `${r.van_id} (${r.driver_id}: ${r.pax} pax)`).join('<br/>')
          : '–';
        const loanBadge = a.assigned_resources.length === 0
          ? '–'
          : (a.cross_faculty_loan
              ? '<span class="pill pill-loan">Yes (Borrowed)</span>'
              : '<span class="pill pill-own">No (Own Van)</span>');
        const statusBadge = a.status === 'FULLY_ASSIGNED'
          ? '<span class="pill pill-ok">Assigned</span>'
          : '<span class="pill pill-no">Rejected</span>';
        tr.innerHTML = `
          <td><strong>${a.request_id}</strong></td>
          <td>${a.faculty}</td>
          <td>${a.pax_served} / ${a.pax_requested}</td>
          <td>${a.scope}</td>
          <td><small>${a.start_dt}<br/>to ${a.end_dt}</small></td>
          <td>${resStr}</td>
          <td>${loanBadge}</td>
          <td>${statusBadge}</td>
          <td><small>${a.reason_en}</small></td>
        `;
        tbody.appendChild(tr);
      }
    }

    window.addEventListener('DOMContentLoaded', loadPreset);
  </script>
</body>
</html>
"""


class VanWebHandlerEN(BaseHTTPRequestHandler):
    def _send_json(self, payload: Dict, status: int = 200) -> None:
        raw = json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        if self.path == "/api/preset":
            reqs, vans, drvs, blks = get_v6_real_pending_preset()
            self._send_json({
                "requests": reqs,
                "vans": vans,
                "drivers": drvs,
                "fixed_busy_blocks": blks,
            })
            return
        raw = HTML_EN.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
        if self.path == "/api/validate":
            ok, msg_th, msg_en = validate_web_request(
                int(body.get("pax", 1)),
                int(body.get("requested_vans", 1)),
                int(body.get("van_capacity", 11)),
            )
            self._send_json({"valid": ok, "msg_th": msg_th, "msg_en": msg_en})
            return
        if self.path == "/api/solve":
            cfg_dict = body.get("config", {})
            cfg = AllocationConfig(
                van_capacity=int(cfg_dict.get("van_capacity", 11)),
                max_hours_per_day=float(cfg_dict.get("max_hours_per_day", 14.0)),
                max_hours_per_14d=float(cfg_dict.get("max_hours_per_14d", 72.0)),
                min_rest_hours=float(cfg_dict.get("min_rest_hours", 10.0)),
                allow_cross_faculty_sharing=bool(cfg_dict.get("allow_cross_faculty_sharing", True)),
            )
            reqs = body.get("requests", [])
            vans = body.get("vans", [])
            drvs = body.get("drivers", [])
            blks = body.get("fixed_busy_blocks", [])
            for r in reqs:
                if "day_hours" in r:
                    r["day_hours"] = {int(k): float(v) for k, v in r["day_hours"].items()}
            out = solve_van_allocation_milp(reqs, vans, drvs, fixed_busy_blocks=blks, config=cfg)
            self._send_json(out)
            return
        self._send_json({"error": "Not found"}, status=404)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description="English Web App for MILP Van Allocation")
    parser.add_argument("--host", default="127.0.0.1", help="Host address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8081, help="Port number (default: 8081)")
    args = parser.parse_args()
    server = HTTPServer((args.host, args.port), VanWebHandlerEN)
    print(f"[EN Web App] MILP Van Allocation Web DSS running at http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()

