# L2 — Push Griego's own family to larger (m,T)

**Slug:** `griego-family-larger-mT`   **Target:** lower bound, beat `C_3a > 1.1740744`.

## Strategy
Keep Griego's exact alphabet and base — `A = {0,2,3,4,5,6,7,8,9,10}`, `b = 21` — fixed, and push
the parameters `m` (digit count) and `T` (digit-sum cap) **past** the recorded `(m,T) = (80,150)`.
The GHR ratio `log(d/s)/log q` for a fixed alphabet rises monotonically toward its asymptotic limit
as `(m,T) → ∞` along the optimal ray `T ≈ r·m`. The open question: was `(80,150)` the family's
supremum, or does a larger `(m,T)` clear `1.1740744`?

## What this round CLOSED — the exact column DP (`exact-sumdiff-dp` hole)
The load-bearing computational hole is now closed with an **exact integer DP** that scales far past
brute force, **self-tested against brute force on 8 cases** `(m,T) ∈ {(2,5),(3,8),(4,10),(4,12),
(5,14),(3,15),(4,40),(5,20)}` — all three of `(|U+U|, |U−U|, max U)` match exactly.

Two structural facts make the DP exact and carry-free (since `b > 2·max(A)`):
- `g(x)+g(y)` has base-`b` digits `(x_i+y_i) ∈ [0,2max A]` (no carries) ⇒
  `|U+U| = #{distinct realizable sum-vectors (x_i+y_i)}`.
- `g(x)−g(y)` has base-`b` digits `(x_i−y_i) ∈ [−max A, max A]` (no borrows) ⇒
  `|U−U| = #{distinct realizable diff-vectors (x_i−y_i)}`.

**Diff-set decoupling (proved & verified):** for each difference value `w` there is a UNIQUE pair
`(x*(w), y*(w)) ∈ A×A` with `x−y=w` minimizing *both* coordinates at once (since `x=y+w`,
minimizing `y` minimizes `x`). Hence a diff-vector `v` is realizable under the two caps iff
`Σ x*(v_i) ≤ T` AND `Σ y*(v_i) ≤ T` — a clean 2-D DP over `(Σx*, Σy*)`, bounded by `T²` states,
fast even at `(80,150)`.

**Sum-set (genuine x↔y tradeoff, no decoupling):** a sum-vector `v` is realizable iff the reachable
set of `Σx_i` (Minkowski sum of the per-column achievable-x sets `X_{v_i}`) meets `[Σv_i−T, T]`.
This reachable set is **non-contiguous** (~13% of cases) because the alphabet skips the digit `1`,
so an interval shortcut is UNSOUND (verified by counterexample). The exact count uses a **bitmask DP**:
state `(Σv, R)` where `R` is the bitmask of reachable `Σx` clamped to `[0,T]`; a vector is counted
iff `R` meets `[max(0,Σv−T), T]` at the end.

`max(U)` is the greedy top-digit assignment (optimal since weights `b^i` strictly increase and
`b > 2max(A)`; verified vs an exact recursion).

The certificate file is **standalone and reproducible** and runs the self-test on every invocation.
The record comparison is the **pure integer inequality** `d^{q'} > s^{q'}·q^{p'}` with
`q'=1250000`, `p'=217593` (from `target−1 = 217593/1250000`) — no floating point in the load-bearing
check.

## ROUND 3 — `scan-mT` CLOSED. VERIFIED RECORD BEAT.

**The sum-set DP wall is gone** (dynamic low-clamp, below), and the `(m,T)` scan now reaches the
crossing in seconds. The Griego family `A={0,2,..,10}, b=21` **climbs strictly past the record**:

| m | T | θ (exact DP) | exact-int `θ>1.1741` | rig-log `θ>1.1740744` |
| --- | --- | --- | --- | --- |
| 80 | 150 | 1.1740744477 | — | True (= Griego's own record point, reproduced exactly) |
| 80 | 154 | **1.1741713540** | **True** | True |
| 100 | 190 | **1.1754955081** | **True** | True |
| 110 | 210 | **1.1760055928** | **True** | True |

**VERIFIED bound (claim, pending reviewer re-run): `C_3a > 1.1741 > 1.1740744`** — beats the record.
The load-bearing certificate is the **pure big-integer inequality, no float**:
`d^10000 > s^10000 · (2M+1)^1741`  ⟺  `θ > 11741/10000 = 1.1741 ≥ TARGET 1.1740744`.
(θ itself climbs to ≈1.1760056 at m=110; 1.1741 is the small-denominator coarse rational chosen so
the integer powers are tractable while still strictly exceeding the record.) A redundant rigorous
400-bit directed-rounded log test confirms `θ > 1.1740744` at each point.

Reproduce:  `python3 constants/3a/certificate/griego-family-larger-mT.py`
(self-test green; reproduces (80,150)=record; certifies (110,210) beats it). Scan audit trail:
`constants/3a/certificate/scan-mT-results.txt`; per-point scanner `certificate/scan_mt.py`.

### The speedup that closed the wall — SOUND dynamic low-clamp (validated vs oracle)
The sum-set bitmask DP state is `(Σv, R)`, `R` = reachable `Σx` clamped to `[0,T]`. KEY: a reachable
`Σx` is feasible only if it can still satisfy `Σx ≥ Σv_final − T`; since `Σv` only GROWS as columns
are added, **any bit below `Σv − T` is already and forever below the lower feasibility edge and is
dropped each layer** (`nR = (nR>>lo)<<lo`, `lo=max(0,Σv−T)`). Exact (the top is already clamped at
`T`), and it collapses mask width + merges states near the top window. Result: `(80,150)` went from
~**35 min → 10 s**; `(110,210)` ~30 s. **Self-test still passes** (matches brute force on all 8
cases), and the clamped count matches the un-clamped count on `(4,12),(5,20),(10,22),(20,42),(30,60)`.
This is exactly the outliner's "sound speedup #1". The NTT path (#2) was not needed — the clamp alone
made the whole `m≈80–110` scan run in seconds.

NOTE on the certification fix: the old `certifies_target` used the FULL target denominator
`q'=1250000`, giving `d^{1250000}` (~10^8-digit operands) — that HANGS (it was the silent stall this
round until isolated). Replaced by (a) `certifies_target_int(s,d,M,num,den)` — the exact integer test
against a SMALL-denominator rational `num/den ≥ TARGET` (here `11741/10000`), and (b) a rigorous
mpmath directed-rounded log cross-check. The load-bearing certificate is the integer one (no float).

## Findings — the family KEEPS CLIMBING with m (best θ data, exact)
Best `θ` (max over `T`) at each `m`, fixed `A={0,2..10}`, `b=21`, all from the exact self-tested DP:

| m | best T | T/m | θ (exact DP) |
| --- | --- | --- | --- |
| 10 | 22 | 2.20 | 1.1459667 |
| 20 | 41 | 2.05 | 1.1594950 |
| 30 | 60 | 2.00 | 1.1652053 |
| 40 | 79 | 1.975 | 1.1684588 |
| 60 | 116 | 1.93 | 1.1721231 |
| 70 | (peak ≥ 1.1728…, running) | ~1.9 | ≥ 1.1728032 (at T=128, peak higher) |
| 80 | (running, incl. T=150) | ~1.9 | pending |

**Crucially, the climb is FASTER than a `1/m` correction.** A `1/m` fit on `m≤60` predicts
`m=70 → 1.17168`, but the exact value at `m=70, T=128` is already `1.1728032` (and `T=128` is below
the m=70 optimum `T≈134`, so the peak is higher still). A `1/√m` correction fits far better and
extrapolates the family supremum to `≈ 1.175–1.176`, **ABOVE the record `1.1740744`**, with the
crossing near `m ≈ 75–85`. This MATCHES the sibling L1 finding (proof-builder memory): the
non-contiguous-alphabet lever is *saturated* — Griego's `{0,2..10}` is the unique optimal alphabet —
and **the record is precisely the `(m,T)→∞` limit of this one family**. So pushing `(m,T)` (this
sketch) is the correct and possibly only lever to beat the record.

## Conclusion / remaining holes
- `exact-sumdiff-dp` (MEDIUM, shared with L1/L3): **CLOSED** — exact, self-tested vs brute force on
  8 cases, scalable. Diff-set minimal-pair decoupling = fast 2-D `(Σx*,Σy*)` recursion; sum-set
  bitmask DP now with the **dynamic low-clamp** (above) runs `m≈110` in ~30 s. **Promotable**.
- `scan-mT` (HARD, load-bearing): **CLOSED — VERIFIED RECORD BEAT.** Found the first `(m,T)` whose
  EXACT integer test clears the record: `m=80, T=154` (θ=1.1741714), and the family keeps climbing
  (`m=100,T=190`→1.1754955; `m=110,T=210`→1.1760056). Each certified by the pure big-integer
  inequality `d^10000 > s^10000·(2M+1)^1741 ⟹ θ > 1.1741 > 1.1740744`, no float on the load-bearing
  step. `m=80,T=150` reproduces Griego's exact record point θ=1.1740744477 as the first check.

**No remaining holes on the path to the bound.** (Follow-on, NOT blocking: port the integer
inequality to Lean `native_decide` for a machine-checked certificate — the bound is already verified
in exact Python big-int.)

## Claimed value (CLAIM until reviewer re-runs the certificate)
**C_3a > 1.1741 > 1.1740744 (record, Griego 2026).** Certified by the exact integer inequality at
`m=110, T=210` (θ≈1.1760056), and equally at `m=80,T=154` and `m=100,T=190`. The exact-integer
certificate is `d^10000 > s^10000·(2M+1)^1741` with the exact `(s,d,M)` printed by the certificate.
Margin over the record: θ≈1.1760 vs 1.1740744 at m=110 (≈0.0019), and even the first crossing
(m=80,T=154) clears it by ≈0.0001. This is a genuine record beat, not extrapolation — exact integer
arithmetic throughout. Pending the proof-reviewer's independent re-run (`python3
constants/3a/certificate/griego-family-larger-mT.py`).

## Promotable lemmas
- `exact-sumdiff-dp` — the exact column DP for `(|U+U|, |U−U|, max U)` of the digit construction
  `U = {Σ x_i b^i : x ∈ A^m, Σx_i ≤ T}` with `b > 2max(A)`, with the structural reductions
  (carry-free digit-vector counting; diff-set minimal-pair decoupling; sum-set bitmask DP **with the
  sound dynamic low-clamp** that makes it run `m≈110` in ~30 s). Proved green and self-tested against
  brute force on 8 cases in `certificate/griego-family-larger-mT.py` (`self_test()`, `count_sumset`,
  `count_diffset`, `max_U`). Reusable by L1 (`noncontig-alphabet-sweep`) and L3 for ANY alphabet `A`.
  The clamp was additionally validated to match the un-clamped count on `(4,12),(5,20),(10,22),
  (20,42),(30,60)`.

## Outliner note (R3) — sum-set DP speedup terrain (prototyped, what is SOUND vs UNSOUND)
The only blocker on `scan-mT` is the **sum-set DP cost** (~35 min at `(80,150)`). I prototyped the
candidate speedups against the existing self-tested `count_sumset` to tell the builder which are
exact before any compute is spent:

- **UNSOUND — collapse state to `(Σv, Σmin x, Σmax x)`** (drop the bitmask, test feasibility by
  `min(Σmax,T) ≥ Σv−T ∧ Σmin ≤ T`). Overcounts: e.g. `m=4,T=12` gives `11592` vs truth `11580`;
  `m=30,T=60` off in the 19th digit. Reason: when `Σmax x > T` the clamp drops top bits and a
  **hole** can sit between the largest reachable `Σx ≤ T` and `Σv−T`. The per-state maxbit test
  only *looked* exact on tiny cases where `Σmax ≤ T`. Do NOT use this.
- **EXACT but UNBOUNDED — track only the top window `[Σmax−WIN, Σmax]` of the reachable set**
  (self-signals `None` when `WIN` too small). Correct, but the required `WIN` grows like
  `Σmax−T = O(m·maxgap)`, so for `Σmax ≫ T` it degenerates to the full mask. No asymptotic win.
- **The bitmask DP is genuinely load-bearing near the top** — non-contiguity is real (per-column
  `X_w = {0} ∪ [2,w]` for `w≤10`; the single missing digit `1` creates the holes). Confirmed the
  explorer's "interval shortcut unsound" warning at the algorithmic level.

**SOUND speedups left for the builder (in priority order):**
1. **Clamp the bitmask to the *active* window `[max(0,Σv−T), T]` dynamically** — the lower edge
   `Σv−T` only rises as the DP advances, so bits below it can be dropped each layer. Keeps the DP
   exact (it already clamps the top at `T`) and shrinks mask width when `Σv` is large. Lowest-risk,
   pure constant-factor + width reduction; validate vs `count_sumset` on the 8 self-test cases.
2. **NTT / repeated-squaring along the cap axis (idea 2)** — the m-fold per-column convolution is
   `O(log m)` squarings of a size-≤T (diff) / ≤T² (sum) array; exact integer NTT keeps it
   Lean-friendly. This is the real `m≈90–110`-in-seconds win but the most code. The sum side must
   still respect the two coupled caps, so the convolution carries the `(Σx,Σy)` pair — heavier than
   the diff side but still polynomial in `T`, not bitmask-blown.

Either path must reproduce `θ(m=80,T=150) ≈ 1.174074` (the record's own point) as its first check,
then push to the first `(m,T)` whose exact integer test `d^{q'} > s^{q'}·q^{p'}` clears `1.1740744`.

## Certify
Numerical (exact big-int), self-tested vs brute force. The integer inequality
`d^{q'} > s^{q'}·q^{p'}` is the Lean-fit certification form for any future winner.
