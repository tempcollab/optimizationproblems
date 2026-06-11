"""
ROUTE 3 — USEFULNESS, the DECISIVE J(mu0) test.

J(mu) = INT^4 log|x1 - x2 - x3 + x4| dmu(x1)dmu(x2)dmu(x3)dmu(x4).

mu lives on the conjugate set, conjugation-symmetric, modeled on the contour
z=e^{it}, t in (0,pi) folded with the conjugate partner.

DECISIVE QUESTION: for a z->1-z SYMMETRIC reference mu0, is J(mu0) ~ 0 (the
2-point energy was ~ -0.012 for symmetric, raise died) or genuinely negative
(slack)?  We compute J(mu0) for:
  - the Flammang no-energy optimum histogram (NOT z->1-z symmetric)
  - a z->1-z symmetrized version
and several reference widths.

We evaluate J on the FULL circle measure (mass p_n at z_n=e^{it_n} and equal mass
at conj). To get the conjugation-symmetric full measure we mirror to t in (-pi,pi).
J is a 4-fold sum: J = sum_{a,b,c,d} p_a p_b p_c p_d log|z_a - z_b - z_c + z_d|.
The diagonal-type zero tuples (z_a-z_b-z_c+z_d=0) are measure-zero in the
continuum but appear in a discrete sum -> we EXCLUDE log(0) entries (set to 0,
i.e. drop the measure-zero diagonal), consistent with the integral.

Because the full 4-fold sum is O(M^4), we evaluate it via FFT/convolution:
let D = z_a - z_b ranges over differences. J = sum over (diff1, diff2) ... but
log|.| is not separable. We instead Monte-Carlo / coarse-grid the 4-fold integral
with a moderate node count and the conj-symmetric structure.

Efficient exact route: J = E_{(a,b,c,d)~mu^4} log|s|, s = (z_a - z_b) + (z_d - z_c).
Let X = z_a - z_b (a,b ~ mu indep) with distribution rho = mu * (-mu) (the
difference measure). Then s = X1 + X2 with X1,X2 ~ rho iid. So
   J = INT INT log|x1 + x2| drho(x1) drho(x2)
i.e. a 2-fold integral against the difference measure rho. rho is supported on a
2D region in C. We discretize rho on a grid (histogram of differences) then do the
2-fold sum -> O(G^2) with G = #grid cells of rho. Much cheaper.
"""
import numpy as np
from scipy.optimize import linprog
from flammang_table1 import get_table

ANCHOR = 0.2487458


def contour(N):
    t = np.linspace(1e-4, np.pi - 1e-4, N)
    z = np.exp(1j * t)
    w = z * (1 - z)
    g = np.log(np.maximum(1.0, np.abs(w)))
    return t, z, w, g


def column_matrix(w):
    cols = [asc for (_, asc) in get_table()]
    A = np.empty((len(w), len(cols)))
    for j, asc in enumerate(cols):
        A[:, j] = np.log(np.abs(np.polyval(list(reversed(asc)), w)))
    return A


def solve_primal(g, A):
    N = len(g); J = A.shape[1]
    Aub = -A.T; bub = np.zeros(J)
    Aeq = np.ones((1, N)); beq = np.array([1.0])
    res = linprog(g, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq,
                  bounds=[(0, None)] * N, method="highs")
    return res.fun, res.x


def full_circle_measure(z_half, p_half):
    """Conjugation-symmetric full-circle measure: mass p/2 at z and p/2 at conj."""
    zf = np.concatenate([z_half, np.conj(z_half)])
    pf = np.concatenate([p_half / 2, p_half / 2])
    return zf, pf


def symmetrize_zz(z_half, p_half):
    """Make the measure z->1-z symmetric AND conjugation symmetric.
    Apply both z->1-z and z->conj. Returns full point set + masses (normalized)."""
    pts = []
    ms = []
    for z, p in zip(z_half, p_half):
        for zz in (z, np.conj(z), 1 - z, 1 - np.conj(z)):
            pts.append(zz); ms.append(p / 4)
    pts = np.array(pts); ms = np.array(ms)
    ms /= ms.sum()
    return pts, ms


def J_of_measure(zf, pf, drop_tol=1e-12):
    """J = sum_{a,b,c,d} p_a p_b p_c p_d log|z_a - z_b - z_c + z_d|, dropping
    the measure-zero exact-zero tuples (log(0)).
    Use difference-measure reduction:
      X = z_a - z_b ~ rho (mass p_a p_b at z_a - z_b)
      J = INT INT log|x1 + x2| drho(x1) drho(x2),  x1=z_a-z_b, x2=z_d-z_c.
    Build rho on the point cloud {z_a - z_b}, then 2-fold sum over rho x rho.
    O(M^4) if naive; we keep M modest (M=len(zf) ~ few hundred)."""
    M = len(zf)
    # difference cloud
    D = (zf[:, None] - zf[None, :]).ravel()          # M^2 points
    W = (pf[:, None] * pf[None, :]).ravel()           # M^2 masses
    # J = sum over (D_i, D_j) of W_i W_j log|D_i + D_j|
    # M^2 can be large -> chunk. With M~200, M^2=40000, (M^2)^2=1.6e9 too big.
    # Reduce: histogram rho onto a coarse complex grid.
    return D, W


def J_via_grid(D, W, ngrid=160):
    """Histogram the difference cloud (D,W) onto an ngrid x ngrid complex grid,
    then 2-fold sum log|c_i + c_j| over occupied cells. Rigorous-ish: the grid
    introduces O(cell) error but reveals SIGN and MAGNITUDE of J."""
    re = D.real; im = D.imag
    r0, r1 = re.min(), re.max()
    i0, i1 = im.min(), im.max()
    eps = 1e-9
    ri = np.clip(((re - r0) / (r1 - r0 + eps) * ngrid).astype(int), 0, ngrid - 1)
    ii = np.clip(((im - i0) / (i1 - i0 + eps) * ngrid).astype(int), 0, ngrid - 1)
    flat = ri * ngrid + ii
    nb = ngrid * ngrid
    massg = np.bincount(flat, weights=W, minlength=nb)
    # cell centers
    rc = r0 + (np.arange(ngrid) + 0.5) / ngrid * (r1 - r0)
    ic = i0 + (np.arange(ngrid) + 0.5) / ngrid * (i1 - i0)
    RC, IC = np.meshgrid(rc, ic, indexing='ij')
    centers = (RC + 1j * IC).ravel()
    occ = massg > 1e-15
    c = centers[occ]; m = massg[occ]
    # 2-fold sum
    S = c[:, None] + c[None, :]
    AbsS = np.abs(S)
    with np.errstate(divide='ignore'):
        L = np.log(AbsS)
    L[~np.isfinite(L)] = 0.0
    J = float(m @ L @ m)
    return J, len(c)


if __name__ == "__main__":
    N = 1500
    t, z, w, g = contour(N)
    A = column_matrix(w)
    m0, p0 = solve_primal(g, A)
    print(f"no-energy m0 = {m0:.7f}  (anchor {ANCHOR})")

    # downsample for the O() difference cloud
    for M in (120, 200):
        idx = np.linspace(0, N - 1, M).astype(int)
        zh = z[idx]; ph = p0[idx]; ph = ph / ph.sum()

        # (1) Flammang optimum (NOT z->1-z symmetric), full circle
        zf, pf = full_circle_measure(zh, ph)
        D, W = J_of_measure(zf, pf)
        Jf, ncell = J_via_grid(D, W)
        print(f"\nM={M}: Flammang-opt (conj-sym only) full-circle: "
              f"J(mu0) = {Jf:+.5f}  (rho cells {ncell})")

        # (2) z->1-z SYMMETRIZED version (the decisive symmetric measure)
        pts, ms = symmetrize_zz(zh, ph)
        D2, W2 = J_of_measure(pts, ms)
        Js, ncell2 = J_via_grid(D2, W2)
        print(f"M={M}: z->1-z SYMMETRIZED measure:            "
              f"J(mu0) = {Js:+.5f}  (rho cells {ncell2})  <-- DECISIVE")
