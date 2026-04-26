"""
Monte Carlo simulation for UK AI externality model.
Run 10,000 trials drawing from parameter distributions, output percentiles.
"""
import numpy as np

np.random.seed(42)
N = 10000

# Parameter distributions (truncated normals)
def trunc_norm(mean, sd, lo, hi, n):
    """Truncated normal sampler."""
    samples = np.random.normal(mean, sd, n * 3)
    samples = samples[(samples >= lo) & (samples <= hi)]
    return samples[:n]

# λ central 0.85, range 0.78-0.92, sd ~0.035
lam = trunc_norm(0.85, 0.035, 0.78, 0.92, N)

# η productivity gap central 0.40, range 0.20-0.60, sd ~0.10
eta = trunc_norm(0.40, 0.10, 0.20, 0.60, N)

# η_reempl re-employment rate central 0.30, range 0.20-0.40, sd ~0.05
eta_reempl = trunc_norm(0.30, 0.05, 0.20, 0.40, N)

# Multiplier central 1.5, range 1.2-1.8, sd ~0.15
mult = trunc_norm(1.50, 0.15, 1.20, 1.80, N)

# Comp factor central 0.25, range 0.15-0.35, sd ~0.05
comp = trunc_norm(0.25, 0.05, 0.15, 0.35, N)

# MPC central 0.62, range 0.50-0.75, sd ~0.06
mpc = trunc_norm(0.62, 0.06, 0.50, 0.75, N)

# Discount rate central 0.04, range 0.025-0.06, sd ~0.008
disc = trunc_norm(0.04, 0.008, 0.025, 0.06, N)

# Component formula matched to spreadsheet engine:
# headline = (λ/0.85) × [137 + 95 + 17 + 105×(η/0.40)] + 44×(η_reempl/0.30)×(mult/1.5)×(1-comp+0.25) + 59×(0.04/disc)
# Adjusted to capture all parameter dependencies

C1 = 137 * (lam / 0.85)  # subscription
C2 = 95 * (lam / 0.85)   # cloud
C3 = 105 * (lam / 0.85) * (eta / 0.40)  # productivity rent
C4 = 44 * (eta_reempl / 0.30) * (mult / 1.50) * ((1 - comp) / 0.75) * (mpc / 0.62)
C5 = 17 * (lam / 0.85)   # HMRC
C6 = 59 * (0.04 / disc)  # forgone frontier (PV inverse)

headline = C1 + C2 + C3 + C4 + C5 + C6

# Percentiles
ptiles = [5, 25, 50, 75, 95]

print("="*70)
print(f"MONTE CARLO RESULTS (N={N:,})")
print("="*70)
print(f"\nHeadline (£bn):")
for p in ptiles:
    print(f"  P{p}: {np.percentile(headline, p):.1f}")
print(f"  Mean: {headline.mean():.1f}")
print(f"  SD:   {headline.std():.1f}")

# Cumulative 2024-30 ≈ headline × ~6.5x (cumulative factor for 7 years roughly)
# Actually paper says £461bn IS cumulative. So headline IS cumulative. Range aligns.

print(f"\nComponent percentiles (£bn):")
for name, comp_arr in [('C1 Subs', C1), ('C2 Cloud', C2), ('C3 Prod', C3),
                       ('C4 Displ', C4), ('C5 HMRC', C5), ('C6 Frontier', C6)]:
    print(f"  {name:12s}: P5={np.percentile(comp_arr,5):6.1f}  P50={np.percentile(comp_arr,50):6.1f}  P95={np.percentile(comp_arr,95):6.1f}")

# Range comparison to paper
p5 = np.percentile(headline, 5)
p95 = np.percentile(headline, 95)
print(f"\nP5-P95 range: {p5:.1f} to {p95:.1f}")
print(f"Paper claim (§5.4 cumulative): £283-658bn")
print(f"Δ: lower bound {abs(p5-283)/283*100:.1f}%, upper bound {abs(p95-658)/658*100:.1f}%")

# Save outputs for Phase 5 build
import json
results = {
    'N': N,
    'headline': {
        'P5': float(np.percentile(headline, 5)),
        'P25': float(np.percentile(headline, 25)),
        'P50': float(np.percentile(headline, 50)),
        'P75': float(np.percentile(headline, 75)),
        'P95': float(np.percentile(headline, 95)),
        'mean': float(headline.mean()),
        'sd': float(headline.std()),
    },
    'components': {}
}

for name, comp_arr in [('C1', C1), ('C2', C2), ('C3', C3),
                       ('C4', C4), ('C5', C5), ('C6', C6)]:
    results['components'][name] = {
        'P5': float(np.percentile(comp_arr, 5)),
        'P50': float(np.percentile(comp_arr, 50)),
        'P95': float(np.percentile(comp_arr, 95)),
        'mean': float(comp_arr.mean()),
        'sd': float(comp_arr.std()),
    }

with open('/home/claude/mc_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print("\nResults saved to /home/claude/mc_results.json")
