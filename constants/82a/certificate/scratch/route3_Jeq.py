"""Confirm J(mu) = I(rho), the log-energy of the difference measure rho,
and check whether J can go negative by direct rho-energy reasoning.
Also: the cut binds only if J(mu0)~0 at the LP-relevant measure. Since the LP
optimum p0 lives on |z|=1 (NOT the diffuse mu0), the constraint the LP sees is
4 INT V_mu0 dp >= 3 J(mu0). Compute INT V_mu0 d(delta over the contour) range to
see how slack it is, AND report J(p0) of the actual sparse LP optimum (atomic ->
self-energy; use the difference distribution which is diffuse)."""
import numpy as np
from scipy.signal import fftconvolve
from scratch.route3_J_fft import (contour, column_matrix, solve_primal, hist_measure, J_from_measure)

N=2000
t,z,w,g=contour(N); A=column_matrix(w)
m0,p0=solve_primal(g,A)

# J of the actual LP optimum measure p0 (conj-symmetrized).
zf=np.concatenate([z,np.conj(z)]); 
# only support points matter
nz=np.where(p0>1e-9)[0]
zs=z[nz]; ps=p0[nz]; ps/=ps.sum()
zf2=np.concatenate([zs,np.conj(zs)]); mf2=np.concatenate([ps,ps])/2
# the difference distribution of an ATOMIC measure is atomic -> J well-defined
# (off-diagonal). Compute directly (small):
from itertools import product
M=len(zf2)
J=0.0
for a,b,c,d in product(range(M),repeat=4):
    v=zf2[a]-zf2[b]-zf2[c]+zf2[d]
    if abs(v)<1e-10: continue
    J+=mf2[a]*mf2[b]*mf2[c]*mf2[d]*np.log(abs(v))
print(f"J(p0) of the ACTUAL conj-sym LP optimum (atomic) = {J:+.6f}")
print("(>0 => even the LP optimum satisfies J>=0 with slack; cut never binds)")
