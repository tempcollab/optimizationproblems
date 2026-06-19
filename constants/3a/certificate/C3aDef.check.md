# Lean certificate record — `lean-c3a-def` (scoped DEFINITION-only sketch)

- **Lake project:** `constants/3a/lean/` (Lean v4.31.0; Mathlib pinned to the `v4.31.0` tag, rev
  `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`). Sketch file
  `constants/3a/lean/Sketches/C3aDef.lean`, imported via the C3a lib glob and the root `C3a.lean`.
- **Build target:** `lake build C3a` (run with `~/.elan/bin/lake`). **R18: EXIT 0, 2970 jobs.**
  `Build completed successfully (2970 jobs).` Remaining `declaration uses 'sorry'` warnings at
  C3aDef.lean:139,150,302,303,304,315,318,323,324,705,714,722 — all documented witness-data / B2-B4
  holes; no smuggled `sorry`. (Lines for `box_elem_range`/`tpow_elem_range`/`an_separated` are NO
  LONGER in the list — closed this round R18.)

## R18 — `an_separated` CLOSED (the residual construction obligation of B1a)
The three R18 sub-holes are all closed sorry-free on their own path:
- `box_elem_range` (the `box`/`emb` step range bound) — `[propext, Classical.choice, Quot.sound]`
  (**NO sorryAx — fully axiom-clean, general, PROMOTABLE**).
- `maxbk_nonneg` (closed-form tower bound nonneg) — `[propext, Classical.choice, Quot.sound]`
  (**NO sorryAx — PROMOTABLE**).
- `tpow_elem_range` (the induction on `tpow`), `setSum_bk_within`/`setDiff_bk_within`,
  `an_shift_spacing`, `an_shift_nonneg`, `interval_union_disjoint_sum`/`_diff`, and `an_separated`
  itself — each `[propext, sorryAx, Classical.choice, Quot.sound]`. Proof TERMS are sorry-free; the
  `sorryAx` enters ONLY via the documented numeric witness-data holes they consume (`Ubase`/`Qbase`/
  `Ubase_carryfree`/`maxUbase`/`Ubase_range`/`mnData`/`negLoData`). This is the R14/R15 honest
  pattern. `griego_ak_disjoint` (B1a) is now fully reassembled from `an_separated` + the cached
  spacing lemmas, so B1a→B1 is a sorry-free chain modulo the witness data.

Mechanism (all in `Sketches/C3aDef.lean`, lines ~468–636):
- `box_elem_range`: `z ∈ box Q U V ⟹ z = u+Q·v`, `mem_image`/`mem_product` + `mul_le_mul_of_nonneg_left`.
- `tpow_elem_range`: `induction n`; base = `hbase` (`Ubase ⊆ [0,maxU]`); step = `box_elem_range` with
  the IH range of the tower as second factor, `0 ≤ Qbase` from `Ubase_carryfree.1`. `maxbk` closed
  form `maxbk maxU Q (k+1) = maxU + Q·(maxbk maxU Q k)`.
- WithinDiam: `setSum (bk n)(bk n) ⊆ [0,2·maxbk n]`, `setDiff ⊆ [−maxbk n, maxbk n]` (diam `2·maxbk n`).
- Witness shape PINNED: `an_shift n i = i·(2·maxbk n+1)` (AP), `an_index n = range (mnData n)`,
  `an_interval n = Icc (negLoData n) (−(2·maxbk n+1))` (band strictly below all translate windows).
  Only the numeric counts `maxUbase`/`mnData`/`negLoData` and `Ubase`/`Qbase` stay documented `sorry`.
- Spacing: `|an_shift n i − an_shift n j| = |i−j|·(2·maxbk n+1) ≥ 2·maxbk n+1 > 2·maxbk n = diam`.
- Interval-vs-union: `disjoint_biUnion_right` + `disjoint_left`; sum side — interval-sum `< 0` ≤
  translate-sum (shift ≥ 0, window ≥ 0); diff side — interval-diff `< −maxbk n` ≤ translate-diff
  (shift ≥ 0, window ≥ −maxbk n). Pure ℤ interval `omega`.

### R18 promotable (flagged for reviewer)
`box_elem_range` and `maxbk_nonneg` — fully general, sorry-free, axiom-clean
(`[propext, Classical.choice, Quot.sound]`), proved in `Sketches/C3aDef.lean`. Reusable element-range
bound for any digit-tensor `box`/`emb` tower.

---
## R15 (superseded by R18 for the build-target/hole lines)

### R15 — sub-hole B1a spacing lemmas CLOSED
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
