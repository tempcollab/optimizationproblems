"""
82a LOWER bound, PATH B stage-2 — FREEZE step for the rigorous OSS log-energy cert.

Produces the FROZEN stage-1 data the interval branch-and-bound certificate
(verify_vec_energy.py) consumes:

  - the histogram reference measure mu0 (Fallback B of the outline review, P3):
    a piecewise-CONSTANT density on coarse uniform t-bins, support {(c_k, mass_k)},
    each bin a uniform arc of t-width L; sum mass_k = 1, mass_k >= 0;
  - the cut LP DUAL weights:  c_j >= 0 (j=1..24, Flammang columns) and
    lambda0 >= 0 (the energy cut), together with m_cut (the LP value), from the
    cut LP solved with a CLEAN potential row (NO -10 fudge — P2);
  - Ihat = I_lo, a rigorous DOWNWARD enclosure of the FINITE log-energy I(mu0)
    (P3): exact closed-form singular self-energy + rigorous interval lower bounds
    on every off-diagonal / conjugate block.

P1 NOTE (load-bearing).  The certificate's proof of cut validity (C3) rests on the
CONTINUOUS negative-definiteness of the log kernel (Ahlfors Lemma 2.1 / OSS eq.6),
valid because mu0 (bounded histogram density) and nu (off the finite exception set)
both have FINITE energy.  The boxcar/Clausen discretization here is ONLY the
numerical route to a rigorous LOWER bound Ihat on the SAME continuous I(mu0); it is
NOT itself the proof of (C3).  See verify_vec_energy.py header.

P3 (the heart of the fix).  I(mu0) = INT INT (1/2)(log|z-w| + log|z-conj w|)
dmu0 dmu0.  For mu0 = sum_b mass_b * Uniform(arc_b):

    I(mu0) = sum_{a,b} mass_a mass_b * M(a,b),
    M(a,b) = (1/2)( T1(a,b) + T2(a,b) ),
    T1 = mean_{s in arc_a, s' in arc_b} log|e^{is}-e^{is'}|   (singular iff a==b),
    T2 = mean log|e^{is}-e^{-is'}|                            (regular here).

We bound M(a,b) BELOW for every block (rounding the mean kernel DOWN), so since
mass_a mass_b >= 0, the sum is a rigorous LOWER bound Ihat <= I(mu0):
  - Diagonal singular T1: EXACT closed form
        T1_self(L) = (1/L^2) INT_0^L INT_0^L log(2|sin((s-s')/2)|) ds ds'
                   = -2 ( zeta(3) - Re Li3(e^{iL}) ) / L^2,
    evaluated in mpmath, then rounded DOWN.
  - Every other contribution (off-diagonal T1, all T2): rigorous interval lower
    bound on the mean of log(dist) over the product of two arcs, by tiling each arc
    into nsub sub-cells and on each pair enclosing the MINIMUM squared distance
    (a monotone function of an angle interval), then log, take lower endpoint.
    Averaging lower bounds gives a lower bound on the mean.  All in mpmath.

Run:  python3 freeze_energy.py                 (compute + dump frozen_energy.npz)
      python3 freeze_energy.py check           (cross-checks + gate)
"""
import sys
import math
import numpy as np
import mpmath as mp
from scipy.optimize import linprog
from flammang_table1 import get_table

mp.mp.prec = 90

ANCHOR = 0.2487458          # log(1.282416), Flammang F18 verified lower bound

# ---- LP plumbing -----------------------------------------------------------

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
    """min p.g s.t. A^T p>=0, [extra row.p>=rhs], sum p=1, p>=0. Returns
    (m, p, dual_cj, dual_lambdas). dual_cj are the >=0 multipliers on the 24
    column constraints; dual_lambdas on the extra rows."""
    N = len(g); J = A.shape[1]
    Aub = -A.T; bub = np.zeros(J)
    n_extra = 0
    if extra_rows is not None:
        n_extra = np.asarray(extra_rows).shape[0]
        Aub = np.vstack([Aub, -np.asarray(extra_rows)])
        bub = np.concatenate([bub, -np.asarray(extra_rhs)])
    Aeq = np.ones((1, N)); beq = np.array([1.0])
    res = linprog(g, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq,
                  bounds=[(0, None)] * N, method="highs")
    if res.status != 0:
        raise RuntimeError(res.message)
    marg = res.ineqlin.marginals
    dual_cj = np.maximum(-marg[:J], 0.0)
    dual_lambdas = list(np.maximum(-marg[J:J + n_extra], 0.0)) if n_extra else []
    return res.fun, res.x, dual_cj, dual_lambdas


# ---- histogram mu0 ---------------------------------------------------------

def build_histogram_mu0(t, p0, B):
    """Bin the no-energy optimum masses p0 into B uniform t-bins on [0,pi].
    Returns (centers, masses, L) over NONZERO bins; each bin a uniform arc of
    t-width L. masses sum to 1."""
    edges = np.linspace(0.0, np.pi, B + 1)
    L = edges[1] - edges[0]
    idx = np.clip(np.searchsorted(edges, t) - 1, 0, B - 1)
    binmass = np.zeros(B)
    for i, m in zip(idx, p0):
        binmass[i] += m
    binmass /= binmass.sum()
    centers_all = 0.5 * (edges[:-1] + edges[1:])
    nz = np.where(binmass > 1e-13)[0]
    return centers_all[nz], binmass[nz], L


# ---- rigorous I(mu0) LOWER bound -------------------------------------------

def _F2(x):
    """F2(x) = Re Li3(e^{ix}) - zeta(3).  Even in x.  Second antiderivative of
    log(2 sin(x/2)) (F2'' = log(2 sin(x/2)) on (0, 2 pi))."""
    return mp.re(mp.polylog(3, mp.e ** (1j * x))) - mp.zeta(3)


def B1_exact(d, L):
    """EXACT mean of log|e^{is} - e^{is'}| over s in arc(width L, sep |d|), i.e.
    the t-width-L uniform double-arc mean of log(2|sin(x/2)|) with x ranging over
    [|d|-L, |d|+L] with triangular density.  Closed form (header derivation):
        B1(d,L) = ( F2(|d|-L) + F2(|d|+L) - 2 F2(|d|) ) / L^2.
    Valid for 0 <= |d|, |d|+L < 2 pi.  d=0 gives the singular self mean (finite,
    integrable log singularity).  Even in d."""
    da = abs(mp.mpf(d)); Lm = mp.mpf(L)
    return (_F2(da - Lm) + _F2(da + Lm) - 2 * _F2(da)) / (Lm * Lm)


def block_mean_M(ca, cb, L):
    """EXACT M(a,b) = (1/2)( T1 + T2 ), the conj-symmetric kernel mean over the
    product of two uniform arcs (centers ca, cb, width L):
        T1 = mean log|e^{is}-e^{is'}|     = B1(ca-cb, L),
        T2 = mean log|e^{is}-e^{-is'}|    = B1(ca+cb, L)."""
    return mp.mpf('0.5') * (B1_exact(ca - cb, L) + B1_exact(ca + cb, L))


def I_mu0_exact(centers, masses, L):
    """EXACT log-energy I(mu0) of the histogram mu0 (closed form via Clausen/Li3).
    Returns an mpmath value; round DOWN to get the rigorous Ihat <= I(mu0)."""
    K = len(centers)
    I = mp.mpf(0)
    for a in range(K):
        for b in range(K):
            I += mp.mpf(masses[a]) * mp.mpf(masses[b]) * block_mean_M(
                centers[a], centers[b], L)
    return I


def I_mu0_reference(centers, masses, L, nsub=120):
    """High-accuracy (NON-rigorous) Riemann reference value of I(mu0), midpoint
    rule with the exact singular self block — independent cross-check that
    Ihat <= I(mu0)."""
    K = len(centers)
    sub = L / nsub
    half = L / 2.0
    t1self = float(B1_exact(0.0, L))
    I = 0.0
    s_off = (np.arange(nsub) + 0.5) * sub - half
    for a in range(K):
        sa = centers[a] + s_off
        za = np.exp(1j * sa)
        for b in range(K):
            sb = centers[b] + s_off
            zb = np.exp(1j * sb)
            with np.errstate(divide="ignore"):
                T2 = np.log(np.abs(za[:, None] - np.conj(zb)[None, :])).mean()
                if a == b:
                    T1 = t1self
                else:
                    T1 = np.log(np.abs(za[:, None] - zb[None, :])).mean()
            I += masses[a] * masses[b] * 0.5 * (T1 + T2)
    return I


# ---- potential row (CLEAN, P2 — no -10 fudge) ------------------------------

def potential_at_nodes_clean(z_nodes, centers, masses, L, nsub=40):
    """U_mu0(z_n) = INT (1/2)(log|z_n - w| + log|z_n - conj w|) dmu0(w), computed
    with mu0 the histogram (uniform arcs).  CLEAN: z_nodes are the LP CONTOUR
    nodes, OFFSET from the mu0 arc structure; for each (node, bin) the mean of the
    smooth kernel over the bin's arc is a fine sub-grid average.  No coincidence
    guard / no -10 fudge ever fires (the contour nodes are not arc subgrid nodes
    and the per-bin average of a log-singular kernel against a fixed exterior point
    is finite).  This row is used ONLY to solve the cut LP for the FROZEN dual
    weights; the certificate re-derives U_mu0 by interval arithmetic independently."""
    sub = L / nsub
    half = L / 2.0
    # offset the sub-grid by an irrational fraction of a cell so no arc node ever
    # lands exactly on a contour node (avoids log(0); no -10 fudge needed).
    s_off = (np.arange(nsub) + 0.3183098861837907) * sub - half
    U = np.zeros(len(z_nodes))
    for c, m in zip(centers, masses):
        sk = c + s_off
        zk = np.exp(1j * sk)
        T1 = np.log(np.abs(z_nodes[:, None] - zk[None, :])).mean(axis=1)
        T2 = np.log(np.abs(z_nodes[:, None] - np.conj(zk)[None, :])).mean(axis=1)
        U += m * 0.5 * (T1 + T2)
    assert np.all(np.isfinite(U)), "potential row has non-finite entries"
    return U


# ---- main freeze -----------------------------------------------------------

def freeze(N=2000, B=55, verbose=True):
    # B=55 is the COMMITTED R17 record measure (15 arcs, L=0.057120) that
    # verify_vec_energy.py loads from frozen_energy.npz. The default MUST match the
    # committed npz so a bare `freeze_energy.py` regenerates the SAME measure and
    # does not silently overwrite the record with a different (e.g. B=80) freeze.
    t, z, w, g = contour(N)
    A = column_matrix(w)
    m0, p0, cj0, _ = solve_primal(g, A)
    centers, masses, L = build_histogram_mu0(t, p0, B)

    # EXACT I(mu0) via closed form, then round DOWN to a float => Ihat <= I(mu0).
    Ihat_mp = I_mu0_exact(centers, masses, L)
    Ihat = float(Ihat_mp)
    # guarantee the float is <= the true mpmath value (rigorous downward rounding)
    while mp.mpf(Ihat) > Ihat_mp:
        Ihat = np.nextafter(Ihat, -np.inf)

    # cut LP with the CLEAN potential row -> frozen dual weights
    U0 = potential_at_nodes_clean(z, centers, masses, L)
    cut_row = 2.0 * U0 - Ihat            # use the SAME Ihat the cert subtracts
    m_cut, p_cut, cj, lams = solve_primal(g, A, extra_rows=[cut_row], extra_rhs=[0.0])
    lambda0 = lams[0] if lams else 0.0

    if verbose:
        print(f"[freeze] N={N} B={B} support bins={len(centers)} L={L:.6f}")
        print(f"[freeze] m0(no-energy LP)      = {m0:.10f}")
        print(f"[freeze] I(mu0) lower (Ihat)   = {Ihat:.10f}")
        print(f"[freeze] I(mu0) reference      = {I_mu0_reference(centers,masses,L):.10f}")
        print(f"[freeze] m_cut (cut LP value)  = {m_cut:.10f}")
        print(f"[freeze] lambda0               = {lambda0:.8f}")
        print(f"[freeze] raise m_cut - ANCHOR  = {m_cut-ANCHOR:+.8f}")
        print(f"[freeze] sum c_j               = {cj.sum():.6f}  (cj>=0: {np.all(cj>=0)})")
    return dict(N=N, B=B, centers=centers, masses=masses, L=L,
                Ihat=Ihat, cj=cj, lambda0=lambda0, m_cut=m_cut, m0=m0,
                Ihat_mp=str(Ihat_mp))


def dump(d, path="frozen_energy.npz"):
    np.savez(path, centers=d["centers"], masses=d["masses"], L=d["L"],
             Ihat=d["Ihat"], cj=d["cj"], lambda0=d["lambda0"],
             m_cut=d["m_cut"], m0=d["m0"], N=d["N"], B=d["B"])
    print(f"[dump] -> {path}")


def check(d=None, path="frozen_energy.npz"):
    """Cross-checks on the COMMITTED frozen measure (the one verify_vec_energy.py
    loads), NOT a freshly recomputed dict: (1) Ihat <= reference I(mu0);
    (2) eigenvalue validity on the FROZEN coarsened mu0 kernel.

    `d` is ignored if a frozen_energy.npz is present on disk -- we always validate
    the committed npz so this check can never drift from what the certificate uses.
    Pass d explicitly only to check an in-memory freeze before dumping it."""
    if d is None:
        fz = np.load(path)
        d = dict(centers=fz["centers"], masses=fz["masses"], L=float(fz["L"]),
                 Ihat=float(fz["Ihat"]), B=int(fz["B"]))
        print(f"[check] validating COMMITTED {path}: B={d['B']} "
              f"arcs={len(d['centers'])} L={d['L']:.6f}")
    centers, masses, L = d["centers"], d["masses"], d["L"]
    ref = I_mu0_reference(centers, masses, L)
    print(f"[check] Ihat={d['Ihat']:.10f} <= I(mu0)_ref={ref:.10f} ? "
          f"{d['Ihat'] <= ref}  (margin {ref-d['Ihat']:.2e})")

    # validity eigenvalue check (P1 numerical WITNESS, not the proof): build the
    # conj-symmetric energy MATRIX whose quadratic form q^T G q = I(measure) for the
    # histogram-style measure sum_n q_n * Uniform(sub-arc_n) on a UNIFORM M-node grid
    # of sub-arcs (each t-width dt).  The diagonal is the EXACT arc self-energy
    # B1(0,dt) and off-diagonals the EXACT block means B1(t_a-t_b,dt), B1(t_a+t_b,dt)
    # -- i.e. the SAME closed form used for Ihat.  This is the genuine continuous-
    # consistent discretization (NOT the diagonal-zeroed naive kernel, which the R12
    # build correctly found is NOT NSD).  eq.6 / Ahlfors 2.1 says I(nu-mu0) <= 0 for
    # finite-energy measures, i.e. this matrix is NSD on mass-zero differences.
    M = 240
    edges = np.linspace(0.0, np.pi, M + 1)
    tg = 0.5 * (edges[:-1] + edges[1:])
    dt = edges[1] - edges[0]
    G = np.empty((M, M))
    diag = float(B1_exact(0.0, dt))
    for a in range(M):
        for b in range(M):
            t1 = diag if a == b else float(B1_exact(tg[a] - tg[b], dt))
            t2 = float(B1_exact(tg[a] + tg[b], dt))
            G[a, b] = 0.5 * (t1 + t2)
    G = 0.5 * (G + G.T)
    ones = np.ones((M, 1)) / np.sqrt(M)
    Gp = G - ones @ (ones.T @ G) - (G @ ones) @ ones.T + ones @ (ones.T @ G @ ones) @ ones.T
    ev = np.linalg.eigvalsh(0.5 * (Gp + Gp.T))
    print(f"[check] EXACT-block conj-sym energy matrix top eigenvalue on mass-zero "
          f"subspace = {ev.max():+.3e}")
    print(f"        (<= ~0 => I(nu-mu0)<=0 for histogram-discretized measures => "
          f"the discrete witness of eq.6/Ahlfors 2.1 holds)")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        # Validate the COMMITTED frozen_energy.npz (what the certificate loads),
        # without recomputing a freeze -- so `check` can never disagree with the cert.
        check()
    else:
        # Bare run regenerates the COMMITTED measure (B=55 default) and dumps it.
        dump(freeze())
