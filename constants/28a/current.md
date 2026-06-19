# 28a — Borsuk first-failing dimension (current)

## Status
none

## Bounds
table: 63 (upper bound, Gri2026 — record to beat) · held: 63 (no improvement; we have
verified no value below 63)

## Progress log
- R1: Verified two negative/scaffold results (no bound; record stays 63). (a) `g24.py`
  exact G_2(4) construction certified and reproduced independently: srg(416,100,36,20),
  standard Gram rank 65 over Q, ω=5, partition |B|=96 (3×32) |C|=320 — promoted to
  `lemmas/g24-construction.md`. (b) `fresh-orthogonal-dir`: hole 3 reshaped to exact
  eigenspace-intersection form; structured fresh-direction family refuted exactly — best
  dim-62 subset = 270 pts (exact rank 62, ω≤5, ceil=54<64); one honest open hole
  (`search_codim4_vector_general`). (c) `srg-sweep`: full Brouwer table (4538 rows) + 17
  big SRGs swept; eigenvalue-multiplicity formula matches table on all 4231 integer rows
  (0 mismatches); 0 rows certify a dim≤62 counterexample; 357 rows ruled out by sound
  conservative kills, 207 left honestly OPEN.
- R3: No bound change (record stays 63; held 63). Two verified advances, both honest
  negatives. (a) `mixed-construction`: hole `build_core` CLOSED — an exact 62-dim,
  270-point two-distance G_2(4) section of C, independently re-derived (rank 62 over Q,
  smaller-distance-graph ω=5 = α(diameter graph)=5; two-distance with norms²=90, inner
  products {-6,18}, diam²=192). Also fixed a real `verify()` correctness bug (it had
  checked ω of the diameter graph; the Borsuk part-cap is α(diameter graph)=ω(complement),
  re-derived as 0 mismatches against the smaller-distance graph). Load-bearing
  `engineer_perturbation` still OPEN (270<316; precise obstruction: the core fills its
  diameter ball). (b) `musin-edge-edit` (new): the μ-raising lever (rook K5□K_m, emb=s+m−2,
  ω=max(5,m)) exactly re-verified at integer root t=2, and a fast exact modular μ-evaluator
  built; but no ω≤5 edit fires (structured optimum rook K5□K5 has fire margin θ+μ−n=−4,
  independently confirmed). Edge-flip-on-balanced-skeleton strategy dead-ended.
- R4: No bound change (record stays 63; held 63). Two verified advances, both honest
  negatives on the chi_f crack. (a) `theta-cover-dual` (new): both load-bearing holes
  ADVANCED — 14 existence-confirmed named vertex-transitive families resolved EXACTLY in
  the NEGATIVE (none fires), converting OPEN srg-sweep rows from the loose Delsarte-Hoffman
  test to exact non-firing resolutions. 13 Steiner block-intersection rows S(2,3,n)/S(2,4,n)
  killed by closed-form clique LOWER bounds (pencil ω(A)≥(n−1)/(k−1) and partial-parallel-
  class ω(Ā)≥⌈(n−1)/(k(k−1))⌉, both > need_omega(v), re-derived and confirmed as true lower
  bounds); Cameron srg(231,30,9,3) built exactly (independently re-verified srg params +
  ω(A)=7 by Bron–Kerbosch), greedy α≥17 — both > need_omega(231)=3. Residual off-table
  discovery hole (`build_candidate_graph`: family-b Cayley + dense 2-graph rows
  v=220/276/344) stays OPEN. `theta_designs.py` scaffold (Bose/Golay/Witt/Cameron) certified
  & promoted to lemmas/. (b) `musin-edge-edit`: both R4 re-planned holes CLOSED — exact
  uniform fractional-clique-cover dual θ(G)≥n/ω(G) (re-derived θ(G)=χ(Ḡ)≥χ_f(Ḡ)=n/α(Ḡ)=
  n/ω(G), exact for vertex-transitive G; promoted as lemma `chi-f-uniform-transitive-dual`),
  and a bounded exact search over Johnson/triangular/Hamming/circulant families — CLEAN
  NEGATIVE, no ω≤5 candidate fires (best margin T(6) −3; embedding dims T(6)=5, H(2,4)=6,
  H(2,5)=8 independently re-derived over Q). chi_f buys nothing over ⌈n/ω⌉ here.
