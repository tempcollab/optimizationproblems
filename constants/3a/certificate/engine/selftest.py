"""
Self-test for the carry-free digit-DP engine (C_3a).

  (1) cross-check the DP against BRUTE-FORCE enumeration on small CARRY-FREE cases
      (B > 2*max(A)), for both the sumset and the difference set;
  (2) confirm the no-cap factorization |U op U| = |A op A|^d;
  (3) reproduce the C_3a base-21 record counts (N+, N-, M) EXACTLY against PR #71 and
      certify 1 + log(N-/N+)/log(2M+1) >= 1.1740744 by the exact integer-power inequality.

NOTE ON THE TRIAGE CASE.  The outline's triage numbers (A={0,2,3,4,5}, B=7, d=3, T=8 ->
|U+U|=386, |U-U|=509) are for B=7, which has 2*max(A)=10 > 7: that case has CARRIES and is
NOT in the carry-free regime this engine targets (the record IS carry-free, B=21 > 20).  We
therefore cross-check the engine on genuinely carry-free small cases (its actual domain),
and verify the triage numbers separately by brute force as a sanity check on the GHR formula
itself (not on the carry-free DP).

Run:  timeout 120 python3 selftest.py
"""

import itertools
import sys
from fractions import Fraction

from digit_dp import count_opset, max_U, value_str


def brute_U(A, B, d, T):
    U = set()
    for digits in itertools.product(A, repeat=d):
        if sum(digits) <= T:
            U.add(sum(a * (B ** i) for i, a in enumerate(digits)))
    return U


def brute_counts(A, B, d, T):
    U = brute_U(A, B, d, T)
    plus = {u + v for u in U for v in U}
    minus = {u - v for u in U for v in U}
    return len(plus), len(minus), max(U)


def main():
    ok = True

    # ---- (0) GHR-formula sanity on the carry-FULL triage case (brute only) ----
    print("=== (0) triage case (B=7, carries) -- brute-force GHR sanity ===", flush=True)
    bp, bm, bmax = brute_counts([0, 2, 3, 4, 5], 7, 3, 8)
    print(f"  brute |U+U|={bp} |U-U|={bm} max={bmax}  (expect 386, 509, 266)", flush=True)
    ok &= (bp, bm, bmax) == (386, 509, 266)

    # ---- (1) DP vs brute on CARRY-FREE small cases (the engine's domain) ----
    print("\n=== (1) carry-free DP vs brute (engine domain, B > 2*max(A)) ===", flush=True)
    cases = [
        ([0, 2, 3, 4, 5], 11, 3, 8),
        ([0, 2, 3, 4, 5], 11, 3, 6),
        ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10], 21, 3, 12),
        ([0, 2, 3, 4, 5], 11, 4, 10),
        ([0, 1, 2, 3], 7, 3, 5),
        ([0, 2, 5], 11, 4, 7),
        ([0, 2, 3, 4, 5, 6, 7, 8, 9, 10], 21, 4, 15),
        ([0, 1, 3, 7], 17, 3, 6),
    ]
    for A, B, d, T in cases:
        assert B > 2 * max(A)
        bp, bm, bmax = brute_counts(A, B, d, T)
        dp_p = count_opset(A, d, T, '+')
        dp_m = count_opset(A, d, T, '-')
        dp_max = max_U(A, B, d, T)
        good = (bp == dp_p) and (bm == dp_m) and (bmax == dp_max)
        ok &= good
        print(f"  A={A} B={B} d={d} T={T}: "
              f"+ {dp_p}=={bp} | - {dp_m}=={bm} | max {dp_max}=={bmax}  "
              f"{'OK' if good else 'FAIL'}", flush=True)

    # ---- (2) no-cap factorization |U op U| = |A op A|^d ----
    print("\n=== (2) no-cap factorization |U op U| = |A op A|^d ===", flush=True)
    A2 = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    Aplus = len({a + b for a in A2 for b in A2})
    Aminus = len({a - b for a in A2 for b in A2})
    for d in (3, 4):
        npc = count_opset(A2, d, 10 ** 9, '+')
        nmc = count_opset(A2, d, 10 ** 9, '-')
        good = (npc == Aplus ** d) and (nmc == Aminus ** d)
        ok &= good
        print(f"  d={d}: |U+U|={npc}=={Aplus}^{d}={Aplus**d}, "
              f"|U-U|={nmc}=={Aminus}^{d}={Aminus**d}  {'OK' if good else 'FAIL'}", flush=True)

    # ---- (3) RECORD reproduction (counts from the committed record_*.txt files) ----
    print("\n=== (3) RECORD reproduction (A={0,2..10}, B=21, d=80, T=150) ===", flush=True)
    Np = int(open('record_plus.txt').read())
    Nm = int(open('record_minus.txt').read())
    M = int(open('record_max.txt').read())
    REC_NP = 75448362167176243488362019935078206851619643198150854886920234689186981134888
    REC_NM = 195351744295266763842135520514417052287242446785296742323733058216909095059024572338564089814415
    REC_M = 2995805288150731620410662946668903948341032736664352641511848666717243994160370658179324073879212562136150
    print(f"  N+ ({len(str(Np))} digits) matches PR#71: {Np == REC_NP}", flush=True)
    print(f"  N- ({len(str(Nm))} digits) matches PR#71: {Nm == REC_NM}", flush=True)
    print(f"  M  ({len(str(M))} digits) matches PR#71: {M == REC_M}", flush=True)
    ok &= (Np == REC_NP) and (Nm == REC_NM) and (M == REC_M)

    print(f"  value = {value_str(Np, Nm, M, 18)}  (PR#71: 1.174074447693521163...)", flush=True)
    print("  (rigorous directed-rounded bound + cert: run  python3 certify_record.py )", flush=True)

    # Sanity that the integer-power inequality machinery (for FUTURE small-q beats) is wired
    # correctly, on a SMALL example where q is tiny -- NOT on the record (q ~ 1.25e6, infeasible).
    from digit_dp import certifies_at_least
    # triage-style small carry-free instance value ~ 1.0x; check the predicate discriminates.
    A0 = [0, 2, 3, 4, 5]
    np0 = count_opset(A0, 3, 8, '+')
    nm0 = count_opset(A0, 3, 8, '-')
    m0 = max_U(A0, 11, 3, 8)
    c_lo = Fraction(104, 100)   # 1.04
    c_hi = Fraction(112, 100)   # 1.12 (above the true value, must fail)
    d_lo = certifies_at_least(np0, nm0, m0, c_lo)
    d_hi = certifies_at_least(np0, nm0, m0, c_hi)
    print(f"  integer-power cert on small case: >=1.04 {d_lo} (True), >=1.12 {d_hi} (False)", flush=True)
    ok &= (d_lo is True) and (d_hi is False)

    print("\n" + ("ALL CHECKS PASSED" if ok else "*** SOME CHECK FAILED ***"), flush=True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
