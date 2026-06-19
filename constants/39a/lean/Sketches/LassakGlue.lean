/-
Sketch — lassak-glue (R3): the TOP-LEVEL ASSEMBLY of H_3 ≤ 13 from a two-regime partition of
Prymak's parameter space, with each regime a hole pointing at a sibling sketch. No sketch in the
population yet STATES the final 13-bound against the genuine registry `H3` and exhibits the glue;
this one does, so the builder/reviewer have a single target to assemble toward and the two halves
have a fixed interface.

WHY A SEPARATE ASSEMBLY SKETCH (the structural argument that makes 13 possible).
Prymak's reduction: H_3 ≤ max_{p∈[0,1]^6} C(E ∪ V_p, int(O_p)), and the 14-floor is attained ONLY
at the single point p=(1/2,…,1/2) (Remark 2.3 — VERIFIED R1 as F0; the 14 marked points are
pairwise ℓ₁-uncoverable, all 51 tight pairs on the boundary of O_p−O_p with ZERO slack). R3
established the complementary hard fact: at p=1/2 NO enlarged covering piece can drop 14→13 (O_p−O_p
is exactly the unit cube; the cube faces are min-vol-box contacts), so the bottleneck point cannot
be beaten inside the O_p frame at all. The escape is to PARTITION p-space:

  GENERIC regime  (p outside a rational δ-ball N(1/2)):  C(E ∪ V_p, int(O_p)) ≤ 13
        — finite rational LP / Farkas; supplied by sketch `GenericThirteenLP` (hole H_GEN).
  NEAR-1/2 regime (p inside N(1/2)):                     H(K_p) ≤ 13  DIRECTLY
        — the body is near-symmetric, Lassak-stability gives ≤ 13; supplied by sketch
          `octahedral-direct` (holes E1/E2). This regime bounds H(K) DIRECTLY (not via the O_p
          cover), which is exactly why it dodges the 14-floor.
  GLUE       max over the two regimes ≤ 13  ⇒  H3 ≤ 13.

The glue + the δ-partition are FINITE/DISCRETE (a two-way case split on p), so the ASSEMBLY is
Lean-fit; the two regime-bounds are the holes (the generic one Lean-fit, the near-1/2 one
Lean-hostile). The TOP-LEVEL THEOREM `H3 ≤ 13` is stated faithfully against the registry `H3` from
CertifyFourteen and the FINAL step (membership ⇒ `H3 ≤ 13`) is now CLOSED via `Nat.sInf_le` — no
value smuggled, correct strict direction (13 < 14).

WHAT IS CLOSED THIS ROUND (R3, builder):
  * `H3_le_13` is reduced to `every_body_cover_13` by `Nat.sInf_le` with NO sorry of its own:
    `13 ∈ {N | ∀ K, IsConvexBody3 K → IsCoveredBy N K (interior K)}` is literally the registry
    membership, so this final glue step is honest and complete.
  * `every_body_cover_13` is reduced to the per-parameter cover `per_param_cover_13` by the Prymak
    parameterization interface (`param`, `body_eq_Body`, `param_mem`) — the only sorry on THIS path
    is `prymak_param` (the affine-normalization existence statement, = Prymak Lemma 2.2 / H_RED).
  * `per_param_cover_13` is reduced to the two regime halves by the TOTAL case split
    `generic_or_near` (CLOSED, no sorry) — the assembly contains no anonymous sorry; each branch is
    a NAMED interface hole (`generic_branch_cover` / `near_cover_le_13`).

REMAINING HOLES (explicit `sorry`; the bound does NOT rest silently on any):
  * H_RED      `prymak_param` — Prymak's affine-normalization (Lemma 2.2): every 3-D convex body is
               an affine image of some `Body p`, p ∈ [0,1]^6, covering-equivalently. Shared infra
               hole (= CertifyFourteen D1/D2/D5).  Also `Body` is an opaque placeholder def (the
               normalized body family; instantiated together with `prymak_param`).
  * H_GENERIC  `generic_branch_cover` — generic regime: `Body p` covered by 13 translates of its
               interior, transported from `GenericThirteenLP.generic_regime_thirteen` (the E ∪ V_p
               LP cover) via the reduction. Its own holes live in GenericThirteenLP.
  * H_NEAR     `near_cover_le_13` — near-1/2 regime: `Body p` covered by 13 translates of its
               interior DIRECTLY for p ∈ N(1/2) (octahedral-direct E1/E2). Lean-hostile.

This file STATES H3 ≤ 13 against the registry def and assembles it; it `lake build`s green (the
remaining holes are explicit `sorry`). Reuses the certified primitives + the registry `H3` via the
imports below.
-/
import Sketches.CertifyFourteen
import Sketches.GenericThirteenLP

open scoped Pointwise

namespace H3.LassakGlue

open H3.CertifyFourteen H3.GenericThirteenLP

/-! ## The two-regime partition of Prymak's parameter space

`P6 = Fin 6 → ℝ` is `[0,1]^6`. We split it into the GENERIC region (sketch A's `Generic`, p outside
a fixed rational δ-ball around `(1/2,…,1/2)`) and its complement the NEAR-1/2 region. The partition
is total: every `p` is `Generic` or `Near`. -/

/-- The near-`1/2` region: the complement of the generic region (p within margin `δ` of the
bottleneck). Builder fixes `δ` to match `GenericThirteenLP.Generic`; abstract here. -/
def Near (p : P6) : Prop := ¬ Generic p

/-- The partition is total (a tautology by `Near := ¬ Generic`; recorded so the glue can case-split
without an extra hole). CLOSED — no sorry. -/
theorem generic_or_near (p : P6) : Generic p ∨ Near p := em (Generic p)

/-! ## The normalized body family (Prymak parameterization, part of H_RED)

`Body p` is the affinely-normalized convex body for parameter `p` (Prymak Lemma 2.2: every 3-D
convex body is, up to an invertible affine map preserving the covering number, one of these). Kept
as an opaque placeholder until the normalization is formalized; `prymak_param` below is the
existence statement that turns an arbitrary body into one of these. -/

/-- The Prymak-normalized body for parameter `p` (opaque placeholder; instantiated with
`prymak_param` when the affine normalization is formalized). -/
def Body (p : P6) : Set (Fin 3 → ℝ) := sorry

/-- **H_RED (shared infra, Prymak Lemma 2.2 / D1).** Every 3-D convex body `K` is, up to an
invertible affine map (which preserves the covering number), some `Body p` with `p ∈ [0,1]^6`;
concretely it suffices that whenever every `Body p` is covered by 13 translates of its interior,
so is every convex body. Stated here as the bridge from the per-parameter covers to the
arbitrary-body statement. (Affine-normalization existence — honest open hole.) -/
theorem prymak_param
    (h : ∀ p : P6, IsCoveredBy 13 (Body p) (interior (Body p))) :
    ∀ K : Set (Fin 3 → ℝ), IsConvexBody3 K → IsCoveredBy 13 K (interior K) := by
  sorry

/-! ## The near-`1/2` regime bound (DIRECT, hole H_NEAR)

For `p` in the near-`1/2` region, the Prymak-normalized body `Body p` is near-symmetric and is
covered DIRECTLY by ≤ 13 translates of its interior (Lassak-stability — sketch `octahedral-direct`).
The hole is the direct cover. -/

/-- **H_NEAR (load-bearing, near-1/2 half).** For `p` near `1/2`, the body is covered by 13
translates of its interior — the DIRECT Lassak-stability cover that dodges the 14-floor. Supplied
by `octahedral-direct` (holes E1/E2; Lean-hostile, numerical certificate). -/
theorem near_cover_le_13 (p : P6) (hp : Near p) :
    IsCoveredBy 13 (Body p) (interior (Body p)) := by
  sorry

/-! ## The generic regime bound (hole H_GENERIC) — imported from GenericThirteenLP

`GenericThirteenLP.generic_regime_thirteen` gives `IsCoveredBy 13 (CoverTarget p) (Piece p)` for
generic `p` (its own holes H_GEN_*). Transporting that `E ∪ V_p`-by-`int(O_p)` cover into a
`Body p`-by-`int(Body p)` cover is the affine-normalization step (part of H_RED); kept as the
`generic_branch_cover` hole here, with the re-export `generic_cover_le_13'` recording the imported
content it rests on. -/

/-- **H_GENERIC re-export.** The generic-regime 13-cover of `E ∪ V_p` by `int(O_p)`, imported
verbatim from `GenericThirteenLP`. (Its own holes H_GEN_* live there.) -/
theorem generic_cover_le_13' (p : P6) (hp : Generic p) :
    IsCoveredBy 13 (CoverTarget p) (Piece p) :=
  generic_regime_thirteen p hp

/-- **H_GENERIC (transport).** For generic `p`, the normalized body `Body p` is covered by 13
translates of its interior. This transports `generic_cover_le_13'` (the `E ∪ V_p`-by-`int(O_p)`
cover) across the affine normalization that identifies the Prymak subproblem with the body cover
(part of H_RED). The imported LP content is `generic_cover_le_13'`; the transport is the open hole. -/
theorem generic_branch_cover (p : P6) (hp : Generic p) :
    IsCoveredBy 13 (Body p) (interior (Body p)) := by
  -- uses `generic_cover_le_13' p hp` + the affine identification `CoverTarget/Piece ↔ Body/int Body`.
  sorry

/-! ## The per-parameter cover (assembled by the case split — CLOSED glue) -/

/-- **GLUE (closed).** Every normalized body `Body p` is covered by 13 translates of its interior:
case-split `p` via the total partition `generic_or_near`; the generic branch is
`generic_branch_cover`, the near branch is `near_cover_le_13`. No anonymous sorry — each branch is a
named interface hole. -/
theorem per_param_cover_13 (p : P6) : IsCoveredBy 13 (Body p) (interior (Body p)) := by
  rcases generic_or_near p with hg | hn
  · exact generic_branch_cover p hg
  · exact near_cover_le_13 p hn

/-! ## The arbitrary-body cover (via Prymak parameterization) -/

/-- Every 3-D convex body is covered by 13 translates of its interior. Reduces to
`per_param_cover_13` over all parameters through the Prymak normalization `prymak_param`. The only
sorry on this path is `prymak_param` (H_RED). -/
theorem every_body_cover_13 :
    ∀ K : Set (Fin 3 → ℝ), IsConvexBody3 K → IsCoveredBy 13 K (interior K) :=
  prymak_param per_param_cover_13

/-! ## The top-level target `H3 ≤ 13` (final glue CLOSED) -/

/-- **The TOP-LEVEL TARGET `H3 ≤ 13`.** `H3 = sInf {N | ∀ K, IsConvexBody3 K → IsCoveredBy N K
(interior K)}`; `every_body_cover_13` is exactly the membership of `13` in that set, so
`Nat.sInf_le` gives `H3 ≤ 13`. This final step is CLOSED (no sorry), against the genuine registry
`H3`, with the correct strict direction (13 < 14 = the Prymak record). The remaining holes are
`prymak_param` (H_RED), `generic_branch_cover` (H_GENERIC transport, + GenericThirteenLP's holes),
and `near_cover_le_13` (H_NEAR). -/
theorem H3_le_13 : H3 ≤ 13 :=
  Nat.sInf_le every_body_cover_13

end H3.LassakGlue
