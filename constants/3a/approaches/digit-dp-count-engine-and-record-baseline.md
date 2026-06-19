# digit-dp-count-engine-and-record-baseline

**Angle.** Build the exact carry-free digit-DP count engine for the C_3a GHR digit-set
construction and reproduce the record lower bound `C_3a ≥ 1.1740744` exactly. This is the
search-immune machinery backbone (analogous to the 9a-367 baseline): gap 0, **NOT a beat** —
it is the reusable engine every other angle (sweep, asymptotic, Lean cert) calls.

## What I did (round 16)

Built and verified an exact-integer digit-DP engine in
`constants/3a/certificate/engine/`:

- **`digit_dp.py`** — `count_opset(A,d,T,op)` returns the EXACT `|U op U|` in the carry-free
  regime (`B > 2·max(A)`), `max_U(A,B,d,T)` the exact `max(U)`, plus `certifies_at_least`
  (the integer-power inequality for future small-q beats) and high-precision value display.
  All load-bearing counts are Python big-ints — no float.
- **`run_record.py`** — computes `N+`, `N−`, `max(U)` for the record, writes `record_*.txt`.
- **`selftest.py`** — DP-vs-brute cross-checks + no-cap factorization + record reproduction.
- **`certify_record.py`** — rigorous mpmath **interval / directed-rounded** lower bound from
  the exact integers.
- **`README.md`** — full math, API, reproduce commands.

### The DP (load-bearing step, closed fully)

`B = 21 > 2·max(A) = 20` ⇒ carry-free, so `u±v` ↔ digit-wise `(a_i ± b_i)`; the only
cross-position coupling is the digit-sum cap `T`. Achievability of an output vector reduces
(because `Sb` is affine in `Sa, Sc`: `Sb = Sc − Sa` for `+`, `Sb = Sa − Sc` for `−`) to a
condition on the reachable `Sa`:
- **sumset**: track the EXACT reachable-`Sa` set as a bitmask (boundary gaps real, e.g.
  `Sa=1` unreachable since `1∉A`); achievable iff `max` reachable `Sa ≥ Sc − T`.
- **difference**: only `min` reachable `Sa` matters, transitions deterministically
  (`minSa += min(a-options of c)`); achievable iff `minSa ≤ T + Sc`. Small, fast state.

This is exactly the "cap-coupled carry-free convolution DP" the outline named, and the hard
cap-vs-carry interaction is handled exactly (verified below).

### Verification (all green, `selftest.py`)

- **8 DP-vs-brute cross-checks**, diverse alphabets `{0,2,3,4,5}`, `{0,1,2,3}`, `{0,2,5}`,
  `{0,1,3,7}`, `{0,2..10}`, lengths `d=3,4`, various caps, **both** sumset and difference —
  every count matches brute-force enumeration EXACTLY, and `max_U` matches.
- **No-cap factorization** `|U+U|=|A+A|^d=20^d`, `|U−U|=|A−A|^d=21^d` for `d=3,4` — exact.
- **Record reproduction (bit-for-bit vs PR #71):**
  - `N+ = |U+U|` = 77-digit `75448362167176243488362019935078206851619643198150854886920234689186981134888` ✓
  - `N− = |U−U|` = 96-digit `195351744295266763842135520514417052287242446785296742323733058216909095059024572338564089814415` ✓
  - `M = max(U)` = 106-digit `2995805288150731620410662946668903948341032736664352641511848666717243994160370658179324073879212562136150` ✓
  - value `= 1.174074447693521163363531806…` (matches PR #71), directed-rounded **guaranteed
    lower bound > 1.1740744** (margin ~4.77e-8).

### Note on the triage case (spec clarification)

The outline's triage numbers `A={0,2,3,4,5},B=7,d=3,T=8 → |U+U|=386,|U−U|=509` are for
`B=7`, where `2·max(A)=10 > 7`: that case has **carries** and is OUTSIDE the carry-free
regime this engine targets. I verified `386/509/266` separately by brute force (GHR-formula
sanity), and cross-checked the carry-free DP on genuinely carry-free small cases
(`B > 2·max(A)`), its real domain. The record IS carry-free (`B=21>20`), so the engine
applies to it directly.

## Value I claim

`C_3a ≥ 1.1740744` (the record, reproduced exactly — **gap 0, NOT a beat**). The reproduction
is the deliverable: an independent exact-integer engine that recomputes the published 77-/96-
/106-digit certificate integers bit-for-bit and the value to 25+ digits, with a rigorous
directed-rounded lower bound. Table value: 1.1740744 (verified). New value: 1.1740744 (ties —
this slug is machinery, not a beat).

## Why no Lean cert of the record this round

`value ≥ 1.1740744` rationalizes to `N-^q ≥ N+^q·(2M+1)^p` with `q = denom((c−1)) =
1 250 000` (since `c−1 = 217593/1250000`), making `N-^q` a ~1.2·10^8-digit integer —
infeasible to `decide`. (Outline-reviewer flagged this.) The integer-power check IS
implemented and verified on small cases, ready for a **found beat** with a fatter margin
(`q ≈ 40..155`), which is the `lean-cert-rational-power` angle's later sub-goal.

## What would push this further

1. **Sweep (sibling slug `directed-param-sweep-exact-beat`)** reuses `count_opset` directly:
   vary alphabet shape (add 1 back, add 11, Sidon-like sub-alphabets), `T`, `d/T` density,
   `B` (keep `> 2·max(A)`), compute the exact rational bound per cell, flag any strict beat
   of 1.1740744 by an exact-integer margin.
2. **Speed**: the sumset DP (~60 s) is the slower half; the bitmask state could be canonicalized
   by `(minSa, maxSa, gap-pattern)` to shrink the distinct-state count if larger `d`/`T` is
   needed for the asymptotic angle.
3. **Lean cert of a found beat**: once the sweep finds a `U` clearing a small-denominator
   rational `c`, `certifies_at_least` gives the integer inequality to port to Lean (the
   `lean-cert-rational-power` angle).

## Spec concerns

- The carry-free regime requires `B > 2·max(A)`; `count_opset` does not itself enforce `B`
  (the count is `B`-independent in this regime), so a CALLER must keep `B > 2·max(A)` or the
  carry-free factorization (and thus the count) is invalid. `ghr_bound_value` raises if
  `B ≤ 2·max(A)`. The sweep must respect this.
- The record Lean certificate is genuinely infeasible by the integer-power route at this
  razor-thin margin; do not attempt it. Lean is for a beat.
