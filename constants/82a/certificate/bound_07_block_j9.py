"""
R4 (this campaign) RIGOROUS upper-bound certificate for C_82, free-exponent family
with a SECOND new low-degree admissible block Q8 = Flammang j9 (deg 8) added as a
SECOND NEW A-BASE block (the prod-P^q base side) on top of the held R2 family

  h = Q1*Q2 * Q5^qE * Q6^qF * (prod P_i^q_i) * j3^qG

(Q5=Flammang j13 deg12, Q6=Flammang j15 deg16, j3=Flammang j3 deg3 first A-base block).

This is Angle 1 of the R4 spec: a SECOND new block enters the BASE product
prod_m P_m^{q_m} (the A-branch) alongside the first A-base block j3.  Doche's Doc01a
§4 framework lets the base set {P_m} be enlarged freely: pick base polys and
perturbing polys, with condition (4) (the integer-polynomial dictionary is
coprime/non-degenerate), and

  D = 2b * max( sum_m q_m deg P_m , deg Q_{l+1} + sum_m q_{k+m} deg Q_m ).

The new SECOND base block Q8 = j9 (deg 8) with exponent qH>=0 therefore adds
+qH*log|j9| to the A-branch and +qH*deg j9 = +qH*8 to the FIRST argument of the
D-max (the sum-q-deg-P branch).

Family (CERTIFIED angle has qB=qC=0):
  A(t) = sum_i q_i*(1/2)log|P_i|^2  +  qG*(1/2)log|j3|^2  +  qH*(1/2)log|j9|^2
  B(t) = (1/2)log|Q1|^2 + (1/2)log|Q2|^2
          + qB*(1/2)log|Q3|^2 + qC*(1/2)log|Q4|^2
          + qE*(1/2)log|Q5|^2 + qF*(1/2)log|Q6|^2               (Q-branch, UNCHANGED)
  G(t) = max(A(t), B(t))
  log h = (1/(2 pi D)) int_0^{2pi} G dt,
  D = max( sum_i q_i deg P_i + qG*deg j3 + qH*deg j9 ,
           56 + qB*deg Q3 + qC*deg Q4 + qE*deg Q5 + qF*deg Q6 ).

ANCHOR identity:
  - At qH=0 this collapses EXACTLY to bound_06_block_j3 at (q,qB,qC,qE,qF,qG):
    A loses the j9 term, D's first argument loses +qH*8 -> BIT-IDENTICAL.

Per-cell enclosure machinery reused VERBATIM from bound_01_doche_base.py.  j9 is added to the
A-branch with weight qH, mechanically identical to any other P/j3 factor (same
rho_full, weighted, outward-rounded).  Because the integrand changed, the mpmath
soundness selftest (selftest_q8A) is re-run on THIS integrand (A now has qH*log|j9|).

Validity: Doc01a Lemmas 2,3,4,5 give log h(q,qB,qC,qE,qF,qG,qH) as a true limit point
of the ZZ spectrum for any admissible exponents >= 0 (no optimality needed), hence
C_82 <= log h.  Admissibility is verified by admissibility_check_q8A() -- for the
certified Angle (qB=qC=0) the active dictionary is the integer-polynomial product
{P1,P2,P4,P6,P8,j3,j9} on the base side and {Q1,Q2,Q5,Q6} on the perturber side, all
pairwise coprime, with the two new base blocks j3,j9 deg>0, squarefree, mutually
coprime, and coprime to every other active factor (condition (4) non-degenerate).
A Doche BASE poly need NOT satisfy P(0)=P(1)=1.

THE COMPARISON TARGET is the CURRENT held UPPER value 0.2538925359 (R2 this campaign),
NOT the superseded R11 value.  certify/tamper compare against HELD_CERT below.

Usage:
  python3 bound_07_block_j9.py anchor                  # qH=0 -> q7A BIT-IDENTICAL
  python3 bound_07_block_j9.py admiss
  python3 bound_07_block_j9.py selftest q1..q5 qB qC qE qF qG qH
  python3 bound_07_block_j9.py certify q1..q5 qB qC qE qF qG qH [M0] [max_refine] [rem_cap]
  python3 bound_07_block_j9.py tamper q1..q5 qB qC qE qF qG qH bogus_target
"""

import os
import sys
import time
import math
import numpy as np

import bound_00_flammang_baseline as vv
import bound_01_doche_base as vu
import bound_05_block_j15 as vq6
import bound_06_block_j3 as vq7A  # for qH=0 anchor cross-check (q8A == q7A at qH=0)

NINF = -np.inf
PINF = np.inf
na = np.nextafter

Q3 = vq6.Q3; DEG_Q3 = vq6.DEG_Q3; ASC_Q3 = vq6.ASC_Q3
Q4 = vq6.Q4; DEG_Q4 = vq6.DEG_Q4; ASC_Q4 = vq6.ASC_Q4
Q5 = vq6.Q5; DEG_Q5 = vq6.DEG_Q5; ASC_Q5 = vq6.ASC_Q5
Q6 = vq6.Q6; DEG_Q6 = vq6.DEG_Q6; ASC_Q6 = vq6.ASC_Q6

# Q7 = j3 (deg 3): the FIRST A-base block, held from R2.  DESCENDING coeffs.
Q7 = [1, 1, -2, 1]
DEG_Q7 = len(Q7) - 1
ASC_Q7 = vu.asc(Q7)

# Q8 = j9 (deg 8): the SECOND new A-base block this round.  DESCENDING coeffs,
# verbatim from flammang_table1.py _TABLE_DESCENDING j=9.
Q8 = [1, -1, 0, -3, 15, -22, 16, -6, 1]
DEG_Q8 = len(Q8) - 1
ASC_Q8 = vu.asc(Q8)

DEGP = vu.DEGP                        # [1,1,4,8,8]
DEGQ12 = vu.DEGQ                      # 56


def _Dval(q, qB, qC, qE, qF, qG, qH):
    # A-branch: j3 (qG) and j9 (qH) BOTH add to the FIRST (sum q deg P) argument.
    return max(float(np.dot(q, DEGP) + qG * DEG_Q7 + qH * DEG_Q8),
               float(DEGQ12 + qB * DEG_Q3 + qC * DEG_Q4
                     + qE * DEG_Q5 + qF * DEG_Q6))


def _sum_lo(terms):
    """Rigorous DOWNWARD-rounded sum of nonnegative floats."""
    acc = 0.0
    for t in terms:
        acc = na(acc + t, NINF)
    return acc


def _prod_lo(x, k):
    """Downward-rounded x*k for nonnegative x and exact integer k."""
    return na(float(x) * float(k), NINF)


def _Dval_lo(q, qB, qC, qE, qF, qG, qH):
    """A rigorous LOWER bound on D = max(arg_A, arg_B).

    D is the DENOMINATOR of log h = (int G)/D, so an UPPER bound on log h needs a
    LOWER bound on D.  Each argument is a sum of nonnegative products
    (exponent >= 0) x (exact integer degree); we round every product and partial
    sum toward -inf, then take the max of the two lower-bounded arguments (a lower
    bound on the max).  Exponents/degrees are nonnegative here, so this is sound.
    """
    argA = _sum_lo([_prod_lo(q[i], int(DEGP[i])) for i in range(len(DEGP))]
                   + [_prod_lo(qG, DEG_Q7), _prod_lo(qH, DEG_Q8)])
    argB = _sum_lo([float(DEGQ12),
                    _prod_lo(qB, DEG_Q3), _prod_lo(qC, DEG_Q4),
                    _prod_lo(qE, DEG_Q5), _prod_lo(qF, DEG_Q6)])
    return max(argA, argB)


# ---------------------------------------------------------------------------
def cell_AB_q8A(a, b, q, qB, qC, qE, qF, qG, qH):
    m = 0.5 * (a + b)
    r = 0.5 * (b - a)
    Wc, DWc, DDWc, DDDWc = vu.w_full_cell(a, b)
    Wm, DWm, DDWm, DDDWm = vu.w_full_point(m)

    def slope_abs_up(rho_m, rhop_m):
        num = 0.5 * np.maximum(np.abs(rhop_m[0]), np.abs(rhop_m[1]))
        den = rho_m[0]
        return np.where(den > 0, na(num / np.where(den > 0, den, 1.0), PINF), PINF)

    # ---- A branch: sum_i q_i (1/2)log|P_i|^2 + qG*(1/2)log|j3|^2 + qH*(1/2)log|j9|^2 ----
    A_hi = np.zeros_like(a)
    A_lo = np.zeros_like(a)
    A_mid_up = np.zeros_like(a)
    A_curv = np.zeros_like(a)
    A_slope = np.zeros_like(a)
    Afactors = [("P1", vu.ASC["P1"], float(q[0])),
                ("P2", vu.ASC["P2"], float(q[1])),
                ("P4", vu.ASC["P4"], float(q[2])),
                ("P6", vu.ASC["P6"], float(q[3])),
                ("P8", vu.ASC["P8"], float(q[4])),
                ("j3", ASC_Q7,       float(qG)),    # 1st A-base block (held R2)
                ("j9", ASC_Q8,       float(qH))]    # 2nd A-base block (NEW this round)
    for nm, ascc, wt in Afactors:
        rho_m, rhop_m, rlo, rhi, fpp = vu.rho_full(
            ascc, m, r, Wm, DWm, DDWm, DDDWm, Wc, DWc, DDWc, DDDWc)
        # Upper sums: weight (>=0) and accumulate with rounding toward +inf.
        A_hi = na(A_hi + na(wt * na(0.5 * vv.log_up(np.maximum(rhi, 1e-300)),
                                    PINF), PINF), PINF)
        # Lower sum: weight and accumulate toward -inf (safe-low).
        A_lo = na(A_lo + np.where(
            rlo > 0, na(wt * na(0.5 * vv.log_down(np.maximum(rlo, 1e-300)),
                                NINF), NINF), -1e300), NINF)
        A_mid_up = na(A_mid_up + na(wt * na(
            0.5 * vv.log_up(np.maximum(rho_m[1], 1e-300)), PINF), PINF), PINF)
        A_curv = na(A_curv + na(wt * fpp, PINF), PINF)
        A_slope = na(A_slope + na(wt * slope_abs_up(rho_m, rhop_m), PINF), PINF)

    # ---- B branch: Q1 + Q2 (fixed) + qB*Q3 + qC*Q4 + qE*Q5 + qF*Q6 (UNCHANGED) ----
    B_hi = np.zeros_like(a)
    B_lo = np.zeros_like(a)
    B_mid_up = np.zeros_like(a)
    B_curv = np.zeros_like(a)
    B_slope = np.zeros_like(a)
    Bfactors = [("Q1", vu.ASC["Q1"], 1.0),
                ("Q2", vu.ASC["Q2"], 1.0),
                ("Q3", ASC_Q3,       float(qB)),
                ("Q4", ASC_Q4,       float(qC)),
                ("Q5", ASC_Q5,       float(qE)),
                ("Q6", ASC_Q6,       float(qF))]
    for nm, ascc, wt in Bfactors:
        rho_m, rhop_m, rlo, rhi, fpp = vu.rho_full(
            ascc, m, r, Wm, DWm, DDWm, DDDWm, Wc, DWc, DDWc, DDDWc)
        B_hi = na(B_hi + na(wt * na(0.5 * vv.log_up(np.maximum(rhi, 1e-300)),
                                    PINF), PINF), PINF)
        B_lo = na(B_lo + np.where(
            rlo > 0, na(wt * na(0.5 * vv.log_down(np.maximum(rlo, 1e-300)),
                                NINF), NINF), -1e300), NINF)
        B_mid_up = na(B_mid_up + na(wt * na(
            0.5 * vv.log_up(np.maximum(rho_m[1], 1e-300)), PINF), PINF), PINF)
        B_curv = na(B_curv + na(wt * fpp, PINF), PINF)
        B_slope = na(B_slope + na(wt * slope_abs_up(rho_m, rhop_m), PINF), PINF)
    return dict(A_hi=A_hi, A_lo=A_lo, A_mid_up=A_mid_up, A_curv=A_curv,
                A_slope=A_slope, B_hi=B_hi, B_lo=B_lo, B_mid_up=B_mid_up,
                B_curv=B_curv, B_slope=B_slope)


def cell_int_maxAB_q8A(a, b, q, qB, qC, qE, qF, qG, qH, rem_cap):
    d = cell_AB_q8A(a, b, q, qB, qC, qE, qF, qG, qH)
    r = na(0.5 * (b - a), PINF)
    width = na(b - a, PINF)
    h3 = na(na(width * width, PINF) * width, PINF)
    h3_24 = na(h3 / 24.0, PINF)
    r2 = na(r * r, PINF)
    r3 = na(r2 * r, PINF)

    A_hi = d["A_hi"]; A_lo = d["A_lo"]
    B_hi = d["B_hi"]; B_lo = d["B_lo"]

    flat = na(width * np.maximum(A_hi, B_hi), PINF)

    mid_up = np.maximum(d["A_mid_up"], d["B_mid_up"])
    slope_max = np.maximum(d["A_slope"], d["B_slope"])
    curv_max = np.maximum(d["A_curv"], d["B_curv"])
    dev_int = na(na(slope_max * r2, PINF)
                 + na(na(0.5 * curv_max, PINF) * na((2.0 / 3.0) * r3, PINF), PINF),
                 PINF)
    straddle_bound = na(na(width * mid_up, PINF) + dev_int, PINF)

    A_dom = A_lo > B_hi
    B_dom = B_lo > A_hi
    A_rem = na(h3_24 * d["A_curv"], PINF)
    B_rem = na(h3_24 * d["B_curv"], PINF)
    A_mid = na(width * d["A_mid_up"] + A_rem, PINF)
    B_mid = na(width * d["B_mid_up"] + B_rem, PINF)
    use_A = A_dom & (A_rem <= rem_cap) & np.isfinite(A_mid)
    use_B = B_dom & (B_rem <= rem_cap) & np.isfinite(B_mid)

    cell_int_hi = np.minimum(flat, straddle_bound)
    cell_int_hi = np.where(use_A, np.minimum(cell_int_hi, A_mid), cell_int_hi)
    cell_int_hi = np.where(use_B, np.minimum(cell_int_hi, B_mid), cell_int_hi)
    cell_int_hi = na(cell_int_hi, PINF)

    refine = ~(use_A | use_B) & (dev_int > rem_cap) & np.isfinite(dev_int)
    refine = refine | ~np.isfinite(cell_int_hi)
    return cell_int_hi, refine


def certify_maxAB_q8A(q, qB, qC, qE, qF, qG, qH, label, target, M0=200000,
                      max_refine=14, rem_cap=1e-10, verbose=True):
    # TWO_PI and D are both DIVISORS of an upper-bounded numerator, so to keep the
    # quotient an over-estimate they must be rounded DOWN (toward -inf): a smaller
    # divisor yields a larger quotient, the safe direction for an upper bound.
    TWO_PI = na(2.0 * math.pi, NINF)
    edges = np.linspace(0.0, 2.0 * math.pi, M0 + 1)
    a = edges[:-1].copy()
    b = edges[1:].copy()
    total_resolved = 0.0
    t0 = time.time()
    rounds = 0
    nbad = 0
    n_leaf = 0
    D = _Dval_lo(q, qB, qC, qE, qF, qG, qH)   # LOWER bound on D (denominator)
    while True:
        cell_hi, refine = cell_int_maxAB_q8A(a, b, q, qB, qC, qE, qF, qG, qH, rem_cap)
        keep = ~refine
        total_resolved = na(
            total_resolved + float(np.sum(np.where(keep, cell_hi, 0.0))), PINF)
        n_leaf += int(np.sum(keep))
        nbad = int(np.sum(refine))
        frontier_flat = float(np.sum(np.where(refine, cell_hi, 0.0)))
        cur_total = na(total_resolved + frontier_flat, PINF)
        cur_logh = na(na(cur_total / TWO_PI, PINF) / D, PINF)
        if verbose:
            print(f"  [{label}] round {rounds}: frontier={a.shape[0]:>9}  "
                  f"refine_next={nbad:>6}  logh_hi<={cur_logh:.10f}  "
                  f"{time.time()-t0:.0f}s", flush=True)
        if nbad == 0 or rounds >= max_refine:
            break
        ab, bb = a[refine], b[refine]
        mid = 0.5 * (ab + bb)
        a = np.concatenate([ab, mid])
        b = np.concatenate([mid, bb])
        rounds += 1
    elapsed = time.time() - t0
    total_hi = cur_total
    integral_s = na(total_hi / TWO_PI, PINF)
    logh_hi = na(integral_s / D, PINF)
    if verbose:
        print(f"  [{label}] leaves={n_leaf}  unresolved frontier={nbad}  "
              f"rounds={rounds}  {elapsed:.1f}s")
        print(f"  [{label}] int_0^2pi G dt  <=  {total_hi:.10f}")
        print(f"  [{label}] int_0^1 G(chi) ds <= {integral_s:.10f}  D = {D}")
        print(f"  [{label}] CERTIFIED  log h <= {logh_hi:.10f}")
        print(f"  [{label}] target            = {target:.10f}")
        print(f"  [{label}] BEATS target (strict <): "
              f"{logh_hi < target}   (margin {target - logh_hi:.3e})")
    return logh_hi, nbad, elapsed, n_leaf, total_hi, integral_s, D


# ---------------------------------------------------------------------------
def float_value_q8A(q, qB, qC, qE, qF, qG, qH, N=8_000_000):
    s = (np.arange(N) + 0.5) / N
    z = np.exp(2j * np.pi * s)
    chi = z * (1 - z)

    def pv(c, x):
        r = np.zeros_like(x)
        for cc in c:
            r = r * x + cc
        return r
    A = (sum(q[i] * np.log(np.abs(pv(vu.BASE[i], chi))) for i in range(5))
         + qG * np.log(np.abs(pv(Q7, chi)))
         + qH * np.log(np.abs(pv(Q8, chi))))
    B = (np.log(np.abs(pv(vu.Q1, chi))) + np.log(np.abs(pv(vu.Q2, chi)))
         + qB * np.log(np.abs(pv(Q3, chi)))
         + qC * np.log(np.abs(pv(Q4, chi)))
         + qE * np.log(np.abs(pv(Q5, chi)))
         + qF * np.log(np.abs(pv(Q6, chi))))
    G = np.maximum(A, B)
    D = _Dval(q, qB, qC, qE, qF, qG, qH)
    return np.mean(G) / D


def admissibility_check_q8A(active_only=True):
    """Admissibility of the A-branch base extension {P1,P2,P4,P6,P8,j3,j9} with
    perturber side {Q1,Q2,Q5,Q6} (the CERTIFIED Angle, qB=qC=0).  Doche condition (4)
    is non-degeneracy of the integer-polynomial dictionary: BOTH new base blocks j3,j9
    must be deg>0, squarefree, mutually coprime, and coprime to every other active
    factor so the product ratio prod P^n / prod Q^n is never +-1."""
    import sympy as sp
    X = sp.symbols('X')

    def sym(c):
        n = len(c) - 1
        return sum(int(v) * X**(n - i) for i, v in enumerate(c))
    Q1s, Q2s = sym(vu.Q1), sym(vu.Q2)
    Q5s, Q6s = sym(Q5), sym(Q6)
    j3s, j9s = sym(Q7), sym(Q8)

    print(f"  [A-branch base blocks j3 (deg {DEG_Q7}) and j9 (deg {DEG_Q8})]")
    print(f"  deg j3={DEG_Q7}(>0:{DEG_Q7>0})  deg j9={DEG_Q8}(>0:{DEG_Q8>0})")
    print(f"  j9 descending coeffs = {Q8}  (flammang_table1 j=9)")
    print(f"  j9(0)={j9s.subs(X,0)} j9(1)={j9s.subs(X,1)} "
          f"(NOT required =1 for a BASE block)")
    sq3 = (sp.gcd(j3s, sp.diff(j3s, X)) == 1)
    sq9 = (sp.gcd(j9s, sp.diff(j9s, X)) == 1)
    irr9 = sp.Poly(j9s, X).is_irreducible
    print(f"  j3 squarefree: {sq3}   j9 squarefree: {sq9}   j9 irreducible: {irr9}")

    # LOAD-BEARING inter-block coprimality j3 vs j9
    g39 = sp.gcd(j3s, j9s) == 1
    distinct = sp.expand(j3s - j9s) != 0
    print(f"  *** inter-A-block *** gcd(j3,j9)=1: {g39}   j3 != j9: {distinct}")

    # base-side coprimality of j9 to the existing base polys P_i AND to j3
    base_ok = True
    for nm, Pc in [("P1", vu.P1), ("P2", vu.P2), ("P4", vu.P4),
                   ("P6", vu.P6), ("P8", vu.P8)]:
        g = sp.gcd(sym(Pc), j9s) == 1
        base_ok = base_ok and g
        print(f"  gcd(j9,{nm})=1 (base-side distinct): {g}")

    # cross-side coprimality of j9 to the kept perturbers: LOAD-BEARING for (4)
    cross_ok = True
    for nm, Qs in [("Q1", Q1s), ("Q2", Q2s), ("Q5", Q5s), ("Q6", Q6s)]:
        g = sp.gcd(j9s, Qs) == 1
        cross_ok = cross_ok and g
        print(f"  *** condition-(4) cross-coprime *** gcd(j9,{nm})=1: {g}")

    # also re-confirm j3 coprime to perturbers (held from R2)
    j3_cross = True
    for nm, Qs in [("Q1", Q1s), ("Q2", Q2s), ("Q5", Q5s), ("Q6", Q6s)]:
        g = sp.gcd(j3s, Qs) == 1
        j3_cross = j3_cross and g
    print(f"  (re-confirm) j3 coprime to all perturbers: {j3_cross}")

    certified_ok = ((DEG_Q7 > 0) and (DEG_Q8 > 0) and sq3 and sq9 and g39
                    and distinct and base_ok and cross_ok and j3_cross)
    print(f"  CERTIFIED-FAMILY admissibility (base {{P1,P2,P4,P6,P8,j3,j9}} vs "
          f"perturbers {{Q1,Q2,Q5,Q6}}, Doche condition (4)): {certified_ok}")
    return certified_ok


def selftest_q8A(q, qB, qC, qE, qF, qG, qH, ntest=200, seed=11):
    """Soundness on the CHANGED integrand: A now has qG*log|j3| + qH*log|j9|."""
    import mpmath as mp
    import random
    mp.mp.prec = 160
    ASCmp = {nm: [int(c) for c in vu.ASC[nm]] for nm in vu.ASC}
    ASCmp_Q3 = [int(c) for c in ASC_Q3]
    ASCmp_Q4 = [int(c) for c in ASC_Q4]
    ASCmp_Q5 = [int(c) for c in ASC_Q5]
    ASCmp_Q6 = [int(c) for c in ASC_Q6]
    ASCmp_Q7 = [int(c) for c in ASC_Q7]
    ASCmp_Q8 = [int(c) for c in ASC_Q8]

    def G_exact(t):
        w = mp.e**(1j * mp.mpf(t)) - mp.e**(2j * mp.mpf(t))

        def lp(asc):
            v = mp.mpc(0)
            for c in reversed(asc):
                v = v * w + c
            return mp.log(abs(v))
        A = (sum(mp.mpf(q[i]) * lp(ASCmp[nm])
                 for i, nm in enumerate(["P1", "P2", "P4", "P6", "P8"]))
             + mp.mpf(qG) * lp(ASCmp_Q7)
             + mp.mpf(qH) * lp(ASCmp_Q8))
        B = (lp(ASCmp["Q1"]) + lp(ASCmp["Q2"])
             + mp.mpf(qB) * lp(ASCmp_Q3) + mp.mpf(qC) * lp(ASCmp_Q4)
             + mp.mpf(qE) * lp(ASCmp_Q5) + mp.mpf(qF) * lp(ASCmp_Q6))
        return float(max(A, B))

    random.seed(seed)
    As, Bs = [], []
    for _ in range(ntest):
        c = random.uniform(0.001, 2 * math.pi - 0.001)
        wdt = 10 ** random.uniform(-6, -3.5)
        As.append(c)
        Bs.append(min(c + wdt, 2 * math.pi - 1e-9))
    A = np.array(As); B = np.array(Bs)
    worst = 0
    for cap, tag in [(0.0, "flat"), (1e-9, "midpt")]:
        cell_hi, refine = cell_int_maxAB_q8A(A, B, np.asarray(q, float),
                                             float(qB), float(qC), float(qE),
                                             float(qF), float(qG), float(qH), cap)
        viol = 0
        wmin = 1e300
        for i in range(len(A)):
            K = 60
            ts = [A[i] + (B[i] - A[i]) * k / K for k in range(K + 1)]
            gs = [G_exact(t) for t in ts]
            true_int = (B[i] - A[i]) / K * (
                0.5 * gs[0] + 0.5 * gs[-1] + sum(gs[1:-1]))
            disc = cell_hi[i] - true_int
            wmin = min(wmin, disc)
            if cell_hi[i] < true_int - 1e-12:
                viol += 1
                if viol <= 5:
                    print(f"  [{tag}] VIOLATION cell[{A[i]:.5f},{B[i]:.5f}] "
                          f"hi={cell_hi[i]:.10f} < true~{true_int:.10f}")
        print(f"  selftest_q8A[{tag}]: {viol}/{ntest} violations  (MUST be 0)  "
              f"worst (cell_hi - true_int) = {wmin:.3e} (>=0 is safe)")
        worst += viol
    return worst == 0


# CURRENT held reviewer-verified UPPER value (R2 this campaign), the value this round
# must STRICTLY beat.  NOT the superseded R11 value 0.2540419719.
HELD_CERT = 0.2538925359


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "anchor"
    # R2-held joint optimum (j3 active, j9 OFF) for the qH=0 anchor.
    R2_Q = [14.283862, 13.947194, 2.593425, 2.283539, 0.249084]
    R2_QE = 0.577911
    R2_QF = 0.565724
    R2_QG = 0.893516

    if mode == "anchor":
        print(f"[anchor] q8A (j9 second A-base) qH=0 must reproduce "
              f"bound_06_block_j3 BIT-IDENTICALLY at held R2 (q,qB=qC=0,qE,qF,qG).")
        v8 = float_value_q8A(R2_Q, 0.0, 0.0, R2_QE, R2_QF, R2_QG, 0.0, N=8_000_000)
        v7 = vq7A.float_value_q7A(R2_Q, 0.0, 0.0, R2_QE, R2_QF, R2_QG, N=8_000_000)
        print(f"  float_value_q8A(R2 q, qE, qF, qG, qH=0) = {v8:.12f}")
        print(f"  float_value_q7A(R2 q, qE, qF, qG)       = {v7:.12f}")
        print(f"  match (==): {v8 == v7}   |diff|<1e-12: {abs(v8 - v7) < 1e-12}")
        D8 = _Dval(np.array(R2_Q), 0.0, 0.0, R2_QE, R2_QF, R2_QG, 0.0)
        D7 = vq7A._Dval(np.array(R2_Q), 0.0, 0.0, R2_QE, R2_QF, R2_QG)
        print(f"  D_q8A(qH=0) = {D8}   D_q7A = {D7}   match: {D8 == D7}")
        aa = np.array([1.0, 2.0, 3.0, 4.0, 5.0]); bb = aa + 1e-4
        c8, r8 = cell_int_maxAB_q8A(aa, bb, np.array(R2_Q), 0.0, 0.0, R2_QE,
                                    R2_QF, R2_QG, 0.0, 1e-10)
        c7, r7 = vq7A.cell_int_maxAB_q7A(aa, bb, np.array(R2_Q), 0.0, 0.0,
                                         R2_QE, R2_QF, R2_QG, 1e-10)
        print(f"  cell enclosure BIT-IDENTICAL at qH=0: "
              f"{np.array_equal(c8, c7)}  refine-mask match: {np.array_equal(r8,r7)}")
    elif mode == "admiss":
        admissibility_check_q8A()
    elif mode == "selftest":
        q = [float(x) for x in sys.argv[2:7]]
        qB = float(sys.argv[7]); qC = float(sys.argv[8])
        qE = float(sys.argv[9]); qF = float(sys.argv[10])
        qG = float(sys.argv[11]); qH = float(sys.argv[12])
        print(f"[selftest_q8A] q={q} qB={qB} qC={qC} qE={qE} qF={qF} qG={qG} qH={qH}")
        ok = selftest_q8A(q, qB, qC, qE, qF, qG, qH)
        print(f"  selftest passed: {ok}")
        sys.exit(0 if ok else 1)
    elif mode == "tamper":
        q = np.array([float(x) for x in sys.argv[2:7]])
        qB = float(sys.argv[7]); qC = float(sys.argv[8])
        qE = float(sys.argv[9]); qF = float(sys.argv[10])
        qG = float(sys.argv[11]); qH = float(sys.argv[12])
        bogus = float(sys.argv[13])
        print(f"=== TAMPER q8A q={q.tolist()} qB={qB} qC={qC} qE={qE} qF={qF} "
              f"qG={qG} qH={qH} bogus={bogus} ===")
        logh_hi, nbad, _, _, _, _, _ = certify_maxAB_q8A(
            q, qB, qC, qE, qF, qG, qH, "tamper", bogus, M0=200000, max_refine=14,
            rem_cap=1e-10, verbose=True)
        beats = (logh_hi < bogus) and (nbad == 0)
        print(f"  BEATS bogus target: {beats}  (frontier resolved: {nbad==0})")
        print("  EXPECT BEATS=False (bogus target is below truth).")
        sys.exit(0)
    elif mode == "certify":
        q = np.array([float(x) for x in sys.argv[2:7]])
        qB = float(sys.argv[7]); qC = float(sys.argv[8])
        qE = float(sys.argv[9]); qF = float(sys.argv[10])
        qG = float(sys.argv[11]); qH = float(sys.argv[12])
        M0 = int(sys.argv[13]) if len(sys.argv) > 13 else 200000
        max_refine = int(sys.argv[14]) if len(sys.argv) > 14 else 14
        rem_cap = float(sys.argv[15]) if len(sys.argv) > 15 else 1e-10
        print(f"=== certify_q8A (j9 second A-branch) q={q.tolist()} qB={qB} "
              f"qC={qC} qE={qE} qF={qF} qG={qG} qH={qH} ===")
        print(f"    M0={M0} max_refine={max_refine} rem_cap={rem_cap}")
        print("\n[admissibility] base ext {P1,P2,P4,P6,P8,j3,j9} (Doche cond (4))")
        adm = admissibility_check_q8A()
        if not adm:
            print("    ABORT: admissibility failed.")
            sys.exit(1)
        print("\n[float] log h(q,qB,qC,qE,qF,qG,qH) ~ (CONJECTURE)")
        vq = float_value_q8A(q.tolist(), qB, qC, qE, qF, qG, qH, N=8_000_000)
        print(f"    float log h = {vq:.10f}  h = {math.exp(vq):.10f}")
        print("\n[selftest_q8A] soundness of per-cell bound on THIS integrand")
        ok = selftest_q8A(q.tolist(), qB, qC, qE, qF, qG, qH)
        print(f"    selftest passed: {ok}")
        if not ok:
            print("    ABORT: selftest failed, certificate not trustworthy.")
            sys.exit(1)
        print("\n[certify] rigorous max(A,B) quadrature enclosure")
        logh_hi, nbad, elapsed, n_leaf, tot, ints, D = certify_maxAB_q8A(
            q, qB, qC, qE, qF, qG, qH, "q8A", HELD_CERT, M0=M0, max_refine=max_refine,
            rem_cap=rem_cap, verbose=True)
        print("\n=== RESULT ===")
        print(f"  CERTIFIED  log h <= {logh_hi:.10f}")
        print(f"  unresolved frontier cells = {nbad}  (MUST be 0)")
        print(f"  leaves = {n_leaf}")
        print(f"  held R2 certified (target)= {HELD_CERT:.10f}")
        print(f"  int_0^2pi G dt <= {tot:.10f}")
        print(f"  int_0^1 G ds   <= {ints:.10f}   D = {D}")
        print(f"  hand arithmetic: {ints:.10f} / {D} = {ints/D:.12f}")
        beats = (logh_hi < HELD_CERT) and (nbad == 0)
        print(f"  beats held (strict, frontier=0): {beats}")
        if beats:
            print(f"  margin below held = {HELD_CERT - logh_hi:.4e}")
        sys.exit(0 if (nbad == 0) else 1)
