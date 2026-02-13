import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import os

# --- PARAMETERS (To be validated by IRIS-Gate-Evo) ---
# Kd_VDAC1: Dissociation constant for CBD-VDAC1 binding (approx 11 uM)
Kd_VDAC1 = 11.0 
# VDAC_conductance_max: Max rate of ion leakage when VDAC is fully open
G_max = 5.0
# Bioenergetic_Capacity: Healthy cells have high capacity (1.0), Cancer cells low (0.4)
# This represents the "Context-Dependent" variable
Cell_Resilience = 0.4 

def system_dynamics(state, t, cbd_conc, blocker_presence):
    """
    state[0] = Mitochondrial Membrane Potential (Psi)
    state[1] = Apoptotic Factors (Cytochrome C release)
    """
    Psi, Apop = state
    
    # --- 1. THERAPEUTIC PATHWAY (Low Dose Protection) ---
    # Effect peaks at low dose (2-5uM) and saturates
    protection_signal = (cbd_conc / (2.0 + cbd_conc)) * 0.5
    
    # --- 2. CYTOTOXIC PATHWAY (VDAC1 Interaction) ---
    # Hill equation for binding occupancy
    # If blocker is present (1.0), binding is effectively 0
    effective_binding = 0 if blocker_presence else (cbd_conc**2 / (Kd_VDAC1**2 + cbd_conc**2))
    
    # VDAC opening causes leak (Conductance)
    leak_current = G_max * effective_binding
    
    # --- DIFFERENTIAL EQUATIONS ---
    
    # dPsi/dt: Potential is maintained by respiration, drained by leak
    # Respiration is boosted by protection_signal, hurt by low Cell_Resilience
    respiration_rate = 1.0 + protection_signal - (1.0 - Cell_Resilience)
    dPsi_dt = respiration_rate - leak_current - (0.1 * Psi)
    
    # dApop/dt: Apoptosis triggers if Potential (Psi) drops below threshold (e.g., 0.5)
    trigger = 1.0 if Psi < 0.5 else 0.0
    dApop_dt = trigger * 0.8  # Rate of cytochrome c release
    
    return [dPsi_dt, dApop_dt]

# --- RUN EXPERIMENT ---
t = np.linspace(0, 50, 100)
initial_state = [1.0, 0.0] # [Full Potential, No Apoptosis]

# Scenario A: High Dose CBD (20uM) - No Blocker
sol_A = odeint(system_dynamics, initial_state, t, args=(20.0, False))

# Scenario B: High Dose CBD (20uM) + VDAC1 BLOCKER
sol_B = odeint(system_dynamics, initial_state, t, args=(20.0, True))

# --- PLOTTING ---
plt.figure(figsize=(10, 6))
plt.plot(t, sol_A[:, 0], 'r--', label='High Dose CBD (Unblocked)')
plt.plot(t, sol_B[:, 0], 'g-', label='High Dose CBD + VDAC1 Blocker')
plt.axhline(0.5, color='k', linestyle=':', label='Death Threshold')
plt.title(f'In Silico Test: VDAC1 Blockade in Vulnerable Cells (Resilience={Cell_Resilience})')
plt.xlabel('Time (Arbitrary Units)')
plt.ylabel('Mitochondrial Potential')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('vdac1_blockade_simulation.png')
print("Simulation complete. Check vdac1_blockade_simulation.png")
