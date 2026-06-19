# Certificate record — tromino-richer-cell-lower (30a, gr(Av(1324)) lower bound)

Sketch: `constants/30a/certificate/tromino-richer-cell-lower.py` (standalone Python, no project).

## Reproduce

```
python3 constants/30a/certificate/tromino-richer-cell-lower.py
```

Requires `python3` with `sympy` (exact symbolic display of the closed form) and `numpy`/`scipy`
(used ONLY for the float threshold diagnostic, NOT load-bearing). The load-bearing comparisons are
pure `fractions.Fraction` arithmetic.

## What is CLOSED this round (R3), all exact, reproducible

- **H2 — the general Thm-5.1 product, re-derived (not re-scaled).**
  `g(g_blk,d,e,f) = exp( [2 d log g_blk + log H(2e-f,e) + 2 log H(d+f,d)] / (2d+e) )`,
  normalisation `N=(2d+e)k²` re-derived from the construction; reproduces EXACTLY 81/8 at
  `(g_blk,d,e,f)=(27/4,14,8,7)` (`verify_H2_reproduces_held`).
- **Threshold — exact-rational.** A block with per-block-point growth `g_blk = 6876/1000` at ratios
  (14,8,7) gives product `> 10.271`, certified by the PURE rational comparison
  `g_blk^28 · H(9,8) · H(21,14)^2  >  (10271/1000)^36`  (= `g^36 > record^36`, all `Fraction`).
  Hence ratio-optimised threshold `gB* < 6.876` (a +1.87% lift over 27/4).
- **Two-cell wall — verified.** Every 2-cell domino (balanced or unbalanced) has per-block-point
  growth EXACTLY 27/4 = 6.75 < 6.876 (BBEPP Prop 3.6 + finite teeth check), so NO 2-cell block can
  clear the record; the richer block needs ≥ 3 cells. (Refutes the "unbalanced 2-cell" candidate.)

## What is OPEN (the record-beating hole)

- **H1 (reshaped, OPEN):** a SOUND ≥3-cell gridded block `B' ⊆ Av(1324)` with per-block-point
  growth `≥ 6876/1000`, exact-rational CW certified, 1324-avoiding under the staircase interleave
  rule. This IS BBEPP's named open tromino problem. `richer_block_growth()` raises
  `NotImplementedError`; `lower_bound()` raises, so no false RECORD line prints.

## Claimed value

CLAIM (not verified — H1 open): no advance on held; held stays 81/8 = 10.125. In hand: the exact
CONDITIONAL lever "any sound ≥3-cell block with per-block-point growth ≥ 6.876 ⇒ gr(Av(1324)) >
10.271." Does NOT beat the record yet (H1 is the missing step).
