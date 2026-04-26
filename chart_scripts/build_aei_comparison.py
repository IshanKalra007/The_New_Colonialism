"""
Figure: AEI vs paper measurement framework comparison.
Two-column visual showing what the AEI (occupational headcount) measures
vs what this paper measures (cross-border rent flow), and why both findings
can be simultaneously correct.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import numpy as np

NAVY = '#1f3a5f'
BLUE = '#3a7ca5'
RED = '#c0392b'
ORANGE = '#e67e22'
GREEN = '#27ae60'
DARK_GREEN = '#16a085'
GREY = '#7f8c8d'

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 11,
    'figure.facecolor': 'white', 'axes.facecolor': 'white',
})

fig, ax = plt.subplots(figsize=(13, 7))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

ax.text(7, 9.5, 'AEI labour market analysis vs this paper: complementary, not contradictory',
        ha='center', fontsize=13, fontweight='bold', color='#222')

# === LEFT COLUMN: AEI ===
ax.add_patch(Rectangle((0.3, 1.0), 6.4, 8.0, facecolor='#eef4f9',
                        edgecolor=BLUE, linewidth=1.2, alpha=0.6))
ax.text(3.5, 8.6, 'Anthropic Economic Index',
        ha='center', fontsize=12, fontweight='bold', color=NAVY)
ax.text(3.5, 8.2, '(British Progress, 2026)',
        ha='center', fontsize=9, style='italic', color='#666')

# AEI: What it measures
ax.text(0.6, 7.6, 'What it measures:', ha='left', fontsize=10, fontweight='bold', color=NAVY)
ax.text(0.6, 7.15, '• Occupational headcount in 412 UK', ha='left', fontsize=9.5, color='#222')
ax.text(0.6, 6.85, '   occupations, rolling 12-month basis', ha='left', fontsize=9.5, color='#222')
ax.text(0.6, 6.55, '• AI-exposure scoring via Claude API', ha='left', fontsize=9.5, color='#222')
ax.text(0.6, 6.25, '   conversation analysis', ha='left', fontsize=9.5, color='#222')

# AEI: What it found
ax.text(0.6, 5.65, 'What it found:', ha='left', fontsize=10, fontweight='bold', color=NAVY)
ax.text(0.6, 5.20, '• AI-exposed occupations grew', ha='left', fontsize=9.5, color='#222')
ax.text(0.6, 4.90, '   marginally faster than unexposed', ha='left', fontsize=9.5, color='#222')
ax.text(0.6, 4.60, '• Sectoral reallocation suggested', ha='left', fontsize=9.5, color='#222')
ax.text(0.6, 4.30, '   absorbing displacement', ha='left', fontsize=9.5, color='#222')

# AEI: What it does NOT capture
ax.text(0.6, 3.70, 'What it cannot identify:', ha='left', fontsize=10, fontweight='bold', color=RED)
limitations = [
    '1. Same role, different worker (no net headcount change)',
    '2. Wage compression at the role level',
    '3. Persistent earnings losses for displaced workers (15–25%)',
    '4. Aggregate labour market signal (5% unemployment, vacancies)',
    '5. Cross-border rent flow (this paper\'s subject)',
]
for i, lim in enumerate(limitations):
    ax.text(0.6, 3.30 - i*0.32, lim, ha='left', fontsize=9, color='#222')

# === RIGHT COLUMN: This paper ===
ax.add_patch(Rectangle((7.3, 1.0), 6.4, 8.0, facecolor='#fef5f5',
                        edgecolor=RED, linewidth=1.2, alpha=0.6))
ax.text(10.5, 8.6, 'This paper',
        ha='center', fontsize=12, fontweight='bold', color=RED)
ax.text(10.5, 8.2, 'Cross-border rent flow framework',
        ha='center', fontsize=9, style='italic', color='#666')

# What we measure
ax.text(7.6, 7.6, 'What it measures:', ha='left', fontsize=10, fontweight='bold', color=RED)
ax.text(7.6, 7.15, '• UK→US AI subscription flow by provider', ha='left', fontsize=9.5, color='#222')
ax.text(7.6, 6.85, '• Five-channel UK domestic capture', ha='left', fontsize=9.5, color='#222')
ax.text(7.6, 6.55, '• Productivity rent transfer to US shareholders', ha='left', fontsize=9.5, color='#222')
ax.text(7.6, 6.25, '• HMRC tax loss; forgone capability', ha='left', fontsize=9.5, color='#222')

# What we found
ax.text(7.6, 5.65, 'What it found:', ha='left', fontsize=10, fontweight='bold', color=RED)
ax.text(7.6, 5.20, '• λ ≈ 0.85: 85p of every £1 paid leaks', ha='left', fontsize=9.5, color='#222')
ax.text(7.6, 4.90, '• £486bn cumulative through 2030', ha='left', fontsize=9.5, color='#222')
ax.text(7.6, 4.60, '• ~2.0% of cumulative UK nominal GDP', ha='left', fontsize=9.5, color='#222')
ax.text(7.6, 4.30, '• Rent flow operates regardless of headcount', ha='left', fontsize=9.5, color='#222')

# What we do NOT claim
ax.text(7.6, 3.70, 'What it does not claim:', ha='left', fontsize=10, fontweight='bold', color=NAVY)
not_claims = [
    '1. AI-attributable layoffs invalidate AEI growth',
    '2. UK labour market is collapsing in headcount terms',
    '3. Productivity gains are zero (we treat them separately)',
    '4. Reallocation is impossible at occupation level',
    '5. Reemployment cannot occur (we model η = 0.40)',
]
for i, nc in enumerate(not_claims):
    ax.text(7.6, 3.30 - i*0.32, nc, ha='left', fontsize=9, color='#222')

# === BOTTOM BAR: Reconciliation ===
ax.add_patch(Rectangle((0.3, 0.15), 13.4, 0.65, facecolor='#16a085', edgecolor='none'))
ax.text(7, 0.55, 'Reconciliation',
        ha='center', va='center', fontsize=11, color='white', fontweight='bold')
ax.text(7, 0.30, 'AEI tracks occupational reallocation; this paper tracks cross-border rent flow. These are independent phenomena — both can be true.',
        ha='center', va='center', fontsize=9, color='white', style='italic')

fig.subplots_adjust(left=0.02, right=0.98, top=0.96, bottom=0.04)

fig.savefig('figures/14_aei_comparison.png', dpi=150, bbox_inches='tight',
            facecolor='white', pad_inches=0.3)
plt.close(fig)
print('Saved figures/14_aei_comparison.png')
