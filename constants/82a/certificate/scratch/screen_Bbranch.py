"""
R8 Angle A step 3-4 -- DESIGN SCREEN for an improving B-PERTURBER block.

Minimize the verified B-branch marginal
   m_B(Q) = (1/D)[ int_{B>A} log|Q(chi)| ds - (log h) deg(Q) ]
(verified vs FD in firstvar_04_perturbing_marginal.py) over admissible integer perturbers Q,
on the held R4 anchor (q_Q=0).  FIRING <=> m_B < 0.

Admissibility (B-perturber; STRICTER than A-base -- run_state Rule):
  (c1) Q(0) = Q(1) = 1   (w-polynomial value at w=0 and w=1; perturbers REQUIRE this)
  (c2) coprime + squarefree (in w) vs the full active dictionary
       {P1,P2,P4,P6,P8,j3,j9, Q1,Q2,Q5,Q6}
  (c3) contour-root-free: min_s |Q(chi(s))| >= 1e-2  (so log|Q(chi)| in L^1)

Candidate sources:
  (A) Flammang Table-1 entries NOT already in the dictionary (the natural locus-hugging
      seeds; deg 7..22).  Table {j1,j3,j5,j8,j9,j12,j13,j15} are already dictionary.
  (B) ORIGINAL constructions: products of small admissible factors and the
      reviewer's firing seed X^4-X^3-X+1, to test whether an original block can
      beat the borrowed ones.

We rank by m_B (most negative first), gate (c1)-(c3) via sympy, and cross-check the
root-potential factorization
   m_B(Q) = sum_rho U^nu_B(rho) + deg*log|lead| - (log h)*deg/D ,
   U^nu_B(zeta) = < log|zeta - chi| 1_{B>A} >_s   (the {B>A} COMPLEMENT region),
to <1e-4 on the top candidate (outline-review R3: the cross-term is the FLAT
-(log h)/D = -0.003526 per unit degree).

Reproduce:  python3 screen_Bbranch.py            (N=2_000_000, ~60-90s)
"""
import sys
import math
import numpy as np
import sympy as sp

import bound_01_doche_base as vu
import bound_07_block_j9 as q8
import flammang_table1 as ft

R4 = dict(q=[14.011500, 13.443930, 2.643590, 2.299880, 0.252420],
          qB=0.0, qC=0.0, qE=0.575080, qF=0.568800, qG=0.891590, qH=0.066860)

X = sp.symbols('X')


def pv(coef_desc, x):
    r = np.zeros_like(x)
    for c in coef_desc:
        r = r * x + c
    return r


def sym_desc(d):
    n = len(d) - 1
    return sum(int(v) * X**(n - i) for i, v in enumerate(d))


def AB_arrays(fam, N):
    q = fam["q"]; qE = fam["qE"]; qF = fam["qF"]; qG = fam["qG"]; qH = fam["qH"]
    s = (np.arange(N) + 0.5) / N
    z = np.exp(2j * np.pi * s)
    chi = z * (1 - z)
    A = (sum(q[i] * np.log(np.abs(pv(vu.BASE[i], chi))) for i in range(5))
         + qG * np.log(np.abs(pv(q8.Q7, chi)))
         + qH * np.log(np.abs(pv(q8.Q8, chi))))
    B = (np.log(np.abs(pv(list(vu.Q1), chi))) + np.log(np.abs(pv(list(vu.Q2), chi)))
         + qE * np.log(np.abs(pv(list(q8.Q5), chi)))
         + qF * np.log(np.abs(pv(list(q8.Q6), chi))))
    return s, A, B, chi


# dictionary blocks (DESCENDING) for coprimality
DICT = {
    'P1': [1, 0], 'P2': [-1, 1], 'P4': list(vu.BASE[2]),
    'P6': list(vu.BASE[3]), 'P8': list(vu.BASE[4]),
    'j3': q8.Q7, 'j9': q8.Q8,
    'Q1': list(vu.Q1), 'Q2': list(vu.Q2), 'Q5': list(q8.Q5), 'Q6': list(q8.Q6),
}
DICT_SYM = {k: sym_desc(v) for k, v in DICT.items()}


def admissible(desc, chi):
    """Gate (c1)-(c3).  Returns (ok, reasons)."""
    reasons = []
    Q = sym_desc(desc)
    # c1
    if Q.subs(X, 0) != 1 or Q.subs(X, 1) != 1:
        reasons.append(f"Q(0)={Q.subs(X,0)},Q(1)={Q.subs(X,1)}!=1")
    # squarefree
    if sp.gcd(Q, sp.diff(Q, X)) != 1:
        reasons.append("not squarefree")
    # coprime to dictionary
    for k, Ds in DICT_SYM.items():
        if sp.gcd(Q, Ds) != 1:
            reasons.append(f"gcd({k})!=1")
    # contour-root-free
    mn = float(np.min(np.abs(pv(desc, chi))))
    if mn < 1e-2:
        reasons.append(f"min|Q(chi)|={mn:.2e}<1e-2")
    return (len(reasons) == 0), reasons, mn


def mB_of(desc, deg, A, B, chi, logh, D):
    logQ = np.log(np.abs(pv(desc, chi)))
    intB = float(np.mean(logQ * (B > A)))
    return (intB - logh * deg) / D, intB


def root_potential_mB(desc, A, B, chi, logh, D, N):
    """Cross-check m_B via roots: sum U^nu_B(rho) + deg*log|lead| - (logh)deg/D."""
    active = B > A
    chi_arc = chi[active]
    roots = np.roots(desc)
    lead = desc[0]
    deg = len(desc) - 1
    pot = sum(float(np.sum(np.log(np.abs(rho - chi_arc)))) / N for rho in roots)
    return pot + deg * math.log(abs(lead)) - logh * deg / D


def main(N=2_000_000):
    print("=" * 100)
    print(f"R8 B-perturber DESIGN SCREEN  (held R4 anchor, q_Q=0, N={N})")
    print("=" * 100)
    s, A, B, chi = AB_arrays(R4, N)
    q = np.array(R4["q"])
    argA = float(np.dot(q, vu.DEGP)) + R4["qG"] * q8.DEG_Q7 + R4["qH"] * q8.DEG_Q8
    argB = vu.DEGQ + R4["qE"] * q8.DEG_Q5 + R4["qF"] * q8.DEG_Q6
    D = max(argA, argB)
    logh = float(np.mean(np.maximum(A, B))) / D
    print(f"  arg_A={argA:.4f} arg_B={argB:.4f} D={D:.4f}  log h={logh:.10f}")
    print(f"  firing threshold: int_{{B>A}}log|Q| < (log h)*deg = {logh:.5f}*deg\n")

    # ----- candidate set A: Flammang Table-1 not already in dict -----
    used = {1, 3, 5, 8, 9, 12, 13, 15}   # table indices already dictionary blocks
    cands = []
    for j, (c, desc) in enumerate(ft._TABLE_DESCENDING, 1):
        if j in used:
            continue
        cands.append((f"j{j}", list(desc)))

    # ----- candidate set B: a few ORIGINAL constructions -----
    # reviewer firing seed and small admissible products (Q(0)=Q(1)=1 preserved
    # under multiplication of factors each with value 1 at w=0,1)
    seed = [1, -1, 0, -1, 1]                      # X^4-X^3-X+1 (reviewer firing)
    seed2 = [1, -1, 1]                            # X^2-X+1
    def poly_mul(a, b):
        return [int(c) for c in np.convolve(a, b)]
    originals = [
        ("X4-X3-X+1", seed),
        ("(X4-X3-X+1)^2", poly_mul(seed, seed)),
        ("(X4-X3-X+1)(X2-X+1)", poly_mul(seed, seed2)),
        ("(X4-X3-X+1)^3", poly_mul(poly_mul(seed, seed), seed)),
    ]

    results = []
    for nm, desc in cands + originals:
        deg = len(desc) - 1
        ok, reasons, mn = admissible(desc, chi)
        mB, intB = mB_of(desc, deg, A, B, chi, logh, D)
        results.append((nm, deg, mB, intB, ok, reasons, mn))

    results.sort(key=lambda r: r[2])   # most negative m_B first
    hdr = (f"{'block':<22}{'deg':>4}{'m_B':>13}{'m_B*D':>11}"
           f"{'int_BgtA':>11}{'min|Q|':>10}  adm  reasons")
    print(hdr)
    print("-" * (len(hdr) + 20))
    firing_admissible = []
    for nm, deg, mB, intB, ok, reasons, mn in results:
        fires = mB < 0
        tag = ("FIRE" if fires else "dry ")
        admtag = "OK " if ok else "NO "
        rs = "" if ok else ";".join(reasons[:2])
        print(f"{nm:<22}{deg:>4}{mB:>13.3e}{mB*D:>11.4f}{intB:>11.5f}"
              f"{mn:>10.2e}  {admtag}{tag}  {rs}")
        if ok and fires:
            firing_admissible.append((nm, deg, mB, list(
                next(d for n, d in cands + originals if n == nm))))

    print("-" * (len(hdr) + 20))
    print(f"\nFIRING + ADMISSIBLE candidates (m_B<0, gates pass), most-negative first:")
    firing_admissible.sort(key=lambda r: r[2])
    for nm, deg, mB, desc in firing_admissible:
        print(f"  {nm:<22} deg={deg:>3}  m_B={mB:.3e}  m_B*D={mB*D:.4f}")
    if not firing_admissible:
        print("  (none)")

    # root-potential cross-check on the top firing-admissible candidate
    if firing_admissible:
        nm, deg, mB, desc = firing_admissible[0]
        rp = root_potential_mB(desc, A, B, chi, logh, D, N)
        print(f"\nRoot-potential cross-check on TOP candidate {nm}:")
        print(f"  direct m_B            = {mB:.8f}")
        print(f"  sum U^nu_B + deg*log|lead| - (logh)deg/D = {rp:.8f}")
        print(f"  |diff| = {abs(mB-rp):.2e}  "
              f"({'MATCH' if abs(mB-rp) < 1e-4 else 'MISMATCH'})")
    return firing_admissible


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2_000_000
    main(N)
