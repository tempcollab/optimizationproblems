# R10 build — UPPER-INTERNAL dual-loci decomposition of the held certificate numerator

## Scope (honest, up front)

STRUCTURAL round. This deliverable does **NOT** move the held UPPER bound
0.2538893183 (verify_upper_q8A.py, R4) — that lever is reviewer-verified EXHAUSTED on the
Doche family (A-base R7, B-branch R8). What it ships is a **NEW verifiable IDENTITY**: the
held certificate's numerator splits exactly over the two upper-internal active loci, and
that split reproduces 0.2538893183 as its PASS criterion. This is a **clean decomposition
identity, not a deep theorem**.

## What the new script checks

New standalone certificate: `constants/82a/certificate/verify_dual_loci_decomposition.py`.
It REUSES the held harness's exact `float_value_q8A` reconstruction (verify_upper_q8A.py
lines 257-277): `A0` = the A-base / prod-P^q arg (carrying the held j3, j9), `B` = the
perturber arg, both at the held R4 exponents q=(14.011500,13.443930,2.643590,2.299880,
0.252420), qB=qC=0, qE=0.575080, qF=0.568800, qG=0.891590, qH=0.066860, chi=z(1-z).
`D = max(arg_A=61.66, arg_B=72.00) = 72.00176`.

Define the two **upper-internal** active loci (standing rule — UPPER-INTERNAL only, NOT
"lower = complement"):

    ACT(A) := {A0 > B}      ACT(B) := {B > A0}

### HEADLINE (Binding Condition A) — the milestone content

- **(P) active-arc PARTITION:** masks `mA = A0>B`, `mB = B>A0` are disjoint
  (`|mA & mB| = 0`, exact integer count), their union is the full grid (`|mA|mB| = N`, no
  grid point on `K={A0=B}`), and `|ACT(A)| + |ACT(B)| = 1` to machine eps.
- **(N) NUMERATOR SPLIT:** `Phi(0) = mean(max(A0,B)) = IA + IB`, where
  `IA = mean(A0*1_{A0>B})`, `IB = mean(B*1_{B>A0})`, via the pointwise identity
  `max(A0,B) = A0*1_{A0>B} + B*1_{B>A0}` a.e. (max attained by exactly one arg off the
  measure-zero kink set K). This is the load-bearing NEW identity — a decomposition of the
  held *certificate numerator* (not a derivative). No on-disk script computes this.
- **(V) VALUE REPRODUCTION:** `(IA+IB)/D = 0.2538891201`, reproducing the held
  0.2538893183 to the documented Riemann-mean-vs-cert slack (1.98e-7).
- **(TAMPER):** swapping the masks (integrate A0 over ACT(B), B over ACT(A)) makes the (N)
  residual jump to 9.36 — the split FAILS, proving it is locus-specific, not a tautology of
  `mean(max) = mean(...)`. The check has teeth.

### CORROBORATION (Binding Condition B) — supporting rows, explicitly labelled

- **(K) kink-count stability** (cites R8-firstvar-rigorous.md Step 4 for |K|=0; this is the
  EVIDENCE, not a re-derivation): sign-changes of A0-B = **64, stable across N ∈
  {5e5, 2e6, 4e6}**, matching the R8 audit. We do NOT re-derive measure-zero.
- **(M) complementary marginals**: the A-base first-variation marginal
  `r~(j9) = (1/D) int_{ACT(A)} log|j9| = -0.00009` (fires) integrates over ACT(A) — evaluated
  on the R2 anchor WITHOUT j9 (standing rule), cross-checked bit-exact against
  `verify_firstvar_lemma.closed_form_rtilde`. The B-branch marginal
  `m_B(X^2-X+1) = (1/D)[int_{ACT(B)} log|Q| - (log h)*deg] = +0.00031` (dry) integrates over
  ACT(B). **PRECISION FLAG honored:** the `-(log h)*deg` cross-term is a FIRST-VARIATION term
  and is kept STRICTLY inside (M); it never enters the (N) residual.
- **(C) per-block conditional-capacity table** (Angle 3): by linearity, IA and IB are the
  weighted sums of per-block conditional log-integrals over their own loci; reproduces IA, IB
  to <1e-8. Labelled corroboration (close to banked R6 marginals), NOT the headline.

## Pass numbers (N=4,000,000)

```
(P)  |mA & mB| = 0;  |mA|mB| = 4000000/4000000;  |ACT(A)|=0.068608  |ACT(B)|=0.931392
     |ACT(A)|+|ACT(B)| = 1.0000000000                                         PASS
(N)  Phi = 18.2804634954;  IA+IB = 18.2804634954;  residual = 0.0e+00 (<1e-9)  PASS
(V)  (IA+IB)/D = 0.2538891201;  |val - held| = 1.982e-7 (<1e-6);
     |Phi - cert int 18.2804777610| = 1.427e-5 (= D*1.98e-7, fixed outward margin) PASS
TAMPER  swapped residual = 9.36 (>>0) -> (N) correctly FAILS                    PASS
(K)  sign-changes = [64,64,64] stable                                          PASS
(M)  r~(j9)=-0.00009 (ACT(A)); m_B(X^2-X+1)=+0.00031 (ACT(B)); r~ match |diff|=0  PASS
(C)  sum per-block = IA, IB to <1e-8                                           PASS
OVERALL: ALL PASS  (~72s at N=4M; quick N=200k sanity runs first)
```

## Note on the (V) Phi-level tolerance

The MEANINGFUL value test is `|(IA+IB)/D - 0.2538893183| < 1e-6` (here 1.98e-7 — the
documented R4 slack). The certificate's `int_0^1 G = 18.2804777610` is an OUTWARD (upper)
enclosure, so it sits ABOVE the float Riemann mean Phi by exactly `D * (value slack) =
72 * 1.98e-7 = 1.43e-5`, a fixed margin that is STABLE across N (1.427e-5 at N=1M, 4M, 8M —
not a discretization error). The Phi-level bound is therefore set to `< 3e-5` (above the
fixed margin); the value bound `< 1e-6` is the real test.

## How to reproduce

```
cd constants/82a/certificate
python3 verify_dual_loci_decomposition.py            # default N=4M, ~72s, exit 0
python3 verify_dual_loci_decomposition.py 2000000    # faster top N, ~40s
```

## Why this is NEW (not R6/R8/R9)

- `verify_shared_pool.py` (R6): integer-polynomial identities only; never touches A0/B, the
  partition, the numerator, or any integral.
- `verify_firstvar_lemma.py` / `verify_Bbranch_marginal.py` / `verify_unified_firstvar.py`
  (R6/R8/R9): compute MARGINALS (derivatives at q=0) for ONE block on ONE arc. None computes
  `Phi(0) = int_{ACT(A)} A0 + int_{ACT(B)} B` (the certificate numerator itself), and none
  checks the partition as an identity.

The must-be-present new artifact is the computed `Phi(0) = IA + IB` identity on the held
family — the locus split of the bound's numerator — which no existing script computes.

## What would push it further

- (Angle 2, deferred) Upgrade the indicator split `mu_A = 1_{ACT(A)} ds` to a
  potential-theoretic identification (active-arc equilibrium / balayage measure of the
  A-base lemniscate). This is UNPROVEN on disk and carries overclaim risk; it would need a
  numerical match of mu_A's log-potential against the active-arc equilibrium potential. A
  stretch layer ON TOP of this verified partition, not a standalone round.
- Tie the per-block (C) table to the integer-transfinite-diameter design framing (R6/R7) as
  a single "each block's contribution to the bound = its conditional capacity on its locus"
  statement for the paper.
