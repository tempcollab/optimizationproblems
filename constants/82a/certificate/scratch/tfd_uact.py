"""tfd_uact.py — the active-arc potential U_act, its minimum, and the continuous
relaxation of inf_Q r_Q.

U_act(beta) = (1/2pi) INT_{B>A} log|beta - w(t)| dt   (mu_act = 1_act dt/2pi, mass m0).

The continuous (no integer constraint) relaxation of inf over MONIC Q of
   r_Q = (1/deg Q) INT log|Q| dmu_act = (1/d) sum_j U_act(beta_j)
is just min_beta U_act(beta) (stack all roots at the global min of U_act).
We compute min U_act and compare to logh.  We also report the value of U_act on the
active locus itself (the level the equilibrium would equalize).
"""
import numpy as np
import scratch.tfd_setup as S

NC = 800_000


def build():
    t, w, A, B = S.contour(NC)
    act = B > A
    return t, w, act


def Uact_grid(betas, w, act):
    """Vectorized U_act over an array of betas (chunked)."""
    out = np.empty(len(betas))
    wa = w[act]
    m0 = act.mean()
    n = len(w)
    for k, b in enumerate(betas):
        out[k] = np.sum(np.log(np.abs(b - wa))) / n
    return out, m0


if __name__ == "__main__":
    t, w, act = build()
    wa = w[act]
    m0 = act.mean()
    print("mu_act mass m0 =", m0, " logh =", S.LOGH)

    # 1) U_act ON the contour support (sample of active points)
    samp = wa[np.linspace(0, len(wa) - 1, 400).astype(int)]
    Uon = np.array([np.sum(np.log(np.abs(b - wa))) / len(w) for b in samp])
    print(f"U_act on Sigma_act: min={Uon.min():.6f} mean={Uon.mean():.6f} "
          f"max={Uon.max():.6f}")

    # 2) global min of U_act over a grid.  U_act is smooth in beta, so a coarse but
    # mass-faithful quadrature of mu_act suffices: subsample wa to W points carrying
    # equal dt-weight, and multiply by m0 (mass) — i.e. U_act = m0 * mean_{wa-sample}.
    W = 6000
    wsub = wa[np.linspace(0, len(wa) - 1, W).astype(int)]
    gr = np.linspace(-2.2, 1.7, 140)
    gi = np.linspace(-2.0, 2.0, 140)
    GR, GI = np.meshgrid(gr, gi)
    BETA = (GR + 1j * GI).ravel()
    # U_act(beta) = m0 * mean over wsub of log|beta-wsub|
    # matrix in chunks of betas
    U = np.empty(len(BETA))
    CH = 2000
    for s in range(0, len(BETA), CH):
        bb = BETA[s:s + CH]
        L = np.log(np.abs(bb[:, None] - wsub[None, :]))
        U[s:s + CH] = m0 * L.mean(axis=1)
    imin = int(np.argmin(U))
    print(f"min U_act over grid = {U[imin]:.6f}  at beta={BETA[imin]:.4f}")
    print(f"=> continuous relaxation inf_Q r_Q (monic, real, roots free) = {U[imin]:.6f}")
    print(f"   logh - inf_continuous = {S.LOGH - U[imin]:+.6f}  (integer-constraint gap)")
