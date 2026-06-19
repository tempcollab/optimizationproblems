"""
EXACT carry-AWARE digit-DP for |U+U|, |U-U|, max(U) for the GHR digit construction
   U = { sum_i a_i B^i : a_i in A, i<d, sum_i a_i <= T },  0 in A.

Works for ANY B (carries handled), so it validates against brute force on the carry anchor
(A={0,2,3,4,5}, B=7) AND computes the record (B=21, carry-free) identically.

Counting distinct VALUES of u+v (resp. u-v):
  An element u+v is a base-B number.  Process positions i=0..d-1 low->high, carrying.
  At each position pick output digit pair contributions; the realized base-B output digit is
  determined by (a_i+b_i+carry_in).  Distinct output base-B digit sequences (incl. the final
  carry flush) <-> distinct values.  Cap constraints sum_a<=T, sum_b<=T couple globally, so
  the DP tracks, PER distinct output-digit prefix, the SET of reachable internal states
  (carry, s1, s2).  We count an output sequence as achievable iff its reachable-state set is
  nonempty at the end with carry fully flushed and s1,s2<=T.

State reduction: for a fixed (carry) we only need Pareto-minimal (s1,s2) within [0,T]^2
(we just need SOME reachable (s1,s2)<=(T,T)).  So a state is a dict carry -> frozenset of
Pareto-minimal (s1,s2).  The DP value is the number of distinct output prefixes mapping to
each such state.

For DIFFERENCES u-v we use a BORROW automaton symmetric to carries.
"""
from collections import defaultdict


def _pareto(points, T):
    pts = sorted(set(p for p in points if 0 <= p[0] <= T and 0 <= p[1] <= T))
    keep = []
    best_y = None
    for x, y in pts:
        if best_y is None or y < best_y:
            keep.append((x, y))
            best_y = y
    return frozenset(keep)


def _canon(state, T):
    """state: dict carry->set of (s1,s2). Return canonical frozenset of (carry, frozenset-pareto)."""
    items = []
    for c, pts in state.items():
        pr = _pareto(pts, T)
        if pr:
            items.append((c, pr))
    return frozenset(items)


def count_sumset(A, B, d, T):
    Aset = sorted(A)
    # output digit at a position given (a+b+carry_in): out = val % B, carry_out = val // B
    # max a+b = 2*max(A); plus carry_in up to (2*max(A)) // B ... carry stays bounded.
    # DP: states map canonical-state -> count of distinct output prefixes.
    init = _canon({0: {(0, 0)}}, T)
    states = {init: 1}
    for _ in range(d):
        new_states = defaultdict(int)
        for st, cnt in states.items():
            stdict = dict(st)  # carry -> frozenset of (s1,s2)
            # for each output digit value 'o' in 0..B-1, gather reachable states
            # produced by choosing a,b in A with (a+b+carry_in) % B == o
            by_out = defaultdict(lambda: defaultdict(set))  # o -> carry_out -> set (s1,s2)
            for carry_in, pts in stdict.items():
                for a in Aset:
                    for b in Aset:
                        val = a + b + carry_in
                        o = val % B
                        carry_out = val // B
                        for (s1, s2) in pts:
                            ns1, ns2 = s1 + a, s2 + b
                            if ns1 <= T and ns2 <= T:
                                by_out[o][carry_out].add((ns1, ns2))
            for o, cstate in by_out.items():
                cs = _canon(dict(cstate), T)
                if cs:
                    new_states[cs] += cnt
        states = dict(new_states)
    # flush remaining carries: each distinct nonzero carry value yields extra high digits.
    # After d positions, a state with carry c>0 still has 'c' to emit as further base-B digits
    # (no more a,b contributions). Different terminal carry sequences are distinct numbers but
    # since no more digits are added, the leftover carry 'c' expands deterministically into
    # base-B digits -> a UNIQUE suffix per carry value. So each distinct (carry) at the end
    # gives a distinct value-suffix; we must NOT merge different carries.
    # Count: for each state, the number of distinct (output-prefix already distinct) times the
    # number of distinct terminal carries reachable with a valid (s1,s2)<=(T,T).
    total = 0
    for st, cnt in states.items():
        carries_ok = sum(1 for (c, pts) in st if len(pts) > 0)
        total += cnt * carries_ok
    return total


def count_diffset(A, B, d, T):
    """
    |U-U|: u-v with borrow automaton.  At position i: val = a - b - borrow_in.
    output digit o = val mod B in [0,B-1], borrow_out = 0 if val>=0 else 1 (val in [-(maxA+1), maxA]).
    The difference u-v can be negative overall; we count distinct integer VALUES of u-v.
    A negative difference -x is distinct from +x; by symmetry |U-U| is symmetric about 0, but
    we count the SET directly so we don't assume symmetry.
    Track terminal borrow: a leftover borrow means the number is negative (high-order sign);
    distinct terminal borrow -> distinct sign-class, handled like carry flush.
    """
    Aset = sorted(A)
    init = _canon({0: {(0, 0)}}, T)  # borrow_in = 0
    states = {init: 1}
    for _ in range(d):
        new_states = defaultdict(int)
        for st, cnt in states.items():
            stdict = dict(st)  # borrow_in -> set (s1,s2)
            by_out = defaultdict(lambda: defaultdict(set))  # o -> borrow_out -> set
            for borrow_in, pts in stdict.items():
                for a in Aset:
                    for b in Aset:
                        val = a - b - borrow_in
                        o = val % B
                        borrow_out = 0 if val >= 0 else 1
                        for (s1, s2) in pts:
                            ns1, ns2 = s1 + a, s2 + b
                            if ns1 <= T and ns2 <= T:
                                by_out[o][borrow_out].add((ns1, ns2))
            for o, bstate in by_out.items():
                cs = _canon(dict(bstate), T)
                if cs:
                    new_states[cs] += cnt
        states = dict(new_states)
    total = 0
    for st, cnt in states.items():
        borrows_ok = sum(1 for (bo, pts) in st if len(pts) > 0)
        total += cnt * borrows_ok
    return total


def maxU(A, B, d, T):
    a_sorted = sorted(A)
    M = 0
    rem = T
    for i in range(d - 1, -1, -1):
        valid = max((x for x in A if x <= rem), default=0)
        M += valid * (B ** i)
        rem -= valid
        if rem <= 0:
            break
    return M
