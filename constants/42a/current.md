# C_42 — Turán's pure power sum constant

C_42 = limsup_n R_n,  R_n = min_{max_i|z_i|=1} max_{1<=k<=n} |sum_i z_i^k|.
(Erdős problem #519.)

## Status
none

## Bounds
table (to beat): lower = 0.5 [Biró Bir94], upper = 0.69368 [Harcos, in Bir00].
Starred/unverified (NOT the bar): upper 0.6906538* [Griego Gri26] — asymptotic two-block
certificate, exact-rational verifier PASSES but no explicit finite threshold N; gap to bar ≈1.55e-7.
held (reviewer-verified by us): none yet.

## Cheer-Goldston [CG96] numerics suggest true value ≈ 0.7 (conjecture, not a bound).
So: lower bound 0.5 is loose by ~0.2; upper bound 0.69 is nearly tight.

## Softer target: the LOWER bound.
- Upper bound is near-exhausted by the two/three-block construction (Harcos ≈ Griego ≈ 0.69).
- Lower bound has ~0.2 slack and two attack routes (see literature/ digests).

## Attack routes (for outliner)
- A: make Biró's "some computable 1/2<c<1/√2" explicit — needs the paywalled Biró papers.
- B (self-contained, reproducible): explicit Fejér/positive-definite kernel test function +
  LP/SDP optimization of kernel coefficients to certify R_n > c > 0.5. First-round goal c≈0.51-0.55.

## Open verification debt
Biró [Bir94] and [Bir00b] are NOT on arXiv and ScienceDirect 403s. Builder must obtain the
PDFs before relying on the exact structure/attribution of Biró's variational constant.

## Literature digests
- literature/DIGEST-upper-bound-Harcos-Biro-Griego.md
- literature/DIGEST-lower-bound-Biro-Atkinson-CheerGoldston.md
- literature/griego-repo/ (cloned v1.0.0; verifier reproduced, all PASS)

## Progress log
(reviewer-appended only)
