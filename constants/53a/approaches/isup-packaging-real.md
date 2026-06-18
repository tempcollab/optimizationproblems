# isup-packaging-real — package the conditional bound into the real-valued ratio

**Angle.** Faithfulness-gap #2 (distinct from the factorization gap #1 that
`factors-bridge-max-extract` closes). `C_53 = sup_{n ≥ 2} (D(C_n^3) − 1)/(n − 1)` is a
supremum of a **real-valued** ratio, but every scaffold theorem lives over `ℤ`
(`c53_le_4_per_n`, `factors_bridge_max` conclude `D n − 1 ≤ 4*((n:ℤ) − 1)`). This angle ties
the conditional bound to the literal ℝ ratio `r n = ((D n : ℝ) − 1) / ((n : ℝ) − 1)` whose
supremum *is* `C_53`.

**Status: BUILT (Round 4) — per-`n` ℝ ratio bound, scoped.** `lake build Constants` green;
new top-level theorem `c53_ratio_real_le` depends only on `[propext, Classical.choice,
Quot.sound]` (no `sorryAx`, no smuggled axiom). This is an infrastructure/faithfulness
increment; it does **NOT** move `held` below 4 (record-break is blocked on the open
eta-coefficient problem, re-confirmed by the explorer this round).

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

## Honest scope / what is deferred

The full `⨆`/`iSup`-over-ℝ packaging `(⨆ n, r n) ≤ 4` is **NOT** formalized. The supremum is
over the restricted domain `n ≥ 2` (not all `n : ℕ`) — the `iSup`-domain-restriction wrinkle
the explorer/outline-reviewer flagged as multi-round. Landing it needs a guarded/subtype sup
plus a `ciSup_le` boundedness argument (and a choice of value for excluded `n < 2`). Scoped
out deliberately this round per the reviewer's guidance ("land step 2, defer `ciSup_le`"); the
per-`n` ratio bound is the load-bearing fact and is the honest, fully-verified increment.

## What would push it further

1. **Define `r : ℕ → ℝ`** with a guard (e.g. `r n = if 2 ≤ n then ((D n:ℝ)−1)/((n:ℝ)−1)
   else 0`) and prove `∀ n, r n ≤ 4` (combining `c53_ratio_real_le` with the trivial `n < 2`
   branch), then `ciSup_le` to get `(⨆ n, r n) ≤ 4`. This is the next one-round increment for
   this slug. Watch: `ciSup_le` needs `BddAbove`/the explicit per-term bound; verify the
   `0`-padding does not raise the sup (it does not, `0 ≤ 4`).
2. **Plug in the real `D`** once the zero-sum inputs (`hbase`/`hstep`) are themselves
   formalized — currently conditional hypotheses (Grinsztajn's axiomatized inputs).
3. Independent of the eta barrier: any future sub-`3p^2` eta breakthrough that lowers the
   constant plugs in *above* `hstep`; this ℝ packaging is the bottom layer and survives.

## Certificate

- Build target: `lake build Constants` from `/home/agentuser/repo/lean`
  (`elan`/`lake` in `~/.elan/bin`).
- `#print axioms Constants.C53a.c53_ratio_real_le` →
  `[propext, Classical.choice, Quot.sound]`.
- Recorded in `constants/53a/certificate/` (build target + axioms line).
