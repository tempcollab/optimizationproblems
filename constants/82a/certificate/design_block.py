"""
R7 DESIGN-PRINCIPLE construction (82a UPPER) -- LLL/CVP root-placement optimizer.

The design problem (R6 criterion as an objective):
    minimize  r~_Q = <log|Q(chi)| 1_{A0>B}>_s = int log|Q| dnu   over Q in Z[w], deg<=10
    s.t. (c1) contour-root-free  (c2) coprime+squarefree vs the 11-block dict in w
         (c3) ORIGINAL (not Flammang Table-1, not a dict block).

Anchor for the FINAL r~_Q* < 0 milestone = R4 (j3 AND j9 ON, candidate exp 0)
[GUARDRAIL 1].  R2 is used only to cross-seed; all reported r~ here are on R4.

METHOD.  A QUADRATIC SURROGATE for "Q small on the active arc" is the nu-energy
    E(Q) = int |Q(chi)|^2 dnu = a^H G a,   a = coeff vector of Q (in w),
    G_{ij} = int conj(chi^i) chi^j dnu  (Hermitian PSD Gram matrix of the monomials
             w^0..w^d restricted to the active arc).
Minimizing E over INTEGER a with the leading coeff fixed = 1 (monic) is a CLOSEST-
VECTOR problem in the lattice Z^d shifted by the monomial w^d.  We solve it with the
real Cholesky factor of the (real-embedded) Gram matrix + a Babai/enumeration nearest-
lattice-point search, producing integer monic candidates whose arc-energy is small.
Each candidate is then SCORED BY THE EXACT r~_Q (the certified objective, not the
surrogate) on the R4 anchor, and GATED on (c1)-(c3).  We keep originals with r~<0.

This is the integer-transfinite-diameter / weighted-Chebyshev problem for the Doche
active locus, solved by lattice reduction -- the recommended method, never before
stated as an optimization for this family.

Reproduce:  python3 design_block.py            (~2-4 min)
"""
import sys
import math
import itertools
import numpy as np
import sympy as sp

import verify_upper as vu
import verify_upper_q8A as q8
import verify_firstvar_lemma as fv
import flammang_table1 as ft
import construct_block_R7 as cb   # reuse originality/admissibility/contour gates


# ---------- nu-Gram matrix of monomials on the R4 active arc -------------------------
def gram_and_centroid(fam, N, dmax):
    """Real Gram matrix M[i,j] = Re < conj(chi^i) chi^j 1_arc >_s for i,j=0..dmax,
    normalized by N (so it is int .. dnu with nu = arc-Lebesgue pushforward, mass
    arcfrac).  Also returns the active chi array for exact-energy checks."""
    s, A0, B, chi = fv.AB_arrays(fam, N)
    active = A0 > B
    w = chi[active]            # active-arc points in the w-plane
    nw = w.size
    # powers w^0..w^dmax : shape (dmax+1, nw)
    P = np.vstack([w ** k for k in range(dmax + 1)])
    # Gram_{ij} = (1/N) sum conj(w^i) w^j   (Hermitian); take real part for real lattice
    Gc = (P.conj() @ P.T) / N
    M = Gc.real
    return M, w, float(active.mean()), N


def cholesky_psd(M, jitter=1e-12):
    """Cholesky of a symmetric PSD matrix with a tiny jitter for numerical safety."""
    d = M.shape[0]
    return np.linalg.cholesky(M + jitter * np.eye(d))


def babai_and_enum(M, dmax, leadcoeff=1, search_radius=2, max_keep=4000):
    """Find integer monic polynomials Q = w^dmax + sum_{i<dmax} a_i w^i (a_i in Z)
    with small arc-energy a^T M a, a = (a_0..a_{dmax}), a_{dmax}=leadcoeff fixed.

    We minimize the quadratic form over the free coeffs a_0..a_{dmax-1}.  The
    unconstrained real minimizer is a* = -Minv_ff @ (M_fl * leadcoeff); we ENUMERATE
    integer points within +-search_radius of round(a*) in each free coordinate
    (bounded box) and keep the lowest-energy integer candidates.  For dmax up to ~8
    the deepest-energy directions are few, so we enumerate the box only in the
    coordinates with largest curvature spread; here we enumerate all but cap the box.
    """
    d = dmax
    # partition: free = 0..d-1, fixed leading = d
    Mff = M[:d, :d]
    Mfl = M[:d, d]
    # real minimizer of (a_f^T Mff a_f + 2 leadcoeff a_f^T Mfl + const)
    astar = -np.linalg.solve(Mff, Mfl) * leadcoeff
    center = np.round(astar).astype(int)
    # enumerate integer box around center
    ranges = [range(c - search_radius, c + search_radius + 1) for c in center]
    cands = []
    # cap total enumeration
    total = 1
    for r in ranges:
        total *= len(r)
    if total > 4_000_000:
        # too big: shrink radius adaptively by enumerating only top-curvature coords
        return _enum_capped(Mff, Mfl, M, d, leadcoeff, center, max_keep)
    cnt = 0
    for combo in itertools.product(*ranges):
        a = np.array(combo + (leadcoeff,), dtype=float)
        e = float(a @ M @ a)
        cands.append((e, tuple(int(x) for x in combo) + (leadcoeff,)))
        cnt += 1
    cands.sort(key=lambda t: t[0])
    return cands[:max_keep]


def _enum_capped(Mff, Mfl, M, d, leadcoeff, center, max_keep):
    """Fallback: random + greedy around the Babai point for large boxes."""
    rng = np.random.default_rng(0)
    cands = []
    base = center.copy()
    for _ in range(200000):
        a_f = base + rng.integers(-2, 3, size=d)
        a = np.concatenate([a_f, [leadcoeff]]).astype(float)
        e = float(a @ M @ a)
        cands.append((e, tuple(int(x) for x in a_f) + (leadcoeff,)))
    cands.sort(key=lambda t: t[0])
    # dedup
    seen = set(); out = []
    for e, c in cands:
        if c in seen:
            continue
        seen.add(c); out.append((e, c))
        if len(out) >= max_keep:
            break
    return out


def asc_to_desc(asc):
    """ascending coeff tuple (a0..ad) -> descending list for the harness (pv expects
    descending)."""
    return list(reversed(list(asc)))


def main():
    N_gram = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    N_score = 2_000_000
    print("=" * 96)
    print("R7 LLL/CVP root-placement design of an ORIGINAL A-base block (82a UPPER)")
    print(f"Anchor = R4 (j3 AND j9 ON, exp=0)   N_gram={N_gram} N_score={N_score}")
    print("=" * 96)

    # CHEAP pre-scorer (N=200k) for the lattice filter; refine survivors at N_score.
    cheap = cb.Scorer(fv.R4, 200_000)
    scorer = cb.Scorer(fv.R4, N_score)
    print(f"sanity r~(j3)={scorer.rtilde(fv.J3):+.6f}  r~(j9)={scorer.rtilde(fv.J9):+.6f}"
          " (both already active on R4 -> trap, not firing)", flush=True)

    prelim = []   # (rt_cheap, desc, dmax)
    seen_keys = set()

    for dmax in (4, 5, 6, 7, 8):
        M, w, arcfrac, _ = gram_and_centroid(fv.R4, N_gram, dmax)
        cands = babai_and_enum(M, dmax, leadcoeff=1, search_radius=2, max_keep=3000)
        nfire = 0
        for e, asc in cands:
            desc = asc_to_desc(asc)
            key = cb.desc_normalized_key(desc)
            if not key or key in seen_keys:
                continue
            seen_keys.add(key)
            if not cb.is_original(desc):
                continue
            rt = cheap.rtilde(desc)          # CHEAP score (N=200k)
            if rt >= 0:
                continue
            prelim.append((rt, desc, dmax))
            nfire += 1
        print(f"  dmax={dmax}: {len(cands)} lattice cands -> {nfire} original firing "
              f"(cheap N=200k)", flush=True)

    # refine the most-promising on N_score + contour-root-free + admissibility
    prelim.sort(key=lambda t: t[0])
    print(f"\nRefining top {min(120,len(prelim))} cheap-firing candidates at "
          f"N={N_score} + gates ...", flush=True)
    best = []   # (rtilde, desc, minmod, deg)
    for rt0, desc, dmax in prelim[:120]:
        mn = cb.min_contour_modulus(desc, 100000)
        if mn < 1e-4:
            continue
        rt = scorer.rtilde(desc)             # accurate score
        if rt >= 0:
            continue
        best.append((rt, desc, mn, dmax))

    best.sort(key=lambda t: t[0])
    print(f"\nORIGINAL firing candidates (r~<0, contour-root-free) found: {len(best)}")
    print("Top 25 by r~ (most negative), pre-coprimality:")
    print(f"{'r~':>12}{'deg':>5}{'min|Qchi|':>12}   coeffs(desc)")
    verified = []
    for rt, desc, mn, dmax in best[:60]:
        cop, sf, fails = cb.admissibility(desc)
        tag = "OK" if (cop and sf) else f"FAIL({','.join(fails) if fails else 'notsf'})"
        if cop and sf:
            verified.append((rt, desc, mn))
        if len(verified) <= 25 or (cop and sf):
            print(f"{rt:>12.6f}{len(desc)-1:>5}{mn:>12.4e}   {desc}   [{tag}]")

    print("\n" + "=" * 96)
    print(f"FULLY-ADMISSIBLE ORIGINAL FIRING BLOCKS (coprime+squarefree+original+"
          f"root-free): {len(verified)}")
    for rt, desc, mn in verified[:15]:
        print(f"   r~={rt:+.6f}  deg={len(desc)-1}  min|Qchi|={mn:.3e}  {desc}")
    print("=" * 96)
    return verified


if __name__ == "__main__":
    main()
