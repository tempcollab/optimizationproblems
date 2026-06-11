# Approach R3 — BMQS primal-measure LP-duality CEILING (lower bound diagnostic)

## Idea
Flammang's [F18] lower bound m* = 0.2487458 is the optimum of Smyth's semi-infinite LP
(the DUAL): maximize min over the contour of the auxiliary function
f(z) = sigma_ZZ(z) - sum_j c_j log|Q_j(z(1-z))|, c_j>=0, Q_j in Z[w], with the honest
density sigma_ZZ(z) = log max(1,|z|) + log max(1,|1-z|) [Flammang eq 2.1].

By LP strong duality (BMQS arXiv:2601.18978 framing; standard finite-LP duality after
discretization) this equals the PRIMAL measure-LP:
    m* = inf_mu  int sigma_ZZ dmu
         s.t.  mu a probability measure on the contour,
               int log|Q_j| dmu >= 0  for every column Q_j in the dictionary.

CEILING mechanism: ANY feasible primal probability measure mu_hat has
int sigma_ZZ dmu_hat >= m* = dual optimum. So C := int sigma_ZZ dmu_hat is a rigorous
UPPER bound (ceiling) on what any auxiliary function in the SPAN of these columns can
certify as a lower bound on C_82.

## What was done (R3)
- Reproduced the Flammang anchor as the PRIMAL LP optimum m_disc = 0.2487464260 (N=4000
  nodes, sigma_ZZ cost vector, 24 base columns) — matches the dual value, +6.3e-7 above
  the verified record 0.2487458 (pure discretization slack).
- Bred the full Z[w] dictionary by LLL to degree 40 against the primal optimal measure
  (276 distinct bred columns). NONE price in: min reduced cost = +4.8e-15 (LP noise).
  This is warrant (b): the dictionary is breeding-SATURATED (re-confirms R1 lll_breed
  and R2 screen_b_lobe_lll verified-negatives).
- Solved a margin-robustified weight LP over FIXED dyadic nodes t_k = n_k/2048 with
  int log|Q_j| dmu >= 8e-5 for all 300 columns; objective 0.24878.
- Rationalized to a genuine probability measure mu_hat: 25 dyadic nodes, integer weights
  / 100000 summing exactly to 1, all >= 0 (ceiling_muhat.json).
- INTERVAL-CERTIFIED (fastiv.py, outward rounding) that mu_hat satisfies
    (i)  int log|Q_j| dmu_hat >= 0 for EVERY one of the 300 columns
         (min interval-lower = +8.82e-5; worst col = Q_1 = w, the binding monomial),
    (ii) int sigma_ZZ dmu_hat <= 0.2487857 (interval upper = 0.2487856346).
  Hence C = 0.2487857 is a rigorous CEILING.

## Result
CERTIFIED ceiling C = 0.2487857 over the breeding-saturated Z[w] dictionary on the
honest sigma_ZZ contour. Only +4e-5 above Flammang 0.2487458 (the +4e-5 is the
deliberate feasibility margin baked into mu_hat so rationalization can't break a
constraint under interval rounding; the true primal optimum is ~0.2487464, +6e-7).

DECISION-RELEVANT READ: the lower bound is intrinsically STUCK near Flammang. No
auxiliary-function / contour argument over Z[w] can beat 0.2487858 materially. The only
way past this is a method engaging the conjugate measure nu's TRUE support — the
inner+outer |z(1-z)|=const lemniscate — NOT the circle |z|=1. This is exactly Angle 2 of
the outline, whose load-bearing "lifting term" is the barred OSS energy object; with only
Z[w] columns as the >=0 budget, min over the lemniscate region just relocates the binding
constraint back to the circle (R2: pure-w f plane-min 0.248751 ON the circle).

## Two-warrant scoping (load-bearing honesty)
The ceiling claim is a CONJUNCTION of two SEPARATE warrants:
  (a) [this build] mu_hat caps every auxiliary function in the SPAN of the {Q_j}
      actually in the dictionary. Fully rigorous (interval-checked feasibility).
  (b) [R1/R2 verified-negatives + this selftest] the dictionary is breeding-SATURATED:
      no new Z[w] column prices in below LP noise to deg ~40.
  Neither alone gives "no Z[w] auxiliary function beats C" — that needs BOTH. C is NOT a
  true upper bound on C_82 (the essential minimum); it is a cap on the METHOD over this
  dictionary+contour.

## Reproduce
    python3 constants/82a/certificate/ceiling_primal.py            # CERTIFIED 0.2487857
    python3 constants/82a/certificate/ceiling_primal.py selftest   # saturation + soundness
    python3 constants/82a/certificate/ceiling_primal.py tamper     # bogus inputs FAIL
Data: certificate/ceiling_muhat.json (mu_hat + the 300-column dictionary).

## What would push it further (and why it likely won't on the lower side)
- The ceiling proves the contour/Z[w] route is exhausted. Pushing the lower bound past
  0.2488 REQUIRES a fundamentally different >=0-droppable admissible term that is large
  off the circle (on the lemniscate) — and the only known candidate (OSS log-energy) is
  BARRED for ZZ (premise I(nu)>=0 fails for non-integer algebraic numbers; R1 retraction).
- A genuinely nonlinear coupling (second-moment energy) IS the barred OSS object (Angle 3
  collapses here). A linear coupling IS another Z[w] column, already in this saturated LP.
- Net: the lower side is method-stuck near Flammang. The pushable frontier is the UPPER
  side (held 0.2540419719, R11), but the user's standing focus is the lower bound — do
  not switch without a fresh user signal.
