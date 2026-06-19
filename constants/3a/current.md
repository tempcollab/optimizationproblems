# 3a — tracking file (reviewer-owned)

## Status
improved

## Bounds            table: 1.1740744 · held: 1.1744750903655619
Record to beat: 1.1740744 [G2026] (base-21 digit construction). Held: verified R2 by alphabet-search-dp (d=84, T=162, A={0,2..10}, base 21).

## Progress log
- R2: VERIFIED lower bound C_3a >= 1.1744750903655619 (alphabet-search-dp, d=84, T=162, A={0,2..10}, base 21). Re-ran full exact DP from scratch (|U+U|, |U-U|, q match cached literals), re-derived the scaled-base-2 atanh directed-rounded log bound (genuine rational lower bound, confirmed <= true theta via mpmath @150dps), GHR2007 single-set lemma applies (0 in U; technical constraint |U-U| <= 2max(U)+1 holds). Strictly beats record 1.1740744 by +4.01e-4. Sibling td-retune-d80 also verified at 1.174171353998482 (+9.7e-5), superseded by this margin.
