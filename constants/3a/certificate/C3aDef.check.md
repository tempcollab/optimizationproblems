# Lean certificate record — `lean-c3a-def` (scoped DEFINITION-only sketch)

- **Lake project:** `constants/3a/lean/` (Lean v4.31.0; Mathlib pinned to the `v4.31.0` tag, rev
  `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`). Sketch file
  `constants/3a/lean/Sketches/C3aDef.lean`, imported via the C3a lib glob and the root `C3a.lean`.
- **Build target:** `lake build C3a` (run with `~/.elan/bin/lake`). **R12: EXIT 0, 2970 jobs.**
  `Build completed successfully (2970 jobs).` Exactly 3 `declaration uses 'sorry'` warnings, at
  `Sketches/C3aDef.lean:139` (`realizes_one`), `:150` (`realizableSet_bddAbove`), `:169`
  (`griego_realizes`) — the 3 documented holes; no smuggled `sorry` elsewhere.

## Purpose
NOT a bound. A scoped definition-only sketch: put a FAITHFUL Lean definition of C_3a as the
[GHR2007] sup-over-constructions exponent on the table, with the read-off left as documented holes,
so the reviewer can rule the definitional approach in/out cheaply. Does NOT raise `held` (stays the
verified Python C_3a > 1.1776, R11).

## R12 — faithfulness fix (the deliverable)
Restores the [GHR2007, ineq. (5)] **bounded-doubling clause `|A+B| ≤ K·|A|`** (fixed K) that the
R11 draft had dropped, and switches to the two-set form (no A=B collapse). Verified against the GHR
source PDF. The definition is now a faithful UNDER-estimate of the registry constant
(`RealizableSet ⊆ {registry-realizable}` ⟹ `C3aRealDef ≤ C_3a`, the safe lower-bound direction).
See `approaches/lean-c3a-def.md` for the full faithfulness argument and the GHR-composite Griego
membership route. Key correction: the bare tensor power `A=B=U^{⊗k}` VIOLATES the doubling clause
(ratio `(|U+U|/|U|)^k → ∞`); the registry witness is the GHR composite
`Aₖ = [1,Lₖ] ∪ ⋃_{i=1}^{mₖ}(aᵢ+Bₖ)`, `Bₖ = U^{⊗k}`, whose m-translate/interval dilution brings
the doubling down to a fixed K.

## The definition on the table
```lean
def Realizes (c : ℝ) : Prop :=
  ∃ A B : ℕ → Finset ℤ, ∃ K : ℝ,
    Filter.Tendsto (fun n => ((A n).card : ℝ)) Filter.atTop Filter.atTop ∧
    (∀ᶠ n in Filter.atTop, ((setSum (A n) (B n)).card : ℝ) ≤ K * ((A n).card : ℝ)) ∧   -- clause (i) doubling
    (∀ᶠ n in Filter.atTop,
      ((setSum (A n) (B n)).card : ℝ) ^ c ≤ ((setDiff (A n) (B n)).card : ℝ))            -- clause (ii) cleared ≫
noncomputable def C3aRealDef : ℝ := sSup { c | Realizes c }
```

## `#print axioms` (R12, verbatim)
- `C3a.c3a_lower_bound_def` → `[propext, sorryAx, Classical.choice, Quot.sound,
  Q_gt_one._native.native_decide.ax_1_1, S_pos._native.native_decide.ax_1_1,
  griego_140_265_int_cert._native.native_decide.ax_1_1]`.
  The `sorryAx` traces ONLY to the 3 declared read-off holes; the `native_decide` axioms are the
  legitimate integer-core ones from `lean-native-decide-smallmt`. NO custom `axiom`, no smuggled
  hard step.
- `C3a.c3a_ge_theta` → `[propext, sorryAx, Classical.choice, Quot.sound]` (sorryAx via the holes).
- `C3a.realizableSet_nonempty` → `[propext, sorryAx, Classical.choice, Quot.sound]`.

## Holes remaining (3, all documented `sorry`)
- `realizes_one : Realizes 1` — nonemptiness witness (bounded-doubling family with `|A−B| ≥ |A+B|`).
- `realizableSet_bddAbove : BddAbove RealizableSet` — the [GHR2007, Theorem 2] 4/3 cap under bounded
  doubling.
- `griego_realizes : Realizes theta` — HOLE B, the read-off via the GHR composite (multi-round).

When these close, `c3a_lower_bound_def : (11771:ℝ)/10000 < C3aRealDef` becomes a self-contained
machine-checked `C_3a > 1.1771` over the concrete registry definition.

## Promotable
None this round (definitional reshape; substantive lemmas remain holes). Imports the already-cached
`tensor-multiplicativity` and `log-bridge` lemmas as-is.
