"""
ROUTE 3 — is J(mu) CONCAVE? (validity of the OSS tangent outer-cut).

The OSS 2-point cut is valid because I(mu) (log-energy) is CONCAVE on the cone of
probability measures (Ahlfors 2.1 / negative-definiteness of the log kernel), so the
tangent at mu0 is an OUTER bound: {I>=0} ⊂ {tangent>=0}, hence adding the linear cut
only relaxes => LP value is a valid lower bound.

For J(mu) = INT^4 log|x1-x2-x3+x4| dmu^4 (a QUARTIC form in mu) concavity is NOT
automatic. If J is NOT concave, the tangent at mu0 is NOT a valid outer cut, and any
LP 'raise' from it is SPURIOUS (not a valid bound). We test concavity directly:

  concave  <=>  J((mu1+mu2)/2) >= (J(mu1)+J(mu2))/2  for ALL mu1,mu2 (midpoint),
  equivalently the Hessian quadratic form d^2/ds^2 J(mu0 + s v) <= 0 for all
  mass-zero directions v.

We sample random measure pairs and random directions and report the WORST violation.
If we find midpoints with J(mid) < avg (i.e. CONVEXITY somewhere) => J is NOT concave
=> the tangent cut is INVALID as an outer relaxation.
"""
import numpy as np
from scipy.signal import fftconvolve
from scratch.route3_J_fft import hist_measure

Nnode = 40
th = (np.arange(Nnode) + 0.5) / Nnode * np.pi
z = np.exp(1j * th)


def expand(q):
    q = np.maximum(q, 0); q = q / q.sum()
    pts = np.concatenate([z, np.conj(z), 1 - z, 1 - np.conj(z)])
    ms = np.concatenate([q, q, q, q]) / 4
    return pts, ms


def J_of(q, G=288, pad=1.2):
    pts, ms = expand(q)
    R = np.abs(pts).max() * pad
    M, h = hist_measure(pts, ms, -R, R, G)
    Mref = M[::-1, ::-1].copy()
    rho = fftconvolve(M, Mref, mode='full'); rho[rho < 0] = 0
    P = fftconvolve(rho, rho, mode='full'); P[P < 0] = 0
    nP = P.shape[0]; c0 = 2 * (G - 1); idx = np.arange(nP) - c0
    IX, IY = np.meshgrid(idx, idx, indexing='ij')
    Ab = np.hypot(IX * h, IY * h)
    with np.errstate(divide='ignore'):
        L = np.log(Ab)
    L[~np.isfinite(L)] = 0.0
    return float((P * L).sum())


if __name__ == "__main__":
    rng = np.random.default_rng(3)
    worst_pair = (0.0, 0.0, 0.0, 1e9)      # track MOST-NEGATIVE gap
    for trial in range(120):
        a1 = rng.uniform(0.1, 3); a2 = rng.uniform(0.1, 3)
        q1 = rng.dirichlet(np.full(Nnode, a1))
        q2 = rng.dirichlet(np.full(Nnode, a2))
        mid = 0.5 * (q1 + q2)
        J1 = J_of(q1); J2 = J_of(q2); Jm = J_of(mid)
        gap = Jm - 0.5 * (J1 + J2)         # >=0 for concave; <0 => convexity (NOT concave)
        if gap < worst_pair[3]:            # track most-negative gap
            worst_pair = (J1, J2, Jm, gap)
        if gap < -1e-3 and trial < 8:
            print(f"  trial {trial}: J1={J1:+.4f} J2={J2:+.4f} Jmid={Jm:+.4f} "
                  f"gap(mid-avg)={gap:+.4f}  {'<-- CONVEX (concavity FAILS)' if gap<0 else ''}")
    J1, J2, Jm, gap = worst_pair
    print(f"\nWORST midpoint gap (mid - avg) = {gap:+.5f}")
    print(f"  at J1={J1:+.4f} J2={J2:+.4f} Jmid={Jm:+.4f}")
    if gap < -1e-3:
        print("  => J is NOT CONCAVE: tangent outer-cut is INVALID as a bound.")
    else:
        print("  => no concavity violation found in this sample (consistent with concave).")
