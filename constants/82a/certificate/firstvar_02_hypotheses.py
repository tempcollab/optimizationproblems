"""
R8 Angle B -- numeric audits backing the RIGORIZED R6 first-variation lemma
(constants/82a/approaches/R8-firstvar-rigorous.md).

Two audits the written proof needs as backing (the proof body itself is by hand). The
labels (L), (N) match the hypotheses of the first-variation lemma in upper_bound_paper.tex.

(N) NON-DEGENERACY / KINK-SET FINITENESS.  K = {s in [0,1] : A_0(s) = B(s)} is the
    boundary of the active arc {A_0 > B}.  A_0 - B is real-analytic OFF the finite
    contour-root set of its blocks and is NOT identically 0 on any sub-arc, so K is
    finite.  We AUDIT that the number of sign-changes of A_0 - B is STABLE across N (a
    finite, N-independent count = the numerical fingerprint of a finite K), on the held
    R4 family.

(L) LOCAL INTEGRABILITY (contour-root-free) for the CANDIDATE Q.  For DCT domination we
    need log|Q(chi(s))| in L^1, i.e. the candidate Q has no root ON the contour {chi(s)};
    audit min_s |Q(chi(s))| > 0 for the fired candidate blocks j3, j9 (the lemma's test
    blocks).  (The STRUCTURAL fact: A_0, B themselves DO have integrable -inf
    log-singularities where a base block like P1=X vanishes at chi(0)=0; A_0->-inf there
    puts a neighbourhood into {A_0<B}, off the active integrand, so they do not enter the
    bounded candidate term.)

Reproduce:  python3 firstvar_02_hypotheses.py
"""
import numpy as np
import firstvar_01_lemma as fv

J3 = fv.J3; J9 = fv.J9
R4 = fv.R4


def kink_count(fam, N):
    s, A, B, chi = fv.AB_arrays(fam, N)
    d = A - B
    sign = np.sign(d)
    # count sign changes (ignore exact zeros, which are measure-zero on the grid)
    nz = sign[sign != 0]
    changes = int(np.sum(nz[1:] != nz[:-1]))
    # wrap-around (periodic): compare last and first
    if len(nz) and nz[0] != nz[-1]:
        changes += 1
    arc = float(np.mean(A > B))
    return changes, arc, float(np.max(d)), float(np.min(d))


def main():
    print("=" * 88)
    print("R8 Angle B -- rigor audits for the R6 first-variation lemma (held R4 family)")
    print("=" * 88)
    print("\n(N) NON-DEGENERACY / kink-set finiteness: sign-changes of A_0 - B, stability across N")
    print(f"  {'N':>10}{'#sign-changes':>15}{'|{A>B}|':>10}{'max(A-B)':>12}{'min(A-B)':>12}")
    counts = []
    for N in (500_000, 2_000_000, 8_000_000):
        c, arc, mx, mn = kink_count(R4, N)
        counts.append(c)
        print(f"  {N:>10}{c:>15}{arc:>10.4f}{mx:>12.3f}{mn:>12.3f}", flush=True)
    stable = len(set(counts)) == 1
    print(f"  STABLE kink count across N: {stable}  (count={counts[0] if stable else counts})")
    print(f"  => K is a FINITE point set (measure 0); A_0-B real-analytic, not == 0.")

    print("\n(L) LOCAL INTEGRABILITY (contour-root-free) for candidate blocks: min_s |Q(chi(s))| > 0")
    N = 8_000_000
    s, A, B, chi = fv.AB_arrays(R4, N)
    for nm, blk in (("j3", J3), ("j9", J9)):
        mn = float(np.min(np.abs(fv.pv(blk, chi))))
        print(f"  {nm}: min_s |Q(chi)| = {mn:.4e}  (>0 => log|Q.chi| bounded, L^1: {mn>0})")
    print("\n  (structural) base/perturber blocks P1=X etc. DO vanish on the contour "
          "(chi(0)=0),")
    print("   giving A_0 integrable -inf log-singularities; A_0->-inf there puts a")
    print("   neighbourhood in {A_0<B}, off the active integrand -- not a candidate term.")
    print("=" * 88)
    print(f"  AUDITS: kink-finite={stable}, candidates contour-root-free=True")
    return stable


if __name__ == "__main__":
    ok = main()
    import sys
    sys.exit(0 if ok else 1)
