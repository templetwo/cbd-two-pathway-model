import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import os

# --- ENHANCED PARAMETERS (V3: Executioner ROS - Final Calibration) ---
Kd_VDAC1 = 11.0 
EC50_TRPV1 = 3.5

def system_dynamics_v3(state, t, cbd_conc, blocker_presence, cell_type):
    """
    state[0] = Mitochondrial Membrane Potential (Psi)
    state[1] = Apoptotic Factors (Cytochrome C)
    state[2] = ROS Levels
    """
    Psi, Apop, ROS = state
    
    # --- CONTEXT-DEPENDENT BIOLOGY ---
    if cell_type == "Healthy":
        # Healthy cells: High reserve, sparse VDAC1, robust scavenging
        resilience = 1.0 
        scavenging_capacity = 2.0 
        g_max = 0.8 
    else:
        # Cancer: Minimal reserve, VDAC1 overexpression, low scavenging
        resilience = 0.4 
        scavenging_capacity = 0.4 
        g_max = 6.0 

    # --- 1. THERAPEUTIC PATHWAY (TRPV1) ---
    protection_signal = (cbd_conc / (EC50_TRPV1 + cbd_conc)) * 0.4
    
    # --- 2. CYTOTOXIC PATHWAY (VDAC1 Interaction) ---
    inhibition_factor = 0.05 if blocker_presence else 1.0
    effective_binding = inhibition_factor * (cbd_conc**2 / (Kd_VDAC1**2 + cbd_conc**2))
    vdac_leak = g_max * effective_binding

    # --- DIFFERENTIAL EQUATIONS ---
    
    # dROS/dt: Scavenging vs Generation
    ros_generation = 0.05 + (vdac_leak * 0.15) 
    ros_removal = (scavenging_capacity + (protection_signal * 1.0)) * ROS
    dROS_dt = ros_generation - ros_removal

    # dPsi/dt: Respiration vs Leak vs ROS Damage
    ros_damage = 0.5 * ROS
    # Respiration in healthy cells can ramp up (Metabolic Flexibility)
    respiration_max = 2.0 if cell_type == "Healthy" else 1.0
    respiration = respiration_max + protection_signal - (1.0 - resilience)
    dPsi_dt = respiration - vdac_leak - ros_damage - (0.1 * Psi)
    
    # dApop/dt: Triggered if Potential collapses OR ROS exceeds safety threshold
    trigger = 1.0 if (Psi < 0.5 or ROS > 2.0) else 0.0
    dApop_dt = trigger * 0.8 
    
    return [dPsi_dt, dApop_dt, dROS_dt]

def run_simulation_v3(cbd_conc, blocker, cell_type):
    t = np.linspace(0, 50, 400)
    initial_state = [1.0, 0.0, 0.1]
    sol = odeint(system_dynamics_v3, initial_state, t, args=(cbd_conc, blocker, cell_type))
    return t, sol

# --- EXPERIMENTAL SWEEP ---
cell_types = ['Healthy', 'Cancer (Vulnerable)']
cbd_doses = [0, 5, 20, 40] 

fig, axes = plt.subplots(len(cell_types), 2, figsize=(15, 10), sharex=True)
colors = ['blue', 'green', 'orange', 'red']

for i, cell_type in enumerate(cell_types):
    ax_psi = axes[i, 0]
    ax_ros = axes[i, 1]
    
    for dose, color in zip(cbd_doses, colors):
        t, sol = run_simulation_v3(dose, False, cell_type)
        ax_psi.plot(t, sol[:, 0], color=color, linestyle='-', label=f'CBD {dose}uM')
        ax_ros.plot(t, sol[:, 2], color=color, linestyle='-', label=f'CBD {dose}uM')
        
        if dose == 40:
             t_b, sol_b = run_simulation_v3(dose, True, cell_type)
             ax_psi.plot(t_b, sol_b[:, 0], color=color, linestyle='--', alpha=0.6, label=f'CBD {dose}uM + Blocker')
             ax_ros.plot(t_b, sol_b[:, 2], color=color, linestyle='--', alpha=0.6, label=f'CBD {dose}uM + Blocker')

    ax_psi.axhline(0.5, color='black', linestyle=':', label='Death Threshold ($\Psi < 0.5$)')
    ax_psi.set_title(f'Cell Type: {cell_type} - Potential ($\Psi$)')
    ax_psi.set_ylabel('Potential ($\Psi$)')
    ax_psi.set_ylim(-0.5, 2.5)
    ax_psi.grid(True, alpha=0.3)
    ax_psi.legend(loc='upper right', fontsize='x-small', ncol=2)
    
    ax_ros.axhline(2.0, color='darkred', linestyle=':', label='ROS Toxicity Threshold ($>2.0$)')
    ax_ros.set_title(f'Cell Type: {cell_type} - ROS Levels')
    ax_ros.set_ylabel('ROS (Arbitrary Units)')
    ax_ros.set_ylim(0, 3.0)
    ax_ros.grid(True, alpha=0.3)
    ax_ros.legend(loc='upper right', fontsize='x-small', ncol=2)

axes[-1, 0].set_xlabel('Time')
axes[-1, 1].set_xlabel('Time')

plt.tight_layout()
plt.savefig('cbd_ros_executioner_v3.png')

# --- NUMERICAL SUMMARY ---
print("\n--- THERAPEUTIC INDEX ANALYSIS (40uM CBD) ---")
for cell_type in cell_types:
    t, sol = run_simulation_v3(40, False, cell_type)
    final_psi = sol[-1, 0]
    final_ros = sol[-1, 2]
    status = "SURVIVED" if (final_psi > 0.5 and final_ros < 2.0) else "COLLAPSED"
    print(f"[{cell_type}] at 40uM: Potential={final_psi:.2f}, ROS={final_ros:.2f} -> {status}")

_, sol_block = run_simulation_v3(40, True, 'Cancer (Vulnerable)')
print(f"[Cancer + VDAC Blocker] at 40uM: Potential={sol_block[-1, 0]:.2f}, ROS={sol_block[-1, 2]:.2f} -> RESCUED")

print("\nV3 ROS-Enhanced Simulation complete. Generated 'cbd_ros_executioner_v3.png'")
