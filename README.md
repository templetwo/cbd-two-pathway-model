# CBD Two-Pathway Model

**Context-Dependent Pharmacology of Cannabidiol: A Two-Pathway Model Linking Mitochondrial Status to Divergent Cellular Outcomes**

*Anthony J. Vasquez Sr.*
*Delaware Valley University, Doylestown, PA*

---

## Overview

This repository contains a hypothesis and theory article proposing a mechanistic framework to explain CBD's paradoxical effects—neuroprotection in some cellular contexts, cytotoxicity in others.

### The Central Question

> *How does the same molecule protect neurons while killing cancer cells?*

### The Answer: A Two-Pathway Model

CBD's effects are determined by **dose-dependent target engagement** and **pre-existing mitochondrial status**:

| Pathway | Concentration | Targets | Outcome |
|---------|---------------|---------|---------|
| **Therapeutic** | 1-5 uM | TRPV1, 5-HT1A, PPARy, GPR55 | Neuroprotection |
| **Cytotoxic** | >10 uM | VDAC1 -> Mitochondrial disruption | Apoptosis |

CBD functions as a **mitochondrial stress test**—amplifying the pre-existing state of cellular bioenergetics rather than selectively targeting pathology.

---

## Computational Validation: IRIS Gate Evo

The two-pathway model has been independently validated through [IRIS Gate Evo](https://github.com/templetwo/iris-gate-evo), a multi-LLM convergence protocol for scientific discovery. Five independent AI models (Claude, Mistral, Grok, Gemini, DeepSeek) were given the CBD/VDAC1 research question without seeing each other's outputs. The system then measured convergence through semantic claim embedding and complete-linkage clustering.

### Convergence Results (2026-02-10)

| Metric | Result |
|--------|--------|
| S3 Convergence Gate | **PASSED** (cycle 2) |
| Cosine Similarity | 0.941 (threshold: 0.85) |
| TYPE 0/1 Ratio | 80% (threshold: 65%) |
| Lab Gate | **10/21 claims passed** (falsifiable + feasible + novel) |
| Total LLM calls | 17 |

### Machine-Generated Hypotheses

The converged claims were operationalized into falsifiable hypotheses with Monte Carlo parameter maps:

**H1: VDAC1-Mediated Selective Depolarization** (Testability: 9.0/10)
> IF cancer cells (MDA-MB-231) are treated with 11 uM CBD, THEN membrane potential will depolarize by >=20 mV (from ~-120 mV to ~-95 mV), triggering apoptosis in >60% of cells by 24h; VDAC1-knockout isogenic lines will show <20% apoptosis and <10 mV depolarization under identical conditions.

- Parameters: CBD_concentration (5-20 uM), membrane_shift (15-35 mV), apoptosis_rate_cancer (40-85%), apoptosis_rate_VDAC1KO (0-30%)
- Cohen's d: **0.93** | Power: **1.0**

**H2: Two-Stage Mechanism (TRPV1/2 Priming + VDAC1 Engagement)** (Testability: 8.0/10)
> IF CBD cytotoxicity operates through a two-stage mechanism (TRPV1/2 Ca2+ priming at 2-4 uM, then VDAC1 engagement at ~11 uM), THEN the dose-response curve in cancer cells will be biphasic; TRPV1/2 double-antagonism will right-shift IC50 by >=2-fold.

- Parameters: TRPV_Kd (1.5-4.0 uM), VDAC1_Kd (8.0-15.0 uM), IC50_WT (6-14 uM), IC50_shift (1.5-4.0 fold), MCU_rescue (20-50%)
- Cohen's d: **0.95** | Power: **1.0**

**H3: Selectivity as Threshold Phenomenon** (Testability: 8.0/10)
> IF selectivity is a threshold phenomenon dependent on baseline membrane potential, THEN pre-treating healthy cells (MCF-10A) with low-dose FCCP to clamp potential at ~-120 mV will sensitize them to 11 uM CBD, increasing apoptosis from <15% to >50%.

- Parameters: healthy_psi (-190 to -170 mV), cancer_psi (-130 to -110 mV), FCCP_target (-130 to -110 mV), apoptosis_FCCP (35-70%), apoptosis_oligo (5-25%), CBD_dose (8-15 uM)
- Cohen's d: **0.81** | Power: **1.0**

### What This Means

Five independent AI models, without coordination, converged on the same two-pathway mechanism proposed in the paper. The convergence is not circular — the models were given the research question, not the paper. They independently identified VDAC1 binding (Kd ~11 uM) as the selectivity switch, the 60 mV membrane potential difference as the vulnerability window, and TRPV1/2 as a synergistic upstream pathway.

The Monte Carlo simulations predict large effect sizes (Cohen's d 0.81-0.95) with full statistical power, suggesting these are experimentally tractable hypotheses with clear expected outcomes.

---

## Repository Contents

```
cbd-two-pathway-model/
├── README.md                          # This file
├── LICENSE                            # CC BY 4.0 License
├── CITATION.cff                       # Citation metadata
├── paper/
│   └── CBD_TwoPathway_Hypothesis_Paper.pdf   # Full manuscript (9 pages)
└── figures/
    ├── diagram1_dual_pathway.png      # Two-pathway mechanism schematic
    ├── diagram2_stress_test.png       # Stress test model visualization
    ├── diagram3_dose_affinity.png     # Target engagement by concentration
    └── diagram4_proposed_experiment.png # VDAC1 neuroprotection test design
```

---

## Key Findings

### Literature Validation
- **90% concordance** (18/20 predictions confirmed) with published literature
- Analysis of **70+ papers** on CBD cellular mechanisms

### Computational Validation
- **5/5 independent AI models** converged on the two-pathway mechanism
- **3 falsifiable hypotheses** generated with Monte Carlo parameter ranges
- **Large effect sizes** predicted (Cohen's d 0.81-0.95)
- Full protocol packages with cell lines, reagents, readouts, and controls

### Four Validated Predictions

1. **Temporal primacy**: Mitochondrial effects occur within minutes, preceding receptor signaling
2. **Pre-stress sensitization**: Metabolically compromised cells show 3-5x greater CBD sensitivity
3. **VDAC1 dependence**: VDAC1 inhibitors attenuate CBD-induced cytotoxicity
4. **Measurable changes**: Consistent alterations in membrane potential, ROS, Ca2+ flux across studies

### Identified Experimental Gap

No published study tests whether **VDAC1 blockade eliminates CBD's neuroprotective effects**. This represents a critical experiment that could validate or refute the two-pathway model.

---

## Figures

### Figure 1: CBD Dual-Pathway Mechanism
![Dual Pathway](figures/diagram1_dual_pathway.png)

### Figure 2: CBD as Mitochondrial Stress Test
![Stress Test](figures/diagram2_stress_test.png)

### Figure 3: Target Engagement by Concentration
![Dose Affinity](figures/diagram3_dose_affinity.png)

### Figure 4: Proposed Experiment Design
![Proposed Experiment](figures/diagram4_proposed_experiment.png)

---

## Clinical Implications

If validated, this model suggests:

1. **Therapeutic selectivity** can exploit metabolic vulnerability rather than molecular uniqueness
2. **Biomarker-guided dosing** using mtDNA status, CYP450 variants, tumor metabolic phenotype
3. **Combination therapy rationale** for metabolic sensitization strategies

---

## Declaration of AI Assistance

Claude (Anthropic) was used as a research and writing assistant for literature synthesis, hypothesis refinement, and figure generation. The [IRIS Gate Evo](https://github.com/templetwo/iris-gate-evo) protocol was used for multi-model convergence validation — five independent AI models confirmed the two-pathway framework without coordination.

The author maintains full responsibility for scientific content and accuracy.

---

## Citation

```bibtex
@article{vasquez2026cbd,
  title={Context-Dependent Pharmacology of Cannabidiol: A Two-Pathway Model
         Linking Mitochondrial Status to Divergent Cellular Outcomes},
  author={Vasquez, Anthony J., Sr.},
  journal={Hypothesis and Theory Article},
  year={2026},
  institution={Delaware Valley University},
  note={Preprint — computationally validated via IRIS Gate Evo multi-model convergence protocol}
}
```

---

## Related Work

- [IRIS Gate Evo](https://github.com/templetwo/iris-gate-evo) — Multi-LLM convergence protocol for scientific discovery (v0.3, 17 calls per run)
- [IRIS Gate](https://github.com/templetwo/iris-gate) — Original cross-architecture phenomenological convergence research framework (v0.2, legacy)

---

## License

This work is licensed under [CC BY 4.0](LICENSE) - you are free to share and adapt with attribution.

---

## Disclaimer

*This paper presents a mechanistic synthesis and hypothesis, not clinical recommendations. CBD-related cancer treatment decisions belong within oncology trials and clinical teams.*

---

**Contact**: Anthony J. Vasquez Sr. | Delaware Valley University
