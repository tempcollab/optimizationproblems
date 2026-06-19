#!/usr/bin/env python3
"""
Sketch `griego-ntt-push` — fast EXACT sum-set count to push the Griego family to m=130-140.

Constant C_3a (Gyarmati-Hennecart-Ruzsa sum-difference exponent), LOWER bound.
Held (verified, R3/R4): C_3a > 1.176 at (m,T)=(110,210) on A={0,2,...,10}, b=21.
Goal of THIS sketch: reach m=130-140 on the SAME family to climb toward the family
supremum Lambda (~1.1785), registering a held value strictly above 1.176.

=====================================================================================
WHAT R5 CLOSED (build report /tmp/round-5/proof-builder-griego-ntt-push.md):

The R5 build re-scoped HOLE 1. After instrumenting the certified R3 oracle
(`count_sumset` in griego-family-larger-mT.py) it turned out the (Sv,R) state count
SATURATES at a fixed T -- ~26.7k states at (110,210), ~37.2k at (130,247) -- so the
oracle is NOT exponential in m; its cost is ~linear in m at fixed T (each m-step
re-processes the saturated state set). At T~1.9m the per-point cost is well within the
watchdog window: m=130 sum-set ~55-67s, diff-set ~25s. The R4 "m=130 did not finish in
5 min" was a too-large-T / un-checkpointed scout, not a true asymptotic wall.

So the LOAD-BEARING engine for |U+U| is the certified shift-OR bitmask DP itself
(`oracle_sumset` below == the R3 `count_sumset`; it IS `mask|=(mask<<x)` shift-OR with
the dynamic low-clamp -- exactly the "PRIMARY route" the plan named, no modulus/CRT/float).
The build's real contribution to the mandatory GATE (HOLE 2) is an *independent* second
counter -- a set-based Minkowski DP (`indep_sumset`, frozenset states, NO big-int bitmask,
NO clamp arithmetic) -- so the gate is a genuine cross-check of two different algorithms,
not a tautology against the same engine. The 3-way agreement brute-force == indep_sumset
== oracle_sumset on 12+ cases (incl. T-clamp and the non-contiguous alphabet) is the real
validation that any large-m count is trustworthy.

CLOSED holes:
  HOLE 1  fast_sumset_count  -> oracle_sumset (certified shift-OR bitmask DP, reused) + an
          independent indep_sumset cross-checker.  CLOSED.
  HOLE 2  validate_fast_dp   -> 3-way exact gate brute == indep == oracle, 12+ cases.  CLOSED.
  HOLE 3  scan_large_m       -> incremental, checkpointed per-point scan m=120..140.  CLOSED.
  HOLE 4  certify_best       -> tightest k/10000 integer inequality at the best point.  CLOSED.

NEW EXACT POINTS (R5):
  m=130, T=247  ->  theta = 1.1768118909, tight cert C_3a > 11768/10000 = 1.1768.
  m=140, T=265  ->  theta = 1.1771373652, tight cert C_3a > 11771/10000 = 1.1771.  (BEST)
The registered best (m=140, T=265) raises held 1.176 -> 1.1771, a +0.0011 advance.
=====================================================================================

Run:
  python3 griego-ntt-push.py --gate            # the mandatory oracle gate (fast)
  python3 griego-ntt-push.py --point M T       # one exact point, checkpointed
  python3 griego-ntt-push.py --certify M T     # tight k/10000 certificate at (M,T)  (recomputes point)
  python3 griego-ntt-push.py --certify-from-scan M T  # ~2s tight cert from committed scan (no DP recompute)
  python3 griego-ntt-push.py --scan LO HI STEP # incremental m-scan (background-friendly)
  python3 griego-ntt-push.py                   # gate + the registered best point + cert
"""
import importlib.util
import math
import os
import sys
import time
from collections import defaultdict
from fractions import Fraction
from itertools import product

# Import the verified R3/R4 clamped-DP oracle (the validation ground truth + cheap DPs).
_L2 = os.path.join(os.path.dirname(__file__), "griego-family-larger-mT.py")
_spec = importlib.util.spec_from_file_location("griego_l2", _L2)
griego_l2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(griego_l2)

A_GRIEGO = griego_l2.A_GRIEGO   # [0,2,3,4,5,6,7,8,9,10]
B_GRIEGO = griego_l2.B_GRIEGO   # 21

build_tables = griego_l2.build_tables
count_diffset = griego_l2.count_diffset          # 2-D DP, scales to m=200, reused as-is
max_U = griego_l2.max_U                           # greedy, O(m), reused as-is
oracle_sumset = griego_l2.count_sumset            # the certified shift-OR bitmask DP (LOAD-BEARING)
ghr_bruteforce = griego_l2.ghr_bruteforce
theta_value = griego_l2.theta_value
certifies_target_int = griego_l2.certifies_target_int
certifies_target = griego_l2.certifies_target
TARGET = griego_l2.TARGET


# ----------------------------------------------------------------- HOLE 1 (CLOSED)
def fast_sumset_count(A, m, T):
    """EXACT |U+U|.  The load-bearing engine is the certified shift-OR bitmask DP
       (oracle_sumset == R3 count_sumset): the reachable-Sigma_x set is a Python int
       bitmask, "add column digit-set X" is OR over x of (mask<<x), the dynamic low-clamp
       (mask>>lo<<lo, lo=max(0,Sv-T)) bounds width to ~T bits.  Trivially EXACT -- it IS
       the reachable set; no modulus, no CRT, no float.  The (Sv,R) state count saturates
       at fixed T, so the cost is ~linear in m and m=130-140 runs inside the watchdog."""
    return oracle_sumset(A, m, T)


def indep_sumset(A, m, T):
    """INDEPENDENT exact |U+U| -- a set-based Minkowski DP used ONLY to cross-check
       fast_sumset_count in the gate (HOLE 2).  Deliberately shares NO code path with the
       big-int bitmask oracle: states are (Sv, frozenset of reachable Sigma_x), the combine
       is an explicit Python set Minkowski sum, and the feasibility window is enforced with
       integer comparisons (no bitmask, no shift, no <<-clamp).  If a bug existed in the
       bitmask shift/clamp it would NOT be replicated here, so brute==indep==oracle is a
       real 3-way agreement.

       Sum-vector v=(v_i) realizable iff exists x_i in X_{v_i} with Sx=sum x_i in
       [Sv - T, T].  We DP over columns carrying (Sv, R) with R = set of reachable Sx,
       pruning any Sx < Sv - T (forever infeasible, since Sv only grows) and any Sx > T."""
    Xw, _, _ = build_tables(A)
    sumvals = sorted(Xw)
    Xsets = {w: tuple(Xw[w]) for w in sumvals}
    cur = defaultdict(int)
    cur[(0, frozenset({0}))] = 1
    for _ in range(m):
        nxt = defaultdict(int)
        for (Sv, R), cnt in cur.items():
            for w in sumvals:
                nSv = Sv + w
                lo = nSv - T
                nR = set()
                for sx in R:
                    for x in Xsets[w]:
                        v = sx + x
                        if v <= T and v >= lo:   # keep only window-feasible Sx
                            nR.add(v)
                if nR:
                    nxt[(nSv, frozenset(nR))] += cnt
        cur = nxt
    total = 0
    for (Sv, R), cnt in cur.items():
        lo = Sv - T
        if any(lo <= sx <= T for sx in R):
            total += cnt
    return total


# ----------------------------------------------------------------- HOLE 2 (CLOSED): GATE
def validate_fast_dp(verbose=True):
    """MANDATORY GATE (Rule R3).  Three-way EXACT agreement on 12+ (m,T) cases that
       exercise the T-clamp AND the non-contiguous alphabet, BEFORE any large-m number is
       trusted:
         brute-force ghr_bruteforce   (ground truth, small m)
         indep_sumset                 (independent set-based Minkowski DP)
         fast_sumset_count            (the certified shift-OR bitmask DP used at large m)
       A miscount of 1 fabricates the held -- so every case must match EXACTLY.

       Cases cover: the clamp (Sigma x <= T binding, e.g. m=4,T=9; m=5,T=22; m=6,T=15),
       the non-contiguous Griego alphabet {0,2,..,10}, AND a contiguous control alphabet."""
    # (m, T) cases.  3-way (brute==indep==oracle) where brute is tractable (|U|^2 small);
    # 2-way (indep==oracle) where brute's O(|U|^2) sumset blows up.  indep_sumset shares NO
    # code with the bitmask oracle, so even the 2-way cases are a real cross-check.
    Acont = [0, 1, 2, 3, 4, 5]                      # contiguous control, b>2*max=10
    bcont = 11
    # 3-WAY: small, brute-tractable; cover the T-clamp (T binding) on BOTH alphabets.
    griego_3way = [(2, 5), (3, 8), (4, 9), (4, 10), (4, 12), (5, 14),
                   (3, 15), (5, 20), (5, 22), (6, 15)]
    cont_3way = [(3, 6), (4, 8), (5, 10), (4, 9), (5, 15)]
    # 2-WAY: brute too slow (|U|^2 ~ 1e8-1e9) but indep vs oracle still cross-checks.
    griego_2way = [(6, 18), (4, 40), (8, 18), (9, 20), (7, 22)]
    ok = True
    for (m, T) in griego_3way:
        bs, _, _ = ghr_bruteforce(A_GRIEGO, m, T, B_GRIEGO)
        isum = indep_sumset(A_GRIEGO, m, T)
        fsum = fast_sumset_count(A_GRIEGO, m, T)
        match = (bs == isum == fsum)
        ok &= match
        if verbose:
            print(f"  [gate 3way] Griego m={m:2d} T={T:2d}: brute={bs} indep={isum} oracle={fsum}"
                  f"  {'OK' if match else 'MISMATCH!!'}", flush=True)
        assert match, f"GATE 3WAY MISMATCH (Griego) m={m} T={T}: {bs} {isum} {fsum}"
    for (m, T) in cont_3way:
        bs, _, _ = ghr_bruteforce(Acont, m, T, bcont)
        isum = indep_sumset(Acont, m, T)
        fsum = fast_sumset_count(Acont, m, T)
        match = (bs == isum == fsum)
        ok &= match
        if verbose:
            print(f"  [gate 3way] cont   m={m:2d} T={T:2d}: brute={bs} indep={isum} oracle={fsum}"
                  f"  {'OK' if match else 'MISMATCH!!'}", flush=True)
        assert match, f"GATE 3WAY MISMATCH (cont) m={m} T={T}: {bs} {isum} {fsum}"
    for (m, T) in griego_2way:
        isum = indep_sumset(A_GRIEGO, m, T)
        fsum = fast_sumset_count(A_GRIEGO, m, T)
        match = (isum == fsum)
        ok &= match
        if verbose:
            print(f"  [gate 2way] Griego m={m:2d} T={T:2d}: indep={isum} oracle={fsum}"
                  f"  {'OK' if match else 'MISMATCH!!'}", flush=True)
        assert match, f"GATE 2WAY MISMATCH (Griego) m={m} T={T}: indep={isum} oracle={fsum}"
    print(f"[gate] PASS: 3-way (brute==indep==oracle) on {len(griego_3way)+len(cont_3way)} "
          f"cases (clamp + non-contiguous + contiguous control) + 2-way (indep==oracle) on "
          f"{len(griego_2way)} larger cases. Large-m counts are trustworthy.", flush=True)
    return ok


# ----------------------------------------------------------------- HOLE 3 (CLOSED): SCAN
def one_point(m, T, cache_dir=None):
    """EXACT (s,d,M,theta) at (m,T), checkpointed per quantity (Rule R2: never silent).
       Caches the big integers to disk so an expensive point need not be recomputed."""
    tag = f"m{m}_T{T}"
    cache = os.path.join(cache_dir, tag + ".txt") if cache_dir else None
    if cache and os.path.exists(cache):
        with open(cache) as f:
            d_s = dict(line.split("=", 1) for line in f.read().splitlines() if "=" in line)
        s, d, M = int(d_s["s"]), int(d_s["d"]), int(d_s["M"])
        th = theta_value(s, d, M)
        print(f"  [point] m={m} T={T} (cached) theta={th:.10f}", flush=True)
        return s, d, M, th
    t0 = time.time()
    s = fast_sumset_count(A_GRIEGO, m, T)
    t1 = time.time()
    print(f"  [point] m={m} T={T}: s done ({len(str(s))} digits) t_s={t1-t0:.1f}s", flush=True)
    d = count_diffset(A_GRIEGO, m, T)
    t2 = time.time()
    print(f"  [point] m={m} T={T}: d done ({len(str(d))} digits) t_d={t2-t1:.1f}s", flush=True)
    M = max_U(A_GRIEGO, m, T, B_GRIEGO)
    th = theta_value(s, d, M)
    print(f"  [point] m={m} T={T}: M done theta={th:.10f}", flush=True)
    if cache:
        os.makedirs(cache_dir, exist_ok=True)
        with open(cache, "w") as f:
            f.write(f"m={m}\nT={T}\ns={s}\nd={d}\nM={M}\ntheta={th:.10f}\n")
    return s, d, M, th


def scan_large_m(m_lo=120, m_hi=140, step=5, T_ratio=1.9, T_window=2,
                 cache_dir=None, append_results=None):
    """Scan m in [m_lo, m_hi] along T ~ T_ratio*m, probing a small T-window around the
       ray to catch the per-m peak.  PRINTS EACH (m,T,theta,s,d,M) point INCREMENTALLY
       (Rule R2: no single silent >5min run -- run me in the background with a watcher).
       Returns the highest-theta point seen."""
    best = None
    for m in range(m_lo, m_hi + 1, step):
        T0 = int(round(T_ratio * m))
        for T in range(T0 - T_window, T0 + T_window + 1):
            if (T - T0) % 2 != 0 and T != T0:
                continue  # T is effectively even-biased near the optimum; sample sparsely
            s, d, M, th = one_point(m, T, cache_dir=cache_dir)
            beat = certifies_target_int(s, d, M, 11761, 10000)  # > next tick past held
            print(f"[scan] m={m} T={T} theta={th:.10f} beats_1.1761={beat}", flush=True)
            if append_results:
                with open(append_results, "a") as f:
                    f.write(f"m={m} T={T} theta={th:.10f} beat={th>1.1740744} "
                            f"s={s} d={d} M={M} (R5 griego-ntt-push scan)\n")
            if best is None or th > best[3]:
                best = (m, T, s, d, M, th)
    print(f"[scan] BEST: m={best[0]} T={best[1]} theta={best[5]:.10f}", flush=True)
    return best


# ----------------------------------------------------------------- HOLE 4 (CLOSED): CERTIFY
def certify_best(m, T, den=10000, s=None, d=None, M=None):
    """At (m,T) emit the LARGEST k/den with d^den > s^den*(2M+1)^(k-den) (theta > k/den)
       AND the negative control (k+1 fails) -- same exact integer-inequality FORM as the
       held 1.176, at a higher theta.  Pure big-integer comparison; NO float on the
       load-bearing step.  Returns (s,d,M,best_k)."""
    if s is None:
        s, d, M, _ = one_point(m, T)
    q = 2 * M + 1
    # bisect the largest k with d^den > s^den * q^(k-den), k in (den, 2*den).
    th = theta_value(s, d, M)
    lo, hi = den, int((th + 0.01) * den) + 2     # th*den is a safe upper bracket
    # ensure hi actually fails
    while certifies_target_int_raw(s, d, q, hi, den):
        hi += 5
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if certifies_target_int_raw(s, d, q, mid, den):
            lo = mid
        else:
            hi = mid
    best_k = lo
    holds = certifies_target_int_raw(s, d, q, best_k, den)
    fails_next = not certifies_target_int_raw(s, d, q, best_k + 1, den)
    print(f"[certify] m={m} T={T}: theta in [{best_k}/{den}, {best_k+1}/{den})", flush=True)
    print(f"  k={best_k}: d^{den} > s^{den}*q^({best_k}-{den})  =>  theta > {best_k/den:.4f}"
          f"  : PASS = {holds}", flush=True)
    print(f"  k={best_k+1} (control): must FAIL = {fails_next}", flush=True)
    assert holds and fails_next, "certificate not tight"
    assert Fraction(best_k, den) >= TARGET, "must beat the external record 1.1740744"
    print(f"[certify] TIGHT held candidate: C_3a > {best_k}/{den} = {best_k/den:.4f}", flush=True)
    return s, d, M, best_k


def certifies_target_int_raw(s, d, q, num, den):
    """d^den > s^den * q^(num-den).  Pure big-int (no TARGET assert; used inside bisection)."""
    return d ** den > s ** den * q ** (num - den)


def _parse_scan_point(m, T, path=None):
    """Read the EXACT committed s,d,M for (m,T) from scan-mT-results.txt.  Lets the tight
       certificate be re-checked as a ~2s pure big-int comparison WITHOUT re-running the
       ~127s DP -- so the reviewer can verify the certificate arithmetic as its own short,
       watchdog-safe step, separately from an independent recompute via --point."""
    if path is None:
        path = os.path.join(os.path.dirname(__file__) or ".", "scan-mT-results.txt")
    want = f"m={m} T={T} "
    s = d = M = None
    with open(path) as f:
        for line in f:
            if not line.startswith(want):
                continue
            toks = line.split()
            kv = {}
            for tok in toks:
                if tok.startswith("s="):
                    kv["s"] = int(tok[2:])
                elif tok.startswith("d="):
                    kv["d"] = int(tok[2:])
                elif tok.startswith("M="):
                    kv["M"] = int(tok[2:])
            if "s" in kv and "d" in kv and "M" in kv:
                s, d, M = kv["s"], kv["d"], kv["M"]   # keep last (latest committed) match
    if s is None:
        raise ValueError(f"no committed scan row for m={m} T={T} in {path}")
    return s, d, M


def certify_from_scan(m, T, den=10000):
    """WATCHDOG-SAFE certificate re-check: load committed s,d,M for (m,T) and run ONLY the
       tight k/10000 big-int comparison (~2s).  No DP recompute.  This is the step the
       reviewer runs to confirm the certificate arithmetic instantly; the INDEPENDENT
       recompute of s,d,M is a SEPARATE short step (--point M T, ~127s at m=140)."""
    s, d, M = _parse_scan_point(m, T)
    print(f"[certify-from-scan] m={m} T={T}: loaded committed "
          f"s({len(str(s))}d) d({len(str(d))}d) M({len(str(M))}d)", flush=True)
    return certify_best(m, T, den=den, s=s, d=d, M=M)


# ----------------------------------------------------------------- the registered R5 point
# Best exact point located by the R5 incremental scan (see scan-mT-results.txt + the build
# report).  theta CLIMBS along the optimal ray; m=130 at its peak T registers held > 1.176.
BEST_R5 = (140, 265)     # set by the R5 scan; peak T for m=140 (beats m=130's 1.1768)


def main():
    print("Sketch griego-ntt-push (R5 BUILT): fast EXACT sum-set count, Griego family, m=130-140.")
    print("Held to beat: C_3a > 1.176 at (110,210). This build targets a held > 1.176 at m=130.\n")
    print("== MANDATORY ORACLE GATE (HOLE 2) ==")
    validate_fast_dp()
    print()
    m, T = BEST_R5
    print(f"== REGISTERED BEST EXACT POINT (HOLE 3) m={m} T={T} ==")
    s, d, M, th = one_point(m, T)
    print()
    print(f"  s=|U+U| = {len(str(s))} digits, head {str(s)[:18]}...")
    print(f"  d=|U-U| = {len(str(d))} digits, head {str(d)[:18]}...")
    print(f"  M=max U = {len(str(M))} digits, head {str(M)[:18]}...")
    print(f"  theta  ~ {th:.10f}")
    print()
    print("== TIGHT CERTIFICATE (HOLE 4) ==")
    s2, d2, M2, best_k = certify_best(m, T, s=s, d=d, M=M)
    ok_log = certifies_target(s, d, M)   # rigorous log: theta > 1.1740744 (external record)
    print(f"  rigorous log cert theta > 1.1740744 (Griego record): {ok_log}")
    print()
    assert best_k > 11760, "R5 must beat the held 1.176 (k=11760)"
    print(f"RESULT: new held candidate C_3a > {best_k}/10000 = {best_k/10000:.4f}  "
          f"(> previous held 1.176).")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--gate":
        validate_fast_dp()
    elif len(sys.argv) > 1 and sys.argv[1] == "--point":
        one_point(int(sys.argv[2]), int(sys.argv[3]), cache_dir="/tmp/ntt_cache")
    elif len(sys.argv) > 1 and sys.argv[1] == "--certify":
        certify_best(int(sys.argv[2]), int(sys.argv[3]))
    elif len(sys.argv) > 1 and sys.argv[1] == "--certify-from-scan":
        certify_from_scan(int(sys.argv[2]), int(sys.argv[3]))
    elif len(sys.argv) > 1 and sys.argv[1] == "--scan":
        scan_large_m(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]),
                     cache_dir="/tmp/ntt_cache",
                     append_results=os.path.join(os.path.dirname(__file__) or ".",
                                                 "scan-mT-results.txt"))
    else:
        main()
