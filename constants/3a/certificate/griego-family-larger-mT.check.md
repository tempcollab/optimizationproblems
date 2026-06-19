# Check — griego-family-larger-mT (C_3a LOWER bound)

## Reproduce
```
python3 constants/3a/certificate/griego-family-larger-mT.py
```
Runtime ~2-3 min (dominated by the self-test brute force and the m=110 exact-integer cert).

## What the run proves
1. `[self-test]` — the exact column DP (`count_sumset`, `count_diffset`, `max_U`) matches a
   brute-force enumeration on 8 small `(m,T)` cases for `(s=|U+U|, d=|U-U|, M=max U)`. Establishes
   DP correctness.
2. Reproduces Griego's record point: `m=80, T=150` gives θ = 1.1740744477 (= the record 1.1740744).
3. The family climbs strictly past the record:
   - m=80,  T=154: θ ≈ 1.1741714
   - m=100, T=190: θ ≈ 1.1754955
   - m=110, T=210: θ ≈ 1.1760056   (best verified point)
4. **Load-bearing certificate (pure big-integer, NO float):** for the best point,
   `d^10000 > s^10000 · (2M+1)^1741`  ⟺  θ > 11741/10000 = 1.1741 ≥ TARGET 1.1740744.
   Printed line `EXACT integer certificate ... : True`. A redundant 400-bit directed-rounded
   mpmath log test confirms θ > 1.1740744.

## Claimed bound
C_3a ≥ θ(m=110,T=210) > 1.1741 > 1.1740744 (record).  Construction: Griego's exact family
A={0,2,3,...,10}, base b=21, U = { Σ x_i b^i : x∈A^m, Σx_i ≤ T }, with the GHR2007 lemma
C_3a ≥ 1 + log(|U−U|/|U+U|)/log(2 max U + 1). Valid (b=21 > 2·max(A)=20 ⇒ injective, carry-free).

## Lean-fit note
The load-bearing step is a single integer inequality `d^10000 > s^10000 * q^1741` on explicit
constants — `native_decide`-shaped. Porting it to a Lake project under constants/3a/lean/ is a
follow-on (not done this round); the bound is already established in exact Python big-int.

## Scan audit trail
`constants/3a/certificate/scan-mT-results.txt` — every scanned `(m,T)` point with exact s, d, M,
θ, and beat flag (per-point scanner `scan_mt.py`).
