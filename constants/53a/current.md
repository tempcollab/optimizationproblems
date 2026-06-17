# 53a — Davenport constant of `C_n^3` — tracking file

`C_53 = sup_{n>=2} (D(C_n^3)-1)/(n-1)`. Movable side = upper bound.

## Status
none

## Bounds
table: `C_53 <= 4` (Grinsztajn 2026, from `D(C_n^3) <= 4n - P(n) - 2`) · held: `C_53 <= 4` (record; not yet independently re-derived unconditionally — the verified Lean artifact this round is a CONDITIONAL re-derivation of the recursion step only, not a new or stronger bound)

## Progress log
- R2: Lean scaffold verified (reviewer). `lake build Constants` green against pinned Lean v4.31.0 / Mathlib `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`; `#print axioms` on `recursion_step` and `comparison_ineq` = `[propext, Classical.choice, Quot.sound]` only (no `sorryAx`, no problem-specific axiom). Genuinely proved: the load-bearing comparison inequality `p^2-2p+2 <= (p-1)Q` (2<=p<=Q) and the integer recursion step (`D m <= 4m-Q-2`, `D(pm) <= p·D(m)+p^2`, `2<=p<=Q` ⊢ `D(pm) <= 4pm-Q-2`), both re-derived independently by the reviewer. Zero-sum number-theory inputs carried as explicit hypotheses, not axioms — honest conditional. INFRASTRUCTURE milestone; `held` UNCHANGED at 4, no bound improvement.
