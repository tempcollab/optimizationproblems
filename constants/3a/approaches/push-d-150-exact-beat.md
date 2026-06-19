# push-d-150-exact-beat

## Idea
Same proven carry-free drop-1 base-21 GHR digit lever as the four prior verified beats
(R18 d=100, R19 Lean port, R22 d=130, R23 d=140), walked one rung further to **d=150**.
Fixed alphabet `A = {0,2,3,4,5,6,7,8,9,10}`, `B = 21`, cap `T = 282` (density 1.8800).
Carry-free holds because `B = 21 > 2·max(A) = 20`, so `|U±U| = |block±block|^d` are exact,
DP-countable integers — no continuum estimate anywhere. The slack the d-push exploits is the
unsaturated per-digit numerator rate `rnum(d)`, still climbing toward `rinf ≈ 0.552`
(asymptote `1 + rinf/log 21 ≈ 1.1813`); G2026 fixed d=80 below its own density limit, so
larger d strictly increases the bound.

GHR2007 lower bound: `C_3a ≥ 1 + log(|U−U|/|U+U|) / log(2·max(U)+1)`
(digest: `constants/3a/literature/GHR2007-lemma-digest.md`).

## Status — CLAIMED (R24), Lean-machine-checked, awaiting reviewer verification
**Claimed lower bound: C_3a ≥ 239/203 = 1.1773399014778…**, strictly beating the R23 held
`1177/1000 = 1.1770` by **+3.40e-4** (exact Fraction). This is a CLAIM until the reviewer
re-establishes it; do NOT treat the value as `held` until then.

### Cell (the fresh d=150 DP)
- `A = {0,2,3,4,5,6,7,8,9,10}`, `B = 21`, `d = 150`, `T = 282`, density 1.8800.
- Exact counts (persisted `constants/3a/certificate/beat_d150/beat_d150.json`, cell `d150_T282`):
  - `|U+U|` = 146-digit int
  - `|U−U|` = 181-digit int
  - `max(U)` = 199-digit int
- True GHR value (float, display only): **1.1774136588225**.
- DP cost: diff/max ≈ 140s (collapsed `minSa`-state); heavy sumset (mask width T+1 = 283)
  ≈ **772.5s** — required its own `timeout`-wrapped call, per the R23 split protocol.
  I confirmed before launching that the diff/max fits one call (~140s/T) and the sumset
  fits one ≤60-min Bash call (~13 min).

### T-neighborhood check
Computed diff/max for `T ∈ {281,282,283}` cheaply (each ~140s). max(U) is 199 digits for all
three; `|U−U|` is 181 digits for all three. T=282 (density 1.8800) is the calibrated optimum
used; the sumset was run only for T=282 to stay within one heavy call.

### Wedge (load-bearing exact big-int inequality)
Chosen by the EXACT `Nm^Q ≥ Np^Q·(2M+1)^P` test in Python `Fraction` first (never the float):
- **c = 239/203 = 1 + 36/203**, `P = 36`, `Q = 203` — the LARGEST-headline wedge with `Q ≤ 250`
  that the exact integers clear (sweep top: 36/203 > 25/141 > 39/220 > 14/79).
- (a) `value_new ≥ c`: `|U−U|^Q ≥ |U+U|^Q·(2·max(U)+1)^P` — PASSES.
- (b) `value_record < c`: d=80 record cell `RNm^Q < RNp^Q·(2·RM+1)^P` — PASSES (strictness).
- `c > 1177/1000` (held), `> 2353/2000`, `> 5877/5000`, `> 1.1740744476935212` (record), all
  exact-rational. `Q = 203` is trivial for `decide` (≪ R22's Q=2000 ~11.5s; nowhere near the
  R21 Q=10000 force-kill).

### Certificates
- **Numerical** `constants/3a/certificate/beat_d150/verify_beat.py`:
  `python3 verify_beat.py` (loads persisted integers, ~80s) and `--recompute` (re-derives the
  d=150 DP from scratch). Re-establishes the record cell bit-for-bit vs `record_baseline.json`
  (PR #71), cross-checks the fast `count_opset` engine vs the independent Pareto `dp_engine` on
  small cells, and re-derives both wedge inequalities in fresh big-int. **Exit 0, CERTIFICATE OK.**
- **Lean** (gold standard) `lean/Constants/C3a.lean`, theorems added (all prior theorems
  `c3a_ge_5877_5000`, `c3a_ge_2353_2000`, `c3a_ge_1177_1000` left untouched):
  `newGE150`, `recLT150`, `Nplus150_pos`, `Nplus150_le_Nminus150`, `Q4_pos`,
  `c3a_ge_239_203`, `c3a_ge_239_203'`.
  - Build: `lake build Constants.C3a` → **PASS** (1980 jobs, ~76s).
  - Axiom audit (`audit150.lean` via `lake env lean`): `newGE150`/`recLT150` = `[propext]`
    only (pure kernel `decide`, NO `native_decide`/`ofReduceBool`/`sorryAx`/new axiom);
    `c3a_ge_239_203(')` = `[propext, Classical.choice, Quot.sound]` (standard ℝ trio, same as
    the R19/R22/R23 theorems). Only trust boundary is the named hypothesis `GHR_lower`.

## How to push further
- **Next rung: d=160 / T=300** (predicted ≈ 1.17763, +1.1e-3 over R23 held). Same lever,
  same split protocol. CAUTION (verified R23/R24 cost model): the sumset is superlinear in T;
  d=150/T=282 took 772.5s, so d=160/T=300 is estimated ~950–1200s — it MUST get its own
  `timeout ≥ 1500` call and the builder must confirm it fits one ≤60-min Bash call before
  launching. diff/max stays ~150s. Do NOT co-build d=160 with another push-d cell.
- The drop-1 base-21 SHAPE is the proven optimum (reshape screen R21 negative; asymptote
  ≈ 1.1813). After d=150 only ~3.6e-3 of asymptotic runway remains on this lever, approached
  with diminishing per-rung gain and rising DP cost — an honest treadmill.
- A real jump past the digit-set 1.25 ceiling needs a NON-digit / non-carry-free `U`
  (`beyond-digit-set-structured-U`), which has no concrete construction in hand and loses the
  clean `|U±U| = |block|^d` factorization (hence the Lean-fit cert path). Not recommended over
  the near-certain marginal d-rung unless a lead appears.
