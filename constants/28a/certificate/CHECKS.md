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

## musin-edge-edit (Musin θ/μ line; PARTIAL — search implemented, does NOT fire)
```
python3 constants/28a/certificate/musin-edge-edit.py
```
- Imports cached `g24.max_clique_le` (exact ω bitset). Runs ~6 s, exit 0.
- Expected: `[selftest] fast evaluator == exact-rational ... OK` (the fast modular
  μ-evaluator `embedding_dim_fast` agrees with the slow exact-rational
  `embedding_dim_two_distance` on the disjoint-K5 skeleton, emb 19, and rook K5□K5,
  emb 8 — both at integer root t=2). Then the μ-raising lever table (rook K5□K_m:
  μ rises 0→16, fire margin θ+μ−n stuck at −4 under ω≤5) and a bounded edge-flip
  search on a 4×K5 skeleton (n=20) that reaches emb 14 (μ=5) and reports
  `fired=False`.
- LOAD-BEARING hole `maximize_mu_over_edge_flips` is now IMPLEMENTED and runs
  (bounded: hard `max_iter` + `wall_budget_s`, stdout progress) but does NOT fire:
  no ω≤5 graph reaching emb≤62 (μ≥n−63) at n≥316 found. The `verify` certification
  core is exact and intact (`verify(rook K5□K5)` → `is_counterexample=False`).
- This is a PARTIAL / negative-leaning result, NOT a bound. Best embedding dim under
  the ω≤5+fire constraints does not beat 63. Nothing is written to `held`.

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
