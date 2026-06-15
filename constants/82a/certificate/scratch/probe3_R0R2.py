"""R1 probe 3: is R0 a coprime 'sibling' of Q1 on the active locus?
And: is bridge=P1^5P2^5P4 chosen so it's NEGLIGIBLE on Omega but reshuffles roots off Omega?"""
import numpy as np, sympy as sp
X=sp.Symbol("X")
C={"P1":[1,0],"P2":[-1,1],"P4":[1,-2,4,-3,1],
 "P8":[1,-3,7,-14,30,-58,96,-123,114,-73,31,-8,1],
 "P7":[1,-3,8,-18,36,-62,97,-123,114,-73,31,-8,1],
 "Q1":[1,-7,30,-97,269,-679,1612,-3618,7646,-15180,28457,-50741,86189,-138288,206152,-279897,339335,-360911,331775,-260367,172556,-95554,43677,-16221,4786,-1084,178,-19,1],
 "Q2":[1,-7,30,-96,255,-586,1212,-2360,4573,-9148,18749,-37783,71770,-124910,195848,-273368,335981,-359545,331349,-260271,172542,-95553,43677,-16221,4786,-1084,178,-19,1]}
P={k:sp.Poly.from_list([sp.Integer(c) for c in v],gens=X,domain=sp.ZZ) for k,v in C.items()}
bridge=P["P1"]**5*P["P2"]**5*P["P4"]
R0=sp.Poly((P["Q1"]-bridge*P["P8"]).as_expr(),X,domain=sp.ZZ).primitive()[1]
if R0.LC()<0: R0=sp.Poly(-R0.as_expr(),X,domain=sp.ZZ)
print("gcd(R0,Q1) deg =",sp.gcd(R0,P["Q1"]).degree(),"  (0 => coprime, R0 is a NEW block)")
print("R0 irreducible?",R0.is_irreducible,"  squarefree?",sp.gcd(R0,R0.diff(X)).degree()==0)
print("R0(0)=",R0.eval(0),"R0(1)=",R0.eval(1),"  (admissible perturbing block needs =1)")

# bridge magnitude on the active locus vs Q1 magnitude:
def ev(poly,chi):
    c=np.array([complex(int(a)) for a in poly.all_coeffs()],dtype=np.complex128)
    v=np.zeros_like(chi)+c[0]
    for a in c[1:]: v=v*chi+a
    return v
N=2_000_000; t=(np.arange(N)+0.5)/N; z=np.exp(2j*np.pi*t); chi=z*(1-z)
# Omega via record family (reuse)
NUM={"P1":26.511877484730615,"P2":23.782846008412744,"P3":0.9707094545190521,"P4":4.526072775020114,"P5":0.038326545650764404,"P6":4.173784226054273,"P8":1.685809173822071}
Cx={"P3":[1,1,-2,1],"P5":[1,-2,4,-7,13,-16,12,-5,1],"P6":[1,-3,8,-16,26,-27,17,-6,1],"P9":[1,-4,10,-17,26,-47,119,-298,592,-878,963,-780,464,-199,59,-11,1]}
for k,v in Cx.items(): P[k]=sp.Poly.from_list([sp.Integer(c) for c in v],gens=X,domain=sp.ZZ)
R2=sp.Poly((P["Q2"]+bridge*P["P7"]).as_expr(),X,domain=sp.ZZ).primitive()[1]
if R2.LC()<0: R2=sp.Poly(-R2.as_expr(),X,domain=sp.ZZ)
A=np.zeros(N)
for k,q in NUM.items(): A+=q*np.log(np.maximum(np.abs(ev(P[k],chi)),1e-300))
B=np.zeros(N)
for blk in ["Q1","Q2","P7","P9"]: B+=np.log(np.maximum(np.abs(ev(P[blk],chi)),1e-300))
B+=np.log(np.abs(ev(R0,chi)))+np.log(np.abs(ev(R2,chi)))
Om=B>A
lbr=np.log(np.abs(ev(bridge*P["P8"],chi)))
lQ1=np.log(np.abs(ev(P["Q1"],chi)))
print(f"\n on Omega ({Om.mean():.3f} measure):")
print(f"   mean log|Q1|        = {lQ1[Om].mean():.3f}")
print(f"   mean log|bridge*P8| = {lbr[Om].mean():.3f}")
print(f"   so |Q1| >> |bridge*P8| on Omega by factor exp({(lQ1-lbr)[Om].mean():.2f})={np.exp((lQ1-lbr)[Om].mean()):.1f}")
print(f"   => on Omega R0=Q1-bridge*P8 ~ Q1 (bridge is a SMALL correction)")
# off Omega (where Q1 large) is the bridge relatively larger?
print(f"\n off Omega: mean log|Q1|={lQ1[~Om].mean():.3f}  mean log|bridge*P8|={lbr[~Om].mean():.3f}")
# the deep wells: is bridge comparable to Q1 there? (that's where subtraction matters)
thr=np.quantile(lQ1,0.02); well=lQ1<=thr
print(f"\n deepest 2% wells of |Q1|: mean log|Q1|={lQ1[well].mean():.2f} mean log|bridge*P8|={lbr[well].mean():.2f}")
print(f"   ratio |bridge*P8|/|Q1| in wells = {np.exp((lbr-lQ1)[well]).mean():.2f}  (>1 => bridge can flip the well)")
