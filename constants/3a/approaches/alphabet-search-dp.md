# alphabet-search-dp — longer-d, retuned-T/d homogeneous construction (PRIMARY)

**Direction:** lower bound on C_3a. **Value to beat (verified held, R2):** 1.1744750903655619
(this same sketch, d=84, T=162). Published record 1.1740744 [G2026] already superseded.
**CLAIMED this round (round 3, certified hole-free):** **C_3a >= 1.1752717416788478**
(d=96, T=184, A={0,2,3,4,5,6,7,8,9,10}, base 21, c=T/d=1.9167). Margin over the prior held
**+7.97e-4**; over the record **+1.20e-3**.
*(Claim, not yet reviewer-verified — the script reproduces it end-to-end from cached exact
counts in <2 s, and the d=96,T=184 counts re-derive from a fresh DP with VERIFY_DP=1; see CHECK.)*

## Strategy (re-scoped round 2)
The homogeneous record alphabet {0,2..10} is SATURATED (explorer Finding A). So this sketch
drops alphabet edits and pushes LENGTH at a RE-TUNED cap ratio. theta rises with d toward the
asymptote, and the optimal T/d sits ABOVE Griego's 1.875. The length gain compounds with the
T/d gain. Same exact-integer DP engine (`ghr_dp.py`), GHR2007 single-set lemma, certified with
a directed-rounded RATIONAL log bound.

## What I closed this round (round 3)
- **H1' LONGER-d FRONTIER (d=88, d=96) — CLOSED.** Scanned d=88 and d=96 at the re-tuned
  T/d grid, ONE point per background invocation across 64 cores (sumset bitmask ~267 s/pt at
  d=88, ~400 s/pt at d=96; diffset <2 s; flush=True progress; never a single silent >600 s
  call — per-role NEVER respected). Both d show an INTERIOR peak; EVERY scanned point beats the
  prior held bound:
  - **d=88:** T=167→1.17475046, 168→1.17476379, **169→1.17476434 (peak, c=1.9205)**,
    170→1.17475214, 171→1.17472719.
  - **d=96:** T=182→1.17526075, 183→1.17527164, **184→1.17527174 (peak, c=1.9167)**,
    185→1.17526106, 186→1.17523960.
  The longer d remains the dominant lever (d=84→1.17448, d=88→1.17476, d=96→1.17527) and the
  optimum c keeps drifting DOWN with d (1.929→1.921→1.917, all still above Griego's 1.875),
  confirming the round-2 pattern. **Best = d=96, T=184.**
- **H2 EXACT CONFIRM — CLOSED.** Exact integer counts for the d=88,T=169 and d=96,T=184 winners
  cached in `WINNERS`. The d=96,T=184 `q=2·max(U)+1` was independently re-derived (`max_U`) and
  matches the cached literal; a fresh full DP recompute at d=96,T=184 (`VERIFY_DP=1` path /
  standalone verify) reproduces the cached `|U+U|`, `|U-U|` exactly.
- **H3 CERTIFY — REUSED (closed round 2).** Same directed-rounded scaled base-2 rational log
  bound (now also the reviewer-certified `lemmas/log_bounds.py`). Applied to d=96,T=184:
  certified `theta_lb = 1.1752717416788478`. terms-sensitivity check: terms ∈ {300,350,400,500}
  all return the identical safe lower bound (terms=300 already saturated at this q~1e132 scale),
  so the certified value is not a truncation artifact. Numerator `log(diff/s)` lower-bounded,
  denominator `log q` upper-bounded ⇒ `theta_lb ≤ theta`, a true LOWER bound; float cross-check
  agrees to <1e-12 in the safe direction.

## Holes remaining
- **None on the path to the claimed bound.** The bound 1.1752717416788478 is hole-free:
  exact-integer DP (d=96,T=184) + directed-rounded rational log bound, fully re-runnable.
- **Open (optional, not on the path):** d in {104, 112, ...} not yet scanned — the asymptote is
  still above (theta keeps rising), so a further small gain is expected, but each point grows as
  ~T² (d=104, c~1.91 ⇒ T~199 ⇒ ~500 s/pt). Left as the next extension; not a hole blocking the
  bound. Helpers `scan_d88`/`scan_d96` (and the `_scan` driver) generalize to any d.

## Verify
```
cd constants/3a/certificate && python3 alphabet-search-dp.py          # <2 s, cached literals
cd constants/3a/certificate && VERIFY_DP=1 python3 alphabet-search-dp.py  # ~700 s, re-runs all DP
```
Expected best line:
`... d=96 T=184  certified theta_lb=1.1752717416788478 beats=True  margin=1.197e-03  <== BEST`
and the closing `CERTIFIED LOWER BOUND on C_3a: 1.1752717416788  (d=96, T=184, ...)`.
(The `_scan_point.py` driver re-runs any single (d,T) point with progress; `_scan_results.txt`
holds the raw exact counts logged during this round's scan.)

## Promotable lemmas
- **None new this round.** The `logN_lb`/`logN_ub` scaled base-2 log-bound primitive was already
  certified into `constants/3a/lemmas/log_bounds.py` (round 2); this round's certify step
  imports/reuses it (verified terms-saturated at the d=96 q~1e132 scale). No new reusable lemma
  was proved — the round 3 work was a frontier scan + caching, not a new general result.
