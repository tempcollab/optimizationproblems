"""Sanity: confirm the cut row machinery CAN produce lambda0>0 (so the 'always slack'
result is real, not a sign bug). We DELIBERATELY force the LP optimum into a region
where J<0 by using as the SOLE feasible measures a tiny set of concentrated atoms
(no Flammang columns), then add the tangent cut at a mu0 with J(mu0)~0. If the cut
binds there, the machinery is correct and the 'slack' for Flammang is genuine."""
import numpy as np
from scipy.optimize import linprog
from scratch.route3_cut_lowJ import (expand_sym, J_grids, J_value, S3_dist, V_pot,
                                     descend_lowJ, zN, thN, Nnode)
from scratch.route3_J_fft import contour

# Build a contour LP with NO column constraints, objective that pulls mass to a
# concentrated cluster (low-J region). g_n = -indicator(near t0) so the optimum
# concentrates -> J<0. Then add the J-cut.
N=2000
t=np.linspace(1e-4,np.pi-1e-4,N); z=np.exp(1j*t)
# objective: prefer a narrow cluster near t=0.5
g = (np.abs(t-0.5)>0.05).astype(float)   # 0 inside cluster, 1 outside -> mass goes inside
A = np.zeros((N,1))  # dummy non-binding column (all zeros -> 0>=0 ok)

# reference mu0 ~ near-zero J
q,J0d = descend_lowJ(seed=2, steps=15)
pts,ms=expand_sym(q); _,hJ,P,c0J,_=J_grids(pts,ms,G=288); J0=J_value(P,hJ,c0J)
P3,h3,c03=S3_dist(pts,ms,G=288)
Vz=V_pot(z,P3,h3,c03)
cut_row=4.0*Vz; rhs=3.0*J0

def solve(g,A,cr,rhs):
    Nn=len(g);J=A.shape[1]
    Aub=np.vstack([-A.T,-cr[None,:]]); bub=np.concatenate([np.zeros(J),[-rhs]])
    res=linprog(g,A_ub=Aub,b_ub=bub,A_eq=np.ones((1,Nn)),b_eq=[1.0],bounds=[(0,None)]*Nn,method="highs")
    lam=max(-res.ineqlin.marginals[-1],0.0)
    return res.fun,res.x,lam

# without cut
m_no,p_no,_=solve(g,A,np.zeros(N),-1e9)
# with cut
m_c,p_c,lam=solve(g,A,cut_row,rhs)
print(f"reference J(mu0)={J0:+.4f}")
print(f"no-cut optimum value   = {m_no:.5f}")
print(f"with-cut optimum value = {m_c:.5f}   lambda0={lam:.5f}  cut {'ACTIVE' if lam>1e-7 else 'slack'}")
print("(If ACTIVE here, the cut machinery is correct => the Flammang 'slack' is genuine.)")
