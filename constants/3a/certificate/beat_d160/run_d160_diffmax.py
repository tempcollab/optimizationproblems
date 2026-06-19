"""Compute the CHEAP pieces (diff |U-U| and max(U)) for d=160 over a small T
neighborhood {299,300,301} and persist to d160_diffmax.json. The heavy sumset
runs in a separate call for the single chosen T.

diff DP is ~150s per T (collapsed minSa-state); max(U) is greedy (instant)."""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
from digit_dp import max_U, count_opset

A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]; B = 21; d = 160
assert B > 2 * max(A)
Ts = [299, 300, 301]
out = {"A": A, "B": B, "d": d, "cells": {}}
t_all = time.time()
for T in Ts:
    t0 = time.time()
    Nm = count_opset(A, d, T, '-')
    M = max_U(A, B, d, T)
    out["cells"][str(T)] = {"T": T, "density": T / d, "Nminus": str(Nm),
                            "maxU": str(M), "elapsed_s": time.time() - t0}
    json.dump(out, open(os.path.join(HERE, "d160_diffmax.json"), "w"), indent=2)
    print(f"T={T}: |U-U|={len(str(Nm))}d max(U)={len(str(M))}d "
          f"t={time.time()-t0:.1f}s PERSISTED", flush=True)
print(f"ALL DONE total={time.time()-t_all:.1f}s", flush=True)
