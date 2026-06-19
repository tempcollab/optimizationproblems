# Current bottom line — 30a, gr(Av(1324))

## Status
none

## Bounds   table: 10.271 · held: 10.125*

(Bounds line above is the lower side — the run's verified advance; eval reads it.)
Upper side — table: 13.5 · held: 13.5 (record reproduced, not beaten).
The canonical rigorous record remains `10.271 ≤ gr(Av(1324)) ≤ 13.5` (BBEPP2017).
`held: 10.125*` (= 81/8) on the lower side is minimally verified (`*`): the count and the
exact symbolic growth limit `lim_k |P_k|^{1/36k²} = 81/8` are reproduced (symbolically and
by hand), but the subclass containment `P_k ⊆ Av(1324)` and the `|B_n| ~ (27/4)^{2n}`
asymptotic order rest on the **cited** BBEPP Thm 5.1 (peer-reviewed), not reproduced
in-script. Still below the record 10.271 (BBEPP's own Thm 7.1 refinement). A fully verified
(non-cited) backstop this run is `gr(Av(1324)) ≥ 8887516/1428099 = 6.223319` from the sound
bounded-state insertion automaton `A_10` with an exact-rational Collatz–Wielandt certificate.

## Progress log
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
