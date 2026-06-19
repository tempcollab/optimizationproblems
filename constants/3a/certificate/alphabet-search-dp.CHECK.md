# Check record — alphabet-search-dp (constant 3a, lower bound)

**Claimed bound (round 3, NEW BEST):** C_3a >= 1.1752717416788478
(vs prior verified held 1.1744750903655619 [R2]; +7.97e-4 · vs record 1.1740744 [G2026]; +1.20e-3)

Construction: GHR2007 single-set lemma at A={0,2,3,4,5,6,7,8,9,10} (omits 1), base b=21,
**d=96, T=184** (c=T/d=1.9167), U = { sum_i a_i 21^i : a_i in A, sum a_i <= 184 }.
(Prior held construction d=84, T=162 still certified by the same script as a second winner.)

**Reproduce (certify from cached exact counts, <2 s):**
```
cd constants/3a/certificate && python3 alphabet-search-dp.py
```
**Reproduce (re-run the full DP and assert cached counts, then certify; ~700 s):**
```
cd constants/3a/certificate && VERIFY_DP=1 python3 alphabet-search-dp.py
```

**Expected tail:**
```
WINNER A=[0, 2, 3, 4, 5, 6, 7, 8, 9, 10] d=88 T=169  certified theta_lb=1.1747643448523182 beats=True  margin=6.899e-04
WINNER A=[0, 2, 3, 4, 5, 6, 7, 8, 9, 10] d=96 T=184  certified theta_lb=1.1752717416788478 beats=True  margin=1.197e-03  <== BEST
CERTIFIED LOWER BOUND on C_3a: 1.1752717416788  (d=96, T=184, A=[0, 2, 3, 4, 5, 6, 7, 8, 9, 10], base=21) > record 1.1740744 [G2026].
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
exact d=96, T=184 literals (BEST, this round):
  |U+U|  = 2354612726795560198637539626081323633677464536763944205611915446610439936255355430057651233079
  |U-U|  = 41657829615040226466508207079583713163528747660407140693727914721760094182467298116869474627721404780883597620670119
  2max(U)+1 = 8571410494579611166108619722960490736204749562145503217128903617006442204626527584995605100800210570065634413170633869420430689
```
DP recompute at d=96,T=184 reproduces |U+U|, |U-U| exactly; q=2·max(U)+1 independently re-derived
via max_U and matches. theta_lb certified with terms=300 (saturated: {300,350,400,500} agree).
```
exact d=88, T=169 literals (second new winner):
  |U+U|  = 37426702858728646432282756452279923211302451814423993558049713846305746450715225147721
  |U-U|  = 8089822321128549482175445108898615340129429952564150606760178195018521495093392976519143508642843850587135
  2max(U)+1 = 226619844173330403699400313808878995189192616963040449480352838082290594716834946150538880875774352576915570878314699
```
```
exact d=84, T=162 literals (prior held bound, still certified):
  |U+U|  = 6097708534951589347439183607038270910158216193597072358058994024712092458076766270
  |U-U|  = 145710369635805984294872090934229656671521875518799257570738793680742528284363557961708618559623567675
  2max(U)+1 = 1165254416489684872554618217361872378435684345652187969599710464819025051454571621932090673372945921527696090485
```
```
exact d=84, T=164 literals (second winner):
  |U+U|  = 16777722616407479187147504571629992614689318525575983076108586880851554003065008694
  |U-U|  = 395408260987655412181207585916583184388551911069273615252881628449017521960376630791972773544057686111
  2max(U)+1 = 1165254416489684872554773367704321832783618869900619554858691396740867998558326013724405243400764220064810193449
```
