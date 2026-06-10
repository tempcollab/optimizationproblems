# Digest: Lemm 2015, "New counterexamples for sums-differences" (arXiv:1404.3745)

## What it is
Lower bounds (counterexamples) for C_3c = SD({0,1,2,∞}; -1), the least exponent in
|A -B| <= max(|A|,|B|,|A+B|,|A+2B|)^c.

## Key reduction (the load-bearing trick)
- A counterexample is a finite G ⊂ R^2 with π_{-1} injective on G, giving
  α = log|G| / max_j log|π_{r_j}(G)|, where π_r(a,b)=a+rb, slopes r ∈ {0,1,2,∞}.
- **Tensorization with a non-uniform measure.** Take any probability measure P on a
  small base set G, approximate by rationals k_g/M, and form G' as the multiset of
  M-tuples with multiplicities k_g. Then |G'| = M!/∏ k_g! and likewise for each
  projection. By Stirling, as M→∞ the exponent converges to the **entropy ratio**
      α = H(X-Y) / max( H(X), H(Y), H(X+Y), H(X+2Y) ),
  where (X,Y) ~ P. (Equivalent to the entropy formulation in the 3c ledger.)
- So C_3c = sup over all discrete distributions P on (X,Y) of that entropy ratio.
  This is a smooth finite-dimensional optimization once the support is fixed.

## Value
Lemm gets C_3c >= 1.61226 from an explicit small non-uniform measure (improving the
prior uniform-set counterexamples).

## Where the slack is
- The bound is just the best entropy ratio Lemm found on his chosen support. Larger /
  better-chosen supports + better optimization push it up. This is exactly what the
  later records did (GGSWT2025 1.668; A2026 1.67471; Griego G2026 1.67473389 on a
  26-point support).
- The method has NO theoretical ceiling at 1.67; the true C_3c is between the best
  construction and the analytic upper bound 1.75 (KT1999). Each new support is a
  fresh optimization problem — pure numerical, certifiable by exact entropy arithmetic.
