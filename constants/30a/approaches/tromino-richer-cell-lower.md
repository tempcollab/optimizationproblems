# tromino-richer-cell-lower — record push via a RICHER sound staircase block

**Side / target.** Lower bound. Top-level target: `gr(Av(1324)) > 10.271` — beat BBEPP2017's
verified record on the cleanest, lowest-risk algebraic lever the R3 explorer flagged (angle D).
**Top-level statement unchanged** (outliner's; faithful, lower side, right direction).

**Strategy.** BBEPP Thm 5.1's domino-staircase product gives EXACTLY 81/8 = 10.125. The record
10.271 is only +1.44% above it. Drop a **richer SOUND block** with strictly higher per-block-point
growth into the SAME Thm-5.1 product machinery and re-optimise the integer point-ratios.

## R3 — what was CLOSED this round

**H2 (the product re-derivation) — CLOSED, exact.** `product_growth_exact(g_blk, d, e, f)` is the
general BBEPP Thm-5.1 product, re-derived from the construction (NOT a re-scaling of 81/8):

    log g = [ 2 d log(g_blk) + log H(2e-f, e) + 2 log H(d+f, d) ] / (2 d + e),
    H(a,b) = a^a / (b^b (a-b)^{a-b}),   N = (2d + e) k^2.

The normalisation `N = (2d+e)k²` was re-derived from the construction (the first 3k cells hold
k dominoes = 2k cells of d·k points + k connecting cells of e·k points; verified against BBEPP's
`N=36k²` at d=14,e=8). `verify_H2_reproduces_held()` confirms it gives EXACTLY 81/8 at
(g_blk,d,e,f)=(27/4,14,8,7). This is the load-bearing product re-derivation the reviewer required
(H2 was the standing caveat: "re-derive the product, do not re-scale 81/8" — done).

**THRESHOLD — CLOSED, exact-rational.** `required_block_growth_certificate()` certifies, by a PURE
exact-rational comparison `g^36 = g_blk^28 · H(9,8) · H(21,14)^2  >  (10271/1000)^36` (every factor
a `fractions.Fraction`, no float, no `sp.sign`), that a block with per-block-point growth
`g_blk = 6876/1000 = 6.876` at ratios (14,8,7) already gives product `10.2717 > 10.271`. Hence the
exact ratio-optimised threshold `gB* < 6.876` (numeric diagnostic: `gB* ≈ 6.87519`). So the record
is cleared by **any** sound block with per-block-point growth `≥ 6.876` — a **+1.87%** lift over
27/4 = 6.75. This is the concrete exact-rational spectral/count target for H1.

**TWO-CELL WALL — CLOSED, verified (reshapes H1).** `verify_two_cell_wall()`: every 2-cell domino
block — balanced OR unbalanced, any top:bottom split — has per-block-point growth EXACTLY 27/4 =
6.75 < 6.876 (BBEPP Prop 3.6: |B_m| ≥ d_max² ≥ |D_m|²/(m+1)², |D_{2m}| ≥ |B_m| ⇒ gr = 27/4 for all
dominoes; the unbalanced split differs from |D_m| only by a polynomial (m+1) factor, invisible to
the m-th-root limit). **Consequence — H1 reshaped:** the original commentary listed an "unbalanced
a:b domino split" as a candidate realisation of the richer block; that candidate is **REFUTED** —
no 2-cell block can clear the record. The richer block MUST use ≥ 3 cells (BBEPP's open tromino
route). The intermediate "richer block" statement is now sharpened from "per-point growth >
(27/4)²" (which conflated per-cell vs per-block growth) to the precise, exact target
"**per-block-point growth ≥ 6876/1000, ≥ 3 cells**".

## Holes remaining

- **H1 (load-bearing, OPEN, reshaped)** `richer_block_growth()` — a SOUND ≥3-cell gridded block
  `B' ⊆ Av(1324)` (under the staircase interleave rule) with per-block-point growth `≥ 6.876`,
  certified by an exact-rational Collatz–Wielandt witness `M_B v ≥ λ v` on a brute-verified-avoider
  automaton. **Blocker:** this is exactly BBEPP's named open tromino problem ("enumerating trominoes
  seems to require some new ideas"). A 2-cell block is now proven capped at 27/4, so the lift
  genuinely requires the cross-cell interleave freedom of ≥3 cells; per per-role memory plain
  integer automata cap logarithmically (three machines agree), so `M_B` must encode that freedom
  (the analogue of the 14k:8k:7k balance), not a skew/insertion truncation. SOUNDNESS
  co-obligation: `B'` must remain 1324-avoiding tiled under the interleave rule (exhaustive
  `contains_1324` at small block size).

## Claimed value

**Claim (clearly a CLAIM, not verified — H1 open): no new bound yet.** Held remains 81/8 = 10.125.
This round did NOT reach the target hole-free: the only open hole H1 is the record-beating step.
What IS now in hand (verified, reproducible, exact): the *conditional* statement "**any** sound
≥3-cell block with per-block-point growth ≥ 6.876 ⇒ gr(Av(1324)) > 10.271, via the re-derived
Thm-5.1 product." The bound is contingent on H1; until H1 closes, the claim is 10.125 (no advance
on the held value, but a sharp, exact, reusable lever and two refuted dead-candidates).

## What would push it further

- Build `M_B` for a 3-cell block (tromino) and CW-certify per-block-point growth ≥ 6.876. The
  exact rational target removes all ambiguity about "how rich is rich enough."
- Per per-role memory, a finite truncation will not reach 6.876 at feasible size — need a
  GF-weighted / Catalan-decorated 3-cell cell, the genuine new idea BBEPP flagged.

## Lean-fit

Yes. H2 + threshold are now exact-rational arithmetic (ideal Lean targets: a single
`Fraction > Fraction` comparison `g_blk^28 · H(9,8) · H(21,14)^2 > (10271/1000)^36`). The two-cell
wall is BBEPP Prop 3.6 (cache lemma `domino_growth_constant`) + finite teeth check. H1's certificate
(when found) is exact-rational CW on a finite nonnegative matrix + finite avoidance enumeration.

## Promotable lemmas

- **`staircase_product_growth_formula`** — the exact closed form
  `g(g_blk,d,e,f) = exp( [2 d log g_blk + log H(2e-f,e) + 2 log H(d+f,d)] / (2d+e) )`, reproducing
  81/8 at (27/4,14,8,7); proved green in `product_growth_exact` + `verify_H2_reproduces_held()`.
  Reusable by every staircase-product sketch (tromino-subclass-lower, staircase-containment-lift).
  General (a closed-form identity), not sketch glue. **Flag for certification.**

**Sketch file.** `constants/30a/certificate/tromino-richer-cell-lower.py` (builds green; H2 +
threshold + two-cell wall CLOSED, H1 raises).
