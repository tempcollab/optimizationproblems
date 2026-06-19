# C_3a — current verified bottom line

## Status
improved

## Bounds
table: 1.1740744476935212 (verified record [G2026], PR #71, base-21 d=80 T=150) · held: 5877/5000 = 1.1754 (exactly certified, R18; true value 1.1754209217852493…)

## Progress log
- R16: pivot to C_3a; digit-DP exact-count engine + record baseline (PR #71 integers reproduced bit-for-bit) — machinery, no beat.
- R18: VERIFIED STRICT BEAT of the lower-bound record. Base-21 digit construction, A={0,2,3,4,5,6,7,8,9,10}, B=21, d=100, T=187 (carry-free, B=21>2·max(A)=20). Exact integer counts |U+U| (97 digits), |U−U| (120 digits), max(U) (132 digits) ALL re-derived bit-for-bit by an independent reviewer DP (validated against brute-force enumeration of U as integer sets), and the strict beat `value_record < 5877/5000 ≤ value_new` decided by pure big-integer power inequalities (Nm^q ≥ Np^q·(2M+1)^p; record cell Nm^q < Np^q·(2M+1)^p), no float. Margin over record ≈ 1.35e-3. Held lower bound: C_3a ≥ 5877/5000 = 1.1754. Cert: constants/3a/certificate/beat_largerd/ (verify_beat.py exit 0, CERTIFICATE OK). Secondary cell d=100,T=180 ≥ 2937/2500 = 1.1748. GHR digit-set ceiling is 1.25 (headroom remains). Numerical certificate (not yet Lean); the small-q wedge (q=5000) makes a Lean integer-power theorem the natural next sub-goal.
