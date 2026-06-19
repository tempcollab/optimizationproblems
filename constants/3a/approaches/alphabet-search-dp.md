# alphabet-search-dp — re-optimize the non-uniform digit alphabet (PRIMARY)

**Direction:** lower bound on C_3a. **Record to beat:** 1.1740744 [G2026].

## Strategy
Griego beat Zheng's uniform-digit asymptotic limit (1.173077) by a *single* alphabet tweak:
`A = {0,2,3,4,5,6,7,8,9,10}` (omits 1), base 21, `d=80`, `T=150` → 1.17407444769. He reported
one alphabet. The alphabet/cap/length space is large and barely explored. Re-optimize
`(A, d, T)` with the **same validated exact-integer DP**, then certify the winner with a
directed-rounded rational log bound.

## Engine (validated, reusable)
`certificate/ghr_dp.py` — exact `|U+U|`, `|U-U|`, `max(U)` for any `(A,d,T)`, carry-free base
`b = 2 max(A)+1`. **Reproduces Griego's record exactly** (`|U+U|`, `|U-U|`, θ all match PR #71;
`python ghr_dp.py` asserts it). Small cases were brute-force checked. This is the shared
certificate template — every Python sketch imports it.

- sumset DP state = frozenset of reachable `(sum a_i, sum a'_i)` pairs (count distinct
  feasible output digit-strings); state count stabilizes (~few hundred), scales to d=80.
- diffset DP state = `(left total, right total)` ≤ `T²`, using the cheapest representative per
  difference digit (simultaneously minimal → feasibility = cheapest-rep totals ≤ T).

## Holes
- **H1 SEARCH (load-bearing):** find `(A,d,T)` with float-θ strictly above the record. Cheap DP
  per point; the hard part is the right neighborhood. Moves: omit different/multiple small
  digits; vary max digit M (→ base 2M+1) and `T/d` around 150/80; longer d at matched `T/d`.
- **H2 EXACT CONFIRM:** exact integer recomputation of the three counts for the winner.
- **H3 CERTIFY:** rational directed-rounded bound `log(d/s) − 0.1740744·log q > 0` with a
  re-runnable margin (atanh series + explicit remainder, as in Griego's certificate).

## Hard step
Finding a parameter point that *actually* beats 1.1740744 (the record already sits only ~7e-5
above the uniform limit, so the win is small) **and** certifying it exactly (not a float claim).

## Certify
Python integer DP + rational log bound (directed-rounded). Also Lean-fittable — the winning
counts feed `ghr-lemma-lean`.
