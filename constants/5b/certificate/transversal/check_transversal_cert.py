#!/usr/bin/env python3
"""
Re-checking script for the C_5b AP-transversal (fractional-matching) certificate machinery
(approach `floorplus1-transversal-N30`, R3 sub-goal: the MACHINERY, validated on A_base).

This script independently re-establishes the *numerical* facts that the Lean file
`lean/Constants/C5bTransversal.lean` encodes and `decide`-checks:

  1. The twelve 3-term APs of the record set A_base.
  2. The fractional-matching certificate `Fcert_base` (denominator D=6): total weight
     T = 27, every vertex load <= 6  =>  fractional matching value nu* = 27/6 = 4.5.
  3. The transversal soundness arithmetic:  T > D*(N - m - 1)  with m = 9
     (6*(14-9-1) = 24 < 27)  =>  h(A_base) <= 9 by the transversal route.
  4. The HONEST integrality gap: the exact min transversal is tau = 6 (so the tight value is
     h = N - tau = 8), while the LP optimum nu* = 4.5 only certifies tau >= 5 (h <= 9).
     Pure LP-duality therefore cannot reach the tight h <= 8 on A_base.

The Lean proof carries the *soundness lemma* (every avoider sublist has length <= m); this
script only re-derives the finite numerical inputs so a reviewer can confirm them outside
Lean.  The gold-standard check remains `lake build Constants.C5bTransversal` +
`#print axioms` (type-checking IS the reproduction).
"""
from fractions import Fraction
from itertools import combinations

A = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
N = len(A)
assert N == 14 and len(set(A)) == 14

# ---- 1. the 3-term APs of A_base -------------------------------------------------------
Aset = set(A)
aps = []
for i in range(N):
    for j in range(i + 1, N):
        for k in range(j + 1, N):
            a, b, c = A[i], A[j], A[k]
            if a + c == 2 * b:
                aps.append((a, b, c))
print("3-term APs of A_base:", len(aps))
assert len(aps) == 12, aps

# ---- 2. the fractional-matching certificate (must MATCH the Lean Fcert_base) ------------
# (triple, integer weight at denominator D=6)
Fcert = [
    ((0, 136, 272), 2),
    ((0, 200, 400), 0),
    ((0, 298, 596), 2),
    ((0, 528, 1056), 2),
    ((136, 596, 1056), 4),
    ((200, 243, 286), 4),
    ((200, 249, 298), 2),
    ((243, 246, 249), 2),
    ((246, 272, 298), 1),
    ((246, 323, 400), 3),
    ((249, 286, 323), 2),
    ((272, 400, 528), 3),
]
D = 6
# every listed edge is a genuine 3-AP fully inside A_base
for (a, b, c), w in Fcert:
    assert a + c == 2 * b and len({a, b, c}) == 3, ("not an AP", (a, b, c))
    assert {a, b, c} <= Aset, ("vertex outside A", (a, b, c))
# vertex loads <= D
load = {v: 0 for v in A}
for (a, b, c), w in Fcert:
    for v in (a, b, c):
        load[v] += w
maxload = max(load.values())
T = sum(w for _, w in Fcert)
print(f"certificate: T (total weight) = {T}, D = {D}, max vertex load = {maxload}")
assert maxload <= D, ("load exceeds D", maxload)
assert T == 27, T
print(f"fractional matching value nu* = T/D = {Fraction(T, D)} = {T / D}")

# ---- 3. the soundness arithmetic: T > D*(N-m-1) with m=9  =>  h <= 9 --------------------
m = 9
assert T > D * (N - m - 1), (T, D * (N - m - 1))
print(f"soundness: {T} = T > D*(N-m-1) = {D}*({N}-{m}-1) = {D * (N - m - 1)}  =>  h(A_base) <= {m}")

# ---- 4. honest integrality gap: exact tau and exact LP optimum --------------------------
# exact min transversal tau (vertex cover of the 3-uniform hypergraph)
def min_transversal(verts, edges):
    for k in range(0, len(verts) + 1):
        for H in combinations(verts, k):
            Hs = set(H)
            if all(any(x in Hs for x in e) for e in aps):
                return k
    return None

tau = min_transversal(A, aps)
print(f"exact min transversal tau = {tau}  =>  TIGHT h(A_base) = N - tau = {N - tau}")
assert tau == 6

# exact LP optimum of the fractional matching (max sum w s.t. per-vertex load <= 1)
try:
    import numpy as np
    from scipy.optimize import linprog
    idx = {v: i for i, v in enumerate(A)}
    E = len(aps)
    c = -np.ones(E)
    Aub = np.zeros((N, E))
    for ei, (a, b, cc) in enumerate(aps):
        for x in (a, b, cc):
            Aub[idx[x], ei] = 1
    res = linprog(c, A_ub=Aub, b_ub=np.ones(N), bounds=[(0, None)] * E, method="highs")
    nu_star = -res.fun
    print(f"exact LP optimum (fractional matching) nu* = {nu_star:.4f}")
    assert abs(nu_star - 4.5) < 1e-6
    print(f"INTEGRALITY GAP: tau = {tau} > ceil(nu*) = {int(np.ceil(nu_star))}  "
          f"=> LP-duality certifies only h <= {N - int(np.ceil(nu_star))}, NOT the tight h <= {N - tau}")
except ImportError:
    print("(scipy not available; LP-optimum check skipped — Fcert already shows nu* = 4.5)")

print("\nALL CHECKS PASSED.")
print("Conclusion: the fractional-matching machinery is SOUND and fires end-to-end "
      "(certifies h(A_base) <= 9, O(|F|*N) cost).")
print("The tight h <= 8 needs an INTEGRAL transversal certificate (next sub-goal) — "
      "A_base has an integrality gap tau=6 > nu*=4.5.")
