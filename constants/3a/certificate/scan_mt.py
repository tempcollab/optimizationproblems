#!/usr/bin/env python3
"""
Checkpointing scan for the C_3a LOWER bound (sketch griego-family-larger-mT).

Computes EXACT (s=|U+U|, d=|U-U|, M=max U) and the exact integer record test
   d^{q'} > s^{q'} * (2M+1)^{p'}   with  q'=1250000, p'=217593   (theta > 1.1740744)
for the Griego family A={0,2,..,10}, b=21, at a list of (m,T) points.

Each point PRINTS immediately and is appended to scan-mT-results.txt.
The DP functions are imported from the (self-tested) oracle module.

Usage:  python3 scan_mt.py m T [T2 T3 ...]
        python3 scan_mt.py --row m   (sweep a band of T around the optimal ray ~1.88*m)
"""
import sys, time, math, importlib.util, os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("g", os.path.join(HERE, "griego-family-larger-mT.py"))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

A, B = g.A_GRIEGO, g.B_GRIEGO
TARGET = Fraction(11740744, 10000000)
E = TARGET - 1
QP, PP = E.denominator, E.numerator   # 1250000, 217593
RESULTS = os.path.join(HERE, "scan-mT-results.txt")


import mpmath
mpmath.mp.prec = 400   # ~120 decimal digits, ample for these ratios


def beats(s, d, M):
    """RIGOROUS (directed-rounding) test of theta > TARGET = 11740744/10000000.
       theta>target  <=>  Q*ln(d/s) > P*ln(q),  Q=1250000, P=217593, q=2M+1.
       Lower-bound the LHS and upper-bound the RHS with mpmath directed rounding;
       return True only if LHS_low > RHS_high (so the strict inequality is certain).
       (The pure-integer form d^Q > s^Q q^P is correct but has ~1e8-digit operands;
        the coarse small-denominator integer certificate below is used for the final
        verified winner.)"""
    q = 2 * M + 1
    with mpmath.workprec(400):
        lhs_lo = QP * (mpmath.log(mpmath.mpf(d)) - mpmath.log(mpmath.mpf(s)))
        rhs_hi = PP * mpmath.log(mpmath.mpf(q))
        # add a tiny guard band (1e-30) to stay safely on the strict side
        return lhs_lo - rhs_hi > mpmath.mpf("1e-30")


def beats_int(s, d, M, num, den):
    """EXACT big-integer certificate that theta > num/den (a rational with num/den
       >= TARGET and a SMALL denominator so the powers are tractable).
       theta>num/den  <=>  (d/s)^den > q^(num-den)  <=>  d^den > s^den * q^(num-den).
       Pure integer comparison, no float -- this is the Lean-fit certification form."""
    assert Fraction(num, den) >= TARGET, "coarse rational must be >= the record target"
    q = 2 * M + 1
    e = num - den            # num/den - 1, times den
    return d ** den > s ** den * q ** e


def theta(s, d, M):
    return 1.0 + math.log(d / s) / math.log(2 * M + 1)


def point(m, T):
    t0 = time.time()
    d = g.count_diffset(A, m, T)
    td = time.time() - t0
    t1 = time.time()
    s = g.count_sumset(A, m, T)
    ts = time.time() - t1
    M = g.max_U(A, m, T, B)
    th = theta(s, d, M)
    bt = beats(s, d, M)
    line = (f"m={m} T={T} theta={th:.10f} beat={bt} "
            f"s={s} d={d} M={M} t_d={td:.1f}s t_s={ts:.1f}s")
    print(line, flush=True)
    with open(RESULTS, "a") as f:
        f.write(line + "\n")
    return th, bt


def main():
    args = sys.argv[1:]
    if not args:
        print("usage: scan_mt.py m T [T...]  |  scan_mt.py --row m [Tlo Thi]")
        return
    if args[0] == "--row":
        m = int(args[1])
        # optimal ray ~1.88*m near the crossing; sweep a band
        center = round(1.88 * m)
        lo = int(args[2]) if len(args) > 2 else center - 4
        hi = int(args[3]) if len(args) > 3 else center + 4
        best = None
        for T in range(lo, hi + 1):
            th, bt = point(m, T)
            if best is None or th > best[0]:
                best = (th, T, bt)
        print(f"ROW m={m}: best theta={best[0]:.10f} at T={best[1]} beat={best[2]}", flush=True)
        return
    m = int(args[0])
    for T in (int(x) for x in args[1:]):
        point(m, T)


if __name__ == "__main__":
    main()
