# R7 outline review — Angle 1 (enrich Doche perturbing dictionary with Q_3)

**Verdict: CHANGES REQUESTED.**

Angle 1 *can* in principle beat the record and reuses the verified rigor back end, so
it is not a dead end and not a RETHINK. But the outline as written contains one
materially wrong claim (the certification step is NOT a drop-in input swap), one
under-specified admissibility condition (the multi-Q case), and one ambiguity that, if
the builder resolves it the wrong way, makes the seeding/monotonicity argument FALSE.
These must be nailed down in the build, not waved through. Specifics below.

---

## What is correct (verified against the harness and Doc01a)

1. **Upper-bound validity for any admissible q — confirmed.** Doc01a Lemma 2 +
   Lemmas 3,4,5 make `log h(q)` a genuine limit point of the ZZ spectrum for any
   admissible `q`, so `C_82 <= log h(q)`. No optimality burden. (verify_upper.py
   header, Doc01a lines 905–1196.) Enlarging the family cannot break this — every
   admissible point is still a valid upper bound.

2. **Seeding/monotonicity logic — correct, WITH a caveat (see Issue A).** I worked
   the general Doche formula (Doc01a eq before line 1160): the perturbing side is
   `Q_{l+1} * prod_{m<=l} Q_m^{q_{k+m}}` and
   `D = 2b*max(sum q_m deg P_m, deg Q_{l+1} + sum q_{k+m} deg Q_m)`. If Q_3 is added as
   a **free-exponent block** `Q_m` (m<=l), then at `q6=0`: `Q_3^0 = 1` leaves the
   perturbing product unchanged AND the second D-branch gains `q6*deg Q3 = 0`, so both
   the integrand and D are identical to the held family. The held value is recovered
   exactly, and a descent from that seed can only go down or stay equal. The
   float-optimum monotonicity claim is sound. I reproduced the R6 baseline
   (`float_value` at the R6 q = 0.2543308, held cert 0.2543309112) to anchor this.

3. **Atomic scoping — realistic, mostly.** "One new poly, finite sympy admissibility,
   reseeded descent, report float, certify only if it drops" is genuinely atomic and
   avoids the R2–R4 multi-stage over-reach. Good. (But see Issue B — the harness edit
   is bigger than the outline admits, which inflates the step.)

4. **Not a recorded dead end.** This is the dictionary-enrichment lever the explorer
   reports identify as untried; it is distinct from the dry same-family q-tuning
   (R5/R6) and the LP column-gen (R1). OK.

---

## Issues to fix while building (these are the CHANGES requested)

### Issue A (LOAD-BEARING — resolve before coding): which slot does Q_3 occupy?
Doche's perturbing side has TWO kinds of factor with DIFFERENT roles:
  - the **distinguished** `Q_{l+1}` carries a **fixed exponent 1** (its `deg>0` is what
    guarantees D's z-degree is positive — Lemma 2 needs `deg Q_{l+1}>0`);
  - the **free-exponent** factors `Q_1..Q_l` carry exponents `q_{k+m}`.

In the *current harness* the whole perturbing block is `Q = Q1*Q2` with **fixed
exponent 1** (B = log|Q1| + log|Q2|, DEGQ=56 hardcoded), i.e. it sits in the
`Q_{l+1}` slot with l=0 (NO free Q exponents at all). The outline's "add Q_3 with its
own free exponent q6, seed q6=0" ONLY makes the seeding/monotonicity argument true if
Q_3 enters as a **free-exponent block** `Q_m`, leaving the existing Q1*Q2 as the fixed
`Q_{l+1}`. If instead the builder folds Q_3 into the fixed block (B = log|Q1*Q2*Q3|,
exponent 1), then there is NO free q6, `q6=0` is meaningless, D jumps from 56 to
56+deg Q3, and the held value is NOT recovered — the change could move the bound UP.
**Build directive:** Q_3 MUST be a free-exponent perturbing factor; keep Q1*Q2 as the
fixed distinguished block. State this explicitly in the build.

### Issue B (the outline's step 5 is WRONG as written): the harness needs a real edit,
not an input swap. The outline claims certify_q.py needs "only the (positive) exponent
vector and the Q-list extended." That is false. The harness hardcodes the perturbing
branch as `B = log|Q1(w)| + log|Q2(w)|` with **no exponent**, and `DEGQ=56` is a module
constant; the free `q` vector only feeds the P-branch `A`. To add a free-exponent Q_3
the builder must:
  - change B to `B = q6*log|Q3(w)| + log|Q1(w)| + log|Q2(w)|` (Q3 weighted, Q1*Q2 fixed);
  - change D's second branch to `deg(Q1*Q2) + q6*deg Q3 = 56 + q6*deg Q3`, i.e. D is now
    `max(sum q_i deg P_i, 56 + q6*deg Q3)`;
  - extend `cell_int_maxAB` / `certify_maxAB` / `float_value` / `selftest_q` so the B
    branch's slope/curvature/midpoint enclosures include the q6*log|Q3| term (the
    rigor machinery treats B exactly like A's per-factor enclosure — mechanically the
    same code, but it IS a code change, and the selftest MUST be re-run because the
    integrand changed).
This is still atomic, but the builder must budget for a harness edit + a re-run of the
mpmath selftest (the R5/R6 verification covered the OLD integrand; a changed B branch
is NOT automatically covered). Do NOT let the build assume "the back end is approved,
just swap inputs" — re-run `selftest_q` on the new integrand and require 0 violations
before trusting any certified number.

### Issue C (admissibility is UNDER-stated for the multi-Q case).
Lemma 5 (Doc01a line 1367) requires `V, W` **relatively prime**, with neither X nor
(1-X) dividing W, where here `W` is the WHOLE perturbing product
`Q1*Q2*Q3^{q6}` (rationalized) and `V = prod P_m^{q_m}`. The outline's check list
(deg Q3>0, Q3(0)=Q3(1)=1, gcd(P_i,Q3)=1) is necessary but **incomplete**:
  - it omits `gcd(Q3, Q1)=1` and `gcd(Q3, Q2)=1` — if Q3 shares a factor with the
    existing perturbers the resultant/non-triviality argument (condition (4),
    `prod P^n / prod Q^n != +/-1`) can be compromised. Add these two gcd checks.
  - condition (4) itself (`prod P_m^{n_m} / (Q1 Q2 Q3)^{n} != +/-1` for all exponent
    tuples) must be re-checked for the enlarged dictionary, not assumed from the old
    one. The harness `admissibility_check()` currently builds Q = Q1*Q2 only; extend it
    to Q1*Q2*Q3 and re-run all gcds.
  - Q3(0)=Q3(1)=1 (so X,(1-X) do not divide Q3) is correct and sufficient for the
    "neither X nor 1-X divides W" half once Q1,Q2 already satisfy it.

### Issue D (calibration gate — re-run it on the ACTUAL new objective).
Per my role memory (round 2, this constant): a calibration gate that passes on a proxy
is not a passed gate. The outline's gate ("reproduce held float 0.2543308 at R6 q with
Q3 off") is the RIGHT gate, but "Q3 off" must mean q6=0 in the EDITED harness (Issue B),
not the old unedited harness. Require: edited harness with q6=0 reproduces 0.2543308 to
>=6 digits BEFORE optimizing q6. If it does not, the B-branch / D-branch edit is wrong
and any subsequent certified number encloses the wrong integral (the round-2 failure
mode).

---

## Feasibility of an actual record-break (the "can it beat the record" question)

The margin is thin (~1.1e-4 below Doc01b's bar, but the held value is itself nearly the
float optimum of the OLD dictionary). Whether Q_3 = Q_alpha (the proposed first
candidate) actually drops the float below 0.2543309112 is genuinely uncertain — Q_alpha
has ZZ-height ~1.290471 (Doc01a line ~1255), which is ABOVE the held limit point
1.28960, so it is a plausible-but-not-obviously-small perturber. The angle is correctly
self-limiting (it bankably reports "Q_alpha does not improve, next candidate" on a
non-drop), so even a null result is a clean, non-crashing round. This is acceptable: the
angle is the right lever and the failure mode is bankable, not a false bound. But set
expectations — a single hand-picked Q_3 dropping the float past a 1e-4-thin,
near-optimal margin is a coin-flip, not a near-certainty. If Q_alpha and one or two
siblings are dry, escalate to Angle 3 (search) rather than re-tuning q.

---

## Summary of required changes (hand to builder)
1. Q_3 enters as a FREE-exponent perturbing block; Q1*Q2 stays the fixed `Q_{l+1}`
   distinguished block (Issue A).
2. Edit the harness B-branch to `q6*log|Q3| + log|Q1| + log|Q2|` and D's second branch
   to `56 + q6*deg Q3`; re-run the mpmath selftest on the NEW integrand, require 0
   violations (Issue B). Step 5 is NOT a pure input swap.
3. Extend admissibility: add `gcd(Q3,Q1)=1`, `gcd(Q3,Q2)=1`, and re-run condition (4)
   on Q1*Q2*Q3 (Issue C).
4. Calibration gate on the EDITED harness at q6=0 must reproduce 0.2543308 to >=6
   digits before optimizing (Issue D).
5. Certify (the rigorous max(A,B) quadrature) only if the float strictly drops; report
   a null cleanly otherwise.

With these five pinned down, the builder can proceed. The angle is valid, certifiable,
and not a dead end — it just needs its hard step (the harness edit + the multi-Q
admissibility) stated honestly rather than as a costless input swap.
