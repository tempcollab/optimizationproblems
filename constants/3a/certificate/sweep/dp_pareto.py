"""
PRODUCTION carry-free DP: Pareto-frontier reachability of (sum_a, sum_b).

Exact count of distinct output vectors (sumset or diffset elements) that admit a feasible
split (both partial sums <= T).  State = Pareto-MINIMAL frontier of reachable (sum_a, sum_b)
within [0,T]^2; value = #distinct output prefixes giving that frontier.  Merging by Pareto-min
frontier is EXACT for the final "exists a point <= (T,T)" feasibility (two prefixes with the
same frontier are interchangeable for all future feasibility).  The state count PLATEAUS in d,
so this scales to the record d=80, T=150.

Validated against brute force / dp_fast / dp_pack on carry-free cases.
"""
from collections import defaultdict


def _pareto(points, T):
    pts = sorted(set(p for p in points if p[0] <= T and p[1] <= T))
    keep = []
    by = None
    for x, y in pts:
        if by is None or y < by:
            keep.append((x, y))
            by = y
    return tuple(keep)


def _count(A, T, d, pairs):
    states = {((0, 0),): 1}
    for _ in range(d):
        ns = defaultdict(int)
        for R, cnt in states.items():
            for o, opts in pairs.items():
                pts = []
                for (s1, s2) in R:
                    for (da, db) in opts:
                        a, b = s1 + da, s2 + db
                        if a <= T and b <= T:
                            pts.append((a, b))
                if not pts:
                    continue
                ns[_pareto(pts, T)] += cnt
        states = dict(ns)
    # every surviving state has a nonempty frontier => feasible; count all
    return sum(states.values())


def count_sumset(A, B, d, T):
    assert B > 2 * max(A)
    Aset = set(A)
    ApA = sorted({x + y for x in A for y in A})
    pairs = {c: [(a, c - a) for a in A if (c - a) in Aset] for c in ApA}
    return _count(A, T, d, pairs)


def count_diffset(A, B, d, T):
    assert B > 2 * max(A)
    Aset = set(A)
    AmA = sorted({x - y for x in A for y in A})
    pairs = {e: [(a, a - e) for a in A if (a - e) in Aset] for e in AmA}
    return _count(A, T, d, pairs)


def maxU(A, B, d, T):
    M = 0
    rem = T
    for i in range(d - 1, -1, -1):
        valid = max((x for x in A if x <= rem), default=0)
        M += valid * (B ** i)
        rem -= valid
        if rem <= 0:
            break
    return M
