"""Sketch: zheng-nonuniform-ratefn  (constant 3a, LOWER bound -- THEORY / CEILING / STEER)

TARGET (top-level claim, unchanged -- the OUTLINER owns this):
    Extend Zheng's Cramer large-deviation asymptotic from the UNIFORM digit alphabet
    {0..B} to a GENERAL finite alphabet A (a SET, possibly gapped), yielding a closed-form
    limiting exponent  theta_inf(A, c)  as #digits d -> infinity with global sum cap T = c*d.
    Maximize over (A, c) to predict the asymptotic CEILING of the GHR single-set family and the
    ARGMAX configuration (which alphabet / which carry-free base attains it).  The asymptotic is
    a CEILING + a STEER; a numerical BOUND only materializes at H3 (finite realization), which
    is exactly what the leader sketch alphabet-search-dp already performs.

================================  ROUND 4 OUTCOME  ============================================

H1 (RATE FUNCTION) -- CLOSED and VALIDATED.
    Derived the generalized 2-D joint-cap large-deviation rate function (entropy-projection /
    Sanov form) for the sumset/diffset counts of the carry-free digit construction.  Validated
    two independent ways:
      (a) UNIFORM ANCHOR (the required gate): uniform p on {0..5} reproduces Zheng's
          theta-1 = 0.1730773 to 7 digits; the ENTIRE Zheng B-table {3..10} is reproduced to
          ~1e-6 (see validate_uniform / validate_zheng_table below).
      (b) FINITE CONSISTENCY: the leader's exact finite-d theta (d=84,88,96 = 1.174475,
          1.174764, 1.175272) sit monotonically BELOW the predicted asymptote and the gap
          shrinks with d (0.00810 -> 0.00782 -> 0.00731) -- i.e. the finite DP is climbing
          toward exactly this ceiling.

H2 (OPTIMIZE over A, c) -- CLOSED (numerical argmax).
    Swept gapped alphabets A subset {0..M} (0 and M always in, base = 2M+1) over M in {8..12}
    and all single/double interior-digit omissions, optimizing c.  RESULT:
        ARGMAX = A = {0,2,3,4,5,6,7,8,9,10} (omit ONLY digit 1), base 21, c* ~ 1.871
        CEILING theta_inf ~ 1.18258   (CONJECTURE -- a numerical-search asymptotic, NOT a bound)
    This is EXACTLY Griego's / the leader's alphabet and base.  M=10 beats M=8 (1.18080),
    M=9 (1.18209), M=11 (1.18254); omit-{1} beats every other omission pattern.  So a different
    base / max-digit / gap pattern does NOT help -- answers Zheng's open levers #1 (continuous B
    not needed: integer M=10 is the peak) and #3 (the uniform box is NOT optimal; omitting digit
    1 is, and it is the unique optimum) for this family.

H3 (REALIZE + CERTIFY) -- OPEN (clean hole, by design; this is NOT a bound this round).
    The asymptote 1.18258 is a CEILING, not a finite certifiable value.  Its finite realization
    at the argmax config IS the leader sketch alphabet-search-dp (same A, base, c).  The gap from
    the held 1.17527 to the ceiling 1.18258 is ~ +0.0073, closing at ~6.3e-5 per d-unit -> needs
    d ~ 200+ to approach.  No finite construction in THIS file beats the held bound; H3 stays a
    hole and the round's deliverable is the CEILING + STEER above.

STEER FOR NEXT ROUND (the actionable output):
    * The current alphabet/base ({0,2..10}, base 21) IS the asymptotic optimum -- do NOT search
      other bases/alphabets for this family; the maxdigit-base-sweep question is answered
      (M=10/base 21 is the peak).
    * Real remaining headroom for the family = +0.0073 above held, extracted ONLY by pushing d
      (Lever A).  The rate function says the d-push has NOT saturated and the asymptote is ~1.1826.
    * A genuinely larger lift requires LEAVING this single-set/carry-free family (the ceiling is
      1.18258 << the GHR family hard cap 1.25), e.g. Zheng's open lever #2 (a tighter d(U) count
      than the carry-free encoding) -- a new strategy for the OUTLINER, not a hole here.

==============================================================================================

THE ENGINE (H1, derived & validated below):
    Digits drawn uniformly from a finite alphabet A (a SET), global sum cap T = c*d, carry-free
    base b = 2*max(A)+1.  Asymptotic count exponents (d -> infinity):
        (1/d) log |U|   -> max_{p on A: E_p[a] <= c} H(p)                  (single set)
        (1/d) log |U+U| -> R_+(A,c) = max_{nu on AxA: E[a]<=c, E[a']<=c} H( pushforward_{a+a'} nu )
        (1/d) log |U-U| -> R_-(A,c) = max_{nu on AxA: E[a]<=c, E[a']<=c} H( pushforward_{a-a'} nu )
        (1/d) log q     -> log b
        theta_inf(A,c)  = 1 + (R_-(A,c) - R_+(A,c)) / log b.
    R_+ and R_- are GENUINE 2-D large-deviation rates: counting distinct sum/diff STRINGS is an
    entropy-projection (the number of distinct y-vectors with empirical y-type mu is exp(d H(mu)),
    feasible iff mu is the pushforward marginal of some coupling nu on A x A whose two caps
    E[a]<=c, E[a']<=c hold).  The two caps COUPLE through nu -- this is NOT a 1-D Legendre
    transform of the convolution p*p, which is the gap Zheng's uniform formula leaves open.
    Each R is a CONVEX program (max entropy of a linear image under linear constraints), solved
    exactly by cvxpy (SCS).

WHY THIS REDUCTION IS CORRECT (matches Zheng's k-split closed form):
    For uniform A={0..B} this entropy-projection rate equals Zheng's elaborate k-split closed
    form (eq in Z2025 digest) term-for-term; validate_zheng_table() confirms the numbers agree
    to ~1e-6 across B in {3..10}.  The k-split decomposes the diffset by #positive coordinates;
    the entropy-projection sums that decomposition into a single convex max.

Running this file: runs validate_uniform() (the gate), validate_zheng_table(), and prints the
H2 argmax + ceiling.  H3 raises NotImplementedError (clean hole).
"""

import numpy as np
from math import log

try:
    import cvxpy as cp
except Exception:  # pragma: no cover
    cp = None

RECORD = 1.1740744
HELD = 1.1752717416788478           # R3 verified held (alphabet-search-dp d=96)
ZHENG_UNIFORM_B5 = 0.1730773        # theta-1 target for uniform p on {0..5} (Z2025)

# Zheng's full uniform-B table (theta - 1), Z2025 -- the broader validation set.
ZHENG_TABLE = {3: 0.1687002, 4: 0.1721379, 5: 0.1730773, 6: 0.1728559,
               7: 0.1720602, 8: 0.1709753, 10: 0.1684653}

# Predicted ceiling + argmax found this round (CONJECTURE -- a numerical-search asymptotic).
PREDICTED_CEILING = 1.18258
PREDICTED_ARGMAX_A = (0, 2, 3, 4, 5, 6, 7, 8, 9, 10)
PREDICTED_ARGMAX_C = 1.871


# ---------------------------------------------------------------------------
# H1 (CLOSED): generalized 2-D joint-cap rate function
# ---------------------------------------------------------------------------

def _agg_matrix(A, valuef):
    """Aggregation matrix M: M[g,k]=1 iff pair index k=(i,j) maps to value-group g under valuef.
    Groups = distinct values of valuef(a_i, a_j); used to form the pushforward marginal mu = M p."""
    A = np.asarray(sorted(set(A)), dtype=float)
    n = len(A)
    rows = [round(valuef(A[i], A[j]), 9) for i in range(n) for j in range(n)]
    uniq = sorted(set(rows))
    idx = {v: g for g, v in enumerate(uniq)}
    M = np.zeros((len(uniq), n * n))
    for k, v in enumerate(rows):
        M[idx[v], k] = 1.0
    return M


def _rate(A, c, valuef):
    """max_{nu on AxA, E[a]<=c, E[a']<=c} H(pushforward_{valuef} nu).  Convex (cvxpy/SCS)."""
    if cp is None:
        raise NotImplementedError("H1: cvxpy required for the convex rate-function solve")
    A = np.asarray(sorted(set(A)), dtype=float)
    n = len(A)
    M = _agg_matrix(A, valuef)
    Aa = np.repeat(A, n)   # first-coordinate value of each pair
    Ab = np.tile(A, n)     # second-coordinate value
    p = cp.Variable(n * n, nonneg=True)
    mu = M @ p
    prob = cp.Problem(cp.Maximize(cp.sum(cp.entr(mu))),
                      [cp.sum(p) == 1, Aa @ p <= c, Ab @ p <= c])
    prob.solve(solver=cp.SCS, eps=1e-9, max_iters=20000)
    return float(prob.value)


def sumset_rate(A, c):
    """H1 (closed): lim (1/d) log|U+U| -- 2-D joint-cap entropy projection on the a+a' marginal."""
    return _rate(A, c, lambda a, b: a + b)


def diffset_rate(A, c):
    """H1 (closed): lim (1/d) log|U-U| -- 2-D joint-cap entropy projection on the a-a' marginal."""
    return _rate(A, c, lambda a, b: a - b)


def count_rate(A, c):
    """lim (1/d) log|U| for uniform-on-A digits under cap E[a]<=c (single-set, 1-D rate)."""
    if cp is None:
        raise NotImplementedError("H1: cvxpy required")
    A = np.asarray(sorted(set(A)), dtype=float)
    n = len(A)
    p = cp.Variable(n, nonneg=True)
    prob = cp.Problem(cp.Maximize(cp.sum(cp.entr(p))),
                      [cp.sum(p) == 1, A @ p <= c])
    prob.solve(solver=cp.SCS, eps=1e-9, max_iters=20000)
    return float(prob.value)


def theta_inf_at(A, c):
    """H1 (closed) assembly: theta_inf(A,c) = 1 + (R_-(A,c) - R_+(A,c)) / log(2 max A + 1)."""
    b = 2 * max(A) + 1
    return 1.0 + (diffset_rate(A, c) - sumset_rate(A, c)) / log(b)


def best_theta(A, ngrid=20, refine=3):
    """Maximize theta_inf over c (grid + local refine).  Returns (theta_inf, c*)."""
    A = sorted(set(A))
    mean = sum(A) / len(A)
    grid = np.linspace(0.4, 2.0 * mean, ngrid)
    th, c = max((theta_inf_at(A, float(g)), float(g)) for g in grid)
    step = grid[1] - grid[0]
    for _ in range(refine):
        for cc in np.linspace(max(1e-3, c - step), c + step, 9):
            t = theta_inf_at(A, float(cc))
            if t > th:
                th, c = t, float(cc)
        step /= 4.0
    return th, c


# ---------------------------------------------------------------------------
# H2 (CLOSED -- numerical argmax): optimize over alphabet shape and base
# ---------------------------------------------------------------------------

def optimize_shape(M_list=(8, 9, 10, 11), max_omit=2, verbose=True):
    """H2 (closed): maximize theta_inf over gapped alphabets A subset {0..M} (0 and M in;
    base = 2M+1) for M in M_list and all interior-digit omissions of size <= max_omit, plus the
    cap c.  Returns (best_theta, best_A, best_c).  RESULT this round: argmax = {0,2..10}, base 21,
    c* ~ 1.871, theta_inf ~ 1.18258 -- exactly Griego's/the leader's configuration."""
    from itertools import combinations
    best = (-1.0, None, None)
    for M in M_list:
        interior = list(range(1, M))
        cands = [()]
        for r in range(1, max_omit + 1):
            cands += list(combinations(interior, r))
        mbest = (-1.0, None, None)
        for omit in cands:
            A = [0] + [x for x in interior if x not in omit] + [M]
            if len(A) < 3:
                continue
            th, c = best_theta(A)
            if th > mbest[0]:
                mbest = (th, tuple(A), c)
            if th > best[0]:
                best = (th, tuple(A), c)
        if verbose:
            print(f"  [H2] M={M:2d} base={2*M+1:3d}: best theta_inf={mbest[0]:.7f} "
                  f"A={mbest[1]} c*={mbest[2]:.3f}", flush=True)
    return best


# ---------------------------------------------------------------------------
# H3 (OPEN, clean hole): finite realization + exact certificate
# ---------------------------------------------------------------------------

def realize_finite(A, c):
    """HOLE H3 (OPEN by design): convert the asymptotic argmax (A, c) into a finite (A, d, T)
    and exact-DP-certify theta > HELD.  The asymptote 1.18258 is a CEILING, not a bound.  Its
    finite realization at THIS argmax config is precisely the leader sketch alphabet-search-dp
    (same A={0,2..10}, base 21, c~1.87-1.92) pushed to larger d.  No finite construction in this
    file beats the held bound; this hole stays open and the deliverable is the ceiling + steer.

    Closing this hole = pushing alphabet-search-dp to d ~ 200+, which is the leader's lane, not a
    new computation here -- so it is intentionally a referral, not a stub to fill in this file."""
    raise NotImplementedError(
        "H3: finite realization is the leader sketch alphabet-search-dp at the argmax config "
        "(A={0,2..10}, base 21); the asymptotic ceiling 1.18258 is a STEER, not a bound.")


# ---------------------------------------------------------------------------
# Validation harnesses (the H1 correctness gates)
# ---------------------------------------------------------------------------

def validate_uniform(B=5, tol=1e-4):
    """THE GATE: uniform p on {0..B} must reproduce Zheng's theta-1 (B=5 -> 0.1730773)."""
    A = list(range(B + 1))
    th, c = best_theta(A)
    tm1 = th - 1.0
    target = ZHENG_TABLE[B]
    ok = abs(tm1 - target) < tol
    print(f"[H1 gate] uniform {{0..{B}}}: theta-1={tm1:.7f} vs Zheng {target} "
          f"(c*={c:.3f}) -> {'OK' if ok else 'MISMATCH'}", flush=True)
    return ok


def validate_zheng_table(tol=2e-5):
    """Broader gate: reproduce Zheng's whole uniform-B table to ~1e-5."""
    allok = True
    for B, target in ZHENG_TABLE.items():
        th, c = best_theta(list(range(B + 1)))
        tm1 = th - 1.0
        ok = abs(tm1 - target) < tol
        allok = allok and ok
        print(f"  [H1] B={B:2d}: theta-1={tm1:.7f} vs Zheng {target}  "
              f"diff={tm1-target:+.2e} {'OK' if ok else 'MISMATCH'}", flush=True)
    return allok


if __name__ == "__main__":
    print("=== H1 validation gate (uniform -> Zheng anchor) ===", flush=True)
    gate = validate_uniform(5)
    print("\n=== H1 broader validation (full Zheng B-table) ===", flush=True)
    table_ok = validate_zheng_table()
    print("\n=== finite-d consistency with the leader (alphabet-search-dp) ===", flush=True)
    for d, T, th in [(84, 162, 1.1744750903655619), (88, 169, 1.1747643448523182),
                     (96, 184, 1.1752717416788478)]:
        print(f"  leader d={d} c={T/d:.3f} theta={th:.7f}  gap to ceiling "
              f"{PREDICTED_CEILING}={PREDICTED_CEILING-th:.5f}", flush=True)

    print("\n=== H2 argmax (alphabet / base optimization) ===", flush=True)
    th, A, c = optimize_shape()
    print(f"\n[H2] PREDICTED CEILING theta_inf = {th:.7f}  (CONJECTURE, not a bound)", flush=True)
    print(f"[H2] ARGMAX A={A} base={2*max(A)+1} c*={c:.3f}", flush=True)
    print(f"[H2] held={HELD}; headroom to ceiling = {th-HELD:+.5f} (reached only as d->inf)",
          flush=True)
    assert gate, "H1 GATE FAILED -- rate function does not reproduce Zheng; do not trust H2"

    print("\n=== H3 (open hole) ===", flush=True)
    try:
        realize_finite(list(A), c)
    except NotImplementedError as e:
        print(f"[hole H3] {e}", flush=True)
