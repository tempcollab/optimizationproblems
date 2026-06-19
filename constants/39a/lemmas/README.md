# Shared goal cache — 39a ($H_3$)

Reviewer-certified lemmas any sketch may import without re-proving. Each entry below
cleared the bound bar at promotion: `sorry`-free, axiom-clean (`#print axioms` =
`[propext, Classical.choice, Quot.sound]`, the standard Mathlib trio — no `sorryAx`,
no custom axiom), statement correct and no stronger than proved.

## Certified (R1, from `lean/Sketches/CertifyFourteen.lean`, namespace `H3.CertifyFourteen`)

Reviewer reproduced `lake build` (green, 2413 jobs) and ran `#print axioms` independently
on each. All four lemmas + four supporting defs are axiom-clean. Import via
`import Sketches.CertifyFourteen` inside the `constants/39a/lean/` Lake project.

Definitions (the shared vocabulary):
- `IsCoveredBy (N : ℕ) (K L : Set V) : Prop := ∃ t : Fin N → V, K ⊆ ⋃ i, (t i +ᵥ L)`
- `coveringNumber (K L : Set V) : ℕ := sInf {N | IsCoveredBy N K L}`
- `IsConvexBody3 (K : Set (Fin 3 → ℝ)) : Prop := Convex ℝ K ∧ IsCompact K ∧ (interior K).Nonempty`
- `H3 : ℕ := sInf {N | ∀ K, IsConvexBody3 K → IsCoveredBy N K (interior K)}`
  — the genuine registry definition of $H_3$; faithful to `[ABP2024-def-Hn]`; contains no
  reference to the value 14 (verified: genuine `def`, not an `axiom`).

Lemmas (reviewer re-derived each statement; all correct, none over-stated):
- `IsCoveredBy.mono_left : IsCoveredBy N K L → K' ⊆ K → IsCoveredBy N K' L`
- `IsCoveredBy.union : IsCoveredBy m A L → IsCoveredBy n B L → IsCoveredBy (m+n) (A ∪ B) L`
- `coveringNumber_mono_left : IsCoveredBy N K L → K' ⊆ K → coveringNumber K' L ≤ coveringNumber K L`
- `icc_covered_by_two : 0 ≤ L → a ≤ b → b ≤ a + 2*L → IsCoveredBy 2 (Set.Icc a b) (Set.Icc 0 L)`
  (reviewer re-derived the two-translate witness `![a, b-L]`: branch `x ≤ a+L` lands in
  `a +ᵥ Icc 0 L`, else in `(b-L) +ᵥ Icc 0 L`; valid since `b-L ≤ a+L` from `b ≤ a+2L`.)

These are reusable by sketches A and C (cover assembly + 1-D edge primitive).

## Certified (R4, from `lean/Sketches/GenericThirteenLP.lean`, namespace `H3.GenericThirteenLP`)

Reviewer reproduced `lake build` (green, 2413 jobs) and ran `#print axioms` independently:
both are axiom-clean (`[propext, Classical.choice, Quot.sound]`, no `sorryAx`). The local def
`edgeSeg` must travel with the lemma (it is part of the statement).

Definition (travels with the lemma):
- `edgeSeg (v0 u : Fin 3 → ℝ) (s : ℝ) : Fin 3 → ℝ := fun k => v0 k + s * u k`
  — the point on the edge line through `v0` with direction `u` at parameter `s`.

Lemma (reviewer re-derived; statement correct, not over-stated):
- `segment_covered_by_two (v0 u c_a c_b : Fin 3 → ℝ) (P : Set (Fin 3 → ℝ)) (σ : ℝ)`
  `(hσ0 : 0 ≤ σ) (hσ1 : σ ≤ 1)`
  `(ha : ∀ s, 0 ≤ s → s ≤ σ → (fun k => edgeSeg v0 u s k - c_a k) ∈ P)`
  `(hb : ∀ s, σ ≤ s → s ≤ 1 → (fun k => edgeSeg v0 u s k - c_b k) ∈ P)`
  `: IsCoveredBy 2 (edgeSeg v0 u '' Set.Icc (0:ℝ) 1) P`
  — the multi-D companion of `icc_covered_by_two`: a parametrized segment in ℝ³ is covered by
  two translates of an arbitrary piece `P` given a split `σ` with the first translate covering
  `s ∈ [0,σ]` and the second `s ∈ [σ,1]`. Witness `![c_a, c_b]`, `by_cases s ≤ σ`. Reviewer
  re-derived the two-branch membership; correct and general (no over-statement; `P` arbitrary).
  Import via `import Sketches.GenericThirteenLP`. NOT promoted: the `*Star`/`cubeEdge`/edge-cover
  lemmas (sketch-specific to the `p*` witness).
