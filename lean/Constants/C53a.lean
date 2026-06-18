/-
# Constant 53a — Davenport constant of `C_n^3`

`C_53 = sup_{n >= 2} (D(C_n^3) - 1) / (n - 1)`, repository bounds `3 <= C_53 <= 4`.

This file is the **conditional Lean scaffold** for Grinsztajn's upper bound
`D(C_n^3) <= 4n - P(n) - 2`  (=> `C_53 <= 4`), discovered in

  M. Grinsztajn, *An upper bound for the Davenport constant of `C_n^3`* (2026),
  https://github.com/maaxgrin/davenport-cn3-bound

The paper's deduction is itself shipped as a *conditional* Lean 4 formalization that
**axiomatizes** the zero-sum number-theory inputs (the p-group lower bound, the extraction
lemma, and the local estimate `D_k(C_p^3) <= p*k + p^2`). We do the same here.

## What is GENUINELY PROVED in this file (no `sorry`, no axiom carrying it)

The load-bearing *integer recursion step* of the global factorization induction:

  from `D(C_m^3) <= 4*m - Q - 2`  and the inductive-method step
       `D(C_{p*m}^3) <= p * D(C_m^3) + p^2`,
  with the side condition `2 <= p <= Q`,
  conclude  `D(C_{p*m}^3) <= 4*(p*m) - Q - 2`.

The arithmetic heart of this step is the **comparison inequality**

  `p^2 - 2*p + 2 <= (p - 1) * Q`     for `2 <= p <= Q`,

proved below as `comparison_ineq` by `nlinarith` over `ℤ` (gold-standard: type-checking
*is* the proof; see `#print axioms` at the bottom — only Lean's three foundational axioms).

## What is AXIOMATIZED / hypothesised (the zero-sum number-theory inputs — NOT proved here)

These are Grinsztajn's cited inputs; they are the *hypotheses* of the recursion lemma, never
the load-bearing algebra. They are carried as ordinary Lean hypotheses (not `axiom`s), so the
recursion theorem is honestly *conditional* and its `#print axioms` shows no smuggled input:

  * `D` : the Davenport invariant `m ↦ D(C_m^3)`, modelled as an abstract `ℕ → ℤ`.
  * `hstep`     : the inductive-method + local-estimate step `D(C_{p m}^3) <= p D(C_m^3) + p^2`
                  (Grinsztajn Lemma 2.1 + Lemma 2.3 — zero-sum inputs).
  * `hbase`     : the prime-power base case `D(C_Q^3) = 3 Q - 2` (Gao–Geroldinger; equivalently
                  `4 Q - Q - 2`).
  * the induction hypothesis `hm : D m <= 4*m - Q - 2`.

The repository `held` upper bound `C_53 <= 4` is NOT changed by this file: this is the
certificate *scaffold* for the conditional argument, not a new bound. See the approach doc
`constants/53a/approaches/lean-conditional-scaffold.md`.
-/

import Mathlib.Tactic

-- This file is a self-contained scaffold, not a Mathlib contribution; the Mathlib style
-- header linter (copyright block / module-doc-first) does not apply.
set_option linter.style.header false

namespace Constants.C53a

/-! ## The load-bearing arithmetic: the comparison inequality -/

/-- **Comparison inequality (the load-bearing algebra).**
For integers with `2 <= p` and `p <= Q` we have `p^2 - 2*p + 2 <= (p - 1) * Q`.

Mechanism (Grinsztajn, Section 3): `(p - 1) * Q >= (p - 1) * p = p^2 - p`, and
`p^2 - p - (p^2 - 2*p + 2) = p - 2 >= 0`. Fully proved, no `sorry`. -/
theorem comparison_ineq (p Q : ℤ) (hp : 2 ≤ p) (hpQ : p ≤ Q) :
    p ^ 2 - 2 * p + 2 ≤ (p - 1) * Q := by
  nlinarith [mul_le_mul_of_nonneg_left hpQ (by linarith : (0:ℤ) ≤ p - 1)]

/-! ## The integer recursion step -/

/-- **Recursion step (conditional).**
Let `D : ℕ → ℤ` model `m ↦ D(C_m^3)`.  Assume:

* `hstep : D (p * m) ≤ p * D m + p^2`   — Grinsztajn Lemma 2.1 (inductive method) composed
  with Lemma 2.3 (local estimate `D_k(C_p^3) <= p k + p^2`); these are the **axiomatized
  zero-sum inputs**, carried as a hypothesis.
* `hm    : D m ≤ 4*m - Q - 2`            — the induction hypothesis.
* `hp : 2 ≤ p`, `hpQ : p ≤ Q`            — `p` a prime factor `<= Q = P(n)`.

Then `D (p * m) ≤ 4*(p*m) - Q - 2`: the bound is preserved when `m` is multiplied by `p`.

This is the inductive step of Grinsztajn's global factorization induction over the prime
multiset of `n`. The *arithmetic* (everything after `hstep`/`hm`) is fully proved here; the
zero-sum content lives entirely in the hypotheses. -/
theorem recursion_step
    (D : ℕ → ℤ) (p m Q : ℤ) (pn mn : ℕ)
    (_hpn : (pn : ℤ) = p) (_hmn : (mn : ℤ) = m)
    (hp : 2 ≤ p) (hpQ : p ≤ Q)
    (hstep : D (pn * mn) ≤ p * D mn + p ^ 2)
    (hm : D mn ≤ 4 * m - Q - 2) :
    D (pn * mn) ≤ 4 * (p * m) - Q - 2 := by
  -- `p * D m + p^2 ≤ p*(4m - Q - 2) + p^2 = 4 p m - p Q - 2 p + p^2`
  have hpdm : p * D mn + p ^ 2 ≤ p * (4 * m - Q - 2) + p ^ 2 := by
    have : p * D mn ≤ p * (4 * m - Q - 2) :=
      mul_le_mul_of_nonneg_left hm (by linarith)
    linarith
  -- and `4 p m - p Q - 2 p + p^2 ≤ 4 p m - Q - 2` ⟺ `p^2 - 2 p + 2 ≤ (p-1) Q`.
  have hcmp : p ^ 2 - 2 * p + 2 ≤ (p - 1) * Q := comparison_ineq p Q hp hpQ
  have hchain : p * (4 * m - Q - 2) + p ^ 2 ≤ 4 * (p * m) - Q - 2 := by nlinarith [hcmp]
  calc D (pn * mn) ≤ p * D mn + p ^ 2 := hstep
    _ ≤ p * (4 * m - Q - 2) + p ^ 2 := hpdm
    _ ≤ 4 * (p * m) - Q - 2 := hchain

/-! ## The conditional global bound, packaged

A convenience statement: starting from the prime-power base case `D(C_Q^3) = 3 Q - 2`
(= `4 Q - Q - 2`), one `recursion_step` advances the bound by one prime factor. This packages
the base + a single step so the shape of the eventual factorization induction is visible.
The full induction over the prime multiset is carried forward (see the approach doc). -/

/-- Base case is in the `4 m - Q - 2` form. -/
theorem base_in_form (D : ℕ → ℤ) (Q : ℤ) (Qn : ℕ) (_hQn : (Qn : ℤ) = Q)
    (hbase : D Qn = 3 * Q - 2) : D Qn ≤ 4 * Q - Q - 2 := by
  rw [hbase]; linarith

/-! ## The ℕ/ℤ coercion bridge for the running product accumulator

The fold below threads a running **ℕ** product (the argument of `D : ℕ → ℤ`) while the bound
arithmetic lives in **ℤ**. The single load-bearing cast fact is that the ℕ→ℤ ring hom commutes
with the running product, so the ℤ-image of `Qn * (ps.prod)` is `(Qn:ℤ) * (ps.prod:ℤ)`. We
isolate it as `acc_cast_bridge`; it is closed by `push_cast` (which knows `Nat.cast_mul` and
`Nat.cast_list_prod`/`Nat.cast_prod` for the ℕ→ℤ cast over `List.prod`). -/

/-- **Cast bridge (the named hard step), proved.**
The ℤ-image of the ℕ running product `Qn * ps.prod` is `(Qn:ℤ) * ps.prod`, where the right-hand
`ps.prod` is the product of the ℤ-cast list. This is what lets each cons of the fold hand
`recursion_step` a coercion witness `((ℕ-product):ℤ) = m`. Proved by `push_cast`; depends only
on the three Lean foundational axioms. -/
theorem acc_cast_bridge (Qn : ℕ) (ps : List ℕ) :
    ((Qn * ps.prod : ℕ) : ℤ) = (Qn : ℤ) * ((ps.map (Nat.cast : ℕ → ℤ)).prod) := by
  have hprod : ((ps.prod : ℕ) : ℤ) = (ps.map (Nat.cast : ℕ → ℤ)).prod := by
    have h := map_list_prod (Nat.castRingHom ℤ) ps
    -- `⇑(Nat.castRingHom ℤ) = (Nat.cast : ℕ → ℤ)` definitionally; align the map functions.
    simpa only [Nat.coe_castRingHom] using h
  rw [Nat.cast_mul, hprod]

/-! ## The global factorization induction (the conditional global bound)

We fold `recursion_step` over a `List ℕ` of prime factors, with `base_in_form` as the base
case. The zero-sum number-theory input stays an **explicit hypothesis** `hstep` (universally
quantified over the factor and the running modulus), so the theorem is honestly *conditional*
and `#print axioms` shows no smuggled problem-specific axiom. -/

/-- **Global factorization induction (conditional).**
Let `D : ℕ → ℤ` model `m ↦ D(C_m^3)`, let `Q = P(n)` be the largest prime factor (carried as an
integer `Q` with its ℕ witness `Qn`), and let `ps : List ℕ` be the remaining prime factors,
each `2 ≤ p ≤ Q`. Assume:

* `hbase : D Qn = 3*Q - 2`  — the prime-power base case (Gao–Geroldinger), i.e. `4Q - Q - 2`.
* `hstep : ∀ p m, D (p*m) ≤ p*D m + p^2` — Grinsztajn Lemma 2.1 (inductive method) + Lemma 2.3
  (local estimate `D_k(C_p^3) ≤ p k + p^2`); the **zero-sum inputs**, carried as a hypothesis.
* `hps : ∀ p ∈ ps, 2 ≤ (p:ℤ) ∧ (p:ℤ) ≤ Q`  — every remaining prime factor is in `[2, Q]`.

Then, writing `n = Qn * ps.prod`,
`D n ≤ 4*(Q * ps.prod) - Q - 2`, where `ps.prod` on the RHS is the ℤ-cast product.

This is exactly `D(C_n^3) ≤ 4n - P(n) - 2` once `ps` is the multiset of prime factors of `n`
other than the largest (carried forward to the multiset variant). The induction folds the
already-proved `recursion_step` (cons step) over `base_in_form` (base), threading the running
product through `acc_cast_bridge`. Fully proved; no `sorry`, no axiom. -/
theorem global_induction
    (D : ℕ → ℤ) (Q : ℤ) (Qn : ℕ) (hQn : (Qn : ℤ) = Q)
    (hbase : D Qn = 3 * Q - 2)
    (hstep : ∀ (p m : ℕ), D (p * m) ≤ (p : ℤ) * D m + (p : ℤ) ^ 2) :
    ∀ (ps : List ℕ), (∀ p ∈ ps, 2 ≤ (p : ℤ) ∧ (p : ℤ) ≤ Q) →
      D (Qn * ps.prod) ≤ 4 * (Q * (ps.map (Nat.cast : ℕ → ℤ)).prod) - Q - 2 := by
  intro ps
  induction ps with
  | nil =>
      intro _
      -- empty product: `n = Qn`, RHS = `4*Q - Q - 2`; this is `base_in_form`.
      simpa using base_in_form D Q Qn hQn hbase
  | cons p ps ih =>
      intro hps
      -- split the per-element hypothesis into head and tail.
      have hp_head : 2 ≤ (p : ℤ) ∧ (p : ℤ) ≤ Q := hps p (by simp)
      have hps_tail : ∀ q ∈ ps, 2 ≤ (q : ℤ) ∧ (q : ℤ) ≤ Q := fun q hq =>
        hps q (by simp [hq])
      -- inductive hypothesis on the tail product.
      have htail := ih hps_tail
      -- the running ℤ-modulus `m` is the tail product times Q.
      set Mℤ : ℤ := (ps.map (Nat.cast : ℕ → ℤ)).prod with hMℤ
      -- abbreviate the ℕ tail product accumulator.
      set Mn : ℕ := Qn * ps.prod with hMn
      -- cast witnesses for `recursion_step`.
      have hpn : ((p : ℕ) : ℤ) = (p : ℤ) := rfl
      have hmn : ((Mn : ℕ) : ℤ) = Q * Mℤ := by
        rw [hMn, acc_cast_bridge, hQn]
      -- `recursion_step` with modulus `m := Q * Mℤ`, prime `p`, side condition from `hp_head`.
      have hstep' : D (p * Mn) ≤ (p : ℤ) * D Mn + (p : ℤ) ^ 2 := hstep p Mn
      -- induction hypothesis in the `4*m - Q - 2` shape (`m = Q * Mℤ`).
      have hm' : D Mn ≤ 4 * (Q * Mℤ) - Q - 2 := htail
      have key :
          D (p * Mn) ≤ 4 * ((p : ℤ) * (Q * Mℤ)) - Q - 2 :=
        recursion_step D (p : ℤ) (Q * Mℤ) Q p Mn hpn hmn
          hp_head.1 hp_head.2 hstep' hm'
      -- rewrite the goal's product `(p :: ps).prod = p * ps.prod` and match shapes.
      have hprod_n : (Qn * (p :: ps).prod) = p * Mn := by
        simp [hMn, List.prod_cons]; ring
      have hprod_z :
          ((p :: ps).map (Nat.cast : ℕ → ℤ)).prod = (p : ℤ) * Mℤ := by
        simp [hMℤ, List.prod_cons]
      rw [hprod_n, hprod_z]
      -- `4*(Q * (p*Mℤ)) - Q - 2 = 4*(p*(Q*Mℤ)) - Q - 2`.
      have : 4 * (Q * ((p : ℤ) * Mℤ)) - Q - 2 = 4 * ((p : ℤ) * (Q * Mℤ)) - Q - 2 := by ring
      rw [this]
      exact key

/-! ## The `C_53 ≤ 4` corollary (per-`n` inequality form)

`C_53 = sup_{n≥2} (D(C_n^3) - 1)/(n-1)`. The bound `C_53 ≤ 4` is the per-`n` statement
`D(C_n^3) - 1 ≤ 4*(n - 1)`, i.e. `D(C_n^3) ≤ 4n - 3`. From `global_induction`'s
`D n ≤ 4n - Q - 2` with `Q = P(n) ≥ 2` this is immediate (`4n - Q - 2 ≤ 4n - 4 = 4(n-1)`,
which is `≤ 4n - 3`). We phrase it on the ℕ `n = Qn * ps.prod`, rewriting the product RHS to
the ℤ-image of `n` via `acc_cast_bridge`, so the conclusion is about `(n : ℤ)`. No `sup`/`iSup`
is formalized (that is multi-round bookkeeping); this is the load-bearing per-`n` inequality. -/

/-- **`C_53 ≤ 4`, per-`n` form (conditional).**
Under the same hypotheses as `global_induction`, and `2 ≤ Q` (the largest prime factor is at
least 2 for `n ≥ 2`), writing `n = Qn * ps.prod` we have `D n - 1 ≤ 4 * ((n : ℤ) - 1)`.
This is `(D(C_n^3) - 1)/(n-1) ≤ 4`, the inequality whose sup over `n ≥ 2` is `C_53 ≤ 4`. -/
theorem c53_le_4_per_n
    (D : ℕ → ℤ) (Q : ℤ) (Qn : ℕ) (hQn : (Qn : ℤ) = Q)
    (hQ2 : 2 ≤ Q)
    (hbase : D Qn = 3 * Q - 2)
    (hstep : ∀ (p m : ℕ), D (p * m) ≤ (p : ℤ) * D m + (p : ℤ) ^ 2)
    (ps : List ℕ) (hps : ∀ p ∈ ps, 2 ≤ (p : ℤ) ∧ (p : ℤ) ≤ Q) :
    D (Qn * ps.prod) - 1 ≤ 4 * (((Qn * ps.prod : ℕ) : ℤ) - 1) := by
  have hgi := global_induction D Q Qn hQn hbase hstep ps hps
  -- `acc_cast_bridge` (with `hQn`) gives `(n:ℤ) = Q * (ps.prod cast)`, so the RHS of `hgi`
  -- equals `4 * (n:ℤ) - Q - 2`.
  have hbridge : ((Qn * ps.prod : ℕ) : ℤ) = Q * (ps.map (Nat.cast : ℕ → ℤ)).prod := by
    rw [acc_cast_bridge, hQn]
  -- now combine: `D n ≤ 4*(n:ℤ) - Q - 2` and `2 ≤ Q` give `D n - 1 ≤ 4*((n:ℤ) - 1)`.
  rw [hbridge]
  linarith [hgi, hQ2]

end Constants.C53a

-- Axiom audit of the load-bearing recursion step. Expect ONLY the three Lean foundational
-- axioms (`propext`, `Classical.choice`, `Quot.sound`) — no `sorryAx`, no smuggled input.
#print axioms Constants.C53a.recursion_step
#print axioms Constants.C53a.comparison_ineq
#print axioms Constants.C53a.acc_cast_bridge
#print axioms Constants.C53a.global_induction
#print axioms Constants.C53a.c53_le_4_per_n
