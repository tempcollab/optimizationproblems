# directed-param-sweep-exact-beat — larger-d exact-integer beat of the C_3a record

## Idea
The record [G2026, PR #71] is the base-21 digit construction at d=80, T=150 (density 1.875),
value 1.1740744476935212. The GHR value rises in d at fixed density (difference-set per-digit
entropy unsaturated at d=80; max(U) growth-rate converged). So climb d with the SAME
alphabet/base and certify a strict beat exactly via the integer-power test — never a float.

## Status — CLAIMED BEAT (R18, unverified until reviewer re-runs `verify_beat.py`)

**Claimed lower bound: C_3a ≥ 5877/5000 = 1.1754** (strictly > record 1.1740744476935212).

Two new cells, BOTH certified strict beats (exact integer-power wedge test):

| cell | A | B | d | T | density | value (float, display) | wedge c | (c−1)=p/q | time |
|------|---|---|---|---|---------|------------------------|---------|-----------|------|
| PRIMARY   | {0,2,3,4,5,6,7,8,9,10} | 21 | 100 | 187 | 1.875 | 1.1754209217852494 | 5877/5000 = 1.1754 | 877/5000 | 140s |
| SECONDARY | {0,2,3,4,5,6,7,8,9,10} | 21 | 100 | 180 | 1.80  | 1.1748968370899104 | 2937/2500 = 1.1748 | 437/2500 | 138s |

Only change from the record: **d=80 → 100**. Carry-free (B=21 > 2·max(A)=20).

### How it was certified (the load-bearing step, no hand-waving)
The table writes the record as 1.1740744, but the bar is the ACTUAL achieved record value
1.1740744476935212. Strict beat `value_new > value_record` is certified EXACTLY by a rational
wedge `c` with `value_record < c ≤ value_new`, both inequalities checked by pure big-int powers:
- `value_new ≥ c`  ⟺  `Nm^q ≥ Np^q·(2M+1)^p`  (new cell, **True**)
- `value_record < c`  ⟺  `RNm^q < RNp^q·(2·RM+1)^p`  (record cell, **True**)
with `c−1 = p/q` in lowest terms. q is small (≤5000) so the powers are fast. No float decides.

### Independent cross-checks done
- Driver reproduces the record cell (d=80/T=150) integers bit-for-bit vs `record_baseline.json`
  (PR #71) — `value 1.1740744476935`, strict_beat=False (cannot beat itself: correct).
- Fast engine `engine/digit_dp.count_opset` agrees bit-for-bit with the independent Pareto
  engine `sweep/dp_engine.count_sumset/diffset/maxU` on d∈{20,30,40} (cells the slow engine
  can finish), for all three of |U+U|, |U−U|, max(U).
- The wedge inequalities re-verified with fresh `Fraction`/big-int arithmetic (separate from
  the driver's `ghr_geq`/`ghr_beats`).
- Standalone `verify_beat.py` re-runs the whole chain from scratch → exit 0, `CERTIFICATE OK`.

## Certificate
- `constants/3a/certificate/beat_largerd/verify_beat.py` — re-runnable, recomputes everything
  from scratch (~5 min); exit 0 + `CERTIFICATE OK` iff valid.
- `constants/3a/certificate/beat_largerd/beat_d100.json` — exact integers (95–120 digits) +
  wedge data for both cells.
- `constants/3a/certificate/beat_largerd/README.md` — full write-up.
- `constants/3a/certificate/sweep/climb_driver.py` — the chunked, progress-emitting, persisted
  per-(d,T)-cell runner; state in `climb_state.json`, log in `climb.log`.

## What would push it further
- **Lean cert (clear next sub-goal):** c=5877/5000 has q=5000 → the inequality
  `Nm^5000 ≥ Np^5000·(2M+1)^877` is finite and Lean-checkable (`decide`/`norm_num` big-ints),
  unlike the record's q≈1.25e6. Gold-standard finish — port the PRIMARY cell to a `lake build`
  theorem. (This is the `lean-cert-rational-power` approach, now unblocked by a found beat.)
- **Climb further:** d=120, 160 at density 1.875 should give ~1.176–1.177 (cost = sumset DP
  bitmask width T+1; budget per-cell timeout + keep per-position progress emission). The
  driver supports it directly: `python3 climb_driver.py 120 225` etc.
- **Density retune:** at d=100 the optimum density may be slightly above 1.875; T∈{190,194}
  cells could add a sliver, at higher sumset-DP cost.
- Hard ceiling of the GHR digit-set method is 1.25, so headroom remains 1.1754 → ~1.25.

## Operational notes (force-kill avoidance — worked this round)
- ONE (d,T) cell per Bash call, `timeout`-wrapped. d=100/T=187 finishes in 140s with the FAST
  `count_opset` engine (NOT dp_pareto, which took 2128s/cell and caused prior force-kills).
- Per-digit-position progress line flushed to `climb.log`; counts persisted to JSON BEFORE the
  wedge step so a kill never loses them.
- Wedge denom capped at 10^5 → reduced q ≤ a few thousand → powers fast. (Denom 10^9 gives
  q≈10^9 = catastrophic powers — the first run's force-kill; fixed.)
