# Alphabet-reshape screen — C_3a, Round 21 (SCOUT, no bound certified)

This is a **scout**, not a bound-move build. It screens alternative digit-alphabet SHAPES
at small `d` to see whether any family's extrapolated `d→∞` asymptote beats the current
drop-1 record family's `~1.1788` ceiling. **It certifies NO bound** — any winning shape
would be a *conjecture* for a future d-push build. Nothing here enters `constants/3a.md`.

## Files
- `screen.py` — the re-runnable screen. Exact carry-free digit-DP counts
  (`../engine/digit_dp.py::count_opset`, big-ints); floats appear only in the rate/asymptote
  DISPLAY.
- `results_{light,smallmax,bigmax}.json` — per-group raw cells.
- `results.json` — combined ranking.

## How to re-run
```
cd constants/3a/certificate/reshape_screen
timeout 120 python3 screen.py light       # max<=10, B=21 shapes
timeout 120 python3 screen.py smallmax    # smaller max/base shapes
timeout 200 python3 screen.py bigmax      # larger max shapes (slower cells)
python3 screen.py rank                     # combine + print ranking
```
Each group resumes from its flushed `results_<group>.json` (a killed run loses nothing).
All cells are `d ≤ 40` (zero force-kill risk); the heaviest cell is ~28s.

## Method
GHR2007 lemma: `value(U) = 1 + log(|U−U|/|U+U|) / log(2·max(U)+1)`, `U(A,B,d,T)` the
base-B carry-free digit set (`B > 2·max(A)`). Per-digit rates
`rnum(d)=log(|U−U|/|U+U|)/d` (climbs with d) and `rden(d)=log(2max+1)/d → log B`. Hence
`value(d→∞) = 1 + rinf/log(B)`, `rinf = lim rnum(d)`. We measure exact counts at three
small d's (per shape), pick the best density near the known optimum, and extrapolate
`rnum(d)=rinf−c/d` from the two largest d's. Same monotone-numerator method the R18/R20
explorers validated to ~6e-4.

## Verdict (see results.json for the full ranking)
**NO reshaped alphabet beats the drop-1 record family.** Top of the ranking:

| asymptote | shape | B | reason it loses |
|-----------|-------|---|-----------------|
| **1.17698** | **drop-1 (RECORD) {0,2..10}** | 21 | the incumbent |
| 1.17632 | drop-1 max12 {0,2..12} | 25 | higher rinf but log(B) grows faster |
| 1.17444 | drop-1 max14 {0,2..14} | 29 | same |
| 1.17382 | drop-1 max8 {0,2..8} | 17 | smaller B but rinf drops more |
| 1.17088 | drop-1-and-2 {0,3..10} | 21 | losing digit 2 hurts the diff-set entropy |

(Asymptotes from the screen's d∈{15,25,35} fit slightly UNDER-estimate — the better
d∈{20,30,40} fit at density 1.875 gives record **1.17897** vs its closest competitor
max12 B=25 **1.17708**, a ~1.9e-3 gap.) The drop-1 family is confirmed near-optimal among
digit-alphabet shapes; the digit-set method is at its honest productive plateau on this
family. The bound move this round (if any) remains the d-push on the existing drop-1
family (`push-d-130-exact-beat`).
