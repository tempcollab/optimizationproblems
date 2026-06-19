# Cached lemma — `exact-sumdiff-dp` (reviewer-certified, R3)

**Promoted by:** proof-reviewer, Round 3. **Bar:** full bound bar (correct, no stronger than proved, reproducible).

## Statement
For a finite digit alphabet `A ⊂ ℤ_{≥0}` with `0 ∈ A`, base `b > 2·max(A)`, and
`U = { Σ_i x_i b^i : x ∈ A^m, Σ_i x_i ≤ T }`, the exact values of
`s = |U+U|`, `d = |U−U|`, and `M = max(U)` are computed by:
- `count_sumset(A, m, T)` — exact `|U+U|` (bitmask DP over `(Σv, reachable Σx clamped to [0,T])` with the dynamic low-clamp).
- `count_diffset(A, m, T)` — exact `|U−U|` (minimal-pair decoupling → 2-D DP over `(Σx*, Σy*)`).
- `max_U(A, m, T, b)` — exact `max(U)` (greedy top-digit assignment).

Source: `constants/3a/certificate/griego-family-larger-mT.py`.

## Why it holds (carry-free reduction)
`b > 2·max(A)` ⇒ base-`b` digits of `g(x)±g(y)` are exactly `x_i±y_i` (no carry/borrow), so
`|U+U|` / `|U−U|` equal the counts of distinct realizable sum-/diff-vectors under the cap `Σ ≤ T`.
The single missing digit `1` in Griego's alphabet makes per-column reachable-`Σx` sets non-contiguous,
so the sum-set bitmask is genuinely load-bearing (no interval shortcut). The dynamic low-clamp is exact
because `Σv` is monotone non-decreasing across columns, so bits below `Σv − T` are forever infeasible.

## Certification (what the reviewer reproduced)
Independently re-implemented brute force from scratch (build `W`, `U`, real sumset/diffset) and matched
all three of `(s, d, M)` on **12** cases including clamp-exercising and non-contiguous ones:
`(2,5),(3,8),(4,10),(4,12),(5,14),(3,15),(4,40),(5,20),(6,18),(5,22),(4,9),(6,15)` — ALL MATCH.
The script's own `self_test()` runs on every invocation and passes (EXIT 0). Statement is no stronger
than proved (exact counts only; the GHR read-off and record certificate live in the sketch, not here).

## Scope / caveat
Numerical (Python big-int), not a Lean proof. Correct for any `A` with `0∈A`, `b>2max(A)`. Importable
by L1 (`noncontig-alphabet-sweep`) and L3 for any alphabet.
