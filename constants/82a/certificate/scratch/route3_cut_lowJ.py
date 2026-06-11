"""
ROUTE 3 — cut LP with a LOW-J reference (so the tangent can actually BIND), plus
the TRUE GLOBAL MIN validity scan over C.

Strategy: a tangent cut at mu0 only bites the no-energy optimum p0 if p0 VIOLATES
4 INT V_mu0 dp >= 3 J(mu0). With the diffuse near-equilibrium mu0 (J(mu0)>0) it did
NOT (huge slack). The min-J search shows symmetric measures with J as low as -0.53.
We:
  1. Find a z->1-z symmetric reference mu0 with J(mu0) <= 0 (descent on q).
  2. Build the tangent cut row r_n = 4 V_mu0(z_n), rhs = 3 J(mu0).
  3. Re-solve the Flammang primal + cut -> m_cut, lambda0.
  4. If lambda0>0 and m_cut>anchor, SCAN the true global min of the auxiliary
     f(z) = log+|z| + log+|1-z| - sum_j c_j log|Q_j(z(1-z))| - lambda0*(4 V_mu0(z) - 3 J0)
     over BOTH circles, the strip, and the bad region near z=1.99+0.16i. Report the
     true global min (the honest bound) vs m_cut.

CRUCIAL CAVEAT (validity): the OSS outer-cut {J>=0} ⊂ {tangent>=0} is valid ONLY if
J is CONCAVE in mu. route3_concavity.py tests that. If J is NOT concave the tangent
is NOT a valid outer relaxation and ANY raise here is SPURIOUS. We still compute the
numbers to see if there is even a numerical raise to chase.
"""
import numpy as np
from scipy.signal import fftconvolve
from scipy.optimize import linprog
from flammang_table1 import get_table
from scratch.route3_J_fft import (contour, column_matrix, solve_primal, hist_measure)

ANCHOR = 0.2487458
Nnode = 40
thN = (np.arange(Nnode) + 0.5) / Nnode * np.pi
zN = np.exp(1j * thN)


def expand_sym(q):
    q = np.maximum(q, 0); q = q / q.sum()
    pts = np.concatenate([zN, np.conj(zN), 1 - zN, 1 - np.conj(zN)])
    ms = np.concatenate([q, q, q, q]) / 4
    return pts, ms


def J_grids(pts, ms, G=384, pad=1.25):
    R = np.abs(pts).max() * pad
    M, h = hist_measure(pts, ms, -R, R, G)
    Mref = M[::-1, ::-1].copy()
    rho = fftconvolve(M, Mref, mode='full'); rho[rho < 0] = 0
    P = fftconvolve(rho, rho, mode='full'); P[P < 0] = 0
    nP = P.shape[0]; c0 = 2 * (G - 1)
    return M, h, P, c0, G


def J_value(P, h, c0):
    nP = P.shape[0]; idx = np.arange(nP) - c0
    IX, IY = np.meshgrid(idx, idx, indexing='ij')
    Ab = np.hypot(IX * h, IY * h)
    with np.errstate(divide='ignore'):
        L = np.log(Ab)
    L[~np.isfinite(L)] = 0.0
    return float((P * L).sum())


def S3_dist(pts, ms, G=384, pad=1.25):
    R = np.abs(pts).max() * pad
    M, h = hist_measure(pts, ms, -R, R, G)
    Mref = M[::-1, ::-1].copy()
    P3 = fftconvolve(fftconvolve(M, Mref, mode='full'), Mref, mode='full')
    P3[P3 < 0] = 0
    c0 = 3 * (G - 1)
    return P3, h, c0


def V_pot(y_eval, P3, h, c0):
    nP = P3.shape[0]; idx = np.arange(nP) - c0
    IX, IY = np.meshgrid(idx, idx, indexing='ij')
    sx = (IX * h).ravel(); sy = (IY * h).ravel(); P = P3.ravel()
    occ = P > P.max() * 1e-9
    s = sx[occ] + 1j * sy[occ]; pw = P[occ]
    y = np.asarray(y_eval); V = np.empty(len(y))
    for i in range(0, len(y), 200):
        yc = y[i:i+200]
        d = np.abs(yc[:, None] + s[None, :])
        with np.errstate(divide='ignore'):
            Lg = np.log(d)
        Lg[~np.isfinite(Lg)] = 0.0
        V[i:i+200] = Lg @ pw
    return V


def descend_lowJ(seed=5, steps=40):
    rng = np.random.default_rng(seed)
    q = rng.dirichlet(np.full(Nnode, 0.3))
    def Jq(q):
        pts, ms = expand_sym(q); _, h, P, c0, _ = J_grids(pts, ms, G=288); return J_value(P, h, c0)
    cur = Jq(q)
    for _ in range(steps):
        eps = 2e-3; grad = np.zeros(Nnode)
        cols = rng.choice(Nnode, 10, replace=False)
        for c in cols:
            qp = q.copy(); qp[c] += eps; grad[c] = (Jq(qp) - cur) / eps
        q = np.maximum(q - 0.4 * grad, 1e-9); q /= q.sum(); cur = Jq(q)
    return q, cur


def solve_with_cut(g, A, cut_row, rhs):
    N = len(g); J = A.shape[1]
    Aub = np.vstack([-A.T, -cut_row[None, :]])
    bub = np.concatenate([np.zeros(J), [-rhs]])
    res = linprog(g, A_ub=Aub, b_ub=bub, A_eq=np.ones((1, N)), b_eq=np.array([1.0]),
                  bounds=[(0, None)] * N, method="highs")
    marg = res.ineqlin.marginals
    lam = max(-marg[-1], 0.0); cj = np.maximum(-marg[:J], 0.0)
    return res.fun, res.x, lam, cj


def global_min_f(cj, lam, P3, h, c0, J0):
    """Scan f over a complex region. f = log+|z|+log+|1-z| - sum cj log|Qj(w)|
       - lam*(4 V_mu0(z) - 3 J0). w=z(1-z)."""
    cols = [asc for (_, asc) in get_table()]
    # grid over a box covering both circles and the bad region
    re = np.linspace(-1.3, 2.3, 360)
    im = np.linspace(-1.3, 1.3, 260)
    RE, IM = np.meshgrid(re, im)
    Z = (RE + 1j * IM).ravel()
    w = Z * (1 - Z)
    f = np.log(np.maximum(1.0, np.abs(Z))) + np.log(np.maximum(1.0, np.abs(1 - Z)))
    for c, asc in zip(cj, cols):
        if c > 0:
            f = f - c * np.log(np.abs(np.polyval(list(reversed(asc)), w)) + 1e-300)
    if lam > 0:
        V = V_pot(Z, P3, h, c0)
        f = f - lam * (4.0 * V - 3.0 * J0)
    fmin = f.min()
    kmin = f.argmin()
    return fmin, Z[kmin]


if __name__ == "__main__":
    N = 2000
    t, z, w, g = contour(N)
    A = column_matrix(w)
    m0, p0 = solve_primal(g, A)
    print(f"no-energy m0 = {m0:.7f}  anchor {ANCHOR}")

    # several low-J references
    for seed in (5, 7, 11):
        q, J0d = descend_lowJ(seed=seed)
        pts, ms = expand_sym(q)
        _, hJ, P, c0J, _ = J_grids(pts, ms, G=384)
        J0 = J_value(P, hJ, c0J)
        P3, h3, c03 = S3_dist(pts, ms, G=384)
        Vz = V_pot(z, P3, h3, c03)
        cut_row = 4.0 * Vz; rhs = 3.0 * J0
        m_cut, p_cut, lam, cj = solve_with_cut(g, A, cut_row, rhs)
        print(f"\nseed {seed}: J(mu0)={J0:+.5f}  m_cut={m_cut:.7f}  lambda0={lam:.5f}  "
              f"raise={m_cut-ANCHOR:+.7f}  cut {'ACTIVE' if lam>1e-7 else 'slack'}")
        if lam > 1e-7 and m_cut - ANCHOR > 1e-6:
            fmin, zmin = global_min_f(cj, lam, P3, h3, c03, J0)
            print(f"   --> TRUE GLOBAL MIN of f over C = {fmin:+.7f} at z={zmin:.4f}")
            print(f"       (LP m_cut={m_cut:.7f}; honest bound = global min = {fmin:.7f})")
            print(f"       beats anchor? {'YES' if fmin>ANCHOR+1e-7 else 'NO -- one-circle artifact'}")
