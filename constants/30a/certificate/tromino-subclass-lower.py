#!/usr/bin/env python3
"""
Sketch: tromino-subclass-lower
Target (LOWER bound): gr(Av(1324)) > 10.271   [beats BBEPP2017 record 10.271]

Strategy (explorer angle B1, mixed but with a discrete core):
  BBEPP decompose the (Av(213),Av(132)) staircase into alternating DOMINOES
  (2 adjacent cells) + connecting cells, build a subclass with an EXACT closed-form
  count, and optimise point-ratios -> 81/8 = 10.125 (Thm 5.1), refined to 10.271.
  They explicitly flag: "If we established a lower bound on the growth rate of
  permutations gridded in the first THREE cells (TROMINOES), we could decompose
  the staircase into trominoes to yield a new bound."

  Plan: build an explicit 3-cell (tromino) subclass of Av(1324) with a computable
  (exact rational/algebraic, or transfer-matrix) growth rate, decompose the
  staircase into trominoes, and optimise -> a bound > 10.271. Trominoes carry
  strictly more structure than dominoes, so the per-block growth exceeds 27/4 and
  the staircase bound should exceed BBEPP's domino-based one.

Load-bearing HARD step (H1): a lower bound on the tromino growth rate. BBEPP say
"enumerating trominoes seems to require some new ideas." A LOWER bound (not exact
enumeration) suffices and may be reachable via a transfer-matrix sub-sub-class
inside the tromino (Lean-fit, like the transfer-matrix-lower sketch), sidestepping
the exact functional equation. Risk: even the lower bound is hard; multi-round.

HOLES:
  H1  tromino_growth_lower(): a certified lower bound g3 on the growth rate of
      1324-avoiding permutations gridded in 3 consecutive staircase cells
      (transfer-matrix / Collatz-Wielandt sub-bound is Lean-fit).
  H2  tromino_decomposition(): the analogue of BBEPP Thm 5.1 -- exact count of the
      tromino-based staircase subclass, guaranteeing 1324-avoidance via the
      between-components interleave rule.
  H3  optimise_ratios(): optimise point-ratios across tromino/connecting cells;
      verify the resulting growth rate > 10.271.

Lean-fit: H1 can be Lean-fit (transfer matrix). H2/H3 are an exact-count +
optimisation; the count is discrete/algebraic, the optimisation is a finite
rational search if ratios are restricted -- partly Lean-fit, partly numerical.
"""
RECORD_LOWER = 10.271  # BBEPP2017 verified lower bound to strictly beat


def tromino_growth_lower():
    """HOLE H1: certified lower bound on the 3-cell (tromino) growth rate."""
    raise NotImplementedError("H1: tromino growth-rate lower bound")


def tromino_decomposition():
    """HOLE H2: exact count of the tromino-based staircase subclass (BBEPP Thm 5.1 analogue)."""
    raise NotImplementedError("H2: tromino staircase subclass exact count")


def optimise_ratios():
    """HOLE H3: optimise point-ratios -> growth rate (must exceed 10.271)."""
    raise NotImplementedError("H3: ratio optimisation -> staircase growth rate")


def lower_bound():
    tromino_growth_lower()      # H1
    tromino_decomposition()     # H2
    g = optimise_ratios()       # H3 (float/Fraction, must be > 10.271)
    assert g > RECORD_LOWER, f"growth {float(g)} does not beat {RECORD_LOWER}"
    print(f"CERTIFIED gr(Av(1324)) >= {float(g)} > {RECORD_LOWER}")
    return g


if __name__ == "__main__":
    lower_bound()
