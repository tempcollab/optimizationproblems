# push-d-160-exact-beat

## Idea
Same proven carry-free drop-1 base-21 GHR digit lever as the five prior verified bound moves
(R18 d=100, R19 Lean port, R22 d=130, R23 d=140, R24 d=150), walked one rung further to
**d=160**. Fixed alphabet `A = {0,2,3,4,5,6,7,8,9,10}`, `B = 21`, cap `T = 300` (density
exactly 1.875). Carry-free holds because `B = 21 > 2·max(A) = 20`, so `|U±U| = |block±block|^d`
are exact, DP-countable integers — no continuum estimate anywhere. The slack the d-push
exploits is the unsaturated per-digit numerator rate `rnum(d)`, still climbing toward
`rinf ≈ 0.552` (asymptote `1 + rinf/log 21 ≈ 1.1813`); G2026 fixed d=80 below its own density
limit, so larger d strictly increases the bound.

GHR2007 lower bound: `C_3a ≥ 1 + log(|U−U|/|U+U|) / log(2·max(U)+1)`
(digest: `constants/3a/literature/GHR2007-lemma-digest.md`).

## Status — CLAIMED (R25), Lean-machine-checked, awaiting reviewer verification
**Claimed lower bound: C_3a ≥ 179/152 = 1.1776315789…**, strictly beating the R24 held
`239/203 = 1.1773399…` by **+2.917e-4** (exact Fraction). This is a CLAIM until the reviewer
re-establishes it; do NOT treat the value as `held` until then.

### Cell (the fresh d=160 DP)
- `A = {0,2,3,4,5,6,7,8,9,10}`, `B = 21`, `d = 160`, `T = 300`, density 1.875.
- Exact counts (persisted `constants/3a/certificate/beat_d160/beat_d160.json`, cell `d160_T300`):
  - `|U+U|` = 155-digit int
  - `|U−U|` = 193-digit int
  - `max(U)` = 212-digit int
- True GHR value (float, display only): **1.1776644803530216**.
- DP cost: diff/max ≈ 227–235s/T (collapsed `minSa`-state, slower than the d=150 ~140s due to
  larger d and T); heavy sumset (mask width T+1 = 301) ≈ **1051.6s** — required its own
  `timeout 2400`-wrapped call, per the R23/R24 split protocol. The two cheap diff/max cells
  (T=299,300) fit one `timeout 600` call (the third, T=301, was cut off by the timeout but is
  not needed). The sumset fit one ≤60-min Bash call (~17.5 min).

### T-neighborhood check
Computed diff/max for `T ∈ {299,300}` cheaply (~230s each). T=300 (density exactly 1.875) is
the calibrated optimum used; the sumset was run only for T=300 to stay within one heavy call.

### Wedge (load-bearing exact big-int inequality)
Chosen by the EXACT `Nm^Q ≥ Np^Q·(2M+1)^P` test in Python `Fraction` first (never the float):
- **c = 179/152 = 1 + 27/152**, `P = 27`, `Q = 152` — the LARGEST-headline wedge with `Q ≤ 200`
  that the exact integers clear (sweep best with Q≤200). Larger than the outline-recommended
  `1+19/107=1.1775701` (which also passes), and still small-Q for a fast `decide`.
- (a) `value_new ≥ c`: `|U−U|^Q ≥ |U+U|^Q·(2·max(U)+1)^P` — PASSES.
- (b) `value_record < c`: d=80 record cell `RNm^Q < RNp^Q·(2·RM+1)^P` — PASSES (strictness ⇒
  strict over the true record 1.1740744476935212, not the table truncation).
- `c > 239/203` (held, +2.917e-4), `> 1177/1000`, `> 2353/2000`, `> 5877/5000`,
  `> 1.1740744476935212` (record), all exact-rational. `Q = 152` is trivial for `decide`
  (≪ R22's Q=2000 ~11.5s; nowhere near the R21 Q=10000 force-kill trap).

### Certificates
- **Numerical** `constants/3a/certificate/beat_d160/verify_beat.py`:
  `python3 verify_beat.py` (loads persisted integers, ~80s) and `--recompute` (re-derives the
  d=160 DP from scratch, ~1300s total). Re-establishes the record cell bit-for-bit vs
  `record_baseline.json` (PR #71), cross-checks the fast `count_opset` engine vs the independent
  Pareto `dp_engine` on small cells d∈{20,30,40}, and re-derives both wedge inequalities in
  fresh big-int. **Exit 0, CERTIFICATE OK.** Also `CERT.md` documents the wedge/literals/target.
- **Lean** (gold standard) `lean/Constants/C3a.lean`, theorems added (all prior theorems
  `c3a_ge_5877_5000`, `c3a_ge_2353_2000`, `c3a_ge_1177_1000`, `c3a_ge_239_203` + their
  `newGE*`/`recLT*` left untouched):
  `newGE160`, `recLT160`, `Nplus160_pos`, `Nplus160_le_Nminus160`, `Q5_pos`,
  `c3a_ge_179_152`, `c3a_ge_179_152'`.
  - Build: `lake build Constants` (from `lean/`) → **PASS** (8571 jobs; `Constants.C3a` built
    in 129s; Mathlib pinned v4.31.0).
  - Axiom audit (`#print axioms` via `lake env lean`): `newGE160`/`recLT160` = `[propext]`
    only (pure kernel `decide`, NO `native_decide`/`ofReduceBool`/`sorryAx`/new axiom);
    `c3a_ge_179_152(')` = `[propext, Classical.choice, Quot.sound]` (standard ℝ trio, same as
    the R19/R22/R23/R24 theorems). Only trust boundary is the named hypothesis `GHR_lower`.

## How to push further
- **Next rung: d=170 / T≈319** (predicted ≈ 1.17784, only ~+2.2e-4 over this d=160 cell).
  Same lever, same split protocol. CAUTION (verified R24/R25 cost model): the sumset is
  superlinear in T and d — d=150/T=282 took 772.5s, d=160/T=300 took 1051.6s, so d=170/T≈319
  (mask width ~320) is estimated ~1400–1700s and is approaching the single-call edge; it MUST
  get its own `timeout ≥ 2400` call and the builder must confirm it fits one ≤60-min Bash call
  before launching. diff/max grows too (~280–300s/T at d=170). Do NOT co-build with another
  push-d cell.
- The drop-1 base-21 SHAPE is the proven optimum (reshape screen R21/R22 negative; asymptote
  ≈ 1.1813). After d=160 only ~**3.4e-3** of asymptotic runway remains on this lever, approached
  with diminishing per-rung gain (≈ +2e-4 per rung now) and rising DP cost — an honest
  treadmill near its long flat tail. Weigh whether further marginal +e-4 rungs justify a full
  heavy-DP round.
- A real jump past the digit-set 1.25 ceiling needs a NON-digit / non-carry-free `U`
  (`beyond-digit-set-structured-U`), which has no concrete construction in hand and loses the
  clean `|U±U| = |block|^d` factorization (hence the Lean-fit cert path). Not recommended over
  the near-certain marginal d-rung unless a concrete lead appears.
