#!/usr/bin/env python3
"""
L2 — Push Griego's own family to larger (m,T) for the C_3a LOWER bound.

Constant C_3a (Gyarmati-Hennecart-Ruzsa sum-difference exponent), LOWER bound.
Target to beat (best verified): C_3a > 1.1740744  (Griego 2026, base-21 digit construction).

Family (fixed, Griego's):   A = {0,2,3,4,5,6,7,8,9,10},  base b = 21.
    W(m,T,A) = { x in A^m : sum x_i <= T },   g(x) = sum_i x_i b^i  (injective since b > 2*max(A)),
    U = { g(x) : x in W },   s = |U+U|,  d = |U-U|,  M = max(U),  q = 2M+1,
    theta = 1 + log(d/s)/log(q),   and  C_3a >= theta   ([GHR2007] lemma).

This script CLOSES the (m,T)-push hole by an EXACT column DP for |U+U|, |U-U|, max(U)
that scales far past brute force, then scans (m,T) to locate the family's supremum of theta.

=====================================================================================
WHY |U+U| / |U-U| reduce to counting digit-vectors (no carries):
Since b > 2*max(A), the base-b digits of g(x)+g(y) are exactly (x_i+y_i) in [0,2max(A)]
(no carries), and of g(x)-g(y) are exactly (x_i-y_i) in [-max(A),max(A)] (no borrows).
Hence
    |U+U| = #{ distinct sum-vectors (x_i+y_i)_i  realizable by x,y in W },
    |U-U| = #{ distinct diff-vectors (x_i-y_i)_i realizable by x,y in W }.
Both are counted EXACTLY below with directed integer arithmetic; the final
record comparison uses the cleared-denominator INTEGER inequality only (no float).

DIFF-SET decoupling (proved/verified):  for each difference value w there is a UNIQUE
pair (x*(w), y*(w)) in A x A with x-y=w minimizing BOTH coordinates simultaneously
(because x = y + w, so minimizing y minimizes x). Therefore a diff-vector v is
realizable under the two caps iff  sum_i x*(v_i) <= T  AND  sum_i y*(v_i) <= T.
=> a clean 2D DP over (sum x*, sum y*).  (self-tested vs brute force below.)

SUM-SET (no such decoupling — genuine x<->y tradeoff): a sum-vector v=(v_i) is realizable
iff there exist x_i in X_{v_i} (the achievable x-values for column-sum v_i) with
sum x_i <= T and sum y_i = (sum v_i) - (sum x_i) <= T, i.e. the reachable set of sum_x
meets [sum v_i - T, T].  We count DISTINCT sum-vectors with an EXACT bitmask DP whose
state is (sum v, reachable-set-of-sum_x-clamped-to-[0,T]); a vector is counted iff its
reachable sum_x set meets the feasibility window.  (self-tested vs brute force below.)

Run:  python3 griego-family-larger-mT.py
"""
import math
from collections import defaultdict
from fractions import Fraction
from itertools import product

TARGET = Fraction(11740744, 10000000)          # C_3a > 1.1740744  (Griego 2026)
A_GRIEGO = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
B_GRIEGO = 21


# ---------------------------------------------------------------- tables
def build_tables(A):
    """Per sum-value w: sorted achievable x-values X_w.
       Per diff-value w: minimal pair (x*(w), y*(w)) minimizing both coords."""
    A = sorted(set(A))
    assert 0 in A
    Xw = {}
    for w in sorted(set(x + y for x in A for y in A)):
        Xw[w] = sorted(set(x for x in A for y in A if x + y == w))
    cx, cy = {}, {}
    for w in sorted(set(x - y for x in A for y in A)):
        pairs = [(x, y) for x in A for y in A if x - y == w]
        ymin = min(y for _, y in pairs)
        x0, y0 = next((x, y) for x, y in pairs if y == ymin)
        cx[w], cy[w] = x0, y0
    return Xw, cx, cy


# ---------------------------------------------------------------- exact DPs
def count_sumset(A, m, T):
    """EXACT |U+U|. State (sum_v, R) where R = bitmask of reachable sum_x clamped to [0,T];
       count distinct sum-vectors whose reachable sum_x meets [sum_v - T, T].

    SOUND dynamic low-clamp (validated vs the un-clamped form and vs brute force):
    a reachable value Sx is feasible for THIS partial vector with running sum_v=Sv
    only if it can still satisfy Sx >= Sv_final - T at the end; since Sv only GROWS
    as columns are added (every column-sum w >= 0), any Sx < Sv - T is already, and
    forever, below the lower feasibility edge and can be dropped. So after each column
    we mask off bits below max(0, Sv - T). This keeps the DP exact (it already clamps
    the top at T) while drastically shrinking mask width and merging states near the
    top window -- the speedup that makes m>=80 run in seconds, not ~35 min.
    """
    Xw, _, _ = build_tables(A)
    sumvals = sorted(Xw)
    Tmask = (1 << (T + 1)) - 1
    shifts = {w: Xw[w] for w in sumvals}
    cur = defaultdict(int)
    cur[(0, 1)] = 1                      # sum_v=0, R={0}
    for _ in range(m):
        nxt = defaultdict(int)
        for (Sv, R), cnt in cur.items():
            for w in sumvals:
                nR = 0
                for x in shifts[w]:
                    nR |= (R << x)
                nSv = Sv + w
                nR &= Tmask                       # clamp top at T
                lo = nSv - T
                if lo > 0:
                    nR = (nR >> lo) << lo         # drop bits below Sv-T (never feasible)
                if nR:
                    nxt[(nSv, nR)] += cnt
        cur = nxt
    total = 0
    for (Sv, R), cnt in cur.items():
        lo = Sv - T
        if lo < 0:
            lo = 0
        rangemask = (Tmask >> lo) << lo          # bits lo..T
        if R & rangemask:
            total += cnt
    return total


def count_diffset(A, m, T):
    """EXACT |U-U| via the minimal-pair decoupling. State (sum x*, sum y*)."""
    _, cx, cy = build_tables(A)
    diffvals = sorted(cx)
    cur = defaultdict(int)
    cur[(0, 0)] = 1
    for _ in range(m):
        nxt = defaultdict(int)
        for (sx, sy), cnt in cur.items():
            for w in diffvals:
                nsx, nsy = sx + cx[w], sy + cy[w]
                if nsx <= T and nsy <= T:
                    nxt[(nsx, nsy)] += cnt
        cur = nxt
    return sum(cur.values())


def max_U(A, m, T, b):
    """EXACT max g(x), x in A^m, sum x <= T. Greedy from the top digit is optimal:
       weights b^i strictly increase and b>2max(A), so spending the cap on the highest
       positions first is optimal (verified vs exact DP for small cases)."""
    A = sorted(set(A))
    rem, val = T, 0
    for i in range(m - 1, -1, -1):
        a = max(x for x in A if x <= rem)
        val += a * b ** i
        rem -= a
        if rem < 0:
            rem = 0
    return val


# ---------------------------------------------------------------- brute-force oracle (small only)
def ghr_bruteforce(A, m, T, b):
    A = sorted(set(A))
    assert 0 in A and b > 2 * max(A)
    W = [t for t in product(A, repeat=m) if sum(t) <= T]
    U = sorted({sum(t[i] * b ** i for i in range(m)) for t in W})
    SS, DD = set(), set()
    for a in U:
        for c in U:
            SS.add(a + c)
            DD.add(a - c)
    return len(SS), len(DD), max(U)


# ---------------------------------------------------------------- read-off + certification
def theta_value(s, d, M):
    return 1.0 + math.log(d / s) / math.log(2 * M + 1)


def certifies_target_int(s, d, M, num, den):
    """EXACT big-integer certificate of  theta > num/den  for a rational num/den that is
       >= TARGET and has a SMALL denominator (so the integer powers are tractable; the full
       TARGET=11740744/10000000 has denominator 1.25e6 -> ~1e8-digit operands, infeasible).

       theta = 1 + log(d/s)/log q,  q = 2M+1.   theta > num/den
         iff  log(d/s)/log q > (num-den)/den
         iff  den*log(d/s) > (num-den)*log q
         iff  (d/s)^den > q^(num-den)
         iff  d^den  >  s^den * q^(num-den).
       Pure big-integer comparison, NO float.  This is the Lean-fit certification form
       (a single `native_decide`-shaped integer inequality).  Proving theta > num/den with
       num/den >= TARGET is a SUFFICIENT (in fact stronger) certificate that beats the record."""
    assert Fraction(num, den) >= TARGET, "the coarse rational must be >= the record target 1.1740744"
    q = 2 * M + 1
    return d ** den > s ** den * q ** (num - den)


def certifies_target(s, d, M, target=TARGET):
    """RIGOROUS directed-rounding test of theta > target via high-precision logs.
       theta>target iff  q'*log(d/s) > p'*log q   (q'=den(target-1), p'=num(target-1)).
       Lower-bound the LHS and upper-bound the RHS at 400-bit precision and require a
       guard band; returns True only when the strict inequality is certain.  (The pure
       integer form d^{q'} > s^{q'} q^{p'} is correct but has ~1e8-digit operands for the
       full target denominator; certifies_target_int above gives the tractable exact
       integer certificate against a small-denominator rational >= target.)"""
    import mpmath
    e = target - Fraction(1)
    qprime, pprime = e.denominator, e.numerator
    q = 2 * M + 1
    with mpmath.workprec(400):
        lhs_lo = qprime * (mpmath.log(mpmath.mpf(d)) - mpmath.log(mpmath.mpf(s)))
        rhs_hi = pprime * mpmath.log(mpmath.mpf(q))
        return lhs_lo - rhs_hi > mpmath.mpf("1e-30")


# ---------------------------------------------------------------- self-test
def self_test():
    A, b = A_GRIEGO, B_GRIEGO
    cases = [(2, 5), (3, 8), (4, 10), (4, 12), (5, 14), (3, 15), (4, 40), (5, 20)]
    for m, T in cases:
        bs, bd, bM = ghr_bruteforce(A, m, T, b)
        ds, dd, dM = count_sumset(A, m, T), count_diffset(A, m, T), max_U(A, m, T, b)
        assert (bs, bd, bM) == (ds, dd, dM), \
            f"DP/brute MISMATCH at m={m} T={T}: brute={(bs,bd,bM)} dp={(ds,dd,dM)}"
    print("[self-test] exact DP matches brute force on", len(cases), "cases (s,d,max).")


# ---------------------------------------------------------------- main
def report(m, T, coarse=(11741, 10000)):
    """Recompute s,d,M EXACTLY at (m,T) and report theta + the two record certificates:
       - EXACT big-integer: theta > coarse num/den (>= TARGET), via d^den > s^den*q^(num-den)
       - RIGOROUS log:      theta > TARGET=1.1740744, via directed-rounded high-precision logs.
       Both are sound certificates that strictly beat the record 1.1740744 (Griego 2026)."""
    s = count_sumset(A_GRIEGO, m, T)
    d = count_diffset(A_GRIEGO, m, T)
    M = max_U(A_GRIEGO, m, T, B_GRIEGO)
    th = theta_value(s, d, M)
    ok_int = certifies_target_int(s, d, M, *coarse)
    ok_log = certifies_target(s, d, M)
    return s, d, M, th, ok_int, ok_log


# Verified record-beating points on the Griego family A={0,2,..,10}, b=21
# (located by the (m,T) scan, see approaches/griego-family-larger-mT.md and
#  certificate/scan-mT-results.txt). theta CLIMBS monotonically along the optimal ray:
#   (80,150)=1.1740744477 (Griego's own point, reproduced exactly = the record),
#   (80,154)=1.1741714, (100,190)=1.1754955, (110,210)=1.1760056 -- all > 1.1740744.
WINNERS = [(80, 154), (100, 190), (110, 210)]
PEAK_MT = (110, 210)   # best verified point in this round's scan


def main():
    print("L2: push Griego's family A={0,2,..,10}, b=21 to larger (m,T).")
    print("Bar to beat (best verified): C_3a > 1.1740744 (Griego 2026).\n")
    self_test()
    print()
    # the record point reproduced exactly, then the climb past it
    print("Reproduce Griego's record point and the climb past it (exact DP):")
    for (m, T) in [(80, 150), (80, 154), (100, 190), (110, 210)]:
        s, d, M, th, ok_int, ok_log = report(m, T)
        tag = "(= Griego record point)" if (m, T) == (80, 150) else ""
        print(f"  m={m:3d} T={T:3d}: theta~{th:.10f}  "
              f"exact_int(theta>1.1741)={ok_int}  rig_log(theta>1.1740744)={ok_log} {tag}")
    print()
    m, T = PEAK_MT
    s, d, M, th, ok_int, ok_log = report(m, T)
    print(f"BEST VERIFIED POINT  m={m} T={T}:")
    print(f"  s=|U+U|={s}")
    print(f"  d=|U-U|={d}")
    print(f"  M=max(U)={M}")
    print(f"  theta ~ {th:.10f}")
    print(f"  EXACT integer certificate  d^10000 > s^10000 * (2M+1)^1741  =>  theta > 1.1741 : {ok_int}")
    print(f"  rigorous log certificate   theta > 1.1740744 (Griego record)               : {ok_log}")
    if ok_int and ok_log:
        assert certifies_target_int(s, d, M, 11741, 10000)
        print(f"  CERTIFIED: C_3a >= theta > 1.1741 > 1.1740744 -- BEATS the record.")
    else:
        print(f"  NOT certified at this point.")


if __name__ == "__main__":
    main()
