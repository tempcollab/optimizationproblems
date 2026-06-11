"""
Conclusive cut-machinery sanity check, v3 — CORRECT linearization.

The directional derivative of J at mu0 in direction (p - mu0), with the FULL
expansion E(p) = (1/4)[p o conj o zz-images], is
   dJ = 4 INT V_mu0(y) dE(p)(y),  V_mu0(y)=INT^3 log|y-x2-x3+x4| dmu0^3.
So the cut functional must integrate V_mu0 against the EXPANDED measure E(p), i.e.
the per-node cut weight is the AVERAGE of V_mu0 over that node's 4 images
{z, conj z, 1-z, 1-conj z}. (The v2 check used only V_mu0(z) -> wrong weight.)

With the correct weight, verify the tangent cut: J(mu) <= L(mu)=4 INT V_mu0 dE(mu) - 3 J(mu0),
so for the tangent to be tight at mu0: L(mu0)=4 J(mu0)-3J(mu0)=J(mu0). Check that.
Then confirm the cut BINDS when the optimum wants J<J(mu0).
"""
import numpy as np
from scipy.optimize import linprog
from scratch.route3_cut_lowJ import (expand_sym, J_grids, J_value, S3_dist, V_pot, zN, Nnode)


def cut_weights(q_ref, G=288):
    """Per-node cut weight w_n = avg of V_mu0 over node n's 4 images."""
    pts0, ms0 = expand_sym(q_ref)
    P3, h3, c03 = S3_dist(pts0, ms0, G=G)
    images = np.concatenate([zN, np.conj(zN), 1 - zN, 1 - np.conj(zN)])
    V = V_pot(images, P3, h3, c03)
    Vw = V.reshape(4, Nnode).mean(axis=0)     # average over the 4 images
    return Vw


def Jq(q, G=288):
    pts, ms = expand_sym(q); _, h, P, c0, _ = J_grids(pts, ms, G=G); return J_value(P, h, c0)


q_diff = np.ones(Nnode) / Nnode
q_clus = np.zeros(Nnode); q_clus[3:8] = 1.0; q_clus /= q_clus.sum()

# reference with J~0
los, his = 0.0, 1.0
for _ in range(25):
    mid = 0.5 * (los + his); qm = (1 - mid) * q_diff + mid * q_clus
    if Jq(qm) > 0: los = mid
    else: his = mid
q0 = (1 - mid) * q_diff + mid * q_clus
J0 = Jq(q0)

Vw = cut_weights(q0)
# tangent tightness at mu0: 4*Vw.q0 - 3*J0 should equal J0
L_mu0 = 4.0 * (Vw @ q0) - 3.0 * J0
print(f"J(mu0)={J0:+.5f}   tangent L(mu0)=4<V,mu0>-3J0={L_mu0:+.5f}  (should ~ J0)")
print(f"   <V_mu0, mu0> = {Vw @ q0:+.5f}  (should ~ J0)")

# objective pulls toward the cluster (J<0). The cut row: 4 Vw . p >= 3 J0.
g = np.ones(Nnode); g[3:8] = 0.0
cut_row = 4.0 * Vw; rhs = 3.0 * J0

def solve(g, cr, rhs):
    res = linprog(g, A_ub=-cr[None, :], b_ub=np.array([-rhs]),
                  A_eq=np.ones((1, Nnode)), b_eq=[1.0], bounds=[(0, None)] * Nnode, method="highs")
    return res.fun, res.x, max(-res.ineqlin.marginals[-1], 0.0)

m_no, p_no, _ = solve(g, np.zeros(Nnode), -1e9)
m_c, p_c, lam = solve(g, cut_row, rhs)
print(f"unconstrained opt: J={Jq(p_no/p_no.sum()):+.4f}")
print(f"with correct J-cut: value={m_c:.4f}  lambda0={lam:.5f}  J(opt)={Jq(p_c/p_c.sum()):+.4f}  "
      f"{'CUT ACTIVE (machinery OK)' if lam>1e-7 else 'slack'}")
