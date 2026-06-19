# Check — griego-ntt-push (C_3a LOWER bound, R5 push to m=140)

## Reproduce — each command is a SEPARATE short PRINTING step (watchdog-safe; R6-re-run)

CHEAP REVIEWER CHECK (the certificate itself, ~2 s, no DP recompute):
```
# tight integer-inequality cert from the committed exact counts (PASS 11771 / FAIL 11772):
python3 -u constants/3a/certificate/griego-ntt-push.py --certify-from-scan 140 265   # ~2s, EXIT 0
# fallback point (PASS 11768 / FAIL 11769):
python3 -u constants/3a/certificate/griego-ntt-push.py --certify-from-scan 130 247   # ~2s, EXIT 0
```

FULL INDEPENDENT VERIFICATION (each its own short call, all print incrementally):
```
# the mandatory oracle gate (3-way + 2-way exact agreement), ~2 min, streamed per case:
python3 -u constants/3a/certificate/griego-ntt-push.py --gate                  # EXIT 0

# independent from-scratch recompute of s,d,M (checkpointed per quantity), ~95 s for m=140:
python3 -u constants/3a/certificate/griego-ntt-push.py --point 140 265         # EXIT 0
```
NEVER run bare `main()` / a single `--gate`+`--point`+`--certify` block silently — that ~4-min
silent stretch is what cost R5. Run the steps separately as above. All print per-quantity
incrementally (no single silent >~3-min run); every step EXIT 0.

### R6 re-verification (this round)
- `--gate`: 20-case agreement PASS, EXIT 0.
- `--point 140 265`: s=136d (64s), d=169d (29s), θ=1.1771373652; the recomputed s, d, AND M
  match the committed `scan-mT-results.txt` row **byte-for-byte** (digit-for-digit big-int
  comparison). Third independent reproduction of the m=140 counts.
- `--certify-from-scan 140 265`: k=11771 PASS, k=11772 FAIL (tight), EXIT 0, ~2 s.
- `--certify-from-scan 130 247`: k=11768 PASS, k=11769 FAIL, EXIT 0, ~2 s.

## What the run proves (R5 — push m=110 → m=140; held 1.176 → 1.1771)

### 1. Mandatory oracle gate (`--gate`)
Three independent counters of `|U+U|` are cross-checked EXACTLY:
- `ghr_bruteforce` — full enumeration of `A^m` (ground truth, small m).
- `indep_sumset` — an INDEPENDENT set-based Minkowski DP (frozenset states, explicit
  Python set sums, integer-comparison window; shares NO code with the bitmask oracle).
- `fast_sumset_count` = the certified shift-OR bitmask DP (`count_sumset` from
  griego-family-larger-mT, the load-bearing engine used at large m).

Result (all OK):
- 3-way `brute == indep == oracle` on **15** cases — Griego non-contiguous {0,2,…,10}
  (incl. T-clamp binding: m=4,T=9; m=5,T=22; m=6,T=15) AND a contiguous control {0,1,…,5}.
- 2-way `indep == oracle` on **5** larger cases (m=6,T=18; m=4,T=40; m=7,T=22; m=8,T=18;
  m=9,T=20) where brute's O(|U|²) sumset is infeasible but the two DPs still agree.

This satisfies the Rule-R3 gate: a fast-but-wrong DP would diverge from the independent
set-DP and/or brute force; it does not. Large-m counts are trustworthy.

### 2. New exact points (`--point`, exact column DPs, re-derived from scratch)
- **m=130, T=247:** s=|U+U| (127 digits), d=|U−U| (157 digits), M=max U (172 digits);
  float θ ≈ 1.1768118909.
- **m=140, T=265 (REGISTERED BEST):** s (136 digits, head `88785247661758800689`),
  d (169 digits, head `54747299867053367517`), M (185 digits, head `64516569533889487833`);
  float θ ≈ 1.1771373652.

The sum-set count is the (Σv, reachable-Σx-bitmask) shift-OR DP with the dynamic low-clamp
(`mask>>lo<<lo`, lo=max(0,Σv−T)); it is EXACT — it IS the reachable set, no modulus/CRT/float.
The (Σv,R) state count SATURATES at fixed T (~37k at m=130, ~? at m=140), so cost is ~linear
in m; m=140 runs in ~110 s, comfortably inside the watchdog. (The R4 "m=130 wall" was a
too-large-T un-checkpointed scout, not a true asymptotic wall.)

### 3. Load-bearing certificate (pure big-integer, NO float), with negative control
For `q=2M+1`, the test `d^10000 > s^10000 · q^(k−10000)` ⟺ θ > k/10000, at m=140,T=265:
- `k=11770` (θ > 1.1770): **PASS = True**
- `k=11771` (θ > 1.1771): **PASS = True**  → held candidate = 1.1771
- `k=11772` (θ > 1.1772): **FAIL = False** → 1.1771 is the LARGEST k/10000 that certifies
  (tight at denominator 10000).
A redundant 400-bit directed-rounded mpmath log test confirms θ > 1.1740744 (external record).
The integer inequality was also re-verified with explicit big-int arithmetic outside the module.

## Claimed bound
C_3a ≥ θ(m=140,T=265) > 11771/10000 = **1.1771** > 1.176 (previous held) > 1.1740744 (record).
Same family/construction and same GHR2007 read-off as the held 1.176; the only change is a new
larger (m,T) exact data point. Valid (b=21 > 2·max(A)=20 ⇒ injective, carry-free).

## Scan audit trail
`constants/3a/certificate/scan-mT-results.txt` — the two new R5 points (m=130,T=247 and
m=140,T=265) appended with exact s, d, M, θ and the tight-cert annotation.
```
build target / load-bearing check: python3 constants/3a/certificate/griego-ntt-push.py
                                    (gate PASS + tight cert C_3a > 11771/10000 = 1.1771)
```
