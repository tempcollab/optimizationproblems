"""
Conclusive cut-machinery sanity check.

We must confirm the tangent-cut code CAN produce lambda0>0, otherwise 'always slack'
could be a sign bug. Set up a CONTROLLED LP whose UNCONSTRAINED optimum has J<0, with
a reference mu0 ON the boundary (J(mu0)~0). Then the cut 4 INT V_mu0 dp >= 3 J(mu0)~0
must be VIOLATED by the optimum and bind.

Construction: variable p over a small node set on the contour (conj+zz expanded
internally via the SAME J machinery). Objective g pulls toward a concentrated cluster
=> unconstrained optimum is a near-atom with J<0 (negative log-energy of its diffuse
difference measure). Reference mu0 = a measure with J~0 (interpolate between the
diffuse near-equilibrium [J>0] and the cluster [J<0] to hit J~0). Build tangent there.
"""
import numpy as np
from scipy.optimize import linprog
from scratch.route3_cut_lowJ import (expand_sym, J_grids, J_value, S3_dist, V_pot, zN, Nnode)

# node objective: reward concentration near node index 5 (cluster) strongly.
g = np.ones(Nnode)
g[3:8] = 0.0                      # cheap to put mass in the cluster band

# helper: J of a q
def Jq(q, G=288):
    pts, ms = expand_sym(q); _, h, P, c0, _ = J_grids(pts, ms, G=G); return J_value(P, h, c0)

# diffuse measure (J>0) and cluster measure (J<0)
q_diff = np.ones(Nnode) / Nnode
q_clus = np.zeros(Nnode); q_clus[3:8] = 1.0; q_clus /= q_clus.sum()
Jd, Jc = Jq(q_diff), Jq(q_clus)
print(f"J(diffuse)={Jd:+.4f}  J(cluster)={Jc:+.4f}")

# find lambda mixing with J~0
los, his = 0.0, 1.0
for _ in range(25):
    mid = 0.5*(los+his)
    qm = (1-mid)*q_diff + mid*q_clus
    if Jq(qm) > 0: los = mid
    else: his = mid
q0 = (1-mid)*q_diff + mid*q_clus
J0 = Jq(q0)
print(f"reference mu0 mix={mid:.3f}  J(mu0)={J0:+.5f}  (target ~0)")

# tangent cut at mu0, evaluated at the contour nodes zN (half-arc representatives)
pts0, ms0 = expand_sym(q0)
P3, h3, c03 = S3_dist(pts0, ms0, G=288)
V = V_pot(zN, P3, h3, c03)         # potential at the Nnode contour reps
cut_row = 4.0*V
rhs = 3.0*J0

def solve(g, cr, rhs):
    Aub = -cr[None, :]; bub = np.array([-rhs])
    res = linprog(g, A_ub=Aub, b_ub=bub, A_eq=np.ones((1, Nnode)), b_eq=[1.0],
                  bounds=[(0, None)]*Nnode, method="highs")
    lam = max(-res.ineqlin.marginals[-1], 0.0)
    return res.fun, res.x, lam

m_no, p_no, _ = solve(g, np.zeros(Nnode), -1e9)
m_c, p_c, lam = solve(g, cut_row, rhs)
print(f"unconstrained optimum: value={m_no:.5f}  J(opt)={Jq(p_no/p_no.sum()):+.4f}")
print(f"with J-cut:            value={m_c:.5f}  lambda0={lam:.5f}  J(opt)={Jq(p_c/p_c.sum()):+.4f}")
print(f"cut {'ACTIVE (machinery correct)' if lam>1e-7 else 'still slack (investigate)'}")
