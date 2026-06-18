# stage-a-max-m-bounded-N30 — direct max-m search over N=30 (4,5)-sets, bounded chunks

**Constant:** C_5b (Erdős #757, Sidon density inside (4,5)-sets). Direction: UPPER bound.
**Record to beat (verified):** c* ≤ 4/7 = 0.5714286 ([MT26], Lean-reproduced).
**Arithmetic beat target:** an indecomposable N=30 (4,5)-set with m = n−2 = 28 and
τ = 13 ⇒ α = N−τ = 17 ⇒ 17/30 ≈ 0.5667 < 4/7. (α ≤ 17 ⇔ τ ≥ 13; HY at m=28 permits
τ ≤ ⌊234/17⌋ = 13, so α=17 is allowed, not forbidden.)

## Idea
The R5 obstruction was diagnosed (explorer, R8 outline) as an **edge-deficit = τ-deficit**:
the best N=30 (4,5)-set found had m = 26 vs the Lemma-2.4 cap n−2 = 28, near-path, α = 19 =
floor+3. R5's search walled because it minimized α *blind to m*. This approach instead
**directly MAXIMIZES m** (the cheap incremental midpoint-injective 3-AP count) over a
**fixed finite candidate pool**, then runs **exact α = N−τ only on the high-m shell** Stage A
surfaces. The thesis: reach the edge cap m=28 first, then check whether α drops to ≤17.

## What was built (R8)
A full rewrite of the DISQUALIFIED R6 anneal loop (`search_N30_mtargeted.py`, which hung
silently and force-killed R6 + R7) into the **binding bounded-compute protocol**:
`constants/5b/certificate/search_N30_stageA.py`.

- **Fixed finite pool P, built once up front** (`build_pool`, NOT an unbounded `{0..W}` box):
  union of A_base coords + the genuine small-scale Fibonacci numbers ≤ 2200 (affine-invariant,
  so they carry real 3-AP structure; the huge-scale R5 subsequence at span 2.18M does NOT
  survive rescaling-with-rounding — that map is non-affine and destroys APs) + a
  Zeckendorf/generalized-Fibonacci lattice (sums of ≤3 distinct Fibonacci numbers) + a
  quadratic-residue/Singer lattice mod a prime near the window + a coarse arithmetic grid.
  **|P| = 1461 in window [0,2200]** (saved to `stageA_pool.json`).
- **Stage A = maximize m, in bounded chunks** (`run_stageA`): best-improvement replacement
  hill-climb (swap out the lowest-3-AP-degree vertex, scan a sampled batch of pool points,
  take the best m-gain) with random kicks + intensification from the best set so far. Each
  chunk has a **hard per-chunk wall-clock cap** (`--chunk-seconds`) and the whole run a
  **hard total cap** (`--total-seconds`); at every chunk boundary it **prints (best m,
  visited, elapsed) and flushes**, and persists the shell + best set to disk
  (`stageA_shell.json`, `stageA_best.json`, `stageA_progress.log`) so a kill loses nothing.
- **Stage B = exact α only on the high-m shell** (`run_stageB`): EXACT α = N−τ via
  scipy.milp cross-checked by branch-and-bound (`search_N30.alpha_exact`, milp==bb — NEVER a
  density heuristic, per Rule), run only on the m ≥ M_SHELL sets Stage A surfaced.

## Result (R8) — a sharper VERIFIED NEGATIVE over the fixed pool P
Two independent bounded batches (~185 s each, seeds 20260808 and 11111), all caps honored,
continuous progress printed:

- **Stage A walls at m = 26 over P** (edge cap is 28). max-m climbed 23 → 25 → 26 across
  chunks; never reached the cap m = n−2 = 28 the beat target requires. (Notably m=26 is now
  reached inside a **bounded window ≤ 2200** — R5 only hit m=26 at the ~2.18M Fibonacci
  scale, so this is a genuinely new finding: the edge-deficit of 2 persists even at moderate
  scale.)
- **Stage B exact-α frontier over P** (50 sets at m ≥ 24, all verified is45set + milp==bb):

  | m  | best α (exact) | τ | α−floor | beats 4/7? |
  |----|----------------|---|---------|------------|
  | 25 | 21             | 9 | floor+5 | no         |
  | 26 | **20**         | 10| floor+4 | no         |

  The max-m level (m=26) reaches only α = 20 = floor+4 — **NO beat** (a beat needs α ≤ 17).

- **Nuance (recorded):** R5's *specific* unbounded Fibonacci m=26 set has α = 19 (floor+3),
  *lower* than these bounded m=26 sets' α = 20. This re-confirms the Rule that maximizing m
  is *necessary but not sufficient* for low α — α depends on the AP overlap/covering pattern,
  not just the edge count. So even reaching the cap m=28 would not guarantee α ≤ 17.

**This is strictly sharper than R5's blind-α wall:** R5 reported "no set with α ≤ floor+1";
here the *direct max-m objective* establishes the mechanism — over the named pool P the
edge-deficit cannot be closed (m walls at 26 < 28), and the exact (m,α) frontier shows α
stays ≥ floor+4 even at the max m reached. Honest scope: this is a wall **over the fixed
pool P**, NOT a global impossibility claim.

## Reproduce
```
cd constants/5b/certificate
python3 search_N30_stageA.py --pool                       # build + print |P|=1461 (instant)
python3 search_N30_stageA.py --stageA --chunks 4 --chunk-seconds 45 --total-seconds 185 --seed 11111
python3 search_N30_stageA.py --stageB                      # exact alpha on the saved shell
python3 search_N30_stageA.py --verify-frontier            # fast deterministic re-check (~5s)
```
The `--verify-frontier` path re-derives the two frontier-defining sets EXACTLY (is45set +
α via milp==bb) from the recorded `FRONTIER_SETS` constant — the reviewer's reproduction
entry point (no search needed). Artifacts: `stageA_pool.json`, `stageA_shell.json`,
`stageA_best.json`, `stageA_progress.log`.

## Claim (UNVERIFIED until reviewer confirms)
No bound is claimed against 4/7 — this is a **verified NEGATIVE**, not a beat. The claim is:
*over the fixed structured pool P (|P|=1461, window [0,2200]), the maximum m attainable by a
size-30 (4,5)-set is 26 (< cap 28), and the minimum exact α over the surfaced high-m shell is
20 = floor+4, so no member of P beats 4/7.* Nothing written to `constants/5b.md` or
`current.md`.

## What would push it further
1. **Larger / smarter pool.** P walls at m=26 partly because high-m (4,5)-sets need a wide
   coordinate span. Try a pool seeded from **affine images of A_base's 3-AP signature**
   (A_base has a degree-4 vertex / clustered midpoints — the cap-saturating structure) rather
   than Fibonacci/QR lattices, which are near-path. The cap m=28 likely needs that clustered,
   non-path arrangement, absent from the current lattice pool.
2. **MILP twin (`milp-coord-place-N30`).** Replace the heuristic Stage A with an exact
   indicator MILP maximizing m over P, run to a dual bound — turns the heuristic m-ceiling
   into a *certified* "no size-30 (4,5)-set in P has m > 26" theorem (the carried sibling).
3. **The α-vs-m gap is the real wall.** Even at m=26 the best α is 20 (this round) / 19 (R5).
   Closing to α=17 needs both m at the cap AND a transversal-efficient overlap pattern; the
   evidence (R5 + R8) is that within reachable pools these pull apart. A genuine beat may need
   a *constructed* family (recursive/CRT) rather than local search, or the upper-bound road may
   be structurally walled at N=30 — strengthening the case for the `lean-cap-lemma` machinery
   line and/or an f(30) ≥ 18 lower-bound proof.
