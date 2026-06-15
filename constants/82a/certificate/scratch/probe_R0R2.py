"""R1 generative-explore probe: WHY does R0=Q1 - P1^5 P2^5 P4 P8 fire?
Test the near-cancellation hypothesis on chi(s)=z(1-z), z=e^{2pi i s}."""
import numpy as np, sympy as sp
X=sp.Symbol("X")
C={
 "P1":[1,0],"P2":[-1,1],"P4":[1,-2,4,-3,1],
 "P7":[1,-3,8,-18,36,-62,97,-123,114,-73,31,-8,1],
 "P8":[1,-3,7,-14,30,-58,96,-123,114,-73,31,-8,1],
 "Q1":[1,-7,30,-97,269,-679,1612,-3618,7646,-15180,28457,-50741,86189,-138288,206152,-279897,339335,-360911,331775,-260367,172556,-95554,43677,-16221,4786,-1084,178,-19,1],
 "Q2":[1,-7,30,-96,255,-586,1212,-2360,4573,-9148,18749,-37783,71770,-124910,195848,-273368,335981,-359545,331349,-260271,172542,-95553,43677,-16221,4786,-1084,178,-19,1],
}
P={k:sp.Poly.from_list([sp.Integer(c) for c in v],gens=X,domain=sp.ZZ) for k,v in C.items()}
bridge=P["P1"]**5*P["P2"]**5*P["P4"]   # deg 14
R0=sp.Poly((P["Q1"]-bridge*P["P8"]).as_expr(),X,domain=sp.ZZ).primitive()[1]
R2=sp.Poly((P["Q2"]+bridge*P["P7"]).as_expr(),X,domain=sp.ZZ).primitive()[1]
if R0.LC()<0: R0=sp.Poly(-R0.as_expr(),X,domain=sp.ZZ)
if R2.LC()<0: R2=sp.Poly(-R2.as_expr(),X,domain=sp.ZZ)
print("deg Q1=",P["Q1"].degree()," deg bridge*P8=",(bridge*P["P8"]).degree()," deg R0=",R0.degree())
print("deg R2=",R2.degree())

def logabs(poly,chi):
    c=np.array([complex(int(a)) for a in poly.all_coeffs()],dtype=np.complex128)
    v=np.zeros_like(chi)+c[0]
    for a in c[1:]: v=v*chi+a
    return np.log(np.maximum(np.abs(v),1e-300)), v

N=2_000_000
t=(np.arange(N)+0.5)/N
z=np.exp(2j*np.pi*t)
chi=z*(1-z)

# active arc for the record: B>A where B uses the record denominator, A the record numerator.
# Approx the perturbing active set Omega via the *candidate-free* anchor used in the paper.
# Simpler proxy first: compare |Q1| vs |bridge*P8| vs |R0| directly on the contour.
la_Q1,_=logabs(P["Q1"],chi)
la_bridgeP8,_=logabs(bridge*P["P8"],chi)
la_R0,vR0=logabs(R0,chi)
la_Q2,_=logabs(P["Q2"],chi)
la_bridgeP7,_=logabs(bridge*P["P7"],chi)
la_R2,vR2=logabs(R2,chi)

# how close are Q1 and bridge*P8 on the contour? (near-cancellation = they nearly agree)
print("\n--- magnitudes on the full contour (mean log|.|) ---")
print(f" mean log|Q1|        = {la_Q1.mean():.4f}")
print(f" mean log|P1^5P2^5P4*P8| = {la_bridgeP8.mean():.4f}")
print(f" mean log|R0|        = {la_R0.mean():.4f}   (Mahler/2pi)")
print(f" mean log|Q2|        = {la_Q2.mean():.4f}")
print(f" mean log|R2|        = {la_R2.mean():.4f}")

# where on the contour is |R0| smallest? Is it where |Q1| ~ |bridge*P8| (cancellation)?
# cancellation depth: log|R0| - log|Q1|  (negative = R0 smaller than Q1 there)
gap=la_R0-la_Q1
print(f"\n min over s of (log|R0|-log|Q1|) = {gap.min():.4f} at s={t[gap.argmin()]:.4f}")
print(f" fraction of s where |R0|<|Q1|: {(gap<0).mean():.3f}")
# region where Q1 and bridge*P8 are close in *value* (true near-cancellation):
diff_rel=np.abs(la_Q1-la_bridgeP8)
print(f" fraction of s where ||log|Q1|-log|bridge*P8|| < 0.5: {(diff_rel<0.5).mean():.3f}")

# Now the ACTUAL active arc Omega. Use the paper's record numerator/denominator.
NUM={"P1":26.511877484730615,"P2":23.782846008412744,"P3":0.9707094545190521,
 "P4":4.526072775020114,"P5":0.038326545650764404,"P6":4.173784226054273,"P8":1.685809173822071}
Cextra={"P3":[1,1,-2,1],"P5":[1,-2,4,-7,13,-16,12,-5,1],"P6":[1,-3,8,-16,26,-27,17,-6,1],"P9":[1,-4,10,-17,26,-47,119,-298,592,-878,963,-780,464,-199,59,-11,1]}
for k,v in Cextra.items(): P[k]=sp.Poly.from_list([sp.Integer(c) for c in v],gens=X,domain=sp.ZZ)
A=np.zeros(N)
for k,q in NUM.items():
    laa,_=logabs(P[k],chi); A+=q*laa
# B = full record denominator Q1 Q2 R0 R2 P7 P9
B=np.zeros(N)
for blk in ["Q1","Q2","P7","P9"]:
    laa,_=logabs(P[blk],chi); B+=laa
B=B+la_R0+la_R2
Omega = B>A
print(f"\n--- active arc Omega={{B>A}} on the record family: measure={Omega.mean():.4f} ---")
# r_Q for R0 on Omega (candidate-free anchor: remove R0 from B)
def rQ_candfree(la_blk,deg,removed_la):
    Bf=B-removed_la
    m=Bf>A
    return float(la_blk[m].mean()/deg), m.mean()
r_R0,om0=rQ_candfree(la_R0,R0.degree(),la_R0)
r_R2,om2=rQ_candfree(la_R2,R2.degree(),la_R2)
r_Q1,_=rQ_candfree(la_Q1,P["Q1"].degree(),la_Q1)
print(f" r_Q(R0) cand-free = {r_R0:.5f}  (deg {R0.degree()}, Omega meas {om0:.3f})")
print(f" r_Q(R2) cand-free = {r_R2:.5f}  (deg {R2.degree()})")
print(f" r_Q(Q1) cand-free = {r_Q1:.5f}  (deg {P['Q1'].degree()}) -- compare to R0")
print(f" record log h ~ 0.25363; r_Q<log h => fires")

# KEY probe: on Omega, is log|R0| < log|Q1|? (does subtracting the bridge DEEPEN the well on Omega?)
print(f"\n on Omega: mean log|R0|={la_R0[Omega].mean():.4f}  mean log|Q1|={la_Q1[Omega].mean():.4f}")
print(f" on Omega: mean(log|R0|-log|Q1|) = {(la_R0[Omega]-la_Q1[Omega]).mean():.4f}")
print(f" on complement: mean(log|R0|-log|Q1|) = {(la_R0[~Omega]-la_Q1[~Omega]).mean():.4f}")
