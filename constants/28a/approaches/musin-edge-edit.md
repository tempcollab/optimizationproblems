# musin-edge-edit — edge-edit a balanced cap-5 clique skeleton to maximize μ

**Attack line A** (explorer round-2 §6). The headline NEW angle of round 2, opened
because the two paths round 1 spent its build budget on are now closed/refuted (SRG
table sweep; the G_2(4) 4th-orthogonal-vector / symmetry family), and the named Gri2026
codim wall blocks every "drop a dimension inside G_2(4)" line.

## Source
Musin 2025, arXiv:2511.03668 (`literature/musin2025.md`). For a two-distance set with
min-distance graph `G` on `n` vertices:

> `dim_E2(G) = n − μ(G) − 1`  (μ = multiplicity of the smallest root `t>1` of the
> Cayley–Menger polynomial `C_G(t)`), and `B(S) = θ(G)` (clique COVER number).
> ⇒ `G` is a Borsuk counterexample **iff `θ(G) + μ(G) > n`**.

Strictly more general than Bondarenko's SRG criterion `ceil(v/ω) > f+1`: any graph, θ
replaces `ceil(v/ω)` (θ ≥ ceil(v/ω), can be strictly larger), and the embedding dim is a
CM-root multiplicity.

## How it evades the standing obstructions
- **Gri codim wall (320 C-points span exactly 63 dims, no spare direction):** this sketch
  does NOT live inside `G_2(4)`. The graph is built from scratch by editing a disjoint-clique
  skeleton; its embedding dimension is `n−μ−1` by construction, never a projection of C. The
  wall simply does not apply.
- **SRG-table sweep (closed):** not a table lookup — the edge-flip search produces a
  non-table graph (no SRG parameter row is consulted).
- **The 4th-vector-in-G_2(4) family (refuted):** R1 sought ONE integer orthogonal vector (a
  rank-1 drop). μ is a multiplicity; inter-clique edge-flips raise it in BULK — a different
  lever entirely.

## Target in the θ/μ language (derived in the sketch header)
Cap-5 cliques ⇒ `θ(G) ≥ ceil(n/5)`. Want embedding dim `n−μ−1 ≤ 62`, i.e. `μ ≥ n−63`, and
`θ+μ > n`. With a balanced partition into `m` cliques of size ≤5 whose minimal clique
partition IS that partition (so `θ = m`, `ω ≤ 5`): fire iff **`m ≥ 64` (⇒ `n ≥ 316`) and
`μ = n−63` (embedding dim exactly 62)**. Same arithmetic target as run_state, recast.

## Strategy (Musin §3.2, Einhorn–Schoenberg)
- Fact (i): `μ(G)=0` iff `G` is a disjoint union of cliques (embedding dim `n−1`).
- Fact (ii): each edge added/removed BETWEEN cliques can raise μ.
- So: fix a **balanced skeleton `C0`** = `m` disjoint `K_5`'s (`m ≥ 64`, `n ≥ 316`), then
  **hill-climb / anneal on inter-clique edge-flips to maximize μ(G)**, keeping the minimal
  clique partition = `C0` (preserves `ω ≤ 5` AND `θ = m`). A winner reaches `μ ≥ n−63`.
- Author's heuristic (from Bondarenko): almost all cliques the same size — use balanced `C0`.

## Holes
1. **`build_balanced_skeleton`** (scaffold, CLOSED) — `m` disjoint `K_5`'s. Runs green;
   embedding dim of the disjoint-K5 skeleton verified `= n−1 = 319` (μ=0) by the exact rational
   Cayley–Menger rank machinery, ω=5 confirmed.
2. **`maximize_mu_over_edge_flips` (LOAD-BEARING) — PARTIALLY CLOSED (round 3), still OPEN.**
   The search step is now IMPLEMENTED and runs (was `raise NotImplementedError`): a bounded
   stochastic local edge-flip search with a hard `max_iter` cap, a `wall_budget_s` wall-clock
   budget, and stdout progress, using a new fast EXACT μ-evaluator (below). It returns the best
   cap-5 graph reached plus a `fired` flag. **It does NOT fire.** Honest residual: no cap-5
   (ω≤5) graph reaching embedding dim ≤62 (μ≥n−63) at n≥316 was found.
3. **`verify`** (Lean-fit core, intact) — `ω(G) ≤ 5` (exact bitset), partition validity
   (`θ = m`), embedding dim `= n−μ−1 ≤ 62` (exact rational rank of the centered CM Gram),
   and the fire condition `θ+μ > n`. Confirmed on rook K5□K5: n=25, ω≤5, exact emb 8,
   `is_counterexample=False` (5+16=21<25) — the core correctly does NOT false-fire.

## What round 3 closed / established
- **Fast EXACT μ-evaluator (`embedding_dim_fast`, NEW).** Integer modular Gaussian elimination
  over GF(p) (vectorised numpy), two-prime agreement check. ~70× faster than the slow
  exact-rational reference (`embedding_dim_two_distance`): ~0.5 s vs ~39 s at n=320.
  Cross-checked to AGREE exactly with the exact-rational machinery on the disjoint-K5 skeleton
  (emb 19) and the rook graph K5□K5 (emb 8) — a `_selftest_fast_evaluator()` guard runs every
  invocation. This turns the abstract "search" hole into a concrete, fast, EXACT instrument.
- **The μ-raising lever WORKS (proof of concept), exact at the integer root t=2.** The rook /
  Cartesian-product coupling K5□K_m drops embedding dim from n−1 to s+m−2, i.e. raises μ in
  bulk from 0 to (s−1)(m−1): at K5□K5, μ jumps 0→16. So Musin/Einhorn–Schoenberg fact (ii)
  (inter-clique edits raise μ) is confirmed concretely, not just cited.
- **Why it doesn't fire — the precise obstruction.** The rook coupling's "threads" (vertex x
  across all m cliques) form a clique of size m, so ω = max(5, m); cap-5 forces m≤5, topping
  out at **K5□K5: n=25, emb=8, μ=16, θ=5, fire margin θ+μ−n = −4**. A bounded local edge-flip
  hill-climb on a balanced cap-5 skeleton does strictly worse (n=20: μ reaches only 5 vs the
  rook's 12). Random/circulant Cayley edits with ω≤5 almost all give μ=0. The triangular graph
  T(6)=J(6,2) (n=15, ω=5) gives emb 5, μ 9, margin −3 — best ratio seen, but it is an SRG
  already covered by the (closed) srg-sweep. **Pattern: every ω≤5 edit that meaningfully raises
  μ is either a swept SRG or has its embedding dim grow as fast as n.** This is exactly why
  G2(4) (an exceptional SRG) is special and why the closed SRG line is so constraining.

## Best embedding dim reached (this round, CONJECTURE — not a bound)
The lowest embedding dim found under the ω≤5 + θ+μ>n constraints **does not beat 63**: the
best firing-feasible structured object is K5□K5 with fire margin −4 (no fire). No counterexample
in dim ≤62 was produced. **Claimed (upper) bound: still 63** — i.e. this round produced NO
improvement, an honest negative-leaning partial result. Nothing is written into `current.md`.

## Hard step (remaining)
`maximize_mu_over_edge_flips` reaching the fire condition `θ+μ>n` at ω≤5, n≥316. The mechanism
and the exact certification are sound and Lean-fit; the evaluator is fast and verified. The
genuine open construction is **a new ω≤5 graph outside the swept SRG table** whose embedding
dim grows slower than n — blind editing of a balanced skeleton provably (this round's evidence)
does not reach it. This is now an outliner-level re-plan question (what ω≤5 family?), not a
fill-the-blank for the builder.

## Certify
Lean-fit (preferred path once a winning graph lands): clique partition (finite) ⇒ θ-cap;
`ω ≤ 5` by bitset enumeration; embedding dim `= n−μ−1` is an exact integer/rational rank of
the Cayley–Menger matrix. Same finite/discrete/algebraic core as the cached `g24` scaffold.
The first construction to land bootstraps `constants/28a/lean/`.

## Borrows
The `g24.max_clique_le` exact-ω bitset routine (the shared Lean-fit certificate core) from
the cached scaffold / `fresh-orthogonal-dir`. Nothing else — the graph is built fresh.
