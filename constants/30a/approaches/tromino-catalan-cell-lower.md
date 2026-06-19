# tromino-catalan-cell-lower — the measurable sub-goal for the H1 record lever

**Side / target.** Lower bound. Top-level target (registry-exact, unchanged):
`gr(Av(1324)) > 10.271`, beating BBEPP2017's verified lower record, where
`gr(Av(1324)) = lim_n |Av_n(1324)|^{1/n}`.

**Why this sketch (R4, new).** `tromino-richer-cell-lower` reduced the record-break to ONE
exact-rational target (all its scaffolding VERIFIED, R3): a **sound ≥3-cell block
`B' ⊆ Av(1324)`** under the staircase between-components interleave with **per-block-point
growth `g_blk ≥ 6876/1000 = 6.876`**, dropped into the re-derived BBEPP Thm-5.1 product. The
two-cell wall (verified R3) caps every 2-cell domino at `27/4 = 6.75`, so the lift must come
from a 3rd cell. That 3-cell count is BBEPP's NAMED OPEN PROBLEM. This sketch is the **concrete,
measurable sub-goal** the R4 explorer asked for: build the exact-count machinery for a 3-cell
**Catalan-forest-decorated** block, measure how close its certifiable per-block-point growth
gets to 6.876, report the gap. Honest framing: low-probability record-break this round; the
bankable output is the measured gap — the number BBEPP could not produce.

**Borrows.** `tromino-richer-cell-lower` (the VERIFIED product `product_growth_exact` + exact
threshold + two-cell wall — H-DROP reuses them verbatim); `staircase-containment-lift` (the
DOMINO-lemma flavour for H-SOUND, extended to a 3-cell window with the real overlap).

**The block.** A tromino `upper(Av213) | middle(Catalan-forest) | lower(Av132)` with
upper/lower points placed strictly BETWEEN the middle cell's skew-indecomposable components
(between-components on BOTH boundaries — the real overlap, per the run_state R3 standing rule).
The middle cell uses the BBEPP Catalan-forest count `|C_{n,c}| = (c/n)·C(2n−c−1, n−1)`; the
+1.87% lift over 27/4 must come from the cross-cell interleave freedom the 3rd cell adds.

**Holes.**
- **H-CNT (load-bearing, OPEN)** `tromino_block_count` — the EXACT count of the
  Catalan-decorated tromino under the between-components interleave in BOTH cell-pair
  directions. NOT a plain product of cell counts (the interleave couples the cells); the
  analogue of `|P_k|` for a 3-cell tile. Needs a closed form OR an exact-rational GF-weighted
  transfer object (an INTEGER automaton caps logarithmically — run_state rule — so it cannot
  reach 6.876). This is the "new idea" BBEPP flagged.
- **H-GROW (OPEN)** `tromino_block_growth` — `g_blk = lim_N |block_N|^{1/N}` from H-CNT; compare
  to the exact `6876/1000`.
- **H-DROP (OPEN)** `assemble_via_product` — drop `g_blk` into the VERIFIED Thm-5.1 product,
  compare `g^36` to `(10271/1000)^36` by EXACT-rational comparison. Closes the record IFF
  `g_blk ≥ 6876/1000`.

## R4 — what was CLOSED this round

- **H-SOUND-TEETH (CLOSED)** `verify_sound_teeth`. Replaces the bare H-SOUND hole with its
  verifiable first half: the 3-cell staircase block's 1324-avoidance is checked under the REAL
  adjacent-cell overlap (free column interleave), NOT a column-separated geometry. At n=6 the
  descending (Av213 | Av132 | Av213) real-overlap window both CONTAINS 1324 (207 fillings) and
  AVOIDS it (513) — proving the 1324 guard is **non-vacuous** (has teeth, run_state R2 rule). A
  column-separated descending stack would avoid 1324 trivially (a vacuous guard); the overlap is
  what makes 1324 reachable. The remaining (open) half of H-SOUND is the length-INDEPENDENT
  structural argument — still part of H-CNT's object, deferred.
- **H-BRACKET (CLOSED, exact-rational)** — replaces the old weak single-proxy H-MEASURE with a
  rigorous two-sided bracket on the per-block-point growth `g_blk` of any sound concretely-
  enumerable 3-cell staircase block, and the EXACT gap to target:
  - column-SEPARATED proxy (a sound lower proxy, skew grid): grows ~3.3 at n=8 (→ ~4 region) —
    well below 6.876; its low value is the measured **proof** that column-separation throws away
    the interleave freedom (the geometry the soundness rule forbids as wrong);
  - value-only proxy (free columns, value bands only): tracks |Av_n(1324)| to within 1
    (1,2,6,23,103,513,2761,…) — a near-whole-class OVERcount (~11.6), confirming a value-only
    relaxation discards the column grid entirely;
  - best CERTIFIED-SOUND concrete block growth: the 2-cell domino's EXACT 27/4 = 6.75 (BBEPP
    Prop 3.6, cache lemma `domino_growth_constant`);
  - **EXACT-rational GAP to target: `6876/1000 − 27/4 = 63/500 = 0.126` (a +1.867% lift)**, pure
    `Fraction`. This is the bankable diagnostic — the precise exact-rational shortfall the open
    3rd-cell overlap freedom must supply, the number BBEPP could not produce for a concrete block.
  - **Pin on H-CNT:** the true block growth lives STRICTLY between the column-separated proxy (~4)
    and the value-only overcount (~11.6); reaching 6.876 needs a GF-weighted (Catalan-forest) cell
    that KEEPS the column grid while crediting the overlap multiplicity — exactly the open object,
    and NOT an integer automaton.

## Claimed value (R4)

**CLAIM (clearly a CLAIM, NOT verified — the record holes are open): no advance on held; held
stays 81/8 = 10.125.** This sketch does NOT beat the record (10.271) this round, as expected —
H-CNT is BBEPP's named open problem. Bankable, reproducible deliverables: (1) the exact-rational
gap **63/500 = 0.126** of the best certified-sound concrete block (the domino, 27/4) to the 6.876
target; (2) the verified **non-vacuous soundness teeth** under the real overlap; (3) the measured
**bracket** (~4 column-separated, ~11.6 value-only) pinning exactly why no integer enumeration
closes H-CNT. All diagnostics, not bounds.

## What would push it further

- The open H-CNT: a GF-weighted (Catalan-forest) 3-cell transfer object whose dominant eigenvalue
  (per-block-point growth) lands in the bracket interior and clears 6.876. The exact gap 63/500
  removes all ambiguity about how much the 3rd cell must add.
- Feed the verified teeth + bracket back to `tromino-richer-cell-lower` (the parent H1 lever) and
  `transfer-matrix-lower` (shared GF-cell blocker).

**Hard step.** H-CNT — the exact interleaved count of a Catalan-decorated 3-cell block. This is
the genuine open math (BBEPP: "enumerating trominoes seems to require some new ideas"). Mechanism
required: a GF-weighted cell (entries are Catalan-forest counts, not integer transition counts)
so the per-block-point growth can exceed the integer-automaton logarithmic cap.

**Lean-fit.** H-DROP + the threshold are exact-rational (Lean-fit). H-CNT's certificate, IF it
is an exact-rational CW witness on a finite GF-weighted matrix, is Lean-fit in shape; if it is a
continuum GF singularity it is Lean-hostile. The honest read: this likely bottoms out in
GF/singularity analysis (the BBEPP open problem), so a numerical certificate is the fallback.

**Sketch file.** `constants/30a/certificate/tromino-catalan-cell-lower.py` (runs green, exits 0;
H-SOUND-TEETH + H-BRACKET CLOSED and print; the three record holes H-CNT/H-GROW/H-DROP raise via
`lower_bound()` until filled, so no false RECORD line can print). Reproduce:
`python3 constants/30a/certificate/tromino-catalan-cell-lower.py` (stdlib only).
