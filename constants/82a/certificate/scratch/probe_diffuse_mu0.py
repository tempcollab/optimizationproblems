"""
DE-RISK PROBE (round 13 outliner): does a FINITE-ENERGY (diffuse) reference mu0
still raise m_cut past 0.2487458 by a margin worth certifying?

The fatal gap in the atomic version: mu0 atomic => I(mu0) = -inf (diagonal
log|z_p-z_p| with positive mass mu0_p^2). The R12 code used off-diagonal-only
I0=-0.097 in place of -inf, which weakens the cut in the UNSAFE direction; the
cut INT(2 U_mu0 - I0) dnu >= I(nu) is then NOT implied by eq.6 and can fail.

Repair: use a SMOOTH/diffuse mu0 with FINITE log-energy. Then eq.6 (concavity of
the continuous log-energy) gives genuinely:
    I(nu - mu0) <= 0
 => 2 I(nu,mu0) - I(mu0) >= I(nu) >= 0
 => INT (2 U_mu0(z) - I(mu0)) dnu >= 0,    with the SAME finite I(mu0) in cut and bound.

We model the diffuse mu0 as a sum of arcs: spread the LP-optimal node masses by a
boxcar of half-width h (in t) so the resulting density on |z|=1 is bounded. To keep
everything as a finite computation with a CONSISTENT diagonal, we represent the
diffuse mu0 itself as a FINE atomic grid of M >> N nodes with masses summing to 1,
and define its log-energy with the SAME kernel convention used for nu, i.e. a
genuine pair energy where the self-pair (diagonal) is replaced by the analytic
self-energy of a small boxcar arc (finite). Concretely, for a uniform arc of
half-width h centered at t0 carrying mass dm, its self log-energy in z = e^{it}:
    (1/(2h)^2) INT_{t0-h}^{t0+h} INT_{t0-h}^{t0+h} log|e^{is}-e^{is'}| ds ds'.
Using |e^{is}-e^{is'}| = 2|sin((s-s')/2)|, this is a finite constant per arc; we
bound it (and the whole I(mu0)) by a fine sub-grid Riemann sum with the singular
diagonal handled by the analytic boxcar self-energy. For the PROBE we just need a
defensible FINITE I(mu0); rigor of the enclosure is a stage-2 detail.

The cut row uses the potential U_mu0(z_n) = INT log|z_n - w| dmu0(w), which for a
diffuse mu0 is a SMOOTH bounded function on |z|=1 (no atom singularities) — exactly
the property that removes the log-kinks.

Run: python3 probe_diffuse_mu0.py
Reports, per (N, h, M): I(mu0) finite, m_cut, lambda0, m_cut-0.2487458, gate.
"""
import numpy as np
from scipy.optimize import linprog
from flammang_table1 import get_table

ANCHOR = 0.2487458
GATE = 1e-4


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


def solve_primal(g, A, extra_rows=None, extra_rhs=None):
    N = len(g); J = A.shape[1]
    Aub = -A.T; bub = np.zeros(J)
    if extra_rows is not None:
        Aub = np.vstack([Aub, -np.asarray(extra_rows)])
        bub = np.concatenate([bub, -np.asarray(extra_rhs)])
    Aeq = np.ones((1, N)); beq = np.array([1.0])
    res = linprog(g, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq,
                  bounds=[(0, None)] * N, method="highs")
    if res.status != 0:
        raise RuntimeError(res.message)
    lambdas = []
    if extra_rows is not None:
        n_extra = np.asarray(extra_rows).shape[0]
        marg = res.ineqlin.marginals[-n_extra:]
        lambdas = list(np.maximum(-marg, 0.0))
    return res.fun, res.x, lambdas


def conj_log_dist(za, zb):
    """1/2(log|za-zb| + log|za-conj zb|), array-broadcast. Diagonal of first term -inf."""
    Za = za[:, None]; Zb = zb[None, :]
    with np.errstate(divide="ignore"):
        T1 = np.log(np.abs(Za - Zb))
        T2 = np.log(np.abs(Za - np.conj(Zb)))
    return 0.5 * (T1 + T2)


def boxcar_self_energy(h):
    """Self log-energy of a UNIFORM boxcar arc of half-width h (in t) on |z|=1,
    using the FULL conjugate-symmetric energy (z and conj z both conjugates):
       1/2 * mean over s,s' in [-h,h] of [ log|e^{is}-e^{is'}| + log|e^{is}-e^{-is'}| ]
    but centered; the value depends only on h to leading order for small h, plus a
    center-dependent second (conj) term. We return the FIRST (singular) part only;
    the conj part is regular and handled in the full grid. Compute by fine subgrid."""
    m = 400
    s = np.linspace(-h, h, m)
    S, Sp = np.meshgrid(s, s)
    with np.errstate(divide="ignore"):
        D = np.log(np.abs(2.0 * np.sin((S - Sp) / 2.0)))
    # diagonal s=s' -> -inf; replace by analytic limit of the local 1D integral.
    # The boxcar self-energy of a uniform measure on an interval of length 2h on the
    # arc (metric ~ ds) has the 1D log-energy of a uniform measure on [-h,h]:
    #   (1/(2h)^2) INT INT log|s-s'| ds ds' = log(2h) - 3/2  (uniform interval energy),
    # plus log( |2 sin(d/2)| / |d| ) corrections ~ O(h^2). Use the closed form:
    return np.log(2.0 * h) - 1.5


def build_diffuse_mu0(t0, m0_masses, h, M):
    """Build a fine M-node atomic representation of the diffuse mu0 = sum_p m0_p *
    Uniform(t0_p - h, t0_p + h). Returns (tg, zg, pg) the fine grid and its masses,
    and a FINITE I(mu0) using the conj-symmetric kernel with the singular self-pairs
    replaced by the analytic boxcar self-energy."""
    # fine global grid
    tg = np.linspace(1e-4, np.pi - 1e-4, M)
    zg = np.exp(1j * tg)
    dt = tg[1] - tg[0]
    pg = np.zeros(M)
    for tp, mp in zip(t0, m0_masses):
        if mp <= 0:
            continue
        lo = tp - h; hi = tp + h
        mask = (tg >= lo) & (tg <= hi)
        k = mask.sum()
        if k == 0:
            j = np.argmin(np.abs(tg - tp)); pg[j] += mp
        else:
            pg[mask] += mp / k
    pg /= pg.sum()
    # I(mu0) with conj-symmetric kernel; off-diagonal pairs from the grid,
    # diagonal self-pairs replaced by analytic boxcar self-energy term.
    Kfull = conj_log_dist(zg, zg)          # diagonal of T1 is -inf
    # replace the singular T1-diagonal contribution by the boxcar self-energy.
    # Each grid node represents a sub-arc of width dt; its self log-energy (1D
    # uniform interval of length dt): log(dt) - 3/2 ... but we want the energy of
    # the SMOOTH mu0, whose self-interaction within distance dt is ~ this. We set
    # the diagonal of T1 to the analytic per-node self term log(dt)-1.5 (= boxcar
    # self energy of a width-dt arc) plus the conj partner which is in T2 already.
    selfdiag = np.log(dt) - 1.5
    Kfull = Kfull.copy()
    # Kfull currently has 0.5*(T1diag(-inf) + T2diag). Rebuild diagonal cleanly:
    Za = zg
    T2diag = np.log(np.abs(Za - np.conj(Za)))   # = log|2 sin t| regular
    np.fill_diagonal(Kfull, 0.5 * (selfdiag + 0.0))  # temp, will add T2diag below
    diag = 0.5 * (selfdiag + T2diag)
    np.fill_diagonal(Kfull, diag)
    I_mu0 = float(pg @ Kfull @ pg)
    return tg, zg, pg, I_mu0


def potential_on_nodes(z_nodes, zg, pg):
    """U_mu0(z_n) = INT 1/2(log|z_n-w|+log|z_n-conj w|) dmu0(w), diffuse mu0 on grid zg
    with masses pg. For z_nodes on the SAME grid as zg, the self term log|z_n-z_n| is
    -inf at one grid node; but since mu0 is DIFFUSE, the true potential is finite. We
    compute on a SEPARATE node set (the LP contour at resolution N != M) so z_n rarely
    coincides with a zg atom; where |z_n - w| is tiny we still get a finite sum because
    pg per node is tiny. For the PROBE we use the off-grid contour nodes directly."""
    Za = z_nodes[:, None]; Zb = zg[None, :]
    with np.errstate(divide="ignore"):
        T1 = np.log(np.abs(Za - Zb))
        T2 = np.log(np.abs(Za - np.conj(Zb)))
    Kmix = 0.5 * (T1 + T2)
    # guard: any -inf (exact coincidence) -> replace by local self term
    bad = ~np.isfinite(Kmix)
    if bad.any():
        Kmix[bad] = -10.0   # crude finite guard for probe only
    return Kmix @ pg


def run(N, h, M):
    t, z, w, g = contour(N)
    A = column_matrix(w)
    m0, p0, _ = solve_primal(g, A)
    # diffuse mu0 from the no-energy optimum's node masses
    tg, zg, pg, I_mu0 = build_diffuse_mu0(t, p0, h, M)
    U0 = potential_on_nodes(z, zg, pg)        # potential at LP contour nodes
    cut_row = 2.0 * U0 - I_mu0
    m_cut, p_cut, lambdas = solve_primal(g, A, extra_rows=[cut_row], extra_rhs=[0.0])
    lam = lambdas[0] if lambdas else 0.0
    return dict(N=N, h=h, M=M, m0=m0, I_mu0=I_mu0, m_cut=m_cut, lam=lam,
                raise_anchor=m_cut - ANCHOR)


def main():
    print("DE-RISK PROBE: diffuse (finite-energy) mu0, cut LP raise vs 0.2487458")
    print(f"{'N':>5}{'h':>8}{'M':>6}{'m0':>12}{'I(mu0)':>11}{'m_cut':>12}"
          f"{'lambda0':>10}{'raise':>12}{'gate':>7}")
    for N in (1000, 2000):
        for h in (0.005, 0.01, 0.02, 0.04, 0.08):
            M = 6000
            r = run(N, h, M)
            gate = "FIRES" if r['raise_anchor'] > GATE else "no"
            print(f"{r['N']:>5}{r['h']:>8.3f}{r['M']:>6}{r['m0']:>12.7f}"
                  f"{r['I_mu0']:>11.4f}{r['m_cut']:>12.7f}{r['lam']:>10.4f}"
                  f"{r['raise_anchor']:>+12.6f}{gate:>7}")


if __name__ == "__main__":
    main()
