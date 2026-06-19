# Lean certificate record — `lean-c3a-def` (scoped DEFINITION-only sketch)

- **Lake project:** `constants/3a/lean/` (Lean v4.31.0; Mathlib pinned to the `v4.31.0` tag, rev
  `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`). Sketch file
  `constants/3a/lean/Sketches/C3aDef.lean`, imported via the C3a lib glob and the root `C3a.lean`.
- **Build target:** `lake build C3a` (run with `~/.elan/bin/lake`). **R15: EXIT 0, 2970 jobs.**
  `Build completed successfully (2970 jobs).` 12 `declaration uses 'sorry'` warnings at
  C3aDef.lean:139,150,302,303,304,309,310,311,403,489,498,506 — all documented; no smuggled `sorry`.
  (Lines 365/380, the two B1a spacing lemmas, are NO LONGER in the list — closed this round.)

## R15 — sub-hole B1a spacing lemmas CLOSED
`setSum_tr_pair_disjoint` / `setDiff_tr_pair_disjoint` (the cheap general half of B1a, the
shift-gap > sumset/diffset-diameter ⟹ disjoint translate-images spacing lemmas) are now proved
**sorry-free and axiom-clean**, and `griego_ak_disjoint` (B1a) is reassembled with a sorry-free proof
term modulo the residual `an_separated`. `#print axioms` (R15, verbatim, from a temporary
`AxCheck.lean`, since removed):
- `C3a.setSum_tr_pair_disjoint`  → `[propext, Classical.choice, Quot.sound]` (NO sorryAx)
- `C3a.setDiff_tr_pair_disjoint` → `[propext, Classical.choice, Quot.sound]` (NO sorryAx)
- `C3a.griego_ak_disjoint`       → `[propext, sorryAx, Classical.choice, Quot.sound]`. Proof TERM
  sorry-free; sorryAx enters ONLY via the `an_separated` obligation it `obtain`s.

Proof: `setSum_tr`/`setDiff_tr` rewrite each translate-image to `image (c+·) (B±B)`;
`Finset.disjoint_left` extracts a common `c+w = c'+w'` with `w,w' ∈ [lo,lo+diam]`; `abs_le` + `omega`
(using that equality + the two `WithinDiam` bounds) give `|c−c'| ≤ diam`, contradicting
`diam < |c−c'|` via `linarith`. (Note: `abs_lt` does NOT match `diam < |w'−w|` — abs on the RHS — so
the `|c−c'| ≤ diam` route via `abs_le` is used instead.)

### R15 hole inventory (12 sorry-warnings = 13 holes counting the witness defs separately)
`realizes_one` (139), `realizableSet_bddAbove` (150); witness data `Ubase`/`Qbase`/`Ubase_carryfree`
(302–304), `an_interval`/`an_index`/`an_shift` (309–311); **`an_separated` (403) — now the
load-bearing residual of B1a** (needs the witness-data pinning + a `maxbk` element-range bound on
`tpow Qbase Ubase n`); B2 `griego_bounded_doubling` (489), B3 `griego_diff_lower_bound` (498), B4
`griego_card_tendsto` (506).

### R15 promotable (flagged for reviewer)
`setSum_tr_pair_disjoint` / `setDiff_tr_pair_disjoint` — general spacing lemmas (shift gap exceeding
the sumset/diffset diameter ⟹ disjoint translate images), sorry-free, axiom-clean, proved in
`Sketches/C3aDef.lean` (lines ~365/380). Reusable for any composite-dilution disjointness argument.

## R14 — sub-hole B1 CLOSED (finite disjoint-union count)
`griego_disjoint_union_count` (B1, the load-bearing finite combinatorics) is now proved
**sorry-free**, plus reusable axiom-clean counting lemmas. `#print axioms` (R14, verbatim, from a
temporary `AxCheck.lean`, since removed):
- `C3a.setSum_card_decompose` → `[propext, Classical.choice, Quot.sound]` (NO sorryAx)
- `C3a.setDiff_card_decompose` → `[propext, Classical.choice, Quot.sound]` (NO sorryAx)
- `C3a.setSum_tr_card` / `setDiff_tr_card` / `setSum_biUnion` / `setDiff_biUnion`
  → `[propext, Classical.choice, Quot.sound]` (NO sorryAx)
- `C3a.griego_disjoint_union_count` → `[propext, sorryAx, Classical.choice, Quot.sound]`. Proof TERM
  sorry-free; sorryAx enters ONLY via the documented holes it consumes (`griego_ak_disjoint` (B1a) +
  witness data `Ubase`/`Qbase`/`Ubase_carryfree`/`an_interval`/`an_index`/`an_shift`).

Two intermediate-statement fixes (recorded in `approaches/lean-c3a-def.md`): exponent `^ n → ^ (n+1)`
(forced by `bk n = tpow Q U n` ⟹ `n+1` factors); single `tₙ` → two witnesses `tsum`/`tdiff` (GHR's
shared `t` needs `|I+B|=|I−B|`, deferred to B3). `bk`/`ak` are now PINNED to the GHR composite shape
(no longer opaque sorry).

### R14 hole inventory (12, all documented)
`realizes_one` (139), `realizableSet_bddAbove` (150); witness data `Ubase`/`Qbase`/`Ubase_carryfree`
(302–304), `an_interval`/`an_index`/`an_shift` (309–311); **B1a `griego_ak_disjoint` (330) — NEW,
the uncached separation/disjointness**; B2 `griego_bounded_doubling` (392), B3
`griego_diff_lower_bound` (401), B4 `griego_card_tendsto` (409).

### R14 promotable (flagged for reviewer)
`setSum_card_decompose` / `setDiff_card_decompose` (+ supports `setSum/Diff_tr_card`,
`setSum/Diff_union`, `setSum/Diff_biUnion`, `setSum/Diff_tr`) — all sorry-free, axiom-clean, general
(not sketch glue), proved in `Sketches/C3aDef.lean`.

---
## R12 record (superseded by R14 above for the build-target/hole lines)

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
