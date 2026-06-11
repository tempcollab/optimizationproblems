"""
R2 (this campaign) RIGOROUS upper-bound certificate for C_82, free-exponent family
with a NEW low-degree admissible block Q7 RE-INTRODUCED on the A-BRANCH (the prod-P^q
base side), on top of the held R11 family h = Q1*Q2*Q5^qE*Q6^qF (Q5=Flammang j13
deg12, Q6=Flammang j15 deg16).

This is Angle 2 of the R2 spec: the new block enters the BASE product
prod_m P_m^{q_m} (the A-branch), NOT the perturber product (the B-branch).  Doche's
Doc01a §4 framework lets the base set {P_m} be enlarged freely: pick base polys
P_1..P_k and perturbing polys Q_1..Q_{l+1}, with condition (4) (the product ratio
prod P^n / prod Q^n != +-1, equivalently the integer-polynomial dictionary is
coprime/non-degenerate), and

  D = 2b * max( sum_m q_m deg P_m , deg Q_{l+1} + sum_m q_{k+m} deg Q_m ).

A new base block Q7 (here a LOW-DEGREE Flammang Table-1 polynomial, default j3 deg 3,
in X=z(1-z)) with exponent qG>=0 therefore adds +qG*log|Q7| to the A-branch and
+qG*deg Q7 to the FIRST argument of the D-max (the sum-q-deg-P branch).  This is
distinct from verify_upper_q7.py (Angle 1) which adds Q7 to the B-branch and the
SECOND D-argument.

Family:
  A(t) = sum_i q_i*(1/2)log|P_i|^2  +  qG*(1/2)log|Q7|^2        (prod-P^q branch + new)
  B(t) = (1/2)log|Q1|^2 + (1/2)log|Q2|^2
          + qB*(1/2)log|Q3|^2 + qC*(1/2)log|Q4|^2
          + qE*(1/2)log|Q5|^2 + qF*(1/2)log|Q6|^2               (Q-branch, unchanged)
  G(t) = max(A(t), B(t))
  log h = (1/(2 pi D)) int_0^{2pi} G dt,
  D = max( sum_i q_i deg P_i + qG*deg Q7 ,
           56 + qB*deg Q3 + qC*deg Q4 + qE*deg Q5 + qF*deg Q6 ).

ANCHOR identity:
  - At qG=0 this collapses EXACTLY to verify_upper_q6 at (q,qB,qC,qE,qF):
    A loses the Q7 term, D's first argument loses +qG*deg Q7 -> BIT-IDENTICAL.

Per-cell enclosure machinery reused VERBATIM from verify_upper.py.  Q7 is added to the
A-branch with weight qG, mechanically identical to any other P factor (same rho_full,
weighted, outward-rounded).  Because the integrand changed, the mpmath soundness
selftest (selftest_q7A) is re-run on THIS integrand (A now has qG*log|Q7|).

Validity: Doc01a Lemmas 2,3,4,5 give log h(q,qB,qC,qE,qF,qG) as a true limit point of
the ZZ spectrum for any admissible exponents >= 0 (no optimality needed), hence
C_82 <= log h.  Admissibility is verified by admissibility_check_q7A() -- for the
certified Angle (qB=qC=0) the active dictionary is the integer-polynomial product
{P1,P2,P4,P6,P8,Q7} on the base side and {Q1,Q2,Q5,Q6} on the perturber side, all
pairwise coprime, with the new base block Q7 deg>0, squarefree, and the LOAD-BEARING
coprimality gcd(Q7, each P_i)=1 (base side distinct) and gcd(Q7, each kept
perturber Q1,Q2,Q5,Q6)=1 (cross-side coprime => condition (4) non-degenerate).
A Doche BASE poly need NOT satisfy P(0)=P(1)=1 (the P_i are base, not perturbers; e.g.
P1=X vanishes at 0); the load-bearing clause for a base block is condition (4)
coprimality/non-triviality, checked here.  (Q7=j3 happens to also satisfy
Q7(0)=Q7(1)=1, which we report but do not require for a base block.)

Q7 block selectable via env var Q7_CAND in {j3,j6,j7,j9} (default j3).

Usage:
  Q7_CAND=j3 python3 verify_upper_q7A.py anchor                  # qG=0 -> q6 BIT-IDENTICAL
  Q7_CAND=j3 python3 verify_upper_q7A.py admiss
  Q7_CAND=j3 python3 verify_upper_q7A.py selftest q1..q5 qB qC qE qF qG
  Q7_CAND=j3 python3 verify_upper_q7A.py certify q1..q5 qB qC qE qF qG [M0] [max_refine] [rem_cap]
  Q7_CAND=j3 python3 verify_upper_q7A.py tamper q1..q5 qB qC qE qF qG bogus_target
"""

import os
import sys
import time
import math
import numpy as np

import verify_vec as vv
import verify_upper as vu
import verify_upper_q4 as vq4
import verify_upper_q5 as vq5
import verify_upper_q6 as vq6   # for qG=0 anchor cross-check (q7A == q6 at qG=0)

NINF = -np.inf
PINF = np.inf
na = np.nextafter

Q3 = vq6.Q3; DEG_Q3 = vq6.DEG_Q3; ASC_Q3 = vq6.ASC_Q3
Q4 = vq6.Q4; DEG_Q4 = vq6.DEG_Q4; ASC_Q4 = vq6.ASC_Q4
Q5 = vq6.Q5; DEG_Q5 = vq6.DEG_Q5; ASC_Q5 = vq6.ASC_Q5
Q6 = vq6.Q6; DEG_Q6 = vq6.DEG_Q6; ASC_Q6 = vq6.ASC_Q6

# Q7 = a LOW-DEGREE Flammang Table-1 block (DESCENDING in X), re-introduced on the
# BASE (A) side.  Verbatim from flammang_table1.py _TABLE_DESCENDING.
_Q7_CANDS = {
    "j3": [1, 1, -2, 1],                                   # deg 3
    "j6": [2, -5, 6, 2, -11, 11, -5, 1],                   # deg 7
    "j7": [1, -2, 4, -7, 13, -16, 12, -5, 1],              # deg 8
    "j9": [1, -1, 0, -3, 15, -22, 16, -6, 1],              # deg 8
}
Q7_CAND = os.environ.get("Q7_CAND", "j3")
if Q7_CAND not in _Q7_CANDS:
    raise SystemExit(f"unknown Q7_CAND={Q7_CAND!r}; choose from {sorted(_Q7_CANDS)}")
Q7 = _Q7_CANDS[Q7_CAND]
DEG_Q7 = len(Q7) - 1
ASC_Q7 = vu.asc(Q7)

DEGP = vu.DEGP                        # [1,1,4,8,8]
DEGQ12 = vu.DEGQ                      # 56


def _Dval(q, qB, qC, qE, qF, qG):
    # A-branch: Q7 adds to the FIRST (sum q deg P) argument.
    return max(float(np.dot(q, DEGP) + qG * DEG_Q7),
               float(DEGQ12 + qB * DEG_Q3 + qC * DEG_Q4
                     + qE * DEG_Q5 + qF * DEG_Q6))


# ---------------------------------------------------------------------------
def cell_AB_q7A(a, b, q, qB, qC, qE, qF, qG):
    m = 0.5 * (a + b)
    r = 0.5 * (b - a)
    Wc, DWc, DDWc, DDDWc = vu.w_full_cell(a, b)
    Wm, DWm, DDWm, DDDWm = vu.w_full_point(m)

    def slope_abs_up(rho_m, rhop_m):
        num = 0.5 * np.maximum(np.abs(rhop_m[0]), np.abs(rhop_m[1]))
        den = rho_m[0]
        return np.where(den > 0, na(num / np.where(den > 0, den, 1.0), PINF), PINF)

    # ---- A branch: sum_i q_i (1/2)log|P_i|^2  +  qG*(1/2)log|Q7|^2 ----
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
                ("Q7", ASC_Q7,       float(qG))]    # NEW base block on the A-side
    for nm, ascc, wt in Afactors:
        rho_m, rhop_m, rlo, rhi, fpp = vu.rho_full(
            ascc, m, r, Wm, DWm, DDWm, DDDWm, Wc, DWc, DDWc, DDDWc)
        A_hi = A_hi + wt * na(0.5 * vv.log_up(np.maximum(rhi, 1e-300)), PINF)
        A_lo = A_lo + wt * np.where(
            rlo > 0, na(0.5 * vv.log_down(np.maximum(rlo, 1e-300)), NINF), -1e300)
        A_mid_up = A_mid_up + wt * na(
            0.5 * vv.log_up(np.maximum(rho_m[1], 1e-300)), PINF)
        A_curv = na(A_curv + wt * fpp, PINF)
        A_slope = na(A_slope + wt * slope_abs_up(rho_m, rhop_m), PINF)

    # ---- B branch: Q1 + Q2 (fixed) + qB*Q3 + qC*Q4 + qE*Q5 + qF*Q6 (unchanged) ----
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
        B_hi = B_hi + wt * na(0.5 * vv.log_up(np.maximum(rhi, 1e-300)), PINF)
        B_lo = B_lo + wt * np.where(
            rlo > 0, na(0.5 * vv.log_down(np.maximum(rlo, 1e-300)), NINF), -1e300)
        B_mid_up = B_mid_up + wt * na(
            0.5 * vv.log_up(np.maximum(rho_m[1], 1e-300)), PINF)
        B_curv = na(B_curv + wt * fpp, PINF)
        B_slope = na(B_slope + wt * slope_abs_up(rho_m, rhop_m), PINF)
    return dict(A_hi=A_hi, A_lo=A_lo, A_mid_up=A_mid_up, A_curv=A_curv,
                A_slope=A_slope, B_hi=B_hi, B_lo=B_lo, B_mid_up=B_mid_up,
                B_curv=B_curv, B_slope=B_slope)


def cell_int_maxAB_q7A(a, b, q, qB, qC, qE, qF, qG, rem_cap):
    d = cell_AB_q7A(a, b, q, qB, qC, qE, qF, qG)
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


def certify_maxAB_q7A(q, qB, qC, qE, qF, qG, label, target, M0=200000,
                      max_refine=14, rem_cap=1e-10, verbose=True):
    TWO_PI = na(2.0 * math.pi, PINF)
    edges = np.linspace(0.0, 2.0 * math.pi, M0 + 1)
    a = edges[:-1].copy()
    b = edges[1:].copy()
    total_resolved = 0.0
    t0 = time.time()
    rounds = 0
    nbad = 0
    n_leaf = 0
    D = _Dval(q, qB, qC, qE, qF, qG)
    while True:
        cell_hi, refine = cell_int_maxAB_q7A(a, b, q, qB, qC, qE, qF, qG, rem_cap)
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
def float_value_q7A(q, qB, qC, qE, qF, qG, N=8_000_000):
    s = (np.arange(N) + 0.5) / N
    z = np.exp(2j * np.pi * s)
    chi = z * (1 - z)

    def pv(c, x):
        r = np.zeros_like(x)
        for cc in c:
            r = r * x + cc
        return r
    A = (sum(q[i] * np.log(np.abs(pv(vu.BASE[i], chi))) for i in range(5))
         + qG * np.log(np.abs(pv(Q7, chi))))
    B = (np.log(np.abs(pv(vu.Q1, chi))) + np.log(np.abs(pv(vu.Q2, chi)))
         + qB * np.log(np.abs(pv(Q3, chi)))
         + qC * np.log(np.abs(pv(Q4, chi)))
         + qE * np.log(np.abs(pv(Q5, chi)))
         + qF * np.log(np.abs(pv(Q6, chi))))
    G = np.maximum(A, B)
    D = _Dval(q, qB, qC, qE, qF, qG)
    return np.mean(G) / D


def admissibility_check_q7A(active_only=True):
    """Admissibility of the A-branch base extension {P1,P2,P4,P6,P8,Q7} with perturber
    side {Q1,Q2,Q5,Q6} (the CERTIFIED Angle, qB=qC=0).  Doche condition (4) is
    non-degeneracy of the integer-polynomial dictionary: the new base block Q7 must be
    deg>0, squarefree, and coprime to every other factor on BOTH sides so the product
    ratio prod P^n / prod Q^n is never +-1 (a base block need NOT be 1 at 0,1)."""
    import sympy as sp
    X = sp.symbols('X')

    def sym(c):
        n = len(c) - 1
        return sum(int(v) * X**(n - i) for i, v in enumerate(c))
    Q1s, Q2s = sym(vu.Q1), sym(vu.Q2)
    Q3s, Q4s, Q5s, Q6s, Q7s = sym(Q3), sym(Q4), sym(Q5), sym(Q6), sym(Q7)

    print(f"  [A-branch base block Q7 = Flammang {Q7_CAND}]")
    print(f"  deg_X Q7 = {DEG_Q7} (>0: {DEG_Q7 > 0})")
    print(f"  Q7(0) = {Q7s.subs(X, 0)}  Q7(1) = {Q7s.subs(X, 1)}  "
          f"(NOT required =1 for a BASE block)")
    sq7 = (sp.gcd(Q7s, sp.diff(Q7s, X)) == 1)
    print(f"  Q7 squarefree: {sq7}")

    # base-side coprimality to the existing base polys P_i (distinct base factors)
    base_ok = True
    for nm, Pc in [("P1", vu.P1), ("P2", vu.P2), ("P4", vu.P4),
                   ("P6", vu.P6), ("P8", vu.P8)]:
        g = sp.gcd(sym(Pc), Q7s) == 1
        base_ok = base_ok and g
        print(f"  gcd(Q7,{nm})=1 (base-side distinct): {g}")

    # cross-side coprimality to the kept perturbers Q1,Q2,Q5,Q6: LOAD-BEARING for (4)
    cross_ok = True
    for nm, Qs in [("Q1", Q1s), ("Q2", Q2s), ("Q5", Q5s), ("Q6", Q6s)]:
        g = sp.gcd(Q7s, Qs) == 1
        cross_ok = cross_ok and g
        print(f"  *** condition-(4) cross-coprime *** gcd(Q7,{nm})=1: {g}")

    # the active integer-polynomial dictionary (both sides) is squarefree & coprime
    # => prod P^n / prod Q^n != +-1 for all nonzero exponent tuples (non-degenerate).
    g73 = sp.gcd(Q7s, Q3s) == 1
    g74 = sp.gcd(Q7s, Q4s) == 1
    print(f"  *** ell-extended cross-coprime *** gcd(Q7,Qa)=1: {g73}   "
          f"gcd(Q7,Qb)=1: {g74}")

    certified_ok = ((DEG_Q7 > 0) and sq7 and base_ok and cross_ok)
    full_ok = certified_ok and g73 and g74
    print(f"  CERTIFIED-FAMILY admissibility (base {{P1,P2,P4,P6,P8,Q7}} vs perturbers "
          f"{{Q1,Q2,Q5,Q6}}, Doche condition (4)): {certified_ok}")
    print(f"  FULL admissibility (incl. Qa,Qb): {full_ok}")
    return certified_ok if active_only else full_ok


def selftest_q7A(q, qB, qC, qE, qF, qG, ntest=200, seed=11):
    """Soundness on the CHANGED integrand: A now has the extra qG*log|Q7|."""
    import mpmath as mp
    import random
    mp.mp.prec = 160
    ASCmp = {nm: [int(c) for c in vu.ASC[nm]] for nm in vu.ASC}
    ASCmp_Q3 = [int(c) for c in ASC_Q3]
    ASCmp_Q4 = [int(c) for c in ASC_Q4]
    ASCmp_Q5 = [int(c) for c in ASC_Q5]
    ASCmp_Q6 = [int(c) for c in ASC_Q6]
    ASCmp_Q7 = [int(c) for c in ASC_Q7]

    def G_exact(t):
        w = mp.e**(1j * mp.mpf(t)) - mp.e**(2j * mp.mpf(t))

        def lp(asc):
            v = mp.mpc(0)
            for c in reversed(asc):
                v = v * w + c
            return mp.log(abs(v))
        A = (sum(mp.mpf(q[i]) * lp(ASCmp[nm])
                 for i, nm in enumerate(["P1", "P2", "P4", "P6", "P8"]))
             + mp.mpf(qG) * lp(ASCmp_Q7))
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
        cell_hi, refine = cell_int_maxAB_q7A(A, B, np.asarray(q, float),
                                             float(qB), float(qC), float(qE),
                                             float(qF), float(qG), cap)
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
        print(f"  selftest_q7A[{tag}]: {viol}/{ntest} violations  (MUST be 0)  "
              f"worst (cell_hi - true_int) = {wmin:.3e} (>=0 is safe)")
        worst += viol
    return worst == 0


# R11-held reviewer-verified UPPER value, the value this round must STRICTLY beat.
HELD_CERT = 0.2540419719


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "anchor"
    R11_Q = [13.937341, 12.515102, 2.541409, 2.068537, 0.753965]
    R11_QE = 0.891271
    R11_QF = 0.246614

    if mode == "anchor":
        print(f"[anchor] Q7={Q7_CAND} (A-branch)  qG=0 must reproduce "
              f"verify_upper_q6 BIT-IDENTICALLY at held R11 (q,qB=qC=0,qE,qF).")
        v7 = float_value_q7A(R11_Q, 0.0, 0.0, R11_QE, R11_QF, 0.0, N=8_000_000)
        v6 = vq6.float_value_q6(R11_Q, 0.0, 0.0, R11_QE, R11_QF, N=8_000_000)
        print(f"  float_value_q7A(R11 q, qB=qC=0, qE, qF, qG=0) = {v7:.12f}")
        print(f"  float_value_q6(R11 q, qB=qC=0, qE, qF)        = {v6:.12f}")
        print(f"  match (==): {v7 == v6}   |diff|<1e-12: {abs(v7 - v6) < 1e-12}")
        D7 = _Dval(np.array(R11_Q), 0.0, 0.0, R11_QE, R11_QF, 0.0)
        D6 = vq6._Dval(np.array(R11_Q), 0.0, 0.0, R11_QE, R11_QF)
        print(f"  D_q7A(qG=0) = {D7}   D_q6 = {D6}   match: {D7 == D6}")
        aa = np.array([1.0, 2.0, 3.0]); bb = aa + 1e-4
        c7, _ = cell_int_maxAB_q7A(aa, bb, np.array(R11_Q), 0.0, 0.0, R11_QE,
                                   R11_QF, 0.0, 1e-10)
        c6, _ = vq6.cell_int_maxAB_q6(aa, bb, np.array(R11_Q), 0.0, 0.0,
                                      R11_QE, R11_QF, 1e-10)
        print(f"  cell enclosure BIT-IDENTICAL at qG=0: "
              f"{np.array_equal(c7, c6)}")
    elif mode == "admiss":
        admissibility_check_q7A()
    elif mode == "selftest":
        q = [float(x) for x in sys.argv[2:7]]
        qB = float(sys.argv[7]); qC = float(sys.argv[8])
        qE = float(sys.argv[9]); qF = float(sys.argv[10]); qG = float(sys.argv[11])
        print(f"[selftest_q7A] Q7={Q7_CAND} q={q} qB={qB} qC={qC} qE={qE} "
              f"qF={qF} qG={qG}")
        ok = selftest_q7A(q, qB, qC, qE, qF, qG)
        print(f"  selftest passed: {ok}")
        sys.exit(0 if ok else 1)
    elif mode == "tamper":
        q = np.array([float(x) for x in sys.argv[2:7]])
        qB = float(sys.argv[7]); qC = float(sys.argv[8])
        qE = float(sys.argv[9]); qF = float(sys.argv[10]); qG = float(sys.argv[11])
        bogus = float(sys.argv[12])
        print(f"=== TAMPER Q7={Q7_CAND}(A) q={q.tolist()} qB={qB} qC={qC} qE={qE} "
              f"qF={qF} qG={qG} bogus={bogus} ===")
        logh_hi, nbad, _, _, _, _, _ = certify_maxAB_q7A(
            q, qB, qC, qE, qF, qG, "tamper", bogus, M0=200000, max_refine=14,
            rem_cap=1e-10, verbose=True)
        beats = (logh_hi < bogus) and (nbad == 0)
        print(f"  BEATS bogus target: {beats}  (frontier resolved: {nbad==0})")
        print("  EXPECT BEATS=False (bogus target is below truth).")
        sys.exit(0)
    elif mode == "certify":
        q = np.array([float(x) for x in sys.argv[2:7]])
        qB = float(sys.argv[7]); qC = float(sys.argv[8])
        qE = float(sys.argv[9]); qF = float(sys.argv[10]); qG = float(sys.argv[11])
        M0 = int(sys.argv[12]) if len(sys.argv) > 12 else 200000
        max_refine = int(sys.argv[13]) if len(sys.argv) > 13 else 14
        rem_cap = float(sys.argv[14]) if len(sys.argv) > 14 else 1e-10
        print(f"=== certify_q7A Q7={Q7_CAND}(A-branch) q={q.tolist()} qB={qB} "
              f"qC={qC} qE={qE} qF={qF} qG={qG} ===")
        print(f"    M0={M0} max_refine={max_refine} rem_cap={rem_cap}")
        print("\n[admissibility] base extension {P1,P2,P4,P6,P8,Q7} (Doche cond (4))")
        adm = admissibility_check_q7A()
        if not adm:
            print("    ABORT: admissibility failed.")
            sys.exit(1)
        print("\n[float] log h(q,qB,qC,qE,qF,qG) ~ (CONJECTURE)")
        vq = float_value_q7A(q.tolist(), qB, qC, qE, qF, qG, N=8_000_000)
        print(f"    float log h = {vq:.10f}  h = {math.exp(vq):.10f}")
        print("\n[selftest_q7A] soundness of per-cell bound on THIS integrand")
        ok = selftest_q7A(q.tolist(), qB, qC, qE, qF, qG)
        print(f"    selftest passed: {ok}")
        if not ok:
            print("    ABORT: selftest failed, certificate not trustworthy.")
            sys.exit(1)
        print("\n[certify] rigorous max(A,B) quadrature enclosure")
        logh_hi, nbad, elapsed, n_leaf, tot, ints, D = certify_maxAB_q7A(
            q, qB, qC, qE, qF, qG, "q7A", HELD_CERT, M0=M0, max_refine=max_refine,
            rem_cap=rem_cap, verbose=True)
        print("\n=== RESULT ===")
        print(f"  CERTIFIED  log h <= {logh_hi:.10f}")
        print(f"  unresolved frontier cells = {nbad}  (MUST be 0)")
        print(f"  leaves = {n_leaf}")
        print(f"  held R11 certified        = {HELD_CERT:.10f}")
        print(f"  int_0^2pi G dt <= {tot:.10f}")
        print(f"  int_0^1 G ds   <= {ints:.10f}   D = {D}")
        print(f"  hand arithmetic: {ints:.10f} / {D} = {ints/D:.12f}")
        beats = (logh_hi < HELD_CERT) and (nbad == 0)
        print(f"  beats held (strict, frontier=0): {beats}")
        if beats:
            print(f"  margin below held = {HELD_CERT - logh_hi:.4e}")
        sys.exit(0 if (nbad == 0) else 1)
