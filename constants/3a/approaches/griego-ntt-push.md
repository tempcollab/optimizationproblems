# Sketch `griego-ntt-push` — fast exact sum-set count to push m=130-140 (higher θ)

## Strategy
Continue the verified Griego-family climb past the m=110 compute wall. The held bound C_3a > 1.176
sits at (110,210); θ is monotone increasing in m toward a conjectural family supremum Λ (geometric-
tail estimate ≈1.1785, R4 power-law fit ≈1.185 — both comfortably below the 1.25 GHR cap). The only
cheap lever past 1.176 is MORE m on the SAME family (base-21 / A={0,2,…,10} is the unique optimal
alphabet — `noncontig-alphabet-sweep` proved this; that family is saturated in alphabet, only m is
left).

**Realistic gain (R5 explorer, recomputed from the exact scan `scan-mT-results.txt`):** the exact
θ(m) step shrinks geometrically (ratio ≈0.83): m=80→1.1740744, 90→1.1748818, 100→1.1754955,
110→1.1760056 (held). Geometric-tail projection: **m=130 → θ≈1.1768, registering held ≈1.1767
(+0.0008)** — the highest-value SINGLE next step, clearing the held with a modest but real margin.
m=150→~1.1773, m=200→~1.1780; the whole lever tops out ≈+0.0025 over 1.176 and is heavily
diminishing past m≈130. **Target m≈130-140 first, not 200** — one new exact point registers a higher
held at no further mathematics.

**Why a new algorithm (not just more of L2):** the R3 dynamic-low-clamp sum-set bitmask DP closes
m≤110 in seconds but walls at m=130+ (per-state reachable-Σx mask width grows with T; a single m=130
point did not finish in ~5 min of R4 scouting). The diff-set DP (2-D over (Σx*,Σy*)) and max_U
(greedy) ALREADY scale cheaply to m=200 — **only the sum-set count is the wall.** So the engineering
target is narrow: a fast exact `|U+U|` count, nothing else.

This is the m-push compute hole of `griego-family-larger-mT`, given its own slug + file so a builder
can own it in parallel without colliding with L2's verified file. It does NOT disturb L2's held
1.176 — it tries to RAISE it. Borrows: `griego-family-larger-mT` (the oracle `count_sumset`, the
family, `count_diffset`/`max_U` reused directly, the certificate form), `exact-sumdiff-dp` lemma.

## The route — shift-OR big-int convolution PRIMARY, NTT fallback (R5 revision)

The R4 plan named NTT as the route. The R5 explorer flagged a **lower-risk path that should be tried
FIRST** and that is now the primary plan:

**PRIMARY — bit-packed big-integer shift-OR convolution.** The reachable-Σx set is a *set of
integers*, so represent it as ONE Python `int` bitmask. The current oracle already does this — the
suspected real bottleneck is not the asymptotics but the *Python-level per-x, per-state* iteration
(`for x in shifts[w]: nR |= (R << x)` over a dict of (Sv,R) states). The shift-OR reformulation does
the inner combine as **whole-int C-level shifts** and, crucially, looks for a state representation
that does not blow up the number of distinct (Sv,R) keys at large m:
- "add a column with digit-set X to the reachable set" is `newmask = OR over x in X of (mask << x)`,
  i.e. `mask` convolved (Minkowski/OR) with the column's reachable-shift set — pure big-int shifts.
- the dynamic low-clamp (`mask >> lo << lo`, lo = max(0, Σv−T)) keeps the int WIDTH bounded to ~T
  bits, exactly as the oracle already does.
- the win is (a) C-level shifts instead of Python bit loops, and/or (b) collapsing the Σv axis where
  possible so the state count stops exploding. **This is trivially EXACT — it IS the set; no modulus,
  no CRT, no float rounding can corrupt an integer count.** It reuses the certified oracle directly
  as ground truth.

**FALLBACK — NTT / exact-integer FFT.** Only if shift-OR still walls at m=130. Per-layer convolution
of the reachable-Σx indicator, repeated-squaring in m (m enters logarithmically). MUST be exact: the
mask is 0/1, so this is an OR-convolution (take the support of the arithmetic convolution) — plain
NTT over a prime modulus / CRT, NOT float FFT unless rounding error is rigorously bounded < 0.5. The
win over a well-written shift-OR is mostly constant-factor, and it carries the exactness risk
shift-OR does not — so it is the fallback, not the lead.

**SIDE-PROBE (high upside, speculative).** Because the alphabet is {0,2,…,10} (only digit 1 missing),
the per-column reachable Σx set is "all sums except those forced through the missing-1 gap." There may
be an inclusion–exclusion against the *contiguous* {0,…,10} sum-set (clean interval/binomial count)
minus the absent-1 corrections. If it closes, the sum-set count is near-closed-form and the wall
vanishes. Flag only — not the build path.

## Holes (file: certificate/griego-ntt-push.py)
1. **`fast_sumset_count` — OPEN (load-bearing engineering).** Exact |U+U|. PRIMARY: bit-packed
   big-int shift-OR convolution with the dynamic low-clamp (reuse the oracle's clamp, replace the
   per-bit Python loop with whole-int shifts; reduce the (Sv,R) state explosion). FALLBACK: NTT /
   exact-integer FFT, repeated squaring in m. Trivially exact in the shift-OR form.
2. **`validate_fast_dp` — OPEN (MANDATORY GATE — make-or-break).** Validate `fast_sumset_count`
   EXACTLY against the R3 clamped-DP oracle (`count_sumset`, imported from L2) AND brute force on the
   smallest cases, on 12+ (m,T) incl. clamp-exercising and non-contiguous ones, BEFORE any large-m
   number is trusted. Rule (R3): a fast-but-wrong DP fabricates a bound. A miscount of 1 fabricates
   the held. The speedup is worthless if this gate is not green first.
3. **`scan_large_m` — OPEN (incremental output REQUIRED).** Scan m=120..140 along the optimal ray
   T≈1.9m, PRINTING EACH (m,T,θ,s,d,M) point INCREMENTALLY as it completes (Rule R2 watchdog: no
   single silent Bash > ~5 min — checkpoint per point; run in background with an until-loop watcher
   if needed). Target the first m∈[120,140] whose exact θ clears 1.1761 (the next tick past held).
4. **`certify_best` — OPEN.** At the best (m,T) emit the largest k/10000 with
   d^10000 > s^10000·(2M+1)^(k-10000), and the negative control (k+1 fails) so the new held is
   registered TIGHT — same certificate FORM as the held 1.176, at a higher θ. That k/10000 is the
   new held candidate (> 1.176).

## Hard step (named, R5)
The load-bearing hole is **HOLE 1 `fast_sumset_count`** — getting an exact |U+U| count that runs at
m≈130 inside the watchdog window. The *mechanism* that makes it hard: the missing digit 1 makes each
column's reachable set non-contiguous (cached lemma: no interval shortcut, no min/max collapse — a
hole sits between top-reachable Σx≤T and Σv−T), so the state is genuinely (Σv, reachable-Σx-set) and
the set count grows with T. Shift-OR attacks the *constant factor* (C-level shifts) and the *state
explosion*; whether that alone breaks the m=130 wall is the open question. **The MANDATORY oracle
gate (HOLE 2) and incremental per-point output (HOLE 3) are non-negotiable correctness/watchdog
requirements, not optional polish** — they are the difference between a real higher held and a
fabricated one / a killed round.

## State
- Revised R5: PRIMARY route switched from NTT to bit-packed shift-OR big-int convolution (lower-risk,
  trivially exact, reuses oracle); NTT demoted to fallback; m-target narrowed to 130-140; side-probe
  (inclusion–exclusion vs contiguous sum-set) noted. Prime build candidate this round.
- New R4: opened/registered, PARKED, never built.

## R5 BUILD — all four holes CLOSED (claimed held 1.176 → 1.1771)

**Key finding that re-scoped HOLE 1.** Instrumenting the certified R3 oracle (`count_sumset`) showed
the (Σv, R) state count **saturates at fixed T** — ~26.7k states at (110,210), ~37.2k at (130,247) —
so the oracle is NOT exponential in m; its cost is ~linear in m at fixed T (each m-step re-processes
the saturated state set). At T≈1.9m the per-point cost is well inside the watchdog: m=130 sum-set
~55-67s, m=140 ~68s, diff-set ~25-40s, max instant. **The R4 "m=130 did not finish in 5 min" was a
too-large-T / un-checkpointed scout, not a true asymptotic wall.** So the shift-OR bitmask DP the plan
named as PRIMARY (which the oracle already IS — `mask|=(mask<<x)` + dynamic low-clamp) reaches m=140
directly. NTT was not needed.

- **HOLE 1 `fast_sumset_count` — CLOSED.** Engine = the certified shift-OR bitmask DP (reused, exact —
  it IS the reachable set; no modulus/CRT/float). Plus an **independent** `indep_sumset` (set-based
  Minkowski DP, frozenset states, no bitmask/shift/clamp — a genuinely different algorithm) added so
  the gate is a real cross-check, not a tautology against the same engine.
- **HOLE 2 `validate_fast_dp` (MANDATORY GATE) — CLOSED, PASSES.** 3-way exact agreement
  `brute == indep == oracle` on **15** cases (Griego non-contiguous {0,2,…,10} with T-clamp binding,
  AND a contiguous control {0,…,5}); 2-way `indep == oracle` on **5** larger cases (m up to 9, where
  brute's O(|U|²) sumset is infeasible). All match exactly. A miscount of 1 would diverge the
  independent set-DP; it does not.
- **HOLE 3 `scan_large_m` — CLOSED.** Incremental per-point scan (checkpoints to /tmp/ntt_cache, prints
  each quantity as it lands). Found per-m peak T: m=130 peak at T=247 (θ=1.1768118909), m=140 peak at
  T=265 (θ=1.1771373652).
- **HOLE 4 `certify_best` — CLOSED.** Tightest k/10000 by bisection on the exact integer inequality
  `d^10000 > s^10000·(2M+1)^(k−10000)`, with the negative control:
  - **m=130, T=247:** PASS k=11768, FAIL k=11769 → C_3a > **1.1768**.
  - **m=140, T=265 (BEST):** PASS k=11771, FAIL k=11772 → C_3a > **1.1771** (tight at den=10000).
  Verified independently with explicit big-int arithmetic outside the module; redundant 400-bit log
  test confirms θ > 1.1740744.

**Exact data (m=140, T=265):** s=|U+U| 136 digits (head `88785247661758800689`), d=|U−U| 169 digits
(head `54747299867053367517`), M=max U 185 digits (head `64516569533889487833`), float θ ≈ 1.1771373652.

**Claimed held (unverified until reviewer confirms): C_3a > 11771/10000 = 1.1771**, beating the prior
held 1.176 by +0.0011 and the external record 1.1740744 by +0.0031.

## What would push further
- m=150-160 along the optimal ray would add ~+0.0002-0.0004 (diminishing; the diff-set 2-D DP grows
  as T² so m≈160 is still tractable, m≈200 starts to bite). Family limit Λ≈1.1785 caps the whole lever
  ~+0.0025 over 1.176; we are now at +0.0011, roughly halfway to the cap. A genuinely bigger jump needs
  a NEW base/alphabet (fresh-sketch question), not more m.
- Lean-fit: the certificate FORM stays Lean-fit at the integer level, but a higher held at den=10000
  has ~1.4M-digit operands — out of `native_decide` reach, so this raises held as a Python big-int
  cert, not a Lean theorem (an operand-size issue, not a step-shape one).

## Promotable lemmas
None new. The sum-set engine is the already-certified `exact-sumdiff-dp` lemma (reused, not re-proved).
`indep_sumset` is a validation-only cross-checker (slow set-DP), not a reusable production lemma.
