#!/usr/bin/env python3
"""
Independent cross-check of the `diffs4B` permutation-invariance claim formalized in
lean/Constants/C5bBridgePerm.lean (theorems `diffs4B_perm4`, `is45setB_to_Is45`).

`diffs4B a b c d` returns True iff the 4-point set {a,b,c,d} has >= 5 distinct pairwise
absolute differences |x - y| (the (4,5)-set difference condition on that 4-subset).

The Lean proof shows `diffs4B` is invariant under ALL 24 orderings of its four arguments
(via `countDistinct_perm` + a compositional pairwise-diff multiset `pdiffs`).  Here we
re-establish the same fact by brute force: for many sample quadruples, `diffs4B` must be
CONSTANT across all 24 permutations of (a,b,c,d).

Run:  python3 check_perm_invariance.py
Expect: "ALL PASS" with both passing and failing quadruples covered.
"""
from itertools import permutations
import random


def diffs4B(a, b, c, d):
    pts = [a, b, c, d]
    diffs = set()
    for i in range(4):
        for j in range(i + 1, 4):
            diffs.add(abs(pts[i] - pts[j]))
    return len(diffs) >= 5


def constant_across_orderings(quad):
    vals = {diffs4B(*p) for p in permutations(quad)}
    return len(vals) == 1, vals


def main():
    # Hand-picked anchors:
    anchors = [
        (0, 136, 200, 243),   # from A_base, a genuine (4,5)-quadruple (True)
        (0, 5, 10, 20),       # has a 3-AP {0,5,10} structure -> few distinct diffs (False)
        (0, 1, 2, 3),         # arithmetic progression (False)
        (0, 14, 21, 28),      # the FACT1-style forbidden subset, 4 distinct diffs (False)
        (-7, 3, 11, 50),      # negatives + mixed (True)
    ]
    saw_true = saw_false = 0
    ok = True
    for q in anchors:
        const, vals = constant_across_orderings(q)
        v = next(iter(vals))
        saw_true += int(v is True)
        saw_false += int(v is False)
        ok &= const
        print(f"anchor {q}: constant across 24 orders = {const}, diffs4B = {v}")

    # Randomized stress test over distinct integer quadruples.
    rng = random.Random(20260618)
    rand_ok = True
    for _ in range(50000):
        q = rng.sample(range(-200, 200), 4)
        const, vals = constant_across_orderings(q)
        if not const:
            rand_ok = False
            print(f"COUNTEREXAMPLE: {q} -> {vals}")
            break
        v = next(iter(vals))
        saw_true += int(v is True)
        saw_false += int(v is False)
    ok &= rand_ok

    print()
    print(f"randomized 50000 quadruples: invariance held = {rand_ok}")
    print(f"coverage: saw True quadruples = {saw_true > 0}, saw False quadruples = {saw_false > 0}")
    if ok and saw_true > 0 and saw_false > 0:
        print("ALL PASS -- diffs4B is constant across all 24 orderings (both outcomes covered).")
    else:
        print("FAIL")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
