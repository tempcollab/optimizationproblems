# push-d-170-exact-beat

## Idea
Same proven carry-free drop-1 base-21 GHR digit lever as the six prior verified bound moves
(R18 d=100, R19 Lean port, R22 d=130, R23 d=140, R24 d=150, R25/R26 d=160), walked one rung
further to **d=170**. Fixed alphabet `A = {0,2,3,4,5,6,7,8,9,10}`, `B = 21`, cap `T = 319`
(density ≈ 1.8765). Carry-free holds because `B = 21 > 2·max(A) = 20`, so
`|U±U| = |block±block|^d` are exact, DP-countable integers — no continuum estimate anywhere.
The slack the d-push exploits is the unsaturated per-digit numerator rate `rnum(d)`, still
climbing toward `rinf ≈ 0.552` (asymptote `1 + rinf/log 21 ≈ 1.1813`); G2026 fixed d=80 below
its own density limit, so larger d strictly increases the bound.

GHR2007 lower bound: `C_3a ≥ 1 + log(|U−U|/|U+U|) / log(2·max(U)+1)`
(digest: `constants/3a/literature/GHR2007-lemma-digest.md`).

## Status — CLAIMED (R28), Lean-machine-checked, awaiting reviewer verification
**Claimed lower bound: C_3a ≥ 53/45 = 1.1777777778…**, strictly beating the R26 held
`179/152 = 1.1776315789…` by **+1.462e-4** (exact Fraction). This is a CLAIM until the
reviewer re-establishes it; do NOT treat the value as `held` until then.

### Cell (the fresh d=170 DP)
- `A = {0,2,3,4,5,6,7,8,9,10}`, `B = 21`, `d = 170`, `T = 319`, density ≈ 1.8765.
- Exact counts (persisted `constants/3a/certificate/beat_d170/beat_d170.json`, cell `d170_T319`):
  - `|U+U|` = 165-digit int
  - `|U−U|` = 205-digit int
  - `max(U)` = 225-digit int
- True GHR value (float, display only): **1.1779005456617866**.
- DP cost / split protocol (the load-bearing anti-stuck fix this round):
  - diff/max (`run_d170_diffmax.py`, collapsed `minSa`-state, op='−' + max): ≈ 186s, persisted
    to `d170_diffmax.json` in a prior call — NOT recomputed.
  - heavy sumset `|U+U|` (mask width T+1 = 320): ≈ **980s** in its own dedicated
    `timeout 2400` call. The previous round's builder was force-killed because it ran the
    sumset as a single SILENT engine call; this round it was run via a **progress-emitting
    copy** of the `_count_plus` DP (`sumset_progress.py`) that prints `pos k/170 states=… t=…s`
    after EACH of the 170 positions, so the watchdog never sees >~6s of silence.
    The progress-copy was VALIDATED bit-for-bit against the trusted engine `count_opset`
    (op='+') on small cells (d=20/T=38, d=25/T=47, d=18/T=33 — all MATCH=True) BEFORE being
    trusted at d=170.
  - The sumset was persisted to `beat_d170.json` the instant it finished, BEFORE the wedge/Lean
    steps. DP + wedge + Lean were NEVER run as one call.

### Wedge (load-bearing exact big-int inequality)
Chosen by the EXACT `Nm^Q ≥ Np^Q·(2M+1)^P` test in Python `Fraction` first (never the float),
in `constants/3a/certificate/beat_d170/wedge_check.py`:
- **c = 53/45 = 1 + 8/45**, `P = 8`, `Q = 45` — the LARGEST-headline reduced wedge with
  `Q ≤ 200` that the exact integers clear strictly above held and below `value_new` (an
  automated scan over all reduced `k/Q`, `2 ≤ Q ≤ 200`, confirmed 53/45 is the maximum). The
  measured value 1.17790 is only ~+1.2e-4 above 53/45, too tight for a cleaner small-Q rational
  in between. `Q = 45` is trivial for `decide` (≪ R22's Q=2000 ~11.5s; nowhere near the R21
  Q=10000 force-kill trap).
- (a) `value_new ≥ c`: `|U−U|^Q ≥ |U+U|^Q·(2·max(U)+1)^P` — **PASSES**.
- (b) `value_record < c`: d=80 record cell `RNm^Q < RNp^Q·(2·RM+1)^P` — record cell does NOT
  pass (strictness ⇒ strict over the true record 1.1740744476935212, not the table
  truncation). Confirmed via `record_baseline.json` integers.
- (c) `c > 179/152` (held, +1.462e-4) exactly via Fraction; also `> 239/203`, `> 1177/1000`,
  `> 2353/2000`, `> 5877/5000`, `> 1.1740744476935212` (record).

### Certificates
- **Numerical** `constants/3a/certificate/beat_d170/`:
  - `d170_diffmax.json` — persisted exact `|U−U|` + `max(U)` (diff/max, ≈186s).
  - `beat_d170.json` — persisted exact `|U+U|`, `|U−U|`, `max(U)`, value (the full cell).
  - `sumset_progress.py` — progress-emitting copy of the `_count_plus` DP; `validate`
    cross-checks bit-for-bit vs the engine `count_opset`, `run <T>` re-derives the sumset.
  - `wedge_check.py` — re-derives both wedge inequalities + the held/record comparisons in
    fresh `Fraction`/big-int, and scans for the largest passing Q≤200 wedge.
  - `CERT.md` — documents the cell, wedge, literals, and how to re-verify WITHOUT a forced
    full-d recompute (load the persisted integers; the progress-copy + small-cell validation
    is the re-derivation path).
- **Lean** (gold standard) `lean/Constants/C3a.lean`, theorems added (all prior theorems
  `c3a_ge_5877_5000`, `c3a_ge_2353_2000`, `c3a_ge_1177_1000`, `c3a_ge_239_203`,
  `c3a_ge_179_152` + their `newGE*`/`recLT*` left untouched):
  `newGE170`, `recLT170`, `Nplus170_pos`, `Nplus170_le_Nminus170`, `Q6_pos`,
  `c3a_ge_53_45`, `c3a_ge_53_45'`.
  - Build: `lake build Constants` (from `lean/`) → **PASS** (8571 jobs; `Constants.C3a` built
    in 32s; Mathlib pinned v4.31.0).
  - Axiom audit (`#print axioms` via `lake env lean`): `newGE170`/`recLT170` = `[propext]`
    only (pure kernel `decide`, NO `native_decide`/`ofReduceBool`/`sorryAx`/new axiom);
    `c3a_ge_53_45(')` = `[propext, Classical.choice, Quot.sound]` (standard ℝ trio, same as the
    R19/R22/R23/R24/R25 theorems). Only trust boundary is the named hypothesis `GHR_lower`.

## How to push further
- **Next rung: d=180 / T≈338** (predicted ≈ 1.17800, only ~+1.0e-4 over this d=170 cell).
  Same lever, same split protocol. CAUTION (verified cost model): the sumset is superlinear in
  T and d — d=150/T=282 took 772.5s, d=160/T=300 took 1051.6s, d=170/T=319 took ~980s (this
  run, with the progress-copy). d=180/T≈338 (mask width ~339) is estimated ~1100–1400s; it MUST
  get its own `timeout ≥ 2400` call with the progress-emitting copy. diff/max grows too. Do NOT
  co-build with another push-d cell, and NEVER run the d-cell DP as a silent engine call (the
  force-kill trap — use `sumset_progress.py`).
- The drop-1 base-21 SHAPE is the proven optimum (reshape screen R21/R22 negative; asymptote
  ≈ 1.1813). After d=170 only ~**3.3e-3** of asymptotic runway remains on this lever, approached
  with diminishing per-rung gain (≈ +1.5e-4 per rung now and shrinking) and rising DP cost — an
  honest treadmill near its long flat tail. Weigh whether further marginal +e-4 rungs justify a
  full heavy-DP round.
- A real jump past the digit-set ceiling needs a NON-digit / non-carry-free `U`
  (`beyond-digit-set-structured-U`), which has no concrete construction in hand and loses the
  clean `|U±U| = |block|^d` factorization (hence the Lean-fit cert path). Not recommended over
  the near-certain marginal d-rung unless a concrete lead appears.
