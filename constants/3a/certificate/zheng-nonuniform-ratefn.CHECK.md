# Check record — zheng-nonuniform-ratefn (constant 3a, lower bound) — THEORY / CEILING / STEER

**This round produces NO bound.** It is a CEILING + STEER: the generalized non-uniform
large-deviation rate function for the GHR single-set carry-free digit family.  A numerical
BOUND only materializes at H3 (finite realization), which is left a clean hole (it is the
leader sketch alphabet-search-dp's lane).

**Predicted asymptotic CEILING (CONJECTURE, not a verified bound):** theta_inf ~ 1.18258
for the GHR single-set / carry-free family.
**Predicted ARGMAX:** A = {0,2,3,4,5,6,7,8,9,10} (omit only digit 1), base b = 21, c* ~ 1.871
— i.e. EXACTLY Griego's / the leader's configuration.

**Dependency:** cvxpy (SCS solver). Install (sandbox, once): `uv pip install --system cvxpy`.

**Run (validates H1 gate + Zheng table + finite consistency + H2 argmax; ~3-4 min):**
```
cd constants/3a/certificate && python3 zheng-nonuniform-ratefn.py
```

**Validation gates (what the run asserts / prints):**
- H1 GATE: uniform {0..5} -> theta-1 = 0.1730773 (matches Zheng Z2025 anchor exactly).
- H1 broader: full Zheng B-table {3..10} reproduced to ~1e-7 (independent check the rate
  function = Zheng's k-split closed form).
- Finite consistency: leader exact theta (d=84,88,96 = 1.174475/1.174764/1.175272) lie below
  the ceiling 1.18258 with the gap shrinking monotonically (0.00810/0.00782/0.00731).
- H2 argmax: M=10/base-21/omit-{1} is the peak (beats M=8,9,11 and all other omissions).
- H3: raises NotImplementedError (clean hole, referral to alphabet-search-dp).

**Expected tail:**
```
[H2] PREDICTED CEILING theta_inf = 1.1825801  (CONJECTURE, not a bound)
[H2] ARGMAX A=(0, 2, 3, 4, 5, 6, 7, 8, 9, 10) base=21 c*=1.871
[H2] held=1.1752717416788478; headroom to ceiling = +0.00731 (reached only as d->inf)
[hole H3] H3: finite realization is the leader sketch alphabet-search-dp ...
```

**Status:** H1 CLOSED (validated), H2 CLOSED (numerical argmax = current config), H3 OPEN.
Hole count remaining: 1 (H3). Target hole-free: NO (this round is a ceiling/steer, by design).
Do NOT write 1.18258 into current.md held — it is a conjecture/asymptotic ceiling.
