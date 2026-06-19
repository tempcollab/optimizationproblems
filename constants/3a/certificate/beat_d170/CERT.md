# C_3a d=170 beat certificate (R28)

## Claim
`C_3a ≥ 53/45 = 1.1777777778…`, strictly beating the held `179/152 = 1.1776315789…` (R26)
by **+1.462e-4** (exact `Fraction`). CLAIM until reviewer-verified.

## The cell (carry-free drop-1 base-21 GHR digit set)
- `A = {0,2,3,4,5,6,7,8,9,10}`, base `B = 21`, `d = 170`, cap `T = 319` (density ≈ 1.8765).
- Carry-free regime: `B = 21 > 2·max(A) = 20`, so `|U±U| = |block±block|^d` are exact integers
  computed by the digit-DP (no continuum estimate).
- Exact counts (in `beat_d170.json`, cell `d170_T319`):
  - `|U+U|` (Nplus) = 165 digits
  - `|U−U|` (Nminus) = 205 digits
  - `max(U)` (maxU) = 225 digits
- True GHR value (float, display only): `1.1779005456617866`.

## The wedge
`c = 53/45 = 1 + 8/45`, so `P = 8`, `Q = 45`. GHR `θ(U) ≥ c ⟺
|U−U|^Q ≥ |U+U|^Q · (2·max(U)+1)^P` (monotone log-free chain; digest
`constants/3a/literature/GHR2007-lemma-digest.md`).
- (a) d=170 cell PASSES: `Nminus^45 ≥ Nplus^45 · (2·maxU+1)^8`.
- (b) d=80 RECORD cell FAILS: `recNminus^45 < recNplus^45 · (2·recMaxU+1)^8` (⇒ strict over the
  true record `1.1740744476935212`, not the table truncation `1.1740744`).
- (c) `53/45 > 179/152` exactly (margin +1.462e-4); chosen as the largest reduced wedge with
  `Q ≤ 200` clearing the exact test.

## Files
- `d170_diffmax.json` — persisted exact `|U−U|`, `max(U)` (diff/max DP, ~186s; not recomputed).
- `beat_d170.json` — persisted exact `|U+U|`, `|U−U|`, `max(U)`, value (full cell, sumset ~980s).
- `sumset_progress.py` — progress-emitting COPY of the engine `_count_plus` DP. Prints
  `pos k/170 states=… t=…s` after each position (anti-stuck; the silent engine call was the
  prior-round force-kill trap).
- `wedge_check.py` — re-derives (a)/(b)/(c) in fresh `Fraction`/big-int; scans Q≤200.
- `run_d170_diffmax.py`, `run_d170_engine.py` — prior-call helpers (diffmax + bare engine sumset).

## How to re-verify (NO forced full-d recompute)
1. Validate the sumset DP copy against the trusted engine (small cells, ~3s):
   `python3 sumset_progress.py validate`   → expect `ALL_MATCH=True`.
2. Confirm the wedge inequalities + held/record comparisons (loads persisted integers, instant):
   `python3 wedge_check.py`                → expect `VERDICT (valid strict beat) : True`.
3. (Optional, ~16 min) Re-derive the d=170 sumset from scratch with live progress:
   `python3 sumset_progress.py run 319`    → rewrites `beat_d170.json`; matches the persisted int.
   The diff/max are in `d170_diffmax.json`; re-derive with `python3 run_d170_diffmax.py` (~186s).
4. Gold standard — Lean: from `lean/`, `lake build Constants` (theorem
   `C3a.c3a_ge_53_45'`), and `#print axioms C3a.c3a_ge_53_45` (standard ℝ trio),
   `#print axioms C3a.newGE170` (`[propext]` only).

Do NOT run a `verify_beat.py --recompute` at d=170 (it re-derives the ~16-min sumset inline —
the force-kill trap). Use the persisted integers + the small-cell validation instead.
