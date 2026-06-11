"""tfd_capacity2.py — fast equilibrium measure & Robin constant of Sigma_act.

Equilibrium (unweighted, +log convention): probability nu* on Sigma maximizing
  I(nu) = INT INT log|w-w'| dnu dnu.
Stationarity: the potential U_nu(w)=INT log|w-w'|dnu is CONSTANT (= I(nu*)) on supp nu*
and >= it off support.  We solve by an iterative balayage / Lawson-type fixed point:
repeatedly equalize the potential on the support by reweighting, restricted to p>=0.

Robin constant gamma = -I(nu*) ; cap(Sigma)=exp(I(nu*)).
"""
import numpy as np
import scratch.tfd_setup as S


def discretize(M, N_contour=600_000):
    t, w, A, B = S.contour(N_contour)
    act = B > A
    wa = w[act]
    idx = np.linspace(0, len(wa) - 1, M).astype(int)
    return wa[idx]


def kernel(w):
    M = len(w)
    Dm = np.abs(w[:, None] - w[None, :])
    big = Dm + np.eye(M) * 1e9
    nn = big.min(axis=1)
    np.fill_diagonal(Dm, nn * 0.5)        # Fekete self-distance regularization
    return np.log(Dm)


def equilibrium(M=1500, iters=4000, field=None):
    """Return p (prob), w, I=p^T K p (+field), robin=-I.
    field: optional array (external field 2*field added: maximize p^TKp+2 field^T p)."""
    w = discretize(M)
    K = kernel(w)
    f = np.zeros(M) if field is None else np.asarray(field, float)
    # Lawson-style multiplicative update toward equal potential U=K p + f.
    p = np.ones(M) / M
    for it in range(iters):
        U = K @ p + f
        # target: raise mass where U is large (max-energy), lower where small.
        # multiplicative weights on (U - mean):
        g = U - U.max()
        p = p * np.exp(0.5 * (U - (p @ U)))
        p = np.maximum(p, 0)
        p /= p.sum()
    U = K @ p + f
    I = p @ K @ p + 2 * f @ p
    return p, w, I, -I, U


if __name__ == "__main__":
    for M in (1000, 1500, 2000):
        p, w, I, rob, U = equilibrium(M, iters=3000)
        supp = (p > p.max() * 1e-4).sum()
        # potential spread on the bulk support (should be ~constant)
        msk = p > p.max() * 1e-3
        print(f"M={M:5d}  I(nu*)={I:.6f}  Robin gamma=-I={rob:.6f}  "
              f"cap=exp(I)={np.exp(I):.6f}  supp={supp}  U_spread={np.ptp(U[msk]):.4f}")
