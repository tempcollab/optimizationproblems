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

================================================================================

## R4 explorer — admissibility table of UNUSED low-degree A-base candidates

Active dictionary after R2: base {P1,P2,P4,P6,P8,j3} | perturbers {Q1,Q2,Q5=j13,Q6=j15}.
Cross-checked Flammang Table-1 blocks NOT yet used, for use as a NEW A-BASE block
(sympy, R4). A-base does NOT require P(0)=P(1)=1; it requires deg>0, squarefree,
coprime to every active poly (condition (4)).

| cand | deg | P(0),P(1) | coprime to active | sqfree | admissible as A-base |
|------|-----|-----------|-------------------|--------|----------------------|
| j6   | 7   | 1,1       | YES               | yes    | **YES**  (best next: lowest new deg) |
| j7   | 8   | 1,1       | YES               | yes    | YES |
| j9   | 8   | 1,1       | YES               | yes    | YES |
| j11  | 11  | 1,1       | YES               | yes    | YES |
| j8   | 8   | 1,1       | NO (shares factor w/ P6/P8) | yes | NO |
| j12  | 12  | 1,1       | NO (shares factor w/ Q5=j13)| yes | NO |

NEXT LEVER (R4 recommendation): clone verify_upper_q7A.py, add **j6 (deg7)** as a
SECOND new A-base block (exponent qH), extend the FIRST D-argument by +qH*7, add
qH*(1/2)log|j6|^2 to A; joint Nelder-Mead multistart over (q1..q5,qE,qF,qG_j3,qH_j6)
seeded at the R2 optimum with qH=0. Make-or-break risk: qH may saturate to ~0 like the
B-branch did (A-base may already be near-saturated after j3) — outline-check the joint
FLOAT drop > 5e-6 BEFORE the ~8 min certify run. B-branch blocks remain DRY (R2 Angle-1).

================================================================================

## R4 proof-outliner — joint FLOAT screen of a SECOND A-base block (pre-certify gate)

The R4 explorer's lead candidate was j6 (deg 7) as a SECOND A-base block. I ran the
mandatory pre-certify FLOAT gate (joint Nelder-Mead multistart over (q1..q5,qE,qF,
qG_j3,qH_block) seeded at the R2 optimum with the new exponent =0), then re-evaluated
each optimum at N=4M to remove Riemann-grid discretization noise (j9 has roots near
the lemniscate, so low-N float is unreliable — a 250k-grid "drop" for j9 evaporated to
0.25404 at a stale seed; the GENUINE joint optimum is stable across N=400k and N=4M).

| 2nd A-base block | deg | joint-opt qH | float val (stable N=4M) | margin vs cert 0.2538925359 | verdict |
|------------------|-----|--------------|-------------------------|------------------------------|---------|
| j6 | 7 | 0.000 (saturates) | 0.2538923368 | +1.99e-7 | **DRY** (qH->0; = R2 value) |
| j7 | 8 | 0.000 (saturates) | 0.2538923368 | +1.99e-7 | **DRY** (qH->0; = R2 value) |
| **j9** | 8 | **0.0662 (ACTIVE)** | **0.2538891103** | **+3.43e-6** | **LIVE but THIN** |

- **j6/j7 are DRY as a second A-base block** — exactly the explorer's predicted make-or-
  break failure: the A-base is near-saturated after j3, the new exponent collapses to 0,
  the qH=0 anchor IS the optimum (same dry mode as the B-branch in R2 Angle 1). Do NOT
  certify j6 or j7 as a second A-base block; the float does not drop.
- **j9 (deg 8) GENUINELY ACTIVATES**: qH=0.0662 (NOT 0 — dropping it, qH=0, gives a much
  worse 0.2539669816), float val 0.2538891103 STABLE at N=4M. So j9 is structurally
  different from j6/j7: it carves a small extra notch in the A>B band that j3 alone
  doesn't reach. But the float drop is only **+3.43e-6 below the held cert** — BELOW the
  ~5e-6 safe-cert margin. The certificate is an UPWARD enclosure (cert > float by ~1e-7..
  1e-6 of B&B/outward-rounding slack), so a 3.43e-6 float drop may certify to ~0.2538895..
  0.2538905 — a strict beat of 0.2538925359 by only ~2e-6..3e-6, RIGHT AT the slack edge.
  Plausibly a real (thin) record break, but NOT a safe one — the build must first push the
  float margin or accept the risk that the certified value lands above the held value.

Reliable joint optimum for j9 (N=4M-confirmed, for the builder to seed the certify):
  base q=(14.283862,13.947194,2.593425,2.283539,0.249084) [R2 values; co-opt may shift],
  qE~0.578, qF~0.566, qG_j3~0.8935, qH_j9~0.0662  (re-tighten at higher N before certify).

NEXT-LEVER ranking (R4):
  1. **j9 as a second A-base block** — the only LIVE candidate; +3.43e-6 float, thin.
     Worth a certify ONLY after tightening the float margin (finer joint opt + higher-N
     re-check) to confirm it clears the held value by more than the cert slack. If the
     tightened float margin stays < ~4e-6, the expected certified value is too close to
     the held 0.2538925359 to be a SAFE strict beat — treat as high-risk.
  2. j6/j7 second A-base block — DRY, do not certify.
  3. D-kink rebalance of the held j3 family alone — float reopt did not drop below the
     R2 value (seed already at the kink optimum); no gain without a new block.

================================================================================

## R4 proof-builder — BUILT & CERTIFIED: j9 as a SECOND A-base block (LIVE BREAK)

Harness: `certificate/verify_upper_q8A.py` (clone of verify_upper_q7A.py; adds Q8 = j9
on the **A-branch** with weight qH, extends D's FIRST argument by +qH*deg j9 = +qH*8,
adds qH*(1/2)log|j9|^2 to A; comparison target SET to the CURRENT held 0.2538925359,
NOT the stale R11 0.2540419719). New scratch optimizer `opt_q8_scratch.py`.

**Status: BUILDER CLAIM — CERTIFIED 0.2538893183, strict beat of held R2 0.2538925359,
margin +3.218e-6** (awaiting reviewer verification; NOT written to current.md held).

### Admissibility (sympy, from scratch) — PASS
j9 = X^8 - X^7 - 3X^5 + 15X^4 - 22X^3 + 16X^2 - 6X + 1 (descending [1,-1,0,-3,15,-22,
16,-6,1], deg 8) matches flammang_table1.py j=9 exactly. squarefree, IRREDUCIBLE,
distinct from j3, gcd(j3,j9)=1, gcd(j9, each of {P1,P2,P4,P6,P8,Q1,Q2,Q5,Q6})=1, and
j3 still coprime to all perturbers. Condition (4) holds (full coprimality + the
always-present deg-56 Q1*Q2 factor => prod P^n / prod Q^n != +-1). A-base does NOT
require j9(0)=j9(1)=1 (it happens to, but irrelevant).

### ANCHOR (qH=0) — PASS, bit-identical
float_value_q8A(R2 q,qE,qF,qG, qH=0) = 0.253892336877 == float_value_q7A(...) (== True);
D_q8A(qH=0)=71.986516 == D_q7A; per-cell enclosure np.array_equal True AND refine-mask
match True. Proves the second A-block genuinely EXTENDS the held R2 cert (valid integrand).

### Joint 9-exponent float re-optimization (N=80k opt, N=4M re-eval) — GATE PASS
3 Nelder-Mead starts seeded at R2 q + qH=0.0662, all converge to the SAME basin:
  start0: 0.2538891350 (qH=0.0695)   start1: 0.2538892584 (qH=0.0527)
  start2: 0.2538891202 (qH=0.0669)  <- best, used to certify
Best (rounded) vector q=(14.0115,13.44393,2.64359,2.29988,0.25242), qE=0.57508,
qF=0.56880, qG=0.89159, qH=0.06686; float N=4M = 0.2538891201, margin +3.416e-6 below
held, STABLE (80k vs 4M differ ~5e-10). qH active (NOT 0): forcing qH=0 recovers the R2
value. ~17x the harness's observed cert slack (~2e-7) -> SAFE beat.

### selftest (mpmath prec-160, CHANGED A-integrand with qG*log|j3|+qH*log|j9|) — PASS
0/200 violations on BOTH caps; worst (cell_hi - true_int) = +3.309e-12 (flat) /
+1.441e-17 (midpt) >= 0 (safe outward side).

### CERTIFIED rigorous bound (the claim)
`python3 verify_upper_q8A.py certify 14.011500 13.443930 2.643590 2.299880 0.252420 0 0
 0.575080 0.568800 0.891590 0.066860 200000 14 1e-10`:
  - CERTIFIED  log h <= **0.2538893183**
  - frontier FULLY RESOLVED: 0 unresolved, 742266 leaves, 6 rounds, ~437s
  - int_0^2pi G dt <= 114.8596292764; int_0^1 G ds <= 18.2804777610;
    D = max(61.65784, 72.00176) = 72.00176 (the PERTURBER B-branch 56+qE*12+qF*16 WINS;
    the A-branch sum-q-deg-P+qG*3+qH*8 = 61.65784 does NOT — watch the report mislabel).
    Hand arithmetic 18.2804777610 / 72.00176 = 0.253889318275.
  - BEATS held 0.2538925359 (strict, frontier=0): True; margin +3.2176e-6.
  - cert (0.2538893183) - independent N=4M float (0.2538891201) slack = +1.98e-7
    (squarely in the harness's logged ~1.2e-7..2.0e-7 band — confirms a SAFE beat).
  - Sits +0.00149 ABOVE the verified lower bound 0.2524001332 (two-sided consistent).

### TAMPER — PASS
bogus target 0.2538893100 (below the true certified 0.2538893183) -> BEATS=False,
frontier fully resolved (no grid fallback). Same value 0.2538893183 reproduced
deterministically.

### Why j9 works where j6/j7 are DRY (mechanism)
The A-base after j3 alone is nearly saturated, so j6/j7 (deg 7,8) drive qH->0 (DRY,
recover R2). j9 (deg 8) has roots near the lemniscate (min|j9(X(t))| ~ 0.0106) so its
log|j9| dips deeply in a narrow band; that extra A-mass carves a notch in a sub-band of
{A>B} that j3 alone underfills, making qH=0.067>0 a genuine interior optimum and the
whole q-vector rebalance. The gain is small (+3.2e-6) because the base is already
nearly saturated after j3.

### What would push it further
- A THIRD A-base block: the next admissible low-deg Flammang block with lemniscate-near
  roots (the property that made j9 live vs DRY j6/j7) — screen for min|Q| dips, not just
  low degree. j11 (deg 11) is admissible but its +qH*11 D-penalty makes it a long shot.
- Now that the B-branch D-arg (72.00176) again strictly wins the D-kink, a perturber
  block that re-balances the two D-args (bring 61.66 closer to 72.00) is the standard
  squeeze; but the A-branch is far below, so a new A-base block is the more direct lever.
- Returns are clearly diminishing: R2 j3 gave +1.49e-4, R4 j9 only +3.2e-6.
