# Sketch `near-octant-budget` — finitize the near-1/2 corrective budget (R5, NEW)

**Goal:** the NEAR-1/2 half of $H_3 \le 13$ — the run's gating problem — recast as a DISCRETE,
decidable sign-pattern / hitting-set claim over a FIXED set of 8 corner directions, so it can
become Lean-FIT (or at least Lean-checkable) instead of the continuum coverability wall that
octahedral-direct's E1b hits.

## Why a new sketch (vs octahedral-direct)

octahedral-direct attacks the near-1/2 half via a CONTINUUM coverability claim ("every
forced-family broken vertex is corner-coverable"), which R4 proved is **not generic**
(`corner_coverability_is_not_generic`) — so its E1b core is Lean-hostile. This sketch takes the
explorer's **finitization route 1** (R5 scouting, "Analogous technique for finitizing budget≤7"):
the corrective directions live in a FIXED set of 8 octant-diagonal corners (R4's
`corner_cover_is_finite_hitting_set`), and "broken vertex $y$ is corner-coverable by $s$" is a
finite system of strict linear inequalities $s\cdot m > 0$ over $y$'s active normals. The recast:
inject the cube/min-vol-box geometry as a finite LINEAR SIGN SYSTEM on the normals, turning
"broken ⇒ corner-coverable, budget ≤ 7" into a finite-case implication over sign patterns — the
shape `decide`/`linarith` close (the same way H_GEN_EDGES finitized).

Borrows: octahedral-direct (E0 core-6 base case + the exact corner predicate / hitting-set
structure) and the cached `IsCoveredBy` vocabulary from certify-fourteen.

## Skeleton / holes (`lean/Sketches/NearOctantBudget.lean`, builds green)

- **N0** (base, imported): 6 core directions $\pm e_i = -V$ illuminate the symmetric core
  (octahedral-direct E0, closed exact).
- **N1** `broken_vertex_corner_coverable` (HOLE — load-bearing): under the min-vol-box sign system
  `MinVolBoxNormals M`, every broken vertex has a covering corner among the 8. **The cube-geometry
  injection** — the abstract version is FALSE (R4), so the sign system is what carries it. Proof
  intended as a finite case analysis over the sign patterns `MinVolBoxNormals` forces.
- **N2** `corner_budget_le_7` (HOLE): a set of ≤ 7 corners hits the whole broken set; the 8th
  excluded by volume balancing (no min-vol box breaks all 8 octant cones at once — explorer route 3
  folded in as the cap). Decidable over `Fin 8` once N1 gives per-vertex coverers.
- **N3** `near_body_covered_by_13` (assembly HOLE): 6 (core) + ≤ 7 (corrective) = 13 illuminating
  directions ⇒ the forced-family body is covered by 13 translates of its interior. Feeds
  `lassak-glue.near_cover_le_13`.
- **CLOSED now** `hits_mono`: superset of a hitting set still hits (combinatorial sanity, exercises
  the `Fin 8` machinery green — de-risks the Lean path).

## Hard step

**N1** — the cube-geometry sign system. The whole difficulty of the near-1/2 regime is concentrated
here: deriving from min-vol-box optimality (six face-center contacts + volume balancing) a FINITE
linear sign system on each broken vertex's active normals that forces a covering corner. If this
system is genuinely finite and linear, N1 closes by `decide`/`linarith` and the near-1/2 half
becomes Lean-fit; if the optimality conditions are irreducibly quadratic (volume), N1 needs a
linear envelope/relaxation that still forces coverability, and the residue is a directed-rounded
continuum certificate. This is the run's load-bearing open problem.

## Certify

Lean if N1 finitizes (the whole point of the recast); numerical directed-rounded fallback for the
volume-balancing envelope if the optimality conditions resist linearization. N2's hitting-set core
and N3's assembly are finite/Lean-fit regardless.

## Claimed bound

**NONE** — N1/N2/N3 are open holes; the near-1/2 half does not yet move the bound. Table value to
beat: $H_3 \le 14$. The combinatorial kernel (`hits_mono`, the `Fin 8` hitting-set shape) is the
only closed content; the load-bearing N1 is the wall.
