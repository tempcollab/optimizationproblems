"""
FAST multistart minimisation of Doche's RECORD-family limit-point objective
log h(q) over the SAME Doc01b family (base P1,P2,P4,P6,P8 + perturbing block
Q = Q1*Q2, D = max(sum q_i deg P_i, 56)).  IDENTICAL objective to
optimize_hq_b.py (imports doche_hq_b.log_h); only the search budget differs:
the float midpoint Riemann sum uses a modest N during the search and a large N
to score the single best candidate.  This proposes a q* only -- the rigorous
upper bound for the chosen q* is verify_upper.py::certify_maxAB.

Record q* to beat (R5, reviewer-verified rigorous): log h(q*) = 0.2543326887
at q* = (11.74, 8.77, 2.45, 1.55, 0.53).  Its float value (N=16e6) = 0.2543325796.
A new candidate is only worth certifying if its float value is comfortably below
0.2543325796 (the certificate adds ~1.1e-7 of outward-rounding slack).
"""

import numpy as np
from scipy.optimize import minimize
from doche_hq_b import log_h

N_SEARCH = 100_000     # search budget (fast)
N_SCORE = 16_000_000   # final high-accuracy score for the chosen q


def make_f(N):
    def f(q):
        if np.any(np.asarray(q) < 0):
            return 1e9
        return log_h(q, N=N)
    return f


def run(verbose=True):
    rng = np.random.default_rng(7)
    fsearch = make_f(N_SEARCH)
    doche = np.array([13.1, 10.6, 3.2, 1.15, 0.24])
    qstar = np.array([11.74, 8.77, 2.45, 1.55, 0.53])
    seeds = [qstar, doche]
    # tight jitter around the current record q* (local polish)
    for _ in range(18):
        seeds.append(qstar * np.exp(rng.normal(0, 0.08, 5)))
    # medium jitter around q* and doche (basin hopping)
    for _ in range(18):
        seeds.append(qstar * np.exp(rng.normal(0, 0.30, 5)))
    for _ in range(10):
        seeds.append(doche * np.exp(rng.normal(0, 0.30, 5)))
    best = None
    for i, s0 in enumerate(seeds):
        res = minimize(fsearch, s0, method="Nelder-Mead",
                       options=dict(xatol=1e-6, fatol=1e-11,
                                    maxiter=2000, maxfev=2000))
        if best is None or res.fun < best.fun:
            best = res
            if verbose:
                print("  improved[seed %d]: logh(N=%d)=%.10f q=%s" %
                      (i, N_SEARCH, res.fun,
                       np.array2string(res.x, precision=5)), flush=True)
    return best


if __name__ == "__main__":
    best = run()
    q = best.x
    print("\nbest q* (search) =", np.array2string(q, precision=6))
    lh = log_h(q, N=N_SCORE)
    print("log h(q*) [N=%d] = %.10f" % (N_SCORE, lh))
    print("h(q*)             = %.10f" % np.exp(lh))
    print("record float       = 0.2543325796  (q*=(11.74,8.77,2.45,1.55,0.53))")
    print("record certified   = 0.2543326887  (R5)")
    print("float beats record float :", lh < 0.2543325796)
