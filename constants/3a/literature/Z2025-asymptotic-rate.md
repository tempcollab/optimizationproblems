# [Z2025] Zheng, *Sums and differences of sets: a further improvement over AlphaEvolve* (arXiv:2506.01896)

Source HTML: https://arxiv.org/html/2506.01896 (digest saved R4).

## The asymptotic construction (large-deviation rate)
Same digit family as the record chain: base `b = 2B+1`, contiguous alphabet `{0,1,…,B}`,
`U = g(W(m,⌊rm⌋,B))` with `g(x)=Σ x_k b^k`. The cardinality of the cap set has a
large-deviation limit (Lemma 1):

```
lim_{m→∞} (1/m)·log|W(m,⌊rm⌋,B)| = log(B+1) − I(r,B)
I(c,B) = 0                                                  if c ≥ B/2
       = sup_t ( t·c − log[ (1+e^t+…+e^{Bt})/(B+1) ] )      if c < B/2   (Legendre/Cramér rate)
```

So θ for this family has a **well-defined m→∞ limit** obtained by plugging the limiting
sum-set / diff-set growth rates into the GHR read-off `θ = 1 + log(d/s)/log q`. The
finite-m values approach this limit **from below** (monotone climb — exactly what our L2
scan sees for the non-contiguous family too).

## What is optimized and how
The limit is optimized **numerically** over `(a, r, B)` in restricted domains (MATLAB
2024b, code in paper). **No closed-form supremum** is given. Optimal contiguous case is
`B=5`, giving `θ ≥ 1.173077`.

## Bearing on our L2 (non-contiguous {0,2,…,10}, b=21)
- Zheng's rate function is for **contiguous** alphabets `{0..B}`. The analogue for an
  arbitrary alphabet `A` replaces `log(B+1)` by `log|A|` and `I` by `I_A` = Legendre
  transform of the alphabet's digit-sum cumulant `log(Σ_{a∈A} e^{ta})`. Griego's
  `{0,2,…,10}` (drops 1) is NOT in Zheng's swept family — that non-contiguity is exactly
  the slack Griego exploited to jump from 1.173 to 1.174.
- **Consequence for our held bound:** the Griego family has an analogous **finite m→∞
  limit Λ**, computable from the same rate-function machinery with the alphabet's own
  cumulant. Our L2 finite-m θ values (1.1741→1.1760 at m=80→110) are climbing toward Λ
  from below. The record 1.1740744 = Griego's finite (80,150) point, NOT Λ; our (110,210)
  = 1.1760 is closer to Λ but still below it. **Λ is the analytic ceiling of the L2
  m-push** — and the ledger states all GHR-lemma bounds of this `log(d/s)/log q` form
  "cannot exceed 1.25." So 1.176 < Λ < 1.25; the family is not saturated at m=110.

## Reusable take
The asymptotic limit Λ of the non-contiguous family is a **closed-form-ish numerical
optimization** (Legendre transform of a finite cumulant), not a new continuum estimate —
cheap to evaluate and would tell the outliner the ceiling of the cheapest lever (the
m-push) before spending compute on ever-larger m. It does NOT itself certify a bound
(it's a limit/conjecture until a finite (m,T) clears it), but it bounds how far the m-push
can go.

## Refs
- [Z2025] Zheng. arXiv:2506.01896. Builds on [G2025] Gerbicz arXiv:2505.16105 (B=5 contiguous,
  m≈81411) and AlphaEvolve [GGSWT2025].
