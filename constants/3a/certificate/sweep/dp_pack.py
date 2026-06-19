"""
Carry-free DP using a 2D reachability bitmask (sum_a, sum_b) packed in one big int, with a
GUTTER so column (sum_b) overflow spills into discardable bits.  Removes the unbounded `se`
dimension that blew up dp_fast's difference DP at large T.

Packing: bit (s_a, s_b) at index s_a*W + s_b, where W = T+1+G, G = max(A) (gutter width >=
max column shift).  Valid region: s_a in [0,T], s_b in [0,T].
Transition for an output digit with valid (da,db) increments: new_mask = OR_d (mask << (da*W+db)),
then AND with KEEP = (bits with s_a in [0,T]) AND (bits with s_b in [0,T] i.e. not in gutter).

DP state = packed mask; value = #distinct output prefixes giving that reachable set.
End feasibility (both sumset and diffset): mask != 0  (every retained bit has s_a,s_b <= T,
which is exactly "exists split with both partial sums <= T").

Validated against brute force / dp_fast on carry-free cases.
"""
from collections import defaultdict


def _build_keep(T, G):
    W = T + 1 + G
    rows = T + 1
    # column mask for one row: bits 0..T set, gutter bits T+1..W-1 clear
    row_ok = (1 << (T + 1)) - 1
    keep = 0
    for r in range(rows):
        keep |= row_ok << (r * W)
    return W, keep


def _count(A, B, d, T, pairs_for):
    """Generic carry-free count. pairs_for(o) -> list of (da,db) increments for output digit o,
    iterating o over the output alphabet."""
    G = max(A)
    W, KEEP = _build_keep(T, G)
    out_alphabet = sorted(pairs_for.keys())
    states = {1: 1}  # bit (0,0) set => index 0
    for _ in range(d):
        ns = defaultdict(int)
        for mask, cnt in states.items():
            for o in out_alphabet:
                nm = 0
                for (da, db) in pairs_for[o]:
                    nm |= mask << (da * W + db)
                nm &= KEEP
                if nm:
                    ns[nm] += cnt
        states = dict(ns)
    return sum(states.values())


def count_sumset(A, B, d, T):
    assert B > 2 * max(A)
    Aset = set(A)
    ApA = sorted({x + y for x in A for y in A})
    pairs = {c: [(a, c - a) for a in A if (c - a) in Aset] for c in ApA}
    return _count(A, B, d, T, pairs)


def count_diffset(A, B, d, T):
    assert B > 2 * max(A)
    Aset = set(A)
    AmA = sorted({x - y for x in A for y in A})
    # element digit e = a - b; increments to (sum_a, sum_b) are (a, b) with a-b=e
    pairs = {e: [(a, a - e) for a in A if (a - e) in Aset] for e in AmA}
    return _count(A, B, d, T, pairs)


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
