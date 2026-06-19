# C_3a strict beat — larger-d digit construction (d=100)

**Claim (unverified until the reviewer re-runs the certificate):**
`C_3a >= 5877/5000 = 1.1754 > 1.1740744476935212` (the verified record [G2026], PR #71).

## Construction

GHR2007 lower bound: for a finite `U ⊆ ℤ≥0` with `0 ∈ U`,
`C_3a >= 1 + log(|U−U| / |U+U|) / log(2·max(U)+1)`.

Digit set `U = { Σ_{i<d} a_i·B^i : a_i ∈ A, Σ a_i ≤ T }` with

| cell | A | B | d | T | density | value (float) | wedge `c` |
|------|---|---|---|---|---------|---------------|-----------|
| **PRIMARY**   | {0,2,3,4,5,6,7,8,9,10} | 21 | 100 | 187 | 1.875 | 1.1754209217852494 | 5877/5000 = 1.1754 |
| SECONDARY     | {0,2,3,4,5,6,7,8,9,10} | 21 | 100 | 180 | 1.80  | 1.1748968370899104 | 2937/2500 = 1.1748 |
| record (ref)  | {0,2,3,4,5,6,7,8,9,10} | 21 | 80  | 150 | 1.875 | 1.1740744476935212 | — |

Same alphabet/base as the record; **the only change is d=80→100** (and a small density
choice). `B=21 > 2·max(A)=20` so the regime is carry-free (the exact-count DP applies).

## Why this beats the record

The record was d=80. Holding the alphabet/base/density fixed and raising d, the GHR value
rises (the difference-set per-digit entropy has not saturated at d=80, while max(U)'s growth
rate has). At d=100 the value crosses the record by ~1.3e-3.

## The exact strict-beat certificate (no float decides anything)

The table records the record as `1.1740744`, but the bar to strictly beat is the **actual
achieved record value 1.1740744476935212** (the d=80/T=150 construction value), not the
7-decimal truncation. We certify `value_new > value_record` exactly by a rational wedge `c`:

For `c − 1 = p/q` in lowest terms (`p,q ≥ 0`, the GHR value is ≥ 1), with the new cell counts
`(Np, Nm, M)` and record cell counts `(RNp, RNm, RM)`:

- **value_new ≥ c**  ⟺  `Nm^q ≥ Np^q · (2M+1)^p`   (exact big-int comparison)
- **value_record < c** ⟺  `RNm^q < RNp^q · (2·RM+1)^p`   (exact big-int comparison)

Both true ⟹ `value_new ≥ c > value_record`: a strict beat. For the PRIMARY cell
`c = 5877/5000`, `p=877, q=5000` (small exponent → the powers are fast big-ints).

## Reproduce

```
python3 verify_beat.py
```

Exit 0 + `CERTIFICATE OK` only if every check passes. The script:
1. recomputes the record cell's `(|U+U|,|U−U|,max U)` from scratch (fast carry-free DP,
   `engine/digit_dp.count_opset`) and asserts they match `sweep/record_baseline.json`
   (the PR #71 integers) bit-for-bit;
2. cross-checks the fast DP against the independent Pareto DP (`sweep/dp_engine`) on three
   small cells (both engines agree bit-for-bit);
3. recomputes each new cell's three integers and runs the exact integer-power wedge test
   above for both cells.

`beat_d100.json` holds the exact 95–120 digit integers and wedge data for both new cells.

## Notes / what would push it further

- The GHR digit-set method has a hard ceiling of 1.25, so headroom remains 1.1754→~1.25.
- The value keeps rising in d; d=120, 160 should give 1.176–1.177 (the cost is the sumset DP
  bitmask width = T+1, so higher d at density 1.875 means larger T — budget the per-cell
  timeout and keep the per-position progress emission).
- **Lean cert (next sub-goal):** the wedge `c = 5877/5000` (p=877, q=5000) is a small-q
  rational, so the integer-power inequality `Nm^5000 ≥ Np^5000·(2M+1)^877` is finite and
  Lean-checkable (`decide`/`norm_num` on big-ints), unlike the record's razor margin
  (q≈1.25e6, infeasible). This is the gold-standard finish for this bound.
