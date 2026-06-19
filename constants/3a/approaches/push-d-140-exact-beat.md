# push-d-140-exact-beat — push the GHR digit construction to d=140, Lean-certified

## Idea
Continuation of `push-d-130-exact-beat` / `directed-param-sweep-exact-beat`: the GHR base-21
drop-1 digit construction value `1 + log(|U−U|/|U+U|)/log(2·max(U)+1)` rises monotonically in
`d` at fixed density (the difference-set per-digit entropy is unsaturated below the d→∞ density
limit; rnum 0.534@d100 → 0.537@d120 → 0.538@d130, asymptote ≈ 0.552 / value ≈ 1.1813). Climbing
`d` past the record's `d=80` strictly beats it. R18 reached d=100 (held 5877/5000), R22 reached
d=130 (held 2353/2000). This round pushes to **d=140** and certifies the larger beat both
numerically AND in Lean.

## Status — CLAIMED BEAT (R23, unverified until reviewer re-runs `verify_beat.py` + `lake build`)

**Claimed lower bound: C_3a ≥ 1177/1000 = 1.1770**
strictly above the previously HELD & Lean-checked `2353/2000 = 1.1765` (R22)
(and `5877/5000 = 1.1754`, and the true record `1.1740744476935212`).

New cell (carry-free, B=21 > 2·max(A)=20):

| cell | A | B | d | T | density | value (float, display) | wedge c | (c−1)=P/Q | decide |
|------|---|---|---|---|---------|------------------------|---------|-----------|--------|
| PRIMARY (R23) | {0,2,3,4,5,6,7,8,9,10} | 21 | 140 | 263 | 1.8786 | 1.1771186319558 | 1177/1000 = 1.1770 | 177/1000 | (Q=1000, fast) |

Only change from the record (d=80/T=150): d=80 → 140 (T scaled at the same density).

Exact integers: `|U+U|` 136d, `|U−U|` 169d, `max(U)` 185d (persisted in
`certificate/beat_d140/beat_d140.json`).

### What I did this round (R23)
1. Ran the SINGLE d=140/T=263 carry-free DP cell, ONE heavy cell per `timeout 600` Bash call,
   NEVER `dp_pareto.py`. The heavy sumset (mask width T+1) is the bottleneck at this density
   and overran a single 600s call when run together with the diff/max. Split it: computed the
   cheap `|U−U|`+`max(U)` first (`run_d140_diffmax.py`, ~135 s) and persisted them, then the
   heavy `|U+U|` via the engine `count_opset` (`run_d140_engine.py`, ~510 s), persisting the
   full `beat_d140.json` immediately on completion (a kill after persistence loses nothing).
2. Confirmed in plain-Python big-int (Fraction) FIRST: with wedge `c = 1177/1000` (P=177,
   Q=1000) the d=140 cell PASSES `Nm^Q ≥ Np^Q·(2M+1)^P` AND the d=80 record cell FAILS the same
   inequality ⇒ `value_record < c ≤ value_new`; and `c = 1177/1000 > 2353/2000` (HELD) exactly.
   Picked 1177/1000 as the cleanest large headline (1.1770) with small Q: Q=1000 < R22's Q=2000
   (which decided in ~11.5 s), well below the R21 Q=10000 blowup. (The even-higher 11771/10000
   = 1.17710 also passes exactly but Q=10000 is the force-kill trap; 113/96 = 1.177083 passes
   with tiny Q=96 but 1177/1000 is a cleaner headline.)
3. Ported to Lean: added `Nplus140`/`Nminus140`/`maxU140` literals + `newGE140`/`recLT140`/
   `c3a_ge_1177_1000`/`c3a_ge_1177_1000'` to `lean/Constants/C3a.lean`, reusing the named
   `GHR_lower` bridge and keeping the R19 `c3a_ge_5877_5000` and R22 `c3a_ge_2353_2000`
   theorems intact.
4. `lake build Constants.C3a` → PASS (1980 jobs, ~236 s). `#print axioms`:
   - `newGE140`, `recLT140`: `[propext]` only (no sorryAx, no native_decide/ofReduceBool).
   - `c3a_ge_1177_1000` / `'`: `[propext, Classical.choice, Quot.sound]` (standard real trio).
   - Lean literals match `beat_d140.json` bit-for-bit (verified by `litcheck`).
5. Wrote `certificate/beat_d140/{verify_beat.py, README.md}`; `python3 verify_beat.py` →
   exit 0, `CERTIFICATE OK` (record-cell recompute bit-for-bit vs PR#71, two-engine cross-check
   on d∈{20,30,40}, both exact wedge inequalities, all bar comparisons).

### The load-bearing step (no hand-waving)
Strict beat `value_record < c ≤ value_new` is certified EXACTLY by big-int powers with
`c−1 = 177/1000`:
- `value_new ≥ c`    ⟺ `Nm^Q ≥ Np^Q·(2M+1)^P`        (d=140 cell, TRUE — Lean `newGE140`)
- `value_record < c` ⟺ `RNm^Q < RNp^Q·(2·RM+1)^P`    (d=80 record, TRUE — Lean `recLT140`)
No float decides anything. The GHR analytic step (`θ(U) ≥ c ⟹ arbitrarily large extremal A,B
⟹ C_3a ≥ c`) is the named hypothesis `GHR_lower`, not an axiom (same trust pattern as 9a
`ThetaGeFromIndep`, 5b `MTThm15`).

### Trust split (integers)
The three d=140 integers are TRUSTED literals (R19/R22/R13 split): the kernel does only the
power arithmetic; provenance is re-derived OUT of Lean by `verify_beat.py --recompute`
(carry-free `digit_dp.count_opset`). Recomputing the carry-free DP inside the Lean kernel is an
OOM hazard and is deliberately NOT done.

## Certificate
- `lean/Constants/C3a.lean` — theorems `newGE140`, `recLT140`, `c3a_ge_1177_1000(')`.
  Build target `Constants.C3a`; `#print axioms` as above.
- `constants/3a/certificate/beat_d140/{verify_beat.py, beat_d140.json, README.md,
  run_d140_diffmax.py, run_d140_engine.py, d140_diffmax.json}`.

## How to push further
- The asymptote for this shape is ≈ 1.1813 (calibrated fit on measured d=100/120/130 cells;
  the hard digit-set ceiling 1.25 is unreachable). d=140 at 1.17712 is ~95% of the runway from
  held to the asymptote; remaining runway above held ≈ 4.2e-3.
- d=150/T=282 (predicted ≈ 1.17738, +8.8e-4 over held) and d=160/T=300 (≈ 1.17763) are the next
  rungs — but each is a hotter superlinear-in-T DP (d=150 needs `timeout 700+`, d=160 over). The
  d=140 sumset here already needed splitting into two calls to fit `timeout 600`; d=150+ should
  budget the heavy sumset its OWN full call. Keep the Lean wedge Q ≤ ~2000.
- This is a SHALLOW treadmill near the family asymptote. A larger jump past 1.25 needs a
  non-digit-set `U` (`beyond-digit-set-structured-U`, speculative, no construction in hand) — the
  reshape road within digit alphabets is CLOSED (R22).
