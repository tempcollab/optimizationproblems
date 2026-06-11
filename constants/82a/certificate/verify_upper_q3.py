"""
R7 RIGOROUS upper-bound certificate for C_82, ENLARGED 6-exponent family.

This EXTENDS the reviewer-verified max(A,B) quadrature of verify_upper.py to a
Doche perturbing dictionary enriched by ONE free-exponent third block Q3=Qa.

Family (Issue A, outline review): Q1*Q2 stays the FIXED distinguished block
Q_{l+1} (exponent 1); Q3 enters as a FREE-exponent block with exponent qB>=0.

  A(t) = sum_i q_i * (1/2) log|P_i(w(t))|^2                 (prod-P^q branch)
  B(t) = (1/2)log|Q1(w(t))|^2 + (1/2)log|Q2(w(t))|^2
                                  + qB * (1/2)log|Q3(w(t))|^2   (Q-branch, Q3 WEIGHTED)
  G(t) = max(A(t), B(t)) = log max(|prod P^q(w)|, |Q1 Q2 (Q3)^{qB}(w)|)  (Jensen)
  log h(q,qB) = (1/(2 pi D)) int_0^{2pi} G dt,
  D = max( sum_i q_i deg_X P_i ,  56 + qB * deg_X Q3 )     (Issue B: D's 2nd branch).

At qB=0:  B reduces to log|Q1|+log|Q2|, D's 2nd branch reduces to 56, so the
integrand AND D are IDENTICAL to verify_upper.py -- the held R6 family is recovered
EXACTLY (Issue A / Issue D calibration anchor).

The per-cell enclosure machinery (rho_full -> midpoint value / slope / curvature /
cell sup-inf of (1/2)log|.|^2, all OUTWARD-rounded) is reused VERBATIM from
verify_upper.py via `import verify_upper as vu`.  The ONLY change is that Q3 is added
to the B-branch with weight qB, exactly as each P_i is added to A with weight q_i --
the rigor treatment of a Q3 factor in B is mechanically identical to a P factor in A
(same rho_full output, weighted, outward-rounded).  Because the integrand changed,
the mpmath soundness selftest (selftest_q3) MUST be re-run on THIS integrand (Issue B);
the R5/R6 selftest only covered the OLD B-branch.

Validity: Doc01a Lemmas 2,3,4,5 give log h(q,qB) as a true limit point of the ZZ
spectrum for any admissible (q, qB>=0) (no optimality needed), hence C_82 <= log h.
Admissibility of W=Q1*Q2*Q3 (deg 80>0, W(0)=W(1)=1, Q3 squarefree, gcd(Q3,P_i)=
gcd(Q3,Q1)=gcd(Q3,Q2)=1) is verified by admissibility_check_q3() (Issue C).

Usage:
  python3 verify_upper_q3.py anchor       # qB=0 must reproduce held 0.2543309112
  python3 verify_upper_q3.py selftest q1..q5 qB
  python3 verify_upper_q3.py admiss
  python3 verify_upper_q3.py certify q1 q2 q3 q4 q5 qB [M0] [max_refine] [rem_cap]
"""

import sys
import time
import math
import numpy as np

import verify_vec as vv
import verify_upper as vu

NINF = -np.inf
PINF = np.inf
na = np.nextafter

# Q3 = Qa (Doc01a calibration perturber, deg 24, H = 1.290471208), high->low in X.
Q3 = [1, -6, 24, -77, 217, -546, 1252, -2647, 5195, -9457, 15898, -24521,
      34402, -43345, 48207, -46413, 37963, -25934, 14558, -6596, 2357, -642,
      126, -16, 1]
DEG_Q3 = len(Q3) - 1                  # = 24
ASC_Q3 = vu.asc(Q3)                   # ascending coeffs for vv.poly_derivs / rho_full

DEGP = vu.DEGP                        # [1,1,4,8,8]
DEGQ12 = vu.DEGQ                      # 56  (fixed distinguished block Q1*Q2)


def _Dval(q, qB):
    return max(float(np.dot(q, DEGP)), float(DEGQ12 + qB * DEG_Q3))


# ---------------------------------------------------------------------------
# Per-cell A,B data.  A branch == verify_upper.cell_AB's A branch (P1..P8).
# B branch == Q1 + Q2 (fixed) + qB*Q3 (free), each factor's (1/2)log|.|^2 enclosed
# by vu.rho_full exactly as in vu.cell_AB.
# ---------------------------------------------------------------------------
def cell_AB_q3(a, b, q, qB):
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

    # ---- B branch: log|Q1|^2/2 + log|Q2|^2/2 + qB*log|Q3|^2/2 ----
    B_hi = np.zeros_like(a)
    B_lo = np.zeros_like(a)
    B_mid_up = np.zeros_like(a)
    B_curv = np.zeros_like(a)
    B_slope = np.zeros_like(a)
    # (factor name, ascending coeffs, weight)
    Bfactors = [("Q1", vu.ASC["Q1"], 1.0),
                ("Q2", vu.ASC["Q2"], 1.0),
                ("Q3", ASC_Q3,       float(qB))]
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


def cell_int_maxAB_q3(a, b, q, qB, rem_cap):
    """UPPER bound on int_cell max(A,B) dt + a `refine` mask.  Identical logic to
    verify_upper.cell_int_maxAB; only cell_AB_q3 differs (Q3 in B)."""
    d = cell_AB_q3(a, b, q, qB)
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


def certify_maxAB_q3(q, qB, label, target, M0=200000, max_refine=14,
                     rem_cap=1e-10, verbose=True):
    """Guaranteed UPPER bound on log h(q,qB) via the un-split max(A,B) enclosure."""
    TWO_PI = na(2.0 * math.pi, PINF)
    edges = np.linspace(0.0, 2.0 * math.pi, M0 + 1)
    a = edges[:-1].copy()
    b = edges[1:].copy()
    total_resolved = 0.0
    t0 = time.time()
    rounds = 0
    nbad = 0
    n_leaf = 0
    D = _Dval(q, qB)
    while True:
        cell_hi, refine = cell_int_maxAB_q3(a, b, q, qB, rem_cap)
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
        print(f"  [{label}] CERTIFIED  log h(q,qB) <= {logh_hi:.10f}")
        print(f"  [{label}] target                  = {target:.10f}")
        print(f"  [{label}] BEATS target (strict <): "
              f"{logh_hi < target}   (margin {target - logh_hi:.3e})")
    return logh_hi, nbad, elapsed, n_leaf


# ---------------------------------------------------------------------------
def float_value_q3(q, qB, N=8_000_000):
    """Float midpoint Riemann sum of log h(q,qB) (CONJECTURE / anchor)."""
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
         + qB * np.log(np.abs(pv(Q3, chi))))
    G = np.maximum(A, B)
    D = _Dval(q, qB)
    return np.mean(G) / D


def admissibility_check_q3():
    """Issue C: admissibility of the ENLARGED dictionary W = Q1*Q2*Q3."""
    import sympy as sp
    X = sp.symbols('X')

    def sym(c):
        n = len(c) - 1
        return sum(int(v) * X**(n - i) for i, v in enumerate(c))
    Q1s, Q2s, Q3s = sym(vu.Q1), sym(vu.Q2), sym(Q3)
    W = sp.expand(Q1s * Q2s * Q3s)
    degW = sp.degree(W, X)
    W0, W1 = W.subs(X, 0), W.subs(X, 1)
    print(f"  deg_X Q3 = {DEG_Q3} (>0: {DEG_Q3 > 0})")
    print(f"  Q3(0) = {Q3s.subs(X, 0)}  Q3(1) = {Q3s.subs(X, 1)}")
    sqfree = (sp.gcd(Q3s, sp.diff(Q3s, X)) == 1)
    print(f"  Q3 squarefree: {sqfree}")
    print(f"  deg_X W = {degW}  W(0) = {W0}  W(1) = {W1}")
    nox = abs(int(W0)) >= 1 and abs(int(W1)) >= 1
    print(f"  X !| W and (1-X) !| W: {nox}")
    allc = True
    for nm, Pc in [("P1", vu.P1), ("P2", vu.P2), ("P4", vu.P4),
                   ("P6", vu.P6), ("P8", vu.P8)]:
        g = sp.gcd(sym(Pc), W); cop = (g == 1); allc = allc and cop
        print(f"  gcd({nm}, W) coprime: {cop}")
    g13 = sp.gcd(Q1s, Q3s) == 1
    g23 = sp.gcd(Q2s, Q3s) == 1
    print(f"  gcd(Q1,Q3) coprime: {g13}   gcd(Q2,Q3) coprime: {g23}")
    ok = (DEG_Q3 > 0) and sqfree and nox and allc and g13 and g23
    print(f"  ALL admissibility (Doche Lemma 5, enlarged dict) hold: {ok}")
    return ok


def selftest_q3(q, qB, ntest=200, seed=11):
    """Issue B/D soundness on the CHANGED integrand: cell_int_maxAB_q3 must
    dominate the true int_cell max(A,B) dt (mpmath, high precision)."""
    import mpmath as mp
    import random
    mp.mp.prec = 140
    ASCmp = {nm: [int(c) for c in vu.ASC[nm]] for nm in vu.ASC}
    ASCmp_Q3 = [int(c) for c in ASC_Q3]

    def G_exact(t):
        w = mp.e**(1j * mp.mpf(t)) - mp.e**(2j * mp.mpf(t))

        def lp(asc):
            v = mp.mpc(0)
            for c in reversed(asc):
                v = v * w + c
            return mp.log(abs(v))
        A = sum(mp.mpf(q[i]) * lp(ASCmp[nm])
                for i, nm in enumerate(["P1", "P2", "P4", "P6", "P8"]))
        B = lp(ASCmp["Q1"]) + lp(ASCmp["Q2"]) + mp.mpf(qB) * lp(ASCmp_Q3)
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
        cell_hi, refine = cell_int_maxAB_q3(A, B, np.asarray(q, float),
                                            float(qB), cap)
        viol = 0
        for i in range(len(A)):
            K = 60
            ts = [A[i] + (B[i] - A[i]) * k / K for k in range(K + 1)]
            gs = [G_exact(t) for t in ts]
            true_int = (B[i] - A[i]) / K * (
                0.5 * gs[0] + 0.5 * gs[-1] + sum(gs[1:-1]))
            if cell_hi[i] < true_int - 1e-12:
                viol += 1
                if viol <= 5:
                    print(f"  [{tag}] VIOLATION cell[{A[i]:.5f},{B[i]:.5f}] "
                          f"hi={cell_hi[i]:.10f} < true~{true_int:.10f}")
        print(f"  selftest_q3[{tag}]: {viol}/{ntest} violations  (MUST be 0)")
        worst += viol
    return worst == 0


HELD_CERT = 0.2543309112


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "anchor"
    R6_Q = [11.73584, 8.77354, 2.44938, 1.55411, 0.53442]

    if mode == "anchor":
        print("[anchor] qB=0 must reproduce the held R6 family EXACTLY.")
        v0 = float_value_q3(R6_Q, 0.0, N=8_000_000)
        vu_v0 = vu.float_value(q=R6_Q)
        print(f"  float_value_q3(R6 q, qB=0) = {v0:.10f}")
        print(f"  vu.float_value(R6 q)       = {vu_v0:.10f}")
        print(f"  match to >=10 digits: {abs(v0 - vu_v0) < 1e-10}")
        print(f"  D at qB=0 = {_Dval(np.array(R6_Q), 0.0)}  (must be 56-branch? "
              f"sum qdegP = {float(np.dot(R6_Q, DEGP)):.5f})")
    elif mode == "admiss":
        admissibility_check_q3()
    elif mode == "selftest":
        q = [float(x) for x in sys.argv[2:7]]
        qB = float(sys.argv[7])
        print(f"[selftest_q3] q={q} qB={qB}")
        ok = selftest_q3(q, qB)
        print(f"  selftest passed: {ok}")
        sys.exit(0 if ok else 1)
    elif mode == "certify":
        q = np.array([float(x) for x in sys.argv[2:7]])
        qB = float(sys.argv[7])
        M0 = int(sys.argv[8]) if len(sys.argv) > 8 else 200000
        max_refine = int(sys.argv[9]) if len(sys.argv) > 9 else 14
        rem_cap = float(sys.argv[10]) if len(sys.argv) > 10 else 1e-10
        print(f"=== certify_q3  q={q.tolist()} qB={qB} ===")
        print(f"    M0={M0} max_refine={max_refine} rem_cap={rem_cap}")
        print("\n[admissibility] enlarged dictionary W=Q1*Q2*Q3 (Issue C)")
        admissibility_check_q3()
        print("\n[float] log h(q,qB) ~ (CONJECTURE)")
        vq = float_value_q3(q.tolist(), qB, N=8_000_000)
        print(f"    float log h = {vq:.10f}  h = {math.exp(vq):.10f}")
        print("\n[selftest_q3] soundness of per-cell bound on THIS integrand")
        ok = selftest_q3(q.tolist(), qB)
        print(f"    selftest passed: {ok}")
        if not ok:
            print("    ABORT: selftest failed, certificate not trustworthy.")
            sys.exit(1)
        print("\n[certify] rigorous max(A,B) quadrature enclosure")
        logh_hi, nbad, elapsed, n_leaf = certify_maxAB_q3(
            q, qB, "q3", HELD_CERT, M0=M0, max_refine=max_refine,
            rem_cap=rem_cap, verbose=True)
        print("\n=== RESULT ===")
        print(f"  CERTIFIED  log h(q,qB) <= {logh_hi:.10f}")
        print(f"  unresolved frontier cells = {nbad}  (MUST be 0)")
        print(f"  held R6 certified         = {HELD_CERT:.10f}")
        beats = (logh_hi < HELD_CERT) and (nbad == 0)
        print(f"  beats held (strict, frontier=0): {beats}")
        if beats:
            print(f"  margin below held = {HELD_CERT - logh_hi:.4e}")
        sys.exit(0 if (nbad == 0) else 1)
