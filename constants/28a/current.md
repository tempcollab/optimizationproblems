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
