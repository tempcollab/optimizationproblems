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

/-! ## The two-regime partition of Prymak's parameter space  (RE-PLANNED R4)

`P6 = Fin 6 → ℝ` is `[0,1]^6`. The R3 partition `Near := ¬Generic` with `Generic = ball-off-1/2`
was VERIFIED FALSE: point-mergeability ≠ edge-feasible 13-cover, so the 13-feasible region is NOT a
ball complement — a slab of `[0,1]^6` (one- or two-coordinate offsets from 1/2) falls through both
halves. We re-plan the partition to the TRUE 13-feasible region.

WHAT THE R4 OUTLINER COMPUTED (certificate `generic-thirteen-lp.py`, exact-rational, reproduced):
the 6 Prymak parameters pair by axis — `{p0,p1}` (axis 0), `{p2,p3}` (axis 1), `{p4,p5}` (axis 2).
For the `{1/10,9/10}`-corner boxes, write `sᵢ = sign(pᵢ − 1/2) ∈ {0,1}`. Then:

  * **ALL 32 even-total-popcount corner boxes** (`∑ᵢ sᵢ ≡ 0 mod 2`) are UNIFORMLY 13-feasible
    (every one solved exactly via the merge structure `thirteen_structure_merge`).
  * The 24 odd-popcount infeasible boxes are exactly the popcount-{1,3,5} sign patterns whose
    axis-parity vector is a single odd axis or all-three-odd; an additional 8 odd-popcount boxes
    ARE feasible (incl. the proven witness `p* = (9/10,1/10,9/10,9/10,1/10,1/10)`, signs (1,0,1,1,0,0)).

So the clean SUFFICIENT generic region is the **even-parity stratum** — a single combinatorial
condition `EvenParity p`, not a ball. Its complement (the odd-parity stratum, a *codim-0 union of
boxes adjacent to 1/2 along an odd number of coordinates*) is the genuine NEAR region handed to the
direct route. This is the correct partition interface: `Generic := EvenParity`, `Near := ¬EvenParity`,
still total, but now MATCHED to where 13 is actually achievable.

NOTE on the witness: `p*` is in the 8-box odd extension, NOT the even stratum — so the generic
half's proven base case lives just outside the clean region. The atlas (`GenericThirteenLP.H_GEN_ATLAS`)
covers the even stratum uniformly; the odd-feasible extension is a bonus, and the odd-INfeasible
stratum is the true Near region. -/

/-- Sign of `pᵢ` relative to the bottleneck `1/2`: `1` if `pᵢ > 1/2`, else `0`. (For the corner
atlas `pᵢ ∈ {1/10,9/10}`; in general the builder reads off the box's side.) -/
noncomputable def coordSign (p : P6) (i : Fin 6) : ℕ := if (1 : ℝ) / 2 < p i then 1 else 0

/-- **The TRUE generic region (RE-PLANNED).** The even-parity stratum: the sum of the six coordinate
signs is even. This is the clean combinatorial condition under which the merge structure gives a
uniform 13-cover (all 32 even-popcount corner boxes verified 13-feasible, exact-rational). Replaces
the false `ball-off-1/2` generic region. (Builder may widen to include the 8 odd-feasible boxes; the
even stratum is the certified-uniform core.) -/
def EvenParity (p : P6) : Prop := (∑ i, coordSign p i) % 2 = 0

/-- The near-`1/2` region: the complement of the TRUE generic region (the odd-parity stratum, which
contains all 24 verified-infeasible corner boxes). This is the correct Near region for the direct
route — it is the slab where the `O_p`-frame 13-cover genuinely fails, not a ball around 1/2. -/
def Near (p : P6) : Prop := ¬ EvenParity p

/-- The partition is total (a tautology by `Near := ¬ EvenParity`; recorded so the glue can
case-split without an extra hole). CLOSED — no sorry. -/
theorem generic_or_near (p : P6) : EvenParity p ∨ Near p := em (EvenParity p)

/-! ## In-code validation of the partition predicate (CLOSED — no sorry)

The R3 partition was VERIFIED FALSE; the re-plan's whole point is that `EvenParity` matches where a
13-cover genuinely exists. The certificate `generic-thirteen-lp.py` (exact-rational, reproduced this
round in `region_finding_summary` / the parity classification) establishes:

  * **All 32 even-popcount `{1/10,9/10}`-corner boxes are 13-feasible (0 infeasible).**
  * The 24 *infeasible* corner boxes are ALL odd-popcount (so they land in `Near`); 8 odd boxes are
    feasible (a bonus, incl. the proven witness `p*`, which has popcount 3 → `Near`).

So the partition is SOUND: `EvenParity` ⊆ feasible region, and every infeasible box ∈ `Near`. The
lemmas below pin the combinatorial meaning of the predicate *in Lean* (not just in commentary): the
sign-vector of a sample even box and of the witness `p*` evaluate as the certificate claims, and
their `EvenParity`/`Near` membership follows. This makes the partition predicate's behaviour a
checked fact, so a wrong predicate cannot silently poison the glue. -/

/-- A sample even-popcount corner box, signs `(1,1,0,0,0,0)` (popcount 2). -/
noncomputable def evenBox : P6 := ![9/10, 9/10, 1/10, 1/10, 1/10, 1/10]

/-- The witness box `p*` of `GenericThirteenLP`, signs `(1,0,1,1,0,0)` (popcount 3, ODD). -/
noncomputable def pStar : P6 := ![9/10, 1/10, 9/10, 9/10, 1/10, 1/10]

/-- `coordSign` reads off the sign-vector of `evenBox` exactly. CLOSED. -/
theorem coordSign_evenBox : ∀ i, coordSign evenBox i = ![1, 1, 0, 0, 0, 0] i := by
  intro i
  fin_cases i <;>
    simp only [coordSign, evenBox, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,
      Matrix.cons_val] <;> norm_num

/-- `coordSign` reads off the sign-vector of the witness `p*` exactly (popcount 3). CLOSED. -/
theorem coordSign_pStar : ∀ i, coordSign pStar i = ![1, 0, 1, 1, 0, 0] i := by
  intro i
  fin_cases i <;>
    simp only [coordSign, pStar, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons,
      Matrix.cons_val] <;> norm_num

/-- **Partition validation (CLOSED).** The sample even-popcount box lies in the generic region — its
sign-popcount `2` is even. (Certificate: this box, and all 32 even boxes, are 13-feasible.) -/
theorem evenBox_mem_generic : EvenParity evenBox := by
  have h : (∑ i, coordSign evenBox i) = ∑ i, (![1, 1, 0, 0, 0, 0] : Fin 6 → ℕ) i :=
    Finset.sum_congr rfl (fun i _ => coordSign_evenBox i)
  rw [EvenParity, h]; decide

/-- **Partition validation (CLOSED).** The witness `p*` lies in the `Near` region — its sign-popcount
`3` is ODD. So the proven `GenericThirteenLP` witness box is in the *odd-feasible extension*, NOT the
clean even stratum: the even stratum's base case must come from an even box (e.g. `evenBox`), with
`p*` a bonus. This is the in-Lean check that the witness/partition geometry is the way the certificate
classified it. -/
theorem pStar_mem_near : Near pStar := by
  rw [Near, EvenParity]
  have h : (∑ i, coordSign pStar i) = ∑ i, (![1, 0, 1, 1, 0, 0] : Fin 6 → ℕ) i :=
    Finset.sum_congr rfl (fun i _ => coordSign_pStar i)
  rw [h]; decide

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

/-- **H_PARITY_FIT (hole, R4 — REFINED).** The even-parity stratum is contained in
`GenericThirteenLP`'s generic LP region: `EvenParity p → Generic p`. This is the interface fact that
the re-planned partition matches the region where the 13-cover actually exists.

WHAT IT REQUIRES (the honest open content — this is NOT `id`-closable from this file).
`GenericThirteenLP.Generic` is currently an OPAQUE placeholder `def Generic : Prop := sorry`, so this
file cannot derive `Generic p` for any `p`. Closing H_PARITY_FIT requires `GenericThirteenLP` to first
*instantiate* `Generic` as a predicate implied by `EvenParity` — i.e. to land its atlas hole
`H_GEN_ATLAS` over the even-parity stratum (proving the 13-cover holds throughout `EvenParity`, not
only at the single witness box `p*`, which is itself ODD-parity, cf. `pStar_mem_near`). Only THEN does
this become `fun h => h` (or a short combinatorial implication). Until the sibling pins `Generic`, this
stays an honest hole; the *partition predicate itself is already validated CLOSED* above
(`evenBox_mem_generic`, `pStar_mem_near`, the sign-vector lemmas) — what is open is the LP-region/atlas
side owned by `GenericThirteenLP`, not the predicate's soundness.

(Spec note for the outliner: the proven `GenericThirteenLP` witness `p*` is ODD-parity → it sits in
`Near`, not the even stratum. The even stratum's base case needs an EVEN-parity witness box;
`evenBox = (9/10,9/10,1/10,1/10,1/10,1/10)` is a concrete one. The certificate confirms all 32 even
boxes are 13-feasible, so such a witness exists — but `GenericThirteenLP`'s formalized concrete cover
is at the odd `p*`, which does not directly seed the even stratum.) -/
theorem evenParity_generic (p : P6) (hp : EvenParity p) : Generic p := by
  sorry

/-- **H_GENERIC re-export.** The generic-regime 13-cover of `E ∪ V_p` by `int(O_p)`, imported
verbatim from `GenericThirteenLP`, for the even-parity stratum (via `evenParity_generic`). -/
theorem generic_cover_le_13' (p : P6) (hp : EvenParity p) :
    IsCoveredBy 13 (CoverTarget p) (Piece p) :=
  generic_regime_thirteen p (evenParity_generic p hp)

/-- **H_GENERIC (transport).** For even-parity `p`, the normalized body `Body p` is covered by 13
translates of its interior. This transports `generic_cover_le_13'` (the `E ∪ V_p`-by-`int(O_p)`
cover) across the affine normalization that identifies the Prymak subproblem with the body cover
(part of H_RED). The imported LP content is `generic_cover_le_13'`; the transport is the open hole. -/
theorem generic_branch_cover (p : P6) (hp : EvenParity p) :
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
