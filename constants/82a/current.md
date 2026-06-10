# C_82a — Essential minimum of the Zhang-Zagier height

## Status
improved

## Bounds
table: lower 0.24874 [F18, Flammang 2018] · upper 0.25444 [Doc01b, Doche 2001]
       (upper bar = log(1.289735) = 0.25443677 exactly)
held: lower 0.24874 (reviewer-verified, R1; RIGOROUS interval branch-and-bound
      certificate re-establishing Flammang's record. Reproduces, does NOT beat.)
      Reproduce: python3 constants/82a/certificate/verify_vec.py  (~30s).
      upper 0.2543326887 (reviewer-verified, R5 — RECORD BREAK over Doc01b's
      0.25443677, margin 1.041e-4). Rigorous outward-rounded max(A,B) quadrature
      enclosure of log h(q*), q*=(11.74,8.77,2.45,1.55,0.53), in Doche's perturbed-
      polynomial limit-point family; frontier fully resolved (628608 leaves, 0
      unresolved). Reproduce: python3 constants/82a/certificate/verify_upper.py stageB
      (~170s). Admissibility (Doche Lemma 5) holds for q* (verify_upper.py admiss).

R4 builder CLAIM (now reviewer-VERIFIED in R5):
  Rigorous max(A,B) quadrature certificate (certify_maxAB in verify_upper.py):
  - STAGE A (re-cert):   C_82 <= log h(Doche q) <= 0.2544362773 < 0.25444.  [verified R5]
  - STAGE B (record-break): C_82 <= log h(q*) <= 0.2543326887 < 0.25443677,
    q* = (11.74,8.77,2.45,1.55,0.53), a STRICT break (margin 1.041e-4).  [verified R5]
  Both fully resolve (frontier=0). Selftest 0/300 violations vs mpmath; independent
  R5 cross-check vs mpmath Gauss-quad on 40 cells (worst cell_hi - ref = +8.3e-14).

Note: BMQS (arXiv:2601.18978, 2026) quote the weaker 0.248247 <= ess <= 0.254437 (Zagier/Doche)
and do NOT cite Flammang. The genuine verified bar (pre-R5) was the registry's lower 0.24874,
upper 0.25444 = log(1.289735); the upper is now improved to 0.2543326887.

## What this constant is
h_Z(alpha) = h(alpha) + h(1-alpha); C_82 = sup H such that {alpha : h_Z(alpha) <= H} is finite.
Equivalently the essential minimum of the Zhang-Zagier height. Lower bounds via Smyth's auxiliary-
function / semi-infinite LP method (Doche, Flammang). Upper bounds via small-measure polynomial
families (Doche). This is a CONTINUOUS optimization constant with a reproducible certificate
(auxiliary function + integrality-of-resultant argument) -- the AlphaEvolve-style tractable kind.

## Literature digested
- literature/flammang_F18_digest.md — the record lower bound 0.24874: method, certificate, slack.
- literature/doche_doc01b_digest.md — the record upper bound family (P1,P2,P4,P6,P8; Q=Q1*Q2).
- literature/bmqs_2026_digest.md — LP-duality framing; no new numeric bound; bar unchanged.
- literature/pdfs/flammang_zz_hal.pdf, doche_perturbed_doc01b.pdf, bmqs2601.18978.pdf

## Progress log
- R1: Reproduced the record method [F18] with an independent re-runnable RIGOROUS certificate: interval branch-and-bound (outward rounding, 2nd-order mean-value enclosure) certifies min_{t in [0,pi]} g(t) >= 0.24874 (worst cell 0.2487400; independent prec-200 true min 0.2487462), with the finite-exception (resultant-integrality) argument re-derived from scratch; all 24 Q_j confirmed in Z[w], all c_j>0. Verified, not a record-break.
- R5: RECORD BREAK on the UPPER bound. Independently verified C_82 <= log h(q*) <= 0.2543326887 < 0.25443677 = log(1.289735) [Doc01b], margin 1.041e-4, at q*=(11.74,8.77,2.45,1.55,0.53) in Doche's perturbed-polynomial limit-point family. Reproduced stageA (0.2544362773), stageB (0.2543326887, 628608 leaves, frontier=0), selftest (0/300), calib (h=1.2897342 = 1.289735 to 7 digits), admiss (Doche Lemma 5 holds for q*). Re-derived the load-bearing O(h^2) straddle bound from scratch (int_cell max(A,B) <= width*max(A_mid_up,B_mid_up) + max(slope)*r^2 + (1/3)max(curv)*r^3, via max(a+x,b+y)<=max(a,b)+max(x,y)) and matched it to the code incl. integration constants; confirmed leaf-only summation / exact tiling / all-outward-rounded; cross-checked the per-cell bound against an independent mpmath Gauss-quad (40 cells, worst cell_hi-ref = +8.3e-14); confirmed Q=Q1*Q2 family + D=56 normalization against the Doc01b PDF.
