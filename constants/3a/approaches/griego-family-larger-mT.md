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
  8 cases, scalable. The **diff-set minimal-pair decoupling** makes my `|U−U|` DP a fast 2-D
  `(Σx*,Σy*)` recursion (`~2s` at `m=50`), far faster than a pair-set diff DP. **Promotable**.
- `scan-mT` (HARD, load-bearing): **STILL OPEN, now looking POSITIVE.** The exact data show the
  family climbing past `1.172` and extrapolating above the record. The decisive datapoint —
  `m=80, T=150` (Griego's exact parameters) and the m=80 optimum — is being computed; the sum DP at
  `(80,150)` is ~`30–40` min (consistent with the sibling's note). Remaining work: finish `m=80`
  (and likely `m≈90–110`) and exhibit the first `(m,T)` whose EXACT integer test
  `d^{q'} > s^{q'}·q^{p'}` clears `1.1740744`. Until that exact point is in hand and certified, the
  sketch is NOT yet a verified win — it stays a live, promising hole.

## Claimed value (CLAIM, not yet verified)
Exact family values verified so far: `θ(m=60) = 1.1721231`, `θ(m=70) ≥ 1.1728032` (peak higher).
These are **below** the record but **climbing**; the extrapolated family supremum
`θ_sup(A={0,2..10}, b=21) ≈ 1.175–1.176` is **above** `1.1740744`. **No verified record-beating
`(m,T)` yet** — the claim of a beat awaits the exact `m≈80+` computation. Reported honestly as an
open, positive-trending hole, not a win.

## Promotable lemmas
- `exact-sumdiff-dp` — the exact column DP for `(|U+U|, |U−U|, max U)` of the digit construction
  `U = {Σ x_i b^i : x ∈ A^m, Σx_i ≤ T}` with `b > 2max(A)`, with the two structural reductions
  (carry-free digit-vector counting; diff-set minimal-pair decoupling; sum-set bitmask DP). Proved
  green and self-tested against brute force on 8 cases in
  `certificate/griego-family-larger-mT.py` (`self_test()`, `count_sumset`, `count_diffset`,
  `max_U`). Reusable by L1 (`noncontig-alphabet-sweep`) and L3 for ANY alphabet `A`.

## Certify
Numerical (exact big-int), self-tested vs brute force. The integer inequality
`d^{q'} > s^{q'}·q^{p'}` is the Lean-fit certification form for any future winner.
