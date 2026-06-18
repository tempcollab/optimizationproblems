# Approach: global-induction-list-fold

**Constant:** 53a — Davenport constant of `C_n^3`,
`C_53 = sup_{n>=2} (D(C_n^3)-1)/(n-1)`, repo bounds `3 <= C_53 <= 4`.
**Moves:** upper bound (re-derives, does NOT beat, `C_53 <= 4`).
**Type:** Lean-fit certificate. INFRASTRUCTURE — lifts the round-2 recursion step to the full
factorization induction. Does not move `held` (still 4); a record-break needs a sub-`3p^2`
generic `eta(C_p^3)`, the open BSP-2017 wall.

## Idea

Fold the already-proved `recursion_step` (round 2) over a `List ℕ` of prime factors, with
`base_in_form` as the base case, to obtain Grinsztajn's global bound shape
`D(C_n^3) <= 4n - P(n) - 2` for `n = Qn * ps.prod` (`Q = P(n)` the largest prime factor,
`ps` the remaining factors each `<= Q`). The zero-sum number-theory inputs stay EXPLICIT
hypotheses (`hbase`, `hstep`), so the theorem is honestly conditional and `#print axioms`
shows no smuggled problem axiom.

## What COMPILED this round (round 3)

File: `lean/Constants/C53a.lean`. Build target `Constants`. `lake build Constants` green
against pinned Lean v4.31.0 / Mathlib `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f`.

New theorems, all fully proved (no `sorry`, no axiom):

- **`acc_cast_bridge`** (the named hard step — the ℕ/ℤ coercion bridge):
  `((Qn * ps.prod : ℕ) : ℤ) = (Qn:ℤ) * (ps.map (Nat.cast : ℕ → ℤ)).prod`.
  Mechanism: `map_list_prod (Nat.castRingHom ℤ) ps` (the ℕ→ℤ ring hom commutes with
  `List.prod`), `Nat.coe_castRingHom` to align `⇑(Nat.castRingHom ℤ)` with `Nat.cast`, then
  `Nat.cast_mul`. Axioms: `[propext]` only.
- **`global_induction`** (the core fold, conditional):
  `∀ ps, (∀ p ∈ ps, 2 ≤ (p:ℤ) ∧ (p:ℤ) ≤ Q) →`
  `D (Qn * ps.prod) ≤ 4 * (Q * (ps.map (Nat.cast).prod)) - Q - 2`,
  given `hbase : D Qn = 3*Q - 2` and `hstep : ∀ p m, D (p*m) ≤ p*D m + p^2`.
  Proof: `List.rec`; `nil` = `base_in_form`; `cons p ps` applies `recursion_step` with
  modulus `m := Q * (tail ℤ-product)` and the head prime, threading the ℕ accumulator
  `Mn = Qn * ps.prod` and its ℤ-image via `acc_cast_bridge`. Reuses `recursion_step` and
  `base_in_form` VERBATIM (not modified/weakened). Axioms:
  `[propext, Classical.choice, Quot.sound]`.
- **`c53_le_4_per_n`** (stretch goal — the `C_53 <= 4` per-`n` inequality):
  under the same hypotheses plus `2 ≤ Q`, `D (Qn*ps.prod) - 1 ≤ 4 * ((n:ℤ) - 1)` where
  `n = Qn * ps.prod`. This is `(D(C_n^3)-1)/(n-1) <= 4` per `n`. From `global_induction`
  (`D n <= 4n - Q - 2`) + `Q >= 2` by `linarith` after rewriting the RHS product to `(n:ℤ)`
  via `acc_cast_bridge`. NO `sup`/`iSup` formalized (deliberately — multi-round bookkeeping).
  Axioms: `[propext, Classical.choice, Quot.sound]`.

Axiom audit: `constants/53a/certificate/axioms.txt`. No `sorryAx`, no problem-specific axiom.

## Hard step — how it was discharged

The named load-bearing claim (outline-reviewer / explorer) was the ℕ/ℤ product-accumulator
bridge: `D : ℕ → ℤ` eats a ℕ product but the bound lives in ℤ, so each cons must hand
`recursion_step` a witness `((ℕ-product):ℤ) = m`. Isolated as `acc_cast_bridge` and proved
via `map_list_prod (Nat.castRingHom ℤ)`. **Pitfall hit and fixed:** writing the cast map as
`fun k => (k : ℤ)` made Lean elaborate the `(k:ℤ)` ascription through `do`/monad notation,
producing a `List.flatMap (fun a => [↑a])` mismatch against `List.map Nat.cast`. Switching the
map function to the explicit `(Nat.cast : ℕ → ℤ)` everywhere fixed it. Also `List.mem_cons_self`
is a plain term (not a function) in this Mathlib rev — used `by simp` for the membership goals.

## Certificate

Lean-fit. Reproduce:
```sh
export PATH="$HOME/.elan/bin:$PATH"
cd /home/agentuser/repo/lean
lake exe cache get        # one-time, fetches pinned Mathlib oleans
lake build Constants      # THE check (prints the #print axioms lines)
```

## Why this does NOT beat 4 (expected)

The fold re-derives `C_53 <= 4` conditionally on `hstep` (= Grinsztajn Lemma 2.1 + 2.3, which
carries the `+p^2` term, i.e. `eta(C_p^3) <= 3p^2`). Beating 4 needs an unconditional
sub-`3p^2` `eta` for all large `p` — the open BSP-2017 wall (`eta-coefficient-barrier.md`).
`held` unchanged at 4.

## What is carried FORWARD (next rounds)

1. **multiset-induction-variant** (registered, deferred): tie `ps` to the ACTUAL prime
   multiset of `n` via `Nat.factors`/`Nat.prod_factors`, identify `Q = P(n)` (argmax of the
   factors) and prove `every other factor <= Q` and `n = Q * (rest).prod`, then reduce to
   `global_induction`. This makes the conclusion literally about `n` rather than an abstract
   `Qn * ps.prod`.
2. **`sup`/`iSup` packaging**: lift `c53_le_4_per_n` to `C_53 <= 4` as an `iSup` over ℝ
   (needs `iSup_le` over `n >= 2`). Deliberately deferred — not one-round bookkeeping.
3. **Faithful `hstep`**: derive `hstep` inside Lean from named Lemma 2.2 (extraction) + Lemma
   2.3 (`D_k(C_p^3) <= p k + p^2`) hypotheses so the `eta(C_p^3) <= c*p^2` dependence is
   syntactically exposed (the seed any eta-win plugs into).
