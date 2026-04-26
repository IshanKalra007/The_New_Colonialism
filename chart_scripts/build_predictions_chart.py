"""
Figure: Forward predictions across three scenarios through Q4 2027.
Shows λ trajectory and cumulative rent loss diverging based on policy choices.
The pre-registration anchor for the paper.
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

NAVY = '#1f3a5f'
RED = '#c0392b'
ORANGE = '#e67e22'
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

fig, axes = plt.subplots(1, 2, figsize=(13, 6.5))

# Quarterly horizon: Q1 2026 through Q4 2027
quarters = ['Q2-26', 'Q3-26', 'Q4-26', 'Q1-27', 'Q2-27', 'Q3-27', 'Q4-27']
x = np.arange(len(quarters))

# === LEFT: λ trajectory across three scenarios ===
ax = axes[0]

# All scenarios start at λ ≈ 0.85 (Q2 2026 ~ now)
# Scenario A: Base case - λ continues drifting up
lambda_a = [0.85, 0.86, 0.87, 0.87, 0.88, 0.88, 0.89]
# Scenario B: Concessions granted - λ jumps after floodgate effect
lambda_b = [0.85, 0.86, 0.87, 0.88, 0.89, 0.90, 0.91]
# Scenario C: Three-pillar policy - λ falls
lambda_c = [0.85, 0.85, 0.84, 0.83, 0.83, 0.82, 0.82]

ax.plot(x, lambda_a, color=ORANGE, linewidth=2.5, marker='o', markersize=7,
        label='Scenario A: Base case (current trajectory)')
ax.plot(x, lambda_b, color=RED, linewidth=2.5, marker='s', markersize=7,
        label='Scenario B: Stargate UK revival concessions')
ax.plot(x, lambda_c, color=DARK_GREEN, linewidth=2.5, marker='^', markersize=7,
        label='Scenario C: Three-pillar policy enacted')

# Annotations at end-of-period
ax.annotate(f'λ = {lambda_a[-1]:.2f}', xy=(x[-1], lambda_a[-1]), xytext=(x[-1]+0.3, lambda_a[-1]),
            fontsize=10, fontweight='bold', color=ORANGE, va='center')
ax.annotate(f'λ = {lambda_b[-1]:.2f}', xy=(x[-1], lambda_b[-1]), xytext=(x[-1]+0.3, lambda_b[-1]),
            fontsize=10, fontweight='bold', color=RED, va='center')
ax.annotate(f'λ = {lambda_c[-1]:.2f}', xy=(x[-1], lambda_c[-1]), xytext=(x[-1]+0.3, lambda_c[-1]),
            fontsize=10, fontweight='bold', color=DARK_GREEN, va='center')

ax.axhline(0.85, color='#888', linewidth=0.8, linestyle=':', alpha=0.6)
ax.text(0, 0.852, 'Current λ (2026 central)', fontsize=8.5, color='#666', va='bottom', style='italic')

ax.set_xticks(x)
ax.set_xticklabels(quarters)
ax.set_xlabel('Quarter', fontsize=11)
ax.set_ylabel('Cross-border leakage parameter λ', fontsize=11)
ax.set_title('Pre-registered λ trajectory through Q4 2027\nDiverging by scenario',
             fontsize=12, fontweight='bold', pad=15)
ax.set_ylim(0.78, 0.94)
ax.set_xlim(-0.5, len(quarters) + 0.3)
ax.legend(loc='lower left', frameon=True, framealpha=0.95, fontsize=9)

# === RIGHT: Cumulative rent loss through Q4 2027 ===
ax = axes[1]

# Cumulative rent loss (£bn) - quarterly buildup from Q2 2026 baseline
# Start from ~£15bn cumulative through Q1 2026, build through Q4 2027
# Each quarter adds rent flow at the prevailing λ-implied rate
base_cumulative = 15
quarterly_flow_a = [4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5]  # Base trajectory
quarterly_flow_b = [4.5, 5.0, 5.8, 6.5, 7.5, 8.5, 9.5]  # Concessions accelerate
quarterly_flow_c = [4.5, 4.8, 4.5, 4.2, 4.0, 3.8, 3.6]  # Policy slows

cum_a = base_cumulative + np.cumsum(quarterly_flow_a)
cum_b = base_cumulative + np.cumsum(quarterly_flow_b)
cum_c = base_cumulative + np.cumsum(quarterly_flow_c)

ax.plot(x, cum_a, color=ORANGE, linewidth=2.5, marker='o', markersize=7,
        label=f'Scenario A: £{cum_a[-1]:.0f}bn by Q4-27')
ax.plot(x, cum_b, color=RED, linewidth=2.5, marker='s', markersize=7,
        label=f'Scenario B: £{cum_b[-1]:.0f}bn by Q4-27')
ax.plot(x, cum_c, color=DARK_GREEN, linewidth=2.5, marker='^', markersize=7,
        label=f'Scenario C: £{cum_c[-1]:.0f}bn by Q4-27')

# Fill between A and C to highlight the policy gap
ax.fill_between(x, cum_a, cum_c, alpha=0.10, color=DARK_GREEN, label='Policy gap (A vs C)')

# Annotations
ax.annotate(f'£{cum_a[-1]:.0f}bn', xy=(x[-1], cum_a[-1]), xytext=(x[-1]+0.2, cum_a[-1]),
            fontsize=10, fontweight='bold', color=ORANGE, va='center')
ax.annotate(f'£{cum_b[-1]:.0f}bn', xy=(x[-1], cum_b[-1]), xytext=(x[-1]+0.2, cum_b[-1]),
            fontsize=10, fontweight='bold', color=RED, va='center')
ax.annotate(f'£{cum_c[-1]:.0f}bn', xy=(x[-1], cum_c[-1]), xytext=(x[-1]+0.2, cum_c[-1]),
            fontsize=10, fontweight='bold', color=DARK_GREEN, va='center')

# Gap callout
gap = cum_b[-1] - cum_c[-1]
ax.annotate('', xy=(x[-1] - 0.3, cum_b[-1]), xytext=(x[-1] - 0.3, cum_c[-1]),
            arrowprops=dict(arrowstyle='<->', color='#444', lw=1.2))
ax.text(x[-1] - 0.55, (cum_b[-1] + cum_c[-1]) / 2, f'£{gap:.0f}bn\ngap',
        ha='right', va='center', fontsize=9.5, fontweight='bold', color='#444')

ax.set_xticks(x)
ax.set_xticklabels(quarters)
ax.set_xlabel('Quarter', fontsize=11)
ax.set_ylabel('Cumulative UK rent loss (£bn)', fontsize=11)
ax.set_title('Pre-registered cumulative loss through Q4 2027\nObservable gap = £18bn between policy and concessions',
             fontsize=12, fontweight='bold', pad=15)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'£{int(x)}bn'))
ax.set_xlim(-0.5, len(quarters) + 0.3)
ax.legend(loc='upper left', frameon=True, framealpha=0.95, fontsize=8.5)

fig.text(0.5, 0.02,
         "Pre-registered predictions: paper commits to recalibration after Q4 2027 outturns. Scenarios are conditional on observed UK policy choices through 2026–2027. "
         "Scenario A reflects current trajectory; Scenario B requires Stargate UK revival concessions; Scenario C requires DST + Sovereign AI Fund expansion + supply-side begins.",
         ha='center', fontsize=8.5, style='italic', color='#555555', wrap=True)
fig.subplots_adjust(bottom=0.14)

fig.savefig('figures/17_forward_predictions.png', dpi=150, bbox_inches='tight',
            facecolor='white', pad_inches=0.3)
plt.close(fig)
print('Saved figures/17_forward_predictions.png')
print(f'Final values: A=£{cum_a[-1]:.0f}bn, B=£{cum_b[-1]:.0f}bn, C=£{cum_c[-1]:.0f}bn')
