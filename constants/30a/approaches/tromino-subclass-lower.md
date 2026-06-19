# tromino-subclass-lower — LOWER bound by a 3-cell (tromino) staircase subclass

**Side / target.** Lower bound. Top-level target: `gr(Av(1324)) >= g > 10.271` from an explicit
tromino-based staircase subclass with computable growth rate `g`. Beats BBEPP2017's 10.271.

**Strategy (explorer angle B1 — BBEPP's named open route).**
BBEPP decompose the (Av(213),Av(132)) staircase into alternating **dominoes** (2 cells) +
connecting cells, build a subclass with an exact closed-form count (Thm 5.1, `|P_k| =
|B_14k|^k·|C_8k,7k|^k·C(21k,14k)^{2k-1}`), optimise point-ratios -> 81/8 = 10.125, refined to
10.271. They flag explicitly (§7.4): "If we established a lower bound on the growth rate of
permutations gridded in the first THREE cells (**trominoes**), we could decompose the staircase
into trominoes to yield a new bound."

Plan: build an explicit 3-cell tromino subclass of Av(1324) with computable growth rate,
decompose the staircase into trominoes (BBEPP Thm 5.1 analogue), optimise ratios -> `g >
10.271`. Trominoes carry strictly more structure than dominoes, so per-block growth exceeds
27/4 and the staircase bound should exceed BBEPP's.

**Holes.**
- **H1 (the hard step)** a *lower bound* on the tromino growth rate. BBEPP: "enumerating
  trominoes seems to require some new ideas." A lower bound (not exact enumeration) suffices —
  reachable via a transfer-matrix sub-sub-class *inside* the tromino (Lean-fit, shares machinery
  with transfer-matrix-lower).
- **H2** exact count of the tromino staircase subclass with the between-components interleave
  rule guaranteeing 1324-avoidance (BBEPP Thm 5.1 analogue).
- **H3** optimise point-ratios -> `g > 10.271`.

**Lean-fit.** Mixed: H1 can be Lean-fit (transfer matrix + Collatz-Wielandt). H2 is an
exact algebraic count; H3 a finite rational ratio search if ratios are restricted — partly
Lean-fit, partly numerical.

**Honest estimate.** Conceptually the most principled lower-bound improvement (more structure =
strictly bigger bound), but H1 is genuinely hard (BBEPP couldn't enumerate trominoes). Borrows
the transfer-matrix/Collatz-Wielandt sub-bound from **transfer-matrix-lower** for H1. Multi-round.

**Sketch file.** `constants/30a/certificate/tromino-subclass-lower.py` (runs; holes raise).
