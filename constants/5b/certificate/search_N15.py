#!/usr/bin/env python3
"""
C_5b — transversal-ilp-floor-search-N15.

GOAL: find a 15-point (4,5)-set A with h(A) = 8, where h(A) = size of the largest
      Sidon subset = independence number alpha of the 3-AP hypergraph (MT26 Lemma 2.3,
      valid since a (4,5)-set is in particular a weak Sidon set). Such a set would give
      c* <= 8/15 = 0.5333... < 4/7 -- a strict beat of the verified record.

The proven floor c* >= 9/17 forces h(A) >= ceil(9*15/17) = ceil(135/17) = 8 at N=15,
so 8 is the FLOOR -- it must be hit EXACTLY. h(A) = 9 gives 9/15 = 0.6 > 4/7 (no beat).

*** SPEC CORRECTION (round 2). *** The round-1 digest claimed a (4,5)-set is EQUIVALENT
to a weak Sidon set ('all pairwise sums distinct'). That is FALSE. Verified against the
arXiv:2602.23282 abstract: a (4,5)-set is the DIFFERENCE condition -- every 4-element
subset has >=5 distinct pairwise absolute differences. This is STRICTLY STRONGER than
weak-Sidon ({0,1,2,4} has distinct sums but only 4 distinct diffs). is_45set below now
uses the CORRECT difference definition. (The round-1 record set A_base satisfies BOTH,
so the round-1 4/7 reproduction is still a valid bound -- but the Lean engine's
`weakSidonB` predicate certifies the WEAKER property and must be tightened before any
NEW gadget is trusted. Flagged in the build report.)

OUTCOME (round 2): NO 15-point (4,5)-set with h <= 8 was found. The realized minimum
across all methods (exact-alpha annealing 30 seeds / multiple move-sets / windows up to
1e7; single-point extension of A_base; dense small-span enumeration; CP-SAT max-#3AP
proposer) was h = 10, ratio 10/15 = 0.667 > 4/7. No strict beat this round.

ALL verification arithmetic is exact integer. The CP-SAT / annealing are only proposers;
the exact alpha B&B (max_no_3ap) and the exact is_45set are the arbiters.
"""
import itertools, sys, time, random

# ----------------------------------------------------------------------------
# Exact primitives (integer arithmetic only) -- shared with the N14 cert.
# ----------------------------------------------------------------------------

def is_45set(A):
    """TRUE (4,5)-set definition (Ma-Tang 2026, verified against arXiv:2602.23282
    abstract): EVERY 4-element subset determines AT LEAST 5 distinct values among its
    6 pairwise ABSOLUTE DIFFERENCES.

    SPEC CORRECTION (round 2): the round-1 digest claimed this is EQUIVALENT to 'all
    pairwise sums distinct' (weak Sidon). IT IS NOT. >=5-distinct-diffs is STRICTLY
    STRONGER than weak-Sidon: e.g. {0,1,2,4} has distinct sums {1,2,3,4,5,6} but only 4
    distinct diffs {1,2,3,4}. The implication is one-way: (4,5)-set ==> weak Sidon, not
    conversely. C_5b is defined over (4,5)-sets (the difference condition), so THIS is
    the predicate the bound must use."""
    A = sorted(A)
    for quad in itertools.combinations(A, 4):
        diffs = set(abs(x - y) for x, y in itertools.combinations(quad, 2))
        if len(diffs) < 5:
            return False
    return True

def is_weak_sidon(A):
    """The WEAKER 'weak Sidon' property: all pairwise sums a+b (a<b) distinct.
    Implied by, but NOT equivalent to, the (4,5)-set property above. Kept only for
    cross-reference; the search uses is_45set (the true difference condition)."""
    A = sorted(A)
    seen = set()
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            s = A[i] + A[j]
            if s in seen:
                return False
            seen.add(s)
    return True

def is_45set_via_differences(A):
    """Alias of is_45set (the >=5-distinct-diffs definition); kept for older callers."""
    return is_45set(A)

def three_ap_triples(A):
    """3-term APs {a, mid, c} inside A, as sorted index triples (i<j<k)."""
    A = sorted(A)
    pos = {v: i for i, v in enumerate(A)}
    Aset = set(A)
    triples = []
    for i in range(len(A)):
        for k in range(i + 1, len(A)):
            s = A[i] + A[k]
            if s % 2 == 0 and (s // 2) in Aset:
                j = pos[s // 2]
                if i < j < k:
                    triples.append((i, j, k))
    return triples

def max_no_3ap(A):
    """EXACT alpha = h(A): largest no-3-AP subset, deterministic branch and bound."""
    A = sorted(A)
    n = len(A)
    triples = three_ap_triples(A)
    incident = [[] for _ in range(n)]
    for (i, j, k) in triples:
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

def witness_no_3ap(A):
    """Return an explicit max no-3-AP subset (the Sidon witness) of A."""
    A = sorted(A)
    n = len(A)
    triples = three_ap_triples(A)
    incident = [[] for _ in range(n)]
    for (i, j, k) in triples:
        incident[i].append(frozenset((j, k)))
        incident[j].append(frozenset((i, k)))
        incident[k].append(frozenset((i, j)))
    order = sorted(range(n), key=lambda v: -len(incident[v]))
    best = [0]; bestset = [None]
    chosen = set()
    def bt(idx, cnt):
        if cnt + (n - idx) <= best[0]:
            return
        if idx == n:
            if cnt > best[0]:
                best[0] = cnt; bestset[0] = set(chosen)
            return
        v = order[idx]
        ok = all(not (pr <= chosen) for pr in incident[v])
        if ok:
            chosen.add(v); bt(idx + 1, cnt + 1); chosen.discard(v)
        bt(idx + 1, cnt)
    bt(0, 0)
    return sorted(A[i] for i in bestset[0])

def no_3ap(S):
    Sset = set(S)
    for a, c in itertools.combinations(sorted(S), 2):
        m = a + c
        if m % 2 == 0 and (m // 2) in Sset and (m // 2) not in (a, c):
            return False
    return True

# ----------------------------------------------------------------------------
# Local search: seed + hill-climb minimizing exact alpha, keeping weak-Sidon.
# ----------------------------------------------------------------------------

def random_weak_sidon(N, window, rng, tries=2000):
    """Build a weak-Sidon set greedily with random additions."""
    for _ in range(tries):
        A = [0]
        sums = set()
        cand = list(range(1, window + 1))
        rng.shuffle(cand)
        for v in cand:
            ok = True
            loc = []
            for x in A:
                s = x + v
                if s in sums:
                    ok = False; break
                loc.append(s)
            if ok:
                for s in loc:
                    sums.add(s)
                A.append(v)
                if len(A) == N:
                    return sorted(A)
    return None

def hill_climb(A0, window, rng, iters=4000, time_budget=20.0):
    """Move one point at a time to reduce exact alpha while staying weak-Sidon."""
    t0 = time.time()
    A = sorted(A0)
    bestA = list(A); besth = max_no_3ap(A)
    N = len(A)
    for it in range(iters):
        if time.time() - t0 > time_budget:
            break
        if besth <= 8:
            break
        i = rng.randrange(N)
        # try replacing A[i] with a new value v keeping weak-Sidon
        rest = A[:i] + A[i+1:]
        v = rng.randint(0, window)
        if v in rest:
            continue
        cand = sorted(rest + [v])
        if not is_45set(cand):
            continue
        h = max_no_3ap(cand)
        if h <= besth:  # accept equal-or-better (plateau move)
            A = cand
            if h < besth:
                besth = h; bestA = list(A)
    return bestA, besth

def search_local(N=15, target=8, window=70, seconds=120, seed=12345):
    rng = random.Random(seed)
    t0 = time.time()
    best = (99, None)
    restarts = 0
    while time.time() - t0 < seconds:
        restarts += 1
        A0 = random_weak_sidon(N, window, rng)
        if A0 is None:
            continue
        A, h = hill_climb(A0, window, rng, time_budget=min(15.0, seconds - (time.time()-t0)))
        if h < best[0]:
            best = (h, list(A))
            print(f"  [local] restart {restarts}: new best h={h}  set={A}")
            if h <= target:
                return best, restarts
    print(f"  [local] {restarts} restarts, best h={best[0]}")
    return best, restarts

# ----------------------------------------------------------------------------
# DIRECT EXTENSION: extend the record 14-pt set to 15 pts keeping weak-Sidon & h<=8.
# This is the most promising route: A_base already has h=8 at N=14; if any single
# integer can be added preserving weak-Sidon WITHOUT raising alpha above 8, done.
# ----------------------------------------------------------------------------

A_BASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]

def search_extend(base, window_lo=-2000, window_hi=4000, target=8):
    """Try adding each integer v (not already present) to `base`; keep those that
    stay weak-Sidon and have exact alpha <= target. Returns list of (set, h)."""
    hits = []
    baseset = set(base)
    for v in range(window_lo, window_hi + 1):
        if v in baseset:
            continue
        A = sorted(base + [v])
        if not is_45set(A):
            continue
        h = max_no_3ap(A)
        if h <= target:
            hits.append((A, h))
    return hits

def search_extend_any45(base, window_lo=-3000, window_hi=6000, target=8):
    """More general: also consider sets obtained by removing one base point and
    adding two new (still N=15) -- a 1-swap-plus-2 perturbation. Kept lightweight:
    only the pure single-add extension is exhaustive here; the perturbations are in
    the local search above."""
    return search_extend(base, window_lo, window_hi, target)

# ----------------------------------------------------------------------------
# CP-SAT proposer: place N points in [0,W], weak-Sidon hard, maximize #3-APs.
# Used ONLY to propose candidates; exact alpha verified off-solver.
# Many 3-APs is NECESSARY (not sufficient) for small alpha, but the solver
# packs them in OVERLAPPING patterns better than random search.
# ----------------------------------------------------------------------------

def cpsat_propose(N=15, W=80, max_solutions=200, seconds=60, seed=0, hint=None):
    from ortools.sat.python import cp_model
    m = cp_model.CpModel()
    x = [m.NewIntVar(0, W, f"x{i}") for i in range(N)]
    m.Add(x[0] == 0)
    for i in range(N - 1):
        m.Add(x[i] + 1 <= x[i + 1])  # strictly increasing
    # weak-Sidon: all pairwise sums distinct. Encode via AllDifferent on s_ij.
    sums = []
    for i in range(N):
        for j in range(i + 1, N):
            sij = m.NewIntVar(0, 2 * W, f"s_{i}_{j}")
            m.Add(sij == x[i] + x[j])
            sums.append(sij)
    m.AddAllDifferent(sums)
    # 3-AP indicator: for ordered i<j<k, b_ijk = 1 iff x[i]+x[k]==2 x[j].
    bvars = []
    for i in range(N):
        for j in range(i + 1, N):
            for k in range(j + 1, N):
                b = m.NewBoolVar(f"b_{i}_{j}_{k}")
                m.Add(x[i] + x[k] == 2 * x[j]).OnlyEnforceIf(b)
                m.Add(x[i] + x[k] != 2 * x[j]).OnlyEnforceIf(b.Not())
                bvars.append(b)
    m.Maximize(sum(bvars))
    if hint is not None:
        for i, v in enumerate(hint):
            m.AddHint(x[i], v)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.random_seed = seed
    solver.parameters.num_search_workers = 8
    st = solver.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        A = sorted(solver.Value(xi) for xi in x)
        return A, int(solver.ObjectiveValue())
    return None, None

def cpsat_search(N=15, target=8, windows=(50, 60, 70, 90), seconds_each=60):
    """Run CP-SAT proposer over windows, collect+verify candidates, return best."""
    best = (99, None)
    for W in windows:
        for sd in range(3):
            A, nap = cpsat_propose(N=N, W=W, seconds=seconds_each, seed=sd)
            if A is None:
                continue
            assert is_45set(A), "CP-SAT returned non-weak-Sidon!"
            h = max_no_3ap(A)
            print(f"  [cpsat] W={W} seed={sd}: #3AP={nap} alpha={h} set={A}")
            if h < best[0]:
                best = (h, list(A))
            if h <= target:
                return best
    return best

# ----------------------------------------------------------------------------
# CEGAR: directly search for a weak-Sidon N-set with exact alpha <= target.
# Model: x[0..N-1] strictly increasing in [0,W], weak-Sidon (AllDifferent sums),
# b_ijk = (x[i]+x[k]==2 x[j]) for i<j<k. We add, lazily, for each "bad" 9-subset S
# of positions found to be independent, the clause: OR_{triple in S} b_triple
# (S must contain a 3-AP). Loop until alpha<=target or infeasible/timeout.
# ----------------------------------------------------------------------------

def cegar_search(N=15, target=8, W=130, max_iters=4000, seconds_total=300,
                 per_solve=15, seed=0, verbose=True):
    from ortools.sat.python import cp_model
    import time
    t0 = time.time()
    m = cp_model.CpModel()
    x = [m.NewIntVar(0, W, f"x{i}") for i in range(N)]
    m.Add(x[0] == 0)
    for i in range(N - 1):
        m.Add(x[i] + 1 <= x[i + 1])
    sums = []
    for i in range(N):
        for j in range(i + 1, N):
            sij = m.NewIntVar(0, 2 * W, f"s_{i}_{j}")
            m.Add(sij == x[i] + x[j])
            sums.append(sij)
    m.AddAllDifferent(sums)
    # b_ijk for all i<j<k (these are the only possible 3-AP carriers given sorted x)
    b = {}
    for i in range(N):
        for j in range(i + 1, N):
            for k in range(j + 1, N):
                bv = m.NewBoolVar(f"b_{i}_{j}_{k}")
                m.Add(x[i] + x[k] == 2 * x[j]).OnlyEnforceIf(bv)
                m.Add(x[i] + x[k] != 2 * x[j]).OnlyEnforceIf(bv.Not())
                b[(i, j, k)] = bv
    # encourage many APs as a soft objective to bias toward small alpha
    m.Maximize(sum(b.values()))

    def triples_in(S):
        S = sorted(S)
        out = []
        for a in range(len(S)):
            for bb in range(a + 1, len(S)):
                for c in range(bb + 1, len(S)):
                    out.append((S[a], S[bb], S[c]))
        return out

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 8
    added = 0
    for it in range(max_iters):
        if time.time() - t0 > seconds_total:
            if verbose: print(f"  [cegar] timeout after {it} iters, {added} cuts")
            return None
        solver.parameters.max_time_in_seconds = min(per_solve, seconds_total - (time.time()-t0))
        solver.parameters.random_seed = seed + it
        st = solver.Solve(m)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            if verbose: print(f"  [cegar] model INFEASIBLE/unknown at iter {it}, status={st}")
            return None
        A = sorted(solver.Value(xi) for xi in x)
        assert is_45set(A), "weak-Sidon violated by solver!"
        h = max_no_3ap(A)
        if verbose and it % 1 == 0:
            print(f"  [cegar] iter {it}: alpha={h} cuts={added} #3AP={int(solver.ObjectiveValue())}")
        if h <= target:
            if verbose: print(f"  [cegar] *** FOUND alpha={h} <= {target}: {A}")
            return A
        # extract an independent (no-3-AP) subset of size target+1 by position, add cut
        W9 = witness_no_3ap(A)            # max no-3-AP subset (size = h > target)
        # take positions of the first target+1 elements of the witness
        pos = {v: idx for idx, v in enumerate(A)}
        wpos = sorted(pos[v] for v in W9)[:target + 1]
        clause = [b[t] for t in triples_in(wpos)]
        m.AddBoolOr(clause)
        added += 1
    if verbose: print(f"  [cegar] hit max_iters, {added} cuts, last alpha={h}")
    return None

# ----------------------------------------------------------------------------
# REPRODUCIBLE SUMMARY (deterministic, fast). Records the round-2 outcome:
# NO 15-point (4,5)-set with h=8 (the 9/17 floor) was found. The best realized
# h across all methods was 10 (ratio 10/15 = 0.667 > 4/7 = 0.571), so N=15 did
# NOT beat the record this round. This re-verifies the headline facts exactly.
# ----------------------------------------------------------------------------

# Best (lowest-alpha) GENUINE (4,5)-set (>=5-diff definition) found this round,
# alpha = h = 10. (Verified is_45set True under the corrected difference definition.)
BEST_N15 = [20, 24, 25, 79, 86, 133, 148, 191, 212, 233, 242, 269, 459, 590, 1160]

# A deterministic, reproducible small-span witness (greedy build, no randomness):
# a genuine (4,5)-set with h = 11 -- documents that even the canonical greedy set is
# far above the floor 8.
GREEDY_N15 = [0, 1, 2, 5, 8, 15, 24, 33, 44, 61, 73, 99, 120, 147, 174]

def main():
    print("=" * 72)
    print("C_5b  transversal-ilp-floor-search-N15  (round 2)")
    print("Target: a 15-point (4,5)-set with h = 8  =>  c* <= 8/15 = 0.5333 < 4/7.")
    print("=" * 72)
    N = 15
    floor = (9 * N + 16) // 17          # ceil(9N/17)
    print(f"  (4,5)-set = every 4-subset has >=5 distinct pairwise differences")
    print(f"            (CORRECTED def, arXiv:2602.23282; NOT just 'sums distinct').")
    print(f"  9/17 lower bound forces h >= ceil(9*{N}/17) = {floor} (the FLOOR).")
    print(f"  A beat needs h = {floor} exactly: {floor}/{N} = {floor/N:.4f} < 4/7 = {4/7:.4f}.")
    print(f"  h = 9 would give 9/15 = {9/15:.4f} > 4/7 -> does NOT beat.")
    print("-" * 72)
    # sanity: the record set IS a genuine (4,5)-set under the corrected definition.
    assert is_45set(A_BASE) and max_no_3ap(A_BASE) == 8
    # sanity: a sums-distinct set need NOT be a (4,5)-set (the round-1 conflation).
    bad = [0, 1, 2, 4, 7, 12, 23, 46, 60, 74, 89, 98, 107, 125, 138]
    assert is_weak_sidon(bad) and not is_45set(bad), "spec-correction sanity failed"
    print("  [spec check] A_base is a genuine (4,5)-set, h=8  :", is_45set(A_BASE))
    print("  [spec check] a weak-Sidon set can FAIL (4,5)     :",
          is_weak_sidon(bad) and not is_45set(bad), "(round-1 conflation)")
    print("-" * 72)
    for label, A in (("best found (h=10)", BEST_N15), ("greedy (h=11)", GREEDY_N15)):
        ok = is_45set(A)
        ws = is_weak_sidon(A)
        h = max_no_3ap(A)
        w = witness_no_3ap(A)
        assert ok and ws and set(w) <= set(A) and no_3ap(w) and len(w) == h
        print(f"  {label}: N={len(A)}  (4,5)-set={ok}  h={h}  "
              f"ratio={h}/{N}={h/N:.4f}  beats 4/7? {7*h < 4*N}")
        print(f"    A = {A}")
        print(f"    size-{h} Sidon witness = {w}")
    print("-" * 72)
    print("  OUTCOME: NO strict beat. Best realized h = 10 (ratio 0.6667 > 4/7).")
    print("  h = 8 (the 9/17 floor) was NOT realized by ANY method tried under the")
    print("  CORRECTED (4,5)-set definition:")
    print("    - single-point extension of the record A_base: 0 extensions keep h<=8;")
    print("    - exact-alpha simulated annealing, 30 seeds, multiple move-sets, windows")
    print("      up to 1e7: wall at h = 10;")
    print("    - CP-SAT max-#3AP proposer: packs 12-13 3-APs, exact alpha stays 11-12")
    print("      (confirms round-1 lesson: edge count != small alpha);")
    print("    - dense small-span (4,5)-set enumeration: h = 10.")
    print("  Consistent with the floor-squeeze: the 9/17 floor pins admissible h to the")
    print("  single value 8 at N=15, and that value appears unreachable for N=15 in the")
    print("  searched space (the realized min sits at floor+2).")
    print("=" * 72)
    assert max_no_3ap(BEST_N15) == 10 and N == 15  # documents the non-beat

if __name__ == "__main__":
    main()
