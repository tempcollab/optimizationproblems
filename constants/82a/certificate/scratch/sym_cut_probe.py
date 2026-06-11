"""
SYMMETRIZED-CUT probe for 82a (R-investigation).

Tests "symmetrize the CUT not the MEASURE": take a STRONG asymmetric histogram
mu0 (the no-energy-optimum histogram, B bins) and use the z->1-z symmetric cut

    cut_sym(z) = E(z) + E(1-z),   E(z) = 2 U_mu0(z) - Ihat

in the Flammang primal LP, with one (or two) lambda>=0 multipliers.

U_mu0(z) = INT (1/2)(log|z-w| + log|z-conj w|) dmu0(w)   [conj-symmetric kernel,
the genuine z-plane log potential of the conj-symmetric measure mu0 built on |z|=1].

We need U_mu0 at the contour nodes z_n=e^{it_n} AND at 1-z_n (off |z|=1).
"""
import numpy as np
from scipy.optimize import linprog
import mpmath as mp
from flammang_table1 import get_table
from freeze_energy import (contour, column_matrix, build_histogram_mu0,
                           I_mu0_exact, solve_primal)

ANCHOR = 0.2487458


def U_potential_at(z_eval, centers, masses, L, nsub=80):
    """U_mu0(z) = INT 1/2(log|z-w|+log|z-conj w|) dmu0(w), mu0 = sum mass_k Uniform(arc_k),
    arcs of t-width L centered at centers (on |z|=1).  z_eval may be ANY complex points
    (on or off |z|=1).  Per-bin mean over its arc via a fine offset sub-grid."""
    z_eval = np.asarray(z_eval, dtype=complex)
    sub = L / nsub
    half = L / 2.0
    s_off = (np.arange(nsub) + 0.3183098861837907) * sub - half
    U = np.zeros(len(z_eval))
    for c, m in zip(centers, masses):
        sk = c + s_off
        zk = np.exp(1j * sk)
        T1 = np.log(np.abs(z_eval[:, None] - zk[None, :])).mean(axis=1)
        T2 = np.log(np.abs(z_eval[:, None] - np.conj(zk)[None, :])).mean(axis=1)
        U += m * 0.5 * (T1 + T2)
    return U


def solve_two_cut(g, A, rows, rhs):
    """Like solve_primal but returns also dual lambdas per extra row."""
    N = len(g); J = A.shape[1]
    Aub = -A.T; bub = np.zeros(J)
    n_extra = len(rows)
    Aub = np.vstack([Aub, -np.asarray(rows)])
    bub = np.concatenate([bub, -np.asarray(rhs)])
    Aeq = np.ones((1, N)); beq = np.array([1.0])
    res = linprog(g, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq,
                  bounds=[(0, None)] * N, method="highs")
    if res.status != 0:
        raise RuntimeError(res.message)
    marg = res.ineqlin.marginals
    cj = np.maximum(-marg[:J], 0.0)
    lams = list(np.maximum(-marg[J:J + n_extra], 0.0))
    return res.fun, res.x, cj, lams


def build_cut_rows(z_nodes, centers, masses, L, Ihat):
    """Return E(z_n), E(1-z_n), and the symmetrized row E(z_n)+E(1-z_n)."""
    Uz = U_potential_at(z_nodes, centers, masses, L)
    U1mz = U_potential_at(1.0 - z_nodes, centers, masses, L)
    Ez = 2.0 * Uz - Ihat
    E1mz = 2.0 * U1mz - Ihat
    return Ez, E1mz, Ez + E1mz


def run_for_B(B, N=2000, verbose=True):
    t, z, w, g = contour(N)
    A = column_matrix(w)
    m0, p0, cj0, _ = solve_primal(g, A)
    centers, masses, L = build_histogram_mu0(t, p0, B)
    Ihat_mp = I_mu0_exact(centers, masses, L)
    Ihat = float(Ihat_mp)
    while mp.mpf(Ihat) > Ihat_mp:
        Ihat = np.nextafter(Ihat, -np.inf)

    Ez, E1mz, Esym = build_cut_rows(z, centers, masses, L, Ihat)

    # (a) single-sided cut E(z) only (the original OSS, asymmetric) -- for reference
    m_single, _, _, lam_single = solve_two_cut(g, A, [Ez], [0.0])
    # (b) symmetrized cut (single multiplier on E(z)+E(1-z))
    m_sym, p_sym, cj_sym, lam_sym = solve_two_cut(g, A, [Esym], [0.0])
    # (c) two separate multipliers
    m_two, p_two, cj_two, lams_two = solve_two_cut(g, A, [Ez, E1mz], [0.0, 0.0])

    out = dict(B=B, L=L, narcs=len(centers), m0=m0, Ihat=Ihat,
               m_single=m_single, lam_single=lam_single[0],
               m_sym=m_sym, lam_sym=lam_sym[0], cj_sym=cj_sym, p_sym=p_sym,
               m_two=m_two, lams_two=lams_two,
               centers=centers, masses=masses)
    if verbose:
        print(f"B={B:3d} arcs={len(centers):2d} L={L:.5f} Ihat={Ihat:+.5f} | "
              f"m0={m0:.7f} | single E(z) m={m_single:.7f} lam={lam_single[0]:.3f} | "
              f"SYM m={m_sym:.7f} lam={lam_sym[0]:.3f} | "
              f"two-lam m={m_two:.7f} lams={[f'{x:.3f}' for x in lams_two]}")
        print(f"        raise(sym - anchor) = {m_sym-ANCHOR:+.7f}")
    return out


if __name__ == "__main__":
    print("=" * 90)
    print("SYMMETRIZED-CUT LP (E(z)+E(1-z)), strong asymmetric histogram mu0")
    print(f"anchor (Flammang) = {ANCHOR}")
    print("=" * 90)
    results = {}
    for B in (45, 50, 55, 60, 70, 80):
        results[B] = run_for_B(B)
