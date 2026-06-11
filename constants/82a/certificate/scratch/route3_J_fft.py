"""
ROUTE 3 — DECISIVE J(mu0), FFT version (fast, well-resolved).

J(mu) = INT INT log|x1 - x2 - x3 + x4| dmu^4
      = INT INT log|s1 + s2| drho(s1) drho(s2),   rho = difference measure of mu
      = INT log|S| d(rho ⊛ rho)(S),  ⊛ = additive convolution.

So: (1) histogram rho onto a complex grid, (2) FFT-convolve rho with itself to get
the distribution of S = s1+s2, (3) integrate log|S| against it. O(G log G).

rho itself is the additive convolution mu ⊛ (-mu) (difference of two mu draws).
So actually S = (x1-x2)+(x4-x3) = x1 - x2 - x3 + x4, and the distribution of S is
mu ⊛ (-mu) ⊛ mu ⊛ (-mu) = |mu ⊛ (-mu)|... = the 4-fold sum distribution. We can get
it in ONE shot: hist mu -> M(k) on grid; hist(-mu) is M reflected; convolve all four.
Distribution of S = conv(M, Mref, M, Mref) where Mref(k)=M(-k).

J = sum_S P(S) log|S|, dropping S=0 (measure-zero).

We compare reference measures mu0:
  (A) Flammang-shaped diffuse (conj-sym), NOT z->1-z sym
  (B) z->1-z symmetrized (conj + z->1-z): the DECISIVE symmetric reference
  (C) uniform-in-t symmetric reference
and several grid resolutions to confirm convergence / sign.
"""
import numpy as np
from scipy.signal import fftconvolve
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
    res = linprog(g, A_ub=-A.T, b_ub=np.zeros(J),
                  A_eq=np.ones((1, N)), b_eq=np.array([1.0]),
                  bounds=[(0, None)] * N, method="highs")
    return res.fun, res.x


def hist_measure(pts, masses, gmin, gmax, G):
    """Histogram complex point masses onto a G x G grid spanning [gmin,gmax]^2
    in (Re, Im). Returns 2D array M[ri, ii] of masses and the cell size h."""
    h = (gmax - gmin) / G
    ri = np.clip(((pts.real - gmin) / h).astype(int), 0, G - 1)
    ii = np.clip(((pts.imag - gmin) / h).astype(int), 0, G - 1)
    M = np.zeros((G, G))
    np.add.at(M, (ri, ii), masses)
    return M, h


def J_from_measure(pts, masses, G=512, pad=1.2):
    """Distribution of S=x1-x2-x3+x4 via 4-fold conv of M and its reflection.
    Then J = sum P(S) log|S| over the S-grid, dropping S=0."""
    # symmetric grid for mu, centered at 0 enough to hold all of pts
    R = np.abs(pts).max() * pad
    gmin, gmax = -R, R
    M, h = hist_measure(pts, masses, gmin, gmax, G)
    Mref = M[::-1, ::-1].copy()        # reflection -> measure of (-x)
    # conv of two => distribution of (x_a - x_b): conv(M, Mref)
    rho = fftconvolve(M, Mref, mode='full')          # support [-2R,2R], grid 2G-1
    rho[rho < 0] = 0.0                                # clip tiny negatives
    # S = (x1-x2) + (x4-x3): conv(rho, rho)
    P = fftconvolve(rho, rho, mode='full')           # 4G-3 grid
    P[P < 0] = 0.0
    # S-grid: rho spans index shift; full conv of M (G) and Mref (G) -> size 2G-1,
    # cell center at (idx)*h + (gmin*2)?  Build coordinate of conv-of-conv.
    # Easier: rho lives on grid of size (2G-1) with cell h, origin at index (G-1)
    # corresponds to S=0 (since reflection centered). Then P size 2*(2G-1)-1=4G-3,
    # origin (S=0) at index 2*(G-1).
    nP = P.shape[0]
    c0 = 2 * (G - 1)                                   # index of S=0 along each axis
    idx = np.arange(nP) - c0
    SX = idx[:, None] * h
    SY = idx[None, :] * h
    AbsS = np.hypot(SX, SY)
    with np.errstate(divide='ignore'):
        L = np.log(AbsS)
    L[~np.isfinite(L)] = 0.0          # drop S=0 (measure zero)
    J = float((P * L).sum())
    return J


# measure builders -----------------------------------------------------------

def diffuse_from_p0(t, p0, B, nper):
    edges = np.linspace(0, np.pi, B + 1)
    Lbin = edges[1] - edges[0]
    idx = np.clip(np.searchsorted(edges, t) - 1, 0, B - 1)
    binmass = np.zeros(B)
    for i, m in zip(idx, p0):
        binmass[i] += m
    binmass /= binmass.sum()
    centers = 0.5 * (edges[:-1] + edges[1:])
    sub = (np.arange(nper) + 0.5) / nper * Lbin - Lbin / 2
    tn, mn = [], []
    for b in range(B):
        if binmass[b] > 1e-13:
            tn.append(centers[b] + sub); mn.append(np.full(nper, binmass[b] / nper))
    return np.concatenate(tn), np.concatenate(mn)


def conj_sym(t_half, m_half):
    z = np.exp(1j * t_half)
    return np.concatenate([z, np.conj(z)]), np.concatenate([m_half / 2, m_half / 2])


def zz_sym(pts, masses):
    return np.concatenate([pts, 1 - pts]), np.concatenate([masses / 2, masses / 2])


if __name__ == "__main__":
    N = 2000
    t, z, w, g = contour(N)
    A = column_matrix(w)
    m0, p0 = solve_primal(g, A)
    print(f"no-energy m0 = {m0:.7f}  (anchor {ANCHOR})\n")

    print("Grid-convergence of J for each reference (G = grid per axis):")
    for B, nper in [(45, 6), (55, 8)]:
        th, mh = diffuse_from_p0(t, p0, B, nper)
        zfA, mfA = conj_sym(th, mh)
        ptsB, msB = zz_sym(zfA, mfA)
        print(f"\n  Flammang-shaped (B={B},nper={nper}):")
        for G in (384, 512, 768):
            JA = J_from_measure(zfA, mfA, G=G)
            print(f"    (A) conj-sym only       G={G}: J = {JA:+.5f}")
        print(f"  z->1-z SYMMETRIZED:")
        for G in (384, 512, 768):
            JB = J_from_measure(ptsB, msB, G=G)
            print(f"    (B) z->1-z symmetric    G={G}: J = {JB:+.5f}   <-- DECISIVE")

    print("\n  (C) uniform-in-t symmetric reference:")
    for M in (120, 200):
        th = (np.arange(M) + 0.5) / M * np.pi
        mh = np.full(M, 1.0 / M)
        zfC, mfC = conj_sym(th, mh)
        ptsC, msC = zz_sym(zfC, mfC)
        for G in (512, 768):
            JC = J_from_measure(ptsC, msC, G=G)
            print(f"    M={M} G={G}: J = {JC:+.5f}")
