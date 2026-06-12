# R8 Angle B — rigorized R6 first-variation lemma (boundary-term-vanishing via DCT)

Status: BANKED structural milestone.  Numeric backing re-run R8 (`verify_firstvar_lemma.py`
N=4M PASS; `audit_firstvar_rigor.py` kink=64 stable, candidates L¹).  The proof body is by
hand; the audits back its hypotheses.  Scoped HONESTLY (no overclaim — see §Scope).

================================================================================
## Setup

`chi(s) = z(1−z)`, `z = e^{2πis}`, `s ∈ [0,1]`.  Let `A_0`, `B` be finite real linear
combinations `sum_k c_k log|R_k(chi(s))|` of logs of integer polynomials `R_k` (the held
R4 family: A_0 from P1,P2,P4,P6,P8,j3,j9; B from Q1,Q2,Q5,Q6).  Let `Q` be an integer
polynomial (the candidate A-base block), `q_Q >= 0` its exponent, and
```
G(s, q_Q) = max( A_0(s) + q_Q·log|Q(chi(s))| ,  B(s) ),     Φ(q_Q) = ∫_0^1 G(s,q_Q) ds.
```

## Hypotheses (CORRECTED per R7-outline-review — the original R6 H1 was FALSE)

- **(H1′)** the CANDIDATE `Q` is contour-root-free: `min_s |Q(chi(s))| > 0`, hence
  `log|Q(chi(·))|` is bounded, so `∈ L¹[0,1]`.
  *Audit:* `min_s|j3∘chi| = 4.07e-2`, `min_s|j9∘chi| = 1.06e-2` (N=8M).  ✓
- **(H1″)** `A_0`, `B` are real-analytic OFF the finite contour-root set of their
  constituent blocks, with integrable `−∞` log-singularities at those roots, and
  `A_0 → −∞` at each (e.g. P1 = X vanishes at `chi(0) = 0`).  Hence a neighbourhood of
  each such point lies in `{A_0 < B}` — these singularities never touch the kink set `K`
  nor the active integrand.
  *Audit:* `min(A_0−B) = −168 → −207` as N grows (the integrable `−∞` at `chi(0)`), all
  in the inactive region; the active arc and kink count are unaffected.  ✓
- **(H2)** at `q_Q = 0` the B-branch attains `D`: `arg_A < arg_B` (R4: 61.66 < 72.00,
  gap 10.34), so `D = arg_B` is locally constant in `q_Q` (an A-base block enters the
  LOSING arg).  ✓

## Active-arc geometry (CORRECTED — not the stale "[0, 0.8221]")

In the `s ∈ [0,1]` harness convention the active set `{A_0 > B}` is a **union of ~32
intervals** with boundary `K = {A_0 = B}` a set of **64 points**, total measure
**≈ 0.0685**.  It does NOT start at `s = 0` (s = 0 is the DEEPEST inactive point, where
`A_0 → −∞`).
*Audit:* sign-changes of `A_0 − B` = **64**, STABLE across N = 5e5, 2e6, 8e6;
`|{A_0>B}| = 0.0686`.  ✓

================================================================================
## Lemma

Under (H1′),(H1″),(H2), `Φ` is right-differentiable at `q_Q = 0` and
```
Φ'(0+) = ∫_{{A_0 > B}} log|Q(chi(s))| ds  =:  r~_Q ,
```
and consequently `d(log h)/dq_Q|_0 = (1/D)·r~_Q` (by (H2), `dD/dq_Q = 0`).
COROLLARY: `Q` fires (small `q_Q>0` lowers `log h`) ⟺ `r~_Q < 0`.

## Proof

**Step 1 (D-constancy, no quotient cross-term).**  `log h = Φ(q_Q)/D(q_Q)`.  By (H2)
`arg_A(q_Q) = arg_A(0) + q_Q·deg Q < arg_B = D` for `|q_Q| < δ`, `δ = (arg_B−arg_A)/deg Q`
(≈ 1.29 for deg 8).  So `D ≡ arg_B` constant there, `dD/dq_Q = 0`, and
`d(log h)/dq_Q = (1/D)·Φ'(0+)`.  (The ±eps FD check uses eps = 1e-4 ≪ δ.)

**Step 2 (the difference quotient is dominated).**  For `q_Q ≠ 0`,
```
ψ_q(s) := [G(s,q_Q) − G(s,0)] / q_Q .
```
Since `t ↦ max(a+t, b)` is 1-Lipschitz in `t`, `|G(s,q_Q) − G(s,0)| ≤ |q_Q|·|log|Q(chi(s))||`,
so `|ψ_q(s)| ≤ |log|Q(chi(s))||`, which by (H1′) is bounded, hence `∈ L¹[0,1]`,
independent of `q_Q`.  This is the **DCT dominating function**.

**Step 3 (a.e. pointwise limit).**  Fix `s ∉ K = {A_0 = B}` (and `s` not a contour root
of `Q`, a finite set).  Two cases:
- `A_0(s) > B(s)`: for `|q_Q|` small enough that `A_0(s)+q_Q log|Q(chi(s))| > B(s)` still
  holds (true for `|q_Q| < (A_0(s)−B(s))/|log|Q(chi(s))||`), `G = A_0 + q_Q log|Q|`, so
  `ψ_q(s) → log|Q(chi(s))|`.
- `A_0(s) < B(s)`: similarly `G = B` for small `q_Q`, so `ψ_q(s) → 0`.
Thus `ψ_q(s) → log|Q(chi(s))|·1_{A_0>B}(s)` for every `s ∉ K`.

**Step 4 (K has measure zero — the load-bearing finiteness).**  `A_0 − B` is
real-analytic on `[0,1]` minus the finite contour-root set of its blocks (H1″), and is
NOT identically 0 (max +2.48, min −207, 64 sign changes — audited stable in N).  A
real-analytic function not ≡ 0 has isolated zeros, so `K` is FINITE on each analytic
sub-arc, hence finite, hence `|K| = 0`.  Near each contour-root singularity `A_0 → −∞`
(H1″) so `A_0 − B < 0` there — those points are NOT in `K` and lie in the inactive set.

**Step 5 (DCT + the boundary term vanishes at first order).**  By Steps 2–4 the DCT
applies to `ψ_q` (dominated by an L¹ function, a.e. convergent), giving
```
Φ'(0+) = lim_{q_Q→0+} ∫_0^1 ψ_q ds = ∫_0^1 log|Q(chi)|·1_{A_0>B} ds = r~_Q.
```
The MOVING-BOUNDARY contribution — the active set `{A_0 + q_Q log|Q| > B}` shifts its
endpoints as `q_Q` grows — is `O(q_Q²)`, hence 0 at first order, because on `K` the two
branches are EQUAL (`A_0 = B`): moving the integration limit across a point where the
integrand of `max(·,·)` is CONTINUOUS changes the value by `o(1)` per unit boundary
motion, and the boundary motion is itself `O(q_Q)`, so the product is `O(q_Q²)`.  This
is the standard envelope/Danskin boundary cancellation — it holds **because A_0−B = 0 on
K, NOT because the boundary is fixed**.  (The DCT in Step 5 already absorbs this: the a.e.
limit in Step 3 is the FIXED-set integrand `1_{A_0>B}`, and DCT certifies the limit of the
quotient equals the integral of that fixed-set limit — no separate boundary term survives.)

QED.

================================================================================
## Numeric backing (re-run R8)

- `verify_firstvar_lemma.py 4000000 1e-4`: closed-form `r~_Q` vs central FD of `log h`:
  ratios **0.9992 / 1.0004 / 1.0006** on j9/j6/j7 (<0.1%); SIGN predicts FIRED/DRY on
  all 4 test rows (j3,j9 FIRED; j6,j7 DRY) including the j9>j6 inversion; D-const holds.
- `verify_firstvar_lemma.py roots`: root-potential identity
  `r~_Q = Σ_ρ U^ν(ρ) + deg·log|lead|` to **5.2e-17** (j3 on R11).
- `audit_firstvar_rigor.py`: kink count **64 stable** across N=5e5/2e6/8e6 (K finite);
  `min|j3∘chi|=4.07e-2`, `min|j9∘chi|=1.06e-2 > 0` (H1′); `min(A_0−B)` diverges to −∞
  with N at the contour root (H1″, inactive region).

================================================================================
## Scope (honest — run_state HONESTY rules)

- The lemma gives the SIGN of `r~_Q` as a weighted-integer-Chebyshev condition on the
  ACTIVE arc `{A_0>B}`.  We do NOT claim the full `inf_Q r~_Q ≍ −log t_{Z,φ}` equivalence
  (future work).
- We do NOT claim "lower locus = set-complement of the upper active arc" — Flammang's
  lower locus is the whole contour minimized to a point; UNSUPPORTED.  The defensible
  dual structure is UPPER-INTERNAL: A-base active arc `{A_0>B}` vs B-perturber active arc
  `{B>A}` (this round's m_B), the two complementary arcs of the same construction.
- Danskin/Bertsekas is a CORROBORATING citation for the envelope step, not a dependency;
  the proof body (Steps 2–5) is self-contained via DCT.

## Companion result (R8 Angle A)

The B-PERTURBER first-variation marginal `m_B(Q) = (1/D)[∫_{B>A}log|Q| − (log h)deg Q]`
(see `R8-build.md`) is the SAME first-variation calculus on the D-ATTAINING branch, with
the extra degree-rewarding cross-term `−(log h)deg/D` that this A-base lemma does not have
(here D is constant; there D moves).  Together the two marginals characterize both arcs of
the construction and prove both branches saturated within reach (A-base: R7; B-perturber:
R8 Angle A).
