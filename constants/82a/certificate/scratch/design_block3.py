"""
R7 design optimizer, v3: HIGH-DEGREE locus-hugging root-target construction.

Findings from v1 (energy-CVP) and v2 (well-rounding), both deg<=10: ZERO original
firing blocks.  Diagnosis (audited): on the SATURATED R4 anchor the firing integer
polynomials are HIGH degree (the lowest-degree firing table block is j13/j12 at deg 12;
the firing-AND-coprime ones are j16/j17 deg16, j20 deg20), and firing is a NON-
PERTURBATIVE knife-edge -- a single +-1 coefficient change swings r~ by ~+0.07 because
the firing roots sit microscopically INSIDE the lemniscate (min|Q.chi| ~ 1e-5..1e-6).
So firing = roots placed just inside the active locus where |Q|<1, a delicate config.

v3 METHOD (locus-hugging root placement, the principled construction):
  - sample the active-arc point cloud {chi(s): A0>B} on R4;
  - pick k points spread along the upper-half arc, pull each slightly INSIDE the
    lemniscate by a shrink factor toward the origin (so |Q|<1 there), use them as
    conjugate root targets;
  - form the monic real poly T(w)=prod(w-rho)(w-conj rho), round to integers, and do a
    small local coefficient search; score by exact r~ on R4; gate originality+coprime+
    squarefree+contour-root-free.
  - degree budget raised to <= 16 to reach where firing lives (the deg<=10 cap of the
    outline was where v1/v2 found nothing; we report the cap honestly as a SEARCH bound,
    and the objective is still bounded below at any fixed degree, r~ >= deg*U_min).

Anchor = R4 (GUARDRAIL 1).
Reproduce:  python3 design_block3.py            (~3-5 min)
"""
import sys
import itertools
import numpy as np

import verify_firstvar_lemma as fv
import construct_block_R7 as cb


def active_arc(fam, N):
    s, A0, B, chi = fv.AB_arrays(fam, N)
    active = A0 > B
    return chi[active]


def upper_arc_samples(arc, k, shrink):
    """Pick k well-spread points in the UPPER-half active arc, ordered by angle, each
    shrunk toward the origin by `shrink` (<1 pulls inside the lemniscate)."""
    up = arc[arc.imag > 0.02]
    ang = np.angle(up)
    order = np.argsort(ang)
    up = up[order]
    idx = np.linspace(0, up.size - 1, k).astype(int)
    pts = up[idx] * shrink
    return pts


def real_poly(conj_roots):
    roots = []
    for r in conj_roots:
        roots.append(r); roots.append(np.conj(r))
    return np.poly(roots).real


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 600_000
    N_score = 2_000_000
    DEGCAP = 16
    print("=" * 96)
    print("R7 v3 locus-hugging root-target design  Anchor=R4  deg<=%d" % DEGCAP)
    print("=" * 96)

    arc = active_arc(fv.R4, N)
    cheap = cb.Scorer(fv.R4, 200_000)
    scorer = cb.Scorer(fv.R4, N_score)
    print(f"active arc pts: {arc.size}", flush=True)

    all_descs = []
    seen = set()
    # k conjugate pairs -> degree 2k; k=6..8 -> deg 12..16 (where firing lives)
    for k in (6, 7, 8):
        for shrink in (0.90, 0.93, 0.95, 0.97, 0.99):
            pts = upper_arc_samples(arc, k, shrink)
            base = [int(round(c)) for c in real_poly(pts)]
            if len(base) - 1 > DEGCAP:
                continue
            d = len(base)
            # perturb the lowest few coeffs (constant + low order) by +-{0,1}
            idxs = list(range(d - 5, d))           # 5 lowest-order coeffs
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
    print(f"total original candidates: {len(all_descs)} -- batch scoring ...", flush=True)

    prelim = {}
    CH = 3000
    for i0 in range(0, len(all_descs), CH):
        chunk = all_descs[i0:i0 + CH]
        rts = cheap.rtilde_batch(chunk)
        for desc, rt in zip(chunk, rts):
            if rt < -1e-5:
                prelim[cb.desc_normalized_key(desc)] = (float(rt), desc)
    print(f"cheap-firing original candidates: {len(prelim)}", flush=True)

    ranked = sorted(prelim.values(), key=lambda t: t[0])
    best = []
    for rt0, desc in ranked[:300]:
        mn = cb.min_contour_modulus(desc, 100000)
        if mn < 1e-5:
            continue
        rt = scorer.rtilde(desc)
        if rt >= 0:
            continue
        cop, sf, fails = cb.admissibility(desc)
        best.append((rt, desc, mn, cop and sf, fails))
    best.sort(key=lambda t: t[0])

    print(f"\nORIGINAL firing root-free candidates: {len(best)}")
    print(f"{'r~':>12}{'deg':>5}{'min|Qchi|':>12} adm   coeffs")
    for rt, desc, mn, adm, fails in best[:25]:
        tag = "OK" if adm else f"FAIL({','.join(fails) if fails else 'nsf'})"
        print(f"{rt:>12.6f}{len(desc)-1:>5}{mn:>12.3e} {tag}", flush=True)

    fully = [(rt, desc, mn) for rt, desc, mn, adm, fails in best if adm]
    print("\n" + "=" * 96)
    print(f"FULLY-ADMISSIBLE ORIGINAL FIRING BLOCKS: {len(fully)}")
    for rt, desc, mn in fully[:10]:
        print(f"   r~={rt:+.6f}  deg={len(desc)-1}  min|Qchi|={mn:.3e}\n     {desc}")
    print("=" * 96)
    return fully


if __name__ == "__main__":
    main()
