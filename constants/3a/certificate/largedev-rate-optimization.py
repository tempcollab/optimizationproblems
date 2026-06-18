#!/usr/bin/env python3
"""
L3 — Joint base + digit-cap re-optimization via the large-deviation rate, for C_3a.

Build the asymptotic GUIDE (which alphabet/ray maximizes the GHR ratio), then
certify the chosen optimum with the SAME finite integer check as L1/L2.

General-alphabet rate (T = floor(r*m)):
    (1/m) log |W(m,T,A)|  ->  log|A| - I_A(r),
    I_A(r) = sup_lambda ( lambda*r - Lambda_A(lambda) ),
    Lambda_A(lambda) = log( (1/|A|) sum_{a in A} e^{lambda a} ).
Sum/difference set growth rates sigma^+_A(r), sigma^-_A(r) come from the digit-pair
multiplicities rho^+_A(v)=#{(a,a'):a+a'=v}, rho^-_A(d)=#{(a,a'):a-a'=d} under the
coupled cap. Then:
    theta_inf(A,r) = 1 + (sigma^-_A(r) - sigma^+_A(r)) / log(2*max(A)+1).
Maximize theta_inf over (A,r); the L1/L2 finite check certifies near the optimum.

The rate function is ONLY a search heuristic — it never enters the certificate.
TARGET TO BEAT (best verified): C_3a > 1.1740744 (Griego 2026).
Run: python3 largedev-rate-optimization.py
"""
import math
from fractions import Fraction
from collections import Counter

TARGET = Fraction(11740744, 10000000)


def Lambda_A(A, lam):
    A = sorted(set(A))
    mean = sum(math.exp(lam * a) for a in A) / len(A)
    return math.log(mean)


def digit_pair_multiplicities(A):
    """Exact (rho^+, rho^-) Counters for the alphabet — NOT a hole, used by the rate."""
    A = sorted(set(A))
    plus, minus = Counter(), Counter()
    for a in A:
        for c in A:
            plus[a + c] += 1
            minus[a - c] += 1
    return plus, minus


def certifies_target(s, d, q, target=TARGET):
    e = target - 1
    return d**e.denominator > s**e.denominator * q**e.numerator


# HOLE 1 (HARD, analytic): sum/difference-set growth-rate functions under the coupled cap.
def sigma_plus_minus(A, r):
    """
    HOLE: Legendre/large-deviation identity giving sigma^+_A(r), sigma^-_A(r),
    the (1/m)log growth rates of |U+U| and |U-U| for the digit construction with
    cap T = r*m, from the pair multiplicities rho^+_A, rho^-_A under the coupled
    constraint (both summands obey sum <= T). Guides the search; not certified.
    """
    raise NotImplementedError("HOLE: large-deviation rate functions sigma^+_A, sigma^-_A")


# HOLE 2 (MEDIUM): maximize theta_inf(A,r) over alphabets and ray.
def optimize_A_r():
    """
    HOLE: outer loop over (small/gapped) alphabets A, inner convex optimization
    over r, using theta_inf(A,r) = 1 + (sigma^- - sigma^+)/log(2max(A)+1).
    Returns the predicted-optimal (A, r).
    """
    raise NotImplementedError("HOLE: maximize theta_inf(A,r) over alphabet A and ray r")


# HOLE 3 (shared with L1): certify the predicted optimum finitely.
def certify_finite(A, r):
    """
    HOLE: instantiate (m, T=floor(r*m)) near the rate-optimal (A,r), compute exact
    s,d,q via the L1 column-DP, and check certifies_target(s,d,q). This is the
    ONLY step that produces a verified bound.
    """
    raise NotImplementedError("HOLE: finite certification at predicted-optimal (A,r)")


def main():
    print("L3 large-deviation rate optimization — bar: C_3a > 1.1740744\n")
    A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    plus, minus = digit_pair_multiplicities(A)
    print(f"  Griego A={A}")
    print(f"  Lambda_A(0.5) = {Lambda_A(A, 0.5):.6f}   (rate-function ingredient, computable)")
    print(f"  |A+A|={len(plus)} distinct sum-digits, |A-A|={len(minus)} distinct diff-digits")
    print("  (these feed sigma^+/sigma^- — the analytic hole)\n")
    try:
        A_opt, r_opt = optimize_A_r()
        print("predicted optimum:", A_opt, r_opt)
        print("certified:", certify_finite(A_opt, r_opt))
    except NotImplementedError as ex:
        print("OPEN HOLE:", ex)


if __name__ == "__main__":
    main()
