"""Joint 9-exponent Nelder-Mead for the q8A family (j3 + j9 both A-base).
Single start per invocation (arg: start index) so output is progressive and we
avoid the watchdog. N=80k for the optimizer; re-eval best at N=4M.
"""
import sys, time
import numpy as np
from scipy.optimize import minimize
import bound_07_block_j9 as q8

R2 = [14.283862, 13.947194, 2.593425, 2.283539, 0.249084, 0.577911, 0.565724, 0.893516]
SEED_QH = 0.0662

def objN(x, N):
    q = x[:5]; qE = x[5]; qF = x[6]; qG = x[7]; qH = x[8]
    if min(q) < 0 or qE < 0 or qF < 0 or qG < 0 or qH < 0:
        return 1.0
    return q8.float_value_q8A(q.tolist(), 0.0, 0.0, qE, qF, qG, qH, N=N)

def main():
    idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    N = 80_000
    base = np.array(R2[:5] + [R2[5], R2[6], R2[7], SEED_QH])
    if idx == 0:
        s = base.copy()
    else:
        rng = np.random.default_rng(100 + idx)
        s = base * (1 + rng.uniform(-0.04, 0.04, size=9))
        s[8] = abs(base[8] * (1 + rng.uniform(-0.5, 0.5)))
    # warm-start file: if a prior best exists, polish from it on idx>=10
    if idx >= 10:
        s = np.load('/tmp/q8_bestx.npy')
    t0 = time.time()
    res = minimize(objN, s, args=(N,), method='Nelder-Mead',
                   options=dict(maxiter=3000, maxfev=3000, xatol=1e-7, fatol=1e-10))
    x = res.x
    print(f"start {idx}: f(N={N})={res.fun:.10f}  q={np.round(x[:5],5).tolist()} "
          f"qE={x[5]:.5f} qF={x[6]:.5f} qG={x[7]:.5f} qH={x[8]:.5f} "
          f"nfev={res.nfev} {time.time()-t0:.0f}s", flush=True)
    v4 = objN(x, 4_000_000)
    held = 0.2538925359
    print(f"  re-eval N=4M: {v4:.10f}  margin below held {held}: {held-v4:.3e}", flush=True)
    # track global best across invocations
    import os
    bestfile = '/tmp/q8_bestx.npy'
    valfile = '/tmp/q8_bestval.txt'
    prev = float(np.load('/tmp/q8_bestval.npy')) if os.path.exists('/tmp/q8_bestval.npy') else 1.0
    if v4 < prev:
        np.save(bestfile, x)
        np.save('/tmp/q8_bestval.npy', np.array(v4))
        print(f"  *** new global best {v4:.10f} saved", flush=True)

if __name__ == "__main__":
    main()
