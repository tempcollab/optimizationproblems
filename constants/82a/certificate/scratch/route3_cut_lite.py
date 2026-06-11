"""Lite correct-V cut LP: small reference K and modest N, exact V via S3 atoms.
Confirms (with corrected potential, INT V dmu0 == J0 self-check) whether the cut
binds on the Flammang primal. Decisive number already known: J(p0)=+0.36>0."""
import numpy as np
from scipy.optimize import linprog
from flammang_table1 import get_table
from scratch.route3_J_fft import contour, column_matrix, solve_primal
ANCHOR=0.2487458

def J_atomic(pts,ms):
    D=(pts[:,None]-pts[None,:]).ravel(); W=(ms[:,None]*ms[None,:]).ravel()
    SS=D[:,None]+D[None,:]
    with np.errstate(divide='ignore'): L=np.log(np.abs(SS))
    L[~np.isfinite(L)]=0.0
    return float(W@L@W)

def V_atomic(y,pts,ms):
    B,C,Dd=np.meshgrid(pts,pts,pts,indexing='ij'); S3=(B+C-Dd).ravel()
    MB,MC,MD=np.meshgrid(ms,ms,ms,indexing='ij'); PS=(MB*MC*MD).ravel()
    out=np.empty(len(y))
    for i in range(0,len(y),50):
        yc=y[i:i+50]; d=np.abs(yc[:,None]-S3[None,:])
        with np.errstate(divide='ignore'): L=np.log(d)
        L[~np.isfinite(L)]=0.0; out[i:i+50]=L@PS
    return out

def ref(kind,K=24):
    th=(np.arange(K)+0.5)/K*np.pi; z=np.exp(1j*th)
    q=np.ones(K) if kind=='diffuse' else (np.abs(th-th[K//2])<0.2).astype(float)
    q/=q.sum()
    pts=np.concatenate([z,np.conj(z),1-z,1-np.conj(z)]); ms=np.concatenate([q]*4)/4
    return pts,ms

N=800
t,z,w,g=contour(N); A=column_matrix(w); m0,p0=solve_primal(g,A)
print(f"m0={m0:.7f}")
images=np.concatenate([z,np.conj(z),1-z,1-np.conj(z)])
for kind in ('diffuse','lowJ'):
    pts0,ms0=ref(kind,K=22); J0=J_atomic(pts0,ms0)
    # self-check INT V dmu0 == J0
    Vsupp=V_atomic(pts0,pts0,ms0); ivchk=float(ms0@Vsupp)
    Vimg=V_atomic(images,pts0,ms0); Vw=Vimg.reshape(4,N).mean(axis=0)
    cut=4.0*Vw; rhs=3.0*J0
    Aub=np.vstack([-A.T,-cut[None,:]]); bub=np.concatenate([np.zeros(A.shape[1]),[-rhs]])
    res=linprog(g,A_ub=Aub,b_ub=bub,A_eq=np.ones((1,N)),b_eq=[1.0],bounds=[(0,None)]*N,method="highs")
    lam=max(-res.ineqlin.marginals[-1],0.0); lhs=float(cut@p0)
    print(f"[{kind}] J0={J0:+.4f} (INT V dmu0 chk={ivchk:+.4f}) | cut.p0={lhs:+.4f} rhs={rhs:+.4f} "
          f"slack={lhs-rhs:+.4f} | m_cut={res.fun:.7f} lam={lam:.5f} {'ACTIVE' if lam>1e-7 else 'SLACK'}")
