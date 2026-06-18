# Digit/base constructions for the C_3a lower bound — record chain

All recent records feed a single finite set U into the [GHR2007] lemma
(`C_3a ≥ 1 + log(|U−U|/|U+U|)/log(2max(U)+1)`). They differ only in *which* finite U.

## The construction family
Fix a digit alphabet `A ⊂ ℤ_{≥0}` (with `0 ∈ A`), a base `b` (typically `b = 2·max(A)+1`),
a digit count `m`, and a digit-sum cap `T`. Define
```
W(m, T, A) = { (x_0,…,x_{m-1}) ∈ A^m : Σ x_i ≤ T }
g(x) = Σ_{i} x_i · b^i        (injective for b > 2·max(A))
U = { g(x) : x ∈ W(m,T,A) }.
```
Because the encoding is injective and base-separated, `|U+U|` and `|U−U|` are computable
combinatorially from the digit-wise sum/difference multiset counts (a convolution / DP over
digit columns), so the cardinalities can be evaluated **without enumerating all of U** — crucial
since `|U|` is astronomically large at the record parameters.

## Record chain (all LOWER bounds; lower bound is the active frontier)
| value | who | construction |
| --- | --- | --- |
| 1.14465 | [GHR2007] | original |
| 1.1479 | AlphaEvolve [GGSWT2025] | search |
| 1.173050 | Gerbicz [G2025] | base `b=2B+1`, `B=5`, contiguous digits `{0..B}`, `m≈81411`, `L=65536`; empirical optimum near `m ≈ (5/4)L`, `B=5` |
| 1.173077 | Zheng [Z2025] | asymptotic sequence: `W(m,⌊rm⌋,B)`, large-deviation rate `lim (1/m) log|W| = log(B+1) − I(r,B)`; optimize over growth rate `r`, coeff bound `a`, base param `B∈{3..10}`. **No conjectured optimum or barrier stated.** |
| **1.1740744** | **Griego [G2026]** (RECORD) | **base 21**, **non-contiguous** digit set `A = {0,2,3,4,5,6,7,8,9,10}` (note: skips 1), `m=80` digits, digit-sum cap `T=150`; exact big-integer counting certificate. |

## Key structural observations (where the slack is)
1. **Griego's jump came from a NON-CONTIGUOUS digit alphabet** (`{0,2,…,10}`, dropping the digit
   `1`) and base `21`, where Gerbicz/Zheng used contiguous `{0..B}` with `B≤10`. The digit-set
   choice is a discrete optimization that the asymptotic analyses of Gerbicz/Zheng did **not**
   sweep — they fixed contiguous alphabets. This is open slack.
2. Zheng's large-deviation formula `(1/m)log|W| = log(B+1) − I(r,B)` is for contiguous alphabets;
   the analogous rate function for an arbitrary alphabet `A` is `lim (1/m) log|W| = log|A| − I_A(r)`
   with `I_A` the Legendre transform of the alphabet's digit-sum cumulant. Re-running the
   optimization over the *alphabet* (not just `B`) is the natural next push.
3. The certificate is finite and exact; **no floating point is needed for validity** — the bound
   to beat is a fixed rational comparison once the alphabet/base/m/T are fixed.

## Reproduction sanity check (done by explorer, round 1)
A toy run of Griego's alphabet `A={0,2,…,10}`, base 21, small `(m,T)`:
`(m=3,T=8)→1.1062`, `(m=4,T=10)→1.1185` — already >1 and climbing with `m,T`, confirming the
mechanism and that the record 1.1740744 is the large-`(m,T)` limit of exactly this family.

## Refs
- [GHR2007] Gyarmati, Hennecart, Ruzsa. Funct. Approx. 37(1):175–186 (2007).
- [G2025] Gerbicz. arXiv:2505.16105.
- [Z2025] Zheng. arXiv:2506.01896.
- [G2026] Griego. teorth/optimizationproblems PR #71 (cert not yet committed to repo; only ledger entry).
- [GGSWT2025] Georgiev–Gómez-Serrano–Tao–Wagner. arXiv:2511.02864 (AlphaEvolve).
