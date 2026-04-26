# Replication Materials: "The New Colonialism: American Silicon, British Bills"

**A Two-Country Extension of the AI Layoff Trap**

Author: Ishan Kalra
Working paper, April 2026
Model version: 2.0 (institutional-grade rebuild)

---

## Contents

| File | Description |
|------|---|
| `paper.pdf` | Full working paper, 57 pages |
| `paper.tex` | LaTeX source |
| `references.bib` | 64-entry bibliography |
| `uk_ai_externality_model.xlsx` | Production-grade calibration model — 17 sheets, 327 formulas, 29 named ranges, 3 embedded charts, scenario engine, two-way sensitivity, Monte Carlo, λ decomposition, Stargate counterfactual |
| `build_xlsx.py` | Original v1 build script (kept for reference) |
| `build_xlsx_v2*.py` | v2 phased build scripts (1 → 5c) |
| `run_monte_carlo.py` | Standalone Monte Carlo simulator (10,000 trials) |
| `mc_results.json` | Pre-computed MC percentile output |
| `recalc_force.sh` | Helper script to force LibreOffice recalc on headless |
| `simulation_scripts/` | Python scripts replicating the four propositions |
| `chart_scripts/` | Standalone chart generators (matplotlib) |
| `figures/` | PDF figures used in the paper |

---

## Quick start

1. **Open `uk_ai_externality_model.xlsx`** in Excel or LibreOffice.
2. **Start at the `Dashboard` sheet** — live executive summary with embedded waterfall chart (right side, columns J–T), scenario selector at C7, three-pillar policy toggle at C10.
3. **Modify any blue input cell** in `Assumptions` — model recomputes throughout via 29 named ranges (`lambda_central`, `eta_reempl`, `tau_d_star`, etc.).
4. **Drill into components** via `C1_Subscription_Flow` through `C6_Forgone_Frontier`.
5. **Run sensitivity** on `Sensitivity_2way` (live two-way table with heat map), `Tornado` (parameter ranking with embedded bar chart), or `Monte_Carlo` (live single-draw engine + precomputed 10k percentiles).
6. **Read documentation** on `Methodology` (section-by-section walkthrough) and `Sources` (20+ data anchors with citations).

After modifying any input, recalculate via Cmd+= (Mac) / F9 (Windows) / Ctrl+Shift+F9 (full).

---

## Spreadsheet architecture (v2.0)

**Seventeen sheets organised in four layers:**

### Layer 1 — Control & integrity (4 sheets)
- **`Dashboard`** — Live executive summary. Scenario selector dropdown at C7. Policy toggle at C10. Headline waterfall, traffic-light reconciliation status, embedded BarChart of the 6 components.
- **`Assumptions`** — All hardcoded inputs in colour-coded cells (blue inputs, yellow key assumptions). Each row has a source citation. 29 named ranges defined here drive the entire model.
- **`Scenario_Engine`** — Four scenarios (Pessimistic/Central/Optimistic/BoE) as columns. CHOOSE-based routing pulls active scenario into the model based on Dashboard!C7.
- **`Audit_Trail`** — Live reconciliation against paper claims for headline aggregate, every component, λ decomposition, and DST optima. Status flags (OK/CHECK) trip at 5% tolerance.

### Layer 2 — Component sheets (6 sheets)
- **`C1_Subscription_Flow`** — Bottom-up build by provider 2023-2030. Cumulative £137.3bn (paper £139bn).
- **`C2_Cloud`** — UK total cloud spend × AI-attributable share, 2023-2030. £94.6bn cumulative (paper £95bn).
- **`C3_Productivity_Rent`** — UK gross AI productivity gain × capture rate θ rising 5%→32%. £104.7bn (paper £105bn).
- **`C4_Displaced_Wage`** — Stock × net wage loss × Keynesian multiplier. £44.4bn (paper £45bn). Uses named ranges `avg_wage`, `eta_reempl`, `keyn_mult`, `comp_factor`.
- **`C5_HMRC`** — Three-component tax loss (labour+NI, transfer-priced CT, lost VAT). £17.4bn (paper £18bn).
- **`C6_Forgone_Frontier`** — Five-industry build (robotics, autonomous, biotech-AI, materials AI, fintech-AI). £59bn (paper £59bn).

### Layer 3 — Analytical sheets (5 sheets)
- **`Lambda_Decomp`** — Five-channel computation of UK domestic capture (US AI firms' UK staff wages, integration partner margins, transfer-priced UK CT, university research partnerships, UK shareholder returns + CGT). Computes implied λ = 1 - capture/gross. Reconciles to paper's 0.76/0.83/0.87 across 2024/2025/2026 within 1.1%.
- **`Stargate_Counterfactual`** — Paper §6.2 case study. Six concession line items totalling £39.25bn central; project value £4.75bn central; welfare margin £34.5bn — pause beats revival.
- **`Sensitivity_2way`** — Live engine cell + two-way data table on (λ × η) with conditional-formatting heat map. Range £380–533bn across (λ ∈ [0.78, 0.90], η ∈ [0.20, 0.60]).
- **`Tornado`** — Nine inputs varied ±20% from central, ranked by absolute headline impact. Embedded horizontal bar chart. λ dominates (£133bn range), η second (£42bn).
- **`Monte_Carlo`** — Live single-draw NORMINV engine + precomputed N=10,000 percentiles. P5–P95 = £410–509bn (uncorrelated draws; tighter than paper §5.4 scenario range £283–658bn as expected). Embedded percentile bar chart.

### Layer 4 — Documentation (2 sheets)
- **`Methodology`** — Section-by-section walkthrough: paper overview, model architecture, component sheet descriptions, scenario engine mechanics, limitations, user guide.
- **`Sources`** — Twenty primary data anchors with source organisation, citation/URL, and access date.

---

## Key features

- **29 named ranges** drive the entire model. Edit Name Manager (Formulas → Name Manager) to inspect.
- **3 embedded native Excel charts** (Dashboard waterfall, Tornado bar, MC percentile distribution) — they update live when inputs change.
- **Live conditional formatting**: heat-map on Sensitivity_2way, traffic-light on Audit_Trail, range-bar on Tornado.
- **Zero formula errors** across all 327 formulas — verified post-recalc.
- **All status flags green** in Audit_Trail at central scenario (13 reconciliation checks pass).
- **Reconciliation tolerance**: headline £457.4bn vs paper £461bn (0.78%), all 6 components within 1.3%.

---

## Named ranges (29 defined)

Defined on the `Assumptions` sheet:
```
lambda_central, lambda_low, lambda_high
rho_mpc, eta_reempl, eta_prod
delta_0, beta_elast
tau_d_star, delta_at_optimum, dst_capture_rate
avg_wage, provider_wage, ct_rate, it_ni_rate
disc_rate, keyn_mult, comp_factor
gdp_2030, employment_total
p1_capture, p2_capture, p3_capture, pillar_total
nvda_cap, big6_cap, hyper_capex
uk_elec, us_elec, no_elec
```

Formulas referencing named ranges are coloured purple (7030A0) in the model.

---

## Scenario engine

Set `Dashboard!C7` to switch scenarios. Net welfare results without three-pillar policy:

| Scenario | Productivity uplift | Cumulative gain | Net welfare |
|----------|--------------------:|----------------:|------------:|
| Pessimistic | 0.1 ppts | £82bn | -£375bn |
| **Central** | **0.3 ppts** | **£239bn** | **-£218bn** |
| Optimistic | 0.6 ppts | £490bn | +£33bn |
| BoE upper-end | 0.8 ppts | £712bn | +£255bn |

With three-pillar policy enabled (Dashboard!C10): all rows improve by £40bn. Even pessimistic still negative; central improves to -£178bn; optimistic to +£73bn.

---

## How to verify

1. **Run a recalc** to populate cached values (Excel does this automatically; LibreOffice may need force-recalc):
   ```bash
   ./recalc_force.sh uk_ai_externality_model.xlsx
   ```

2. **Check `Audit_Trail`** — every status flag (column F) should read **OK** (green). Thirteen flags total: headline + 6 components + 3 λ trajectory points + 3 DST optima.

3. **Check `Dashboard`** — total at C21 should be **£457.4bn**, tolerance at C26 should be **0.78%**.

4. **Inspect named ranges** via Excel Name Manager (Formulas → Name Manager).

5. **Test the scenario engine** — change Dashboard!C7 to Pessimistic, observe headline drop and reconciliation flags refresh.

6. **Stress test** — visit Sensitivity_2way, change λ in B9 from 0.85 to 0.78, watch B11 engine output drop.

7. **Live MC draw** — open Monte_Carlo, press F9. Row 19 (drawn parameters) and row 22 (drawn components+total) refresh with a new random sample.

---

## Replication of paper propositions

Beyond the calibration spreadsheet, the four propositions in the paper (which are derivations, not numerical claims) can be verified via Python scripts in `simulation_scripts/`:

- `prop1_simulation.py` — Two-country welfare proposition
- `prop2_simulation.py` — Productivity inefficiency under leakage
- `prop3_simulation.py` — Demand multiplier with cross-border MPC
- `prop4_simulation.py` — DST optimal rate with avoidance

All four propositions verified within 1.5% numerical tolerance.

---

## Build scripts

The v2.0 institutional-grade model is built in five phases. To rebuild from scratch:

```bash
python3 build_xlsx_v2.py                  # Phase 1: foundations (Dashboard, Assumptions, Scenario_Engine, Audit_Trail)
python3 build_xlsx_v2_phase2.py           # Phase 2: 6 component sheets (C1-C6)
python3 build_xlsx_v2_phase3.py           # Phase 3: Lambda_Decomp + Stargate_Counterfactual
python3 build_xlsx_v2_phase4.py           # Phase 4: Sensitivity_2way + Tornado
python3 build_xlsx_v2_phase5a_mc.py       # Phase 5a: Monte_Carlo
python3 run_monte_carlo.py                # (re-run if you want to update MC percentiles)
python3 build_xlsx_v2_phase5b_charts.py   # Phase 5b: embedded native Excel charts
python3 build_xlsx_v2_phase5c.py          # Phase 5c: Methodology + Sources
./recalc_force.sh uk_ai_externality_model.xlsx     # Force recalc via LibreOffice
```

---

## Citation

If using this model or replication materials, please cite the working paper:

> Kalra, I. (2026). "The New Colonialism: American Silicon, British Bills: A Two-Country Extension of the AI Layoff Trap." Working paper. Available at: [SSRN URL forthcoming].

For questions about the model: ishanworkmail01@gmail.com

---

*Model architecture inspired by financial-model conventions used in PE / hedge fund / institutional research. Built to reviewer-ready standards: every input cited, every formula auditable, every reconciliation traceable, sensitivity bounded, uncertainty quantified.*
