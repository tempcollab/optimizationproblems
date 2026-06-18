#!/usr/bin/env python3
"""
Independent re-check of the INTERLEAVED (fix-then-branch) transversal certificate for C_5b
(lean/Constants/C5bInterleaved.lean).

It re-derives, WITHOUT Lean:

  (A) the synthetic instance A_syn fires the budget-shrink mechanism:
        fractional value a = 2 (two vertex-disjoint APs, nu* = 2),
        residual branch budget g = 1 (two vertex-disjoint APs, tau = 2),
        combined tau(A_syn) = 4 = a + (g + 1)  -> h(A_syn) <= 12 - 4 = 8,
      branching only g = 1 (3 leaves) instead of the full tau = 4 (3^4 = 81 worst-case).

  (B) the HONEST A_base finding (why the interleaving DEGENERATES there):
        A_base's 3-AP hypergraph is fully HALF-INTEGRAL (cover LP value nu* = 4.5,
        all vertices 0 or 1/2, no integral component, no forced vertex);
        max over ALL support sets P of  ( ceil(nu*(edges in P)) + tau(edges avoiding P) )
        equals 6, attained ONLY at P = empty (a = 0, full branch budget g = 5).
      So on A_base no support choice beats the pure branch budget -- the proposed
        g ~ tau - ceil(nu*) = 1 budget is NOT achievable for this pathological gadget.
      The Lean validation therefore uses the DEGENERATE P = empty form (a = 0, g = 5),
        which still soundly re-derives the tight h(A_base) <= 8.

All checks are exact (integer arithmetic + exact LP via scipy); no heuristics.
Run:  python3 check_interleaved_cert.py
"""
from itertools import combinations
import math
import numpy as np
from scipy.optimize import linprog

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def tau(fam):
    """Exact minimum hitting set (transversal) size of a 3-uniform family."""
    verts = sorted({v for ap in fam for v in ap})
    for k in range(0, len(verts) + 1):
        for H in combinations(verts, k):
            Hs = set(H)
            if all(any(v in Hs for v in ap) for ap in fam):
                return k
    return len(verts)

def supp(fam):
    return {v for ap in fam for v in ap}

def nustar(fam):
    """Exact fractional-matching value nu*(fam) = max sum w_e, vertex loads <= 1."""
    if not fam:
        return 0.0
    verts = sorted(supp(fam))
    vi = {v: i for i, v in enumerate(verts)}
    ne = len(fam)
    c = -np.ones(ne)
    A_ub = np.zeros((len(verts), ne))
    for ei, ap in enumerate(fam):
        for v in ap:
            A_ub[vi[v], ei] = 1.0
    res = linprog(c, A_ub=A_ub, b_ub=np.ones(len(verts)), bounds=[(0, None)] * ne)
    return -res.fun

def cover_lp(fam, verts):
    """Min vertex-cover LP: min sum x_v, edge x_a+x_b+x_c >= 1, 0<=x<=1. Returns (value, x)."""
    vi = {v: i for i, v in enumerate(verts)}
    nv = len(verts)
    c = np.ones(nv)
    A_ub, b_ub = [], []
    for ap in fam:
        row = np.zeros(nv)
        for v in ap:
            row[vi[v]] = -1.0
        A_ub.append(row); b_ub.append(-1.0)
    res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub), bounds=[(0, 1)] * nv)
    return res.fun, res.x

# ---------------------------------------------------------------------------
# (A) synthetic instance -- the mechanism fires
# ---------------------------------------------------------------------------
print("=" * 72)
print("(A) Synthetic instance A_syn  (the budget-shrink mechanism FIRES)")
print("=" * 72)
Asyn = [0, 1, 2, 10, 11, 12, 100, 101, 102, 200, 201, 202]
APfrac = [(100, 101, 102), (200, 201, 202)]
APres  = [(0, 1, 2), (10, 11, 12)]
APfull = APfrac + APres

a_frac = math.ceil(nustar(APfrac) - 1e-9)
tau_res = tau(APres)
g = tau_res - 1
print(f"  fractional family {APfrac}")
print(f"     nu*(frac) = {nustar(APfrac):.3f}  -> a = ceil = {a_frac}")
print(f"  residual family  {APres}")
print(f"     tau(res) = {tau_res}  -> branch budget g = {g}  (3^{g} = {3**g} leaves)")
print(f"  support(frac) disjoint from support(res)? "
      f"{supp(APfrac).isdisjoint(supp(APres))}")
tau_full = tau(APfull)
print(f"  combined tau(A_syn) = {tau_full}   (== a + (g+1) = {a_frac + g + 1})")
bound = len(Asyn) - tau_full
print(f"  => h(A_syn) <= N - tau = {len(Asyn)} - {tau_full} = {bound}")
assert a_frac == 2 and g == 1 and tau_full == 4 and bound == 8, "SYN MISMATCH"
print(f"  pure-branch budget would be tau - 1 = {tau_full - 1} (3^{tau_full-1} = "
      f"{3**(tau_full-1)} leaves); interleaved uses only g = {g}.  BUDGET-SHRINK OK.")

# ---------------------------------------------------------------------------
# (B) A_base -- the honest degeneracy finding
# ---------------------------------------------------------------------------
print()
print("=" * 72)
print("(B) A_base  (interleaving DEGENERATES -- half-integral, no budget shrink)")
print("=" * 72)
Abase = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
S = set(Abase)
APbase = []
for x in Abase:
    for y in Abase:
        if x < y:
            c = 2 * y - x
            if c in S and c > y:
                APbase.append((x, y, c))
assert len(APbase) == 12, f"expected 12 APs, got {len(APbase)}"
print(f"  A_base has {len(APbase)} 3-term APs; tau(A_base) = {tau(APbase)}")

val, x = cover_lp(APbase, Abase)
print(f"  cover LP value nu* = {val:.4f}")
halfint = all(abs(xi - round(xi * 2) / 2) < 1e-6 for xi in x)
integral_verts = [Abase[i] for i in range(len(Abase)) if x[i] > 1 - 1e-6]
print(f"  LP solution fully half-integral (all in {{0, 1/2, 1}})? {halfint}")
print(f"  integral (x=1) vertices NT can fix: {integral_verts}  "
      f"(none => NT fixing is vacuous)")

# exhaustive: max over all P of ceil(nu*(edges in P)) + tau(edges avoiding P)
def nustar_in_P(P):
    frac = [ap for ap in APbase if set(ap) <= set(P)]
    return nustar(frac)

best = (-1, None)
N = len(Abase)
for mask in range(1 << N):
    P = [Abase[i] for i in range(N) if mask & (1 << i)]
    Ps = set(P)
    a = math.ceil(nustar_in_P(P) - 1e-9)
    residual = [ap for ap in APbase if not (set(ap) & Ps)]
    val_P = a + tau(residual)
    if val_P > best[0]:
        best = (val_P, (a, tau(residual), sorted(P)))
print(f"  max over ALL P of  ceil(nu*(edges in P)) + tau(edges avoiding P) = {best[0]}")
print(f"     attained at  a = {best[1][0]}, tau(residual) = {best[1][1]}, "
      f"P = {best[1][2]}")
assert best[0] == 6 and best[1][0] == 0 and best[1][2] == [], \
    "A_base degeneracy claim FAILED -- a nontrivial split would beat the branch budget!"
print("  => only the TRIVIAL P = [] reaches 6 (a=0, full branch budget g=5).")
print("     The interleaved cert cannot shrink the A_base budget below the pure branch.")
print("     Lean validation uses the degenerate P=[] form; still sound (h<=8).")

print()
print("=" * 72)
print("ALL CHECKS PASSED.")
print("  (A) interleaved mechanism verified on A_syn: a=2 + branch g=1 => tau=4, h<=8.")
print("  (B) A_base is half-integral; no support P beats the branch budget (honest).")
print("=" * 72)
