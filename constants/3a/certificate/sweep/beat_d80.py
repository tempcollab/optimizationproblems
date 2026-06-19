"""
d=80 BEAT TEST for the density lever: record alphabet A={0,2..10}, B=21, d=80, vary cap T.
Record cell is T=150 (value 1.174074447693521).  Compute EXACT counts + the EXACT
integer-rational-power test ghr_beats against 1.1740744 for each T.

Bounded/persisted: each T computed in turn, result appended to beat_d80.json after each,
progress flushed to beat_d80.log.  Pass a comma-separated T list as argv[1] to chunk.
"""
import sys, time, math, json, os
from fractions import Fraction
from dp_pareto import count_sumset, count_diffset, maxU
from dp_engine import ghr_beats

A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
B, d = 21, 80
RECORD = Fraction(11740744, 10000000)  # 1.1740744 exact

Ts = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else [150, 154, 158]
STATE = "beat_d80.json"
log = open("beat_d80.log", "a", buffering=1)
def out(s):
    print(s, flush=True); log.write(s + "\n")

results = json.load(open(STATE)) if os.path.exists(STATE) else {}
for T in Ts:
    k = str(T)
    if k in results:
        out(f"T={T} cached: val={results[k]['value_float']:.15f}")
        continue
    t0 = time.time()
    p = count_sumset(A, B, d, T)
    m = count_diffset(A, B, d, T)
    mx = maxU(A, B, d, T)
    val = 1 + math.log(m / p) / math.log(2 * mx + 1)
    beats = ghr_beats(m, p, mx, RECORD)   # EXACT integer test: value > 1.1740744 ?
    results[k] = {"T": T, "Nplus": str(p), "Nminus": str(m), "maxU": str(mx),
                  "value_float": val, "beats_1.1740744_exact": beats}
    json.dump(results, open(STATE, "w"), indent=2)
    out(f"T={T}: val={val:.15f}  beats_1.1740744(exact)={beats}  ({time.time()-t0:.1f}s)")
out("CHUNK DONE")
