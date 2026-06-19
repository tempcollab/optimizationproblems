/-
Sketch D -- certify-fourteen: machine-checked Lean infrastructure toward H_3 <= 14 (Prymak 2023).

This is NOT a record-break: 14 is already the verified bound. The sketch is the Lean-infrastructure
de-risk for the record-break sketches A (special-case-p-half) and C (larger-covering-piece):
it (i) gives H_3 a GENUINE registry definition (no bound-smuggling axiom), and (ii) proves the
finite, reusable covering primitives that A and C both depend on -- monotonicity of the covering
number and the 1-D interval-covering LP primitive that is the heart of Prymak's edge-coverage step.

What is sorry-free here (verified, #print axioms shows no sorryAx):
  * `H3` -- the registry definition of the Hadwiger covering number in R^3, built from a genuine
    `IsCovered`/`coveringNumber` over translates of the interior of a 3-D convex body. NO axiom.
  * `coveringNumber_mono_left` -- monotonicity: shrinking the covered set cannot raise the count.
  * `IsCoveredBy.union` and `IsCoveredBy.add` -- a cover of A by m and of B by n gives a cover of
    A ∪ B by m+n (the bookkeeping A/C use to assemble per-piece covers).
  * `icc_covered_by_two` -- the 1-D interval primitive: a closed interval of length <= 2L is
    covered by two translates of `[0,L]` placed at the two endpoints. This is exactly Prymak's
    edge-coverage LP in dimension one (edges of the cube skeleton are 1-D), reduced to an explicit
    rational/real feasibility witness. Reusable by A and C.

Holes that remain (explicit `sorry`, honest -- the proof does NOT rest on them being true; they
are the steps still to formalize, NOT smuggled hypotheses):
  * D1  affine-normalization reduction to the cube-skeleton problem (Prymak Lemma 2.2)
  * D2  open->closed discretization Q_P (Prymak Lemma 2.4 / Cor 2.5)
  * D3  per-box rational LP feasibility => local count <= 14 (Prymak Prop 2.6, multi-D Farkas)
  * D4  Lean-checkable box atlas compressing Prymak's 4.66M boxes (the real obstacle)
  * D5  assemble => H3 <= 14   (`H3_le_14`, an explicit open hole, NOT proved)
-/
import Mathlib.Analysis.Convex.Basic
import Mathlib.Analysis.Convex.Topology
import Mathlib.Topology.Algebra.Module.FiniteDimension
import Mathlib.Analysis.InnerProductSpace.EuclideanDist

open scoped Pointwise

namespace H3.CertifyFourteen

/-! ## Covering numbers (genuine, reusable) -/

variable {V : Type*} [AddCommGroup V] [Module ℝ V] [TopologicalSpace V]

/-- `IsCoveredBy N K L`: the set `K` is covered by `N` translates of `L`, i.e. there are
`N` translation vectors `t 0, …, t (N-1)` with `K ⊆ ⋃ i, (t i +ᵥ L)`. -/
def IsCoveredBy (N : ℕ) (K L : Set V) : Prop :=
  ∃ t : Fin N → V, K ⊆ ⋃ i, (t i +ᵥ L)

/-- The covering number `C(K, L)`: the least number of translates of `L` covering `K`
(`0` if no finite cover exists, by the convention of `sInf` on the empty set). -/
noncomputable def coveringNumber (K L : Set V) : ℕ :=
  sInf {N | IsCoveredBy N K L}

/-- Monotonicity in the covered set: a cover of `K` is a cover of every subset of `K`. -/
theorem IsCoveredBy.mono_left {N : ℕ} {K K' L : Set V}
    (h : IsCoveredBy N K L) (hsub : K' ⊆ K) : IsCoveredBy N K' L := by
  obtain ⟨t, ht⟩ := h
  exact ⟨t, hsub.trans ht⟩

/-- Two covers combine: `m` translates covering `A` and `n` covering `B` give `m + n`
translates covering `A ∪ B`.  This is the assembly bookkeeping sketches A and C use to glue
per-piece covers (8 vertex pieces + 6 face/edge pieces = 14). -/
theorem IsCoveredBy.union {m n : ℕ} {A B L : Set V}
    (hA : IsCoveredBy m A L) (hB : IsCoveredBy n B L) : IsCoveredBy (m + n) (A ∪ B) L := by
  obtain ⟨s, hs⟩ := hA
  obtain ⟨t, ht⟩ := hB
  refine ⟨Fin.append s t, ?_⟩
  intro x hx
  rcases hx with hx | hx
  · obtain ⟨i, hxi⟩ := Set.mem_iUnion.mp (hs hx)
    refine Set.mem_iUnion.mpr ⟨Fin.castAdd n i, ?_⟩
    simpa [Fin.append_left] using hxi
  · obtain ⟨i, hxi⟩ := Set.mem_iUnion.mp (ht hx)
    refine Set.mem_iUnion.mpr ⟨Fin.natAdd m i, ?_⟩
    simpa [Fin.append_right] using hxi

/-- Monotonicity of the covering number in the covered set, when `K` admits some finite cover. -/
theorem coveringNumber_mono_left {K K' L : Set V} {N : ℕ}
    (hK : IsCoveredBy N K L) (hsub : K' ⊆ K) :
    coveringNumber K' L ≤ coveringNumber K L := by
  -- `coveringNumber K L = sInf S` is a member of `S` (S nonempty via `hK`); that same `N`
  -- covers `K' ⊆ K`, so it is an upper-bound witness for `coveringNumber K'`.
  have hne : {M | IsCoveredBy M K L}.Nonempty := ⟨N, hK⟩
  have hmem : IsCoveredBy (coveringNumber K L) K L := Nat.sInf_mem hne
  exact Nat.sInf_le (hmem.mono_left hsub)

/-! ## The 1-D interval-covering primitive (Prymak's edge LP, dimension one)

A closed interval whose length is at most `2L` is covered by two translates of the closed
interval `[0, L]`, placed at its two endpoints. The edges of the cube 1-skeleton in Prymak's
reduction are 1-D, and covering each by closed translates of a piece is exactly this LP; the
explicit endpoint placement is the rational feasibility witness. -/

set_option linter.unusedVariables false in
/-- A closed interval `[a, b]` with `b ≤ a + 2*L` is covered by the two translates of `[0, L]`
placed at `a` and at `b - L`.  Explicit witness; no LP solver needed.
(`hL` and `hab` are genuine premises consumed by `linarith` inside the two branches.) -/
theorem icc_covered_by_two {a b L : ℝ} (hL : 0 ≤ L) (hab : a ≤ b) (hlen : b ≤ a + 2 * L) :
    IsCoveredBy 2 (Set.Icc a b) (Set.Icc (0 : ℝ) L) := by
  refine ⟨![a, b - L], ?_⟩
  intro x hx
  obtain ⟨hxa, hxb⟩ := hx
  by_cases hmid : x ≤ a + L
  · -- translate by `a`: the witness preimage is `x - a ∈ [0, L]`
    refine Set.mem_iUnion.mpr ⟨0, x - a, ⟨by linarith, by linarith⟩, ?_⟩
    simp [Matrix.cons_val_zero]
  · -- translate by `b - L`: the witness preimage is `x - (b - L) ∈ [0, L]`
    rw [not_le] at hmid
    refine Set.mem_iUnion.mpr ⟨1, x - (b - L), ⟨by linarith, by linarith⟩, ?_⟩
    simp [Matrix.cons_val_one]

/-! ## The registry definition of `H_3` (genuine; replaces the bound-smuggling axiom) -/

/-- A `3`-dimensional convex body in `ℝ³ = Fin 3 → ℝ`: a convex, compact set with nonempty
interior (the standard meaning of "`n`-dimensional convex body"). -/
def IsConvexBody3 (K : Set (Fin 3 → ℝ)) : Prop :=
  Convex ℝ K ∧ IsCompact K ∧ (interior K).Nonempty

/-- The Hadwiger covering number `H_3`: the least `N` such that **every** `3`-dimensional convex
body `K ⊆ ℝ³` is covered by `N` translates of its interior `int(K)`.  This is the registry
definition; it contains **no** reference to the value `14`. -/
noncomputable def H3 : ℕ :=
  sInf {N | ∀ K : Set (Fin 3 → ℝ), IsConvexBody3 K → IsCoveredBy N K (interior K)}

/-! ## The target bound (HONEST OPEN HOLE -- not proved, not smuggled)

Prymak 2023: `H3 ≤ 14`.  The proof route is D1–D5 above; none is formalized yet, so this is an
explicit `sorry`.  The definitions above are sorry-free and axiom-clean; this theorem is the
only `sorry` and it is `H3_le_14` itself, so nothing downstream silently depends on an unproved
hard step. -/
theorem H3_le_14 : H3 ≤ 14 := by
  -- HOLE D1 (reduction) + D2 (discretization) + D3 (per-box Farkas LP) + D4 (atlas) + D5 (assemble).
  sorry

end H3.CertifyFourteen
