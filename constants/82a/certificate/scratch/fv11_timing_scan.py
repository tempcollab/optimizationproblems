import numpy as np, time
import firstvar_11_firing_obstruction as F
for Ns in [40000, 100000, 200000, 400000]:
    t=time.time()
    SC=F.precompute_scells(Ns)
    ci=int(np.sum(SC['certainly_in'])); st=int(np.sum(SC['straddle']))
    meas_ci=float(np.sum(SC['w'][SC['certainly_in']]))/F.TWO_PI
    meas_ci_st=SC['omega_meas']
    print(f"Ns={Ns}: certIN={ci} straddle={st} meas_in={meas_ci:.6f} meas_couldin={meas_ci_st:.6f} ({time.time()-t:.1f}s)")
