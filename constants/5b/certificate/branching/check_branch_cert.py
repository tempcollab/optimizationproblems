#!/usr/bin/env python3
"""
Re-check script for the BRANCHING transversal certificate (C_5b, round 4).

This mirrors, in plain Python, the structurally-recursive `Bool` predicate
`noTransLe` formalized in lean/Constants/C5bBranch.lean, and re-derives the
load-bearing facts that the Lean `decide` checks:

  * noTransLe(Abase_APs, 5) == True   (no transversal of size <= 5; tau >= 6)
  * noTransLe(Abase_APs, 6) == False  (a transversal of size 6 EXISTS; tau = 6, TIGHT)

Hence the minimum transversal of A_base's 3-AP hypergraph is tau = 6 exactly,
giving the TIGHT h(A_base) = N - tau = 14 - 6 = 8 by the complement/cardinality
bridge (hLe_of_branchCert). This CLOSES the integrality gap of the fractional
certificate (which only reached h <= 9, since nu* = 4.5 < tau = 6).

It also reports the search-tree node count (must be small enough for plain
kernel `decide`).

This is a re-check aid for the reviewer; the AUTHORITATIVE certificate is the
Lean proof (lake build Constants.C5bBranch; #print axioms shows no sorryAx,
no native_decide, only propext/Classical.choice/Quot.sound).
"""

import sys
sys.setrecursionlimit(1_000_000)

# The 14-point record gadget A_base (h = 8) and its twelve 3-term APs
# (verified in lean/Constants/C5b.lean and C5bTransversal.lean).
ABASE = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
APS = [
    (0, 136, 272), (0, 200, 400), (0, 298, 596), (0, 528, 1056),
    (136, 596, 1056), (200, 243, 286), (200, 249, 298), (243, 246, 249),
    (246, 272, 298), (246, 323, 400), (249, 286, 323), (272, 400, 528),
]


def is_ap(t):
    a, b, c = t
    return (a + c == 2 * b) and a != b and b != c and a != c


def remove_vertex(edges, v):
    """removeVertex: drop every edge through v (matches the Lean filter)."""
    return [e for e in edges if v not in e]


def no_trans_le(edges, budget):
    """noTransLe: True iff NO vertex set of size <= budget hits all edges."""
    if not edges:                # FW = [] : empty set hits all -> transversal exists
        return False
    if budget == 0:              # FW nonempty, no budget -> none hits
        return True
    a, b, c = edges[0]           # branch on the first edge's 3 vertices
    return all(no_trans_le(remove_vertex(edges, v), budget - 1) for v in (a, b, c))


def count_nodes(edges, budget):
    n = 1
    if not edges or budget == 0:
        return n
    a, b, c = edges[0]
    for v in (a, b, c):
        n += count_nodes(remove_vertex(edges, v), budget - 1)
    return n


def brute_min_transversal(edges, verts):
    """Exact min hitting set by increasing size (independent cross-check of tau)."""
    from itertools import combinations
    for k in range(0, len(verts) + 1):
        for H in combinations(verts, k):
            Hs = set(H)
            if all(any(v in Hs for v in e) for e in edges):
                return k, set(H)
    return None, None


def main():
    ok = True

    # (0) every listed edge is a genuine non-degenerate 3-AP inside A_base.
    for t in APS:
        assert is_ap(t), f"not a 3-AP: {t}"
        assert all(x in ABASE for x in t), f"vertex outside A_base: {t}"
    assert len(APS) == 12, "expected 12 APs"
    print(f"[ok] 12 genuine 3-term APs of A_base, all vertices in A_base")

    # (1) the load-bearing decide facts
    c5 = no_trans_le(APS, 5)
    c6 = no_trans_le(APS, 6)
    print(f"noTransLe(APS, 5) = {c5}   (Lean Abase_branch_tau: expect True)")
    print(f"noTransLe(APS, 6) = {c6}   (expect False: size-6 transversal exists)")
    ok &= (c5 is True) and (c6 is False)

    # (2) search-tree size (must be tiny for plain `decide`)
    nodes = count_nodes(APS, 5)
    print(f"branching tree nodes at budget 5 = {nodes}   (worst case 3^5 = 243 leaves)")
    ok &= nodes < 10_000

    # (3) independent exact min-transversal cross-check (tau = 6)
    tau, H = brute_min_transversal(APS, ABASE)
    print(f"exact min transversal tau = {tau}   witness = {sorted(H)}")
    ok &= (tau == 6)

    # (4) the bound it certifies
    N = len(ABASE)
    h_branch = N - tau            # tight: 14 - 6 = 8
    print(f"=> h(A_base) <= N - tau = {N} - {tau} = {h_branch}   (TIGHT; fractional gave 9)")
    ok &= (h_branch == 8)

    print()
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
