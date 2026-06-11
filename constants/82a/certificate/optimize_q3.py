"""
R7 multistart minimisation of log h(q, qB) over the 6-exponent ENLARGED family
(Doc01b base P1,P2,P4,P6,P8 + fixed Q1*Q2 + free-exponent Q3=Qa).  Seeded at the
held R6 point with qB=0 so the optimum can only go DOWN or stay equal.

Held value to beat: certified 0.2543309112 (R6); held R6 float = 0.2543308006.
The max(A,B) certificate adds ~1.1e-7 slack, so a candidate is only worth
certifying if its FLOAT clearly beats 0.2543308006 by more than ~1.1e-7.
"""

import numpy as np
from scipy.optimize import minimize
from doche_hq_q3 import log_h

N_SEARCH = 100_000
N_SCORE = 16_000_000

R6_Q = np.array([11.73584, 8.77354, 2.44938, 1.55411, 0.53442])
HELD_FLOAT = 0.2543308006


def make_f(N):
    def f(x):
        q = x[:5]
        qB = x[5]
        if np.any(q < 0) or qB < 0:
            return 1e9
        return log_h(q, qB=qB, N=N)
    return f


def run(verbose=True):
    rng = np.random.default_rng(7)
    fsearch = make_f(N_SEARCH)
    base = np.concatenate([R6_Q, [0.0]])          # anchor seed: qB=0
    seeds = [base]
    # seeds turning qB ON at various small positive values (q frozen at R6)
    for qB0 in [0.05, 0.1, 0.2, 0.4, 0.8, 1.5]:
        seeds.append(np.concatenate([R6_Q, [qB0]]))
    # jitter around (R6, qB=small)
    for _ in range(20):
        jq = R6_Q * np.exp(rng.normal(0, 0.08, 5))
        qB0 = abs(rng.normal(0, 0.4))
        seeds.append(np.concatenate([jq, [qB0]]))
    for _ in range(20):
        jq = R6_Q * np.exp(rng.normal(0, 0.25, 5))
        qB0 = abs(rng.normal(0, 0.8))
        seeds.append(np.concatenate([jq, [qB0]]))
    best = None
    for i, s0 in enumerate(seeds):
        res = minimize(fsearch, s0, method="Nelder-Mead",
                       options=dict(xatol=1e-6, fatol=1e-11,
                                    maxiter=3000, maxfev=3000))
        if best is None or res.fun < best.fun:
            best = res
            if verbose:
                print("  improved[seed %d]: logh(N=%d)=%.10f  qB=%.5f  q=%s"
                      % (i, N_SEARCH, res.fun, res.x[5],
                         np.array2string(res.x[:5], precision=5)), flush=True)
    return best


if __name__ == "__main__":
    best = run()
    x = best.x
    q, qB = x[:5], x[5]
    print("\nbest (search)  q =", np.array2string(q, precision=6), " qB =", qB)
    lh = log_h(q, qB=qB, N=N_SCORE)
    print("log h [N=%d] = %.10f" % (N_SCORE, lh))
    print("held R6 float          = %.10f" % HELD_FLOAT)
    print("held R6 certified      = 0.2543309112")
    print("float beats held float :", lh < HELD_FLOAT,
          " (delta = %.3e)" % (HELD_FLOAT - lh))
    # Also report the value at the pure anchor for sanity.
    print("anchor qB=0 score     = %.10f" % log_h(R6_Q, qB=0.0, N=N_SCORE))
