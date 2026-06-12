"""
R6 Angle 3 (ANCHOR milestone): the SHARED-POOL statement, rigorously checked.

Claim (verified here by exact integer-polynomial identities, no floats):

  Every integer polynomial that appears in BOTH the Doche [Doc01a] UPPER-bound
  construction (this campaign's family) AND the Flammang [F18] LOWER-bound
  construction is an entry of Flammang [F18] Table 1 -- ONE shared pool of
  small-Mahler-measure integer polynomials in the variable w = z(1-z).

  Specifically, as polynomials in w:
    Doche base polys :  P4 = j5 (deg 4),  P6 = j8 (deg 8),  P8 = j12 (deg 12)
    A-base blocks    :  j3 = j3 (deg 3),  j9 = j9 (deg 8)      [this campaign]
    Perturber blocks :  Q5 = j13 (deg 12), Q6 = j15 (deg 16)
  are all Flammang Table-1 entries (jk).

  And the FULL active dictionary used by the held R4 upper certificate
    base side      {P1, P2, P4, P6, P8, j3, j9}
    perturber side {Q1, Q2, Q5, Q6}
  is admissible: each block squarefree, every pair coprime (Doc01a condition (4)
  non-degeneracy: the product ratio prod P^n / prod Q^n is never +-1).

HONESTY GUARDRAIL (the genuine DUAL-LOCI structure -- UPPER-INTERNAL only):
  The two upper-side levers act on COMPLEMENTARY arcs of the SAME contour
  t |-> w(t) = z(1-z), z = e^{i t}:
      A-base lever  acts where  G = max(A,B) = A   (the active arc {A>B}),
      B-perturber lever acts where  G = B          (its complement {A<B}).
  We DO NOT claim "lower-bound locus = set-complement of the upper active arc";
  no on-disk evidence supports that, and it is NOT asserted here.

The shared pool is the precise sense in which both the Doche upper construction and
the Flammang lower construction are instances of the SAME WEIGHTED INTEGER
TRANSFINITE-DIAMETER problem t_{Z,phi} on the lemniscate w = z(1-z): both pick
integer polynomials of small weighted log-norm on a sub-locus of that curve, drawn
from the same Table-1 pool.

Reproduce:  python3 verify_shared_pool.py
"""
import sys
import sympy as sp

import verify_upper as vu
import flammang_table1 as ft

X = sp.symbols('X')


def sym_desc(desc):
    """Build a sympy poly in X from a DESCENDING-coefficient integer list."""
    n = len(desc) - 1
    return sum(int(v) * X ** (n - i) for i, v in enumerate(desc))


def sym_asc(asc):
    """Build a sympy poly in X from an ASCENDING-coefficient integer list
    (verify_upper stores P1,P2,... DESCENDING; this is for the ASC dicts)."""
    return sum(int(v) * X ** i for i, v in enumerate(asc))


# Flammang Table-1, indexed by campaign name jk:  _TAB[k] = DESCENDING coeffs.
# NUMBERING TRAP: ft._TABLE_DESCENDING is 0-indexed; campaign jk = entry k-1.
_TAB = {j + 1: desc for j, (c, desc) in enumerate(ft._TABLE_DESCENDING)}


def main():
    print("=" * 70)
    print("R6 Angle 3 -- SHARED-POOL identity check (exact, integer-polynomial)")
    print("=" * 70)

    # Doche base polys (DESCENDING) from verify_upper, and the campaign blocks.
    #   verify_upper.P4/P6/P8 are DESCENDING coeff lists in the variable chi=z(1-z).
    doche = {
        "P4": (vu.P4, 5),   # claim P4 == Flammang j5
        "P6": (vu.P6, 8),   # claim P6 == Flammang j8
        "P8": (vu.P8, 12),  # claim P8 == Flammang j12
    }
    all_ok = True

    # ---- 1. Doche base = Flammang Table-1 entries ----------------------------
    print("\n[1] Doche base polynomials are Flammang Table-1 entries (exact eq):")
    for nm, (desc_doche, jk) in doche.items():
        lhs = sym_desc(desc_doche)
        rhs = sym_desc(_TAB[jk])
        eq = sp.expand(lhs - rhs) == 0
        all_ok = all_ok and bool(eq)
        print(f"  {nm} (deg {len(desc_doche)-1})  ==  Flammang j{jk}: {eq}")
        if not eq:
            print(f"      LHS={desc_doche}  RHS(j{jk})={_TAB[jk]}")

    # ---- 2. Campaign A-base blocks = Flammang Table-1 entries ----------------
    print("\n[2] Campaign A-base blocks are Flammang Table-1 entries (exact eq):")
    j3_desc = [1, 1, -2, 1]
    j9_desc = [1, -1, 0, -3, 15, -22, 16, -6, 1]
    for nm, desc, jk in [("j3", j3_desc, 3), ("j9", j9_desc, 9)]:
        eq = sp.expand(sym_desc(desc) - sym_desc(_TAB[jk])) == 0
        all_ok = all_ok and bool(eq)
        print(f"  campaign {nm} (deg {len(desc)-1})  ==  Flammang j{jk}: {eq}")

    # ---- 3. Perturber blocks Q5,Q6 = Flammang Table-1 entries ----------------
    # verify_upper_q6 stores Q5,Q6 DESCENDING.  Import from q8A which re-exports.
    import verify_upper_q8A as q8
    print("\n[3] Perturber blocks are Flammang Table-1 entries (exact eq):")
    for nm, desc, jk in [("Q5", list(q8.Q5), 13), ("Q6", list(q8.Q6), 15)]:
        eq = sp.expand(sym_desc(desc) - sym_desc(_TAB[jk])) == 0
        all_ok = all_ok and bool(eq)
        print(f"  campaign {nm} (deg {len(desc)-1})  ==  Flammang j{jk}: {eq}")

    # ---- 4. Full active dictionary: squarefree + pairwise coprime -----------
    print("\n[4] Active dictionary admissibility (Doc01a condition (4)):")
    # verify_upper stores P1,P2,P4,P6,P8,Q1,Q2 DESCENDING.
    active = {
        "P1": sym_desc(vu.P1), "P2": sym_desc(vu.P2),
        "P4": sym_desc(vu.P4), "P6": sym_desc(vu.P6), "P8": sym_desc(vu.P8),
        "j3": sym_desc(j3_desc), "j9": sym_desc(j9_desc),
        "Q1": sym_desc(list(vu.Q1)), "Q2": sym_desc(list(vu.Q2)),
        "Q5": sym_desc(list(q8.Q5)), "Q6": sym_desc(list(q8.Q6)),
    }
    names = list(active.keys())

    # squarefree
    sf_ok = True
    for nm in names:
        p = active[nm]
        sf = (sp.gcd(p, sp.diff(p, X)) == 1)
        sf_ok = sf_ok and bool(sf)
        if not sf:
            print(f"  NOT squarefree: {nm}")
    print(f"  all {len(names)} blocks squarefree: {sf_ok}")
    all_ok = all_ok and sf_ok

    # pairwise coprime
    cop_ok = True
    bad = []
    for i in range(len(names)):
        for jx in range(i + 1, len(names)):
            g = sp.gcd(active[names[i]], active[names[jx]])
            c = (sp.degree(g, X) == 0)
            if not c:
                cop_ok = False
                bad.append((names[i], names[jx], g))
    print(f"  all {len(names)*(len(names)-1)//2} pairs coprime: {cop_ok}")
    if bad:
        for a, b, g in bad:
            print(f"    NON-COPRIME: gcd({a},{b}) = {g}")
    all_ok = all_ok and cop_ok

    # ---- 5. Honesty guardrail (no false dual-loci claim) --------------------
    print("\n[5] Dual-loci framing (UPPER-INTERNAL only; no upper-vs-lower claim):")
    print("  A-base lever acts on active arc {A>B}; B-perturber lever on {A<B}.")
    print("  (We do NOT assert lower-locus = complement of upper active arc.)")

    print("\n" + "=" * 70)
    print(f"  SHARED-POOL CHECK: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 70)
    return all_ok


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
