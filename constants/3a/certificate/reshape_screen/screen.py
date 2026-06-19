"""
Alphabet-reshape screen for C_3a (GHR sum-difference constant), Round 21.

PURPOSE (scout, NOT a bound-move build): screen alternative digit-ALPHABET SHAPES at
SMALL d (d <= 40, every cell fast, ZERO force-kill risk) to see whether any family's
extrapolated d->oo asymptote beats the current drop-1 record family's ~1.1788 ceiling.

If a shape's extrapolated asymptote exceeds ~1.1788, that shape is a NON-treadmill road
for a future bound-move build (push d there). If none does, the digit-set method is
confirmed near its ceiling on this family and the run is near its honest productive plateau.

================================ THE BOUND FORMULA ============================
GHR2007 lemma: for finite U subset Z>=0 with 0 in U,
    value(U) = 1 + log(|U-U| / |U+U|) / log(2*max(U)+1).
Construction: base-B carry-free digit set
    U(A,B,d,T) = { sum_{i} a_i B^i : a_i in A, sum a_i <= T },   need B > 2*max(A).

Per-digit rates:
    rnum(d) = log(|U-U|/|U+U|) / d       (numerator entropy rate; CLIMBS with d)
    rden(d) = log(2*max(U)+1) / d        (denominator rate; converges fast to log(B))
    value   = 1 + rnum(d)/rden(d).

ASYMPTOTE: rden(d) -> log(B) (since max(U) ~ B^(d-1), log(2max+1)/d -> log B). So
    value(d->oo) = 1 + rinf / log(B),   rinf = lim_{d->oo} rnum(d).
The optimal asymptote over densities is the d->oo sup of rnum at the best T/d.

================================ EXTRAPOLATION METHOD =========================
(Same monotone-numerator method the R18 explorer used, validated to 6e-4.)
rnum climbs as rnum(d) = rinf - c/d. From two d-points (d1<d2) solve:
    rinf = (d2*rnum2 - d1*rnum1) / (d2 - d1),   c = d1*d2*(rnum2-rnum1)/(d2-d1).
We measure rnum at d in {20,30,40} (all carry-free, all fast), use the (30,40) pair for
the headline asymptote and (20,30),(20,40) for a robustness band. The asymptote VALUE is
    value_inf = 1 + rinf / log(B).
For each shape we also optimize the density T/d (scan a small grid) at the largest measured d.

================================ HONESTY ====================================
ALL counts are EXACT big-ints (carry-free digit-DP, engine/digit_dp.count_opset). Floats
appear ONLY in the rate/asymptote DISPLAY -- NO bound is certified here. A winning shape is
a CONJECTURE; it becomes a bound only when a later d-push certifies it by the exact
integer-power wedge. Nothing here enters constants/3a.md.
"""

import sys
import os
import math
import json
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "engine"))
from digit_dp import count_opset, max_U  # noqa: E402


def rates(A, B, d, T):
    """Exact counts -> (value, rnum, rden, Np, Nm, M) at this cell. B>2max(A) required."""
    assert B > 2 * max(A), f"B={B} not > 2max(A)={2*max(A)} (carry-free fails)"
    Np = count_opset(A, d, T, "+")
    Nm = count_opset(A, d, T, "-")
    M = max_U(A, B, d, T)
    if Nm <= Np:  # value would be <= 1: useless shape
        rnum = math.log(Nm / Np) / d
    else:
        rnum = math.log(Nm / Np) / d
    rden = math.log(2 * M + 1) / d
    value = 1.0 + rnum / rden
    return value, rnum, rden, Np, Nm, M


def fit_rinf(d1, r1, d2, r2):
    """rnum(d)=rinf-c/d from two points. Returns (rinf, c)."""
    rinf = (d2 * r2 - d1 * r1) / (d2 - d1)
    c = d1 * d2 * (r2 - r1) / (d2 - d1)
    return rinf, c


def best_density_at_d(A, B, d, dens_grid):
    """At fixed d, scan densities T/d; return (best_value, best_T, best_rnum, best_rden)."""
    best = None
    for dens in dens_grid:
        T = round(dens * d)
        if T < 1:
            continue
        v, rnum, rden, Np, Nm, M = rates(A, B, d, T)
        if best is None or v > best[0]:
            best = (v, T, rnum, rden)
    return best


def screen_shape(name, A, B, ds=(15, 25, 35), dens_grid=None):
    """
    Screen one shape. Pick the best density ONCE at the smallest d (cheap grid), then hold
    that density fixed and measure rnum(d) at the ds points; extrapolate rnum -> rinf using
    the (ds[-2], ds[-1]) pair, asymptote = 1+rinf/log(B).

    Compute is dominated by the sumset DP mask width T+1, so we use a COARSE density grid
    near the known optimum (~1.875) and small d (<=35) -- every cell sub-timeout, zero
    force-kill risk.
    """
    if dens_grid is None:
        dens_grid = [1.7, 1.8, 1.875, 1.95, 2.05, 2.2]
    t0 = time.time()
    logB = math.log(B)
    # best density chosen once at the smallest d (cheapest)
    d0 = ds[0]
    _, T0, _, _ = best_density_at_d(A, B, d0, dens_grid)
    best_dens = T0 / d0
    per_d = []
    for d in ds:
        T = round(best_dens * d)
        v, rnum, rden, Np, Nm, M = rates(A, B, d, T)
        per_d.append({"d": d, "T": T, "value": v, "rnum": rnum, "rden": rden,
                      "dens": round(T / d, 4)})
    # headline asymptote from the two largest d's, at their respective best densities
    d1, r1 = per_d[-2]["d"], per_d[-2]["rnum"]
    d2, r2 = per_d[-1]["d"], per_d[-1]["rnum"]
    rinf, cfit = fit_rinf(d1, r1, d2, r2)
    asym = 1.0 + rinf / logB
    # robustness band using the other pairs
    band = []
    for (i, j) in [(0, 1), (0, 2)]:
        ri, _ = fit_rinf(per_d[i]["d"], per_d[i]["rnum"], per_d[j]["d"], per_d[j]["rnum"])
        band.append(1.0 + ri / logB)
    elapsed = time.time() - t0
    return {
        "name": name, "A": A, "B": B, "max_A": max(A), "alphabet_size": len(A),
        "logB": logB, "per_d": per_d,
        "rinf": rinf, "asymptote": asym, "asymptote_band": sorted(band + [asym]),
        "elapsed_s": round(elapsed, 1),
    }


# Shape catalogue. Each entry: (name, A, B, ds). ds kept small/cheap; heavy (large-max)
# shapes use shorter ds since their values are already far below drop-1 (bigger B raises
# the denominator faster than the numerator). Grouped so each group is one timeout call.
SHAPES = {
    "light": [  # max<=10, small alphabets -- fast even at d=35
        ("drop-1 (RECORD)", [0, 2, 3, 4, 5, 6, 7, 8, 9, 10], 21, (15, 25, 35)),
        ("drop-1-and-2", [0, 3, 4, 5, 6, 7, 8, 9, 10], 21, (15, 25, 35)),
        ("drop-1-2-3", [0, 4, 5, 6, 7, 8, 9, 10], 21, (15, 25, 35)),
        ("full {0..10}", list(range(0, 11)), 21, (15, 25, 35)),
        ("drop-1-and-mid(6)", [0, 2, 3, 4, 5, 7, 8, 9, 10], 21, (15, 25, 35)),
        ("drop-1-5-9", [0, 2, 3, 4, 6, 7, 8, 10], 21, (15, 25, 35)),
        ("AP-step2 {0,2,..,10}", [0, 2, 4, 6, 8, 10], 21, (15, 25, 35)),
        ("AP-step3 {0,3,6,9}", [0, 3, 6, 9], 21, (15, 25, 35)),
        # sparse-ends {0,2,9,10} screened separately: value ~1.05 (sparse alphabet kills
        # the diff/sum ratio) and its d=35 mask is slow -- a confirmed non-contender, dropped.
    ],
    "smallmax": [  # smaller max + smaller base -- fast
        ("drop-1 max6 B=13", [0, 2, 3, 4, 5, 6], 13, (15, 25, 35)),
        ("drop-1 max8 B=17", [0, 2, 3, 4, 5, 6, 7, 8], 17, (15, 25, 35)),
        ("drop-1 max5 B=11", [0, 2, 3, 4, 5], 11, (15, 25, 35)),
        ("drop-1 max4 B=9", [0, 2, 3, 4], 9, (15, 25, 35)),
        ("drop-1 max3 B=7", [0, 2, 3], 7, (15, 25, 35)),
    ],
    "bigmax": [  # large max -- slow cells, shorter ds (already clearly worse, confirm only)
        ("drop-1 max12 B=25", [0] + list(range(2, 13)), 25, (12, 18, 24)),
        ("drop-1 max14 B=29", [0] + list(range(2, 15)), 29, (12, 18, 24)),
        ("drop-1 max20 B=41", [0] + list(range(2, 21)), 41, (12, 18, 24)),
        ("drop-1-2 max16 B=33", [0] + list(range(3, 17)), 33, (12, 18, 24)),
    ],
}


def run_group(group):
    out = os.path.join(os.path.dirname(__file__), f"results_{group}.json")
    # resume: keep shapes already flushed (so a timeout-killed group can continue)
    results = []
    done = set()
    if os.path.exists(out):
        results = json.load(open(out))
        done = {r["name"] for r in results}
    for (name, A, B, ds) in SHAPES[group]:
        if name in done:
            continue
        r = screen_shape(name, A, B, ds=ds)
        results.append(r)
        print_one(r)
        with open(out, "w") as f:
            json.dump(results, f, indent=2)
    print(f"\nGroup '{group}' done -> {out}")


def combine_and_rank():
    results = []
    for group in SHAPES:
        p = os.path.join(os.path.dirname(__file__), f"results_{group}.json")
        if os.path.exists(p):
            results.extend(json.load(open(p)))
    results.sort(key=lambda r: r["asymptote"], reverse=True)
    print("\n" + "=" * 72)
    print("RANKING by extrapolated d->oo asymptote (1 + rinf/log B):")
    print("=" * 72)
    for r in results:
        band = r["asymptote_band"]
        print(f"{r['asymptote']:.5f}  [{band[0]:.5f},{band[-1]:.5f}]  "
              f"rinf={r['rinf']:.5f}  B={r['B']:<3} |A|={r['alphabet_size']:<2}  {r['name']}")
    drop1_asym = next(r["asymptote"] for r in results if "RECORD" in r["name"])
    print("\nDrop-1 (record) asymptote = %.5f  (explorer reference ~1.1788)" % drop1_asym)
    winners = [r for r in results if r["asymptote"] > drop1_asym + 1e-4 and "RECORD" not in r["name"]]
    print("\nSHAPES beating drop-1 asymptote by >1e-4:")
    if winners:
        for r in winners:
            print(f"  *** {r['name']}: asymptote {r['asymptote']:.5f} > {drop1_asym:.5f}")
    else:
        print("  (NONE) -- no reshaped alphabet beats the drop-1 d->oo ceiling.")
    out = os.path.join(os.path.dirname(__file__), "results.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print("\nCombined ranking written to results.json")


def print_one(r):
    print(f"\n[{r['name']}] B={r['B']} A={r['A']} ({r['elapsed_s']}s)")
    for p in r["per_d"]:
        print(f"  d={p['d']:>3} T={p['T']:>3} dens={p['dens']} value={p['value']:.6f} "
              f"rnum={p['rnum']:.5f} rden={p['rden']:.5f}")
    print(f"  -> rinf={r['rinf']:.5f}  ASYMPTOTE={r['asymptote']:.5f}  "
          f"band={[round(x,5) for x in r['asymptote_band']]}")
    sys.stdout.flush()


if __name__ == "__main__":
    # Usage:
    #   python3 screen.py <group>   run one shape group (light|smallmax|bigmax), flush per shape
    #   python3 screen.py rank      combine all results_*.json and print/write the ranking
    arg = sys.argv[1] if len(sys.argv) > 1 else "rank"
    if arg == "rank":
        combine_and_rank()
    elif arg in SHAPES:
        run_group(arg)
    else:
        print(f"unknown arg {arg}; use one of {list(SHAPES)} or 'rank'")
