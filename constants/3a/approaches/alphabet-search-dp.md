# alphabet-search-dp — longer-d, retuned-T/d homogeneous construction (PRIMARY)

**Direction:** lower bound on C_3a. **Record to beat:** 1.1740744 [G2026].
**CLAIMED this round (round 2, certified hole-free):** **C_3a >= 1.1744750903655619**
(d=84, T=162, A={0,2,3,4,5,6,7,8,9,10}, base 21). Margin over record **+4.01e-4**.
*(Claim, not yet reviewer-verified — but the script reproduces it end-to-end; see CHECK below.)*

## Strategy (re-scoped round 2)
The homogeneous record alphabet {0,2..10} is SATURATED (explorer Finding A). So this sketch
drops alphabet edits and pushes LENGTH at a RE-TUNED cap ratio. theta rises with d toward the
asymptote, and the optimal T/d sits ABOVE Griego's 1.875. The length gain compounds with the
T/d gain. Same exact-integer DP engine (`ghr_dp.py`), GHR2007 single-set lemma, certified with
a directed-rounded RATIONAL log bound.

## What I closed this round
- **H1 SEARCH — CLOSED.** Ran the longer-d scan with the fast engine, chunked one point at a
  time (diffset ~1 s, sumset bitmask ~210-235 s/pt at d=84). At d=84 the optimum is interior:
  - T=160 (c=1.905) -> float theta 1.1744734004
  - **T=162 (c=1.929) -> float theta 1.1744750903655619  (BEST)**
  - T=164 (c=1.952) -> float theta 1.1744209690
  - T=166 (c=1.976) -> float theta 1.1743111592
  All four strictly beat the record. The d=40 probe (peak near c=1.95-1.975) and the d=84 scan
  (peak near c=1.92-1.93) confirm the optimum c drifts down slightly as d grows but stays above
  Griego's 1.875. The longer d is the dominant lever: d=84 gives +4.01e-4 vs the d=80 retune's
  +9.7e-5.
- **H2 EXACT CONFIRM — CLOSED.** Exact integer counts for the winners cached in `WINNERS`
  (script `alphabet-search-dp.py`). A fresh DP recompute at d=84,T=162 (`VERIFY_DP=1`) matches
  the cached `|U+U|`, `|U-U|`, `2 max U + 1` exactly.
- **H3 CERTIFY — CLOSED, and the LOAD-BEARING FLAW FIXED.** The shared per-position
  `certify_theta_lb` ran the atanh log series directly on q ~ 21^84 (and on diff/s ~ 1e18) where
  z=(x-1)/(x+1) ~ 1, so it needed ~1e106 terms and returned garbage. Replaced with a
  **scaled base-2 expansion** (Griego's base-b template at b=2): for any integer N >= 1,
  `log N = k*log 2 + log(N / 2^k)` with `k = N.bit_length()-1` and `N/2^k in [1,2)`, so the
  atanh argument has z <= 1/3 and converges in a few hundred terms. log 2 is bounded once at
  z=1/3. Numerator `log(diff/s)` lower-bounded (`logN_lb(diff) - logN_ub(s)`), denominator
  `log q` upper-bounded (`logN_ub(q)`), so `theta_lb = 1 + num_lb/den_ub <= theta` — a true
  directed-rounded LOWER bound. Validated on the record (matches float to ~1e-12, beats=True)
  and on adversarial N up to 1e111 (log bounds bracket the true value, widths ~1e-287).

## Holes remaining
- **None on the path to the claimed bound.** The bound 1.1744750903655619 is hole-free:
  exact-integer DP + directed-rounded rational log bound, fully re-runnable.
- **Open (optional, not on the path):** d in {88, 96} not yet scanned — likely a further small
  gain (the asymptote is still above), but each d=96 point is more expensive (~T^2; T~185).
  Left as a marked extension in `search_for_better()` (not a hole blocking the bound).

## Verify
```
cd constants/3a/certificate && python3 alphabet-search-dp.py          # <1 s, cached literals
cd constants/3a/certificate && VERIFY_DP=1 python3 alphabet-search-dp.py  # ~230 s, re-runs DP
```
Expected best line: `... d=84 T=162  certified theta_lb=1.1744750903655619 beats=True ...`

## Promotable lemmas
- **`logN_lb` / `logN_ub` (scaled base-2 rational log bounds)** — proved green in
  `certificate/alphabet-search-dp.py` (functions `_log_small_lb/_ub`, `_floor_log2`, `logN_lb`,
  `logN_ub`, `certify_theta_lb_scaled`). General-purpose: directed-rounded rational LOWER/UPPER
  bounds on `log N` for any integer N >= 1, valid at any scale (atanh runs only at z <= 1/3).
  This is the correct replacement for the broken shared `certify_theta_lb` and is imported-worthy
  by every Python sketch (td-retune-d80 independently implemented the same fix at base 21). Bar:
  validated on the record + adversarial N up to 1e111. Recommend the reviewer certify into
  `constants/3a/lemmas/` so all sketches share one correct log-bound primitive.
