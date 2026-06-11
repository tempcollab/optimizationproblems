"""tfd_capacity.py — equilibrium measure & Robin constant of the active locus Sigma_act.

We discretize the active arcs of the contour w(t)=z(1-z), |z|=1, into M point masses,
solve the (continuous) weighted/unweighted equilibrium problem by minimizing the
discrete log-energy with the Fekete linear-algebra method, and compare the resulting
equilibrium measure to the uniform-in-t active measure mu_act.

Capacity / Robin constant definitions (UNWEIGHTED, standard potential theory):
  For a probability measure nu on Sigma, energy I(nu)= INT INT log|w-w'| dnu dnu.
  Equilibrium nu* MAXIMIZES I (least-energy in the -log convention) and
  I(nu*) = log cap(Sigma) =: -Robin? -- conventions vary; we use:
      Robin constant  gamma = -log cap(Sigma) = - max_nu I(nu)
  so cap = exp(-gamma).  Larger Sigma -> larger cap -> smaller gamma.

The object the brief wants compared to logh is the LOG-CAPACITY pairing.  We compute
both the equilibrium measure and the value max_nu I(nu) on Sigma_act, then form the
relevant comparison.
"""
import numpy as np
import scratch.tfd_setup as S


def active_points(N_contour=400_000):
    """Return active w-points (subsampled) with their dt-weights, as the support of
    Sigma_act.  Each point carries equal dt (uniform-in-t)."""
    t, w, A, B = S.contour(N_contour)
    act = B > A
    return t[act], w[act]


def discretize(M, N_contour=400_000):
    """M roughly-uniform-in-t support points on Sigma_act (active arcs)."""
    ta, wa = active_points(N_contour)
    idx = np.linspace(0, len(wa) - 1, M).astype(int)
    return ta[idx], wa[idx]


def energy_matrix(w):
    """K[i,j]=log|w_i-w_j| (diagonal: regularized by local spacing)."""
    M = len(w)
    D = np.abs(w[:, None] - w[None, :])
    np.fill_diagonal(D, 1.0)
    K = np.log(D)
    # regularize diagonal: log of half the min neighbor distance (Fekete self-term)
    # use nearest-neighbor spacing as the local scale
    Dtmp = np.abs(w[:, None] - w[None, :]) + np.eye(M) * 1e9
    nn = Dtmp.min(axis=1)
    np.fill_diagonal(K, np.log(nn * 0.5))
    return K


def equilibrium_measure(M=1200, weight=None):
    """Solve for the probability vector p>=0, sum p=1, maximizing p^T K p
    (equilibrium / max-energy measure in the +log|.| convention).  With an optional
    external field weight phi (Robin: maximize p^T K p + 2 sum p_i log phi_i, i.e.
    weighted equilibrium with field Q=-log phi).  Returns (p, w, value, robin)."""
    ta, w = discretize(M)
    K = energy_matrix(w)
    field = np.zeros(M) if weight is None else np.log(weight(w))
    # Maximize F(p)=p^T K p + 2 field^T p on the simplex.  The unconstrained
    # stationary condition (equal-potential) is 2 K p + 2 field = lambda 1.
    # Solve [2K, -1; 1^T, 0][p;lambda]=[-2 field;1]; then clip negatives & re-solve
    # on the active support (projected-gradient-free Fekete LP-ish iteration).
    Mn = M
    p = np.ones(Mn) / Mn
    active = np.ones(Mn, bool)
    for _ in range(60):
        ai = np.where(active)[0]
        Ka = K[np.ix_(ai, ai)]
        fa = field[ai]
        n = len(ai)
        Aug = np.zeros((n + 1, n + 1))
        Aug[:n, :n] = 2 * Ka
        Aug[:n, n] = -1.0
        Aug[n, :n] = 1.0
        rhs = np.zeros(n + 1)
        rhs[:n] = -2 * fa
        rhs[n] = 1.0
        sol = np.linalg.lstsq(Aug, rhs, rcond=None)[0]
        pa = sol[:n]
        lam = sol[n]
        if (pa >= -1e-12).all():
            p = np.zeros(Mn)
            p[ai] = np.maximum(pa, 0)
            p /= p.sum()
            break
        # drop the most-negative
        kill = ai[np.argmin(pa)]
        active[kill] = False
        p = np.zeros(Mn)
        p[ai] = np.maximum(pa, 0)
        if p.sum() > 0:
            p /= p.sum()
    value = p @ K @ p + 2 * field @ p          # max energy (with field)
    robin = -value                              # Robin constant gamma
    return p, w, value, robin


if __name__ == "__main__":
    for M in (800, 1200, 1600):
        p, w, val, rob = equilibrium_measure(M)
        print(f"M={M:5d}  max_nu I(nu) = {val:.6f}  Robin gamma=-I = {rob:.6f}  "
              f"cap=exp(-gamma)={np.exp(-rob):.6f}  support_size={(p>1e-9).sum()}")
