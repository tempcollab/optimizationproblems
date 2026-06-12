"""
R8 Angle A -- the B-BRANCH first-variation marginal m_B(Q), with the NEW cross-term
that the R6 A-base lemma did NOT have, plus a finite-difference verification that
correctly MOVES D (outline-review correction R1: a B-perturber enters arg_B, which
ATTAINS D, so dD/dq_Q = deg(Q) != 0).

================================  THE MARGINAL  ================================
Held family: log h = <G>/D,  <G> = int_0^1 G ds,  G = max(A, B),
  A(s) = sum_i q_i log|P_i(chi)| + qG log|j3| + qH log|j9|         (A-branch)
  B(s) = log|Q1 Q2| + qE log|Q5| + qF log|Q6|                      (perturber branch)
  D    = max( arg_A , arg_B ),  arg_A = sum q_i deg P_i + qG*3 + qH*8 ,
                                arg_B = 56 + qE*12 + qF*16 .
On the held R4 family arg_B = 72.00 > arg_A = 61.66 (gap 10.34) -- the B-branch ATTAINS D.

Introduce a NEW B-perturber block Q (integer poly in w=chi) with exponent q_Q >= 0:
  B(s) -> B(s) + q_Q log|Q(chi(s))|   AND   arg_B -> arg_B + q_Q deg(Q)  (so D MOVES).

Quotient rule, with log h = <G>/D:
  d(log h)/dq_Q = [ d<G>/dq_Q * D - <G> * dD/dq_Q ] / D^2 .

  - ENVELOPE (Danskin) term: G = max(A, B), only B carries q_Q.  For s NOT on the kink
    set {A=B}: dG/dq_Q = (dB/dq_Q) * 1_{B>A} = log|Q(chi)| * 1_{B>A}.  The kink set has
    measure zero (A-B real-analytic, not identically 0); the moving-boundary term is
    2nd order because A-B = 0 ON {A=B} (continuity of the max across the kink).  Hence
        d<G>/dq_Q|_0 = int_{B>A} log|Q(chi)| ds .
    [ACTIVE REGION for a B-perturber = {B>A}, the COMPLEMENT of the A-base arc {A>B}.]

  - D-MOVEMENT term: arg_B attains D and arg_B is AFFINE in q_Q with slope deg(Q), so
    for |q_Q| < (arg_B - arg_A)/deg(Q) the max is unkinked and dD/dq_Q = deg(Q).
    On R4 gap/deg = 10.34/deg, e.g. 2.59 for deg 4 -- eps=1e-4 is deep inside.

Putting these together and using <G>/D = log h:
  d(log h)/dq_Q|_0 = (1/D) int_{B>A} log|Q| ds  -  (log h) * deg(Q) / D
                   = (1/D) [ int_{B>A} log|Q(chi)| ds  -  (log h) * deg(Q) ]
                   =: m_B(Q).

FIRING  <=>  m_B(Q) < 0  <=>  int_{B>A} log|Q| ds  <  (log h) * deg(Q).

The cross-term  -(log h) deg(Q)/D  is NEGATIVE (firing-favorable: REWARDS degree),
because growing D lowers log h = <G>/D.  This is the qualitatively new term absent
from the R6 A-base marginal r~_Q = (1/D) int_{A>B} log|Q| (no D-movement there, since
an A-base block enters the LOSING arg of D).

================================  THE CHECK  ================================
FD-vs-closed-form on the held R4 family at q_Q=0 (the correct anchor for a NEW
perturber).  CRITICAL (outline-review R1): the +-eps perturbed evaluation MUST move D:
  D(+-eps) = max( arg_A , arg_B0 +- eps*deg(Q) ).
A copy of the A-base FD path that holds D fixed would MISMATCH and falsely reject m_B.

Reproduce:  python3 firstvar_04_perturbing_marginal.py            (N=4_000_000, ~40s)
            python3 firstvar_04_perturbing_marginal.py 1000000     (faster, coarser)
"""
import sys
import math
import numpy as np

import bound_01_doche_base as vu
import bound_07_block_j9 as q8

# held R4 family (j3 AND j9 A-base ON; perturbers Q5,Q6 ON). The q_Q=0 anchor for a
# NEW perturber sits alongside the existing perturbers.
R4 = dict(q=[14.011500, 13.443930, 2.643590, 2.299880, 0.252420],
          qB=0.0, qC=0.0, qE=0.575080, qF=0.568800, qG=0.891590, qH=0.066860)


def pv(coef_desc, x):
    r = np.zeros_like(x)
    for c in coef_desc:
        r = r * x + c
    return r


def AB_arrays(fam, N):
    q = fam["q"]; qB = fam["qB"]; qC = fam["qC"]
    qE = fam["qE"]; qF = fam["qF"]; qG = fam["qG"]; qH = fam["qH"]
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


def args(fam, extra_deg=0.0, extra_q=0.0):
    """(arg_A, arg_B) for fam, with an EXTRA B-PERTURBER of degree extra_deg, exp
    extra_q added to arg_B (so D moves with the perturber)."""
    q = np.array(fam["q"])
    argA = float(np.dot(q, vu.DEGP)) + fam["qG"] * q8.DEG_Q7 + fam["qH"] * q8.DEG_Q8
    argB = (vu.DEGQ + fam["qE"] * q8.DEG_Q5 + fam["qF"] * q8.DEG_Q6
            + extra_q * extra_deg)
    return argA, argB


def closed_form_mB(fam, block_desc, block_deg, A, B, chi):
    """m_B(Q) = (1/D)[ int_{B>A} log|Q| ds - (log h) deg(Q) ].
    Returns (mB, intBgtA, logh, D, arcfrac_BgtA)."""
    logQ = np.log(np.abs(pv(block_desc, chi)))
    active_B = B > A                       # B-perturber active region
    intBgtA = float(np.mean(logQ * active_B))
    argA, argB = args(fam)
    D = max(argA, argB)
    G = np.maximum(A, B)
    logh = float(np.mean(G)) / D
    mB = (intBgtA - logh * block_deg) / D
    return mB, intBgtA, logh, D, float(np.mean(active_B))


def _logh_at(fam, block_desc, block_deg, qQ, A, B, chi, logQ):
    """log h with the B-perturber carried at exponent qQ. D RE-EVALUATED with the
    perturber degree added to arg_B (D MOVES -- outline-review R1)."""
    argA, argB = args(fam, extra_deg=block_deg, extra_q=qQ)
    D = max(argA, argB)
    G = np.maximum(A, B + qQ * logQ)       # perturber adds to the B branch
    return float(np.mean(G)) / D


def finite_diff_marginal_B(fam, block_desc, block_deg, eps, A, B, chi):
    """Central FD of d(log h)/dq_Q at q_Q=0 for a B-PERTURBER, with D MOVED."""
    logQ = np.log(np.abs(pv(block_desc, chi)))
    lp = _logh_at(fam, block_desc, block_deg, +eps, A, B, chi, logQ)
    lm = _logh_at(fam, block_desc, block_deg, -eps, A, B, chi, logQ)
    return (lp - lm) / (2.0 * eps)


# control blocks (DESCENDING): the reviewer's firing test block + an existing
# admissible perturber + a deg-2 sanity block.
BLOCKS = [
    ("X^2-X+1",     [1, -1, 1],          2, "sanity (reviewer FD ratio 0.99997)"),
    ("X^4-X^3-X+1", [1, -1, 0, -1, 1],   4, "reviewer FIRING test block (m_B*D=-0.209)"),
]


def run(N=4_000_000, eps=1e-4):
    print("=" * 100)
    print(f"R8 B-branch marginal m_B  closed-form vs FD (D MOVED)   N={N} eps={eps}")
    print("=" * 100)
    s, A, B, chi = AB_arrays(R4, N)
    argA, argB = args(R4)
    D = max(argA, argB)
    G = np.maximum(A, B)
    logh = float(np.mean(G)) / D
    fracB = float(np.mean(B > A))
    print(f"  held R4: arg_A={argA:.4f}  arg_B={argB:.4f}  D={D:.4f}  "
          f"(B attains D, gap={argB-argA:.4f})")
    print(f"  log h(R4) = {logh:.10f}   measure{{B>A}} = {fracB:.4f} "
          f"(complement of A-base arc 0.0686)")
    print(f"  cross-term coefficient -(log h)/D = {-logh/D:.6f} per unit degree "
          f"(degree-reward)")
    print()
    hdr = (f"{'block':<14}{'deg':>4}{'int_{B>A}logQ':>15}{'(logh)*deg':>13}"
           f"{'m_B':>13}{'m_B*D':>11}{'FD dlogh/dq':>14}{'ratio':>9}  fires")
    print(hdr)
    print("-" * len(hdr))
    all_ratio_ok = True
    for nm, desc, deg, note in BLOCKS:
        mB, intB, lh, Dd, _ = closed_form_mB(R4, desc, deg, A, B, chi)
        fd = finite_diff_marginal_B(R4, desc, deg, eps, A, B, chi)
        ratio = mB / fd if fd != 0 else float('nan')
        fires = mB < 0
        ok = abs(ratio - 1.0) < 5e-3
        all_ratio_ok = all_ratio_ok and ok
        print(f"{nm:<14}{deg:>4}{intB:>15.6f}{lh*deg:>13.6f}{mB:>13.3e}"
              f"{mB*Dd:>11.4f}{fd:>14.3e}{ratio:>9.4f}  "
              f"{'YES' if fires else 'no':<4}  [{note}]")
    print("-" * len(hdr))
    print(f"\n  closed-form m_B == FD (D moved) to <0.5% on all rows: "
          f"{'PASS' if all_ratio_ok else 'FAIL'}")
    print(f"  (the cross-term sign/magnitude is verified; firing <=> m_B<0)")
    return all_ratio_ok


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 4_000_000
    eps = float(sys.argv[2]) if len(sys.argv) > 2 else 1e-4
    ok = run(N, eps)
    sys.exit(0 if ok else 1)
