# push-d-cotuned-T

## Idea

Take the record family of [G2026] — digit set `A = {0,2,3,...,10}` (digit 1 dropped, max
digit 10), base `b = 21` — and scale the depth `d` past the record's `d = 80`, co-tuning the
digit-sum cap `T` to each depth's optimum. The GHR2007 lemma gives
`C_3a >= theta(U) = 1 + ln(|U-U|/|U+U|)/ln(2*max(U)+1)`, and the explorer/reviewer verified
`theta(d)` is **monotone increasing and not converged** at the record `d=80` (it stopped
short), so a larger `d` at the co-tuned ratio is a guaranteed valid win on the *same valid
family* — no new validity question, only DP runtime.

The record used `T/d = 150/80 = 1.875`; the per-`d` optimum ratio is slightly higher
(~1.91–1.95). At `d=90` the optimum is `T=172` (ratio 1.911), beating `T=170` and `T=174`.

## Chosen parameters (round 2)

- base `b = 21`, `A = {0,2,...,10}`, `d = 110`, `T = 210` (ratio T/d ≈ 1.909, the per-`d`
  optimum the explorer/outline-reviewer measured around 1.91·d).
- A single ~78s exact-counting run — the safe certifiable increment for round 2.
- The d=90 / T=172 result below is the round-1 claim (never reviewer-verified); d=110 / T=210
  is the stronger round-2 claim that supersedes it on the same artifact.

## Claimed result — round 2 (UNVERIFIED — reviewer to confirm)

- `S = |U+U|` = 107-digit integer; `D = |U-U|` = 133-digit; `max(U)` = 146-digit (all exact,
  printed by the script).
- **Certified theta (rigorous lower bound) = 1.1760055927978140029771014788...**
  (lower endpoint of an mpmath interval enclosure, `iv.prec=400`).
- Record to beat [G2026]: **1.1740744**. Margin: **+0.0019311927978139...**. Strictly beats: **YES**.
- Reproduce command (run ALONE — CPU contention multiplies runtime 5–10×):
  `cd constants/3a/certificate && python3 certify_3a.py 110 210`  (counting runtime 78.4 s here).
- Brute-force re-validated both DPs vs full enumeration at (d,T) ∈ {(2,8),(3,8),(2,20),(3,10),(4,10)} —
  S, D, max(U) all match exactly before this run.

### Prior round-1 claim (superseded, d=90 / T=172)

- `S` = 88-digit, `D` = 109-digit, `max(U)` = 119-digit; theta = 1.1748992466319329...;
  margin +0.000824847. Never reviewer-verified.

## Fallback (if d=110 overruns budget)

- `python3 certify_3a.py 100 192` → theta ≥ 1.175495346956…, margin +0.00142, ~55 s.

## Why it is valid (GHR-lemma hypotheses + validity guard)

- `U` finite, non-negative, contains 0 (all-zero digit vector; `0 <= T`). Checked & printed.
- **Validity guard** `base >= 2*max(A)+1` → `21 >= 21` holds, so U+U and U-U have carry-free
  base-21 reps and the two DPs count **distinct integers** (the base-20 trap, which overcounts,
  is excluded). Printed by the certificate.
- DPs validated against brute-force enumeration of U at small `(d,T)`.

## Status

CLAIMED (round 2: built, reproducible, d=110/T=210, beats record by +0.0019312). Awaiting
proof-reviewer verification. The record at `d=80` reproduces exactly (1.1740744477) with the
same harness, anchoring the family.

## How to push further next round

- **Larger `d` (the dominant lever).** `theta(d)` keeps rising. The bottleneck is DP runtime
  (state count grows with `T`, hence with `d`). Estimate: `d=90` ≈ 35s; `d=100–110` is a few
  minutes — feasible if the round budget allows a longer single run. Co-tune `T ≈ 1.91·d`
  (sweep a small window ±2 around it). Expected: `d≈110–120` → ~1.1755–1.176.
- **Compose with digit-set-hole-search (the companion build).** If `M=11`/base-23 (or another
  hole pattern) is confirmed to keep its small edge at large `d`, swap the family and re-run the
  same certificate — the M-knob shifts the whole family's asymptote, compounding the d-push.
- **Speed the DP** to reach larger `d` within the time budget: prune unreachable bitset states,
  or exploit symmetry; the sum DP's bitset state is the memory/time driver.
- The numerical certificate machinery (exact DP + mpmath interval ln) is reusable verbatim at
  any `(A, base, d, T)` — only the parameters change.
