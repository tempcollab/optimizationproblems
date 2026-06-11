# 82a UPPER — third / replacement free-exponent perturbing block (Flammang Q5)

Status: BUILT (R10), AWAITING REVIEW. Angle 1 certified. Outline + completed
search/admissibility/float-probe done in the planning step; the builder authored
verify_upper_q5.py and ran the full atomic certify.

## R10 BUILD RESULT (Angle 1 — replacement block h = Q1*Q2*Q5^qE, drop Qa,Qb)
Builder claim (UNVERIFIED until reviewer signs off — do NOT write to `held`):
  CERTIFIED  log h <= **0.2540639638**  (vs held 0.2542657872; margin **2.018e-4**).
  q = (12.832632, 11.283857, 2.380952, 2.049198, 0.701066), qB=qC=0, qE = 0.862588.
  D = max(sum q_i deg P_i = 49.55..., 56 + 0.862588*12) = 66.351056 (perturb branch).
  int_0^2pi G dt <= 105.9182451984; int_0^1 G ds <= 16.8574122869;
  16.8574122869 / 66.351056 = 0.254063963759 (hand-checked).
  Frontier FULLY RESOLVED: 0 unresolved, 679713 leaves, 6 refine rounds, ~224s.
  Reproduce: python3 constants/82a/certificate/verify_upper_q5.py certify \
    12.832632 11.283857 2.380952 2.049198 0.701066 0 0 0.862588 200000 14 1e-10
Checks all PASS:
  - anchor 1 (qE=0): float + D + per-cell enclosure BIT-IDENTICAL to verify_upper_q4
    at the held R9 (q,qB,qC) => Q5 is a genuine free-exponent EXTENSION.
  - anchor 2 (qB=qC=qE=0): recovers Doche base h=Q1*Q2 to >=10 digits, D collapses to 56.
  - admiss: deg Q5=12>0, Q5(0)=Q5(1)=1, squarefree, X & 1-X !| W=Q1*Q2*Q5 (deg 68);
    gcd(Q5, each of P1,P2,P4,P6,P8,Q1,Q2)=1 (load-bearing for the certified family);
    full ell=3 grid also passes incl. gcd(Q5,Qa)=gcd(Q5,Qb)=1.
  - selftest_q5 (mpmath prec=160): 0/200 violations on the CHANGED integrand (B has
    qE*log|Q5|), worst (cell_hi - true_int) = +1.29e-17 (>=0, safe side).
  - tamper (bogus target 0.25404 below truth): BEATS=False, frontier resolved. No fake.
What would push it further: the JOINT float optimum also has an ell=3 variant (keep
Qa,Qb,Q5) at ~0.2540721 (slightly worse), and the 18-candidate Flammang screen left 17
other admissible deg-vary factors that wanted qE=0 with q frozen but might help in a
deeper joint search. A genuinely new small-Mahler-measure deg~12-16 block (LLL route,
Angle 3) is the next lever once Q5 is banked. Headroom to Doche's conjectured smallest
limit point (~0.25272) is now ~0.00135.

## Bar to beat
Held reviewer-verified UPPER cert: **0.2542657872** (R9, ell=2 with Q3=Qa, Q4=Qb).
Any strict improvement below this is a record-break (still well under Doc01b 0.25443677).
Doche's conjectured smallest limit point ~0.25272 leaves ~0.0015 of headroom.

## What was done THIS round (planning step, with Bash) — the SEARCH is finished

### 1. Admissibility screen of all 24 Flammang Table 1 polynomials Q_j(w), w = X = z(1-z)
The Flammang Q_j live in exactly the upper-side variable (w = z(1-z) = X). Screened each
for: deg>0, Q(0)=1, Q(1)=1, squarefree, and coprime to the WHOLE current dictionary
{P1,P2,P4,P6,P8,Q1,Q2,Qa,Qb} (the load-bearing NEW checks gcd(Q5,Qa)=1, gcd(Q5,Qb)=1).

Self-screen pass (deg>0, Q(0)=Q(1)=1, squarefree): j = 3,5,6,7,8,9,...,24 (j=1,2,4 fail
normalization). Coprimality: j=5 shares a factor with P4, j=8 with P6, j=12 with P8 —
those THREE are rejected. **18 fully admissible candidates**:
  j = 3, 6, 7, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24.
All 18 pass gcd(Q_j, Qa)=1 AND gcd(Q_j, Qb)=1 (printed in the screen). The screen is
reproducible from flammang_table1.py + verify_upper.py + verify_upper_q4.py via sympy.

### 2. Float-probe (single block, q FROZEN at the R9 q4-optimum, optimize only qE>=0)
With q,(qB,qC) frozen and one new block Q5=Q_j added at exponent qE, only ONE candidate
lowered the bound: **j=13** (deg 12), qE*≈0.0042, drop ≈ 7.3e-7. Every other admissible
candidate wanted qE=0 (the existing dictionary dominates them). This already clears the
~1e-7 cert slack, but the real result is in the JOINT probe.

### 3. Float-probe (JOINT re-optimization, all exponents free) — THE HEADLINE
Re-optimizing q,(qB,qC),qE jointly from the q4-optimum reveals that Q5=j13 is a FAR
stronger perturber than the two deg-24 blocks Qa,Qb combined. The joint optimum DRIVES
qB→0 and qC→0 (Qa,Qb drop OUT) and uses Q5=j13 alone:

  q ≈ (12.78, 11.45, 2.31, 2.13, 0.64), qB=qC=0, qE ≈ 0.84
  float log h ≈ **0.2540684** (verified at N=8e6), drop ≈ **1.97e-4** below the held cert.

This is ~2000x the cert slack — robustly certifiable. Two concrete build families (each
~0.25406, essentially tied; pick the simpler TARGET A):
  - TARGET A (6-exp, DROP Qa,Qb): h = Q1*Q2 * Q5^qE.
      logh ≈ 0.2540638, q≈(12.83,11.28,2.38,2.05,0.70), qE≈0.86.
  - TARGET B (8-exp, KEEP Qa,Qb,Q5, ell=3): logh ≈ 0.2540721, qB=0, qC≈0.09, qE≈0.80.
TARGET A is cleaner AND slightly better — recommend it. (These are float CONJECTURES; the
builder re-optimizes lightly then certifies. The exact certified value is whatever the
rigorous run returns; it will be ~0.25407, comfortably below 0.2542657872.)

### Q5 = Flammang Table 1 entry j=13 (deg 12 in X)
ascending in X:  [1, -8, 31, -73, 114, -123, 97, -62, 36, -18, 8, -3, 1]
DESCENDING in X (harness convention, high->low, like Q3/Q4):
  Q5 = [1, -3, 8, -18, 36, -62, 97, -123, 114, -73, 31, -8, 1]
  DEG_Q5 = 12.   Q5(0)=1, Q5(1)=1, squarefree, coprime to {P1,P2,P4,P6,P8,Q1,Q2,Qa,Qb}.
(c_j=0.000256750154 is its Flammang LOWER-bound weight — irrelevant to the upper role.)

---

## Angle 1 (TOP PICK): replacement block — h = Q1*Q2 * Q5^qE, drop Qa,Qb (TARGET A)

Moves: UPPER bound, aiming for ≈ 0.25407 (float 0.2540638; drop ~1.9e-4 below held).

This is the structurally CLEANEST atomic build: it is the EXACT shape of verify_upper_q3
(one free block) with Q3 replaced by Q5=j13 (deg 12 instead of 24) — i.e. fewer moving
parts than the held ell=2 cert. Just one free exponent qE.

Skeleton:
  1. Admissibility of W = Q1*Q2*Q5 — already done above (deg>0, W(0)=W(1)=1, Q5 squarefree,
     gcd(Q5, each of P1,P2,P4,P6,P8,Q1,Q2)=1). By Doc01a Lemma 5 + condition (4), valid.
  2. Set B(t) = log|Q1| + log|Q2| + qE*log|Q5|, A(t) = sum q_i log|P_i|,
     G = max(A,B), D = max(sum q_i deg P_i, 56 + qE*deg Q5) = max(sum q_i deg P_i, 56+12*qE).
     This is the Doc01a §4 D-formula with a SINGLE perturbing block of degree 12.
  3. log h(q,qE) = (1/(2 pi D)) int_0^{2pi} G dt is a genuine ZZ-spectrum limit point for any
     admissible (q, qE>=0) — by Doc01a Lemmas 2,3,4,5 (NO optimality burden) — so C_82 <= log h.
  4. Certify the integral by the R9-verified outward-rounded max(A,B) quadrature, frontier
     fully resolved (refine until 0 unresolved). Result ~0.25407 < 0.2542657872.

Hard step: **the load-bearing claim is the FLOAT->CERT transfer — that the certified
outward-rounded integral stays below 0.2542657872.** Mechanism: the joint float drop is
1.97e-4, ~2000x the historical cert-vs-float slack (R9 slack was ~1e-7: float 0.2542656824
vs cert 0.2542657872). The max(A,B) Jensen form provably caps every downward log-singularity
at Q5's roots (at a Q5 zero B->-inf but A finite, so G_hi=A_hi finite — no vacuous cell),
exactly as for Q1,Q2,Qa,Qb. So the cert reproduces the float to ~1e-7 and the drop survives.

Check (what the builder runs): clone verify_upper_q4.py -> verify_upper_q5.py with the EXACT
edits in the "Certificate edits" section below, then
  - `anchor`: at qE=0 reproduce the held ell=2 (or, if Qa/Qb dropped, the R6 Q1*Q2 D=56)
    float to >=10 digits and D collapses correctly — proves Q5 genuinely extends.
  - `admiss`: prints the full gcd grid incl. gcd(Q5,Qa)=gcd(Q5,Qb)=1.
  - `selftest`: 0 violations on the CHANGED integrand (B now has qE*log|Q5|), mpmath prec>=140.
  - `certify q1..q5 qE M0 max_refine rem_cap`: frontier=0, CERTIFIED <= ~0.25407 < held,
    BEATS=True; `tamper` with a below-truth target -> BEATS=False.
  - reviewer mpmath prec-200 mp.quad cross-check on ~30 cells, worst (cell_hi - true_int) >= 0.

## Angle 2 (fallback / robustness): full ell=3 — keep Qa,Qb AND add Q5 (TARGET B)
Moves UPPER to ≈ 0.25407 (float 0.2540721). Skeleton identical to verify_upper_q4 with a
THIRD free block Q5 (deg 12, exponent qE): B += qE*log|Q5|, D = max(sum q_i deg P_i,
56 + qB*24 + qC*24 + qE*12). Hard step: the inter-block coprimality grid now needs the TWO
new checks gcd(Q5,Qa)=1, gcd(Q5,Qb)=1 (both verified above) in addition to gcd(Qa,Qb)=1.
Check: same harness, anchor at qE=0 must reproduce the R9 ell=2 cert exactly. Use this ONLY
if the reviewer prefers a strict superset of the held family (so the anchor is the held cert
itself, not a different family). It is ~8e-6 WORSE than Angle 1 and has more moving parts,
so it is the fallback, not the pick.

## Angle 3 (deeper search, only if Angles 1-2 somehow fail to certify): higher-degree
Flammang factors / Doche tables. The 18-candidate screen showed only j=13 improves with q
frozen, but j=13's joint dominance suggests deg~12 small-height factors are the sweet spot.
If a richer block is wanted later, breed a new small-Mahler-measure integer poly in X near
deg 12-16 (the LLL route) or factor a deeper Doche/Flammang small-height table entry. HEAVY
and uncertain — do NOT scope for R10. Recorded for the next campaign.

## Ranking
Angle 1 first: it is BOTH the largest certified drop AND the structurally simplest atomic
build (one free block, the verify_upper_q3 shape). The float drop (1.97e-4) is enormous
relative to the cert slack, so the certify is low-risk and well-trodden. Fall back to Angle 2
only if the reviewer insists the new family be a strict superset of the held ell=2 family
(so the anchor is the held cert). Angle 3 is a future-campaign note, not for this round.

## Certificate edits (verify_upper_q4.py -> verify_upper_q5.py) — for the builder
The builder's task collapses to: copy verify_upper_q4.py, make these mechanical edits, run.
For TARGET A (Angle 1, drop Qa,Qb), set qB=qC=0 is NOT enough — cleanest is to author the
6-exponent q5 harness directly (one free block). But the SAFEST minimal-diff path is to
author the ell=3 harness (Angle 2 shape) and let qB=qC=0 recover Angle 1 — that keeps the
anchor identity to the held ell=2 cert. Builder's call; both certify ~0.25407.

  Q5 (descending in X, high->low):
    Q5 = [1, -3, 8, -18, 36, -62, 97, -123, 114, -73, 31, -8, 1]   # DEG_Q5 = 12
    ASC_Q5 = vu.asc(Q5)

  D-formula (ell=3, Angle 2 shape; Angle 1 = same with qB=qC=0):
    D = max( sum_i q_i deg P_i ,  56 + qB*deg Qa + qC*deg Qb + qE*deg Q5 )
      = max( float(np.dot(q, DEGP)) ,  56 + qB*24 + qC*24 + qE*12 )

  B-branch: add ("Q5", ASC_Q5, float(qE)) to the Bfactors list, exactly as Q4 was added:
    Bfactors = [("Q1",vu.ASC["Q1"],1.0), ("Q2",vu.ASC["Q2"],1.0),
                ("Q3",ASC_Q3,float(qB)), ("Q4",ASC_Q4,float(qC)),
                ("Q5",ASC_Q5,float(qE))]
    The rigor treatment of a Q5 factor in B is mechanically identical to Q3/Q4 (same
    vu.rho_full output, weighted, outward-rounded). No new enclosure logic.

  float_value: add  + qE*np.log(np.abs(pv(Q5,chi)))  to B.
  selftest (selftest_q5): MUST re-run on the CHANGED integrand (B now has qE*log|Q5|);
    add ASCmp_Q5 and the  + mp.mpf(qE)*lp(ASCmp_Q5)  term to G_exact; require 0/ntest.
  admiss (admissibility_check_q5): add Q5 to the symbolic dictionary and print the FULL
    pairwise gcd grid INCLUDING the two new load-bearing checks gcd(Q5,Qa)=1, gcd(Q5,Qb)=1,
    plus gcd(Q5,Q1)=gcd(Q5,Q2)=gcd(Q5,P_i)=1, Q5(0)=Q5(1)=1, Q5 squarefree.
  anchor: at qE=0 the harness must reproduce the held R9 ell=2 cert float to >=10 digits and
    D must collapse to 64.4696 (the held D) — proves Q5 genuinely EXTENDS (valid upper bound,
    not a broken-integrand artifact).
  HELD_CERT constant -> 0.2542657872 (the value to beat).

  Builder seed (re-optimize lightly around these, they are float conjectures):
    Angle 1 (drop Qa,Qb): q≈(12.83,11.28,2.38,2.05,0.70), qE≈0.86, expect cert ~0.25406.
    Angle 2 (keep all):   q≈(13.16,11.27,2.36,2.04,0.81), qB=0, qC≈0.09, qE≈0.80, ~0.25407.

## Notes / risks
- The single-block frozen-q probe gave only +7.3e-7 for j=13; the 1.97e-4 comes from JOINT
  re-optimization (q rebalances and Qa,Qb drop out). The builder MUST re-optimize, not freeze.
- Why j=13 dominates the deg-24 Qa,Qb: Q5 is deg 12, so each unit of qE costs only 12 in the
  D denominator (vs 24 for Qa/Qb) while contributing comparable -log|Q5| depth where A<B; the
  D-penalty-per-perturbation is half, so its optimal exponent (~0.84) is large and effective.
- All values are FLOAT conjectures (numerical Riemann sum). They are NOT to be written as
  `held` — only the reviewer-verified cert value is held. They establish the angle WILL beat
  the record; the rigorous certify is the builder's atomic task.
```
