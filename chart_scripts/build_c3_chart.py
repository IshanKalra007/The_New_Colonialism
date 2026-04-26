"""
Figure: Component 3 productivity rent capture trajectory.
Visualises the 5%->32% capture rate ramp anchored on three sources.
Currently only in Appendix B as a table — needs to be in body where Component 3
is introduced.
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

NAVY = '#1f3a5f'
RED = '#c0392b'
ORANGE = '#e67e22'
GREEN = '#27ae60'

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 11,
    'axes.titlesize': 13, 'axes.titleweight': 'bold',
    'axes.labelsize': 11, 'figure.facecolor': 'white',
    'axes.facecolor': 'white', 'axes.spines.top': False,
    'axes.spines.right': False, 'axes.grid': True,
    'axes.grid.axis': 'y', 'grid.alpha': 0.3, 'grid.linestyle': '--',
})

fig, axes = plt.subplots(1, 2, figsize=(13, 6), gridspec_kw={'width_ratios': [1.1, 1]})

# === LEFT: Capture rate trajectory ===
ax = axes[0]
years = list(range(2023, 2031))
capture_rate = [5, 8, 12, 17, 22, 27, 31, 32]
capture_lower = [3, 5, 8, 12, 16, 19, 22, 22]
capture_upper = [7, 12, 17, 22, 28, 35, 39, 40]

ax.fill_between(years, capture_lower, capture_upper, alpha=0.15, color=RED)
ax.plot(years, capture_rate, color=RED, linewidth=3, marker='o', markersize=8,
        label='Central trajectory')
ax.plot(years, capture_lower, color=RED, linewidth=1, linestyle=':', alpha=0.6)
ax.plot(years, capture_upper, color=RED, linewidth=1, linestyle=':', alpha=0.6)

# Annotation: cloud computing precedent benchmark
ax.axhline(30, color=NAVY, linewidth=1, linestyle='--', alpha=0.7)
ax.text(2023.2, 31, 'Cloud computing capture rate (precedent)',
        fontsize=9, color=NAVY, va='bottom', style='italic')

# Three anchor points
ax.scatter([2024], [8], s=150, color='white', edgecolor=NAVY, linewidth=2.5, zorder=5)
ax.annotate('Anchor 1:\nMicrosoft Copilot\nDec 2025 +13%', xy=(2024, 8), xytext=(2023.2, 18),
            fontsize=9, color=NAVY, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.2))

ax.scatter([2026], [17], s=150, color='white', edgecolor=ORANGE, linewidth=2.5, zorder=5)
ax.annotate('Anchor 2:\nSalesforce token\nbilling Oct 2025', xy=(2026, 17), xytext=(2026.7, 6),
            fontsize=9, color=ORANGE, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.2))

ax.scatter([2030], [32], s=150, color='white', edgecolor=GREEN, linewidth=2.5, zorder=5)
ax.annotate('Anchor 3:\nCloud precedent\n(7-9yr matures)', xy=(2030, 32), xytext=(2027.5, 38),
            fontsize=9, color=GREEN, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.2))

# Value labels
for i, (yr, rate) in enumerate(zip(years, capture_rate)):
    if i % 2 == 0 or i == len(years) - 1:
        ax.text(yr, rate - 2, f'{rate}%', ha='center', fontsize=9, color=RED, fontweight='bold')

ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Capture rate θ (%)', fontsize=11)
ax.set_title('Provider capture rate θ trajectory, 2023–2030\nAnchored on three precedents',
             fontsize=12, fontweight='bold', pad=15)
ax.set_ylim(0, 45)
ax.set_xticks(years)

# === RIGHT: Annual transfer to US shareholders ===
ax = axes[1]
prod_gain = [1.0, 4.5, 14.0, 29.0, 49.0, 72.0, 96.0, 119.0]
us_rent = [pg * cr / 100 for pg, cr in zip(prod_gain, capture_rate)]
cum_rent = np.cumsum(us_rent)

x = np.arange(len(years))
width = 0.65
bars = ax.bar(x, us_rent, width, color=RED, edgecolor='white', linewidth=0.5,
              label='Annual rent transfer')

for bar, val in zip(bars, us_rent):
    if val >= 1:
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.8,
                f'£{val:.1f}bn', ha='center', fontsize=8.5, fontweight='bold', color='#222')

# Cumulative line on right axis
ax2 = ax.twinx()
ax2.plot(x, cum_rent, color=NAVY, linewidth=2.5, marker='s', markersize=6, zorder=5)
ax2.set_ylabel('Cumulative through 2030 (£bn)', fontsize=10, color=NAVY)
ax2.tick_params(axis='y', labelcolor=NAVY)
ax2.set_ylim(0, max(cum_rent) * 1.18)
ax2.spines['top'].set_visible(False)
ax2.grid(False)
ax2.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'£{int(x)}bn'))

# Cumulative final annotation
ax2.annotate(f'£{cum_rent[-1]:.0f}bn\ncumulative\n(Component 3)',
             xy=(7, cum_rent[-1]), xytext=(4, cum_rent[-1] - 25),
             fontsize=10, fontweight='bold', color=NAVY, ha='center',
             arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.2))

ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Annual rent transfer (£bn)', fontsize=11, color=RED)
ax.tick_params(axis='y', labelcolor=RED)
ax.set_title('Productivity rent transfer to US shareholders\nθ × UK AI productivity gain',
             fontsize=12, fontweight='bold', pad=15)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'£{int(x)}bn'))
ax.set_ylim(0, max(us_rent) * 1.20)

fig.text(0.5, 0.02,
         "Capture rate θ = (price − marginal cost) / (productivity gain − marginal cost). Anchors: Microsoft Investor Relations Dec 2025; Salesforce Q3 FY26 earnings; cloud capture rate (AWS/Azure/GCP) 2010–2025 compressed to 7–9 years. "
         "Sensitivity range £60–160bn (Appendix B).",
         ha='center', fontsize=8.5, style='italic', color='#555555', wrap=True)
fig.subplots_adjust(bottom=0.13)

fig.savefig('figures/15_component3_trajectory.png', dpi=150, bbox_inches='tight',
            facecolor='white', pad_inches=0.3)
plt.close(fig)
print('Saved figures/15_component3_trajectory.png')
print(f'Cumulative C3 = £{cum_rent[-1]:.0f}bn (target: £105bn)')
