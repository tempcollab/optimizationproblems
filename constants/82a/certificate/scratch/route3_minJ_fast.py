"""Lean no-go: random + light descent search for negative J, with flushed output."""
import sys, numpy as np
from scipy.signal import fftconvolve
from scratch.route3_J_fft import contour, column_matrix, solve_primal, hist_measure

def J_of(pts, ms, G=288, pad=1.2):
    R=np.abs(pts).max()*pad
    M,h=hist_measure(pts,ms,-R,R,G); Mref=M[::-1,::-1].copy()
    rho=fftconvolve(M,Mref,mode='full'); rho[rho<0]=0
    P=fftconvolve(rho,rho,mode='full'); P[P<0]=0
    nP=P.shape[0]; c0=2*(G-1); idx=np.arange(nP)-c0
    IX,IY=np.meshgrid(idx,idx,indexing='ij')
    Ab=np.hypot(IX*h,IY*h)
    with np.errstate(divide='ignore'): L=np.log(Ab)
    L[~np.isfinite(L)]=0.0
    return float((P*L).sum())

def expand(q,z,sym):
    q=np.maximum(q,0); q=q/q.sum()
    if sym:
        pts=np.concatenate([z,np.conj(z),1-z,1-np.conj(z)]); ms=np.concatenate([q,q,q,q])/4
    else:
        pts=np.concatenate([z,np.conj(z)]); ms=np.concatenate([q,q])/2
    return pts,ms

rng=np.random.default_rng(0)
Nnode=40
th=(np.arange(Nnode)+0.5)/Nnode*np.pi; z=np.exp(1j*th)
for sym in (True,False):
    tag="SYMMETRIC" if sym else "asymmetric"
    best=np.inf; bestq=None
    for _ in range(600):
        a=rng.uniform(0.05,4.0)
        # also try measures concentrated near various t (sharp)
        q=rng.dirichlet(np.full(Nnode,a))
        pts,ms=expand(q,z,sym); J=J_of(pts,ms)
        if J<best: best=J; bestq=q
    # also single-point-ish and two-cluster measures (extremes)
    for _ in range(200):
        k=rng.integers(1,5); idx=rng.choice(Nnode,k,replace=False)
        q=np.full(Nnode,1e-6); q[idx]=rng.uniform(0.1,1,k); 
        pts,ms=expand(q,z,sym); J=J_of(pts,ms)
        if J<best: best=J; bestq=q
    print(f"{tag}: min J over ~800 measures = {best:+.5f}", flush=True)
    # light local descent from the best
    q=bestq.copy(); cur=best
    for it in range(25):
        eps=2e-3; grad=np.zeros(Nnode)
        cols=rng.choice(Nnode,8,replace=False)
        for c in cols:
            qp=q.copy(); qp[c]+=eps; pts,ms=expand(qp,z,sym); grad[c]=(J_of(pts,ms)-cur)/eps
        q=np.maximum(q-0.4*grad,1e-9); q/=q.sum()
        pts,ms=expand(q,z,sym); cur=J_of(pts,ms)
    print(f"{tag}: after descent min J = {cur:+.5f}", flush=True)
print("\nIf min J stays > 0 => J>=0 globally inert; the 4-point cut NEVER binds.", flush=True)
