# Cached lemmas — `C3a.box_elem_range` / `C3a.maxbk_nonneg` (reviewer-certified, R18)

**Promoted by:** proof-reviewer, Round 18. **Bar:** full bound bar (Lean: `sorry`-free, axiom-clean, statement correct and no stronger than proved, `lake build` reproducible).

**Source file:** `constants/3a/lean/Sketches/C3aDef.lean` (`box_elem_range` ~L468, `maxbk_nonneg` ~L482; `maxbk` closed-form def ~L308; supports `box`/`emb` in `Sketches/TensorMultiplicativity.lean` L81/L84).

## What they are
Element-range bounds for the carry-free digit-tensor tower, the structural content underlying the
`an_separated` separation in B1a (the AP shifts must be spaced wider than the diameter of `bk n ± bk n`,
which is `2·maxbk`).

- `box_elem_range`: the single `box`/`emb` step. An element of `box Q U V = (U ×ˢ V).image (emb Q)`
  with `emb Q (u,v) = u + Q·v` lands in `[0, maxU + Q·maxV]` when `0 ≤ Q`, `U ⊆ [0,maxU]`,
  `V ⊆ [0,maxV]`. Both bounds are TIGHT (the top `maxU + Q·maxV` is hit when `maxU∈U`, `maxV∈V`), so the
  statement is not over-strong. Fully parametric in `Q`/`maxU`/`maxV`/`U`/`V` — reusable for any
  two-factor digit box.
- `maxbk_nonneg`: the closed-form tower bound `maxbk maxU Q n` (defined `maxbk … 0 = maxU`,
  `maxbk … (k+1) = maxU + Q·maxbk … k`) is nonnegative when `0 ≤ maxU` and `0 ≤ Q`. Plain induction.
  General over `maxU`/`Q`/`n`.

## Statements (Lean, exact)
```lean
def maxbk (maxU Q : ℤ) : ℕ → ℤ
  | 0 => maxU
  | (k + 1) => maxU + Q * maxbk maxU Q k

theorem box_elem_range (Q maxU maxV : ℤ) (U V : Finset ℤ) (hQ : 0 ≤ Q)
    (hU : ∀ u ∈ U, 0 ≤ u ∧ u ≤ maxU) (hV : ∀ v ∈ V, 0 ≤ v ∧ v ≤ maxV) :
    ∀ z ∈ box Q U V, 0 ≤ z ∧ z ≤ maxU + Q * maxV

theorem maxbk_nonneg (maxU Q : ℤ) (hmaxU : 0 ≤ maxU) (hQ : 0 ≤ Q) (n : ℕ) :
    0 ≤ maxbk maxU Q n
```

## Verification (R18)
- `lake build C3a` EXIT 0 (2970 jobs).
- `#print axioms` on BOTH lemmas: `[propext, Classical.choice, Quot.sound]` — NO `sorryAx`.
- `box_elem_range` re-derived by hand: `mem_image`/`mem_product` extract `(u,v)`; `Q·v ≤ Q·maxV` via
  `mul_le_mul_of_nonneg_left`, `0 ≤ Q·v` via `mul_nonneg`, then `linarith`. Correct and tight.
- `maxbk_nonneg`: induction, step `0 ≤ Q·maxbk` via `mul_nonneg` + `linarith`. Correct.
- No `axiom`/`native_decide`/`admit` in the file (grep).

## How to use
`import` is implicit (same project). `tpow_elem_range` (the tower range bound) is the induction
combining `box_elem_range` at each step; it stays in the sketch because it fixes the sorry base data
`Qbase`/`Ubase`. The two lemmas here are the axiom-clean, base-data-independent pieces.
