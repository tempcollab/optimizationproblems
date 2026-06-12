"""
R6 Angle 1 (HEADLINE): the FIRST-VARIATION LEMMA for the 82a upper construction.

================================  LEMMA  ================================
Let the held upper family be  log h = (1/D) * <G>_s ,  G(s) = max(A(s), B(s)),
on  s in [0,1],  chi(s) = z(1-z),  z = e^{2 pi i s}, with
    A(s) = sum_i q_i log|P_i(chi)| + (A-base terms)
    B(s) = log|Q1 Q2| + (perturber terms),
    D    = max( sum q_i deg P_i + (A-base degs) , 56 + (perturber degs) ),
exactly as in bound_07_block_j9.float_value_q8A and _Dval.

Introduce a NEW A-base block Q (integer poly) with exponent q_Q >= 0:
    A(s) |-> A(s) + q_Q * log|Q(chi(s))| .
Suppose, at the BASE family (q_Q = 0), the B-branch attains D, i.e.
    arg_A := sum q_i deg P_i + (A-base degs)  <  arg_B := 56 + (perturber degs) = D .
Then D is locally constant in q_Q (it stays = arg_B until arg_A catches up,
which needs q_Q*deg(Q) > arg_B - arg_A), so dD/dq_Q = 0 near q_Q = 0, and

    d(log h)/dq_Q |_{q_Q=0}  =  (1/D) * < log|Q(chi)| * 1_{A_0 > B} >_s   =:  (1/D) * r~_Q ,

where A_0, B and the active set {A_0 > B} are those of the BASE family BEFORE Q is
switched on.  Define the ACTIVE-ARC LOG-FUNCTIONAL
    r~_Q := < log|Q(chi)| * 1_{A_0>B} >_s  =  (1/(2 pi)) int_{A_0>B} log|Q(chi(t))| dt .
COROLLARY (firing criterion):
    Q FIRES (a small q_Q>0 LOWERS log h)  <=>  d(log h)/dq_Q|_0 < 0  <=>  r~_Q < 0 ,
i.e. Q is, on average over the active arc, INSIDE the unit lemniscate |Q|<1.

================================  PROOF  ================================
1. Quotient rule: d(log h)/dq_Q = [ d<G>/dq_Q * D - <G> * dD/dq_Q ] / D^2.
   Under the hypothesis arg_A < arg_B, dD/dq_Q = 0 in a neighbourhood of q_Q=0,
   so the second term vanishes:  d(log h)/dq_Q = (1/D) d<G>/dq_Q.   (D-CONSTANCY)
2. DANSKIN / ENVELOPE.  G(s,q_Q) = max(A(s,q_Q), B(s)), with only A depending on q_Q
   and dA/dq_Q = log|Q(chi(s))|.  For each fixed s NOT on the kink set {A_0 = B}:
     - if A_0(s) > B(s):  near q_Q=0, G = A, so dG/dq_Q = log|Q(chi(s))|;
     - if A_0(s) < B(s):  near q_Q=0, G = B, so dG/dq_Q = 0.
   The kink set {A_0 = B} has Lebesgue measure zero (A_0 - B is real-analytic, not
   identically 0).  Differentiating under the integral (G is Lipschitz in q_Q,
   uniformly bounded gradient log|Q| in L^1) gives
     d<G>/dq_Q|_0 = < dG/dq_Q |_0 >_s = < log|Q(chi)| 1_{A_0>B} >_s = r~_Q.
   The active-set BOUNDARY motion (the set {A>B} shifts as q_Q grows) is a SECOND-
   order effect: at the boundary A_0 = B, the two branches are EQUAL, so moving the
   integration limit there changes the integrand value by 0 to first order
   (the standard envelope-theorem boundary-term cancellation).  Hence r~_Q is exact
   to first order; the support-shrink enters only at O(q_Q^2).
3. Combine 1 and 2:  d(log h)/dq_Q|_0 = (1/D) r~_Q.   QED.

================================  CHECK  ================================
For each candidate block on its CORRECT ANCHOR family (the family that does NOT yet
contain it; r~ is a FIRST VARIATION AT q_Q=0, so it must be measured where q_Q=0):
    j3 -> R11 family  (no A-base block at all)
    j9 -> R2  family  (has j3 A-base, NOT j9)
    j6 -> R2  family  (the family it was screened against; DRY)
    j7 -> R2  family  (DRY)
We (a) compute the closed-form r~_Q and the predicted marginal (1/D) r~_Q;
   (b) compute the finite-difference d(log h)/dq_Q by perturbing q_Q to +eps on the
       SAME anchor family (this re-evaluates A, G, D at q_Q=eps -- a fully independent
       measurement, NOT reusing the base active set);
   (c) assert closed-form ~ finite-diff (ratio ~1) AND the SIGN correctly predicts
       FIRED (r~<0) vs DRY (r~>=0), including the j9-vs-j6 inversion.

WRONG-ANCHOR CONTROL: we also print r~(j9) on the SATURATED R4 family (which already
contains j9).  There the first variation is at the WRONG (already-active) point and
gives r~>0 / FD>0 -- the documented trap.  This row is a NEGATIVE control, NOT a test
of the lemma.

Reproduce:  python3 firstvar_01_lemma.py            (N=4_000_000, ~30-60s)
            python3 firstvar_01_lemma.py 1000000     (faster, coarser)
"""
import sys
import math
import numpy as np

import bound_01_doche_base as vu
import bound_07_block_j9 as q8

# ---- Block definitions (DESCENDING coeffs), from the harness / Flammang table ----
# NUMBERING: campaign jk == ft._TABLE_DESCENDING[k-1] (the screen_swap_R5._TAB map).
J3 = [1, 1, -2, 1]                                  # campaign j3 (deg 3)  == table j3
J9 = [1, -1, 0, -3, 15, -22, 16, -6, 1]             # campaign j9 (deg 8)  == table j9
J6 = [2, -5, 6, 2, -11, 11, -5, 1]                  # campaign j6 (deg 7)  == table j6  (DRY)
J7 = [1, -2, 4, -7, 13, -16, 12, -5, 1]             # campaign j7 (deg 8)  == table j7  (DRY)

# ---- Anchor families (the family with the candidate's exponent = 0) --------------
# R11 family: perturbers Q5,Q6 only; NO A-base block (qG=qH=0). Anchor for j3.
R11 = dict(q=[13.937341, 12.515102, 2.541409, 2.068537, 0.753965],
           qB=0.0, qC=0.0, qE=0.891271, qF=0.246614, qG=0.0, qH=0.0)
# R2 family: j3 A-base ON (qG), j9 OFF (qH=0). Anchor for j9, j6, j7.
R2 = dict(q=[14.283862, 13.947194, 2.593425, 2.283539, 0.249084],
          qB=0.0, qC=0.0, qE=0.577911, qF=0.565724, qG=0.893516, qH=0.0)
# R4 family (SATURATED: j3 AND j9 both ON). WRONG anchor for j9 -- negative control.
R4 = dict(q=[14.011500, 13.443930, 2.643590, 2.299880, 0.252420],
          qB=0.0, qC=0.0, qE=0.575080, qF=0.568800, qG=0.891590, qH=0.066860)


def pv(coef_desc, x):
    """Horner eval of a DESCENDING-coefficient polynomial at array x."""
    r = np.zeros_like(x)
    for c in coef_desc:
        r = r * x + c
    return r


def AB_arrays(fam, N):
    """Return s-grid, A_0(s), B(s) and chi(s) for an anchor family `fam`
    (using EXACTLY the harness's float_value_q8A convention)."""
    q = fam["q"]; qB = fam["qB"]; qC = fam["qC"]
    qE = fam["qE"]; qF = fam["qF"]; qG = fam["qG"]; qH = fam["qH"]
    s = (np.arange(N) + 0.5) / N
    z = np.exp(2j * np.pi * s)
    chi = z * (1 - z)
    A = (sum(q[i] * np.log(np.abs(pv(vu.BASE[i], chi))) for i in range(5))
         + qG * np.log(np.abs(pv(q8.Q7, chi)))      # j3 A-base (Q7)
         + qH * np.log(np.abs(pv(q8.Q8, chi))))     # j9 A-base (Q8); 0 on R11/R2
    B = (np.log(np.abs(pv(list(vu.Q1), chi))) + np.log(np.abs(pv(list(vu.Q2), chi)))
         + qB * np.log(np.abs(pv(list(q8.Q3), chi)))
         + qC * np.log(np.abs(pv(list(q8.Q4), chi)))
         + qE * np.log(np.abs(pv(list(q8.Q5), chi)))
         + qF * np.log(np.abs(pv(list(q8.Q6), chi))))
    return s, A, B, chi


def Dval(fam, extra_deg=0.0, extra_q=0.0):
    """D for anchor family fam, optionally with an EXTRA A-base block of degree
    `extra_deg` and exponent `extra_q` (so the finite-difference re-evaluates D
    exactly as the construction would). Mirrors q8._Dval."""
    q = np.array(fam["q"])
    argA = (float(np.dot(q, vu.DEGP))
            + fam["qG"] * q8.DEG_Q7 + fam["qH"] * q8.DEG_Q8
            + extra_q * extra_deg)
    argB = (vu.DEGQ + fam["qB"] * q8.DEG_Q3 + fam["qC"] * q8.DEG_Q4
            + fam["qE"] * q8.DEG_Q5 + fam["qF"] * q8.DEG_Q6)
    return max(argA, argB), argA, argB


def closed_form_rtilde(fam, block_desc, A, B, chi):
    """r~_Q = < log|Q(chi)| * 1_{A_0>B} >_s  (the base-family active arc)."""
    logQ = np.log(np.abs(pv(block_desc, chi)))
    active = A > B
    return float(np.mean(logQ * active)), float(np.mean(active))


def _logh_at(fam, block_desc, block_deg, qQ, A0, B, chi, logQ):
    """log h = <max(A0 + qQ*logQ, B)>_s / D(qQ) for the anchor family with the
    candidate block carried at exponent qQ. D re-evaluated exactly."""
    D, _, _ = Dval(fam, extra_deg=block_deg, extra_q=qQ)
    G = np.maximum(A0 + qQ * logQ, B)
    return float(np.mean(G)) / D


def finite_diff_marginal(fam, block_desc, block_deg, eps, A0, B, chi):
    """d(log h)/dq_Q at q_Q=0 by a CENTRAL finite difference (cancels the O(eps)
    active-set-shift second-order term, leaving O(eps^2)).  Each evaluation
    INDEPENDENTLY re-evaluates A=A0+qQ*logQ, G=max(A,B) and D -- it does NOT reuse
    the base active set.  (The +-eps evaluation of the smooth scalar <G>/D is a
    legitimate numerical derivative even though only q_Q>=0 is a valid construction.)
    """
    logQ = np.log(np.abs(pv(block_desc, chi)))
    D0, argA0, argB0 = Dval(fam)
    Dp, argAp, _ = Dval(fam, extra_deg=block_deg, extra_q=eps)
    lp = _logh_at(fam, block_desc, block_deg, +eps, A0, B, chi, logQ)
    lm = _logh_at(fam, block_desc, block_deg, -eps, A0, B, chi, logQ)
    d_emp = (lp - lm) / (2.0 * eps)
    return d_emp, D0, argA0, argB0, Dp, argAp


def run(N=4_000_000, eps=1e-4):
    print("=" * 96)
    print(f"R6 first-variation lemma -- closed-form vs finite-difference  "
          f"(N={N}, eps={eps})")
    print("=" * 96)

    # candidate -> (block, deg, anchor family name, anchor dict, expected, is_test)
    cases = [
        ("j3", J3, 3, "R11", R11, "FIRED", True),
        ("j9", J9, 8, "R2",  R2,  "FIRED", True),
        ("j6", J6, 7, "R2",  R2,  "DRY",   True),
        ("j7", J7, 8, "R2",  R2,  "DRY",   True),
        # negative control: wrong anchor for j9 (already saturated) -- NOT a test
        ("j9", J9, 8, "R4*", R4,  "TRAP",  False),
    ]

    hdr = (f"{'blk':<4}{'anchor':<7}{'arg_A':>9}{'arg_B':>9}{'D':>10}"
           f"{'|act arc|':>10}{'r~_Q':>12}{'(1/D)r~':>13}"
           f"{'FD dlogh/dq':>14}{'ratio':>9}  pred  exp")
    print(hdr)
    print("-" * len(hdr))

    all_pass = True
    test_rows = []
    for name, blk, deg, anm, fam, exp, is_test in cases:
        s, A0, B, chi = AB_arrays(fam, N)
        rt, arcfrac = closed_form_rtilde(fam, blk, A0, B, chi)
        d_emp, D0, argA0, argB0, Deps, argAeps = finite_diff_marginal(
            fam, blk, deg, eps, A0, B, chi)
        pred_marg = rt / D0
        ratio = pred_marg / d_emp if d_emp != 0 else float('nan')
        pred = "FIRED" if rt < 0 else "DRY"
        if name == "j9" and not is_test:
            pred = "TRAP+" if rt > 0 else "TRAP-"
        sign_ok = (pred == exp) if is_test else True
        # D-constancy check: arg_A must stay below arg_B under the eps perturbation
        dconst = argAeps < argB0
        print(f"{name:<4}{anm:<7}{argA0:>9.3f}{argB0:>9.3f}{D0:>10.4f}"
              f"{arcfrac:>10.4f}{rt:>12.5f}{pred_marg:>13.3e}"
              f"{d_emp:>14.3e}{ratio:>9.4f}  {pred:<5} {exp}")
        if is_test:
            test_rows.append((name, exp, pred, ratio, dconst, sign_ok))
            all_pass = all_pass and sign_ok

    print("-" * len(hdr))
    print("\nPer-test-row assertions:")
    # j9, j6, j7 are the clean quantitative rows (close-to-1 ratio); j3 is sign-only.
    quant_ok = True
    for name, exp, pred, ratio, dconst, sign_ok in test_rows:
        sign_str = "SIGN-OK" if sign_ok else "SIGN-FAIL"
        # quantitative identity match for j9/j6/j7 (j3 is degenerate -> sign only)
        if name in ("j9", "j6", "j7"):
            q_ok = abs(ratio - 1.0) < 0.05
            quant_ok = quant_ok and q_ok
            qstr = f"ratio={ratio:.4f} ({'MATCH' if q_ok else 'OFF'})"
        else:
            qstr = f"ratio={ratio:.4f} (sign-only row)"
        dstr = "D-const-OK" if dconst else "D-SWITCHED"
        print(f"  {name:<4} anchor exp={exp:<6} pred={pred:<6} {sign_str}  "
              f"{qstr}  {dstr}")

    print("\nKey separations:")
    # j9 fires, j6 dry on the SAME R2 anchor (the inversion the explorer's r_Q got wrong)
    j9row = next(r for r in test_rows if r[0] == "j9")
    j6row = next(r for r in test_rows if r[0] == "j6")
    inv_ok = (j9row[2] == "FIRED" and j6row[2] == "DRY")
    print(f"  j9 FIRED vs j6 DRY on the SAME R2 anchor (un-normalized lemma): "
          f"{'RECOVERED' if inv_ok else 'FAILED'}")

    overall = all_pass and quant_ok and inv_ok
    print("\n" + "=" * 96)
    print(f"  FIRST-VARIATION LEMMA CHECK: {'PASS' if overall else 'FAIL'}")
    print("  (sign predicts fired/dry for all 4 test rows; closed-form == finite-diff")
    print("   to <5% on the clean rows j9/j6/j7; j9>j6 inversion recovered un-normalized.)")
    print("=" * 96)
    return overall


def root_potential_check(N=2_000_000):
    """LEMMA step 5 cross-check (potential-theoretic identification of r~_Q).

    With nu = pushforward of arc-Lebesgue measure (restricted to {A0>B}) under
    s |-> chi(s), the active-arc functional factors over Q's roots:
        r~_Q = < log|Q(chi)| 1_{A0>B} >_s
             = sum_{rho: Q(rho)=0} U^nu(rho)  +  deg(Q) * log|lead(Q)|,
    where U^nu(zeta) = int log|zeta - chi| dnu = < log|zeta - chi| 1_{A0>B} >_s is the
    logarithmic potential of nu.  This shows the marginal gain is the SUM OF THE
    ARC-POTENTIAL evaluated at Q's roots -- Q fires iff its roots sit where U^nu is
    most negative, i.e. near the equilibrium-type measure of the active locus.

    We verify the identity numerically for j3 (deg 3, leading coeff 1) on R11.
    """
    print("=" * 72)
    print(f"LEMMA step 5 -- root-potential identity for r~_Q  (j3 on R11, N={N})")
    print("=" * 72)
    fam = R11
    blk = J3
    s, A0, B, chi = AB_arrays(fam, N)
    active = A0 > B
    chi_arc = chi[active]
    # LHS: r~_Q directly
    logQ = np.log(np.abs(pv(blk, chi)))
    lhs = float(np.mean(logQ * active))
    # roots of j3 = X^3 + X^2 - 2X + 1 (DESCENDING -> numpy poly1d expects descending)
    roots = np.roots(blk)
    lead = blk[0]
    # U^nu(rho) = < log|rho - chi| 1_arc >_s    (sum over the active grid / N)
    pot = []
    for rho in roots:
        u = float(np.sum(np.log(np.abs(rho - chi_arc)))) / N
        pot.append(u)
    rhs = sum(pot) + (len(blk) - 1) * math.log(abs(lead))
    print(f"  j3 roots: {np.round(roots, 6).tolist()}   leading coeff = {lead}")
    for rho, u in zip(roots, pot):
        print(f"    U^nu(rho={rho:+.5f}) = {u:+.6f}")
    print(f"  sum U^nu(roots) + deg*log|lead| = {rhs:.8f}")
    print(f"  r~_Q  (direct)                  = {lhs:.8f}")
    print(f"  |LHS - RHS| = {abs(lhs - rhs):.2e}  "
          f"({'MATCH' if abs(lhs - rhs) < 1e-5 else 'MISMATCH'})")
    ok = abs(lhs - rhs) < 1e-5
    print(f"  ROOT-POTENTIAL IDENTITY: {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "roots":
        N = int(sys.argv[2]) if len(sys.argv) > 2 else 2_000_000
        ok = root_potential_check(N)
        sys.exit(0 if ok else 1)
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 4_000_000
    eps = float(sys.argv[2]) if len(sys.argv) > 2 else 1e-4
    ok = run(N, eps)
    sys.exit(0 if ok else 1)
