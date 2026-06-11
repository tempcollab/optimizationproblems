"""
FAST diffuse-cap confirmation: min C_n over symmetric measures with per-node mass
capped at c (diffuseness constraint), small K and G, few starts. Confirms n>=2
stays >= 0 unless the cap allows near-atom collapse.
"""
import sys
import numpy as np
from scipy.optimize import minimize
from scratch.nogo_Cmu0 import C_n_from_measure, conj_sym, zz_sym

K = 16
t_half = (np.arange(K) + 0.5) / K * (np.pi / 2)
unif = 1.0 / K


def build(q):
    q = np.maximum(q, 0); q = q / q.sum()
    z, m = conj_sym(t_half, q)
    return zz_sym(z, m)


def Cfun(n, G=224):
    def f(q):
        p, m = build(q)
        return C_n_from_measure(p, m, n, G=G)
    return f


def min_capped(n, cap, ntry=4):
    f = Cfun(n)
    cons = {'type': 'eq', 'fun': lambda q: q.sum() - 1.0}
    bnds = [(0, cap)] * K
    rng = np.random.default_rng(n * 50 + int(cap * 1000))
    best = np.inf
    starts = [np.ones(K) / K]
    s = np.zeros(K); s[0] = cap; s[1] = cap; s = s / s.sum() if s.sum() > 0 else s
    starts.append(np.minimum(s, cap))
    for _ in range(ntry):
        starts.append(rng.dirichlet(np.ones(K)))
    for q0 in starts:
        q0 = np.minimum(q0, cap); q0 = q0 / q0.sum() if q0.sum() else q0
        r = minimize(f, q0, method='SLSQP', bounds=bnds, constraints=cons,
                     options={'maxiter': 120, 'ftol': 1e-9})
        best = min(best, r.fun)
    return best


print(f"K={K}, uniform per-node mass = {unif:.4f}")
print("min C_n over symmetric measures, per-node cap = c (c=uniform => max diffuse):\n")
print(f"{'cap':>7} | " + "  ".join(f"n={n}(k={2*n})" for n in (1,2,3,4)))
for cap in (unif, 2*unif, 3*unif, 0.30, 1.0):
    cap = min(cap, 1.0)
    vals = [min_capped(n, cap) for n in (1, 2, 3, 4)]
    print(f"{cap:7.3f} | " + "  ".join(f"{v:+.4f}" for v in vals))
    sys.stdout.flush()
