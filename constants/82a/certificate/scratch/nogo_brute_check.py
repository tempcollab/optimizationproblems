"""
Cross-check the FFT C_n routine against a direct brute-force k-fold sum on small
discrete measures, for k=2,4 (and k=6 on a tiny measure). Validates the
convolution identity C_n = INT log|S| d(rho^{*n}).
"""
import numpy as np
from itertools import product
from scratch.nogo_Cmu0 import C_n_from_measure, conj_sym, zz_sym


def C_brute(pts, ms, k):
    """Direct: C = sum over all k-tuples of prod(masses) * log|sum_i s_i x_i|,
    s = (+1,...,+1,-1,...,-1) balanced. Drop exact-zero (measure-zero diag)."""
    n = k // 2
    s = [1] * n + [-1] * n
    M = len(pts)
    tot = 0.0
    for tup in product(range(M), repeat=k):
        S = sum(s[m] * pts[tup[m]] for m in range(k))
        a = abs(S)
        if a < 1e-14:
            continue
        wt = 1.0
        for m in range(k):
            wt *= ms[tup[m]]
        tot += wt * np.log(a)
    return tot


if __name__ == "__main__":
    # small symmetric measure: 3 half-nodes
    K = 3
    th = (np.arange(K) + 0.5) / K * (np.pi / 2)
    q = np.array([0.5, 0.3, 0.2])
    z, m = conj_sym(th, q / q.sum())
    pts, ms = zz_sym(z, m)        # 12 points (3 half * 2 conj * 2 zz)
    print(f"measure has {len(pts)} atoms, total mass {ms.sum():.6f}")

    for k in (2, 4):
        cb = C_brute(pts, ms, k)
        cf = C_n_from_measure(pts, ms, k // 2, G=640, pad=1.2)
        print(f"k={k}: brute = {cb:+.6f}   FFT = {cf:+.6f}   diff = {cb-cf:+.2e}")

    # k=6 brute is 12^6 = 3M tuples -> use a smaller (4-atom) measure
    K2 = 1
    th2 = np.array([0.7])
    z2, m2 = conj_sym(th2, np.array([1.0]))
    pts2, ms2 = zz_sym(z2, m2)    # 4 atoms
    print(f"\nsmall 4-atom measure for k=6 check ({len(pts2)} atoms)")
    for k in (2, 4, 6):
        cb = C_brute(pts2, ms2, k)
        cf = C_n_from_measure(pts2, ms2, k // 2, G=640, pad=1.3)
        print(f"k={k}: brute = {cb:+.6f}   FFT = {cf:+.6f}   diff = {cb-cf:+.2e}")
