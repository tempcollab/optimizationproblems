"""
NO-GO / balanced signed-sum hierarchy — THE KEY TEST.

For a BALANCED sign vector s of length k=2n, the linear form sum_i s_i x_i can be
grouped (pair each +1 with a -1) into n difference variables:
    S = (x_{a1}-x_{b1}) + ... + (x_{an}-x_{bn}),
all x's iid ~ mu. So the distribution of S is

    P_S = rho^{*n},   rho = mu ⊛ (-mu)   (difference measure of mu),

an n-fold additive convolution. Then

    C_{Q_S}(mu) = INT log|S| dP_S(S).

Because every balanced sign pattern of the same length k yields the SAME S-distribution
(it's always n iid difference draws), C_{Q_S}(mu) depends ONLY on n=k/2, NOT on the
particular sign assignment. (Confirmed independently in nogo_validity.py: all sign
patterns gave identical J.)

We compute C_n(mu) := INT log|S| d(rho^{*n}) for n=1,2,3,4 (k=2,4,6,8) via FFT:
  M  = histogram of mu on a complex grid,
  Mr = reflected M  (measure of -x),
  rho = fftconvolve(M, Mr),         # distribution of one difference
  P_S = rho convolved with itself n-1 more times (n total difference draws),
  C_n = sum_S P_S log|S|  (drop S=0, measure zero).

Reference measures mu0 (all conjugation-symmetric; we report both conj-only and the
DECISIVE z->1-z symmetrized version):
  (A) Flammang no-energy LP optimum p0 (conj-sym; NOT z->1-z sym),
  (B) p0 symmetrized under z->1-z  (the valid symmetric reference),
  (C) uniform-in-t symmetric reference,
  (D) a few other diffuse symmetric histograms (concentrated / spread / bimodal).

THE CONJECTURE: C_n(mu0) >= 0 for EVERY n and EVERY z->1-z symmetric mu0
(=> Flammang optimum is interior to {C_{Q_S}>=0}, cut can't bind).
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


def hist_measure(pts, masses, R, G):
    """Histogram complex point masses onto a G x G grid spanning [-R,R]^2."""
    h = (2 * R) / G
    ri = np.clip(((pts.real + R) / h).astype(int), 0, G - 1)
    ii = np.clip(((pts.imag + R) / h).astype(int), 0, G - 1)
    M = np.zeros((G, G))
    np.add.at(M, (ri, ii), masses)
    return M, h


def C_n_from_measure(pts, masses, n, G=384, pad=1.15):
    """C_n(mu) = INT log|S| d(rho^{*n}),  rho = mu ⊛ (-mu).
    Returns C_n for the given n via FFT convolutions."""
    R = np.abs(pts).max() * pad
    M, h = hist_measure(pts, masses, R, G)
    Mr = M[::-1, ::-1].copy()              # measure of -x
    rho = fftconvolve(M, Mr, mode='full')  # size (2G-1)^2; S=0 at index (G-1)
    rho[rho < 0] = 0.0
    # n-fold convolution of rho
    P = rho.copy()
    for _ in range(n - 1):
        P = fftconvolve(P, rho, mode='full')
        P[P < 0] = 0.0
    # locate S=0 index. rho origin (S=0) at index (G-1). After (n-1) more convs of
    # size-(2G-1) arrays, origin shifts to (G-1)*n.
    c0 = (G - 1) * n
    nP = P.shape[0]
    idx = np.arange(nP) - c0
    SX = idx[:, None] * h
    SY = idx[None, :] * h
    AbsS = np.hypot(SX, SY)
    with np.errstate(divide='ignore'):
        L = np.log(AbsS)
    L[~np.isfinite(L)] = 0.0
    return float((P * L).sum())


# ---- measure builders -------------------------------------------------------

def diffuse_from_p0(t, p0, B, nper):
    """Re-bin p0 into B arcs, spread each arc over nper sub-points (diffuse)."""
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
    """z -> 1-z symmetrize."""
    return np.concatenate([pts, 1 - pts]), np.concatenate([masses / 2, masses / 2])


def uniform_t_sym(M):
    th = (np.arange(M) + 0.5) / M * np.pi
    mh = np.full(M, 1.0 / M)
    z, m = conj_sym(th, mh)
    return zz_sym(z, m)


def shaped_t_sym(M, kind):
    th = (np.arange(M) + 0.5) / M * np.pi
    if kind == 'concentrated':       # mass near t=pi/2 (top of circle)
        q = np.exp(-((th - np.pi / 2) ** 2) / (2 * 0.25 ** 2))
    elif kind == 'spread':           # mass at the two ends t->0, t->pi
        q = np.exp(-((th - 0.3) ** 2) / 0.05) + np.exp(-((th - (np.pi - 0.3)) ** 2) / 0.05)
    elif kind == 'bimodal':          # two lumps
        q = np.exp(-((th - 0.9) ** 2) / 0.08) + np.exp(-((th - 2.2) ** 2) / 0.08)
    elif kind == 'flammang_like':    # peaked near small t (Flammang opt shape)
        q = np.exp(-((th - 0.55) ** 2) / 0.06)
        q += 0.3 * np.exp(-((th - (np.pi - 0.55)) ** 2) / 0.06)  # z->1-z mirror
    else:
        q = np.ones(M)
    q /= q.sum()
    z, m = conj_sym(th, q)
    return zz_sym(z, m)


if __name__ == "__main__":
    N = 2000
    t, z, w, g = contour(N)
    A = column_matrix(w)
    m0, p0 = solve_primal(g, A)
    print(f"no-energy LP m0 = {m0:.7f}  (Flammang anchor {ANCHOR})\n")

    NS = (1, 2, 3, 4)   # n = k/2; k = 2,4,6,8
    G = 384

    def row(label, pts, ms):
        vals = [C_n_from_measure(pts, ms, n, G=G) for n in NS]
        cells = "  ".join(f"k={2*n}:{v:+.5f}" for n, v in zip(NS, vals))
        minv = min(vals)
        flag = "" if minv >= 0 else "  <<< NEGATIVE"
        print(f"  {label:<34} {cells}{flag}")
        return vals

    print("C_n(mu0) for k=2,4,6,8  (n=k/2). NEGATIVE = potential cut.\n")

    # (A) Flammang opt conj-sym only (NOT z->1-z sym -> bound would be invalid, but
    #     report it as the diagnostic)
    th, mh = diffuse_from_p0(t, p0, 55, 8)
    zA, mA = conj_sym(th, mh)
    row("(A) Flammang p0 conj-only", zA, mA)

    # (B) z->1-z symmetrized Flammang p0  -- DECISIVE
    pB, mB = zz_sym(zA, mA)
    row("(B) p0 z->1-z SYM  [DECISIVE]", pB, mB)

    # (C) uniform-in-t symmetric
    pC, mC = uniform_t_sym(200)
    row("(C) uniform-t sym", pC, mC)

    # (D) shaped symmetric references
    for kind in ('concentrated', 'spread', 'bimodal', 'flammang_like'):
        pD, mD = shaped_t_sym(200, kind)
        row(f"(D) {kind} sym", pD, mD)

    # grid convergence check on (B), n=1 and n=2
    print("\n  grid-convergence on (B) (z->1-z sym):")
    for Gc in (256, 384, 512, 640):
        v1 = C_n_from_measure(pB, mB, 1, G=Gc)
        v2 = C_n_from_measure(pB, mB, 2, G=Gc)
        print(f"    G={Gc}: k=2 {v1:+.6f}   k=4 {v2:+.6f}")
