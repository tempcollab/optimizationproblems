# Check record — sketch `noncontig-alphabet-sweep` (C_3a lower bound)

**Run / reproduce:**
```
python3 constants/3a/certificate/noncontig-alphabet-sweep.py
```

**What it asserts (load-bearing):**
- `self_test()` — the exact column-DP (`count_sum`, `count_diff`, `maxU`) equals brute-force
  enumeration on 10 cases (contiguous and non-contiguous alphabets). `assert` fails the run if
  the DP is wrong. This is the validated exact oracle (closes hole `exact-sumdiff-dp`).
- Reproduces the explorer's sanity numbers EXACTLY: `(m=3,T=8)→θ≈1.1062345`,
  `(m=4,T=10)→θ≈1.1184785`.
- Alphabet sweep (closes hole `search-alphabet`, NEGATIVE result): no alphabet in the
  single/double-digit-drop + top-B family beats Griego's `{0,2,…,10}` base 21. B=9 vs B=10 each
  T-optimized → B=10 (Griego) wins.

**Load-bearing exact certification (Lean `native_decide` shape, not floating point):**
`certify_target(s,d,q,P,Q)` decides `θ = 1 + log(d/s)/log q > P/Q` via the pure big-integer
inequality `d^Q > s^Q · q^(P−Q)` (with small-denominator `P/Q`). Verified in-script to agree
with the float comparison above and below the bar.

**Outcome:** NOT a record-break. The alphabet lever is saturated at Griego's choice; this
sketch refutes "a different alphabet beats 1.1740744". Best θ from any swept alphabet at the
moderate `m` used is Griego's own `{0,2,…,10}` at θ≈1.1652 (m=30,T=60), below 1.1740744.

**Known limitation:** the bigint pair-set DP is too slow to reproduce the exact m=80,T=150
Griego numbers (sum DP ~37 min, 13476 states, |U+U|~10^76; diff DP did not finish in ~50 min).
The conclusion does not depend on it — alphabet ranking is read off at m≤30, and the DP is
validated by `self_test()` on small cases.
