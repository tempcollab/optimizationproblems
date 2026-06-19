# push-d-130-exact-beat — push the GHR digit construction to d=130, Lean-certified

## Idea
Continuation of `directed-param-sweep-exact-beat`: the GHR base-21 drop-1 digit construction
value `1 + log(|U-U|/|U+U|)/log(2max(U)+1)` rises monotonically in `d` at fixed density (the
difference-set per-digit entropy is unsaturated and `max(U)`'s growth-rate has converged), so
climbing `d` past the record's `d=80` strictly beats it. R18 reached `d=100` (held 5877/5000).
This angle pushes to `d=130` and certifies the larger beat both numerically AND in Lean.

## Status — CLAIMED BEAT (R22, unverified until reviewer re-runs `verify_beat.py` + `lake build`)

**Claimed lower bound: C_3a >= 2353/2000 = 1.1765**
strictly above the previously HELD & Lean-checked `5877/5000 = 1.1754`
(and the true record `1.1740744476935212`).

New cell (carry-free, B=21 > 2*max(A)=20):

| cell | A | B | d | T | density | value (float, display) | wedge c | (c-1)=p/q | decide |
|------|---|---|---|---|---------|------------------------|---------|-----------|--------|
| PRIMARY (R22) | {0,2,3,4,5,6,7,8,9,10} | 21 | 130 | 244 | 1.8769 | 1.1767830604497 | 2353/2000 = 1.1765 | 353/2000 | ~11.5s |
| fallback      | {0,2,3,4,5,6,7,8,9,10} | 21 | 120 | 225 | 1.8750 | 1.1763975172306 | 11763/10000 | 1763/10000 | (numeric only) |

Only change from the record (d=80/T=150): d=80 -> 130.

### What I did this round (R22)
The R21 build's heavy digit-DP already completed and persisted the exact d=130 integers
(`certificate/sweep/climb_state.json::d130_T244`: Nplus 126d, Nminus 157d, maxU 172d,
value_float 1.1767830604497, strict_beat=True). R21 was force-killed during the LEAN PORT,
because it tried a wedge with Q=10000 (kernel `decide` blowup). This round I did ONLY the
de-risked Lean port (no DP re-run):

1. Chose the wedge `c = 2353/2000` (so `c-1 = 353/2000`, P=353, Q=2000). Confirmed in plain
   Python (Fraction/big-int) that the d=130 integers pass the exact integer test
   `Nminus^Q >= Nplus^Q * (2*maxU+1)^P` AND the record cell fails it — for Q=2000.
   Q=2000 < R19's working Q=5000, so it is below the blowup; timed the standalone Lean
   `decide` at ~11.5s total for both wedge lemmas before committing.
2. Picked Q=2000 over the tiny-but-smaller-headline alternatives (147/125=1.176 with Q=125;
   20/17=1.17647 with Q=17): 2353/2000 gives the largest headline (1.1765) among wedges that
   stay comfortably fast (Q <= ~2000).
3. Added the three d=130 integers + the new theorems to `lean/Constants/C3a.lean`
   (`newGE130`, `recLT130`, `c3a_ge_2353_2000`, `c3a_ge_2353_2000'`), reusing the named
   `GHR_lower` bridge and keeping the R19 `c3a_ge_5877_5000` theorems intact.
4. `lake build Constants.C3a` PASS (1980 jobs, ~13s). `#print axioms`:
   - `newGE130`, `recLT130`: `[propext]` only (no sorryAx, no native_decide/ofReduceBool).
   - `c3a_ge_2353_2000` / `'`: `[propext, Classical.choice, Quot.sound]` (standard real trio).
5. Updated the numerical cert (`certificate/beat_d130/`): `verify_beat.py` re-keyed to wedge
   2353/2000, added `beat_d130.json`, wrote `README.md`. `python3 verify_beat.py` -> exit 0,
   `CERTIFICATE OK` (record-cell recompute bit-for-bit vs PR#71, two-engine cross-check on
   d in {20,30,40}, both exact wedge inequalities, both bar comparisons).

### The load-bearing step (no hand-waving)
Strict beat `value_record < c <= value_new` is certified EXACTLY by big-int powers:
- `value_new >= c`     <=> `Nm^Q >= Np^Q*(2M+1)^P`        (d=130 cell, TRUE — Lean `newGE130`)
- `value_record < c`   <=> `RNm^Q < RNp^Q*(2*RM+1)^P`     (d=80 record, TRUE — Lean `recLT130`)
with `c-1 = 353/2000`. No float decides anything. The GHR analytic step (`theta(U) >= c`
=> arbitrarily large extremal A,B => `C_3a >= c`) is the named hypothesis `GHR_lower`, not an
axiom (same trust pattern as 9a `ThetaGeFromIndep`, 5b `MTThm15`).

### Trust split (integers)
The three d=130 integers are TRUSTED literals (R19/R13 split): the kernel does only the
power arithmetic; the integers' provenance is re-derived OUT of Lean by `verify_beat.py
--recompute` (carry-free `digit_dp.count_opset`). Recomputing the carry-free DP inside the
Lean kernel is an OOM hazard and is deliberately NOT done.

## Certificate
- `lean/Constants/C3a.lean` — theorems `newGE130`, `recLT130`, `c3a_ge_2353_2000(')`.
  Build target `Constants.C3a`; `#print axioms` as above.
- `constants/3a/certificate/beat_d130/{verify_beat.py, beat_d130.json, README.md}`.
- `constants/3a/certificate/sweep/climb_state.json::d130_T244` — the persisted exact integers.

## How to push further
- Climb `d` further (d=160, 200) at the same density for a larger headline — but each cell's
  digit-DP is ~440s (d=130) and grows; persist integers BEFORE any wedge step, and keep the
  Lean wedge denominator Q <= ~2000 to stay below the kernel blowup.
- The asymptote (R21 reshape screen): value -> 1 + rinf/log(B) ~ 1.179 for this shape, so the
  d-climb saturates near ~1.179 — d=130 at 1.1768 is already ~93% of the way. A bigger jump
  needs a different alphabet shape (closed within digit alphabets per R21) or a non-digit
  construction.
