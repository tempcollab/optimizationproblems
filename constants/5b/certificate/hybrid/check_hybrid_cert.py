#!/usr/bin/env python3
"""
Independent numerical re-check of the HYBRID transversal certificate for C_5b (round 4).

This mirrors the arithmetic the Lean lemma `C5bHybrid.hLe_of_hybrid` relies on, computed
from scratch in Python so the reviewer can cross-check the Lean kernel:

  - the 12 three-term APs of A_base (the 3-AP hypergraph H(A_base));
  - the FRACTIONAL bound: the supplied weighting (denominator D=6, total T=27) is a valid
    fractional matching (every vertex load <= D) with value nu* = T/D = 4.5, so ceil(nu*) = 5,
    giving tau >= 5 and h <= N - 5 = 9;
  - the BRANCHING bound: the EXACT minimum transversal tau = 6 (brute force over the 14
    vertices), giving h <= N - 6 = 8;
  - the HYBRID: tau >= max(5, 6) = 6, so the hybrid h-bound = N - 6 = 8 -- the max correctly
    PREFERS the branch value over the (looser) fractional one.

The Lean lemma packages this as `S.length <= min(m_frac, N - k_branch - 1) = min(9, 8) = 8`.

NOTE (honest scope): this `max` composition does NOT shrink the branch budget. The exact tau
here was found by full enumeration; the certified Lean `noTransLe` budget for A_base is the
full 5 (= tau - 1), NOT a small residual. The genuinely-scaling interleaved version (branch
only the integral-fractional residual) is a further step -- see the approach doc.

Exit 0 on success, nonzero on any mismatch.
"""

from itertools import combinations

A = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
N = len(A)
Aset = set(A)

# ---- 1. enumerate the 3-term APs of A (edges of H(A)) ----
# a < b < c with a + c = 2b, all distinct, all in A.
APs = []
for a, b, c in combinations(sorted(A), 3):
    if a + c == 2 * b:
        APs.append((a, b, c))
APs.sort()

expected_APs = [
    (0, 136, 272), (0, 200, 400), (0, 298, 596), (0, 528, 1056),
    (136, 596, 1056), (200, 243, 286), (200, 249, 298), (243, 246, 249),
    (246, 272, 298), (246, 323, 400), (249, 286, 323), (272, 400, 528),
]
assert sorted(APs) == sorted(expected_APs), f"AP family mismatch: {APs}"
assert len(APs) == 12, f"expected 12 APs, got {len(APs)}"
print(f"[ok] H(A_base) has {len(APs)} three-term APs (edges)")

# ---- 2. FRACTIONAL bound: validate the supplied weighting ----
# weights matching lean/Constants/C5bTransversal.lean Fcert_base (denominator D = 6).
D = 6
weights = {
    (0, 136, 272): 2, (0, 200, 400): 0, (0, 298, 596): 2, (0, 528, 1056): 2,
    (136, 596, 1056): 4, (200, 243, 286): 4, (200, 249, 298): 2,
    (243, 246, 249): 2, (246, 272, 298): 1, (246, 323, 400): 3,
    (249, 286, 323): 2, (272, 400, 528): 3,
}
assert set(weights) == set(APs), "weighting must cover exactly the AP family"
T = sum(weights.values())
assert T == 27, f"total weight expected 27, got {T}"
# vertex loads <= D
load = {v: 0 for v in A}
for e, w in weights.items():
    for v in e:
        load[v] += w
maxload = max(load.values())
assert maxload <= D, f"fractional matching violated: max vertex load {maxload} > D={D}"
nu_star = T / D
import math
ceil_nu = math.ceil(nu_star)
tau_frac = ceil_nu                      # tau >= ceil(nu*)
h_frac = N - tau_frac
print(f"[ok] fractional: T={T}, D={D}, nu*={nu_star}, ceil(nu*)={ceil_nu} "
      f"-> tau >= {tau_frac}, h <= {h_frac}")
assert h_frac == 9, f"fractional h-bound expected 9, got {h_frac}"

# ---- 3. BRANCHING bound: EXACT minimum transversal tau ----
# minimum number of vertices of A that hit every AP (3-uniform hitting set).
def min_transversal(edges, verts):
    # increasing-size brute force; tiny instance (12 edges, 14 verts).
    for k in range(0, len(verts) + 1):
        for H in combinations(verts, k):
            Hs = set(H)
            if all(any(v in Hs for v in e) for e in edges):
                return k, H
    return len(verts), tuple(verts)

tau_exact, witness = min_transversal(APs, A)
h_branch = N - tau_exact
print(f"[ok] branching: exact tau={tau_exact} (witness {witness}) -> h <= {h_branch}")
assert tau_exact == 6, f"exact tau expected 6, got {tau_exact}"
assert h_branch == 8, f"branch h-bound expected 8, got {h_branch}"

# ---- 4. HYBRID: max of the two tau-bounds (= min of the two h-bounds) ----
tau_hybrid = max(tau_frac, tau_exact)
h_hybrid = N - tau_hybrid
print(f"[ok] hybrid: tau >= max({tau_frac}, {tau_exact}) = {tau_hybrid} -> h <= {h_hybrid}")
assert tau_hybrid == 6, "hybrid max should prefer the branch bound (tau=6)"
assert h_hybrid == 8, "hybrid h-bound should be the tight 8"
# this matches the Lean `min m_frac (N - k_branch - 1) = min 9 (14-5-1) = min 9 8 = 8`
assert min(h_frac, h_branch) == 8

print()
print("[PASS] hybrid certificate arithmetic reproduced:")
print(f"       fractional h <= {h_frac}, branch h <= {h_branch}, "
      f"hybrid (max of tau) h <= {h_hybrid}")
print("       matches Lean min(9, 8) = 8 in C5bHybrid.Validation.Abase_avoiders_le_8_hybrid.")
print("       NOTE: this is the MAX composition; the branch budget is NOT reduced "
      "(tau certified in full).")
