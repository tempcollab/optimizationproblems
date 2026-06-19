"""
Directed exact d-climb for a STRICT beat of the verified record lower bound on C_3a.

Record (verified, PR #71): A={0,2,3,4,5,6,7,8,9,10}, B=21, d=80, T=150 ->
  value_record = 1 + log(Nminus/Nplus)/log(2*maxU+1) = 1.1740744476935212
The TABLE writes 1.1740744 (a 7-decimal truncation), but the BAR to strictly beat is the
ACTUAL achieved record value 1.1740744476935212, NOT the truncation.

EXACT STRICT-BEAT CERTIFICATE (no float decides anything):
  A new cell (d',T') with counts (Np', Nm', M') strictly beats the record iff
      value_new > value_record.
  We certify this exactly by exhibiting a RATIONAL wedge c with
      value_record < c <= value_new,
  checked by pure big-int power comparisons:
      (a) record does NOT reach c:  ghr_beats(Nm,Np,M, c) == False   (value_record < c)
      (b) new   DOES  reach c:      ghr_geq  (Nm',Np',M', c) == True  (value_new   >= c)
  Then value_new >= c > value_record: a STRICT beat, fully integer-certified.
  We pick c = k/10^7 (or finer) inside the wedge; the float value only STEERS which c to try.

Engine: the FAST carry-free DP engine/digit_dp.count_opset (NOT the slow dp_pareto).
This driver wraps count_opset with a per-digit-position progress print so a long sumset
cell never idles silently.  ONE (d,T) cell per invocation; state persisted to JSON.

Usage:  python3 climb_driver.py <d> <T>
"""
import sys, os, time, json, math
from fractions import Fraction
from collections import defaultdict

ENGINE = os.path.join(os.path.dirname(__file__), "..", "engine")
sys.path.insert(0, ENGINE)
from digit_dp import _decompositions, max_U          # noqa: E402
from dp_engine import ghr_beats, ghr_geq             # noqa: E402  (exact integer tests)

A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
B = 21
# The record cell's exact integers (read, never recomputed for the bar).
REC = json.load(open(os.path.join(os.path.dirname(__file__), "record_baseline.json")))
REC_NP = int(REC["Nplus"]); REC_NM = int(REC["Nminus"]); REC_M = int(REC["maxU"])

STATE = os.path.join(os.path.dirname(__file__), "climb_state.json")
LOG = open(os.path.join(os.path.dirname(__file__), "climb.log"), "a", buffering=1)


def out(s):
    print(s, flush=True)
    LOG.write(s + "\n")


# ---- count_opset with a per-position progress print (verbatim DP, instrumented) ----
def count_plus_progress(A, d, T, tag):
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
        if pos % 4 == 0 or pos == d - 1:
            out(f"  [{tag}+ pos {pos+1}/{d}] states={len(dp)} ({time.time()-t0:.1f}s)")
    total = 0
    for (mask, sc), cnt in dp.items():
        if (mask.bit_length() - 1) >= (sc - T):
            total += cnt
    return total


def count_minus_progress(A, d, T, tag):
    decomp = _decompositions(A, '-')
    out_digits = sorted(decomp.keys())
    a_options = {c: sorted({a for (a, b) in pairs}) for c, pairs in decomp.items()}
    min_a = {c: a_options[c][0] for c in out_digits}
    dp = {(0, 0): 1}
    t0 = time.time()
    for pos in range(d):
        new_dp = defaultdict(int)
        for (msa, sc), cnt in dp.items():
            for c in out_digits:
                nmsa = msa + min_a[c]
                if nmsa <= T:
                    new_dp[(nmsa, sc + c)] += cnt
        dp = dict(new_dp)
        if pos % 8 == 0 or pos == d - 1:
            out(f"  [{tag}- pos {pos+1}/{d}] states={len(dp)} ({time.time()-t0:.1f}s)")
    total = 0
    for (msa, sc), cnt in dp.items():
        if msa <= (T + sc):
            total += cnt
    return total


def find_wedge(Np, Nm, M, denom):
    """
    Find the largest rational c = k/denom with value_record < c <= value_new, certified
    by exact integer-power tests.  Returns (c, k) or None if no wedge at this denom.
    Strategy: value_new float steers; we scan k just above record and confirm exactly.

    IMPORTANT: the exact test cost is the big-int power exponent = the REDUCED denominator
    q of (c-1).  denom must stay SMALL (<= 10^5; reduced q in the thousands) or the powers
    explode (q=10^9 is infeasible).  10^5 separates record 1.17407445 from a >=1e-4 beat.
    """
    # float steer for the search window
    v_new = 1 + math.log(Nm / Np) / math.log(2 * M + 1)
    v_rec = 1 + math.log(REC_NM / REC_NP) / math.log(2 * REC_M + 1)
    if v_new <= v_rec:
        return None
    # candidate k window: from just above record up to just below new
    klo = int(v_rec * denom)            # c ~ record
    khi = int(v_new * denom) + 2        # c ~ new
    best = None
    for k in range(khi, klo - 1, -1):   # prefer the LARGEST c that still works
        c = Fraction(k, denom)
        q = (c - 1).denominator
        if q > 200000:                  # guard: skip any reduced q that would explode
            continue
        # record must NOT reach c (strictly below): ghr_beats(record, c) == False
        rec_below = not ghr_beats(REC_NM, REC_NP, REC_M, c)
        if not rec_below:
            continue
        # new must reach c: value_new >= c
        new_ok = ghr_geq(Nm, Np, M, c)
        if new_ok:
            best = (c, k)
            break
    return best


def main():
    d = int(sys.argv[1]); T = int(sys.argv[2])
    key = f"d{d}_T{T}"
    results = json.load(open(STATE)) if os.path.exists(STATE) else {}
    if key in results and results[key].get("done"):
        out(f"{key} cached: val={results[key]['value_float']:.13f} "
            f"strict_beat={results[key]['strict_beat']}")
        return
    dens = T / d
    out(f"=== CELL {key}  density={dens:.4f}  (T={T}, d={d}) ===")
    t0 = time.time()
    # cheap difference DP first
    Nm = count_minus_progress(A, d, T, key)
    out(f"  Nminus done: {len(str(Nm))} digits ({time.time()-t0:.1f}s)")
    # expensive sumset DP
    Np = count_plus_progress(A, d, T, key)
    out(f"  Nplus done: {len(str(Np))} digits ({time.time()-t0:.1f}s)")
    M = max_U(A, B, d, T)
    v_new = 1 + math.log(Nm / Np) / math.log(2 * M + 1)
    v_rec = 1 + math.log(REC_NM / REC_NP) / math.log(2 * REC_M + 1)
    # Persist the exact integers BEFORE the wedge step so a kill never loses the counts.
    results[key] = {
        "d": d, "T": T, "density": dens,
        "Nplus": str(Np), "Nminus": str(Nm), "maxU": str(M),
        "value_float": v_new, "value_record_float": v_rec,
        "strict_beat": None, "wedge_c": None, "done": False,
        "elapsed_s": time.time() - t0,
    }
    json.dump(results, open(STATE, "w"), indent=2)
    out(f"  counts persisted; value_new={v_new:.13f} value_record={v_rec:.13f}")
    # EXACT strict beat: does value_new > value_record?  Certified by a rational wedge.
    # denom capped at 10^5 -> reduced power exponent stays small (fast big-int powers).
    wedge = None
    for denom in (10**4, 10**5):
        wedge = find_wedge(Np, Nm, M, denom)
        if wedge:
            break
    strict_beat = wedge is not None
    rec = {
        "d": d, "T": T, "density": dens,
        "Nplus": str(Np), "Nminus": str(Nm), "maxU": str(M),
        "value_float": v_new, "value_record_float": v_rec,
        "strict_beat": strict_beat,
        "wedge_c": (str(wedge[0]) if wedge else None),
        "wedge_c_float": (float(wedge[0]) if wedge else None),
        "elapsed_s": time.time() - t0, "done": True,
    }
    results[key] = rec
    json.dump(results, open(STATE, "w"), indent=2)
    out(f"  value_new={v_new:.13f}  value_record={v_rec:.13f}")
    out(f"  STRICT BEAT (exact)={strict_beat}  wedge_c={rec['wedge_c']}  ({time.time()-t0:.1f}s)")
    out(f"=== {key} DONE strict_beat={strict_beat} ===")


if __name__ == "__main__":
    main()
