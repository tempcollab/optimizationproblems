"""
Continuous multistart minimisation of Doche's limit-point objective h(q)
over the recovered Doc01a base-polynomial family {P1,P2,P3,P4,P5} + Q1.

Any admissible q* makes log h(q*) a rigorous UPPER bound on C_82 (Doc01a
Lemmas 2,3,4,5).  This script only PROPOSES a good q* (float optimisation);
the rigorous certificate for the chosen q* is in doche_hq_certify.py.
"""

import numpy as np
from scipy.optimize import minimize
from doche_hq import log_h, DEFAULT_PS, DEFAULT_QS

# fast objective for the optimiser (cheaper N; refined later)
N_OPT = 400_000


def f(q):
    # keep exponents non-negative (admissible domain q in R_+^5)
    if np.any(np.asarray(q) < 0):
        return 1e9
    return log_h(q, N=N_OPT)


def run():
    rng = np.random.default_rng(0)
    seeds = [np.array([17.9, 12.2, 0.9, 0.35, 0.29])]  # Doche's q
    # random restarts around Doche's q and broader
    for _ in range(30):
        seeds.append(np.array([17.9, 12.2, 0.9, 0.35, 0.29]) *
                     np.exp(rng.normal(0, 0.5, 5)))
    for _ in range(30):
        seeds.append(rng.uniform([1, 1, 0, 0, 0], [40, 40, 5, 5, 5]))

    best = None
    for s0 in seeds:
        res = minimize(f, s0, method="Nelder-Mead",
                       options=dict(xatol=1e-6, fatol=1e-9, maxiter=20000,
                                    maxfev=20000))
        if res.success or True:
            if best is None or res.fun < best.fun:
                best = res
    return best


if __name__ == "__main__":
    best = run()
    q = best.x
    lh = best.fun
    print("best q* =", q)
    print("log h(q*) [N=%d] = %.8f" % (N_OPT, lh))
    print("h(q*)            = %.8f" % np.exp(lh))
    # refine value at the optimum with high N
    lh_fine = log_h(q, N=16_000_000)
    print("log h(q*) [N=16e6 refine] = %.8f" % lh_fine)
    print("h(q*)        [refine]     = %.8f" % np.exp(lh_fine))
    print("record to beat: log 1.289735 = 0.25443677")
    print("beats record (float):", lh_fine < 0.25443677)
