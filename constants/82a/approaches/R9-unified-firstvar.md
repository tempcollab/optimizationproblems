# R9 — Unified first-variation lemma for the Doche upper family (all D-regimes)

Status: structural milestone (NO numeric break; held upper 0.2538893183 UNCHANGED,
Status:none). This document states and proves a SINGLE first-variation theorem for the
Doche upper construction that does NOT assume which of the two D-arguments attains the
outer maximum. It contains the two separately-verified per-branch results (R6/R8 A-base,
no cross-term; R8 B-branch, cross-term `-(log h)deg/D`) as corollaries by zeroing an
index indicator, and supplies the missing TIE-case (`arg_A = arg_B`) derivation, which
is a genuine ONE-SIDED kink. The angle is Angle 1 of `R9-unified-firstvar-outline.md`
(direct one-sided quotient rule + one-sided Danskin on the outer max), with all four
outline-review fixes folded in (`R9-outline-review.md`).

INPUTS (cited, NOT re-derived):
- The A-base inner-max one-sided derivative `Phi+'(0) = int_{A_0>B} log|Q.chi| ds`,
  rigorized in `R8-firstvar-rigorous.md` (DCT on the difference quotient). VERIFIED.
- The B-branch cross-term derivation, header of `certificate/verify_Bbranch_marginal.py`,
  reviewer-reproduced R8. VERIFIED.

================================================================================
## 1. The object

`chi(s) = z(1-z)`, `z = e^{2*pi*i*s}`, `s in [0,1]`. The Doche limit-point construction
(Doc01a §4, Lemma 2; PDF-verified R2/R4/R7) gives, for an exponent vector,

```
  log h(q) = Phi(q) / D(q) ,
  Phi(q)   = int_0^1 max( A(s,q), B(s,q) ) ds ,
  D(q)     = max( arg_A(q), arg_B(q) ) ,
```

where `A`, `B` are finite real combinations of `log|R_k(chi)|` (the held R4 family:
`A` from P1,P2,P4,P6,P8,j3,j9; `B = log|Q1 Q2| + qE log|Q5| + qF log|Q6|`), and the two
D-arguments are AFFINE in every exponent:

```
  arg_A(q) = sum_i q_i deg P_i + qG deg(j3) + qH deg(j9) ,
  arg_B(q) = 56 + qE deg(Q5) + qF deg(Q6) .
```

Affineness of `arg_A`, `arg_B` is the Doc01a §4 D-formula
`D = 2b * max(sum q_m deg P_m, deg Q_{l+1} + sum q_{k+m} deg Q_m)` — CITED, PDF-verified
in the R2/R4/R7 progress-log entries; NOT re-derived here.

We perturb by ONE new integer block `Q` (squarefree, contour-root-free in the sense of
H1' below) entering ONE of the two sides with exponent `q >= 0`:

- If `Q` joins the **A-side**: `A -> A + q log|Q.chi|`, `arg_A -> arg_A + q deg(Q)`.
- If `Q` joins the **B-side**: `B -> B + q log|Q.chi|`, `arg_B -> arg_B + q deg(Q)`.

The exponent of an admissible perturbation is NONNEGATIVE (`q >= 0`); a block "fires"
(strictly lowers `log h` for small `q > 0`) iff the RIGHT directional derivative
`d+ log h /dq |_{q=0}` is `< 0`. Throughout, `d+` denotes the right (one-sided)
derivative `lim_{q -> 0+}`.

Write `a := arg_A(0)`, `b := arg_B(0)`. Exactly one regime holds at `q = 0`:

```
  (I)   a > b   : A attains D.   (no live Doche family on disk is in this regime)
  (II)  a < b   : B attains D.   (the held R4 family: a = 61.66 < b = 72.00)
  (III) a = b   : TIE, D is a max of two args BOTH moving in q.   (the hard case)
```

================================================================================
## 2. Theorem (unified one-sided first-variation marginal)

Let `Q` be an integer block joining side `X in {A, B}` with exponent `q >= 0`, under the
standing hypotheses (H1'),(H1''),(D-aff) below. Then `log h` is RIGHT-differentiable at
`q = 0`, and

```
  d+ log h /dq |_0  =  (1/D) [ Phi+'(0)  -  log h * (dD/dq)+ |_0 ] ,            (T)

  Phi+'(0)     =  int_{ ACT(X) } log|Q(chi(s))| ds ,
  ACT(A) = {A_0 > B},     ACT(B) = {B > A_0},
  (dD/dq)+|_0  =  deg(Q) * [[ X is one of the args attaining D at q=0 ]]    in regimes I, II,
  (dD/dq)+|_0  =  deg(Q) * [[ X = (the side carrying the LARGER slope at the tie) ]]  in regime III,
```

where `D = D(0) >= 56 > 0`, `log h = log h(0) = Phi(0)/D`, and `[[ . ]]` is the {0,1}
indicator of the bracketed condition. Concretely, by regime:

| regime | side X | (dD/dq)+ | d+ log h /dq |
|--------|--------|----------|---------------|
| (I) a>b | A | deg(Q) | `(1/D)[ int_{A_0>B} log|Q| - (log h) deg(Q) ]` |
| (I) a>b | B | 0      | `(1/D) int_{B>A_0} log|Q|` |
| (II) a<b | A | 0     | `(1/D) int_{A_0>B} log|Q|`  (= R6/R8 r~_Q) |
| (II) a<b | B | deg(Q)| `(1/D)[ int_{B>A_0} log|Q| - (log h) deg(Q) ]`  (= R8 m_B) |
| (III) a=b | A | deg(Q)*[[deg(Q) >= s_other]] | see §4.3 |
| (III) a=b | B | deg(Q)*[[deg(Q) >= s_other]] | see §4.3 |

`Q` FIRES iff `d+ log h /dq |_0 < 0`.

The two regime-II rows are EXACTLY the two previously-verified results: A-side recovers
the R6/R8 marginal `r~_Q = (1/D) int_{A_0>B} log|Q|` (no cross-term), B-side recovers the
R8 marginal `m_B = (1/D)[ int_{B>A_0} log|Q| - (log h) deg(Q) ]`. They are COROLLARIES of
(T), obtained by reading off the indicator. The other four rows are the new content
(regimes I and III).

Standing hypotheses (all CITED from R8; not re-derived):
- (H1') `Q` is contour-root-free: `min_s |Q(chi(s))| > 0`, so `log|Q(chi(.))|` is
  bounded, hence in `L^1[0,1]`. (R8 audit: `min|j3.chi|=4.07e-2`, `min|j9.chi|=1.06e-2`.)
- (H1'') `A_0`, `B` real-analytic off the finite contour-root set of their blocks, with
  integrable `-inf` log-singularities there, lying in the inactive region of each branch.
- (D-aff) `arg_A`, `arg_B` are affine in `q` (Doc01a §4 D-formula, PDF-verified).

================================================================================
## 3. Why the inner-max derivative is REGIME-INDEPENDENT (the hinge of the unification)

The single fact that makes (T) a unification rather than three unrelated computations:

> **`Phi+'(0)` exists and equals `int_{ACT(X)} log|Q.chi| ds` in ALL three regimes,
> because the proof of its existence (`R8-firstvar-rigorous.md`) references ONLY the
> inner `max(A, B)` and NEVER the outer `D = max(arg_A, arg_B)`.**

Re-reading `R8-firstvar-rigorous.md` Steps 2–5 line by line, the only ingredients are:

1. (Step 2, domination) `t -> max(a+t, b)` is 1-Lipschitz, so the difference quotient
   `psi_q(s) = [G(s,q) - G(s,0)]/q` satisfies `|psi_q(s)| <= |log|Q(chi(s))||`, an `L^1`
   dominator by (H1'), UNIFORMLY in `q`. — uses only the inner max and (H1').
2. (Step 3, a.e. limit) for `s` not on `K = {A_0 = B}`, `psi_q(s) -> log|Q.chi| * 1_{A_0>B}`
   (resp. `1_{B>A_0}` for a B-side block). — uses only the inner max.
3. (Step 4, `|K| = 0`) `A_0 - B` is real-analytic and not identically 0, so its zero set
   `K` is finite, hence null. — uses only `A_0, B` (the integrands), not the args.
4. (Step 5, DCT) the dominated, a.e.-convergent quotient passes to the limit; the
   moving-boundary term vanishes at first order BECAUSE `A_0 - B = 0` on `K` (envelope
   cancellation). — uses only the inner max.

NOWHERE do Steps 2–5 reference `arg_A`, `arg_B`, or which one attains the outer `D`. The
outer `D(q)` enters `log h = Phi(q)/D(q)` ONLY as the (affine) NORMALIZER outside the
integral `Phi`; it is invisible to the inner-max difference quotient. Therefore the R8
DCT lemma's hypotheses and conclusion are **regime-independent of the outer `D`**: the
same `Phi+'(0) = int_{ACT(X)} log|Q.chi| ds` holds whether we are in regime I, II, or III,
and whether `Q` joins the D-attaining arg or the losing arg.

This decoupling is precisely why the THREE regimes differ ONLY in the `(dD/dq)+` factor of
the quotient rule (T) — the `Phi+'` factor is identical across all of them. (The
outline-review CHECK 2 flagged this as load-bearing; it is now stated explicitly.)

For a B-side block the symmetric statement `Phi+'(0) = int_{B>A_0} log|Q.chi| ds` follows
by the IDENTICAL DCT argument with the roles of the two inner branches swapped (the
moving block is now inside `B`, the kink set is the same `K`, the dominator is the same
`|log|Q.chi||`). The B-branch header of `verify_Bbranch_marginal.py` states exactly this
envelope/Danskin step, reviewer-reproduced R8.

================================================================================
## 4. Proof of (T)

### 4.1 One-sided quotient rule

`log h = Phi / D`, with `D(q) >= 56 > 0` bounded away from zero on a neighbourhood of
`q = 0` (since `arg_A, arg_B >= 56` and `D` is their max). Two facts:

- `Phi` is right-differentiable at `0` with `Phi+'(0) = int_{ACT(X)} log|Q.chi| ds` — by
  the R8 DCT lemma, applied to whichever side `Q` joins (§3; regime-independent).
- `D` is right-differentiable at `0` (established in §4.2).

A function that is right-differentiable and continuous, with a denominator bounded away
from `0`, gives a right-differentiable quotient with the usual one-sided quotient rule:
for `f, g` right-differentiable at `0` and `g(0) != 0`,
`(f/g)+'(0) = (f+'(0) g(0) - f(0) g+'(0)) / g(0)^2`. (Elementary: write the difference
quotient of `f/g`, add and subtract `f(0)g(0)`, take `q -> 0+`; continuity of `f, g` and
`g(0) != 0` make the cross-terms converge. No two-sided differentiability is needed.)
Hence

```
  d+ log h /dq |_0 = ( Phi+'(0) D - Phi(0) (dD/dq)+|_0 ) / D^2
                   = (1/D) [ Phi+'(0) - log h * (dD/dq)+|_0 ] ,
```

using `Phi(0)/D = log h`. This is (T), modulo identifying `(dD/dq)+`.

### 4.2 One-sided derivative of the outer max (one-sided Danskin)

`D(q) = max(arg_A(q), arg_B(q))` is a max of two AFFINE functions (D-aff), hence convex
and piecewise-linear in `q`. A convex function on `R` has one-sided derivatives
everywhere; for a finite max of differentiable functions the RIGHT derivative is the max
of the right derivatives over the ACTIVE index set at the base point:

```
  (dD/dq)+|_0 = max{ arg_A'(0) : a attains D(0) } u { arg_B'(0) : b attains D(0) } .
```

This is the one-sided Danskin / max-rule for a finite max of `C^1` (here affine)
functions — Danskin's theorem (Bertsekas, *Nonlinear Programming*, Prop. on directional
derivatives of max functions) / Rockafellar, *Convex Analysis*, Thm 23.4 & the
subdifferential of a max (Thm 23.8): the right directional derivative of
`max_i f_i` at a point equals the max over the ACTIVE set `{i : f_i = max_j f_j}` of the
directional derivatives `f_i'`. For an explicit 2-term max of affine functions this is one
line of convex calculus, used here as a CITATION not a dependency.

The slopes are `arg_A'(0) = deg(Q) * [[X = A]]` and `arg_B'(0) = deg(Q) * [[X = B]]` (only
the side `Q` joined moves; the other arg's slope in `q` is 0).

### 4.3 The three regimes

**Regime II (`a < b`, B attains D) — the held family, RECOVERS the two known results.**
Active set at `0` is `{B}` only. So `(dD/dq)+ = arg_B'(0) = deg(Q) [[X=B]]`.
- `X = A` (A-base block enters the LOSING arg): `(dD/dq)+ = 0`, and (T) gives
  `d+ log h /dq = (1/D) int_{A_0>B} log|Q| = r~_Q`. NO cross-term. This is the R6 lemma,
  rigorized in R8. ✓ (recovered exactly).
- `X = B` (perturber enters the D-attaining arg): `(dD/dq)+ = deg(Q)`, and (T) gives
  `d+ log h /dq = (1/D)[ int_{B>A_0} log|Q| - (log h) deg(Q) ] = m_B`. The R8 B-branch
  marginal, WITH the degree-rewarding cross-term `-(log h)deg/D`. ✓ (recovered exactly).

**Regime I (`a > b`, A attains D) — the A-ATTAINING cross-term (NEW; NO live family).**
Active set at `0` is `{A}` only. So `(dD/dq)+ = arg_A'(0) = deg(Q) [[X=A]]`.
- `X = A` (A-base block enters the D-attaining arg): `(dD/dq)+ = deg(Q)`, and (T) gives
  ```
    d+ log h /dq = (1/D)[ int_{A_0>B} log|Q| - (log h) deg(Q) ] .          (A-attaining)
  ```
  This is the SAME quotient-rule output as the regime-II B-branch row with `A <-> B`
  swapped (`{A_0>B}` is the A-side active arc; the cross-term is the SAME `-(log h)deg/D`
  appearing whenever the perturbed side attains `D`). It is NOT a separate empirical fact:
  it is the MECHANICAL specialization of (T) with the A-index active. (Outline-review
  CHECK 3: this must be DERIVED, not asserted by "same structure" — it is here a single
  line of (T) with the indicator activated. It is exercised on a regime-I TOY in §5,
  NOT on a live Doche family, because no A-dominant Doche family exists on disk; see §6.)
- `X = B` (perturber enters the LOSING arg): `(dD/dq)+ = 0`, and (T) gives
  `d+ log h /dq = (1/D) int_{B>A_0} log|Q|`. No cross-term.

**Regime III (`a = b`, TIE) — genuine one-sided kink (the hard step).**
Active set at `0` is `{A, B}` (BOTH attain `D(0)`). By §4.2,
```
  (dD/dq)+|_0 = max( arg_A'(0), arg_B'(0) ) = max( deg(Q)[[X=A]], deg(Q)[[X=B]] ) .
```
Since the block joins exactly one side, exactly one slope is `deg(Q)` and the other is `0`,
so `(dD/dq)+ = max(deg(Q), 0) = deg(Q)` — the perturbed arg's slope wins the max iff it is
positive, which it is (`deg(Q) >= 1`). Thus AT A TIE the perturbed arg always becomes the
unique D-attainer for `q > 0`, and
```
  d+ log h /dq |_0 = (1/D)[ int_{ACT(X)} log|Q| - (log h) deg(Q) ] ,        (tie)
```
i.e. the tie gives the SAME cross-term as the D-attaining regime. (If, hypothetically, two
DIFFERENT blocks of different degrees entered the two tied args simultaneously, the max
would select the larger degree; with a single block on one side the formula above is exact.)

CRUCIAL one-sidedness (outline-review CHECK 1, the single most common way such a lemma goes
wrong): at a tie `log h` is NOT two-sided differentiable. For `q -> 0-` the OTHER arg
becomes active, the LEFT derivative of `D` is `min(arg_A'(0), arg_B'(0)) = 0` (the
unperturbed arg), and the left derivative of `log h` is `(1/D) int_{ACT(X)} log|Q|` (NO
cross-term). Since `(dD/dq)+ = deg(Q) > 0 = (dD/dq)-`, the kink is REAL: `D` (hence
`log h`) has different left and right derivatives at a tie. Admissible perturbations have
`q >= 0`, so the RIGHT derivative is the only physically meaningful one, and the firing
test is `d+ log h /dq < 0`. We do NOT claim two-sided differentiability at a tie; the
formula (tie) is a RIGHT derivative, the genuine convex-PL kink being a feature.

This closes the regime-III gap with a one-sided Danskin/envelope identity on an explicit
2-term affine max — not an open inequality.

QED.

================================================================================
## 5. Verification artifact — three-regime toy

`certificate/verify_unified_firstvar.py` (runtime ~1–2 s; no live certify). It builds a
2-term affine outer max `D(q) = max(a0_A + sA q, a0_B + sB q)` and a smooth inner
functional `Phi(q) = Phi0 + r q` (`r` standing for `int_{ACT} log|Q|`), and checks that
the RIGHT finite-difference of `Phi(q)/D(q)` matches the closed-form (T) marginal
`(1/D)[ r - (Phi0/D) (dD/dq)+ ]` in EACH of the three regimes, with the tie additionally
showing the LEFT FD differs (the kink). It covers:

- **Regime I (singleton-A, A attains D):** `a0_A > a0_B`, A-side block (`sA = deg`,
  `sB = 0`). Closed form `(1/D)[ r - logh * deg ]` — the A-ATTAINING cross-term. The script
  also runs the B-side sub-case (block in the losing arg, `(dD/dq)+ = 0`, no cross-term).
- **Regime II (singleton-B, B attains D):** `a0_B > a0_A`, mirror of regime I; B-side
  block recovers `m_B`'s cross-term, A-side block recovers `r~_Q` (no cross-term).
- **Regime III (tie):** `a0_A = a0_B`; right FD matches `(1/D)[ r - logh * deg ]` (cross
  term present), LEFT FD matches `(1/D) r` (no cross term) — the two DIFFER, demonstrating
  the genuine one-sided kink.

Each row prints the closed-form value, the right FD, the residual `|closed - rightFD|`, and
PASS iff residual `< 1e-7`. The tie row additionally prints `|leftFD - rightFD|` and
asserts it is `> 1e-3` (kink present). The toy isolates EXACTLY the outer-max one-sided
derivative + quotient-rule composition; it needs no Doche family.

The two regime-II COROLLARIES on the LIVE held family are exercised (unchanged) by the
existing engines `verify_firstvar_lemma.py` (A-side, `r~_Q`) and
`verify_Bbranch_marginal.py` (B-side, `m_B`). Per run_state, re-running those ALONE banks
no milestone — they are corroboration that (T) reduces correctly on the live family; the
milestone is the unified statement (T) + the regime-I/tie derivations + the toy.

================================================================================
## 6. Scope (HONEST — enforced)

- This is a UNIFICATION + TIE-CASE theorem, NOT a claim of a new live A-dominant family or
  a new numeric bound. The held upper 0.2538893183 is UNCHANGED.
- Regime II (both sides) IS the held family; its two corollaries (`r~_Q`, `m_B`) are
  FD-exercised on disk by the existing engines and were reviewer-verified R6/R8.
- Regime I (A attains D) and the A-ATTAINING cross-term `-(log h)deg/D` for an A-side block
  are DERIVED as a line of the unified quotient rule (§4.3) and EXERCISED on a regime-I
  TOY (§5), NOT on a live Doche family: NO A-dominant Doche family exists on disk (the held
  family has `arg_A = 61.66 < arg_B = 72.00`, regime II). The toy certifies the FORMULA;
  there is no claim that the A-attaining cross-term is exercised on a LIVE family.
- Regime III (tie) is likewise exercised on a TOY (no Doche family sits exactly on a tie);
  the closed form and the genuine left/right kink are checked there. The tie derivation is
  a one-sided Danskin/envelope identity, written out in full (§4.3), not hand-waved.
- The firing test throughout is the RIGHT derivative `d+ log h /dq < 0` (`q >= 0`).
- Prior HONESTY guardrails kept: dual loci scoped UPPER-INTERNAL (`{A_0>B}` A-side arc vs
  `{B>A_0}` B-side arc); NO "lower locus = complement of upper arc"; NO
  `inf_Q r~_Q = -log t_{Z,phi}` overclaim.

================================================================================
## 7. Reproduce

```
cd constants/82a/certificate
python3 verify_unified_firstvar.py          # ~1-2 s, three-regime toy, prints PASS/FAIL + residuals
# corollary corroboration on the LIVE family (NOT the milestone by itself):
python3 verify_firstvar_lemma.py 4000000 1e-4      # regime II A-side, r~_Q, ~55 s
python3 verify_Bbranch_marginal.py 4000000 1e-4    # regime II B-side, m_B,  ~40 s
```
