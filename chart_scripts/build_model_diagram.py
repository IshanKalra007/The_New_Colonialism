"""
Figure: Two-country model flow diagram (cleaner version).
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch
import numpy as np

NAVY = '#1f3a5f'
BLUE = '#3a7ca5'
RED = '#c0392b'
ORANGE = '#e67e22'
GREEN = '#27ae60'
DARK_GREEN = '#16a085'

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 11,
    'figure.facecolor': 'white', 'axes.facecolor': 'white',
})

fig, ax = plt.subplots(figsize=(13, 7))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

ax.text(7, 9.5, 'Two-country model: where the cross-border externality lives',
        ha='center', fontsize=14, fontweight='bold', color='#222')

# === DEPLOYING ECONOMY (left) ===
ax.add_patch(Rectangle((0.3, 1.0), 6.4, 7.7, facecolor='#fef5f5',
                        edgecolor=RED, linewidth=1.2, alpha=0.5))
ax.text(3.5, 8.4, 'Deploying economy (UK)',
        ha='center', fontsize=12, fontweight='bold', color=RED)

# UK firms
ax.add_patch(FancyBboxPatch((0.7, 6.3), 2.4, 1.4, boxstyle="round,pad=0.05",
                             facecolor='white', edgecolor=NAVY, linewidth=1.5))
ax.text(1.9, 7.3, 'N firms', ha='center', va='center', fontsize=11, fontweight='bold')
ax.text(1.9, 6.85, 'Choose α ∈ [0,1]', ha='center', va='center', fontsize=9)
ax.text(1.9, 6.55, '(automation level)', ha='center', va='center', fontsize=8.5, color='#666', style='italic')

# UK workers
ax.add_patch(FancyBboxPatch((0.7, 4.0), 2.4, 1.4, boxstyle="round,pad=0.05",
                             facecolor='white', edgecolor=BLUE, linewidth=1.5))
ax.text(1.9, 5.0, 'Workers', ha='center', va='center', fontsize=11, fontweight='bold')
ax.text(1.9, 4.55, 'Wage w; MPC ρ', ha='center', va='center', fontsize=9)
ax.text(1.9, 4.25, 'Reemployment η', ha='center', va='center', fontsize=9)

# UK aggregate demand
ax.add_patch(FancyBboxPatch((0.7, 1.7), 2.4, 1.4, boxstyle="round,pad=0.05",
                             facecolor='white', edgecolor=ORANGE, linewidth=1.5))
ax.text(1.9, 2.7, 'Aggregate demand', ha='center', va='center', fontsize=11, fontweight='bold')
ax.text(1.9, 2.3, 'E = autonomous +', ha='center', va='center', fontsize=9)
ax.text(1.9, 2.0, 'worker spending', ha='center', va='center', fontsize=9)

# UK arrows (vertical chain)
arrow_e = FancyArrowPatch((1.9, 6.3), (1.9, 5.4), arrowstyle='->',
                          mutation_scale=18, color=BLUE, lw=1.8)
ax.add_patch(arrow_e)
ax.text(2.4, 5.85, 'Employ\n(1−α)L workers', ha='left', va='center', fontsize=8.5, color=BLUE)

arrow_s = FancyArrowPatch((1.9, 4.0), (1.9, 3.1), arrowstyle='->',
                          mutation_scale=18, color=ORANGE, lw=1.8)
ax.add_patch(arrow_s)
ax.text(2.4, 3.55, 'Spend ρw', ha='left', va='center', fontsize=8.5, color=ORANGE)

# UK feedback arrow (curved on left side)
arrow_fb = FancyArrowPatch((0.85, 2.5), (0.85, 7.0),
                           arrowstyle='->', mutation_scale=18, color='#666',
                           lw=1.4, connectionstyle="arc3,rad=-0.3")
ax.add_patch(arrow_fb)
ax.text(0.45, 4.7, 'Revenue E/N', ha='center', va='center',
        fontsize=8.5, color='#666', style='italic', rotation=90)

# Note about within-economy cycle - placed in the clear space between
# the cross-border arrow and the return flow, at right side of UK panel
ax.text(5.55, 6.0, 'Within-economy cycle\n(Hemenway-Falk-Tsoukalas 2026)',
        ha='center', va='center', fontsize=8.5, style='italic', color='#888',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='#ccc', linewidth=0.5))

# === AI PROVIDER ECONOMY (right) ===
ax.add_patch(Rectangle((7.3, 1.0), 6.4, 7.7, facecolor='#fff8e1',
                        edgecolor='#f9a825', linewidth=1.2, alpha=0.5))
ax.text(10.5, 8.4, 'AI provider economy (US)',
        ha='center', fontsize=12, fontweight='bold', color='#e65100')

# AI provider
ax.add_patch(FancyBboxPatch((8.0, 6.3), 4.0, 1.4, boxstyle="round,pad=0.05",
                             facecolor='white', edgecolor='#e65100', linewidth=1.5))
ax.text(10.0, 7.3, 'AI provider', ha='center', va='center', fontsize=11, fontweight='bold')
ax.text(10.0, 6.85, 'Sells AI tasks at price c', ha='center', va='center', fontsize=9)
ax.text(10.0, 6.55, 'Receives αLc per firm', ha='center', va='center', fontsize=9)

# US economy
ax.add_patch(FancyBboxPatch((9.3, 4.0), 3.4, 1.4, boxstyle="round,pad=0.05",
                             facecolor='white', edgecolor='#888', linewidth=1.5))
ax.text(11.0, 5.0, 'US economy', ha='center', va='center', fontsize=11, fontweight='bold')
ax.text(11.0, 4.55, 'Staff wages, dividends,', ha='center', va='center', fontsize=9)
ax.text(11.0, 4.25, 'US corporation tax', ha='center', va='center', fontsize=9)

# AI provider → US economy (kept-back portion)
arrow_us = FancyArrowPatch((10.5, 6.3), (10.8, 5.4),
                           arrowstyle='->', mutation_scale=18, color='#e65100', lw=2)
ax.add_patch(arrow_us)
ax.text(12.5, 5.85, 'λαLc retained\n(85p of £1)',
        ha='center', va='center', fontsize=9, color='#e65100', fontweight='bold')

# === KEY ARROW: Cross-border AI flow (the central object) ===
arrow_xb = FancyArrowPatch((3.1, 7.0), (8.0, 7.0),
                            arrowstyle='->', mutation_scale=28, color=RED, lw=4)
ax.add_patch(arrow_xb)
ax.text(5.55, 7.5, 'AI subscription flow: αLc',
        ha='center', va='center', fontsize=11, fontweight='bold', color=RED)
ax.text(5.55, 7.85, '(UK firm pays US AI provider)',
        ha='center', va='center', fontsize=8.5, style='italic', color='#666')

# Return flow: (1-λ) returns to UK
arrow_return = FancyArrowPatch((9.3, 4.7), (3.1, 4.7),
                                arrowstyle='->', mutation_scale=18,
                                color=DARK_GREEN, lw=2.5)
ax.add_patch(arrow_return)
ax.text(6.2, 5.2, 'Return flow: (1−λ)αLc returns to UK',
        ha='center', va='center', fontsize=10, fontweight='bold', color=DARK_GREEN)
ax.text(6.2, 4.4, 'Five channels: UK staff wages, integration partners,',
        ha='center', va='center', fontsize=8.5, style='italic', color='#666')
ax.text(6.2, 4.1, 'UK CT, university research, equity dividends',
        ha='center', va='center', fontsize=8.5, style='italic', color='#666')

# Bottom box: parameter definition (full-width, clear)
ax.add_patch(Rectangle((0.3, 0.15), 13.4, 0.65, facecolor='#1a1a1a', edgecolor='none'))
ax.text(7, 0.55, 'λ = cross-border leakage parameter',
        ha='center', va='center', fontsize=10.5, color='white', fontweight='bold')
ax.text(7, 0.30, 'λ = 0: closed-economy benchmark (Hemenway-Falk-Tsoukalas 2026)   |   λ = 0.85: UK central case   |   λ = 1: complete leakage',
        ha='center', va='center', fontsize=9, color='white')

fig.subplots_adjust(left=0.02, right=0.98, top=0.96, bottom=0.04)

fig.savefig('figures/13_two_country_model.png', dpi=150, bbox_inches='tight',
            facecolor='white', pad_inches=0.3)
plt.close(fig)
print('Saved figures/13_two_country_model.png')
