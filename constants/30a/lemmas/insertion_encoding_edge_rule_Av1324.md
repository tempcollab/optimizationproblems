# Lemma `insertion_encoding_edge_rule_Av1324` — certified R2

## Statement

Let `p` be a permutation that avoids 1324, and let `pos ∈ {0,…,len(p)}`. Form `p'` by
inserting a new **global maximum** `M` (= a value strictly larger than every entry of `p`)
at position `pos`, i.e. `p' = p[:pos] ++ [M] ++ p[pos:]`. Then

> `p'` contains the pattern 1324  ⇔  the left prefix `p[:pos]` contains the pattern 132.

Equivalently: the allowed insertion positions of `p` (those keeping `p'` a 1324-avoider)
are exactly `pos ∈ {0,…,t}` where `t` is the length of the longest 132-avoiding prefix of `p`.

## Proof (structural — holds for all lengths, not merely the exhaustive range)

`p` avoids 1324, so any 1324 occurrence in `p'` must use the only new point, `M`.
`M` is the global maximum, hence in a 1324 = (1,3,2,4) it can only play the largest value,
the `4`, which sits at the **rightmost** of the four positions. The other three points
(playing 1,3,2) therefore lie strictly to the left of `M` in `p'`, i.e. among `p[:pos]`
(inserting `M` at `pos` leaves the entries before it unchanged and in order). Those three
form a 132 pattern. Conversely, if `p[:pos]` contains a 132, appending the larger value `M`
to its right (the `4`) completes a 1324 in `p'`. Hence `p'` contains 1324 ⇔ `p[:pos]`
contains 132. ∎

## Certification

- Reviewer (R2) re-derived the structural proof from scratch — it is airtight and
  length-independent (the new occurrence must use `M`; `M` is forced to be the `4`).
- Independently re-verified exhaustively with a from-scratch reimplementation of both
  pattern checkers: for every 1324-avoider `p` of length ≤ 7 and every `pos`,
  `contains_1324(insert_max(p,pos)) == contains_132(p[:pos])`. Matches the builder's
  in-script `prove_edge_rule` (checked to length 8). Source:
  `constants/30a/certificate/transfer-matrix-lower.py` (`prove_edge_rule`).
- Statement is correct and no stronger than proved.

## Used by

`transfer-matrix-lower` (insertion-encoding automaton `A_K` soundness, E2), and any future
insertion-encoding / walk-graph construction on `Av(1324)` (e.g. `conjecture8-diagonal-lower`).
