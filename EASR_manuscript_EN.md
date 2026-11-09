Research Article

# Optimal cross-faculty shared passenger van allocation with safety-compliant hours-of-service constraints using mixed-integer linear programming

**Author Name^1^ and Corresponding Author^1,\*^**

^1^Department of Information and Communication Technology, School of Information and Communication Technology, Public University Case Study, 56000, Thailand.

\*Corresponding author. Tel.: +66-00-000-0000; Email address: corresponding.author@university.ac.th

## Abstract
Public universities frequently operate decentralized passenger van fleets managed independently by individual faculties. This siloed structure creates severe utilization imbalances, where excess demand in one faculty leads to trip rejections or costly external rentals while vans in neighboring faculties remain idle. Furthermore, manual first-come, first-served (FCFS) dispatching lacks systematic mechanisms to enforce cumulative driver fatigue limits and cross-faculty borrowing priorities. This study formulates a Mixed-Integer Linear Programming (MILP) decision support model for multi-faculty shared passenger van and driver allocation over a rolling 14-day planning horizon. The mathematical formulation integrates hierarchical goal programming with hard safety constraints <span style="color:red">parameterized from Thai public-sector and transport duty regulations and international Hours-of-Service (HOS) standards</span>—specifically a 14-hour daily workload cap, a 72-hour bi-weekly cumulative workload limit, and a mandatory 10-hour inter-shift rest period. The model is evaluated using cleaned operational data from two faculties (Information and Communication Technology [ICT] and Science [SCI], comprising 383 valid booking requests and 2,169 driver work logs) combined with a stress-test faculty profile (Energy and Environment [SEEN]) at a public university in Thailand. Across an exhaustive 864-scenario state space weighted by empirical demand probabilities, the MILP model achieves a 97.09% full-assignment rate with 100% algorithmic agreement against an independent rule-based verification oracle. In comparative simulations across 900 multi-request scenarios, the MILP framework outperforms safety-compliant FCFS (FCFS-B) and shortest-duration-first (Heuristic-SDF) baselines by 20.6 percentage points in request fulfillment (97.6% vs. 77.0%) while maintaining zero safety violations. Under moderate demand (15 requests per two weeks), cross-faculty pooling achieves a 93.3% service level with a single van per faculty, matching the performance of two isolated vans per faculty under manual dispatching and solving up to 60 concurrent requests in 2.14 seconds.

**Keywords:** Mixed-integer linear programming, Shared fleet allocation, Campus logistics, Hours-of-service regulations, Cross-faculty resource pooling, Decision support system

---

## 1. Introduction

### 1.1 Background and problem statement
Resource allocation efficiency is a cornerstone of sustainable campus management in modern public higher education institutions. Passenger van fleets represent a vital logistical asset supporting academic field trips, inter-campus administration, research excursions, and community outreach. Despite substantial capital depreciation, insurance, maintenance, and driver personnel costs, most public universities in developing and emerging economies continue to manage their vehicle fleets under a decentralized, faculty-owned administrative structure. Under this siloed paradigm, each faculty independently dispatches its own vehicles and full-time drivers to serve internal requests, without an automated mechanism to pool idle capacity across faculties.

Empirical operational audits at a public university in northern Thailand—spanning the School of Information and Communication Technology (ICT), the School of Science (SCI), and the School of Energy and Environment (SEEN)—reveal pronounced spatiotemporal demand asymmetry. During peak examination or fieldwork weeks, one faculty frequently experiences simultaneous multi-day out-of-province requests that exceed its internal fleet capacity, resulting in trip cancellations or expensive commercial chartering. Concurrently, passenger vans in adjacent faculties remain parked with high idle availability (empirical free rates of 69.1% in ICT and 75.8% in SCI). Although informal cross-faculty vehicle borrowing is permitted in principle, administrative coordinators rely on manual calendar inspection and First-Come, First-Served (FCFS) booking rules. Without an optimization engine, dispatchers face two recurring operational failures: (i) myopic allocation, where assigning a vehicle to an early short request blocks a subsequent multi-day inter-provincial mission, and (ii) inadvertent driver fatigue violations when tracking cumulative work hours and overnight rest intervals across discontinuous trips.

### 1.2 Literature review and research gaps
The Vehicle Routing Problem (VRP) and Fleet Assignment Problem (FAP) have been extensively studied since the seminal formulation by Dantzig and Ramser [1]. In commercial logistics and public transit, Mixed-Integer Linear Programming (MILP) serves as the standard mathematical paradigm for joint vehicle-crew scheduling, guaranteeing global optimality and explicit dual optimality bounds [2-4]. Cordeau et al. [3] and Savelsbergh and Sol [4] demonstrated that exact mathematical programming for pickup-and-delivery and fleet sizing problems can reduce active fleet requirements by 15–25% compared to decentralized manual dispatching. In shared mobility systems, dynamic fleet pooling and repositioning models developed by Boyacı et al. [5], Jorge et al. [6], and Nair and Miller-Hooks [7] confirm that consolidating fragmented sub-fleets buffers stochastic demand spikes. However, commercial car-sharing models [5-8] primarily focus on self-drive passenger vehicles or commercial ride-hailing fleets, which omit institutional ownership hierarchy—namely, the requirement that a faculty's vehicle must prioritize its home faculty's requests and only lend surplus capacity when internal demand is satisfied.

A second critical dimension is regulatory safety compliance. Driver fatigue is a leading cause of severe road accidents in passenger transport [9-11]. Goel and Vidal [9] and Prescott-Gagnon et al. [10] integrated mandatory Hours-of-Service (HOS) rules into commercial freight routing, showing that enforcing rest windows alters tour feasibility but eliminates fatigue-induced hazards. Under United States Federal Motor Carrier Safety Administration (FMCSA) regulations [12] and European Union Regulation (EC) No 561/2006 [13], commercial drivers are restricted by daily duty windows (14 hours), minimum inter-shift rest periods (10–11 consecutive hours), and weekly cumulative work caps (60–70 hours over 7–8 days). In Thailand, statutory passenger transport safety is governed by the Land Transport Act B.E. 2522 (Sections 103 and 103/1) and the Road Traffic Act B.E. 2522 (Section 43 ter) [14], which mandate a 1-hour rest after 4 consecutive driving hours and limit standard driving to 8–10 hours per day, alongside public-sector overtime regulations that cap combined regular and overtime duty at 12–14 hours per day and 36 hours per week (72 hours over a 14-day bi-weekly cycle) <span style="color:red">[15]</span>. The 72-hour bi-weekly ceiling adopted in this study is therefore derived from the public-sector duty limit and is stricter than the 60–70 hours per 7–8 days permitted under the FMCSA and EU rules; Section 3.4 examines alternative ceilings of 48–96 hours. Despite these legal mandates, campus vehicle booking systems rarely embed multi-day cumulative work-hour tracking and minimum 10-hour turnaround rest constraints directly into an automated dispatch solver.

Furthermore, existing university transport studies predominantly focus on fixed-route student shuttle buses [16, 17] rather than on-demand, multi-day administrative and academic van charters. Meanwhile, comparative studies contrasting greedy FCFS scheduling against batch mathematical optimization in resource-constrained service systems [18-21] indicate that myopic rules suffer rapid performance degradation as temporal overlap increases.

### 1.3 Research contributions
To bridge these gaps, this study develops and validates a safety-compliant MILP optimization model for cross-faculty passenger van and driver allocation. The main contributions are threefold:
1. **Hierarchical cross-faculty MILP formulation with statutory HOS constraints:** We formulate a lexicographic multi-objective MILP model solved via the CBC branch-and-cut engine [18] that jointly handles request splitting across multiple vans, vehicle-driver pairing, home-faculty preference penalties, and three hard safety rules (14-hour daily duty cap, 72-hour 14-day rolling workload cap, and 10-hour inter-shift rest interval).
2. **Empirical validation using multi-faculty university operational logs:** We construct a rigorous validation pipeline combining real booking and driver duty records from two faculties (ICT and SCI) with a stress-test faculty profile (SEEN), evaluating the model across an exhaustive 864-scenario parametric state space and real pending booking queues.
3. **Multi-baseline benchmarking and policy sensitivity analysis:** We benchmark the MILP solver against three operational baselines—greedy FCFS without fatigue checks (`FCFS-A`), safety-compliant FCFS (`FCFS-B`), and a Shortest-Duration-First heuristic (`Heuristic-SDF`)—across varying fleet capacities, HOS quota thresholds, and request scales ($N = 5$ to $60$).

---

## 2. Materials and methods

### 2.1 Empirical dataset and preprocessing
Operational data were collected from the vehicle reservation and driver log databases of a public university in Thailand covering academic years 2023–2025 (B.E. 2566–2568). The dataset encompasses three faculties: ICT, SCI, and SEEN. To ensure data integrity and prevent primary-key collisions across independently maintained faculty spreadsheets, automated data cleaning was executed prior to optimization:
- **Booking requests (`bookings`):** Raw records totaled 650 requests. For ICT, 247 raw records yielded 246 valid approved bookings after removing 1 canceled entry. For SCI, eliminating 841 blank trailing spreadsheet rows from the raw export left 156 true booking records; standardizing status labels (`approve` $\rightarrow$ `approved`, `delete` $\rightarrow$ `cancel`) and filtering incomplete timestamps yielded 137 valid bookings. Because historical digitized logs for SEEN were unavailable during the data collection phase, 247 synthetic stress-test requests were generated to represent a zero-fleet or constrained-fleet partner faculty. In total, 630 clean booking records were retained, while empirical probability estimation was strictly restricted to the $N = 383$ verified real bookings from ICT and SCI.
- **Driver work logs (`driver_logs`):** Raw driver duty records totaled 2,798 entries (598 from ICT, 1,602 from SCI, and 598 simulated for SEEN). In the SCI dataset, dates recorded in the Thai Buddhist Era (`2566–2568`, plus 8 typographical entries recorded as `2577`) were converted to the Gregorian calendar prior to timestamp parsing to avoid 64-bit nanosecond overflow (`OutOfBoundsDatetime`), and dot-delimited time strings (e.g., `10.00`) were normalized to ISO `HH:MM:SS` format. This pipeline recovered 1,571 valid SCI driver logs (98.1% recovery rate), yielding 2,169 real driver logs across ICT and SCI (2,767 total clean logs across all three faculties).
- **Pre-existing schedule blocks (`FixedBusyBlocks`):** Historical logs of retired or transferred drivers (`_OLD`) were isolated for statistical profiling, whereas active duty logs of current drivers (`_NOW`) within the active planning window were converted into immutable busy intervals (`ICT_DRIVER_NOW`: 411 blocks; `SCI_DRIVER_NOW`: 668 blocks; `SEEN_DRIVER_NOW`: 229 blocks).

### 2.2 Mathematical formulation of the MILP model
Let $R$ denote the set of pending booking requests, $V$ the set of available passenger vans across all participating faculties, $D$ the set of active drivers, $T = \{1, 2, \dots, 14\}$ the discrete days in a 14-day rolling planning horizon, and $F = \{\text{ICT}, \text{SCI}, \text{SEEN}\}$ the set of faculties. Table 1 summarizes the model sets, parameters, and decision variables.

**Table 1** Sets, parameters, and decision variables of the MILP van allocation model

| Symbol | Type | Description |
| :--- | :--- | :--- |
| $r \in R$ | Index / Set | Pending vehicle requests within the 14-day planning window |
| $v \in V, d \in D$ | Index / Set | Available passenger vans ($V$) and active drivers ($D$) across all faculties |
| $t \in T$ | Index / Set | Discrete days in the 14-day rolling horizon ($|T| = 14$) |
| $P_r, K_r$ | Parameter | Total passenger count ($P_r$) and maximum vans allowed for splitting ($K_r \in \{1,2,3\}$) |
| $\tau_r^s, \tau_r^e, H_{r,t}$ | Parameter | Start timestamp ($\tau_r^s$), end timestamp ($\tau_r^e$), and work hours of request $r$ on day $t$ ($H_{r,t}$) |
| $Q_r \in \{0,1\}$ | Parameter | Trip scope indicator ($1$ = out-of-province requiring a dedicated driver, $0$ = in-province) |
| $C_v$ | Parameter | Seating capacity of van $v$ ($C_v = 11$ seats for standard university commuter vans) |
| $H_{d,t}^{\text{base}}, H_{\max}^{\text{day}}, H_{\max}^{14\text{d}}$ | Parameter | Pre-existing hours of driver $d$ on day $t$; daily cap ($14\text{ h}$); 14-day cap ($72\text{ h}$) |
| $y_{r,v} \in \{0,1\}$ | Binary var. | $1$ if van $v$ is assigned to serve request $r$; $0$ otherwise |
| $x_{r,v,d} \in \{0,1\}$ | Binary var. | $1$ if driver $d$ is paired with van $v$ to serve request $r$; $0$ otherwise |
| $p_{r,v} \in \mathbb{Z}_{\ge 0}$ | Integer var. | Number of passengers of request $r$ allocated to van $v$ |
| $u_r \in \mathbb{Z}_{\ge 0}$ | Integer var. | Unserved passenger shortfall for request $r$ (slack variable) |
| $z_r \in \{0,1\}$ | Binary var. | $1$ if request $r$ is fully assigned ($u_r = 0$); $0$ otherwise |
| $w_{d,t} \in \{0,1\}$ | Binary var. | $1$ if driver $d$ performs any duty on day $t$; $0$ otherwise |

#### 2.2.1 Objective function
The model minimizes a lexicographically weighted cost function $Z$ comprising four hierarchical tiers:
$$\min Z = \sum_{r \in R} W_1 u_r - \sum_{r \in R} W_2 z_r + \sum_{r \in R} \sum_{v \in V} W_{3,r,v} y_{r,v} + \sum_{r \in R} \sum_{v \in V} \sum_{d \in D} W_{4,r,v,d} x_{r,v,d} \tag{1}$$
where $W_1 = 10^7$ penalizes each unserved passenger ($u_r$), $W_2 = 5 \times 10^5$ rewards full request completion ($z_r$), $W_{3,r,v} \in [50, 1000]$ penalizes extra van usage and cross-faculty borrowing (assigning zero cross-faculty penalty when the van's home faculty matches the requester's faculty $f_v = f_r$, and a positive penalty otherwise), and $W_{4,r,v,d} \in [10, 500]$ enforces preferred vehicle-driver pairing (prioritizing a van's designated primary driver).

#### 2.2.2 Passenger coverage and fleet splitting constraints
Every request $r \in R$ must account for all $P_r$ passengers either through allocated seats across assigned vans or via the unserved slack variable $u_r$:
$$\sum_{v \in V} p_{r,v} + u_r = P_r, \quad \forall r \in R \tag{2}$$
$$y_{r,v} \le p_{r,v} \le C_v y_{r,v}, \quad \forall r \in R, \forall v \in V \tag{3}$$
$$\sum_{v \in V} y_{r,v} \le K_r, \quad \forall r \in R \tag{4}$$
$$P_r (1 - z_r) \ge u_r, \quad \text{and} \quad u_r \ge 1 - z_r, \quad \forall r \in R \tag{5}$$
Constraint (3) ensures a van carries passengers only if selected ($y_{r,v}=1$) without exceeding its capacity $C_v = 11$, and prevents empty ghost assignments ($p_{r,v} \ge y_{r,v}$). Constraint (4) bounds the maximum number of split vans per request to $K_r$, and Constraint (5) links the binary full-fulfillment indicator $z_r$ to zero unserved passengers ($u_r = 0 \iff z_r = 1$).

#### 2.2.3 Driver pairing and spatiotemporal non-overlapping constraints
Out-of-province missions ($Q_r = 1$) strictly require a qualified driver for each assigned van, whereas in-province missions ($Q_r = 0$) allow optional self-driving by authorized faculty staff if no driver is assigned:
$$\sum_{d \in D} x_{r,v,d} = y_{r,v}, \quad \forall r \in R \text{ with } Q_r = 1, \forall v \in V \tag{6}$$
$$\sum_{d \in D} x_{r,v,d} \le y_{r,v}, \quad \forall r \in R \text{ with } Q_r = 0, \forall v \in V \tag{7}$$
$$\sum_{v \in V} x_{r,v,d} \le 1, \quad \forall r \in R, \forall d \in D \tag{8}$$
For any pair of requests $(r_1, r_2) \in \mathcal{O}_V$ whose time intervals overlap ($\tau_{r_1}^s < \tau_{r_2}^e$ and $\tau_{r_2}^s < \tau_{r_1}^e$), the same van cannot be assigned to both requests:
$$y_{r_1,v} + y_{r_2,v} \le 1, \quad \forall (r_1, r_2) \in \mathcal{O}_V, \forall v \in V \tag{9}$$
Similarly, if van $v$ or driver $d$ has a pre-existing committed schedule block in $\text{Busy}(v)$ or $\text{Busy}(d)$ overlapping request $r$, the corresponding assignment variable is fixed to zero ($y_{r,v} = 0$ or $x_{r,v,d} = 0$).

#### 2.2.4 Statutory Hours-of-Service (HOS) and rest constraints
To enforce driver-duty limits aligned with Thai regulations [14], public-sector overtime limits <span style="color:red">[15]</span>, and international HOS fatigue benchmarks [12, 13], three safety constraints are enforced for every driver $d \in D$:
$$\sum_{r \in R} \sum_{v \in V} x_{r,v,d} + \sum_{r' \in R} \sum_{v' \in V} x_{r',v',d} \le 1, \quad \forall (r, r') \in \mathcal{O}_D(\Delta_{\text{rest}}), \forall d \in D \tag{10}$$
$$H_{d,t}^{\text{base}} + \sum_{r \in R} \sum_{v \in V} H_{r,t} x_{r,v,d} \le H_{\max}^{\text{day}} w_{d,t}, \quad \forall d \in D, \forall t \in T \tag{11}$$
$$\sum_{t \in T} H_{d,t}^{\text{base}} + \sum_{t \in T} \sum_{r \in R} \sum_{v \in V} H_{r,t} x_{r,v,d} \le H_{\max}^{14\text{d}}, \quad \forall d \in D \tag{12}$$
where $\mathcal{O}_D(\Delta_{\text{rest}})$ is the set of request pairs separated by less than the minimum mandatory rest turnaround $\Delta_{\text{rest}} = 10\text{ h}$ (i.e., $\tau_{r}^s < \tau_{r'}^e + 10\text{ h}$ and $\tau_{r'}^s < \tau_{r}^e + 10\text{ h}$), $H_{\max}^{\text{day}} = 14\text{ h}$ caps total daily operational duty, and $H_{\max}^{14\text{d}} = 72\text{ h}$ limits cumulative bi-weekly workload over the 14-day horizon.

### 2.3 Baseline algorithms and experimental design
To evaluate the operational value of global optimization over manual campus dispatching, the MILP model (implemented in Python 3.11 using PuLP and the COIN-OR CBC solver [18]) is compared against three baseline algorithms:
1. **Greedy FCFS without HOS Fatigue Enforcement (`FCFS-A`):** Processes requests sequentially in chronological order of submission (`created_at`). It checks only physical vehicle/driver overlap and seating capacity, ignoring the 14h/72h workload caps and 10h inter-shift rest rule. This baseline reflects informal manual dispatching when cumulative driver logs are not cross-checked.
2. **Safety-Compliant Greedy FCFS (`FCFS-B`):** Processes requests chronologically by `created_at` while strictly enforcing all hard constraints (2)–(12). If a request cannot be satisfied without violating HOS limits, it is rejected or partially served, without backtracking to swap earlier assignments.
3. **Shortest-Duration-First Heuristic (`Heuristic-SDF`):** A rule-based greedy heuristic that sorts pending requests in ascending order of total trip duration ($\tau_r^e - \tau_r^s$) and passenger demand ($P_r$) before applying safety-compliant sequential assignment, aiming to maximize the count of completed requests.

Four experimental suites were executed:
- **Experiment 1 (Exhaustive 864-Scenario State Space):** Evaluates all $3 \times 2 \times 3 \times 2 \times 3 \times 8 = 864$ valid combinations of requester faculty ($|\{\text{ICT}, \text{SCI}, \text{SEEN}\}|=3$), trip scope ($|\{\text{in-province}, \text{out-of-province}\}|=2$), passenger-vehicle tier ($|\{(\le 11, 1\text{ van}), (\le 11, 2\text{ vans}), (>11, 2\text{ vans})\}|=3$), urgency ($2$), trip duration ($|\{1\text{d}, 2\text{d}, \ge 3\text{d}\}|=3$), and binary availability states across the 3 faculty van-driver units ($2^3 = 8$). Every MILP solution is cross-checked against an independent deterministic Rule-Based Verification Oracle.
- **Experiment 2 (Real Pending Queue & Multi-Request Benchmarks):** Compares all four algorithms on (a) the $N = 10$ real pending requests extracted from the university's active booking queue and (b) 900 synthetic high-contention multi-request scenarios (30 random seeds $\times$ 30 demand configurations).
- **Experiment 3 (Fleet Sizing & HOS Quota Sensitivity):** Tests fleet capacity from 1 to 3 vans per faculty across request loads $N \in \{5, 10, 15, 20, 25, 30\}$ and varies the 14-day HOS cap $H_{\max}^{14\text{d}} \in \{48, 60, 72, 84, 96\}\text{ h}$.
- **Experiment 4 (Computational Scalability):** Measures solver wall-clock runtime and optimality gap across batch sizes $N \in \{5, 10, 15, 20, 25, 30, 40, 50, 60\}$.

---

## 3. Results

### 3.1 Empirical fleet utilization and probability weights
Table 2 presents the empirical probability distributions derived strictly from the cleaned operational records of the two faculties with verified logs ($N = 383$ bookings and $N = 2,169$ driver logs across ICT and SCI). ICT accounts for 64.2% of booking demand and SCI accounts for 35.8%. In-province trips slightly outnumber out-of-province trips (54.3% vs. 45.7%). Single-van trips ($\le 11$ passengers) represent 100% of historical single-ticket entries (mean $4.11 \pm 3.19$ passengers, median $3.0$, maximum $11.0$), as larger groups historically submitted multiple separate tickets under the legacy system. Single-day trips dominate at 86.7%, whereas multi-day trips of $\ge 3$ days account for 8.6%. Historical daily fleet availability averages 69.1% for ICT and 75.8% for SCI, confirming substantial idle capacity suitable for cross-faculty pooling.

**Table 2** Empirical probability distributions extracted from cleaned university logs (ICT and SCI)

| Parameter Dimension | Category / Level | Empirical Probability (v6 Real Data) | Uniform Synthetic Baseline | Data Source & Sample Size |
| :--- | :--- | :--- | :--- | :--- |
| **Requester Faculty ($f_r$)** | ICT / SCI / SEEN | $0.642$ / $0.358$ / $0.000^*$ | $0.333$ / $0.333$ / $0.333$ | Clean real bookings ($N = 383$) |
| **Trip Scope ($Q_r$)** | In-province / Out-of-province | $0.543$ / $0.457$ | $0.500$ / $0.500$ | Clean real bookings ($N = 383$) |
| **Passenger Group ($P_r$)** | $\le 11$ / $12\text{–}22$ / $23\text{–}33$ pax | $1.000$ / $0.000^*$ / $0.000^*$ | $0.333$ / $0.333$ / $0.333$ | Clean real bookings ($\text{Mean}=4.11, \text{SD}=3.19$) |
| **Trip Duration** | $1\text{ day}$ / $2\text{ days}$ / $\ge 3\text{ days}$ | $0.867$ / $0.047$ / $0.086$ | $0.333$ / $0.333$ / $0.333$ | Clean real bookings ($N = 383$) |
| **Fleet Free Rate** | ICT free / SCI free | $0.691$ / $0.758$ | $0.850$ / $0.850$ | Clean real driver logs ($N = 2,169$) |

*\*Note: Categories with zero historical single-ticket observations use Laplace smoothing ($\alpha = 0.01\text{–}0.10$) during exhaustive state-space stress testing so extreme multi-van and partner-faculty scenarios retain non-zero analytical weight.*

### 3.2 Exhaustive 864-scenario evaluation
Table 3 compares the unweighted scenario counts, synthetic-weighted probabilities, and empirical-weighted probabilities across all 864 parametric scenarios. Verification against the independent Rule-Based Oracle confirmed a **100.0% exact match (864/864 scenarios)** in feasibility, passenger allocation, and cost hierarchy, with zero HOS violations. When weighted by the empirical university distributions, **97.09% of expected operational scenarios achieve full passenger assignment**, 0.84% result in partial assignment (serving 11 of 15–22 passengers when 2 vans are requested but only one van is free), and 2.07% are unassigned (occurring only when all vans are busy or out-of-province requests lack any HOS-compliant driver).

**Table 3** Exhaustive evaluation across 864 parametric scenarios and probability weighting schemes

| Allocation Outcome | Scenario Count ($N=864$) | Unweighted Share (%) | Synthetic Weight (%) | Empirical Weight (v6 Real Data, %) | Safety Violations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Fully Assigned ($z_r = 1$)** | 540 | 62.50% | 95.00% | **97.09%** | 0 |
| **Partially Assigned ($0 < u_r < P_r$)** | 216 | 25.00% | 2.30% | **0.84%** | 0 |
| **Unassigned ($u_r = P_r$)** | 108 | 12.50% | 2.70% | **2.07%** | 0 |
| **Total / Oracle Agreement** | **864 (100% match)** | **100.00%** | **100.00%** | **100.00%** | **0** |

Table 4 decomposes the 324 scenarios that were not fully assigned. All 216 partial assignments arise when a multi-van request (2 vans requested) finds only one van free, so that 11 passengers are served. The 108 unassigned scenarios occur when none of the three faculty van-driver units (`T01`, `T02`, `T03`) is available (`Free_vans = "-"`), comprising <span style="color:red">54</span> in-province scenarios (<span style="color:red">1.12%</span> empirical weight) where all vans are occupied and <span style="color:red">54</span> out-of-province scenarios (<span style="color:red">0.95%</span> empirical weight) where no van with an HOS-compliant driver is available.

**Table 4** Causes of non-full assignment among the 864 parametric scenarios (324 scenarios)

| Outcome | Cause | Scenario count | Empirical weight (%) |
| :--- | :--- | :--- | :--- |
| Partially assigned | Multi-van request, only one van free (11 passengers served) | 216 | 0.84% |
| Unassigned | All vans busy or unavailable (in-province requests) | <span style="color:red">54</span> | <span style="color:red">1.12%</span> |
| Unassigned | Out-of-province request, no HOS-compliant driver / van unit available | <span style="color:red">54</span> | <span style="color:red">0.95%</span> |
| **Unassigned (subtotal)** | | **108** | **2.07%** |

*\*Note: Because each resource unit (`T01`–`T03`) in the 864-scenario grid bundles a faculty van with its primary driver, all 108 unassigned scenarios share the aggregate state `Free_vans = "-"` (`Reason = รถว่างไม่พอ` in `scenario_exhaustive_results.csv`, i.e., 108 scenarios = 2.07% total), partitioned equally into 54 in-province scenarios (1.12%) and 54 out-of-province scenarios (0.95%).*

### 3.3 Comparative evaluation on real pending requests and synthetic demand
Table 5 summarizes algorithmic performance across both the real pending request queue ($N = 10$ concurrent requests spanning ICT, SCI, and SEEN) and the 900 multi-request synthetic stress-test batches.

**Table 5** Comparison of MILP against baseline scheduling algorithms on real and synthetic benchmark suites

| Benchmark Suite | Metric | MILP (Proposed) | FCFS-A (No HOS Check) | FCFS-B (Safety-Compliant) | Heuristic-SDF (Shortest First) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Real Pending Queue ($N = 10$)** | Fully assigned requests (%) | **90.0% (9/10)** | 100.0% (10/10) | 90.0% (9/10) | 90.0% (9/10) |
| | Passengers served / Total | <span style="color:red">**62 / 69 (89.9%)**</span> | <span style="color:red">69 / 69 (100.0%)</span> | <span style="color:red">62 / 69 (89.9%)</span> | <span style="color:red">62 / 69 (89.9%)</span> |
| | Cross-faculty van loans | **8 trips (from SCI)** | <span style="color:red">4 trips</span> | 8 trips | 8 trips |
| | Safety / HOS violations | **0** | **7 (<10h rest)** | 0 | 0 |
| | Mean solve time (s) | **0.246 s** | 0.010 s | 1.502 s | 1.296 s |
| **Synthetic Batches (900 runs)** | Request fulfillment rate (%) | **97.6%** | 98.2% | 77.0% | 79.4% |
| | Passenger fulfillment rate (%) | **97.5%** | 98.4% | 75.5% | 78.1% |
| | Total safety violations | **0** | **312 violations** | 0 | 0 |
| | Mean solve time (s) | **0.238 s** | 0.002 s | 0.002 s | 0.002 s |

On the real pending queue ($N = 10$), recovering the SCI driver logs (`SCI_SCI_DRIVER_NOW`) enables the MILP model to fulfill **9 out of 10 requests (90.0%, serving <span style="color:red">62 of 69</span> passengers)** in 0.246 seconds with **zero safety violations**, executing 8 cross-faculty van loans from SCI to cover ICT and SEEN requests while ICT's and SEEN's primary drivers are committed to pre-existing schedules or rest turnarounds. Only a single in-province request (<span style="color:red">`SEEN_SEEN_BK_0208`</span> on 2 April 2026, <span style="color:red">7</span> passengers) is rejected because the SEEN driver has only <span style="color:red">5.8 h</span> of rest (<10 h limit) after a morning walk-in duty, the ICT van is committed to a pre-existing schedule, and the SCI backup van is already assigned to the overlapping request <span style="color:red">`SEEN_SEEN_BK_0207`</span> (09:00–17:28 on the same day). By contrast, `FCFS-A` blindly assigns all 10 requests, triggering **7 severe inter-shift rest violations (<10h rest)**. In the 900 multi-request synthetic benchmarks where multi-day and multi-van requests compete for overlapping slots, MILP achieves a **97.6% request fulfillment rate**, outperforming `FCFS-B` (77.0%) by **20.6 percentage points** and `Heuristic-SDF` (79.4%) by **18.2 percentage points** (Figure 1).

![Figure 1 Comparison of request fulfillment rate and safety compliance across scheduling algorithms](raw_output/baseline_fulfillment.png)
**Figure 1** Comparison of request fulfillment rate and safety compliance across scheduling algorithms

The slightly higher fulfillment of `FCFS-A` on the synthetic batches (98.2% vs. 97.6%) should not be read as superior performance: `FCFS-A` ignores the 14 h daily cap, the 72 h bi-weekly cap, and the 10 h rest rule, and consequently accumulates 312 violations (Table 5). The 0.6-percentage-point gap can be interpreted as the capacity cost of enforcing full safety compliance.

Table 6 reports the outcome of each of the 10 real pending requests under the MILP model. The MILP, `FCFS-B`, and `Heuristic-SDF` methods fully assign the same number of requests and serve the same number of passengers on this queue (Table 5). The real queue contains only <span style="color:red">1</span> pair of requests with overlapping time windows (<span style="color:red">`SEEN_SEEN_BK_0207` and `SEEN_SEEN_BK_0208` on 2 April 2026</span>), so the sequential rules rarely block a later request; the advantage of global optimization emerges under the higher contention of the 900 synthetic batches.

**Table 6** Request-level results of the MILP model on the real pending queue ($N = 10$)

| Request ID | Faculty | Passengers | Scope / duration | Assigned van (driver) | Cross-faculty loan | Outcome | Reason |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| <span style="color:red">ICT_BK000447</span> | <span style="color:red">ICT</span> | <span style="color:red">4</span> | <span style="color:red">Out-of-province, 1 day (9.00 h)</span> | <span style="color:red">SCI van (SCI_DRIVER_NOW)</span> | <span style="color:red">Yes (from SCI)</span> | <span style="color:red">Assigned</span> | <span style="color:red">ICT van busy on walk-in duty & over 14 h/72 h HOS caps; borrowed SCI van</span> |
| <span style="color:red">SEEN_SEEN_BK_0153</span> | <span style="color:red">SEEN</span> | <span style="color:red">11</span> | <span style="color:red">Out-of-province, 1 day (4.20 h)</span> | <span style="color:red">SEEN van (SEEN_DRIVER_NOW)</span> | <span style="color:red">No (own van)</span> | <span style="color:red">Assigned</span> | <span style="color:red">Home faculty van and driver available and compliant with all HOS rules</span> |
| <span style="color:red">SEEN_SEEN_BK_0172</span> | <span style="color:red">SEEN</span> | <span style="color:red">10</span> | <span style="color:red">Out-of-province, 1 day (4.78 h)</span> | <span style="color:red">SCI van (SCI_DRIVER_NOW)</span> | <span style="color:red">Yes (from SCI)</span> | <span style="color:red">Assigned</span> | <span style="color:red">SEEN driver had 6.1 h rest (<10 h limit) after prior booked trip; borrowed SCI van</span> |
| <span style="color:red">SEEN_SEEN_BK_0186</span> | <span style="color:red">SEEN</span> | <span style="color:red">2</span> | <span style="color:red">In-province, 1 day (7.63 h)</span> | <span style="color:red">SCI van (SCI_DRIVER_NOW)</span> | <span style="color:red">Yes (from SCI)</span> | <span style="color:red">Assigned</span> | <span style="color:red">SEEN van overlaps booked trip & exceeds 14 h daily cap (14.9 h); borrowed SCI van</span> |
| <span style="color:red">SEEN_SEEN_BK_0200</span> | <span style="color:red">SEEN</span> | <span style="color:red">11</span> | <span style="color:red">In-province, 1 day (1.68 h)</span> | <span style="color:red">SCI van (SCI_DRIVER_NOW)</span> | <span style="color:red">Yes (from SCI)</span> | <span style="color:red">Assigned</span> | <span style="color:red">SEEN van overlaps pre-existing walk-in duty (11:55–12:59); borrowed SCI van</span> |
| <span style="color:red">SEEN_SEEN_BK_0205</span> | <span style="color:red">SEEN</span> | <span style="color:red">9</span> | <span style="color:red">Out-of-province, 1 day (4.70 h)</span> | <span style="color:red">SCI van (SCI_DRIVER_NOW)</span> | <span style="color:red">Yes (from SCI)</span> | <span style="color:red">Assigned</span> | <span style="color:red">SEEN driver had 7.2 h rest (<10 h limit) after prior walk-in duty; borrowed SCI van</span> |
| <span style="color:red">SEEN_SEEN_BK_0207</span> | <span style="color:red">SEEN</span> | <span style="color:red">10</span> | <span style="color:red">Out-of-province, 1 day (8.47 h)</span> | <span style="color:red">SCI van (SCI_DRIVER_NOW)</span> | <span style="color:red">Yes (from SCI)</span> | <span style="color:red">Assigned</span> | <span style="color:red">SEEN van overlaps morning walk-in duty (08:47–10:15); borrowed SCI van</span> |
| <span style="color:red">SEEN_SEEN_BK_0221</span> | <span style="color:red">SEEN</span> | <span style="color:red">4</span> | <span style="color:red">Out-of-province, 1 day (1.18 h)</span> | <span style="color:red">SCI van (SCI_DRIVER_NOW)</span> | <span style="color:red">Yes (from SCI)</span> | <span style="color:red">Assigned</span> | <span style="color:red">SEEN driver had 9.5 h rest (<10 h limit) after prior walk-in duty; borrowed SCI van</span> |
| <span style="color:red">SEEN_SEEN_BK_0225</span> | <span style="color:red">SEEN</span> | <span style="color:red">1</span> | <span style="color:red">In-province, 1 day (5.35 h)</span> | <span style="color:red">SCI van (SCI_DRIVER_NOW)</span> | <span style="color:red">Yes (from SCI)</span> | <span style="color:red">Assigned</span> | <span style="color:red">SEEN driver had 7.4 h rest (<10 h limit) before next booked trip; borrowed SCI van</span> |
| <span style="color:red">SEEN_SEEN_BK_0208</span> | <span style="color:red">SEEN</span> | <span style="color:red">7</span> | <span style="color:red">In-province, 1 day (1.05 h)</span> | – | – | Rejected | <span style="color:red">SEEN driver had 5.8 h rest (<10 h); ICT van busy; SCI van serving overlapping SEEN_SEEN_BK_0207</span> |
| **Total** | | <span style="color:red">**62 / 69 served**</span> | <span style="color:red">**9 / 10 vans**</span> | | **8 loans from SCI** | **9 / 10 fully assigned** | |

### 3.4 Sensitivity and computational scalability analysis
Figure 2 and Table 7 illustrate the sensitivity of service fulfillment to fleet size (1, 2, or 3 vans per faculty), bi-weekly HOS workload caps ($H_{\max}^{14\text{d}} \in \{48, \dots, 96\}\text{ h}$), and batch request size ($N \in \{5, \dots, 60\}$).

![Figure 2 Sensitivity analysis of fleet size and HOS quota and computational scalability up to 60 concurrent requests](raw_output/sensitivity_and_scalability.png)
**Figure 2** Sensitivity analysis of fleet size and HOS quota and computational scalability up to 60 concurrent requests

**Table 7** Sensitivity to fleet size and computational scalability across request batch sizes

| Batch Size ($N$) | MILP Fulfillment (1 Van/Fac, %) | FCFS-B Fulfillment (1 Van/Fac, %) | MILP Fulfillment (2 Vans/Fac, %) | FCFS-B Fulfillment (2 Vans/Fac, %) | MILP Solve Time (Mean $\pm$ SD, s) | Optimal Solutions (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| $N = 5$ | 100.0% | 92.0% | 100.0% | 100.0% | $0.08 \pm 0.02\text{ s}$ | 100.0% |
| $N = 10$ | 98.0% | 83.0% | 100.0% | 96.0% | $0.19 \pm 0.04\text{ s}$ | 100.0% |
| $N = 15$ | **93.3%** | 74.7% | 100.0% | **93.3%** | $0.34 \pm 0.07\text{ s}$ | 100.0% |
| $N = 20$ | 86.5% | 68.0% | 99.0% | 88.5% | $0.58 \pm 0.11\text{ s}$ | 100.0% |
| $N = 30$ | 74.0% | 56.3% | 95.7% | 79.0% | $1.02 \pm 0.19\text{ s}$ | 100.0% |
| $N = 40$ | 63.5% | 48.0% | 91.2% | 71.5% | $1.41 \pm 0.25\text{ s}$ | 100.0% |
| $N = 50$ | 55.2% | 41.6% | 86.4% | 65.0% | $1.78 \pm 0.31\text{ s}$ | 100.0% |
| $N = 60$ | 48.8% | 36.5% | 81.7% | 59.3% | **$2.14 \pm 0.38\text{ s}$** | **100.0%** |

At a representative bi-weekly demand of $N = 15$ requests per 14 days, the MILP model operating with only **1 van per faculty** achieves a **93.3% fulfillment rate**, exactly matching the service level of `FCFS-B` operating with **2 vans per faculty (93.3%)**. Regarding HOS quota sensitivity (Table 8; at $N = 20$, 1 van/faculty), tightening $H_{\max}^{14\text{d}}$ from 72 h to 48 h reduces MILP fulfillment from 86.5% to 69.0% (with <span style="color:red">60 h</span> yielding <span style="color:red">79.5%</span>), whereas relaxing it to 84 h or 96 h yields marginal gains (<span style="color:red">88.0%</span> and <span style="color:red">88.5%</span>, respectively) because physical vehicle overlap and the 14-hour daily cap become the active binding bottlenecks. Similarly, when varying the daily duty limit $H_{\max}^{\text{day}} \in \{10, 12, 14, 16\}\text{ h}$ at $\Delta_{\text{rest}} = 10\text{ h}$ (`exp3_hos_sensitivity.csv`, $N = 25$), fulfillment rises from <span style="color:red">69.3%</span> (10 h/day) and <span style="color:red">72.8%</span> (12 h/day) to <span style="color:red">82.9%</span> (14 h/day) and plateaus at <span style="color:red">82.9%</span> (16 h/day). Computationally, because campus van allocation is structured as a discrete interval assignment problem rather than a node-routing VRP, the CBC solver reaches proven global optimality (0.0% mip gap) across 100% of test instances, requiring only **2.14 seconds at $N = 60$ requests**.

**Table 8** Sensitivity of MILP fulfillment to the 14-day HOS cap ($N = 20$, 1 van per faculty) and daily duty cap ($N = 25$, $\Delta_{\text{rest}} = 10\text{ h}$)

| $H_{\max}^{14\text{d}}$ (h) ($N=20$, $H_{\max}^{\text{day}}=14\text{ h}$) | MILP fulfillment (%) | $H_{\max}^{\text{day}}$ (h) ($N=25$, $H_{\max}^{14\text{d}}=72\text{ h}$) | MILP fulfillment (%) |
| :--- | :--- | :--- | :--- |
| 48 | 69.0% | <span style="color:red">10.0</span> | <span style="color:red">69.3%</span> |
| 60 | <span style="color:red">79.5%</span> | <span style="color:red">12.0</span> | <span style="color:red">72.8%</span> |
| 72 | 86.5% | <span style="color:red">14.0 (Baseline)</span> | <span style="color:red">82.9%</span> |
| 84 | <span style="color:red">88.0%</span> | <span style="color:red">16.0</span> | <span style="color:red">82.9%</span> |
| 96 | <span style="color:red">88.5%</span> | – | – |

---

## 4. Discussion

### 4.1 Operational insights and cross-faculty pooling efficacy
The experimental findings demonstrate why manual FCFS dispatching underperforms in multi-faculty university environments. Under `FCFS-B`, an early single-day in-province request submitted by Faculty A occupies Faculty A's van during the middle of the week, blocking a subsequent 3-day out-of-province academic excursion. By solving the 14-day horizon simultaneously, the MILP engine reassigns the short in-province trip to an idle van borrowed from Faculty B (as observed in the 8 cross-faculty loans from SCI in Table 5), preserving the home van and driver with sufficient HOS quota for the multi-day excursion. At moderate demand levels ($N = 15$ requests per two weeks), this pooling effect allows a university to achieve the same 93.3% service reliability with half the active fleet (1 van vs. 2 vans per faculty), deferring capital expenditure on additional vehicles.

### 4.2 Safety compliance under Thai and international HOS standards
A critical operational hazard exposed in Table 5 is that unmonitored greedy scheduling (`FCFS-A`) generates 7 inter-shift rest violations (<10 hours rest between consecutive trips) on the 10 real pending requests and 312 violations across the synthetic suite. Embedding Constraints (10)–(12) directly into the allocation core guarantees 100% compliance with the modeled limits (14 h/day, 72 h/14 days, and 10 h rest), which are parameterized from Thai duty regulations [14, <span style="color:red">15</span>] and international fatigue standards [12, 13], without requiring manual logbook audits by dispatch staff. Moreover, the HOS sensitivity results (Table 8) indicate that the 72-hour bi-weekly ceiling (36 hours/week) and 14-hour daily ceiling lie near the knee of the utilization curve: tightening them to 48 h/14d (or 10 h/day) reduces fulfillment sharply, whereas relaxing them yields only marginal gains.

### 4.3 Limitations and multi-university generalizability
Three practical limitations should be noted. First, while historical bookings and driver logs for ICT and SCI were obtained from real operational archives ($N = 383$ bookings and $N = 2,169$ driver logs), historical records for the third partner faculty (SEEN) were simulated for stress testing; future deployment should integrate live database feeds across all campus faculties. Second, the model enforces daily, bi-weekly, and inter-shift rest limits but does not model the continuous-driving rule (a 1-hour rest after 4 consecutive driving hours) cited in Section 1.2. Third, the current formulation treats trip start and end timestamps ($\tau_r^s, \tau_r^e$) as deterministic inputs and does not route multi-stop passenger pickups across different requests. Nevertheless, because the model parameterizes the faculty set $F$, fleet capacity $C_v$, cross-faculty penalty matrix $W_{3,r,v}$, and HOS thresholds ($H_{\max}^{\text{day}}, H_{\max}^{14\text{d}}, \Delta_{\text{rest}}$) via external configuration tables, other universities can directly adopt the accompanying open-source engine by supplying their own faculty list and vehicle roster.

---

## 5. Conclusions

This paper presented a Mixed-Integer Linear Programming (MILP) framework for cross-faculty passenger van and driver allocation under statutory Hours-of-Service safety constraints. Validated on cleaned operational records from a public university in Thailand (383 real bookings and 2,169 real driver duty logs from ICT and SCI, supplemented by 247 synthetic booking requests and 598 simulated driver logs for SEEN), the proposed model achieved a 97.09% empirical full-assignment rate across 864 parametric scenarios and fulfilled 90.0% of real pending requests (<span style="color:red">62 of 69 passengers</span>) via automated cross-faculty van lending from the School of Science (SCI) with zero safety violations. Across multi-request benchmarks, the MILP model improved request fulfillment by 20.6 percentage points over safety-compliant FCFS (97.6% vs. 77.0%) and 18.2 percentage points over a shortest-duration-first heuristic (79.4%), while solving 60-request batches to proven optimality in 2.14 seconds. Under moderate bi-weekly demand ($N = 15$ requests), cross-faculty optimization enables a single van per faculty to match the service level of two unshared vans per faculty (93.3%), providing university administrators with an immediately deployable, safety-compliant decision support tool.

---

## 6. Acknowledgements

The authors gratefully acknowledge the administrative transport offices of the School of Information and Communication Technology (ICT) and the School of Science (SCI) for providing anonymized historical vehicle reservation and driver duty records supporting this research.

---

## 7. References

[1] Dantzig GB, Ramser JH. The truck dispatching problem. Manage Sci. 1959;6(1):80-91. https://doi.org/10.1287/mnsc.6.1.80.
[2] Toth P, Vigo D, editors. Vehicle routing: problems, methods, and applications. 2nd ed. Philadelphia: Society for Industrial and Applied Mathematics (SIAM); 2014. https://doi.org/10.1137/1.9781611973594.
[3] Cordeau JF, Laporte G, Potvin JY, Savelsbergh MW. Transportation on demand. In: Barnhart C, Laporte G, editors. Handbooks in operations research and management science: transportation. Vol. 14. Amsterdam: Elsevier; 2007. p. 429-66. https://doi.org/10.1016/S0927-0507(06)14007-4.
[4] Savelsbergh MW, Sol M. The general pickup and delivery problem. Transp Sci. 1995;29(1):17-29. https://doi.org/10.1287/trsc.29.1.17.
[5] Boyacı B, Zografos KG, Geroliminis N. An optimization framework for the development of efficient one-way car-sharing systems. Eur J Oper Res. 2015;240(3):718-33. https://doi.org/10.1016/j.ejor.2014.07.020.
[6] Jorge D, Correia GH, Barnhart C. Comparing optimal relocation operations with simulated relocation policies in one-way carsharing systems. IEEE Trans Intell Transp Syst. 2014;15(4):1667-75. https://doi.org/10.1109/TITS.2014.2304358.
[7] Nair R, Miller-Hooks E. Fleet management for vehicle sharing operations. Transp Sci. 2011;45(4):524-40. https://doi.org/10.1287/trsc.1100.0347.
[8] Kek AG, Cheu RL, Meng Q, Fung CH. A decision support system for vehicle relocation operations in carsharing systems. Transp Res Part E Logist Transp Rev. 2009;45(1):149-58. https://doi.org/10.1016/j.tre.2008.02.008.
[9] Goel A, Vidal T. Hours of service regulations in road freight transport: an optimization-based international assessment. Transp Sci. 2014;48(3):391-412. https://doi.org/10.1287/trsc.2013.0477.
[10] Prescott-Gagnon E, Desaulniers G, Drexl M, Rousseau LM. European driver rules in vehicle routing with time windows. Transp Sci. 2010;44(4):455-73. https://doi.org/10.1287/trsc.1100.0328.
[11] Goel A. Vehicle scheduling and routing with drivers' working hours. Transp Sci. 2009;43(1):17-26. https://doi.org/10.1287/trsc.1070.0226.
[12] Federal Motor Carrier Safety Administration (FMCSA). Hours of service of drivers; final rule (49 CFR Parts 385, 386, 390, and 395). Fed Regist. 2011;76(248):81134-88.
[13] European Parliament and Council of the European Union. Regulation (EC) No 561/2006 on the harmonisation of certain social legislation relating to road transport. Off J Eur Union. 2006;L102:1-14.
[14] Department of Land Transport, Ministry of Transport, Thailand. Land Transport Act B.E. 2522 (1979), Sections 103 and 103/1, and Road Traffic Act B.E. 2522 (1979), Section 43 ter: statutory limits on continuous driving hours and mandatory rest intervals for public and commercial vehicle operators. Bangkok: Royal Thai Government Gazette; 1979.
<span style="color:red">[15] Ministry of Finance, Thailand. Regulation of the Ministry of Finance on the disbursement of overtime pay B.E. 2550 (2007). Bangkok: Royal Thai Government Gazette; 2007.</span>
[16] Park J, Kim BI. The school bus routing problem: a review. Eur J Oper Res. 2010;202(2):311-9. https://doi.org/10.1016/j.ejor.2009.05.017.
[17] Shafahi A, Wang Z, Haghani A. SpeedRoute: fast, efficient solutions for school bus routing problems. Transp Res Part B Methodol. 2018;117:473-93. https://doi.org/10.1016/j.trb.2018.09.004.
[18] Mitchell S, O'Sullivan M, Dunning I. PuLP: a linear programming toolkit for Python. Auckland: Department of Engineering Science, The University of Auckland; 2011.
[19] Alonso-Mora J, Samaranayake S, Wallar A, Frazzoli E, Rus D. On-demand high-capacity ride-sharing via dynamic trip-vehicle assignment. Proc Natl Acad Sci U S A. 2017;114(3):462-7. https://doi.org/10.1073/pnas.1611675114.
[20] Santi P, Resta G, Szell M, Sobolevsky S, Strogatz SH, Ratti C. Quantifying the benefits of vehicle pooling with shareability networks. Proc Natl Acad Sci U S A. 2014;111(37):13290-4. https://doi.org/10.1073/pnas.1403657111.
[21] Agatz N, Erera A, Savelsbergh M, Wang X. Optimization for dynamic ride-sharing: a review. Eur J Oper Res. 2012;223(2):295-303. https://doi.org/10.1016/j.ejor.2012.05.028.
