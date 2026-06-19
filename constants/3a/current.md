# 3a — tracking file (reviewer-owned)

## Status
improved

## Bounds            table: 1.1740744 · held: 1.1752717416788478
Record to beat: 1.1740744 [G2026] (base-21 digit construction). Held: verified R3 by alphabet-search-dp (d=96, T=184, A={0,2..10}, base 21).

## Progress log
- R2: VERIFIED lower bound C_3a >= 1.1744750903655619 (alphabet-search-dp, d=84, T=162, A={0,2..10}, base 21). Re-ran full exact DP from scratch (|U+U|, |U-U|, q match cached literals), re-derived the scaled-base-2 atanh directed-rounded log bound (genuine rational lower bound, confirmed <= true theta via mpmath @150dps), GHR2007 single-set lemma applies (0 in U; technical constraint |U-U| <= 2max(U)+1 holds). Strictly beats record 1.1740744 by +4.01e-4. Sibling td-retune-d80 also verified at 1.174171353998482 (+9.7e-5), superseded by this margin.
- R3: VERIFIED lower bound C_3a >= 1.1752717416788478 (alphabet-search-dp, d=96, T=184, A={0,2..10}, base 21, c=1.9167). Independent fresh exact DP at d=96,T=184 reproduces |U+U|, |U-U|, q exactly (sumset 397s, diffset 1.6s); DP carry-free/cap logic re-cross-checked vs brute force incl carry-stress cases. Re-derived the certified rational log bound: mpmath@200dps true theta=1.175271741678847842..., certified Fraction 1.1752717416788478 <= true theta (lb/ub bracket s,diff,q confirmed). GHR2007 constraint |U-U|<=2max(U)+1 holds (ratio 4.86e-12), 0 in U. Strictly beats prior held 1.1744750903655619 by +7.97e-4. (Lean line ghr-lemma-lean machine-checked the d=84 exponent inequality >1.1740744, axiom-clean, but does not raise the numerical held — GHR bridge not yet formalized.)
