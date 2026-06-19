/-
  Sketch `lean-tensor-multiplicativity` — the FINITE/DISCRETE half of the GHR bridge.

  Context. The held bound C_3a > 1.1774 is carried by a Python big-integer certificate, and the
  companion sketch `lean-native-decide-smallmt` machine-checks the integer core
  `D^10000 > S^10000·Q^1771` (θ > 1.1771) hole-free with `native_decide`. The SOLE remaining hole
  to a self-contained Lean theorem is the GHR2007 read-off `ghr : θ ≤ C3aReal`, which the explorer
  judged (R9) to be multi-round real-analysis infra: a Lean DEFINITION of C_3a (a sup/limsup over
  arbitrarily large constructions) PLUS the k→∞ tensor-power limit argument.

  THIS sketch chips the FINITE, Lean-fit half off that hole, independent of the C_3a sup definition:
  the **carry-free tensor-power multiplicativity**

        |U^{⊗(k+1)} + U^{⊗(k+1)}| = |U+U|^(k+1)   and   |U^{⊗(k+1)} - U^{⊗(k+1)}| = |U-U|^(k+1),

  where U^{⊗(k+1)} is the base-Q digit-product of U (Q = 2·max(U)+1 makes the digit map injective and
  carry-free). This is pure additive combinatorics / counting — no real analysis, no sup. It is the
  step that lets the realized exponent log(D/S)/log Q be PRESERVED under the k-fold product (so the
  family realizes θ in the limit). Once this is a Lean theorem, the only thing left in `ghr` is the
  real-analysis sup-realization wrapper (the genuinely multi-round piece) — i.e. this sketch turns
  the GHR hole from "counting + sup-limit, both open" into "sup-limit only".

  ===========================================================================================
  THE LOAD-BEARING CLAIM, isolated as a clean finite statement.

  Work over ℤ. The embedding  φ : (u,v) ↦ u + Q·v  respects ±-sumsets UNCONDITIONALLY (pure ring
  algebra: (u₁+Q·v₁) ± (u₂+Q·v₂) = (u₁±u₂) + Q·(v₁±v₂)):

        φ(U×V) ± φ(U×V)  =  φ((U±U) × (V±V))      (as finite sets — see `sumset_image_eq`).

  The carry-free gap condition `CarryFree Q U` (2·|a±b| < Q for all a,b ∈ U, and 0 < Q) is needed
  only to turn the SET identity into a CARDINALITY identity: it makes φ injective on the relevant
  box (no carry from the first coordinate reaches the second), so

        |φ(U×V) + φ(U×V)| = |U+U|·|V+V|,   |φ(U×V) - φ(U×V)| = |U-U|·|V-V|.

  KEY OBSERVATION (intermediate-statement search, R9): the cardinality lemma only needs
  `CarryFree Q U` — the SECOND factor V is unconstrained, because injectivity of φ on
  (U±U) ×ˢ (V±V) only needs the FIRST coordinate range (U±U) to fit inside one "digit" (|·| < Q/2).
  This is exactly what lets the k-fold induction go through: in `tpow Q U (k+1) = box Q U (tpow Q U k)`
  the base set U (always carry-free at Q) is the first factor, and the tower `tpow Q U k` — which is
  NOT carry-free at Q — is only ever the second factor. So no CarryFree propagation through the tower
  is required (the "second subtlety" flagged in the plan dissolves once HOLE 3/4 drop their `hcfV`).

  Iterating gives `|U^{⊗(k+1)} ± U^{⊗(k+1)}| = |U±U|^(k+1)`.

  WHY IT IS LEAN-FIT (finite/discrete): every object is a `Finset ℤ`; the sumset is
  `Finset.image₂ (·+·)`; the carry-free condition is a single arithmetic inequality on `Q`;
  injectivity of `u + Q·v` under that condition is elementary integer arithmetic. NO continuum
  estimate appears.

  ===========================================================================================
  STATUS (R9): ALL 7 holes CLOSED, sorry-free. `lake build C3a` EXIT 0;
  `#print axioms C3a.tensor_pow_sumset_card` / `C3a.tensor_pow_diffset_card` show no `sorryAx`
  (only the standard propext / Classical.choice / Quot.sound). Reshapes vs the R9 plan, all faithful:
    * `CarryFree` carries `0 < Q` as a top-level conjunct (was nested under ∀, which vacuously
      failed when U = ∅ and broke the `0 < Q` extraction);
    * `sumset_image_eq` / `diffset_image_eq` are UNCONDITIONAL (the set identity needs no gap —
      it is pure ring algebra); the gap enters only at the cardinality step;
    * `sumset_card_mul_of_carryfree` / `diffset_card_mul_of_carryfree` need only `CarryFree Q U`,
      not `CarryFree Q V` (the dropped `hcfV` is what makes the k-fold induction need no tower
      carry-freeness).

  This sketch does NOT define C_3a and does NOT close `ghr` — it certifies the counting identity
  that the GHR limit argument rests on, leaving only the sup-realization wrapper to the (multi-round)
  real-analysis sketch. It does NOT raise `held` on its own (held stays the Python cert).

  Borrows: `lean-native-decide-smallmt` (the project, the Mathlib pin, the namespace `C3a`);
  `exact-sumdiff-dp` (the finite-set counting semantics it formalizes).
-/

import Mathlib.Data.Finset.NAry
import Mathlib.Data.Finset.Prod
import Mathlib.Tactic

namespace C3a

open Finset

/-- The carry-free digit embedding of a two-factor box: `(u,v) ↦ u + Q·v`. -/
def emb (Q : ℤ) (uv : ℤ × ℤ) : ℤ := uv.1 + Q * uv.2

/-- The image of the box `U ×ˢ V` under `emb Q` — the two-factor "tensor" set. -/
def box (Q : ℤ) (U V : Finset ℤ) : Finset ℤ := (U ×ˢ V).image (emb Q)

/-- The (finite) sumset of a Finset with itself, as `image₂ (+)`. -/
def sumset (S : Finset ℤ) : Finset ℤ := Finset.image₂ (· + ·) S S

/-- The (finite) diffset of a Finset with itself. -/
def diffset (S : Finset ℤ) : Finset ℤ := Finset.image₂ (· - ·) S S

/-- The carry-free gap condition: `0 < Q`, and the base `Q` exceeds twice every absolute value
    reachable in `U ± U`, so no carry can mix the two coordinates of `emb`. (R9 reshape: `0 < Q`
    is a top-level conjunct so it survives `U = ∅`.) -/
def CarryFree (Q : ℤ) (U : Finset ℤ) : Prop :=
  0 < Q ∧ ∀ a ∈ U, ∀ b ∈ U, 2 * |a + b| < Q ∧ 2 * |a - b| < Q

/-- General injectivity engine for `emb`. `emb Q` is injective on the box `A ×ˢ B` whenever the
    FIRST-coordinate range `A` fits inside one digit: `|a - a'| < Q` for all `a, a' ∈ A`.
    (Euclidean-division uniqueness: `u₁ + Q·v₁ = u₂ + Q·v₂` ⟹ `u₁ - u₂ = Q·(v₂ - v₁)`; the LHS
    is `< Q` in abs value while the RHS is a multiple of `Q`, forcing `v₁ = v₂` then `u₁ = u₂`.) -/
theorem emb_injOn (Q : ℤ) (A B : Finset ℤ) (hQ : 0 < Q)
    (hbound : ∀ a ∈ A, ∀ a' ∈ A, |a - a'| < Q) :
    Set.InjOn (emb Q) (↑(A ×ˢ B) : Set (ℤ × ℤ)) := by
  rintro ⟨u1, v1⟩ hp1 ⟨u2, v2⟩ hp2 h
  simp only [coe_product, Set.mem_prod, mem_coe] at hp1 hp2
  obtain ⟨hu1, hv1⟩ := hp1
  obtain ⟨hu2, hv2⟩ := hp2
  simp only [emb] at h
  have hb : |u1 - u2| < Q := hbound u1 hu1 u2 hu2
  have hkey : u1 - u2 = Q * (v2 - v1) := by ring_nf; linarith [h]
  have hv : v2 - v1 = 0 := by
    by_contra hne
    have h1 : 1 ≤ |v2 - v1| := by
      rcases lt_or_gt_of_ne hne with h' | h'
      · rw [abs_of_neg (by omega)]; omega
      · rw [abs_of_pos (by omega)]; omega
    have : Q ≤ |u1 - u2| := by
      rw [hkey, abs_mul, abs_of_pos hQ]
      calc Q = Q * 1 := by ring
        _ ≤ Q * |v2 - v1| := mul_le_mul_of_nonneg_left h1 (le_of_lt hQ)
    omega
  have huv : v1 = v2 := by omega
  have : u1 = u2 := by rw [huv] at h; linarith
  simp [this, huv]

/-- HOLE 1 — `emb Q` is injective on the box `U ×ˢ V` under the gap condition.
    (Special case of `emb_injOn` with `A = U`: `CarryFree Q U` bounds `|a - a'| < Q` on `U`.) -/
theorem carryfree_inj (Q : ℤ) (U V : Finset ℤ)
    (hcf : CarryFree Q U) (_hcfV : CarryFree Q V) :
    Set.InjOn (emb Q) (↑(U ×ˢ V) : Set (ℤ × ℤ)) := by
  apply emb_injOn Q U V hcf.1
  intro a ha a' ha'
  -- |a - a'| ≤ |a + a'| + ... ; cleanest: 2|a-a'| < Q from CarryFree on the diff, then |a-a'| < Q.
  have := (hcf.2 a ha a' ha').2
  have hnn : (0 : ℤ) ≤ |a - a'| := abs_nonneg _
  omega

/-- HOLE 2 — the sumset of the box equals the box of the coordinate sumsets.
    `(box Q U V) + (box Q U V) = box Q (sumset U) (sumset V)`.  UNCONDITIONAL — pure ring algebra:
    `(u₁+Q·v₁) + (u₂+Q·v₂) = (u₁+u₂) + Q·(v₁+v₂)`. The gap condition is NOT needed here (R9). -/
theorem sumset_image_eq (Q : ℤ) (U V : Finset ℤ) :
    sumset (box Q U V) = box Q (sumset U) (sumset V) := by
  ext z
  simp only [sumset, box, mem_image₂, mem_image, mem_product]
  constructor
  · rintro ⟨x, ⟨⟨u1, v1⟩, ⟨hu1, hv1⟩, rfl⟩, y, ⟨⟨u2, v2⟩, ⟨hu2, hv2⟩, rfl⟩, rfl⟩
    exact ⟨⟨u1 + u2, v1 + v2⟩, ⟨⟨u1, hu1, u2, hu2, rfl⟩, ⟨v1, hv1, v2, hv2, rfl⟩⟩,
      by simp only [emb]; ring⟩
  · rintro ⟨⟨s, t⟩, ⟨⟨u1, hu1, u2, hu2, rfl⟩, ⟨v1, hv1, v2, hv2, rfl⟩⟩, rfl⟩
    exact ⟨emb Q (u1, v1), ⟨⟨u1, v1⟩, ⟨hu1, hv1⟩, rfl⟩,
      emb Q (u2, v2), ⟨⟨u2, v2⟩, ⟨hu2, hv2⟩, rfl⟩, by simp only [emb]; ring⟩

/-- HOLE 2' — the diffset analogue (also unconditional). -/
theorem diffset_image_eq (Q : ℤ) (U V : Finset ℤ) :
    diffset (box Q U V) = box Q (diffset U) (diffset V) := by
  ext z
  simp only [diffset, box, mem_image₂, mem_image, mem_product]
  constructor
  · rintro ⟨x, ⟨⟨u1, v1⟩, ⟨hu1, hv1⟩, rfl⟩, y, ⟨⟨u2, v2⟩, ⟨hu2, hv2⟩, rfl⟩, rfl⟩
    exact ⟨⟨u1 - u2, v1 - v2⟩, ⟨⟨u1, hu1, u2, hu2, rfl⟩, ⟨v1, hv1, v2, hv2, rfl⟩⟩,
      by simp only [emb]; ring⟩
  · rintro ⟨⟨s, t⟩, ⟨⟨u1, hu1, u2, hu2, rfl⟩, ⟨v1, hv1, v2, hv2, rfl⟩⟩, rfl⟩
    exact ⟨emb Q (u1, v1), ⟨⟨u1, v1⟩, ⟨hu1, hv1⟩, rfl⟩,
      emb Q (u2, v2), ⟨⟨u2, v2⟩, ⟨hu2, hv2⟩, rfl⟩, by simp only [emb]; ring⟩

/-- Every element of `sumset U` fits inside one digit: `2·|s| < Q`. -/
theorem sumset_bound (Q : ℤ) (U : Finset ℤ) (hcf : CarryFree Q U) :
    ∀ s ∈ sumset U, 2 * |s| < Q := by
  intro s hs
  simp only [sumset, mem_image₂] at hs
  obtain ⟨a, ha, b, hb, rfl⟩ := hs
  exact (hcf.2 a ha b hb).1

/-- Every element of `diffset U` fits inside one digit: `2·|s| < Q`. -/
theorem diffset_bound (Q : ℤ) (U : Finset ℤ) (hcf : CarryFree Q U) :
    ∀ s ∈ diffset U, 2 * |s| < Q := by
  intro s hs
  simp only [diffset, mem_image₂] at hs
  obtain ⟨a, ha, b, hb, rfl⟩ := hs
  exact (hcf.2 a ha b hb).2

/-- HOLE 3 — carry-free multiplicativity of the sumset count over a two-factor box.
    `|sumset (box Q U V)| = |sumset U|·|sumset V|`.  (R9 reshape: needs ONLY `CarryFree Q U` — the
    second factor `V` is unconstrained.)  From `sumset_image_eq` + injectivity of `emb` on
    `(sumset U) ×ˢ (sumset V)` (`sumset_bound` ⟹ first-coordinate range fits one digit). -/
theorem sumset_card_mul_of_carryfree (Q : ℤ) (U V : Finset ℤ) (hcf : CarryFree Q U) :
    (sumset (box Q U V)).card = (sumset U).card * (sumset V).card := by
  rw [sumset_image_eq]
  have hbnd := sumset_bound Q U hcf
  have hinj : Set.InjOn (emb Q) (↑((sumset U) ×ˢ (sumset V)) : Set (ℤ × ℤ)) := by
    apply emb_injOn Q _ _ hcf.1
    intro a ha a' ha'
    have h1 := hbnd a ha
    have h2 := hbnd a' ha'
    calc |a - a'| ≤ |a| + |a'| := abs_sub a a'
      _ < Q := by omega
  unfold box
  rw [card_image_of_injOn hinj, card_product]

/-- HOLE 4 — the diffset analogue of HOLE 3. -/
theorem diffset_card_mul_of_carryfree (Q : ℤ) (U V : Finset ℤ) (hcf : CarryFree Q U) :
    (diffset (box Q U V)).card = (diffset U).card * (diffset V).card := by
  rw [diffset_image_eq]
  have hbnd := diffset_bound Q U hcf
  have hinj : Set.InjOn (emb Q) (↑((diffset U) ×ˢ (diffset V)) : Set (ℤ × ℤ)) := by
    apply emb_injOn Q _ _ hcf.1
    intro a ha a' ha'
    have h1 := hbnd a ha
    have h2 := hbnd a' ha'
    calc |a - a'| ≤ |a| + |a'| := abs_sub a a'
      _ < Q := by omega
  unfold box
  rw [card_image_of_injOn hinj, card_product]

/-- The k-fold base-Q digit-tensor power of a base set `U`. (`tpow 0 = U`,
    `tpow (k+1) = box Q U (tpow k)`.) -/
def tpow (Q : ℤ) (U : Finset ℤ) : ℕ → Finset ℤ
  | 0 => U
  | (k + 1) => box Q U (tpow Q U k)

/-- HOLE 5 — tensor-power multiplicativity of the sumset count:
    `|sumset (U^{⊗k})| = |sumset U|^(k+1)`.  (Induction on `k`; step = HOLE 3 with the base set `U`
    as the carry-free first factor and the tower `tpow Q U k` as the unconstrained second factor —
    NO carry-freeness of the tower is required.) -/
theorem tensor_pow_sumset_card (Q : ℤ) (U : Finset ℤ) (hcf : CarryFree Q U) :
    ∀ k : ℕ, (sumset (tpow Q U k)).card = (sumset U).card ^ (k + 1) := by
  intro k
  induction k with
  | zero => simp [tpow]
  | succ n ih =>
    rw [tpow, sumset_card_mul_of_carryfree Q U (tpow Q U n) hcf, ih]
    ring

/-- HOLE 6 — tensor-power multiplicativity of the diffset count:
    `|diffset (U^{⊗k})| = |diffset U|^(k+1)`. -/
theorem tensor_pow_diffset_card (Q : ℤ) (U : Finset ℤ) (hcf : CarryFree Q U) :
    ∀ k : ℕ, (diffset (tpow Q U k)).card = (diffset U).card ^ (k + 1) := by
  intro k
  induction k with
  | zero => simp [tpow]
  | succ n ih =>
    rw [tpow, diffset_card_mul_of_carryfree Q U (tpow Q U n) hcf, ih]
    ring

end C3a
