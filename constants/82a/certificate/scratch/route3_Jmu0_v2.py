"""
ROUTE 3 — DECISIVE J(mu0), v2.  Use a DIFFUSE histogram reference (like
freeze_energy.py), NOT the sparse atomic LP optimum. Compute J on a fine
node-cloud directly with the difference-measure reduction:

  J = INT INT log|x1 + x2| drho drho,   rho = mu0 *(- mu0)  (difference measure)

rho lives on the cloud {z_a - z_b}. We DON'T grid (that lost accuracy); instead
we keep the full difference cloud but compute the 2-fold sum in CHUNKS to control
memory. With M diffuse nodes, the cloud has M^2 points; the 2-fold sum is
(M^2)^2 = M^4 ops. We keep M ~ 90..150 so M^4 ~ 1e8..5e8 (feasible in chunks),
and drop only the EXACT zero tuples (log(0), measure-zero diagonal).

Reference measures (all conjugation-symmetric, diffuse uniform density on arcs):
  (A) Flammang-shaped: density ~ the no-energy optimum, but SMOOTHED to a diffuse
      histogram (bin the sparse p0 into B bins, uniform within bin) -> NOT z->1-z sym.
  (B) z->1-z SYMMETRIC diffuse: take (A) and average with its z->1-z image.
  (C) the two-circle equilibrium-like symmetric measure (uniform in t on (0,pi)),
      conj+ z->1-z symmetrized -- a clean symmetric reference.

The DECISIVE number is J for the SYMMETRIC references (B),(C): if ~0 -> Route 3
dies like the 2-point case; if meaningfully NEGATIVE -> slack.
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


def diffuse_from_p0(t, p0, B, nper):
    """Bin p0 into B uniform t-bins; within each occupied bin lay down `nper`
    uniform nodes carrying equal share of the bin mass. Returns half-arc nodes
    t_nodes (in (0,pi)) and masses (sum=1)."""
    edges = np.linspace(0, np.pi, B + 1)
    Lbin = edges[1] - edges[0]
    idx = np.clip(np.searchsorted(edges, t) - 1, 0, B - 1)
    binmass = np.zeros(B)
    for i, m in zip(idx, p0):
        binmass[i] += m
    binmass /= binmass.sum()
    tn = []; mn = []
    centers = 0.5 * (edges[:-1] + edges[1:])
    sub = (np.arange(nper) + 0.5) / nper * Lbin - Lbin / 2
    for b in range(B):
        if binmass[b] > 1e-13:
            tn.append(centers[b] + sub)
            mn.append(np.full(nper, binmass[b] / nper))
    return np.concatenate(tn), np.concatenate(mn)


def full_conj(t_half, m_half):
    """Conjugation-symmetric full-circle node cloud: z=e^{it} and conj=e^{-it}."""
    z = np.exp(1j * t_half)
    zf = np.concatenate([z, np.conj(z)])
    mf = np.concatenate([m_half / 2, m_half / 2])
    return zf, mf


def zz_symmetrize(zf, mf):
    """Add z->1-z images, renormalize -> conj AND z->1-z symmetric."""
    pts = np.concatenate([zf, 1 - zf])
    ms = np.concatenate([mf / 2, mf / 2])
    return pts, ms


def J_diffcloud(zf, mf, chunk=4000):
    """J = sum log|x1+x2| over rho x rho, rho=(z_a-z_b, m_a m_b). Drop exact zeros.
    Chunked over rho points to bound memory."""
    D = (zf[:, None] - zf[None, :]).ravel()
    W = (mf[:, None] * mf[None, :]).ravel()
    # prune negligible-weight diff points to shrink the cloud
    keep = W > (W.max() * 1e-10)
    D = D[keep]; W = W[keep]
    G = len(D)
    J = 0.0
    for s in range(0, G, chunk):
        Dc = D[s:s + chunk]; Wc = W[s:s + chunk]
        S = Dc[:, None] + D[None, :]
        Ab = np.abs(S)
        with np.errstate(divide='ignore'):
            L = np.log(Ab)
        L[~np.isfinite(L)] = 0.0
        J += float(Wc @ L @ W)
    return J, G


if __name__ == "__main__":
    N = 2000
    t, z, w, g = contour(N)
    A = column_matrix(w)
    m0, p0 = solve_primal(g, A)
    print(f"no-energy m0 = {m0:.7f}  (anchor {ANCHOR})\n")

    for B, nper in [(40, 4), (55, 4), (40, 6)]:
        th, mh = diffuse_from_p0(t, p0, B, nper)
        Mhalf = len(th)
        # (A) Flammang-shaped, conj-sym only
        zfA, mfA = full_conj(th, mh)
        JA, GA = J_diffcloud(zfA, mfA)
        # (B) z->1-z symmetrized
        zfB, mfB = zz_symmetrize(zfA, mfA)
        JB, GB = J_diffcloud(zfB, mfB)
        print(f"B={B} nper={nper}  (half-nodes {Mhalf})")
        print(f"   (A) Flammang-shaped conj-sym : J(mu0) = {JA:+.6f}  (cloud {GA})")
        print(f"   (B) z->1-z SYMMETRIZED       : J(mu0) = {JB:+.6f}  (cloud {GB})  <-- DECISIVE")

    # (C) clean symmetric reference: uniform-in-t density on (0,pi)
    print("\n(C) uniform-in-t symmetric reference:")
    for M in (100, 160):
        th = (np.arange(M) + 0.5) / M * np.pi
        mh = np.full(M, 1.0 / M)
        zfC, mfC = full_conj(th, mh)
        zfC, mfC = zz_symmetrize(zfC, mfC)
        JC, GC = J_diffcloud(zfC, mfC)
        print(f"   M={M}: J(mu0) = {JC:+.6f}  (cloud {GC})")
