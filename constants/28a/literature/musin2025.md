# Musin 2025 — Borsuk's conjecture for two-distance sets, equivalent graph formulation (arXiv:2511.03668, Nov 2025)

PDF/txt saved under `pdfs/2511.03668.{pdf,txt}`. **The most general reformulation in the
literature** and the freshest (Nov 2025). Companion long paper [8] (Musin, not yet on arXiv
at digest time) has full proofs/examples. This is the key new angle for round 2: it replaces
the SRG-only lens with an ANY-graph lens, and gives a concrete generative search strategy.

## The reformulation (Theorem 1) — generalizes the whole SRG line

For a two-distance set `S = {p_i}` with distances `1` and `b>1`, form the graph `G` with an
edge `ij` iff `dist(p_i,p_j)=1` (min distance). Let `C_G(t)` be the Cayley–Menger polynomial
in `t=b^2`, and `μ(G)` = multiplicity of the smallest root `t>1` of `C_G(t)=0`. Then
(Einhorn–Schoenberg):

> **dim_E2(G) = n − μ(G) − 1**   (smallest two-distance embedding dimension of G)
> and  **B(S) = θ(G)**   (Borsuk number of S = clique cover number of G).

So **G is a Borsuk counterexample iff  θ(G) + μ(G) > n.**  (n = #vertices.)

This is strictly more general than Bondarenko's SRG criterion `ceil(v/ω) > f+1`:
- It applies to ANY graph, not just SRGs. The embedding dimension is `n−μ−1` (μ = an
  eigenvalue/CM-root multiplicity), recovering `f` only for the SRG normalization.
- θ(G) (clique cover number) replaces `ceil(v/ω)`; θ ≥ ceil(v/ω) always, and can be larger,
  so the criterion `θ+μ>n` can fire where `ceil(v/ω)>f+1` is too weak.
- Spherical version is Theorem 2 (same formula, needs R(G)<∞ / well-defined HL).

Sanity vs the known chain (paper §3.1): Bondarenko S1 (416 pts, R^65, B≥84), Jenrich S3
(352 pts, R^64, B≥71). Cardinalities are FAR below the max `c2(d)=d(d+1)/2` (e.g.
416 << c2(65)=2145, 352 << c2(64)=2080) — i.e. there is huge cardinality headroom; the
known counterexamples are sparse, suggesting denser graphs at fixed dim may exist.

## §3.2 — the generative search strategy (the new actionable angle)

Facts (Einhorn–Schoenberg, [8]):
- (i) `dim_E2(G)=n−1` (μ=0) **iff G is a disjoint union of cliques**. Each added/removed edge
  between cliques can raise μ.
- (ii) if `dim_E2(G) ≤ n−2` the two-distance rep is unique up to isometry (rigidity).

Strategy: **fix a clique-partition skeleton `C0`** (m cliques `c_1..c_m`, so θ=m once
`Clq(G)=C0` is preserved), then **add/remove edges BETWEEN the cliques to MAXIMIZE μ(G)**
while keeping the minimal clique partition equal to C0. Whenever `m + μ(G) > n`, G is a
counterexample in dim `n−μ−1`. Author's heuristic from Bondarenko: **almost all cliques have
the SAME size** — use a balanced C0. This is discrete optimization (hill-climb / ML over
edge-flips) on a fixed clique skeleton — exactly the "edit a structured graph" move, not a
table lookup.

For dim ≤ 62 the target becomes: find a graph G on n vertices with a balanced clique
partition into m cliques (cap ≤ 5 per clique gives θ ≥ ceil(n/5)) and `μ(G) = n−1−d` for some
`d ≤ 62`, with `m + μ > n`, i.e. `m > d+1 = 63`, i.e. θ(G) ≥ 64 while embedding in ≤62 dims.
Concretely (cap-5 cliques): need n ≥ 316 vertices, clique-partition into ≥64 cliques of ≤5,
and μ(G) ≥ n−63. This recasts the SAME arithmetic target (run_state) in the θ/μ language but
opens edge-editing of a clique skeleton as a fresh construction method distinct from
(a) SRG-table sweep [closed], (b) 4th-orthogonal-vector-in-G2(4) [structured family refuted].

## §3.3 — s-distance generalization (feeds mixed-construction)

Extends to `s`-distance sets: color `E(K_n)` with s colors `G_1..G_s` (distances
`1=a_1>a_2>...>a_s`). Then `L` is a Borsuk counterexample only if `θ(Ḡ_1) > dim_E2(L)+1`.
Polynomial `C_L(t_2,...,t_s)`, matrix `A_L`, `dim_E2(L)=rank` minimization over the `t_i`.
**This is the rigorous backing for the `mixed-construction` (line D) sketch**: Gri's record
set is already 3-distance, and Musin says the SAME θ-vs-dim criterion governs s-distance sets
— so a 3-distance graph with a small clique-cover-1 color and a low-rank realization is a
legitimate route. Open: an efficient algorithm to pick the `t_i` minimizing rank.

## What it does NOT give
- **No new explicit graph/SRG** for dim < 64 (confirmed: §2 strategy is programmatic, not a
  named construction). No G2(4) sub-configuration/descendant/local-graph trick.
- **No new clique-cover lower-bound certification technique** — θ(G) lower bounds still come
  from `ceil(n/ω)` or explicit cover arguments.
- Reconfirms the open gap "dimensions 4 to 63"; notes d=4 fully enumerated (Szöllősi,
  arXiv:1806.07861, no counterexample) and Radchenko found none for d≤7 — so the **lower side
  is freshly confirmed hard at the bottom**, reinforcing UPPER-only targeting.

## Lean-fit of this angle
A counterexample produced by §3.2 certifies via: (1) the clique partition (finite), giving
θ ≤ m and a cap on smaller-diameter parts; (2) `μ(G)` = multiplicity of an integer/rational
CM-polynomial root ⇒ embedding dim `n−μ−1` is an exact rank/eigenvalue-multiplicity fact;
(3) θ(G) ≥ 64 needs a clique-cover LOWER bound (the harder discrete step — for cap-5 cliques
it's `ceil(n/ω)` again, so ω(G)≤5 by exact bitset search). All finite/discrete/algebraic ⇒
Lean-fit, same core as the existing g24 scaffold. The NEW load-bearing search step (maximize
μ over edge-flips on a fixed C0) is itself a finite search; certification of a winner is
clean.
