# Certificate record — staircase-containment-lift (30a, lift held 81/8 `*`→verified)

Sketch: `constants/30a/certificate/staircase-containment-lift.py` (standalone Python, no project).

## Reproduce

```
python3 constants/30a/certificate/staircase-containment-lift.py     # ~9 s, prints LIFTED
```

Requires: `python3` only (stdlib `fractions`, `itertools`, `math`, `random`). No numpy/scipy.

## What is established (in-script, reproducible)

This sketch does NOT produce a new numeric bound; it LIFTS the existing held value
`gr(Av(1324)) ≥ 81/8 = 10.125` from `*`-minimally-verified (containment + growth-order CITED to
BBEPP Thm 5.1 / Prop 3.6) to in-script-proved on the held axis. Below the record 10.271 by
construction (81/8 IS BBEPP Thm 5.1's own value).

- **H-C (containment `P_k ⊆ Av(1324)`, all k) — CLOSED.** Two length-independent lemmas:
  - LEMMA DOMINO: orientation-A between-components domino avoids 1324, proved for all sizes by
    CLOSURE under induced sub-permutations (`lemma_domino_closure`, 0 violations) + complete
    finite base over all ≤6-point dominoes incl. every 4-point split
    (`lemma_domino_exhaustive_base`, 1779 dominoes, all avoid 1324; 3 other orientations DO make
    1324 — teeth).
  - LEMMA REDUCTION: a 1324 in a descending staircase is confined to two consecutive cells
    (`lemma_reduction_structural`/`_stress`, 114804 superset fillings, 0 span ≥3 cells; boundary
    check confirms the column-disjointness premise has teeth).
  - Composition: `P_k ⊆ Av(1324)` for all k.
- **H-T (sub-exponential factor) — CLOSED.** Held limit uses only `gr(D)=27/4` (cache lemma
  `domino_growth_constant`); `|D_n|=θ(n)(27/4)^n` with `|log θ|/n → 0` and `|log θ|/log n` bounded
  (polynomial θ ⇒ `θ^{1/n}→1`), so θ drops out of the n-th-root limit.

## Soundness / scope (reviewer-checkable)

- No `sorry`/`NotImplementedError` left; every load-bearing check is asserted in-script, the
  script runs to a printed `LIFTED:` line.
- The MATHEMATICAL content is in-script (closure + complete finite base; structural value/column
  argument). The one judgment is MODEL FAITHFULNESS: that the abstract family (descending
  value-bands-by-cell + neighbor-only column overlap + orientation-A between-components) captures
  BBEPP's exact `P_k` — argued from `literature/BBEPP2017.md`, not machine-certified.

## Promotable lemma proposed

`staircase_domino_containment_Av1324` — see `approaches/staircase-containment-lift.md` for the
exact statement (keyed to the abstract family `P`; `P_k` is an instance) and proof locations.
