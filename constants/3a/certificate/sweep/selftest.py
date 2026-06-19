"""Self-test the DP engine against BRUTE-FORCE enumeration on small cases."""
import sys, itertools, time
from dp_engine import count_sumset, count_diffset, maxU, ghr_value_float, ghr_beats, ghr_geq
from fractions import Fraction


def brute(A, B, d, T):
    """Enumerate U exactly, compute |U+U|, |U-U|, max(U) by brute force."""
    U = set()
    for digits in itertools.product(A, repeat=d):
        if sum(digits) <= T:
            val = sum(a * (B ** i) for i, a in enumerate(digits))
            U.add(val)
    U = sorted(U)
    plus = set()
    minus = set()
    for u in U:
        for v in U:
            plus.add(u + v)
            minus.add(u - v)
    return len(plus), len(minus), max(U), len(U)


def check(A, B, d, T, exp_plus=None, exp_minus=None, exp_val=None):
    assert B > 2 * max(A), f"NOT carry-free: B={B} <= 2*max(A)={2*max(A)}"
    t0 = time.time()
    bp, bm, bmax, bsize = brute(A, B, d, T)
    dp_p = count_sumset(A, B, d, T)
    dp_m = count_diffset(A, B, d, T)
    dp_max = maxU(A, B, d, T)
    el = time.time() - t0
    ok = (bp == dp_p) and (bm == dp_m) and (bmax == dp_max)
    print(f"A={A} B={B} d={d} T={T} |U|={bsize}")
    print(f"  |U+U|: brute={bp} dp={dp_p} {'OK' if bp==dp_p else 'FAIL'}")
    print(f"  |U-U|: brute={bm} dp={dp_m} {'OK' if bm==dp_m else 'FAIL'}")
    print(f"  max:   brute={bmax} dp={dp_max} {'OK' if bmax==dp_max else 'FAIL'}")
    val = ghr_value_float(dp_m, dp_p, dp_max)
    print(f"  GHR value (float): {val:.7f}")
    if exp_plus is not None:
        print(f"  EXPECTED |U+U|={exp_plus} |U-U|={exp_minus} val~{exp_val}: "
              f"{'MATCH' if (bp==exp_plus and bm==exp_minus) else 'MISMATCH'}")
    print(f"  ({el:.2f}s)  ALL={'OK' if ok else 'FAIL'}", flush=True)
    return ok


if __name__ == "__main__":
    allok = True
    # The prescribed anchor self-test
    allok &= check([0, 2, 3, 4, 5], 7, 3, 8, exp_plus=386, exp_minus=509, exp_val=1.0440566)
    # extra brute cross-checks (vary every parameter)
    allok &= check([0, 1, 2, 3], 7, 3, 5)
    allok &= check([0, 2, 4, 6], 13, 3, 9)
    allok &= check([0, 2, 3, 4, 5], 11, 4, 6)
    allok &= check([0, 1, 2, 3, 4, 5], 11, 3, 7)
    allok &= check([0, 2, 5, 6], 13, 4, 8)
    # no-cap case must factor as |A+-A|^d
    A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    p = count_sumset(A, 21, 3, 10**9)
    m = count_diffset(A, 21, 3, 10**9)
    ApA = len({x+y for x in A for y in A}); AmA = len({x-y for x in A for y in A})
    print(f"no-cap factor check: |U+U|={p} vs |A+A|^d={ApA**3} {'OK' if p==ApA**3 else 'FAIL'}; "
          f"|U-U|={m} vs |A-A|^d={AmA**3} {'OK' if m==AmA**3 else 'FAIL'}", flush=True)
    allok &= (p == ApA**3 and m == AmA**3)
    # exact-comparison discriminating test on the anchor
    bp, bm, bmax, _ = brute([0,2,3,4,5],7,3,8)
    print("exact ghr_beats anchor c=1.044:", ghr_beats(bm, bp, bmax, Fraction(1044,1000)),
          " c=1.0441:", ghr_beats(bm, bp, bmax, Fraction(10441,10000)), flush=True)
    print("\nSELFTEST", "PASS" if allok else "FAIL")
    sys.exit(0 if allok else 1)
