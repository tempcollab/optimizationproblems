# 82a UPPER — R1 ranked attack angles to push below 0.2540419719

Outliner, round 1 (this campaign). Target to STRICTLY beat: **upper 0.2540419719**
(R11 reviewer-verified, h = Q1·Q2·Q5^qE·Q6^qF, Q5=Flammang j13 deg12, Q6=Flammang j15
deg16; D=70.641076). Moving the UPPER bound. Lower side is being pushed separately
(held 0.2524001332, gap to upper now ~0.00164).

Spec review: not required  (top angle is the proven R5–R11 dictionary-enrichment lever
on the already-verified `verify_upper_q*.py` harness; validity is the SAME Doc01a
Lemma-5 / condition-(4) admissibility check, re-run for one new low-degree block. No new
measure-theoretic claim. Promote to `required` ONLY if Angle 1 falls back to a bred /
LLL block whose admissibility or smallness rests on a non-obvious construction.)

Read of the slack before ranking (load-bearing for the ranking):
- The R5→R11 margins were 1.04e-4, 1.78e-6, 1.24e-5, 5.28e-5, 2.02e-4, 2.20e-5 — i.e.
  the BIG jumps (R5 first break, R10 +2.0e-4) came from a genuinely NEW kind of block
  (q-tuning R6 was 1.8e-6; the structural R7/R10 adds were the wins). Pure q-tuning of
  the held family is dry.
- The Flammang Table-1 well is nearly drained: of 18 admissible Q_j only j13, j15
  cleared the cert slack; the runner-up j19 gives ~1.8e-6 (BELOW the ~1e-7…1e-6 cert
  slack is borderline — not a safe break). So "add another Flammang block" alone is
  unlikely to clear a strict break this round.
- THE structural signal (from upper_q5_block.md notes): j13 (deg 12) dominated the
  deg-24 Qa,Qb because the D-formula penalizes a block by deg(block) in the denominator
  — "each unit of qE costs only 12 in D" vs 24. **Lower-degree small-height blocks are
  the sweet spot and are UNDER-explored.** The whole Flammang screen only tested blocks
  against a FROZEN q with single-block additions; a low-degree block in a JOINT
  re-optimization is the untested lever.

Note on the BMQS Thm 4.5 μ_{P,Q} family (this round's explorer): the bare single-pair
pushforward sits at 0.34–0.69 for low degree and has no efficient high-degree search
direction — NOT a standalone route (explorer verdict, confirmed). Its only live value is
as the Remark-4.6 weighted recast of the Doche family, captured as Angle 3 below.

================================================================================

## Angle 1 (TOP PICK): add ONE low-degree admissible block + JOINT re-optimization
### exploiting the deg-penalty asymmetry the R10/R11 wins revealed

Moves: UPPER bound, aiming for < 0.2540419719 (realistic reach ~0.25400–0.25403, a
~1e-5…4e-5 break; the same order as R7/R9/R11 structural adds).

Why it can beat the record (the mechanism, not a hope): the D denominator charges
deg(block)·q_block for every perturber. The held family spends its perturbation budget
on Q5 (deg 12) and Q6 (deg 16). A *lower-degree* admissible small-height block (deg ≤ 8)
contributes -log|Q_new| depth in the band where A<B at HALF or a THIRD the D-cost of Q5.
Adding it as a new free-exponent block STRICTLY enlarges the family (seed its exponent
=0 recovers the held cert exactly), so the joint optimum can only go down; the only way
it stays put is if the block's roots are orthogonal to the active band. The
under-explored low-degree admissible candidates are exactly the ones the frozen-q single
-block screen could not see.

Specific candidates to test, in order (all already on disk, all in X=z(1-z)):
  (a) **Flammang j3** (deg 3): w^3+w^2-2w+1, c=0.00121 — admissible (passed self-screen),
      lowest-degree nontrivial block, never tried as a free block. Deg-3 cost in D.
  (b) **Flammang j4** (deg 3): w^3-4w^2+3w-1 — NOTE check Q(0)=−1, may fail the Q(0)=1
      normalization gate; if so SKIP (it was among j=1,2,4 failing normalization — the
      builder must re-run the admiss gate, do NOT assume).
  (c) **Flammang j6 (deg 7), j7 (deg 8), j9 (deg 8), j11 (deg 11)** — all on the 18-
      admissible list, all deg < 12, none cleared the FROZEN-q screen but were never put
      through a JOINT re-optimization with q,qE,qF all free. Test j6/j7 next.
  (d) The base polys **P3, P5, P7** that Doche DROPPED from {P1..P8}: re-introduce one as
      a free block in the A-branch (prod-P^q side). Doche's selection was "forced by the
      search"; with the enriched Q5,Q6 perturbers present, a dropped P_m may now help.
      (Different branch — see Angle 2; listed here as the cheapest variant.)

Skeleton:
  1. Recover the held R11 family and reproduce its float (0.25404185) at the held
     (q,qE,qF) with the new block's exponent = 0 — the CALIBRATION GATE. — by reading
     verify_upper_q6.py + one float eval.
  2. Pick block Q7 from the ordered candidate list (a)→(d). Run the Doc01a Lemma-5 /
     condition-(4) admissibility gate on the enlarged dictionary W = Q1·Q2·Q5·Q6·Q7:
     deg Q7>0, Q7(0)=Q7(1)=1, Q7 squarefree, gcd(Q7, each kept factor incl. the
     load-bearing inter-block gcd(Q7,Q5)=gcd(Q7,Q6)=1). — by the existing `admiss`
     routine, extended (sympy).
  3. JOINT re-optimize ALL exponents (q1..q5, qE, qF, and the new qG≥0) by multistart
     L-BFGS / Nelder-Mead, seeded at the R11 optimum with qG=0 (recovers held exactly).
     Report the float min as a CONJECTURE. — by scipy on the float Riemann sum.
  4. IF the float min is below 0.2540419719 by a margin ≫ cert slack (target ≥ 5e-6 to be
     safe): certify with the EXTENDED outward-rounded max(A,B) quadrature, frontier fully
     resolved. The bound is automatic for any admissible q (no optimality burden,
     Doc01a Lemmas 2–5). — by the in-hand harness.

Hard step: **producing a block whose JOINT optimum strictly drops the integral past a
safe margin (≥5e-6) below 0.2540419719.** Mechanism it works: enlarging the family is
monotone-down, and a low-degree block has a small D-penalty so its optimal exponent can
be large and effective in the A<B band — the same reason j13 (deg 12) beat the deg-24
Qa,Qb by ~2e-4. Mechanism it can fail: the held family may already capture the active
band's depth, so a low-degree block adds depth only where A>B (G=A, no effect) → float
doesn't drop and the round banks only a re-certification + a narrowed dictionary. The
diminishing R11 margin (2.2e-5) warns the remaining slack in the Flammang dictionary is
thin — hence the deg-3 (j3) and dropped-P (P3/P5/P7) candidates, which are OUTSIDE the
already-screened deg-12..16 well, are the ones with a real chance.

Check (builder runs, reviewer reproduces): clone `verify_upper_q6.py` →
`verify_upper_q7.py`, add Q7 to the B-branch (or A-branch for P3/P5/P7) with weight qG
exactly as Q6 was added, extend the D-formula's perturb branch by +qG·deg Q7, then:
  - `anchor` qG=0 → float, D, and per-cell enclosure BIT-IDENTICAL to verify_upper_q6 at
    held (q,qE,qF) — proves Q7 genuinely extends (valid upper bound, not a broken
    integrand);
  - `admiss` prints the full pairwise gcd grid incl. the new inter-block checks;
  - `selftest` 0 violations on the CHANGED integrand (B/A now has qG·log|Q7|), mpmath
    prec≥160;
  - `certify q1..q5 qE qF qG …` → frontier=0, CERTIFIED ≤ ~0.25403 < 0.2540419719,
    BEATS=True; `tamper` below-truth → BEATS=False;
  - reviewer mpmath prec-220 mp.quad cross-check on ~40 cells, worst (cell_hi−true)≥0.

================================================================================

## Angle 2: re-introduce a DROPPED base polynomial (P3/P5/P7) as a free A-branch block
### — enlarge the prod-P^q side, not the Q perturber side

Moves: UPPER bound, < 0.2540419719. Doche fixed the base set to {P1,P2,P4,P6,P8}, a
SUBSET of P1..P8 "forced by the search of the minimum". With the R10/R11 perturbers
(Q5,Q6) now in the family, the optimal base set may differ — a re-included P_m can lower
h. This is a distinct, never-tried lever (all prior adds were on the Q side).

Skeleton: identical to Angle 1 but the new block enters the A-branch:
A(t) += qH·log|P_new|, and D's prod-P branch becomes max(Σq_i deg P_i + qH·deg P_new,
56+…). Re-optimize jointly seeded at held with qH=0.

Hard step: **the A-branch D-bookkeeping.** When the new block is on the prod-P side, the
D-formula's FIRST argument (Σ q_i deg P_i) grows, not the perturb branch — the perturb
branch dominates the held D (70.64 vs 59.20), so a P-side add only helps if it raises A
in the band where A>B (shifting G=A down per unit D) or, more usefully, lets the q
rebalance so the perturb branch can shrink. Subtler than a Q-add; the float probe must
confirm a real drop. Admissibility: P_new(0)=P_new(1)=? — the P_i are NOT required to be
1 at 0,1 (they are base polys, not perturbers); the builder must read Doc01a §4 on how
P_m enter condition (4) (they sit under prod P^q, coprime to the perturber product) and
re-run the gate accordingly — do NOT assume the Q-block gate applies verbatim.

Check: same harness pattern, with the A-branch and prod-P D-argument edited; anchor at
qH=0 recovers held; selftest on changed A; certify frontier=0 < record.

================================================================================

## Angle 3: BMQS Remark-4.6 free-real-exponent PUSHFORWARD recast of the SAME family
### — a cheaper/alternative single-circle certificate, possibly exposing new exponents

Moves: UPPER bound, < 0.2540419719 (re-coordinatization of the Doche family; the gain,
if any, comes from a richer/cheaper parametrization, not new validity).

The idea (BMQS Remark 4.6 / §1.4 V=∏P^q, explorer §2): the Doche limit measure is the
weighted-product member of the SAME cone P^Z_log(C) that BMQS Thm 4.5's μ_{P,Q} lives
in. Recast log h as the Prop-7.8 single-circle pushforward objective
∫₀¹ ρ(θ)dθ, ρ(θ)=(1/D)·Σ_{S_θ(w)=0}[log⁺|w|+log⁺|1−w|], with the WEIGHTED
S_θ(X)=∏_m P_m(X)^{?}−e^{2πiθ}·∏ Q_i(X)^{q_i} carrying the free real exponents. This is a
1-D integral over θ of a sum of log⁺ over the roots of S_θ — the same KIND of
outward-rounded quadrature as `verify_upper_*.py`, but collapses the χ-coordinate double
integral to one unit circle.

Why it could help: a cleaner single-circle integrand may admit a tighter/faster
enclosure (more cells, lower slack) and a different exponent parametrization that the
χ-coordinate optimizer cannot reach — possibly squeezing the cert slack itself
(~1e-7…1e-6) into a strict micro-break, or revealing exponent directions the Doche
parametrization fixes.

Hard step: **proving the WEIGHTED pushforward (real exponents on a PRODUCT) is a genuine
admissible measure with the resultant/integrality clause intact** — Thm 4.5 proves it
for a single coprime IRREDUCIBLE integer pair (P,Q) with INTEGER exponents; the
real-exponent weighted-product version (Remark 4.6 / μ′) is stated but the explicit
admissibility (∫log|F|dμ′ ≥ 0 via the resultant being a nonzero integer) for a PRODUCT
with real exponents must be derived, not assumed. This is exactly the non-obvious
validity step — if it reduces to the SAME Doc01a condition-(4) the family already
satisfies, the recast is sound; if not, it is invalid.

Check: build the Prop-7.8 ρ(θ) evaluator (np.roots of S_θ over a θ-grid + sympy
irreducible/coprime/monic gate on P,Q to avoid the 0.194 invalid-measure trap the
explorer flagged), confirm it reproduces the held 0.25404 on the Doche exponents
(SANITY GATE — if it doesn't match, the recast is wrong), THEN re-optimize exponents and
certify the single-circle integral with outward rounding + interval root-enclosure (must
guard ramification points where S_θ has a multiple root). Reviewer reproduces the ρ(θ)
quadrature and the P,Q admissibility derivation.

================================================================================

## Ranking

1. **Angle 1 first.** It is the proven R5–R11 lever, reuses the twice-verified
   `verify_upper_q*.py` back end with only inputs changed (lowest rigor/reproducibility
   risk), the bound is automatic for any admissible q (zero optimality burden), and it
   targets the GENUINELY under-explored direction the data points to: LOW-degree blocks
   (deg ≤ 8, esp. Flammang j3 deg 3) and the joint re-optimization the frozen-q screen
   never ran. The deg-penalty mechanism (j13 deg12 beat Qa,Qb deg24 by 2e-4) is concrete
   evidence the sweet spot is lower degree than anything tried. Atomic first step: add
   j3, run admiss, joint-reoptimize seeded at held with qG=0, report float. If j3 is dry,
   step through j6/j7/j9 then Angle 2.
2. **Angle 2 (fall back to it if Angle 1's Q-side low-degree blocks are all dry).** A
   distinct never-tried lever (the A-branch / dropped base polys), but the D-bookkeeping
   is subtler and the gain mechanism is indirect (q-rebalance), so it is second.
3. **Angle 3 (only if Angles 1–2 fail to certify a break).** Highest novelty but its
   payoff is a re-coordinatization of the SAME bound, and its hard step (real-exponent
   weighted-pushforward admissibility) is a non-obvious validity derivation — would need
   `Spec review: required` if promoted. The explorer's verdict (the record family already
   lives in this cone; Thm 4.5 is re-coordinatization, not new slack) caps its expected
   gain to the cert-slack micro-break, so it ranks last on gain-per-effort.

Dead ends NOT re-proposed (already burned): same-family q-only tuning (R6 dry, 1.8e-6);
bare low-degree single-pair μ_{P,Q} (0.34–0.69, hopeless); non-coprime/reducible (P,Q)
(invalid measure, sub-lower-bound trap); pure potential-theory/LP reframing (strong
duality leaves no gap); adding ANOTHER deg-12..16 Flammang block from the already-screened
well (j19 runner-up only ~1.8e-6, below safe cert margin).
