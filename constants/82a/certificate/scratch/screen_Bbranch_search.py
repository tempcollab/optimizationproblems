"""
R8 Angle A -- BROADER ORIGINAL search for a firing+admissible B-perturber.

The Flammang-table screen (screen_Bbranch.py) found: every FIRING table block is
either already in the dictionary OR fails (c1) Q(0)=Q(1)=1 OR (c3) contour-root-free
(min|Q(chi)|<1e-2).  This script searches ORIGINAL integer blocks for a firing AND
fully-admissible one, two ways:

  (1) PRODUCTS of admissible squarefree "atoms" with Q(0)=Q(1)=1 (so the product keeps
      it): build atoms = small monic integer polys p with p(0)=p(1)=1, squarefree,
      contour-root-free, and form products up to a degree cap; score m_B; keep firing
      admissibles.

  (2) DIRECT integer-coefficient enumeration of low-degree monic blocks with the
      Q(0)=Q(1)=1 constraint, scored by a fast vectorized m_B (Scorer pattern, R7
      per-role memory), then admissibility-gated on survivors.

m_B(Q) = (1/D)[ int_{B>A} log|Q(chi)| ds - (log h) deg(Q) ]  (verified marginal).
FIRING <=> m_B < 0.  Anti-firing term int_{B>A} log|Q| must stay below (log h)*deg.

Reproduce:  python3 screen_Bbranch_search.py [degcap] [N]
            python3 screen_Bbranch_search.py 8 1000000
"""
import sys
import math
import itertools
import numpy as np
import sympy as sp

import bound_01_doche_base as vu
import bound_07_block_j9 as q8
import screen_Bbranch as sb

X = sp.symbols('X')


def main(degcap=10, N=1_000_000):
    s, A, B, chi = sb.AB_arrays(sb.R4, N)
    q = np.array(sb.R4["q"])
    argA = float(np.dot(q, vu.DEGP)) + sb.R4["qG"] * q8.DEG_Q7 + sb.R4["qH"] * q8.DEG_Q8
    argB = vu.DEGQ + sb.R4["qE"] * q8.DEG_Q5 + sb.R4["qF"] * q8.DEG_Q6
    D = max(argA, argB)
    active = B > A
    logh = float(np.mean(np.maximum(A, B))) / D
    logabs_chi_cache = {}
    print("=" * 92)
    print(f"R8 ORIGINAL B-perturber search  degcap={degcap}  N={N}")
    print(f"  D={D:.4f}  log h={logh:.10f}  firing thresh int<(logh)*deg")
    print("=" * 92, flush=True)

    def mB_desc(desc):
        deg = len(desc) - 1
        logQ = np.log(np.abs(sb.pv(desc, chi)))
        intB = float(np.mean(logQ * active))
        return (intB - logh * deg) / D, deg, intB

    # ---------- (1) PRODUCTS of admissible firing-leaning atoms ----------
    # atoms: squarefree, Q(0)=Q(1)=1, contour-root-free; we want atoms whose
    # individual int_{B>A} log|.| / deg is SMALL (close to firing).
    # generate monic atoms deg 2..5 with bounded coeffs and Q(0)=Q(1)=1.
    print("\n[atoms] building admissible squarefree atoms (deg2..5, |coef|<=3, "
          "Q(0)=Q(1)=1, contour-root-free)...", flush=True)
    atoms = []
    for deg in range(2, 6):
        # descending: [1, c_{deg-1}, ..., c_1, c0]; monic, c0 free
        for mid in itertools.product(range(-3, 4), repeat=deg - 1):
            for c0 in (-1, 1, 3, -3):
                desc = [1] + list(mid) + [c0]
                # Q(0) = c0 ; Q(1) = sum desc
                if c0 != 1:
                    continue
                if sum(desc) != 1:
                    continue
                Qs = sb.sym_desc(desc)
                if sp.gcd(Qs, sp.diff(Qs, X)) != 1:
                    continue
                mn = float(np.min(np.abs(sb.pv(desc, chi))))
                if mn < 1e-2:
                    continue
                m, dd, intB = mB_desc(desc)
                atoms.append((tuple(desc), intB / dd, m))
    # rank atoms by per-degree integral (smaller = more firing-leaning)
    atoms.sort(key=lambda a: a[1])
    print(f"  {len(atoms)} admissible atoms; best per-deg int (firing-leaning):")
    for desc, perdeg, m in atoms[:8]:
        print(f"    {list(desc)}  int/deg={perdeg:.4f}  m_B={m:.3e} (need int/deg<{logh:.4f})")

    # products of up to 3 best atoms within degcap, gated admissible vs full dict
    best_atoms = [a[0] for a in atoms[:20]]
    firing_admissible = []
    def poly_mul(a, b):
        return tuple(int(c) for c in np.convolve(a, b))
    print(f"\n[products] forming products of top atoms (deg<= {degcap}), scoring m_B...",
          flush=True)
    seen = set()
    prod_list = list(best_atoms)
    # 2- and 3-fold products
    for r in (1, 2, 3):
        for combo in itertools.combinations_with_replacement(best_atoms, r):
            prod = (1,)
            for at in combo:
                prod = poly_mul(prod, at)
            if len(prod) - 1 > degcap:
                continue
            if prod in seen:
                continue
            seen.add(prod)
            desc = list(prod)
            ok, reasons, mn = sb.admissible(desc, chi)
            if not ok:
                continue
            m, dd, intB = mB_desc(desc)
            if m < 0:
                firing_admissible.append((desc, dd, m, mn))
    firing_admissible.sort(key=lambda r: r[2])
    print(f"\n[result] firing+admissible ORIGINAL products: {len(firing_admissible)}")
    for desc, dd, m, mn in firing_admissible[:15]:
        print(f"    {desc} deg={dd} m_B={m:.3e} m_B*D={m*D:.4f} min|Q|={mn:.2e}")
    if not firing_admissible:
        print("    (NONE -- every admissible product is dry, m_B>=0)")

    # ---------- (2) report the closest-to-firing admissible block found ----------
    # scan all admissible atoms + products, report the MINIMUM m_B (least dry)
    allcands = [(list(a[0]), a[2]) for a in atoms]
    allcands += [(d, m) for d, dd, m, mn in firing_admissible]
    allcands.sort(key=lambda r: r[1])
    print(f"\n[closest] most-firing ADMISSIBLE block found (min m_B):")
    for desc, m in allcands[:5]:
        print(f"    {desc}  m_B={m:.3e}  m_B*D={m*D:.4f}  {'FIRE' if m<0 else 'dry'}")
    return firing_admissible


if __name__ == "__main__":
    degcap = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 1_000_000
    main(degcap, N)
