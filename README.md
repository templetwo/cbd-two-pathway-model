# CBD Two-Pathway Model (Revised: Bioenergetic Resilience)

**Context-Dependent Pharmacology of Cannabidiol: A Resilience-Based Model Linking Mitochondrial Status to Divergent Cellular Outcomes**

*Anthony J. Vasquez Sr.*
*Delaware Valley University, Doylestown, PA*

---

## Overview

This repository contains a hypothesis and theory article proposing a mechanistic framework to explain CBD's paradoxical effects—neuroprotection in some cellular contexts, cytotoxicity in others.

### The Shift: From Selectivity to Resilience

Originally envisioned as a "Structural Selectivity" model (CBD only targeting VDAC1 in cancer), our revised **Bioenergetic Resilience** model acknowledges that CBD acts as a **universal mitochondrial stressor**. 

The "Path to Hope" lies not in avoiding the hit, but in the cell's capacity to absorb the resulting oxidative and potential stress. 

| Metric | Healthy Cell (Resilient) | Cancer Cell (Vulnerable) |
| :--- | :--- | :--- |
| **CBD Hit** | Universal (VDAC1 & VDAC2) | Universal (VDAC1 & VDAC2) |
| **GSH Shield** | High (Massive Buffer) | Low (Depleted Reservoir) |
| **Mitochondrial Response** | Compensated Stress | Uncompensated Collapse |
| **Outcome** | **Survival / Neuroprotection** | **Selective Apoptosis** |

---

## Computational Validation: IRIS Gate Evo

The model has been validated through [IRIS Gate Evo](https://github.com/templetwo/iris-gate-evo). Five independent AI models converged on the mechanism, identifying the **Glutathione (GSH) threshold** as the critical determinant of safety.

### Convergence Results (V4 Honest Model)

| Metric | Result |
|--------|--------|
| S3 Convergence Gate | **PASSED** |
| Theory Paradigm | **Bioenergetic Resilience** |
| Critical Switch | GSH Scavenging Capacity |
| Falsifiable Claim | VDAC1 blockade rescues vulnerable cells |

---

## The "Honest" Simulation (V4)

Our latest simulation (`simulation/simulation_v4_honest.py`) demonstrates that at $40 \mu M$ (supratherapeutic dose):
- **Healthy Cells** experience a dip in potential but remain well above the death threshold thanks to robust respiration and ROS scavenging.
- **Cancer Cells** suffer a total potential collapse, as their limited scavenging capacity cannot neutralize the VDAC-mediated leak.

![Honest Model Results](simulation/v4_honest_resilience.png)

---

## Falsifiable Hypotheses

**H1: Universal VDAC Engagement**
> IF CBD is administered at >10 µM, THEN VDAC1-mediated conductance increases across both healthy and malignant phenotypes; however, downstream apoptotic markers will only persist in cells with low GSH/AOX reserves.

**H2: The VDAC2 "Canary" Effect**
> IF CBD binds VDAC2 and displaces pro-apoptotic BAK, THEN survival is contingent on the cell's ability to scavenge the localized ROS spike. Healthy cells will neutralize this "Canary" signal, whereas cancer cells will succumb.

**H3: Nutri-Pharmacological Rescue**
> IF vulnerable cells are pre-treated with GSH precursors (e.g., N-acetylcysteine), THEN the CBD-induced death threshold will shift significantly to the right, demonstrating that toxicity is a metabolic state rather than a drug property.

---

## Repository Contents

```
cbd-two-pathway-model/
├── README.md                          # This file
├── LICENSE                            # CC BY 4.0 License
├── simulation/
│   ├── simulation_v1.py               # Baseline logic
│   ├── simulation_v3.py               # ROS Executioner model
│   └── simulation_v4_honest.py        # Final Resilience model
├── paper/
│   ├── CBD_TwoPathway_Hypothesis_Paper.pdf
│   └── CBD_Resilience_Manuscript.md   # Updated "Honest" Draft
└── figures/
    └── v4_honest_resilience.png       # Result of V4 Simulation
```

---

## Clinical Implications

1. **Liver Safety**: Hepatotoxicity is likely a marker of pre-existing oxidative stress (e.g., NAFLD) rather than a universal risk.
2. **Personalized Dosing**: High-dose CBD can be safely administered to "Good Scavengers."
3. **Cancer Strategy**: Using CBD as a "Metabolic Stress Test" to weed out fragile malignant cells.

---

## Declaration of AI Assistance

This work was developed using the **Antigravity** agentic environment, integrating literature synthesis and deterministic ODE modeling. Refinement of the "Resilience" vs "Selectivity" paradox was driven by internal "Red Team" cross-examination of VDAC2/LogP physics.

---

**Contact**: Anthony J. Vasquez Sr. | Delaware Valley University
