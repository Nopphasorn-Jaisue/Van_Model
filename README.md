# Multi-Faculty University Van Allocation Model (MILP + HOS Safety Constraints)
**ตัวแบบโปรแกรมเชิงเส้นจำนวนเต็มแบบผสมสำหรับการจัดสรรรถตู้ร่วมระหว่างคณะภายใต้ข้อจำกัดชั่วโมงการทำงานของพนักงานขับรถ**

Repository for the research manuscript prepared for **Engineering and Applied Science Research (EASR, Khon Kaen University)** and the accompanying **Web Decision Support System (DSS) + MILP Optimization Source Code** (Thai & English Editions).

---

## 📁 โครงสร้างคลังข้อมูล (Repository Structure)

### 1. [`soure_code/`](./soure_code/) — Source Code ระบบเว็บช่วยตัดสินใจและคู่มือการติดตั้ง (2 ภาษา: ไทย / อังกฤษ)
- [`soure_code/van_allocation_engine.py`](./soure_code/van_allocation_engine.py) — เอ็นจินหาค่าเหมาะสมที่สุด MILP (PuLP + COIN-OR CBC), ตัวตรวจสอบความจุหน้าเว็บ ($P_r \le C_v \times K_r$ ตามกรณีทดสอบ `TC66–TC69`), และชุดข้อมูลจริงรอจัดสรร v6 (`10` คำขอ)
- [`soure_code/web_app_th.py`](./soure_code/web_app_th.py) — **ระบบเว็บแอปพลิเคชันช่วยตัดสินใจ ฉบับภาษาไทย** (พอร์ตเริ่มต้น `8080`)
- [`soure_code/web_app_en.py`](./soure_code/web_app_en.py) — **Web Decision Support System — English Edition** (Default port `8081`)
- [`soure_code/INSTALL_AND_WEB_MANUAL_TH.md`](./soure_code/INSTALL_AND_WEB_MANUAL_TH.md) & [`INSTALL_AND_WEB_MANUAL_TH.docx`](./soure_code/INSTALL_AND_WEB_MANUAL_TH.docx) — **คู่มือการติดตั้งและใช้งานระบบเว็บแอปพลิเคชัน (ฉบับภาษาไทย)**
- [`soure_code/INSTALL_AND_WEB_MANUAL_EN.md`](./soure_code/INSTALL_AND_WEB_MANUAL_EN.md) & [`INSTALL_AND_WEB_MANUAL_EN.docx`](./soure_code/INSTALL_AND_WEB_MANUAL_EN.docx) — **Web Application & Source Code Installation Manual (English Edition)**
- [`soure_code/requirements.txt`](./soure_code/requirements.txt) — รายการไลบรารีที่จำเป็น (`pulp`, `pandas`, `numpy`)

### 2. บทความวิจัยฉบับสมบูรณ์ตามเทมเพลตวารสาร EASR (Manuscripts — EN & TH)
- [`EASR_manuscript_EN.md`](./EASR_manuscript_EN.md) & [`EASR_manuscript_EN_revised.docx`](./EASR_manuscript_EN_revised.docx) — ต้นฉบับบทความวิจัยภาษาอังกฤษตามเทมเพลต EASR 2026 พร้อมไฮไลต์ตัวเลขสีแดงจากการทดลอง `v6`
- [`EASR_manuscript_TH.md`](./EASR_manuscript_TH.md) & [`EASR_manuscript_TH_revised.docx`](./EASR_manuscript_TH_revised.docx) — ต้นฉบับบทความวิจัยภาษาไทยคู่ขนานตามเทมเพลต EASR 2026 พร้อมไฮไลต์ตัวเลขสีแดงจากการทดลอง `v6`
- [`EASR_Submission/`](./EASR_Submission/) — โฟลเดอร์รวมไฟล์ส่งวารสาร รูปภาพความละเอียดสูง และคู่มือ

### 3. ชุดการทดลองและข้อมูลจริง (`v6 Candidate`)
- [`testing_v6_Candidate.ipynb`](./testing_v6_Candidate.ipynb) — Jupyter Notebook ฉบับสมบูรณ์ที่รันชุดการทดลองทั้ง 4,320 สถานการณ์ (`S1_Baseline`, `S2_Sharing`, `S3_Sensitivity`, `S4_Scalability`, `S5_Backtest`, และ `TC01–TC69`)
- [`raw_data/`](./raw_data/) — ข้อมูลบันทึกการใช้รถและคนขับจริงจากระบบ e-Office ของมหาวิทยาลัยพะเยา (คณะ ICT และคณะวิทยาศาสตร์ SCI)
- [`raw_output/`](./raw_output/) — ผลลัพธ์เชิงตัวเลข (`.csv`, `.xlsx`) จากการรันโมเดล `v6`

---

## 🚀 การเริ่มต้นใช้งานอย่างรวดเร็ว (Quick Start)

```powershell
# 1. ติดตั้งไลบรารี
pip install -r soure_code/requirements.txt

# 2. รันระบบเว็บแอปพลิเคชัน (ภาษาไทย - พอร์ต 8080)
python soure_code/web_app_th.py --port 8080

# 3. รันระบบเว็บแอปพลิเคชัน (ภาษาอังกฤษ - พอร์ต 8081)
python soure_code/web_app_en.py --port 8081

# 4. รันผ่านบรรทัดคำสั่ง (CLI Demo ตารางที่ 6 ของเปเปอร์)
python soure_code/van_allocation_engine.py --mode demo
```
