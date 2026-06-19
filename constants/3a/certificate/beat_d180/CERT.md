# C_3a d=180 beat certificate (R29, the seventh / capstone bound move)

## Claim
`C_3a ≥ 86/73 = 1.1780821917808…`, strictly beating the held `53/45 = 1.1777777778…`
(R28) by **+3.044e-4** (exact `Fraction`), and the true published record
`1.1740744476935212` [G2026] by ~3.96e-3.

This is a CLAIM until the reviewer re-establishes it. Do NOT treat it as `held` until then.

## Construction (carry-free drop-1 base-21 GHR digit set)
- Alphabet `A = {0,2,3,4,5,6,7,8,9,10}`, base `B = 21`, depth `d = 180`, cap `T = 338`
  (density `338/180 ≈ 1.8778`).
- Carry-free regime: `B = 21 > 2·max(A) = 20`, so `|U±U|` and `max(U)` are exact integers
  (digit-DP-countable; no continuum estimate).
- `U = { Σ_{i=0}^{179} a_i·21^i : a_i ∈ A, Σ a_i ≤ 338 }`.
- GHR2007 lower bound: `C_3a ≥ 1 + log(|U−U|/|U+U|) / log(2·max(U)+1)`
  (digest: `constants/3a/literature/GHR2007-lemma-digest.md`).

## Exact integers (persisted `beat_d180.json`, cell `d180_T338`)
- `|U+U|` = 175-digit int
- `|U−U|` = 217-digit int
- `max(U)` = 238-digit int
- True GHR value (float, display only): **1.1781127097299942**.

## DP cost / split protocol (the anti-stuck fix)
- diff/max (`run_d180_diffmax.py`, collapsed `minSa`-state op='−' + greedy max): **247.1s**,
  persisted to `d180_diffmax.json` in its own call — NOT recomputed later.
- heavy sumset `|U+U|` (mask width `T+1 = 339`): **1327.5s** in its own dedicated
  `timeout 2400` call, run via the **progress-emitting copy** `sumset_progress.py`
  (prints `pos k/180 states=… t=…s` after EACH of the 180 positions; never >~20s silent).
  The progress-copy was VALIDATED bit-for-bit vs the trusted engine `count_opset` (op='+')
  on small cells (d=20/T=38, d=25/T=47, d=18/T=33 — all MATCH=True) BEFORE being trusted at
  d=180.
- `beat_d180.json` was persisted the INSTANT the sumset finished, BEFORE any wedge/Lean step.

## Wedge (load-bearing exact big-int inequality), `wedge_check.py`
Selected by the EXACT `Nm^Q ≥ Np^Q·(2M+1)^P` test in Python `Fraction` against the MEASURED
integers (never the float):
- **c = 86/73 = 1 + 13/73**, `P = 13`, `Q = 73` — the LARGEST-headline reduced wedge with
  `Q ≤ 200` that the exact integers clear strictly above held and below `value_new`. An
  automated scan over all reduced `k/Q`, `2 ≤ Q ≤ 200`, confirmed `86/73` is the maximum;
  `87/73` (P=14) FAILS the beat cell, so `86/73` is maximal at `Q = 73`.
  - This improves on the outline's predicted candidate `139/118 = 1.1779661` (P=21, Q=118),
    which also passes but has a smaller margin (+1.88e-4) and larger Q.
  - `Q = 73` is trivial for `decide` (the power inequality is ~52600-bit; ≪ R22's Q=2000;
    nowhere near the R21 Q=10000 force-kill trap).
- (a) `value_new ≥ c`: `|U−U|^73 ≥ |U+U|^73·(2·max(U)+1)^13` — **PASSES** (lhs 52603 bits ≥
  rhs 52601 bits, independent fresh re-derivation).
- (b) `value_record < c`: d=80 record cell `RNm^73 < RNp^73·(2·RM+1)^13` — record cell does
  NOT pass (strictness ⇒ strict over the true record 1.1740744476935212, not the table
  truncation). Confirmed via `../sweep/record_baseline.json` integers.
- (c) `c > 53/45` (held, +3.044e-4) exactly via `Fraction`; also `> 179/152`, `> 239/203`,
  `> 1177/1000`, `> 2353/2000`, `> 5877/5000`, `> 1.1740744476935212` (record).

## Files
- `d180_diffmax.json` — persisted exact `|U−U|` + `max(U)` (diff/max, 247.1s).
- `beat_d180.json` — persisted exact `|U+U|`, `|U−U|`, `max(U)`, value (the full cell).
- `sumset_progress.py` — progress-emitting copy of `_count_plus`; `validate` cross-checks
  bit-for-bit vs the engine `count_opset`, `run 338` re-derives the sumset.
- `run_d180_diffmax.py` — the diff/max DP driver.
- `wedge_check.py` — re-derives both wedge inequalities + held/record comparisons in fresh
  `Fraction`/big-int, and scans for the largest passing Q≤200 wedge.

## Lean certificate (gold standard) — `lean/Constants/C3a.lean`
Theorems ADDED (all seven prior theorems left untouched):
`Nplus180`, `Nminus180`, `maxU180`, `P7`, `Q7`, `newGE180`, `recLT180`, `Nplus180_pos`,
`Nplus180_le_Nminus180`, `Q7_pos`, `c3a_ge_86_73`, `c3a_ge_86_73'`.
- Build: `lake build Constants` (from `lean/`) → **PASS** (8571 jobs; `Constants.C3a` built
  in 14s; Mathlib pinned v4.31.0).
- Axiom audit (`#print axioms` via `lake env lean`):
  - `newGE180` / `recLT180` = `[propext]` only (pure kernel `decide`, NO
    `native_decide`/`ofReduceBool`/`sorryAx`/new axiom).
  - `c3a_ge_86_73` / `c3a_ge_86_73'` = `[propext, Classical.choice, Quot.sound]` (standard ℝ
    trio, same as every prior theorem). Only trust boundary is the named hypothesis
    `GHR_lower`.

## Re-verification recipe (reviewer)
1. `python3 sumset_progress.py validate` (small-cell bit-for-bit vs engine — ~2s).
2. (optional full recompute, ~1330s in its own ≥2400s call)
   `python3 sumset_progress.py run 338`; diff/max via `python3 run_d180_diffmax.py` (~250s).
   Otherwise load the persisted integers.
3. `python3 wedge_check.py` — both inequalities + held/record comparisons re-derived fresh.
4. `lake build Constants` from `lean/`; `#print axioms C3a.newGE180 C3a.recLT180
   C3a.c3a_ge_86_73`.
