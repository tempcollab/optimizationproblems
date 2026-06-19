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

HOLES (explicit `sorry`; the bound does NOT silently rest on any of them):
  * H_GEN_τ   the explicit 13-piece structure τ′ + the per-box rational translate vectors
              (the LP solution). Found by the builder's rational LP search at a concrete off-center
              box; recorded as exact rationals. This is the load-bearing combinatorial hole.
  * H_GEN_FARKAS  per-box feasibility ⇒ local count ≤ 13, via the multi-D rational membership /
              Farkas primitive (generalizing `icc_covered_by_two` from lemmas/ to ℝ³ polytope
              membership — the D3 primitive). Reuses lemmas/ `IsCoveredBy.union`, `.mono_left`.
  * H_GEN_ATLAS   the symmetry-reduced box atlas covering [0,1]^6 ∖ N(1/2); each box gets a
              feasible (P_j, τ′_j). The genuine scale concern — must be FAR smaller than Prymak's
              4.66M (the off-1/2 region is generic, so a coarse atlas should suffice). Open.
  * H_GEN_GLUE    max over the atlas ⇒ generic-regime subproblem ≤ 13.

This file STATES the generic-regime target and assembles it from the holes; it `lake build`s green
(holes are `sorry`). Reuses the certified primitives in constants/39a/lemmas/ via import below.
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

/-! ## The 13-piece local bound (the load-bearing claim)

For every generic `p`, the target `E ∪ V_p` is covered by 13 translates of `int(O_p)`. This is the
union over the atlas of per-box feasible LP solutions; the per-box step is the rational Farkas
membership, the atlas step is the finite box decomposition. -/

/-- **H_GEN (load-bearing).** Every generic-regime covering subproblem needs at most 13 translates.
Holes: τ′ structure (H_GEN_τ), per-box Farkas (H_GEN_FARKAS), atlas (H_GEN_ATLAS), glue
(H_GEN_GLUE). -/
theorem generic_cover_le_13 (p : P6) (hp : Generic p) :
    IsCoveredBy 13 (CoverTarget p) (Piece p) := by
  -- H_GEN_τ + H_GEN_FARKAS per box, glued over H_GEN_ATLAS by IsCoveredBy.union / .mono_left.
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
