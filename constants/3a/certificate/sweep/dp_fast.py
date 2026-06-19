"""
FAST exact carry-free digit-DP for |U+U|, |U-U|, max(U).
Regime: B > 2*max(A) (carry-free).  Validated against the carry-aware dp_carry on
overlapping carry-free cases and against brute force via dp_carry's own validation.

Reformulation (kills the 2D Pareto blow-up):
  Sumset element <-> output vector c, c_i in A+A.  c feasible iff EXISTS split a_i+b_i=c_i,
  a_i,b_i in A, sum_a <= T, sum_b <= T.  With SC = sum_i c_i and S1 = sum_i a_i we have
  sum_b = SC - S1, so feasibility <=>  EXISTS reachable S1 with  S1 <= T  AND  SC - S1 <= T
                                       i.e. max(0, SC-T) <= S1 <= T.
  DP state per output prefix = (SC_partial, reachable-S1 set as a bitmask over [0..T]).
  Count distinct c = sum over end-states that are feasible, weighted by #prefixes.
  Bitmask reachable-S1: transition for output digit c adds, for each a in S_a(c)={a in A: c-a in A},
  a shift of the mask by a (capped at T).  SC_partial advances by c.

  Symmetric for differences: element <-> e_i in A-A, e feasible iff EXISTS a_i in A,
  b_i=a_i-e_i in A, sum_a<=T, sum_b<=T.  Track (SE_partial = sum e_i, reachable sum_a set).
  sum_b = sum_a - SE, feasibility <=> EXISTS reachable S1 in [max(0,SE), T+SE]∩[0,T] ... handled
  exactly via the second sum tracked directly -> we instead track (reachable (sum_a) bitmask)
  plus the running SE, and at the end require EXISTS S1 with S1<=T and S1 - SE in [0,T]
  i.e. SE <= S1 <= T  AND  S1 <= T+SE -> S1 in [max(0,SE), min(T, T+SE)] = [SE, T] (since SE>=? can be neg).
  e can be negative so SE can be negative; we keep the exact arithmetic.

Mask = Python int bitmask, bit k set <=> sum_a = k reachable (0<=k<=T).
"""
from collections import defaultdict

FULLMASK_CACHE = {}


def _cap_mask(T):
    return (1 << (T + 1)) - 1


def count_sumset(A, B, d, T):
    assert B > 2 * max(A), "dp_fast requires carry-free B > 2*max(A)"
    Aset = set(A)
    ApA = sorted({x + y for x in A for y in A})
    # per output digit c: the set of valid a (a in A, c-a in A)
    avals = {c: [a for a in A if (c - a) in Aset] for c in ApA}
    cap = _cap_mask(T)
    # state: (sc_partial) -> { mask(reachable sum_a) : count_of_prefixes }
    # but distinct masks must be tracked separately; key = (sc, mask)
    states = {(0, 1): 1}  # sc=0, mask bit0 set (sum_a=0 reachable), 1 prefix
    for _ in range(d):
        ns = defaultdict(int)
        for (sc, mask), cnt in states.items():
            for c in ApA:
                # new mask = OR over a in avals[c] of (mask << a), capped at T
                nm = 0
                for a in avals[c]:
                    nm |= (mask << a)
                nm &= cap
                if nm == 0:
                    continue  # all sum_a exceed T -> infeasible prefix extension
                ns[(sc + c, nm)] += cnt
        states = dict(ns)
    # finalize: feasible iff EXISTS S1 in mask with max(0,SC-T) <= S1 <= T
    total = 0
    for (sc, mask), cnt in states.items():
        lo = max(0, sc - T)
        # bits in [lo, T] of mask
        window = mask & (cap ^ ((1 << lo) - 1))  # clear bits below lo
        if window:
            total += cnt
    return total


def count_diffset(A, B, d, T):
    assert B > 2 * max(A), "dp_fast requires carry-free B > 2*max(A)"
    Aset = set(A)
    AmA = sorted({x - y for x in A for y in A})
    # per output digit e: valid a (a in A, a-e in A); b = a-e
    avals = {e: [a for a in A if (a - e) in Aset] for e in AmA}
    cap = _cap_mask(T)
    maxE = max(AmA)        # = max(A); also -min(AmA) = max(A) by symmetry of A-A
    minE = min(AmA)        # = -max(A)
    # track (se_partial, mask of reachable sum_a)
    states = {(0, 1): 1}
    for pos in range(d):
        rem = d - pos - 1          # positions AFTER this one
        ns = defaultdict(int)
        for (se, mask), cnt in states.items():
            for e in AmA:
                nm = 0
                for a in avals[e]:
                    nm |= (mask << a)
                nm &= cap
                if nm == 0:
                    continue
                nse = se + e
                # PRUNE on se: any reachable end-state needs final SE in [-T, T]
                # (sum_b = sum_a - SE, sum_a in [0,T], sum_b in [0,T] => SE in [-T,T]).
                # Future positions can change se by [rem*minE, rem*maxE].
                if nse + rem * maxE < -T or nse + rem * minE > T:
                    continue   # cannot complete to a feasible SE
                ns[(nse, nm)] += cnt
        states = dict(ns)
    total = 0
    for (se, mask), cnt in states.items():
        # need EXISTS S1 with S1<=T and sum_b = S1 - se in [0,T] -> se<=S1<=T+se
        lo = max(0, se)
        hi = min(T, T + se)
        if hi < lo:
            continue
        window = mask & (((1 << (hi + 1)) - 1) ^ ((1 << lo) - 1))
        if window:
            total += cnt
    return total


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
