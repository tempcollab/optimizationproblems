#!/usr/bin/env python3
"""
Exact-integer-counting certificate for a lower bound on the
Gyarmati-Hennecart-Ruzsa sum-difference constant C_3a.

Engine (GHR2007 lemma, see constants/3a.md and literature/GHR2007_lemma.md):
  Any finite set U of non-negative integers with 0 in U yields
        C_3a >= theta(U) = 1 + ln(|U-U| / |U+U|) / ln(2*max(U)+1).

Construction (G2026 family, pushed to larger depth d this round):
  digit set  A = {0,2,3,4,5,6,7,8,9,10}   (the digit 1 is DROPPED; max digit = 10)
  base       b = 21
  depth      d
  digit-sum cap  T
        U = { sum_{i=0}^{d-1} a_i * b^i : a_i in A, sum_i a_i <= T }.

This certificate:
  * Counts S = |U+U|, D = |U-U|, and m = max(U) as EXACT Python big integers
    (no floats in the counting).
  * Enforces & prints the VALIDITY GUARD  b >= 2*max(A)+1, which guarantees the
    base-b digit representations of every element of U+U and U-U are carry-free,
    so the two dynamic programs below count distinct integers (not distinct digit
    vectors).  (At b = 2*max(A) = 20 the carries collide and the DP OVERCOUNTS --
    the "base-20 trap"; the guard rules that out.)
  * Confirms the GHR-lemma hypotheses on U: finite, non-negative, contains 0.
  * Computes a RIGOROUS LOWER BOUND on theta(U) using mpmath INTERVAL arithmetic
    (mpmath.iv) on the exact bignums S, D, q = 2m+1 -- i.e. NO float math.log.
    The printed theta is the lower endpoint of a verified enclosing interval and
    is therefore a guaranteed lower bound on the true real-number value of theta.

Run:  python3 certify_3a.py
(Default d=90, T=172; runtime ~45s.  Pass d and T on the command line to change.)
"""

import sys
import time

# ----------------------------------------------------------------------------
# Construction parameters
# ----------------------------------------------------------------------------
A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]   # digit set: drop the digit 1, max digit 10
BASE = 21                             # base b
RECORD = 1.1740744                    # best VERIFIED lower bound to beat [G2026]


# ----------------------------------------------------------------------------
# Exact integer counting
# ----------------------------------------------------------------------------
def max_U(A, base, d, T):
    """max(U) as an exact big integer: greedily fill the highest digits with the
    largest admissible digit, respecting the digit-sum cap T."""
    A = sorted(set(A))
    rem = T
    m = 0
    for i in range(d - 1, -1, -1):
        a = max(x for x in A if x <= rem)
        m += a * (base ** i)
        rem -= a
    return m


def count_sum(A, base, d, T):
    """|U+U| as an exact big integer.

    An element of U+U is  sum_i (a_i + b_i) * base^i  with a_i,b_i in A,
    sum a_i <= T, sum b_i <= T.  Because base >= 2*max(A)+1, every per-digit
    value (a_i+b_i) lies in [0, 2*max(A)] < base, so there are NO carries and the
    integer is in bijection with the digit vector y = (y_i = a_i + b_i).
    Hence |U+U| = #{ achievable digit vectors y with y_i in A+A and a
    representation y_i = a_i + b_i obeying both sum caps }.

    DP over digit positions.  State after placing some prefix of digits:
      ty   = running sum of the digit-sum  sum_i y_i  (= sum a_i + sum b_i)
      bits = bitset over s in [0..T] of the values  s = sum_i a_i  achievable
             for THIS y-prefix (bit s set <=> some choice of the a_i with the
             chosen y_i achieves sum a_i = s and is feasible so far).
    Placing a new digit y multiplies bits by the per-digit "shift" polynomial
    (a may be any value with a in A and y-a in A; each contributes a <<a shift),
    and advances ty by y.  At the end an element is feasible iff there is an s
    with  s <= T  (sum a_i ok)  AND  ty - s <= T  (sum b_i = ty - s ok).
    """
    A = sorted(set(A))
    Aset = set(A)
    Y = sorted({a + b for a in A for b in A})            # possible per-digit y
    # for each y, the admissible a (then b = y-a) values:
    P = {y: tuple(a for a in A if (y - a) in Aset) for y in Y}
    mask = (1 << (T + 1)) - 1                             # keep only bits 0..T

    cache = {}
    def shift(bitset, y):
        k = (bitset, y)
        v = cache.get(k)
        if v is not None:
            return v
        out = 0
        for a in P[y]:
            out |= bitset << a
        out &= mask                                      # any s>T is infeasible
        cache[k] = out
        return out

    # states: ty -> { bitset : count_of_y_prefixes_with_that_(ty,bitset) }
    states = {0: {1: 1}}                                 # empty prefix: sum a_i = 0
    for _ in range(d):
        ns = {}
        for ty, bs in states.items():
            for bitset, cnt in bs.items():
                for y in Y:
                    nty = ty + y
                    if nty <= 2 * T:                     # sum a + sum b <= 2T
                        nb = shift(bitset, y)
                        if nb:                           # some a-sum still <= T
                            b = ns.setdefault(nty, {})
                            b[nb] = b.get(nb, 0) + cnt
        states = ns

    full = (1 << (T + 1)) - 1
    S = 0
    for ty, bs in states.items():
        lower = max(0, ty - T)                           # need s >= ty - T (b-cap)
        feas = full ^ ((1 << lower) - 1) if lower else full   # bits s in [lower, T]
        for bitset, cnt in bs.items():
            if bitset & feas:                            # feasible s exists
                S += cnt
    return S


def count_diff(A, base, d, T):
    """|U-U| as an exact big integer.

    An element of U-U is  sum_i (a_i - b_i) * base^i  with a_i,b_i in A,
    sum a_i <= T, sum b_i <= T.  Because base >= 2*max(A)+1, every per-digit
    value (a_i - b_i) lies in [-max(A), max(A)], a carry-free signed-digit
    representation, so the integer is in bijection with the digit vector
    delta = (a_i - b_i).  We must count distinct delta vectors that admit SOME
    representation a_i - b_i = delta_i with both sum caps satisfied.

    For a fixed target delta, the per-digit choice (a,b) with a-b=delta and
    a,b in A that MINIMIZES both sums simultaneously takes the smallest feasible
    b (and a = b + delta); minimizing every digit's (a,b) jointly minimizes both
    sum a_i and sum b_i, so feasibility of delta <=> the min-sum representation
    obeys both caps.  DP over (left = running sum a_i, right = running sum b_i)
    using, per delta, the unique min-sum (a,b) pair.
    """
    A = sorted(set(A))
    Aset = set(A)
    Delta = sorted({a - b for a in A for b in A})
    feats = []
    for delta in Delta:
        b = min(x for x in A if (x + delta) in Aset)     # smallest feasible b
        feats.append((b + delta, b))                     # (a, b) = (left, right) increments

    st = {(0, 0): 1}                                     # (sum a, sum b) -> #delta prefixes
    for _ in range(d):
        ns = {}
        for (l, r), cnt in st.items():
            for da, db in feats:
                nl = l + da
                nr = r + db
                if nl <= T and nr <= T:
                    k = (nl, nr)
                    ns[k] = ns.get(k, 0) + cnt
        st = ns
    return sum(st.values())


# ----------------------------------------------------------------------------
# Rigorous lower bound on theta via interval arithmetic (no float log)
# ----------------------------------------------------------------------------
def theta_lower_bound(S, D, m):
    """Return (theta_lo as Python float for printing, theta_lo_mpf exact-ish).

    theta = 1 + ln(D/S) / ln(q),  q = 2m+1,  with D > S > 0 and q > 1, so the
    numerator and denominator are both strictly positive.  Using mpmath INTERVAL
    arithmetic (mpmath.iv) every ln is computed as a verified enclosing interval
    [lo, hi] with lo <= true <= hi.  We then form
        theta_iv = 1 + ln_iv(D/S) / ln_iv(q)
    and take theta_iv.a (the LOWER endpoint of the verified enclosure) as the
    certified lower bound.  Interval division of two positive intervals already
    rounds the quotient's lower endpoint down, so theta_iv.a <= true theta.
    """
    from mpmath import iv, mpf
    iv.prec = 400                                        # >120 decimal digits of working precision

    S_iv = iv.mpf(S)                                     # exact: integers are representable
    D_iv = iv.mpf(D)
    q_iv = iv.mpf(2 * m + 1)

    num_iv = iv.log(D_iv / S_iv)                         # enclosure of ln(D/S) > 0
    den_iv = iv.log(q_iv)                                # enclosure of ln(q)   > 0
    theta_iv = 1 + num_iv / den_iv                       # enclosing interval for theta

    theta_lo = theta_iv.a                                # certified lower endpoint
    return theta_lo


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    d = int(sys.argv[1]) if len(sys.argv) > 1 else 90
    T = int(sys.argv[2]) if len(sys.argv) > 2 else 172

    maxA = max(A)
    guard_ok = BASE >= 2 * maxA + 1

    print("=" * 72)
    print("EXACT-INTEGER-COUNTING CERTIFICATE for a lower bound on C_3a")
    print("=" * 72)
    print("Engine: GHR2007 lemma  C_3a >= 1 + ln(|U-U|/|U+U|) / ln(2*max(U)+1)")
    print()
    print("Construction:")
    print("  base b            =", BASE)
    print("  digit set A       =", A, " (digit 1 dropped; max digit =", maxA, ")")
    print("  depth d           =", d)
    print("  digit-sum cap T   =", T)
    print("  U = { sum_i a_i*b^i : a_i in A, sum_i a_i <= T }")
    print()

    # --- GHR-lemma hypotheses on U -------------------------------------------
    print("GHR-lemma hypotheses on U:")
    print("  U finite?            YES (a_i range over the finite set A, d digits)")
    print("  U non-negative?      YES (0 = min(A), base^i > 0  =>  every element >= 0)")
    print("  0 in U?              YES (all a_i = 0 gives 0, and sum 0 <= T)")
    print()

    # --- Validity guard ------------------------------------------------------
    print("VALIDITY GUARD (carry-free / no base-20 trap):")
    print("  require base >= 2*max(A)+1  =>  %d >= %d : %s" %
          (BASE, 2 * maxA + 1, "OK" if guard_ok else "VIOLATED"))
    print("  (At base = 2*max(A) the per-digit sums reach the base and carries")
    print("   collide, so the DP would overcount |U+U|/|U-U|.  Guard rules it out;")
    print("   with the guard the base-b digit reps of U+U and U-U are carry-free,")
    print("   so the two DPs below count DISTINCT INTEGERS.)")
    if not guard_ok:
        print("  >>> GUARD VIOLATED -- construction INVALID, aborting.")
        sys.exit(1)
    print()

    # --- Exact counts --------------------------------------------------------
    t0 = time.time()
    m = max_U(A, BASE, d, T)
    S = count_sum(A, BASE, d, T)
    D = count_diff(A, BASE, d, T)
    t1 = time.time()

    q = 2 * m + 1
    print("Exact integer counts (Python big integers, no floats):")
    print("  S = |U+U| =", S)
    print("           (%d decimal digits)" % len(str(S)))
    print("  D = |U-U| =", D)
    print("           (%d decimal digits)" % len(str(D)))
    print("  max(U)    =", m)
    print("           (%d decimal digits)" % len(str(m)))
    print("  q = 2*max(U)+1 =", q)
    print("  D > S ?", D > S, " (required for theta > 1)")
    print("  counting runtime: %.1f s" % (t1 - t0))
    print()

    # --- Certified theta (rigorous lower bound, interval arithmetic) ---------
    theta_lo = theta_lower_bound(S, D, m)
    print("Certified theta (RIGOROUS LOWER bound via mpmath interval arithmetic):")
    print("  method: theta_iv = 1 + iv.log(D/S) / iv.log(q) at iv.prec=400 bits;")
    print("          report the lower endpoint theta_iv.a  (<= true theta).")
    from mpmath import mp, mpf
    mp.prec = 400
    print("  theta_lower_bound =", mpf(theta_lo))
    print()

    beats = theta_lo > RECORD
    print("-" * 72)
    print("  record to beat [G2026] : %.7f" % RECORD)
    print("  certified theta (lower): %s" % mpf(theta_lo))
    print("  margin over record     : %s" % (mpf(theta_lo) - mpf(RECORD)))
    print("  BEATS RECORD %.7f: %s" % (RECORD, "YES" if beats else "NO"))
    print("-" * 72)


if __name__ == "__main__":
    main()
