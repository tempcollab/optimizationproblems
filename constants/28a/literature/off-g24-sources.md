# Off-G_2(4) Borsuk counterexample sources — survey (round 4 math-explorer)

The run's central R4 question: is there a genuinely NEW off-G_2(4) source of a dense,
low-clique-number point set in <=62 dims? This digest records the survey so future rounds
do not re-walk it. **Verdict: no verified sub-64 construction off G_2(4) exists in the
literature; every off-G_2(4) candidate fails the *rigorous partition lower bound* test,
which is exactly the lever G_2(4) supplies (omega=5 => ceil(n/5) clique-cover bound).**

## 1. Leech lattice / laminated sublattices — Jenrich, arXiv:2305.06283 ("Sub-25-dim...?")
- **Construction (genuinely off-G_2(4)):** M_n = minimal-norm vectors of the laminated
  lattice Lambda_n (sublattices of the Leech lattice Lambda_24). Diameter graph: inner
  product > -16 (i.e. the two closest-to-antipodal shells). Point counts are HUGE and dense:
  n=14: 1422 pts, ... n=22: 49896, n=23: 93150, n=24: 196560.
- **Claimed parts (TABUCOL heuristic, NOT proven):** n=22 -> 25 parts (=n+1, no failure),
  n=23 -> 29 (>24, would be a counterexample IF proven), n=24 -> 34 (>25, the headline
  "potential" counterexample). n<=21 all colour into n+1, so NO claim there.
- **VERIFICATION STATUS: entirely heuristic.** Author's own words: "a potential but
  currently unverified counterexample." There is **no rigorous lower bound** on the number
  of parts — no clique-number, fractional-chromatic, or Lovász-theta certificate. The bound
  is "TABUCOL could not find a smaller colouring," which is not a proof.
- **WHY it is NOT Lean-fit / NOT adaptable to our lever:** the G_2(4) line works because the
  diameter graph has **clique number omega = 5** (small), so the cheap, finite, certifiable
  bound ceil(|X|/omega) already exceeds n+1. The Leech diameter graphs have **large clique
  number** (the dense minimal-vector shells contain big mutually-diameter cliques), so
  ceil(|X|/omega) is FAR below n+1 — the partition lower bound must come from a genuine
  chromatic-number argument, which is the open, Lean-hostile, computationally-infeasible
  step (graph colouring optimality on 10^5-vertex graphs). This is the precise reason the
  Leech family cannot be turned into a verified sub-64 bound by the same machinery.
- **Bottom line for us:** off-G_2(4), dense, low-dim — but the partition lower bound is the
  wrong shape (no small clique number). Not a usable construction. Do not open a sketch on it
  unless someone has a *rigorous* chromatic lower-bound technique for these graphs (none in
  the literature; this is itself a hard open problem).

## 2. Boolean-cube Borsuk numbers — arXiv:2504.01233 (Apr 2025), chi(Q_10)=6
- Verified computational result: max chromatic number of a diameter graph on subsets of the
  10-dim Boolean cube is 6 << 11 = n+1. **CONSISTENT with Borsuk, not a counterexample.**
  Confirms the cube route gives no low-dim counterexample (cube diameter graphs are too
  colourable). Not relevant to the 62-63 frontier.

## 3. Musin arXiv:2511.03668 (re-read R4) — no new explicit graph
- Re-confirmed: gives NO explicit graph/family for dim < 64. Only the §3.2 generative
  edge-flip strategy (already the basis of musin-edge-edit, RETHINK) and §3.3 s-distance
  (backs mixed-construction). Does NOT name any non-G_2(4)/non-Fi_23 family. Does not discuss
  theta(G) > ceil(v/omega) as an exploitable gap. d=4 checked (no counterexample), d<=7 none
  (Radchenko) — reconfirms LOWER side hard at the bottom.
- **The one un-mined idea in Musin worth flagging:** theta(G) (clique COVER number) can
  STRICTLY exceed ceil(v/omega). The whole G_2(4) line uses the weak bound theta >=
  ceil(v/omega). A graph in <=62 embedding dim where theta is provably large by a *clique-
  cover* argument STRONGER than ceil(v/omega) (e.g. a fractional/LP clique-cover lower bound
  certifiable by an explicit dual) could fire at smaller n than the ceil(n/5)>=64 => n>=316
  target demands. No such graph is known, but the criterion theta+mu>n is the only place a
  *sub-316-point* counterexample could hide. This is a genuinely new angle nobody in the run
  has tried (all sketches assume theta = ceil(n/5)).

## 4. Other families checked in prior rounds (R2 digest, reconfirmed >=64)
- arXiv:2005.12025 (More SRG counterexamples): Fi_23 descendants -> dim 240; 2401-vtx graph
  -> dim 240. All >= 64.
- arXiv:1409.3520 (New SRGs from G_2(4)): induced-subgraph dim-drop only loses points. >=64.
- Reuleaux-polyhedra / Borsuk-Vazsonyi (ScienceDirect 2025): dimension 3 constant-width
  bodies. Irrelevant to the 62-63 frontier.

## Synthesis
Two distinct construction *worlds* exist: (A) the **small-omega world** (G_2(4), Fi_23,
SRG two-distance sets) where the partition lower bound is cheap (ceil(v/omega)) and
Lean-fit, but the smallest known dim is 63 and every sub-config tops at 270<316 pts; and
(B) the **large-omega / dense-lattice world** (Leech, cube) where dense low-dim point sets
exist but the partition lower bound is a hard chromatic argument nobody can certify. The
63->62 improvement needs EITHER a new small-omega object in world A (the run's whole effort
so far — walled at 270) OR a *rigorous* partition lower-bound technique that works in world
B (a research-level open problem, Lean-hostile). The only crack between them is Musin's
theta > ceil(v/omega) gap (§3 above), unexplored by the run.

## 5. Round-5 extension — 2024/2025 two-distance & clique-cover literature (all negative)

Searched the 2024-2026 literature for (a) any new sub-63 / non-transitive construction,
(b) two-distance set cardinality bounds, (c) clique-cover / Lovász-theta chromatic lower
bounds. **Nothing yields a new bound. No sub-63 construction has appeared.**

- **arXiv:2509.00858 (Sep 2024), "Bounds on two-distance sets in Euclidean space and Unit
  Sphere":** UPPER bounds on cardinality only (Seidel-matrix spectral method), no new dense
  construction, does not mention Borsuk or diameter-graph clique/chromatic numbers. An upper
  bound on |X| works AGAINST a counterexample; useless for firing. Not digest-worthy beyond
  this line.
- **arXiv:2211.02331 (coherent configurations type (2,2;3) two-distance embedding):** a
  UNIQUENESS result — Lisonek's 45-pt set in R^8 is the *only* such embedding. Negative
  (rules examples out), no new high-dim object. Irrelevant to 62-63.
- **arXiv:2301.13076 "Extremal spherical polytopes and Borsuk's conjecture": WITHDRAWN**
  (author content-disagreement). Disregard.
- **Dense two-graph rows (theta-cover-dual residual hole) — now QUANTIFIED as DEAD.** The 3
  rows are v=220/276/344 with need_omega = 3/4/5 respectively (firing needs alpha(diameter
  graph) <= need_omega). The v=276 row is srg(276,140,58,84) (the unique regular two-graph
  on 276 vertices, Conway-Goethals-Seidel / .3 group), degree k=140 ~ v/2, eigenvalues
  {140, 2, -28}. Hoffman ratio bound gives alpha <= 46 — and the TRUE alpha of such a dense
  graph is far above 4. Firing needs alpha <= 4. The ratio v/alpha is ~33 at best, nowhere
  near 64. Both the graph and its complement are dense (k ~ v/2), so both clique numbers are
  large: neither orientation can fire. The residual hole's own prediction ("both omega
  expected LARGE") is correct and now numerically pinned. **These rows cannot fire; computing
  exact clique numbers would only confirm a negative already forced by the Hoffman bound.**
- **Lovász-theta sandwich — the concrete shape of the reviewer's "non-vertex-transitive"
  hint.** theta-bar(G) (theta of the complement) satisfies omega(G) <= theta-bar(G) <= chi(G)
  for EVERY graph, transitive or not. So a Lovász-theta lower bound on chi(G_d) is a valid
  firing certificate WITHOUT needing vertex-transitivity (the chi_f = v/alpha pin that walls
  theta-cover-dual). BUT: (i) theta-bar is an SDP value, Lean-HOSTILE (continuum, not a
  finite rational dual) unless it lands on an exact algebraic number with a rational
  dual-certificate; (ii) for a vertex-transitive graph theta-bar = v/alpha exactly (Lovász),
  so it gives NOTHING new over the existing pin there — its only added power is on
  NON-transitive graphs; (iii) it still requires a graph whose theta-bar exceeds d+1 at
  <= 62 emb-dim, i.e. the same density wall. No such graph is in the literature. Records the
  lever precisely so a future round need not re-derive it: the non-transitive route exists in
  principle (theta-bar), but it is Lean-hostile and has no candidate object.
