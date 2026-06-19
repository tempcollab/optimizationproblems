# Sketch `generic-thirteen-lp` — the Lean-fit generic-regime $14\to13$ half

**Goal:** the generic-regime half of $H_3\le 13$. Prymak's reduction gives
$H_3 \le \max_{p\in[0,1]^6} C(E\cup V_p,\operatorname{int}(O_p))$ with the 14-floor supported
ONLY at $p=(1/2,\dots,1/2)$. Away from 1/2 a vertex/face MERGE should drop $14\to13$. This sketch
is the finite/rational/Lean-fit half (the near-1/2 neighbourhood is a sibling, `octahedral-direct`).

Lineage: continuation of `special-case-p-half`'s Lean-fit generic engine (A2/A3); the enlargement
half (A1′) is retired (geometrically dead, R3).

## Round 3 (builder) — what I CLOSED

**The load-bearing combinatorial hole H_GEN_τ is closed at one concrete off-center box, and its
marked-point core is now a sorry-free, axiom-clean Lean lemma.**

- Built the full covering LP **including the 12 edges** (`generic-thirteen-lp.py`): 13 translates
  with free rational centers; every cube vertex, every face point, and every edge (1-D, covered by
  its two endpoint vertex-translates) must be covered. Searched over covering structures
  (vertex-merge and face/face-merge), solved each as a margin-maximizing float LP to PROPOSE
  centers, then **re-verified EXACTLY with `Fraction` arithmetic** (no float in the load-bearing
  check; `scipy` only proposes).
- **Witness:** at $p^*=(9/10,1/10,9/10,9/10,1/10,1/10)$ (every $p_i$ a full $2/5$ off 1/2), the 14
  marked points are covered by **13** translates of $\operatorname{int}(O_{p^*})$ — one merge
  ($q_{20}$ shares vertex-translate $t_5$), strict-interior margin $0.0218$. Exact rationals
  recorded; `verify_witness()` re-derives it deterministically.
- **Lean:** `Sketches/GenericThirteenLP.lean` now contains `inOpStar` (the open polytope via the 8
  exact integer facets), `markedStar` (14 points), `centerStar` (13 rational translates),
  `assignStar` (duty map with the merge), and two sorry-free lemmas:
  - `markedStar_mem` — every marked point minus its assigned translate lies in
    $\operatorname{int}(O_{p^*})$ (the exact rational Farkas membership, by `norm_num`);
  - `marked_points_covered_by_thirteen : IsCoveredBy 13 (Set.range markedStar) PieceStar`.
  Both axiom-clean (`[propext, Classical.choice, Quot.sound]`, no `sorryAx`). `lake build
  Sketches.GenericThirteenLP` green (2412 jobs); `LassakGlue` (which imports this) still green.

## Round 4 (builder) — what I CLOSED: H_GEN_EDGES

**H_GEN_EDGES is now CLOSED in Lean, sorry-free and axiom-clean.** The 12 cube edges are covered
by the SAME 13 translates `centerStar` of `int(O_{p*})` that cover the marked points.

- Built the reusable multi-D segment-cover primitive `segment_covered_by_two` (and its subset
  form `segment_subset_two`): a parametrized segment `{v₀ + s·u : s ∈ [0,1]}` is covered by two
  translates of an arbitrary open piece `P ⊆ ℝ³` whenever a split parameter `σ ∈ [0,1]` exists
  with the first translate covering `s ∈ [0,σ]` and the second `s ∈ [σ,1]`. This is the multi-D
  generalization of cached `icc_covered_by_two` (a 1-D interval vs `[0,L]`) — same two-translate
  endpoint logic, lifted to a segment in ℝ³ vs a polytope. **Promotable** (see below).
- Ported the exact `edge_covered_exact` data: defined `cubeEdge` (the 12 edges as `(v₀,u)` pairs)
  and `edgeCover` (each edge's two endpoint vertex-translate indices + the exact rational split
  `σ ∈ {1/2, 5/12, 7/12}` read off the certificate's reach-interval overlaps). Proved
  `cubeEdge_subset` (each edge ⊆ the 13-translate union) and `edges_covered_by_thirteen`
  (`IsCoveredBy 13 (⋃ edges) PieceStar`). The load-bearing inequality per edge is the 8 facet
  inequalities `n·(v₀ + s·u − cₜ) < d`, each LINEAR in `s`, closed by `linarith` from `0≤s≤σ`
  (resp. `σ≤s≤1`) — checked in code, no hand-wave.
- Capstone `target_star_covered_by_thirteen`: edges ∪ marked points = the FULL target `E ∪ V_{p*}`,
  covered by 13 translates (same family, no extra pieces). So `C(E ∪ V_{p*}, int(O_{p*})) ≤ 13` at
  `p*` is now fully machine-checked in Lean (was: marked-points-only in R3).
- `#print axioms` on all five new theorems: `[propext, Classical.choice, Quot.sound]` — NO
  `sorryAx`. `lake build Sketches.GenericThirteenLP Sketches.LassakGlue` → exit 0, 2413 jobs.

## Holes that REMAIN (honest, the bound is still 14 globally)

- ~~**H_GEN_EDGES**~~ — **CLOSED R4** (see above). The 12 edges are Lean-certified at `p*`.
- **H_GEN_ATLAS** (REVISED — see Spec concern): a finite atlas of the THIN 13-feasible region (NOT
  $[0,1]^6\setminus N(1/2)$), each box feasible over $Q_P=\bigcap_{v\in P}O_v$, plus its complement
  handed to the near-1/2 sibling. The single-point witness is the $|P|=1$ base case. Open.
- **H_GEN_GLUE / Prymak reduction**: $\max_p\le13$ over the atlas, then glue to $H_3$ (shared with
  certify-fourteen's D-holes and `lassak-glue`). Open.

## Spec concern (NON-EMPTY — the plan needs a rework here)

The planned H_GEN_ATLAS assumed the 13-feasible region is all of $[0,1]^6\setminus N(1/2)$ and that
a coarse atlas suffices. **This is FALSE.** My exact LP screen shows:
- A single-coordinate offset from 1/2 (e.g. $p_0=9/10$, rest 1/2) has **NO** 13-cover — the merge
  is point-available but the 13-structure is edge-INFEASIBLE.
- Two-coordinate offsets likewise infeasible. The alternating corner $(9/10,1/10,\dots)$ infeasible.
- Only **40/64** of the $\{1/10,9/10\}$-corner boxes admit a 13-cover; margins are tiny
  ($\sim0.001$–$0.02$).

Root cause: **point-mergeability $\ne$ edge-feasible 13-cover.** The 14→13 merge frees a covering
piece ONLY where the 8 vertex-translates ALONE still cover all 12 edges, which requires ALL six
$p_i$ bounded off 1/2 in a compatible pattern. So the generic/near-1/2 partition is NOT a simple
ball around 1/2: a large slab of $[0,1]^6$ (single-/two-coord offsets) is neither "generic-13" nor
"near-1/2-symmetric" and currently falls through both halves. **This is for the outliner**: the
two-regime partition that `lassak-glue` assumes (`Near := ¬Generic`, `Generic` = bounded off 1/2)
does not match where 13 is actually achievable. Either (a) the near-1/2 sibling must cover this
whole non-13 slab directly (much larger than a neighbourhood of 1/2), or (b) a richer covering
piece / structure than translate-of-$O_p$ is needed off-diagonal. The strategy line is sound at the
corners but the region geometry must be re-planned.

## Claimed value (CLAIM, unverified until reviewer confirms)

- **Verified this round (reproducible, R4):** $C(E\cup V_{p^*},\operatorname{int}O_{p^*})\le 13$ at
  the single box $p^*$ — now FULLY machine-checked in Lean (`target_star_covered_by_thirteen`,
  axiom-clean): edges (`edges_covered_by_thirteen`, R4) + marked points
  (`marked_points_covered_by_thirteen`, R3). No `sorry` on this per-box result.
- **Global bound CLAIM:** still **14** (NOT improved). The 13 holds only at $p^*$ (and ~40/64
  corners); H_GEN_ATLAS + the near-1/2 half are open, and the Spec concern shows the region is
  thin. Table value to beat: $H_3\le14$. This sketch does **not** yet beat it — the per-box
  generic step is now hole-free, but the atlas tiling + near-1/2 glue remain.

## What would push it further
1. Re-plan the regime partition (outliner) given the thin-region finding above.
2. Port H_GEN_EDGES to Lean via a segment-vs-polytope interval primitive (reuse `icc_covered_by_two`
   idea in 3-D), to make the per-box 13-cover fully Lean-certified.
3. If the off-diagonal slab cannot be 13-covered by translates of $O_p$, escalate to door (b)
   (a different covering piece) — but that is an outliner strategy decision, not a builder fill.

## Promotable lemmas

**`segment_covered_by_two`** (and its subset form **`segment_subset_two`**) — proved green and
axiom-clean this round in `lean/Sketches/GenericThirteenLP.lean` (just after `marked_points_…`).
GENERAL, reusable (not tied to the witness box):

> `segment_covered_by_two (v0 u c_a c_b : Fin 3 → ℝ) (P : Set (Fin 3 → ℝ)) (σ : ℝ)`
> `(hσ0 : 0 ≤ σ) (hσ1 : σ ≤ 1)`
> `(ha : ∀ s, 0 ≤ s → s ≤ σ → (fun k => edgeSeg v0 u s k - c_a k) ∈ P)`
> `(hb : ∀ s, σ ≤ s → s ≤ 1 → (fun k => edgeSeg v0 u s k - c_b k) ∈ P) :`
> `IsCoveredBy 2 (edgeSeg v0 u '' Set.Icc (0:ℝ) 1) P`

This is the multi-D generalization of cached `icc_covered_by_two` (1-D interval → ℝ³ segment vs an
arbitrary piece). Reusable by any sketch needing 1-D-edge / segment coverage against a polytopal
piece (lassak-glue's transport, certify-fourteen's edge step, octahedral-direct's corrective
segments). Reviewer: certify into `lemmas/` if it carries the bar (it depends on the local def
`edgeSeg v0 u s := fun k => v0 k + s * u k`, which should travel with it).

`markedStar_mem` / `marked_points_covered_by_thirteen` / `cubeEdge_subset` /
`edges_covered_by_thirteen` / `target_star_covered_by_thirteen` remain sketch-specific (tied to the
concrete witness box $p^*$ and the `centerStar` data) — do NOT promote.
