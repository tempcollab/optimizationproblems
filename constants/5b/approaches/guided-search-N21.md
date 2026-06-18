# guided-search-N21 — Optimization-guided search for a (4,5)-set beating 4/7

**Angle:** upper bound. Find a finite (4,5)-set A with h(A)/|A| < 4/7 ≈ 0.5714286; by
[MT26] Thm 1.5 (c* = inf_n f(n)/n) one such gadget proves c* ≤ h(A)/|A|.

**Bar to beat:** verified 4/7 (record 14-point gadget, h=8). No asterisk.

## Round 1 outcome — NO strict beat found (documented near-miss)

Best ratio achieved by search across all methods: **4/7** (ties the record at N=7 with
h=4 and N=14 with h=8; otherwise searches plateau at ratios ≈ 0.60–0.67). **Claim
(CONJECTURE-level, unverified beyond the bar):** I did not find any (4,5)-set beating 4/7.
The held bound stays 4/7. What I *did* establish rigorously this round is a feasibility
map that sharply narrows where a beat can live and rules out the originally-targeted N.

### The decisive finding: the 9/17 lower bound rules out N=14 and N=21

Combining the **proven** lower bound c* ≥ 9/17 [MT26, via Henning–Yeo] with the gadget
framework: every (4,5)-set of size N has h(A) ≥ (9/17)N, so h(A) ≥ ⌈9N/17⌉. A gadget of
size N can beat 4/7 **only if** ⌈9N/17⌉ / N < 4/7, i.e. 7·⌈9N/17⌉ < 4N. Consequences
(all exact integer arithmetic, in the certificate part B):

- **N = 14:** ⌈126/17⌉ = 8, and 8/14 = 4/7 exactly → the record is *optimal at N=14*; no
  14-point gadget can beat 4/7.
- **N = 21:** ⌈189/17⌉ = 12, and 12/21 = 4/7 exactly → **the slug's own target h=11 is
  below the proven floor and therefore impossible.** N=21 cannot beat 4/7 at all.
- Smallest N that *can* beat 4/7: **9, 11, 13, 15, 16, 17, 18, 20, 22, 23, …**
  (e.g. N=15 needs h≤8 → 8/15≈0.533; N=13 needs h≤7 → 7/13≈0.538; N=28 needs h≤15).

This is a genuine correction to the outline (which suggested 11/21 and N=14-style targets):
those exact targets are arithmetically dead given the verified lower bound.

### Exact obstruction at the smallest feasible N

Complete (window-limited, anchored-at-0) exact search shows the floor is *not* reached at
the smallest feasible N inside the searched windows:

- **N=9, target h≤5** (floor): COMPLETE search over [0,45] and [0,50] → **no** weak-Sidon
  set with h ≤ 5; min h is 6 (= 2/3, worse than 4/7).
- **N=11, target h≤6** (floor): COMPLETE search over [0,40] → **no** weak-Sidon set with
  h ≤ 6.

So the 9/17 floor is *not tight* at small feasible N in compact windows — the gap between
the floor and what is realizable is exactly the room a beat would need, and it isn't there
for small N. (Wider windows for N≥13 are not exhaustible in the round budget; see below.)

## Search methods tried (all use EXACT integer h via branch-and-bound)

1. **Random weak-Sidon + simulated annealing** (h-aware moves, remove-from-independent-set
   + AP-completing replacement): plateaus at h/N ≈ 0.667 (N=21). Random weak-Sidon sets
   are too "spread out" to pack 3-APs; local moves can't dig to the optimum.
2. **AP-seeded greedy + anneal hybrid:** ≈ 0.64. Slow (greedy restarts dominate), no beat.
3. **Beam search maximizing 3-AP edge count, exact-α tie-break:** reaches the Lemma-2.4
   saturation m = n−2 edges (e.g. 12 edges at N=14, 13 at N=15) but α stays high
   (N=14→9, N=13→8, N=15→9). **Lesson: maximizing edge *count* is necessary but not
   sufficient — the AP *overlap pattern* (a covering design) controls α, and greedy
   edge-packing builds a long "chain" with a large independent set, not a covering.**
4. **CP-SAT, maximize completed 3-APs s.t. weak-Sidon:** the O(L²) pairwise-sum conflict
   constraints make even L=400 infeasible to solve in time; abandoned.
5. **Complete window-limited DFS with a sound prune** (greedy maximal no-3-AP set is a
   lower bound on h; h is non-decreasing under point addition → prune branches whose
   partial h already exceeds the target): the only method that *proves* non-existence; it
   resolves N≤11 in compact windows but the tree explodes for N≥13.

## Why beating 4/7 is genuinely hard (structural obstruction)

The two requirements pull apart: **weak-Sidon (all pairwise sums distinct) forces points
apart**, while **small h needs many overlapping 3-APs, which want points close/compact**.
The record's 14-point set is an AI-found needle that hits the 9/17 floor exactly at N=14.
Reaching the floor at a *feasible* N (where floor/N < 4/7) is the whole game and my
searches consistently miss it by the ≈0.03–0.10 margin that separates the floor from the
realizable minimum.

## How to push further (next round)

- **Target the right N.** Only N ∈ {13,15,16,17,18,20,22,…} can beat. Best margins:
  N=15 (h≤8, 0.533), N=17 (h≤9, 0.529), N=28 (h≤15, 0.536), N=34 (h≤18, 0.529).
- **Better search engine.** The plateau is a *local-search* failure, not a feasibility
  proof. Worth trying: (a) a proper **CEGAR/transversal** ILP using α = N − τ(min
  transversal) — maximize the minimum transversal directly; (b) a **constraint model that
  fixes a target covering design** (a 3-AP hypergraph with small α first, then realize it
  as integers with distinct pairwise sums — "design-first, embed-second"); (c) seed local
  search from *structured* AP-trees (caterpillars of overlapping APs) rather than random.
- **Sharpen the lower bound instead.** The fact that the record sits exactly on the 9/17
  floor at N=14 suggests the *upper* bound may already be near-optimal; the modular-
  construction / lower-bound angles may be more fruitful than more gadget search.
- **Feed the Lean scaffold (slug lean-scaffold-and-warmup).** Any beating gadget found
  later drops straight into the two decidable predicates (is45set, hLe). For N≤16 raw
  `decide`/`native_decide` is plausible; for larger N use the explicit witness + 3-AP
  transversal certificate. The certificate's exact `is_45set` / `max_no_3ap` /
  `three_ap_edges` are the reference semantics for the Lean definitions.

## Certificate

`constants/5b/certificate/search_cert_N14.py` — self-contained (stdlib only),
deterministic, exact integer arithmetic. Reproduces: (A) record is a (4,5)-set with h=8
(two independent (4,5)-checks agree; explicit size-8 Sidon witness), (B) the feasibility
map ruling out N=14/21, (C) the complete small-N obstruction. Run:
`python constants/5b/certificate/search_cert_N14.py` (< 1 min).
