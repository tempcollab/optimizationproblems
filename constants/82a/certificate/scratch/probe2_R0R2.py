"""R1 probe 2: pin down the near-cancellation mechanism precisely.
Hypothesis A: R0=Q1-bridge*P8 is a 'best integer approx' making |R0| small on Omega.
Hypothesis B: subtracting bridge deepens specific WELLS of log|Q1| where bridge~Q1 in value."""
import numpy as np, sympy as sp
X=sp.Symbol("X")
C={"P1":[1,0],"P2":[-1,1],"P4":[1,-2,4,-3,1],
 "P7":[1,-3,8,-18,36,-62,97,-123,114,-73,31,-8,1],
 "P8":[1,-3,7,-14,30,-58,96,-123,114,-73,31,-8,1],
 "Q1":[1,-7,30,-97,269,-679,1612,-3618,7646,-15180,28457,-50741,86189,-138288,206152,-279897,339335,-360911,331775,-260367,172556,-95554,43677,-16221,4786,-1084,178,-19,1],
 "Q2":[1,-7,30,-96,255,-586,1212,-2360,4573,-9148,18749,-37783,71770,-124910,195848,-273368,335981,-359545,331349,-260271,172542,-95553,43677,-16221,4786,-1084,178,-19,1]}
P={k:sp.Poly.from_list([sp.Integer(c) for c in v],gens=X,domain=sp.ZZ) for k,v in C.items()}
bridge=P["P1"]**5*P["P2"]**5*P["P4"]
R0=sp.Poly((P["Q1"]-bridge*P["P8"]).as_expr(),X,domain=sp.ZZ).primitive()[1]
if R0.LC()<0: R0=sp.Poly(-R0.as_expr(),X,domain=sp.ZZ)
def ev(poly,chi):
    c=np.array([complex(int(a)) for a in poly.all_coeffs()],dtype=np.complex128)
    v=np.zeros_like(chi)+c[0]
    for a in c[1:]: v=v*chi+a
    return v
N=2_000_000
t=(np.arange(N)+0.5)/N
z=np.exp(2j*np.pi*t); chi=z*(1-z)
vQ1=ev(P["Q1"],chi); vbr=ev(bridge*P["P8"],chi); vR0=ev(R0,chi)

# Where are the DEEP WELLS of |Q1| (the smallest-|Q1| spots, where firing comes from)?
lQ1=np.log(np.abs(vQ1)); lR0=np.log(np.abs(vR0))
# focus on deepest 5% wells of |Q1|
thr=np.quantile(lQ1,0.05)
well=lQ1<=thr
print("DEEP WELLS of |Q1| (lowest 5% of log|Q1|):")
print(f"  in wells: mean log|Q1|={lQ1[well].mean():.3f}  mean log|R0|={lR0[well].mean():.3f}")
print(f"  in wells: |bridge*P8|/|Q1| ratio mean = {np.exp((np.log(np.abs(vbr))-lQ1)[well]).mean():.3f}")
print(f"  fraction of wells where R0 is DEEPER than Q1: {(lR0[well]<lQ1[well]).mean():.3f}")
# Is the cancellation putting a NEW root of R0 near the wells? R0 has its own roots.
# The point: does R0 create a deeper notch than Q1 at the SAME spots?
print(f"  deepest log|R0| value overall: {lR0.min():.3f} at s={t[lR0.argmin()]:.4f}")
print(f"  deepest log|Q1| value overall: {lQ1.min():.3f} at s={t[lQ1.argmin()]:.4f}")

# Hypothesis: R0 is constructed so that on the part of Omega where Q1 is ALREADY small,
# bridge*P8 matches Q1 and the difference R0 develops EVEN smaller dips (a tuned root).
# Compare roots of R0 vs Q1 inside the lemniscate region.
rR0=np.array([complex(r) for r in np.roots([complex(int(a)) for a in R0.all_coeffs()])])
rQ1=np.array([complex(r) for r in np.roots([complex(int(a)) for a in P["Q1"].all_coeffs()])])
# active locus point cloud (w=chi on Omega) -- need Omega; recompute quickly with record family
NUM={"P1":26.511877484730615,"P2":23.782846008412744,"P3":0.9707094545190521,"P4":4.526072775020114,"P5":0.038326545650764404,"P6":4.173784226054273,"P8":1.685809173822071}
Cx={"P3":[1,1,-2,1],"P5":[1,-2,4,-7,13,-16,12,-5,1],"P6":[1,-3,8,-16,26,-27,17,-6,1],"P9":[1,-4,10,-17,26,-47,119,-298,592,-878,963,-780,464,-199,59,-11,1]}
for k,v in Cx.items(): P[k]=sp.Poly.from_list([sp.Integer(c) for c in v],gens=X,domain=sp.ZZ)
A=np.zeros(N)
for k,q in NUM.items(): A+=q*np.log(np.maximum(np.abs(ev(P[k],chi)),1e-300))
B=np.zeros(N)
for blk in ["Q1","Q2","P7","P9"]: B+=np.log(np.maximum(np.abs(ev(P[blk],chi)),1e-300))
B+=np.log(np.abs(vR0))+np.log(np.maximum(np.abs(ev(sp.Poly((P["Q2"]+bridge*P["P7"]).as_expr(),X,domain=sp.ZZ).primitive()[1],chi)),1e-300))
Om=B>A
wOm=chi[Om]  # active locus in w-plane
# distance of R0's roots vs Q1's roots to the active locus
def mindist(roots,cloud):
    return [float(np.min(np.abs(r-cloud))) for r in roots]
dR0=sorted(mindist(rR0[np.abs(rR0)<1.5],wOm))[:6]
dQ1=sorted(mindist(rQ1[np.abs(rQ1)<1.5],wOm))[:6]
print(f"\n R0 roots: closest 6 dists to active locus: {[f'{d:.4f}' for d in dR0]}")
print(f" Q1 roots: closest 6 dists to active locus: {[f'{d:.4f}' for d in dQ1]}")
# how many roots does each put INSIDE the active region?
print(f" R0 roots with |.|<1.0 (inside lemniscate-ish): {(np.abs(rR0)<1.0).sum()} of {len(rR0)}")
print(f" Q1 roots with |.|<1.0: {(np.abs(rQ1)<1.0).sum()} of {len(rQ1)}")
