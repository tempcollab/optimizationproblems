"""Reproduce the record baseline at (A={0,2..10}, B=21, d=80, T=150) with EXACT counts
using the fast Pareto-frontier DP.  Sanity anchor for the sweep."""
import time, math, json
from dp_pareto import count_sumset, count_diffset, maxU

A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
B, d, T = 21, 80, 150
log = open("record_log.txt", "w", buffering=1)
def out(s):
    print(s, flush=True); log.write(s + "\n")

t0 = time.time()
p = count_sumset(A, B, d, T); out(f"|U+U| done {time.time()-t0:.1f}s, {len(str(p))} digits")
t1 = time.time()
m = count_diffset(A, B, d, T); out(f"|U-U| done {time.time()-t1:.1f}s, {len(str(m))} digits")
mx = maxU(A, B, d, T)
val = 1 + math.log(m / p) / math.log(2 * mx + 1)
out(f"|U+U| = {p}")
out(f"|U-U| = {m}")
out(f"max(U) has {len(str(mx))} digits")
out(f"value (float) = {val:.15f}")
out(f"target        = 1.174074447693521")
json.dump({"A": A, "B": B, "d": d, "T": T, "Nplus": str(p), "Nminus": str(m),
           "maxU": str(mx), "value_float": val}, open("record_baseline.json", "w"), indent=2)
out(f"total {time.time()-t0:.1f}s; WROTE record_baseline.json")
