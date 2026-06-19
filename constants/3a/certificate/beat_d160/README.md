# beat_d160 — C_3a strict-beat certificate (Round 25, d=160 cell)

Strict lower-bound beat **C_3a ≥ 179/152 = 1.1776316**, over R24 held 239/203 = 1.1773399
(margin +2.917e-4). See `CERT.md` for the full write-up.

## Files
- `CERT.md` — full certificate write-up (claim, construction, integers, wedge, Lean target,
  `#print axioms`).
- `beat_d160.json` — the persisted exact integers (`|U+U|`, `|U−U|`, `max(U)`) for cell
  `d160_T300`, plus the chosen wedge (P=27, Q=152, c=179/152).
- `d160_diffmax.json` — persisted cheap diff/max counts for T∈{299,300}.
- `verify_beat.py` — re-runnable numerical certificate. `python3 verify_beat.py` (loads
  persisted, ~80s, exit 0 "CERTIFICATE OK"); `--recompute` re-derives the d=160 integers from
  scratch (~1300s) and bit-checks them.
- `run_d160_diffmax.py` — Call A: cheap diff/max DP (split-call template, `timeout 600`).
- `run_d160_engine.py` — Call B: heavy sumset DP (split-call template, `timeout 2400`).

## Lean
- Target: `cd lean && lake build Constants`   (builds `Constants.C3a`; PASS, 8571 jobs, 129s).
- Theorems: `newGE160`, `recLT160` (`[propext]`-only kernel `decide`),
  `c3a_ge_179_152`, `c3a_ge_179_152'` (`[propext, Classical.choice, Quot.sound]`).
- `#print axioms`: no `sorryAx`, no `Lean.ofReduceBool`, no new/smuggled axiom; `GHR_lower`
  is a named hypothesis (trust boundary), absent from `#print axioms`.
