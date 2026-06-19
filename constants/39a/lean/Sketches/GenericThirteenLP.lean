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
  * H_GEN_τ   [CORE CLOSED at one box] the explicit 13-piece structure τ′ + per-box rational
              translates. The MARKED-POINT part (vertices+face points, incl. the merge) is now a
              sorry-free Lean lemma `marked_points_covered_by_thirteen`. What REMAINS of H_GEN_τ is
              H_GEN_EDGES below (the 1-D edge coverage), kept honest.
  * H_GEN_EDGES   [NEW hole, split out of H_GEN_τ] the 12 cube edges (1-D segments) are covered by
              the same 13 translates via the endpoint vertex-translates. In the certificate this is
              checked exactly (`edge_covered_exact`); the Lean port needs the multi-D interval
              primitive (generalize `icc_covered_by_two` to a segment vs a polytope) — open.
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
