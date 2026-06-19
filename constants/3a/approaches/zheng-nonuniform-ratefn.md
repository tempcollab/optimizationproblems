# zheng-nonuniform-ratefn — generalize Zheng's rate function to non-uniform digits (THEORY/CEILING/STEER)

**Direction:** lower bound on C_3a. **Value to beat (verified held, R3):** 1.1752717416788478.
**This round (R4) = a CEILING + STEER, not a bound** (the outline-reviewer explicitly scoped it
so; a bound only at H3, which is the leader's lane). **Borrows:** the finite exact-DP engine
(`ghr_dp.py` / `alphabet-search-dp.py`) for the realization step (H3).

## Strategy
Zheng's Cramer large-deviation asymptotic assumes the **uniform** alphabet `{0..B}`, so his
closed-form theta does **not** cover Griego's non-uniform / gapped set (`{0..10}\{1}`). Nobody
had written the limiting theta for a **general finite alphabet**. Deriving it (a) gives the
asymptotic **ceiling** of the GHR single-set carry-free family and (b) identifies the **argmax**
(which alphabet / which base attains it) — a principled answer to "is base 21 / max-digit 10
optimal?" that no finite brute scan can give.

## What was closed this round (R4)

**H1 RATE FUNCTION — CLOSED and VALIDATED.**
Derived the generalized **2-D joint-cap large-deviation rate function** as an
entropy-projection (Sanov) form. For digits drawn uniformly from a finite alphabet `A` with
global sum cap `T = c·d` and carry-free base `b = 2·max(A)+1`:
```
(1/d) log|U+U| -> R_+(A,c) = max_{nu on AxA, E[a]<=c, E[a']<=c} H( pushforward_{a+a'} nu )
(1/d) log|U-U| -> R_-(A,c) = max_{nu on AxA, E[a]<=c, E[a']<=c} H( pushforward_{a-a'} nu )
(1/d) log q    -> log b
theta_inf(A,c) = 1 + (R_-(A,c) - R_+(A,c)) / log b
```
R_+/R_- are genuine **2-D** rates: the two caps couple through the joint coupling `nu` on `A×A`,
NOT a 1-D Legendre transform of `p∗p` (the gap Zheng's uniform formula leaves open). Each R is a
**convex program** (max entropy of a linear image under linear constraints), solved exactly by
cvxpy/SCS in ~0.02 s.

Validated TWO independent ways:
- **The required uniform gate PASSED EXACTLY:** uniform `p` on `{0..5}` reproduces Zheng's
  `theta-1 = 0.1730773` to 7 digits. The **entire Zheng B-table {3..10}** is reproduced to
  ~1e-7 (B=3→0.1687000, 4→0.1721379, 5→0.1730773, 6→0.1728555, 7→0.1720601, 8→0.1709753,
  10→0.1684650). This confirms the entropy-projection rate = Zheng's elaborate k-split closed
  form, term-for-term.
- **Finite-d consistency with the leader:** the leader's exact finite theta (d=84,88,96 =
  1.174475, 1.174764, 1.175272) sit monotonically BELOW the predicted ceiling 1.18258 with the
  gap shrinking (0.00810 → 0.00782 → 0.00731) — the finite DP is climbing toward exactly this
  asymptote.

**H2 OPTIMIZE — CLOSED (numerical argmax).**
Swept gapped alphabets `A ⊆ {0..M}` (0 and M always in, base = 2M+1) over `M ∈ {8..11}` and all
single/double interior omissions, optimizing `c`. Result:
```
M= 8 base=17: 1.1807955  A={0,2..8}
M= 9 base=19: 1.1820923  A={0,2..9}
M=10 base=21: 1.1825801  A={0,2..10}   <-- PEAK
M=11 base=23: 1.1825358  A={0,2..11}
```
At M=10, omit-{1} beats every other single/double omission (next best omit-{1,2}=1.1766). So:
- **ARGMAX = A={0,2,3,4,5,6,7,8,9,10}, base 21, c* ≈ 1.871** — EXACTLY Griego's/the leader's set.
- **PREDICTED CEILING theta_inf ≈ 1.18258** (CONJECTURE — a numerical-search asymptotic).
This directly answers Zheng's open levers #1 (a continuous B is NOT needed; integer M=10 is the
discrete peak) and #3 (the uniform box is NOT optimal; omitting digit 1 is, uniquely).

## Holes remaining
- **H3 REALIZE + CERTIFY — OPEN (clean hole, by design).** The asymptote 1.18258 is a CEILING,
  not a finite certifiable value. Its finite realization at the argmax config *is* the leader
  sketch `alphabet-search-dp` (same A, base, c), pushed to larger d. `realize_finite` raises a
  clear NotImplementedError that refers to the leader rather than stubbing a redundant DP here.
  **Blocker:** closing it = pushing `alphabet-search-dp` to d ~ 200+ (the gap +0.0073 closes at
  ~6.3e-5 per d-unit), which is the leader's lane, not a new computation in this file.

## Claimed value (CONJECTURE, NOT a bound)
Asymptotic ceiling **1.18258** for the GHR single-set carry-free family (argmax {0,2..10}/base 21).
This is a numerical-search asymptotic — it is NOT a verified bound and must NOT enter
`current.md` held. The verified held remains 1.1752717416788478 (alphabet-search-dp).

## STEER for next round (the actionable deliverable)
1. **The current alphabet/base is the asymptotic optimum.** Do not search other bases/alphabets
   for this family — `maxdigit-base-sweep`'s central question is answered: M=10/base-21/omit-{1}
   is the peak. (If the parallel `maxdigit-base-sweep` finite scan disagrees at moderate d, the
   asymptotic argmax here is the principled tie-breaker.)
2. **Remaining family headroom = +0.0073 above held, extracted ONLY by pushing d (Lever A).**
   The rate function confirms the d-push has not saturated and the ceiling is ~1.18258.
3. **A larger lift needs LEAVING this single-set/carry-free family** (ceiling 1.18258 ≪ GHR
   family hard cap 1.25). The principled next lever is Zheng's open #2: a *tighter d(U)* count
   than the crude carry-free encoding (the diffset rate R_- here already uses the full joint
   coupling, but the encoding-to-base step itself is lossy). That is a NEW STRATEGY for the
   OUTLINER, not a hole to fill in this sketch.

## Promotable lemmas
None this round. The rate-function module (`_rate`, `sumset_rate`, `diffset_rate`,
`theta_inf_at`) is validated and reusable, but it is a *guide* (asymptotic, cvxpy-based,
floating-point) — not a `sorry`-free axiom-clean bound primitive, so it does not meet the
`lemmas/` admission bar. Keep it in the sketch as the steer engine.

## Certify
The asymptotic guides; a BOUND would be certified by the finite integer DP (H3) — that path is
`alphabet-search-dp`. Not Lean-fit (continuous convex optimization).
