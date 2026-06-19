# Certificate record — tromino-catalan-cell-lower (30a, gr(Av(1324)) lower bound)

Sketch: `constants/30a/certificate/tromino-catalan-cell-lower.py` (standalone Python, no project).

## Reproduce

```
python3 constants/30a/certificate/tromino-catalan-cell-lower.py
```

Requires only `python3` (stdlib: `fractions`, `itertools`, `math`). No numpy/sympy. The
load-bearing arithmetic (the exact gap) is pure `fractions.Fraction`. Exits 0 (the top-level
`lower_bound()` is wrapped so the open-hole `NotImplementedError` prints and the script exits
green). Runtime: a few seconds (enumeration capped at n ≤ 8).

## What is CLOSED this round (R4), exact, reproducible

- **H-SOUND-TEETH (`verify_sound_teeth`).** The soundness obligation for a 3-cell staircase block
  is checked under the REAL adjacent-cell overlap (free column interleave), NOT a column-separated
  geometry. At n=6 the descending (Av213 | Av132 | Av213) real-overlap window both CONTAINS 1324
  (207 fillings) and AVOIDS it (513) — so the 1324 guard is non-vacuous (has teeth, run_state R2
  rule). A column-separated descending stack would avoid 1324 trivially (vacuous guard); the
  overlap is what makes 1324 reachable.
- **H-BRACKET / exact gap (`exact_gap_certificate`).** Pure-`Fraction` bracket on the
  per-block-point growth of any sound concretely-enumerable 3-cell staircase block:
  - column-SEPARATED proxy (sound lower proxy): grows ~3.3 at n=8 (→ ~4 region) — well below target;
  - best CERTIFIED-SOUND concrete block growth: the 2-cell domino's EXACT 27/4 = 6.75 (BBEPP
    Prop 3.6, cache lemma `domino_growth_constant`);
  - EXACT-rational gap to target: **6876/1000 − 27/4 = 63/500 = 0.126** (a +1.867% relative lift).
  This is the bankable diagnostic number — the precise exact-rational shortfall the open 3rd-cell
  overlap freedom must supply, the number BBEPP did not produce for a concrete block.

## What is OPEN (the record-beating holes)

- **H-CNT (load-bearing, OPEN):** exact count of the Catalan-decorated tromino under the
  between-components interleave on both boundaries — BBEPP's NAMED open tromino-enumeration problem
  (arXiv:1711.10325 §7.4 item 3). R4 PINNED the target regime: column-separated grids undercount
  (~4, measured) and value-only relaxations overcount to ~the whole class (~11.6, measured); the
  true block growth lives strictly between, reachable only by a GF-weighted (Catalan-forest) cell
  that keeps the column grid — NOT an integer automaton (which caps logarithmically, run_state rule).
- **H-GROW (OPEN):** per-block-point growth from H-CNT vs 6876/1000. Needs H-CNT.
- **H-DROP (OPEN):** drop g_blk into the VERIFIED Thm-5.1 product, exact-rational compare. Needs H-GROW.

`tromino_block_count` / `tromino_block_growth` / `assemble_via_product` raise
`NotImplementedError`; `lower_bound()` raises, so no false RECORD line can print.

## Claimed value

CLAIM (NOT verified — the record holes are open): no advance on held; held stays 81/8 = 10.125.
This sketch does NOT beat the record. Bankable deliverable this round: the exact-rational gap
63/500 = 0.126 of the best certified-sound concrete block to the 6.876 target, plus the verified
non-vacuous soundness teeth and the measured bracket pinning why integer enumeration cannot close
H-CNT. DIAGNOSTIC, not a bound.
