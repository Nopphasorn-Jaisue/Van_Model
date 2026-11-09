# Cross-Faculty Shared Passenger Van Allocation MILP System (`soure_code/`)
# ระบบเว็บและซอร์สโค้ดจัดสรรรถตู้โดยสารส่วนกลางร่วมกันข้ามคณะด้วยโมเดล MILP

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Solver: PuLP + COIN-OR CBC](https://img.shields.io/badge/Solver-PuLP%20%2B%20CBC-success.svg)](https://coin-or.github.io/pulp/)

---

## 🇹🇭 เริ่มต้นใช้งานอย่างรวดเร็ว (ฉบับภาษาไทย)

### 1. การติดตั้งไลบรารี
```powershell
cd soure_code
pip install -r requirements.txt
```

### 2. การรันระบบเว็บแอปพลิเคชัน (2 เวอร์ชัน: ไทย และ อังกฤษ)
```powershell
# รันเว็บแอปพลิเคชัน รุ่นภาษาไทย (พอร์ต 8080) -> เปิด http://127.0.0.1:8080
python web_app_th.py --port 8080

# รันเว็บแอปพลิเคชัน รุ่นภาษาอังกฤษ (พอร์ต 8081) -> เปิด http://127.0.0.1:8081
python web_app_en.py --port 8081
```

### 3. การรันเอนจิน MILP ผ่าน Command Line
```powershell
# ทดสอบแก้ปัญหาคิวคำขอจริง 10 รายการ (Table 6 ในบทความวิจัย)
python van_allocation_engine.py --mode demo

# แสดงตารางผลลัพธ์เชิงประจักษ์ v6 ทั้งหมด
python van_allocation_engine.py --mode summary
```

* 📄 **คู่มือการติดตั้งและใช้งานฉบับเต็ม (ภาษาไทย):** [`INSTALL_AND_WEB_MANUAL_TH.md`](./INSTALL_AND_WEB_MANUAL_TH.md) | [`INSTALL_AND_WEB_MANUAL_TH.docx`](./INSTALL_AND_WEB_MANUAL_TH.docx)

---

## 🇬🇧 Quick Start Guide (English Edition)

### 1. Install Dependencies
```powershell
cd soure_code
pip install -r requirements.txt
```

### 2. Launch the Web Decision Support Application (Thai & English Versions)
```powershell
# Launch English Web Application (Port 8081) -> Open http://127.0.0.1:8081
python web_app_en.py --port 8081

# Launch Thai Web Application (Port 8080) -> Open http://127.0.0.1:8080
python web_app_th.py --port 8080
```

### 3. Run the MILP Engine via Command Line
```powershell
# Solve the N=10 real pending request queue (Table 6 in the EASR manuscript)
python van_allocation_engine.py --mode demo

# Print all verified v6 empirical benchmark tables
python van_allocation_engine.py --mode summary
```

* 📄 **Full Installation & Web User Manual (English):** [`INSTALL_AND_WEB_MANUAL_EN.md`](./INSTALL_AND_WEB_MANUAL_EN.md) | [`INSTALL_AND_WEB_MANUAL_EN.docx`](./INSTALL_AND_WEB_MANUAL_EN.docx)

