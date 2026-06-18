# cpsat-exact-existence-N28-N30 — exact-α search for an indecomposable N∈{30,32,34} (4,5)-set beating 4/7

**Type:** gadget half of an upper-bound beat (numerical, conjecture-only this round).
**Status (R5):** BUILT (first time — was an empty placeholder since R4). NEGATIVE /
obstruction result. No candidate beating 4/7 found; a robust **τ-deficit obstruction** is
recorded. Re-runnable cert: `constants/5b/certificate/search_N30.py`.

## Idea

By [MT26] Theorem 1.5, `c* = inf_N f(N)/N` where `f(N) = min over (4,5)-sets of size N of
h(A)`, and `h(A) = ` largest Sidon subset `= ` independence number α of the 3-AP hypergraph
(Lemma 2.3). So ONE indecomposable (4,5)-set `A` with `h(A)/|A| < 4/7` strictly beats the
verified record 4/7. The smallest sizes where the empirically-reachable value `h = ⌈9N/17⌉+1`
(floor+1) itself beats 4/7 are `N ∈ {30, 32, 34}`:

| N  | floor=⌈9N/17⌉ | target h=floor+1 | ratio   | beats 4/7? |
|----|---------------|------------------|---------|------------|
| 28 | 15            | 16               | 16/28 = 0.5714 | **NO (ties exactly)** |
| 30 | 16            | **17**           | 17/30 = 0.5667 | YES |
| 32 | 17            | 18               | 18/32 = 0.5625 | YES |
| 34 | 18            | 19               | 19/34 = 0.5588 | YES |

(All four rows re-verified exactly in `search_N30.py::part_arithmetic`, integer arithmetic.)
Block assembly is dead (Lemma 3.6: a well-separated union has additive h → mediant → tie at
best; two A_base copies = 16/28 = 4/7). So the gadget MUST be a **single indecomposable** set.

## What was built (R5)

`constants/5b/certificate/search_N30.py` — a deterministic, re-runnable exact-α search:

- **(4,5)-property** checked EXACTLY by the **difference condition** (every 4-subset has ≥5
  distinct pairwise |differences|) — the corrected definition (R2, verified vs arXiv:2602.23282),
  strictly stronger than weak-Sidon. An incremental `add_keeps_45` checks only the C(|A|,3) quads
  containing the new point, making greedy construction fast.
- **h(A) computed EXACTLY** as `α = N − τ`, τ = min 3-AP transversal, by an **ILP** (`scipy.milp`)
  AND cross-checked by a deterministic branch-and-bound `alpha_bb` (the two agree on every
  reported set — `milp == bb`). NEVER a 3-AP-edge-count heuristic (the standing rule: maximizing
  edges does NOT minimize α).
- **Indecomposability** checked by `block_split` (no well-separated 2-block split → not killed by
  Lemma 3.6).
- **Search**: greedy (4,5)-set builder + simulated annealing (`anneal_alpha`, accept-worse to
  escape plateaus) + hill-climb polish (`hill_climb_alpha`), all keeping the (4,5)-property every
  move, α minimized EXACTLY. Seeded both OUTSIDE the A_base basin (random restarts, Fibonacci/CRT/
  Singer templates) AND from the A_base basin (direct extension), all deterministic (seeded RNG).

## Result — NEGATIVE, with a τ-deficit obstruction; best from a STRUCTURED family

No (4,5)-set with `α ≤ floor+1` was found at any N ∈ {30,32,34}. The **lowest-α sets came from a
structured seed, not the random search** — the (4,5)-valid subsequence of the **Fibonacci numbers**
(dropping the {1,2,3,5} difference collisions) gives a clean indecomposable family, exact α
(milp==bb verified), `α = floor+3` at every N:

| N  | best α (Fib family) | floor | floor+1 (target) | ratio   | beats 4/7? | random-search wall |
|----|---------------------|-------|------------------|---------|------------|--------------------|
| 30 | **19**              | 16    | 17               | 0.6333  | no (floor+3) | 20–21 |
| 32 | **20**              | 17    | 18               | 0.6250  | no (floor+3) | 22 |
| 34 | **21**              | 18    | 19               | 0.6176  | no (floor+3) | — |

All recorded in `BEST_SETS`. Random/anneal (basin-free, win 2200/3000, many restarts) and
A_base-direct-extension (indecomposable, valid) BOTH wall HIGHER (α ≈ 20–22 at N=30); the Fibonacci
structured family is decisively best. Other structured seeds fail: CRT/Singer templates keep only
7–9 of 30 points under the (4,5) filter; geometric (3^k) is 3-AP-free (α=N).

**The obstruction, stated precisely (`part_obstruction`, re-verified exactly):**
A beat at N needs `τ = N − α ≥ N − floor − 1`, i.e. a τ-density:

| set                  | N  | α  | τ  | τ/N    |
|----------------------|----|----|----|--------|
| A_base (record)      | 14 | 8  | 6  | 0.4286 |
| **target N=30**      | 30 | 17 | 13 | 0.4333 |
| **best found N=30**  | 30 | 19 | 11 | **0.3667** |

The best achieved τ-density (~0.37) stays below both the floor+1 target (~0.43) AND A_base's own
rate (0.4286). The per-point transversal efficiency does not reach A_base's level at larger N in the
searched region — the opposite of what a beat requires. The **τ-deficit is 2 at every N ∈ {30,32,34}**
(realized `α = floor+3`, need `floor+1`).

**Why:** the (4,5) difference condition is severe — it forbids 4-term APs and most overlapping
3-AP configurations ({0,2,3,4,6}, which packs 4 3-APs, is NOT a (4,5)-set; no translate-union of
A_base is a (4,5)-set for any shift in [500,2200)). 3-AP density (which lowers α) and the (4,5)
separation pull in opposite directions, and A_base (an AI-optimized record at N=14) sits near the
extremal trade-off. Sustaining its τ-rate to N=30 in a single indecomposable set was not achieved.

## Honest compute limits

- α is **exact** everywhere (ILP + B&B cross-check); the SEARCH (anneal/hill-climb) is heuristic,
  so "best α = 19 at N=30" is an **upper bound on the realizable min α in the searched space**, NOT
  a proof that α=17 is impossible. It is strong evidence (multi-method, random + basin-seeded +
  structured Fibonacci/CRT/Singer templates, ~40 min of search), not a theorem.
- Budget: ~440s/N annealing at window 2200, plus separate win=3000 runs (reached 20) and an A_base
  extension run (reached 21). Larger windows dilute 3-AP density; smaller windows can't fit a
  size-30 (4,5)-set (greedy needs window ≳2000 to reach N=30).
- This is a CONJECTURE-only deliverable: NO bound is written into `constants/5b.md`.

## What would push it further

1. **A structured low-α construction** is the road, confirmed: the Fibonacci subsequence already
   beats random search (α=floor+3 vs floor+4/5), so the extremal trade-off is structural. Push the
   Fibonacci idea — a recursive `a(n)=a(n-1)+a(n-2)`-type layout packs 3-APs `{a,a+d,a+2d}` while the
   super-increasing growth keeps the difference condition; engineering ONE more τ per ~15 points
   (closing floor+3 → floor+1) is the target. Generalized-Fibonacci / Zeckendorf-window variants and
   2-scale designs (where cross-scale 3-APs add τ without breaking (4,5)) are the next experiments.
   Naive extension and translate-union both fail (verified R5).
2. **An exact-α-minimization ILP/CP over the point coordinates** (not just over the transversal):
   a single MILP that places N points AND minimizes α subject to the (4,5) constraints — far
   heavier, but exact, and would either find α=17 or (with optimality) prove a wall at a given N.
3. **A lower bound on f(N) at N=30** would CLOSE this angle: if one can prove `f(30) ≥ 18` (i.e.
   every (4,5)-set of size 30 has α ≥ 18), then N=30 cannot beat 4/7 even in principle, and the
   search target shifts. The τ-density obstruction is suggestive of such a structural bound.
4. The paired Lean cert (`interleaved-residual-cert`, built in parallel R5) is what would certify
   any candidate this search DOES find — but with no sub-4/7 candidate, there is nothing to certify
   yet. The two halves have not converged.

## Sources

- [MT26] J. Ma, Q. Tang, arXiv:2602.23282 — Thm 1.5 (`c*=inf f(N)/N`), Lemma 2.3 (h = α of 3-AP
  hypergraph), Lemma 3.6 (well-separated union additivity), (4,5)=difference condition.
- Lower bound `c* ≥ 9/17` ⇒ `h ≥ ⌈9N/17⌉` (the floor), [MT26].
