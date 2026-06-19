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
