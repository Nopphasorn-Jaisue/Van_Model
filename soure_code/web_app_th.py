#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_app_th.py
===============================================================================
ระบบเว็บสนับสนุนการตัดสินใจจัดสรรรถตู้โดยสารส่วนกลางร่วมกันข้ามคณะด้วยโมเดล MILP
(Cross-Faculty Shared Passenger Van Allocation Web Decision Support System - รุ่นภาษาไทย)

วิธีรันเซิร์ฟเวอร์ (Usage):
  python web_app_th.py --port 8080
จากนั้นเปิดเบราว์เซอร์ไปที่: http://localhost:8080
===============================================================================
"""

from __future__ import annotations
import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict, List

from van_allocation_engine import (
    AllocationConfig,
    get_v6_real_pending_preset,
    solve_van_allocation_milp,
    validate_web_request,
)

HTML_TH = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ระบบจัดสรรรถตู้โดยสารส่วนกลางข้ามคณะด้วยโมเดล MILP (รุ่นภาษาไทย)</title>
  <style>
    :root {
      --primary: #1e3a8a;
      --primary-light: #2563eb;
      --accent: #059669;
      --danger: #dc2626;
      --warning: #d97706;
      --bg: #f8fafc;
      --card: #ffffff;
      --border: #e2e8f0;
      --text: #0f172a;
      --muted: #475569;
    }
    * { box-sizing: border-box; font-family: 'Sarabun', 'Segoe UI', Tahoma, sans-serif; }
    body { margin: 0; background: var(--bg); color: var(--text); }
    header {
      background: linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 100%);
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
    .card h2 { margin: 0 0 14px; font-size: 1.1rem; color: var(--primary); border-bottom: 2px solid #eff6ff; padding-bottom: 8px; }
    .form-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
    .form-group { display: flex; flex-direction: column; gap: 4px; }
    .form-group label { font-size: 0.85rem; font-weight: 600; color: var(--muted); }
    .form-group input, .form-group select {
      padding: 8px 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 0.92rem;
    }
    .btn-row { display: flex; gap: 10px; margin-top: 14px; flex-wrap: wrap; }
    button {
      cursor: pointer; border: none; border-radius: 8px; padding: 10px 16px;
      font-weight: 600; font-size: 0.92rem; transition: 0.15s;
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
    .kpi .label { font-size: 0.8rem; color: var(--muted); font-weight: 600; }
    .kpi .val { font-size: 1.45rem; font-weight: 700; margin-top: 4px; color: var(--text); }
    .kpi .sub { font-size: 0.78rem; color: var(--accent); margin-top: 2px; }
    .alert {
      padding: 10px 14px; border-radius: 8px; margin-top: 12px; font-size: 0.88rem; display: none;
    }
    .alert-error { background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }
    .alert-ok { background: #ecfdf5; color: #065f46; border: 1px solid #a7f3d0; }
    table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
    th, td { padding: 10px 10px; border-bottom: 1px solid var(--border); text-align: left; }
    th { background: #f1f5f9; font-weight: 700; color: var(--primary); }
    .pill {
      display: inline-block; padding: 3px 8px; border-radius: 999px; font-size: 0.76rem; font-weight: 700;
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
      <h1>🚐 ระบบสนับสนุนการตัดสินใจจัดสรรรถตู้โดยสารส่วนกลางร่วมกันข้ามคณะ (MILP Engine v6)</h1>
      <p>รองรับข้อจำกัดชั่วโมงการทำงานและการพักผ่อนตามเกณฑ์ความปลอดภัย (HOS 14 ชม./วัน, 72 ชม./14 วัน, พักขั้นต่ำ 10 ชม.)</p>
    </div>
    <div class="badge-bar">
      <span class="badge">รุ่นภาษาไทย (TH)</span>
      <span class="badge">Solver: PuLP + COIN-OR CBC</span>
    </div>
  </header>

  <div class="container">
    <div class="grid-top">
      <!-- ตั้งค่าพารามิเตอร์มหาวิทยาลัยและกฎ HOS -->
      <div class="card">
        <h2>⚙️ 1. ตั้งค่านโยบายมหาวิทยาลัยและเกณฑ์ความปลอดภัย (HOS Parameters)</h2>
        <div class="form-grid">
          <div class="form-group">
            <label>ความจุรถตู้มาตรฐาน (ที่นั่ง/คัน)</label>
            <input type="number" id="cfg_cap" value="11" min="1" max="40" />
          </div>
          <div class="form-group">
            <label>เพดานทำงานรายวันสูงสุด (ชม./วัน)</label>
            <input type="number" id="cfg_daily" value="14.0" step="0.5" min="4" max="24" />
          </div>
          <div class="form-group">
            <label>เพดานสะสม 14 วันสูงสุด (ชม./14 วัน)</label>
            <input type="number" id="cfg_14d" value="72.0" step="1" min="20" max="140" />
          </div>
          <div class="form-group">
            <label>เวลาพักขั้นต่ำระหว่างทริป (ชม.)</label>
            <input type="number" id="cfg_rest" value="10.0" step="0.5" min="0" max="24" />
          </div>
          <div class="form-group" style="grid-column: span 2;">
            <label>นโยบายการยืมรถข้ามคณะ (Cross-Faculty Resource Pooling)</label>
            <select id="cfg_sharing">
              <option value="true" selected>✅ เปิดใช้งานการแชร์รถข้ามคณะ (Shared Pool — แนะนำ)</option>
              <option value="false">🔒 ปิดการแชร์รถ (Siloed Policy — ใช้เฉพาะรถของคณะตนเอง)</option>
            </select>
          </div>
        </div>
        <div class="btn-row">
          <button class="btn-success" onclick="runSolve()">🚀 รันจัดสรรรถตู้ด้วยโมเดล MILP</button>
          <button class="btn-outline" onclick="loadPreset()">🔄 โหลดคิวคำขอจริง 10 รายการ (v6 Preset)</button>
        </div>
      </div>

      <!-- เพิ่มคำขอใหม่พร้อมตรวจสอบกติกาเว็บ -->
      <div class="card">
        <h2>➕ 2. เพิ่มคำขอจองรถตู้ใหม่ (พร้อมระบบตรวจสอบความจุตามกติกาเว็บ TC66–TC69)</h2>
        <div class="form-grid">
          <div class="form-group">
            <label>รหัสคำขอ (Request ID)</label>
            <input type="text" id="req_id" value="ICT_NEW_01" />
          </div>
          <div class="form-group">
            <label>คณะผู้ยื่นคำขอ (Faculty)</label>
            <select id="req_fac">
              <option value="ICT">ICT (คณะเทคโนโลยีสารสนเทศฯ)</option>
              <option value="SCI">SCI (คณะวิทยาศาสตร์)</option>
              <option value="SEEN">SEEN (คณะพลังงานและสิ่งแวดล้อม)</option>
            </select>
          </div>
          <div class="form-group">
            <label>จำนวนผู้โดยสาร (คน)</label>
            <input type="number" id="req_pax" value="8" min="1" max="50" />
          </div>
          <div class="form-group">
            <label>จำนวนรถที่ขอ (คัน)</label>
            <input type="number" id="req_vans" value="1" min="1" max="3" />
          </div>
          <div class="form-group">
            <label>ขอบเขตการเดินทาง</label>
            <select id="req_scope">
              <option value="1">ต่างจังหวัด (บังคับคนขับประจำรถ)</option>
              <option value="0">ภายในจังหวัด</option>
            </select>
          </div>
          <div class="form-group">
            <label>ชั่วโมงปฏิบัติงานของทริป (ชม.)</label>
            <input type="number" id="req_hours" value="6.0" step="0.5" min="1" max="14" />
          </div>
        </div>
        <div class="btn-row">
          <button class="btn-primary" onclick="addRequest()">+ ตรวจสอบกติกาเว็บและเพิ่มลงในคิว</button>
        </div>
        <div id="val_alert" class="alert"></div>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="kpi-grid">
      <div class="kpi">
        <div class="label">อัตราจัดสรรคำขอสำเร็จ</div>
        <div class="val" id="kpi_req">-</div>
        <div class="sub" id="kpi_status">สถานะตัวแก้ปัญหา: พร้อมทำงาน</div>
      </div>
      <div class="kpi">
        <div class="label">จำนวนผู้โดยสารที่รองรับ</div>
        <div class="val" id="kpi_pax">-</div>
        <div class="sub" id="kpi_pax_pct">-</div>
      </div>
      <div class="kpi">
        <div class="label">การยืมรถข้ามคณะ</div>
        <div class="val" id="kpi_loans">-</div>
        <div class="sub">ยืมเฉพาะเมื่อรถคณะตนเองติดภารกิจ</div>
      </div>
      <div class="kpi">
        <div class="label">การละเมิดกฎความปลอดภัย HOS</div>
        <div class="val" id="kpi_viol">0 ครั้ง</div>
        <div class="sub">ตรวจเพดาน 14 ชม./72 ชม./พัก 10 ชม.</div>
      </div>
      <div class="kpi">
        <div class="label">เวลาประมวลผล (CBC Solver)</div>
        <div class="val" id="kpi_time">-</div>
        <div class="sub">Global Optimal (MIP Gap 0.0%)</div>
      </div>
    </div>

    <!-- ตารางผลลัพธ์การจัดสรรรายคำขอ -->
    <div class="card">
      <h2>📋 3. ตารางผลลัพธ์การจัดสรรรถตู้และพนักงานขับรถรายคำขอ (Request-Level Allocation Results)</h2>
      <div style="overflow-x:auto;">
        <table>
          <thead>
            <tr>
              <th>รหัสคำขอ</th>
              <th>คณะผู้ขอ</th>
              <th>ผู้โดยสาร (จัดได้/ขอ)</th>
              <th>ขอบเขต</th>
              <th>วัน-เวลาเดินทาง</th>
              <th>รถและคนขับที่จัดสรร</th>
              <th>การยืมข้ามคณะ</th>
              <th>สถานะ</th>
              <th>เหตุผลประกอบการจัดสรร</th>
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
        alertBox.textContent = '❌ ' + vData.msg_th;
        return;
      }
      alertBox.className = 'alert alert-ok';
      alertBox.textContent = '✅ ' + vData.msg_th + ' — เพิ่มคำขอเข้าสู่คิวและคำนวณใหม่เรียบร้อยแล้ว';

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
      document.getElementById('kpi_status').textContent = `สถานะ: ${out.solver_status}`;
      document.getElementById('kpi_pax').textContent = `${out.total_pax_served} / ${out.total_pax_requested} คน`;
      document.getElementById('kpi_pax_pct').textContent = `คิดเป็นร้อยละ ${out.pax_fulfillment_pct}%`;
      document.getElementById('kpi_loans').textContent = `${out.cross_faculty_loans} เที่ยว`;
      document.getElementById('kpi_viol').textContent = `${out.safety_violations} ครั้ง`;
      document.getElementById('kpi_time').textContent = `${out.solve_time_sec} วินาที`;

      const tbody = document.getElementById('res_tbody');
      tbody.innerHTML = '';
      for (const a of out.assignments) {
        const tr = document.createElement('tr');
        const resStr = a.assigned_resources.length
          ? a.assigned_resources.map(r => `${r.van_id} (${r.driver_id}: ${r.pax} คน)`).join('<br/>')
          : '–';
        const loanBadge = a.assigned_resources.length === 0
          ? '–'
          : (a.cross_faculty_loan
              ? '<span class="pill pill-loan">ยืมข้ามคณะ</span>'
              : '<span class="pill pill-own">รถคณะตนเอง</span>');
        const statusBadge = a.status === 'FULLY_ASSIGNED'
          ? '<span class="pill pill-ok">จัดสรรสำเร็จ</span>'
          : '<span class="pill pill-no">ปฏิเสธ / ไม่ว่าง</span>';
        const scopeTh = a.scope === 'Out-of-Province' ? 'ต่างจังหวัด' : 'ในจังหวัด';
        tr.innerHTML = `
          <td><strong>${a.request_id}</strong></td>
          <td>${a.faculty}</td>
          <td>${a.pax_served} / ${a.pax_requested} คน</td>
          <td>${scopeTh}</td>
          <td><small>${a.start_dt}<br/>ถึง ${a.end_dt}</small></td>
          <td>${resStr}</td>
          <td>${loanBadge}</td>
          <td>${statusBadge}</td>
          <td><small>${a.reason_th}</small></td>
        `;
        tbody.appendChild(tr);
      }
    }

    window.addEventListener('DOMContentLoaded', loadPreset);
  </script>
</body>
</html>
"""


class VanWebHandlerTH(BaseHTTPRequestHandler):
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
        raw = HTML_TH.encode("utf-8")
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
    parser = argparse.ArgumentParser(description="Thai Web App for MILP Van Allocation")
    parser.add_argument("--host", default="127.0.0.1", help="Host address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8080, help="Port number (default: 8080)")
    args = parser.parse_args()
    server = HTTPServer((args.host, args.port), VanWebHandlerTH)
    print(f"[TH Web App] ระบบเว็บจัดสรรรถตู้ (ภาษาไทย) พร้อมทำงานที่ http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()

