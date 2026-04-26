"""
Figure: Four-layer AI rent architecture.
Shows the four sequential layers of rent capture (chips, cloud, foundation models,
applications), with margin and US ownership concentration at each layer, and
indicators for where Sovereign AI (Pillar 2) sits vs where the upstream Layer 1-2
monopoly remains structurally unaddressed by any individual non-US economy.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
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
    'figure.facecolor': 'white', 'axes.facecolor': 'white',
})

fig, ax = plt.subplots(figsize=(13, 8))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

ax.text(7, 9.6, 'Four-layer AI rent architecture',
        ha='center', fontsize=14, fontweight='bold', color='#222')
ax.text(7, 9.15,
        'Each layer captures rent. Sovereign AI sits at Layer 4. Layers 1–3 remain US-controlled regardless.',
        ha='center', fontsize=10, style='italic', color='#666')

# Layer dimensions
layer_x = 1.0
layer_w = 7.5
layer_h = 1.6
gap = 0.2

# Layers from top (closest to user) to bottom (foundation)
layers = [
    {
        'name': 'Layer 4: Applications (SaaS)',
        'examples': 'Microsoft Copilot, Salesforce Agentforce, ChatGPT Enterprise',
        'margin': '~25–35% gross margin',
        'ownership': 'Mostly US-domiciled; some UK/EU/AU local apps',
        'sovereign_ai_here': True,
        'color': '#a8c5d8',
        'border': BLUE,
    },
    {
        'name': 'Layer 3: Foundation models',
        'examples': 'OpenAI GPT, Anthropic Claude, Google Gemini',
        'margin': '~50–70% gross margin (training amortised)',
        'ownership': '~95% US-controlled (OpenAI, Anthropic, Google, Meta, xAI)',
        'sovereign_ai_here': False,
        'color': '#fdeaa7',
        'border': ORANGE,
    },
    {
        'name': 'Layer 2: Cloud infrastructure (IaaS)',
        'examples': 'AWS, Microsoft Azure, Google Cloud Platform',
        'margin': '~35–45% operating margin',
        'ownership': '~65% global hyperscale = US firms',
        'sovereign_ai_here': False,
        'color': '#f5c6cb',
        'border': RED,
    },
    {
        'name': 'Layer 1: Semiconductor fabrication and design',
        'examples': 'NVIDIA (85% AI GPU), TSMC fabs, AMD, Intel, Broadcom',
        'margin': '~75–80% gross margin (NVIDIA datacenter)',
        'ownership': 'Design: ~95% US firms. Fab: TSMC (Taiwan) + Samsung (Korea)',
        'sovereign_ai_here': False,
        'color': '#d6c5e0',
        'border': '#7d3c98',
    },
]

# Draw layers from bottom up so visual hierarchy reads naturally
y_positions = [7.0, 5.2, 3.4, 1.6]

for layer, y in zip(layers, y_positions):
    # Layer box
    ax.add_patch(FancyBboxPatch((layer_x, y), layer_w, layer_h,
                                 boxstyle="round,pad=0.02",
                                 facecolor=layer['color'], edgecolor=layer['border'],
                                 linewidth=1.5))
    # Layer name (top-left)
    ax.text(layer_x + 0.2, y + layer_h - 0.3, layer['name'],
            fontsize=11, fontweight='bold', color=layer['border'])
    # Examples
    ax.text(layer_x + 0.2, y + layer_h - 0.65, layer['examples'],
            fontsize=9, color='#333')
    # Margin
    ax.text(layer_x + 0.2, y + 0.55, f"Margin: {layer['margin']}",
            fontsize=9, color='#222', fontweight='bold')
    # Ownership
    ax.text(layer_x + 0.2, y + 0.25, f"Ownership: {layer['ownership']}",
            fontsize=9, color='#222', style='italic')

    # Sovereign AI marker on Layer 4
    if layer['sovereign_ai_here']:
        ax.text(layer_x + layer_w - 0.3, y + layer_h - 0.4,
                '← UK Sovereign AI Fund\n   operates here',
                fontsize=9, color=DARK_GREEN, fontweight='bold', ha='right')

# Right side: rent flow arrow showing capture at each layer
right_x = 9.5
ax.text(right_x + 1.5, 9.0, 'Rent capture at each layer',
        ha='center', fontsize=11, fontweight='bold', color='#222')

# Vertical arrow showing rent flow upward (user payment flows down to capture at each layer)
arrow_payment = FancyArrowPatch((right_x + 1.5, 0.7), (right_x + 1.5, 8.5),
                                arrowstyle='<-', mutation_scale=20,
                                color='#444', lw=2)
ax.add_patch(arrow_payment)

# Label boxes at each layer level showing rent capture
captures = [
    (y_positions[0] + 0.8, '£1 user payment\nat Layer 4', '#666', BLUE),
    (y_positions[1] + 0.8, '~30p captured\nat Layer 3', ORANGE, ORANGE),
    (y_positions[2] + 0.8, '~25p captured\nat Layer 2', RED, RED),
    (y_positions[3] + 0.8, '~15p captured\nat Layer 1', '#7d3c98', '#7d3c98'),
]

for y_lvl, txt, txt_color, border in captures:
    ax.add_patch(FancyBboxPatch((right_x + 0.3, y_lvl - 0.45), 2.4, 0.9,
                                 boxstyle="round,pad=0.05",
                                 facecolor='white', edgecolor=border, linewidth=1.2))
    ax.text(right_x + 1.5, y_lvl, txt, ha='center', va='center',
            fontsize=9, fontweight='bold', color=txt_color)

# Bottom note box: implication for policy
ax.add_patch(Rectangle((0.5, 0.15), 13, 1.0, facecolor='#1a1a1a', edgecolor='none'))
ax.text(7, 0.85, 'Implication for policy:',
        ha='center', va='center', fontsize=10.5, color='white', fontweight='bold')
ax.text(7, 0.55,
        'Sovereign AI at Layer 4 redirects only ~30p of every £1, leaving 70p captured at Layers 1–3 regardless of UK firm ownership.',
        ha='center', va='center', fontsize=9, color='white')
ax.text(7, 0.30,
        'The Layer 1–2 monopoly is beyond what any individual non-US economy can close unilaterally; this paper does not propose a specific multilateral response.',
        ha='center', va='center', fontsize=8.5, color='#ffe4b5', style='italic')

fig.subplots_adjust(left=0.02, right=0.98, top=0.96, bottom=0.04)

fig.savefig('figures/19_four_layer_rent.png', dpi=150, bbox_inches='tight',
            facecolor='white', pad_inches=0.3)
plt.close(fig)
print('Saved figures/19_four_layer_rent.png')
