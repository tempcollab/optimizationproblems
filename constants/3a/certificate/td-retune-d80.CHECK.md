# Check record — td-retune-d80 (constant 3a, lower bound)

**Claimed bound:** C_3a >= 1.174171353998482  (vs verified record 1.1740744 [G2026]; +9.70e-5)

**Reproduce (full, ~170 s):**
```
cd constants/3a/certificate && python3 td-retune-d80.py
```
**Reproduce (certify from cached exact counts, seconds):**
```
cd constants/3a/certificate && python3 td-retune-d80.py --replay
```
**Re-run the T-scan (one point at a time, ~170 s/pt):**
```
cd constants/3a/certificate && python3 td-retune-d80.py --scan
```

**Expected tail:**
```
[H3] CERTIFIED theta_lb >= 1.174171353998482  (exact rational, shown round-DOWN to 15 places)
[H3] record = 1.1740744; beats strictly = True
[H3] rational margin over record = 9.695e-05
[OK] verified lower bound on C_3a: 1.1741713539984822 > 1.1740744
```

**Load-bearing step:** GHR2007 single-set lemma at A={0,2..10}, base b=21, d=80, **T=154**, with
exact-integer DP counts (|U+U|, |U-U|, max U) and a directed-rounded RATIONAL lower bound on
`theta = 1 + log(|U-U|/|U+U|)/log(2 max U + 1)`.  The log bound uses the base-b reduction
`log N = floor(log_b N)*log(b) + log(residual in [1,b))` so the atanh series runs only where it
converges (z <= 20/22) — replacing the shared `certify_theta_lb` which fed q~21^80 and diff/s~1e18
into the series at z~1 and silently returned theta_lb~1.0.  No hole on the path to the bound.
```
exact T=154 literals:
  |U+U|  = 597130362133498688344900538759091221981599964605490705452812019502078419618406
  |U-U|  = 1583022697814754823730226433460816281662151877595631959725969360255416773109712840757177539870935
  max(U) = 2995805288150731620427416034073013045407712819639364547243511761614441608214402813704058986719974740854874
```
