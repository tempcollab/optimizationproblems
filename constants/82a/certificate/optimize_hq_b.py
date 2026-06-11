"""
Continuous multistart minimisation of Doche's RECORD-family limit-point
objective h(q) (Doc01b: base polys P1,P2,P4,P6,P8 + perturbing block Q=Q1*Q2).

Any admissible q (q in R_+^5) makes log h(q) a rigorous UPPER bound on C_82
(Doc01b Theorem via Doc01a Lemmas 2,3,4,5).  This script only PROPOSES a good
q* by float optimisation; the rigorous interval enclosure for the chosen q* is
in doche_hq_b_certify.py.

Record to beat: log h = log 1.289735 = 0.25443677  (Doche's hand-tuned q).
"""

import numpy as np
from scipy.optimize import minimize
from doche_hq_b import log_h

N_OPT = 600_000


def f(q):
    if np.any(np.asarray(q) < 0):
        return 1e9
    return log_h(q, N=N_OPT)


def run(verbose=True):
    rng = np.random.default_rng(1)
    doche = np.array([13.1, 10.6, 3.2, 1.15, 0.24])
    seeds = [doche]
    for _ in range(40):
        seeds.append(doche * np.exp(rng.normal(0, 0.4, 5)))
    for _ in range(40):
        seeds.append(rng.uniform([1, 1, 0.1, 0.1, 0.0],
                                 [30, 30, 8, 5, 3]))
    best = None
    for s0 in seeds:
        res = minimize(f, s0, method="Nelder-Mead",
                       options=dict(xatol=1e-7, fatol=1e-11,
                                    maxiter=40000, maxfev=40000))
        if best is None or res.fun < best.fun:
            best = res
            if verbose:
                print("  improved: logh=%.8f q=%s" %
                      (res.fun, np.array2string(res.x, precision=5)))
    return best


if __name__ == "__main__":
    best = run()
    q = best.x
    print("\nbest q* =", q)
    lh = log_h(q, N=16_000_000)
    print("log h(q*) [N=16e6] = %.8f" % lh)
    print("h(q*)             = %.8f" % np.exp(lh))
    rec_logh = np.log(1.289735)
    print("record   log h    = %.8f  (1.289735)" % rec_logh)
    print("margin (record - new) = %.3e" % (rec_logh - lh))
    print("beats record (float):", lh < rec_logh)
