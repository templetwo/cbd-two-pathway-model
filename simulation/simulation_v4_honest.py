import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(SCRIPT_DIR, '..', 'figures')

# --- PARAMETERS: THE "UNIVERSAL HIT" MODEL (V4.1 HONEST CALIBRATION) ---
# Purpose: Show that BOTH cell types take a hit, but Healthy survives via resilience.
#
# PARAMETER JUSTIFICATION (anchored to IRIS Gate Evo convergence data)
# ====================================================================
#
# Kd_VDAC = 11.0 uM
#   Source: Rimmerman et al. (2013) Cell Death & Disease 4, e949.
#   IRIS validation: Used as prior in all pharmacology runs; 4/5 models
#   confirmed sub-Kd hepatic concentrations at 50mg/day oral dosing.
#
# EC50_TRPV1 = 3.5 uM
#   Source: Bisogno et al. (2001) Br J Pharmacol 134(4), 845-852.
#   CBD binds TRPV1 at lower concentrations than VDAC1, establishing
#   the therapeutic window below the cytotoxic threshold.
#
# scavenging_capacity: Healthy=3.0, Cancer=0.6
#   Basis: GSH synthesis rate ratio. IRIS chronic dosing run
#   (evo_20260213_042930, S3 PASSED, cosine=0.9024) found:
#   - Healthy hepatocyte GSH synthesis: 0.5-2.3 umol/g/hr (TYPE 0, 4/5)
#   - NAFLD/compromised: >2x reduction (TYPE 0, 4/5)
#   - HCC baseline GSH: 2-8 mM vs healthy 5-10 mM (EFSA run TYPE 0)
#   The 5:1 ratio (3.0/0.6) reflects the combined effect of reduced
#   synthesis rate AND depleted baseline reserves in cancer phenotype.
#
# g_max: Healthy=2.5, Cancer=5.0
#   Basis: VDAC1 is overexpressed 2-5x in many cancer types.
#   - Shoshan-Barmatz et al. (2010) Mol Aspects Med 31(3), 227-285.
#   - HCC cells show elevated VDAC1 density on outer mitochondrial membrane.
#   The 2:1 ratio (5.0/2.5) is conservative relative to literature (up to 5x).
#
# respiration_max: Healthy=2.5, Cancer=1.0
#   Basis: Warburg effect. Cancer cells have reduced oxidative phosphorylation
#   capacity and rely on glycolysis, limiting their ability to compensate
#   for VDAC-mediated uncoupling.
#
# resilience: Healthy=1.0, Cancer=0.4
#   Composite parameter capturing metabolic flexibility. Cancer cells have
#   less capacity to reroute metabolism under mitochondrial stress.
#
# IRIS GATE EVO VALIDATION SUMMARY
#   Run 1 (EFSA stress test, evo_20260213_035958): S3 PASSED
#     - 5/5 TYPE 0: CBD does not discriminate VDAC1 vs VDAC2
#     - 4/5 TYPE 0: GSH depletion threshold ~20 uM
#     - Monte Carlo: all 4 hypotheses power=1.0, d=0.73-1.01
#   Run 2 (Chronic dosing, evo_20260213_042930): S3 PASSED (cosine 0.9024)
#     - 4/5 TYPE 0: GSH synthesis drops >2x in NAFLD
#     - 4/5 TYPE 0: CBD-VDAC1 binding reversible, resets overnight
#     - 3/5 TYPE 1: Safety margin 5-10x healthy, 2-3x compromised
#     - First INDEPENDENT REPLICATION: sub-Kd hepatic CBD confirmed
# ====================================================================

Kd_VDAC = 11.0  # uM, Rimmerman et al. 2013
EC50_TRPV1 = 3.5  # uM, Bisogno et al. 2001

def system_dynamics_v4(state, t, cbd_conc, blocker_presence, cell_type):
    """
    state[0] = Mitochondrial Membrane Potential (Psi)
    state[1] = Apoptotic Factors (Cytochrome C)
    state[2] = ROS Levels
    """
    Psi, Apop, ROS = state
    
    # --- DIVERGENT RESILIENCE PARAMETERS ---
    # See PARAMETER JUSTIFICATION block above for sources and IRIS validation.
    if cell_type == "Healthy":
        resilience = 1.0       # Full metabolic flexibility
        scavenging_capacity = 3.0  # GSH 5-10 mM baseline, synthesis 0.5-2.3 umol/g/hr
        g_max = 2.5            # Normal VDAC1 density
        respiration_max = 2.5  # Intact oxidative phosphorylation
    else:
        resilience = 0.4       # Warburg-limited metabolic rerouting
        scavenging_capacity = 0.6  # GSH 2-8 mM, synthesis reduced >2x (IRIS TYPE 0)
        g_max = 5.0            # VDAC1 overexpressed 2-5x (Shoshan-Barmatz 2010)
        respiration_max = 1.0  # Glycolysis-dependent, limited OXPHOS reserve

    # --- 1. THE "HIT": CBD Binds VDAC1/2 ---
    inhibition_factor = 0.1 if blocker_presence else 1.0
    effective_binding = inhibition_factor * (cbd_conc**2 / (Kd_VDAC**2 + cbd_conc**2))
    vdac_leak = g_max * effective_binding

    # --- 2. THE PROTECTIVE SIGNAL (TRPV1) ---
    protection_signal = (cbd_conc / (EC50_TRPV1 + cbd_conc)) * 0.4

    # --- DIFFERENTIAL EQUATIONS ---
    
    # ROS Generation: Proportional to VDAC leak
    ros_generation = 0.1 + (vdac_leak * 0.3) 
    # ROS Scavenging: Boosted by protection signal
    ros_removal = (scavenging_capacity + protection_signal) * ROS
    dROS_dt = ros_generation - ros_removal

    # Potential: Respiration vs Leak vs ROS damage
    ros_damage = 0.4 * ROS
    respiration = respiration_max + (protection_signal * 0.2) - (1.0 - resilience)
    # The potential equation:
    dPsi_dt = respiration - vdac_leak - ros_damage - (0.1 * Psi)
    
    # Apoptosis Trigger
    # Thresholds: Psi < 0.4 or ROS > 2.0
    trigger = 1.0 if (Psi < 0.4 or ROS > 2.0) else 0.0
    dApop_dt = trigger * 0.8 
    
    return [dPsi_dt, dApop_dt, dROS_dt]

def run_simulation(cbd_conc, blocker, cell_type):
    t = np.linspace(0, 50, 400)
    initial_state = [1.0, 0.0, 0.1]
    sol = odeint(system_dynamics_v4, initial_state, t, args=(cbd_conc, blocker, cell_type))
    return t, sol

# --- VISUALIZING THE "RESILIENCE" MODEL ---
cell_types = ['Healthy', 'Cancer (Vulnerable)']
doses = [0, 5, 20, 40] 

fig, axes = plt.subplots(2, 2, figsize=(15, 10), sharex=True)
colors = ['blue', 'green', 'orange', 'red']

for i, cell_type in enumerate(cell_types):
    for dose, color in zip(doses, colors):
        t, sol = run_simulation(dose, False, cell_type)
        
        # Plot Psi
        axes[i, 0].plot(t, sol[:, 0], color=color, label=f'CBD {dose}uM')
        # Plot ROS
        axes[i, 1].plot(t, sol[:, 2], color=color, label=f'CBD {dose}uM')

    # Formatting
    axes[i, 0].set_title(f'{cell_type} - Potential ($\Psi$)')
    axes[i, 0].axhline(0.4, color='k', linestyle='--', alpha=0.5, label='Death Threshold')
    axes[i, 0].set_ylim(-0.5, 3.0)
    axes[i, 0].legend(fontsize='x-small', ncol=2)
    
    axes[i, 1].set_title(f'{cell_type} - ROS')
    axes[i, 1].axhline(2.0, color='r', linestyle='--', alpha=0.5, label='Toxicity Threshold')
    axes[i, 1].set_ylim(0, 3.0)
    axes[i, 1].legend(fontsize='x-small', ncol=2)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'v4_honest_resilience.png'), dpi=150, bbox_inches='tight')

print("\n--- HONEST MODEL RESULTS (40uM CBD) ---")
for cell_type in cell_types:
    _, sol = run_simulation(40, False, cell_type)
    final_psi, final_ros = sol[-1, 0], sol[-1, 2]
    status = "SURVIVED" if (final_psi > 0.4 and final_ros < 2.0) else "COLLAPSED"
    print(f"[{cell_type}]: Potential={final_psi:.2f}, ROS={final_ros:.2f} -> {status}")
