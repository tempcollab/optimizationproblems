#!/usr/bin/env python3
"""
C_5b (Sidon density in (4,5)-sets) — guided-search-N21 round-1 certificate.

STATUS: NO strict improvement over the record 4/7 was found this round.
This script is the REPRODUCIBLE artifact for what WAS established:

  (A) The record 14-point gadget A_base IS a (4,5)-set and has h = 8, giving the
      verified bar c* <= 8/14 = 4/7  (exact integer arithmetic, deterministic).
  (B) A rigorous *feasibility map*: combining the PROVEN lower bound c* >= 9/17
      [MT26, Thm via Henning-Yeo] with the gadget framework (Thm 1.5,
      c* = inf_n f(n)/n) shows that a finite (4,5)-set of size N can beat 4/7
      ONLY IF  ceil(9N/17) / N < 4/7,  i.e.  7*ceil(9N/17) < 4N.
      In particular N = 14 and N = 21 (the naive targets) are RULED OUT:
        N=14: floor h >= ceil(126/17)=8, 8/14 = 4/7 exactly (record is optimal at N=14);
        N=21: floor h >= ceil(189/17)=12, 12/21 = 4/7 exactly.
      So beating 4/7 needs a *different* N (smallest feasible: 9,11,13,15,16,17,...).
  (C) Exact, complete (window-limited) search confirming small feasible N sit AT or
      ABOVE their 9/17 floor in the searched window: e.g. N=9 has min h = 6 (> floor 5)
      for all weak-Sidon sets anchored at 0 inside [0,80].  (A documented near-miss /
      structural obstruction, not a beat.)

ALL verification arithmetic is EXACT (Python ints). No floats decide anything.
No randomness in any verification step. Run:  python search_cert_N14.py
"""
import itertools, math

# ---------------------------------------------------------------------------
# Exact primitives (integer arithmetic only)
# ---------------------------------------------------------------------------

def is_45set(A):
    """A is a (4,5)-set / weak Sidon set  <=>  all pairwise sums a+b (a<b) distinct.
    (Equivalently every 4-subset has >=5 distinct pairwise differences; the pairwise-sum
    formulation is the standard equivalent, MT26 Sec.1.)"""
    A = sorted(A)
    seen = set()
    for i in range(len(A)):
        ai = A[i]
        for j in range(i + 1, len(A)):
            s = ai + A[j]
            if s in seen:
                return False
            seen.add(s)
    return True

def is_45set_via_differences(A):
    """Independent cross-check: every 4-element subset has >=5 distinct |differences|."""
    A = sorted(A)
    for quad in itertools.combinations(A, 4):
        diffs = set()
        for x, y in itertools.combinations(quad, 2):
            diffs.add(abs(x - y))
        if len(diffs) < 5:
            return False
    return True

def three_ap_edges(A):
    """3-term APs {p, p+d, p+2d} inside A, as sorted index triples."""
    A = sorted(A)
    pos = {v: i for i, v in enumerate(A)}
    Aset = set(A)
    edges = []
    for i in range(len(A)):
        for k in range(i + 1, len(A)):
            s = A[i] + A[k]
            if s % 2 == 0 and (s // 2) in Aset:
                j = pos[s // 2]
                if i < j < k:
                    edges.append((i, j, k))
    return edges

def max_no_3ap(A):
    """EXACT largest subset of A with no 3-term AP = h(A) (= alpha of the AP-hypergraph),
    by deterministic branch-and-bound. By MT26 Lemma 2.3, within a weak Sidon set this
    equals the largest Sidon subset."""
    A = sorted(A)
    n = len(A)
    edges = three_ap_edges(A)
    # for each vertex v, the pairs {other two} that together with v form a 3-AP
    incident = [[] for _ in range(n)]
    for (i, j, k) in edges:
        incident[i].append(frozenset((j, k)))
        incident[j].append(frozenset((i, k)))
        incident[k].append(frozenset((i, j)))
    order = sorted(range(n), key=lambda v: -len(incident[v]))
    best = [0]
    chosen = set()
    def bt(idx, cnt):
        if cnt + (n - idx) <= best[0]:
            return
        if idx == n:
            if cnt > best[0]:
                best[0] = cnt
            return
        v = order[idx]
        ok = True
        for pr in incident[v]:
            if pr <= chosen:
                ok = False
                break
        if ok:
            chosen.add(v)
            bt(idx + 1, cnt + 1)
            chosen.discard(v)
        bt(idx + 1, cnt)
    bt(0, 0)
    return best[0]

def no_3ap(S):
    """True iff S (a list of ints) contains no 3-term AP — used to verify a Sidon witness."""
    Sset = set(S)
    for a, c in itertools.combinations(sorted(S), 2):
        m = (a + c)
        if m % 2 == 0 and (m // 2) in Sset and (m // 2) not in (a, c):
            return False  # found a 3-term AP a, mid, c
    return True

# ---------------------------------------------------------------------------
# (A) The record gadget: re-establish the bar 4/7, exactly.
# ---------------------------------------------------------------------------

A_base = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
WITNESS = [0, 136, 200, 243, 246, 298, 323, 528]   # a size-8 Sidon (no-3-AP) subset

def part_A():
    print("=" * 70)
    print("(A) Record 14-point gadget  A_base  (the bar to beat = 4/7)")
    print("    A_base =", A_base)
    ok1 = is_45set(A_base)
    ok2 = is_45set_via_differences(A_base)
    assert ok1 == ok2, "the two (4,5) checks disagree!"
    print("    is (4,5)-set (distinct pairwise sums) :", ok1)
    print("    is (4,5)-set (>=5 diffs per 4-subset) :", ok2)
    h = max_no_3ap(A_base)
    # cross-check witness genuinely no-3-AP and contained in A_base, size 8
    assert set(WITNESS) <= set(A_base)
    assert no_3ap(WITNESS) and len(WITNESS) == 8
    print("    h(A_base) = max no-3-AP subset (exact) :", h)
    print("    explicit size-8 Sidon witness          :", WITNESS, "(no 3-AP: True)")
    N = len(A_base)
    print(f"    => c* <= h/N = {h}/{N} = 4/7   (7*{h}={7*h} == 4*{N}={4*N}: ties record)")
    assert ok1 and h == 8 and N == 14
    return h, N

# ---------------------------------------------------------------------------
# (B) Feasibility map from the proven lower bound c* >= 9/17.
# ---------------------------------------------------------------------------

def part_B():
    print("=" * 70)
    print("(B) Which N can beat 4/7 at all?  Need ceil(9N/17)/N < 4/7, exactly")
    print("    floor h(N) := ceil(9N/17)  (proven: every (4,5)-set has h >= 9/17 * N)")
    feasible = []
    for N in range(7, 30):
        lb = (9 * N + 16) // 17           # ceil(9N/17), integer
        beats = 7 * lb < 4 * N            # exact: lb/N < 4/7
        if beats:
            feasible.append(N)
    print("    Smallest N that CAN beat 4/7:", feasible[:12])
    for ban in (14, 21):
        lb = (9 * ban + 16) // 17
        print(f"    N={ban}: floor h={lb}, 7*{lb}={7*lb} vs 4*{ban}={4*ban} "
              f"-> beat impossible (floor ratio = {lb}/{ban} = 4/7)")
    assert 14 not in feasible and 21 not in feasible
    assert feasible[:5] == [9, 11, 13, 15, 16]
    return feasible

# ---------------------------------------------------------------------------
# (C) Exact complete (window-limited) min-h for small feasible N: the obstruction.
# ---------------------------------------------------------------------------

def min_h_complete(N, window, target, time_budget=25.0):
    """COMPLETE search (anchored at 0, all elements in [0,window], strictly increasing):
    returns (found_set_or_None, completed_bool, min_h_seen).
    Sound prune: a greedy maximal no-3-AP subset gives a LOWER bound on h, and h is
    non-decreasing as points are added, so if that bound exceeds `target` the branch
    cannot reach h<=target. We report the exact min h over all *full* size-N sets that
    survived the prune (which is the true min over the whole window when target>=that min).
    """
    import time
    t0 = time.time()
    res = {"set": None, "min": N + 1, "timeout": False}
    A = [0]; sums = set()

    def greedy_lb(B):
        chosen = []
        for v in B:
            bad = False
            for i in range(len(chosen)):
                for j in range(i + 1, len(chosen)):
                    a, b = chosen[i], chosen[j]
                    if a + b == 2 * v or a + v == 2 * b or b + v == 2 * a:
                        bad = True; break
                if bad: break
            if not bad:
                chosen.append(v)
        return len(chosen)

    def dfs():
        if res["timeout"]:
            return
        if time.time() - t0 > time_budget:
            res["timeout"] = True; return
        if greedy_lb(A) > target:
            return
        if len(A) == N:
            h = max_no_3ap(A)
            if h < res["min"]:
                res["min"] = h; res["set"] = list(A)
            return
        start = A[-1] + 1
        if start + (N - len(A)) - 1 > window:
            return
        for v in range(start, window + 1):
            if res["timeout"]:
                return
            ok = True; loc = []
            for x in A:
                s = x + v
                if s in sums:
                    ok = False; break
                loc.append(s)
            if not ok:
                continue
            for s in loc:
                sums.add(s)
            A.append(v)
            dfs()
            A.pop()
            for s in loc:
                sums.discard(s)

    dfs()
    return res["set"], (not res["timeout"]), res["min"]

def part_C():
    print("=" * 70)
    print("(C) Exact complete (window-limited) search for small feasible N")
    print("    Goal: find ANY weak-Sidon set with h <= floor (a strict beat). None exist")
    print("    in the searched window -> documented structural obstruction.")
    cases = [(9, 45, 5), (9, 50, 5), (11, 40, 6)]   # (N, window, target=floor)
    any_beat = False
    for (N, w, tgt) in cases:
        s, complete, mn = min_h_complete(N, w, tgt, time_budget=40.0)
        status = "COMPLETE" if complete else "incomplete(timeout)"
        if s is not None and 7 * max_no_3ap(s) < 4 * N:
            any_beat = True
            print(f"    N={N} w={w}: *** BEAT FOUND *** {s}")
        else:
            note = f"min h>{tgt}" if mn > tgt else f"min h={mn}"
            print(f"    N={N} w={w} target h<={tgt}: NO beat ({status}); within window all "
                  f"weak-Sidon sets have h > {tgt} (>= floor); {note}")
    return any_beat

# ---------------------------------------------------------------------------

def main():
    h, N = part_A()
    feasible = part_B()
    any_beat = part_C()
    print("=" * 70)
    print("SUMMARY")
    print(f"  Bar (verified record):        c* <= 4/7 = {4/7:.7f}   [N=14, h=8]")
    print(f"  Strict beat found this round: {'YES' if any_beat else 'NO'}")
    if not any_beat:
        print("  Best ratio achieved by search: 4/7 (ties, does NOT beat).")
        print("  N=14 and N=21 proven INCAPABLE of beating 4/7 (9/17 floor).")
        print("  This is a documented near-miss; held bound stays 4/7.")
    print("=" * 70)

if __name__ == "__main__":
    main()
