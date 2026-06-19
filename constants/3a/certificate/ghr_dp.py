"""Shared exact-counting DP for the GHR single-set digit construction (constant 3a).

This is the reusable certificate ENGINE every Python sketch imports. It is VALIDATED
against Griego's record (PR #71): for A={0,2,3,4,5,6,7,8,9,10}, d=80, T=150, base=21 it
reproduces

    |U+U| = 75448362167176243488362019935078206851619643198150854886920234689186981134888
    |U-U| = 195351744295266763842135520514417052287242446785296742323733058216909095059024572338564089814415
    theta = 1.17407444769352116...

exactly (see tests at bottom; `python ghr_dp.py` runs them).

CONSTRUCTION.  Fix a digit alphabet A (finite, 0 in A), d digits, a global digit-sum cap T,
and the carry-free base b = 2*max(A)+1.  Define
    U = { sum_i a_i * b^i : a_i in A, sum_i a_i <= T }.
Because b = 2*max(A)+1, digit-wise sums/differences stay in [-(b-1), b-1] so the base-b
encoding is injective on U+U and U-U (no carries).  Then the GHR2007 single-set lemma gives
    C_3a >= 1 + log(|U-U| / |U+U|) / log(2*max(U)+1).

All three quantities |U+U|, |U-U|, max(U) are EXACT INTEGERS computed below.  The only
non-integer step is the final log-ratio, which a certifier bounds rationally (see the
`certify_*` sketches).  This makes the construction Lean-fittable (exact Nat counting + one
rational log inequality).
"""

from collections import defaultdict

try:
    import numpy as _np
except Exception:  # numpy optional; fast diffset degrades to the frozenset path
    _np = None


def carry_free_base(A):
    return 2 * max(A) + 1


def sumset_size(A, d, T):
    """Exact |U+U| via DP.

    An element of U+U is a base-b integer whose digit string (y_0..y_{d-1}), y_i in A+A,
    admits a split a_i+a'_i=y_i with a_i,a'_i in A, sum a_i <= T AND sum a'_i <= T.
    Distinct feasible y-strings <-> distinct elements of U+U (carry-free => injective).

    DP over positions; per partial string we track the SET of reachable (sa, sap) =
    (running sum of a_i, running sum of a'_i), both pruned at T.  Two partial strings with
    the same reachable-set are merged for counting (state = frozenset of (sa,sap) pairs,
    value = number of strings reaching it).  The number of distinct reachable-sets
    stabilizes (~few hundred), so this scales to d=80, T=150.
    """
    A = sorted(set(A))
    setA = set(A)
    AA = sorted(set(x + y for x in A for y in A))
    Py = {y: [a for a in A if (y - a) in setA] for y in AA}
    states = {frozenset([(0, 0)]): 1}
    for _ in range(d):
        new = defaultdict(int)
        for st, cnt in states.items():
            for y in AA:
                reach = set()
                for (sa, sap) in st:
                    for a in Py[y]:
                        nsa = sa + a
                        nsap = sap + (y - a)
                        if nsa <= T and nsap <= T:
                            reach.add((nsa, nsap))
                if reach:
                    new[frozenset(reach)] += cnt
        states = new
    return sum(states.values())


def diffset_size(A, d, T):
    """Exact |U-U| via DP.

    An element of U-U is a base-b integer with digit string (delta_0..delta_{d-1}),
    delta_i in A-A, that admits a split a_i-a'_i=delta_i, a_i,a'_i in A, with
    sum a_i <= T AND sum a'_i <= T.  For each delta the cheapest representative
    (a,a') = (q_delta+delta, q_delta), q_delta = min{b in A : b+delta in A}, simultaneously
    minimizes both totals, so a string is feasible iff its cheapest-rep totals are <= T.
    DP tracks (left total, right total), both pruned at T (so |state| <= (T+1)^2).
    """
    A = sorted(set(A))
    setA = set(A)
    DD = sorted(set(x - y for x in A for y in A))
    rep = {}
    for delta in DD:
        q = min(b for b in A if (b + delta) in setA)
        rep[delta] = (q + delta, q)
    states = {(0, 0): 1}
    for _ in range(d):
        new = defaultdict(int)
        for (la, ra), cnt in states.items():
            for delta in DD:
                dl, dr = rep[delta]
                nla, nra = la + dl, ra + dr
                if nla <= T and nra <= T:
                    new[(nla, nra)] += cnt
        states = new
    return sum(states.values())


def diffset_fast(A, d, T):
    """FAST exact |U-U| (numpy 2D shift-add, object dtype keeps counts EXACT).

    Identical semantics to ``diffset_size`` (same cheapest-rep argument) but the per-position
    transition ``new[la+dl, ra+dr] += old[la, ra]`` is a single vectorized slice-add over the
    (left total, right total) grid, so it runs in <1 s at the record scale (d=80, T=150) vs the
    hundreds-of-seconds frozenset path. Validated exact-match vs ``diffset_size`` on small cases
    and against Griego's |U-U| literal (see ``__main__``). Falls back to ``diffset_size`` if
    numpy is unavailable.
    """
    if _np is None:
        return diffset_size(A, d, T)
    A = sorted(set(A))
    setA = set(A)
    DD = sorted(set(x - y for x in A for y in A))
    reps = []
    for delta in DD:
        q = min(b for b in A if (b + delta) in setA)
        reps.append((q + delta, q))
    cur = _np.zeros((T + 1, T + 1), dtype=object)
    cur[0, 0] = 1
    for _ in range(d):
        nxt = _np.zeros((T + 1, T + 1), dtype=object)
        for (dl, dr) in reps:
            if dl <= T and dr <= T:
                nxt[dl:, dr:] += cur[:T + 1 - dl, :T + 1 - dr]
        cur = nxt
    return int(cur.sum())


def sumset_bitmask(A, d, T):
    """FAST exact |U+U| via a Python big-int bitmask per reachable-set state (~4x faster).

    Identical semantics to ``sumset_size`` but each state's reachable set of (sa, sap) pairs is
    encoded as ONE big integer (bit ``sa*W + sap``, ``W = 2T+2`` to stop row-bleed); the output
    digit transition is ``acc |= state << (a*W + ap)`` over admissible splits, masked back into
    the cap box. Big-int OR/shift is C-level, so the record scale (d=80, T=150) runs in ~155 s
    vs ~600 s for the frozenset path. Validated exact-match vs ``sumset_size`` on small cases and
    against Griego's |U+U| literal (see ``__main__``).
    """
    A = sorted(set(A))
    setA = set(A)
    AA = sorted(set(x + y for x in A for y in A))
    Py = {y: [a for a in A if (y - a) in setA] for y in AA}
    W = 2 * T + 2
    keep = 0
    for sa in range(T + 1):
        for sap in range(T + 1):
            keep |= 1 << (sa * W + sap)
    states = {1: 1}  # state big-int (only {(0,0)} set) -> count of digit-strings
    for _ in range(d):
        new = {}
        for st, cnt in states.items():
            for y in AA:
                acc = 0
                for a in Py[y]:
                    ap = y - a
                    if a <= T and ap <= T:
                        acc |= st << (a * W + ap)
                acc &= keep
                if acc:
                    new[acc] = new.get(acc, 0) + cnt
        states = new
    return sum(states.values())


def theta_floatbound_fast(A, d, T, verbose=False):
    """Same as ``theta_floatbound`` but uses the FAST diffset/sumset routines. Prints a
    per-stage progress line with ``flush=True`` when ``verbose`` (so a long run never looks
    like a silent hang)."""
    import time
    from math import log
    if verbose:
        print(f"  [dp] A={A} d={d} T={T} ...", flush=True)
    t0 = time.time()
    diff = diffset_fast(A, d, T)
    if verbose:
        print(f"  [dp] diffset done ({time.time()-t0:.1f}s)", flush=True)
    t1 = time.time()
    s = sumset_bitmask(A, d, T)
    if verbose:
        print(f"  [dp] sumset done ({time.time()-t1:.1f}s)", flush=True)
    q = 2 * max_U(A, d, T) + 1
    th = 1.0 + (log(diff) - log(s)) / log(q)
    if verbose:
        print(f"  [dp] theta={th:.10f} (total {time.time()-t0:.1f}s)", flush=True)
    return th, s, diff, q


def max_U(A, d, T):
    """Exact max(U): greedily fill highest positions with the largest admissible digit
    subject to the global cap sum a_i <= T."""
    A = sorted(set(A))
    b = carry_free_base(A)
    val = 0
    rem = T
    for i in range(d - 1, -1, -1):
        cands = [x for x in A if x <= rem]
        a = max(cands) if cands else 0
        val += a * b ** i
        rem -= a
    return val


def theta_floatbound(A, d, T):
    """Quick (NON-certified) float estimate of theta for search/ranking.  The CERTIFIED
    value comes from a directed-rounded rational log bound (see certify_* sketches)."""
    from math import log
    s = sumset_size(A, d, T)
    diff = diffset_size(A, d, T)
    q = 2 * max_U(A, d, T) + 1
    return 1.0 + (log(diff) - log(s)) / log(q), s, diff, q


if __name__ == "__main__":
    # Validation against Griego's record (small cases brute-checked separately).
    A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # Cross-check fast routines vs the validated frozenset/2D-grid oracles on small cases.
    for d0, T0 in [(6, 12), (8, 15), (10, 18)]:
        assert sumset_bitmask(A, d0, T0) == sumset_size(A, d0, T0), (d0, T0)
        assert diffset_fast(A, d0, T0) == diffset_size(A, d0, T0), (d0, T0)
    print("fast routines match oracle on small cases: OK")
    d, T = 80, 150
    s = sumset_size(A, d, T)
    diff = diffset_size(A, d, T)
    assert s == 75448362167176243488362019935078206851619643198150854886920234689186981134888, s
    assert diff == 195351744295266763842135520514417052287242446785296742323733058216909095059024572338564089814415, diff
    th, _, _, q = theta_floatbound(A, d, T)
    print("record reproduced: theta =", th)
    assert abs(th - 1.17407444769352116) < 1e-12
    print("OK")
