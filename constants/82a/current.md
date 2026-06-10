# C_82a — Essential minimum of the Zhang-Zagier height

## Status
none

## Bounds
table: lower 0.24874 [F18, Flammang 2018] · upper 0.25444 [Doc01b, Doche 2001]
       (upper bar = log(1.289735) = 0.25443677 exactly)
held: lower 0.24874 (reviewer-verified, R1; RIGOROUS interval branch-and-bound
      certificate re-establishing Flammang's record. Reproduces, does NOT beat.)
      Reproduce: python3 constants/82a/certificate/verify_vec.py  (~30s).
      upper: NONE reviewer-verified yet (the upper bar has had no re-cert in this repo).

CLAIMED this round (R4, builder — PENDING reviewer verification, NOT yet in `held`):
  Rigorous max(A,B) quadrature certificate (certify_maxAB in verify_upper.py):
  - STAGE A (re-cert):   C_82 <= log h(Doche q) <= 0.2544362773 < 0.25444.
  - STAGE B (record-break): C_82 <= log h(q*) <= 0.2543326887 < 0.25443677,
    q* = (11.74,8.77,2.45,1.55,0.53), a STRICT break (margin 1.041e-4).
  Both fully resolve (frontier=0). Selftest 0/300 violations vs mpmath.
  Reproduce: python3 constants/82a/certificate/verify_upper.py stageA   (~145s)
             python3 constants/82a/certificate/verify_upper.py stageB   (~145s)
             python3 constants/82a/certificate/verify_upper.py selftest (soundness)

Note: this round REPRODUCED the record (lower bound 0.24874) with an independent
re-runnable rigorous certificate — it does NOT strictly beat the record. Stage B
(column generation for a break) found no improving integer column; see
approaches/lp-column-generation.md. `held` set by the reviewer.

Note: BMQS (arXiv:2601.18978, 2026) quote the weaker 0.248247 <= ess <= 0.254437 (Zagier/Doche)
and do NOT cite Flammang. The genuine verified bar is the registry's lower 0.24874 = log(1.282416),
upper 0.25444 = log(1.287527... perturbed).

## What this constant is
h_Z(alpha) = h(alpha) + h(1-alpha); C_82 = sup H such that {alpha : h_Z(alpha) <= H} is finite.
Equivalently the essential minimum of the Zhang-Zagier height. Lower bounds via Smyth's auxiliary-
function / semi-infinite LP method (Doche, Flammang). Upper bounds via small-measure polynomial
families (Doche). This is a CONTINUOUS optimization constant with a reproducible certificate
(auxiliary function + integrality-of-resultant argument) -- the AlphaEvolve-style tractable kind.

## Literature digested
- literature/flammang_F18_digest.md — the record lower bound 0.24874: method, certificate, slack.
- literature/bmqs_2026_digest.md — LP-duality framing; no new numeric bound; bar unchanged.
- literature/pdfs/flammang_zz_hal.pdf, literature/pdfs/bmqs2601.18978.pdf

## Progress log
- R1: Reproduced the record method [F18] with an independent re-runnable RIGOROUS certificate: interval branch-and-bound (outward rounding, 2nd-order mean-value enclosure) certifies min_{t in [0,pi]} g(t) >= 0.24874 (worst cell 0.2487400; independent prec-200 true min 0.2487462), with the finite-exception (resultant-integrality) argument re-derived from scratch; all 24 Q_j confirmed in Z[w], all c_j>0. Verified, not a record-break.
