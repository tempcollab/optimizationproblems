# Certificate record — staircase-containment-lift (30a, lift held 81/8 `*`→verified)

Sketch: `constants/30a/certificate/staircase-containment-lift.py` (standalone Python, no project).

## Reproduce

```
python3 constants/30a/certificate/staircase-containment-lift.py     # <1 s, prints LIFTED
```

Requires: `python3` only (stdlib `fractions`, `itertools`, `math`, `random`). No numpy/scipy.
Deterministic (the single random use is a fixed-seed teeth check).

## What is established (in-script, reproducible) — R4

This sketch does NOT produce a new numeric bound; it LIFTS the existing held value
`gr(Av(1324)) ≥ 81/8 = 10.125` from `*`-minimally-verified (containment + growth-order CITED to
BBEPP Thm 5.1 / Prop 3.6) to in-script-proved on the held axis. Below the record 10.271 by
construction (81/8 IS BBEPP Thm 5.1's own value).

R3 left the load-bearing hole **H-X** OPEN (after correctly RETIRING the R3 "1324 local to 2
cells" reduction, which had been "proved" with a FALSE column-separated geometry). R4 CLOSES H-X.

- **H-X / H-C (containment `P_k ⊆ Av(1324)`, all k) — CLOSED.** Three length-independent lemmas:
  - **LEMMA DOMINO** (`lemma_domino_structural`): orientation-A between-components domino avoids
    1324, proved for all sizes by CLOSURE under induced sub-permutations (0 violations) + complete
    finite base over all ≤6-point dominoes incl. every 4-point split (1779 dominoes, all avoid
    1324; 3 other orientations DO make 1324 — teeth). (Unchanged from R3; SOUND.)
  - **LEMMA REDUCTION** (`lemma_reduction_grid_structural`): every 1324 in the descending
    (Av213,Av132) staircase GRID CLASS is confined to two CONSECUTIVE cells. Proof is a COMPLETE,
    GENERATOR-FREE order-constraint enumeration on the grid blocks `col_block(m)=⌈m/2⌉`,
    `row_block(m)=⌈(m+1)/2⌉` (read off BBEPP Fig 1 / Fig 10): over 2 steps both blocks rise, so
    cells `|m−m'|≥2` are skew-separated; enumerate every assignment of the four 1324-roles to cell
    indices consistent with the forced block inequalities — EVERY one has cell-span ≤ 1
    (`by_span={0:…, 1:…}`, invariant under index-window size). This is the FAITHFUL replacement for
    the refuted R3 reduction; independently corroborated by exhaustive small-staircase enumeration.
  - **LEMMA CROSS-CELL** (`lemma_crosscell_exclusion`): a consecutive-cell pair avoids 1324. The
    pair is either (A) a domino — 1324-free by the DEFINITION of a domino (BBEPP line 920), which
    P_k places in domino cells — or (B) a connecting/domino pair, where the between-components rule
    makes BOTH vertical sub-cases (connecting cell lower Av132 = orientation-A = LEMMA DOMINO, or
    upper Av213) avoid 1324, proved by closure + complete ≤6-pt base; horizontal sub-cases follow
    by the INVOLUTION argument (1324, 213, 132 are all self-inverse, so transposing the plot maps a
    vertical between-components pair to a horizontal one preserving avoidance). Teeth: a FREE
    interleave (no between-components rule) DOES create 1324s.
  - Composition: `P_k ⊆ Av(1324)` for all k.
- **H-T (sub-exponential factor) — CLOSED (R3, unchanged).** Held limit uses only `gr(D)=27/4`
  (cache lemma `domino_growth_constant`); `|D_n|=θ(n)(27/4)^n` with `|log θ|/n → 0` and
  `|log θ|/log n` bounded (polynomial θ ⇒ `θ^{1/n}→1`), so θ drops out of the n-th-root limit.

## Soundness / scope (reviewer-checkable)

- No `sorry`/`NotImplementedError` left; every load-bearing check is asserted in-script, the
  script runs to a printed `LIFTED:` line (exit 0).
- The MATHEMATICAL content of every load-bearing step is in-script, COMPLETE, and
  length-independent: REDUCTION is a finite order enumeration (no sampling); CROSS-CELL is closure
  + complete finite bases + the involution identities; all carry TEETH.
- The ONE judgment left to the reviewer is MODEL FAITHFULNESS: that the grid blocks
  `col_block/row_block`, the per-cell patterns (odd Av213 / even Av132), and the
  between-components rule ARE BBEPP's `P_k` — argued line-by-line from `literature/BBEPP2017.md`
  and the paper PDF (lines 216-260, 903-936), pinned to the verbatim reduction at line 919 and the
  verbatim between-components rule at lines 933-936. Same kind of judgment the reviewer made for
  `insertion_encoding_edge_rule_Av1324`.

## Promotable lemma proposed

`staircase_domino_containment_Av1324` — see `approaches/staircase-containment-lift.md` for the
exact statement and proof locations.
