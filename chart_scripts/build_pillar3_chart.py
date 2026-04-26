"""
Figure 8: Pillar 3 supply-side leak.
Shows where £1 deployed in a UK AI startup actually ends up — the central argument
for why Pillars 1+2 are insufficient and Pillar 3 (UK-hosted infrastructure) is
welfare-necessary.
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.patches as patches
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

NAVY = '#1f3a5f'
BLUE = '#3a7ca5'
RED = '#c0392b'
ORANGE = '#e67e22'
YELLOW = '#f1c40f'
GREEN = '#27ae60'
DARK_GREEN = '#16a085'
GREY = '#7f8c8d'

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 11,
    'axes.titlesize': 13, 'axes.titleweight': 'bold',
    'axes.labelsize': 11, 'figure.facecolor': 'white',
    'axes.facecolor': 'white', 'axes.spines.top': False,
    'axes.spines.right': False, 'axes.grid': False,
})

fig, axes = plt.subplots(1, 2, figsize=(13, 6.5), gridspec_kw={'width_ratios': [1.1, 1]})

# ============================================================
# LEFT PANEL: Where £1 of UK AI startup spend goes (donut)
# ============================================================
ax = axes[0]

# Cost structure of typical UK AI startup
# Sources: Crunchbase, Beauhurst UK AI startup data, sample of 50 firms
labels = [
    'Cloud & compute\n(AWS / Azure / GCP)\n55p',
    'Hardware\n(NVIDIA 85% / AMD)\n8p',
    'UK wages\nand operations\n30p',
    'Other US\nservices*\n7p',
]
sizes = [55, 8, 30, 7]
# Red palette for US-bound, green for UK-retained
colors = [RED, '#a93226', GREEN, '#c0392b']
explode = (0.02, 0.02, 0.05, 0.02)  # Slight separation, UK section stands out

wedges, texts = ax.pie(sizes, labels=labels, colors=colors, startangle=90,
                       wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
                       explode=explode, textprops={'fontsize': 10})

# Center summary
ax.text(0, 0.10, 'Of £1 deployed by\nthe Sovereign AI Fund...',
        ha='center', va='center', fontsize=11, color='#444')
ax.text(0, -0.10, '70p leaks\nto US', ha='center', va='center',
        fontsize=18, fontweight='bold', color=RED)
ax.text(0, -0.30, '30p stays in UK', ha='center', va='center',
        fontsize=11, fontweight='bold', color=GREEN)

ax.set_title("Where £1 of UK AI startup spend actually goes\n(typical cost structure, post-Sovereign-AI-Fund deployment)",
             fontsize=12, fontweight='bold', pad=15)

# ============================================================
# RIGHT PANEL: Pillar 3 closing the loop (sankey-style flow)
# ============================================================
ax = axes[1]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Title
ax.text(5, 9.5, 'Pillar 3 closes the loop',
        ha='center', fontsize=12, fontweight='bold', color='#222')

# Status quo box (left)
ax.add_patch(Rectangle((0.3, 7), 4, 1.5, facecolor='#f5f5f5',
                        edgecolor='#888', linewidth=1))
ax.text(2.3, 7.75, 'Without Pillar 3',
        ha='center', va='center', fontsize=11, fontweight='bold')
ax.text(2.3, 7.25, '£1 in → 30p UK retained',
        ha='center', va='center', fontsize=10, color=RED)

# With Pillar 3 box
ax.add_patch(Rectangle((5.5, 7), 4, 1.5, facecolor='#e8f5e9',
                        edgecolor=GREEN, linewidth=1.5))
ax.text(7.5, 7.75, 'With Pillar 3',
        ha='center', va='center', fontsize=11, fontweight='bold', color=DARK_GREEN)
ax.text(7.5, 7.25, '£1 in → 60-70p UK retained',
        ha='center', va='center', fontsize=10, color=DARK_GREEN, fontweight='bold')

# Three Pillar 3 components below
components = [
    {
        'y': 5.2,
        'title': '(i) UK-hosted hyperscale compute',
        'detail': '£15-25bn capital 2026-2030',
        'mechanism': 'Cloud spend (55p) → UK-resident:\n~30-40p of cloud retained',
        'color': BLUE,
    },
    {
        'y': 3.4,
        'title': '(ii) Non-US chip partnerships',
        'detail': 'Cerebras, Graphcore (UK), Tenstorrent, SambaNova',
        'mechanism': 'Hardware spend (8p) → diversified:\n~3-5p retained or non-US allocated',
        'color': ORANGE,
    },
    {
        'y': 1.6,
        'title': '(iii) Energy policy',
        'detail': 'SMRs, grid, renewables → £40/MWh from £180/MWh',
        'mechanism': 'Removes binding constraint on (i):\nmakes UK hosting economically viable',
        'color': YELLOW,
    },
]

for comp in components:
    # Component box
    ax.add_patch(Rectangle((0.3, comp['y']-0.6), 9.4, 1.4,
                           facecolor='white', edgecolor=comp['color'], linewidth=1.8))
    ax.text(0.5, comp['y']+0.5, comp['title'],
            ha='left', va='center', fontsize=10, fontweight='bold', color=comp['color'])
    ax.text(0.5, comp['y']+0.15, comp['detail'],
            ha='left', va='center', fontsize=9, color='#444', style='italic')
    ax.text(0.5, comp['y']-0.25, comp['mechanism'],
            ha='left', va='center', fontsize=9, color='#222')

# Bottom note
ax.text(5, 0.4, '£20-35bn total Pillar 3 outlay → £3-7bn supply-side leakage reduction',
        ha='center', va='center', fontsize=9.5, fontweight='bold', color=DARK_GREEN,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#e8f5e9', edgecolor=GREEN, linewidth=1))

# Save
fig.text(0.5, 0.02,
         "Cost structure based on Crunchbase, Beauhurst UK AI startup data; sample of 50 UK AI firms 2024-2025. "
         "* 'Other US services' = SaaS subscriptions, payment processing, analytics tools. "
         "Cloud and hardware shares vary by stage; figures reflect typical Series A/B AI startup.",
         ha='center', fontsize=8.5, style='italic', color='#555555', wrap=True)
fig.subplots_adjust(bottom=0.14)

fig.savefig('figures/08_pillar3_supply_leak.png', dpi=150, bbox_inches='tight',
            facecolor='white', pad_inches=0.3)
plt.close(fig)
print('Saved figures/08_pillar3_supply_leak.png')
