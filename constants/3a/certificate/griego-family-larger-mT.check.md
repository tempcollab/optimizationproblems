# Check — griego-family-larger-mT (C_3a LOWER bound)

## Reproduce
```
python3 constants/3a/certificate/griego-family-larger-mT.py
```
Runtime ~2 min (self-test brute force + one m=110 exact-integer cert; prints per-step incrementally,
well under the 5-min watchdog). EXIT 0.

## What the run proves (R4 TIGHTEN — held 1.1741 → 1.176)
1. `[self-test]` — the exact column DP (`count_sumset`, `count_diffset`, `max_U`) matches a
   brute-force enumeration on 8 small `(m,T)` cases for `(s=|U+U|, d=|U-U|, M=max U)`. Establishes
   DP correctness. (DP also certified as lemma `exact-sumdiff-dp`, R3.)
2. **Re-derives (s,d,M) at m=110,T=210 FROM SCRATCH** (recompute, no trusted external value), printing
   digit counts per step:
   - `s=|U+U|`: 107 digits, leading `927052801501495…`, trailing `…95284`
   - `d=|U−U|`: 133 digits, leading `368199722009600…`, trailing `…22441`
   - `M=max(U)`: 146 digits, leading `139024846765954…`, trailing `…60010`
   - float θ ≈ 1.1760055928 (consistency only; NOT load-bearing).
3. **Load-bearing certificate (pure big-integer, NO float), with explicit negative control:**
   for `q=2M+1`, the test `d^10000 > s^10000 · q^(k-10000)` ⟺ θ > k/10000:
   - `k=11760` (θ > 1.176): **PASS = True**  → held = 1.176
   - `k=11761` (θ > 1.1761): **FAIL = False** → 1.176 is the LARGEST k/10000 that certifies (tight
     at denominator 10000).
   Printed lines `k=11760 ... PASS = True` and `k=11761 ... FAIL = False ... tightness OK = True`.
   The script hard-asserts both, so it exits nonzero if either breaks. A redundant 400-bit
   directed-rounded mpmath log test confirms θ > 1.1740744.

## Claimed bound
C_3a ≥ θ(m=110,T=210) > 11760/10000 = 1.176 > 1.1740744 (record).  Construction: Griego's exact family
A={0,2,3,...,10}, base b=21, U = { Σ x_i b^i : x∈A^m, Σx_i ≤ T }, with the GHR2007 lemma
C_3a ≥ 1 + log(|U−U|/|U+U|)/log(2 max U + 1). Valid (b=21 > 2·max(A)=20 ⇒ injective, carry-free).

## Lean-fit note
The load-bearing step is a single integer inequality `d^10000 > s^10000 * q^1760` on explicit
constants — `native_decide`-shaped. Porting it to a Lake project under constants/3a/lean/ is a
follow-on (the sibling `lean-native-decide-smallmt` sketch does this at a smaller operand point);
the bound here is already established in exact Python big-int.

## Scan audit trail
`constants/3a/certificate/scan-mT-results.txt` — every scanned `(m,T)` point with exact s, d, M,
θ, and beat flag (per-point scanner `scan_mt.py`).
