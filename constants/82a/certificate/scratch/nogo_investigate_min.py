"""
Investigate the minimizing measure found by nogo_minsearch: mass concentrates at
half-node 0 (t near 0 => z near 1). Is this a genuine counterexample or an artifact
of concentrating at the excluded points {0,1} where the whole framework degenerates?

Key facts to check:
 - the minimizer puts mass near z=1 and z=0 (z->1-z images), the EXCLUDED roots
   (z^2-z factor of the exception set). A measure concentrated there is NOT a
   reference measure that yields a valid cut: the conjugate measure mu0 must be a
   legitimate diffuse measure, and points at 0/1 are exactly the finite exception
   set Flammang removes.
 - As mass -> delta at a single orbit {z, conj z, 1-z, 1-conj z}, what is C_n?
   For a 4-atom measure C_n is a FIXED number (computed in brute_check). Concentrating
   gives a degenerate near-atomic measure. Is C_n(near-atom) < 0 for n>=2?
 - DECISIVE distinction for the cut argument: the cut from column C_{Q_S} can only
   bind if C_{Q_S}(p0) < 0 at the ACTUAL Flammang LP optimum p0 (or its symmetrization),
   NOT at some adversarially-chosen reference. The reference mu0 is OUR choice for the
   self-cut (2 grad - C) >= 0; but the cut separates the LP optimum p0 only if the LP
   optimum itself has C_{Q_S}(p0) < 0. The minsearch minimizes over ALL measures, which
   answers a DIFFERENT question (does the column constraint cut ANY measure) -- yes it
   does for atoms, but the LP optimum is diffuse and sits where C_n>=0.

So: re-examine. Print the minimizing q, the resulting atomic structure, and C_n for
a sequence of measures interpolating uniform -> the minimizer, to see WHERE C_n
crosses 0 and whether that region is the (excluded) atomic corner.
"""
import numpy as np
from scipy.signal import fftconvolve
from scipy.optimize import minimize
from scratch.nogo_Cmu0 import C_n_from_measure, conj_sym, zz_sym


def build_symmetric(q, t_half):
    q = np.maximum(q, 0); q = q / q.sum()
    z, m = conj_sym(t_half, q)
    return zz_sym(z, m)


def make_Cfun(n, t_half, G=320):
    def f(q):
        pts, ms = build_symmetric(q, t_half)
        return C_n_from_measure(pts, ms, n, G=G)
    return f


if __name__ == "__main__":
    K = 18
    t_half = (np.arange(K) + 0.5) / K * (np.pi / 2)
    print("half-node t values (radians):", np.round(t_half, 4))
    print(f"node 0 at t={t_half[0]:.4f} => z=e^(it)={np.exp(1j*t_half[0]):.4f} (near z=1)\n")

    # re-find the minimizer for n=2 and inspect it
    for n in (2, 3, 4):
        f = make_Cfun(n, t_half, G=320)
        e0 = np.zeros(K); e0[0] = 1.0
        res = minimize(f, e0, method='SLSQP',
                       bounds=[(0, 1)] * K,
                       constraints={'type': 'eq', 'fun': lambda q: q.sum() - 1},
                       options={'maxiter': 300, 'ftol': 1e-10})
        qmin = np.maximum(res.x, 0); qmin /= qmin.sum()
        print(f"n={n}: min C_n = {res.fun:+.5f}")
        print(f"      minimizing q (half-node masses): {np.round(qmin, 3)}")
        # how concentrated near z=1 (node 0)?
        print(f"      mass on node 0 (t~{t_half[0]:.3f}, z~1): {qmin[0]:.3f}; "
              f"mass on nodes 0-2 (t<{t_half[2]:.3f}): {qmin[:3].sum():.3f}")
        # interpolate uniform -> minimizer; where does C_n cross 0?
        unif = np.ones(K) / K
        print(f"      C_n along uniform->minimizer:")
        for lam in (0.0, 0.25, 0.5, 0.75, 0.9, 1.0):
            qi = (1 - lam) * unif + lam * qmin
            print(f"         lam={lam:.2f}  C_n={f(qi):+.5f}  (mass@node0={qi[0]:.3f})")
        print()
