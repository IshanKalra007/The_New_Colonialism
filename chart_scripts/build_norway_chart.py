"""
Figure: Norway vs UK bilateral AI flow comparison.
Vertical layout — UK on top, Norway on bottom — to avoid label collisions.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch
import numpy as np

NAVY = '#1f3a5f'
RED = '#c0392b'
ORANGE = '#e67e22'
DARK_GREEN = '#16a085'

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 11,
    'figure.facecolor': 'white', 'axes.facecolor': 'white',
})

fig, axes = plt.subplots(1, 2, figsize=(13, 6.8), gridspec_kw={'width_ratios': [1.4, 1]})

# LEFT PANEL
ax = axes[0]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

ax.text(5, 9.7, 'Bilateral AI flows: UK vs Norway',
        ha='center', fontsize=13, fontweight='bold', color='#222')

# UK row
ax.add_patch(Rectangle((0, 6), 10, 3.3, facecolor='#fef5f5', edgecolor='#fce4e4', linewidth=0))
ax.text(0.3, 8.7, 'UK:', ha='left', va='center', fontsize=11, fontweight='bold', color=RED)

uk_box = FancyBboxPatch((0.3, 7.0), 2.5, 1.0, boxstyle="round,pad=0.05",
                        facecolor='white', edgecolor=RED, linewidth=1.8)
ax.add_patch(uk_box)
ax.text(1.55, 7.5, 'United Kingdom', ha='center', va='center', fontsize=11, fontweight='bold')

us_box_uk = FancyBboxPatch((7.2, 7.0), 2.5, 1.0, boxstyle="round,pad=0.05",
                            facecolor='white', edgecolor='#888', linewidth=1.5)
ax.add_patch(us_box_uk)
ax.text(8.45, 7.5, 'United States', ha='center', va='center', fontsize=11, fontweight='bold')

arrow_uk_a = FancyArrowPatch((2.85, 7.5), (7.15, 7.5),
                              arrowstyle='->', mutation_scale=22, color=RED, lw=4)
ax.add_patch(arrow_uk_a)
ax.text(5, 8.0, 'Flow A: AI consumption  →  λ ≈ 0.85, £139bn by 2030',
        ha='center', va='center', fontsize=10, color=RED, fontweight='bold')
ax.text(5, 6.7, '(No Flow B — Stargate UK paused April 2026)',
        ha='center', va='center', fontsize=9.5, style='italic', color='#888')

# Divider
ax.plot([0, 10], [5.7, 5.7], color='#ccc', linewidth=0.8)

# Norway row
ax.add_patch(Rectangle((0, 1.8), 10, 3.5, facecolor='#f5fdf7', edgecolor='#e0f0e5', linewidth=0))
ax.text(0.3, 5.0, 'Norway:', ha='left', va='center', fontsize=11, fontweight='bold', color=DARK_GREEN)

no_box = FancyBboxPatch((0.3, 3.5), 2.5, 1.0, boxstyle="round,pad=0.05",
                        facecolor='white', edgecolor=DARK_GREEN, linewidth=1.8)
ax.add_patch(no_box)
ax.text(1.55, 4.0, 'Norway', ha='center', va='center', fontsize=11, fontweight='bold')

us_box_no = FancyBboxPatch((7.2, 3.5), 2.5, 1.0, boxstyle="round,pad=0.05",
                            facecolor='white', edgecolor='#888', linewidth=1.5)
ax.add_patch(us_box_no)
ax.text(8.45, 4.0, 'United States', ha='center', va='center', fontsize=11, fontweight='bold')

arrow_no_a = FancyArrowPatch((2.85, 4.2), (7.15, 4.2),
                              arrowstyle='->', mutation_scale=22, color=RED, lw=4)
ax.add_patch(arrow_no_a)
ax.text(5, 4.7, 'Flow A: AI consumption  →  λ ≈ 0.80–0.85 (similar to UK)',
        ha='center', va='center', fontsize=10, color=RED, fontweight='bold')

arrow_no_b = FancyArrowPatch((7.15, 3.8), (2.85, 3.8),
                              arrowstyle='->', mutation_scale=22, color=DARK_GREEN, lw=4)
ax.add_patch(arrow_no_b)
ax.text(5, 3.3, 'Flow B: Infrastructure hosting  ←  λ ≈ 0.40–0.50 (partial offset)',
        ha='center', va='center', fontsize=10, color=DARK_GREEN, fontweight='bold')

# Bottom summary box
ax.add_patch(Rectangle((0.3, 0.4), 9.4, 1.1, facecolor='#f9f9f9', edgecolor='#888', linewidth=1))
ax.text(0.6, 1.15, 'UK:', ha='left', va='center', fontsize=9.5, fontweight='bold', color=RED)
ax.text(1.4, 1.15, 'full consumption leak, no offsetting inflow → net rent flow outbound only',
        ha='left', va='center', fontsize=9.5, color='#222')
ax.text(0.6, 0.7, 'Norway:', ha='left', va='center', fontsize=9.5, fontweight='bold', color=DARK_GREEN)
ax.text(1.7, 0.7, 'consumption leak partially offset by hosting; GPFG buffers residual loss',
        ha='left', va='center', fontsize=9.5, color='#222')

# RIGHT PANEL
ax = axes[1]
countries = ['Norway\n(Narvik)', 'US (Texas\nlarge user)', 'UK industrial\n(current)', 'UK industrial\n(target)']
prices = [35, 40, 180, 70]
colors = [DARK_GREEN, '#888', RED, ORANGE]

x = np.arange(len(countries))
bars = ax.bar(x, prices, color=colors, edgecolor='white', linewidth=0.5, width=0.65)

for bar, val in zip(bars, prices):
    ax.text(bar.get_x() + bar.get_width()/2, val + 5,
            f'£{val}/MWh', ha='center', fontsize=10, fontweight='bold', color='#222')

ax.annotate('', xy=(2, 175), xytext=(0, 35),
            arrowprops=dict(arrowstyle='<->', color='#444', lw=1.2))
ax.text(1, 105, '5×\ndifferential', ha='center', fontsize=10,
        fontweight='bold', color='#444')

ax.annotate('', xy=(3, 70), xytext=(2, 175),
            arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.5))
ax.text(2.55, 130, 'Pillar 3\nenergy policy\ngap', ha='center', fontsize=9,
        fontweight='bold', color=ORANGE)

ax.set_xticks(x)
ax.set_xticklabels(countries, fontsize=9)
ax.set_ylabel('Industrial electricity (£/MWh)', fontsize=11)
ax.set_title('Energy cost: the binding constraint\n(Why Norway hosts and the UK cannot)',
             fontsize=12, fontweight='bold', pad=15)
ax.set_ylim(0, 220)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

fig.text(0.5, 0.02,
         "Sources: IEA Industrial Electricity Prices G7 Comparison Q1 2026; Norwegian hydropower wholesale rates (Narvik); ERCOT large-user pricing. "
         "UK target reflects Pillar 3 outcome with grid investment, SMRs, and renewables tied to compute infrastructure.",
         ha='center', fontsize=8.5, style='italic', color='#555555', wrap=True)
fig.subplots_adjust(bottom=0.13)

fig.savefig('figures/12_norway_uk_comparison.png', dpi=150, bbox_inches='tight',
            facecolor='white', pad_inches=0.3)
plt.close(fig)
print('Saved figures/12_norway_uk_comparison.png')
