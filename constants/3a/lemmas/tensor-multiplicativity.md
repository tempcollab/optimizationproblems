# Cached lemma — `C3a.tensor_pow_sumset_card` / `tensor_pow_diffset_card` (reviewer-certified, R11)

**Promoted by:** proof-reviewer, Round 11. **Bar:** full bound bar (Lean: `sorry`-free, axiom-clean, statement correct and no stronger than proved, `lake build` reproducible).

## Statements (Lean, exact)
```lean
/-- The carry-free digit embedding `(u,v) ↦ u + Q·v`. -/
def emb (Q : ℤ) (uv : ℤ × ℤ) : ℤ := uv.1 + Q * uv.2
def box (Q : ℤ) (U V : Finset ℤ) : Finset ℤ := (U ×ˢ V).image (emb Q)
def sumset (S : Finset ℤ) : Finset ℤ := Finset.image₂ (· + ·) S S
def diffset (S : Finset ℤ) : Finset ℤ := Finset.image₂ (· - ·) S S
def CarryFree (Q : ℤ) (U : Finset ℤ) : Prop :=
  0 < Q ∧ ∀ a ∈ U, ∀ b ∈ U, 2 * |a + b| < Q ∧ 2 * |a - b| < Q
def tpow (Q : ℤ) (U : Finset ℤ) : ℕ → Finset ℤ
  | 0 => U
  | (k + 1) => box Q U (tpow Q U k)

theorem tensor_pow_sumset_card (Q : ℤ) (U : Finset ℤ) (hcf : CarryFree Q U) :
    ∀ k : ℕ, (sumset (tpow Q U k)).card = (sumset U).card ^ (k + 1)

theorem tensor_pow_diffset_card (Q : ℤ) (U : Finset ℤ) (hcf : CarryFree Q U) :
    ∀ k : ℕ, (diffset (tpow Q U k)).card = (diffset U).card ^ (k + 1)
```
**Where proved:** `constants/3a/lean/Sketches/TensorMultiplicativity.lean`, `namespace C3a`. Build target `lake build C3a` (EXIT 0, 2969 jobs). Mathlib pin: `leanprover/lean4:v4.31.0` (`lean/lake-manifest.json`).

## Reading
For a base set `U` whose `±`-sumsets fit inside one base-`Q` digit (`CarryFree Q U`: `0<Q` and `2|a±b|<Q` for all `a,b ∈ U`), the `k`-fold base-`Q` digit-tensor power `tpow Q U k` has
`|U^{⊗(k+1)} + U^{⊗(k+1)}| = |U+U|^(k+1)` and `|U^{⊗(k+1)} − U^{⊗(k+1)}| = |U−U|^(k+1)`.
This is the FINITE/discrete (counting) half of the GHR θ-realization argument: it preserves the realized exponent `log(|U−U|/|U+U|)/log Q` under the tensor power, so the family realizes θ in the `k→∞` limit. It does NOT define `C_3a` and does NOT contain the sup-realization limit (that real-analysis wrapper remains open).

## Supporting lemmas (also clean and reusable, same file)
- `emb_injOn (Q A B) (hQ : 0<Q) (hbound : ∀ a∈A, ∀ a'∈A, |a-a'|<Q) : Set.InjOn (emb Q) ↑(A ×ˢ B)` — general injectivity engine: only the FIRST-coordinate range `A` must fit one digit; the second factor `B` is unconstrained.
- `sumset_image_eq / diffset_image_eq (Q U V) : sumset/diffset (box Q U V) = box Q (sumset/diffset U) (sumset/diffset V)` — UNCONDITIONAL set identity (pure ring algebra; no gap needed).
- `sumset_card_mul_of_carryfree / diffset_card_mul_of_carryfree (Q U V) (hcf : CarryFree Q U) : (sumset/diffset (box Q U V)).card = (sumset/diffset U).card * (sumset/diffset V).card` — needs only `CarryFree Q U` (first factor).

## Certification (what the reviewer reproduced — R11)
- `lake build C3a` → EXIT 0, "Build completed successfully (2969 jobs)", zero warnings.
- `#print axioms` on all 7 lemmas (`tensor_pow_sumset_card`, `tensor_pow_diffset_card`, `sumset_image_eq`, `diffset_image_eq`, `emb_injOn`, `sumset_card_mul_of_carryfree`, `diffset_card_mul_of_carryfree`) → `[propext, Classical.choice, Quot.sound]` — Mathlib's standard axioms ONLY. NO `sorryAx`, NO `native_decide` axiom, NO custom `axiom`.
- Statements re-derived by hand and confirmed correct and no stronger than proved:
  - `emb_injOn`: `u1+Qv1=u2+Qv2 ⟹ u1−u2 = Q(v2−v1)`; LHS has `|·|<Q`, RHS is a multiple of `Q`, so `v1=v2` hence `u1=u2`. Correct; only the first-coordinate gap is used.
  - `sumset_image_eq`: `(u1+Qv1)+(u2+Qv2)=(u1+u2)+Q(v1+v2)` — set identity unconditional. Correct.
  - card lemmas: injectivity of `emb` on `(sumset U) ×ˢ (sumset V)` needs only `|a−a'| ≤ |a|+|a'| < Q` on the first factor (`2|a|<Q` from `CarryFree Q U`); the second factor is free. Correct — the dropped `hcfV` is genuinely not needed.
  - `tensor_pow_*`: induction on `k`, step = card lemma with base `U` (carry-free) as first factor and the tower `tpow Q U k` (NOT carry-free) as the unconstrained second factor; base case `k=0` is `tpow 0 = U`, `(…).card^1`. Correct.
- The `CarryFree` reshape lifting `0<Q` to a top-level conjunct (vs nested under ∀) is strictly equivalent for nonempty `U` and correct (not weaker) for `U=∅`.

## Scope / caveat
A purely finite/combinatorial Lean theorem. It is the counting identity the GHR limit argument rests on, but it is NOT itself a bound on `C_3a` and does NOT raise `held` — it leaves the sup-realization (`k→∞`) wrapper and the `C_3a` definition open. Any C_3a / GHR sketch can import it for the tensor-power preservation step without re-proving.
