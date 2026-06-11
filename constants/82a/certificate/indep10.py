"""
Correct contamination check using use_A/use_B flags directly (not chosen==A_mid).
A kept cell uses midpoint on branch A (use_A) -> bound = min(flat,straddle,A_mid).
If A_mid is the binding term AND branch A has a suspect factor -> potential unsound.
Branch A={P*}, branch B={Q1,Q2}. Report:
 - kept cells using midpoint (use_A|use_B)
 - of those, where the DOMINANT branch has a suspect factor (rho_lo<=0) -> curv unsound
 - of THOSE, where A_mid (resp B_mid) is actually the binding min (< flat and < straddle)
"""
import numpy as np, math
import verify_upper as vu
na=np.nextafter; PINF=np.inf
def branch_rholo(a,b):
    m=0.5*(a+b); r=0.5*(b-a)
    Wc,DWc,DDWc,DDDWc=vu.w_full_cell(a,b)
    Wm,DWm,DDWm,DDDWm=vu.w_full_point(m)
    As=np.zeros_like(a,dtype=bool); Bs=np.zeros_like(a,dtype=bool)
    for nm in ["P1","P2","P4","P6","P8"]:
        As=As|(vu.rho_full(vu.ASC[nm],m,r,Wm,DWm,DDWm,DDDWm,Wc,DWc,DDWc,DDDWc)[2]<=0)
    for nm in ["Q1","Q2"]:
        Bs=Bs|(vu.rho_full(vu.ASC[nm],m,r,Wm,DWm,DDWm,DDDWm,Wc,DWc,DDWc,DDDWc)[2]<=0)
    return As,Bs
def diag(a,b,q,rem_cap):
    d=vu.cell_AB(a,b,q)
    r=na(0.5*(b-a),PINF); width=na(b-a,PINF)
    h3_24=na(na(na(width*width,PINF)*width,PINF)/24.0,PINF)
    r2=na(r*r,PINF); r3=na(r2*r,PINF)
    A_hi=d["A_hi"];A_lo=d["A_lo"];B_hi=d["B_hi"];B_lo=d["B_lo"]
    flat=na(width*np.maximum(A_hi,B_hi),PINF)
    mid_up=np.maximum(d["A_mid_up"],d["B_mid_up"])
    slope_max=np.maximum(d["A_slope"],d["B_slope"]); curv_max=np.maximum(d["A_curv"],d["B_curv"])
    dev_int=na(na(slope_max*r2,PINF)+na(na(0.5*curv_max,PINF)*na((2/3)*r3,PINF),PINF),PINF)
    straddle=na(na(width*mid_up,PINF)+dev_int,PINF)
    A_dom=A_lo>B_hi; B_dom=B_lo>A_hi
    A_rem=na(h3_24*d["A_curv"],PINF); B_rem=na(h3_24*d["B_curv"],PINF)
    A_mid=na(width*d["A_mid_up"]+A_rem,PINF); B_mid=na(width*d["B_mid_up"]+B_rem,PINF)
    use_A=A_dom&(A_rem<=rem_cap)&np.isfinite(A_mid)
    use_B=B_dom&(B_rem<=rem_cap)&np.isfinite(B_mid)
    refine=~(use_A|use_B)&(dev_int>rem_cap)&np.isfinite(dev_int)
    return flat,straddle,A_mid,B_mid,use_A,use_B,refine
edges=np.linspace(0.0,2.0*math.pi,200001)
a=edges[:-1].copy(); b=edges[1:].copy()
rounds=0; kept_mid=0; contam=0; contam_binding=0
while True:
    As,Bs=branch_rholo(a,b)
    flat,straddle,A_mid,B_mid,uA,uB,refine=diag(a,b,vu.QSTAR,1e-10)
    keep=~refine
    kept_mid+=int(np.sum(keep&(uA|uB)))
    # midpoint on a suspect dominant branch:
    bad=keep&((uA&As)|(uB&Bs))
    contam+=int(np.sum(bad))
    # and where that midpoint is the binding min:
    A_binding=uA&(A_mid<np.minimum(flat,straddle))
    B_binding=uB&(B_mid<np.minimum(flat,straddle))
    bad_bind=keep&((A_binding&As)|(B_binding&Bs))
    contam_binding+=int(np.sum(bad_bind))
    nbad=int(np.sum(refine))
    if nbad==0 or rounds>=12: break
    ab,bb=a[refine],b[refine]; mid=0.5*(ab+bb)
    a=np.concatenate([ab,mid]); b=np.concatenate([mid,bb]); rounds+=1
print(f"kept midpoint cells (use_A|use_B)={kept_mid}")
print(f"  midpoint on SUSPECT dominant branch={contam}")
print(f"  of those where midpoint is the BINDING min={contam_binding} (must be 0 for soundness)")
