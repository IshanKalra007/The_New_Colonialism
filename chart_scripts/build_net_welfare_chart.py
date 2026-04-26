"""
Figure: Net welfare scenarios.
Shows gross UK AI productivity gain across three scenarios vs the £486bn rent extraction,
illustrating the central honesty argument that under realistic productivity assumptions
the UK is net welfare-negative on AI through 2030.
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

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
    'axes.spines.right': False, 'axes.grid': True,
    'axes.grid.axis': 'y', 'grid.alpha': 0.3, 'grid.linestyle': '--',
})

fig, ax = plt.subplots(figsize=(11, 6.5))

scenarios = ['Pessimistic\n(0.1 ppts)', 'Central\n(0.3 ppts)', 'Optimistic\n(0.6 ppts)', 'BoE forecast\n(0.8 ppts)']
gross_gain = [82, 239, 490, 712]
rent_extraction = [486, 486, 486, 486]
net_no_policy = [-404, -247, 4, 226]
net_with_policy = [-364, -207, 44, 266]

x = np.arange(len(scenarios))
width = 0.22

# Bars - 4 grouped bars per scenario
bars1 = ax.bar(x - 1.5*width, gross_gain, width,
               label='Gross AI productivity gain (UK)',
               color=GREEN, edgecolor='white', linewidth=0.5)
bars2 = ax.bar(x - 0.5*width, [-r for r in rent_extraction], width,
               label='Cross-border rent extraction (£486bn)',
               color=RED, edgecolor='white', linewidth=0.5)
bars3 = ax.bar(x + 0.5*width, net_no_policy, width,
               label='Net welfare without policy',
               color=NAVY, edgecolor='white', linewidth=0.5)
bars4 = ax.bar(x + 1.5*width, net_with_policy, width,
               label='Net welfare with three-pillar policy',
               color=BLUE, edgecolor='white', linewidth=0.5,
               hatch='//')

# Value labels above/below bars
def label_bars(bars, values, color):
    for bar, val in zip(bars, values):
        height = bar.get_height()
        if val >= 0:
            ax.text(bar.get_x() + bar.get_width()/2, height + 15,
                    f'+£{val}bn', ha='center', va='bottom',
                    fontsize=9, fontweight='bold', color=color)
        else:
            ax.text(bar.get_x() + bar.get_width()/2, height - 15,
                    f'£{val}bn', ha='center', va='top',
                    fontsize=9, fontweight='bold', color=color)

label_bars(bars1, gross_gain, '#1e8449')
label_bars(bars2, [-r for r in rent_extraction], '#922b21')
label_bars(bars3, net_no_policy, NAVY)
label_bars(bars4, net_with_policy, BLUE)

# Zero line
ax.axhline(0, color='#222', linewidth=1)

# Shading for scenarios more / less consistent with current data
ax.axvspan(-0.5, 1.5, alpha=0.05, color=RED, zorder=-1)
ax.axvspan(1.5, 3.5, alpha=0.05, color=GREEN, zorder=-1)

# Annotation on shading
ax.text(0.5, ax.get_ylim()[1] * 0.94, 'More consistent with\ncurrent UK productivity data',
        ha='center', va='top', fontsize=9, style='italic', color='#922b21')
ax.text(2.5, ax.get_ylim()[1] * 0.94, 'Requires step-change in\nUK productivity dynamics',
        ha='center', va='top', fontsize=9, style='italic', color='#1e8449')

ax.set_xticks(x)
ax.set_xticklabels(scenarios)
ax.set_ylabel('Cumulative through 2030 (£ billion)', fontsize=11)
ax.set_title('Net Welfare Arithmetic Across Productivity Scenarios\n£486bn rent extraction vs gross UK AI productivity gain, with and without three-pillar policy',
             fontsize=12, fontweight='bold', pad=15)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'£{int(x):+d}bn' if x != 0 else '£0bn'))
ax.set_ylim(-560, 800)
ax.legend(loc='lower right', frameon=True, framealpha=0.95, fontsize=9)

fig.text(0.5, 0.02,
         "Productivity gain calculated year-by-year from £2,720bn 2023 GDP base at 1% baseline plus AI ppts. "
         "BoE 0.8 ppts forecast (Bank of England 2025) shown as upper-bound case. UK measured productivity 2023-2025 most consistent with pessimistic-to-central range.",
         ha='center', fontsize=8.5, style='italic', color='#555555', wrap=True)
fig.subplots_adjust(bottom=0.13)

fig.savefig('figures/10_net_welfare_scenarios.png', dpi=150, bbox_inches='tight',
            facecolor='white', pad_inches=0.3)
plt.close(fig)
print('Saved figures/10_net_welfare_scenarios.png')
