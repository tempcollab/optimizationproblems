"""
82a LOWER bound, PATH B stage-2 — RIGOROUS interval branch-and-bound certificate
WITH the OSS log-energy potential column.  Extends verify_vec.py by ONE added
potential-term loop (the lambda0 * U_mu0 term), mirroring its 24-column log|Q_j|
loop.  Goal: certify a LOWER bound m_energy > 0.2487458 (Flammang F18 record).

=============================================================================
THE RIGOROUS INEQUALITY CHAIN (frozen from freeze_energy.py; see that header + the
round-13 outline outline_lower_stage2_v2.md for full statements).
=============================================================================
Let P be the minimal polynomial of an algebraic integer alpha NOT in the finite
exception set E, deg d, conjugate measure nu (mass 1/d per conjugate, in z),
g(z)=log+|z|+log+|1-z| folded to log+|w|, w=z(1-z).  FROZEN data (frozen_energy.npz):
  - c_j >= 0  (j=1..24): the cut-LP DUAL weights on the Flammang Table-1 columns,
  - lambda0 >= 0        : the cut-LP DUAL weight on the energy cut,
  - mu0                 : a histogram (piecewise-constant) reference probability
                          measure on |z|=1, support {(center c_k, mass_k)}, each
                          bin a uniform arc of t-width L, mass_k>=0, sum=1,
  - Ihat = I_lo         : a RIGOROUS DOWNWARD enclosure of the FINITE log-energy
                          I(mu0) (closed form, rounded down — P3).

(C1) INT g dnu = (1/d) log Z(alpha).                                    [identity]
(C2) INT log|Q_j(w)| dnu >= 0, since Res(P, Q_j(z(1-z))) is a NONZERO INTEGER off E
     => |Res|>=1 => log>=0.                                             [>= 0]
(C3) ENERGY column (NEW, rigorous):  INT (2 U_mu0(z) - Ihat) dnu >= 0.  [>= 0]
     P1 (load-bearing): this rests on the CONTINUOUS negative-definiteness of the
     log kernel (Ahlfors Lemma 2.1 / OSS arXiv:2401.03252 eq.6): for ANY two
     FINITE-energy probability measures,  I(nu)+I(mu0)-2 I(nu,mu0) <= 0.  Both mu0
     (bounded histogram density) and nu (off E) have finite energy, so
        2 I(nu,mu0) - I(mu0) >= I(nu) >= 0
     (I(nu) = (1/d^2) log|disc(P)| >= 0 because disc(P) is a NONZERO INTEGER off E
     — the SAME finite-exception integrality clause as C2).  Replacing I(mu0) by
     Ihat <= I(mu0) keeps the inequality (the LHS only GAINS the nonneg I(mu0)-Ihat):
        INT(2 U_mu0 - Ihat) dnu = [2 I(nu,mu0)-I(mu0)] + (I(mu0)-Ihat) >= 0.
     The discretization in freeze_energy.py is only the numerical route to a
     rigorous LOWER bound Ihat on the SAME continuous I(mu0); it is NOT the proof
     of (C3).  (freeze_energy.py check prints the discrete NSD WITNESS: the
     exact-block conj-symmetric energy matrix has top eigenvalue ~1e-15 on the
     mass-zero subspace.)
(C4) POINTWISE (certified here by interval B&B on |z|=1):
        f(z) := g(z) - sum_j c_j log|Q_j(w)| - lambda0 (2 U_mu0(z) - Ihat) >= m_cert.
(C5) Average C4 against dnu; C2,C3 subtracted with NONNEG weights c_j, lambda0:
        (1/d) log Z(alpha) = INT g dnu >= m_cert  =>  C_82 >= m_cert.
The min-locus reduction to |z|=1 is Flammang's (R1): -2 lambda0 U_mu0 is
SUPERHARMONIC (positive log-potential of a measure ON |z|=1), so f attains its
minimum on |z|=1 and |1-z|=1, reduced to |z|=1 by z->1-z symmetry.  No Prop-6.1
log-R haircut: C4 is certified DIRECTLY and globally on |z|=1, no support split.

=============================================================================
THE POTENTIAL TERM, per cell (P4 — near-node cells are HARDEST, never free).
=============================================================================
f contains the SUBTRACTED term -lambda0 (2 U_mu0(t) - Ihat).  A LOWER bound on f
needs an UPPER bound on U_mu0(t) over the cell.  For the histogram mu0,
  U_mu0(t) = sum_k mass_k * (1/2)( P1_k(t) + P2_k(t) ),
  P1_k(t) = (1/L) INT_{arc_k} log|e^{it} - e^{is}| ds  (arc_k center c_k, width L),
  P2_k(t) = (1/L) INT_{arc_k} log|e^{it} - e^{-is}| ds  (conjugate; center -c_k).
Each P is an ARC-AVERAGE of log(distance); a rigorous UPPER bound over t in [a,b]:
  P_k(t) <= log( max_{t in [a,b], s in arc_k} |e^{it} - e^{i s}| )
         = log( max chord between cell-arc [a,b] and support-arc [c_k-L/2, c_k+L/2] ),
since the average is <= the max.  max chord = 2|sin(Delta/2)| at the maximum angular
separation Delta of the two arcs (finite, <= 2, on EVERY cell — including cells
containing a support node, where the far end of the cell is a positive distance from
the node).  Over-estimating U_mu0 only LOWERS f's bound — the SAFE direction.  Near
a support node the subtracted -2 lambda0 U_mu0 -> -inf in the limit, so those cells
have the LARGEST f and bisect normally; nothing auto-certifies (P4).

Run:  python3 verify_vec_energy.py            (full certification)
      python3 verify_vec_energy.py selftest   (soundness vs mpmath, incl. potential)

=============================================================================
R15 RESULT (TARGET raised 0.2509 -> 0.25113; ONLY the TARGET line changed):
=============================================================================
  [OK] CERTIFIED  min_t f(t) >= 0.2511300035   (cells=17564, depth=7, ~11.4s)
       worst/binding cell at t~1.4726 (mu0 node-cluster region; same binding
       region as R14), frontier fully resolved (0 unresolved cells).
       => C_82 >= 0.2511300035 > 0.2509000289 (R14 held) > 0.2487458 [Flammang F18].
       Margin over Flammang record +0.00238420; raise over R14 held +2.29975e-04.
  Non-regression / anchors (all unchanged f / mu0 / cj / lambda0 / Ihat):
    - selftest: 0/636 (scipy spence) + 0/88 (mpmath polylog) violations  (== R14).
    - R14 anchor certify(0.2509): ok=True, worst=0.2509000289, 6924 cells, depth 3
      (BIT-IDENTICAL to the R14 held cert -> this is a genuine tightening of the
      SAME f, not a different/broken certificate).
    - Ceiling tamper (proves NO auto-certify / NO grid fallback): a TARGET above the
      frozen-mu0 fine-grid ceiling 0.2511326614 correctly FAILS to resolve (ok=False
      via a depth-hit, never auto-certified):
        certify(0.2520, ...) -> ok=False  (depth-hit cell ~t=0.4712)
        certify(0.2512, ...) -> ok=False  (depth-hit cell ~t=1.4765, the binding
                                            ceiling cell just below where 0.25113 sits)
      [run with max_depth=10 for tractable runtime; at the original max_depth=14 the
       SAME cells still fail -- a larger max_depth only makes the B&B work longer
       before hitting the identical ceiling wall, it can NEVER certify above it.]
0.25113 sits 2.66e-5 below the ceiling -> robust headroom (resolved with room to
spare); we deliberately do NOT chase the last ~2.6e-5 (Clausen arc-average per-cell
over-estimate, depth-independent).  See approaches/lower_oss_energy_cut.md (R15).
"""

import sys
import time
import math
import numpy as np
from scipy.special import spence
from flammang_table1 import get_table

# import the verified geometric / poly machinery from the R1 cert unchanged
from verify_vec import (radd, rsub, rmul, cadd, cmul, cadd_int, cscale2, cabs2,
                        cos_iv, sin_iv, w_cell, w_point, poly_derivs, rho_terms,
                        log_up, log_down, NINF, PINF, _pad)

ANCHOR = 0.2487458
_FZ = np.load("frozen_energy.npz")
CJ = _FZ["cj"]                       # (24,) cut-LP dual column weights >= 0
LAM0 = float(_FZ["lambda0"])         # cut-LP dual energy weight >= 0
CENTERS = _FZ["centers"]             # (K,) mu0 support arc centers (t)
MASSES = _FZ["masses"]               # (K,) mu0 arc masses >= 0, sum 1
LBIN = float(_FZ["L"])               # mu0 arc t-width
IHAT = float(_FZ["Ihat"])            # rigorous downward I(mu0) enclosure
MCUT_LP = float(_FZ["m_cut"])        # LP value (conjecture, for reference)

assert np.all(CJ >= 0) and LAM0 >= 0 and np.all(MASSES >= 0)
assert abs(MASSES.sum() - 1.0) < 1e-9

# conservative target strictly above the record (0.2487458) but below the true min
# of f (~0.25115) so every cell resolves and the B&B reports the true worst cell.
# R15 raise: 0.25113 resolves in ~17.5k cells / depth ~7; the certified worst cell
# is ~0.2511300035, sitting ~2.66e-5 below the frozen-mu0 fine-grid ceiling
# 0.2511326614 (so it resolves with robust headroom). The +2e-4 left in R14 (0.2509)
# was pure B&B-target slack; raising TARGET tightens the SAME f/mu0/cj/Ihat cert.
# (R14 anchor: TARGET=0.2509 still resolves to 0.2509000289 — see checks().)
TARGET = 0.25113


# ---- per-cell UPPER bound on 2*lambda0*U_mu0(t) (the added potential loop) ----
# EXACT arc-average closed form (tight; converges with cell width, unlike max-chord):
#   P_k(t) = (1/L) INT_{arc} log|e^{it} - e^{i eps s}| ds
#          = ( Cl2(t - mu - L/2) - Cl2(t - mu + L/2) ) / L,    mu = eps*c_k,
# with Cl2(x) = Im Li2(e^{ix}) the Clausen function (= -INT_0^x log(2|sin(u/2)|)du,
# so Cl2'' gives the arc-average of log(2|sin|)).  We need an UPPER bound on P_k(t)
# over the cell: since L>0,  P_k <= ( Cl2_up([t-mu-L/2 range]) - Cl2_lo([t-mu+L/2 range]) )/L.
_TWO_PI = 2.0 * math.pi
_C_CL2 = 1.0149416064096536          # Cl2(pi/3), global max of Cl2; -value is the min
_CL2_PAD = 1e-11                     # rigorous outward pad (spence vs mpmath agrees ~1e-15)


def _cl2_pt(x):
    """Cl2(x) = Im Li2(e^{ix}), vectorized via scipy dilogarithm (spence(z)=Li2(1-z))."""
    return spence(1.0 - np.exp(1j * x)).imag


def _cl2_iv(xlo, xhi):
    """Rigorous enclosure (lo, hi) of Cl2 over [xlo, xhi] (arrays).  Cl2 is monotone
    between its extrema at x = pi/3 + 2 pi k (max +C) and x = -pi/3 + 2 pi k (min -C);
    enclosure = [min, max] of endpoint values and any enclosed extremum, padded out."""
    vlo = _cl2_pt(xlo); vhi = _cl2_pt(xhi)
    lo = np.minimum(vlo, vhi); hi = np.maximum(vlo, vhi)
    has_max = np.ceil((xlo - math.pi / 3) / _TWO_PI) <= np.floor((xhi - math.pi / 3) / _TWO_PI)
    hi = np.where(has_max, np.maximum(hi, _C_CL2), hi)
    has_min = np.ceil((xlo + math.pi / 3) / _TWO_PI) <= np.floor((xhi + math.pi / 3) / _TWO_PI)
    lo = np.where(has_min, np.minimum(lo, -_C_CL2), lo)
    return lo - _CL2_PAD, hi + _CL2_PAD


def _P_upper(a, b, mu):
    """UPPER bound (array) on P_k(t) = (Cl2(t-mu-L/2)-Cl2(t-mu+L/2))/L over t in [a,b]."""
    L = LBIN
    # arg1 = t-mu-L/2 over [a-mu-L/2, b-mu-L/2]; arg2 = t-mu+L/2 over [a-mu+L/2, b-mu+L/2]
    a1lo = a - mu - 0.5 * L; a1hi = b - mu - 0.5 * L
    a2lo = a - mu + 0.5 * L; a2hi = b - mu + 0.5 * L
    c1lo, c1hi = _cl2_iv(a1lo, a1hi)
    c2lo, c2hi = _cl2_iv(a2lo, a2hi)
    # P_up = (Cl2_up(arg1) - Cl2_lo(arg2)) / L, L>0
    num_hi = np.nextafter(c1hi - c2lo, PINF)
    Linv_up = np.nextafter(1.0 / L, PINF)
    return np.where(num_hi >= 0,
                    np.nextafter(num_hi * Linv_up, PINF),
                    np.nextafter(num_hi * np.nextafter(1.0 / L, NINF), PINF))


def pot_upper_batch(a, b):
    """UPPER bound (array) on U_mu0(t) over each cell [a,b]:
       U_mu0 <= sum_k mass_k * (1/2)( P_up(+c_k) + P_up(-c_k) ).
    All masses >= 0 so summing per-arc UPPER bounds gives a valid UPPER bound."""
    U = np.zeros_like(a)
    for c, mk in zip(CENTERS, MASSES):
        p1 = _P_upper(a, b, float(c))
        p2 = _P_upper(a, b, -float(c))
        half_sum = np.nextafter(0.5 * np.nextafter(p1 + p2, PINF), PINF)
        term = np.nextafter(float(mk) * half_sum, PINF)
        U = np.nextafter(U + term, PINF)
    return U                                    # >= U_mu0(t) on the cell


# ---- cell lower bound on f = g - sum c_j log|Q_j| - lambda0(2 U_mu0 - Ihat) ----
def lower_bound_batch(a, b):
    m = 0.5 * (a + b)
    r = 0.5 * (b - a)
    r_lo = -r
    r2_hi = np.nextafter(r * r, PINF)
    Wc, DWc, DDWc = w_cell(a, b)
    Wm, DWm, _ = w_point(m)

    # sigma = log max(1,|w|): lower bound (identical to verify_vec)
    w2 = cabs2(Wc)
    w2lo = w2[0]
    sigma_lo = np.where(w2lo > 1.0,
                        np.nextafter(0.5 * log_down(np.maximum(w2lo, 1e-300)), NINF),
                        0.0)
    total = sigma_lo.copy()

    # --- 24 Flammang columns, with the FROZEN cut-LP dual weights c_j ---
    table = get_table()
    for (c_unused, asc), cj in zip(table, CJ):
        if cj == 0.0:
            continue
        rho_m, drho_m, rpp = rho_terms(asc, Wm, DWm, Wc, DWc, DDWc)
        s_lin = (r_lo, r)
        t_lin = rmul(drho_m[0], drho_m[1], s_lin[0], s_lin[1])
        s_sq = (np.zeros_like(r2_hi), r2_hi)
        hrpp = rmul(rpp[0], rpp[1], 0.5, 0.5)
        t_sq = rmul(hrpp[0], hrpp[1], s_sq[0], s_sq[1])
        U2 = radd(*radd(rho_m[0], rho_m[1], t_lin[0], t_lin[1]), t_sq[0], t_sq[1])
        U2hi = np.maximum(U2[1], 1e-300)
        logU = log_up(U2hi)                     # >= log|Q_j(w)|^2
        hc = 0.5 * cj
        hc_up = np.nextafter(hc, PINF)
        hc_dn = np.nextafter(hc, NINF)
        contrib = np.where(logU >= 0,
                           np.nextafter(hc_up * logU, PINF),
                           np.nextafter(hc_dn * logU, PINF))
        total = np.nextafter(total - contrib, NINF)

    # --- NEW: the lambda0 * (2 U_mu0 - Ihat) potential term (ONE added loop) ---
    # subtract lambda0*(2 U_mu0_hi - Ihat); U_mu0_hi is the UPPER bound from pot_upper_batch.
    if LAM0 > 0.0:
        Uhi = pot_upper_batch(a, b)             # >= U_mu0(t)
        two_U = np.nextafter(2.0 * Uhi, PINF)   # >= 2 U_mu0
        bracket_hi = np.nextafter(two_U - IHAT, PINF)   # >= 2 U_mu0 - Ihat
        lam_up = np.nextafter(LAM0, PINF)
        lam_dn = np.nextafter(LAM0, NINF)
        # lambda0 >= 0; need an UPPER bound on lambda0*bracket to subtract:
        sub = np.where(bracket_hi >= 0,
                       np.nextafter(lam_up * bracket_hi, PINF),
                       np.nextafter(lam_dn * bracket_hi, PINF))
        total = np.nextafter(total - sub, NINF)
    return total


def certify(target, init_intervals=4000, max_depth=120, batch_print=True):
    a = np.linspace(0.0, np.pi, init_intervals + 1)
    A = a[:-1].copy(); B = a[1:].copy()
    D = np.zeros_like(A, dtype=np.int64)
    worst = np.inf
    n_cells = 0
    depth_used = 0
    t0 = time.time()
    last_print = 0
    while A.size:
        n_cells += A.size
        depth_used = max(depth_used, int(D.max()))
        L = lower_bound_batch(A, B)
        ok = L >= target
        if ok.any():
            worst = min(worst, float(L[ok].min()))
        bad = ~ok
        if bad.any():
            if (D[bad] >= max_depth).any():
                i = np.where(bad & (D >= max_depth))[0][0]
                return (False, float(L[i]), n_cells, depth_used, (float(A[i]), float(B[i])))
            Ab = A[bad]; Bb = B[bad]; Db = D[bad]
            M = 0.5 * (Ab + Bb)
            A = np.concatenate([Ab, M]); B = np.concatenate([M, Bb])
            D = np.concatenate([Db + 1, Db + 1])
            if batch_print and n_cells - last_print > 1_000_000:
                last_print = n_cells
                print(f"   ... {n_cells} cells, frontier {A.size}, depth {depth_used}, "
                      f"{time.time()-t0:.0f}s", flush=True)
        else:
            A = np.array([]); B = np.array([]); D = np.array([], dtype=np.int64)
    return (True, worst, n_cells, depth_used, None)


def main():
    print("=" * 74)
    print("82a LOWER — OSS log-energy interval B&B certificate (PATH B stage-2)")
    print("=" * 74)
    print(f"[..] frozen: support bins={len(CENTERS)}  L={LBIN:.6f}  lambda0={LAM0:.6f}")
    print(f"[..] Ihat (downward I(mu0))={IHAT:.10f}   sum c_j={CJ.sum():.6f}")
    print(f"[..] LP cut value m_cut={MCUT_LP:.10f} (conjecture); ANCHOR={ANCHOR}")
    print(f"[..] TARGET={TARGET} (> record 0.2487458); certifying min_t f(t) ...")
    t0 = time.time()
    ok, worst, n_cells, depth, bad = certify(TARGET)
    dt = time.time() - t0
    if ok:
        print(f"[OK] CERTIFIED  min_t f(t) >= {worst:.10f}")
        print(f"     worst certified cell lower bound m_energy = {worst:.10f}")
        print(f"     cells={n_cells}, max depth={depth}, time={dt:.1f}s")
        print(f"     RECORD 0.2487458 -> m_energy {worst:.10f}  "
              f"(margin {worst-ANCHOR:+.8f})")
        if worst > ANCHOR:
            print(f"==> C_82 >= {worst:.10f} > 0.2487458 = RECORD.  LOWER-BOUND BREAK.")
        else:
            print(f"==> m_energy does NOT beat the record; bound not improved.")
        return 0
    else:
        print(f"[FAIL] uncertified cell {bad}; L={worst}; depth {depth}")
        return 1


def selftest():
    """Soundness: the vectorized lower bound on f must never exceed true f on a cell.
    Includes near-mu0-node cells (the P4 hardest cells)."""
    import mpmath as mp
    mp.mp.prec = 120
    table = get_table()

    def Cl2_mp(x):
        return float(mp.im(mp.polylog(2, mp.e ** (1j * mp.mpf(x)))))

    def U_true_mp(t):
        """Histogram potential via mpmath polylog (independent of scipy spence)."""
        U = 0.0
        for c, mk in zip(CENTERS, MASSES):
            c = float(c); mk = float(mk)
            p1 = (Cl2_mp(t - c - 0.5 * LBIN) - Cl2_mp(t - c + 0.5 * LBIN)) / LBIN
            p2 = (Cl2_mp(t + c - 0.5 * LBIN) - Cl2_mp(t + c + 0.5 * LBIN)) / LBIN
            U += mk * 0.5 * (p1 + p2)
        return U

    def U_true_sp(t):
        """Same potential via scipy spence (fast); cross-checked == U_true_mp below."""
        c = CENTERS; mk = MASSES
        p1 = (_cl2_pt(t - c - 0.5 * LBIN) - _cl2_pt(t - c + 0.5 * LBIN)) / LBIN
        p2 = (_cl2_pt(t + c - 0.5 * LBIN) - _cl2_pt(t + c + 0.5 * LBIN)) / LBIN
        return float((mk * 0.5 * (p1 + p2)).sum())

    def f_exact(t, U_of_t):
        z = mp.expjpi(mp.mpf(t) / mp.pi); w = z - z * z
        val = mp.log(max(mp.mpf(1), abs(w)))
        for (c_un, asc), cj in zip(table, CJ):
            if cj == 0.0:
                continue
            q = mp.mpc(0)
            for aa in reversed(asc):
                q = q * w + aa
            val -= mp.mpf(float(cj)) * mp.log(abs(q))
        val -= mp.mpf(LAM0) * (2 * mp.mpf(U_of_t) - mp.mpf(IHAT))
        return float(val)

    # (0) confirm the spence and mpmath-polylog potentials agree (so the fast
    #     spence-based check below is a faithful stand-in for the polylog one).
    import random as _r
    _r.seed(5)
    du = max(abs(U_true_sp(_r.uniform(0.05, 3.09)) -
                 U_true_mp(_r.uniform(0.05, 3.09))) for _ in range(1))
    dchk = max(abs(U_true_sp(tt) - U_true_mp(tt))
               for tt in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0))
    print(f"  [potential xcheck] max |spence - mpmath polylog| over samples = {dchk:.2e}")

    import random
    random.seed(11)
    As = []; Bs = []
    # generic random cells
    for _ in range(500):
        a = random.uniform(0.001, 3.13)
        wdt = 10 ** random.uniform(-6, -2)
        As.append(a); Bs.append(a + wdt)
    # near-node cells (P4 hardest): straddle each mu0 support node and its conjugate
    for c in list(CENTERS) + [math.pi - float(c) for c in CENTERS]:
        for wdt in (1e-2, 1e-3, 1e-4, 1e-5):
            As.append(float(c) - 0.5 * wdt); Bs.append(float(c) + 0.5 * wdt)
    A = np.array(As); B = np.array(Bs)
    L = lower_bound_batch(A, B)

    # (1) FAST large soundness check: true f via scipy-spence potential.
    viol = 0; worst_gap = -1e9
    for i in range(len(A)):
        mn = min(f_exact(A[i] + (B[i] - A[i]) * k / 10, U_true_sp(A[i] + (B[i] - A[i]) * k / 10))
                 for k in range(11))
        worst_gap = max(worst_gap, L[i] - mn)
        if L[i] > mn + 1e-12:
            viol += 1
            if viol <= 8:
                print(f"  VIOLATION cell[{A[i]:.6f},{B[i]:.6f}] L={L[i]:.10f} > "
                      f"true_min={mn:.10f}")
    print(f"selftest(spence f): {viol}/{len(A)} violations (L > true f); MUST be 0.  "
          f"worst (L - true_min) = {worst_gap:+.2e}")

    # (2) HIGH-PRECISION mpmath cross-check on a small sample (incl. near-node cells).
    viol2 = 0
    idx = list(range(0, 20)) + list(range(500, 500 + 4 * len(CENTERS)))  # 20 generic + +c_k near-node
    for i in idx:
        mn = min(f_exact(A[i] + (B[i] - A[i]) * k / 10,
                         U_true_mp(A[i] + (B[i] - A[i]) * k / 10)) for k in range(11))
        if L[i] > mn + 1e-12:
            viol2 += 1
            print(f"  MP VIOLATION cell[{A[i]:.6f},{B[i]:.6f}] L={L[i]:.10f} > {mn:.10f}")
    print(f"selftest(mpmath polylog f): {viol2}/{len(idx)} violations; MUST be 0.")
    return viol == 0 and viol2 == 0


def checks():
    """Anchor + tamper sanity checks for the reviewer (fast)."""
    # ANCHOR: at lambda0=0 the potential term must drop out, so the per-cell bound
    # equals the no-energy LP-dual cell bound and its grid min ~ the LP m0=0.2487474.
    print("[anchor] lambda0=0 drops the energy term -> recovers the no-energy bound:")
    saved = globals()["LAM0"]
    cells = 200000
    a = np.linspace(0.0, np.pi, cells + 1)
    A = a[:-1]; B = a[1:]
    globals()["LAM0"] = 0.0
    L0 = lower_bound_batch(A, B)
    globals()["LAM0"] = saved
    Lf = lower_bound_batch(A, B)
    m0 = float(_FZ["m0"])
    # worst cell = MIN over the per-cell lower bounds (the binding cell)
    w0 = float(L0.min()); wf = float(Lf.min())
    print(f"   lambda0=0 fine-grid worst cell = {w0:.10f}  (no-energy LP m0="
          f"{m0:.10f}, diff {w0-m0:+.2e}; slightly below m0 due to grid-cell slack)")
    print(f"   WITH energy term, fine-grid worst cell = {wf:.10f}  "
          f"=> energy RAISE = {wf-w0:+.6f} (>0: the cut genuinely lifts the bound)")

    # TAMPER: a TARGET above the true worst cell (~0.25099) must FAIL to resolve.
    print("[tamper] a TARGET above the true min (0.2520) must FAIL to resolve:")
    ok, worst, n, depth, bad = certify(0.2520, init_intervals=2000,
                                       max_depth=14, batch_print=False)
    print(f"   TARGET=0.2520: ok={ok} (expected False), depth_hit={depth}, cells={n}")
    print(f"   => tamper {'PASSED (correctly failed)' if not ok else 'FAILED (false pass!)'}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        sys.exit(0 if selftest() else 1)
    if len(sys.argv) > 1 and sys.argv[1] == "checks":
        checks()
        sys.exit(0)
    sys.exit(main())
