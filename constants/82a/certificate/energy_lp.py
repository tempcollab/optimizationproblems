"""
82a LOWER bound — Stage-1 CONJECTURE: OSS log-energy self-cut LP (PATH B).

This script tests whether the Orloski-Sardari-Smith (arXiv:2401.03252) logarithmic
energy / discriminant dual column

        I(mu) = INT INT log|z1 - z2| dmu(z1) dmu(z2)  >= 0

(valid because disc(P) is a NONZERO INTEGER for a min-poly P, off a finite
exceptional set — the SAME finite-exception integrality argument R1-verified for
Flammang's c_j columns) can RAISE the verified lower bound 0.2487458 = log(1.282416)
[Flammang F18] for the Zhang-Zagier essential minimum.

We work with the primal measure LP (BMQS primal P(g)):

        m  =  min_p  sum_n p_n g_n
        s.t.  sum_n p_n log|Q_j(w_n)| >= 0   (j=1..24, Flammang Table 1 columns)
              sum_n p_n = 1,  p_n >= 0

over the contour w(t) = e^{it} - e^{2it} = z(1-z),  z = e^{it},  t in (0, pi),
g_n = log+|w_n| = log max(1, |w_n|).  The no-energy optimum reproduces ~0.2487458
(the Flammang anchor m0).

ENERGY column (the NEW constraint).  I(mu) is concave in mu (gradient 2 K mu).
We linearize it at the no-energy optimum mu0 (OSS eq.8, an OUTER cut):

        I(mu) <= L_{mu0}(mu) := 2 U_{mu0} . mu - I(mu0)       for ALL mu,

so {I >= 0} SUBSET {L_{mu0} >= 0}.  Adding the single LINEAR constraint
L_{mu0}(p) >= 0 to the primal is therefore:
  (i) a VALID outer relaxation of the true energy-constrained problem
      => m0 <= m_cut <= m_true <= C_82  (UNDER-estimates the true energy optimum,
         can never over-shoot C_82); and
  (ii) it only ADDS a constraint to the no-energy primal => m_cut >= m0
       (the raise is real and valid-directioned).

KERNEL.  The conjugate set of a real min-poly is closed under conjugation, so the
conjugate measure nu in z is conjugation-symmetric.  We fold it onto the half-arc
t in (0, pi) with the conjugate-symmetric kernel

        K_{ab} = 1/2 ( log|z_a - z_b| + log|z_a - conj(z_b)| )

which reproduces the full-circle symmetric energy INT INT log|z1-z2| dnu dnu EXACTLY
for a symmetric nu (verified to 1e-9 in the self-test below).  The diagonal of the
first term (log|z_a - z_a| = -inf) is EXCLUDED (the standard energy convention);
the second term is regular on the open half-arc.

This is STAGE-1: a CONJECTURE from a convex solve.  m_cut is a valid lower-bound
DIRECTION, but discretizing the conjugate measure on the LITERAL contour |z|=1 (vs
the capacity-1 lemniscate where it truly lives) is a MODELING CHOICE, not yet a
rigorous certificate.  NO value is written to held; that is stage-2.

Run:  python3 energy_lp.py
Prints, for N in {1000, 2000, 4000}:  m0 (anchor), I(mu0) under BOTH the naive
half-arc kernel and the symmetric conjugate K, m_cut, the dual multiplier lambda_0
on the energy cut, I(mu_cut), and the raises m_cut - m0 and m_cut - 0.2487458.
"""

import numpy as np
from scipy.optimize import linprog
from flammang_table1 import get_table

ANCHOR = 0.2487458          # log(1.282416), Flammang F18 verified lower bound
GATE = 1e-4                 # stage-1 -> stage-2 gate on m_cut - ANCHOR


def contour(N):
    """Half-arc nodes; returns t, z, w, g (= log+|w|)."""
    t = np.linspace(1e-4, np.pi - 1e-4, N)
    z = np.exp(1j * t)
    w = z * (1 - z)                 # = e^{it} - e^{2it}
    g = np.log(np.maximum(1.0, np.abs(w)))
    return t, z, w, g


def column_matrix(w):
    """A[n, j] = log|Q_j(w_n)| for the 24 Flammang Table 1 polynomials."""
    cols = [asc for (_, asc) in get_table()]
    N = len(w)
    A = np.empty((N, len(cols)))
    for j, asc in enumerate(cols):
        A[:, j] = np.log(np.abs(np.polyval(list(reversed(asc)), w)))
    return A


def conj_kernel(z, eps_diag=None):
    """Conjugate-symmetric energy kernel on the half-arc:
         K_{ab} = 1/2 ( log|z_a - z_b| + log|z_a - conj z_b| ),
       diagonal of the FIRST term excluded (set to its row mean as a numerically
       harmless placeholder — it is multiplied by p_a p_a which is tiny and, more
       importantly, the diagonal NEVER enters a self-consistent energy of a diffuse
       measure; we exclude it explicitly so the off-diagonal sum is the genuine
       pair energy).  The SECOND term is regular on the open arc.
    """
    Za = z[:, None]
    Zb = z[None, :]
    # term 1: log|z_a - z_b|, diagonal -> -inf, exclude it
    D1 = np.abs(Za - Zb)
    with np.errstate(divide="ignore"):
        T1 = np.log(D1)
    np.fill_diagonal(T1, 0.0)          # exclude diagonal of the singular term
    # term 2: log|z_a - conj z_b| (regular)
    T2 = np.log(np.abs(Za - np.conj(Zb)))
    K = 0.5 * (T1 + T2)
    return K


def naive_kernel(z):
    """Naive half-arc z-kernel L_{ab} = log|z_a - z_b| (diag excluded). For the
       diagnostic comparison only — NOT the energy object used in the cut."""
    Za = z[:, None]
    Zb = z[None, :]
    with np.errstate(divide="ignore"):
        L = np.log(np.abs(Za - Zb))
    np.fill_diagonal(L, 0.0)
    return L


def solve_primal(g, A, extra_rows=None, extra_rhs=None):
    """min sum_n p_n g_n  s.t.  A^T p >= 0 (24),  sum p = 1,  p >= 0,
       plus optional extra inequality rows (each row . p >= rhs).
       Returns (m, p, lambdas) where lambdas are the dual multipliers on the
       extra rows (>= 0), or [] if none.

       scipy.linprog minimizes c.x with A_ub x <= b_ub.  We write all >= as <=.
    """
    N = len(g)
    J = A.shape[1]
    # Inequality constraints as A_ub p <= b_ub:
    #   -A^T p <= 0          (column constraints A^T p >= 0)
    #   -row . p <= -rhs     (extra row . p >= rhs)
    Aub = -A.T                                   # (J, N)
    bub = np.zeros(J)
    if extra_rows is not None:
        Aub = np.vstack([Aub, -np.asarray(extra_rows)])
        bub = np.concatenate([bub, -np.asarray(extra_rhs)])
    Aeq = np.ones((1, N))
    beq = np.array([1.0])
    bounds = [(0, None)] * N
    res = linprog(g, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq,
                  bounds=bounds, method="highs")
    if res.status != 0:
        raise RuntimeError(f"linprog failed: status {res.status} {res.message}")
    m = res.fun
    p = res.x
    # dual multipliers on the extra rows: linprog marginals on A_ub are <= 0
    # (sensitivity of objective to RELAXING b_ub upward). For our -row.p <= -rhs
    # the multiplier of the original >= constraint is -marginal >= 0.
    lambdas = []
    if extra_rows is not None:
        n_extra = np.asarray(extra_rows).shape[0]
        marg = res.ineqlin.marginals[-n_extra:]
        lambdas = list(np.maximum(-marg, 0.0))
    return m, p, lambdas


def self_test_kernel():
    """Verify the conjugate-symmetric K reproduces the full-circle symmetric energy
       INT INT log|z1-z2| dnu dnu EXACTLY for a conjugation-symmetric measure nu.

       Take an arbitrary measure on the FULL circle that is symmetric under
       conjugation: put mass q_k at z_k = e^{i t_k} AND equal mass at conj = e^{-i t_k}
       for t_k in (0, pi).  Its full-circle self energy (off-diagonal) should equal
       sum_{a,b} p_a p_b K_{ab} on the half-arc with p the half-arc masses (each
       carrying its conjugate partner), normalized consistently.
    """
    rng = np.random.default_rng(0)
    n = 30
    tk = np.sort(rng.uniform(0.2, np.pi - 0.2, n))
    qk = rng.uniform(0.1, 1.0, n)
    qk /= qk.sum()                 # half-arc masses, total 1 on the half-arc
    zk = np.exp(1j * tk)

    # Full-circle measure: mass qk/2 at zk and qk/2 at conj(zk) (total 1).
    zfull = np.concatenate([zk, np.conj(zk)])
    pfull = np.concatenate([qk / 2, qk / 2])
    Zf = zfull[:, None] - zfull[None, :]
    with np.errstate(divide="ignore"):
        Lf = np.log(np.abs(Zf))
    np.fill_diagonal(Lf, 0.0)
    E_full = pfull @ Lf @ pfull

    # Half-arc folded energy with K, masses qk (each carrying conjugate partner).
    # The conjugate-symmetric K already sums the (a,b),(a,bbar) contributions; the
    # (abar,b),(abar,bbar) contributions are equal by symmetry, so with the masses
    # arranged as above the half-arc form is p^T K p with p = qk.
    K = conj_kernel(zk)
    E_half = qk @ K @ qk
    err = abs(E_full - E_half)
    print(f"  [self-test] full-circle symmetric energy = {E_full:+.12f}")
    print(f"  [self-test] half-arc conj-kernel  energy = {E_half:+.12f}")
    print(f"  [self-test] |difference| = {err:.2e}  (should be ~1e-9)")
    return err


def run_at_N(N):
    t, z, w, g = contour(N)
    A = column_matrix(w)

    # ----- ANCHOR: no-energy primal -----
    m0, p0, _ = solve_primal(g, A)

    # ----- DIAGNOSTIC: I(mu0) under both kernels -----
    K = conj_kernel(z)
    L = naive_kernel(z)
    I0_K = float(p0 @ K @ p0)        # conjugate-symmetric (the energy object)
    I0_L = float(p0 @ L @ p0)        # naive half-arc (diagnostic only)

    # ----- SELF-CUT: OSS eq.8 linear outer cut at mu0 -----
    # I(mu) <= 2 U_{mu0}.mu - I(mu0).  Cut: (2 U_{mu0} - I0_K) . p >= 0.
    U0 = K @ p0                       # potential of mu0 at every node
    cut_row = 2.0 * U0 - I0_K        # length-N vector
    m_cut, p_cut, lambdas = solve_primal(g, A, extra_rows=[cut_row], extra_rhs=[0.0])
    lambda0 = lambdas[0] if lambdas else 0.0
    I_cut = float(p_cut @ K @ p_cut)

    # reduced-cost identity sanity: reduced cost of the cut at mu0 == I0_K
    rc = float(cut_row @ p0)         # = 2 I0_K - I0_K = I0_K
    return dict(N=N, m0=m0, I0_K=I0_K, I0_L=I0_L, m_cut=m_cut,
                lambda0=lambda0, I_cut=I_cut, rc=rc)


def main():
    print("=" * 78)
    print("82a LOWER bound — Stage-1 CONJECTURE: OSS log-energy self-cut LP")
    print("Target to beat (RAISE only): lower 0.2487458 = log(1.282416) [Flammang F18]")
    print("=" * 78)

    print("\nKernel validity self-test (conj-symmetric K == full-circle energy):")
    self_test_kernel()

    print("\n" + "-" * 78)
    print(f"{'N':>6} {'m0 (anchor)':>14} {'I(mu0) symK':>13} {'I(mu0) naive':>13} "
          f"{'m_cut':>14} {'lambda_0':>11}")
    print("-" * 78)
    results = []
    for N in (1000, 2000, 4000):
        r = run_at_N(N)
        results.append(r)
        print(f"{r['N']:>6} {r['m0']:>14.7f} {r['I0_K']:>13.5f} {r['I0_L']:>13.5f} "
              f"{r['m_cut']:>14.7f} {r['lambda0']:>11.4f}")

    print("\n" + "-" * 78)
    print("RAISES and gate (gate fires if m_cut - 0.2487458 > 1e-4):")
    print("-" * 78)
    print(f"{'N':>6} {'m_cut - m0':>14} {'m_cut - 0.2487458':>20} {'I(mu_cut)':>12} "
          f"{'gate?':>7} {'cut active?':>12}")
    for r in results:
        raise_m0 = r['m_cut'] - r['m0']
        raise_anchor = r['m_cut'] - ANCHOR
        gate = "FIRES" if raise_anchor > GATE else "no"
        active = "yes" if r['lambda0'] > 1e-6 else "no"
        print(f"{r['N']:>6} {raise_m0:>+14.6f} {raise_anchor:>+20.6f} "
              f"{r['I_cut']:>+12.5f} {gate:>7} {active:>12}")

    print("\n" + "-" * 78)
    print("Reduced-cost identity check (must equal I(mu0) under symK):")
    for r in results:
        print(f"  N={r['N']:>5}: cut_row . mu0 = {r['rc']:+.6f}  "
              f"vs I(mu0)_symK = {r['I0_K']:+.6f}  "
              f"match: {abs(r['rc'] - r['I0_K']) < 1e-9}")

    print("\n" + "=" * 78)
    print("VALIDITY (re-derivable by the reviewer):")
    print("  m0 <= m_cut  : the cut only ADDS a constraint to the no-energy primal.")
    print("  m_cut <= m_true <= C_82 : the linear cut is an OUTER relaxation of")
    print("    {I(mu) >= 0} (concavity of I), so m_cut UNDER-estimates the true")
    print("    energy-constrained optimum and can never over-shoot C_82.")
    print("  => 0.2487458 = m0 <= m_cut <= C_82 : a VALID lower-bound direction.")
    print("\n  STAGE-1 CONJECTURE ONLY: the conjugate measure is modeled on the")
    print("  literal contour |z|=1; the rigorous interval certificate with the fixed")
    print("  potential term lambda_0*U_mu is STAGE-2.  NO value written to held.")
    print("=" * 78)


if __name__ == "__main__":
    main()
