"""
R7 DESIGN-PRINCIPLE construction (82a UPPER).

Turn the R6 first-variation criterion into a BLOCK-DESIGN OPTIMIZER and use it to
CONSTRUCT an ORIGINAL integer A-base block Q* (NOT in Flammang Table-1, NOT in the
active dictionary) with verified firing marginal r~_Q* < 0.

DESIGN PROBLEM (the new framing, the contribution):
    minimize  r~_Q = < log|Q(chi)| * 1_{A0>B} >_s = int log|Q| dnu       (the certified
                                                                          first-variation
                                                                          marginal, R6 lemma)
    over      Q in Z[X],  deg(Q) <= 10,
    s.t.      (c1) contour-root-free:  min_s |Q(chi(s))| > 0  (L1 screen >= ~1e-2),
              (c2) gcd(Q, dict_block) = 1 and Q squarefree, in w = z(1-z),
              (c3) ORIGINAL: Q not in Flammang Table-1 (24 entries) and not a dict block.

ANCHOR (GUARDRAIL 1, outline review): the FINAL r~_Q* < 0 milestone claim for a THIRD
A-base block is measured on the R4 family (j3 AND j9 both ON, candidate exponent = 0),
recomputing {A>B} there.  (R2 anchor is ONLY for seeding the U^nu well-map; R4 is the
q_Q=0 base point of the family Q* is being added to.)

FACTORIZATION (the lever the optimizer acts on; identity verified to 5.2e-17 in
firstvar_01_lemma.root_potential_check):
    r~_Q = sum_{rho: Q(rho)=0} U^nu(rho) + deg(Q)*log|lead(Q)|,
    U^nu(zeta) = < log|zeta - chi| 1_{A0>B} >_s   (the active-arc log-potential).
So r~ is driven DOWN by placing integer roots at the deepest U^nu wells while staying
contour-root-free.

Note: blocks are polynomials in w = chi = z(1-z); coprimality/originality is checked
in w (the shared variable, per R6 firstvar_06_dictionary).

Reproduce:  python3 construct_block_R7.py            (well map + enumeration, ~1-2 min)
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import sys
import math
import itertools
import numpy as np
import sympy as sp

import bound_01_doche_base as vu
import bound_07_block_j9 as q8
import firstvar_01_lemma as fv
import flammang_table1 as ft

W = sp.symbols('w')

# ---- The active 11-block dictionary, as DESCENDING-coeff lists in w ----------------
DICT_BLOCKS = {
    'P1': list(vu.BASE[0]), 'P2': list(vu.BASE[1]), 'P4': list(vu.BASE[2]),
    'P6': list(vu.BASE[3]), 'P8': list(vu.BASE[4]),
    'j3': list(q8.Q7), 'j9': list(q8.Q8),
    'Q1': list(vu.Q1), 'Q2': list(vu.Q2), 'Q5': list(q8.Q5), 'Q6': list(q8.Q6),
}


def desc_to_poly(desc):
    """DESCENDING int coeff list -> sympy Poly in w."""
    return sp.Poly(list(desc), W)


def desc_normalized_key(desc):
    """Normalize a descending int coeff list to a canonical key (strip leading zeros,
    fix leading sign positive) for deterministic originality equality."""
    d = list(desc)
    while d and d[0] == 0:
        d = d[1:]
    if not d:
        return tuple()
    if d[0] < 0:
        d = [-c for c in d]
    return tuple(d)


# Precompute originality blacklist: Flammang Table-1 (descending) + dict blocks.
def build_blacklist():
    keys = set()
    for c, desc in ft._TABLE_DESCENDING:
        keys.add(desc_normalized_key(desc))
    for name, desc in DICT_BLOCKS.items():
        keys.add(desc_normalized_key(desc))
    return keys


BLACKLIST = build_blacklist()


def is_original(desc):
    return desc_normalized_key(desc) not in BLACKLIST


def admissibility(desc):
    """Return (coprime_ok, squarefree_ok, gcd_failures). Checks gcd(Q, block)=1 in w
    for every dictionary block, and Q squarefree."""
    Q = desc_to_poly(desc)
    if Q.degree() < 1:
        return False, False, ['deg<1']
    failures = []
    for name, bdesc in DICT_BLOCKS.items():
        Bp = desc_to_poly(bdesc)
        g = sp.gcd(Q, Bp)
        if g.degree() >= 1:
            failures.append(name)
    # squarefree: gcd(Q, Q') has degree 0
    sf = sp.gcd(Q, Q.diff(W)).degree() < 1
    return (len(failures) == 0), sf, failures


def min_contour_modulus(desc, N=200000):
    """min_s |Q(chi(s))| -- the contour-root-free screen (c1)."""
    s = (np.arange(N) + 0.5) / N
    z = np.exp(2j * np.pi * s)
    chi = z * (1 - z)
    vals = np.abs(fv.pv(desc, chi))
    return float(vals.min())


# ============================ U^nu WELL MAP (on R4) ==================================

def compute_unu_grid(fam, N, re_lo, re_hi, im_lo, im_hi, ng):
    """U^nu on a complex grid over the active locus bounding box (fam=R4 anchor)."""
    s, A0, B, chi = fv.AB_arrays(fam, N)
    active = A0 > B
    chi_arc = chi[active]
    arcfrac = active.mean()
    res = np.linspace(re_lo, re_hi, ng)
    ims = np.linspace(im_lo, im_hi, ng)
    RE, IM = np.meshgrid(res, ims)
    Z = (RE + 1j * IM).ravel()
    U = np.empty(Z.size)
    # U^nu(zeta) = (1/N) * sum_{arc} log|zeta - chi|
    for k, zeta in enumerate(Z):
        U[k] = np.sum(np.log(np.abs(zeta - chi_arc))) / N
    return Z.reshape(RE.shape), U.reshape(RE.shape), chi_arc, arcfrac, N


def find_wells(Z, U, n_wells=12):
    """Return the deepest (most negative) U^nu grid points, deduplicated by locality."""
    flatZ = Z.ravel(); flatU = U.ravel()
    order = np.argsort(flatU)
    wells = []
    for idx in order:
        z = flatZ[idx]; u = flatU[idx]
        if any(abs(z - w[0]) < 0.12 for w in wells):
            continue
        wells.append((z, u))
        if len(wells) >= n_wells:
            break
    return wells


# ============================ r~ scoring (on the R4 anchor) ==========================

class Scorer:
    """r~ scorer. Precomputes the ACTIVE-arc chi array once so each rtilde() touches
    only the active arc (arcfrac ~ 0.0686 of N), not the full grid -- ~15x faster."""
    def __init__(self, fam, N):
        s, A0, B, chi = fv.AB_arrays(fam, N)
        self.active = A0 > B
        self.chi = chi
        self.chi_arc = chi[self.active]
        self.N = N

    def rtilde(self, desc):
        # r~ = (1/N) sum_{active} log|Q(chi)|  (inactive grid contributes 0)
        logQ = np.log(np.abs(fv.pv(desc, self.chi_arc)))
        return float(np.sum(logQ)) / self.N

    def rtilde_batch(self, descs):
        """Vectorized r~ for a list of DESCENDING coeff lists, all padded to the same
        degree. Returns np.array of r~ values. Horner across all polys at once."""
        maxlen = max(len(d) for d in descs)
        C = np.zeros((len(descs), maxlen))
        for i, d in enumerate(descs):
            C[i, maxlen - len(d):] = d         # right-align (descending) with leading 0s
        x = self.chi_arc                        # (nw,)
        acc = np.zeros((len(descs), x.size), dtype=complex)
        for k in range(maxlen):
            acc = acc * x + C[:, k][:, None]    # Horner step, broadcast
        logQ = np.log(np.abs(acc))              # (M, nw)
        return logQ.sum(axis=1) / self.N


# ============================ ENUMERATION (Angle 2: seeded) ==========================

def quad_from_pair(p):
    """Integer monic quadratic with roots nearest a complex p and its conjugate:
    X^2 - round(2 Re p) X + round(|p|^2).  DESCENDING."""
    b = -int(round(2 * p.real))
    c = int(round(abs(p) ** 2))
    return [1, b, c]


def poly_mult(a, b):
    """Multiply two DESCENDING int coeff lists."""
    pa = np.poly1d(a); pb = np.poly1d(b)
    return [int(round(c)) for c in (pa * pb).c]


def enumerate_products(wells, scorer, max_factors=4, lead_pairs=8):
    """Build ORIGINAL candidate blocks as products of monic integer quadratics
    seeded at the U^nu wells (each well -> one conjugate-pair quadratic factor), plus
    small integer perturbations of the well-targeting real/imag parts. Score by r~ on
    the R4 anchor; gate by originality first (cheap), then return sorted-by-r~."""
    # candidate quadratic factors from each well (and small perturbations)
    well_pts = [w[0] for w in wells[:lead_pairs]]
    quad_factors = set()
    for p in well_pts:
        for dre in (-1, 0, 1):
            for dim in (0,):
                pp = complex(p.real + 0.0, p.imag)
                b = -int(round(2 * pp.real)) + dre
                c = int(round(abs(pp) ** 2))
                for dc in (-1, 0, 1):
                    quad_factors.add((1, b, c + dc))
    quad_factors = [list(q) for q in quad_factors]

    cands = {}  # key -> (desc, rt)
    # products of 1..max_factors quad factors (allow repeats up to 1 each -> distinct)
    for r in range(2, max_factors + 1):
        for combo in itertools.combinations_with_replacement(range(len(quad_factors)), r):
            desc = [1]
            for idx in combo:
                desc = poly_mult(desc, quad_factors[idx])
            if len(desc) - 1 > 10:
                continue
            key = desc_normalized_key(desc)
            if key in cands:
                continue
            if not is_original(desc):
                continue
            rt = scorer.rtilde(desc)
            cands[key] = (desc, rt)
    return cands


def main():
    N_well = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    N_score = 2_000_000
    print("=" * 96)
    print("R7 DESIGN-PRINCIPLE construction of an ORIGINAL A-base block (82a UPPER)")
    print(f"Anchor = R4 (j3 AND j9 ON, candidate exp=0)   N_well={N_well} N_score={N_score}")
    print("=" * 96)

    # --- bounding box of the R4 active locus -------------------------------------
    s, A0, B, chi = fv.AB_arrays(fv.R4, N_well)
    active = A0 > B
    chi_arc = chi[active]
    arcfrac = float(active.mean())
    re_lo, re_hi = chi_arc.real.min(), chi_arc.real.max()
    im_lo, im_hi = chi_arc.imag.min(), chi_arc.imag.max()
    print(f"active arcfrac = {arcfrac:.5f}  ({chi_arc.size} pts)")
    print(f"Re w in [{re_lo:.4f},{re_hi:.4f}]  Im w in [{im_lo:.4f},{im_hi:.4f}]")

    # --- U^nu well map -----------------------------------------------------------
    print("\nComputing U^nu well map on a 60x60 grid ...")
    Z, U, _, _, _ = compute_unu_grid(fv.R4, N_well, re_lo - 0.1, re_hi + 0.1,
                                     im_lo - 0.1, im_hi + 0.1, 60)
    wells = find_wells(Z, U, n_wells=12)
    print("Deepest U^nu wells (zeta, U^nu):")
    for z, u in wells:
        print(f"   zeta={z.real:+.4f}{z.imag:+.4f}j   U^nu={u:+.5f}")

    # --- scorer on R4 ------------------------------------------------------------
    scorer = Scorer(fv.R4, N_score)

    # sanity: reproduce r~(j9), r~(j3) on R4 (traps, both already active => expect >=~0)
    print("\nSanity (TRAP anchor R4, blocks already active -> not firing here):")
    print(f"   r~(j3) on R4 = {scorer.rtilde(fv.J3):+.6f}")
    print(f"   r~(j9) on R4 = {scorer.rtilde(fv.J9):+.6f}")

    # --- Angle 2: seeded product enumeration -------------------------------------
    print("\nEnumerating ORIGINAL well-seeded product blocks (Angle 2) ...")
    cands = enumerate_products(wells, scorer, max_factors=4, lead_pairs=10)
    ranked = sorted(cands.values(), key=lambda dr: dr[1])
    print(f"  built {len(cands)} original candidates; top 20 by r~ (most negative):")
    firing = [dr for dr in ranked if dr[1] < 0]
    for desc, rt in ranked[:20]:
        deg = len(desc) - 1
        print(f"   r~={rt:+.6f}  deg={deg:<2}  {desc}")

    print(f"\n  ORIGINAL firing candidates (r~ < 0): {len(firing)}")
    return wells, ranked, firing, scorer


if __name__ == "__main__":
    main()
