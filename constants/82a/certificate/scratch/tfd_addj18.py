"""tfd_addj18.py — float test: does adding block j18 (r_Q < logh) improve log h?

This grounds the integer-transfinite-diameter theorem with REAL CONTENT: the envelope
criterion r_Q < logh predicts j18 (deg 17, r_Q=0.25388 < 0.25404) should lower the
upper bound to first order.  We add it as a third free perturbing block and re-optimize
the exponents by a small Nelder-Mead.  FLOAT/CONJECTURE only — not a certificate.
"""
import numpy as np
from scipy.optimize import minimize
import scratch.tfd_setup as S
import verify_upper as vu
import flammang_table1 as ft

T = ft.get_table()
Q18 = T[18][1][::-1]          # high->low
DEG18 = 17


def pv(coef_hl, x):
    r = np.zeros_like(x, dtype=complex)
    for c in coef_hl:
        r = r * x + c
    return r


def logh(params, N):
    q = params[:5]
    qE, qF, qG = params[5], params[6], params[7]
    t = (np.arange(N) + 0.5) / N * 2 * np.pi
    z = np.exp(1j * t)
    w = z * (1 - z)
    A = sum(q[i] * np.log(np.abs(pv(S.BASE[i], w))) for i in range(5))
    B = (np.log(np.abs(pv(S.Q1, w))) + np.log(np.abs(pv(S.Q2, w)))
         + qE * np.log(np.abs(pv(S.Q5, w)))
         + qF * np.log(np.abs(pv(S.Q6, w)))
         + qG * np.log(np.abs(pv(Q18, w))))
    G = np.maximum(A, B)
    D = max(float(np.dot(q, S.DEGP)),
            56 + qE * S.DEG_Q5 + qF * S.DEG_Q6 + qG * DEG18)
    return np.mean(G) / D


if __name__ == "__main__":
    N = 1_000_000
    # held R11 point, qG=0 (recovers held)
    x0 = np.array([13.937341, 12.515102, 2.541409, 2.068537, 0.753965,
                   0.891271, 0.246614, 0.0])
    print("held (qG=0) log h =", logh(x0, 4_000_000))

    # turn on qG a little (envelope says decrease)
    for qG in (0.0, 0.05, 0.1, 0.2, 0.3):
        xx = x0.copy(); xx[7] = qG
        print(f"  qG={qG:.2f}  log h = {logh(xx, 1_000_000):.8f}")

    # full re-optimization with qG free
    def obj(x):
        if np.any(x[5:] < 0) or np.any(x[:5] <= 0):
            return 1e3
        return logh(x, N)
    res = minimize(obj, x0, method="Nelder-Mead",
                   options=dict(xatol=1e-5, fatol=1e-9, maxiter=4000))
    print("\nre-optimized with j18 free:")
    print("  x* =", np.round(res.x, 6).tolist())
    v = logh(res.x, 8_000_000)
    print(f"  log h* (N=8M) = {v:.8f}   held R11 cert = 0.2540419719")
    print(f"  float improvement vs held float 0.2540418523 = {0.2540418523 - v:+.3e}")
