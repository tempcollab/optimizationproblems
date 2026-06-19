# mixed-construction — <=62-dim G_2(4) section core + perturbation in 62 dims

**Attack line D** (explorer §5). The speculative wildcard.

## Target
A finite point set `X` in `R^62`, `|X| >= 316`, whose **diameter graph** `G_d` has
independence number `alpha(G_d) <= 5`, giving Borsuk parts
`chi(G_d) >= ceil(|X|/5) >= 64 > 63`. `X` need NOT be two-distance.

## CORRECT criterion (reconciled round 3 — a correctness fix)
Borsuk(X) = `chi(G_d)`, `G_d` = diameter graph (edge iff dist == diameter). A part has
diameter < diam, so it is an **independent set of G_d**. Lower bound
`chi(G_d) >= |X| / alpha(G_d)`. So the certifiable target is **`alpha(G_d) <= 5`**, i.e.
`omega(complement of G_d) <= 5` (the non-diameter graph). For a two-distance set the
complement is exactly the smaller-distance graph; for G_2(4)'s C-points that is the induced
adjacency `A[T,T]` (adjacency <-> inner product 18 <-> the *smaller* distance), so the
certified g24 fact `omega(A)=5` is precisely `alpha(G_d)=5`.

**Round-2 bug fixed:** the old `verify()` checked `omega` of the *diameter* graph — the wrong
quantity. The part bound is governed by `alpha` of the diameter graph = `omega` of its
*complement*. `verify()` now uses the correct graph, with exact integer rank + exact clique,
matching the certified `fresh-orthogonal-dir`/`g24` machinery. (Intermediate-statement search.)

## Holes
1. **`build_core`** — **CLOSED (round 3).** A G_2(4) hyperplane section of `C` that sits
   **exactly in 62 dims**. Take the standard partition `B,C` (|C|=320, spans exactly 63), then
   delete the C-points lying in the B-structure of a *second* isotropic point (the structured
   family of `fresh-orthogonal-dir`). The surviving `T ⊆ C` has **`|T| = 270`**, exact integer
   rank over Q `= 62` (certified by `fo.exact_rank`, not float SVD), and smaller-distance clique
   `omega(A[T,T]) = 5` = `alpha(G_d) = 5` (certified by exact bitset `g24.max_clique_le`).
   `ceil(270/5) = 54`. This is a genuine, exactly-certified two-distance core in 62 dims.
   No float rep is load-bearing.
2. **`engineer_perturbation` (load-bearing)** — **OPEN**, obstruction now made precise.
   Need `>= 46` more points (316 − 270) inside the same 62-dim subspace keeping
   `alpha(G_d) <= 5`. A bounded greedy search (20000 iters / 90 s cap, frequent stdout)
   accepted **0** points. Diagnosis (separate bounded probe): the core nearly *fills* the ball
   of diameter² = 192, so any addable point `p` (one not growing the diameter) is at the
   diameter from only ~2 core points and at *non-diameter* distance from ~268 of them. Hence
   `p` is a complement-neighbor of ~268 core points; those contain 5-cliques of the complement
   (the core's `omega(complement) = 5`), so `p` extends a 5-clique to 6 → `alpha(G_d)` jumps to
   ≥ 6 → the part bound collapses. A valid `p` would need to be at the diameter from all but ≤4
   core points — geometrically impossible against this core (the diameter sphere only grazes ~2
   points). This is exactly why Gri added only ONE non-two-distance point. **Open construction:**
   either a *different*, less ball-filling 62-dim core that leaves diameter-sphere room for many
   addable points, or a fundamentally different perturbation family (e.g. simultaneously
   re-choosing the diameter).
3. **`verify`** — done (corrected): builds the diameter graph directly, checks `dim<=62`
   (exact for the integer core), `alpha(G_d) <= 5` (exact clique of the complement),
   `ceil(n/5) >= 64`. `verify_core_exact` certifies the core exactly.

## Status / claim
- **build_core CLOSED** — exactly-certified 62-dim, 270-point two-distance core (subset of C).
- **engineer_perturbation OPEN** — best reached `|X| = 270` (`ceil = 54 < 64`); deficit 46 pts.
- **Claimed value: NONE / no improvement.** Upper bound stays the verified **63** (table 63).
  The 270-point 62-dim core is real and certified but is NOT a counterexample
  (`54 < 64`); reaching 316 in the fixed subspace is the undischarged load-bearing hole, now
  with a precise geometric obstruction. Nothing written into `current.md`.

## How it evades the named obstruction (and where it still bites)
Unlike A/B it does NOT need `C` (or any single SRG) to drop to 62 dims as a whole — the 270
core sits in 62 dims by exact rank from the start. But the perturbation count runs into a
*new* wall: the certified core is so dense in its diameter ball that no extra point can be
added without inflating `alpha(G_d)`. The "buy a dimension with controlled extra points" plan
needs a sparser core; that is the remaining live question.

## What would push it further
- A 62-dim section with the *same* `alpha <= 5` but **fewer points clustered against the
  diameter** (room on the diameter sphere) — then near-boundary points become addable.
- Or change the diameter: add a *shell* of points at a NEW, larger distance so the old
  pairs stop being diameter pairs (resets `G_d`), à la Gri — but keeping `alpha` capped.
- The general (non-structured) 62-dim section question (does a >270 section of C exist?) is the
  open hole in `fresh-orthogonal-dir`; a larger core shrinks the perturbation deficit.

## Promotable lemmas
None this round. (`_omega_le` duplicates the certified `g24.max_clique_le` on a boolean matrix
and was cross-checked equal on the core, but it is sketch glue, not a new general fact. The
270-point exact-rank-62 core is a concrete object, not a reusable lemma.)
