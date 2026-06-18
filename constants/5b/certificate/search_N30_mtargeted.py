#!/usr/bin/env python3
"""
C_5b (Sidon density in (4,5)-sets, Erdos #757) — approach cpsat-exact-existence-N28-N30.
ROUND 6 EXTENSION: m as a FIRST-CLASS objective (the new lever).

This file REUSES the exact, validated machinery in search_N30.py (is_45set / the
DIFFERENCE-condition (4,5) predicate, three_ap_triples, alpha_milp + alpha_bb exact
cross-checked alpha=N-tau, block_split indecomposability) and adds the ROUND-6 lever the
R5 search never used: drive m = #(midpoint-injective 3-APs) toward the Lemma-2.4 cap
n-2, with a transversal-efficient (clustered / non-path) arrangement, BEFORE/while
minimizing alpha exactly.

WHY (verified, R6 digest constants/5b/literature/R6-lowerbound-and-target-digest.md):
  * Lemma 2.4: m <= n-2 for a weak-Sidon (hence (4,5)) set.  A_base SATURATES it
    (N=14, m=12=n-2) and is Henning-Yeo-extremal (tau=6 = HY cap).
  * The R5 best (Fibonacci subsequence) has m=26 < n-2=28 at N=30 -- an EDGE-DEFICIT of 2.
    Its tau-deficit of 2 (alpha=19=floor+3, need floor+1=17) IS that edge-deficit: a near-
    path max-degree-3 hypergraph.  A_base by contrast has a DEGREE-4 vertex (non-path).
  * The sharp beat target: an indecomposable N=30 (4,5)-set with m=n-2=28 AND tau=13 =>
    alpha = N-tau = 17 => 17/30 = 0.5667 < 4/7.  HY (17 tau <= 5n+3m) at m=28 permits
    tau <= 13.76 => tau=13 is ALLOWED, not forbidden.

WHAT THIS ROUND ADDS over R5 (all exact; alpha never an edge-count proxy):
  1. m_count / midpoint-injective edge bookkeeping and the DEGREE PROFILE (clustering).
  2. A lexicographic local search optimizing (m, -alpha) -- Stage A drives m UP toward the
     cap; alpha is the exact milp tie-break.  Replaces R5's blind min-alpha.
  3. Degree-shaping: a tertiary reward for sum_v C(deg_v, 2) (clustered midpoints, A_base's
     non-path profile) -- steers AWAY from the Fibonacci near-path that walls.
  4. An m-frozen high-m SHELL pass: collect all distinct high-m (m >= M0) (4,5)-sets the
     search visits, run EXACT alpha (milp==bb) only on that shell, and report the JOINT
     (m, alpha) frontier -- the sharper R6 deliverable: does pushing m to the cap close the
     tau-deficit, or is (m near n-2) AND (alpha=floor+1) JOINTLY infeasible at N=30?

EXACTNESS / HONESTY (CLAUDE.md rigor, unchanged from R5):
  * (4,5) by the DIFFERENCE condition (every 4-subset >=5 distinct |diffs|), exact.
  * alpha = N - tau exact via scipy.milp, cross-checked by the alpha_bb branch-and-bound.
  * A found gadget is a CONJECTURE until the Lean cert fires; this script writes NOTHING
    into constants/5b.md.  Deliverable: a re-runnable candidate-or-(joint-infeasibility)
    obstruction map.

Run:  python3 search_N30_mtargeted.py            (fast reproducible summary, ~1 min)
      python3 search_N30_mtargeted.py --search   (heavy m-targeted search, deterministic)
"""
import itertools, random, sys, time
import numpy as np

import search_N30 as S   # reuse the exact, validated R5 machinery


# ---------------------------------------------------------------------------
# m (midpoint-injective 3-AP count) and the degree profile of the 3-AP hypergraph.
# ---------------------------------------------------------------------------

def m_count(A):
    """Number of 3-term APs (midpoint-injective 3-APs) inside A = #edges of H(A).
    By Lemma 2.4 this is <= n-2 for a weak-Sidon (hence (4,5)) set."""
    return len(S.three_ap_triples(A))


def degree_profile(A):
    """Degree sequence of the 3-AP hypergraph (sorted desc).  A_base has a degree-4
    vertex (non-path); the Fibonacci family is max-degree-3 (near-path)."""
    tr = S.three_ap_triples(A)
    n = len(A)
    deg = [0] * n
    for (i, j, k) in tr:
        deg[i] += 1; deg[j] += 1; deg[k] += 1
    return sorted(deg, reverse=True)


def cluster_score(A):
    """sum_v C(deg_v, 2): rewards clustered (high-degree) midpoints -- A_base's non-path
    structure.  A near-path (all deg<=3) scores low; A_base's degree-4 vertex contributes
    C(4,2)=6.  Used as the tertiary (degree-shaping) reward in the lexicographic search."""
    return sum(d * (d - 1) // 2 for d in degree_profile(A))


def m_add_gain(A_sorted, v):
    """How many NEW 3-APs appear when adding v to the (4,5)-set A_sorted.  Counts triples
    {a, b, v} that form an AP: either v is an endpoint (other endpoint 2*mid - a in A) or
    v is the midpoint (a + c = 2v).  Cheap incremental m bookkeeping for the search."""
    Aset = set(A_sorted)
    gain = 0
    n = len(A_sorted)
    # v as midpoint: pairs (a, c) in A with a + c = 2v
    for a in A_sorted:
        c = 2 * v - a
        if c > a and c in Aset:
            gain += 1
    # v as endpoint: for each b in A, the AP {v, b, 2b - v} or {2b - v, b, v}
    for b in A_sorted:
        # b is the midpoint between v and (2b - v)
        other = 2 * b - v
        if other != v and other in Aset and other > v:
            # AP {v, b, other} with v < b? need v<b<other or other<b<v; this is the
            # "v endpoint, b midpoint" case -- count to avoid double counting with above
            if (v < b < other) or (other < b < v):
                gain += 1
    return gain


# ---------------------------------------------------------------------------
# Lexicographic objective: (m, cluster, -alpha).  We MAXIMIZE m first (drive to the
# cap), then cluster (degree shaping), then MINIMIZE alpha (exact, milp).  alpha is only
# the tie-break / final arbiter -- never the steering edge-count.
# ---------------------------------------------------------------------------

def lex_key(A, use_alpha=True):
    """Lexicographic score for a (4,5)-set A: (m, cluster_score, -alpha_exact).
    Higher is better.  alpha computed EXACTLY (milp) only when use_alpha (it is the
    expensive term; the m/cluster terms drive the bulk of the search)."""
    m = m_count(A)
    cl = cluster_score(A)
    if use_alpha:
        a = S.alpha_milp(A)
        return (m, cl, -a)
    return (m, cl, 0)


def m_targeted_search(N, window, rng, seconds, M0=None, log=None):
    """Lexicographic (m, cluster, -alpha) local search over (4,5)-sets of size N.
    Single-point REPLACEMENT moves, (4,5)-property kept EVERY move.  Returns the best
    set by lex_key AND the full set of distinct HIGH-m (m >= M0) (4,5)-sets visited
    (the shell) with their EXACT (m, alpha) so part-2 can map the joint frontier.

    The search is deterministic (seeded rng).  alpha is exact (milp) on accepted
    improving moves and on the final shell; the bulk of moves use the cheap (m, cluster)
    surrogate so we explore many sets per second.
    """
    import math
    t0 = time.time()
    cap = N - 2
    if M0 is None:
        M0 = cap - 2          # the shell: m within 2 of the cap (>= n-4)
    # ---- start from the best known low-alpha basin (Fibonacci) if N matches, else greedy
    if N in S.BEST_SETS:
        A = sorted(S.BEST_SETS[N][1])
    else:
        A = S.greedy_build(N, window, rng)
        if A is None:
            A = sorted(random.sample(range(window + 1), N))
    cur_m = m_count(A)
    cur_cl = cluster_score(A)
    best_lex = lex_key(A)         # exact alpha here
    best = list(A)
    shell = {}                    # tuple(set) -> (m, alpha) exact, for high-m sets

    def record_shell(B):
        if m_count(B) >= M0 and S.is_45set(B):
            key = tuple(B)
            if key not in shell:
                a = S.alpha_exact(B, cross_check=True)   # milp == bb
                shell[key] = (m_count(B), a)

    record_shell(A)
    T = 2.5
    it = 0
    while time.time() - t0 < seconds:
        it += 1
        T *= 0.9997
        if T < 0.05:
            T = 2.5
        i = rng.randrange(N)
        rest = sorted(A[:i] + A[i + 1:])
        v = rng.randint(0, window)
        if v in rest or not S.add_keeps_45(rest, v):
            continue
        cand = sorted(rest + [v])
        # cheap surrogate score (m, cluster) -- the steering objective
        cm = m_count(cand)
        ccl = cluster_score(cand)
        # accept by lexicographic (m, cluster) with annealing on the m drop
        dm = cm - cur_m
        accept = False
        if dm > 0:
            accept = True
        elif dm == 0:
            accept = (ccl >= cur_cl) or (rng.random() < math.exp(-(cur_cl - ccl) / (4 * T)))
        else:  # m dropped -- accept rarely to escape, annealed
            accept = rng.random() < math.exp(dm / T)
        if accept:
            A = cand
            cur_m = cm
            cur_cl = ccl
            record_shell(A)
            k = lex_key(A)        # exact alpha only on accepted move
            if k > best_lex:
                best_lex = k
                best = list(A)
                if log and (k[0] > best_lex[0] - 1):
                    log(f"      [N={N}] m={k[0]} cl={k[1]} alpha={-k[2]} "
                        f"(cap m={cap}, move {it}, T={T:.2f})")
    return best, best_lex, shell


# ---------------------------------------------------------------------------
# Reproducible structural facts (fast).
# ---------------------------------------------------------------------------

def part_m_structure():
    """Re-verify the load-bearing R6 structural facts EXACTLY: A_base saturates m=n-2 and
    is non-path (degree-4); the R5 Fibonacci best is 2 edges short of the cap and is a
    near-path (max degree 3).  This is the WHOLE basis of the m-targeted lever."""
    print("=" * 74)
    print("(m-structure) the R6 lever: m vs the Lemma-2.4 cap n-2, and the degree profile")
    A = S.A_BASE
    mA = m_count(A); aA = S.alpha_exact(A)
    print(f"  A_base   N=14: m={mA} (cap n-2={len(A)-2}, SATURATED={mA == len(A)-2})  "
          f"alpha={aA} tau={len(A)-aA} (tau/N={ (len(A)-aA)/len(A):.4f})")
    print(f"           degree profile: {degree_profile(A)}  -> degree-4 vertex (NON-path)")
    print(f"           cluster_score sum C(deg,2) = {cluster_score(A)}")
    fib = S.BEST_SETS[30][1]
    mF = m_count(fib); aF = S.alpha_exact(fib)
    print(f"  Fib best N=30: m={mF} (cap n-2={len(fib)-2}, deficit={len(fib)-2-mF})  "
          f"alpha={aF} tau={len(fib)-aF} (tau/N={(len(fib)-aF)/len(fib):.4f})")
    print(f"           degree profile: {degree_profile(fib)}  -> max degree 3 (NEAR-PATH)")
    print(f"           cluster_score sum C(deg,2) = {cluster_score(fib)}")
    print("  => R6 lever: push m to the cap (28 at N=30) with A_base's clustered, non-path")
    print("     arrangement (high cluster_score), not the Fibonacci near-path.")


# Best (highest-m / lowest-alpha) GENUINE (4,5)-sets found by the m-targeted search,
# recorded for a fast deterministic summary.  CONJECTURES / obstruction witnesses, NOT
# certified bounds.  Each: exact (4,5)-set, exact (m, alpha) with milp == bb.
# (Populated by --search; the recorded entries below are the R6 m-targeted-search bests.)
MTARGET_BEST = {
    # filled in after the heavy --search run; see part_frontier.
}


def floor_h(N):
    return (9 * N + 16) // 17


def part_frontier(records=None):
    """The JOINT (m, alpha) frontier from the m-targeted shell: for each high-m level,
    the LOWEST alpha achieved.  The R6 question: as m -> cap, does alpha -> floor+1, or is
    (m near n-2, alpha=floor+1) JOINTLY infeasible at N=30?"""
    print("=" * 74)
    print("(frontier) joint (m, alpha) at N=30 -- does pushing m to the cap close the gap?")
    if records is None:
        records = MTARGET_BEST.get(30)
    cap = 30 - 2
    fl = floor_h(30)
    print(f"  N=30: cap m=n-2={cap}, floor=ceil(9N/17)={fl}, BEAT needs alpha<={fl+1}=17 "
          f"(tau>=13)")
    if not records:
        print("  (no recorded frontier yet -- run with --search to populate)")
        return
    print("    m  | best alpha | tau | alpha-floor | beats 4/7?")
    print("   ----+------------+-----+-------------+-----------")
    for m in sorted(records, reverse=True):
        a = records[m]
        tau = 30 - a
        beats = 7 * a < 4 * 30
        print(f"    {m:2d} |     {a:2d}     | {tau:2d}  |   floor+{a-fl}   | "
              f"{'YES *** BEAT' if beats else 'no'}")


def main():
    do_search = "--search" in sys.argv
    part_m_structure()
    records30 = None
    if do_search:
        print("=" * 74)
        print("(search) heavy m-targeted lexicographic (m, cluster, -alpha) search")
        logf = "/tmp/search_N30_mtargeted.log"

        def log(msg):
            with open(logf, "a", buffering=1) as f:
                f.write(msg + "\n")
            print(msg, flush=True)

        for N in (30, 32, 34):
            rng = random.Random(20260618 + N)
            window = max(2200, 4 * N)
            t0 = time.time()
            best, key, shell = m_targeted_search(N, window, rng,
                                                 seconds=600, log=log)
            # joint frontier: best alpha at each m level in the shell
            frontier = {}
            for (B, (m, a)) in shell.items():
                if m not in frontier or a < frontier[m]:
                    frontier[m] = a
            bm, bcl, bna = key
            print(f"\n  N={N}: best (m={bm}, cluster={bcl}, alpha={-bna})  "
                  f"shell size={len(shell)}  time={time.time()-t0:.0f}s")
            print(f"        joint (m,alpha) frontier: {dict(sorted(frontier.items()))}")
            if N == 30:
                records30 = frontier
    part_frontier(records30)
    print("=" * 74)
    print("STATUS: m-targeted gadget search (R6 lever).  A candidate is a CONJECTURE until")
    print("        the Lean cert fires; no bound is written into constants/5b.md here.")
    print("=" * 74)


if __name__ == "__main__":
    main()
