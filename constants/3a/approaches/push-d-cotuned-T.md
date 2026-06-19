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

## Chosen parameters (round 3) — d=150, co-tuned T=285

- base `b = 21`, `A = {0,2,...,10}`, `d = 150`, **`T = 285`** (ratio T/d = 1.900).
- T co-tuned by a SOLO sweep at fixed d=150 (each T a separate run, no parallelism per role
  memory): T ∈ {283,284,285,286,287,289}. The verified interval-ln lower endpoint peaks at
  **T=285**:

  | T   | θ_lower (interval lower endpoint) | runtime |
  |-----|-----------------------------------|---------|
  | 283 | 1.1774227596708463…               | 296.0 s |
  | 284 | 1.1774273365700025…               | 295.0 s |
  | **285** | **1.1774273905511207…**       | 300.6 s |
  | 286 | 1.1774229226713084…               | 299.1 s |
  | 287 | 1.1774139340143219…               | 302.6 s |
  | 289 | 1.1773823988412312…               | 314.1 s |

  T=285 is the local optimum (strictly above both neighbours 284 and 286, and well above the
  explorer's predicted 287). The explorer's T≈1.91·d guess slightly overshoots at d=150; the
  per-d optimum ratio is ~1.90 here.
- Full certificate output captured at
  `constants/3a/certificate/cert_output_d150_T285.txt`.

## Chosen parameters (round 2)

- base `b = 21`, `A = {0,2,...,10}`, `d = 110`, `T = 210` (ratio T/d ≈ 1.909, the per-`d`
  optimum the explorer/outline-reviewer measured around 1.91·d).
- A single ~78s exact-counting run — the safe certifiable increment for round 2.
- The d=90 / T=172 result below is the round-1 claim (never reviewer-verified); d=110 / T=210
  is the stronger round-2 claim that supersedes it on the same artifact.

## Claimed result — round 3 (UNVERIFIED — reviewer to confirm)

- d=150, T=285, same exact valid family (A={0,2,…,10}, base 21, drop-1).
- `S = |U+U|` = 146-digit integer; `D = |U-U|` = 182-digit; `max(U)` = 199-digit (all exact,
  printed by the script; full literals in `certificate/cert_output_d150_T285.txt`).
- **Certified theta (rigorous lower bound) = 1.1774273905511207333163761169274037138206…**
  (lower endpoint of an mpmath interval enclosure, `iv.prec=400`).
- Bar to beat this round = our verified **held θ ≥ 1.1760055927978140** (d=110/T=210). Margin
  over held: **+0.0014217977533067** (strictly beats: **YES**). Margin over table record
  1.1740744 [G2026]: **+0.0033529906**.
- `D > S ? True` and validity guard `21 >= 21 : OK` both printed by the run.
- Reproduce command (run ALONE — CPU contention multiplies runtime 5–10×):
  `cd constants/3a/certificate && python3 certify_3a.py 150 285`  (counting runtime ~300 s here).
- Same brute-force-validated DP recurrences as the verified d=110 build; only (d,T) changed, so
  no new validity question (the carry-free guard 21≥2·max(A)+1 is d-independent).

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

CLAIMED (round 3: built, reproducible, d=150/T=285, θ ≥ 1.1774273905511207, beats verified held
1.1760055927978140 by +0.0014218 and table record 1.1740744 by +0.0033530). Awaiting
proof-reviewer verification. T co-tuned by a solo sweep (T=285 is the local optimum at d=150).
Supersedes the round-2 d=110/T=210 claim on the same artifact. The record at `d=80` reproduces
exactly (1.1740744477) with the same harness, anchoring the family.

## How to push further next round

- **Larger `d` (the dominant lever), but runtime now bites.** `theta(d)` keeps rising toward the
  family asymptote θ_∞ ≈ 1.1786 (explorer's geometric-decay fit). At d=150 the counting run is
  ~300 s (sum-DP dominates, growing ~quadratically), so a single d=170 run (~7–8 min) and even
  d=200 (~12–15 min) still fit one tool call WITHOUT a speedup — these are the next d-pushes.
  Co-tune `T ≈ 1.90·d` (the per-d optimum ratio measured ~1.90 at d=150, slightly below the
  earlier 1.91 estimate); sweep ±2 around it as SEPARATE solo runs. Expected: d=170 → ~1.17775,
  d=200 → ~1.17810. Beyond d≳200 the `dp-speedup-prune` lever becomes necessary.
- **Compose with digit-set-hole-search (the companion build).** If `M=11`/base-23 (or another
  hole pattern) is confirmed to keep its small edge at large `d`, swap the family and re-run the
  same certificate — the M-knob shifts the whole family's asymptote, compounding the d-push.
- **Speed the DP** to reach larger `d` within the time budget: prune unreachable bitset states,
  or exploit symmetry; the sum DP's bitset state is the memory/time driver.
- The numerical certificate machinery (exact DP + mpmath interval ln) is reusable verbatim at
  any `(A, base, d, T)` — only the parameters change.
