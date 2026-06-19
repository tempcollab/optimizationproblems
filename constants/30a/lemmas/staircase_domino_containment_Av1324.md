# Lemma `staircase_domino_containment_Av1324` — certified R4

## Statement (keyed to the in-script abstract grid family; BBEPP's `P_k` is an instance)

Consider the descending `(Av(213), Av(132))` staircase grid class: cells indexed `m = 1,2,…`
down the anti-diagonal, with grid blocks `col_block(m) = ⌈m/2⌉`, `row_block(m) = ⌈(m+1)/2⌉`
(row-block 1 = highest values), odd cells avoiding 213, even cells avoiding 132. Let `σ` be a
permutation gridded in this staircase such that

  (i)  each domino cell-pair is a genuine 1324-avoiding domino (upper Av213 / lower Av132 cell,
       the pair jointly 1324-avoiding — the object BBEPP place in domino cells), and
  (ii) every domino-cell point sits strictly between two consecutive skew-indecomposable
       components of each adjacent connecting cell (the BBEPP between-components rule).

Then `σ` avoids 1324.

In particular, BBEPP2017 Thm 5.1's subclass `P_k` (which is built to satisfy (i)–(ii)) avoids
1324 for every `k`, so `P_k ⊆ Av(1324)`.

## Proof (length-independent; two structural lemmas composed)

1. **REDUCTION.** In the staircase grid order, a point in a cell with smaller `col_block` is
   strictly left of one with larger `col_block`, and a point in a cell with smaller `row_block`
   is strictly above one with larger `row_block` (grid-class incidence; within a shared block the
   order is the free interleave). These give necessary block inequalities for any 1324 occurrence
   (column order `w<x<y<z` ⇒ `col_block` nondecreasing along `w,x,y,z`; value order `w<y<x<z` ⇒
   `row_block` nonincreasing). A complete, window-robust enumeration of all role→cell assignments
   consistent with these inequalities shows every consistent assignment has cell-index span ≤ 1.
   Hence every 1324 is confined to two CONSECUTIVE cells. (Over two cell-steps both blocks rise,
   so cells with `|m−m'| ≥ 2` are skew-separated — distant cells cannot jointly hold a 1324.)

2. **CROSS-CELL EXCLUSION.** A consecutive cell pair is either domino-internal (1324-free by (i))
   or a connecting/domino boundary under (ii). For the boundary pairs: the two VERTICAL sub-cases
   (connecting cell lower = Av132, or connecting cell upper = Av213) avoid 1324, proved by a
   complete ≤6-pt finite base plus closure under induced sub-permutations (length-independence);
   the HORIZONTAL sub-cases follow by the involution argument — 213, 132, and 1324 are all
   self-inverse, and 1324-containment is preserved under permutation inverse (transpose), so a
   horizontal between-components pair avoids 1324 iff the corresponding vertical one does.

Composing 1 and 2: any 1324 in `σ` would lie in a single consecutive pair, but every consecutive
pair avoids 1324 — contradiction. So `σ` avoids 1324. ∎

## Certification

- Reviewer (R4) re-ran `constants/30a/certificate/staircase-containment-lift.py` (green, exit 0,
  no `NotImplementedError`/TODO on the path) and independently re-derived the load-bearing step:
  - REDUCTION enumeration re-implemented from scratch; `maxspan = 1` is robust to window size
    (verified at window 12, not just the in-script 10) — a genuine deductive result, not a sample.
  - Independently corroborated by a faithfully-overlapping staircase build (random within-block
    interleave, strict between-block separation): ~1.0×10⁵ actual 1324 occurrences, every one of
    span ≤ 1. This is the geometry the R3 attempt failed to model.
  - CROSS-CELL finite base re-enumerated to ≤7 pts (one step beyond the in-script ≤6) for BOTH
    `conn_side` cases: 7593 pairs each, 0 containing 1324. Closure check passes in-script.
  - Involution facts re-verified: 213/132/1324 all self-inverse; 1324-containment preserved under
    inverse on 20000 random permutations (0 violations).
- **One residual judgment** (model faithfulness): that the in-script grid blocks, per-cell
  patterns, and between-components rule ARE BBEPP's `P_k`. Accepted at the same standard as
  `insertion_encoding_edge_rule_Av1324` — matches the BBEPP digest (`literature/BBEPP2017.md`,
  Prop 2.1 / Thm 5.1 construction, the verbatim between-components rule). The lemma is admitted
  keyed to the abstract grid family above; `P_k` is an instance by that judgment.
- Statement is correct and no stronger than proved (it is a CONTAINMENT/avoidance statement, not
  a conditional value identity — the R3-rejected `staircase_product_growth_formula` was rejected
  for being the latter; this one is not).

## Used by

`tromino-subclass-lower` (lifts its containment `*` once it imports this), `staircase-containment-
lift` (the lift itself), and any future staircase/tromino construction that needs `P_k ⊆ Av(1324)`
without re-proving the containment. Carries the held value `gr(Av(1324)) ≥ 81/8 = 10.125`
(fully verified, below the record 10.271 by construction).
