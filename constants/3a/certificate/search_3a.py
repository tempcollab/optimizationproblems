#!/usr/bin/env python3
"""
Digit-set / hole search for the C_3a lower bound.

Reuses the EXACT integer-counting DPs from certify_3a.py (count_sum, count_diff,
max_U) and the rigorous interval theta (theta_lower_bound).  Each candidate digit
set A gets its OWN valid base = 2*max(A)+1 (the validity guard; base must be
>= 2*max(A)+1 or the carry-free DP overcounts -- the base-20 trap).

This script does two things:
  1) brute-force validation of count_sum / count_diff against a direct enumeration
     of U for several digit-set shapes (including holes) at small (d,T), to confirm
     the carry-free DP gives no overcount for the chosen base;
  2) a FLOAT-based screening sweep over (digit set, base=2M+1, T) at a moderate d
     to rank configurations, finding the best max-digit / hole pattern.

Ranking uses floats (math.log) for speed; the final certified number for the
winner is produced by certify_3a.py's rigorous interval theta_lower_bound.

Run:  python3 search_3a.py            (validation + sweep, ~a few minutes)
      python3 search_3a.py validate   (just the brute-force validation)
"""

import sys
import time
import math
from itertools import product

from certify_3a import count_sum, count_diff, max_U, theta_lower_bound


# ----------------------------------------------------------------------------
# Brute-force ground truth (enumerate U directly), for validation only
# ----------------------------------------------------------------------------
def brute_U(A, base, d, T):
    """All elements of U as a Python set (only usable for tiny d,T)."""
    A = sorted(set(A))
    elems = set()

    def rec(i, val, ssum):
        if i == d:
            elems.add(val)
            return
        p = base ** i
        for a in A:
            if ssum + a <= T:
                rec(i + 1, val + a * p, ssum + a)
    rec(0, 0, 0)
    return elems


def brute_counts(A, base, d, T):
    U = brute_U(A, base, d, T)
    SS = {x + y for x in U for y in U}
    DD = {x - y for x in U for y in U}
    return len(SS), len(DD), max(U)


# ----------------------------------------------------------------------------
# Candidate digit-set families
# ----------------------------------------------------------------------------
def family_drop1(M):
    """{0, 2, 3, ..., M}: drop the single digit 1, max digit M (the record shape)."""
    return [0] + list(range(2, M + 1))


def family_full(M):
    """{0, 1, 2, ..., M}: no hole."""
    return list(range(0, M + 1))


def family_drop_one(M, hole):
    """{0..M} with one interior digit `hole` removed (1 <= hole <= M-1, hole!=0,M)."""
    return [a for a in range(0, M + 1) if a != hole]


def family_drop_two(M, h1, h2):
    """{0..M} with two interior digits removed."""
    drop = {h1, h2}
    return [a for a in range(0, M + 1) if a not in drop]


def theta_float(A, base, d, T):
    """Fast FLOAT theta for ranking (NOT the certificate)."""
    m = max_U(A, base, d, T)
    S = count_sum(A, base, d, T)
    D = count_diff(A, base, d, T)
    if D <= S:
        return None, S, D, m
    th = 1.0 + math.log(D / S) / math.log(2 * m + 1)
    return th, S, D, m


# ----------------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------------
def validate():
    print("=" * 72)
    print("BRUTE-FORCE VALIDATION of count_sum/count_diff for several digit shapes")
    print("=" * 72)
    cases = [
        # (A, base, d, T) -- base = 2*max(A)+1 in every case (valid)
        (family_drop1(10), 21, 3, 8),
        (family_drop1(10), 21, 4, 10),
        (family_full(5), 11, 3, 9),
        (family_full(5), 11, 4, 8),
        (family_drop_one(11, 1), 23, 3, 9),       # M=11, hole=1 (drop1-M11)
        (family_drop_one(11, 5), 23, 3, 9),       # M=11, interior hole 5
        (family_drop_one(7, 3), 15, 4, 10),       # M=7, hole=3
        (family_drop_two(9, 1, 4), 19, 3, 9),     # two holes
        (family_full(11), 23, 3, 8),
    ]
    all_ok = True
    for A, base, d, T in cases:
        assert base >= 2 * max(A) + 1, "test case violates guard"
        Sb, Db, mb = brute_counts(A, base, d, T)
        Sd = count_sum(A, base, d, T)
        Dd = count_diff(A, base, d, T)
        md = max_U(A, base, d, T)
        ok = (Sb == Sd and Db == Dd and mb == md)
        all_ok = all_ok and ok
        print("A=%-28s b=%2d d=%d T=%2d : S %s/%s  D %s/%s  m %s  %s" % (
            str(A), base, d, T,
            Sd, Sb, Dd, Db, "ok" if md == mb else "MAX-MISMATCH",
            "OK" if ok else "*** MISMATCH ***"))
    print()
    # base-20 trap demonstration (guard-violating; DP must NOT be trusted here)
    Atrap = family_drop1(10)
    Sd = count_sum(Atrap, 20, 2, 20)
    Dd = count_diff(Atrap, 20, 2, 20)
    Sb, Db, _ = brute_counts(Atrap, 20, 2, 20)
    print("base-20 TRAP (guard violated, base=20<21): DP S/D = %d/%d  but true %d/%d "
          "-> DP overcounts (expected; guard rules this out)" % (Sd, Dd, Sb, Db))
    print()
    print("VALIDATION:", "ALL OK" if all_ok else "*** FAILURES ABOVE ***")
    print()
    return all_ok


# ----------------------------------------------------------------------------
# Screening sweep
# ----------------------------------------------------------------------------
def best_T(A, base, d, Tlo, Thi):
    """Return (bestT, best_theta_float, S, D, m) over T in [Tlo, Thi]."""
    bestT, bestth, bS, bD, bm = None, -1.0, None, None, None
    for T in range(Tlo, Thi + 1):
        th, S, D, m = theta_float(A, base, d, T)
        if th is not None and th > bestth:
            bestth, bestT, bS, bD, bm = th, T, S, D, m
    return bestT, bestth, bS, bD, bm


def sweep(d):
    print("=" * 72)
    print("SCREENING SWEEP (float theta, ranking only) at d =", d)
    print("=" * 72)
    # T window scales ~1.9*d around the per-d optimum; widen to be safe.
    Tlo = int(1.6 * d)
    Thi = int(2.1 * d) + 2

    candidates = []
    # record shape drop1, varying max digit M
    for M in range(8, 14):
        A = family_drop1(M)
        candidates.append(("drop1-M%d" % M, A, 2 * M + 1))
    # full {0..M}
    for M in range(8, 14):
        A = family_full(M)
        candidates.append(("full-M%d" % M, A, 2 * M + 1))
    # single interior hole at various positions for M=10,11,12
    for M in (10, 11, 12):
        for hole in range(1, M):
            A = family_drop_one(M, hole)
            candidates.append(("M%d-hole%d" % (M, hole), A, 2 * M + 1))

    rows = []
    for name, A, base in candidates:
        assert base >= 2 * max(A) + 1
        bT, bth, S, D, m = best_T(A, base, d, Tlo, Thi)
        rows.append((bth, name, A, base, bT, S, D, m))
        print("  %-12s base=%2d  bestT=%3d  theta=%.9f" % (name, base, bT, bth))
    rows.sort(reverse=True)
    print()
    print("TOP 6 by float theta at d=%d:" % d)
    for bth, name, A, base, bT, S, D, m in rows[:6]:
        print("  %-12s base=%2d  T=%3d  theta=%.9f" % (name, base, bT, bth))
    print()
    return rows


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "validate":
        validate()
        return

    t0 = time.time()
    ok = validate()
    if not ok:
        print("Validation failed; aborting sweep.")
        sys.exit(1)

    # Order-preservation check across two d values (outliner's requirement)
    rows40 = sweep(40)
    rows50 = sweep(50)

    # Report top config and its T window for the certified large-d run.
    print("=" * 72)
    print("Winner ranking (d=40 then d=50). Pick the config that leads at BOTH d.")
    print("Top at d=40:", rows40[0][1], "theta=%.9f" % rows40[0][0])
    print("Top at d=50:", rows50[0][1], "theta=%.9f" % rows50[0][0])
    print("total sweep runtime: %.1f s" % (time.time() - t0))


if __name__ == "__main__":
    main()
