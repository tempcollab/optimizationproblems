"""Heavy sumset |U+U| via the engine's count_opset (proven-fast path, no logging
overhead). Loads diff/max from d160_diffmax.json for the chosen T, persists
beat_d160.json. The chosen T is read from argv[1] (default 300)."""
import os, sys, json, time, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))
from digit_dp import count_opset

A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]; B = 21; d = 160
T = int(sys.argv[1]) if len(sys.argv) > 1 else 300
dm = json.load(open(os.path.join(HERE, "d160_diffmax.json")))
cell = dm["cells"][str(T)]
Nm = int(cell["Nminus"]); M = int(cell["maxU"])
t0 = time.time()
Np = count_opset(A, d, T, '+')
el = time.time() - t0
v = 1 + math.log(Nm / Np) / math.log(2 * M + 1)
out = {"cell": f"d160_T{T}", "A": A, "B": B, "d": d, "T": T, "density": T / d,
       "Nplus": str(Np), "Nminus": str(Nm), "maxU": str(M),
       "value_float": v, "value_record_float": 1.1740744476935212,
       "elapsed_s": el, "done": True}
json.dump(out, open(os.path.join(HERE, "beat_d160.json"), "w"), indent=2)
with open(os.path.join(HERE, "run_d160_engine.log"), "w") as f:
    f.write(f"T={T} |U+U|={len(str(Np))}d sum_elapsed={el:.1f}s value={v:.13f} PERSISTED\n")
print(f"T={T} |U+U|={len(str(Np))}d sum_elapsed={el:.1f}s value={v:.13f} PERSISTED", flush=True)
