"""
Figure: Big Tech market capitalization vs nation-state GDP.
Shows the unprecedented private capital concentration: individual firms now
match or exceed the nominal GDP of major economies — a structural backdrop
that distinguishes the AI rent extraction from previous trade imbalances.
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from matplotlib.patches import Patch

NAVY = '#1f3a5f'
BLUE = '#3a7ca5'
LIGHT_BLUE = '#a8c5d8'
RED = '#c0392b'
ORANGE = '#e67e22'
GREEN = '#27ae60'
YELLOW = '#f1c40f'
GREY = '#7f8c8d'

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 11,
    'axes.titlesize': 13, 'axes.titleweight': 'bold',
    'axes.labelsize': 11, 'figure.facecolor': 'white',
    'axes.facecolor': 'white', 'axes.spines.top': False,
    'axes.spines.right': False, 'axes.grid': True,
    'axes.grid.axis': 'x', 'grid.alpha': 0.3, 'grid.linestyle': '--',
})

fig, axes = plt.subplots(1, 2, figsize=(13, 7.5), gridspec_kw={'width_ratios': [1.3, 1]})

# ============================================================
# LEFT: Mixed ranked list of firms and national GDPs
# ============================================================
ax = axes[0]

# Type: 'company' (red) or 'country' (navy) — values in $ trillion
# Market cap data as of 24-26 April 2026
data = [
    ('United States',      30.5, 'country'),
    ('China',              20.0, 'country'),
    ('NVIDIA',              5.0, 'company'),
    ('Germany',             4.7, 'country'),
    ('Japan',               4.4, 'country'),
    ('India',               4.3, 'country'),
    ('Apple',               3.9, 'company'),
    ('Alphabet',            3.9, 'company'),
    ('UK',                  3.6, 'country'),
    ('Microsoft',           3.5, 'company'),
    ('France',              3.3, 'country'),
    ('Amazon',              2.6, 'company'),
    ('Italy',               2.4, 'country'),
    ('Canada',              2.3, 'country'),
    ('TSMC',                2.0, 'company'),
    ('Meta',                1.7, 'company'),
]

# Sort descending
data_sorted = sorted(data, key=lambda x: -x[1])
labels = [d[0] for d in data_sorted]
values = [d[1] for d in data_sorted]
types = [d[2] for d in data_sorted]
colors = [RED if t == 'company' else NAVY for t in types]

y = np.arange(len(labels))
bars = ax.barh(y, values, color=colors, edgecolor='white', linewidth=0.5)
ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=10)
ax.invert_yaxis()

# Value labels
for i, (val, t) in enumerate(zip(values, types)):
    suffix = ' GDP' if t == 'country' else ''
    ax.text(val + 0.4, i, f'${val:.1f}T{suffix}', va='center',
            fontsize=9, fontweight='bold' if t == 'company' else 'normal',
            color=RED if t == 'company' else NAVY)

# Custom legend
legend_elements = [
    Patch(facecolor=RED, label='US Big Tech market cap'),
    Patch(facecolor=NAVY, label='National GDP (nominal)'),
]
ax.legend(handles=legend_elements, loc='lower right', frameon=True, framealpha=0.95)

ax.set_xlabel('US$ trillion', fontsize=11)
ax.set_title('Individual firms now sit alongside G20 economies\n(Market cap vs nominal GDP, April 2026)',
             fontsize=12, fontweight='bold', pad=15)
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${int(x)}T'))
ax.set_xlim(0, max(values) * 1.20)

# ============================================================
# RIGHT: Aggregate Big-6 vs combined major economies
# ============================================================
ax = axes[1]

# Aggregates
big6_total = 5.0 + 3.9 + 3.9 + 3.5 + 2.6 + 1.7  # NVDA, AAPL, GOOG, MSFT, AMZN, META
g7_minus_us = 4.7 + 4.4 + 3.6 + 3.3 + 2.4 + 2.3  # DE, JP, UK, FR, IT, CA

# Historical comparison anchors
eic_peak_relative = 0.15  # East India Company peak as fraction of UK GDP
uk_gdp = 3.6

categories = [
    'US Big 6\ntech firms',
    'G7 ex-US\n(combined GDP)',
    'UK\nGDP',
    'East India Co.\npeak (~1800)',
]
values_agg = [big6_total, g7_minus_us, uk_gdp, eic_peak_relative * uk_gdp]
colors_agg = [RED, NAVY, BLUE, GREY]

x = np.arange(len(categories))
bars = ax.bar(x, values_agg, color=colors_agg, edgecolor='white', linewidth=0.5, width=0.65)

for bar, val in zip(bars, values_agg):
    if val < 1:
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.5,
                f'~${val:.2f}T\n(0.15× UK GDP\nat peak)',
                ha='center', fontsize=9, fontweight='bold', color=GREY)
    else:
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.4,
                f'${val:.1f}T',
                ha='center', fontsize=10, fontweight='bold', color='#222')

# Annotation comparing scales
ax.annotate('', xy=(0, big6_total), xytext=(1, g7_minus_us),
            arrowprops=dict(arrowstyle='<->', color='#444', lw=1.2))
ax.text(0.5, max(big6_total, g7_minus_us) + 1, 'Comparable scale',
        ha='center', fontsize=9, fontweight='bold', color='#444',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#fffbe6',
                  edgecolor='#aaa', linewidth=0.8))

ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=9)
ax.set_ylabel('US$ trillion', fontsize=11)
ax.set_title('Aggregate concentration is unprecedented\n(Big 6 ≈ G7 ex-US combined)',
             fontsize=12, fontweight='bold', pad=15)
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${int(x)}T'))
ax.set_ylim(0, max(values_agg) * 1.30)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.grid(axis='x', visible=False)

fig.text(0.5, 0.02,
         "Sources: CompaniesMarketCap (April 2026); IMF World Economic Outlook (October 2025) for nominal GDP. "
         "East India Company peak market cap relative to UK GDP from Global Financial Data (Bryan Taylor, Finaeon) — "
         "the EIC at peak was approximately 0.15× UK GDP, far smaller relative to host economy than today's Big Tech firms.",
         ha='center', fontsize=8.5, style='italic', color='#555555', wrap=True)
fig.subplots_adjust(bottom=0.13)

fig.savefig('figures/18_marketcap_vs_gdp.png', dpi=150, bbox_inches='tight',
            facecolor='white', pad_inches=0.3)
plt.close(fig)
print('Saved figures/18_marketcap_vs_gdp.png')
print(f'Big 6 total: ${big6_total:.1f}T  vs  G7 ex-US combined: ${g7_minus_us:.1f}T')
