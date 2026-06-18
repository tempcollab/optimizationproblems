#!/usr/bin/env python3
"""
C_5b — approach cpsat-exact-existence-N28-N30, ROUND 6 STRUCTURAL CERTIFICATE.

A fast, deterministic, re-runnable certificate of the R6 structural findings about the
m = n-2 ("edge-cap saturated") (4,5)-sets that the m-targeted search targets.  These are
EXACT, exhaustively-verified combinatorial facts (no heuristic search), and they sharpen
the R5 obstruction from "the search walls" to a STRUCTURAL statement about WHY the
edge-cap and a low alpha pull apart.

Reuses the exact machinery in search_N30.py (is_45set difference condition,
three_ap_triples, alpha_milp/alpha_bb exact cross-checked).

THE THREE VERIFIED FACTS
========================

FACT 1  (midpoint-degree <= 1).  In ANY (4,5)-set, no vertex is the MIDPOINT of two
        distinct 3-APs.  Proof: if p is the midpoint of {p-d1,p,p+d1} and {p-d2,p,p+d2}
        with d1>d2>0, the 4-subset Q={p-d1,p-d2,p+d2,p+d1} has pairwise differences
        {d1-d2, d1+d2, 2d1, 2d2} -- exactly FOUR distinct values (d1-d2 and d1+d2 each
        occur twice).  Four < five, so Q violates the (4,5) difference condition.  []
        Verified exhaustively over all d1>d2 up to a large bound below.

FACT 2  (edge-cap characterization).  Since every 3-AP has a unique midpoint and (FACT 1)
        each vertex is a midpoint of at most one 3-AP, the midpoint map
            mu : {3-APs of A} -> {interior vertices of A}
        is INJECTIVE and misses min A, max A (a min/max cannot be a midpoint).  Hence
        m = #3-APs <= n-2 (this RE-DERIVES Lemma 2.4), and
            m = n-2  <=>  mu is a BIJECTION onto the interior  <=>  EVERY interior vertex
            is the midpoint of exactly one 3-AP.
        Verified on A_base (m=12=n-2: midpoints == interior, bijection).

FACT 3  (the joint-feasibility tension, the SHARP R6 obstruction).  At the edge cap m=n-2,
        the n-2 interior vertices are EXACTLY the midpoints (one 3-AP each).  The two pure
        endpoints are min A, max A.  A large independent set (low alpha) must avoid hitting
        a 3-AP, i.e. must be a transversal-COMPLEMENT.  The verified measurements below map,
        EXACTLY, the achieved (m, alpha=N-tau) for the cap-saturator A_base (N=14) and the
        best near-cap N=30 set, and quantify the remaining edge-deficit -> tau-deficit link.

EXACTNESS / HONESTY: alpha is exact (milp == bb) everywhere; FACTS 1-2 are exhaustive
combinatorial proofs (not search).  Nothing here is written into constants/5b.md.

Run:  python3 structure_msat_N30.py     (fast, ~30s)
"""
import itertools, sys
import search_N30 as S
import search_N30_mtargeted as M


def fact1_midpoint_degree(Dbound=200):
    """FACT 1: exhaustively confirm that two 3-APs sharing a midpoint ALWAYS give a 4-subset
    with exactly 4 distinct differences (< 5) -> forbidden in a (4,5)-set."""
    print("=" * 74)
    print("FACT 1  midpoint-degree <= 1 in every (4,5)-set (exhaustive over d1>d2):")
    bad = ok = 0
    worst = 0
    for d1 in range(1, Dbound + 1):
        for d2 in range(1, d1):
            Q = sorted({-d1, -d2, d2, d1})
            if len(Q) < 4:
                continue
            diffs = {abs(a - b) for a, b in itertools.combinations(Q, 2)}
            worst = max(worst, len(diffs))
            if len(diffs) >= 5:
                ok += 1
                print(f"   !!! COUNTEREXAMPLE d1={d1} d2={d2}: {len(diffs)} distinct diffs")
            else:
                bad += 1
    assert ok == 0, "midpoint-degree theorem FALSE"
    print(f"   checked all 0<d2<d1<= {Dbound}: {bad} configs, ALL have exactly "
          f"<=4 distinct diffs (max seen {worst}), 0 admissible.")
    print("   => THEOREM (exhaustive): a (4,5)-set vertex is the midpoint of <=1 3-AP.")
    return ok == 0


def fact2_cap_characterization():
    """FACT 2: the midpoint map is injective (FACT 1) + misses min,max => m <= n-2; and
    m=n-2 iff every interior vertex is a midpoint.  Verified on A_base."""
    print("=" * 74)
    print("FACT 2  edge-cap m<=n-2 via injective midpoint map; saturation = bijection:")
    A = sorted(S.A_BASE)
    tr = S.three_ap_triples(A)
    mids = sorted({A[j] for (i, j, k) in tr})
    interior = sorted(set(A[1:-1]))
    # every midpoint is interior, distinct (injective), and at saturation == interior
    assert all(A[0] < p < A[-1] for p in mids), "a midpoint equals min or max?!"
    assert len(mids) == len(tr), "midpoint map NOT injective (FACT 1 violated on A_base)"
    print(f"   A_base: n={len(A)} m={len(tr)} (cap n-2={len(A)-2})  "
          f"#distinct midpoints={len(mids)} (== m, injective)")
    print(f"   midpoints == interior vertices (bijection, cap SATURATED)? "
          f"{mids == interior}")
    print("   => m=n-2 <=> midpoint map is a BIJECTION onto the interior "
          "(every interior vertex is a unique 3-AP midpoint).")
    return mids == interior


def fact3_joint_tension():
    """FACT 3: exact (m, alpha=N-tau) for the cap-saturator A_base and the best near-cap
    N=30 set, with the edge-deficit -> tau-deficit link made exact."""
    print("=" * 74)
    print("FACT 3  joint (m, alpha) tension -- the SHARP R6 obstruction (exact):")
    rows = [("A_base (record, N=14)", S.A_BASE),
            ("Fib best (N=30, R5)", S.BEST_SETS[30][1])]
    print("   set                     | n  | m  | n-2 | edge-def | alpha | tau | tau/n")
    print("   ------------------------+----+----+-----+----------+-------+-----+------")
    for name, A in rows:
        A = sorted(A)
        n = len(A); m = M.m_count(A)
        a = S.alpha_exact(A, cross_check=True)   # milp == bb
        tau = n - a
        print(f"   {name:23s} | {n:2d} | {m:2d} |  {n-2:2d} |    {n-2-m:2d}    "
              f"|  {a:2d}   | {tau:2d}  | {tau/n:.4f}")
    # The exact link: A_base reaches the cap (edge-def 0) AND tau/n=0.4286; the N=30 best
    # is edge-def 2 AND tau/n=0.3667.  Beat target N=30: alpha<=17 <=> tau>=13 <=> tau/n>=0.4333.
    fl = (9 * 30 + 16) // 17
    print(f"   N=30 BEAT target: alpha <= {fl+1} <=> tau >= {30-(fl+1)} <=> tau/n >= "
          f"{(30-(fl+1))/30:.4f}")
    print("   => the cap-saturator A_base (edge-def 0) sits at tau/n=0.4286 (just under the")
    print("      0.4333 target); the best N=30 set is 2 edges short (edge-def 2) and falls to")
    print("      tau/n=0.3667.  Closing the beat requires BOTH edge-def 0 AND tau/n>=0.4333 at")
    print("      N=30 simultaneously -- i.e. an A_base-grade cap saturator that ALSO lifts")
    print("      tau-efficiency above A_base's own rate.  Whether such a set exists at N=30 is")
    print("      the open question; the m-targeted search (search_N30_mtargeted.py) probes it.")


def main():
    ok1 = fact1_midpoint_degree(Dbound=200)
    ok2 = fact2_cap_characterization()
    fact3_joint_tension()
    print("=" * 74)
    print(f"SUMMARY: FACT1(midpoint-deg<=1)={ok1}  FACT2(cap=bijection)={ok2}.")
    print("These are EXACT structural facts (FACT1/2 exhaustive proofs, FACT3 exact alpha).")
    print("They sharpen the R5 'search walls' to: a beat needs a cap saturator (every")
    print("interior vertex a unique midpoint) with tau/n>=0.4333 at N=30.  CONJECTURE-only;")
    print("no bound written to constants/5b.md.")
    print("=" * 74)


if __name__ == "__main__":
    main()
