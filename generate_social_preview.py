"""Generate a social preview image (1280x640) for GitHub repository."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

fig, ax = plt.subplots(figsize=(12.8, 6.4), dpi=100)
fig.patch.set_facecolor('#0d1117')
ax.set_xlim(0, 12.8)
ax.set_ylim(0, 6.4)
ax.axis('off')

# Title
ax.text(6.4, 5.2, 'CBD Two-Pathway Model',
        fontsize=36, fontweight='bold', color='white',
        ha='center', va='center', fontfamily='sans-serif')

# Subtitle
ax.text(6.4, 4.4, 'Bioenergetic Resilience as Determinant of Selective Cytotoxicity',
        fontsize=16, color='#8b949e', ha='center', va='center', fontfamily='sans-serif')

# Divider
ax.plot([2.5, 10.3], [3.8, 3.8], color='#30363d', linewidth=2)

# Left pathway box
left_box = mpatches.FancyBboxPatch((1.2, 1.2), 4.5, 2.2,
    boxstyle="round,pad=0.15", facecolor='#0e4429', edgecolor='#238636',
    linewidth=2)
ax.add_patch(left_box)
ax.text(3.45, 2.9, 'THERAPEUTIC', fontsize=14, fontweight='bold',
        color='#3fb950', ha='center', va='center')
ax.text(3.45, 2.3, '1\u20135 \u00b5M', fontsize=13,
        color='#8b949e', ha='center', va='center')
ax.text(3.45, 1.7, 'TRPV1 \u00b7 5-HT1A \u00b7 PPAR\u03b3',
        fontsize=11, color='#c9d1d9', ha='center', va='center')

# Right pathway box
right_box = mpatches.FancyBboxPatch((7.1, 1.2), 4.5, 2.2,
    boxstyle="round,pad=0.15", facecolor='#490202', edgecolor='#da3633',
    linewidth=2)
ax.add_patch(right_box)
ax.text(9.35, 2.9, 'CYTOTOXIC', fontsize=14, fontweight='bold',
        color='#f85149', ha='center', va='center')
ax.text(9.35, 2.3, '>10 \u00b5M', fontsize=13,
        color='#8b949e', ha='center', va='center')
ax.text(9.35, 1.7, 'VDAC1 \u00b7 ROS \u00b7 \u0394\u03a8m collapse',
        fontsize=11, color='#c9d1d9', ha='center', va='center')

# Arrow between
ax.annotate('', xy=(6.9, 2.3), xytext=(5.9, 2.3),
            arrowprops=dict(arrowstyle='->', color='#8b949e', lw=2))

# Bottom attribution
ax.text(6.4, 0.5, 'Vasquez 2026  \u00b7  Delaware Valley University  \u00b7  CC BY 4.0',
        fontsize=11, color='#484f58', ha='center', va='center', fontfamily='sans-serif')

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figures', 'social_preview.png')
plt.savefig(output_path, dpi=100, bbox_inches='tight', pad_inches=0,
            facecolor=fig.get_facecolor())
plt.close()
print(f"Social preview saved to {output_path}")
