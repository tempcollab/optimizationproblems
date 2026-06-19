# [G2025] Gerbicz (1.173050) and [Z2025] Zheng (1.173077) — the simplex family

PDFs: constants/3a/literature/pdfs/gerbicz_2505.16105.pdf , zheng_2506.01896.pdf

## [G2025] Gerbicz, arXiv:2505.16105 — θ ≥ 1.173050

Idea (improves AlphaEvolve 1.1584): start from V(m,L) = simplex {x∈N^m : Σx_i ≤ L}, map to
integers g(x)=Σ x_k·(base)^k. AlphaEvolve/GHR used base L_k≈(2L)^k (huge). Gerbicz's observation:
for Σx_i ≤ L the AVERAGE coordinate is only L/m, so the digits stay small; bound each coordinate
x_k ≤ B and use base (2B+1). This keeps g injective on W±W while shrinking max(U) (the denominator
log(2max(U)+1)), raising θ.

Construction set: W(m,L,B) = {x∈N^m : Σx_i≤L, x_k≤B ∀k}, U = {g(x)}, g(x)=Σ x_k(2B+1)^k.

EXACT counting formulas (load-bearing — these are reused by Zheng AND by Griego's DP):
- |W(m,L,B)| = Σ_{k=0}^{⌊L/(B+1)⌋} (−1)^k C(m,k) C(m+L−k(B+1), m)   (inclusion–exclusion)
- s(U)=|U+U| = |W(m,2L,2B)|   (sum coords ≤2L, each ≤2B; no carries since base=2B+1)
- d(U)=|U−U| = Σ_{k=0}^{min(m,L)} C(m,k)·|W(k,L−k,B−1)|·|W(m−k,L,B)|
- q(U)=2max(U)+1 = (2B+1)^m − (2B+1)^{m−t} + 2(L%B)(2B+1)^{m−t−1} + 1, t=⌊L/B⌋.

Empirical optimum: B=5 (base 11) with m ≈ (5/4)L. Record at m=81411, L=65536=2^16, B=5:
θ=1.173050 (15 hours exact GMP arithmetic). |U|≈6.31e43546.
Author's note: "Further improvements might be possible by increasing L, but any additional gain is
likely < 0.0001." → diminishing returns in THIS (contiguous simplex) family.

## [Z2025] Zheng, arXiv:2506.01896 — θ ≥ 1.173077 (asymptotic ceiling of the simplex family)

Takes Gerbicz's W(m,L,B) family to the LIMIT m,L→∞ with L=⌊rm⌋, via large-deviation (Cramér)
estimates. Rate function:
  I(c,B) = 0 if c ≥ B/2; else sup_t ( tc − log((1+e^t+...+e^{Bt})/(B+1)) ).
  lim_{m→∞} log|W(m,⌊rm⌋,B)|/m = log(B+1) − I(r,B).
Plugging into θ=1+(log d − log s)/log q gives the closed-form sup:
  θ0 = sup_{B≥1} sup_{r>0} sup_{a∈(0,min(1,1/r))}
       [ log2 + ar·logB + (1−ar)log(B+1) − I(ar,1) − ar·I((1−a)/a, B−1)
         − (1−ar)·I(r/(1−ar), B) + I(2r, 2B) ] / log(2B+1).
Numerically (MATLAB, table by B): MAX at B=5 → θ0 = 1.173077285... B=4 gives 1.172138, B=6 gives
1.172856. So 1.173077 is the TRUE supremum of the contiguous simplex family — a hard ceiling for
{0,1,...,B} digit sets.

## The gap Griego exploits

Griego (1.1740744) BEATS Zheng's asymptotic ceiling 1.173077 — so he is NECESSARILY outside the
contiguous-digit family. His lever: NON-CONTIGUOUS digit set {0,2,3,...,10} (drop digit 1) +
explicit digit-sum cap T. The Zheng asymptotic machinery does NOT cover gapped digit sets; an
analogous large-deviation analysis for an arbitrary digit set A (with its own per-digit
distribution) would give a higher ceiling and could be optimized over A. THIS is the open
theoretical lever.
