/-
# C_9 = Θ(C_7): the verified Polak–Schrijver size-367 certificate in C_7^⊠5.

This file imports the explicit 367-codeword independent set from [PS2018]
(arXiv:1808.07438, Appendix), `decide`-checks that it is pairwise-independent under the
`C_7^⊠5` confusability relation (no `native_decide`, no `sorry`), and assembles the engine
soundness lemma `isNIndepSet_of_cert` to conclude there is a genuine independent set of
size 367 in `C_7^⊠5`, i.e. `α(C_7^⊠5) ≥ 367`.

The final lower bound `Θ(C_7) ≥ 367^(1/5) > 3.2578` is obtained from `α(C_7^⊠5) ≥ 367`
via the Shannon-capacity definition `Θ(G) = sup_n α(G^⊠n)^(1/n)`; that supremum step is
carried as the explicitly-named bridge hypothesis `ThetaGeFromIndep` (the honest trust
boundary, analogue of the 5b `MTThm15`), since Mathlib has no `Θ`. The rational-power
comparison `367^(1/5) > 3.2578` is proven in Lean.

This REPRODUCES the existing record 3.2578 as a machine-checked baseline; it does NOT beat
the record.

Reference: [PS2018] Polak–Schrijver, "New lower bound on the Shannon capacity of C_7 from
circular graphs", IPL 143 (2019), arXiv:1808.07438.
-/
import Constants.C9Graph

namespace C9

open SimpleGraph

set_option maxRecDepth 100000

/-- The explicit 367-codeword Polak–Schrijver independent set in `C_7^⊠5`,
transcribed verbatim from the Appendix of arXiv:1808.07438. Each word is a length-5 list
of symbols in `[0,6]`. -/
def S367 : List (List ℕ) := [
  [0,2,0,2,0], [0,2,1,1,2], [0,2,2,0,4], [0,2,3,0,6], [0,2,4,6,1], [0,2,5,5,3],
  [0,3,6,4,5], [0,3,0,4,0], [0,3,0,3,2], [0,3,1,2,4], [0,3,2,2,6], [0,3,3,1,1],
  [0,3,4,0,3], [1,4,1,4,4], [1,4,2,3,1], [1,4,3,2,3], [1,4,4,1,5], [1,4,5,1,0],
  [1,5,6,0,2], [1,5,0,6,4], [1,5,1,6,6], [1,5,2,5,1], [1,5,3,4,3], [1,5,4,3,0],
  [1,5,5,2,2], [1,6,6,1,4], [1,6,0,1,6], [1,6,1,0,1], [1,6,2,6,3], [1,6,3,5,5],
  [1,6,4,5,0], [1,6,5,4,2], [1,0,6,3,6], [1,0,0,2,1], [1,0,1,1,3], [1,0,2,0,5],
  [1,0,3,0,0], [1,0,4,6,2], [1,0,5,5,4], [1,1,6,5,6], [1,1,0,4,1], [1,1,0,3,3],
  [1,1,1,2,5], [1,1,2,2,0], [1,1,3,1,2], [1,1,4,0,4], [1,1,5,0,6], [1,2,6,6,1],
  [1,2,0,5,3], [1,2,1,4,5], [1,2,2,4,0], [1,2,2,3,2], [1,2,3,2,4], [1,2,4,2,6],
  [1,2,5,1,1], [1,3,6,0,3], [1,3,0,6,5], [1,3,1,6,0], [1,3,2,5,2], [1,3,3,4,4],
  [1,3,4,4,6], [1,3,4,3,1], [2,4,0,1,0], [2,4,1,0,2], [2,4,2,6,4], [2,4,3,6,6],
  [2,4,4,5,1], [2,4,5,4,3], [2,5,6,3,0], [2,5,0,2,2], [2,5,1,1,4], [2,5,2,1,6],
  [2,5,3,0,1], [2,5,4,6,3], [2,5,5,5,5], [2,6,6,5,0], [2,6,0,4,2], [2,6,0,3,4],
  [2,6,1,3,6], [2,6,2,2,1], [2,6,3,1,3], [2,6,4,0,5], [2,6,5,0,0], [2,0,6,6,2],
  [2,0,0,5,4], [2,0,1,5,6], [2,0,2,4,1], [2,0,2,3,3], [2,0,3,2,5], [2,0,4,2,0],
  [2,0,5,1,2], [2,1,6,0,4], [2,1,0,0,6], [2,1,1,6,1], [2,1,2,5,3], [2,1,3,4,5],
  [2,1,4,4,0], [2,1,4,3,2], [2,2,6,2,6], [2,2,0,1,1], [2,2,1,0,3], [2,2,2,6,5],
  [2,2,3,6,0], [2,2,4,5,2], [2,2,5,4,4], [2,3,6,3,1], [2,3,0,2,3], [2,3,1,1,5],
  [2,3,2,1,0], [2,3,3,0,2], [2,3,4,6,4], [2,3,5,6,6], [3,4,1,3,0], [3,4,2,2,2],
  [3,4,3,1,4], [3,4,4,1,6], [3,4,5,0,1], [3,5,6,6,3], [3,5,0,5,5], [3,5,1,5,0],
  [3,5,2,4,2], [3,5,2,3,4], [3,5,3,3,6], [3,5,4,2,1], [3,5,5,1,3], [3,6,6,0,5],
  [3,6,0,0,0], [3,6,1,6,2], [3,6,2,5,4], [3,6,3,5,6], [3,6,4,4,1], [3,6,4,3,3],
  [3,0,6,2,0], [3,0,0,1,2], [3,0,1,0,4], [3,0,2,0,6], [3,0,3,6,1], [3,0,4,5,3],
  [3,0,5,4,5], [3,1,6,3,2], [3,1,0,2,4], [3,1,1,2,6], [3,1,2,1,1], [3,1,3,0,3],
  [3,1,4,6,5], [3,1,5,6,0], [3,2,6,5,2], [3,2,0,4,4], [3,2,1,3,1], [3,2,2,2,3],
  [3,2,3,1,5], [3,2,4,1,0], [3,2,5,0,2], [3,3,6,6,4], [3,3,0,6,6], [3,3,1,5,1],
  [3,3,2,4,3], [3,3,2,3,5], [3,3,3,3,0], [3,3,4,2,2], [4,4,6,1,6], [4,4,0,0,1],
  [4,4,1,6,3], [4,4,2,5,5], [4,4,3,5,0], [4,4,4,4,2], [4,4,4,3,4], [4,4,5,3,6],
  [4,5,6,2,1], [4,5,0,1,3], [4,5,1,0,5], [4,5,2,0,0], [4,5,3,6,2], [4,5,4,5,4],
  [4,5,5,5,6], [4,6,6,3,3], [4,6,0,2,5], [4,6,1,2,0], [4,6,2,1,2], [4,6,3,0,4],
  [4,6,4,0,6], [4,6,5,6,1], [4,0,6,5,3], [4,0,0,4,5], [4,0,1,3,2], [4,0,2,2,4],
  [4,0,3,2,6], [4,0,4,1,1], [4,0,5,0,3], [4,1,6,6,5], [4,1,0,6,0], [4,1,1,5,2],
  [4,1,2,4,4], [4,1,3,3,1], [4,1,4,2,3], [4,1,5,1,5], [4,2,6,1,0], [4,2,0,0,2],
  [4,2,1,6,4], [4,2,2,6,6], [4,2,3,5,1], [4,2,4,4,3], [4,2,4,3,5], [4,3,6,2,2],
  [4,3,0,1,4], [4,3,1,1,6], [4,3,2,0,1], [4,3,3,6,3], [4,3,4,5,5], [4,3,5,5,0],
  [5,4,6,3,4], [5,4,0,3,6], [5,4,1,2,1], [5,4,2,1,3], [5,4,3,0,5], [5,4,4,0,0],
  [5,4,5,6,2], [5,5,6,5,4], [5,5,0,5,6], [5,5,1,4,1], [5,5,1,3,3], [5,5,2,2,5],
  [5,5,3,2,0], [5,5,4,1,2], [5,5,5,0,4], [5,6,6,0,6], [5,6,0,6,1], [5,6,1,5,3],
  [5,6,2,4,5], [5,6,3,3,2], [5,6,4,2,4], [5,6,5,2,6], [5,0,6,1,1], [5,0,0,0,3],
  [5,0,1,6,5], [5,0,2,6,0], [5,0,3,5,2], [5,0,4,4,4], [5,1,6,2,3], [5,1,0,1,5],
  [5,1,1,1,0], [5,1,2,0,2], [5,1,3,6,4], [5,1,5,5,1], [5,2,6,4,3], [5,2,6,3,5],
  [5,2,0,3,0], [5,2,1,2,2], [5,2,2,1,4], [5,3,6,5,5], [5,3,1,3,4], [6,4,3,3,2],
  [6,4,4,2,4], [6,4,5,2,6], [6,5,6,1,1], [6,5,0,0,3], [6,5,2,6,0], [6,5,3,5,2],
  [6,5,4,4,4], [6,5,5,4,6], [6,6,6,2,3], [6,6,1,1,0], [6,6,2,0,2], [6,6,3,6,4],
  [6,6,4,6,6], [6,6,5,5,1], [6,0,6,4,3], [6,0,6,4,5], [6,0,0,3,0], [6,0,1,2,2],
  [6,0,2,1,4], [6,0,3,1,6], [6,0,4,0,1], [6,0,5,6,3], [6,1,0,5,0], [6,1,1,4,2],
  [6,1,1,3,4], [6,1,2,3,6], [6,1,3,2,1], [6,1,4,1,3], [6,2,6,0,0], [6,2,0,6,2],
  [6,2,1,5,4], [6,2,2,5,6], [6,2,3,4,1], [6,2,3,3,3], [6,2,5,2,0], [6,3,6,1,2],
  [6,3,0,0,4], [6,3,1,0,6], [6,3,2,6,1], [6,3,3,5,3], [6,3,4,4,5], [6,3,5,4,0],
  [6,4,5,3,2], [0,4,0,2,6], [0,4,1,1,1], [0,4,2,0,3], [0,4,4,6,0], [0,4,5,5,2],
  [0,5,6,4,4], [0,5,0,3,1], [0,5,1,2,3], [0,5,3,1,0], [0,5,4,0,2], [0,5,5,6,4],
  [0,6,6,6,6], [0,6,0,5,1], [0,6,1,4,3], [0,6,2,3,0], [0,6,3,2,2], [0,6,4,1,4],
  [0,6,5,1,6], [0,0,6,0,1], [0,0,0,6,3], [0,0,1,5,5], [0,0,2,5,0], [0,0,3,4,2],
  [0,0,3,3,4], [0,0,4,3,6], [0,1,6,1,3], [0,1,1,0,0], [0,1,2,6,2], [0,1,3,5,4],
  [0,1,4,5,6], [0,1,5,4,1], [0,2,6,2,5], [0,0,5,2,1], [0,1,0,0,5], [0,2,5,3,3],
  [0,3,5,6,5], [0,4,0,5,2], [0,4,3,6,5], [0,4,6,2,4], [0,4,6,6,0], [0,5,0,4,6],
  [0,5,2,2,5], [1,0,5,3,4], [1,4,2,4,6], [1,5,4,3,5], [2,2,5,2,4], [2,4,6,1,5],
  [2,4,6,5,1], [3,2,0,4,6], [3,4,0,3,5], [3,4,0,4,3], [3,6,5,2,5], [4,0,0,4,0],
  [4,1,2,4,6], [4,2,5,3,0], [4,3,5,1,4], [4,5,6,4,1], [5,0,5,3,1], [5,1,4,5,6],
  [5,2,4,0,0], [5,2,5,6,3], [5,3,0,5,0], [5,3,1,4,2], [5,3,3,2,0], [5,3,4,1,2],
  [5,6,3,4,0], [6,1,5,0,5], [6,2,4,2,5], [6,4,1,5,4], [6,4,3,4,0], [6,5,1,0,5],
  [6,6,0,2,5]
]

/-- The certificate has 367 words. -/
theorem S367_length : S367.length = 367 := by decide

/-- All words have length 5. -/
theorem S367_lengths : ∀ w ∈ S367, w.length = 5 := by decide

/-- All symbols are `< 7`. -/
theorem S367_valid : ∀ w ∈ S367, ∀ x ∈ w, x < 7 := by decide

/-- The words are distinct. -/
theorem S367_nodup : S367.Nodup := by decide

/-- **Load-bearing kernel check**: the 367-word set is pairwise-independent under the
`C_7^⊠5` confusability relation. Plain kernel `decide` over C(367,2)=67,161 pairs, each a
short-circuiting 5-coordinate check — NO `native_decide`. -/
theorem S367_indep : allPairsIndep S367 = true := by decide

/-- **Engine soundness applied**: there is a genuine independent set of size 367 in
`C_7^⊠5`. Equivalently `α(C_7^⊠5) ≥ 367`. -/
theorem alpha_C7pow5_ge_367 :
    (C7pow 5).IsNIndepSet 367 (S367.map (vec 5)).toFinset := by
  have h := isNIndepSet_of_cert 5 S367 S367_indep S367_nodup S367_valid S367_lengths
  rwa [S367_length] at h

/-! ## The Shannon-capacity bridge (named trust boundary).

`ThetaGeFromIndep` packages the Shannon-capacity inequality
`α(C_7^⊠n) ≥ N → Θ(C_7) ≥ N^(1/n)`, which is the definitional unfolding of
`Θ(G) = sup_n α(G^⊠n)^(1/n)` together with `α ≥ N` and rpow-monotonicity. Mathlib has no
`Θ`, so we carry it as an explicit hypothesis on the bound theorem rather than as an
axiom — keeping `#print axioms` clean and the trust link visible in the signature. -/

/-- The bridge predicate: `theta` is at least `N^(1/n)` whenever there is an independent set
of size `N` in `C_7^⊠n`. -/
def ThetaGeFromIndep (theta : ℝ) : Prop :=
  ∀ (n N : ℕ) (s : Finset (Fin n → Fin 7)),
    (C7pow n).IsNIndepSet N s → theta ≥ (N : ℝ) ^ ((1 : ℝ) / n)

/-- `367^(1/5) > 3.2578` — the rational-power comparison, proven in Lean. -/
theorem rpow_367_gt : (367 : ℝ) ^ ((1 : ℝ) / 5) > 3.2578 := by
  rw [gt_iff_lt, show (1:ℝ)/5 = ((5:ℕ):ℝ)⁻¹ by norm_num,
    Real.lt_rpow_inv_iff_of_pos (by norm_num) (by norm_num) (by norm_num)]
  norm_num

/-- **Main baseline theorem**: under the Shannon-capacity bridge, the verified 367-set
gives `Θ(C_7) ≥ 367^(1/5) > 3.2578`. REPRODUCES the [PS2018] record as a machine-checked
baseline. -/
theorem theta_C7_ge_baseline (theta : ℝ) (hbridge : ThetaGeFromIndep theta) :
    theta ≥ (367 : ℝ) ^ ((1 : ℝ) / 5) :=
  hbridge 5 367 _ alpha_C7pow5_ge_367

/-- **Numeric baseline**: under the bridge, `Θ(C_7) > 3.2578`. -/
theorem theta_C7_gt_3_2578 (theta : ℝ) (hbridge : ThetaGeFromIndep theta) :
    theta > 3.2578 :=
  lt_of_lt_of_le rpow_367_gt (theta_C7_ge_baseline theta hbridge)

end C9
