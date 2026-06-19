"""
BOUNDED, CHUNKED, PROGRESS-EMITTING directed parameter sweep for a strict beat of the
GHR lower bound on C_3a (record 1.1740744, base-21 digit construction).

Strategy (keeps each candidate fast):
  - SCREEN candidates at a moderate depth d_screen (cheap), comparing each candidate's GHR
    value AT THAT d to the record alphabet's value at the SAME d.  A candidate that beats the
    record alphabet at d_screen is a promotion candidate.
  - The absolute beat (value > 1.1740744) requires the candidate evaluated at the record depth
    (d=80); that is done in the separate promotion step for the few screen-winners, not here.

Each invocation runs ONE chunk (a fixed slice of the candidate grid), with a hard internal
time budget, prints best-so-far + tried + elapsed each candidate, and PERSISTS the incumbent
to sweep_state.json so a killed chunk loses nothing.

All counts EXACT (dp_fast big-int DP, validated vs brute force).  GHR comparison via exact
integer rational-power inequality (ghr_beats), never float for the load-bearing test.
"""
import sys, time, json, math, os
from fractions import Fraction
from dp_fast import count_sumset, count_diffset, maxU
from dp_engine import ghr_beats, ghr_geq

STATE = "sweep_state.json"
RECORD = Fraction(11740744, 10000000)  # 1.1740744 = exact record to beat


def ghr_value_exact_float(m, p, mx):
    return 1 + math.log(m / p) / math.log(2 * mx + 1)


def candidate_value(A, B, d, T):
    """Exact integer counts + (float) GHR value for screening. Returns (val, Nminus,Nplus,max)."""
    if B <= 2 * max(A):
        return None
    p = count_sumset(A, B, d, T)
    m = count_diffset(A, B, d, T)
    mx = maxU(A, B, d, T)
    if p == 0 or m <= p:
        return None
    return ghr_value_exact_float(m, p, mx), m, p, mx


def build_grid():
    """Fixed candidate grid declared UP FRONT.  Each = (A, B, d, T).
    Screening depth fixed; alphabets/bases/cap-density varied around the record cell."""
    grid = []
    d = 24          # screen depth (cheap ~12s/cand)
    # cap density around record 150/80 = 1.875 per digit
    densities = [1.625, 1.75, 1.875, 2.0, 2.25]
    # alphabet families (max(A)=mA, choose B = 2*mA+1 minimal carry-free base, and a couple larger)
    alphabets = {
        "rec_0_2..10":        [0, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "add1_0..10":         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "add11_0_2..11":      [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        "add1and11_0..11":    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        "drop2_0_3..10":      [0, 3, 4, 5, 6, 7, 8, 9, 10],
        "0_2..9":             [0, 2, 3, 4, 5, 6, 7, 8, 9],
        "0_2..12":            [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "0_2_4..10_even":     [0, 2, 4, 6, 8, 10],
        "0_2..10_skip":       [0, 2, 3, 4, 5, 6, 7, 8, 10],   # drop 9
        "wide_0_2..14":       [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    }
    # KEY INSIGHT (verified): in the carry-free regime |U+U|,|U-U| are INDEPENDENT of B;
    # only max(U) depends on B and is minimized (=> value maximized) at the minimal
    # carry-free base B = 2*max(A)+1.  So use ONLY that base for every alphabet.
    for name, A in alphabets.items():
        mA = max(A)
        B = 2 * mA + 1
        for dens in densities:
            T = round(dens * d)
            grid.append((name, A, B, d, T))
    return grid


def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"tried": 0, "best": None, "results": [], "record_alpha_baseline": {}}


def save_state(st):
    json.dump(st, open(STATE, "w"), indent=2)


def main():
    chunk = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    chunk_size = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    budget = float(sys.argv[3]) if len(sys.argv) > 3 else 210.0  # hard internal cap (s)

    grid = build_grid()
    st = load_state()
    lo = chunk * chunk_size
    hi = min(lo + chunk_size, len(grid))
    print(f"[chunk {chunk}] candidates {lo}..{hi} of {len(grid)}  (budget {budget}s)", flush=True)
    t0 = time.time()
    done_keys = {tuple(r["key"]) for r in st["results"]}

    for idx in range(lo, hi):
        if time.time() - t0 > budget:
            print(f"[chunk {chunk}] BUDGET hit at idx {idx}, stopping cleanly", flush=True)
            break
        name, A, B, d, T = grid[idx]
        key = (name, B, d, T)
        if key in done_keys:
            continue
        ct = time.time()
        res = candidate_value(A, B, d, T)
        st["tried"] += 1
        if res is None:
            print(f"  [{idx}] {name} B={B} T={T}: infeasible/skip ({time.time()-ct:.1f}s)", flush=True)
            st["results"].append({"key": list(key), "A": A, "val": None})
            save_state(st)
            continue
        val, m, p, mx = res
        rec = {"key": list(key), "A": A, "val": val, "Nminus": str(m), "Nplus": str(p),
               "maxU_digits": len(str(mx))}
        st["results"].append(rec)
        # track best SCREEN value (relative)
        if st["best"] is None or val > st["best"]["val"]:
            st["best"] = rec
        save_state(st)
        print(f"  [{idx}] {name} B={B} d={d} T={T}: val={val:.7f}  "
              f"best={st['best']['val']:.7f}  tried={st['tried']}  ({time.time()-ct:.1f}s)",
              flush=True)

    # report screen-relative ranking at the end of the chunk
    vals = [(r["val"], r["key"]) for r in st["results"] if r.get("val") is not None]
    vals.sort(reverse=True)
    print(f"[chunk {chunk}] top-5 screen values so far:", flush=True)
    for v, k in vals[:5]:
        print(f"    {v:.7f}  {k}", flush=True)
    print(f"[chunk {chunk}] DONE tried={st['tried']} elapsed={time.time()-t0:.1f}s", flush=True)


if __name__ == "__main__":
    main()
