"""Definitive: J of the no-energy LP optimum p0 (conj-symmetrized), high-precision
brute force on its support; plus J of p0 z->1-z symmetrized. If J(p0)>0 the no-energy
optimum is INTERIOR to {J>=0} and NO tangent cut can separate it -> Route 3 cannot
raise the bound, period."""
import numpy as np
from itertools import product
from scratch.route3_J_fft import contour, column_matrix, solve_primal

N=3000
t,z,w,g=contour(N); A=column_matrix(w)
m0,p0=solve_primal(g,A)
nz=np.where(p0>1e-10)[0]
zs=z[nz]; ps=p0[nz]; ps/=ps.sum()
print(f"m0={m0:.7f}  support={len(nz)}")

def Jbrute(pts,ms,tol=1e-10):
    M=len(pts); J=0.0
    for a,b,c,d in product(range(M),repeat=4):
        v=pts[a]-pts[b]-pts[c]+pts[d]
        if abs(v)<tol: continue
        J+=ms[a]*ms[b]*ms[c]*ms[d]*np.log(abs(v))
    return J

# (i) conj-symmetric p0
zf=np.concatenate([zs,np.conj(zs)]); mf=np.concatenate([ps,ps])/2
Ji=Jbrute(zf,mf)
print(f"J(p0) conj-sym               = {Ji:+.6f}")
# (ii) z->1-z symmetrized p0
zf2=np.concatenate([zf,1-zf]); mf2=np.concatenate([mf,mf])/2
Jii=Jbrute(zf2,mf2)
print(f"J(p0) z->1-z symmetrized     = {Jii:+.6f}")
print()
print("J(p0) > 0  =>  no-energy optimum is FEASIBLE for J>=0 (interior, slack);")
print("a tangent cut can only separate a point with J<0 => cut cannot bind => no raise.")
