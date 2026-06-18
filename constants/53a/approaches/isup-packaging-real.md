# isup-packaging-real — package the conditional bound into the real-valued ratio

**Angle.** Faithfulness-gap #2 (distinct from the factorization gap #1 that
`factors-bridge-max-extract` closes). `C_53 = sup_{n ≥ 2} (D(C_n^3) − 1)/(n − 1)` is a
supremum of a **real-valued** ratio, but every scaffold theorem lives over `ℤ`
(`c53_le_4_per_n`, `factors_bridge_max` conclude `D n − 1 ≤ 4*((n:ℤ) − 1)`). This angle ties
the conditional bound to the literal ℝ ratio `r n = ((D n : ℝ) − 1) / ((n : ℝ) − 1)` whose
supremum *is* `C_53`.

**Status: BUILT (Round 5) — full iSup-over-ℝ capstone, faithfulness-gap #2 CLOSED.**
`lake build Constants` green (2968 jobs, no warnings); the new top-level theorems
`c53Ratio_le`, `c53_isup_real_le`, `C53_le_4` all depend only on `[propext,
Classical.choice, Quot.sound]` (no `sorryAx`, no smuggled axiom). The Lean theorem now
literally states the bound as a supremum: `(⨆ n, c53Ratio D n) ≤ 4`, i.e.
`C_53 = sup_{n≥2} (D(C_n^3)−1)/(n−1) ≤ 4`. This is the infrastructure/faithfulness CAPSTONE;
it does **NOT** move `held` below 4 (record-break is blocked on the open eta-coefficient
problem, re-confirmed by the explorer this round) — still `≤ 4`, not sub-4, still conditional
on `hbase`/`hstep`.

**Status: BUILT (Round 4) — per-`n` ℝ ratio bound, scoped.** `lake build Constants` green;
top-level theorem `c53_ratio_real_le` depends only on `[propext, Classical.choice,
Quot.sound]` (no `sorryAx`, no smuggled axiom). This is the load-bearing per-`n` fact the
Round-5 capstone now lifts to the supremum.

## What was built this round

New theorem in `lean/Constants/C53a.lean` (downstream of `factors_bridge_max`, which another
builder added the same round — no collision, separate region):

```
theorem c53_ratio_real_le
    (D : ℕ → ℤ) (n : ℕ) (hn : 2 ≤ n)
    (hbase : D (largest prime factor of n) = 3 * (largest prime factor of n : ℤ) - 2)
    (hstep : ∀ (p m : ℕ), D (p * m) ≤ (p : ℤ) * D m + (p : ℤ) ^ 2) :
    ((D n : ℝ) - 1) / ((n : ℝ) - 1) ≤ 4
```

Reuses `factors_bridge_max` verbatim for the integer per-`n` bound, then bridges to ℝ:
- cast the ℤ inequality `D n − 1 ≤ 4*((n:ℤ) − 1)` to ℝ via `exact_mod_cast`;
- `(n:ℝ) − 1 > 0` from `n ≥ 2`;
- `div_le_iff₀ (hc : 0 < c) : b / c ≤ a ↔ b ≤ a * c`
  (`Mathlib.Algebra.Order.GroupWithZero.Basic`, present in pinned rev `fabf563`), then
  `linarith`.

Conclusion is the literal `n`-th term of the family whose sup is `C_53`, read off the actual
prime factorization of `n` (via the `factors_bridge_max` reuse).

## What was built in Round 5 — the iSup capstone

Single downstream addition to `lean/Constants/C53a.lean` (below `c53_ratio_real_le`):

```
noncomputable def c53Ratio (D : ℕ → ℤ) (n : ℕ) : ℝ :=
  if 2 ≤ n then ((D n : ℝ) - 1) / ((n : ℝ) - 1) else 0

theorem c53Ratio_le (D) (hbase : ∀ n (hn : 2 ≤ n), …) (hstep …) : ∀ n, c53Ratio D n ≤ 4
  -- intro n; unfold; split_ifs:
  --   2 ≤ n  branch: c53_ratio_real_le D n h (hbase n h) hstep   (VERBATIM reuse)
  --   n < 2  branch: 0 ≤ 4 by norm_num

theorem c53_isup_real_le (D) (hbase …) (hstep …) : (⨆ n, c53Ratio D n) ≤ 4
  := ciSup_le (c53Ratio_le D hbase hstep)

noncomputable def C53 (D : ℕ → ℤ) : ℝ := ⨆ n, c53Ratio D n
theorem C53_le_4 (D) (hbase …) (hstep …) : C53 D ≤ 4 := c53_isup_real_le D hbase hstep
```

The R4-deferred obstacle dissolved exactly as the outline-reviewer verified: the pinned
Mathlib `ciSup_le [Nonempty ι] (H : ∀ x, f x ≤ c) : iSup f ≤ c`
(`Mathlib/Order/ConditionallyCompleteLattice/Indexed.lean:139`) carries **no** separate
`BddAbove` obligation — the per-term bound `∀ n, c53Ratio D n ≤ 4` *is* the boundedness, and
`[Nonempty ℕ]` is an existing instance. So the whole step reduced to the two-branch
`split_ifs` plus the verbatim `c53_ratio_real_le` reuse. The `0`-padding for `n < 2` cannot
raise the sup (`0 ≤ 4`).

`hbase` is now **universally quantified** over all valid `n ≥ 2` (same per-`n` base
expression, `∀`'d) — the single honest input the supremum statement requires. `hstep`
unchanged. Both remain explicit Lean hypotheses; the bound 4 is re-derived, not smuggled.

**Non-vacuity.** The family is over a non-empty honest domain (`n = 2` included), and the
R4 zero-sum witness `D m = 3m − 2` gives ratio `3 ≤ 4` (a genuine non-padded value) — the
supremum bounds a real family, not a vacuous `⨆` of zeros.

The `c53-statement-tie` companion (named `def C53` + `C53_le_4`) was folded in here per the
outline-reviewer's instruction (same file, cheap).

## What would push it further

1. **Plug in the real `D`** once the zero-sum inputs (`hbase`/`hstep`) are themselves
   formalized — currently conditional hypotheses (Grinsztajn's axiomatized inputs).
3. Independent of the eta barrier: any future sub-`3p^2` eta breakthrough that lowers the
   constant plugs in *above* `hstep`; this ℝ packaging is the bottom layer and survives.

## Certificate

- Build target: `lake build Constants` from `/home/agentuser/repo/lean`
  (`elan`/`lake` in `~/.elan/bin`).
- `#print axioms Constants.C53a.c53_ratio_real_le` →
  `[propext, Classical.choice, Quot.sound]`.
- Recorded in `constants/53a/certificate/` (build target + axioms line).
