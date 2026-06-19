"""
Self-contained EXACT digit-DP engine for the GHR sum-difference lower bound on C_3a.

C_3a >= 1 + log(|U-U|/|U+U|) / log(2*max(U)+1)   (GHR2007), U finite subset of Z>=0, 0 in U.

Construction (digit set):
   U = { sum_i a_i * B^i : a_i in A, i < d, sum_i a_i <= T }, with 0 in A so 0 in U.

CARRY-FREE regime: if B > 2*max(A) then for u,v in U the digit vectors of u+v and u-v have
no carries/borrows, so each sum/difference element is identified by its per-position digit
vector.  The ONLY coupling between positions is the global digit-sum cap T.

This module computes |U+U|, |U-U|, max(U) as EXACT integers (Python int / no float in the
load-bearing count), and the GHR bound exactly via a rational-power comparison (no float).

Independent re-derivation (does NOT use the sibling engine/ dir).
"""
from fractions import Fraction
from functools import lru_cache


def maxU(A, B, d, T):
    """Exact max element of U: greedily fill highest positions with max(A) subject to sum<=T."""
    a = max(A)
    M = 0
    rem = T
    # put digits at the highest positions (largest B^i) to maximize value
    for i in range(d - 1, -1, -1):
        use = min(a, rem)
        # use must be a valid digit in A; pick the largest digit in A that is <= rem
        valid = max((x for x in A if x <= rem), default=0)
        M += valid * (B ** i)
        rem -= valid
        if rem <= 0:
            break
    return M


# ---------------------------------------------------------------------------
# Pareto-set helpers (2D, minimization; a point dominates another if it is <= in
# both coords).  We only ever need: does the reachable set contain a point with
# both coords <= T?  So we keep Pareto-MINIMAL points within the box [0,T]^2.
# ---------------------------------------------------------------------------

def pareto_reduce(points, T):
    """Keep only Pareto-minimal points (no other point is <= in BOTH coords),
    dropping any point outside the box [0,T]^2.  Returns a frozenset."""
    pts = [p for p in points if p[0] <= T and p[1] <= T]
    pts = sorted(set(pts))
    keep = []
    # sort by x asc, then for minimal y frontier
    best_y = None
    for x, y in pts:
        if best_y is None or y < best_y:
            keep.append((x, y))
            best_y = y
    # the above keeps, for increasing x, strictly decreasing y -> Pareto-minimal
    return frozenset(keep)


def count_sumset(A, B, d, T):
    """
    EXACT |U+U| in the carry-free regime (B > 2*max(A)).
    Output element identified by digit vector c_i in A+A.
    c is achievable iff EXISTS split a_i in A, b_i = c_i - a_i in A, sum a <= T, sum b <= T.
    DP over positions: state = Pareto-minimal reachable set R of (sum_a, sum_b) within [0,T]^2,
    value = number of distinct c-prefixes yielding exactly that reachable set.
    Count distinct full c with nonempty R.
    """
    Aset = set(A)
    ApA = sorted({x + y for x in A for y in A})
    # for each output digit value c, the increment options (da, db) with da,db in A, da+db=c
    incr = {}
    for c in ApA:
        opts = [(a, c - a) for a in A if (c - a) in Aset]
        incr[c] = opts

    # initial state: one prefix (empty), reachable {(0,0)}
    states = {frozenset({(0, 0)}): 1}
    for _ in range(d):
        new_states = {}
        for R, cnt in states.items():
            for c in ApA:
                pts = []
                for (s1, s2) in R:
                    for (da, db) in incr[c]:
                        ns1, ns2 = s1 + da, s2 + db
                        if ns1 <= T and ns2 <= T:
                            pts.append((ns1, ns2))
                if not pts:
                    continue  # this output digit infeasible from this state
                R2 = pareto_reduce(pts, T)
                if not R2:
                    continue
                new_states[R2] = new_states.get(R2, 0) + cnt
        states = new_states
    return sum(states.values())


def count_diffset(A, B, d, T):
    """
    EXACT |U-U| in the carry-free regime.
    u - v has per-position digit (a_i - b_i) over A-A; carry-free since B > 2*max(A)
    (the borrow magnitude per position is at most max(A) < B).  Difference element
    identified by digit vector e_i in A-A.
    e achievable iff EXISTS a_i in A, b_i in A with a_i - b_i = e_i, sum a <= T, sum b <= T.
    Same DP shape; increments (da, db) = (a, b) with a-b = e.
    """
    Aset = set(A)
    AmA = sorted({x - y for x in A for y in A})
    incr = {}
    for e in AmA:
        opts = [(a, a - e) for a in A if (a - e) in Aset]
        incr[e] = opts

    states = {frozenset({(0, 0)}): 1}
    for _ in range(d):
        new_states = {}
        for R, cnt in states.items():
            for e in AmA:
                pts = []
                for (s1, s2) in R:
                    for (da, db) in incr[e]:
                        ns1, ns2 = s1 + da, s2 + db
                        if ns1 <= T and ns2 <= T:
                            pts.append((ns1, ns2))
                if not pts:
                    continue
                R2 = pareto_reduce(pts, T)
                if not R2:
                    continue
                new_states[R2] = new_states.get(R2, 0) + cnt
        states = new_states
    return sum(states.values())


# ---------------------------------------------------------------------------
# Exact GHR bound value and exact comparison to a target.
# ---------------------------------------------------------------------------

def ghr_value_float(Nminus, Nplus, M):
    """Float value of the GHR bound (for reporting/sorting ONLY, never load-bearing)."""
    import math
    return 1.0 + math.log(Nminus / Nplus) / math.log(2 * M + 1)


def ghr_beats(Nminus, Nplus, M, c):
    """
    EXACT (integer-only) test of  1 + log(Nminus/Nplus)/log(2M+1) > c  (c a Fraction).
    Equivalent to log(Nminus/Nplus) > (c-1)*log(2M+1)
             <=> (Nminus/Nplus) > (2M+1)^(c-1)
             <=> Nminus^q > Nplus^q * (2M+1)^p   where c-1 = p/q, p,q in N, q>0.
    Returns True iff strictly greater.  Pure big-int comparison, NO float.
    """
    cm1 = Fraction(c) - 1
    p = cm1.numerator
    q = cm1.denominator
    base = 2 * M + 1
    if p < 0:
        # (2M+1)^(p/q) with p<0: Nminus/Nplus > (2M+1)^(p/q) <=>
        # Nminus^q * (2M+1)^(-p) > Nplus^q
        return (Nminus ** q) * (base ** (-p)) > (Nplus ** q)
    return (Nminus ** q) > (Nplus ** q) * (base ** p)


def ghr_geq(Nminus, Nplus, M, c):
    """EXACT >= test (same rationalization)."""
    cm1 = Fraction(c) - 1
    p = cm1.numerator
    q = cm1.denominator
    base = 2 * M + 1
    if p < 0:
        return (Nminus ** q) * (base ** (-p)) >= (Nplus ** q)
    return (Nminus ** q) >= (Nplus ** q) * (base ** p)


if __name__ == "__main__":
    # quick smoke
    A = [0, 2, 3, 4, 5]
    print("smoke maxU:", maxU(A, 7, 3, 8))
