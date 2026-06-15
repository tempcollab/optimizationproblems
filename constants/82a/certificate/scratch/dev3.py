"""Full enumeration + admissibility + float margin sweep (moderate grid) with progress."""
import sys, itertools, time
import numpy as np
import sympy as sp
X=sp.Symbol("X")
POLY_COEFFS={"P1":[1,0],"P2":[-1,1],"P4":[1,-2,4,-3,1],
    "P8":[1,-3,7,-14,30,-58,96,-123,114,-73,31,-8,1],
    "Q1":[1,-7,30,-97,269,-679,1612,-3618,7646,-15180,28457,-50741,86189,-138288,
          206152,-279897,339335,-360911,331775,-260367,172556,-95554,43677,-16221,
          4786,-1084,178,-19,1]}
NUMERATOR_Q={"P1":26.511877484730615,"P2":23.782846008412744,"P3":0.9707094545190521,
    "P4":4.526072775020114,"P5":0.038326545650764404,"P6":4.173784226054273,"P8":1.685809173822071}
NUM_EXTRA={"P3":[1,1,-2,1],"P5":[1,-2,4,-7,13,-16,12,-5,1]}
EXTRA={"P6":[1,-3,8,-16,26,-27,17,-6,1],
    "P7":[1,-3,8,-18,36,-62,97,-123,114,-73,31,-8,1],
    "P9":[1,-4,10,-17,26,-47,119,-298,592,-878,963,-780,464,-199,59,-11,1],
    "Q2":[1,-7,30,-96,255,-586,1212,-2360,4573,-9148,18749,-37783,71770,-124910,
          195848,-273368,335981,-359545,331349,-260271,172542,-95553,43677,-16221,
          4786,-1084,178,-19,1]}
def _poly(c): return sp.Poly.from_list([sp.Integer(x) for x in c],gens=X,domain=sp.ZZ)
lib={k:_poly(v) for k,v in POLY_COEFFS.items()}
core5=(lib["P1"]**5)*(lib["P2"]**5); Q1=lib["Q1"]; coreP8=core5*lib["P8"]
def build_R_d(d_hl):
    raw=Q1 - coreP8*_poly(d_hl)
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
def ch(name):
    return POLY_COEFFS.get(name) or NUM_EXTRA.get(name) or EXTRA.get(name)

t0=time.time()
box=[]
for c3,c2,c1 in itertools.product(range(-4,5),repeat=3):
    d=[1,c3,c2,c1,1]; ok,pp=adm(d)
    if ok: box.append((d,pp))
print(f"box admissible={len(box)}/729 ({time.time()-t0:.1f}s)")

# anchor
N=400000
edges=(np.arange(N+1)/N)*2*np.pi
m=0.5*(edges[:-1]+edges[1:]); w=edges[1:]-edges[:-1]
chi=np.exp(1j*m); chi=chi*(1-chi)
LF=1e-300
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
om=Bf>Af
inv=1/(2*np.pi); deg=28
def marg(pp):
    cf=[int(c) for c in pp.all_coeffs()]
    lP=np.log(np.maximum(np.abs(fev(cf)),LF))
    return (np.sum((w*lP)[om])*inv)/deg
rP4=marg(R0)
print(f"r_R0={rP4:+.6f} (expect -0.0356); N={N}")
rows=sorted((marg(pp),d) for d,pp in box)
print("top6:",[(round(r,5),d) for r,d in rows[:6]])
print("P4 unique min?",rows[0][1]==[1,-2,4,-3,1])
gaps=[(r-rP4,d) for r,d in rows]
nm=[g for g in gaps if g[0]<3e-3 and g[0]>1e-12]
print(f"near-miss (0<gap<3e-3): {len(nm)}")
for g,d in nm: print(f"  gap={g:+.4e} d={d}")
print(f"total {time.time()-t0:.1f}s")
