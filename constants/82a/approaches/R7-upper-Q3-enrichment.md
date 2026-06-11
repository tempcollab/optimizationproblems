# R7 — UPPER bound: enrich Doche's perturbing dictionary with a free-exponent Q3

Approach (round 7, DEPTH). Build target = Angle 1 of `R7-structural-angles.md`,
with the five pinned gaps of `R7-outline-review.md` (Issues A-D + feasibility) honored.

Moves: UPPER bound. Held to beat (verified, R6): **certified 0.2543309112**
(float 0.2543308006). Goal: strictly below 0.2543309112.

## Idea

Doche's perturbing side (Doc01a, general `l`) is
`Q_{l+1} * prod_{m<=l} Q_m^{q_{k+m}}`, with
`D = 2b * max( sum_m q_m deg P_m , deg Q_{l+1} + sum_{m<=l} q_{k+m} deg Q_m )`.
The held R6 harness used `l=0`: the whole perturbing block is the FIXED distinguished
factor `Q_{l+1} = Q1*Q2` (deg 56, exponent 1). The untouched lever (structure report)
is to ADD a free-exponent block.

**Q3 = Qa** (Doc01a calibration perturber, deg 24 in X, ZZ-height H=1.290471208,
transcribed in `upper-bound-optimization.md` lines 36-38) enters as the single
free-exponent block `Q_1` (exponent `qB`), so

    B(t) = (1/2)log|Q1(w)|^2 + (1/2)log|Q2(w)|^2 + qB*(1/2)log|Q3(w)|^2
    D    = max( sum_i q_i deg P_i ,  56 + qB*24 ).

At `qB=0`: Q3^0=1 leaves the integrand unchanged and D's 2nd branch -> 56, so the
held R6 family is recovered EXACTLY. A descent from (R6 q, qB=0) can only go down.

## Issue A (load-bearing): Q3 is a FREE-exponent block; Q1*Q2 stays fixed.
Implemented exactly so. The B-branch weights Q3 by `qB` while Q1,Q2 keep weight 1;
D's second branch is `56 + qB*deg Q3`. At `qB=0` both reduce to the held family.
ANCHOR CHECK (verify_upper_q3.py anchor): `float_value_q3(R6 q, qB=0) = 0.2543308006`
matches `vu.float_value(R6 q) = 0.2543308006` to >=10 digits. PASS.

## Issue C: admissibility of the ENLARGED dictionary W = Q1*Q2*Q3 (sympy, exact).
`verify_upper_q3.py admiss` (and inside `certify`):
- deg Q3 = 24 > 0; Q3(0)=Q3(1)=1; Q3 squarefree (gcd(Q3,Q3')=1).
- deg W = 80; W(0)=W(1)=1  => X !| W and (1-X) !| W.
- gcd(Q3,P_i)=1 for all five P_i; gcd(Q3,Q1)=1; gcd(Q3,Q2)=1.
All Doche Lemma-5 hypotheses on the enlarged dictionary HOLD. Non-triviality
condition (4) holds: every factor is a monic non-constant integer polynomial, so any
non-trivial ratio `prod P^{n} / (Q1 Q2 Q3)^{n}` is a non-unit rational function,
never +/-1. PASS.

## Issue B: the harness was EDITED, not input-swapped; selftest re-run.
New module `verify_upper_q3.py` (imports `verify_upper as vu`, `verify_vec as vv`):
- `cell_AB_q3`: A-branch verbatim (P1..P8); B-branch now Q1,Q2 (weight 1) PLUS Q3
  (weight qB), each via `vu.rho_full` exactly as a P-factor in A (same outward-rounded
  midpoint value / slope / curvature / cell sup-inf of (1/2)log|.|^2).
- `cell_int_maxAB_q3`: identical straddle/flat/midpoint logic; only `cell_AB_q3` differs.
- `certify_maxAB_q3`: D = max(sum q_i deg P_i, 56 + qB*24).
- `selftest_q3`: mpmath prec-140 soundness on the CHANGED integrand (B includes
  qB*log|Q3|). 0/200 violations on BOTH flat and midpt branches. PASS.

## Issue D: calibration gate on the EDITED harness at qB=0.
Anchor (above) reproduces 0.2543308006 to >=10 digits BEFORE optimizing. PASS.

## Float optimization (6 exponents, seeded at R6 q with qB=0)
`optimize_q3.py` (Nelder-Mead multistart, seed includes the qB=0 anchor). The optimizer
immediately turns qB ON (qB ~ 0.129) and drops the float:

    candidate  q = (12.040, 9.380, 2.462, 1.711, 0.581),  qB = 0.129
    float log h (N=16e6) = 0.2543184416   (CONJECTURE)
    held R6 float        = 0.2543308006
    drop vs held float   = 1.236e-5   (>> the ~1.1e-7 certificate slack)

So the enlarged family's float optimum is ~1.24e-5 below the held value -- a strong
candidate for a certified break.

## Rigorous certificate (frontier=0, all outward-rounded)
`python3 verify_upper_q3.py certify 12.040 9.380 2.462 1.711 0.581 0.129 200000 14 1e-10`
runs admissibility (Issue C) + selftest_q3 (Issue B/D) + the max(A,B) outward-rounded
quadrature with adaptive bisection (leaf-only summation, frontier driven to 0).

CERTIFIED RESULT (cert_q3_R7.txt):
- admissibility (enlarged W): all Lemma-5 hypotheses hold.
- selftest_q3: 0/200 violations (flat) + 0/200 (midpt) on the CHANGED integrand.
- max(A,B) quadrature: frontier driven to 0 (637808 leaves, 6 refine rounds, 172s),
  int_0^2pi G dt <= 94.4313050433, int_0^1 G ds <= 15.0292089803, D = 59.096.
- **CERTIFIED  log h(q,qB) <= 0.2543185491**  (= 15.0292089803 / 59.096, by hand).
- held R6 certified = 0.2543309112  =>  STRICT RECORD BREAK, margin 1.236e-5.

D = 56 + qB*deg Q3 = 56 + 0.129*24 = 59.096 (the perturbing branch dominates, since
sum_i q_i deg P_i = 49.604 < 59.096) -- this is exactly Doche's `deg Q_{l+1} +
sum q_{k+m} deg Q_m` branch with the free Q3 block live.

## Result
NEW UPPER BOUND (certified, unverified-by-reviewer): C_82 <= 0.2543185491,
tightening the held 0.2543309112 by 1.236e-5. The Q3-enrichment lever WORKED on the
first hand-picked candidate (Qa).

REPRODUCE:
  python3 constants/82a/certificate/verify_upper_q3.py certify \
      12.040 9.380 2.462 1.711 0.581 0.129 200000 14 1e-10
(~3 min; prints admissibility + selftest_q3 0/200 + CERTIFIED 0.2543185491, frontier=0).
Anchor (Issue A/D): `verify_upper_q3.py anchor` -> qB=0 reproduces held 0.2543308006.

## What would push it further
- Q3=Qa worked; the lever is the DICTIONARY. Try a genuinely smaller-height block
  (Doche conjectures the ess min < log 1.2875274 = 0.25272; Qa's height 1.290471 is
  ABOVE the limit point, yet it still helped -- a smaller-height Q3 should help more).
- Add a SECOND free block (Qb, deg 24, the sibling of Qa) as `Q_2` -> 7 exponents;
  same harness pattern (append to `Bfactors` with its own weight, D's branch gains
  `qC*deg Qb`). Re-run anchor + selftest + admissibility for the larger W.
- The certificate slack here was 0.2543185491 - 0.2543184416(float) = 1.07e-7, in line
  with the documented ~1.1e-7 max(A,B) slack -- so the float optimum is the real lever;
  push the float lower with better Q3 candidates, not finer quadrature.

