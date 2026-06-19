# Current bottom line — 30a, gr(Av(1324))

## Status
none

## Bounds   table: 10.271 · held: 3.773326

(Bounds line above is the lower side — the run's verified advance; eval reads it.)
Upper side — table: 13.5 · held: 13.5 (record reproduced, not beaten).
The canonical rigorous record remains `10.271 ≤ gr(Av(1324)) ≤ 13.5` (BBEPP2017).
`held: 3.773326` on the lower side is the run's verified bottom line on a subclass
`S_8 ⊆ Av(1324)` — true and reproducible, but well below the record (no record change).

## Progress log
- R1: verified lower bound gr(Av(1324)) ≥ 1886663/500000 = 3.773326 — exact rational
  Collatz–Wielandt certificate on the L=8 skew-sum-closure companion matrix; soundness
  rests on the certified lemma `skew_sum_closure_Av1324` (S_8 ⊆ Av(1324)). Does not beat
  record 10.271. Certified two cache lemmas: `skew_sum_closure_Av1324`,
  `domino_growth_constant` (gr(D)=27/4). Upper-side sketch `decorated-domino-upper`
  refuted its planned pure-word forbidden-factor mechanism (no local forbidden factor of
  length ≤4) — H2 re-points to joint (word,domino) counting; no upper-bound improvement.
