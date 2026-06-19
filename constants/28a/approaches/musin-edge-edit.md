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
1. **`build_balanced_skeleton`** (scaffold, trivial/certifiable) — `m` disjoint `K_5`'s.
   Runs green; embedding dim of the disjoint-K5 skeleton verified `= n−1 = 319` (μ=0) by the
   exact rational Cayley–Menger rank machinery, ω=5 confirmed.
2. **`maximize_mu_over_edge_flips` (LOAD-BEARING, the one real hole)** — edit `C0` to reach
   embedding dim `≤ 62` (`μ ≥ n−63`) with `θ = m ≥ 64`, keeping the minimal clique partition
   fixed. Finite discrete optimization: a single-flip Δμ evaluator (recompute exact embedding
   dim at the critical `t` after each candidate flip) + greedy/SA hill-climb + a guard that
   each flip preserves `ω ≤ 5` (`g24.max_clique_le`) and the clique partition.
   **Open question:** does the edge-flip landscape on a balanced cap-5 skeleton EVER reach
   `μ = n−63`, or does it plateau below? Unknown — this is the genuine risk.
3. **`verify`** (Lean-fit core, written) — `ω(G) ≤ 5` (exact bitset), partition validity
   (`θ = m`), embedding dim `= n−μ−1 ≤ 62` (exact rational rank of the centered CM Gram),
   and the fire condition `θ+μ > n`.

## Hard step
`maximize_mu_over_edge_flips`. The mechanism is sound (Musin/Einhorn–Schoenberg), the
certification is clean and Lean-fit (exact rank + bitset ω), but whether the finite edge-flip
search actually lands `μ = n−63` is the open construction. The exact embedding-dim evaluator
is already implemented and verified on the μ=0 skeleton, so the builder can measure Δμ per
flip from day one.

## Certify
Lean-fit (preferred path once a winning graph lands): clique partition (finite) ⇒ θ-cap;
`ω ≤ 5` by bitset enumeration; embedding dim `= n−μ−1` is an exact integer/rational rank of
the Cayley–Menger matrix. Same finite/discrete/algebraic core as the cached `g24` scaffold.
The first construction to land bootstraps `constants/28a/lean/`.

## Borrows
The `g24.max_clique_le` exact-ω bitset routine (the shared Lean-fit certificate core) from
the cached scaffold / `fresh-orthogonal-dir`. Nothing else — the graph is built fresh.
