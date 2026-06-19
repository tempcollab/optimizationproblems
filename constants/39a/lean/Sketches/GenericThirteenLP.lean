/-
Sketch — generic-thirteen-lp: the GENERIC-REGIME 13-piece cover of E ∪ V_p, as a finite
rational LP, certified in Lean. This is the Lean-FIT lead for H_3 ≤ 13.

STRATEGY (the half of the bound that is finite/rational/discrete).
Prymak's reduction gives  H_3 ≤ max_{p∈[0,1]^6} C(E ∪ V_p, int(O_p)),  E = cube 1-skeleton,
V_p = 6 contact points, O_p = conv(V_p). Prymak certifies the RHS ≤ 14 over 4.66M boxes.

The 14-floor is supported ONLY at the single point p=(1/2,…,1/2) (Remark 2.3 — the 14 marked
points are pairwise ℓ₁-uncoverable by one translate of int(O_p), VERIFIED in R1 as F0). For EVERY
p bounded away from 1/2, F1 (VERIFIED R1) gives a count-reducing MERGE: one translate of int(O_p)
covers a cube vertex AND an adjacent face point simultaneously. This sketch builds the
generic-regime half: a redesigned 13-piece injection τ′ whose Prop-2.6 rational LP — vertices +
6 face rectangles + ALL 12 edges — is feasible on every box of a symmetry-reduced atlas of
[0,1]^6 MINUS a neighborhood N(1/2) of the bottleneck.

  Off p=1/2:  H_3-subproblem ≤ 13   (THIS sketch — Lean-fit, rational LP / Farkas)
  Near p=1/2: handled by a sibling sketch (octahedral-direct / minvol-corner-slack — Lean-hostile)
  Glue:       max over both regimes ≤ 13.

WHAT THE R1 + R2-OUTLINER SCREEN ESTABLISHED about the 13-structure (drives τ′ design):
  * At p=1/2 the 8 vertex-translates already cover all 12 edges with ZERO residual middle
    (symmetric placement reaches edge-midpoints exactly; residual gap g=1-2r=0). So at p=1/2 the
    edges are FREE and the cost is purely the 6 face points → 14. (Edge-redundancy gives no free
    saving — refuted as a standalone lead R2.)
  * Away from p=1/2 residual edge-middle gaps OPEN UP (g≈0.14 at p=0.6, g≈0.33 at p=0.7): the
    vertex translates no longer cover the full edges, so a correct τ′ must REASSIGN edge-middle
    duty to the (now merged) face translates. The naive single-merge (drop one face translate,
    keep the other 5 doing only face-rectangle duty) is edge-INFEASIBLE — the dropped translate's
    edge-middle is uncovered. τ′ must be a genuine combinatorial redesign: 8 vertex translates
    (each tuned to maximize min edge-reach over its 3 edges) + 4 edge/face translates covering the
    5 residual face points and 12 residual edge-middles, with one vertex/face MERGE.

ROUND-3 PROGRESS (builder). The load-bearing combinatorial hole H_GEN_τ is CLOSED *at one
concrete off-center box* and its **finite marked-point core is now formalized in Lean** below
(`marked_points_covered_by_thirteen`, sorry-free, `decide`-checked rational membership). The
witness was found by an exact rational LP/Farkas search (see
`constants/39a/certificate/generic-thirteen-lp.py`, `verify_witness`, pure-`Fraction`
re-verification — NO floating point in the load-bearing check) at the box
  p* = (9/10, 1/10, 9/10, 9/10, 1/10, 1/10)   (every pᵢ bounded 2/5 off 1/2).
There the 14 marked points {8 cube vertices} ∪ Vₚ are covered by **13** explicit rational
translates of O_{p*} — one merge: the contact point q₂₀ shares vertex-translate t₅. Margin
0.0218 (strict interior). So  C({marked} , int O_{p*}) ≤ 13  at p*.

REVISED STRUCTURAL FACT (reshapes H_GEN_ATLAS — was wrong as planned). The 13-feasible region
is NOT all of [0,1]⁶ ∖ N(1/2): point-mergeability is NOT sufficient. The merge frees a covering
piece ONLY where the 8 vertex-translates ALONE still cover all 12 edges, which forces ALL six pᵢ
bounded off 1/2 in a compatible pattern (a single- or two-coordinate offset gives NO 13-cover —
verified in the script). Only 40/64 of the {1/10,9/10}-corner boxes admit a 13-cover. So the
generic atlas must tile this THIN region and the rest of [0,1]⁶ ∖ {13-region} falls to the
near-1/2 sibling — the partition is NOT the simple "ball around 1/2".

HOLES (explicit `sorry`; the bound does NOT silently rest on any of them):
  * H_GEN_τ   [FULLY CLOSED at one box, R4] the explicit 13-piece structure τ′ + per-box rational
              translates. The MARKED-POINT part is `marked_points_covered_by_thirteen` (R3); the
              EDGE part is `edges_covered_by_thirteen` (R4); the capstone
              `target_star_covered_by_thirteen` covers the full E ∪ V_{p*} by 13 — all sorry-free,
              axiom-clean. The per-box content of the load-bearing hole is now hole-free at p*.
  * H_GEN_EDGES   [CLOSED, R4] the 12 cube edges (1-D segments) are covered by the same 13
              translates via the endpoint vertex-translates. Ported from the certificate's exact
              `edge_covered_exact` via the reusable multi-D segment primitive
              `segment_covered_by_two` (generalizes `icc_covered_by_two` to a segment vs a
              polytope), one rational split σ per edge. See `edges_covered_by_thirteen` below.
  * H_GEN_ATLAS   [REVISED] a finite atlas of the THIN 13-feasible region (NOT [0,1]⁶∖N(1/2)); each
              box a feasible (P_j, τ′_j) over Q_P = ⋂_{v∈P} O_v. Plus its complement handed to the
              near-1/2 sibling. Open. (The single-point witness above is the |P|=1 base case.)
  * H_GEN_GLUE    max over the atlas ⇒ generic-regime subproblem ≤ 13; then glue with the sibling.

This file STATES the generic-regime target, FORMALIZES the marked-point core of the load-bearing
hole at the witness box, and assembles the rest from holes; it `lake build`s green. Reuses the
certified primitives in constants/39a/lemmas/ via import below.
-/
import Sketches.CertifyFourteen

open scoped Pointwise

namespace H3.GenericThirteenLP

open H3.CertifyFourteen

/-! ## The generic-regime covering subproblem

`CoverSubproblem p` is the set `E ∪ V_p` (cube 1-skeleton ∪ the 6 contact points) that Prymak's
reduction requires covering by translates of `int(O_p)`. We keep it abstract here (a `sorry`-typed
placeholder set), to be instantiated by the builder against the concrete rational `A_p`. -/

/-- Placeholder for the parameter space `[0,1]^6`. -/
abbrev P6 : Type := Fin 6 → ℝ

/-- The marked/skeleton target set `E ∪ V_p ⊆ ℝ³` for a parameter `p`. (Builder instantiates from
`A_p`; abstract here so the skeleton builds.) -/
def CoverTarget (p : P6) : Set (Fin 3 → ℝ) := sorry

/-- The covering piece `int(O_p) ⊆ ℝ³`, `O_p = conv(V_p)`. (Builder instantiates from `A_p`.) -/
def Piece (p : P6) : Set (Fin 3 → ℝ) := sorry

/-- The "generic regime": parameters bounded away from the bottleneck `p=(1/2,…,1/2)` by a fixed
rational margin `δ`. (Builder fixes `δ`; abstract here.) -/
def Generic (p : P6) : Prop := sorry

/-! ## Concrete witness at the off-center box `p* = (9/10,1/10,9/10,9/10,1/10,1/10)`

The genuinely-checked core of `H_GEN_τ`: the 14 marked points (8 cube vertices + 6 contact
points `Vₚ*`) are covered by **13** explicit rational translates of `int(O_{p*})`, one merge.
This is the rational-Farkas membership (the D3 primitive specialised) made fully concrete and
checked by `norm_num` — the Lean-fit content of the LP search. The vectors come from
`generic-thirteen-lp.py` (`verify_witness`, exact `Fraction` re-check). -/

/-- `int(O_{p*})` as the open polytope cut out by the 8 exact facet inequalities of `O_{p*}`
(integer coefficients; `n · x < d`). A point of `ℝ³` is `![x,y,z]` here. -/
def inOpStar (x : Fin 3 → ℝ) : Prop :=
  80 * x 1 - 10 * x 2 < 71 ∧
  80 * x 0 + 10 * x 2 < 81 ∧
  10 * x 1 - 80 * x 2 < 1 ∧
  x 0 - x 1 - x 2 < 0 ∧
  - x 0 + x 1 + x 2 < 1 ∧
  10 * x 0 + 80 * x 2 < 81 ∧
  -80 * x 0 - 10 * x 1 < -9 ∧
  -10 * x 0 - 80 * x 1 < -9

/-- The covering piece at `p*`: `int(O_{p*})`. -/
def PieceStar : Set (Fin 3 → ℝ) := {x | inOpStar x}

/-- The 14 marked points `{8 cube vertices} ∪ V_{p*}` at the witness box. -/
noncomputable def markedStar : Fin 14 → (Fin 3 → ℝ)
  | 0 => ![0, 0, 0]
  | 1 => ![0, 0, 1]
  | 2 => ![0, 1, 0]
  | 3 => ![0, 1, 1]
  | 4 => ![1, 0, 0]
  | 5 => ![1, 0, 1]
  | 6 => ![1, 1, 0]
  | 7 => ![1, 1, 1]
  | 8 => ![0, 9/10, 1/10]      -- q10
  | 9 => ![1, 9/10, 1/10]      -- q11
  | 10 => ![9/10, 0, 9/10]     -- q20  (merged onto translate 5)
  | 11 => ![9/10, 1, 9/10]     -- q21
  | 12 => ![1/10, 1/10, 0]     -- q30
  | 13 => ![1/10, 1/10, 1]     -- q31

/-- The 13 explicit rational translate vectors (the LP solution at `p*`). -/
noncomputable def centerStar : Fin 13 → (Fin 3 → ℝ)
  | 0 => ![-1/8, -1/8, -23/49]
  | 1 => ![-1/8, -1/8, 23/49]
  | 2 => ![-7/16, 22/53, -13/34]
  | 3 => ![-12/35, 12/35, 12/35]
  | 4 => ![12/35, -12/35, -12/35]
  | 5 => ![13/34, -7/39, 5/54]
  | 6 => ![7/39, 5/54, -13/34]
  | 7 => ![13/34, 7/16, 22/53]
  | 8 => ![-7/8, -3/43, -45/58]
  | 9 => ![1/8, -3/43, -45/58]
  | 10 => ![1/41, 1/33, 1/41]
  | 11 => ![-45/58, -20/23, -7/8]
  | 12 => ![-45/58, -20/23, 1/8]

/-- The duty assignment: which translate covers which marked point (point 10 = q20 shares
translate 5 with cube vertex 5 — the single merge that drops 14 → 13). -/
def assignStar : Fin 14 → Fin 13
  | 0 => 0 | 1 => 1 | 2 => 2 | 3 => 3 | 4 => 4 | 5 => 5 | 6 => 6 | 7 => 7
  | 8 => 8 | 9 => 9 | 10 => 5 | 11 => 10 | 12 => 11 | 13 => 12

/-- **H_GEN_τ core (CLOSED, sorry-free).** Every marked point lies in its assigned translate of
`int(O_{p*})`: `markedStar i − centerStar (assignStar i) ∈ int(O_{p*})`. This is the exact
rational Farkas membership of the 13-piece cover — the load-bearing computation, checked. -/
theorem markedStar_mem (i : Fin 14) :
    inOpStar (fun k => markedStar i k - centerStar (assignStar i) k) := by
  fin_cases i <;>
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    · simp only [markedStar, centerStar, assignStar, Matrix.cons_val_zero, Matrix.cons_val_one,
        Matrix.head_cons, Matrix.cons_val_fin_one, Matrix.cons_val]
      norm_num

/-- **The concrete 13-cover of the MARKED POINTS at `p*`** (sorry-free): the 14 marked points are
covered by 13 translates of `int(O_{p*})`. The merge (point 10 ↦ translate 5) is what makes it 13,
not 14. (Edge coverage — H_GEN_EDGES — is a separate honest hole.) -/
theorem marked_points_covered_by_thirteen :
    IsCoveredBy 13 (Set.range markedStar) PieceStar := by
  refine ⟨centerStar, ?_⟩
  rintro _ ⟨i, rfl⟩
  refine Set.mem_iUnion.mpr ⟨assignStar i, ?_⟩
  -- `markedStar i ∈ centerStar (assignStar i) +ᵥ PieceStar`
  refine Set.mem_vadd_set.mpr ⟨fun k => markedStar i k - centerStar (assignStar i) k, ?_, ?_⟩
  · exact markedStar_mem i
  · funext k; simp [vadd_eq_add]

/-! ## H_GEN_EDGES — the 12 cube edges covered by the same 13 translates

The marked POINTS are covered above. Prymak's reduction also requires covering the cube
1-skeleton `E` (the 12 edges), each a 1-D segment. This is the multi-D generalization of the
cached `icc_covered_by_two` primitive: along each edge line `v₀ + s·u` (`s ∈ [0,1]`), each
translate of `int(O_{p*})` cuts out an OPEN `s`-interval (one `n·u` ratio per facet — the D3
rational-Farkas primitive specialised). The exact-verified certificate
(`generic-thirteen-lp.py`, `edge_covered_exact`) shows each edge is covered by a 2-body chain:
its two endpoint vertex-translates `t_a, t_b`. We port that here.

`segment_covered_by_two` is the reusable primitive: a segment `{v₀ + s·u : s ∈ [0,1]}` is
covered by two translates `c_a, c_b` of an open piece `P` whenever there is a split point
`σ ∈ [0,1]` with `v₀ + s·u − c_a ∈ P` for `s ∈ [0,σ]` and `v₀ + s·u − c_b ∈ P` for `s ∈ [σ,1]`.
This is `icc_covered_by_two` lifted from the line to a parametrized segment in ℝ³ against an
arbitrary (here polytopal-open) piece. -/

/-- The point on the edge line through `v₀` with direction `u` at parameter `s`. -/
def edgeSeg (v0 u : Fin 3 → ℝ) (s : ℝ) : Fin 3 → ℝ := fun k => v0 k + s * u k

/-- **Reusable multi-D segment-cover primitive** (generalizes cached `icc_covered_by_two` from a
1-D interval to a parametrized segment vs an arbitrary piece `P ⊆ ℝ³`). If a split parameter
`σ ∈ [0,1]` exists with the first translate covering the segment for `s ∈ [0,σ]` and the second
for `s ∈ [σ,1]`, the whole segment `{v₀ + s·u : s ∈ [0,1]}` is covered by the two translates
`c_a, c_b` of `P`. -/
theorem segment_covered_by_two (v0 u c_a c_b : Fin 3 → ℝ) (P : Set (Fin 3 → ℝ)) (σ : ℝ)
    (hσ0 : 0 ≤ σ) (hσ1 : σ ≤ 1)
    (ha : ∀ s, 0 ≤ s → s ≤ σ → (fun k => edgeSeg v0 u s k - c_a k) ∈ P)
    (hb : ∀ s, σ ≤ s → s ≤ 1 → (fun k => edgeSeg v0 u s k - c_b k) ∈ P) :
    IsCoveredBy 2 (edgeSeg v0 u '' Set.Icc (0 : ℝ) 1) P := by
  refine ⟨![c_a, c_b], ?_⟩
  rintro _ ⟨s, ⟨hs0, hs1⟩, rfl⟩
  by_cases hmid : s ≤ σ
  · refine Set.mem_iUnion.mpr ⟨0, ?_⟩
    refine Set.mem_vadd_set.mpr ⟨fun k => edgeSeg v0 u s k - c_a k, ha s hs0 hmid, ?_⟩
    funext k; simp [vadd_eq_add, Matrix.cons_val_zero]
  · push_neg at hmid
    refine Set.mem_iUnion.mpr ⟨1, ?_⟩
    refine Set.mem_vadd_set.mpr ⟨fun k => edgeSeg v0 u s k - c_b k, hb s hmid.le hs1, ?_⟩
    funext k; simp [vadd_eq_add, Matrix.cons_val_one]

/-- **Subset form** of `segment_covered_by_two` against a fixed family `t : Fin 13 → ℝ³`: the
edge segment is contained in the union of the 13 translates, picking the two indices `a, b` whose
translates `t a, t b` are `c_a, c_b`. This is what `edges_covered_by_thirteen` glues over the 12
edges (so each edge's two translates land inside the same 13-piece union as the marked points). -/
theorem segment_subset_two (v0 u : Fin 3 → ℝ) (P : Set (Fin 3 → ℝ)) (t : Fin 13 → (Fin 3 → ℝ))
    (a b : Fin 13) (σ : ℝ)
    (ha : ∀ s, 0 ≤ s → s ≤ σ → (fun k => edgeSeg v0 u s k - t a k) ∈ P)
    (hb : ∀ s, σ ≤ s → s ≤ 1 → (fun k => edgeSeg v0 u s k - t b k) ∈ P) :
    edgeSeg v0 u '' Set.Icc (0 : ℝ) 1 ⊆ ⋃ i : Fin 13, t i +ᵥ P := by
  rintro _ ⟨s, ⟨hs0, hs1⟩, rfl⟩
  by_cases hmid : s ≤ σ
  · refine Set.mem_iUnion.mpr ⟨a, ?_⟩
    refine Set.mem_vadd_set.mpr ⟨fun k => edgeSeg v0 u s k - t a k, ha s hs0 hmid, ?_⟩
    funext k; simp [vadd_eq_add]
  · push_neg at hmid
    refine Set.mem_iUnion.mpr ⟨b, ?_⟩
    refine Set.mem_vadd_set.mpr ⟨fun k => edgeSeg v0 u s k - t b k, hb s hmid.le hs1, ?_⟩
    funext k; simp [vadd_eq_add]

/-- The 12 cube edges as `(v₀, u)` pairs: `v₀` an endpoint vertex, `u` the unit axis direction to
the other endpoint, so the edge is `{v₀ + s·u : s ∈ [0,1]}`. (Matches `CUBE_EDGES` in the
certificate.) -/
def cubeEdge : Fin 12 → (Fin 3 → ℝ) × (Fin 3 → ℝ)
  | 0 => (![0, 0, 0], ![0, 0, 1])   -- v0 → v1
  | 1 => (![0, 0, 0], ![0, 1, 0])   -- v0 → v2
  | 2 => (![0, 0, 0], ![1, 0, 0])   -- v0 → v4
  | 3 => (![0, 0, 1], ![0, 1, 0])   -- v1 → v3
  | 4 => (![0, 0, 1], ![1, 0, 0])   -- v1 → v5
  | 5 => (![0, 1, 0], ![0, 0, 1])   -- v2 → v3
  | 6 => (![0, 1, 0], ![1, 0, 0])   -- v2 → v6
  | 7 => (![0, 1, 1], ![1, 0, 0])   -- v3 → v7
  | 8 => (![1, 0, 0], ![0, 0, 1])   -- v4 → v5
  | 9 => (![1, 0, 0], ![0, 1, 0])   -- v4 → v6
  | 10 => (![1, 0, 1], ![0, 1, 0])  -- v5 → v7
  | 11 => (![1, 1, 0], ![0, 0, 1])  -- v6 → v7

/-- For each edge `e`, the two endpoint vertex-translates `(t_a, t_b)` that cover it and the split
parameter `σ`, exactly as computed in the certificate. (`t_a` reaches the start `s=0`, `t_b` the
end `s=1`; they overlap across `σ`.) -/
noncomputable def edgeCover : Fin 12 → Fin 13 × Fin 13 × ℝ
  | 0 => (0, 1, 1/2)
  | 1 => (0, 2, 1/2)
  | 2 => (0, 4, 5/12)
  | 3 => (1, 3, 5/12)
  | 4 => (1, 5, 1/2)
  | 5 => (2, 3, 5/12)
  | 6 => (2, 6, 1/2)
  | 7 => (3, 7, 7/12)
  | 8 => (4, 5, 7/12)
  | 9 => (4, 6, 7/12)
  | 10 => (5, 7, 1/2)
  | 11 => (6, 7, 1/2)

/-- **H_GEN_EDGES, edge 0** (v0->v1). Covered by `centerStar 0` / `centerStar 1`, split `s=1/2`. -/
theorem edge0_covered :
    IsCoveredBy 2 (edgeSeg ![0, 0, 0] ![0, 0, 1] '' Set.Icc (0 : ℝ) 1) PieceStar := by
  refine segment_covered_by_two _ _ (centerStar 0) (centerStar 1) PieceStar (1/2)
    (by norm_num) (by norm_num) ?_ ?_ <;> intro s hs0 hs1 <;>
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    · simp only [edgeSeg, centerStar, PieceStar, Set.mem_setOf_eq, inOpStar,
        Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_fin_one,
        Matrix.cons_val]
      linarith

/-- **H_GEN_EDGES, edge 1** (v0->v2). Covered by `centerStar 0` / `centerStar 2`, split `s=1/2`. -/
theorem edge1_covered :
    IsCoveredBy 2 (edgeSeg ![0, 0, 0] ![0, 1, 0] '' Set.Icc (0 : ℝ) 1) PieceStar := by
  refine segment_covered_by_two _ _ (centerStar 0) (centerStar 2) PieceStar (1/2)
    (by norm_num) (by norm_num) ?_ ?_ <;> intro s hs0 hs1 <;>
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    · simp only [edgeSeg, centerStar, PieceStar, Set.mem_setOf_eq, inOpStar,
        Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_fin_one,
        Matrix.cons_val]
      linarith

/-- **H_GEN_EDGES, edge 2** (v0->v4). Covered by `centerStar 0` / `centerStar 4`, split `s=5/12`. -/
theorem edge2_covered :
    IsCoveredBy 2 (edgeSeg ![0, 0, 0] ![1, 0, 0] '' Set.Icc (0 : ℝ) 1) PieceStar := by
  refine segment_covered_by_two _ _ (centerStar 0) (centerStar 4) PieceStar (5/12)
    (by norm_num) (by norm_num) ?_ ?_ <;> intro s hs0 hs1 <;>
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    · simp only [edgeSeg, centerStar, PieceStar, Set.mem_setOf_eq, inOpStar,
        Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_fin_one,
        Matrix.cons_val]
      linarith

/-- **H_GEN_EDGES, edge 3** (v1->v3). Covered by `centerStar 1` / `centerStar 3`, split `s=5/12`. -/
theorem edge3_covered :
    IsCoveredBy 2 (edgeSeg ![0, 0, 1] ![0, 1, 0] '' Set.Icc (0 : ℝ) 1) PieceStar := by
  refine segment_covered_by_two _ _ (centerStar 1) (centerStar 3) PieceStar (5/12)
    (by norm_num) (by norm_num) ?_ ?_ <;> intro s hs0 hs1 <;>
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    · simp only [edgeSeg, centerStar, PieceStar, Set.mem_setOf_eq, inOpStar,
        Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_fin_one,
        Matrix.cons_val]
      linarith

/-- **H_GEN_EDGES, edge 4** (v1->v5). Covered by `centerStar 1` / `centerStar 5`, split `s=1/2`. -/
theorem edge4_covered :
    IsCoveredBy 2 (edgeSeg ![0, 0, 1] ![1, 0, 0] '' Set.Icc (0 : ℝ) 1) PieceStar := by
  refine segment_covered_by_two _ _ (centerStar 1) (centerStar 5) PieceStar (1/2)
    (by norm_num) (by norm_num) ?_ ?_ <;> intro s hs0 hs1 <;>
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    · simp only [edgeSeg, centerStar, PieceStar, Set.mem_setOf_eq, inOpStar,
        Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_fin_one,
        Matrix.cons_val]
      linarith

/-- **H_GEN_EDGES, edge 5** (v2->v3). Covered by `centerStar 2` / `centerStar 3`, split `s=5/12`. -/
theorem edge5_covered :
    IsCoveredBy 2 (edgeSeg ![0, 1, 0] ![0, 0, 1] '' Set.Icc (0 : ℝ) 1) PieceStar := by
  refine segment_covered_by_two _ _ (centerStar 2) (centerStar 3) PieceStar (5/12)
    (by norm_num) (by norm_num) ?_ ?_ <;> intro s hs0 hs1 <;>
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    · simp only [edgeSeg, centerStar, PieceStar, Set.mem_setOf_eq, inOpStar,
        Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_fin_one,
        Matrix.cons_val]
      linarith

/-- **H_GEN_EDGES, edge 6** (v2->v6). Covered by `centerStar 2` / `centerStar 6`, split `s=1/2`. -/
theorem edge6_covered :
    IsCoveredBy 2 (edgeSeg ![0, 1, 0] ![1, 0, 0] '' Set.Icc (0 : ℝ) 1) PieceStar := by
  refine segment_covered_by_two _ _ (centerStar 2) (centerStar 6) PieceStar (1/2)
    (by norm_num) (by norm_num) ?_ ?_ <;> intro s hs0 hs1 <;>
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    · simp only [edgeSeg, centerStar, PieceStar, Set.mem_setOf_eq, inOpStar,
        Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_fin_one,
        Matrix.cons_val]
      linarith

/-- **H_GEN_EDGES, edge 7** (v3->v7). Covered by `centerStar 3` / `centerStar 7`, split `s=7/12`. -/
theorem edge7_covered :
    IsCoveredBy 2 (edgeSeg ![0, 1, 1] ![1, 0, 0] '' Set.Icc (0 : ℝ) 1) PieceStar := by
  refine segment_covered_by_two _ _ (centerStar 3) (centerStar 7) PieceStar (7/12)
    (by norm_num) (by norm_num) ?_ ?_ <;> intro s hs0 hs1 <;>
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    · simp only [edgeSeg, centerStar, PieceStar, Set.mem_setOf_eq, inOpStar,
        Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_fin_one,
        Matrix.cons_val]
      linarith

/-- **H_GEN_EDGES, edge 8** (v4->v5). Covered by `centerStar 4` / `centerStar 5`, split `s=7/12`. -/
theorem edge8_covered :
    IsCoveredBy 2 (edgeSeg ![1, 0, 0] ![0, 0, 1] '' Set.Icc (0 : ℝ) 1) PieceStar := by
  refine segment_covered_by_two _ _ (centerStar 4) (centerStar 5) PieceStar (7/12)
    (by norm_num) (by norm_num) ?_ ?_ <;> intro s hs0 hs1 <;>
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    · simp only [edgeSeg, centerStar, PieceStar, Set.mem_setOf_eq, inOpStar,
        Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_fin_one,
        Matrix.cons_val]
      linarith

/-- **H_GEN_EDGES, edge 9** (v4->v6). Covered by `centerStar 4` / `centerStar 6`, split `s=7/12`. -/
theorem edge9_covered :
    IsCoveredBy 2 (edgeSeg ![1, 0, 0] ![0, 1, 0] '' Set.Icc (0 : ℝ) 1) PieceStar := by
  refine segment_covered_by_two _ _ (centerStar 4) (centerStar 6) PieceStar (7/12)
    (by norm_num) (by norm_num) ?_ ?_ <;> intro s hs0 hs1 <;>
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    · simp only [edgeSeg, centerStar, PieceStar, Set.mem_setOf_eq, inOpStar,
        Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_fin_one,
        Matrix.cons_val]
      linarith

/-- **H_GEN_EDGES, edge 10** (v5->v7). Covered by `centerStar 5` / `centerStar 7`, split `s=1/2`. -/
theorem edge10_covered :
    IsCoveredBy 2 (edgeSeg ![1, 0, 1] ![0, 1, 0] '' Set.Icc (0 : ℝ) 1) PieceStar := by
  refine segment_covered_by_two _ _ (centerStar 5) (centerStar 7) PieceStar (1/2)
    (by norm_num) (by norm_num) ?_ ?_ <;> intro s hs0 hs1 <;>
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    · simp only [edgeSeg, centerStar, PieceStar, Set.mem_setOf_eq, inOpStar,
        Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_fin_one,
        Matrix.cons_val]
      linarith

/-- **H_GEN_EDGES, edge 11** (v6->v7). Covered by `centerStar 6` / `centerStar 7`, split `s=1/2`. -/
theorem edge11_covered :
    IsCoveredBy 2 (edgeSeg ![1, 1, 0] ![0, 0, 1] '' Set.Icc (0 : ℝ) 1) PieceStar := by
  refine segment_covered_by_two _ _ (centerStar 6) (centerStar 7) PieceStar (1/2)
    (by norm_num) (by norm_num) ?_ ?_ <;> intro s hs0 hs1 <;>
    refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
    · simp only [edgeSeg, centerStar, PieceStar, Set.mem_setOf_eq, inOpStar,
        Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_fin_one,
        Matrix.cons_val]
      linarith

/-- The set of points on cube edge `e` (the image of `[0,1]` under its parametrization). -/
noncomputable def cubeEdgeSet (e : Fin 12) : Set (Fin 3 → ℝ) :=
  edgeSeg (cubeEdge e).1 (cubeEdge e).2 '' Set.Icc (0 : ℝ) 1

/-- Each cube edge `e` is contained in the union of the 13 `centerStar` translates of
`int(O_{p*})`, via its two endpoint vertex-translates and split parameter from `edgeCover`. -/
theorem cubeEdge_subset (e : Fin 12) :
    cubeEdgeSet e ⊆ ⋃ i : Fin 13, centerStar i +ᵥ PieceStar := by
  rw [cubeEdgeSet]
  refine segment_subset_two _ _ PieceStar centerStar (edgeCover e).1 (edgeCover e).2.1
    (edgeCover e).2.2 ?_ ?_ <;>
  · intro s hs0 hs1
    fin_cases e <;>
    · simp only [cubeEdge, edgeCover] at hs0 hs1 ⊢
      refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;>
      · simp only [edgeSeg, centerStar, PieceStar, Set.mem_setOf_eq, inOpStar,
          Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, Matrix.cons_val_fin_one,
          Matrix.cons_val]
        linarith

/-- **H_GEN_EDGES (CLOSED, sorry-free).** The full cube 1-skeleton — the union of all 12 edge
segments — is covered by the **same 13 translates** `centerStar` of `int(O_{p*})` that cover the
marked points. Each edge is covered by its two endpoint vertex-translates (`cubeEdge_subset` via
`segment_subset_two`, with the exact split parameters from the certificate), and all those
translates are among the 13.

This is the multi-D edge-coverage step of Prymak's reduction at the witness box `p*`, generalizing
the cached 1-D `icc_covered_by_two` primitive. With `marked_points_covered_by_thirteen`, the FULL
target `E ∪ V_{p*}` (edges ∪ marked points) is now covered by 13 translates of `int(O_{p*})`. -/
theorem edges_covered_by_thirteen :
    IsCoveredBy 13 (⋃ e : Fin 12, cubeEdgeSet e) PieceStar := by
  refine ⟨centerStar, ?_⟩
  rw [Set.iUnion_subset_iff]
  exact cubeEdge_subset

/-- **The full witness target at `p*` (CLOSED, sorry-free).** The complete covering subproblem at
the witness box — the cube 1-skeleton `E` (all 12 edges) together with the 14 marked points
`V_{p*}` ∪ vertices — is covered by **13** translates of `int(O_{p*})`. This combines
`edges_covered_by_thirteen` and `marked_points_covered_by_thirteen` over the SAME 13 translates
`centerStar`, so no extra pieces are spent: `C(E ∪ V_{p*}, int(O_{p*})) ≤ 13` at `p*`, with the
14→13 saving coming from the single merge (point `q₂₀` shares vertex-translate `t₅`). -/
theorem target_star_covered_by_thirteen :
    IsCoveredBy 13 ((⋃ e : Fin 12, cubeEdgeSet e) ∪ Set.range markedStar) PieceStar := by
  -- The marked points lie in the SAME 13-translate union as the edges (`centerStar`).
  have hM : Set.range markedStar ⊆ ⋃ i : Fin 13, centerStar i +ᵥ PieceStar := by
    rintro _ ⟨i, rfl⟩
    refine Set.mem_iUnion.mpr ⟨assignStar i, ?_⟩
    refine Set.mem_vadd_set.mpr ⟨fun k => markedStar i k - centerStar (assignStar i) k,
      markedStar_mem i, ?_⟩
    funext k; simp [vadd_eq_add]
  have hE : (⋃ e : Fin 12, cubeEdgeSet e) ⊆ ⋃ i : Fin 13, centerStar i +ᵥ PieceStar := by
    rw [Set.iUnion_subset_iff]; exact cubeEdge_subset
  refine ⟨centerStar, ?_⟩
  rw [Set.union_subset_iff]
  exact ⟨hE, hM⟩

/-! ## The 13-piece local bound (the load-bearing claim)

For every generic `p`, the target `E ∪ V_p` is covered by 13 translates of `int(O_p)`. This is the
union over the atlas of per-box feasible LP solutions; the per-box step is the rational Farkas
membership, the atlas step is the finite box decomposition. -/

/-- **H_GEN (load-bearing).** Every generic-regime covering subproblem needs at most 13 translates.
Status after R3: the per-box MARKED-POINT core is CLOSED concretely at the witness box `p*`
(`marked_points_covered_by_thirteen`, sorry-free, axiom-clean). What remains to close THIS theorem:
H_GEN_EDGES (1-D edge coverage by the same translates), H_GEN_ATLAS (tile the thin 13-region), and
H_GEN_GLUE (max over the atlas). Held open as `sorry`; the marked-point lemma above is the genuine
discharged sub-step it is built from. -/
theorem generic_cover_le_13 (p : P6) (hp : Generic p) :
    IsCoveredBy 13 (CoverTarget p) (Piece p) := by
  -- At p* the marked-point core is `marked_points_covered_by_thirteen` (CLOSED). Generalising to
  -- every generic p and adding the edges (H_GEN_EDGES) + atlas (H_GEN_ATLAS) is the remaining work.
  sorry

/-! ## Statement of the generic-regime contribution to the bound

When the near-`1/2` regime is supplied by a sibling sketch (octahedral-direct / corner-slack), the
two combine to `H3 ≤ 13`. Here we state ONLY the generic half as a clean target; the glue to `H3`
itself lives in the assembly sketch. The honest open hole is `generic_cover_le_13`. -/

/-- Marker theorem: the generic regime contributes a 13-cover. (Just re-exports the load-bearing
claim; the full `H3 ≤ 13` needs the near-`1/2` half from a sibling sketch + Prymak's reduction
D1/D2, tracked in certify-fourteen's D-holes.) -/
theorem generic_regime_thirteen :
    ∀ p : P6, Generic p → IsCoveredBy 13 (CoverTarget p) (Piece p) :=
  fun p hp => generic_cover_le_13 p hp

end H3.GenericThirteenLP
