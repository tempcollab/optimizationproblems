# Approach: transversal-ilp-floor-search-N18

**Constant:** C_5b (Sidon density in (4,5)-sets, Erdős #757).
**Direction:** UPPER bound. Record to beat: `c* ≤ 4/7 ≈ 0.5714286` ([MT26], verified).
**This round's result: NO strict beat. Negative / obstruction result at N = 18** (documented,
reproducible). Best 18-point (4,5)-set found has `h = 11` (ratio `11/18 ≈ 0.6111`, which does
NOT beat 4/7).

## Goal of the approach

Find an 18-point (4,5)-set (weak Sidon set) `A ⊂ ℤ` with `h(A) = 10`
(`h` = largest Sidon subset = independence number `α` of the 3-AP hypergraph, by [MT26]
Lemma 2.3). That would give the strict beat `c* ≤ 10/18 = 5/9 ≈ 0.5556 < 4/7`.

Why 10 is the target (and the only target): from the **proven** lower bound `c* ≥ 9/17`,
every size-`N` (4,5)-set has `h(A) ≥ ⌈9N/17⌉`. At `N = 18`, `⌈162/17⌉ = 10`, so `α = 10` is
exactly the **floor** (the minimum possible). And `11/18 > 4/7`, so `h = 11` already fails —
**only `h = 10` (the floor itself) beats 4/7 at N = 18.** Hitting the floor is the whole game.

## What was done this round (search)

Four independent exact-`α` search methods (independence number computed EXACTLY by
deterministic branch-and-bound on the 3-AP hypergraph, never an edge-count heuristic — the
round-1 lesson):

1. **Exhaustive record-extension.** From the record `A_base` (N=14, α=8) extend by points,
   computing exact α at each step. Wide-beam (BW up to 40) reaches the values below.
2. **Exhaustive 18th-point test.** For the 3 best N=17 sets with α=10, tried EVERY integer
   18th point in `[0,1300]` keeping weak-Sidon — **none** kept α ≤ 10 (all give α ≥ 11).
3. **Stochastic beam** (765 restarts) and **simulated annealing** from random weak-Sidon
   starts (871 restarts, windows up to 1200): best α = 11 (beam) / 12 (SA from scratch).
4. **1-swap local polish** on the best α=11 set: confirmed α=11 is a **local minimum** — no
   single-point replacement over `[0,1300]` lowers α below 11.

### The "floor + 1" obstruction pattern (the headline finding)

Wide-beam exact-α extension of the record reaches the **floor only at N=14** and **floor + 1**
at every larger feasible N:

| N  | floor ⌈9N/17⌉ | min α found (record extension) | gap |
|----|---------------|--------------------------------|-----|
| 14 | 8             | 8  (the record itself)         | 0   |
| 15 | 8             | 9                              | +1  |
| 16 | 9             | 10                             | +1  |
| 17 | 9             | 10                             | +1  |
| 18 | 10            | **11**                         | +1  |

Adding any point to a floor-realizing set raised α above the next floor in every searched
extension. This is consistent with the math-explorer's independent finding that the floor is
unreachable at N=9 (min realized h=6 > floor 5). The record is "floor-optimal at N=14", and a
beat needs a floor-realizer at an N whose floor ratio < 4/7 — none was found at N=18.

### Best 18-point (4,5)-set found (verified, NOT a beat)

```
A = [0, 2, 9, 10, 18, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
```
- weak Sidon: YES (all 153 pairwise sums distinct — double-checked two ways: distinct sums
  AND ≥5 distinct differences per 4-subset).
- `h(A) = α = 11` (exact branch-and-bound).
- ratio `11/18 ≈ 0.6111 > 4/7` → does NOT beat.
- `α = 11` is a 1-swap local minimum over `[0,1300]`.

## Claim

**No improvement is claimed.** The held bound stays `4/7`. This round establishes a
**reproducible negative result**: in the searched region (record neighborhood + random + SA +
stochastic beam, exact α throughout) the minimum independence number at N=18 is **11**, not
the floor 10 a beat requires. The result is honestly scoped — it is NOT a proof that no
18-point (4,5)-set with h=10 exists globally (the integer window is unbounded and only a
finite region was searched), but it is strong multi-method evidence that the floor is not
realized at N=18 the way it is at N=14.

## Certificate (reproducible)

`constants/5b/certificate/search_cert_N18.py` — deterministic, integer-only, runs in ~1-2 min:
- (A) re-establishes the bar (A_base is a (4,5)-set, h=8, c* ≤ 4/7);
- (B) the floor arithmetic (only h=10 beats 4/7 at N=18; h=11 fails) with exact assertions;
- (C) the best found 18-point (4,5)-set, h=11 verified two ways, 1-swap-local-minimum check;
- (D) the floor+1 obstruction pattern via deterministic wide-beam extension.
All load-bearing facts are re-derived by `assert` inside the script. The heavy stochastic
searches (random/SA/beam) are SEARCH tools only; their best result (α=11) is re-checked
deterministically.

## Why no Lean certificate this round

The Lean engine (`lean/Constants/C5b.lean`) certifies a *beating gadget* by a one-line list
swap + re-`decide`. There is no beating gadget to certify (the best found, α=11, is worse than
the record). The engine remains ready for any future floor-realizer. No `constants/5b.md` or
`current.md` edit — nothing verified beats 4/7.

## What would push it further

- **Chase floor+1, not the floor — and the right N is N=30 (KEY actionable finding).** The
  searches reach `floor+1` at every feasible N from 15 to 18, never the floor. If `floor+1` is
  the true achievable minimum, the question becomes: *at which N does `floor+1` itself beat
  4/7?* Exact computation (in the certificate-adjacent check): `⌈9N/17⌉ + 1 < 4N/7` first holds
  at **N = 30** (`floor=16, floor+1=17`, ratio `17/30 ≈ 0.5667 < 4/7`), then again at N=32
  (18/32=0.5625), N=34 (19/34≈0.5588), N=37, N=39. **At all feasible N ≤ 29, floor+1 ties or
  exceeds 4/7** (e.g. N=18 floor+1=11 → 0.6111; N=28 floor+1=16 → exactly 4/7). So the
  small-N gadget search (N ≤ ~22, including this N=18 angle) is **structurally squeezed** — even
  the realistically-achievable α=floor+1 cannot beat 4/7 there. **The strategic pivot: target
  N = 30 (or 32) aiming for h = floor+1 = 17 (resp. 18).** This is the smallest N where the
  empirically-reachable value actually beats the record. A new approach slug
  (`floorplus1-search-N30`) is warranted next round; the same exact-α machinery applies (cost:
  N=30 weak-Sidon sets and C(30,18) subsets — well past raw `decide`, so the Lean
  transversal-certificate fallback would be needed).
- **Break out of the record neighborhood.** All searches that reached α=11 are near `A_base`.
  A *structurally different* floor-realizer (e.g. from the `modular-construction` CRT/digit
  idea, or a covering-design-first construction realized as integers) is the only untried
  route that could escape the floor+1 wall. High risk; the antagonism (weak-Sidon spreads
  points, small-α packs 3-APs) is real and is exactly what produces the +1.
- **A complete-search non-existence proof** at N=18 would need a bounded-window argument; the
  window for 18-pt weak-Sidon sets is large (≥ ~80; W=75 proven CP-SAT-infeasible) so a full
  complete DFS is out of reach with current compute. The current result is "strongly
  obstructed in the searched region", not "globally impossible".

## Status

**Negative result (no beat), documented and reproducible.** Min α at N=18 found = 11 (ratio
0.6111). Floor h=10 not realized. Held bound stays 4/7. Engine ready; no canonical edits made.
