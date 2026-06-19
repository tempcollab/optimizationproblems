# Check record — alphabet-search-dp (constant 3a, lower bound)

**Claimed bound:** C_3a >= 1.1744750903655619  (vs verified record 1.1740744 [G2026]; +4.01e-4)

Construction: GHR2007 single-set lemma at A={0,2,3,4,5,6,7,8,9,10} (omits 1), base b=21,
**d=84, T=162**, U = { sum_i a_i 21^i : a_i in A, sum a_i <= 162 }.

**Reproduce (certify from cached exact counts, <1 s):**
```
cd constants/3a/certificate && python3 alphabet-search-dp.py
```
**Reproduce (re-run the ~230 s DP and assert cached counts, then certify):**
```
cd constants/3a/certificate && VERIFY_DP=1 python3 alphabet-search-dp.py
```

**Expected tail:**
```
WINNER A=[0, 2, 3, 4, 5, 6, 7, 8, 9, 10] d=84 T=162  certified theta_lb=1.1744750903655619 beats=True  margin=4.007e-04  <== BEST
WINNER A=[0, 2, 3, 4, 5, 6, 7, 8, 9, 10] d=84 T=164  certified theta_lb=1.1744209689691891 beats=True  margin=3.466e-04
CERTIFIED LOWER BOUND on C_3a: 1.1744750903656  (d=84, T=162, A=[0, 2, 3, 4, 5, 6, 7, 8, 9, 10], base=21) > record 1.1740744 [G2026].
```

**Load-bearing step:** GHR2007 single-set lemma with exact-integer DP counts (|U+U|, |U-U|,
max U) and a directed-rounded RATIONAL lower bound on
`theta = 1 + log(|U-U|/|U+U|)/log(2 max U + 1)`.

The log bound uses the **scaled base-2 reduction** `log N = (N.bit_length()-1)*log 2 + log(N/2^k)`
with `N/2^k in [1,2)`, so the atanh series runs only where it converges (z <= 1/3) — replacing
the shared `certify_theta_lb`, which fed q~21^84 and diff/s~1e18 into the series at z~1 and
returned garbage. Numerator lower-bounded, denominator upper-bounded => certified theta is a true
LOWER bound on theta. No hole on the path to the bound.

```
exact d=84, T=162 literals:
  |U+U|  = 6097708534951589347439183607038270910158216193597072358058994024712092458076766270
  |U-U|  = 145710369635805984294872090934229656671521875518799257570738793680742528284363557961708618559623567675
  2max(U)+1 = 1165254416489684872554618217361872378435684345652187969599710464819025051454571621932090673372945921527696090485
```
DP recompute at d=84,T=162 (VERIFY_DP=1) matches these literals exactly (confirmed this round).
```
exact d=84, T=164 literals (second winner):
  |U+U|  = 16777722616407479187147504571629992614689318525575983076108586880851554003065008694
  |U-U|  = 395408260987655412181207585916583184388551911069273615252881628449017521960376630791972773544057686111
  2max(U)+1 = 1165254416489684872554773367704321832783618869900619554858691396740867998558326013724405243400764220064810193449
```
