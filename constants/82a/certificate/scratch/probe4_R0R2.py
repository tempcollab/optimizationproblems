"""R1 probe 4: is R0 a 'best integer approximation' that minimizes r_Q among siblings Q1 - integer*P8?
Test the closest-vector framing: vary the bridge multiplier and see if R0's bridge minimizes r_Q."""
import numpy as np, sympy as sp
X=sp.Symbol("X")
C={"P1":[1,0],"P2":[-1,1],"P4":[1,-2,4,-3,1],
 "P8":[1,-3,7,-14,30,-58,96,-123,114,-73,31,-8,1],
 "P7":[1,-3,8,-18,36,-62,97,-123,114,-73,31,-8,1],"P6":[1,-3,8,-16,26,-27,17,-6,1],
 "Q1":[1,-7,30,-97,269,-679,1612,-3618,7646,-15180,28457,-50741,86189,-138288,206152,-279897,339335,-360911,331775,-260367,172556,-95554,43677,-16221,4786,-1084,178,-19,1]}
P={k:sp.Poly.from_list([sp.Integer(c) for c in v],gens=X,domain=sp.ZZ) for k,v in C.items()}
def ev(poly,chi):
    c=np.array([complex(int(a)) for a in poly.all_coeffs()],dtype=np.complex128)
    v=np.zeros_like(chi)+c[0]
    for a in c[1:]: v=v*chi+a
    return v
N=1_000_000; t=(np.arange(N)+0.5)/N; z=np.exp(2j*np.pi*t); chi=z*(1-z)
# crude Omega: |Q1| large region (record family ~ all but near roots). Use a fixed proxy: |Q1|>1.
lQ1=np.log(np.abs(ev(P["Q1"],chi)))
Om=lQ1>0   # rough active region proxy
def rq(poly):
    la=np.log(np.maximum(np.abs(ev(poly,chi)),1e-300))
    return float(la[Om].mean()/poly.degree())

# Try R0 with different bridges: Q1 - P1^a P2^a P4 P8 for a in {3,4,5,6,7} and different tail polys
print("sibling r_Q (proxy Omega=|Q1|>1), log h~0.254:")
print(f"  Q1 itself: r_Q={rq(P['Q1']):.5f}")
for a in [3,4,5,6,7]:
    br=P["P1"]**a*P["P2"]**a*P["P4"]
    Rcand=sp.Poly((P["Q1"]-br*P["P8"]).as_expr(),X,domain=sp.ZZ).primitive()[1]
    if Rcand.LC()<0: Rcand=sp.Poly(-Rcand.as_expr(),X,domain=sp.ZZ)
    cop=sp.gcd(Rcand,P["Q1"]).degree()==0
    irr=Rcand.is_irreducible
    try: r=rq(Rcand)
    except: r=float('nan')
    print(f"  a={a}: deg={Rcand.degree()} r_Q={r:.5f} coprime(Q1)={cop} irred={irr} R0(0)={Rcand.eval(0)}")
# different tail (P6 instead of P8):
for tail in ["P6","P7","P8"]:
    br=P["P1"]**5*P["P2"]**5*P["P4"]
    Rcand=sp.Poly((P["Q1"]-br*P[tail]).as_expr(),X,domain=sp.ZZ).primitive()[1]
    if Rcand.LC()<0: Rcand=sp.Poly(-Rcand.as_expr(),X,domain=sp.ZZ)
    print(f"  tail={tail}: deg={Rcand.degree()} r_Q={rq(Rcand):.5f} coprime={sp.gcd(Rcand,P['Q1']).degree()==0}")
