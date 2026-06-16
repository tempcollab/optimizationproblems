import time, sys
sys.path.insert(0,"/home/agentuser/repo/constants/82a/certificate")
import firstvar_10_bridge_support as F
lib=F.build_library(); static=F.prep_static(lib)
for d,label in [([1,-1,4,-3,1],'near#2'),([1,0,0,0,1],'generic'),([1,2,-1,-1,1],'near')]:
    for N,depth,tol in [(4000,8,1e-3),(4000,14,5e-4)]:
        t0=time.time()
        res=F.cert_one(lib,d,static,N,tol,depth)
        print(f'{label} d={d} N={N} depthcap={depth} tol={tol}: D_lo={res["D_lo"]:+.3e} mRd={res["m_Rd"]:.1e} mRP4={res["m_RP4"]:.1e} depth={res["depth"]} unres={res["n_unresolved"]} {time.time()-t0:.1f}s',flush=True)
