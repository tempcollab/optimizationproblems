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
