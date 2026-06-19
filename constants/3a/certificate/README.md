# Certificate — C_3a lower bound (numerical, exact-integer counting)

This is the **one numerical certificate** the rounds extend for constant 3a. Constant 3a is
Lean-hostile at the final step (a real-number log ratio), so the certified artifact is a
directed-rounded Python script, per the explorer's triage and `CLAUDE.md`.

## What it certifies

A lower bound on the Gyarmati–Hennecart–Ruzsa sum-difference constant C_3a, via the GHR2007
lemma: any finite non-negative U ∋ 0 gives `C_3a >= 1 + ln(|U-U|/|U+U|)/ln(2*max(U)+1)`.

Construction (G2026 family, depth pushed this round):
- base `b = 21`, digit set `A = {0,2,3,...,10}` (digit 1 dropped, max digit 10),
- depth `d`, digit-sum cap `T`,
- `U = { sum_i a_i*b^i : a_i in A, sum_i a_i <= T }`.

## Reproduce (one command)

Run the certifying DP **ALONE** — CPU contention from parallel runs multiplies its runtime
5–10×.

```
cd constants/3a/certificate
python3 certify_3a.py 110 210    # round-2 claim: d=110, T=210   (~78s)
```

The depth `d` and digit-sum cap `T` are command-line args (default `90 172`, ~35s).
Fallback if d=110 overruns budget: `python3 certify_3a.py 100 192` (θ ≥ 1.175495, ~55s).

## Claimed result (round 2, d=110, T=210)

- `S = |U+U|` : 107-digit integer (printed exactly by the script)
- `D = |U-U|` : 133-digit integer
- `max(U)`    : 146-digit integer; `q = 2*max(U)+1`
- **Certified theta (rigorous lower bound): 1.1760055927978140029771014788...** (lower endpoint
  of an mpmath interval enclosure at `iv.prec=400`).
- Record to beat [G2026]: **1.1740744**. Margin: **+0.0019311927978139...**. BEATS RECORD: **YES**.
- Counting runtime here: 78.4 s.

This is a builder's CLAIM until the proof-reviewer re-runs and confirms it. (Round-1 d=90/T=172
gave θ = 1.1748992466319329..., margin +0.000824847 — superseded by the round-2 d=110 run.)

## How the load-bearing steps are certified (for the reviewer)

1. **Exact counts.** `S`, `D`, `max(U)` are Python big integers; no float enters the counting.
   The two DPs are documented inline in `certify_3a.py`:
   - **sum DP**: state `(ty = running digit-sum of U+U, bitset of achievable sum a_i)`; a
     final element is feasible iff some `s` with `s <= T` and `ty - s <= T` (both sum caps).
   - **diff DP**: state `(running sum a_i, running sum b_i)` using, per signed digit `delta`,
     the unique min-sum `(a,b)` pair; feasible iff both running sums stay `<= T`.
   Both DPs were validated against brute-force enumeration of U at small `(d,T)`
   (e.g. d=3 T=8, d=4 T=10, d=2 T=20) — counts match exactly.
2. **Validity guard.** The script asserts and prints `base >= 2*max(A)+1` (here `21 >= 21`).
   This makes every base-`b` digit representation in U+U and U-U carry-free, so the DPs count
   **distinct integers**, not distinct digit vectors. The "base-20 trap" (base = 2*max(A) = 20)
   was confirmed to make the DP OVERCOUNT (DP 400/441 vs true 382/421 at d=2, T=20) — so the
   guard is load-bearing.
3. **Rigorous theta.** Instead of `math.log` (a float), theta is computed with mpmath
   **interval arithmetic** (`mpmath.iv`, `iv.prec=400`): `theta_iv = 1 + iv.log(D/S)/iv.log(q)`.
   Both logs are positive (D>S>0, q>1), so the interval division's lower endpoint
   `theta_iv.a` is a guaranteed **lower bound** on the true real value. The script prints
   `theta_iv.a`. The enclosure width at 400 bits is far below the +0.000825 margin, so the
   lower bound provably clears the record.

## Re-establish target (what the reviewer re-runs)

- Command: `python3 certify_3a.py 110 210` (run ALONE), runtime ~78s.
- Check the printed `BEATS RECORD 1.1740744: YES`, the validity-guard line `21 >= 21 : OK`,
  and that the printed `theta_lower_bound` (= 1.1760055927978140...) strictly exceeds 1.1740744.
- Independently re-derive: the two DP recurrences (documented inline), the validity guard,
  and that `theta_iv.a <= true theta` (positive-interval division rounds the quotient down).
