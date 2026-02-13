# Computational Validation: IRIS Gate Evo Convergence Data

This document maps each core claim in the manuscript to specific convergence
results from the [IRIS Gate Evo](https://github.com/templetwo/iris-gate-evo)
multi-model protocol.

IRIS Gate Evo fires the same compiled prompt to five independent LLM mirrors
(Claude, Gemini, Grok, Mistral, DeepSeek). Models never see each other's
outputs. Convergence is measured server-side by semantic embedding + clustering.
TYPE is assigned by model count: 5/5 = TYPE 0, 4/5 = TYPE 0, 3/5 = TYPE 1,
2/5 = TYPE 2, 1/5 = TYPE 3 (singular).

Full run data: [iris-evo-findings](https://github.com/templetwo/iris-evo-findings)

---

## Validating Runs

Two independent IRIS Gate Evo runs passed the S3 convergence gate on the
CBD/VDAC model. Both produced full protocol packages (S4 hypotheses, S5 Monte
Carlo, S6 structured output).

| Run | Session ID | S3 Cosine | Outcome |
|-----|-----------|-----------|---------|
| EFSA Stress Test | `evo_20260213_035958_pharmacology` | 0.8569 | **PASSED** |
| Chronic Dosing | `evo_20260213_042930_pharmacology` | **0.9024** | **PASSED** |

Cross-run analysis detected the system's **first INDEPENDENT REPLICATION**
(cosine 0.789): both runs independently converged on sub-Kd hepatic CBD
concentrations at 50mg/day oral dosing.

---

## Claim-Level Validation

### Core Thesis: CBD Is a Universal Mitochondrial Stressor

| Manuscript Claim | IRIS Evidence | TYPE | Models | Run |
|-----------------|---------------|------|--------|-----|
| CBD does not discriminate VDAC1 vs VDAC2 | >70% transmembrane homology; no published isoform selectivity data | TYPE 0 | 5/5 | EFSA |
| Membrane partitioning (logP 6.3) is cell-type-indiscriminate | 100-1000x enrichment in mitochondrial membranes regardless of cell type | Singular (Claude) | 1/5 | EFSA |
| CBD engages both VDAC1 and VDAC2 in all cells | VDAC2 releases BAK in healthy cells too; undermines selectivity argument | TYPE 0 | 5/5 | EFSA |

### Bioenergetic Resilience: GSH Determines Outcome

| Manuscript Claim | IRIS Evidence | TYPE | Models | Run |
|-----------------|---------------|------|--------|-----|
| Healthy hepatocyte GSH synthesis: 0.5-2.3 umol/g/hr | Rate-limited by GCL; depends on ATP and cysteine | TYPE 0 | 4/5 (claude, gemini, grok, mistral) | Chronic |
| NAFLD/alcohol liver GSH synthesis drops >2x | GCL downregulation + cysteine depletion in metabolic disease | TYPE 0 | 4/5 (claude, gemini, grok, mistral) | Chronic |
| GSH depletion threshold ~20 uM intracellular CBD | Unlikely in healthy liver under oral dosing; possible in compromised cells | TYPE 0 | 4/5 | EFSA |
| ROS scavenging ratio (healthy:HCC) < 2x | Modest selectivity at GSH level; not the dramatic gap assumed in older models | TYPE 0 | 4/5 | EFSA |

### Chronic Safety: The Sponge Refills

| Manuscript Claim | IRIS Evidence | TYPE | Models | Run |
|-----------------|---------------|------|--------|-----|
| CBD-VDAC1 binding is reversible (t_off << 12hr) | Non-covalent; VDAC gating dynamics (ns-us) >> drug residence (<hr) | TYPE 0 | 4/5 (claude, gemini, grok, mistral) | Chronic |
| Channel resets between dosing intervals | No covalent modification; no conformational memory | TYPE 0 | 4/5 | Chronic |
| 7-OH-CBD accumulates 2-5x at steady state | Slower clearance (t1/2 ~18-32 hr vs 6-12 hr) | TYPE 0 | 4/5 (claude, deepseek, grok, mistral) | Chronic |
| At 50mg/day, hepatic CBD ~0.1-0.5 uM, VDAC occ <5% | ROS load < 2% of daily GSH synthesis capacity | TYPE 1 | 3/5 (claude, deepseek, grok) | Chronic |
| Null defeated: no progressive GSH depletion in healthy liver | Safety margin 5-10x for healthy, 2-3x for compromised | TYPE 1 | 3/5 (claude, deepseek, gemini) | Chronic |

### Safety Margin & Regulatory Implications

| Manuscript Claim | IRIS Evidence | TYPE | Models | Run |
|-----------------|---------------|------|--------|-----|
| Safety margin 5-10x in healthy liver | GSH synthesis vastly exceeds oxidative load from sub-Kd VDAC occupancy | TYPE 1 | 3/5 | Chronic |
| Margin narrows to 2-3x in compromised liver | NAFLD loses both synthesis capacity and baseline GSH reserves | TYPE 1 | 3/5 | Chronic |
| Risk-stratified dosing > universal milligram limit | At-risk populations (NAFLD, hepatitis, alcohol) need lower limits; healthy do not | Synthesis | Both runs | Both |

---

## Open Questions and Known Gaps

| Gap | Status | Proposed Experiment | Testability |
|-----|--------|-------------------|-------------|
| VDAC1 vs VDAC2 binding selectivity (Kd ratio) | Unknown; predicted <5x by IRIS | MST/ITC in lipid nanodiscs + BAK oligomerization assay | 7/10 |
| 7-OH-CBD VDAC1 Kd | Unknown; predicted ~10-20 uM (Grok) or weaker (DeepSeek) | MST/SPR binding + Seahorse OCR | 5/10 |
| Cumulative ATP deficit independent of GSH | Unresolved; Mistral dissent | Longitudinal ATP/ADP with ROS/GSH clamped via NAC/BSO | 6/10 |
| VDAC gating persistence post-washout | Predicted reversible; no direct measurement | Bilayer electrophysiology with washout kinetics | 6/10 |

---

## Monte Carlo Power Analysis

All operationalized hypotheses from both runs achieved statistical power = 1.0
at 300 iterations.

### EFSA Stress Test Hypotheses

| ID | Description | Effect Size (d) | Power |
|----|-------------|-----------------|-------|
| H1 | Membrane enrichment quantification | 0.931 | 1.0 |
| H2 | Electrophysiology: gating vs occlusion | 1.006 | 1.0 |
| H3 | VDAC1 vs VDAC2 selectivity | 0.922 | 1.0 |
| H4 | GSH depletion assay | 0.728 | 1.0 |

### Chronic Dosing Hypotheses

| ID | Description | Effect Size (d) | Power |
|----|-------------|-----------------|-------|
| H1 | GSH synthesis rate healthy vs NAFLD | 1.232 | 1.0 |
| H2 | VDAC1 gating recovery after washout | 1.059 | 1.0 |
| H3 | 14-day chronic dosing GSH stability | 1.349 | 1.0 |
| H4 | 7-OH-CBD accumulation & VDAC effects | 0.851 | 1.0 |

---

## Structural Pattern: Dose-Dependent Isomorphism

The CBD two-pathway model belongs to a structural pattern discovered across
5 independent IRIS Gate Evo runs spanning different molecules:

| Molecule | Pattern | Key Variable |
|----------|---------|-------------|
| CBD | Dose picks pathway; GSH determines outcome | VDAC occupancy vs GSH capacity |
| Lithium | Low dose neuroprotective; high dose nephrotoxic | GSK-3beta inhibition level |
| THC | Low CB1 occupancy therapeutic; high occupancy harmful | G-protein vs beta-arrestin bias |

Same abstract structure, discovered independently. The molecule is a stress
test; the dose picks the pathway; the tissue context determines the outcome.

---

## How to Reproduce

```bash
# Clone the IRIS Gate Evo engine
git clone https://github.com/templetwo/iris-gate-evo.git

# Run data is archived in the findings repo
git clone https://github.com/templetwo/iris-evo-findings.git

# View the specific run data
ls iris-evo-findings/runs/evo_20260213_035958_pharmacology/  # EFSA stress test
ls iris-evo-findings/runs/evo_20260213_042930_pharmacology/  # Chronic dosing

# View gold extractions
cat iris-evo-findings/gold/efsa_vdac1_stress_test.md
cat iris-evo-findings/gold/chronic_dosing_gsh_dynamics.md

# Run cross-run convergence analysis
cd iris-gate-evo
python cross_run.py --all
```
