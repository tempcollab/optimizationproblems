"""Time the enumeration pieces separately with progress prints."""
import sys, itertools, time
import numpy as np
import sympy as sp
X = sp.Symbol("X")
POLY_COEFFS = {
    "P1":[1,0],"P2":[-1,1],"P4":[1,-2,4,-3,1],
    "P8":[1,-3,7,-14,30,-58,96,-123,114,-73,31,-8,1],
    "Q1":[1,-7,30,-97,269,-679,1612,-3618,7646,-15180,28457,-50741,86189,-138288,
          206152,-279897,339335,-360911,331775,-260367,172556,-95554,43677,-16221,
          4786,-1084,178,-19,1],
}
def _poly(c): return sp.Poly.from_list([sp.Integer(x) for x in c],gens=X,domain=sp.ZZ)
lib={k:_poly(v) for k,v in POLY_COEFFS.items()}
core5=(lib["P1"]**5)*(lib["P2"]**5)
Q1=lib["Q1"]; P8=lib["P8"]
coreP8 = core5*P8   # precompute the fixed factor

t0=time.time()
def build_R_d(d_hl):
    d=_poly(d_hl)
    raw=Q1 - coreP8*d
    cont,pp=sp.Poly(raw.as_expr(),X,domain=sp.ZZ).primitive()
    if pp.LC()<0: pp=sp.Poly(-pp.as_expr(),X,domain=sp.ZZ)
    return abs(int(cont)),pp

# time 20 builds
for i,(c3,c2,c1) in enumerate(itertools.product(range(-4,5),repeat=3)):
    if i>=20: break
    cont,pp=build_R_d([1,c3,c2,c1,1])
print(f"20 builds: {time.time()-t0:.2f}s -> est {729*(time.time()-t0)/20:.0f}s for 729")

# time one full admissibility check
t1=time.time()
cont,pp=build_R_d([1,-2,4,-3,1])
g1=sp.gcd(pp,Q1).degree()
g2=sp.gcd(pp,pp.diff(X)).degree()
v=(pp.eval(0)==1 and pp.eval(1)==1)
print(f"one full admissibility (deg={int(pp.degree())},cont={cont},gcdQ1={g1},sqfree={g2},v01={v}): {time.time()-t1:.2f}s")
