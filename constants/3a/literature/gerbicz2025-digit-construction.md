# Digest: Gerbicz 2025, "Sums and differences of sets" (arXiv:2505.16105)

## What it is
Lower bound for C_3a = largest c s.t. exist large A,B with |A+B| << |A| and
|A-B| >> |A+B|^c. Proves C_3a >= 1.173050 (later edged to 1.173077 by Zheng;
record now 1.1740744 by Griego, base-21 digit construction, PR #71).

## Method (GHR power trick + digit/base construction)
- GHR2007 lemma: a finite set U of non-neg integers with 0 ∈ U gives
      C_3a >= 1 + log(|U-U| / |U+U|) / log(2 max(U) + 1).
- Gerbicz builds U as a base-(2B+1) digit set: g(x_0,...,x_{m-1}) = Σ x_k (2B+1)^k
  with each digit 0<=x_k<=B and a constraint on the coordinate sum (<=L). Then
  |U+U| and |U-U| are counted exactly by counting weighted compositions W(m,L,B).
  Example: m=81411, L=65536, B=5 gives θ >= 1.173050.

## Ceiling / slack
- The GHR-lemma route is **capped at 1.25** (stated in the 3a ledger). Upper bound is
  4/3 = 1.3333 (GHR2007), believed possibly tight; gap 1.174 -> 1.333.
- Gerbicz: "Further improvements might be possible by increasing L, but any additional
  gain is likely to be less than 0.0001." So this construction is essentially
  saturated near 1.1741. Squeezing more out of digit constructions yields <1e-4 gains
  — a poor target for a single run aiming to beat the verified record 1.1740744.
- Genuine improvement past ~1.18 needs a different construction idea, not a bigger U.
