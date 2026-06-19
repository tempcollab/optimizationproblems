# Reproducible checks — constant 28a

Per-sketch run/verify commands (Python sketches; the directed check is the script itself
running green and reproducing its reported result).

## srg-sweep (finite SRG-parameter database search; negative result)
```
python3 constants/28a/certificate/srg-sweep.py
```
- Self-contained: reads cached Brouwer feasible-parameter HTML from
  `constants/28a/certificate/srgtab_html/` (26 files, v<=1300, 4538 rows) + embedded
  `LARGE_SRGS` (17 big named SRGs) — no network needed.
- Expected (exit 0): G_2(4) sanity `f=65, certifies=False`; **0** rows certify a
  counterexample in dim<=62; of 564 rows with `f<=62`, **357 ruled out**, **207 open**.
  Verdict line: `NEGATIVE (certifiable): no feasible SRG parameter set ... yields a
  Delsarte-Hoffman-certifiable Borsuk counterexample in dimension <= 62.`
- Internal cross-checks asserted at runtime: eigenvalue-multiplicity formula matches the
  table's own `r^f` column on all 4231 integer rows (0 mismatches); G_2(4) embedding
  dim = 65.
- This is a NEGATIVE search result, NOT a bound. Nothing is written to `held`.

## g24 (shared scaffold; exact G_2(4) construction + partition)
```
python3 constants/28a/certificate/g24.py
```
- Builds G_2(4) from Brouwer's PG(2,16) Hermitian model (exact GF(16) arithmetic +
  integer bitsets; deterministic vertex order). Asserts at runtime, exit 0:
  srg(416,100,36,20), adjacency eigenvalues 100/20/-4 (mult 1/65/350), Gram
  `96I+24A-6J` rank 65, omega=5 (5-clique exists, no 6-clique), standard partition
  |B|=96 (3 components of 32) |C|=320. Prints `... PASS`.
- This is trusted scaffold (mirrors Gri2026's already-verified facts); a `lemmas/`
  candidate (build_g24 + standard_partition + b_components).

## musin-edge-edit (Musin θ/μ line, R4 chi_f re-plan; CLEAN NEGATIVE — does NOT fire)
```
python3 constants/28a/certificate/musin-edge-edit.py
```
- Imports cached `g24.max_clique_le` (exact ω bitset). Runs ~6 s, exit 0.
- Expected: `[selftest] fast evaluator == exact-rational ... ; chi_f dual exact &
  feasible on T(6): OK` (the fast modular μ-evaluator `embedding_dim_fast` agrees with
  the slow exact-rational `embedding_dim_two_distance` on the disjoint-K5 skeleton
  emb 19 and rook K5□K5 emb 8, both at integer root t=2; AND the new uniform chi_f
  dual gives chi_f(T(6)) = 15/5 = 3 exactly with dual feasibility |S|/ω ≤ 1). Then the
  μ-raising lever table (rook K5□K_m, refuted baseline) and the R4 chi_f family search.
- **R4 LOAD-BEARING holes CLOSED (both):**
  - `fractional_part_lower_bound_dual` — CLOSED. Exact uniform fractional-clique-cover
    dual for vertex-transitive G: `w_v = 1/ω(G)`, certified bound `chi_f(G) = n/ω(G)`,
    dual feasibility `|S|/ω ≤ 1` immediate (every clique S has |S| ≤ ω). No LP, no float.
  - `search_assoc_scheme_family` — CLOSED as a bounded EXACT search over mu-rich
    vertex-transitive families (Johnson J(k,2)=T(k), J(k,3); Hamming H(d,q); circulant
    Cayley Cay(Z_n,S), n<37). Each evaluated with exact ω (bitset b&b), exact embedding
    dim (fast modular + 2-prime agreement), exact rational chi_f = n/ω. Fire iff
    `chi_f + μ > n` with `ω(G) ≤ 5`, emb ≤ 62.
- **RESULT — CLEAN NEGATIVE:** no candidate fires. Among the ω(G)≤5 candidates the
  firing margin `chi_f + μ − n` is STRICTLY NEGATIVE in every case (best: T(6) at −3;
  H(2,4) −3; H(2,5) −4; J(7,3) −14; …). I.e. `chi_f = n/ω(G) ≤ emb+1` throughout, so
  the sharper fractional dual buys nothing over Bondarenko's `ceil(n/ω)` for these
  mu-rich families. Final line: `CLEAN NEGATIVE: no mu-rich vertex-transitive
  candidate with omega(G)<=5 fires ... Upper bound stays 63.`
- This is a NEGATIVE result, NOT a bound. The two R4 holes are computed (no
  `NotImplementedError`); the remaining open question is OUTLINER-level (does any
  non-table, non-transitive ω≤5 two-distance family escape `n/ω ≤ emb+1`?). Nothing
  written to `held`.

## theta-cover-dual (chi_f = v/alpha vertex-transitive pin; named families CLOSED, off-table discovery OPEN)
```
python3 constants/28a/certificate/theta_designs.py     # design constructors self-test
python3 constants/28a/certificate/theta-cover-dual.py  # the sketch
```
- `theta_designs.py` (network-free, exact GF(2)/integer): builds Steiner triple systems
  (Bose), the extended Golay code (verified weight enum 1+759x^8+2576x^12+759x^16+x^24),
  the Witt designs S(5,8,24)→S(3,6,22) (77 blocks, every triple once), and the Cameron
  graph srg(231,30,9,3) (M22-transitive, regular degree 30). Self-test exit 0.
- The sketch fires on the GENUINE theorem `chi(G_d) >= chi_f(G_d) = v/alpha(G_d)` EXACT for
  vertex-transitive G_d (not the weak `ceil(v/5)`). Firing needs alpha(G_d) <= need_omega(v)
  (= largest w with ceil(v/w)>=64) in some orientation, at embedding dim <= 62.
- **R4 ADVANCE — both load-bearing holes CLOSED for the 14 existence-confirmed named
  vertex-transitive families** among the srg-sweep's 207 parameter-only-OPEN rows
  (the ex='+', f<=62 rows the parameter-only Delsarte-Hoffman test could not settle):
  - **13 Steiner block-intersection rows** S(2,3,n) (n=37..63) and S(2,4,n) (n=49,52,61):
    settled by CLOSED-FORM clique LOWER bounds, no construction needed —
    `omega(A) >= (n-1)/(k-1)` (pencil clique through a point) and
    `omega(A-bar) >= ceil((n-1)/(k(k-1)))` (maximal partial parallel class, via a
    maximality counting argument). BOTH exceed need_omega(v) for all n<=63, so neither
    spherical orientation fires.
  - **Cameron graph srg(231,30,9,3)**: built exactly; `omega(A)=7` by exact bitset
    branch-and-bound (g24.max_clique_le, matches Brouwer), greedy `alpha(A)>=17` (Hoffman
    exact 21). Both `> need_omega(231)=3`, so it does not fire.
- **RESULT — CLEAN NEGATIVE on the 14 named families: NONE fires** (`resolve_named_families`
  asserts `any_fire=False` at runtime; the script exits 0 with `fired=False`). The true
  point/clique ratio `v/alpha` of every settled row is far below 64 (e.g. Cameron 231/7=33),
  confirming G_2(4)'s 416/5=83.2 remains the densest known ratio.
- **RESIDUAL OPEN HOLE (honest):** `build_candidate_graph` still raises NotImplementedError
  for the genuine off-table discovery — a NEW vertex-transitive two-distance set (family-b
  Cayley graph), or the exact clique numbers of the 3 remaining dense 2-graph rows
  (v=220,276,344, which are dense so expected large-omega but not yet computed here) —
  with `min(omega(A),omega(A-bar)) <= need_omega(v)` at emb<=62. No such object known.
- This is a NEGATIVE / informativeness result, NOT a bound. Nothing written to `held`.

## fresh-orthogonal-dir (attack line A; exact NEGATIVE on the structured family)
```
python3 constants/28a/certificate/fresh-orthogonal-dir.py
```
- Holes 1&2 closed via g24. Hole 3 reshaped to its exact form: embedding-dim(T) <= 62
  <=> dim(E ∩ span(e_{T^c})) >= 3, where E = colspace(Gram) = eig-20 eigenspace of A.
- Expected (exit 0): exact integer rank of Gram on C = 63 (obstruction confirmed);
  cap_dim(E,B)=2; structured search yields a best dim-62 subset of EXACTLY 270 points
  (exact integer rank 62, omega<=5), ceil(270/5)=54 << 64. DEFICIT 46 points.
- This is a NEGATIVE result on the structured fresh-direction family, NOT a bound.
  The general existence question (any <=100-coord Q with cap_dim>=3) remains an OPEN
  HOLE (search_codim4_vector_general raises NotImplementedError). Nothing to `held`.

## mixed-construction (attack line D; build_core CLOSED, perturbation OPEN)
```
python3 constants/28a/certificate/mixed-construction.py
```
- Imports cached g24 (exact clique) + fresh-orthogonal-dir (exact rank, eigenspace,
  structured section). Runs ~20 s, exit 0.
- **build_core CLOSED (round 3):** a G_2(4) hyperplane section of C with
  `|T|=270`, EXACT integer rank over Q `= 62` (via `fo.exact_rank`, not float SVD),
  and `alpha(diameter graph) = omega(smaller-distance graph A[T,T]) = 5` (exact bitset
  `g24.max_clique_le`), `ceil(270/5)=54`. Asserted at runtime.
- **Correct Borsuk criterion (fixed round 3):** parts = `chi(diam graph)`; lower bound
  `>= |X|/alpha(diam graph)`; certifiable target `alpha(G_d) <= 5` = `omega(complement
  of G_d) <= 5`. The round-2 `verify()` checked `omega` of the diameter graph (wrong
  quantity) — now corrected. `_omega_le` cross-checked equal to `g24.max_clique_le` on
  the core's diameter-graph complement.
- **engineer_perturbation OPEN:** bounded greedy (20000 iters / 90 s cap, frequent
  stdout) accepts 0 points; best `|X| = 270` (`ceil = 54 < 64`). Obstruction:
  the core fills its diameter ball, so any addable point is a complement-neighbor of
  ~268 core points and extends a 5-clique of the complement to 6, breaking
  `alpha <= 5`. Reaching 316 is undischarged.
- This is NOT a bound. The 270-pt 62-dim core is real/exactly-certified but
  `54 < 64`, so no counterexample. Nothing written to `held`.
