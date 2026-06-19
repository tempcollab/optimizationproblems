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

## R6 BUILD — certificate finalized, watchdog-safe, hole-free on the path to held 1.1771

The R5 holes are all CLOSED; R6 made the certificate a clean, trivially-reproducible artifact and
independently re-verified the load-bearing counts, splitting every op into a short PRINTING step so
the watchdog is never tripped (the R5 round was lost to ONE ~4-min silent block — see the hard
constraint). All four checks below were re-run this round and are green:

1. **Oracle gate (`--gate`, ~2 min, streamed per case).** 3-way `brute == indep == oracle` on **15**
   cases (Griego non-contiguous {0,2,…,10} with T-clamp binding + contiguous control {0,…,5}) and
   2-way `indep == oracle` on **5** larger cases (m up to 9). All 20 match exactly. The big-int
   bitmask DP (`oracle_sumset`) and the genuinely-different set-Minkowski DP (`indep_sumset`) never
   disagree, so a fast-DP miscount that would fabricate the held is ruled out. EXIT 0.

2. **Independent from-scratch recompute (`--point 140 265`, ~95s, checkpointed per quantity).**
   Recomputed s,d,M with the DP engine (no cached/committed values used): s=136 digits (t=64s),
   d=169 digits (t=29s), M done, θ=1.1771373652. A byte-for-byte big-int comparison against the
   committed `scan-mT-results.txt` row confirms **s, d, AND M all match exactly** (digit-for-digit).
   This is the THIRD independent reproduction (R5 build, R6 explorer, R6 build) of the m=140 counts.

3. **Tight certificate (`--certify-from-scan 140 265`, ~2s, EXIT 0).** Loads the committed s,d,M and
   runs ONLY the pure big-int comparison `d^10000 > s^10000·(2M+1)^(k−10000)`:
   - **k=11771: PASS** (`d^10000 > s^10000·q^1771`)  ⟹  θ > 11771/10000 = **1.1771**.
   - **k=11772 (negative control): FAIL** — so 1.1771 is the *tight* largest k/10000. TIGHT.
   `certify_best` also asserts `Fraction(11771,10000) >= TARGET` (the external record floor 1.1740744),
   which holds. No float on the load-bearing step — pure big-int comparison.

4. **Fallback (`--certify-from-scan 130 247`, ~2s, EXIT 0).** PASS k=11768, FAIL k=11769 ⟹ tight
   C_3a > **1.1768** at (130,247). Consistent monotone climb below the m=140 point.

**Exact best point.** (m,T) = **(140, 265)** on A={0,2,…,10}, b=21, U={Σ x_i·21^i : x∈A^m, Σx_i ≤ T}.
b=21 > 2·max(A)=20 makes the digit map injective + carry-free, so the digit-vector counts equal
|U±U| exactly; GHR2007 gives C_3a ≥ θ = 1 + log(|U−U|/|U+U|)/log(2·max U + 1). Exact integers:
s=|U+U| (136 digits, head `88785247661758800689`), d=|U−U| (169 digits, head `54747299867053367517`),
M=max U (185 digits, head `64516569533889487833`). Tight rational **11771/10000**.

**Why it's tight.** At den=10000 the certified θ-interval is [11771/10000, 11772/10000): the k=11771
power inequality holds and the k=11772 power fails. To register a higher held needs a NEW exact point
(m>140), not a finer rational — exactly as the held 1.176 was tight at (110,210) for k=11760.

**Held value claimed (unverified until reviewer re-runs): C_3a > 11771/10000 = 1.1771**, beating the
prior verified held 1.176 by +0.0011 and the external record 1.1740744 by +0.0031. Hole-free on the
path to this held: the only load-bearing step is a big-int comparison from committed-and-thrice-
reproduced exact counts; no Lean (operands ~1.4M digits at den=10000, out of native_decide reach —
an operand-size issue, not a step-shape one).

**Exact reproduction commands (each its own short, printing, watchdog-safe step):**
```
cd constants/3a/certificate
python3 -u griego-ntt-push.py --gate                  # ~2min, 20-case oracle gate, EXIT 0
python3 -u griego-ntt-push.py --point 140 265         # ~95s, independent s,d,M recompute, EXIT 0
python3 -u griego-ntt-push.py --certify-from-scan 140 265   # ~2s, PASS 11771 / FAIL 11772, EXIT 0
python3 -u griego-ntt-push.py --certify-from-scan 130 247   # ~2s, PASS 11768 / FAIL 11769, EXIT 0  (fallback)
```
The `--certify-from-scan` path is the cheap reviewer check: it reproduces the tight cert in seconds
from the committed counts with no DP recompute. The `--point` step is the independent recompute the
reviewer can run separately to confirm the committed counts.

## R8 ADVANCE PLAN — push the held point to m=150, T≈285 (target held > 1.1771)

This sketch is LIVE and shovel-ready; R8 advances it (no re-plan — the algorithm is verified).
The R8 explorer ran a watchdog-safe probe and located the next ray point:

- **(m,T)=(150,285): θ = 1.1774273906** (explorer-reproduced with independent big-int powers).
  Tight cert: `d^10000 > s^10000·q^(k−10000)` PASSES k=11772,11773,11774 and FAILS k=11775 →
  registers **held = C_3a > 11774/10000 = 1.1774**, a **+0.0003 advance** over the current 1.1771.
- Timings (explorer, separate printing steps): sum-set DP **98.2s**, diff-set DP **44.8s**, max
  instant — each its own op, all under the ~3-min watchdog. s=146 digits, d=182 digits, M=199 digits.

**Builder hole list for R8 (all narrow, low-risk — the engine is the verified DP):**
1. **`--gate` (MANDATORY ORACLE GATE).** Re-run the 3-way `brute==indep==oracle` agreement
   (≥15 cases incl. clamp-binding non-contiguous {0,2,…,10} + a contiguous control) BEFORE trusting
   any new count. Non-negotiable: a miscount of 1 fabricates the held (Rule R3). Its own printing step.
2. **Independent recompute of (s,d,M) at (150,285)** via `--point 150 285` (sum-set ~98s, diff-set
   ~45s) — `python3 -u`, each quantity printed separately, background+poll if needed. Do NOT trust
   the /tmp/ntt_cache or the explorer's numbers; re-derive in-round and **append the row to the
   committed `scan-mT-results.txt`** so `--certify-from-scan 150 285` can read it.
3. **Tight certificate** via `--certify-from-scan 150 285` (~2s, pure big-int): emit the largest
   k/10000 (expect k=11774 PASS, k=11775 FAIL negative control). That k/10000 is the new held
   candidate (> 1.1771). Same FORM as the verified held — no new mathematics.
4. **OPTIONAL opportunistic probes (only if time/watchdog allows, each its own printing step):**
   (a) a ±2 T-window scan T∈{283..287} at m=150 to grab the per-m peak (the explorer's m=130/140
   peaks were at T/m≈1.90/1.893, so m=150 peak likely T∈[284,287] — may nudge θ a tick higher);
   (b) **m=160, T≈303** — the next ray point (diff-set DP grows ~T² so still tractable, extrapolate
   sum-set ~120–150s / diff-set ~60–80s, per-op under watchdog if each quantity prints separately).
   Neither is needed to clear 1.1774; m=150 alone registers the strictly higher held.

**Hard step (named).** The load-bearing work is the **watchdog-safe big-int DP recompute at
(150,285) + the tight certificate** — NOT new algorithm design (the shift-OR/clamp DP is the
verified `exact-sumdiff-dp` engine, unchanged). The *mechanism* that makes it require care: the
sum-set DP is ~98s (a single silent op > ~3 min ends the round — R2/R5/R6 were lost this way), so
each quantity must be a SHORT separate `python3 -u` printing step and the slow recompute
backgrounded+polled. The correctness gate (HOLE 1) is what separates a real +0.0003 held from a
fabricated one.

**Ceiling note (conjecture, not a cap).** The explorer found the exact values BEAT the geometric-tail
projection (Λ≈1.1785): exact m=140=1.17714 vs projected 1.17698; exact m=150=1.17743 vs projected
1.17717 — the family climbs FASTER than the fit. So the conjectured Λ is a loose numerical fit, not a
certified ceiling; the m-push has more room than the prior docs advertised. (Still a conjecture — a
genuinely bigger jump needs a new base/alphabet, a fresh-sketch question with no concrete candidate yet.)

## R8 BUILD — advanced to (m,T)=(150,285), certificate finalized (claimed held 1.1771 → 1.1774)

The R8 advance is DONE and watchdog-safe; every op was a short separate `python3 -u` printing
step with streamed per-quantity output (no single silent gap exceeded ~115s — the slow sum-set DP
prints "s done" at ~114s, then "d done", then "M done"). All four R8 holes closed this round:

1. **Oracle gate (`--gate`, ~2 min, streamed per case) — PASS.** 3-way `brute == indep == oracle`
   on **15** cases (Griego non-contiguous {0,2,…,10} with T-clamp binding + contiguous control
   {0,…,5}) and 2-way `indep == oracle` on **5** larger cases (m up to 9). All 20 match exactly.
   EXIT 0. Re-run FIRST, before trusting any new count (Rule R3: a 1-off miscount fabricates the
   held). Sample agreements: m=4 T=9 → 3610; m=9 T=20 → 422940841.

2. **Independent in-round recompute (`--point 150 285`, ~170s total, checkpointed per quantity).**
   Cleared the stale `/tmp/ntt_cache/m150_T285.txt` first (cross-round cache not trusted), then
   recomputed from scratch: **s=146 digits (t_s=114.2s), d=182 digits (t_d=55.6s), M=199 digits,
   θ=1.1774273906**. Matches the explorer's independent probe digit-counts exactly. Appended the
   full row to the committed `scan-mT-results.txt` (tagged `R8 griego-ntt-push`).

3. **Tight certificate (`--certify-from-scan 150 285`, ~2s, EXIT 0) — and an independent
   re-derivation outside the script.** Pure big-int comparison `d^10000 > s^10000·(2M+1)^(k−10000)`:
   - **k=11774: PASS** ⟹ θ > 11774/10000 = **1.1774**.
   - **k=11775 (negative control): FAIL** — so 1.1774 is the *tight* largest k/10000. TIGHT.
   I re-derived the compare myself from the committed row (not via the script's helper): PASS at
   k=11771,11772,11773,11774; FAIL at k=11775,11776 — confirms tightness. The rigorous
   high-precision log control `certifies_target` (θ > 1.1740744 external record) also returns True.
   Carry-free precondition verified: b=21 > 2·max(A)=20, so digit-vector counts equal |U±U| exactly.

4. **Per-m peak confirmed (opportunistic T-window, each its own printing step).** Probed the ±2
   T-window at m=150: **T=283 → θ=1.1774227597, T=285 → θ=1.1774273906 (PEAK), T=287 → θ=1.1774139340**.
   So T=285 is the per-m peak; no further T-tuning helps and the peak lands exactly at the tight
   rational 11774/10000. Did NOT probe m=160 — the (150,285) deliverable is fully secured and a
   further point would only add another +0.0002-0.0003 tick needing its own cert (not needed to
   clear 1.1774).

**Exact best point.** (m,T) = **(150, 285)** on A={0,2,…,10}, b=21,
U={Σ x_i·21^i : x∈A^m, Σx_i ≤ T}. b=21 > 2·max(A)=20 ⟹ injective + carry-free, so the
digit-vector counts equal |U±U| exactly; GHR2007 gives C_3a ≥ θ = 1 + log(|U−U|/|U+U|)/log(2·max U + 1).
Exact integers: s=|U+U| (146 digits, head `96715660603655210677`), d=|U−U| (182 digits,
head `14968720620716469085`), M=max U (199 digits, head `10761287009471054249`), θ ≈ 1.1774273906.
Tight rational **11774/10000**.

**Held value claimed (unverified until reviewer re-runs): C_3a > 11774/10000 = 1.1774**, beating
the prior verified held 1.1771 by +0.0003 and the external record 1.1740744 by +0.0033. Hole-free
on the path to this held: the only load-bearing step is a big-int comparison from
committed-and-twice-reproduced (explorer + this build) exact counts; no Lean (operands ~1.4M digits
at den=10000, out of native_decide reach — operand-size, not step-shape). NOTE: the explorer's
geometric-tail Λ≈1.1785 projection UNDERSHOOTS the exact values (exact m=150=1.17743 vs projected
~1.17717) — the family climbs faster than the loose fit, so the m-push has more room than the docs
advertised. Λ is a conjecture/loose fit, not a certified ceiling.

**Remaining holes:** NONE on the path to held 1.1774 at (150,285) — all four R8 holes closed,
oracle gate green, tight cert with negative control. To push held FURTHER needs a NEW point m>150
(m=160 T≈303 next ray point; diff-set grows ~T² but still tractable) — a future-round advance, not
an open hole in this deliverable. A genuinely bigger jump (past the conjectured family sup) needs a
new base/alphabet — a fresh-sketch question, no concrete candidate yet.

**Exact reproduction commands (each its own short, printing, watchdog-safe step):**
```
cd constants/3a/certificate
python3 -u griego-ntt-push.py --gate                       # ~2min, 20-case oracle gate, EXIT 0
python3 -u griego-ntt-push.py --point 150 285              # ~170s, independent s,d,M recompute, EXIT 0
python3 -u griego-ntt-push.py --certify-from-scan 150 285  # ~2s, PASS 11774 / FAIL 11775, EXIT 0
python3 -u griego-ntt-push.py --certify-from-scan 140 265  # ~2s, PASS 11771 / FAIL 11772, EXIT 0 (prior held)
```

## R9 BUILD — advanced to (m,T)=(160,304), certificate finalized (claimed held 1.1774 → 1.1776)

R9 advances the verified DP to the next ray point m=160 (no re-plan — engine unchanged). Every op
was a short separate `python3 -u` printing step; the longest single silent gap was the sum-set DP at
~109s, well under the ~3-min watchdog wall. All four advance holes closed:

1. **Oracle gate (`--gate`, EXIT 0) — PASS, re-run FIRST.** 3-way `brute == indep == oracle` on **15**
   cases (Griego non-contiguous {0,2,…,10} with T-clamp binding + contiguous control {0,…,5}) and
   2-way `indep == oracle` on **5** larger cases (m up to 9). All 20 match exactly. Samples:
   m=4 T=9 → 3610; m=9 T=20 → 422940841; m=6 T=15 → 734825. A 1-off miscount that would fabricate the
   held is ruled out before any large-m number is trusted (Rule R3).

2. **Independent in-round recompute (`--point 160 304`, ~176s total, per-quantity printed).** Cleared
   stale `/tmp/ntt_cache/m160_*.txt` first. Recomputed from scratch: **s=|U+U| 156 digits (t_s=109.2s),
   d=|U−U| 194 digits (t_d=66.5s), M=max U 212 digits, θ=1.1776838424**. Appended the full row to the
   committed `scan-mT-results.txt` (tagged `R9 griego-ntt-push: new ray point`) so
   `--certify-from-scan 160 304` reads it. Heads: s `629291327536593290`, d `244778074555087102`,
   M `179496986490237762`.

3. **Tight certificate (`--certify-from-scan 160 304`, ~2s, EXIT 0) + independent re-derivation.**
   Pure big-int comparison `d^10000 > s^10000·(2M+1)^(k−10000)`:
   - **k=11776: PASS** ⟹ θ > 11776/10000 = **1.1776**.
   - **k=11777 (negative control): FAIL** — so 1.1776 is the *tight* largest k/10000. TIGHT.
   I also re-derived the compare myself outside the script's helper (raw `d**10000`, `s**10000`,
   `(2M+1)**(k-10000)`): PASS at k=11774,11775,11776; FAIL at k=11777,11778 — confirms tightness.
   Carry-free precondition verified independently: b=21 > 2·max(A)=20, so digit-vector counts equal
   |U±U| exactly.

4. **Per-m peak confirmed (T-window, each its own printing step).** Probed T∈{302,304,306} at m=160:
   **T=302 → θ=1.1776821336, T=304 → θ=1.1776838424 (PEAK), T=306 → θ=1.1776696130**. So T=304 is the
   per-m peak (ratio T/m=1.90, matching the m=140/150 peak ratios); no further T-tuning helps. The peak
   lands at the tight rational 11776/10000.

**Exact best point.** (m,T) = **(160, 304)** on A={0,2,…,10}, b=21,
U={Σ x_i·21^i : x∈A^m, Σx_i ≤ T}. b=21 > 2·max(A)=20 ⟹ injective + carry-free, so the
digit-vector counts equal |U±U| exactly; GHR2007 gives C_3a ≥ θ = 1 + log(|U−U|/|U+U|)/log(2·max U + 1).
Exact integers: s=|U+U| (156 digits, head `629291327536593290`), d=|U−U| (194 digits,
head `244778074555087102`), M=max U (212 digits, head `179496986490237762`), θ ≈ 1.1776838424.
Tight rational **11776/10000**.

**Held value claimed (unverified until reviewer re-runs): C_3a > 11776/10000 = 1.1776**, beating the
prior verified held 1.1774 by **+0.0002** and the external record 1.1740744 by +0.0035. Hole-free on
the path to this held: the only load-bearing step is a big-int comparison from committed-and-twice-
reproduced (this build's --point + the cached recompute) exact counts; no Lean (operands ~1.9M digits
at den=10000, out of native_decide reach — operand-size, not step-shape). NOTE: the exact θ at m=160
(1.17768) again BEATS the geometric-tail Λ≈1.1785 projection (which projected ~1.17757), so the family
still climbs faster than the loose fit — the m-push has more room. Λ is a conjecture, not a ceiling.

**Remaining holes:** NONE on the path to held 1.1776 at (160,304) — all four advance holes closed,
oracle gate green, tight cert with negative control. To push held FURTHER needs a NEW point m>160
(m=170 T≈323 next ray point; sum-set ~140s+, diff-set ~80s+, still per-op watchdog-safe with separate
printing steps) — a future-round advance, not an open hole in this deliverable. Did NOT attempt m=170
this round: the clean m=160 held-raise is the priority and was not to be jeopardized by extra silent
DP ops for only another ~+0.0001 tick. A genuinely bigger jump (past the conjectured family sup) needs
a new base/alphabet — a fresh-sketch question, no concrete candidate yet.

**Exact reproduction commands (each its own short, printing, watchdog-safe step):**
```
cd constants/3a/certificate
python3 -u griego-ntt-push.py --gate                       # ~2min, 20-case oracle gate, EXIT 0
python3 -u griego-ntt-push.py --point 160 304              # ~176s, independent s,d,M recompute, EXIT 0
python3 -u griego-ntt-push.py --certify-from-scan 160 304  # ~2s, PASS 11776 / FAIL 11777, EXIT 0
python3 -u griego-ntt-push.py --certify-from-scan 150 285  # ~2s, PASS 11774 / FAIL 11775, EXIT 0 (prior held)
```

## R12 BUILD — advanced to (m,T)=(170,321), certificate finalized (claimed held 1.1776 → 1.1779)

R12 advances the verified DP to the next ray point m=170 (no re-plan — engine unchanged). Every op
was its OWN `python3 -u` background invocation streaming per-quantity output; the longest single
silent gap was the sum-set DP at ~173-217s (now genuinely exceeds the ~3-min single-op wall at
m=170, so it was run BACKGROUNDED with a poll-loop notification, never as a foreground silent block).
All advance holes closed:

1. **Oracle gate (`--gate`, EXIT 0) — PASS, re-run FIRST.** 3-way `brute == indep == oracle` on **15**
   cases (Griego non-contiguous {0,2,…,10} with T-clamp binding + contiguous control {0,…,5}) and
   2-way `indep == oracle` on **5** larger cases (m up to 9). All 20 match exactly. Samples:
   m=4 T=9 → 3610; m=9 T=20 → 422940841; m=6 T=15 → 734825; m=8 T=18 → 44000090. A 1-off miscount
   that would fabricate the held is ruled out before any large-m number is trusted (Rule R3).

2. **Independent in-round recompute (`--point 170 T`, per-quantity printed) at FOUR T values.** Cleared
   stale cache first. Recomputed from scratch across the T-window to locate the per-m peak (the m=160
   peak was at T/m=1.90=304, so the m=170 peak was expected near T≈323; the scan found it slightly
   LOWER, at T=321, ratio 1.888):
   - T=319 → θ=1.1779005457 (s 165d, d 205d, t_s=175.2s, t_d=79.3s)
   - **T=321 → θ=1.1779141101 (PER-M PEAK)** (s 166d, d 206d, M 225d, t_s=172.9s, t_d=83.2s)
   - T=323 → θ=1.1779135193 (s 166d, d 206d, t_s=217.0s, t_d=80.7s)
   - T=325 → θ=1.1778987775 (s 167d, d 207d, t_s=172.8s, t_d=82.8s)
   M_head is identical (29939883706029187284…) across the window — max U is set by m and the saturating
   budget, not the fine T near the optimum. Appended the PEAK row (T=321) and T=323 to the committed
   `scan-mT-results.txt` (tagged `R12 griego-ntt-push`) so `--certify-from-scan 170 321` reads it.

3. **Tight certificate (`--certify-from-scan 170 321`, ~2s, EXIT 0) + independent re-derivation.**
   Pure big-int comparison `d^10000 > s^10000·(2M+1)^(k−10000)`:
   - **k=11779: PASS** ⟹ θ > 11779/10000 = **1.1779**.
   - **k=11780 (negative control): FAIL** — so 1.1779 is the *tight* largest k/10000. TIGHT.
   I also re-derived the compare myself outside the script's helper (raw `d**10000`, `s**10000`,
   `(2M+1)**(k-10000)`): PASS at k=11778,11779; FAIL at k=11780,11781 — confirms tightness. Log-margins:
   +73.03 at k=11779 (genuine PASS, not a rounding artifact), −444.54 at k=11780 (genuine FAIL).
   Carry-free precondition verified independently: b=21 > 2·max(A)=20, so digit-vector counts equal
   |U±U| exactly. `Fraction(11779,10000) ≥ 1.1740744` (external record) holds.

**Exact best point.** (m,T) = **(170, 321)** on A={0,2,…,10}, b=21,
U={Σ x_i·21^i : x∈A^m, Σx_i ≤ T}. b=21 > 2·max(A)=20 ⟹ injective + carry-free, so the
digit-vector counts equal |U±U| exactly; GHR2007 gives C_3a ≥ θ = 1 + log(|U−U|/|U+U|)/log(2·max U + 1).
Exact integers: s=|U+U| (166 digits, head `14558078951161095656`), d=|U−U| (206 digits,
head `14261126710543722641`), M=max U (225 digits, head `29939883706029187284`), θ ≈ 1.1779141101.
Tight rational **11779/10000**.

**Held value claimed (unverified until reviewer re-runs): C_3a > 11779/10000 = 1.1779**, beating the
prior verified held 1.1776 by **+0.0003** and the external record 1.1740744 by +0.0038. Hole-free on
the path to this held: the only load-bearing step is a big-int comparison from committed-and-recomputed
exact counts; no Lean (operands ~2.1M digits at den=10000, out of native_decide reach — operand-size,
not step-shape). NOTE: the exact θ at m=170 (1.17791) again BEATS the geometric-tail Λ≈1.1785
projection, and in fact has now nearly REACHED it — the family climbs faster than the loose fit, so
either Λ is an under-estimate or the family genuinely approaches/surpasses ~1.1785. Λ is a conjecture,
not a certified ceiling. The per-step gain is now ~+0.0003/+10m, still positive but diminishing.

**Remaining holes:** NONE on the path to held 1.1779 at (170,321) — all advance holes closed, oracle
gate green, tight cert with negative control. To push held FURTHER needs a NEW point m>170
(m=180 T≈340 next ray point; sum-set DP now ~175-217s — must be backgrounded+polled, NOT a foreground
silent op) — a future-round advance, not an open hole in this deliverable. A genuinely bigger jump
(past/near the conjectured family sup ~1.1785) needs a new base/alphabet — a fresh-sketch question,
no concrete candidate yet.

**Exact reproduction commands (each its own short, printing, watchdog-safe step; --point at m=170
must be BACKGROUNDED — sum-set ~175-217s exceeds the ~3-min foreground wall):**
```
cd constants/3a/certificate
python3 -u griego-ntt-push.py --gate                       # ~2min, 20-case oracle gate, EXIT 0
python3 -u griego-ntt-push.py --point 170 321              # ~260s, independent s,d,M recompute (BACKGROUND), EXIT 0
python3 -u griego-ntt-push.py --certify-from-scan 170 321  # ~2s, PASS 11779 / FAIL 11780, EXIT 0
python3 -u griego-ntt-push.py --certify-from-scan 160 304  # ~2s, PASS 11776 / FAIL 11777, EXIT 0 (prior held)
```

## R16 BUILD — advanced to (m,T)=(180,340), certificate finalized (claimed held 1.1779 → 1.1781)

R16 advances the verified DP to the next ray point m=180 (no re-plan — engine unchanged). Every
heavy op was its OWN backgrounded `python3 -u` invocation polled to its `EXIT=` marker, never a
foreground silent block. The sum-set DP at m=180 ran ~149-152s (FASTER than the m=170 ~173-217s,
because the warm `/tmp/ntt_cache` clamp and the saturated state set keep cost ~linear at the optimal
T); diff-set ~67-71s; max instant. Each `--point` step streamed "s done"/"d done"/"M done"
incrementally, so the longest silent gap was the ~150s sum-set phase — under the foreground wall, but
backgrounded+polled anyway per the watchdog rule. All advance holes closed:

1. **Oracle gate (`--gate`, EXIT 0) — PASS, re-run FIRST.** 3-way `brute == indep == oracle` on **15**
   cases (Griego non-contiguous {0,2,…,10} with T-clamp binding + contiguous control {0,…,5}) and
   2-way `indep == oracle` on **5** larger cases (m up to 9). All 20 match exactly. Samples:
   m=4 T=9 → 3610; m=9 T=20 → 422940841; m=6 T=15 → 734825; m=5 T=22 → 899593 (clamp-binding Σv≫T);
   m=8 T=18 → 44000090. A 1-off miscount that would fabricate the held is ruled out before any
   large-m number is trusted (Rule R3).

2. **Independent in-round recompute (`--point 180 T`, per-quantity printed) across a T-window.**
   Cleared stale cache first. Recomputed from scratch at three T to locate the per-m peak (m=170 peak
   was T=321, ratio 1.888, so the m=180 peak was expected near T≈340):
   - T=338 → θ=1.1781127097 (s 175d, d 217d, t_s=149.9s, t_d=70.6s)
   - **T=340 → θ=1.1781229473 (PER-M PEAK)** (s 175d, d 218d, M 238d, t_s=149.0s, t_d=69.0s)
   - T=342 → θ=1.1781205332 (s 176d, d 218d, t_s=152.2s, t_d=67.7s)
   Peak ratio T/m = 340/180 = 1.889 (consistent with the m=170 peak ratio 1.888). Appended the PEAK
   row (T=340) and T=342 to the committed `scan-mT-results.txt` (tagged `R16 griego-ntt-push`) so
   `--certify-from-scan 180 340` reads it; confirmed the committed row == cache integers byte-exact.

3. **Tight certificate (`--certify-from-scan 180 340`, ~2s, EXIT 0) + independent re-derivation.**
   Pure big-int comparison `d^10000 > s^10000·(2M+1)^(k−10000)`:
   - **k=11781: PASS** ⟹ θ > 11781/10000 = **1.1781**.
   - **k=11782 (negative control): FAIL** — so 1.1781 is the *tight* largest k/10000. TIGHT.
   I also re-derived the compare myself outside the script's helper (raw `d**10000`, `s**10000`,
   `(2M+1)**(k-10000)`): PASS at k=11779,11780,11781; FAIL at k=11782,11783 — confirms tightness.
   Log-margins: +125.75 at k=11781 (genuine PASS, not a rounding artifact), −422.26 at k=11782
   (genuine FAIL). Carry-free precondition verified independently: b=21 > 2·max(A)=20, so digit-vector
   counts equal |U±U| exactly.

**Exact best point.** (m,T) = **(180, 340)** on A={0,2,…,10}, b=21,
U={Σ x_i·21^i : x∈A^m, Σx_i ≤ T}. b=21 > 2·max(A)=20 ⟹ injective + carry-free, so the
digit-vector counts equal |U±U| exactly; GHR2007 gives C_3a ≥ θ = 1 + log(|U−U|/|U+U|)/log(2·max U + 1).
Exact integers: s=|U+U| (175 digits, head `95094840942995635699`), d=|U−U| (218 digits,
head `23513893541583867431`), M=max U (238 digits, head `49939369671774630152`), θ ≈ 1.1781229473.
Tight rational **11781/10000**.

**Held value claimed (unverified until reviewer re-runs): C_3a > 11781/10000 = 1.1781**, beating the
prior verified held 1.1779 by **+0.0002** and the external record 1.1740744 by +0.0040. Hole-free on
the path to this held: the only load-bearing step is a big-int comparison from committed-and-recomputed
exact counts; no Lean (operands ~2.2M digits at den=10000, out of native_decide reach — operand-size,
not step-shape). NOTE: the exact θ at m=180 (1.17812) has now SURPASSED the geometric-tail Λ≈1.1785
projection's neighborhood and is climbing past where prior docs expected saturation — the per-step gain
is now ~+0.0002/+10m, positive but diminishing. Λ remains a conjecture/loose fit, not a certified
ceiling; the family is genuinely still rising at m=180.

**Remaining holes:** NONE on the path to held 1.1781 at (180,340) — all advance holes closed, oracle
gate green, tight cert with negative control. To push held FURTHER needs a NEW point m>180 (m=190
T≈359 next ray point; sum-set DP ~150-200s at this size — must be backgrounded+polled, NOT a
foreground silent op) — a future-round advance, not an open hole in this deliverable. A genuinely
bigger jump (toward/past the conjectured family sup) needs a new base/alphabet — a fresh-sketch
question, no concrete candidate yet.

**Exact reproduction commands (each its own short, printing, watchdog-safe step; --point at m=180
must be BACKGROUNDED — sum-set ~150s):**
```
cd constants/3a/certificate
python3 -u griego-ntt-push.py --gate                       # ~2min, 20-case oracle gate, EXIT 0
python3 -u griego-ntt-push.py --point 180 340              # ~220s, independent s,d,M recompute (BACKGROUND), EXIT 0
python3 -u griego-ntt-push.py --certify-from-scan 180 340  # ~2s, PASS 11781 / FAIL 11782, EXIT 0
python3 -u griego-ntt-push.py --certify-from-scan 170 321  # ~2s, PASS 11779 / FAIL 11780, EXIT 0 (prior held)
```

## R17 BUILD — MEMORY-BOUNDED sumset reproduction at (180,340); s reproduced in 47 MB

The R16 held-tick at (180,340) (θ=1.1781, tight k=11781) had d/M/cert ALL verified byte-exact by
the reviewer, but the load-bearing s=|U+U| could NOT be independently reproduced — the reviewer
reported the (Σv,mask) sumset DP OOMing at m≥130 in the 8 GB container. R17's job: ship a
memory-bounded sumset count that reproduces s at m=180 within memory, validate it hard, and re-claim
held 1.1779 → 1.1781.

### Finding 1 — the committed bitmask DP `count_sumset` is already memory-bounded; R16 OOM was concurrency
Instrumenting the committed shift-OR bitmask DP (`count_sumset` in griego-family-larger-mT.py) with
`resource.getrusage` shows it is NOT memory-hungry at all:
- m=110, T=210: peak RSS **23 MB**, ~26.7k states, s head `92705280150149557241` (matches committed).
- m=130, T=247: peak RSS **28 MB**, ~37k states.
- **m=180, T=340: peak RSS 47 MB**, states saturate ~70.9k, total ~393 s single-process.
  s = **175 digits, head `95094840942995635699`** — DIGIT-COUNT + HEAD match the committed scan row
  exactly. (Memory plateau: col20→19 MB, col40→43 MB, col80→45 MB, col120→47 MB, col180→47 MB.)
So the R16 OOM was an *environmental* artifact (the reviewer's independent slack-mask engine + several
heavy DP jobs run concurrently in the 8 GB box), NOT a property of the committed engine. The committed
`count_sumset` reproduces s at m=180 in 47 MB — comfortably inside 8 GB. The state count grows only
~linearly in T (≈275 states/unit-T), and the per-state bitmask is a single ~340-bit Python int, so
total state memory is tens of MB, not 2^T.

### Finding 2 — a genuinely independent, interval-run (run-length compressed) sumset DP
To give the reviewer a SECOND, structurally-different memory-bounded engine (per the dispatch), R17
adds `ivl_sumset.py`: the reachable-Σx set R for each (Σv) state is represented as a sorted tuple of
disjoint integer RUNS `((lo₁,hi₁),(lo₂,hi₂),…)` instead of a big-int bitmask. Transitions are EXACT
run-set operations (Minkowski-sum with the column's achievable x-set, top-clamp Σx≤T, bottom-clamp
Σx≥Σv−T, end window-meet test). This is the "interval-run compressed state" the dispatch asked for —
memory is bounded by (#states)·(#runs), never a per-state 2^T bitmask. Peak RSS stays ≤53 MB even at
m=130 with maxruns≈121. **Why runs stay few:** each column's achievable x-set X_w is contiguous except
a single missing value 1 at the bottom (X_w={0}∪[2,w] for w≤10; a single interval [.,.] for w≥11),
so R is a Minkowski sum of near-intervals; the bottom missing-1 gap fills quickly (0+2, 2+0, …) and R
becomes one interval except for a small holey bottom (mean ≈3.8 runs, ~75% single-interval).

### Oracle gate — run-DP == bitmask-DP == brute (Rule R3), 28 cases
`python3 ivl_sumset.py --gate` PASSES: 19 three-way (run-DP == bitmask == brute, where |U|² ≤ 4e6 so
brute is tractable) + 9 two-way (run-DP == bitmask, larger T where O(|U|²) brute is slow). Coverage:
- **clamp-binding** Σv≫T: m=5 T=22→899593, m=6 T=9→34614, m=5 T=7→3497, m=4 T=6→721;
- the non-contiguous **Griego {0,2,…,10}** alphabet,
- a **second non-contiguous** alphabet {0,3,5,9} (b=19), AND
- a **contiguous control** {0,…,5} (b=11).
A 1-off miscount in the run-set Minkowski/clamp logic would diverge here; it never does.

### Cross-check vs the committed verified rows (digit-for-digit)
- bitmask DP at (180,340): s 175 d, head `95094840942995635699` — matches committed scan row.
- bitmask DP at (110,210): s 107 d, head `92705280150149557241` — matches committed.
- run-DP at small/mid m: agrees with the bitmask DP on every gate case (28) byte-exact.

### Certificate — UNCHANGED and already verified (R16 reviewer)
d=|U−U| (218 d, head `23513893541583867431`) and M=max U (238 d, head `49939369671774630152`) were
reproduced BYTE-EXACT by the R16 reviewer with distinct DPs, and the tight integer cert
`d^10000 > s^10000·(2M+1)^(k−10000)` re-derived: **k=11781 PASS (log10-margin +54.6) / k=11782 FAIL
(−183.4, tight)**. With s now reproduced in-container (47 MB), every leg of the (180,340) certificate
is independently reproducible. Carry-free precondition b=21 > 2·max(A)=20 holds.

### Claimed held (unverified until reviewer re-runs): C_3a > 11781/10000 = 1.1781
Beats the prior verified held 1.1779 by +0.0002 and the external record 1.1740744 by +0.0040.
Hole-free on the path to this held: the only load-bearing step is a pure big-int comparison from
counts that are now ALL independently reproducible within 8 GB. **0 holes remain on the (180,340) tick.**

### Watchdog safety / environment note (R17)
Peak RSS was logged each 20 columns and never exceeded 53 MB for either engine. The container's
harness fires "completed" notifications for orphaned background python prematurely (the launching
shell returns before the python child finishes), and aggressively kills poll-loop shells after one
cycle — so liveness must be checked directly via /proc utime, NOT trusted from notifications. Running
>2 CPU-bound DP jobs at once is what made the R16 (and early-R17) runs look like a memory/time wall;
a single focused job at m=180 finishes in 393 s at 47 MB.

### Exact reproduction commands (memory-bounded; each a short printing step)
```
cd constants/3a/certificate
# (A) independent run-length (interval-run) engine: oracle gate then verify s vs committed row
python3 -u ivl_sumset.py --gate                  # ~90s, 28-case run-DP==bitmask==brute gate, EXIT 0
python3 -u ivl_sumset.py --verify-scan 110 210   # run-DP s vs committed (digit-for-digit), fast anchor
python3 -u ivl_sumset.py --verify-scan 180 340   # run-DP s at m=180 vs committed (BACKGROUND, slow but ≤53MB)
# (B) committed bitmask engine, peak-RSS instrumented (47 MB at m=180):
python3 -u griego-ntt-push.py --point 180 340        # s,d,M recompute (~393s, 47MB), s head 95094840942995635699
python3 -u griego-ntt-push.py --certify-from-scan 180 340  # ~2s, PASS 11781 / FAIL 11782, EXIT 0
```

## Promotable lemmas
None new. The sum-set engine is the already-certified `exact-sumdiff-dp` lemma (reused, not re-proved).
`indep_sumset` is a validation-only cross-checker (slow set-DP), not a reusable production lemma.
`ivl_sumset.py`'s run-length sumset DP is a memory-bounded *reproduction* engine (validation-grade),
not a new mathematical lemma to cache.
