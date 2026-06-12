"""
R11 RIGOROUS upper-bound certificate for C_82, free-exponent family with TWO free
perturbing blocks Q5 (Flammang Table 1 entry j=13, deg 12) and a NEW second free
block Q6 (Flammang Table 1 entry j=15, deg 16).

This EXTENDS the R10-approved bound_04_block_j13.py (free blocks Q3=Qa, Q4=Qb deg 24,
Q5=j13 deg 12) by adding a FOURTH free-exponent perturbing block Q6 = Flammang
Table 1 entry j=15 (deg 16 in X = z(1-z)), exponent qF>=0.  Authored in the ell=4
shape so that qF=0 recovers EXACTLY bound_04_block_j13 (held R10 family h=Q1*Q2*Q5^qE),
qE=qF=0 recovers bound_03_block_Qb (held R9 ell=2 family), and qB=qC=qE=qF=0 recovers
the Doche base h=Q1*Q2, D=56.

Family (Doche general-l, multi-free-block perturber):
  Q1*Q2 stays the FIXED distinguished block Q_{l+1} (exponent 1);
  Q3=Qa free with exponent qB>=0; Q4=Qb free with exponent qC>=0;
  Q5=j13 (deg 12) free with exponent qE>=0; Q6=j15 (NEW, deg 16) free with qF>=0.

  A(t) = sum_i q_i * (1/2) log|P_i(w(t))|^2                       (prod-P^q branch)
  B(t) = (1/2)log|Q1|^2 + (1/2)log|Q2|^2
          + qB*(1/2)log|Q3|^2 + qC*(1/2)log|Q4|^2
          + qE*(1/2)log|Q5|^2 + qF*(1/2)log|Q6|^2                 (Q-branch)
  G(t) = max(A(t), B(t)) = log max(|prod P^q|, |Q1 Q2 Q3^qB Q4^qC Q5^qE Q6^qF|)  (Jensen)
  log h(q,qB,qC,qE,qF) = (1/(2 pi D)) int_0^{2pi} G dt,
  D = max( sum_i q_i deg_X P_i ,
           56 + qB*deg Q3 + qC*deg Q4 + qE*deg Q5 + qF*deg Q6 ).

This is the Doc01a §4 D-formula with a perturbing side of (here) up to four free
blocks (Q3,Q4,Q5,Q6) on top of the fixed distinguished block Q1*Q2.

ANCHOR identities:
  - At qF=0 this collapses EXACTLY to bound_04_block_j13 at the same (q,qB,qC,qE):
    B loses the Q6 term and D's perturbing branch loses the +qF*16 summand.
  - At qE=qF=0 it collapses to bound_03_block_Qb (held R9 ell=2 family).
  - At qB=qC=qE=qF=0 it collapses to bound_01_doche_base (h=Q1*Q2, D=56), the Doche base.

The per-cell enclosure machinery (rho_full -> midpoint value / slope / curvature /
cell sup-inf of (1/2)log|.|^2, all OUTWARD-rounded) is reused VERBATIM from
bound_01_doche_base.py via `import bound_01_doche_base as vu`.  The ONLY change vs q5 is that Q6 is
added to the B-branch with weight qF, exactly as Q3,Q4,Q5 are added -- the rigor
treatment of a Q6 factor in B is mechanically identical to a P factor in A (same
rho_full output, weighted, outward-rounded). Because the integrand changed, the mpmath
soundness selftest (selftest_q6) is re-run on THIS integrand (B now has qF*log|Q6|).

Validity: Doc01a Lemmas 2,3,4,5 give log h(q,qB,qC,qE,qF) as a true limit point of the
ZZ spectrum for any admissible (q, qB,qC,qE,qF >= 0) (no optimality needed), hence
C_82 <= log h. Admissibility of the active dictionary is verified by
admissibility_check_q6() -- for the certified Angle (qB=qC=0) the active dict is
W = Q1*Q2*Q5*Q6 (all factors non-constant & pairwise coprime, W(0)=W(1)=1, Q6
squarefree, gcd(Q6, each kept factor)=1 incl. the LOAD-BEARING inter-block
gcd(Q6,Q5)=1).

Usage:
  python3 bound_05_block_j15.py anchor                  # qF=0 -> q5; qE=qF=0 -> q4; base
  python3 bound_05_block_j15.py admiss
  python3 bound_05_block_j15.py selftest q1..q5 qB qC qE qF
  python3 bound_05_block_j15.py certify q1 q2 q3 q4 q5 qB qC qE qF [M0] [max_refine] [rem_cap]
  python3 bound_05_block_j15.py tamper q1..q5 qB qC qE qF bogus_target
"""

import sys
import time
import math
import numpy as np

import bound_00_flammang_baseline as vv
import bound_01_doche_base as vu
import bound_03_block_Qb as vq4   # for qE=qF=0 anchor chain
import bound_04_block_j13 as vq5   # for qF=0 anchor cross-check (q6 == q5 at qF=0)

NINF = -np.inf
PINF = np.inf
na = np.nextafter

# Q3 = Qa (Doc01a calibration perturber, deg 24), high->low in X.  (Same as q5/q4.)
Q3 = vq4.Q3
DEG_Q3 = vq4.DEG_Q3
ASC_Q3 = vq4.ASC_Q3

# Q4 = Qb (Doc01a calibration perturber, deg 24), high->low in X.  (Same as q5/q4.)
Q4 = vq4.Q4
DEG_Q4 = vq4.DEG_Q4
ASC_Q4 = vq4.ASC_Q4

# Q5 = Flammang Table 1 entry j=13 (deg 12 in X = z(1-z)), high->low.  (Same as q5.)
Q5 = vq5.Q5
DEG_Q5 = vq5.DEG_Q5
ASC_Q5 = vq5.ASC_Q5

# Q6 = Flammang Table 1 entry j=15 (deg 16 in X = z(1-z)), high->low (descending,
# harness convention, like Q3/Q4/Q5).
# Ascending in X: [1,-11,59,-199,464,-780,963,-878,592,-298,119,-47,26,-17,10,-4,1].
Q6 = [1, -4, 10, -17, 26, -47, 119, -298, 592, -878, 963, -780, 464, -199, 59, -11, 1]
DEG_Q6 = len(Q6) - 1                  # = 16
ASC_Q6 = vu.asc(Q6)

DEGP = vu.DEGP                        # [1,1,4,8,8]
DEGQ12 = vu.DEGQ                      # 56  (fixed distinguished block Q1*Q2)


def _Dval(q, qB, qC, qE, qF):
    return max(float(np.dot(q, DEGP)),
               float(DEGQ12 + qB * DEG_Q3 + qC * DEG_Q4
                     + qE * DEG_Q5 + qF * DEG_Q6))


# ---------------------------------------------------------------------------
# Per-cell A,B data.  A branch == bound_01_doche_base.cell_AB's A branch (P1..P8).
# B branch == Q1 + Q2 (fixed) + qB*Q3 + qC*Q4 + qE*Q5 + qF*Q6 (free), each factor's
# (1/2)log|.|^2 enclosed by vu.rho_full exactly as in vu.cell_AB.
# ---------------------------------------------------------------------------
def cell_AB_q6(a, b, q, qB, qC, qE, qF):
    m = 0.5 * (a + b)
    r = 0.5 * (b - a)
    Wc, DWc, DDWc, DDDWc = vu.w_full_cell(a, b)
    Wm, DWm, DDWm, DDDWm = vu.w_full_point(m)

    def slope_abs_up(rho_m, rhop_m):
        num = 0.5 * np.maximum(np.abs(rhop_m[0]), np.abs(rhop_m[1]))
        den = rho_m[0]
        return np.where(den > 0, na(num / np.where(den > 0, den, 1.0), PINF), PINF)

    # ---- A branch: sum_i q_i (1/2)log|P_i|^2 ----
    A_hi = np.zeros_like(a)
    A_lo = np.zeros_like(a)
    A_mid_up = np.zeros_like(a)
    A_curv = np.zeros_like(a)
    A_slope = np.zeros_like(a)
    for i, nm in enumerate(["P1", "P2", "P4", "P6", "P8"]):
        rho_m, rhop_m, rlo, rhi, fpp = vu.rho_full(
            vu.ASC[nm], m, r, Wm, DWm, DDWm, DDDWm, Wc, DWc, DDWc, DDDWc)
        qi = q[i]
        A_hi = A_hi + qi * na(0.5 * vv.log_up(np.maximum(rhi, 1e-300)), PINF)
        A_lo = A_lo + qi * np.where(
            rlo > 0, na(0.5 * vv.log_down(np.maximum(rlo, 1e-300)), NINF), -1e300)
        A_mid_up = A_mid_up + qi * na(
            0.5 * vv.log_up(np.maximum(rho_m[1], 1e-300)), PINF)
        A_curv = na(A_curv + qi * fpp, PINF)
        A_slope = na(A_slope + qi * slope_abs_up(rho_m, rhop_m), PINF)

    # ---- B branch: log|Q1|/2 + log|Q2|/2 + qB*log|Q3|/2 + qC*log|Q4|/2
    #               + qE*log|Q5|/2 + qF*log|Q6|/2 ----
    B_hi = np.zeros_like(a)
    B_lo = np.zeros_like(a)
    B_mid_up = np.zeros_like(a)
    B_curv = np.zeros_like(a)
    B_slope = np.zeros_like(a)
    # (factor name, ascending coeffs, weight)
    Bfactors = [("Q1", vu.ASC["Q1"], 1.0),
                ("Q2", vu.ASC["Q2"], 1.0),
                ("Q3", ASC_Q3,       float(qB)),
                ("Q4", ASC_Q4,       float(qC)),
                ("Q5", ASC_Q5,       float(qE)),
                ("Q6", ASC_Q6,       float(qF))]    # NEW second free block
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


def cell_int_maxAB_q6(a, b, q, qB, qC, qE, qF, rem_cap):
    """UPPER bound on int_cell max(A,B) dt + a `refine` mask.  Identical logic to
    bound_01_doche_base.cell_int_maxAB; only cell_AB_q6 differs (Q3,Q4,Q5,Q6 in B)."""
    d = cell_AB_q6(a, b, q, qB, qC, qE, qF)
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


def certify_maxAB_q6(q, qB, qC, qE, qF, label, target, M0=200000, max_refine=14,
                     rem_cap=1e-10, verbose=True):
    """Guaranteed UPPER bound on log h(q,qB,qC,qE,qF) via the un-split max(A,B)
    enclosure."""
    TWO_PI = na(2.0 * math.pi, PINF)
    edges = np.linspace(0.0, 2.0 * math.pi, M0 + 1)
    a = edges[:-1].copy()
    b = edges[1:].copy()
    total_resolved = 0.0
    t0 = time.time()
    rounds = 0
    nbad = 0
    n_leaf = 0
    D = _Dval(q, qB, qC, qE, qF)
    while True:
        cell_hi, refine = cell_int_maxAB_q6(a, b, q, qB, qC, qE, qF, rem_cap)
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
def float_value_q6(q, qB, qC, qE, qF, N=8_000_000):
    """Float midpoint Riemann sum of log h(q,qB,qC,qE,qF) (CONJECTURE / anchor)."""
    s = (np.arange(N) + 0.5) / N
    z = np.exp(2j * np.pi * s)
    chi = z * (1 - z)

    def pv(c, x):
        r = np.zeros_like(x)
        for cc in c:
            r = r * x + cc
        return r
    A = sum(q[i] * np.log(np.abs(pv(vu.BASE[i], chi))) for i in range(5))
    B = (np.log(np.abs(pv(vu.Q1, chi))) + np.log(np.abs(pv(vu.Q2, chi)))
         + qB * np.log(np.abs(pv(Q3, chi)))
         + qC * np.log(np.abs(pv(Q4, chi)))
         + qE * np.log(np.abs(pv(Q5, chi)))
         + qF * np.log(np.abs(pv(Q6, chi))))
    G = np.maximum(A, B)
    D = _Dval(q, qB, qC, qE, qF)
    return np.mean(G) / D


def admissibility_check_q6(active_only=True):
    """Admissibility of the active perturbing dictionary.

    For the CERTIFIED Angle (qB=qC=0) the active dictionary is W=Q1*Q2*Q5*Q6;
    Qa,Qb are dropped, so only the kept dictionary matters for validity. We verify:
      - Q6 Doche condition (4): deg Q6>0, Q6(0)=Q6(1)=1, Q6 squarefree;
      - Q6 coprime to every kept factor (P_i, Q1, Q2) AND the LOAD-BEARING
        inter-block gcd(Q6,Q5)=1 (the new block must be coprime to the held Q5);
      - the active dictionary W=Q1*Q2*Q5*Q6 (deg>0, W(0)=W(1)=1, all factors
        non-constant & pairwise coprime => condition (4) by unique factorization).
      - the full pairwise grid incl. gcd(Q6,Qa)=gcd(Q6,Qb)=1 (ell=4 also certified).
    """
    import sympy as sp
    X = sp.symbols('X')

    def sym(c):
        n = len(c) - 1
        return sum(int(v) * X**(n - i) for i, v in enumerate(c))
    Q1s, Q2s = sym(vu.Q1), sym(vu.Q2)
    Q3s, Q4s, Q5s, Q6s = sym(Q3), sym(Q4), sym(Q5), sym(Q6)

    # --- Q6 Doche condition (4) ---
    print(f"  deg_X Q6 = {DEG_Q6} (>0: {DEG_Q6 > 0})")
    print(f"  Q6(0) = {Q6s.subs(X, 0)}  Q6(1) = {Q6s.subs(X, 1)}")
    q6_norm = (int(Q6s.subs(X, 0)) == 1 and int(Q6s.subs(X, 1)) == 1)
    sq6 = (sp.gcd(Q6s, sp.diff(Q6s, X)) == 1)
    print(f"  Q6(0)=Q6(1)=1: {q6_norm}   Q6 squarefree: {sq6}")

    # --- active dictionary W = Q1*Q2*Q5*Q6 (the CERTIFIED Angle, qB=qC=0) ---
    W = sp.expand(Q1s * Q2s * Q5s * Q6s)
    degW = sp.degree(W, X)
    W0, W1 = int(W.subs(X, 0)), int(W.subs(X, 1))
    print(f"  [certified family, qB=qC=0]  deg_X W=Q1*Q2*Q5*Q6 = {degW}  "
          f"W(0)={W0}  W(1)={W1}")
    nox = abs(W0) >= 1 and abs(W1) >= 1
    print(f"  X !| W and (1-X) !| W: {nox}")

    # --- Q6 coprime to every kept factor (P_i, Q1, Q2): LOAD-BEARING ---
    kept_ok = True
    for nm, Pc in [("P1", vu.P1), ("P2", vu.P2), ("P4", vu.P4),
                   ("P6", vu.P6), ("P8", vu.P8)]:
        g = sp.gcd(sym(Pc), Q6s) == 1
        kept_ok = kept_ok and g
        print(f"  gcd(Q6,{nm})=1: {g}")
    g61 = sp.gcd(Q6s, Q1s) == 1
    g62 = sp.gcd(Q6s, Q2s) == 1
    print(f"  gcd(Q6,Q1)=1: {g61}   gcd(Q6,Q2)=1: {g62}")
    kept_ok = kept_ok and g61 and g62

    # --- LOAD-BEARING inter-block: gcd(Q6,Q5)=1 (new block coprime to held Q5) ---
    g65 = sp.gcd(Q6s, Q5s) == 1
    print(f"  *** LOAD-BEARING inter-block *** gcd(Q6,Q5)=1: {g65}")
    kept_ok = kept_ok and g65

    # --- inter-block grid vs the deg-24 Qa,Qb (needed only if an ell=4 run is used) ---
    g63 = sp.gcd(Q6s, Q3s) == 1
    g64 = sp.gcd(Q6s, Q4s) == 1
    print(f"  *** ell=4 inter-block *** gcd(Q6,Qa)=1: {g63}   gcd(Q6,Qb)=1: {g64}")

    certified_ok = ((DEG_Q6 > 0) and q6_norm and sq6 and nox and kept_ok)
    full_ok = certified_ok and g63 and g64
    print(f"  CERTIFIED-FAMILY admissibility (W=Q1*Q2*Q5*Q6, Doche Lemma 5): "
          f"{certified_ok}")
    print(f"  FULL ell=4 admissibility (incl. Qa,Qb inter-block): {full_ok}")
    return certified_ok if active_only else full_ok


def selftest_q6(q, qB, qC, qE, qF, ntest=200, seed=11):
    """Soundness on the CHANGED integrand: cell_int_maxAB_q6 must dominate the true
    int_cell max(A,B) dt (mpmath, high precision).  B now has qB*log|Q3| + qC*log|Q4|
    + qE*log|Q5| + qF*log|Q6| -- the q5 selftest did NOT cover the qF*log|Q6| term."""
    import mpmath as mp
    import random
    mp.mp.prec = 160
    ASCmp = {nm: [int(c) for c in vu.ASC[nm]] for nm in vu.ASC}
    ASCmp_Q3 = [int(c) for c in ASC_Q3]
    ASCmp_Q4 = [int(c) for c in ASC_Q4]
    ASCmp_Q5 = [int(c) for c in ASC_Q5]
    ASCmp_Q6 = [int(c) for c in ASC_Q6]

    def G_exact(t):
        w = mp.e**(1j * mp.mpf(t)) - mp.e**(2j * mp.mpf(t))

        def lp(asc):
            v = mp.mpc(0)
            for c in reversed(asc):
                v = v * w + c
            return mp.log(abs(v))
        A = sum(mp.mpf(q[i]) * lp(ASCmp[nm])
                for i, nm in enumerate(["P1", "P2", "P4", "P6", "P8"]))
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
        cell_hi, refine = cell_int_maxAB_q6(A, B, np.asarray(q, float),
                                            float(qB), float(qC), float(qE),
                                            float(qF), cap)
        viol = 0
        wmin = 1e300                              # worst (cell_hi - true_int)
        for i in range(len(A)):
            K = 60
            ts = [A[i] + (B[i] - A[i]) * k / K for k in range(K + 1)]
            gs = [G_exact(t) for t in ts]
            true_int = (B[i] - A[i]) / K * (
                0.5 * gs[0] + 0.5 * gs[-1] + sum(gs[1:-1]))
            disc = cell_hi[i] - true_int          # MUST be >= 0 (safe side)
            wmin = min(wmin, disc)
            if cell_hi[i] < true_int - 1e-12:
                viol += 1
                if viol <= 5:
                    print(f"  [{tag}] VIOLATION cell[{A[i]:.5f},{B[i]:.5f}] "
                          f"hi={cell_hi[i]:.10f} < true~{true_int:.10f}")
        print(f"  selftest_q6[{tag}]: {viol}/{ntest} violations  (MUST be 0)  "
              f"worst (cell_hi - true_int) = {wmin:.3e} (>=0 is safe)")
        worst += viol
    return worst == 0


# R10-held reviewer-verified UPPER value, the value this round must STRICTLY beat.
HELD_CERT = 0.2540639638


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "anchor"
    # R10 (q5) optimum (the qF=0 anchor point): the held Angle family h=Q1*Q2*Q5^qE.
    R10_Q = [12.832632, 11.283857, 2.380952, 2.049198, 0.701066]
    R10_QE = 0.862588
    # R9 (q4) optimum (the qE=qF=0 anchor point): the held ell=2 family.
    R9_Q = [13.5067, 9.9134, 2.7258, 1.7086, 0.7364]
    R9_QB = 0.1092
    R9_QC = 0.2437

    if mode == "anchor":
        print("[anchor 1] qF=0 must reproduce the R10 (q5) Angle family BIT-IDENTICALLY.")
        v6 = float_value_q6(R10_Q, 0.0, 0.0, R10_QE, 0.0, N=8_000_000)
        v5 = vq5.float_value_q5(R10_Q, 0.0, 0.0, R10_QE, N=8_000_000)
        print(f"  float_value_q6(R10 q, qB=qC=0, qE, qF=0) = {v6:.12f}")
        print(f"  float_value_q5(R10 q, qB=qC=0, qE)       = {v5:.12f}")
        print(f"  match to >=10 digits: {abs(v6 - v5) < 1e-10}")
        D6 = _Dval(np.array(R10_Q), 0.0, 0.0, R10_QE, 0.0)
        D5 = vq5._Dval(np.array(R10_Q), 0.0, 0.0, R10_QE)
        print(f"  D_q6(qF=0) = {D6}   D_q5 = {D5}   match: {abs(D6-D5) < 1e-12}")
        # cell enclosure bit-identity at qF=0
        aa = np.array([1.0, 2.0, 3.0]); bb = aa + 1e-4
        c6, _ = cell_int_maxAB_q6(aa, bb, np.array(R10_Q), 0.0, 0.0, R10_QE,
                                  0.0, 1e-10)
        c5, _ = vq5.cell_int_maxAB_q5(aa, bb, np.array(R10_Q), 0.0, 0.0,
                                      R10_QE, 1e-10)
        print(f"  cell enclosure bit-identical at qF=0: "
              f"{np.array_equal(c6, c5)}")

        print("\n[anchor 2] qE=qF=0 must reproduce the R9 (q4) ell=2 family.")
        v6b = float_value_q6(R9_Q, R9_QB, R9_QC, 0.0, 0.0, N=8_000_000)
        v4 = vq4.float_value_q4(R9_Q, R9_QB, R9_QC, N=8_000_000)
        print(f"  float_value_q6(R9 q, qB,qC, qE=qF=0) = {v6b:.12f}")
        print(f"  float_value_q4(R9 q, qB,qC)          = {v4:.12f}")
        print(f"  match to >=10 digits: {abs(v6b - v4) < 1e-10}")
        D6b = _Dval(np.array(R9_Q), R9_QB, R9_QC, 0.0, 0.0)
        D4 = vq4._Dval(np.array(R9_Q), R9_QB, R9_QC)
        print(f"  D_q6(qE=qF=0) = {D6b}   D_q4 = {D4}   match: {abs(D6b-D4) < 1e-12}")

        print("\n[anchor 3] qB=qC=qE=qF=0 must reproduce the Doche BASE h=Q1*Q2, D=56.")
        BASE_Q = [11.73584, 8.77354, 2.44938, 1.55411, 0.53442]  # R6 base q
        vb = float_value_q6(BASE_Q, 0.0, 0.0, 0.0, 0.0, N=8_000_000)
        vu_b = vu.float_value(q=BASE_Q)
        Db = _Dval(np.array(BASE_Q), 0.0, 0.0, 0.0, 0.0)
        print(f"  float_value_q6(base q, all 0) = {vb:.12f}")
        print(f"  vu.float_value(base q)        = {vu_b:.12f}")
        print(f"  match to >=10 digits: {abs(vb - vu_b) < 1e-10}")
        print(f"  D at qB=qC=qE=qF=0 = {Db}  (must be 56-branch; "
              f"sum q.degP = {float(np.dot(BASE_Q, DEGP)):.5f})")
        print(f"  D == 56: {abs(Db - 56.0) < 1e-12}")
    elif mode == "admiss":
        admissibility_check_q6()
    elif mode == "selftest":
        q = [float(x) for x in sys.argv[2:7]]
        qB = float(sys.argv[7]); qC = float(sys.argv[8])
        qE = float(sys.argv[9]); qF = float(sys.argv[10])
        print(f"[selftest_q6] q={q} qB={qB} qC={qC} qE={qE} qF={qF}")
        ok = selftest_q6(q, qB, qC, qE, qF)
        print(f"  selftest passed: {ok}")
        sys.exit(0 if ok else 1)
    elif mode == "tamper":
        q = np.array([float(x) for x in sys.argv[2:7]])
        qB = float(sys.argv[7]); qC = float(sys.argv[8])
        qE = float(sys.argv[9]); qF = float(sys.argv[10])
        bogus = float(sys.argv[11])
        print(f"=== TAMPER  q={q.tolist()} qB={qB} qC={qC} qE={qE} qF={qF} "
              f"bogus={bogus} ===")
        logh_hi, nbad, _, _, _, _, _ = certify_maxAB_q6(
            q, qB, qC, qE, qF, "tamper", bogus, M0=200000, max_refine=14,
            rem_cap=1e-10, verbose=True)
        beats = (logh_hi < bogus) and (nbad == 0)
        print(f"  BEATS bogus target: {beats}  (frontier resolved: {nbad==0})")
        print("  EXPECT BEATS=False (bogus target is below truth).")
        sys.exit(0)
    elif mode == "certify":
        q = np.array([float(x) for x in sys.argv[2:7]])
        qB = float(sys.argv[7]); qC = float(sys.argv[8])
        qE = float(sys.argv[9]); qF = float(sys.argv[10])
        M0 = int(sys.argv[11]) if len(sys.argv) > 11 else 200000
        max_refine = int(sys.argv[12]) if len(sys.argv) > 12 else 14
        rem_cap = float(sys.argv[13]) if len(sys.argv) > 13 else 1e-10
        print(f"=== certify_q6  q={q.tolist()} qB={qB} qC={qC} qE={qE} qF={qF} ===")
        print(f"    M0={M0} max_refine={max_refine} rem_cap={rem_cap}")
        print("\n[admissibility] active perturbing dictionary (Doche Lemma 5)")
        adm = admissibility_check_q6()
        if not adm:
            print("    ABORT: admissibility failed.")
            sys.exit(1)
        print("\n[float] log h(q,qB,qC,qE,qF) ~ (CONJECTURE)")
        vq = float_value_q6(q.tolist(), qB, qC, qE, qF, N=8_000_000)
        print(f"    float log h = {vq:.10f}  h = {math.exp(vq):.10f}")
        print("\n[selftest_q6] soundness of per-cell bound on THIS integrand")
        ok = selftest_q6(q.tolist(), qB, qC, qE, qF)
        print(f"    selftest passed: {ok}")
        if not ok:
            print("    ABORT: selftest failed, certificate not trustworthy.")
            sys.exit(1)
        print("\n[certify] rigorous max(A,B) quadrature enclosure")
        logh_hi, nbad, elapsed, n_leaf, tot, ints, D = certify_maxAB_q6(
            q, qB, qC, qE, qF, "q6", HELD_CERT, M0=M0, max_refine=max_refine,
            rem_cap=rem_cap, verbose=True)
        print("\n=== RESULT ===")
        print(f"  CERTIFIED  log h <= {logh_hi:.10f}")
        print(f"  unresolved frontier cells = {nbad}  (MUST be 0)")
        print(f"  leaves = {n_leaf}")
        print(f"  held R10 certified        = {HELD_CERT:.10f}")
        print(f"  int_0^2pi G dt <= {tot:.10f}")
        print(f"  int_0^1 G ds   <= {ints:.10f}   D = {D}")
        print(f"  hand arithmetic: {ints:.10f} / {D} = {ints/D:.12f}")
        beats = (logh_hi < HELD_CERT) and (nbad == 0)
        print(f"  beats held (strict, frontier=0): {beats}")
        if beats:
            print(f"  margin below held = {HELD_CERT - logh_hi:.4e}")
        sys.exit(0 if (nbad == 0) else 1)
