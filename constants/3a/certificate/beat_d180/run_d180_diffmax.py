"""Compute the CHEAP pieces (diff |U-U| and max(U)) for d=180, T=338 and persist
to d180_diffmax.json. The heavy sumset runs in a separate call.

diff DP uses the collapsed (minSa,Sc) state (deterministic min-transition); max(U)
is greedy (instant). Both fit comfortably in one ~250-300s call at d=180."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
from digit_dp import max_U, count_opset

A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]; B = 21; d = 180
assert B > 2 * max(A)
Ts = [338]
out = {"A": A, "B": B, "d": d, "cells": {}}
t_all = time.time()
for T in Ts:
    t0 = time.time()
    Nm = count_opset(A, d, T, '-')
    M = max_U(A, B, d, T)
    out["cells"][str(T)] = {"T": T, "density": T / d, "Nminus": str(Nm),
                            "maxU": str(M), "elapsed_s": time.time() - t0}
    json.dump(out, open(os.path.join(HERE, "d180_diffmax.json"), "w"), indent=2)
    print(f"T={T}: |U-U|={len(str(Nm))}d max(U)={len(str(M))}d "
          f"t={time.time()-t0:.1f}s PERSISTED", flush=True)
print(f"ALL DONE total={time.time()-t_all:.1f}s", flush=True)
