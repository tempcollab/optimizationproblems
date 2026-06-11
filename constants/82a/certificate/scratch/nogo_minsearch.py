"""
NO-GO / counterexample search — adversarially MINIMIZE C_n(mu) over z->1-z symmetric
reference measures, for each n=1,2,3,4 (k=2,4,6,8).

C_n is a quadratic-ish-in-mass functional but the convolution structure makes it a
degree-(2n) form in the node masses q (mu = sum_a q_a delta at node a's z->1-z &
conj orbit). We search for the MOST NEGATIVE C_n attainable:

  min over q >= 0, sum q = 1  of  C_n(mu(q)),  mu z->1-z & conj symmetric.

Strategy:
  - Build a node set on t in (0,pi/2] (half-arc); the z->1-z + conj symmetrization
    is applied so the measure is automatically valid-symmetric for ANY q.
  - C_n(mu) via the FFT routine (depends on q through the histogram).
  - Minimize with scipy (SLSQP / differential_evolution) over the simplex.
  - Also try many RANDOM symmetric measures (multi-start) to catch non-convex dips.

The decisive question: can ANY n>=2 case reach C_n < 0 (let alone < -threshold so a
cut raises the LP by >2e-4)? If the minimum stays >= 0 (with margin) for n>=2, the
whole hierarchy above the 2-point energy is interior-inert.

For n=1 we expect the known result: symmetric 2-point energy floors near 0 (tiny).
"""
import numpy as np
from scipy.signal import fftconvolve
from scipy.optimize import minimize, differential_evolution
from scratch.nogo_Cmu0 import C_n_from_measure, conj_sym, zz_sym


def build_symmetric(q, t_half):
    """Given masses q on half-arc nodes t_half in (0,pi/2], build the conj + z->1-z
    symmetric measure (mass spread to the 4-image orbit)."""
    q = np.maximum(q, 0)
    s = q.sum()
    if s <= 0:
        q = np.ones_like(q); s = q.sum()
    q = q / s
    z, m = conj_sym(t_half, q)
    return zz_sym(z, m)


def make_Cfun(n, t_half, G=320):
    def f(q):
        pts, ms = build_symmetric(q, t_half)
        return C_n_from_measure(pts, ms, n, G=G)
    return f


if __name__ == "__main__":
    np.random.seed(0)
    # half-arc nodes (t in (0, pi/2]); symmetrization fills the rest of the circle
    K = 18
    t_half = (np.arange(K) + 0.5) / K * (np.pi / 2)

    for n in (1, 2, 3, 4):
        f = make_Cfun(n, t_half, G=320)
        # multi-start random search over the simplex
        best = np.inf; best_q = None
        # include structured starts: uniform, single-node spikes, pairs
        starts = [np.ones(K)]
        for i in range(K):
            e = np.zeros(K); e[i] = 1.0; starts.append(e)
        for _ in range(40):
            starts.append(np.random.dirichlet(np.ones(K) * 0.3))
        for _ in range(40):
            starts.append(np.random.dirichlet(np.ones(K) * 3.0))
        for q0 in starts:
            v = f(q0)
            if v < best:
                best = v; best_q = q0.copy()
        # local polish from the best random start
        cons = {'type': 'eq', 'fun': lambda q: q.sum() - 1.0}
        bnds = [(0, 1)] * K
        res = minimize(f, best_q / best_q.sum(), method='SLSQP', bounds=bnds,
                       constraints=cons, options={'maxiter': 200, 'ftol': 1e-9})
        polished = res.fun
        final = min(best, polished)
        # which start gave the min
        active = np.where(best_q / best_q.sum() > 0.05)[0]
        print(f"n={n} (k={2*n}): min C_n over z->1-z SYM measures = {final:+.5f}  "
              f"(random-best {best:+.5f}, SLSQP {polished:+.5f})  "
              f"active half-nodes {list(active)}")
