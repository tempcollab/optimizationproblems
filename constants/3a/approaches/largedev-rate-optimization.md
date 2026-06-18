# L3 — Joint base + digit-cap re-optimization via the large-deviation rate

**Slug:** `largedev-rate-optimization`   **Target:** lower bound, beat `C_3a > 1.1740744`.

## Strategy
Where L1/L2 are *blind* searches over `(A,b,m,T)`, L3 builds the **asymptotic guide** that tells
the search where to look, then certifies the chosen optimum with the same finite integer check.

Generalize Zheng's contiguous-alphabet rate to an arbitrary alphabet `A`. With `T = ⌊r·m⌋`:
```
(1/m) log |W(m,T,A)|  →  log|A| − I_A(r),
```
where `I_A` is the Legendre transform of the alphabet's digit cumulant
`Λ_A(λ) = log( (1/|A|) Σ_{a∈A} e^{λ a} )`, i.e. `I_A(r) = sup_λ (λ r − Λ_A(λ))`. The matching
growth rates of the **sum** and **difference** sets are governed by the digit-pair multiplicities:
`A+A` with multiplicity `ρ⁺_A(v) = #{(a,a'): a+a'=v}` and `A−A` with `ρ⁻_A(δ)`. Define rate
functions `σ⁺_A(r)`, `σ⁻_A(r)` for `(1/m)log|U+U|` and `(1/m)log|U−U|` from these pair cumulants
under the *coupled* cap (both summands obey `Σ≤T`). Then
```
θ_∞(A,r) = 1 + (σ⁻_A(r) − σ⁺_A(r)) / log(2·max(A)+1).
```
Maximizing `θ_∞` over `(A, r)` is a **finite convex / Legendre optimization** per alphabet — it
predicts the optimal `(A,r)` and the asymptotic bound, which the L1/L2 finite check then certifies
at concrete `(m,T)`.

## How the bound value is computed (and certified)
The rate `θ_∞` is only the *guide*. The **certified** value is always the L1 finite read-off:
pick `(A,b,m,T)` near the rate-optimal `(A, r=T/m)`, compute exact `s,d,q`, certify
`d^a·q^b ≥ s^a`. So even an *unproved* rate function is harmless — it never enters the certificate,
only the search. This keeps L3 Lean-fit while giving the search a principled target.

## Holes
1. **`rate-function-sumdiff` (HARD, analytic):** the Legendre/large-deviation identity for the
   sum- and difference-set growth rates `σ⁺_A`, `σ⁻_A` of the digit construction under the coupled
   cap. This is the clean analytic lemma; it guides but does not certify, so an approximate or
   heuristic version still drives the search.
2. **`optimize-A-r` (MEDIUM):** maximize `θ_∞(A,r)` over alphabets `A` (small/gapped) and `r`,
   producing candidate `(A,r)`. A convex program per `A`; outer loop over alphabets.
3. **`certify-finite` (shared with L1):** for the predicted optimal `(A,r)`, instantiate
   `(m,T=⌊rm⌋)`, compute exact `s,d,q` via the column-DP, certify the integer inequality vs
   `1.1740744`.

## What would push it
A rate-optimal alphabet that the L1 blind sweep would miss (e.g. an irregular multi-gap set the
Legendre objective favors), then certified finitely. Highest ceiling of the three — it is the only
line that *explains* where the optimum is rather than stumbling on it — but the slowest to first
green because of the analytic hole.

## Certify
Numerical (exact big-int at the chosen optimum) → **Lean** `native_decide`. The rate function
itself is NOT certified (it is a search heuristic); only the final integer inequality is.
