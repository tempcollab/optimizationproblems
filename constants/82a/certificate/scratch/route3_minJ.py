"""
ROUTE 3 — is J ever negative on this geometry? (the Route-1-style no-go test).

J(mu) = INT log|S| dP4(S), P4 = distribution of x1-x2-x3+x4, the 4-fold sum.
J is a QUARTIC form in mu (degree-4 in the masses). Minimizing a quartic over the
simplex is non-convex, but we can:
  (1) sample MANY random measures on the contour (both symmetric and asymmetric)
      and report the min J found;
  (2) do a local descent (projected gradient on the simplex) from several starts
      to push J as low as possible.
If min J stays clearly POSITIVE, the constraint J>=0 is GLOBALLY INERT (never binds)
=> Route 3 gives no cut, EVER -- a clean complete negative result.

We restrict to measures supported on the contour z=e^{it}, t in (0,pi), folded
conj-symmetric (and optionally z->1-z symmetric). Variable = masses q on a node set.
"""
import numpy as np
from scipy.signal import fftconvolve
from scratch.route3_J_fft import (contour, column_matrix, solve_primal, hist_measure)

ANCHOR = 0.2487458


def build_nodes(Nnode, zz_symmetric):
    """Node cloud (complex) closed under conj (and z->1-z if requested) and the
    'reduction' map index->mass. Returns base half-arc nodes + an expansion fn."""
    th = (np.arange(Nnode) + 0.5) / Nnode * np.pi
    z = np.exp(1j * th)

    def expand(q):
        q = np.maximum(q, 0); q = q / q.sum()
        if zz_symmetric:
            pts = np.concatenate([z, np.conj(z), 1 - z, 1 - np.conj(z)])
            ms = np.concatenate([q, q, q, q]) / 4
        else:
            pts = np.concatenate([z, np.conj(z)])
            ms = np.concatenate([q, q]) / 2
        return pts, ms
    return th, expand


def J_of(pts, ms, G=384, pad=1.2):
    R = np.abs(pts).max() * pad
    M, h = hist_measure(pts, ms, -R, R, G)
    Mref = M[::-1, ::-1].copy()
    rho = fftconvolve(M, Mref, mode='full'); rho[rho < 0] = 0
    P = fftconvolve(rho, rho, mode='full'); P[P < 0] = 0
    nP = P.shape[0]; c0 = 2 * (G - 1)
    idx = np.arange(nP) - c0
    IX, IY = np.meshgrid(idx, idx, indexing='ij')
    AbsS = np.hypot(IX * h, IY * h)
    with np.errstate(divide='ignore'):
        L = np.log(AbsS)
    L[~np.isfinite(L)] = 0.0
    return float((P * L).sum())


def random_search(expand, Nnode, ntrial, rng, G=320):
    best = np.inf
    for _ in range(ntrial):
        # random measures of varied concentration
        a = rng.uniform(0.1, 3.0)
        q = rng.dirichlet(np.full(Nnode, a))
        pts, ms = expand(q)
        J = J_of(pts, ms, G=G)
        best = min(best, J)
    return best


def descent(expand, Nnode, rng, G=320, steps=60, lr=0.5):
    """Projected-gradient descent on q (simplex) to minimize J. Finite-diff grad."""
    q = rng.dirichlet(np.full(Nnode, 1.0))
    def f(q):
        pts, ms = expand(q); return J_of(pts, ms, G=G)
    cur = f(q)
    for it in range(steps):
        # stochastic coordinate finite-diff grad (cheap subset)
        eps = 1e-3
        grad = np.zeros(Nnode)
        cols = rng.choice(Nnode, size=min(Nnode, 12), replace=False)
        for c in cols:
            qp = q.copy(); qp[c] += eps; qp = np.maximum(qp, 0); qp /= qp.sum()
            grad[c] = (f(qp) - cur) / eps
        q = q - lr * grad
        q = np.maximum(q, 1e-9); q /= q.sum()
        cur = f(q)
    return cur


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    for sym in (True, False):
        tag = "z->1-z SYMMETRIC" if sym else "asymmetric (conj only)"
        th, expand = build_nodes(40, sym)
        br = random_search(expand, 40, 400, rng, G=288)
        bd = min(descent(expand, 40, rng, G=288) for _ in range(4))
        print(f"{tag:24s}: min J  random={br:+.5f}  descent={bd:+.5f}  -> "
              f"min J ~ {min(br,bd):+.5f}")
    print("\nIf min J > 0 everywhere => J>=0 is globally inert (never a binding cut).")
