# R8 build — Angle A (B-branch perturber) + Angle B (rigorized first-variation lemma)

Builder, round 8.  Held VERIFIED upper bound to beat: **0.2538893183** (R4).
Outcome: **NO numeric break** (B-branch lever proven DRY); **two structural deliverables**:
(A) the verified corrected B-branch first-variation marginal `m_B(Q)` + a B-perturber
saturation screen; (B) the rigorized R6 first-variation lemma (Angle B), banked.

================================================================================
## Angle A — B-branch perturber: the corrected marginal m_B(Q), and the screen

### A.1  The marginal (derived, then FD-verified with D MOVED)

Held family: `log h = <G>/D`, `<G> = int_0^1 G ds`, `G = max(A,B)`,
- `A(s) = sum_i q_i log|P_i(chi)| + qG log|j3| + qH log|j9|`   (A-branch),
- `B(s) = log|Q1 Q2| + qE log|Q5| + qF log|Q6|`              (perturber branch),
- `D = max(arg_A, arg_B)`, `arg_A = sum q_i deg P_i + qG·3 + qH·8`,
  `arg_B = 56 + qE·12 + qF·16`.

On the held R4 family **arg_A = 61.66 < arg_B = 72.00 (gap 10.34)** — the **B-branch
ATTAINS D**.  Introduce a NEW B-perturber `Q` with exponent `q_Q >= 0`:
`B -> B + q_Q log|Q(chi)|` AND `arg_B -> arg_B + q_Q deg(Q)` (so D MOVES — this is the
qualitatively new feature vs the A-base lemma, where a block enters the LOSING arg of D).

Quotient rule (`log h = <G>/D`):
```
d(log h)/dq_Q = [ d<G>/dq_Q · D − <G> · dD/dq_Q ] / D²
```
- **Envelope (Danskin) term.** `G = max(A,B)`, only B carries `q_Q`.  For `s` off the
  kink set `{A=B}` (measure 0): `dG/dq_Q = log|Q(chi)|·1_{B>A}`.  The moving-boundary
  term is 2nd order because `A−B = 0` ON `{A=B}` (continuity of the max).  Hence
  `d<G>/dq_Q|_0 = int_{B>A} log|Q(chi)| ds`.  **Active region = {B>A}** (the COMPLEMENT
  of the A-base arc {A>B}; measure ≈ 0.931).
- **D-movement term.** `arg_B` attains D and is affine in `q_Q` with slope `deg(Q)`, so
  for `|q_Q| < (arg_B−arg_A)/deg(Q)` (= 10.34/deg) D is unkinked and `dD/dq_Q = deg(Q)`.

Using `<G>/D = log h`:
```
m_B(Q) := d(log h)/dq_Q|_0 = (1/D)[ int_{B>A} log|Q(chi)| ds − (log h)·deg(Q) ].
FIRING  <=>  m_B(Q) < 0  <=>  int_{B>A} log|Q| ds < (log h)·deg(Q) ≈ 0.25389·deg(Q).
```
The cross-term `−(log h)·deg(Q)/D = −0.003526·deg(Q)` is NEGATIVE (degree-rewarding:
growing D lowers `log h = <G>/D`).  This is the new term ABSENT from the R6 A-base
marginal `r~_Q = (1/D) int_{A>B} log|Q|` (no D-movement on the losing arg).

### A.2  FD verification (script `certificate/verify_Bbranch_marginal.py`, N=4M, ~40s)

CRITICAL correction (outline-review R1): the central FD MUST move D in the perturbed
evaluation, `D(±eps) = max(arg_A, arg_B0 ± eps·deg(Q))`.  Reusing the A-base FD (D fixed)
falsely rejects the formula.  Result (held R4, eps=1e-4):

| block            | deg | int_{B>A}log\|Q\| | (logh)·deg | m_B       | m_B·D   | FD d(logh)/dq | ratio  | fires |
|------------------|-----|------------|-----------|-----------|---------|---------------|--------|-------|
| X²−X+1           | 2   | 0.530427   | 0.507778  | +3.146e-4 | +0.0226 | +3.146e-4     | 1.0000 | no    |
| X⁴−X³−X+1        | 4   | 0.806872   | 1.015556  | −2.898e-3 | −0.2087 | −2.898e-3     | 1.0000 | YES   |

Closed-form `m_B` == FD (D moved) to **ratio 1.0000** on both rows — the cross-term
sign AND magnitude are verified.  This reproduces the outline-reviewer's independent
FD result (m_B·D = −0.209 for X⁴−X³−X+1, ratio 0.99997).

### A.3  The design screen — and the SATURATION result

`certificate/screen_Bbranch.py` (N=2M) + `screen_Bbranch_search.py` (original search).
Admissibility for a B-perturber (STRICTER than A-base — run_state Rule):
(c1) `Q(0)=Q(1)=1`; (c2) squarefree + coprime (in w) to the full active dictionary
`{P1,P2,P4,P6,P8,j3,j9, Q1,Q2,Q5,Q6}`; (c3) contour-root-free `min_s|Q(chi)| >= 1e-2`.

**Result: NO firing-AND-admissible B-perturber exists within reach.**

- Of the 24 Flammang Table-1 blocks, **only 4 fire** (m_B<0): j1(deg1), j2(deg1),
  j5(deg4), j15(deg16).  **All four are inadmissible:**
  - j1 = P1, j5 = P4, j15 = Q6 — already dictionary blocks (gcd≠1; the "firing" is the
    existing factor already counted);
  - j1, j2 are the degree-1 atoms `w`, `w−1`; j2 fails Q(1)=0;
  - all four additionally have `min|Q(chi)| < 1e-2` (contour roots).
- The reviewer's firing test block `X⁴−X³−X+1` is INADMISSIBLE: it = `(X−1)²(X²+X+1)`,
  so Q(1)=0 and it is not squarefree.  It was only ever an FD-validation block, not a
  candidate.
- Original product search (admissible squarefree atoms deg2..5, |coef|≤3, Q(0)=Q(1)=1,
  contour-root-free; products to deg 12): **0 firing+admissible products.**  The cheapest
  admissible atoms have per-degree integral `int/deg ≈ 0.2631–0.2657`, ALL above the
  firing threshold `log h = 0.2539`.  Products only ADD per-degree integrals, so no
  admissible product can fire.  The least-dry admissible block is `X²−X+1`
  (`int/deg = 0.2652`, m_B·D = +0.0226 > 0).

This is the **B-branch analog of the R7 A-base maximal-firing-set result**: the firing
blocks are exactly those whose roots hug the lemniscate (driving `int/deg` below
threshold), and those are precisely the high-degree Flammang entries that are EITHER
already in the dictionary OR violate contour-root-freeness (c3) / Q(0)=Q(1)=1 (c1).

### A.4  Float pre-gate — CONFIRMS dry (script `certificate/float_pregate_q9B.py`)

Since no admissible block fires, there is nothing to certify.  To document dryness I
ran the joint Nelder-Mead re-opt (10 exponents) with the least-dry admissible block
`X²−X+1` as a new B-perturber (qJ), seeded at the held R4 point:

```
base log h (qJ=0)      = 0.2538891201
re-optimized log h     = 0.2538891200
qJ* (new B-exponent)   = -0.000000   (driven to 0)
drop below HELD        = 1.98e-07    (= the cert-float slack, same as R4)
FLOAT GATE (>=5e-6)    = FAIL (dry)
```
The exponent goes to 0; the only "drop" is the ~2e-7 cert-float slack, ~25x below the
5e-6 gate.  **Per the run_state Rule and the dispatch, NO CERTIFY is run.**

### A.5  Honest verdict on Angle A

The numeric B-branch lever is **DRY** — proven by a verified marginal + an exhaustive
table screen + an original product search + a float gate.  The deliverable is
STRUCTURAL: the **corrected B-branch first-variation marginal m_B(Q)** (the
first-variation result for the D-ATTAINING branch, which the R6 A-base lemma did not
cover — it has the NEW degree-rewarding cross-term `−(log h)deg/D`), together with the
B-perturber saturation screen.  Combined with R7's A-base maximal-firing-set result,
BOTH branches of the held Doche family are now characterized as saturated:
no admissible firing block exists on either the losing (A-base) or the attaining
(B-perturber) arg of D, within the search reach.

### Reproduce (cd constants/82a/certificate)
```
python3 verify_Bbranch_marginal.py 4000000 1e-4     # m_B vs FD (D moved), ratio 1.0000  (~40s)
python3 screen_Bbranch.py 2000000                    # table screen: 0 firing+admissible (~70s)
python3 screen_Bbranch_search.py 12 1000000          # original products: 0 firing+admissible (~150s)
python3 float_pregate_q9B.py 1,-1,1 400000 4000000   # least-dry block: qJ*->0, drop 1.98e-7 (~250s)
```

================================================================================
## Angle B (banked) — rigorized R6 first-variation lemma

See `constants/82a/approaches/R8-firstvar-rigorous.md` for the full written proof with
the H1'/H1'' corrections, the union-of-32-intervals active-arc geometry, and the
boundary-term-vanishing argument.  Numeric backing re-run this round:

- `verify_firstvar_lemma.py 4000000 1e-4`: PASS — closed-form r~_Q == central FD to
  <0.1% on j9/j6/j7 (ratios 0.9992/1.0004/1.0006), sign predicts FIRED/DRY on all 4
  test rows, j9-FIRED-vs-j6-DRY inversion recovered un-normalized.  Root-potential
  identity holds to 5.2e-17 (`verify_firstvar_lemma.py roots`).
- `audit_firstvar_rigor.py`: kink-count of A_0−B STABLE at **64** across N=5e5/2e6/8e6
  (=> K finite, measure 0); candidate blocks contour-root-free (min|j3∘chi|=4.07e-2,
  min|j9∘chi|=1.06e-2 > 0 => log|Q∘chi| ∈ L¹, H1' holds).  The growing min(A−B) with N
  (−168→−207) is the integrable −∞ log-singularity at the contour root (H1''), in the
  inactive region {A<B} — off the active integrand, as the proof requires.

### Reproduce
```
python3 verify_firstvar_lemma.py 4000000 1e-4   # lemma PASS  (~55s)
python3 verify_firstvar_lemma.py roots          # root-potential identity 5.2e-17
python3 audit_firstvar_rigor.py                 # kink finite (64), candidates L^1  (~60s)
```

================================================================================
## What would push Angle A further (for the next round)

The B-branch is saturated within the admissible-block reach, for the SAME reason as the
A-base: firing requires locus-hugging roots, which forces contour roots (c3 fail) or
collision with an existing dictionary block (c2 fail).  A numeric UPPER break now needs
a STRUCTURALLY DIFFERENT move, not another perturber/base block on the held family:
- a qualitatively different measure family (a new BMQS mu_{P,Q} weighted-product config),
  OR
- accept the held upper is near-converged toward Doche's conjecture (~0.25272) and pivot
  the paper fully to the structural contribution: the design-problem framing (R7) + the
  TWO-BRANCH first-variation marginals (R6 A-base r~_Q + this round's B-branch m_B) +
  the dual saturation characterization.
The cross-term math is now fully in hand for both branches — that is the publishable
kernel, and it is what the screen used to PROVE saturation rather than search blindly.
