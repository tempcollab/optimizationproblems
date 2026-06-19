# C_3a strict-beat certificate — d=130 cell, wedge c = 2353/2000 (R22)

## Claim

    C_3a  >=  2353/2000  =  1.1765
          >  5877/5000   =  1.1754                  (our previously HELD bound, R18/R19)
          >  1.1740744476935212                     (the historical [G2026] PR #71 record)

This is a STRICT improvement over the previously held & Lean-machine-checked
`5877/5000 = 1.1754`.

## Construction (GHR digit-set, the record alphabet pushed to larger d)

    A = {0,2,3,4,5,6,7,8,9,10},  B = 21      (carry-free: B = 21 > 2*max(A) = 20)
    U = { sum_{i<d} a_i B^i : a_i in A, sum a_i <= T }
    value = 1 + log(|U-U| / |U+U|) / log(2*max(U)+1)      (GHR2007 lower bound on C_3a)

    PRIMARY beat cell:  d = 130, T = 244 (density 1.8769)  ->  value ~ 1.1767830604497

Only change from the d=80/T=150 record cell: d=80 -> 130 (same alphabet/base/regime).

## The exact wedge (load-bearing step, no float decides)

Pick `c = 2353/2000`, so `c - 1 = 353/2000` in lowest terms => `P = 353`, `Q = 2000`.
The monotone log-free chain (`d >= s > 0`, `q > 1`, `p,q >= 0`) gives

    value_new >= c     <=>  Nm^Q >= Np^Q * (2*M+1)^P          (d=130 cell:  TRUE)
    value_record < c   <=>  RNm^Q <  RNp^Q * (2*RM+1)^P        (d=80 record:  TRUE)

so  value_record < c <= value_new  is established by pure big-int powers (no float).
The wedge denominator Q=2000 keeps the kernel `decide` fast (~11.5s; R21's Q=10000 was the
blowup that force-killed the previous attempt; R19 proved Q=5000 in ~4s, so Q=2000 is safe).

## Integers

`(Nplus, Nminus, maxU)` for the d=130 cell are in `beat_d130.json` (mirrored from the
re-runnable climb state `../sweep/climb_state.json::d130_T244`). They are 126 / 157 / 172
digits. Provenance is re-derivable OUT of Lean by the carry-free digit-DP
(`../engine/digit_dp.count_opset`); see `verify_beat.py --recompute`.

## Reproduce

    python3 verify_beat.py            # loads persisted d=130 integers, recomputes the RECORD
                                      # cell + small-cell two-engine cross-check, re-derives the
                                      # EXACT wedge from scratch.  Exit 0 + "CERTIFICATE OK".
    python3 verify_beat.py --recompute   # ALSO recomputes the d=130 integers from scratch
                                         # via the DP (~440s) and asserts they match.

NOTE: the default mode does NOT re-run the heavy d=130 DP (that ~440s silent op is the
known force-kill trap); every other load-bearing step (record recompute, engine
cross-check, both exact wedge inequalities, both bar comparisons) is re-run from scratch.

## Machine-checked Lean theorem

The same exact wedge is carried into Lean as `C3a.c3a_ge_2353_2000` /
`C3a.c3a_ge_2353_2000'` in `lean/Constants/C3a.lean`:
- `newGE130`  : `Nplus130^Q2 * (2*maxU130+1)^P2 <= Nminus130^Q2`   (`decide`, `[propext]`)
- `recLT130`  : record cell fails the same wedge (`decide`, `[propext]`)
- `c3a_ge_2353_2000'` : `C_3a >= 2353/2000` under the named `GHR_lower` bridge
  (axioms `[propext, Classical.choice, Quot.sound]`).

Build:  `lake build Constants.C3a`  (PASS, 1980 jobs, ~13s).
The three big integers are TRUSTED literals (same R19/R13 trust split): the kernel does the
power arithmetic; the integers' provenance is re-derived out-of-Lean by this certificate.
