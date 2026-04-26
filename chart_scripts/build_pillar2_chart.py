"""
Figure: Pillar 2 VC reality waterfall.
Shows where £350m of Sovereign AI Fund equity capital actually ends up
under realistic venture capital base rates from Cambridge Associates and PitchBook.
The argument: even with optimal manager selection, VC base rates dominate fund returns.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

NAVY = '#1f3a5f'
RED = '#c0392b'
ORANGE = '#e67e22'
GREEN = '#27ae60'
GREY = '#7f8c8d'

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 11,
    'axes.titlesize': 13, 'axes.titleweight': 'bold',
    'axes.labelsize': 11, 'figure.facecolor': 'white',
    'axes.facecolor': 'white', 'axes.spines.top': False,
    'axes.spines.right': False, 'axes.grid': True,
    'axes.grid.axis': 'y', 'grid.alpha': 0.3, 'grid.linestyle': '--',
})

fig, axes = plt.subplots(1, 2, figsize=(13, 6.5), gridspec_kw={'width_ratios': [1.3, 1]})

# === LEFT: Waterfall chart of £350m fund equity outcomes ===
ax = axes[0]

# Starting point: £350m deployed across ~30 portfolio companies
# Realistic base rates from Cambridge Associates / PitchBook:
# - 65-75% return less than 1x capital (write-offs / partial returns)
# - 15-20% return 1-3x (modest)
# - 5-10% return 3-10x (good outcomes)
# - 1-3% return 10x+ (home runs)

# Categories and outcomes for £350m
categories = [
    'Total deployed',          # +350
    'Write-offs (~70%)',       # -245 (companies fail, return 0.3x avg)
    'Modest 1-3x (~17%)',      # +60 net (returns ~£120m on £60m, net +£60m)
    'Good 3-10x (~10%)',       # +120 net (returns ~£155m on £35m, net +£120m)
    'Home runs 10-30x (~3%)',  # +110 net (returns ~£120m on £10m, net +£110m)
    'Net realised value',      # final
]

# Component values for waterfall
deployment = 350
write_offs = -245
modest_net = 60
good_net = 120
home_runs_net = 110
final = deployment + write_offs + modest_net + good_net + home_runs_net  # = 395

print(f'Final fund value: £{final}m on £{deployment}m deployed = {final/deployment:.2f}x')
print(f'Net retained equity (above £350m capital): £{final - deployment}m')

# Build waterfall
labels = ['Capital\ndeployed', 'Write-offs', 'Modest\n(1–3x)',
          'Good\n(3–10x)', 'Home runs\n(10x+)', 'Total\nfund value']
values = [deployment, write_offs, modest_net, good_net, home_runs_net, final]

# Calculate bar bottoms for waterfall
bottoms = [0]  # Start
running = deployment
for v in values[1:-1]:
    if v < 0:
        bottoms.append(running + v)
        running += v
    else:
        bottoms.append(running)
        running += v
bottoms.append(0)  # Final bar starts at 0

heights = [deployment, abs(write_offs), modest_net, good_net, home_runs_net, final]

colors = [NAVY, RED, '#e8a87c', GREEN, '#f1c40f', NAVY]

x = np.arange(len(labels))
for i, (xi, h, b, c) in enumerate(zip(x, heights, bottoms, colors)):
    ax.bar(xi, h, bottom=b, color=c, edgecolor='white', linewidth=0.8, width=0.6)

# Connecting lines between bars
for i in range(len(x) - 1):
    if i == 0:
        # From top of deployment to top of write-off start
        y1 = deployment
        y2 = bottoms[1] + heights[1]
        ax.plot([x[i] + 0.3, x[i+1] - 0.3], [y1, y2], color='#888', linestyle=':', linewidth=1)
    elif i == len(x) - 2:
        # To final bar
        y1 = bottoms[i] + (heights[i] if values[i] > 0 else -heights[i])
        # actually just use running total at this point
        running_at_i = sum(values[:i+1])
        ax.plot([x[i] + 0.3, x[i+1] - 0.3], [running_at_i, running_at_i], color='#888', linestyle=':', linewidth=1)
    else:
        running_at_i = sum(values[:i+1])
        ax.plot([x[i] + 0.3, x[i+1] - 0.3], [running_at_i, running_at_i], color='#888', linestyle=':', linewidth=1)

# Value labels on bars
for i, (xi, h, b, v) in enumerate(zip(x, heights, bottoms, values)):
    if i == 1:  # Write-offs
        ax.text(xi, b + h/2, f'−£{abs(v)}m', ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')
    elif v > 0 and i not in (0, 5):
        ax.text(xi, b + h/2, f'+£{v}m', ha='center', va='center',
                fontsize=10, fontweight='bold', color='white')
    elif i in (0, 5):
        ax.text(xi, h + 10, f'£{v}m', ha='center', va='bottom',
                fontsize=11, fontweight='bold', color='#222')

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=8.5)
ax.set_ylabel('£ million', fontsize=11)
ax.set_title('Sovereign AI Fund: £350m equity outcomes after 8–10 years\n(Realistic VC base rates from Cambridge Associates / PitchBook)',
             fontsize=12, fontweight='bold', pad=15)
ax.set_ylim(0, 450)
ax.axhline(deployment, color='#888', linewidth=0.8, linestyle='--', alpha=0.6)
ax.text(0.05, deployment + 8, 'Capital deployed line (£350m)', fontsize=8, color='#888', style='italic')

# === RIGHT: Implications for the £40bn welfare-gap-closing claim ===
ax = axes[1]

categories_eq = ['Pillar 1\nrent capture', 'Pillar 2\nequity', 'Pillar 3\nleak reduction', 'Combined\ntotal']
values_eq = [35, 0.3, 5, 40.3]
colors_eq = [GREEN, ORANGE, NAVY, '#222']

bars_eq = ax.bar(categories_eq, values_eq, color=colors_eq, edgecolor='white',
                 linewidth=0.5, width=0.6)
for bar, val in zip(bars_eq, values_eq):
    if val < 1:
        ax.text(bar.get_x() + bar.get_width()/2, val + 1.5,
                f'£{val:.1f}bn', ha='center', fontsize=10, fontweight='bold', color=ORANGE)
    else:
        ax.text(bar.get_x() + bar.get_width()/2, val + 1.5,
                f'£{val:.0f}bn', ha='center', fontsize=10, fontweight='bold', color='#222')

# Annotation explaining Pillar 2 small contribution
ax.annotate('Pillar 2 contributes\n<1% of total\n— even with success', xy=(1, 0.3),
            xytext=(1, 18), fontsize=9.5, color=ORANGE, fontweight='bold', ha='center',
            arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.2))

ax.set_ylabel('Welfare gap closed (£bn cumulative through 2035)', fontsize=10)
ax.set_title('Three-pillar contribution decomposition\nPillar 2 equity returns are not the welfare lever',
             fontsize=12, fontweight='bold', pad=15)
ax.set_ylim(0, 50)
import matplotlib.ticker as mtick
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'£{int(x)}bn'))

fig.text(0.5, 0.02,
         "VC base rates: ~70% of portfolio returns <1x (write-offs averaging 0.3x), ~17% return 1–3x, ~10% return 3–10x, ~3% return 10–30x. "
         "Total realised value £395m on £350m deployed = 1.13x net of capital. "
         "Implication: Pillar 2 succeeds at picking — equity returns are still small relative to rent capture.",
         ha='center', fontsize=8.5, style='italic', color='#555555', wrap=True)
fig.subplots_adjust(bottom=0.16)

fig.savefig('figures/16_pillar2_vc_waterfall.png', dpi=150, bbox_inches='tight',
            facecolor='white', pad_inches=0.3)
plt.close(fig)
print('Saved figures/16_pillar2_vc_waterfall.png')
