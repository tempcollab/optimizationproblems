#!/usr/bin/env python3
"""
Memory-bounded EXACT |U+U| sum-set count for the Griego family (constant C_3a).

Sketch: griego-ntt-push.  This is the R17 deliverable that REPLACES the (Sv, big-int
bitmask) sum-set DP (`count_sumset` in griego-family-larger-mT.py) with an INTERVAL-RUN
(run-length-compressed) state, so the load-bearing s=|U+U| count reproduces at m>=180
inside the 8 GB container (the bitmask DP's reviewer/builder both OOM'd at m>=130 in R16).

=====================================================================================
SET-UP (identical to the verified family; b > 2*max(A) carry-free).
  A = {0,2,3,4,5,6,7,8,9,10}  (the true Griego alphabet: 0..10 with only 1 missing),
  base b = 21 (b > 2*max(A)=20  =>  digit map injective, no carries),
  U = { sum_i x_i b^i : x in A^m, sum_i x_i <= T }.
Carry-free  =>  |U+U| = #{ distinct sum-vectors (x_i+y_i)_i realizable by x,y in W },
where W = { x in A^m : sum x_i <= T }.

A sum-vector v=(v_i), v_i in (A+A) = {0,2,3,...,20}, is realizable iff there exist
x_i in X_{v_i} (achievable x-values for column-sum v_i) with
  sum x_i <= T   AND   sum y_i = (sum v_i) - (sum x_i) <= T,
i.e. the reachable set of  Sx = sum x_i  meets the window [ (sum v_i) - T , T ].

DP over columns carrying state (Sv, R):
  Sv = running sum of v_i  (sum-vector digit-sum so far),
  R  = set of reachable Sx = sum x_i  given the v-prefix, clamped to the live window.
A distinct sum-vector is counted iff at the end R meets [Sv - T, T].

=====================================================================================
WHY RUNS, AND WHY THEY STAY FEW (the memory bound).
Each column's achievable x-set X_w is CONTIGUOUS except for a single missing value 1 at
the bottom (X_w = {0} u {2,..,w} for w<=10; fully contiguous for w>=11; verified in code).
So R = Minkowski sum (over chosen columns) of near-interval sets; after a few nonzero
columns the bottom gap at 1 is filled (0+2, 2+0, ...) and R becomes a SINGLE interval
except for a tiny non-contiguous bottom. Empirically max ~58 runs, mean ~3.8 runs at
T=114, and the bitmask is replaced by a sorted tuple of <=O(few-dozen) (lo,hi) runs.
Memory is then bounded by (#states) * (#runs), NOT by 2^T per-state bitmask width.

EXACTNESS.  The run-set operations below (Minkowski-sum with X_w, clamp to <=T, drop
bits below Sv-T, membership-meets-window test) are EXACT set operations on integer
intervals -- no modulus, no float, no rounding.  Validated bit-for-bit against the
big-int bitmask DP `count_sumset` AND against brute force (see --gate).

Run:
  python3 ivl_sumset.py --gate           # oracle gate: runs == bitmask == brute (small)
  python3 ivl_sumset.py --cross M T       # cross-check runs-DP vs bitmask DP at (M,T)
  python3 ivl_sumset.py --point M T        # exact s=|U+U| at (M,T), memory-bounded
=====================================================================================
"""
import importlib.util
import os
import resource
import sys
import time
from collections import defaultdict
from itertools import product

_L2 = os.path.join(os.path.dirname(__file__), "griego-family-larger-mT.py")
_spec = importlib.util.spec_from_file_location("griego_l2", _L2)
griego_l2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(griego_l2)

A_GRIEGO = griego_l2.A_GRIEGO        # [0,2,3,4,5,6,7,8,9,10]
B_GRIEGO = griego_l2.B_GRIEGO        # 21
build_tables = griego_l2.build_tables
count_sumset = griego_l2.count_sumset   # the big-int bitmask DP (exact, OOMs at large T)
ghr_bruteforce = griego_l2.ghr_bruteforce


# ----------------------------------------------------------------- run-set primitives
# A run-set is a tuple of sorted, disjoint, NON-ADJACENT (gap>=1) integer intervals
#   ((lo1,hi1),(lo2,hi2),...) with lo1<=hi1 < lo2-1 <= ... (each interval inclusive).
# It denotes the integer set  U_k [lo_k, hi_k].  Empty set = ().

def runs_from_intervals(ivals):
    """Normalize an unsorted list of (lo,hi) (inclusive, lo<=hi) into canonical run-set:
       sort, then merge overlapping/adjacent intervals.  EXACT."""
    iv = sorted(i for i in ivals if i[0] <= i[1])
    if not iv:
        return ()
    out = [list(iv[0])]
    for lo, hi in iv[1:]:
        if lo <= out[-1][1] + 1:           # overlap or adjacent -> merge
            if hi > out[-1][1]:
                out[-1][1] = hi
        else:
            out.append([lo, hi])
    return tuple((a, b) for a, b in out)


def list_to_runs(xs):
    """Compress a sorted list of integers into canonical run-set (merge consecutive)."""
    return runs_from_intervals([(x, x) for x in xs])


def _merge_sorted_ivals(ivals):
    """Merge an ALREADY-SORTED (by lo) list of (lo,hi) intervals into canonical run-set,
       in one linear pass (no sort).  EXACT."""
    if not ivals:
        return ()
    out = []
    clo, chi = ivals[0]
    for lo, hi in ivals[1:]:
        if lo <= chi + 1:                  # overlap or adjacent -> extend
            if hi > chi:
                chi = hi
        else:
            out.append((clo, chi))
            clo, chi = lo, hi
    out.append((clo, chi))
    return tuple(out)


def runs_minkowski_rr(R, Xruns):
    """Minkowski sum of two run-sets R and Xruns, i.e. { r + x : r in R, x in X }.
       Each pair of intervals adds as [a,b]+[c,d] = [a+c, b+d] (interval + interval = an
       interval, EXACTLY).  Xruns has very few runs (the column achievable x-set is
       {0} u [2,w] for w<=10, else a single interval).  For |Xruns|==1 the shifted copy of R
       is already sorted -> a single linear merge (no sort).  For |Xruns|>1 we heap-merge the
       few shifted-and-sorted copies.  EXACT; equivalent to runs_from_intervals(all pairs)."""
    if not R or not Xruns:
        return ()
    if len(Xruns) == 1:
        c, d = Xruns[0]
        shifted = [(a + c, b + d) for (a, b) in R]   # already sorted by lo
        return _merge_sorted_ivals(shifted)
    # few Xruns: build per-Xrun sorted shifted copies, heap-merge them.
    import heapq
    streams = []
    for c, d in Xruns:
        streams.append([(a + c, b + d) for (a, b) in R])
    merged = list(heapq.merge(*streams))             # sorted by lo (then hi)
    return _merge_sorted_ivals(merged)


def runs_minkowski(R, Xw):
    """Minkowski sum of run-set R with the integer set Xw (a sorted list of x-values).
       Compresses Xw to runs first (few runs), then interval+interval addition.  EXACT."""
    return runs_minkowski_rr(R, list_to_runs(Xw))


def runs_clamp_top(R, T):
    """Intersect run-set R with (-inf, T], i.e. drop everything above T.  EXACT."""
    out = []
    for lo, hi in R:
        if lo > T:
            break                          # runs sorted ascending; rest all > T
        out.append((lo, min(hi, T)))
    return tuple(out)


def runs_clamp_bottom(R, lo_edge):
    """Intersect run-set R with [lo_edge, +inf), i.e. drop everything below lo_edge.
       (Mirrors the bitmask DP's `(nR>>lo)<<lo` low-clamp: values below Sv-T are forever
        infeasible since Sv only grows.)  EXACT."""
    if lo_edge <= 0:
        return R
    out = []
    for lo, hi in R:
        if hi < lo_edge:
            continue
        out.append((max(lo, lo_edge), hi))
    return tuple(out)


def runs_meets_window(R, lo_edge, T):
    """True iff run-set R has any element in [max(0,lo_edge), T].  EXACT."""
    lo_edge = max(0, lo_edge)
    for lo, hi in R:
        if hi < lo_edge:
            continue
        if lo > T:
            return False
        return True                        # [lo,hi] overlaps [lo_edge,T]
    return False


def runs_max_runcount(R):
    return len(R)


# ----------------------------------------------------------------- the memory-bounded DP
def sumset_runs(A, m, T, progress=False, prog_every=20):
    """EXACT |U+U| via the INTERVAL-RUN DP.  State key (Sv, run-set tuple); the reachable
       Sx set is run-length compressed, so memory is bounded by (#states)*(#runs), not by
       a 2^T per-state bitmask.  Identical semantics to count_sumset; validated vs it and
       vs brute force in --gate.

       The dynamic window is the SAME as the bitmask DP:
         - top clamp:    drop Sx > T            (carry of more than T into x is infeasible)
         - bottom clamp: drop Sx < Sv - T       (since Sv only grows, forever infeasible)
       A sum-vector is counted iff at the end its reachable Sx meets [Sv-T, T]."""
    Xw, _, _ = build_tables(A)
    sumvals = sorted(Xw)
    Xruns = {w: list_to_runs(Xw[w]) for w in sumvals}   # precompute column run-sets
    # Precompute transition descriptors per column-sum w:
    #   xmin = min achievable x, xspan = (Xruns[w] has a single interval [c,d])?
    # Most w produce a single interval; the only multi-run Xruns are w in {2,3,4,..,10}
    # (the {0} u [2,w] shape -- a leading {0} run then [2,w]).  Handle both with an inlined
    # merge that ALSO applies the top clamp (<=T) in the same pass.
    cur = defaultdict(int)
    cur[(0, ((0, 0),))] = 1                 # Sv=0, R={0}  (flat tuple of (lo,hi))
    t0 = time.time()
    peak_states = 1
    peak_runs = 1
    for col in range(m):
        nxt = defaultdict(int)
        nxt_get = nxt.__getitem__         # micro-opt: bound method lookup
        for (Sv, R), cnt in cur.items():
            for w in sumvals:
                Xr = Xruns[w]
                # --- Minkowski(R, Xr): interval+interval add, then merge sorted, top-clamp T ---
                if len(Xr) == 1:
                    c, d = Xr[0]
                    # shifted copy of R, already sorted by lo
                    it = iter(R)
                    a, b = next(it)
                    clo = a + c
                    chi = b + d
                    if chi > T:
                        chi = T
                    out = []
                    ap = out.append
                    if clo <= T:
                        for a, b in it:
                            lo = a + c
                            hi = b + d
                            if hi > T:
                                hi = T
                            if lo > T:
                                break
                            if lo <= chi + 1:
                                if hi > chi:
                                    chi = hi
                            else:
                                ap((clo, chi))
                                clo, chi = lo, hi
                        ap((clo, chi))
                        nR = tuple(out)
                    else:
                        nR = ()
                else:
                    nR = runs_clamp_top(runs_minkowski_rr(R, Xr), T)
                if not nR:
                    continue
                nSv = Sv + w
                loedge = nSv - T
                if loedge > 0:
                    nR = runs_clamp_bottom(nR, loedge)
                    if not nR:
                        continue
                nxt[(nSv, nR)] += cnt
        cur = nxt
        peak_states = max(peak_states, len(cur))
        if cur:
            peak_runs = max(peak_runs, max(len(R) for (_, R) in cur))
        if progress and ((col + 1) % prog_every == 0 or col == m - 1):
            rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
            mr = max((len(R) for (_, R) in cur), default=0)
            print(f"  [runs-DP] col={col+1}/{m} states={len(cur)} maxruns={mr} "
                  f"maxRSS={rss:.0f}MB t={time.time()-t0:.0f}s", flush=True)
    total = 0
    for (Sv, R), cnt in cur.items():
        if runs_meets_window(R, Sv - T, T):
            total += cnt
    if progress:
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
        print(f"  [runs-DP] DONE m={m} T={T}: s={len(str(total))} digits "
              f"head={str(total)[:20]} peak_states={peak_states} peak_runs={peak_runs} "
              f"maxRSS={rss:.0f}MB t={time.time()-t0:.0f}s", flush=True)
    return total


# ----------------------------------------------------------------- validation
def oracle_gate(verbose=True, brute_cap=4_000_000):
    """EXACT agreement of the run-set DP against TWO independent counters on cases that
       exercise the T-clamp (Sv >> T), the non-contiguous Griego alphabet {0,2,..,10}, a
       contiguous control, AND another non-contiguous alphabet {0,3,5,9}:

         3-WAY  runs-DP == bitmask-DP == brute     where |U|^2 <= brute_cap (brute tractable)
         2-WAY  runs-DP == bitmask-DP              for larger T where O(|U|^2) brute is slow
                                                   (the bitmask DP is itself certified vs
                                                    brute at smaller sizes here AND in R3..R13)

       A miscount of 1 in the run-set Minkowski/clamp logic would diverge here.  Rule R3.
       Brute is the ground truth; the bitmask DP is the prior-verified engine; the run-set
       DP is the new memory-bounded engine under test."""
    from itertools import product as _prod
    A = A_GRIEGO
    Acont = [0, 1, 2, 3, 4, 5]
    bcont = 11
    Anc = [0, 3, 5, 9]                       # second non-contiguous, b>2*9=18
    bnc = 19

    def usq(al, m, T, b):
        W = [t for t in _prod(al, repeat=m) if sum(t) <= T]
        return len({sum(t[i] * b ** i for i in range(m)) for t in W}) ** 2

    # (alphabet, b, list of (m,T)) -- include clamp-binding Sv>>T and tiny T.
    suites = [
        ("Griego{0,2..10}", A, B_GRIEGO,
         [(2, 5), (3, 8), (4, 9), (4, 10), (4, 12), (5, 14), (3, 15),
          (5, 20), (5, 22), (6, 15), (6, 9), (5, 7), (4, 6), (6, 18), (7, 16)]),
        ("cont{0..5}", Acont, bcont,
         [(3, 6), (4, 8), (5, 10), (4, 9), (5, 15), (5, 3), (6, 12)]),
        ("nc{0,3,5,9}", Anc, bnc,
         [(3, 8), (4, 12), (5, 14), (5, 30), (4, 5), (6, 20)]),
    ]
    ok = True
    n3 = n2 = 0
    for name, al, b, cases in suites:
        for (m, T) in cases:
            ms = count_sumset(al, m, T)
            rs = sumset_runs(al, m, T)
            do_brute = usq(al, m, T, b) <= brute_cap
            if do_brute:
                bs, _, _ = ghr_bruteforce(al, m, T, b)
                match = (bs == ms == rs)
                n3 += 1
                tag = f"brute={bs} bitmask={ms} runs={rs}"
            else:
                bs = None
                match = (ms == rs)
                n2 += 1
                tag = f"bitmask={ms} runs={rs}"
            ok &= match
            if verbose:
                kind = "3way" if do_brute else "2way"
                print(f"  [gate {kind}] {name:16s} m={m:2d} T={T:2d}: {tag}  "
                      f"{'OK' if match else 'MISMATCH!!'}", flush=True)
            assert match, f"GATE MISMATCH {name} m={m} T={T}: brute={bs} bitmask={ms} runs={rs}"
    print(f"[gate] PASS: runs-DP == bitmask-DP == brute on {n3} cases (3-way) + "
          f"runs-DP == bitmask-DP on {n2} larger cases (2-way) "
          f"(clamp-binding + non-contiguous x2 + contiguous control).", flush=True)
    return ok


def cross_check(m, T):
    """Cross-check runs-DP vs the bitmask DP at (m,T) where brute is infeasible but the
       bitmask DP still fits (moderate T).  Reports both heads + agreement."""
    t0 = time.time()
    rs = sumset_runs(A_GRIEGO, m, T, progress=True)
    t1 = time.time()
    ms = count_sumset(A_GRIEGO, m, T)
    t2 = time.time()
    agree = (rs == ms)
    print(f"[cross] m={m} T={T}: runs s={len(str(rs))}d head={str(rs)[:20]} (t={t1-t0:.0f}s) | "
          f"bitmask s={len(str(ms))}d head={str(ms)[:20]} (t={t2-t1:.0f}s) | "
          f"AGREE={agree}", flush=True)
    assert agree, "runs-DP disagrees with bitmask DP!"
    return rs


def point(m, T):
    """Memory-bounded exact s=|U+U| at (m,T), with per-column progress + peak RSS."""
    s = sumset_runs(A_GRIEGO, m, T, progress=True)
    print(f"s={s}", flush=True)
    return s


def _committed_s(m, T):
    """Read the committed s=|U+U| string for (m,T) from scan-mT-results.txt (last match)."""
    path = os.path.join(os.path.dirname(__file__) or ".", "scan-mT-results.txt")
    want = f"m={m} T={T} "
    s = None
    with open(path) as f:
        for line in f:
            if line.startswith(want):
                for tok in line.split():
                    if tok.startswith("s="):
                        s = int(tok[2:])
    if s is None:
        raise ValueError(f"no committed scan row for m={m} T={T}")
    return s


def verify_scan(m, T):
    """Independent memory-bounded run-DP recompute of s=|U+U| at (m,T), compared
       DIGIT-FOR-DIGIT against the committed scan-mT-results.txt row.  This is the
       reviewer's reproduction step: a genuinely different (run-length) engine confirming
       the committed load-bearing sum-set count within bounded memory."""
    s = sumset_runs(A_GRIEGO, m, T, progress=True)
    sc = _committed_s(m, T)
    ok = (s == sc)
    print(f"[verify] m={m} T={T}: run-DP s={len(str(s))}d head={str(s)[:20]} tail={str(s)[-20:]}",
          flush=True)
    print(f"[verify] committed   s={len(str(sc))}d head={str(sc)[:20]} tail={str(sc)[-20:]}",
          flush=True)
    print(f"[verify] DIGIT-FOR-DIGIT MATCH = {ok}", flush=True)
    assert ok, "run-DP s does NOT match committed scan row!"
    return s


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--gate":
        oracle_gate()
    elif len(sys.argv) > 1 and sys.argv[1] == "--cross":
        cross_check(int(sys.argv[2]), int(sys.argv[3]))
    elif len(sys.argv) > 1 and sys.argv[1] == "--point":
        point(int(sys.argv[2]), int(sys.argv[3]))
    elif len(sys.argv) > 1 and sys.argv[1] == "--verify-scan":
        verify_scan(int(sys.argv[2]), int(sys.argv[3]))
    else:
        print("usage: ivl_sumset.py [--gate | --cross M T | --point M T | --verify-scan M T]")
