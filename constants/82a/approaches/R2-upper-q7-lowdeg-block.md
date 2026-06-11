# R2 (this campaign) UPPER — add a NEW low-degree admissible block + joint re-optimize

Target to STRICTLY beat: **upper 0.2540419719** (R11 reviewer-verified, family
h = Q1*Q2*Q5^qE*Q6^qF, Q5=Flammang j13 deg12, Q6=Flammang j15 deg16, D=70.641076).

Status: **BUILDER CLAIM — CERTIFIED 0.2538925359 (Angle 2, A-branch j3 block),
strict beat margin +1.4944e-4** (awaiting reviewer verification; NOT yet written to
current.md held).

================================================================================

## Angle 1 (Q-side, B-branch) — DRY for every admissible low-degree block

Harness: `certificate/verify_upper_q7.py` (clone of verify_upper_q6.py, adds Q7 to
the B-branch with weight qG, extends D's SECOND argument by +qG*deg Q7).  Q7
selectable via env Q7_CAND.

- ANCHOR gate (qG=0): float, D, per-cell enclosure all BIT-IDENTICAL
  (np.array_equal True, float ==) to verify_upper_q6 at held R11 (q,qB=qC=0,qE,qF).
  Confirms Q7 genuinely extends the held family.

- ADMISSIBILITY (sympy) + JOINT float re-optimization (N=500k Riemann sum,
  Nelder-Mead multistart seeded at the R11 optimum with qG=0), candidate blocks
  from flammang_table1.py:

  | block | deg | admissible? | joint-opt qG | float min      | margin vs held |
  |-------|-----|-------------|--------------|----------------|----------------|
  | j3    | 3   | YES (full gcd grid =1) | ~0 (1.3e-13) | 0.2540418523 | +1.2e-7 (DRY) |
  | j5    | 4   | **NO** (gcd(j5,P4)≠1; j5 == P4) | n/a | (0.2517 below LB → invalid) | inadmissible |
  | j6    | 7   | YES | ~0 (2.6e-13) | 0.2540418523 | +1.2e-7 (DRY) |
  | j7    | 8   | YES | ~0 (2.7e-11) | 0.2540418523 | +1.2e-7 (DRY) |
  | j9    | 8   | YES | ~0 (3.0e-13) | 0.2540418523 | +1.2e-7 (DRY) |

  Note: j4 fails Q(0)=Q(1)=1 (gives -1) — skipped, as the spec predicted.
  Note: j5 IS the base poly P4 ([1,-2,4,-3,1]) re-labelled, hence not coprime to the
  base — its apparent "0.2517" float drop is an INADMISSIBLE configuration (and would
  sit below the verified lower bound 0.2524, an impossibility for a true upper bound),
  correctly caught by the admissibility gate.  Not a bound.

  **Verdict Angle 1: the held R11 family already saturates the active A<B band on the
  perturber side; every admissible low-degree B-branch block drives its joint-optimal
  exponent qG back to ~0 (the qG=0 anchor IS the optimum).  No B-branch break.**
  This matches the outline's predicted failure mode (the block adds depth only where
  A>B, G=A, no effect).  DEAD END for the B-branch — do not retry j3/j6/j7/j9 on the
  B-side.

================================================================================

## Angle 2 (A-side, base extension) — LIVE BREAK with j3

Harness: `certificate/verify_upper_q7A.py` (clone of verify_upper_q6.py, adds Q7 to
the **A-branch** prod-P^q side with weight qG, extends D's **FIRST** argument
sum q_i deg P_i by +qG*deg Q7).  This re-introduces a small-height integer polynomial
as a NEW BASE block, exactly the Doc01a §4 enlargement of the base set {P_m}
(condition (4): the integer-polynomial dictionary stays coprime/non-degenerate; a
BASE block need NOT satisfy P(0)=P(1)=1).  Q7 selectable via env Q7_CAND.

### Gates (all PASS for Q7 = j3, deg 3)
- ANCHOR (qG=0): BIT-IDENTICAL to verify_upper_q6 at held R11 — float ==
  (0.254041852337), D == (70.641076), per-cell enclosure np.array_equal True.
  Proves the A-branch harness genuinely extends the held R11 family (valid upper
  bound, not a broken integrand).
- ADMISSIBILITY (sympy): deg j3 = 3 > 0; j3 squarefree; gcd(j3, each base P_i)=1
  (base-side distinct); the LOAD-BEARING condition-(4) cross-coprimality
  gcd(j3,Q1)=gcd(j3,Q2)=gcd(j3,Q5)=gcd(j3,Q6)=1 (and gcd(j3,Qa)=gcd(j3,Qb)=1).
  So the active dictionary {P1,P2,P4,P6,P8,j3} (base) vs {Q1,Q2,Q5,Q6} (perturbers)
  is pairwise coprime ⇒ prod P^n / prod Q^n ≠ ±1 (Doche condition (4) holds).
- SELFTEST (mpmath prec-160, CHANGED integrand A has qG*log|j3|): 0/200 violations on
  BOTH caps; worst (cell_hi - true_int) = +3.31e-12 (flat) / +1.44e-17 (midpt) ≥ 0
  (the safe outward side).

### Joint float optimum (CONJECTURE)
Multistart Nelder-Mead over (q1..q5, qE, qF, qG), seeded at the R11 optimum with
qG=0, gave a STABLE drop to qG ≈ 0.8935 across all 6 starts:
  q = (14.283862, 13.947194, 2.593425, 2.283539, 0.249084), qB=qC=0,
  qE = 0.577911, qF = 0.565724, qG = 0.893516.
Float min log h (N=4M Riemann sum) = **0.2538923369** (h = 1.2890330155),
margin +1.496e-4 below the held 0.2540419719 — well above the 5e-6 safe cert margin.
[This is the float CONJECTURE; the rigorous value is the certified bound below.]

### CERTIFIED rigorous bound (the claim)
`python3 verify_upper_q7A.py certify 14.283862 13.947194 2.593425 2.283539 0.249084 0 0 0.577911 0.565724 0.893516 200000 14 1e-10`
(with `Q7_CAND=j3`):
  - CERTIFIED  log h ≤ **0.2538925359**  (h ≤ 1.28903...)
  - frontier FULLY RESOLVED: 0 unresolved cells, 741290 leaves, 6 refine rounds,
    ~589s.
  - int_0^2pi G dt ≤ 114.8367668786; int_0^1 G ds ≤ 18.2768390974;
    D = max(sum q_i deg P_i + qG*3, 56 + qE*12 + qF*16) = 71.986516
    (the A-branch sum-q-deg-P branch now wins: sum q_i deg P_i =
    14.283862*1+13.947194*1+2.593425*4+2.283539*8+0.249084*8 + 0.893516*3 ≈ 71.9865).
    Hand arithmetic: 18.2768390974 / 71.986516 = 0.253892535894.
  - BEATS held (strict, frontier=0): True; margin below held = +1.4944e-4.
  - Sits +0.0015 ABOVE the verified lower bound 0.2524001332 (consistency OK).
- TAMPER (bogus target 0.25389, BELOW the true certified 0.2538925359):
  see verify_upper_q7A.py tamper — expect BEATS=False (no grid fallback faking a
  proof).

### Why it works (mechanism)
The held R11 perturber side (Q1*Q2*Q5^qE*Q6^qF) was saturated, so no B-branch block
helped (Angle 1 dry).  But re-introducing the SMALLEST-degree small-height block j3
(deg 3) on the BASE side lets the whole q-vector REBALANCE: the qE,qF perturber
exponents drop (0.891→0.578, 0.247→0.566 shifts) while the base exponents and qG=0.89
shift the A-branch to raise A in the band where A>B at a low (deg-3) D-cost, lowering
the certified int G / D by ~1.5e-4.  This is the indirect q-rebalance lever the
outline named for Angle 2, and it is the same order as the R7/R9/R10 structural gains.

================================================================================

## What would push it further
- The A-branch break came from the LOWEST-degree block (j3, deg 3).  Re-run the
  Angle-2 A-branch joint optimization for the OTHER small-height base candidates
  (the genuinely DROPPED Doche base polys P3/P5/P7 from Doc01a's {P1..P8}, if their
  exact coefficients can be recovered from the Doc01a PDF — NOT in the current
  digests; j5 turned out to equal P4 so is not a new block).  A second admissible
  low-degree base block, jointly optimized on top of j3, could give a further drop.
- Try j3 AND a Q-side block re-optimized jointly (Angle1+Angle2 combined): now that
  the base has rebalanced, a perturber block that was dry against the OLD q might
  re-activate against the NEW q.
- Push the D-formula: the A-branch sum-q-deg-P branch now dominates (71.99 vs the
  perturb branch); rebalancing q to bring the two D-branches closer (the kink of the
  max) is the standard next squeeze.
