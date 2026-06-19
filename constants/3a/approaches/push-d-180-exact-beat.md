# push-d-180-exact-beat

## Idea
Same proven carry-free drop-1 base-21 GHR digit lever as the seven prior verified bound moves
(R18 d=100, R19 Lean port, R22 d=130, R23 d=140, R24 d=150, R25/R26 d=160, R28 d=170), walked
one rung further to **d=180** — the seventh / capstone bound move. Fixed alphabet
`A = {0,2,3,4,5,6,7,8,9,10}`, `B = 21`, cap `T = 338` (density ≈ 1.8778). Carry-free holds
because `B = 21 > 2·max(A) = 20`, so `|U±U|` are exact, DP-countable integers — no continuum
estimate anywhere. The slack the d-push exploits is the unsaturated per-digit numerator rate
`rnum(d)`, still climbing toward `rinf ≈ 0.552` (asymptote `1 + rinf/log 21 ≈ 1.1813`); G2026
fixed d=80 below its own density limit, so larger d strictly increases the bound.

GHR2007 lower bound: `C_3a ≥ 1 + log(|U−U|/|U+U|) / log(2·max(U)+1)`
(digest: `constants/3a/literature/GHR2007-lemma-digest.md`).

## Status — CLAIMED (R29), Lean-machine-checked, awaiting reviewer verification
**Claimed lower bound: C_3a ≥ 86/73 = 1.1780821917808…**, strictly beating the R28 held
`53/45 = 1.1777777778…` by **+3.044e-4** (exact `Fraction`). This is a CLAIM until the
reviewer re-establishes it; do NOT treat the value as `held` until then.

### Cell (the fresh d=180 DP)
- `A = {0,2,3,4,5,6,7,8,9,10}`, `B = 21`, `d = 180`, `T = 338`, density ≈ 1.8778.
- Exact counts (persisted `constants/3a/certificate/beat_d180/beat_d180.json`, cell `d180_T338`):
  - `|U+U|` = 175-digit int
  - `|U−U|` = 217-digit int
  - `max(U)` = 238-digit int
- True GHR value (float, display only): **1.1781127097299942**.
- DP cost / split protocol (the load-bearing anti-stuck fix):
  - diff/max (`run_d180_diffmax.py`, collapsed `minSa`-state, op='−' + max): **247.1s**,
    persisted to `d180_diffmax.json` in its OWN call — NOT recomputed.
  - heavy sumset `|U+U|` (mask width T+1 = 339): **1327.5s** in its own dedicated
    `timeout 2400` call, run via the **progress-emitting copy** `sumset_progress.py` of the
    `_count_plus` DP (prints `pos k/180 states=… t=…s` after EACH of the 180 positions, so the
    watchdog never sees >~20s of silence — the bare silent engine call is the force-kill trap
    that killed the R25/R27 builders). The progress-copy was VALIDATED bit-for-bit against the
    trusted engine `count_opset` (op='+') on small cells (d=20/T=38, d=25/T=47, d=18/T=33 — all
    MATCH=True) BEFORE being trusted at d=180.
  - The sumset was persisted to `beat_d180.json` the instant it finished, BEFORE the wedge/Lean
    steps. DP + wedge + Lean were NEVER run as one call.

### Wedge (load-bearing exact big-int inequality)
Chosen by the EXACT `Nm^Q ≥ Np^Q·(2M+1)^P` test in Python `Fraction` against the MEASURED
d=180 integers (never the float), in `constants/3a/certificate/beat_d180/wedge_check.py`:
- **c = 86/73 = 1 + 13/73**, `P = 13`, `Q = 73` — the LARGEST-headline reduced wedge with
  `Q ≤ 200` that the exact integers clear strictly above held and below `value_new` (an
  automated scan over all reduced `k/Q`, `2 ≤ Q ≤ 200`, confirmed 86/73 is the maximum; `87/73`
  with P=14 FAILS the beat cell, so 86/73 is maximal at Q=73). This **improves on the outline's
  predicted candidate `139/118 = 1.1779661`** (P=21, Q=118), which also passes but has a smaller
  margin (+1.88e-4 over held) and a larger Q. `Q = 73` is trivial for `decide` (~52600-bit power
  inequality, ≪ R22's Q=2000 ~11.5s; nowhere near the R21 Q=10000 force-kill trap).
- (a) `value_new ≥ c`: `|U−U|^73 ≥ |U+U|^73·(2·max(U)+1)^13` — **PASSES** (lhs 52603 bits ≥ rhs
  52601 bits; independent fresh re-derivation).
- (b) `value_record < c`: d=80 record cell `RNm^73 < RNp^73·(2·RM+1)^13` — record cell does NOT
  pass (strictness ⇒ strict over the true record 1.1740744476935212, not the table truncation).
  Confirmed via `record_baseline.json` integers.
- (c) `c > 53/45` (held, +3.044e-4) exactly via `Fraction`; also `> 179/152`, `> 239/203`,
  `> 1177/1000`, `> 2353/2000`, `> 5877/5000`, `> 1.1740744476935212` (record).

### Certificates
- **Numerical** `constants/3a/certificate/beat_d180/`:
  - `d180_diffmax.json` — persisted exact `|U−U|` + `max(U)` (diff/max, 247.1s).
  - `beat_d180.json` — persisted exact `|U+U|`, `|U−U|`, `max(U)`, value (the full cell).
  - `sumset_progress.py` — progress-emitting copy of the `_count_plus` DP; `validate`
    cross-checks bit-for-bit vs the engine `count_opset`, `run 338` re-derives the sumset.
  - `run_d180_diffmax.py` — the diff/max DP driver.
  - `wedge_check.py` — re-derives both wedge inequalities + the held/record comparisons in
    fresh `Fraction`/big-int, and scans for the largest passing Q≤200 wedge.
  - `CERT.md` — documents the cell, wedge, literals, and re-verification recipe.
- **Lean** (gold standard) `lean/Constants/C3a.lean`, theorems added (all SEVEN prior
  theorems left untouched): `Nplus180`, `Nminus180`, `maxU180`, `P7`, `Q7`, `newGE180`,
  `recLT180`, `Nplus180_pos`, `Nplus180_le_Nminus180`, `Q7_pos`, `c3a_ge_86_73`,
  `c3a_ge_86_73'`.
  - Build: `lake build Constants` (from `lean/`) → **PASS** (8571 jobs; `Constants.C3a` built
    in 14s; Mathlib pinned v4.31.0).
  - Axiom audit (`#print axioms` via `lake env lean`): `newGE180`/`recLT180` = `[propext]`
    only (pure kernel `decide`, NO `native_decide`/`ofReduceBool`/`sorryAx`/new axiom);
    `c3a_ge_86_73(')` = `[propext, Classical.choice, Quot.sound]` (standard ℝ trio, same as the
    R19/R22/R23/R24/R25/R28 theorems). Only trust boundary is the named hypothesis `GHR_lower`.

## How to push further
- **The digit-set lever is now essentially exhausted for round-sized compute.** d=180 is the
  last comfortable single-call rung: the sumset took 1327.5s (mask width 339); d=190 (T≈356)
  ≈1900–2200s crosses the single-call force-kill edge, d=200 is over it. Only ~3.2e-3 of
  asymptotic runway remains to the ≈1.1813 family asymptote, each further rung buying only
  ~+1.5–2e-4 at superlinearly-rising DP cost. The outline-reviewer's explicit ruling: take the
  d=180 capstone, then **declare the digit-set lever exhausted at d=180** (do NOT start a d≥190
  treadmill). This approach realizes that capstone.
- The drop-1 base-21 SHAPE is the proven optimum (reshape screen R21/R22 negative; asymptote
  ≈ 1.1813). The reshape road is CLOSED.
- A real jump past the digit-set ceiling needs a NON-digit / non-carry-free `U`
  (`beyond-digit-set-structured-U`), which has no concrete construction in hand and would
  likely lose the clean `|U±U| = |block|^d` factorization (hence the Lean-fit exact-integer
  cert path). Speculative, not round-sized.
