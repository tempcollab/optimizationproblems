# alphabet-reshape-screen — C_3a (GHR sum-difference constant)

**Type:** SCOUT (non-treadmill hedge). Movable side = LOWER bound. This angle certifies
NO finite bound by itself — it screens whether a reshaped digit-alphabet has a higher
`d→∞` asymptote than the current drop-1 record family, which (if found) would open a
NON-treadmill road past the digit-set method's ~1.1788 plateau on the held family.

**Held bar (NOT moved by this angle):** C_3a ≥ 5877/5000 = 1.1754 (R18-verified, R19
Lean-machine-checked).

## Idea
The bound is `value(U) = 1 + log(|U−U|/|U+U|) / log(2·max(U)+1)` for the base-B carry-free
digit set `U(A,B,d,T)` (GHR2007). Decompose into per-digit rates:
- `rnum(d) = log(|U−U|/|U+U|)/d` — numerator entropy rate, CLIMBS with d.
- `rden(d) = log(2·max(U)+1)/d → log(B)` — converges fast (max(U) ~ B^(d-1)).
- `value(d→∞) = 1 + rinf/log(B)`, `rinf = lim rnum(d)`.

So the d→∞ asymptote of a shape is governed by `rinf/log(B)`: a winning shape raises the
difference-set entropy per digit FASTER than it raises log(B). Griego beat Zheng precisely
by reshaping (drop digit 1) the full {0..B} alphabet. The question: is there a further
reshape that wins?

## What was done (Round 21)
Screened 17 alphabet shapes at small d (d ≤ 40, every cell fast, zero force-kill risk) with
EXACT carry-free digit-DP counts (`certificate/engine/digit_dp.py::count_opset`), floats only
for the rate display. For each shape: pick the best density near the known optimum, measure
`rnum(d)` at three small d's, extrapolate `rinf` (two-point `rnum=rinf−c/d`), asymptote
`1+rinf/log(B)`. Re-runnable: `certificate/reshape_screen/screen.py` (groups light/smallmax/
bigmax + `rank`), raw + combined results in `reshape_screen/results*.json`.

### Shapes screened and extrapolated asymptotes (combined ranking)
| asymptote | shape | A | B | rinf |
|-----------|-------|---|---|------|
| **1.17698** | **drop-1 (RECORD)** | {0,2..10} | 21 | 0.5388 |
| 1.17632 | drop-1 max12 | {0,2..12} | 25 | 0.5675 |
| 1.17444 | drop-1 max14 | {0,2..14} | 29 | 0.5874 |
| 1.17382 | drop-1 max8 | {0,2..8} | 17 | 0.4925 |
| 1.17088 | drop-1-and-2 | {0,3..10} | 21 | 0.5202 |
| 1.16315 | drop-1 max20 | {0,2..20} | 41 | 0.6059 |
| 1.16242 | drop-1-and-mid(6) | {0,2,3,4,5,7..10} | 21 | 0.4945 |
| 1.15966 | drop-1-2 max16 | {0,3..16} | 33 | 0.5582 |
| 1.15895 | full {0..10} | {0..10} | 21 | 0.4839 |
| 1.15276 | drop-1 max6 | {0,2..6} | 13 | 0.3918 |
| 1.14633 | drop-1-5-9 (drop 1,5,9) | {0,2,3,4,6,7,8,10} | 21 | 0.4455 |
| 1.14540 | drop-1-2-3 | {0,4..10} | 21 | 0.4427 |
| 1.13051 | AP-step2 | {0,2,4,6,8,10} | 21 | 0.3974 |
| 1.12417 | drop-1 max5 | {0,2..5} | 11 | 0.2978 |
| 1.10227 | AP-step3 | {0,3,6,9} | 21 | 0.3114 |
| 1.08736 | drop-1 max4 | {0,2..4} | 9 | 0.1920 |
| 1.07975 | drop-1 max3 | {0,2,3} | 7 | 0.1552 |

(Plus `sparse-ends {0,2,9,10}`, screened separately: value ~1.05, a confirmed non-contender
with a slow d=35 mask, dropped from the catalogue.)

The screen's d∈{15,25,35} fit slightly UNDER-estimates (small-d lag); a higher-d check at
d∈{20,30,40}, density 1.875, gives the record family **1.17897** (matching the explorer's
~1.1788 reference) vs its closest competitor max12 B=25 **1.17708** — a ~1.9e-3 gap.

## Hard step — answered
**Does ANY reshaped alphabet's extrapolated asymptote exceed the drop-1 family's ~1.1788?**
**NO.** Every shape screened loses, and the loss has a clean structural reason:
- **Bigger max / bigger B** (max12/14/20): raises `rinf` (more per-digit entropy) but log(B)
  grows FASTER, so `rinf/log(B)` falls. The numerator gain is sub-logarithmic in max(A).
- **Smaller max / smaller B** (max3..8): lowers log(B) but `rinf` collapses even faster
  (fewer distinct differences), net worse.
- **Dropping more digits** (drop-1-2, drop-1-2-3, drop-mid, AP-step): each removed digit
  shrinks the difference-set spread faster than the sum-set, lowering `rinf`. Drop-1 is the
  sweet spot — dropping exactly the single digit `1` maximizes diff/sum asymmetry without
  killing entropy.
- **Full {0..10}** (no drop): 1.15895, confirming Griego's drop-1 beat over the full
  alphabet from first principles.

**Conclusion:** the drop-1 base-21 family is near-optimal among digit-alphabet shapes. The
digit-set method is confirmed near its ceiling on this family; the run is near its honest
productive plateau. No new bound-move road opens from reshaping.

## Value claimed
**No bound claimed** (this is a scout). The *information* delivered: the reshape road is
**closed** — drop-1 B=21 wins the shape screen, so the only remaining digit-set bound-move
lever is the d-push on the existing family (`push-d-130-exact-beat`).

## What would push this further
- A genuinely DIFFERENT ansatz beyond `value=1+rinf/log(B)` digit alphabets: a non-uniform
  per-position alphabet (different A_i at different positions), a non-digit-set structured U
  (the `beyond-digit-set-structured-U` speculative angle), or a multi-base construction.
  These break the single-`log(B)` denominator that caps every shape here.
- A wider density scan at the small-max shapes (their grids peaked at the grid edge ~1.73);
  unlikely to flip the verdict (they lose by 2–10e-3) but would tighten the band.
- If a future explorer finds a shape with `rinf/log(B) > 0.5806` (= the record's
  d→∞ `rinf≈0.5445 / log(21)`), THAT shape becomes a d-push target — but none of the 17
  screened here, including all sensible drop/gap/base variants, comes close.
