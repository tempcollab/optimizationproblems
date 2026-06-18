# Approach: factors-bridge-max-extract

**Constant:** 53a — Davenport constant of `C_n^3`,
`C_53 = sup_{n>=2} (D(C_n^3)-1)/(n-1)`, repo bounds `3 <= C_53 <= 4`.
**Moves:** upper bound (re-derives, does NOT beat, `C_53 <= 4`).
**Type:** Lean-fit certificate. INFRASTRUCTURE / faithfulness — ties the abstract factor list
of `global_induction` / `c53_le_4_per_n` to the ACTUAL prime factorization of a concrete `n`.
Does NOT move `held` (still 4); a record-break needs a sub-`3p^2` generic `eta(C_p^3)`, the
open BSP-2017 wall. This is conditional on the same zero-sum hypotheses (`hbase`, `hstep`) by
design.

## Idea (closes faithfulness-gap #1)

`global_induction` / `c53_le_4_per_n` (round 3) took an ABSTRACT list `ps : List ℕ` of primes
in `[2, Q]` plus a designated factor `Qn` (image `Q`). True and proved, but it did not yet
*literally* read off the prime factorization of `n`. This approach supplies the bridge:

> For a concrete `n >= 2`, set `L := Nat.primeFactorsList n` (prime factors with multiplicity).
> Take `Qmax := L.maximum_of_length_pos` (the LARGEST prime factor, a genuine element of `L`)
> and `ps := L.erase Qmax`. The permutation `L ~ Qmax :: ps` transports the product, so
> `Qmax * ps.prod = L.prod = n`. Every `p ∈ ps` is in `L`, hence prime (`2 <= p`) and
> `<= Qmax`; `Qmax` is prime so `2 <= Qmax`. Feed `c53_le_4_per_n` with `Q := (Qmax : ℤ)`.

Result: `D n - 1 <= 4 * ((n:ℤ) - 1)`, i.e. `(D(C_n^3) - 1)/(n - 1) <= 4`, read off the
**actual** factorization of `n`, with the modulus `Q` being literally the largest prime factor.

## What COMPILED this round (round 4)

File: `lean/Constants/C53a.lean`. Build target `Constants`. `lake build Constants` green
against pinned Lean v4.31.0 / Mathlib `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`.

New theorem, fully proved (no `sorry`, no axiom beyond the three foundational):

- **`factors_bridge_max (D : ℕ → ℤ) (n : ℕ) (hn : 2 ≤ n) (hbase ...) (hstep ...)`**
  `: D n - 1 ≤ 4 * ((n : ℤ) - 1)`.
  `hbase` and `hstep` are the SAME conditional zero-sum inputs as `global_induction`, here with
  the base-case factor pinned to `Qmax = (primeFactorsList n).maximum_of_length_pos …`.
  Axioms: `[propext, Classical.choice, Quot.sound]`. No `sorryAx`, no problem-specific axiom.

Reuses `c53_le_4_per_n` VERBATIM (the bridge only constructs the `ps`/`Q`/side-condition
arguments from the factorization API and applies it).

Axiom audit: `constants/53a/certificate/axioms.txt`. Genuine recompile confirmed (olean
deleted then rebuilt), not a cache replay.

## Hard step — how it was discharged

The named load-bearing claim was the product re-presentation `n = Qmax * (L.erase Qmax).prod`
via the cons/erase/permutation chain. Discharged as:

```
hperm : List.Perm L (Qmax :: ps) := List.perm_cons_erase hQmem      -- Qmax ∈ L
h1    : L.prod = (Qmax :: ps).prod := hperm.prod_eq                  -- product is perm-invariant
        rw [List.prod_cons] at h1                                    -- (Qmax::ps).prod = Qmax*ps.prod
hLprod: L.prod = n := Nat.prod_primeFactorsList hn0                  -- L.prod = n
=> hprodeq : Qmax * ps.prod = n
```

Membership bookkeeping: `Qmax ∈ L` by `List.maximum_of_length_pos_mem`; each `p ∈ ps` lies in
`L` by `List.mem_of_mem_erase`, giving `Nat.prime_of_mem_primeFactorsList` (=> `2 ≤ p` via
`Nat.Prime.two_le`) and `p ≤ Qmax` via `List.le_maximum_of_length_pos_of_mem`. Nonemptiness for
`n ≥ 2` from `Nat.primeFactorsList_ne_nil` + `List.length_pos_of_ne_nil`.

**Pitfalls hit and fixed (round 4):**
- `List.Perm` infix `~` is not in scope in this file (no `open List`); wrote
  `List.Perm L (Qmax :: ps)` explicitly.
- `Nat.prime_of_mem_primeFactorsList` returns `Nat.Prime p` directly in this Mathlib rev (the
  explorer's note that it gives `_root_.Prime` needing `Nat.prime_iff` was WRONG for fabf563);
  used it directly, no `Nat.prime_iff` bridge.

## Certificate

Lean-fit. Reproduce:
```sh
export PATH="$HOME/.elan/bin:$PATH"
cd /home/agentuser/repo/lean
lake exe cache get        # one-time, fetches pinned Mathlib oleans
lake build Constants      # THE check (prints the #print axioms lines)
```
`#print axioms Constants.C53a.factors_bridge_max` =>
`[propext, Classical.choice, Quot.sound]`.

## §3 subtlety — largest PRIME vs largest prime POWER (honest)

Grinsztajn's `P(n)` is the largest prime POWER `max_{pᵃ ∥ n} pᵃ`. Here `Q = Qmax` is the
largest PRIME. Since largest-prime `<= P(n)` and both `>= 2`, the conclusion `4n - Qmax - 2`
is `>=` Grinsztajn's `4n - P(n) - 2`, but still `<= 4n - 4 = 4(n-1)`. So the record-relevant
corollary `C_53 <= 4` (which uses only `Q >= 2`) is FULLY PRESERVED. This is a faithful-to-
`C_53<=4` statement even though it is not verbatim the `P(n)` form.

## Why this does NOT beat 4 (expected)

Conditional on `hstep` (= Grinsztajn Lemma 2.1 + 2.3, carrying the `+p^2`, i.e.
`eta(C_p^3) <= 3p^2`). Beating 4 needs an unconditional sub-`3p^2` `eta` for all large `p` —
the open BSP-2017 wall (`eta-coefficient-barrier.md`). `held` unchanged at 4.

## What would push it further (next rounds)

1. **Route P (prime-power `P(n)` faithful):** run the induction over the prime-power primary
   components `{p^{v_p(n)}}` to get Grinsztajn's exact `P(n)`. Needs `recursion_step` re-proved
   for prime-power multipliers (multiply by `p^a` in one step or iterate). Mathlib has
   `ordProj`, `Nat.ordProj_mul_ordCompl_eq_self`, `Finset.max'` over `n.primeFactors`.
   Multi-round — parked.
2. **`iSup` packaging (gap #2):** lift the per-`n` bound to the literal `⨆ n, … ≤ 4` over ℝ.
   See sibling slug `isup-packaging-real`.
3. **Faithful `hstep`:** derive `hstep` inside Lean from named Lemma 2.2 (extraction) + Lemma
   2.3, exposing the `eta(C_p^3) <= c*p^2` dependence syntactically (the seed any eta-win
   plugs into).
