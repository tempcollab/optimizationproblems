"""Progress-emitting COPY of the engine's _count_plus sumset DP (count_opset op='+').

This replicates the exact DP logic of engine/digit_dp.py::_count_plus but inserts a
per-position progress print so the watchdog never sees long silence. It is VALIDATED
against the trusted engine count_opset on small cells before being trusted at d=180.

Usage:
  python sumset_progress.py validate     # cross-check vs engine on small cells
  python sumset_progress.py run <T>      # run d=180 sumset, persist beat_d180.json
"""
import os, sys, json, time, math
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "engine"))

A_FAMILY = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
B = 21
D = 180


def _decompositions(A, op):
    decomp = defaultdict(set)
    for a in A:
        for b in A:
            c = a + b if op == '+' else a - b
            decomp[c].add((a, b))
    return {c: sorted(pairs) for c, pairs in decomp.items()}


def count_plus_progress(A, d, T, log_every=1, label=""):
    """Exact |U+U| count; identical DP to engine _count_plus, with progress prints."""
    decomp = _decompositions(A, '+')
    out_digits = sorted(decomp.keys())
    a_options = {c: sorted({a for (a, b) in pairs}) for c, pairs in decomp.items()}

    TMASK = (1 << (T + 1)) - 1
    dp = {(1, 0): 1}
    t0 = time.time()
    for pos in range(d):
        new_dp = defaultdict(int)
        for (mask, sc), cnt in dp.items():
            for c in out_digits:
                nm = 0
                for a in a_options[c]:
                    nm |= mask << a
                nm &= TMASK
                if nm:
                    new_dp[(nm, sc + c)] += cnt
        dp = dict(new_dp)
        if (pos + 1) % log_every == 0 or pos == d - 1:
            el = time.time() - t0
            print(f"{label}pos {pos + 1}/{d} states={len(dp)} t={el:.0f}s", flush=True)
    total = 0
    for (mask, sc), cnt in dp.items():
        if (mask.bit_length() - 1) >= (sc - T):
            total += cnt
    return total


def validate():
    from digit_dp import count_opset
    cases = [(A_FAMILY, 20, 38), (A_FAMILY, 25, 47), ([0, 2, 3, 4, 5], 18, 33)]
    ok = True
    for (A, d, T) in cases:
        ref = count_opset(A, d, T, '+')
        mine = count_plus_progress(A, d, T, log_every=10, label=f"[d{d}T{T}] ")
        match = (ref == mine)
        ok = ok and match
        print(f"VALIDATE d={d} T={T}: engine={ref} progress={mine} MATCH={match}", flush=True)
    print(f"ALL_MATCH={ok}", flush=True)
    return ok


def run(T):
    dm = json.load(open(os.path.join(HERE, "d180_diffmax.json")))
    cell = dm["cells"][str(T)]
    Nm = int(cell["Nminus"]); M = int(cell["maxU"])
    t0 = time.time()
    Np = count_plus_progress(A_FAMILY, D, T, log_every=1, label="")
    el = time.time() - t0
    v = 1 + math.log(Nm / Np) / math.log(2 * M + 1)
    out = {"cell": f"d180_T{T}", "A": A_FAMILY, "B": B, "d": D, "T": T, "density": T / D,
           "Nplus": str(Np), "Nminus": str(Nm), "maxU": str(M),
           "value_float": v, "value_record_float": 1.1740744476935212,
           "sumset_elapsed_s": el, "done": True}
    json.dump(out, open(os.path.join(HERE, "beat_d180.json"), "w"), indent=2)
    print(f"DONE T={T} |U+U|={len(str(Np))}d sumset_elapsed={el:.1f}s value={v:.13f} PERSISTED", flush=True)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "validate":
        sys.exit(0 if validate() else 1)
    elif len(sys.argv) >= 3 and sys.argv[1] == "run":
        run(int(sys.argv[2]))
    else:
        print("usage: sumset_progress.py validate | run <T>")
        sys.exit(2)
