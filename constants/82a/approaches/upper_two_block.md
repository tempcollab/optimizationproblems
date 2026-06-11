# Approach: UPPER bound via a SECOND free-exponent perturbing block (Qb), R8

Status: BUILT (round 8) — builder claims CERTIFIED upper 0.2542657872 < held R7
0.2543185491 (margin 5.276e-5), pending reviewer verification. Direct extension of the
R7-APPROVED single-extra-block harness `verify_upper_q3.py`. ONE atomic step: add
Q4 = Qb (deg-24 sibling of Qa) as a SECOND free-exponent perturbing block with its own
exponent qC.

## R8 BUILD RESULT (builder, unverified by reviewer)

Harness: `certificate/verify_upper_q4.py` (self-contained, imports verify_upper as vu,
verify_vec as vv, verify_upper_q3 as vq3 for the anchor cross-check).

Optimized 7-exponent point (Nelder-Mead on the float midpoint Riemann sum, seeded at the
R7 optimum with a small positive qC nudge so qC engages; the q-vector re-balances
substantially when qC turns on — naively adding qC at the fixed R7 q INCREASES the value,
so re-optimization is essential):
  q   = (13.5067, 9.9134, 2.7258, 1.7086, 0.7364)
  qB  = 0.1092   qC = 0.2437
  D   = max(sum q_i deg P_i, 56 + qB*24 + qC*24) = max(53.8833, 64.4696) = 64.4696
        (the perturbing branch dominates; both free blocks contribute to D).
  float log h (16M midpoint) = 0.2542656824.

Gates (ALL passed):
  - ANCHOR (qC=0): float_value_q4(R7 q, qB=0.129, qC=0) = 0.254318441601 reproduces
    float_value_q3 to >=10 digits; D collapses to 56+0.129*24=59.096; per-cell enclosure
    bit-identical to verify_upper_q3. -> Qb is a genuine free-exponent EXTENSION.
  - ADMISSIBILITY of W=Q1*Q2*Q3*Q4: deg 104, W(0)=W(1)=1, Q3,Q4 squarefree, FULL pairwise
    gcd grid INCLUDING the NEW gcd(Qa,Qb)=1 — all True.
  - SELFTEST_q4 on the CHANGED integrand (B now has qB*log|Q3| AND qC*log|Q4|): 0/200
    violations on BOTH branches (flat cap=0.0, midpt cap=1e-9).
  - CERTIFY at frontier=0: 665192 leaves, 0 unresolved, 6 rounds, 212s. int_0^2pi G dt
    <= 102.9965722302, int_0^1 G ds <= 16.3924135920, D = 64.4696.
    CERTIFIED log h <= 16.3924135920/64.4696 = 0.2542657872 (hand-checked).
    Strict beat of held R7 0.2543185491, margin 5.276e-5.
  - TAMPER: bogus target 0.25425 (below truth 0.2542657872) -> BEATS=False, frontier=0
    (no grid fallback faking a proof).

Reproduce:
  python3 constants/82a/certificate/verify_upper_q4.py certify \
    13.5067 9.9134 2.7258 1.7086 0.7364 0.1092 0.2437 200000 14 1e-10
  (~3.5 min; prints admissibility, float, selftest 0/200, then CERTIFIED 0.2542657872).
  Anchor: verify_upper_q4.py anchor. Admiss: verify_upper_q4.py admiss.
  Tamper: verify_upper_q4.py tamper 13.5067 9.9134 2.7258 1.7086 0.7364 0.1092 0.2437 0.25425.

What would push it further: a THIRD free-exponent perturbing block (Doc01a's family has
only Qa,Qb at deg 24; a further block would need a new squarefree deg>0 factor coprime to
the whole dictionary), or a higher-degree distinguished/perturbing block. The certificate
slack here is larger than R7's (~1e-4 at the flat stage, resolving to the float to ~1e-7
by round 6) because qC=0.244 makes Q4's near-zeros sharper, so the frontier grew to ~236k
mid-run before resolving — still finishes in 6 rounds. The float optimum remains the lever.

---

### ORIGINAL SPEC (below)

Moves: UPPER bound. Target to beat: **held 0.2543185491** (reviewer-verified, R7).
Float probe (R8 triage, `literature/R8_explore_triage.md`): 7-exp optimum lands at
~0.2542655 (qB~0.110, qC~0.253), a ~5.3e-5 drop over held — ~4x the R7 gain and
>> the ~1e-7 certificate slack. A record-break = any admissible (q,qB,qC>=0) whose
rigorous max(A,B) quadrature enclosure certifies log h < 0.2543185491.

## Spec review: skip

Rationale: this is a mechanical second application of the EXACT edit the reviewer
already verified in R7 (B-branch gains one more weighted log|.| term; D's perturbing
branch gains one more `+ q*deg` summand). One file, one integrand change, no new math
machinery, no self-coupling, no multi-stage sequencing. The only genuinely new
admissibility fact is gcd(Qa,Qb)=1, and the outliner has ALREADY confirmed it (sympy,
this round — see "Hard step" below). The R7 gating checklist (anchor, selftest,
admissibility grid, tamper, hand arithmetic) transfers verbatim. Risk is low enough
that the build can go straight to the builder; the reviewer's adversarial pass is the
safety net. (If the builder finds the anchor or selftest does NOT reproduce, that is
itself the abort signal — no review needed to catch it.)

---

## 1) The exact harness edit (extend verify_upper_q3.py -> verify_upper_q4.py)

Copy `verify_upper_q3.py` to `verify_upper_q4.py` (keep q3 intact as the R7 cert).
Add Qb and a 7th exponent qC. Concretely:

NEW MODULE CONSTANT (Qb, high->low in X; verified deg 24, Qb(0)=Qb(1)=1, squarefree
this round):
```
Q4 = [1, -5, 16, -39, 85, -180, 385, -796, 1551, -2907, 5421, -10003, 17368,
      -26734, 34951, -37880, 33603, -24203, 14041, -6486, 2342, -641, 126, -16, 1]
DEG_Q4 = 24
ASC_Q4 = vu.asc(Q4)
```

CHANGES (function by function):

- `_Dval(q, qB, qC)`: D's perturbing branch gains the qC*deg term:
  `return max(float(np.dot(q, DEGP)), float(DEGQ12 + qB*DEG_Q3 + qC*DEG_Q4))`.
  (At qB=qC=0 this collapses to max(sumP, 56) exactly as before.)

- `cell_AB_q3 -> cell_AB_q4(a,b,q,qB,qC)`: the B-branch `Bfactors` list gains ONE
  entry — `("Q4", ASC_Q4, float(qC))` — appended after the Q3 entry. The A-branch is
  UNCHANGED. Everything else (rho_full call, weighted outward-rounded accumulation of
  B_hi/B_lo/B_mid_up/B_curv/B_slope) is IDENTICAL — Qb is treated exactly like Q3,
  which is treated exactly like each P in A. This is the load-bearing observation: a
  Q-factor in B with weight qC is mechanically the same rigor object as a P-factor in
  A with weight q_i (same `vu.rho_full` output, weighted, outward-rounded).

- `cell_int_maxAB_q3 -> cell_int_maxAB_q4(a,b,q,qB,qC,rem_cap)`: only the call
  `cell_AB_q3(...)` becomes `cell_AB_q4(...)`. The straddle/flat/midpoint/refine logic
  is UNCHANGED (it consumes A_hi..B_slope, agnostic to how many factors built them).

- `certify_maxAB_q3 -> certify_maxAB_q4(q,qB,qC,...)`: thread qC through to
  `cell_int_maxAB_q4` and `_Dval`. The frontier branch-and-bound loop is UNCHANGED.

- `float_value_q3 -> float_value_q4(q,qB,qC,...)`: B gains `+ qC*np.log(np.abs(pv(Q4,chi)))`;
  D via `_Dval(q,qB,qC)`. UNCHANGED otherwise.

- `admissibility_check_q3 -> admissibility_check_q4()`: W = Q1*Q2*Q3*Q4. See section 2.

- `selftest_q3 -> selftest_q4(q,qB,qC,...)`: the mpmath `G_exact` B-line gains
  `+ mp.mpf(qC)*lp(ASCmp_Q4)`. cell_int call becomes cell_int_maxAB_q4. The CHANGED
  integrand (B now has qC*log|Qb|) MUST be re-self-tested — the q3 selftest did not
  cover this term.

- `HELD_CERT = 0.2543185491` (the R7 value this round must beat). The anchor target
  becomes the R7 held float (see section 3), not the R6 one.

- CLI: `anchor`, `admiss`, `selftest q1..q5 qB qC`, `certify q1..q5 qB qC [M0]...`.

WHAT STAYS UNTOUCHED: all of `verify_upper.py` (`vu`) — w_full_cell/point, rho_full,
log_up/down, ASC dict, BASE, Q1, Q2, DEGP, DEGQ. The entire per-cell enclosure and the
O(h^2) straddle bound are reused verbatim; we only feed one more B-factor and one more
D-summand.

## 2) Admissibility checklist for the enlarged W = Q1*Q2*Qa*Qb (Doche Lemma 5 + cond (4))

The builder MUST run `admissibility_check_q4()` and confirm ALL of:

- deg_X Q4 = 24 > 0, deg_X Q3 = 24 > 0, deg_X(Q1*Q2)=56 (each block non-constant).
- Q4(0) = Q4(1) = 1  (so X does not divide Qb and (1-X) does not divide Qb).
- Q4 squarefree (gcd(Qb, Qb') = 1).
- deg_X W = 104, W(0) = W(1) = 1  (X !| W and (1-X) !| W => V=prod P^q coprime to the
  X,(1-X) part; the W(0)=W(1)=1 check captures this).
- FULL pairwise coprimality grid:
    gcd(Q4, P_i) = 1 for ALL FIVE P_i  (P1,P2,P4,P6,P8),
    gcd(Q4, Q1) = 1,  gcd(Q4, Q2) = 1,
    **gcd(Q4, Q3) = gcd(Qb, Qa) = 1**   <- THE ONE NEW CHECK (two distinct free blocks).
  (Plus the inherited Q3 grid: gcd(Q3,P_i)=gcd(Q3,Q1)=gcd(Q3,Q2)=1, re-run.)
- Doche Lemma 5 + condition (4) for the MULTI-BLOCK construction: with the fixed
  distinguished block Q_{l+1}=Q1*Q2 (exponent 1) and the perturbing product
  Q3^{qB} * Q4^{qC}, the family is a genuine sequence of integer polynomials (the
  condition (4) divisibility / the coprimality of V=prod P^q to W). This is the SAME
  Lemma 5 / cond (4) the reviewer re-derived in R7 for one perturbing block, now with
  two perturbing blocks Q3,Q4 — coprime to each other and to the rest, so the
  construction extends with no new obstruction.

WHERE Qb's COEFFICIENTS COME FROM: transcribed from Doc01a's calibration family
(approaches/upper-bound-optimization.md lines 39-41 — the "Qb(X) = X^24 -5X^23 ...
+1" list, the sibling of Qa in Doc01a's Q1=Qa*Qb). The outliner re-keyed them into
the `Q4` list above and VERIFIED this round via sympy: deg 24, Qb(0)=Qb(1)=1,
squarefree True, AND gcd(Qa,Qb)=1 True. The builder must NOT re-key from memory —
copy the `Q4` list verbatim from this doc, then re-run admissibility_check_q4 as the
independent gate.

## 3) Verification gates (non-negotiable, inherited from R7)

These are the SAME gates the reviewer enforced in R7; all must pass before the
certified value is trusted:

1. ANCHOR (qC=0 must recover the R7 family EXACTLY). With qC=0, B's Q4 term vanishes
   and D's perturbing branch loses the +qC*24 summand, so the integrand AND D become
   IDENTICAL to verify_upper_q3 at the same (q,qB). The anchor mode MUST show
   `float_value_q4(q, qB, qC=0)` reproduces `float_value_q3(q, qB)` to >= 10 digits,
   AND that a `certify` run at the R7 optimum (q=(12.040,9.380,2.462,1.711,0.581),
   qB=0.129, qC=0) reproduces the held R7 certified 0.2543185491-equivalent float to
   >= 10 digits with D collapsing correctly to 59.096. This proves Qb is a genuine
   free-exponent EXTENSION (recovers the old family at qC=0), so the new value is a
   valid UPPER bound, not a broken-integrand artifact.

2. SELFTEST on the CHANGED integrand: `selftest_q4(q,qB,qC)` MUST report 0/200
   violations on BOTH branches (flat cap=0.0 and midpt cap=1e-9). The q3 selftest does
   NOT cover the qC*log|Qb| term, so this re-run is mandatory.

3. INDEPENDENT mpmath cross-check: on ~40 random cells, the per-cell max(A,B)
   enclosure (cell_int_maxAB_q4, both flat and midpt) must dominate an independent
   high-precision (prec>=160) mpmath Gauss-quad / mp.quad of int_cell G dt — worst
   `cell_hi - true_int >= 0` (outward-rounded). (selftest_q4 already does a Riemann-sum
   version of this; the reviewer's mp.quad is the independent confirmation.)

4. TAMPER test: feed a bogus target below truth (e.g. 0.25425) and confirm the harness
   reports BEATS=False with frontier=0 — no grid fallback faking a proof.

5. CERTIFY: frontier must fully resolve (0 unresolved leaves), and the final value
   `int_0^1 G ds / D` must be re-derived BY HAND from the printed `int_0^2pi G dt`,
   `int_0^1 G ds`, and `D = max(sum q deg P, 56 + qB*24 + qC*24)`, then compared
   strictly < 0.2543185491.

## 4) The hard step and failure modes

HARD STEP (the ONE riskiest sub-step):
**Admissibility of the enlarged dictionary W = Q1*Q2*Qa*Qb — specifically the NEW
inter-block coprimality gcd(Qa, Qb) = 1.** Mechanism: Doche's multi-block limit-point
construction (Doc01a Lemma 5 / cond (4)) requires every factor of the dictionary W to
be pairwise coprime (and W coprime to V=prod P^q, with X,(1-X) not dividing W) so that
the family is a genuine sequence of distinct integer polynomials. Qa and Qb are two
DISTINCT deg-24 perturbing factors; if they shared a common factor the two "free
blocks" would not be independent and Lemma 5 would not apply with separate exponents
qB,qC. The outliner has CONFIRMED gcd(Qa,Qb)=1 this round (sympy), so the construction
is admissible — but the builder must re-run admissibility_check_q4 as the independent
gate and abort if any cell of the grid (or W(0)=W(1)=1, or squarefree) fails. If
admissibility holds, the certificate is the SAME reviewer-verified R7 machinery and the
float probe (5.3e-5 drop) strongly indicates the value clears.

FAILURE MODES:
- (Low) Anchor mismatch at qC=0: would mean the Q4-term plumbing or D-edit is wrong
  (e.g. forgot the +qC*24 in `_Dval`, or appended Q4 to the wrong branch). Caught by
  gate 1 before any trust. Fix and re-run.
- (Low) selftest_q4 > 0 violations: a sign/weight error in the new B-factor. Caught
  by gate 2; abort.
- (Very low) admissibility fails (mis-keyed Qb coefficients): caught by gate's
  squarefree / W(0)=W(1)=1 / gcd checks. The outliner-keyed `Q4` list above already
  passes all of these — copy it verbatim.
- (Possible, bankable null) certified value does not clear 0.2543185491 by the float
  margin: even so the round logs a verified admissibility + anchor + selftest + re-run
  reproduction (milestone-grade), and we learn the block needs a tighter rem_cap /
  finer M0, or that the qC optimum sits higher than probed. Re-tune (q,qB,qC) seeded
  at the probe optimum (qB~0.110, qC~0.253) and re-certify. The float probe's 5.3e-5
  drop is ~530x the ~1e-7 cert slack, so a clear break is expected.

## Ranking

ONE angle (per the R8 dispatch — the explorer already decided PATH A over the
deferred PATH B OSS-energy lower-bound play). Within it the ONE riskiest sub-step is
the gcd(Qa,Qb)=1 inter-block coprimality (named above, already confirmed). No fallback
angle needed; the bankable-null path (re-tune and re-certify at the probe optimum) is
the recovery if the first (q,qB,qC) misses the margin.
