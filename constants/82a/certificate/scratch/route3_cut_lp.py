"""
ROUTE 3 — the cut LP and the global-min validity check.

Supergradient of J at mu0:
  V_mu0(y) = INT INT INT log|y - x2 - x3 + x4| dmu0(x2)dmu0(x3)dmu0(x4)   (3-fold potential)
  dJ/dmu (y) = 4 V_mu0(y).
If J is concave in mu (log-energy of the difference measure; OSS eq.6 gives the
2-point case is concave; the 4-point form J(mu)=INT log|s1+s2| drho drho with
rho=rho(mu) is NOT obviously concave in mu -- but for the CUT we only need a VALID
OUTER linear relaxation. We test the tangent cut numerically and, crucially, the
TRUE GLOBAL MIN of the resulting auxiliary f over C.)

Tangent (assuming concavity): J(mu) <= L(mu) := 4 INT V_mu0 dmu - 3 J(mu0).
Cut added to Flammang primal:  L(p) >= 0, i.e. (4 V_mu0(z_n) - 3 J(mu0)/... ) ...
Row r_n = 4 V_mu0(z_n); rhs = 3 J(mu0).  (sum_n p_n r_n >= 3 J(mu0).)

We compute V_mu0(y) by FFT: distribution of (-x2-x3+x4) = S3 is conv(Mref,Mref,M)
(reflection for x2,x3; plus for x4). Then V_mu0(y) = INT log|y + s| dP3(s),
P3 = distribution of S3' where y - x2 - x3 + x4 = y + (x4 - x2 - x3). Let
S3 = x4 - x2 - x3 distribution = conv(M, Mref, Mref). V(y)=INT log|y+s| dP3? No:
y - x2 - x3 + x4 = y + (x4 - x2 - x3), s = x4-x2-x3. V(y) = INT log|y+s| dS3(s).
Evaluate at the contour nodes y=z_n (and at 1-z_n for the global-min scan).
"""
import numpy as np
from scipy.signal import fftconvolve
from scipy.optimize import linprog
from flammang_table1 import get_table
from scratch.route3_J_fft import (contour, column_matrix, solve_primal,
                                   diffuse_from_p0, conj_sym, zz_sym, hist_measure,
                                   J_from_measure)

ANCHOR = 0.2487458


def S3_distribution(pts, masses, G, pad=1.2):
    """Distribution of S3 = x4 - x2 - x3 (x's iid ~ mu): conv(M, Mref, Mref).
    Returns P3 grid, cell size h, and index c0 of S3=0."""
    R = np.abs(pts).max() * pad
    M, h = hist_measure(pts, masses, -R, R, G)
    Mref = M[::-1, ::-1].copy()
    P3 = fftconvolve(fftconvolve(M, Mref, mode='full'), Mref, mode='full')
    P3[P3 < 0] = 0.0
    nP = P3.shape[0]
    # M centered: index G-1 ~ value 0. conv of 3 -> 3*(G-1) is the S=0 index.
    c0 = 3 * (G - 1)
    return P3, h, c0


def V_potential(y_eval, P3, h, c0):
    """V(y) = INT log|y + s| dP3(s), s on the P3 grid.
    Sum over occupied P3 cells. y_eval: array of complex eval points."""
    nP = P3.shape[0]
    idx = np.arange(nP) - c0
    IX, IY = np.meshgrid(idx, idx, indexing='ij')
    SX = (IX * h).ravel()
    SY = (IY * h).ravel()
    P = P3.ravel()
    occ = P > P.max() * 1e-9
    sx = SX[occ]; sy = SY[occ]; pw = P[occ]
    s = sx + 1j * sy
    y = np.asarray(y_eval)
    V = np.empty(len(y))
    # chunk over eval points
    for i in range(0, len(y), 256):
        yc = y[i:i + 256]
        d = np.abs(yc[:, None] + s[None, :])
        with np.errstate(divide='ignore'):
            Lg = np.log(d)
        Lg[~np.isfinite(Lg)] = 0.0
        V[i:i + 256] = Lg @ pw
    return V


def solve_with_cut(g, A, cut_row, rhs):
    N = len(g); J = A.shape[1]
    Aub = np.vstack([-A.T, -cut_row[None, :]])
    bub = np.concatenate([np.zeros(J), [-rhs]])
    res = linprog(g, A_ub=Aub, b_ub=bub, A_eq=np.ones((1, N)), b_eq=np.array([1.0]),
                  bounds=[(0, None)] * N, method="highs")
    marg = res.ineqlin.marginals
    lam = max(-marg[-1], 0.0)
    cj = np.maximum(-marg[:J], 0.0)
    return res.fun, res.x, lam, cj


if __name__ == "__main__":
    N = 2000
    t, z, w, g = contour(N)
    A = column_matrix(w)
    m0, p0 = solve_primal(g, A)
    print(f"no-energy m0 = {m0:.7f}  (anchor {ANCHOR})\n")

    G = 512
    # Use the z->1-z SYMMETRIC diffuse reference (the valid one).
    th, mh = diffuse_from_p0(t, p0, 55, 8)
    zfA, mfA = conj_sym(th, mh)
    pts, ms = zz_sym(zfA, mfA)               # conj + z->1-z symmetric mu0

    J0 = J_from_measure(pts, ms, G=G)
    print(f"J(mu0) [z->1-z symmetric] = {J0:+.6f}")

    P3, h, c0 = S3_distribution(pts, ms, G)
    # cut row at contour nodes y=z_n
    Vz = V_potential(z, P3, h, c0)
    cut_row = 4.0 * Vz
    rhs = 3.0 * J0
    # sanity: cut_row . p0 should ~ 4 J(mu0) (since INT V dmu0 = J0)
    print(f"  check INT V dmu0 ~ J0: (cut_row.p0)/4 = {(cut_row @ p0)/4:+.6f}  vs J0 {J0:+.6f}")

    m_cut, p_cut, lam, cj = solve_with_cut(g, A, cut_row, rhs)
    print(f"\n  m_cut = {m_cut:.7f}   lambda0 = {lam:.6f}   raise vs anchor = {m_cut-ANCHOR:+.7f}")
    print(f"  cut active? {'YES' if lam>1e-7 else 'NO (slack -> no gain)'}")

    # ALSO try the asymmetric Flammang-shaped reference (conj-sym only)
    print("\n  --- asymmetric (conj-sym only) reference ---")
    J0a = J_from_measure(zfA, mfA, G=G)
    print(f"  J(mu0) asym = {J0a:+.6f}")
    P3a, ha, c0a = S3_distribution(zfA, mfA, G)
    Vza = V_potential(z, P3a, ha, c0a)
    m_cut_a, p_cut_a, lam_a, _ = solve_with_cut(g, A, 4.0 * Vza, 3.0 * J0a)
    print(f"  m_cut(asym) = {m_cut_a:.7f}  lambda0 = {lam_a:.6f}  raise = {m_cut_a-ANCHOR:+.7f}")
    print(f"  cut active? {'YES' if lam_a>1e-7 else 'NO'}")

    # GLOBAL-MIN scan would only matter if a cut were active; report it anyway for the
    # active case below.
    np.savez('scratch/route3_cut_frozen.npz', pts=pts, ms=ms, J0=J0,
             zfA=zfA, mfA=mfA, J0a=J0a)
