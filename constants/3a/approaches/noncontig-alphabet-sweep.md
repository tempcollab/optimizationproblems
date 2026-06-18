# L1 — Non-contiguous digit-alphabet sweep

**Slug:** `noncontig-alphabet-sweep`   **Target:** lower bound, beat `C_3a > 1.1740744` (Griego 2026).

## Strategy
The lower-bound frontier reduces, by the [GHR2007] lemma, to exhibiting **one** finite
`U ⊂ ℤ_{≥0}` with `0 ∈ U` and reading off `s=|U+U|`, `d=|U−U|`, `q=2·max(U)+1`,
`θ = 1 + log(d/s)/log(q)`, with `C_3a ≥ θ`. We use the digit/base family
`W(m,T,A) = {x∈A^m : Σx_i≤T}`, `g(x)=Σx_i b^i`, `b=2max(A)+1`, `U=g(W)`. Because `b>2max(A)`,
`g` is injective and base-separated (no carry in sums, no borrow in differences), so
`|U+U|` = #{distinct digit-wise sum vectors} and `|U−U|` = #{distinct difference vectors}.
The unswept discrete lever is the **alphabet** `A` (Griego's jump came from non-contiguous
`{0,2,…,10}`); prior asymptotics fixed contiguous `{0..B}`.

## What I closed this round

### Hole `exact-sumdiff-dp` — CLOSED (verified)
Implemented the exact column-DP `count_sum`, `count_diff`, `maxU` in
`certificate/noncontig-alphabet-sweep.py`. The cap `Σx_i≤T, Σy_i≤T` couples columns, so a
digit-wise vector `v` is feasible iff some per-column split `(x_i,y_i)` has running
`(Σx,Σy)` both `≤T`. The DP carries the reachable set of `(Σx,Σy)` prefixes as a packed
big-integer bitmask (bit index `Σx·stride+Σy`, `stride=T+maxdigit+1` to prevent wrap);
transitions are bit-shift ORs over the per-column split set. `maxU` is greedy (load highest
positions to the max digit, validated against brute force).
**Self-test (`self_test()`, asserted on every run): the DP equals brute force on 10 cases**,
contiguous AND non-contiguous (`{0,2,…,10}`, `{0,2,5}`, `{0,1,3,4}`, `{0,2,4,6}`, …). This is
a promotable lemma candidate (the shared `exact-sumdiff-dp` dependency of L1/L2/L3).

### Hole `search-alphabet` — CLOSED, with a NEGATIVE result (the load-bearing finding)
Swept the alphabet space with the exact DP:
- **All 45 single/double-digit drops from `{0..10}`** (m=20,T=38): the unique top is
  `{0,2,3,…,10}` (drop digit 1) at θ=1.158446. The entire TOP-5 are "drop 1 plus possibly
  drop high digits", all strictly below. Dropping any *other* single digit (e.g. drop 2 →
  1.1219, drop 9 → 1.1370) is far worse; adding a *second* gap always hurts.
- **m=30,T=56 screen** (7 alphabets incl. extended tops, multi-gap): `{0,2,…,10}` wins at
  1.164431; every variant below.
- **drop-1 with varying top B** (m=30, fixed T=56): B=6→1.1415, 7→1.1556, 8→1.1622,
  9→1.164541, 10→1.164431, 11→1.163026, 12→1.160960 — a broad B∈{9,10} plateau. At the *fixed*
  T=56, B=9 appeared to edge B=10 by ~1e-4, which looked like a micro-lead.
- **B=9 vs B=10, each with its OWN optimal T** (m=30): this RESOLVES the apparent lead.
  B=9 (`{0,2,…,9}`, base 19) peaks at **1.1645409 (T=56)**; B=10 (`{0,2,…,10}`, base 21, =Griego)
  peaks at **1.1652053 (T=60)**. B=10 wins once T is optimized per alphabet — the earlier
  B9>B10 was purely a wrong-T artifact (the larger-max-digit alphabet wants a higher cap).
  **Griego's `{0,2,…,10}` base-21 is the genuine optimum.**

**Conclusion: the alphabet lever is saturated at Griego's `{0,2,…,10}` base 21.** No swept
alphabet beats `1.1740744` at finite `m`; the record is the `(m,T)→∞` limit of *this single
alphabet*, which is sibling sketch `griego-family-larger-mT`'s job (push m,T), not the alphabet
sweep. This is an honest, well-tested negative for the new-alphabet hypothesis — real
information that routes effort off this lever.

## Value claimed
**Best θ from a NEW alphabet: does NOT beat the record.** At the moderate `m` where the sweep
runs (m≤30), the best alphabet is Griego's own `{0,2,…,10}` base 21, peaking at θ=1.1652053
(m=30, T=60), below 1.1740744 (the record is its own m→∞ limit). Every *other* alphabet is
strictly worse. This sketch produces **no new bound** — it refutes the premise that a different
alphabet beats Griego's. (A claim, pending reviewer confirmation; clearly NOT a verified
advance, and NOT a record-break.)

## Remaining holes
- **None load-bearing for this sketch.** Both holes (`exact-sumdiff-dp`, `search-alphabet`) are
  closed; the alphabet search is exhausted with a negative. The one engineering limitation: the
  bigint pair-set DP is too slow to *reproduce* the exact m=80,T=150 numbers (sum DP ~37 min,
  13476 states, |U+U|~10^76; diff DP ~3× slower, did not finish in ~50 min). This does not affect
  the conclusion (the DP is validated by `self_test()` on 10 small cases, and alphabet ranking is
  read off at m≤30 where it is fast). A faster diff DP would let one re-derive Griego's exact
  certificate, but that confirms the record rather than beating it — out of this sketch's scope.

## Certify
The load-bearing check is exact and Lean-ready: `θ > P/Q ⟺ d^Q > s^Q·q^(P−Q)`
(`certify_target`, verified to match the float comparison above/below in tests) — a pure
big-integer inequality, transcribable to Lean `native_decide` with `P/Q` a small-denominator
rational. No floating point in the load-bearing step.

## Promotable lemmas
- **`exact-sumdiff-dp`** — the column-DP `count_sum/count_diff/maxU` computing `|U+U|`,`|U−U|`,
  `max(U)` exactly for `U=g(W(m,T,A))`, proved equal to brute force on 10 cases by `self_test()`
  in `certificate/noncontig-alphabet-sweep.py`. Reusable by `griego-family-larger-mT` and
  `largedev-rate-optimization`. (Python certificate, not a Lean lemma yet — promote as the
  shared exact oracle.)
