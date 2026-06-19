# Certificate record — transfer-matrix-lower (30a, gr(Av(1324)) lower bound)

Sketch: `constants/30a/certificate/transfer-matrix-lower.py` (standalone Python, no project).

## Reproduce

```
cd constants/30a/certificate
python3 transfer-matrix-lower.py          # default K=10 headline (~9 min)
python3 transfer-matrix-lower.py 8        # fast self-check (seconds), K=8 -> 5.286072
```

Requires: `python3` with `numpy` (used ONLY to pick the CW witness vector; the load-bearing
Collatz–Wielandt inequality is checked in exact `fractions.Fraction`).

## What is certified (all exact-rational, sound, UNCONDITIONAL)

- R1 floor (skew-sum subclass `S_8 ⊆ Av(1324)`, companion matrix CW):
  `gr(Av(1324)) ≥ 1886663/500000 = 3.773326`.
- R2 headline (sound bounded-state insertion-encoding automaton `A_K`, K=10, dominant-SCC
  exact-rational CW): **`gr(Av(1324)) ≥ 8887516/1428099 = 6.223319`**.
  Lower-K self-checks (also exact): K=6 `21667027/5467507`=3.962871, K=8 `19992608/3782129`=5.286072,
  K=9 `1804171/311442`=5.792960.

CLAIMED held advance: **3.773326 → 6.223319** (sound, unconditional, reproducible). Does NOT beat
the record 10.271 (no feasible K does — logarithmic convergence to ~11.6).

## Soundness (load-bearing, reviewer re-derivable)

`A_K` counts the subclass `B_K = { p ∈ Av(1324) : every value-prefix's insertion state has
length ≤ K }` EXACTLY (verified `|B_K,n| = #walks`, n≤8; `#walks ≤ |Av_n|`, n≤12), so
`ρ(A_K) = gr(B_K) ≤ gr(Av(1324))`. Edge rule "insert new max at pos creates 1324 ⇔ p[:pos]
contains 132" verified exhaustively to length 8→9 (`prove_edge_rule`). The dominant-SCC CW bound
`λ = min_i (Mw)_i/w_i` satisfies `Mw ≥ λw` entrywise in exact `Fraction` arithmetic by
construction. No averaging, no min-weighting, no Conjecture 8 — strictly sound.

No `sorry`/`NotImplementedError` on the certified path: the script runs to a printed CERTIFIED
line with all load-bearing checks asserted in exact arithmetic.
