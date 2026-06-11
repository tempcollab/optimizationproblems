"""
FAST rigorous re-certification of Flammang's lower bound C_82 >= 0.24874.

Same rigor chain and same 2nd-order Taylor-model enclosure as verify_flammang.py
(see that file's header for the full mathematical justification), but the inner
interval arithmetic is done in fast outward-rounded float64 (fastiv.py) instead
of mpmath.iv, giving ~100x speedup so the full branch-and-bound over [0,pi]
completes in minutes.

Enclosure of g(t) = log max(1,|w(t)|) - sum_j c_j log|Q_j(w(t))|, w(t)=e^{it}-e^{2it},
over a cell [a,b] (midpoint m, half-width r):

  * w, w', w'' enclosed over [a,b] via rigorous cos/sin interval enclosures.
  * w_m, w'_m, w''_m at the midpoint m as (near-degenerate) intervals.
  * For each j, rho_j(t) = |Q_j(w(t))|^2:
        rho_m   = |Q_j(w_m)|^2                              (narrow interval)
        rho'_m  = 2 Re(conj(Q_j(w_m)) Q_j'(w_m) w'_m)       (narrow interval)
        Rpp     = enclosure of rho''_j(t) over [a,b]        (wide, but x r^2)
    2nd-order Taylor (mean value of the remainder):
        rho_j(t) in  rho_m + rho'_m*[-r,r] + 0.5*Rpp*[0,r^2]
    Upper bound U2_j = .hi of that.  Then
        -c_j log|Q_j| = -0.5 c_j log rho_j >= -0.5 c_j log_up(U2_j)   (c_j>0).
    Only an UPPER bound on |Q_j|^2 is ever used, so the +infinity at Q_j zeros
    causes no blow-up (it only HELPS the lower bound).
  * sigma lower bound: 0.5 log_down(max(1, lower(|w|^2 over cell))) (>=0).
  * g(t) >= L(cell) = sigma_lo - sum_j 0.5 c_j log_up(U2_j).

Run:  python3 verify_fast.py
"""

import sys
import time
import math
import fastiv as F
from fastiv import Iv
from flammang_table1 import get_table

TARGET = 0.24874   # registry verified record


def w_derivs_cell(a, b):
    """w, w', w'' as complex intervals (re,im) over t in [a,b]."""
    cT = F.cos_iv(a, b); sT = F.sin_iv(a, b)
    c2 = F.cos_iv(2 * a, 2 * b); s2 = F.sin_iv(2 * a, 2 * b)
    two = Iv(2.0); four = Iv(4.0)
    wr = cT - c2; wi = sT - s2
    # w' = -sinT + 2 sin2T  + i(cosT - 2 cos2T)
    dwr = -sT + two * s2
    dwi = cT - two * c2
    # w'' = -cosT + 4 cos2T + i(-sinT + 4 sin2T)
    ddwr = -cT + four * c2
    ddwi = -sT + four * s2
    return (wr, wi), (dwr, dwi), (ddwr, ddwi)


def _padiv(v):
    """Tiny interval around a float trig value to absorb libm rounding (a few ULP)."""
    lo = v; hi = v
    for _ in range(4):
        lo = F._down(lo); hi = F._up(hi)
    return Iv(lo, hi)


def w_derivs_point(t):
    """w, w', w'' as small intervals around the TRUE values at t.  We enclose
    cos/sin(t),(2t) with a few-ULP pad so rho_m, rho'_m below are rigorous."""
    cT = _padiv(math.cos(t)); sT = _padiv(math.sin(t))
    c2 = _padiv(math.cos(2 * t)); s2 = _padiv(math.sin(2 * t))
    two = Iv(2.0); four = Iv(4.0)
    wr = cT - c2; wi = sT - s2
    dwr = -sT + two * s2; dwi = cT - two * c2
    ddwr = -cT + four * c2; ddwi = -sT + four * s2
    return (wr, wi), (dwr, dwi), (ddwr, ddwi)


def poly_derivs(asc, wr, wi):
    """Q(w), Q'(w), Q''(w) as complex intervals; Horner with integer coeffs."""
    qr = Iv(0.0); qi = Iv(0.0)
    dqr = Iv(0.0); dqi = Iv(0.0)
    ddqr = Iv(0.0); ddqi = Iv(0.0)
    for a in reversed(asc):
        # ddq = ddq*w + 2*dq
        nr, ni = F.cmul(ddqr, ddqi, wr, wi)
        ddqr = nr + dqr + dqr
        ddqi = ni + dqi + dqi
        # dq = dq*w + q
        nr, ni = F.cmul(dqr, dqi, wr, wi)
        dqr = nr + qr; dqi = ni + qi
        # q = q*w + a
        nr, ni = F.cmul(qr, qi, wr, wi)
        qr = nr.add_const(int(a)); qi = ni
    return (qr, qi), (dqr, dqi), (ddqr, ddqi)


def rho_point(asc, wpt):
    """rho=|Q(w_m)|^2 and rho'=2Re(conj(Q)Q' w') at midpoint, as intervals."""
    (wr, wi), (dwr, dwi), _ = wpt
    (qr, qi), (dqr, dqi), _ = poly_derivs(asc, wr, wi)
    rho = qr * qr + qi * qi
    # u' = Q' * w'
    upr, upi = F.cmul(dqr, dqi, dwr, dwi)
    # rho' = 2 Re(conj(Q) u') = 2(qr*upr + qi*upi)
    drho = (qr * upr + qi * upi).scale_pos(2)
    return rho, drho


def rho_dd_cell(asc, wcell):
    """Enclosure of rho''(t) over the cell."""
    (wr, wi), (dwr, dwi), (ddwr, ddwi) = wcell
    (qr, qi), (dqr, dqi), (ddqr, ddqi) = poly_derivs(asc, wr, wi)
    # u' = Q' w'
    upr, upi = F.cmul(dqr, dqi, dwr, dwi)
    # u'' = Q'' w'^2 + Q' w''
    w2r, w2i = F.cmul(dwr, dwi, dwr, dwi)
    a1r, a1i = F.cmul(ddqr, ddqi, w2r, w2i)
    a2r, a2i = F.cmul(dqr, dqi, ddwr, ddwi)
    uppr = a1r + a2r; uppi = a1i + a2i
    # rho'' = 2(|u'|^2 + Re(conj(u) u''))
    upmag2 = upr * upr + upi * upi
    re_conj = qr * uppr + qi * uppi
    return (upmag2 + re_conj).scale_pos(2)


def lower_bound_g(a, b, table):
    m = 0.5 * (a + b)
    r = 0.5 * (b - a)
    s_lin = Iv(-r, r)
    s_sq = Iv(0.0, F._up(r * r))
    wcell = w_derivs_cell(a, b)
    wpt = w_derivs_point(m)

    # sigma = log max(1,|w|): lower bound
    (wr, wi), _, _ = wcell
    w2 = wr * wr + wi * wi
    w2lo = w2.lo
    if w2lo <= 1.0:
        sigma_lo = 0.0
    else:
        sigma_lo = F._down(0.5 * F.log_down(w2lo))

    total_lo = sigma_lo
    for c, asc in table:
        rho_m, drho_m = rho_point(asc, wpt)
        Rpp = rho_dd_cell(asc, wcell)
        # U2 = rho_m + drho_m*[-r,r] + 0.5*Rpp*[0,r^2]
        half = Iv(0.5)
        U2 = rho_m + drho_m * s_lin + half * Rpp * s_sq
        U2hi = U2.hi
        if U2hi <= 0:
            return None
        logU = F.log_up(U2hi)            # rigorous: logU >= log(U2hi) >= log|Q_j|^2...
        # We have |Q_j|^2 <= U2hi, so log|Q_j| <= 0.5*logU.  Need an UPPER bound
        # of 0.5*c_j*logU to subtract (gives a valid LOWER bound of -c_j log|Q_j|).
        # 0.5*c is an exact-ish positive float; build the product with each step
        # rounded UP (toward +inf) so the result >= the exact 0.5*c_j*logU.
        # (logU may be negative when |Q_j|<1; outward rounding toward +inf still
        #  yields a valid upper bound of the signed product.)
        hc_up = F._up(0.5 * c)           # >= 0.5*c_j
        hc_dn = F._down(0.5 * c)         # <= 0.5*c_j
        if logU >= 0:
            contrib_up = F._up(hc_up * logU)     # upper bound of (0.5 c)*logU
        else:
            contrib_up = F._up(hc_dn * logU)     # negative product: smallest 0.5c
        total_lo = F._down(total_lo - contrib_up)
    return total_lo


def certify(table, target, init_intervals=3000, max_depth=80):
    import math as _m
    lo0 = 0.0
    hi0 = _m.pi
    step = (hi0 - lo0) / init_intervals
    stack = [(lo0 + i * step, lo0 + (i + 1) * step, 0) for i in range(init_intervals)]
    # ensure last endpoint exactly pi
    stack[-1] = (stack[-1][0], hi0, 0)
    worst = float("inf")
    n_cells = 0
    depth_used = 0
    _t0 = time.time()
    while stack:
        a, b, d = stack.pop()
        n_cells += 1
        if d > depth_used:
            depth_used = d
        if n_cells % 50000 == 0:
            print(f"   ... {n_cells} cells, stack={len(stack)}, "
                  f"front t~{a:.4f}, depth {d}, {time.time()-_t0:.0f}s", flush=True)
        L = lower_bound_g(a, b, table)
        if L is None or L < target:
            if d >= max_depth:
                return (False, L, n_cells, depth_used, (a, b))
            mid = 0.5 * (a + b)
            stack.append((a, mid, d + 1))
            stack.append((mid, b, d + 1))
        else:
            if L < worst:
                worst = L
    return (True, worst, n_cells, depth_used, None)


def main():
    table = get_table()
    for j, (c, asc) in enumerate(table, 1):
        assert all(isinstance(x, int) for x in asc), f"Q_{j} not integer!"
        assert c > 0, f"c_{j} not positive!"
    print(f"[OK] {len(table)} polynomials Q_j: all INTEGER coefficients, all c_j > 0.")
    print(f"[..] TARGET = {TARGET} (registry verified record 0.24874).")
    print(f"[..] fast interval mean-value branch-and-bound on t in [0, pi] ...")
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


if __name__ == "__main__":
    sys.exit(main())
