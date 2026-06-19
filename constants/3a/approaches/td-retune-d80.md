# td-retune-d80 — re-tune the sum cap T at Griego's alphabet & d (CHEAPEST SHOT)

**Direction:** lower bound on C_3a. **Record to beat:** 1.1740744 [G2026].
**Status (round 2): ALL HOLES CLOSED — claimed verified lower bound 1.1741713539984820 > record.**
**Borrows:** the exact-DP engine from `alphabet-search-dp` (`ghr_dp.py`, sped up) and the
atanh log primitives `_log_lb` / `_log_ub` from `per-position-alphabet` (NOT its broken
`certify_theta_lb` — see H3).

## Strategy
Griego's record fixes A = {0,2,3,4,5,6,7,8,9,10}, d = 80, **T = 150** (T/d = 1.875). The
math-explorer (round 2) found the alphabet is saturated (Finding A) but the **T/d ratio is mildly
off-optimal**: the theta-vs-T/d curve peaks near T/d ≈ 1.90–1.95, above Griego's 1.875. At d=80
the analogue is T ≈ 152–156. The only free knob is **T**: a one-parameter scan at d=80, record
alphabet, around T ∈ {150,152,154,156,158}. **T=154 wins.**

## What closed this round

### H1 T-SCAN — CLOSED
Ran `theta_floatbound_fast(ARECORD, 80, T)` one point at a time (~170 s/pt, progress printed):
- T=150 → theta = 1.1740744477  (reproduces Griego's record literal exactly — sanity)
- T=154 → theta = 1.1741713540  (**+9.7e-5 over the record on float — the winner**)

(T=156 was started; T=154 already clears the bar with margin, so it is the certified point.)

### H2 EXACT CONFIRM — CLOSED
Exact integer counts at d=80, T=154 (from the validated fast DP, ~170 s sumset):
- |U+U| = 597130362133498688344900538759091221981599964605490705452812019502078419618406
- |U-U| = 1583022697814754823730226433460816281662151877595631959725969360255416773109712840757177539870935
- max(U) = 2995805288150731620427416034073013045407712819639364547243511761614441608214402813704058986719974740854874
- q = 2·max(U)+1.

These are cached as `S154`/`D154`/`M154`; the full run recomputes them with the fast routines and
**asserts equality** to the cached literals (and `--replay` certifies from the cache in seconds).
Cross-check: `_oracle_crosscheck()` confirms the two fast routines == the slow frozenset oracle at
d ∈ {8,12,20} (three independent implementations agree); `ghr_dp.__main__` confirms the same at
small d AND reproduces Griego's d=80 record literals.

### H3 CERTIFY — CLOSED (the load-bearing fix)
**The flaw the reviewer flagged was real and BIGGER than stated.** `per-position-alphabet.certify_theta_lb`
ran the atanh log series directly on **both** q ~ 21^80 **and** diff/s ~ 1e18. For each, z =
(x−1)/(x+1) ≈ 1, so the series needs ~1e106 terms and collapses to a useless bound (theta_lb → ~1.0).
The denominator was not the only problem — the numerator log(diff/s) is at z≈1 too.

**Fix (Griego's base-b reduction):** for any integer N ≥ 1, with k = floor(log_b N),
`log(N) = k·log(b) + log(N/b^k)`, residual N/b^k ∈ [1,b) so its z ≤ (b−1)/(b+1) = 20/22 ≈ 0.909
— the atanh series converges in a few hundred terms. log(b)=log(21) itself is bounded by the same
series (z = 10/11). Directed rounding, all exact `Fraction`:
- numerator log(diff) − log(s): LOWER-bound log(diff) (k_d·logb_LB + atanh-LB residual),
  UPPER-bound log(s) (k_s·logb_UB + atanh-UB residual);
- denominator log(q): UPPER-bound (k_q·logb_UB + atanh-UB residual).

Truncation/tail are conservative, so `theta_lb` is a rigorous lower bound on the true theta.
**Verified directionally** (each piece on the correct side of the float value; all residual z<1):
log diff lb ≤ float, log s ub ≥ float, log q ub ≥ float. **Validated on the record instance**
(reproduces theta_lb = 1.174074447694 to 12 digits, matching float, beats=True) before use at T=154.

**Result at T=154:**
`theta_lb ≥ 1.174171353998482` (exact rational, shown round-DOWN to 15 places; terms=400),
float check 1.174171353998, **rational margin over the record = +9.695e-5, beats strictly = True.**

## Claimed bound (CLAIM until the reviewer verifies)
**C_3a ≥ 1.174171353998482** (directed-rounded rational certificate, base-b reduced log bound),
strictly exceeding the verified record **1.1740744** [G2026] by **+9.70e-5**. Construction is the
GHR2007 single-set lemma at the record alphabet A={0,2..10}, base b=21, d=80, **T=154**.

## Reproduce
- `python td-retune-d80.py`          full pipeline (~170 s sumset DP, then certify)
- `python td-retune-d80.py --replay` certify from cached exact counts only (seconds)
- `python td-retune-d80.py --scan`   re-run the T-scan around 150–158 (one point at a time)

## Holes remaining
None on the path to the claimed bound. (A wider T-scan / larger-d push would be a *further*
improvement, not needed for this bound — that is alphabet-search-dp's frontier.)

## Promotable lemmas
`certify_theta_lb` (base-b reduced directed-rounded rational lower bound on
`1 + log(diff/s)/log(q)` for diff≥s≥1, q≥2) — proved green in `td-retune-d80.py` (functions
`_floor_log_b`, `_log_big_lb`, `_log_big_ub`, `certify_theta_lb`, validated by
`_validate_certify_on_record`). This is the correct replacement for the broken shared
`per-position-alphabet.certify_theta_lb`, reusable by every Python sketch (alphabet-search-dp,
per-position-alphabet) at the q ~ b^d scale where the old one silently fails. Recommend the
reviewer certify it into `lemmas/` (or have the broken shared one redirected to it).

## Feeds the Lean line
The winning triple (|U+U|, |U-U|, max U) at T=154 above is exactly what `ghr-lemma-lean` needs to
formalize an actual improvement (not a re-certification of the record).
