"""
R7 design optimizer, v2: ROOT-TARGET rounding + local lattice search.

Insight from design_block.py (v1) + the U^nu well map: the deep U^nu wells all sit
INSIDE the unit disk (|zeta| ~ 0.4..0.85), where NO single integer quadratic can place
a root (integer w^2-pw+q with q>=1 has |root|>=1, U^nu>0).  Firing blocks (j9,j13,j15..)
are IRREDUCIBLE high-degree polys whose CONJUGATE SET happens to include roots near the
wells -- the negative-U^nu roots outweigh the positive ones in r~ = sum U^nu(rho).

METHOD (root-target rounding).  Pick a set of target roots placed at/near the deepest
U^nu wells (conjugate-symmetric so the polynomial is real), form the monic real
polynomial  T(w) = prod (w - rho_target),  ROUND its coefficients to integers, and
LOCALLY perturb each non-leading coefficient by +-{0,1,2}.  Each integer candidate Q is
scored by the EXACT r~_Q on the R4 anchor and gated by originality + contour-root-free +
coprimality.  Because rounding the whole polynomial (not each root) keeps the root
configuration close to the wells, this reaches firing configurations the coordinate
energy-CVP missed.

Anchor = R4 (GUARDRAIL 1).  deg <= 10 (GUARDRAIL 3).
Reproduce:  python3 design_block2.py            (~2-4 min)
"""
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
import sys
import itertools
import numpy as np

import firstvar_01_lemma as fv
import construct_block_R7 as cb


def unu_wells(fam, N, n_wells=24):
    s, A0, B, chi = fv.AB_arrays(fam, N)
    active = A0 > B
    arc = chi[active]
    def U(zeta):
        return float(np.sum(np.log(np.abs(zeta - arc)))) / N
    res = np.linspace(-2.0, 1.3, 90)
    ims = np.linspace(0.0, 2.0, 70)   # upper half only (conjugate symmetry)
    RE, IM = np.meshgrid(res, ims)
    Z = (RE + 1j * IM).ravel()
    Uv = np.array([U(z) for z in Z])
    order = np.argsort(Uv)
    wells = []
    for idx in order:
        z = Z[idx]; u = Uv[idx]
        if z.imag < 0.02:
            continue
        if any(abs(z - w[0]) < 0.13 for w in wells):
            continue
        wells.append((z, u))
        if len(wells) >= n_wells:
            break
    return wells, U


def real_poly_from_conj_roots(conj_roots):
    """conj_roots: list of complex roots in the UPPER half plane; we add conjugates and
    build the monic real polynomial. Returns DESCENDING real coeff list."""
    roots = []
    for r in conj_roots:
        roots.append(r)
        roots.append(np.conj(r))
    p = np.poly(roots)   # descending, monic
    return p.real


def round_desc(p_real):
    return [int(round(c)) for c in p_real]


def main():
    N_well = int(sys.argv[1]) if len(sys.argv) > 1 else 600_000
    N_score = 2_000_000
    print("=" * 96)
    print("R7 ROOT-TARGET design of an ORIGINAL A-base block (v2)  Anchor=R4  deg<=10")
    print("=" * 96)

    wells, U = unu_wells(fv.R4, N_well, n_wells=20)
    print("Deepest U^nu wells (upper half, used as root targets):")
    for z, u in wells:
        print(f"   rho={z.real:+.4f}{z.imag:+.4f}j  U^nu={u:+.5f}", flush=True)

    cheap = cb.Scorer(fv.R4, 200_000)
    scorer = cb.Scorer(fv.R4, N_score)

    # Build target root sets: pick k conjugate pairs (k=1..5 -> deg 2..10) from the
    # deepest wells, in all combinations of the top wells.
    well_pts = [w[0] for w in wells]
    seen = set()
    topW = well_pts[:8]
    # collect ALL original candidate descs (deduped), then BATCH-score r~.
    all_descs = []
    for k in range(2, 6):            # k pairs -> degree 2k (4..10)
        for combo in itertools.combinations(range(len(topW)), k):
            roots = [topW[i] for i in combo]
            p_real = real_poly_from_conj_roots(roots)
            base = round_desc(p_real)
            if len(base) - 1 > 10:
                continue
            d = len(base)
            idxs = list(range(1, d))
            if 3 ** (d - 1) > 30000:
                idxs = idxs[-min(5, len(idxs)):]   # perturb lowest 5 coeffs only
            for deltas in itertools.product((-1, 0, 1), repeat=len(idxs)):
                desc = list(base)
                for ii, dl in zip(idxs, deltas):
                    desc[ii] = base[ii] + dl
                key = cb.desc_normalized_key(desc)
                if not key or key in seen:
                    continue
                seen.add(key)
                if not cb.is_original(desc):
                    continue
                all_descs.append(desc)
    print(f"\ntotal original candidate polys: {len(all_descs)} -- batch scoring r~ ...",
          flush=True)

    # batch-score in chunks
    prelim = {}
    CH = 4000
    for i0 in range(0, len(all_descs), CH):
        chunk = all_descs[i0:i0 + CH]
        rts = cheap.rtilde_batch(chunk)
        for desc, rt in zip(chunk, rts):
            if rt < -1e-6:
                prelim[cb.desc_normalized_key(desc)] = (float(rt), desc)
    print(f"cheap-firing original candidates: {len(prelim)}", flush=True)

    ranked = sorted(prelim.values(), key=lambda t: t[0])
    print(f"Refining top {min(200,len(ranked))} at N={N_score} + gates ...", flush=True)
    best = []
    for rt0, desc in ranked[:200]:
        mn = cb.min_contour_modulus(desc, 100000)
        if mn < 1e-4:
            continue
        rt = scorer.rtilde(desc)
        if rt >= 0:
            continue
        cop, sf, fails = cb.admissibility(desc)
        best.append((rt, desc, mn, cop and sf, fails))

    best.sort(key=lambda t: t[0])
    print(f"\nORIGINAL firing root-free candidates: {len(best)}")
    print(f"{'r~':>12}{'deg':>5}{'min|Qchi|':>12} adm   coeffs(desc)")
    for rt, desc, mn, adm, fails in best[:30]:
        tag = "OK" if adm else f"FAIL({','.join(fails) if fails else 'nsf'})"
        print(f"{rt:>12.6f}{len(desc)-1:>5}{mn:>12.3e} {tag:<14} {desc}", flush=True)

    fully = [(rt, desc, mn) for rt, desc, mn, adm, fails in best if adm]
    print("\n" + "=" * 96)
    print(f"FULLY-ADMISSIBLE ORIGINAL FIRING BLOCKS: {len(fully)}")
    for rt, desc, mn in fully[:15]:
        print(f"   r~={rt:+.6f}  deg={len(desc)-1}  min|Qchi|={mn:.3e}  {desc}")
    print("=" * 96)
    return fully


if __name__ == "__main__":
    main()
