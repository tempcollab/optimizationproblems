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
