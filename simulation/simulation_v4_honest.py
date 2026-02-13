import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import os

# --- PARAMETERS: THE "UNIVERSAL HIT" MODEL (V4.1 HONEST CALIBRATION) ---
# Purpose: Show that BOTH cell types take a hit, but Healthy survives via resilience.
Kd_VDAC = 11.0 
EC50_TRPV1 = 3.5

def system_dynamics_v4(state, t, cbd_conc, blocker_presence, cell_type):
    """
    state[0] = Mitochondrial Membrane Potential (Psi)
    state[1] = Apoptotic Factors (Cytochrome C)
    state[2] = ROS Levels
    """
    Psi, Apop, ROS = state
    
    # --- DIVERGENT RESILIENCE PARAMETERS ---
    if cell_type == "Healthy":
        # Healthy: High metabolic reserve, High scavenging
        resilience = 1.0 
        scavenging_capacity = 3.0 # Strong buffer
        g_max = 2.5 # Significant hit (Universal Stress)
        respiration_max = 2.5 # High metabolic flexibility
    else:
        # Cancer: Brittle metabolism, depleted scavenging
        resilience = 0.4 
        scavenging_capacity = 0.6 # Minimal buffer
        g_max = 5.0 # Higher VDAC density
        respiration_max = 1.0 # Limited flexibility

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
plt.savefig('v4_honest_resilience.png')

print("\n--- HONEST MODEL RESULTS (40uM CBD) ---")
for cell_type in cell_types:
    _, sol = run_simulation(40, False, cell_type)
    final_psi, final_ros = sol[-1, 0], sol[-1, 2]
    status = "SURVIVED" if (final_psi > 0.4 and final_ros < 2.0) else "COLLAPSED"
    print(f"[{cell_type}]: Potential={final_psi:.2f}, ROS={final_ros:.2f} -> {status}")
