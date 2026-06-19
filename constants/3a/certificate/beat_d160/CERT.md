# C_3a strict-beat certificate — Round 25, d=160 cell

## Claim

    C_3a  ≥  c = 179/152 = 1.1776315789…
          >  239/203   = 1.1773399…   (R24 HELD, Lean-checked)
          >  1177/1000 = 1.1770       (R23 held)
          >  2353/2000 = 1.1765       (R22 held)
          >  5877/5000 = 1.1754       (R18/R19 held)
          >  1.1740744476935212       ([G2026] PR #71 record — the TRUE record value,
                                        strictly above the table truncation 1.1740744).

Strict beat of the R24 held bound 239/203 by margin **+2.917e-4** (exact, via Fraction).

## Construction (drop-1 base-21 GHR digit family, pushed to d=160)

    A = {0,2,3,4,5,6,7,8,9,10},  B = 21       (carry-free: B = 21 > 2·max(A) = 20)
    U = { Σ_{i<d} a_i·B^i : a_i ∈ A,  Σ a_i ≤ T },   d = 160,  T = 300  (density 1.875)
    value = 1 + log(|U−U| / |U+U|) / log(2·max(U)+1)        (GHR2007 lower bound on C_3a)

The carry-free regime (B > 2·max(A)) makes |U+U|, |U−U|, max(U) EXACT integers,
computed by the digit-DP engine `constants/3a/certificate/engine/digit_dp.py::count_opset`.

## The exact integers (cell d160_T300, in beat_d160.json)

| quantity      | digits | provenance |
|---------------|--------|------------|
| `|U+U|`       | 155    | `count_opset(A,160,300,'+')`, heavy sumset DP, 1051.6s |
| `|U−U|`       | 193    | `count_opset(A,160,300,'-')`, diff DP, 227.2s |
| `max(U)`      | 212    | `max_U(A,21,160,300)`, greedy, instant |

`value_new` (float, display only) = 1.1776644803530216.

## The wedge (the load-bearing decision is EXACT big-int, never the float)

c = 1 + P/Q with **P = 27, Q = 152** (already in lowest terms), so c = 179/152.

Two EXACT integer-power inequalities decide the strict beat (no float anywhere):

  (a) **newGE160** — d=160 cell passes the wedge:
        |U+U|^Q · (2·max(U)+1)^P  ≤  |U−U|^Q          ⟺  value_new ≥ c
  (b) **recLT160** — d=80 record cell FAILS the same wedge:
        recNminus^Q  <  recNplus^Q · (2·recMaxU+1)^P  ⟺  value_record < c

(a) & (b)  ⟹  value_record < c ≤ value_new, so the beat is STRICT over the true record.
The wedge was chosen as the largest-headline small-Q rational with Q ≤ 200 that clears
held 239/203 and passes both inequalities; Q = 152 keeps the Lean `decide` fast.

## Numerical re-check

    python3 verify_beat.py              # loads persisted integers, ~80s, exits 0 "CERTIFICATE OK"
    python3 verify_beat.py --recompute  # also re-derives the d=160 integers from scratch
                                        #   (diff/max ~230s + sumset ~1050s) and bit-checks them

verify_beat.py also re-derives the d=80 record cell from scratch and checks it bit-for-bit
against `../sweep/record_baseline.json` (PR #71), and cross-checks the fast engine against the
independent Pareto engine (`../engine/dp_engine.py`) on small carry-free cells d ∈ {20,30,40}.

## Lean machine-check (gold standard)

- File: `lean/Constants/C3a.lean` (block "ROUND 25 — the d=160 beat cell").
- Build target: `lake build Constants`   (from `lean/`; builds `Constants.C3a`).
  Result: PASS, 8571 jobs, Constants.C3a built in 129s, Mathlib pinned v4.31.0.
- Theorems added (all prior theorems left intact):
  - `newGE160 : Nplus160 ^ Q5 * (2 * maxU160 + 1) ^ P5 ≤ Nminus160 ^ Q5`   (`decide`)
  - `recLT160 : recNminus ^ Q5 < recNplus ^ Q5 * (2 * recMaxU + 1) ^ P5`    (`decide`)
  - `c3a_ge_179_152  (c3a : ℝ) (hbridge : GHR_lower c3a) : c3a ≥ 1 + 27/152`
  - `c3a_ge_179_152' (c3a : ℝ) (hbridge : GHR_lower c3a) : c3a ≥ 179/152`
- `#print axioms`:
  - `newGE160`  → `[propext]`
  - `recLT160`  → `[propext]`
  - `c3a_ge_179_152`  → `[propext, Classical.choice, Quot.sound]`
  - `c3a_ge_179_152'` → `[propext, Classical.choice, Quot.sound]`
  No `sorryAx`, no `Lean.ofReduceBool` (native_decide), no smuggled/new axiom.

`GHR_lower` is the single named trust boundary (the GHR2007 θ(U) ≥ c ⟹ C_3a ≥ c existence
step; Mathlib has no C_3a object). It is a HYPOTHESIS on the bound theorem, not an axiom, so
it is absent from `#print axioms`; the trust link is visible in the signature. Same pattern
as 9a's `ThetaGeFromIndep` and 5b's `MTThm15`.

## References

- [GHR2007] Gyarmati, Hennecart, Ruzsa, "Sums and differences of finite sets",
  Funct. Approx. Comment. Math. 37(1):175–186, 2007.
- [G2026] Griego, repo PR #71 (the d=80 record construction, value 1.1740744476935212).
