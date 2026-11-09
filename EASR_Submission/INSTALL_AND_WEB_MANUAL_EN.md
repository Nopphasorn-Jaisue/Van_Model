# Web Application & Source Code Installation and User Manual: Cross-Faculty Shared Van Allocation MILP System (English Edition)

**Source Code Directory:** `soure_code/`  
**GitHub Repository:** https://github.com/Nopphasorn-Jaisue/Van_Model.git  
**Included Versions:**
1. **Thai Web Decision Support Application (`web_app_th.py`)** — Default port `8080`
2. **English Web Decision Support Application (`web_app_en.py`)** — Default port `8081`
3. **Core MILP Optimization Engine (`van_allocation_engine.py`)** — PuLP + COIN-OR CBC solver featuring Web Capacity Validation (`TC66–TC69`) and statutory Hours-of-Service (HOS: 14h/day, 72h/14d, 10h mandatory rest) constraints.

---

## 1. File Structure in `soure_code/`

| Filename | Type | Description |
| :--- | :--- | :--- |
| `web_app_en.py` | Web Server (EN) | Interactive Web Decision Support System (**English Edition**, `http://127.0.0.1:8081`) |
| `web_app_th.py` | Web Server (TH) | Interactive Web Decision Support System (**Thai Edition**, `http://127.0.0.1:8080`) |
| `van_allocation_engine.py` | Core MILP Engine | MILP mathematical solver (PuLP + CBC), Web Capacity Validator, Buddhist Era CSV preprocessor, and CLI runner |
| `requirements.txt` | Dependencies | Required Python packages for the solver and web server |
| `INSTALL_AND_WEB_MANUAL_EN.md` / `.docx` | Manual (English) | Complete installation and web user guide (English Edition) |
| `INSTALL_AND_WEB_MANUAL_TH.md` / `.docx` | Manual (Thai) | Complete installation and web user guide (Thai Edition) |
| `README.md` | Documentation | Bilingual (Thai & English) quick-start guide |

---

## 2. System Requirements & Installation

### 2.1 Minimum System Requirements
- **Operating System:** Windows 10/11, macOS, or Linux (Ubuntu 20.04+)
- **Python Version:** Python 3.9 – 3.12 (Python 3.11 recommended)
- **Web Browser:** Google Chrome, Microsoft Edge, Mozilla Firefox, or Safari
- **MILP Solver:** **COIN-OR CBC**, automatically bundled with `pulp` (100% open-source; no commercial license required)

### 2.2 Step-by-Step Installation from GitHub
Open a PowerShell or Terminal window and run the following commands:

```powershell
# 1. Clone the repository from GitHub
git clone https://github.com/Nopphasorn-Jaisue/Van_Model.git
cd Van_Model/soure_code

# 2. (Recommended) Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Install all required dependencies
pip install -r requirements.txt
```

---

## 3. Launching the Web Applications (Thai & English Editions)

### 3.1 Running the English Web Application (`web_app_en.py`)
```powershell
python web_app_en.py --port 8081
```
- Open your browser and navigate to **`http://127.0.0.1:8081`**.
- The dashboard automatically loads the real 10-request pending queue (`v6 Preset`, corresponding to Table 6 in the EASR manuscript) and solves the MILP model in real time.

### 3.2 Running the Thai Web Application (`web_app_th.py`)
```powershell
python web_app_th.py --port 8080
```
- Open your browser and navigate to **`http://127.0.0.1:8080`**.
- Provides the full Thai-language interface for university transport coordinators in Thailand.

---

## 4. Web Application User Guide

The interactive web dashboard consists of three core panels designed for university administrators and fleet dispatchers:

### Panel 1: University Policy & Hours-of-Service (HOS) Configuration
Administrators can customize institutional parameters and click **"🚀 Run MILP Optimization"** to evaluate policy impacts immediately:
1. **Standard Van Capacity (Seats/Van):** Defaults to `11` seats (adjustable to `12`, `13`, or `20` seats for larger campus minibuses).
2. **Max Daily Duty Cap (Hours/Day):** Defaults to `14.0` hours/day.
3. **Max 14-Day Cumulative Cap (Hours/14d):** Defaults to `72.0` hours per 14-day horizon (derived from the 36 h/week public-sector duty limit).
4. **Min Mandatory Inter-Shift Rest (Hours):** Defaults to `10.0` consecutive hours between trips.
5. **Cross-Faculty Fleet Sharing Policy:**
   - **✅ Enable Cross-Faculty Pooling (Shared Pool):** Allows idle vans from partner faculties (e.g., SCI) to cover requests when a requester's home fleet is occupied, fulfilling **9/10 requests (90.0%)** and **62/69 passengers (89.9%)** with 8 cross-faculty loans from SCI.
   - **🔒 Disable Sharing (Siloed Policy):** Restricts each faculty to its own van, causing fulfillment on the real pending queue to drop to **1/10 requests (10.0%)**, visually demonstrating the impact of cross-faculty pooling.

### Panel 2: Add Booking Request with Web Capacity Validation (`TC66–TC69`)
1. Enter a **Request ID**, select the **Requester Faculty** (`ICT`, `SCI`, `SEEN`), **Passenger Count**, **Requested Vans**, **Trip Scope** (Out-of-Province / In-Province), and **Trip Work Duration**.
2. Click **"+ Validate Capacity & Add to Queue"**.
3. The web backend enforces the capacity rule before admitting any request into the MILP queue:
   $$\text{Passenger Count } (P_r) \le \text{Van Capacity } (C_v) \times \text{Requested Vans } (K_r)$$
   - If a user requests 1 van for 15 passengers, or 2 vans for 23 passengers (exceeding $11 \times 2 = 22$ seats as in Test Case `TC68`), the web server immediately blocks the submission with an **`INVALID_INPUT`** alert banner.
   - Valid requests are appended to the queue and solved automatically.

### Panel 3: KPI Summary Cards & Request-Level Allocation Schedule
- **5 Real-Time KPI Cards:** Display Requests Fulfilled, Passengers Served, Cross-Faculty Loans, Safety/HOS Violations (`0`), and COIN-OR CBC Solve Time.
- **Request-Level Schedule Table:** Displays each request's ID, faculty, passengers served vs. requested, scope, schedule window, assigned van and driver, cross-faculty loan badge, outcome badge, and detailed allocation rationale (reproducing Table 6 of the research paper).

---

## 5. Command-Line Interface (CLI) & REST API Reference

### 5.1 Command-Line Execution (`van_allocation_engine.py`)
```powershell
# Solve the N=10 real pending queue preset and print JSON output to console
python van_allocation_engine.py --mode demo

# Print all verified v6 empirical benchmark tables from raw_output/
python van_allocation_engine.py --mode summary
```

### 5.2 Web Server REST API Endpoints
- `GET /api/preset` — Returns the 10 real pending requests, faculty vans, drivers, and pre-existing schedule blocks (`FixedBusyBlocks`).
- `POST /api/validate` — Validates passenger count against requested vans (`{"pax": 15, "requested_vans": 2, "van_capacity": 11}`).
- `POST /api/solve` — Solves the MILP allocation model for any JSON payload of requests, vans, drivers, and `config` parameters.
