"""
Continuation: Get the (1 - 1/N) factor right.

The key insight: in HFT, firms compete in a symmetric Cournot-like equilibrium where
each firm's revenue depends on aggregate demand E. So firm i's PROFIT depends on E
(through its share E/N) AND on its own automation choice.

When firm i increases alpha_i, two effects:
1. Direct: cost saving s*L*alpha_i, friction (k/2)*L*alpha_i^2
2. Indirect: alpha_i changes E (the aggregate), which changes firm i's revenue E/N
   This is the demand-externality channel that PARTIALLY self-internalises.

The firm's PRIVATE problem:
  maximise: revenue - cost = E/N - C_i  
                            = E/N - [L(w - s*alpha_i) + (k/2)*L*alpha_i^2]

Taking dPi/d(alpha_i) holding other firms' alpha fixed:
  d(E/N)/d(alpha_i) = (1/N) * d(E)/d(alpha_i)
  
  d(E)/d(alpha_i) where ONLY firm i's alpha changes (others held fixed):
  Looking at E = A + rho*[w*L*N - (1-eta)*w*L*sum(alpha_j)] + rho*(1-lambda)*L*c*sum(alpha_j)
  d(E)/d(alpha_i) = -rho*(1-eta)*w*L + rho*(1-lambda)*L*c
                 = rho*L*[(1-lambda)*c - (1-eta)*w]

So firm i's private FOC includes (1/N) of this demand effect:
  dPi/d(alpha_i) = (1/N) * rho*L*[(1-lambda)*c - (1-eta)*w] + s*L - k*L*alpha_i = 0

In closed economy (lambda=0, eta=0):
  (1/N) * rho*L*(c - w) + s*L - k*L*alpha_i = 0
  -(1/N)*rho*L*s + s*L - k*L*alpha_i = 0
  alpha_i = s*(1 - rho/N) / k

Hmm, that's not s/k either. Let me check: HFT presumably has firms NOT internalising
their own demand effect at all in the basic version (myopic / atomistic). Then the
tax (1-1/N)*rho corrects for the (N-1)/N portion that would be borne by other firms.

Actually re-reading: in HFT the firm's revenue may not depend on E at all in the basic 
setup -- they might have constant demand at E_individual_firm regardless. Let me try 
that interpretation.

Setup: each firm has revenue function that depends on aggregate output not aggregate
spending. In that case the firm doesn't internalise E at all, and the social externality
is the full demand-multiplier impact spread across all N firms.

If firms are atomistic (don't internalise E), then:
  Private FOC: -L*s + k*L*alpha_i = 0  =>  alpha_i = s/k  ✓ matches paper

For the social planner:
  Total welfare = sum of firm profits + worker welfare 
  In symmetric equilibrium with all firms at alpha:
  W = N * (E/N) - N * C_i + worker welfare
    = E - N*C_i + (worker welfare term)
  
  But if E goes to firms (as revenue), and workers receive wages, then worker welfare
  is just w*L*(N - sum(alpha_j)) -- but actually displaced workers receive (1-eta)*w
  in transfers/lost income too. Let me ignore the welfare-of-workers component for
  now and focus on firm-side welfare (matching HFT's apparent setup).

W_firms = E - N*C_i (symmetric)
  = [A + rho*w*L*N - rho*(1-eta)*w*N*alpha*L + rho*(1-lambda)*N*alpha*L*c]
    - N*[L*(w - s*alpha) + (k/2)*L*alpha^2]
  
dW/d(alpha) (in symmetric equilibrium, all alpha move together):
  = [-rho*(1-eta)*w*N*L + rho*(1-lambda)*N*L*c] - N*[-L*s + k*L*alpha]
  = N*L*[-rho*(1-eta)*w + rho*(1-lambda)*c + s - k*alpha]

Setting = 0:
  k*alpha = s - rho*(1-eta)*w + rho*(1-lambda)*c

In closed economy (lambda=0, eta=0):
  k*alpha = s - rho*w + rho*c = s - rho*(w-c) = s - rho*s = s*(1-rho)
  alpha_social = s*(1-rho)/k

So my derivation DOES give s*(1-rho)/k for the social optimum, and the gap is rho*s/k,
giving Pigouvian tax tau = rho*s (per task) or rho (as rate on s).

NOT (1-1/N)*rho. Where does the (1-1/N) come from in HFT?

Hypothesis: HFT might be using a different specification where firms in the symmetric
equilibrium DO partially internalise the demand effect through a per-firm revenue share.
Let me try that.
"""

from sympy import symbols, diff, solve, simplify, expand, Rational

alpha, alpha_i, alpha_others = symbols('alpha alpha_i alpha_others', positive=True, real=True)
N, L, w, c, s, k, rho, eta, lam, A = symbols('N L w c s k rho eta lambda A', positive=True, real=True)
tau_a, tau_d, delta = symbols('tau_a tau_d delta', nonnegative=True)

# Setup with firm i optimising taking other firms' alpha as given
# Aggregate demand depends on sum of all alphas
# Sum of alpha_j = alpha_i + (N-1)*alpha_others

E_with_i = A + rho*(w*L*N - (1-eta)*w*L*(alpha_i + (N-1)*alpha_others)) + rho*(1-lam)*L*c*(alpha_i + (N-1)*alpha_others)

# Firm i's revenue = E/N (assuming firms split aggregate demand equally)
revenue_i = E_with_i / N

# Firm i's profit
C_i_w = L*(w - s*alpha_i) + (k/2)*L*alpha_i**2
profit_i = revenue_i - C_i_w

# Private FOC for firm i (holding alpha_others fixed)
foc_private = diff(profit_i, alpha_i)
print("Private FOC (firm i takes alpha_others as given, but DOES see E/N revenue):")
print(f"  d(profit_i)/d(alpha_i) = {simplify(foc_private)}")

alpha_priv_eq = solve(foc_private, alpha_i)[0]
# In symmetric equilibrium, alpha_i = alpha_others = alpha
alpha_priv_symmetric = simplify(alpha_priv_eq.subs(alpha_others, alpha_priv_eq))
# Self-consistent: alpha_i = alpha_priv_eq when alpha_others = alpha_i
# So just substitute back
alpha_priv = solve(alpha_i - alpha_priv_eq.subs(alpha_others, alpha_i), alpha_i)[0]
print(f"\nPrivate symmetric equilibrium: alpha = {simplify(alpha_priv)}")

# Closed economy
alpha_priv_closed = simplify(alpha_priv.subs([(lam, 0), (eta, 0), (w, s+c)]))
print(f"Closed economy (lambda=0, eta=0, w=s+c): alpha_priv = {alpha_priv_closed}")

# Now social planner's optimum -- maximises total welfare
# Total welfare = sum of profits = E - N*C_i (in symmetric eq)
W_total = E_with_i.subs(alpha_others, alpha_i) - N*C_i_w
# But this is "all firms at alpha_i" -- to get social planner, we need symmetric 
# substitute alpha_i = alpha (the aggregate choice variable)
W_total_sym = W_total.subs(alpha_i, alpha)
foc_social = diff(W_total_sym, alpha)
alpha_social = solve(foc_social, alpha)[0]
print(f"\nSocial planner FOC = 0 yields:")
print(f"  alpha_social = {simplify(alpha_social)}")

# Closed economy
alpha_social_closed = simplify(alpha_social.subs([(lam, 0), (eta, 0), (w, s+c)]))
print(f"Closed economy: alpha_social = {alpha_social_closed}")

# Gap
gap = simplify(alpha_priv_closed - alpha_social_closed)
print(f"\nGap (alpha_priv - alpha_social) in closed economy: {gap}")

# Pigouvian tax: tau such that (s - tau)/k = alpha_social, i.e., 
# but wait -- if firms partially internalise, the relationship isn't (s - tau)/k
# Let me redo. With the firm seeing E/N, the private FOC gives:
# alpha_priv = (s + (1/N)*rho*((1-lambda)*c - (1-eta)*w)) / k

# With a tax tau_a per task:
# Modified profit: revenue/N - C_i_w - tau_a*L*alpha_i
# FOC adds -tau_a*L
# alpha_priv(tau) = (s - tau_a + (1/N)*rho*((1-lambda)*c - (1-eta)*w)) / k

# To match alpha_social: 
# alpha_social = (s + rho*((1-lambda)*c - (1-eta)*w)) / k  [from above]
# Wait, let me recompute social.

print("\n" + "="*78)
print("CAREFUL RE-DERIVATION")
print("="*78)

# Step 1: aggregate E in symmetric equilibrium
E_sym = A + rho*(w*L*N - (1-eta)*w*L*N*alpha) + rho*(1-lam)*L*c*N*alpha

# Step 2: total firm cost
C_total_sym = N*(L*(w - s*alpha) + (k/2)*L*alpha**2)

# Step 3: total welfare = aggregate revenue (=E since symmetric) - total cost
# Actually, total welfare aggregating across firms = E - C_total
# Because each firm's profit = E/N - C_i, summed = E - sum(C_i) = E - N*C_i
W_total = E_sym - C_total_sym
W_total_simplified = expand(W_total)
print(f"\nTotal welfare (symmetric):\n  W = {W_total_simplified}")

# Social FOC
foc_W = diff(W_total, alpha)
print(f"\ndW/d(alpha) = {simplify(foc_W)}")
alpha_social_v2 = solve(foc_W, alpha)[0]
print(f"alpha_social = {simplify(alpha_social_v2)}")

# Closed economy:
alpha_social_v2_closed = simplify(alpha_social_v2.subs([(lam, 0), (eta, 0), (w, s+c)]))
print(f"Closed economy alpha_social = {alpha_social_v2_closed}")

# Now firm i's private FOC with E/N revenue (other firms held fixed):
# Revenue_i = E/N where E depends on sum(alpha_j)
# d(E)/d(alpha_i) = rho*L*[(1-lambda)*c - (1-eta)*w]  -- single firm changing alpha
# d(Revenue_i)/d(alpha_i) = (1/N) * d(E)/d(alpha_i)

# Firm i's marginal profit:
# = d(Rev_i)/d(alpha_i) - d(C_i)/d(alpha_i)
# = (1/N)*rho*L*[(1-lambda)*c - (1-eta)*w] - (-L*s + k*L*alpha_i)
# = (1/N)*rho*L*[(1-lambda)*c - (1-eta)*w] + L*s - k*L*alpha_i

# In symmetric equilibrium: alpha_i = alpha_priv
# Setting marginal profit = 0:
#   alpha_priv = [s + (1/N)*rho*((1-lambda)*c - (1-eta)*w)] / k

dEi_dai = rho*L*((1-lam)*c - (1-eta)*w)
foc_priv_v2 = (1/N)*dEi_dai + L*s - k*L*alpha
alpha_priv_v2 = solve(foc_priv_v2, alpha)[0]
print(f"\nPrivate alpha (with E/N internalisation): {simplify(alpha_priv_v2)}")

alpha_priv_v2_closed = simplify(alpha_priv_v2.subs([(lam, 0), (eta, 0), (w, s+c)]))
print(f"Closed economy alpha_priv = {alpha_priv_v2_closed}")

# Gap
gap_v2 = simplify(alpha_priv_v2_closed - alpha_social_v2_closed)
print(f"\nGap (priv - social) in closed economy: {gap_v2}")

# Pigouvian tax that closes gap (tax per unit alpha_i):
# Modified private FOC: (1/N)*dEi/dai + L*s - k*L*alpha_i - tau_a*L = 0
# alpha_priv(tau) = [s - tau_a + (1/N)*rho*((1-lambda)*c - (1-eta)*w)] / k
# Set = alpha_social
# tau_a = s - k*alpha_social + (1/N)*rho*((1-lambda)*c - (1-eta)*w)

# Let me solve directly: at what tau_a does alpha_priv(tau) = alpha_social?
tau_for_internalisation = solve(
    alpha_priv_v2.subs(s, s) - tau_a/k - alpha_social_v2,  # alpha_priv with tax = alpha_social
    tau_a
)
# Actually clearer: alpha_priv with tax = (s - tau_a + (1/N)*dEi/dai) / k
# Set equal to alpha_social = (s + dEi/dai) / k  (from full social planner)
# tau_a = (1 - 1/N)*dEi/dai 
# But dEi/dai = rho*L*[(1-lambda)*c - (1-eta)*w] which is NEGATIVE in closed economy
# So tau_a = -(1 - 1/N)*rho*L*s  which is negative??

# Wait. Let me recheck. The demand-externality is NEGATIVE: each firm's automation 
# REDUCES aggregate demand. The Pigouvian tax should be POSITIVE (discouraging too 
# much automation). Let's see.

# alpha_social = (s - rho*s) / k = (1-rho)*s/k    [closed economy, less than s/k]
# alpha_priv_v2 = (s - rho*s/N) / k = s*(1 - rho/N)/k    [closed, slightly less than s/k]
# 
# So alpha_priv_v2 > alpha_social: firms automate too much.
# Tax should reduce alpha_priv. With tax: alpha_priv(tau) = (s - tau - rho*s/N)/k
# Set equal to alpha_social = (1-rho)*s/k:
# s - tau - rho*s/N = s*(1-rho)
# tau = s - s*(1-rho) - rho*s/N = rho*s - rho*s/N = rho*s*(1 - 1/N)
# tau = (1 - 1/N)*rho*s   <-- THERE'S THE (1-1/N) FACTOR!

print("\n" + "*"*78)
print("RECOVERED THE (1 - 1/N)*rho RESULT!")
print("*"*78)

# Let me redo this cleanly
# Closed economy:
# alpha_priv (with E/N revenue, no tax) = s*(1 - rho/N)/k
# alpha_social = s*(1-rho)/k
# Pigouvian tax (closed economy) = (1 - 1/N)*rho*s   [as amount per task]
# As rate on s: tau/s = (1 - 1/N)*rho   [matches HFT]

print(f"\nClosed economy:")
print(f"  alpha_private (with E/N internalisation) = s*(1 - rho/N) / k")
print(f"  alpha_social                              = s*(1 - rho)   / k")
print(f"  Gap                                       = s*rho*(1 - 1/N) / k")
print(f"  Pigouvian tax per task (closed)           = (1 - 1/N)*rho*s")
print(f"  Pigouvian tax RATE on s (closed)          = (1 - 1/N)*rho   [matches HFT]")
print(f"\n  At UK parameters (N=50, rho=0.85): tau_rate = (1 - 1/50)*0.85 = {(1 - 1/50)*0.85:.4f}")
print(f"  As percentage of s: {(1 - 1/50)*0.85 * 100:.1f}%")

# Now open economy (lambda > 0):
# Marginal demand effect of firm i's alpha (with cross-border):
# dEi/dai = rho*L*[(1-lambda)*c - (1-eta)*w]

# Substituting w = s + c:
# dEi/dai = rho*L*[(1-lambda)*c - (1-eta)*(s+c)]
#         = rho*L*[c - lambda*c - s + eta*s - c + eta*c]
#         = rho*L*[-lambda*c - s + eta*s + eta*c]
#         = rho*L*[eta*(s+c) - s - lambda*c]
#         = -rho*L*[s + lambda*c - eta*(s+c)]
#         = -rho*L*[s*(1-eta) + c*(lambda - eta)]

# So with eta = 0:
# dEi/dai = -rho*L*[s + lambda*c] = -rho*L*s*[1 + lambda*c/s]

# alpha_social: dW/d(alpha) = 0 in symmetric eq
# W = E - N*C_i, dW/d(alpha) = dE/d(alpha) - N*dC/d(alpha_i)|_{alpha_i=alpha}
# dE/d(alpha) = N * dEi/dai (since dE_sym/d(alpha) accounts for all N firms moving)
# Wait no. dE/d(alpha) when alpha is the aggregate symmetric choice = N * dEi/dai
# 
# N * dEi/dai = -rho*L*N*[s*(1-eta) + c*(lambda - eta)]
# 
# dC_total/d(alpha) = N * (-L*s + k*L*alpha)
# 
# dW/d(alpha) = -rho*L*N*[s*(1-eta) + c*(lambda - eta)] - N*L*(-s + k*alpha) = 0
# Dividing by N*L:
# -rho*[s*(1-eta) + c*(lambda - eta)] + s - k*alpha = 0
# k*alpha = s - rho*s*(1-eta) - rho*c*(lambda - eta)
# alpha_social_open = [s*(1 - rho*(1-eta)) - rho*c*(lambda-eta)] / k
# 
# With eta=0:
# alpha_social_open = [s*(1-rho) - rho*c*lambda] / k

# alpha_private with cross-border (E/N internalisation):
# alpha_priv_open = [s + (1/N)*dEi/dai] / k
#                = [s - (1/N)*rho*L*(s + lambda*c)] / k    [eta=0]
#                = [s*(1 - rho/N) - (rho*lambda*c)/N] / k

# Gap (priv - social) [eta=0]:
# = [s*(1 - rho/N) - rho*lambda*c/N - s*(1-rho) + rho*lambda*c] / k
# = [s*rho - s*rho/N - rho*lambda*c/N + rho*lambda*c] / k
# = [rho*s*(1 - 1/N) + rho*lambda*c*(1 - 1/N)] / k
# = (1 - 1/N)*rho*[s + lambda*c] / k

# Pigouvian tax (per unit alpha) = (1-1/N)*rho*[s + lambda*c]
# As rate on s: tau/s = (1-1/N)*rho*[1 + lambda*c/s]
# 
# This is the COMBINED single-instrument tax for the open economy.
# It matches the paper's combined formula in spirit, but more clearly separates the components.

print("\n" + "="*78)
print("OPEN ECONOMY (lambda > 0, eta = 0)")
print("="*78)
print("\nMarginal demand effect of firm i's alpha:")
print("  dEi/dai = rho*L*[(1-lambda)*c - (1-eta)*w]  (general)")
print("          = -rho*L*(s + lambda*c)             (with eta=0, w=s+c)")
print("\nPrivate optimum (E/N internalisation):")
print("  alpha_priv = [s - (1/N)*rho*(s + lambda*c)] / k")
print("\nSocial optimum:")
print("  alpha_social = [s - rho*(s + lambda*c)] / k")
print("                = [(1-rho)*s - rho*lambda*c] / k")
print("\nGap = alpha_priv - alpha_social = (1 - 1/N)*rho*[s + lambda*c] / k")
print("\nCombined Pigouvian tax (single instrument, per task):")
print("  tau_a* = (1 - 1/N)*rho*[s + lambda*c]")
print("\nAs a rate on the cost saving s:")
print("  tau_a*/s = (1 - 1/N)*rho*[1 + lambda*c/s]")

# UK numerical values
N_val = 50
rho_val = 0.85
lam_val = 0.85
# c/s ratio: in the paper, AI per-task cost c is typically ~10-20% of wage w
# so c ~ 0.15*w and s = w-c ~ 0.85*w, giving c/s ~ 0.15/0.85 ~ 0.18
# This is highly assumed; actual c/s depends on automation maturity.
# Let me try a few values.
print("\n" + "-"*78)
print("UK numerical: tau_a*/s = (1 - 1/N)*rho*[1 + lambda*c/s]")
print("-"*78)
for c_over_s in [0.10, 0.15, 0.20, 0.30]:
    tau_rate = (1 - 1/N_val) * rho_val * (1 + lam_val * c_over_s)
    print(f"  c/s = {c_over_s:.2f}:  tau_a*/s = {tau_rate:.4f} = {tau_rate*100:.2f}%")
