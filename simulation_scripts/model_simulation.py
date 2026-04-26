"""
Full bottom-up simulation of the two-country AI Layoff Trap model.

Goals:
1. Set up the model from first principles (Hemenway-Falk-Tsoukalas 2026 + cross-border lambda)
2. Derive private and social FOCs symbolically and verify
3. Compute closed-economy Pigouvian tax (Prop 1)
4. Compute open-economy combined tax (Prop 2)
5. Compute optimal DST under endogenous avoidance (Prop 4 - rigorous)
6. Compute UK numerical results (Prop 5)
7. Verify the welfare arithmetic in Section 7.4 actually works
8. Verify the layoff trajectory across Sections 4.2, 7.1, 9.2 reconciles
9. Verify Component 1, 3, 4, 5, 6 numbers reconcile
10. Output the consistent set of numbers the paper should use
"""

import numpy as np
from sympy import symbols, diff, solve, simplify, Rational, expand, collect, Symbol, latex

# =============================================================================
# PART 1: Model setup and symbolic derivation
# =============================================================================

print("="*78)
print("PART 1: SYMBOLIC DERIVATION OF OPTIMAL TAXES")
print("="*78)

# Symbols
alpha, alpha_i, alpha_other = symbols('alpha alpha_i alpha_other', positive=True)
N, L, w, c, s, k, rho, eta, lam, A = symbols(
    'N L w c s k rho eta lambda A', positive=True
)
tau_a, tau_d, delta = symbols('tau_a tau_d delta', nonnegative=True)
beta_avoid = symbols('beta', positive=True)  # avoidance elasticity

# Cost saving per task
# s = w - c (defined; we treat s as a primitive parameter)

# -----------------------------------------------------------------------------
# Firm i's private cost function (closed-economy benchmark, no tax)
# -----------------------------------------------------------------------------
# Cost = wage bill on non-automated workers + AI cost on automated tasks + integration friction
C_private = L*(alpha_i*c + (1 - alpha_i)*w) + (k/2)*L*alpha_i**2

# Simplify: w(1-alpha) + c*alpha = w - alpha(w-c) = w - alpha*s
C_private_simplified = L*(w - alpha_i*s) + (k/2)*L*alpha_i**2

print("\nFirm cost function:")
print(f"  C_i = L(w - s*alpha_i) + (k/2)*L*alpha_i^2")
print(f"  where s = w - c (cost saving per automated task)")

# Private FOC: dC/dalpha_i = 0
foc_private = diff(C_private_simplified, alpha_i)
alpha_private = solve(foc_private, alpha_i)[0]
print(f"\nPrivate FOC: dC/d(alpha) = -L*s + k*L*alpha = 0")
print(f"Private optimum: alpha* = {alpha_private}  =  s/k")

# -----------------------------------------------------------------------------
# Aggregate demand E (with cross-border leakage)
# -----------------------------------------------------------------------------
# Symmetric equilibrium: all firms choose alpha
# E = A + rho*[wLN - (1-eta)*w*sum(alpha_j)*L] + rho*(1-lambda)*sum(alpha_j)*L*c
# In symmetric equilibrium sum(alpha_j) = N*alpha

E_aggregate = A + rho*(w*L*N - (1-eta)*w*N*alpha*L) + rho*(1-lam)*N*alpha*L*c
E_aggregate = expand(E_aggregate)
print(f"\nAggregate demand E (symmetric):")
print(f"  E = A + rho*w*L*N - rho*(1-eta)*w*N*L*alpha + rho*(1-lambda)*N*L*c*alpha")

# Simplify the alpha-dependent terms
dE_dalpha = diff(E_aggregate, alpha)
print(f"\ndE/d(alpha) = {dE_dalpha}")
print(f"  This is the marginal effect of one firm increasing alpha on aggregate demand")
print(f"  (multiplied by N because of symmetric equilibrium)")

# Per-firm demand effect (since each firm faces E/N revenue)
# Firm i's automation alpha_i changes E by: rho*L*[c*(1-lambda) - w*(1-eta)]
dE_dalpha_i = rho*L*((1-lam)*c - (1-eta)*w)
print(f"\nMarginal demand effect of firm i's automation:")
print(f"  dE/d(alpha_i) = rho*L*[(1-lambda)*c - (1-eta)*w]")
print(f"               = rho*L*[(1-lambda)*c - (1-eta)*w]")

# When lambda=0 and eta=0:
#   dE/d(alpha_i) = rho*L*(c - w) = -rho*L*s
# This matches Hemenway-Falk-Tsoukalas closed economy.

closed_check = dE_dalpha_i.subs([(lam, 0), (eta, 0)])
print(f"\nCheck: closed-economy benchmark (lambda=0, eta=0):")
print(f"  dE/d(alpha_i) = {simplify(closed_check)}")
print(f"  Expected: -rho*L*s = -rho*L*(w-c)")
print(f"  Verified: {simplify(closed_check - (-rho*L*(w-c)))} (should be 0)")

# -----------------------------------------------------------------------------
# Social planner's FOC
# -----------------------------------------------------------------------------
# Social welfare = firm surplus + worker income (incl. demand multiplier through E)
# When firm i automates one more unit:
#   - Captures cost saving s*L (private benefit)
#   - Imposes demand externality on other firms: 
#     other firms experience (N-1)/N of the demand effect
#   - Demand effect = rho*L*[(1-lambda)*c - (1-eta)*w]

# In the closed-economy benchmark (lambda=0, eta=0):
# demand effect = -rho*L*s
# Externality on others = (N-1)/N * rho*L*s (positive cost to others)
# Social marginal benefit = s*L - k*L*alpha - (N-1)/N * rho*L*s

# Setting social MB = 0:
# s - k*alpha - (1-1/N)*rho*s = 0
# alpha = s*(1 - (1-1/N)*rho) / k

# To match the proof's claim alpha_social = (1-rho)*s/k, we'd need (1-1/N)*rho ≈ rho
# That happens as N -> infinity. For finite N, the social optimum is:
#   alpha_social = s*(1 - (1-1/N)*rho) / k

print("\n" + "-"*78)
print("CLOSED-ECONOMY SOCIAL OPTIMUM (lambda=0, eta=0)")
print("-"*78)

# Per firm social cost = private cost + externality on others
# externality = -(N-1)/N * (demand effect on others) -- this is what firm i imposes
# In closed economy, demand effect of alpha_i = -rho*L*s*alpha_i (negative because demand falls)
# (N-1)/N of this falls on other firms
# So firm i imposes externality of magnitude (N-1)/N * rho*L*s*alpha_i on others (in welfare terms)

# Social welfare contribution of firm i's alpha_i:
# private firm surplus: s*L*alpha_i - (k/2)*L*alpha_i^2
# minus externality on (N-1) other firms:
#   each other firm sees demand fall by rho*L*s*alpha_i / N
#   each loses alpha_other share of that as revenue (in symmetric equilibrium)
# 
# Actually, the cleanest derivation: in HFT, the externality is that firm i's automation
# reduces demand for the sector good by (1-eta)*rho*w*L per unit alpha_i, and firm i 
# only internalises 1/N of this through its own E/N revenue share.
# The uninternalised portion is (1-1/N) * (1-eta)*rho*w*L per unit alpha_i.
# 
# Adding back the cross-border term: firm i's automation also reduces demand by 
# lambda*rho*c*L per unit alpha_i (the leaked AI subscription that doesn't recirculate).
# Closed economy (lambda=0): no cross-border component
# 
# Pigouvian tax to internalise: tau_a per unit alpha_i = (1-1/N)*(1-eta)*rho*w + (1-1/N)*lambda*rho*c
# Or as a rate on the cost saving s: tau_a / s

# Let me set this up properly with the planner's problem.

# In symmetric equilibrium, social welfare per firm:
# W_per_firm = revenue/N - cost = E/N - C_i
# where E depends on aggregate alpha

# Social planner chooses alpha to maximise total welfare = N * W_per_firm
# = E - sum(C_i) = E - N*C_i (symmetric)

# dW_total/d(alpha) where each firm chooses same alpha:
# = dE/d(alpha) - N * dC_i/d(alpha_i) (evaluated at symmetric alpha)
# = N * rho*L*[(1-lambda)*c - (1-eta)*w] - N*L*(-s + k*alpha)
# = N*L * [rho*(1-lambda)*c - rho*(1-eta)*w + s - k*alpha]

# Setting = 0:
# k*alpha = s + rho*(1-lambda)*c - rho*(1-eta)*w
#        = s + rho*(1-lambda)*c - rho*(1-eta)*(s+c)   [since w = s+c]
#        = s - rho*(1-eta)*s + rho*(1-lambda)*c - rho*(1-eta)*c
#        = s*(1 - rho*(1-eta)) + rho*c*[(1-lambda) - (1-eta)]
#        = s*(1 - rho*(1-eta)) + rho*c*(eta - lambda)

# Hmm, this gets messy because w and c are both primitive. Let me redo with w = s+c.

w_subbed = s + c  # since s = w - c
E_subbed = A + rho*((s+c)*L*N - (1-eta)*(s+c)*N*alpha*L) + rho*(1-lam)*N*alpha*L*c
E_subbed = expand(E_subbed)
dE_total_dalpha = diff(E_subbed, alpha)  # this is the TOTAL demand response in symmetric eq
dC_total_dalpha = N*diff(C_private_simplified.subs(w, s+c), alpha_i).subs(alpha_i, alpha)
# Using w = s + c
dW_total_dalpha = dE_total_dalpha - dC_total_dalpha
print(f"\nTotal welfare FOC (after setting w = s + c):")
print(f"  dW_total/d(alpha) = {simplify(dW_total_dalpha)}")
alpha_social = solve(dW_total_dalpha, alpha)[0]
alpha_social_simplified = simplify(alpha_social)
print(f"\n  alpha_social = {alpha_social_simplified}")

# Closed economy (lambda=0, eta=0):
alpha_social_closed = simplify(alpha_social.subs([(lam, 0), (eta, 0)]))
print(f"\nClosed economy (lambda=0, eta=0):")
print(f"  alpha_social = {alpha_social_closed}")

# Compare to private
alpha_priv_subbed = (s).subs(w, s+c) / k
print(f"  alpha_private = s/k = {s/k}")

# The gap
gap_closed = simplify(alpha_priv_subbed - alpha_social_closed)
print(f"  Gap (private - social) = {gap_closed}")

# Pigouvian tax to close gap: solve for tau_a such that 
# private FOC with tax = social optimum
# (s - tau_a)/k = alpha_social_closed
tau_pigou_closed = simplify(s - k*alpha_social_closed)
print(f"\n  Pigouvian tax (closed economy): tau_a* = {tau_pigou_closed}")
print(f"  This is the tax PER UNIT ALPHA (per task automated)")

# As a rate: tau_a / s
tau_rate_closed = simplify(tau_pigou_closed / s)
print(f"  As a rate on s: tau_a/s = {tau_rate_closed}")
# This should equal (1 - 1/N)*rho... wait, let's see.

print("\n" + "-"*78)
print("CHECKING: Does tau_pigou_closed match HFT's (1 - 1/N)*rho?")
print("-"*78)

# HFT's claim: tau* = (1 - 1/N)*rho  (interpreted as a rate on s)
# What we derived: tau_a* / s = ?
print(f"  Our derivation: tau_a / s = {tau_rate_closed}")
print(f"  HFT claim: (1 - 1/N)*rho = {1 - 1/N} * rho = {(1 - 1/N)*rho}")

# Hmm, our derivation might give rho * (something) without the (1-1/N) factor.
# Let me check more carefully.
