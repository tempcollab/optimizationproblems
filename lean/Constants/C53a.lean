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

end Constants.C53a

-- Axiom audit of the load-bearing recursion step. Expect ONLY the three Lean foundational
-- axioms (`propext`, `Classical.choice`, `Quot.sound`) — no `sorryAx`, no smuggled input.
#print axioms Constants.C53a.recursion_step
#print axioms Constants.C53a.comparison_ineq
