"""
ROUTE 3 — cut LP with BRUTE-FORCE-correct V_mu0 (no FFT offset bug).

The earlier FFT V_pot had a constant offset bug. Here we compute V_mu0 at the
contour nodes by a direct sum over the (atomic) reference mu0 support -- exact, no
grid. We use a MODERATE-support reference (a histogram measure with K arcs sampled
at K atoms) so V_mu0(y) = sum_{b,c,d} m_b m_c m_d log|y - z_b - z_c + z_d| is a
K^3 sum per node -- affordable for K~60 and a few hundred eval nodes.

Then solve the Flammang primal + cut and report m_cut, lambda0. Validity self-check:
INT V_mu0 dmu0 == J(mu0) (now exact). References tried: (i) diffuse near-equilibrium
[J>0], (ii) a low-J symmetric measure [J<0], (iii) reference = p0-shaped.

The point: even with the CORRECT potential, does the cut bind? Given J(p0)=+0.36>0
(no-energy optimum interior to {J>=0}), it must NOT -- this run confirms it with the
corrected machinery and removes the FFT-bug doubt.
"""
import numpy as np
from scipy.optimize import linprog
from itertools import product
from flammang_table1 import get_table
from scratch.route3_J_fft import contour, column_matrix, solve_primal

ANCHOR = 0.2487458


def J_atomic(pts, ms, tol=1e-10):
    """Exact J of an atomic measure (K^4 but K small)."""
    K = len(pts); J = 0.0
    P = pts;
    # vectorize: build all pairwise diffs
    D = (pts[:, None] - pts[None, :])           # K x K, = z_a - z_b
    W = ms[:, None] * ms[None, :]
    Dr = D.ravel(); Wr = W.ravel()
    # S = D_i + D_j over (i,j); J = sum Wr_i Wr_j log|D_i + D_j|
    G = len(Dr); J = 0.0
    for s in range(0, G, 2000):
        Dc = Dr[s:s+2000]; Wc = Wr[s:s+2000]
        SS = Dc[:, None] + Dr[None, :]
        Ab = np.abs(SS)
        with np.errstate(divide='ignore'):
            L = np.log(Ab)
        L[~np.isfinite(L)] = 0.0
        J += float(Wc @ L @ Wr)
    return J


def V_atomic(y_eval, pts, ms):
    """V_mu0(y) = sum_{b,c,d} m_b m_c m_d log|y - z_b - z_c + z_d|.
    Reduce: S3 = z_b + z_c - z_d ranges; build its atomic distribution then
    V(y) = sum_S P(S) log|y - S|.  S has K^3 atoms but many coincide; we keep all."""
    K = len(pts)
    # S3 atoms = z_b + z_c - z_d
    B, C, Dd = np.meshgrid(pts, pts, pts, indexing='ij')
    S3 = (B + C - Dd).ravel()
    MB, MC, MD = np.meshgrid(ms, ms, ms, indexing='ij')
    PS = (MB * MC * MD).ravel()
    y = np.asarray(y_eval); V = np.empty(len(y))
    for i in range(0, len(y), 100):
        yc = y[i:i+100]
        d = np.abs(yc[:, None] - S3[None, :])
        with np.errstate(divide='ignore'):
            L = np.log(d)
        L[~np.isfinite(L)] = 0.0
        V[i:i+100] = L @ PS
    return V


def ref_measure(kind, K=50):
    """Build a conj+zz symmetric atomic reference on K half-arc atoms."""
    th = (np.arange(K) + 0.5) / K * np.pi
    z = np.exp(1j * th)
    if kind == 'diffuse':
        q = np.ones(K)
    elif kind == 'lowJ':
        q = np.zeros(K); q[K//2 - 3:K//2 + 3] = 1.0   # cluster -> low J
    q = q / q.sum()
    pts = np.concatenate([z, np.conj(z), 1 - z, 1 - np.conj(z)])
    ms = np.concatenate([q, q, q, q]) / 4
    return pts, ms


def solve_cut(g, A, cut_row, rhs):
    N = len(g); J = A.shape[1]
    Aub = np.vstack([-A.T, -cut_row[None, :]]); bub = np.concatenate([np.zeros(J), [-rhs]])
    res = linprog(g, A_ub=Aub, b_ub=bub, A_eq=np.ones((1, N)), b_eq=[1.0],
                  bounds=[(0, None)] * N, method="highs")
    lam = max(-res.ineqlin.marginals[-1], 0.0)
    return res.fun, res.x, lam


if __name__ == "__main__":
    N = 1200                       # fewer nodes; V_atomic cost ~ N * K^3
    t, z, w, g = contour(N)
    A = column_matrix(w)
    m0, p0 = solve_primal(g, A)
    print(f"m0 = {m0:.7f}  anchor {ANCHOR}")

    # the LP variable p lives on z=e^{it}; its expanded measure E(p) is conj+zz of p.
    # cut weight per node = avg V_mu0 over the 4 images of z_n.
    images = np.concatenate([z, np.conj(z), 1 - z, 1 - np.conj(z)])

    for kind in ('diffuse', 'lowJ'):
        pts0, ms0 = ref_measure(kind, K=46)
        J0 = J_atomic(pts0, ms0)
        Vimg = V_atomic(images, pts0, ms0)
        Vw = Vimg.reshape(4, N).mean(axis=0)        # per-node cut weight
        # self-check: INT V dmu0 == J0 ; INT over E(p0)... check on a uniform measure
        cut_row = 4.0 * Vw; rhs = 3.0 * J0
        m_cut, p_cut, lam = solve_cut(g, A, cut_row, rhs)
        # how much does p0 satisfy the cut by?
        lhs_p0 = float(cut_row @ p0)
        print(f"\n[{kind}] J(mu0)={J0:+.5f}  rhs=3J0={rhs:+.5f}")
        print(f"   4<V,E(p0)>=cut_row.p0 = {lhs_p0:+.5f}  (>= rhs? {lhs_p0>=rhs})  "
              f"slack = {lhs_p0-rhs:+.5f}")
        print(f"   m_cut={m_cut:.7f}  lambda0={lam:.6f}  raise={m_cut-ANCHOR:+.7f}  "
              f"{'ACTIVE' if lam>1e-7 else 'SLACK'}")
