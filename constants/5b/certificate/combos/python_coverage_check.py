#!/usr/bin/env python3
"""Independent re-enumeration of C5b.combos's recurrence vs itertools.combinations.
Confirms `combos l 4` enumerates EVERY 4-subset of l exactly once.
Run: python3 python_coverage_check.py  (expect all True)."""
from itertools import combinations

def combos(l, k):
    # mirrors C5b.combos:  combos (x::xs)(k+1) = map(x::) combos(xs,k) ++ combos(xs,k+1)
    if k == 0:
        return [[]]
    if not l:
        return []
    x, xs = l[0], l[1:]
    return [[x] + c for c in combos(xs, k - 1)] + combos(xs, k)

for L in ([0,1,2,3,4,5], [10,20,30,40,50,60,70], list(range(8)), [3,1,4,11,5,9,2,6]):
    n = len(L)
    cb = combos(L, 4)
    sets_from_combos = set(frozenset(t) for t in cb)
    all_4subsets = set(frozenset(s) for s in combinations(L, 4))
    print(f"n={n}: |combos|={len(cb)} C(n,4)={len(all_4subsets)} "
          f"len4={all(len(t)==4 for t in cb)} "
          f"count={len(cb)==len(all_4subsets)} "
          f"cover_all_subsets={sets_from_combos==all_4subsets}")
