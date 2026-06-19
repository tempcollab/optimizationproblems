# Current bottom line — 30a, gr(Av(1324))

## Status
none

## Bounds   table: 10.271 · held: 10.125

(Bounds line above is the lower side — the run's verified advance; eval reads it.)
Upper side — table: 13.5 · held: 13.5 (record reproduced, not beaten).
The canonical rigorous record remains `10.271 ≤ gr(Av(1324)) ≤ 13.5` (BBEPP2017).
`held: 10.125` (= 81/8) on the lower side is now FULLY VERIFIED (the `*` was removed in R4):
the count and the exact symbolic growth limit `lim_k |P_k|^{1/36k²} = 81/8` are reproduced
(symbolically and by hand), AND the subclass containment `P_k ⊆ Av(1324)` is now reproduced
in-script (`staircase-containment-lift`, R4): a complete, window-robust order-constraint
enumeration (REDUCTION — every 1324 in the descending (Av213,Av132) staircase grid is confined
to two consecutive cells, independently corroborated on faithfully-overlapping staircases:
~1.0×10⁵ real 1324 occurrences, all span ≤ 1) + finite-base+closure (CROSS-CELL — every
consecutive between-components pair avoids 1324: both vertical sub-cases enumerated to ≤7 pts,
horizontal by the 1324/213/132 self-inverse involution) + cached `domino_growth_constant` for the
`|B_n|~(27/4)^{2n}` order. The one residual is a model-faithfulness judgment (the in-script grid
family IS BBEPP's `P_k`) — the same accepted standard as `insertion_encoding_edge_rule_Av1324`.
NOT a record-break: 81/8 is BBEPP Thm 5.1's own value, below the record 10.271 (its Thm 7.1
refinement). A fully verified
(non-cited) backstop this run is `gr(Av(1324)) ≥ 8887516/1428099 = 6.223319` from the sound
bounded-state insertion automaton `A_10` with an exact-rational Collatz–Wielandt certificate.

## Progress log
- R4: `staircase-containment-lift` — held LEVEL upgrade `10.125*` → `10.125` (fully verified).
  The R3 trap is fixed: the REDUCTION is now a deterministic, complete order-constraint
  enumeration on the real staircase grid order (col_block(m)=⌈m/2⌉, row_block(m)=⌈(m+1)/2⌉),
  window-robust (maxspan=1 holds at window 12), proving every 1324 is confined to two consecutive
  cells — NOT the R3 column-separated stress (which was retired). Independently re-derived by the
  reviewer: a faithfully-overlapping staircase build (random within-block interleave, strict
  between-block separation) yields ~1.0×10⁵ actual 1324 occurrences, every one of span ≤ 1.
  CROSS-CELL reproduced: both vertical between-components sub-cases (conn lower/upper) avoid 1324
  on the complete finite base (reviewer extended to ≤7 pts, 0 violations) + closure under induced
  subperms; horizontal cases by the 1324/213/132 self-inverse involution (all three verified
  self-inverse; 1324-containment verified preserved under inverse). LEMMA DOMINO + H-T (cached
  gr(D)=27/4) unchanged. Containment now reproduced in-script (not a bare citation); the residual
  is the model-faithfulness judgment, accepted at the `insertion_encoding_edge_rule_Av1324`
  standard. Cache lemma `staircase_domino_containment_Av1324` ADMITTED (keyed to the in-script
  abstract grid family; P_k an instance per the BBEPP digest). NOT a record-break: 10.125 < 10.271.
  `tromino-catalan-cell-lower` — honest diagnostic, no bound claimed; sharpened the record hole H1.
  Reproduced: exact-rational gap of the best certified-sound concrete block (2-cell domino 27/4) to
  the target = 6876/1000 − 27/4 = 63/500 = 0.126 (+1.867%), pure Fraction; teeth verified (real-
  overlap 3-cell window at n=6 both contains 1324 (207) and avoids it (513)). H-CNT (BBEPP's named
  open tromino-enumeration problem) stays open; top-level raises NotImplementedError, no false record.
- R3: `tromino-richer-cell-lower` — VERIFIED the general BBEPP Thm-5.1 staircase-product
  closed form `g(g_blk,d,e,f)=exp([2d·log g_blk + log H(2e-f,e) + 2 log H(d+f,d)]/(2d+e))`,
  re-derived from the construction's exponent bookkeeping (k dominoes ×2 cells ×d·k pts + k
  connecting cells ×e·k pts, N=(2d+e)k²) — NOT a re-scaling of 81/8 — reproducing 81/8 EXACTLY
  at (27/4,14,8,7) (`g^36==(81/8)^36` in `Fraction`). VERIFIED exact-rational threshold: a block
  with per-block-point growth `g_blk = 6876/1000 = 6.876` clears the record (`g^36 > (10271/1000)^36`,
  exact). VERIFIED two-cell wall: every domino caps at gr=27/4 (Prop 3.6), so the unbalanced-2-cell
  candidate is refuted — a record-beating block needs ≥3 cells (H1, BBEPP's open tromino route, stays
  open). No new bound: this is a conditional lever, held unchanged.
  `staircase-containment-lift` — the `*`→verified lift was NOT earned and held stays `10.125*`:
  LEMMA DOMINO (one orientation-A 2-cell block avoids 1324) is sound and faithful (closure under
  induced subperms + complete ≤6-pt base, corroborated at sizes 7–8), but LEMMA REDUCTION's stress
  models a column-separated SKEW SUM (its `|noise|<0.5` band makes adjacent cells column-disjoint, so
  the test passes vacuously) — it does NOT capture the staircase's adjacent-cell overlap (the
  interleave). In the true overlapping geometry a 1324 CAN span ≥3 cells (independent test: ~1.5×10⁵
  counterexamples), so REDUCTION+DOMINO does not compose to `P_k ⊆ Av(1324)`. The containment is
  still TRUE (it is BBEPP Thm 5.1, peer-reviewed) — which is why `10.125*` remains a valid `*`-minimal
  bound — but it is not established in-script, so the `*` stays. Proposed lemmas
  `staircase_product_growth_formula` and `staircase_domino_containment_Av1324` NOT admitted (see review).
- R2: held floor raised 3.773326 → 6.223319 (fully verified) and → 10.125* (minimally
  verified). (1) `transfer-matrix-lower`: sound bounded-state insertion automaton `A_K`
  exactly counting `B_K ⊆ Av(1324)` (edge rule, bijection, walks==|B_K,n| and walks≤|Av_n|
  all reconfirmed independently); dominant-SCC exact-rational Collatz–Wielandt gives
  `gr ≥ 8887516/1428099 = 6.223319` (K=10) — VERIFIED, unconditional, reproduced. (2)
  `tromino-subclass-lower`: reconstructed BBEPP Thm 5.1 domino-staircase product, exact
  symbolic growth limit `lim_k |P_k|^{1/36k²} = 81/8 = 10.125` reproduced symbolically and
  by hand — MINIMALLY VERIFIED (`*`): containment `P_k ⊆ Av(1324)` and `|B_n|~(27/4)^{2n}`
  cited to BBEPP Thm 5.1, not reproduced. Neither beats the record 10.271 (both below; the
  record IS the BBEPP Thm 7.1 refinement of the 81/8 line). Certified cache lemma
  `insertion_encoding_edge_rule_Av1324` (structural proof, length-independent).
- R1: verified lower bound gr(Av(1324)) ≥ 1886663/500000 = 3.773326 — exact rational
  Collatz–Wielandt certificate on the L=8 skew-sum-closure companion matrix; soundness
  rests on the certified lemma `skew_sum_closure_Av1324` (S_8 ⊆ Av(1324)). Does not beat
  record 10.271. Certified two cache lemmas: `skew_sum_closure_Av1324`,
  `domino_growth_constant` (gr(D)=27/4). Upper-side sketch `decorated-domino-upper`
  refuted its planned pure-word forbidden-factor mechanism (no local forbidden factor of
  length ≤4) — H2 re-points to joint (word,domino) counting; no upper-bound improvement.
