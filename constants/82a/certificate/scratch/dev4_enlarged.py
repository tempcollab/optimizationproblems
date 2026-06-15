"""MF1 enlarged-box diagnostic: |ci|<=6. Confirm no admissible d OUTSIDE |ci|<=4
comes within 1e-3 of P4's margin (boundary inactive)."""
import itertools, time
import numpy as np
import sympy as sp
X=sp.Symbol("X")
exec(open("dev3.py").read().split("t0=time.time()")[0])  # reuse defs up to enumeration
core5=(lib["P1"]**5)*(lib["P2"]**5); coreP8=core5*lib["P8"]; Q1=lib["Q1"]
def build_R_d(d_hl):
    raw=Q1-coreP8*_poly(d_hl)
    cont,pp=sp.Poly(raw.as_expr(),X,domain=sp.ZZ).primitive()
    if pp.LC()<0: pp=sp.Poly(-pp.as_expr(),X,domain=sp.ZZ)
    return abs(int(cont)),pp
def adm(d_hl):
    cont,pp=build_R_d(d_hl)
    if int(pp.degree())!=28 or cont!=1: return False,pp
    if sp.gcd(pp,Q1).degree()!=0: return False,pp
    if sp.gcd(pp,pp.diff(X)).degree()!=0: return False,pp
    if not(pp.eval(0)==1 and pp.eval(1)==1): return False,pp
    return True,pp
def ch(name): return POLY_COEFFS.get(name) or NUM_EXTRA.get(name) or EXTRA.get(name)
N=400000
edges=(np.arange(N+1)/N)*2*np.pi
m=0.5*(edges[:-1]+edges[1:]); w=edges[1:]-edges[:-1]
chi=np.exp(1j*m); chi=chi*(1-chi); LF=1e-300
def fev(cf):
    c=np.array([complex(int(x)) for x in cf],dtype=np.complex128)
    v=np.zeros_like(chi)+c[0]
    for x in c[1:]: v=v*chi+x
    return v
ok,R0=adm([1,-2,4,-3,1])
P7=_poly(EXTRA["P7"]); Q2=_poly(EXTRA["Q2"])
rawR2=Q2+core5*lib["P4"]*P7
_,R2p=sp.Poly(rawR2.as_expr(),X,domain=sp.ZZ).primitive()
if R2p.LC()<0: R2p=sp.Poly(-R2p.as_expr(),X,domain=sp.ZZ)
Af=np.zeros_like(m)
for nm,q in NUMERATOR_Q.items(): Af+=q*np.log(np.maximum(np.abs(fev(ch(nm))),LF))
Bf=np.zeros_like(m)
for blk in ["Q2","R0","R2","P7","P9"]:
    if blk=="R0": cf=[int(c) for c in R0.all_coeffs()]
    elif blk=="R2": cf=[int(c) for c in R2p.all_coeffs()]
    else: cf=ch(blk)
    Bf+=np.log(np.maximum(np.abs(fev(cf)),LF))
om=Bf>Af; inv=1/(2*np.pi); deg=28
def marg(pp):
    cf=[int(c) for c in pp.all_coeffs()]
    return (np.sum((w*np.log(np.maximum(np.abs(fev(cf)),LF)))[om])*inv)/deg
rP4=marg(R0)
t0=time.time()
worst=None; n_out_adm=0; near=[]
for c3,c2,c1 in itertools.product(range(-6,7),repeat=3):
    if abs(c3)<=4 and abs(c2)<=4 and abs(c1)<=4: continue  # only OUTSIDE the |ci|<=4 box
    d=[1,c3,c2,c1,1]; ok,pp=adm(d)
    if not ok: continue
    n_out_adm+=1
    g=marg(pp)-rP4
    if g<1e-3: near.append((g,d))
    if worst is None or g<worst[0]: worst=(g,d)
print(f"enlarged box |ci|<=6, OUTSIDE |ci|<=4: admissible competitors={n_out_adm} ({time.time()-t0:.1f}s)")
print(f"smallest gap to P4 among them: {worst[0]:+.4e} at d={worst[1]}")
print(f"competitors within 1e-3 of P4 OUTSIDE |ci|<=4: {len(near)}  (MF1 wants this EMPTY)")
for g,d in near: print("  ",g,d)
