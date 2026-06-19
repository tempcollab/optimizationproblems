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

## Round 4 — the chi_f re-plan: BOTH holes CLOSED, CLEAN NEGATIVE

The R4 re-plan moved the load-bearing step off blind edge-flips onto the sharper
`chi_f(G_d)` part-count, searching mu-rich vertex-transitive association-scheme / Cayley
graphs. This round **closed both re-planned holes with computed, exact content** and the
result is a clean, reproducible negative.

### Correct firing condition (re-derived, single convention)
Musin: G = the **smaller-distance** graph; a Borsuk part of smaller diameter is a **clique
of G**, so parts = clique-cover θ(G) and the part-cap is **ω(G) ≤ 5** (= α(diameter graph)).
For a vertex-transitive G the fractional clique-cover is exact: **chi_f(G) = n/ω(G)**. Borsuk
fire iff θ(G)+μ > n; sufficient (and exact for transitive G): `chi_f(G) + μ > n`, i.e.
**`n/ω(G) > emb+1`** where emb = n−μ−1. (Note: an earlier sweep using α(A) of the *diameter*
graph as the cap produced spurious "margin 0" tight cases — that mislabels the Musin
clique-COVER convention; corrected here. The cap is ω of the min-distance graph.)

### Hole 1 — `fractional_part_lower_bound_dual` — CLOSED (exact, Lean-fit)
The exact uniform fractional-clique-cover dual for vertex-transitive G: `w_v = 1/ω(G)`,
giving the certified bound `chi_f(G) = n/ω(G)`. Dual feasibility is immediate and exact —
every clique S of G has |S| ≤ ω(G), so `Σ_{v∈S} w_v = |S|/ω ≤ 1`. No LP solver, no floating
point; ω(G) is the exact bitset clique number (`g24.max_clique_le`). This is the sharpest a
uniform transitive dual gives, and for vertex-transitive G it is the exact chi_f (the
symmetry-averaged LP optimum). Self-tested on T(6): chi_f = 15/5 = 3, w = 1/5, feasible.

### Hole 2 — `search_assoc_scheme_family` — CLOSED as a bounded exact search → NEGATIVE
A bounded, fully-exact search over the mu-rich vertex-transitive families the re-plan named:
Johnson J(k,2)=T(k) and J(k,3); Hamming H(d,q); circulant Cayley Cay(Z_n,S) (n<37,
divisor-coset + random symmetric connection sets, with a sound cheap pre-screen
`emb+1 < n/2` since ω≥2). Each candidate: exact ω (bitset b&b), exact embedding dim (fast
modular evaluator + 2-prime agreement), exact rational chi_f = n/ω.

**RESULT: no candidate fires.** Every ω(G)≤5 candidate has `chi_f = n/ω(G) ≤ emb+1`, i.e.
firing margin `chi_f+μ−n < 0`:

| candidate | n | ω(G) | emb | chi_f=n/ω | margin chi_f+μ−n |
|-----------|---|------|-----|-----------|------------------|
| T(6) (best) | 15 | 5 | 5 | 3.0 | **−3** |
| H(2,4) | 16 | 4 | 6 | 4.0 | −3 |
| H(2,5) | 25 | 5 | 8 | 5.0 | −4 |
| J(6,3) | 20 | 4 | 14 | 5.0 | −10 |
| J(7,3) | 35 | 5 | 20 | 7.0 | −14 |
| H(3,4) | 64 | 4 | 36 | 16.0 | −21 |
| circulants n<37 | — | ≤5 | — | — | none fire |

The sharper fractional dual buys **nothing** over Bondarenko's `ceil(n/ω)` for these families:
a graph that is mu-rich (low emb) with ω(G)≤5 has `n/ω` *far below* emb+1, not marginally
below. T(6) is the closest at margin −3, and the gap widens for every larger or denser member.

### Why (the structural obstruction, honest)
Low embedding dim = high algebraic structure (large eigenvalue multiplicities), which in these
two-distance schemes forces ω(G) up *or* keeps n/ω small relative to the dimension. The named
mu-rich transitive families sit on or below the Borsuk-tight line `n/ω = emb+1`; they never
cross it with ω≤5. This is the complementary face of the same `ceil(n/ω) > emb+1` wall that
all G_2(4)-derived sketches hit at 316 points — chi_f sharpens the *rounding*, but the
underlying ratio `n/ω ≤ emb+1` is what actually binds, and it binds here.

## Claimed bound (this round)
**No improvement. Claimed upper bound: still 63** (a claim, and in fact a clean negative — the
chi_f crack does not open for the mu-rich vertex-transitive scheme/Cayley family). Nothing is
written into `current.md`. The script runs green in ~6 s, exit 0, both holes computed (no
`NotImplementedError`), and reproduces the negative.

## Remaining open question (OUTLINER-level, not a builder fill-the-blank)
Is there ANY two-distance family with ω(G)≤5 escaping `n/ω ≤ emb+1`? The searched
vertex-transitive scheme/Cayley graphs provably do not (this round). What is NOT covered: (i)
**non-vertex-transitive** graphs, where chi_f can exceed n/ω (the uniform dual is no longer
optimal) — but then the dual must be hand-built per graph and the family is unstructured; (ii)
**non-table, non-scheme** ω≤5 SRG-like graphs (the srg-sweep's 207 open rows). Both are
outliner-level re-plans; the cheap, structured probe this sketch owned is now a verified clean
negative — it should be retired or pointed at (i)/(ii) explicitly.

## Promotable lemmas
**`chi_f_uniform_transitive_dual`** (proved green this round, reusable, also the exact lever
theta-cover-dual needs). Statement: for a vertex-transitive graph G on n vertices with clique
number ω(G), the constant weight `w_v = 1/ω(G)` is a feasible fractional-clique-cover dual
(every clique S satisfies `Σ_{v∈S} w_v = |S|/ω(G) ≤ 1`), so the clique-cover number satisfies
`θ(G) ≥ chi_f(G) = n/ω(G)`, and for vertex-transitive G this is exact. Proved in
`certificate/musin-edge-edit.py::fractional_part_lower_bound_dual` (+ `exact_omega`), with the
feasibility/exactness self-tested on T(6) in `_selftest_fast_evaluator`. The feasibility half
(`θ(G) ≥ n/ω(G)` from the constant dual) is fully elementary and Lean-fit (finite rational
inequalities + an exact bitset ω); the "exact for vertex-transitive" half cites the standard
fractional-chromatic-number identity (Frankl; Scheinerman–Ullman, *Fractional Graph Theory*,
Prop. 3.1.1 — for vertex-transitive H, χ_f(H) = |V(H)|/α(H)). Reviewer: certify the feasibility
lower bound at minimum; the exactness is a literature citation, not re-derived here.

## (superseded) Round-3 edge-flip baseline
The lowest embedding dim found under ω≤5 + θ+μ>n via blind edge-flips did not beat 63: the
best firing-feasible structured object is K5□K5 with fire margin −4 (no fire). Kept as the
refuted baseline in the sketch (`maximize_mu_over_edge_flips`). The R4 re-plan above is the
live load-bearing line, now also closed as a clean negative.

## Certify
Lean-fit (preferred path once a winning graph lands): clique partition (finite) ⇒ θ-cap;
`ω ≤ 5` by bitset enumeration; embedding dim `= n−μ−1` is an exact integer/rational rank of
the Cayley–Menger matrix. Same finite/discrete/algebraic core as the cached `g24` scaffold.
The first construction to land bootstraps `constants/28a/lean/`.

## Borrows
The `g24.max_clique_le` exact-ω bitset routine (the shared Lean-fit certificate core) from
the cached scaffold / `fresh-orthogonal-dir`. Nothing else — the graph is built fresh.
