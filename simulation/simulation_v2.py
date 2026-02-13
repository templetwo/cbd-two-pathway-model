import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(SCRIPT_DIR, '..', 'figures')

# --- ENHANCED PARAMETERS (IRIS-Gate-Evo Validated) ---
# Kd_VDAC1: Dissociation constant for CBD-VDAC1 binding (ref: Rimmerman 2013)
Kd_VDAC1 = 11.0 
# EC50_TRPV1: Approximate concentration for protection signal (ref: Bisogno 2001)
EC50_TRPV1 = 3.5
# G_max: Max Ion Leakage from VDAC1
G_max = 5.0

def system_dynamics(state, t, cbd_conc, blocker_presence, cell_resilience):
    """
    state[0] = Mitochondrial Membrane Potential (Psi)
    state[1] = Apoptotic Factors (Cytochrome C release)
    """
    Psi, Apop = state
    
    # --- 1. THERAPEUTIC PATHWAY (TRPV1/Low Dose Protection) ---
    # Simplified protection signal: peaks at low dose, saturates.
    protection_signal = (cbd_conc / (EC50_TRPV1 + cbd_conc)) * 0.4
    
    # --- 2. CYTOTOXIC PATHWAY (VDAC1 Interaction) ---
    # If blocker is present, binding is effectively inhibited.
    # Assume VBIT-4 (blocker) reduces binding efficiency by 95%
    inhibition_factor = 0.05 if blocker_presence else 1.0
    effective_binding = inhibition_factor * (cbd_conc**2 / (Kd_VDAC1**2 + cbd_conc**2))
    
    # VDAC opening causes leak (Conductance)
    leak_current = G_max * effective_binding
    
    # --- DIFFERENTIAL EQUATIONS ---
    # Potential is maintained by respiration, drained by leak and basal decay
    # Respiration boosted by protection_signal, dampened by poor resilience
    respiration_rate = 1.0 + protection_signal - (1.0 - cell_resilience)
    dPsi_dt = respiration_rate - leak_current - (0.1 * Psi)
    
    # dApop/dt: Apoptosis triggers if Potential (Psi) drops below death threshold (0.5)
    trigger = 1.0 if Psi < 0.5 else 0.0
    dApop_dt = trigger * 0.8  # Rate of cytochrome c release
    
    return [dPsi_dt, dApop_dt]

def run_simulation(cbd_conc, blocker, resilience):
    t = np.linspace(0, 50, 200)
    initial_state = [1.0, 0.0] # [Full Potential, No Apoptosis]
    sol = odeint(system_dynamics, initial_state, t, args=(cbd_conc, blocker, resilience))
    return t, sol

# --- EXPERIMENTAL SWEEP ---
resilience_settings = {
    'Healthy': 0.95,
    'Cancer (Vulnerable)': 0.4
}
cbd_doses = [0, 5, 20, 50] # uM

fig, axes = plt.subplots(len(resilience_settings), 1, figsize=(12, 10), sharex=True)
colors = ['blue', 'green', 'orange', 'red']

for i, (label, resilience) in enumerate(resilience_settings.items()):
    ax = axes[i]
    for dose, color in zip(cbd_doses, colors):
        t, sol = run_simulation(dose, False, resilience)
        ax.plot(t, sol[:, 0], color=color, linestyle='-', label=f'CBD {dose}uM')
        
        # Run one with blocker for the high dose
        if dose == 20:
             t, sol_b = run_simulation(dose, True, resilience)
             ax.plot(t, sol_b[:, 0], color=color, linestyle='--', alpha=0.6, label=f'CBD {dose}uM + Blocker')

    ax.axhline(0.5, color='black', linestyle=':', label='Death Threshold')
    ax.set_title(f'Cell Type: {label} (Resilience={resilience})')
    ax.set_ylabel('Mitochondrial Potential ($\Psi$)')
    ax.legend(loc='upper right', fontsize='small', ncol=2)
    ax.grid(True, alpha=0.3)

axes[-1].set_xlabel('Time (Arbitrary Units)')
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'cbd_resilience_sweep.png'), dpi=150, bbox_inches='tight')
print("Simulation complete. Output: figures/cbd_resilience_sweep.png")
