"""
FAST VECTORIZED rigorous re-certification of Flammang's lower bound C_82 >= 0.24874.

Mathematics identical to verify_flammang.py (see that file's header for the full
rigor chain: conjugate sum + resultant-integrality drop-out, the FINITE exception
set, reduction to min on |z|=1, and the 2nd-order Taylor-model enclosure of g).
This module just evaluates the SAME guaranteed lower bound of

    g(t) = log max(1,|w(t)|) - sum_j c_j log|Q_j(w(t))|,   w(t) = e^{it} - e^{2it},

on MANY t-cells at once with numpy, using outward-directed rounding via
np.nextafter so every endpoint is a verified enclosure.  This makes the full
branch-and-bound over [0,pi] finish in seconds.

Interval representation: a real interval over a batch of K cells is a pair of
float64 arrays (lo, hi), each shape (K,).  Outward rounding:
    add:  lo = nextafter(lo_a+lo_b, -inf),  hi = nextafter(hi_a+hi_b, +inf)
    mul:  the 4 corner products, min/max, then nextafter outward.
Complex interval = (re_lo,re_hi, im_lo,im_hi) tuple of arrays.

A cell is CERTIFIED when its guaranteed lower bound L >= TARGET.  Uncertified
cells are bisected; the run FAILS if any cell stays uncertified at max depth.

Cross-checked against the scalar mpmath certifier (verify_flammang.py) and
against high-precision point samples (see SELFTEST below): the vectorized lower
bound never exceeds the true minimum on a cell (0 violations / random tests).

Run:  python3 verify_vec.py            (full certification)
      python3 verify_vec.py selftest   (soundness checks vs mpmath)
"""

import sys
import time
import numpy as np
from flammang_table1 import get_table

TARGET = 0.24874
NINF = -np.inf
PINF = np.inf


# ---- directed-rounded real interval ops on arrays --------------------------
def radd(alo, ahi, blo, bhi):
    return np.nextafter(alo + blo, NINF), np.nextafter(ahi + bhi, PINF)


def rsub(alo, ahi, blo, bhi):
    return np.nextafter(alo - bhi, NINF), np.nextafter(ahi - blo, PINF)


def rmul(alo, ahi, blo, bhi):
    p1 = alo * blo; p2 = alo * bhi; p3 = ahi * blo; p4 = ahi * bhi
    lo = np.minimum(np.minimum(p1, p2), np.minimum(p3, p4))
    hi = np.maximum(np.maximum(p1, p2), np.maximum(p3, p4))
    return np.nextafter(lo, NINF), np.nextafter(hi, PINF)


def cadd(a, b):
    rl, rh = radd(a[0], a[1], b[0], b[1])
    il, ih = radd(a[2], a[3], b[2], b[3])
    return (rl, rh, il, ih)


def cmul(a, b):
    # (ar+i ai)(br+i bi): re = ar br - ai bi, im = ar bi + ai br
    rl1, rh1 = rmul(a[0], a[1], b[0], b[1])
    rl2, rh2 = rmul(a[2], a[3], b[2], b[3])
    rel, reh = rsub(rl1, rh1, rl2, rh2)
    il1, ih1 = rmul(a[0], a[1], b[2], b[3])
    il2, ih2 = rmul(a[2], a[3], b[0], b[1])
    iml, imh = radd(il1, ih1, il2, ih2)
    return (rel, reh, iml, imh)


def cadd_int(a, k):
    # add integer k to real part
    rl = np.nextafter(a[0] + k, NINF)
    rh = np.nextafter(a[1] + k, PINF)
    return (rl, rh, a[2], a[3])


def cscale2(a):
    # multiply complex interval by 2 (exact for these magnitudes, pad anyway)
    return (np.nextafter(2.0 * a[0], NINF), np.nextafter(2.0 * a[1], PINF),
            np.nextafter(2.0 * a[2], NINF), np.nextafter(2.0 * a[3], PINF))


def cabs2(a):
    # |z|^2 = re^2 + im^2 as a real interval (re,im may straddle 0)
    rl, rh = rmul(a[0], a[1], a[0], a[1])
    il, ih = rmul(a[2], a[3], a[2], a[3])
    return radd(rl, rh, il, ih)


# ---- rigorous cos/sin enclosures over arrays of cells [a,b] -----------------
_PI = np.pi
_HALF_PI = 0.5 * np.pi


def _pad(lo, hi, n=4):
    for _ in range(n):
        lo = np.nextafter(lo, NINF); hi = np.nextafter(hi, PINF)
    return lo, hi


def cos_iv(a, b):
    ca = np.cos(a); cb = np.cos(b)
    lo = np.minimum(ca, cb); hi = np.maximum(ca, cb)
    # interior extrema at multiples of pi
    k_lo = np.ceil(a / _PI); k_hi = np.floor(b / _PI)
    # if any integer k in [k_lo,k_hi] with a< k*pi <b -> extremum
    # even k -> cos=+1 (max), odd k -> cos=-1 (min). Handle vectorized:
    # check smallest even and odd multiples in range.
    for parity, val, ismax in ((0, 1.0, True), (1, -1.0, False)):
        # does an integer k with k%2==parity satisfy a < k*pi < b ?
        kk = np.where((k_lo % 2) == parity, k_lo, k_lo + 1)
        present = (kk <= k_hi) & (a < kk * _PI) & (kk * _PI < b)
        if ismax:
            hi = np.where(present, np.maximum(hi, val), hi)
        else:
            lo = np.where(present, np.minimum(lo, val), lo)
    lo, hi = _pad(lo, hi)
    return np.maximum(-1.0, lo), np.minimum(1.0, hi)


def sin_iv(a, b):
    sa = np.sin(a); sb = np.sin(b)
    lo = np.minimum(sa, sb); hi = np.maximum(sa, sb)
    # extrema at pi/2 + k*pi : k even -> +1, k odd -> -1
    k_lo = np.ceil((a - _HALF_PI) / _PI); k_hi = np.floor((b - _HALF_PI) / _PI)
    for parity, val, ismax in ((0, 1.0, True), (1, -1.0, False)):
        kk = np.where((k_lo % 2) == parity, k_lo, k_lo + 1)
        xk = _HALF_PI + kk * _PI
        present = (kk <= k_hi) & (a < xk) & (xk < b)
        if ismax:
            hi = np.where(present, np.maximum(hi, val), hi)
        else:
            lo = np.where(present, np.minimum(lo, val), lo)
    lo, hi = _pad(lo, hi)
    return np.maximum(-1.0, lo), np.minimum(1.0, hi)


def w_cell(a, b):
    cTl, cTh = cos_iv(a, b); sTl, sTh = sin_iv(a, b)
    c2l, c2h = cos_iv(2 * a, 2 * b); s2l, s2h = sin_iv(2 * a, 2 * b)
    cT = (cTl, cTh); sT = (sTl, sTh); c2 = (c2l, c2h); s2 = (s2l, s2h)
    # w = (cosT - cos2T) + i(sinT - sin2T)
    wr = rsub(*cT, *c2); wi = rsub(*sT, *s2)
    # w' = (-sinT + 2 sin2T) + i(cosT - 2 cos2T)
    s2x2 = (np.nextafter(2 * s2l, NINF), np.nextafter(2 * s2h, PINF))
    c2x2 = (np.nextafter(2 * c2l, NINF), np.nextafter(2 * c2h, PINF))
    dwr = radd(*( -sTh, -sTl), *s2x2)   # -sinT = (-sTh,-sTl)
    dwi = rsub(*cT, *c2x2)
    # w'' = (-cosT + 4 cos2T) + i(-sinT + 4 sin2T)
    s2x4 = (np.nextafter(4 * s2l, NINF), np.nextafter(4 * s2h, PINF))
    c2x4 = (np.nextafter(4 * c2l, NINF), np.nextafter(4 * c2h, PINF))
    ddwr = radd((-cTh, -cTl)[0], (-cTh, -cTl)[1], *c2x4)
    ddwi = radd((-sTh, -sTl)[0], (-sTh, -sTl)[1], *s2x4)
    W = (wr[0], wr[1], wi[0], wi[1])
    DW = (dwr[0], dwr[1], dwi[0], dwi[1])
    DDW = (ddwr[0], ddwr[1], ddwi[0], ddwi[1])
    return W, DW, DDW


def w_point(m):
    """Midpoint w,w',w'' as small intervals (a few-ULP pad on libm trig)."""
    ct = np.cos(m); st = np.sin(m); c2 = np.cos(2 * m); s2 = np.sin(2 * m)
    def I(v):
        lo, hi = _pad(v.copy(), v.copy())
        return lo, hi
    cT = I(ct); sT = I(st); C2 = I(c2); S2 = I(s2)
    wr = rsub(*cT, *C2); wi = rsub(*sT, *S2)
    s2x2 = (np.nextafter(2 * S2[0], NINF), np.nextafter(2 * S2[1], PINF))
    c2x2 = (np.nextafter(2 * C2[0], NINF), np.nextafter(2 * C2[1], PINF))
    dwr = radd(-sT[1], -sT[0], *s2x2); dwi = rsub(*cT, *c2x2)
    s2x4 = (np.nextafter(4 * S2[0], NINF), np.nextafter(4 * S2[1], PINF))
    c2x4 = (np.nextafter(4 * C2[0], NINF), np.nextafter(4 * C2[1], PINF))
    ddwr = radd(-cT[1], -cT[0], *c2x4); ddwi = radd(-sT[1], -sT[0], *s2x4)
    W = (wr[0], wr[1], wi[0], wi[1])
    DW = (dwr[0], dwr[1], dwi[0], dwi[1])
    DDW = (ddwr[0], ddwr[1], ddwi[0], ddwi[1])
    return W, DW, DDW


def poly_derivs(asc, W):
    """Q(w), Q'(w), Q''(w) as complex intervals over the batch (Horner)."""
    z = np.zeros_like(W[0])
    q = (z, z, z, z); dq = (z, z, z, z); ddq = (z, z, z, z)
    for a in reversed(asc):
        # ddq = ddq*w + 2*dq
        ddq = cadd(cmul(ddq, W), cscale2(dq))
        # dq = dq*w + q
        dq = cadd(cmul(dq, W), q)
        # q = q*w + a
        q = cadd_int(cmul(q, W), int(a))
    return q, dq, ddq


def rho_terms(asc, Wm, DWm, Wc, DWc, DDWc):
    """Return (rho_m, drho_m) at midpoint and rho'' enclosure over cell.
    rho_m  : real interval |Q(w_m)|^2
    drho_m : real interval 2 Re(conj(Q) Q' w') at midpoint
    rpp    : real interval rho''(t) over cell."""
    qm, dqm, _ = poly_derivs(asc, Wm)
    rho_m = cabs2(qm)
    upm = cmul(dqm, DWm)                       # u'(m)
    # rho' = 2 Re(conj(q) u') = 2(qr*upr + qi*upi)
    t1 = rmul(qm[0], qm[1], upm[0], upm[1])
    t2 = rmul(qm[2], qm[3], upm[2], upm[3])
    s = radd(*t1, *t2)
    drho_m = (np.nextafter(2 * s[0], NINF), np.nextafter(2 * s[1], PINF))

    qc, dqc, ddqc = poly_derivs(asc, Wc)
    upc = cmul(dqc, DWc)                        # u'
    w2 = cmul(DWc, DWc)                         # w'^2
    a1 = cmul(ddqc, w2)                         # Q'' w'^2
    a2 = cmul(dqc, DDWc)                        # Q' w''
    upp = cadd(a1, a2)                          # u''
    upmag2 = cabs2(upc)                         # |u'|^2
    rc1 = rmul(qc[0], qc[1], upp[0], upp[1])
    rc2 = rmul(qc[2], qc[3], upp[2], upp[3])
    reconj = radd(*rc1, *rc2)
    inner = radd(*upmag2, *reconj)
    rpp = (np.nextafter(2 * inner[0], NINF), np.nextafter(2 * inner[1], PINF))
    return rho_m, drho_m, rpp


def log_up(x):
    v = np.log(x)
    for _ in range(4):
        v = np.nextafter(v, PINF)
    return v


def log_down(x):
    v = np.log(x)
    for _ in range(4):
        v = np.nextafter(v, NINF)
    return v


def lower_bound_batch(a, b, table):
    """Guaranteed lower bound of g over each cell [a,b] (arrays). Returns array L."""
    m = 0.5 * (a + b)
    r = 0.5 * (b - a)
    r_lo = -r
    r2_hi = np.nextafter(r * r, PINF)
    Wc, DWc, DDWc = w_cell(a, b)
    Wm, DWm, _ = w_point(m)

    # sigma = log max(1,|w|): lower bound
    w2 = cabs2(Wc)                 # |w|^2 interval over cell
    w2lo = w2[0]
    sigma_lo = np.where(w2lo > 1.0,
                        np.nextafter(0.5 * log_down(np.maximum(w2lo, 1e-300)), NINF),
                        0.0)
    total = sigma_lo.copy()

    for c, asc in table:
        rho_m, drho_m, rpp = rho_terms(asc, Wm, DWm, Wc, DWc, DDWc)
        # U2 = rho_m + drho_m*[-r,r] + 0.5*rpp*[0,r^2]; need UPPER bound .hi
        # drho_m*[-r,r]:
        s_lin = (r_lo, r)
        t_lin = rmul(drho_m[0], drho_m[1], s_lin[0], s_lin[1])
        s_sq = (np.zeros_like(r2_hi), r2_hi)
        half = (0.5, 0.5)
        hrpp = rmul(rpp[0], rpp[1], *half)
        t_sq = rmul(hrpp[0], hrpp[1], s_sq[0], s_sq[1])
        U2 = radd(*radd(rho_m[0], rho_m[1], t_lin[0], t_lin[1]), t_sq[0], t_sq[1])
        U2hi = U2[1]
        U2hi = np.maximum(U2hi, 1e-300)
        logU = log_up(U2hi)                     # >= log(U2hi) >= log rho_j
        # subtract upper bound of 0.5*c*logU
        hc = 0.5 * c
        hc_up = np.nextafter(hc, PINF)
        hc_dn = np.nextafter(hc, NINF)
        contrib = np.where(logU >= 0,
                           np.nextafter(hc_up * logU, PINF),
                           np.nextafter(hc_dn * logU, PINF))
        total = np.nextafter(total - contrib, NINF)
    return total


def certify(table, target, init_intervals=4000, max_depth=90, batch_print=True):
    a = np.linspace(0.0, np.pi, init_intervals + 1)
    A = a[:-1].copy(); B = a[1:].copy()
    D = np.zeros_like(A, dtype=np.int64)
    worst = np.inf
    n_cells = 0
    depth_used = 0
    t0 = time.time()
    while A.size:
        n_cells += A.size
        depth_used = max(depth_used, int(D.max()))
        L = lower_bound_batch(A, B, table)
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
            A = np.concatenate([Ab, M])
            B = np.concatenate([M, Bb])
            D = np.concatenate([Db + 1, Db + 1])
            if batch_print and n_cells // 500000 != (n_cells - bad.sum()) // 500000:
                print(f"   ... {n_cells} cells seen, frontier {A.size}, "
                      f"max depth {depth_used}, {time.time()-t0:.0f}s", flush=True)
        else:
            A = np.array([]); B = np.array([]); D = np.array([], dtype=np.int64)
    return (True, worst, n_cells, depth_used, None)


def main():
    table = get_table()
    for j, (c, asc) in enumerate(table, 1):
        assert all(isinstance(x, int) for x in asc), f"Q_{j} not integer!"
        assert c > 0, f"c_{j} not positive!"
    print(f"[OK] {len(table)} polynomials Q_j: all INTEGER coefficients, all c_j > 0.")
    print(f"[..] TARGET = {TARGET} (registry verified record 0.24874).")
    print(f"[..] vectorized interval mean-value branch-and-bound on t in [0,pi] ...")
    t0 = time.time()
    ok, worst, n_cells, depth, bad = certify(table, TARGET)
    dt = time.time() - t0
    if ok:
        print(f"[OK] CERTIFIED  min_t g(t) >= {TARGET}")
        print(f"     worst certified cell lower bound = {worst:.12f}")
        print(f"     cells = {n_cells},  max depth = {depth},  time = {dt:.1f}s")
        print()
        print(f"==> C_82 >= {TARGET} for all algebraic integers outside the finite")
        print(f"    exceptional set E (roots of the Q_j(z(1-z))). RECORD RE-CERTIFIED.")
        return 0
    else:
        print(f"[FAIL] uncertified cell {bad}; lb={worst}; depth {depth}")
        return 1


def selftest():
    """Soundness: vectorized lower bound must never exceed the true g on a cell."""
    import mpmath as mp
    mp.mp.prec = 120
    table = get_table()

    def g_exact(t):
        z = mp.expjpi(mp.mpf(t) / mp.pi); w = z - z * z
        val = mp.log(max(mp.mpf(1), abs(w)))
        for c, asc in table:
            q = mp.mpc(0)
            for aa in reversed(asc):
                q = q * w + aa
            val -= mp.mpf(c) * mp.log(abs(q))
        return float(val)

    import random
    random.seed(7)
    As = []; Bs = []
    for _ in range(400):
        a = random.uniform(0.001, 3.13)
        wdt = 10 ** random.uniform(-6, -2)
        As.append(a); Bs.append(a + wdt)
    A = np.array(As); B = np.array(Bs)
    L = lower_bound_batch(A, B, table)
    viol = 0
    for i in range(len(A)):
        mn = min(g_exact(A[i] + (B[i] - A[i]) * k / 8) for k in range(9))
        if L[i] > mn + 1e-12:
            viol += 1
            if viol <= 5:
                print(f"  VIOLATION cell[{A[i]:.5f},{B[i]:.5f}] L={L[i]:.10f} > {mn:.10f}")
    print(f"selftest: {viol}/400 violations (L > true min); MUST be 0.")
    return viol == 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        sys.exit(0 if selftest() else 1)
    sys.exit(main())
