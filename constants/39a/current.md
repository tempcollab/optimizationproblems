# 39a — $H_3$ (Hadwiger covering / illumination number in $\mathbb{R}^3$)

## Status
none

## Bounds
table: $H_3 \le 14$ (Prymak 2023; verified record to beat) · lower $H_3 \ge 8$ (cube).
held: $H_3 \le 14$ (the known record; this run has not yet beaten it).

## Progress log
- R1: Verified structural facts (exact rational, reviewer-reproduced + independently re-derived).
  At $p=(1/2,\dots,1/2)$: the 14 marked points (8 cube vertices + 6 face centres) have all 91
  pairwise $\ell_1$-distances $\ge 1$, min exactly 1 (51 pairs on the boundary of $O_p-O_p$),
  so none coverable by one translate of $\operatorname{int}(O_p)$ — Prymak Remark 2.3 reproduced.
  The regular octahedron's minimal-volume circumscribing parallelotope has volume 2 (det-4 $\pm1$
  matrix), strictly below the cube's 8 — so the cube is NOT its min-vol box and $O_p$ does NOT
  normalize to $p=1/2$ (sketch A's F2 correct; sketch C's contrary claim refuted).
  Lean infra (sketch D): genuine sorry-free, axiom-clean `H3` registry definition + four reusable
  covering primitives certified into `lemmas/`. No bound improvement this round (held stays 14).
- R3: Closed the marked-point core of generic-thirteen-lp's load-bearing hole H_GEN_τ in Lean
  (`marked_points_covered_by_thirteen`, sorry-free, axiom-clean `[propext, Classical.choice,
  Quot.sound]`). Independently re-derived in exact rational arithmetic: at the off-center box
  $p^*=(9/10,1/10,9/10,9/10,1/10,1/10)$ the 14 marked points (8 cube vertices + 6 contacts $V_{p^*}$)
  are covered by exactly **13** explicit rational translates of $\operatorname{int}(O_{p^*})$ (one
  merge, translate 5 covers two points), every point strictly interior (min facet slack $1/35>0$);
  confirmed the 8 facet inequalities cut out a 6-vertex polytope whose vertices are exactly $V_{p^*}$,
  so `PieceStar` is the genuine $\operatorname{int}(O_{p^*})$ (no weakened proxy). Lassak-glue's
  top-level `H3_le_13 : H3 ≤ 13` confirmed (by `rfl`) to target the genuine registry def with no
  bound smuggling; its hard content remains honest open holes. Structural finding (reproduced): the
  13-feasible region is THIN — only 40/64 corner boxes admit a 13-cover, single-/two-coordinate
  offsets do not (point-mergeability ≠ edge-feasible 13-cover) — so the two-regime partition must be
  re-planned. No bound improvement this round (held stays 14; target NOT reached hole-free).
- R4: Closed generic-thirteen-lp's edge half H_GEN_EDGES in Lean, sorry-free, axiom-clean
  (`edges_covered_by_thirteen`, `target_star_covered_by_thirteen`: `[propext, Classical.choice,
  Quot.sound]`, no sorryAx). Independently re-derived in exact rationals: the 12 genuine cube
  edges (verified = the real adjacent-vertex edge set) are each covered by 2 of the same 13
  translates of `int(O_{p*})` along the edge line, strict interior at every subinterval endpoint
  (tightest slack 1/35 > 0); the 8 facets recover exactly the 6 vertices V_{p*}, so `PieceStar`
  is the genuine octahedron (no proxy). With the R3 marked-point core, the FULL target E ∪ V_{p*}
  is now covered by 13 translates of int(O_{p*}) hole-free AT THE WITNESS BOX p* — the per-box
  generic step is hole-free; H_GEN_ATLAS (tile the thin region) + the near-1/2 glue remain open.
  Promoted `segment_covered_by_two` (+ `edgeSeg`) to lemmas/ (multi-D companion of
  `icc_covered_by_two`, axiom-clean). Independently reproduced lassak-glue's even-parity partition:
  all 32 even-popcount corner boxes exact-verified 13-feasible (0 infeasible), all 24 infeasible
  boxes odd-popcount → land in Near; so `EvenParity ⊆ 13-feasible` (sound partition predicate, does
  not poison the glue); 4 partition-validation lemmas axiom-clean. octahedral-direct advanced E1b
  structure (exact rational illumination predicate, finite corner hitting-set, honest-limit
  counterexample independently reproduced); E1a + E1b coverability/budget stay open (budget≤7 is a
  labeled conjecture, not certified). No bound improvement this round (held stays 14; no global
  ≤13 reached hole-free — H_GEN_ATLAS + the near-1/2 wall remain).
