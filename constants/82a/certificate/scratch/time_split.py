import time, sys, math
import numpy as np
sys.path.insert(0,"/home/agentuser/repo/constants/82a/certificate")
import firstvar_10_bridge_support as F
import bound_00_flammang_baseline as vv
import bound_01_doche_base as vu
lib=F.build_library(); static=F.prep_static(lib)
A_R_P4,A_num,A_denom,denom_blocks=static
LOG_FLOOR=F.LOG_FLOOR; na=np.nextafter; PINF=math.inf; NINF=-math.inf; TWO_PI=2*math.pi
N=4000
edges=(np.arange(N+1,dtype=np.float64)/N)*TWO_PI
a_=edges[:-1]; b_=edges[1:]
# time: membership+R(P4) (shared) vs one R(d) rho eval
def rho(coef,a_,b_):
    geo=F.cell_geometry(a_,b_); return F.cell_rho_lo_hi(coef,geo)
t0=time.time()
for _ in range(5):
    geo=F.cell_geometry(a_,b_)
    F.cell_rho_lo_hi(A_R_P4,geo)
t_rp4=(time.time()-t0)/5
t0=time.time()
for _ in range(5):
    geo=F.cell_geometry(a_,b_)
    for nm in A_num: F.cell_rho_lo_hi(A_num[nm],geo)
    for blk in denom_blocks: F.cell_rho_lo_hi(A_denom[blk],geo)
t_mem=(time.time()-t0)/5
A_R_d=F.asc([int(c) for c in F.build_R_d(lib,[1,0,0,0,1])[1].all_coeffs()])
t0=time.time()
for _ in range(5):
    geo=F.cell_geometry(a_,b_)
    F.cell_rho_lo_hi(A_R_d,geo)
t_rd=(time.time()-t0)/5
print(f"per base-grid pass (N={N}): R(P4)={t_rp4*1000:.1f}ms membership(12blk)={t_mem*1000:.1f}ms R(d)={t_rd*1000:.1f}ms",flush=True)
print(f"shared fraction = {(t_rp4+t_mem)/(t_rp4+t_mem+t_rd)*100:.0f}%",flush=True)
