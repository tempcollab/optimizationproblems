"""One-point DP scan driver for the longer-d frontier (round 3).

Usage:  python3 _scan_point.py <d> <T>
Runs ONE (d,T) point with the fast routines, prints progress (flush=True), and
appends the exact counts + float theta as a Python-literal line to _scan_results.txt
so a later certify step can read them without re-running the DP.
"""
import sys
import os
import time
from math import log

sys.path.insert(0, os.path.dirname(__file__))
from ghr_dp import diffset_fast, sumset_bitmask, max_U

A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
RECORD = 1.1740744
HELD = 1.1744750903655619

d = int(sys.argv[1])
T = int(sys.argv[2])

print(f"[scan] d={d} T={T} c={T/d:.4f} A={A}", flush=True)
t0 = time.time()
diff = diffset_fast(A, d, T)
print(f"[scan]   diffset done ({time.time()-t0:.1f}s) bits={diff.bit_length()}", flush=True)
t1 = time.time()
s = sumset_bitmask(A, d, T)
print(f"[scan]   sumset done ({time.time()-t1:.1f}s) bits={s.bit_length()}", flush=True)
q = 2 * max_U(A, d, T) + 1
th = 1.0 + (log(diff) - log(s)) / log(q)
beats_rec = th > RECORD
beats_held = th > HELD
print(f"[scan] d={d} T={T} theta={th:.13f} beats_record={beats_rec} beats_held={beats_held} "
      f"(total {time.time()-t0:.1f}s)", flush=True)

with open(os.path.join(os.path.dirname(__file__), "_scan_results.txt"), "a") as f:
    f.write(f"({d}, {T}): dict(s={s}, diff={diff}, q={q}, float_theta={th!r}),  "
            f"# c={T/d:.4f} beats_held={beats_held}\n")
print("[scan] appended to _scan_results.txt", flush=True)
