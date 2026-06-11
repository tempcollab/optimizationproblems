# Approach: LP column-generation / richer dictionary for new polynomials Q_j

Status: ATTEMPTED (round 1). NEGATIVE RESULT — no improving integer column found,
        no record break. Recorded honestly; logs no milestone by itself.
Moves: LOWER bound. Target: strictly > 0.24874.

## RESULT (round 1, proof-builder) — NO BREAK
Implemented in certificate/stageB_colgen.py and run on top of the certified Stage A.
1. Solved Smyth's semi-infinite LP (scipy linprog, HiGHS) at Flammang's 24-poly set
   on 6000-8000 control points: recovered m* = 0.2487464, matching the grid min and
   Flammang's 0.2487458. LP machinery validated.
2. Extracted the dual measure mu* (the HiGHS ineqlin marginals, normalized to a
   probability measure; support ~25 binding control points across the flat band).
3. Priced thousands of candidate INTEGER polynomials Q in w by reduced cost
   r(Q) = sum_n mu*_n log|Q(w(t_n))|: dictionaries = low-degree small-coeff integer
   polys (deg<=4), pairwise AND triple products of the existing Q_j (deg<=26), and
   single-coefficient +/-1 perturbations of each Q_j.
4. OUTCOME: the most-negative reduced cost was ~ -1e-7 (and most < -1e-8), at the
   level of control-point discretization noise. Adding the best candidate column and
   re-solving moved the LP optimum by ~2e-11 (0.2487464129 -> 0.2487464130) —
   negligible, not a real or certifiable gain.

## Why it stalled (the genuine bottleneck)
The reduced-cost / column-generation logic is sound (and non-circular, per the
outline review): if an improving integer column existed in the dictionary, pricing
against mu* would surface it. The dictionaries reachable cheaply (products,
perturbations, low degree) do NOT contain one — Flammang's set is effectively
LP-optimal over them. A genuine improvement needs columns that pricing CANNOT
cheaply generate: new integer polynomials of degree > 22 bred by Flammang's own
LLL / weighted-integer-transfinite-diameter recipe at search depth k>32 (where she
stopped). That breeding step — LLL on Re/Im of trial polynomial values at control
points near the active minima, for k from 5 to >32 — is the real, compute-heavy
search and is the concrete thing that would push m above 0.24874 in a future round.

## What would push it further (for the next round)
- Implement Flammang's LLL breeding (Section 2.3): for k = 24..40, minimize
  sup_t |Q(v)R(v)| exp(-(r+k)/(2t) log max(1,|v|)) over integer R via LLL on the
  Re/Im linear forms at control points v_n near the t≈0.577 active minimum and the
  other flat-band minima; keep factors R_j with nonzero c_j after re-optimizing the LP.
- Then re-certify the enlarged f with certificate/verify_vec.py (the Stage A machinery
  transfers directly — just extend flammang_table1.py with the new Q_j and re-run).

## Idea
The bound m = max over (c_j>=0) of [ min_t f ] is the optimum of a semi-infinite LP whose
COLUMNS are the candidate integer polynomials Q_j (each Q contributes the constraint-column
{-log|Q(w(t_n))|}_n with variable c_Q >= 0). Flammang's set is search-truncated at k<=32 and
her search direction was the weighted transfinite diameter only. The slack is entirely in
WHICH columns are present. Modern column generation chooses columns by reduced cost against
the current LP dual, which is precisely "the efficient criterion to find the optimal direction"
that BMQS say is missing.

## Skeleton
1. Reproduce the LP at Flammang's set (Angle 1 Stage A/B) to get the dual variables: the
   optimal LP has a measure mu* on the binding control points t_n (the dual of the
   semi-infinite LP is exactly BMQS's primal P(g): a probability measure with int log|Q| dmu* >= 0).
2. PRICING: for a large dictionary of candidate integer polynomials Q (degree up to ~24,
   bounded coefficients, e.g. products/perturbations of cyclotomic-in-w and the existing Q_j,
   plus LLL-bred candidates near the active minimum), compute the reduced cost
   r(Q) = int log|Q(w(t))| dmu*(t)  ( = sum_n mu*_n log|Q(w(t_n))| ).
   A column with r(Q) < 0 (i.e. mu* puts negative integral on it) can improve the bound:
   adding it tightens the dual / relaxes the binding constraint and raises m.
3. Add the few best-reduced-cost columns, re-solve the LP, iterate (standard column generation).
4. Stop when no integer Q in the dictionary has improving reduced cost, or m exceeds target.
5. Rigorously certify the final min (Angle 1's hard step machinery) before claiming the bound.

## Artifact
`certificate/colgen_search.py` (dictionary build + pricing + linprog loop) and the resulting
(Q_j, c_j) set, plus the branch-and-bound min-certificate for the final f.

## HARDEST step (named)
Finding integer polynomials Q with improving reduced cost that ALSO survive re-optimization
(get c_Q > 0) and genuinely raise m past 0.248746.
- Mechanism: column generation guarantees that if any improving column EXISTS in the dictionary
  it is found by pricing against mu*; the open question is whether the dictionary (bounded-degree
  bounded-coefficient integer polynomials in w) CONTAINS one. The integer constraint is the catch:
  the LP is over reals c_j but the columns must be integer polynomials, and the transfinite-diameter
  theory says good columns have coefficients growing with degree — so LLL on Re/Im at the control
  points (Flammang's construction) is the right generator, but it may reproduce her set without
  improving it.
- Why it might work past Flammang: she generated columns ONLY via transfinite diameter and stopped
  at compute limits (k<=32); pricing against the actual dual mu* is a sharper, cheaper criterion
  she did not use, so even within degree <=24 there may be unexploited improving columns.
- Risk: HIGH. May find no improving integer column (the gain Doche->Flammang was only 5e-4 after a
  big search). Fallback: even a null result that the current set is LP-optimal over a large
  dictionary is informative but logs no milestone by itself.

## Check the builder runs
Pricing values r(Q) for the added columns (must be negative), the re-solved LP's m, and the
rigorous min-certificate. Reviewer re-runs linprog and the certificate.

## Spec review: required
(Novel search criterion; it is NOT clear it can beat the record — the central feasibility
question "does an improving integer column exist within reach" is open. Worth an outline-reviewer
pass before the builder spends compute, but ONLY pursue after Angle 1 Stage A logs the safe milestone.)
