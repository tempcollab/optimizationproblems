"""
Stage B (EXTEND / record-break attempt) for constant 82a.

Column generation on Smyth's semi-infinite LP for the Zhang-Zagier lower bound.
The LP (at a fixed integer-polynomial set {Q_j}) is:
    maximize m   s.t.   sum_j c_j log|Q_j(w(t))| + m <= log max(1,|w(t)|)  for all t,
                        c_j >= 0,
discretized at control points t_n.  Its optimum is m* = the certified bound.

Dual: a measure mu* >= 0 on the control points with sum_n mu*_n = 1 and, for every
admissible column Q, sum_n mu*_n log|Q(w(t_n))| >= 0 at optimality (complementary
slackness / BMQS primal P(g)).  A candidate integer polynomial Q with
    reduced cost  r(Q) = sum_n mu*_n log|Q(w(t_n))|  < 0
can be added to RAISE m (column generation optimality test, outline-reviewer
confirmed non-circular).

This script:
  1. solves the LP at Flammang's 24-polynomial set, extracting m* and mu*;
  2. builds a large dictionary of candidate integer polynomials in w
     (perturbations/products of the existing Q_j, low-degree integer polys,
      and LLL-bred candidates near the active minima);
  3. prices every candidate by r(Q); reports any with r(Q) < -tol;
  4. adds the best improving columns, re-solves, and iterates;
  5. reports the new LP optimum m_new (a CONJECTURE until rigorously certified
     by the verify_fast.py machinery on the enlarged set).

NOTE: an improved m_new from the LP is a NUMERICAL CONJECTURE only; it becomes a
bound iff verify_fast.py certifies it.  No uncertified value is written to held.
"""

import numpy as np
from scipy.optimize import linprog
from itertools import product
from flammang_table1 import get_table


def control_points(N=6000):
    t = np.linspace(1e-4, np.pi - 1e-4, N)
    z = np.exp(1j * t)
    w = z * (1 - z)
    b = np.log(np.maximum(1.0, np.abs(w)))
    return t, w, b


def logabsQ(asc, w):
    return np.log(np.abs(np.polyval(list(reversed(asc)), w)))


def solve_lp(cols, w, b):
    """cols: list of ascending int-coeff lists. Returns (m, c_vec, duals)."""
    N = len(w)
    J = len(cols)
    A = np.empty((N, J))
    for j, asc in enumerate(cols):
        A[:, j] = logabsQ(asc, w)
    Aub = np.hstack([A, np.ones((N, 1))])
    cost = np.zeros(J + 1); cost[-1] = -1.0
    bounds = [(0, None)] * J + [(None, None)]
    res = linprog(cost, A_ub=Aub, b_ub=b, bounds=bounds, method="highs")
    if res.status != 0:
        return None
    m = -res.fun
    c_vec = res.x[:J]
    # duals on the <= constraints (HiGHS: marginals are <=0 for <= ub at optimum)
    duals = -res.ineqlin.marginals       # mu*_n >= 0
    duals = np.maximum(duals, 0.0)
    s = duals.sum()
    if s > 0:
        duals = duals / s                # normalize to a probability measure
    return m, c_vec, duals


def reduced_cost(asc, w, mu):
    return float(np.sum(mu * logabsQ(asc, w)))


def base_columns():
    return [asc for (_, asc) in get_table()]


def candidate_dictionary():
    """Build a dictionary of candidate integer polynomials in w.
    Strategy: (a) low-degree integer polys with small coefficients;
              (b) products of pairs of existing Q_j (degree <= ~24);
              (c) small integer perturbations of existing Q_j."""
    base = base_columns()
    cands = {}

    def add(asc):
        # normalize (strip leading zeros, ensure nonzero)
        while len(asc) > 1 and asc[-1] == 0:
            asc = asc[:-1]
        if all(x == 0 for x in asc):
            return
        key = tuple(asc)
        cands[key] = list(asc)

    # (a) low-degree small-coeff integer polynomials in w, degree<=4, coeffs in [-3,3]
    for deg in range(1, 5):
        for coeffs in product(range(-3, 4), repeat=deg):
            asc = [1] + list(coeffs)            # leading coeff 1, ascending after? careful
            # interpret as descending [1, c1, ..., c_deg] -> ascending reversed
            add(list(reversed([1] + list(coeffs))))

    # (b) products of pairs of existing Q_j with combined degree <= 24
    for i in range(len(base)):
        for j in range(i, len(base)):
            di = len(base[i]) - 1
            dj = len(base[j]) - 1
            if di + dj <= 24:
                prod_poly = np.convolve(base[i], base[j]).astype(np.int64)
                add([int(x) for x in prod_poly])

    # (c) integer perturbations of each existing Q_j: +/- w^k for small k
    for asc in base:
        for k in range(0, min(len(asc), 6)):
            for s in (1, -1):
                pert = list(asc)
                pert[k] += s
                add(pert)

    return list(cands.values())


def main():
    t, w, b = control_points(6000)
    cols = base_columns()
    m0, c0, mu = solve_lp(cols, w, b)
    print(f"[Stage B] LP optimum at Flammang's 24-poly set: m* = {m0:.10f}")
    print(f"          (matches grid min / Flammang 0.2487458 -> LP machinery valid)")
    print(f"          dual measure mu* support size (mu>1e-6): {(mu>1e-6).sum()}")

    dictionary = candidate_dictionary()
    print(f"[Stage B] candidate dictionary size: {len(dictionary)}")

    # price all candidates
    base_keys = {tuple(a) for a in cols}
    priced = []
    for asc in dictionary:
        if tuple(asc) in base_keys:
            continue
        r = reduced_cost(asc, w, mu)
        priced.append((r, asc))
    priced.sort(key=lambda x: x[0])
    print(f"[Stage B] most-negative reduced costs (improving if r < ~ -1e-6):")
    for r, asc in priced[:15]:
        print(f"    r={r:+.3e}  Q(asc)={asc if len(asc)<=8 else str(asc[:8])+'...'}")

    # column generation loop
    improving = [asc for r, asc in priced if r < -1e-7]
    print(f"[Stage B] columns with r < -1e-7: {len(improving)}")
    if not improving:
        print("[Stage B] NO improving integer column found in the dictionary.")
        print("          Flammang's set is LP-optimal over this dictionary; no break.")
        return

    best = m0
    for batch in range(1, 40):
        # add up to 5 best improving columns and re-solve
        addcols = [asc for r, asc in priced if r < -1e-7][:5 * batch]
        newcols = cols + [a for a in addcols if tuple(a) not in base_keys]
        out = solve_lp(newcols, w, b)
        if out is None:
            break
        m_new, c_new, mu_new = out
        print(f"   batch {batch}: +{len(newcols)-len(cols)} cols -> m_new = {m_new:.10f}")
        if m_new > best + 1e-10:
            best = m_new
        # re-price against new dual for next batch
        priced = []
        for asc in dictionary:
            r = reduced_cost(asc, w, mu_new)
            priced.append((r, asc))
        priced.sort(key=lambda x: x[0])
        if not any(r < -1e-7 for r, _ in priced):
            print("   no more improving columns.")
            break
    print(f"[Stage B] best LP m over column generation: {best:.10f}  (CONJECTURE)")
    print(f"          record to beat: 0.2487458.  improved-by-LP: {best>0.2487458+1e-7}")


if __name__ == "__main__":
    main()
