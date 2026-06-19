# C_3a strict-beat certificate — Round 23, d=140 cell

## Claim

`C_3a ≥ 1177/1000 = 1.1770`

strictly above:
- our R22 held & Lean-checked `2353/2000 = 1.1765`,
- the R18/R19 held `5877/5000 = 1.1754`,
- the true [G2026] PR #71 record `1.1740744476935212` (table truncation `1.1740744` sits below it).

## Construction (same family as the record, pushed to larger d)

GHR digit-set, drop-1 base-21 alphabet:
- `A = {0,2,3,4,5,6,7,8,9,10}`, base `B = 21` (carry-free: `B = 21 > 2·max(A) = 20`),
- `U = { Σ_{i<d} a_i·B^i : a_i ∈ A, Σ a_i ≤ T }`,
- value `= 1 + log(|U−U| / |U+U|) / log(2·max(U)+1)`  (GHR2007 lower bound on C_3a).

**PRIMARY cell:** `d = 140`, `T = 263` (density ≈ 1.8786) → value ≈ **1.1771186319558**.

Only change from the record cell (`d=80, T=150`): `d` pushed 80 → 140 (and `T` scaled at the
same density). The d-push is the live lever — the difference-set per-digit entropy is still
unsaturated below the d→∞ density limit (rnum 0.534@d100 → 0.538@d130 → asymptote ≈0.552).

## Exact integers (carry-free digit-DP, `engine/digit_dp.py::count_opset`)

| quantity | digits |
|----------|--------|
| `|U+U|`  | 136 |
| `|U−U|`  | 169 |
| `max(U)` | 185 |

Persisted in `beat_d140.json` (cell `d140_T263`). The cheap pieces (`|U−U|`, `max(U)`) were
computed first (`run_d140_diffmax.py`, ~135 s) and the heavy sumset `|U+U|` via the engine
(`run_d140_engine.py`, ~510 s) — both under the per-call `timeout 600` budget, ONE heavy cell
per call. `dp_pareto.py` was NOT used (the R15/R17 force-kill trap).

## The wedge — strict beat decided by EXACT big-int powers

Wedge `c = 1177/1000`, so `c − 1 = P/Q = 177/1000` (P=177, Q=1000). No float decides anything:
- `value_new ≥ c`   ⟺  `|U−U|^Q ≥ |U+U|^Q · (2·max(U)+1)^P`  (d=140 cell — **TRUE**),
- `value_record < c` ⟺  `RNm^Q < RNp^Q · (2·RM+1)^P`        (d=80 record cell — **TRUE**),

so `value_record < c ≤ value_new`. And `c = 1177/1000 > 2353/2000 = held` exactly (Fraction),
margin over held `+5.0e-4` (the true float margin of value_new over held is `+6.19e-4`).

## How to re-check

```
python3 verify_beat.py              # loads persisted d=140 integers; recomputes the d=80
                                    # record cell bit-for-bit vs PR#71; two-engine cross-check
                                    # on d∈{20,30,40}; both exact wedge inequalities; all bar
                                    # comparisons. ~3–4 min. Exit 0 + "CERTIFICATE OK".
python3 verify_beat.py --recompute  # ALSO recompute the d=140 cell from scratch via the DP
                                    # (~650 s extra: diff/max ~135 s + sumset ~510 s).
```

## Lean certificate (gold standard — `lake build` is the check)

`lean/Constants/C3a.lean`, theorems `c3a_ge_1177_1000` / `c3a_ge_1177_1000'` (R19's
`c3a_ge_5877_5000` and R22's `c3a_ge_2353_2000` left intact). Build target `Constants.C3a`.

- `lake build Constants.C3a` → PASS (1980 jobs, ~236 s).
- `#print axioms`:
  - `newGE140` (d=140 cell passes wedge), `recLT140` (record cell fails wedge): `[propext]`
    only — pure kernel `decide`, no `sorryAx`, no `native_decide`/`ofReduceBool`, no added axiom.
  - `c3a_ge_1177_1000`, `c3a_ge_1177_1000'`: `[propext, Classical.choice, Quot.sound]` (standard
    real trio).
- The only trust boundary is the named hypothesis `GHR_lower` (the GHR2007 analytic
  `θ(U) ≥ c ⟹ C_3a ≥ c` existence step — a hypothesis, NOT an axiom, so absent from
  `#print axioms`; same pattern as 9a `ThetaGeFromIndep`, 5b `MTThm15`). The big integers are
  TRUSTED literals whose provenance is re-derived OUT of Lean by `verify_beat.py`.

## References

- [GHR2007] Gyarmati, Hennecart, Ruzsa, "Sums and differences of finite sets",
  Funct. Approx. Comment. Math. 37(1):175–186, 2007.
- [G2026] Griego, repo PR #71 (the d=80 record, value 1.1740744476935212).
