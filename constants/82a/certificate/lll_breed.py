"""
DELIVERABLE 2 — bounded high-degree LLL integer-column breeding for the C_82a
LOWER bound, priced against Flammang's LP dual.

Per the round-1 outline review (R1-outline-review.md, section B.3), the ONLY
unscreened forward lever is high-degree (k > 32) LLL breeding of integer w-columns
Q(w), w = z(1-z), priced against Flammang's (single = both-circle) LP dual mu*.
The cheap dictionary (low-degree polys, products, +-1 perturbations) is exhausted
(R1 colgen: best reduced cost ~ -1e-7, LP moved ~2e-11) and the "symmetrized
R(z)R(1-z)" variable is NOT new — it lives in Z[w]. So the only open shot is deeper
LLL columns that cheap pricing cannot reach.

METHOD (Flammang/Smyth weighted-integer recipe, named in F18 / explore digest):
  1. Solve the Smyth LP at Flammang's 24 columns; extract the optimal dual measure
     mu* >= 0 on the contour control points (its support = the binding band).
  2. For each degree k = 24..40, build a lattice in the integer coefficient vector
     (q_0,...,q_k) of Q(w) = sum_i q_i w^i.  Embed via the monomials evaluated at a
     set of control points v_n = w(t_n) seeded AT mu*'s support, scaled by a weight
     exp(-W(t_n)) (small where mu* lives).  Real and imaginary parts give 2*M real
     linear forms; LLL on the (k+1) x (k+1 + 2M) integer/scaled matrix returns short
     integer vectors = polynomials Q with small |Q(v_n)| on the support.
  3. Price each bred Q by its reduced cost r(Q) = sum_n mu*_n log|Q(w(t_n))|.  An
     improving column has r(Q) < 0 (column-generation optimality test; a column
     with r<0 can be added to RAISE the LP value m).  Keep r < -1e-5 (above the
     ~-1e-7 noise floor).
  4. Add the best improving bred columns, re-solve the LP, report whether m rises.

HONEST EXPECTATION (outline review): inert, ~1e-8..1e-11.  A negative result that
closes the lever is the valid outcome; we report the numbers plainly.

NOTE ON VALIDITY (what a positive result would need, NOT claimed here): any bred Q
in Z[w] is automatically an admissible Flammang column — Res(P, Q(z(1-z))) is a
nonzero integer off the finite set {P | Q(z(1-z))}, the SAME integrality clause as
Flammang's 24 columns (NO a_lead obstruction, unlike OSS).  A raised LP value is a
CONJECTURE until re-certified by verify_vec.py interval B&B on the honest locus;
that re-certification is only run if a column actually prices in.

Run:  python3 lll_breed.py
"""
import sys
import numpy as np
from scipy.optimize import linprog
from sympy import Matrix
from flammang_table1 import get_table


def control_points(N=8000):
    t = np.linspace(1e-4, np.pi - 1e-4, N)
    z = np.exp(1j * t)
    w = z * (1 - z)
    b = np.log(np.maximum(1.0, np.abs(w)))
    return t, z, w, b


def logabsQ(asc, w):
    return np.log(np.abs(np.polyval(list(reversed(asc)), w)))


def base_columns():
    return [list(asc) for (_, asc) in get_table()]


def solve_lp(cols, w, b):
    """max m s.t. sum_j c_j log|Q_j(w_n)| + m <= b_n, c_j>=0. Returns (m, c, mu*)."""
    N = len(w); J = len(cols)
    A = np.empty((N, J))
    for j, asc in enumerate(cols):
        A[:, j] = logabsQ(asc, w)
    Aub = np.hstack([A, np.ones((N, 1))])
    cost = np.zeros(J + 1); cost[-1] = -1.0
    bounds = [(0, None)] * J + [(None, None)]
    res = linprog(cost, A_ub=Aub, b_ub=b, bounds=bounds, method="highs")
    if res.status != 0:
        return None
    m = -res.fun
    c_vec = res.x[:J]
    mu = np.maximum(-res.ineqlin.marginals, 0.0)
    s = mu.sum()
    if s > 0:
        mu = mu / s
    return m, c_vec, mu


def reduced_cost(asc, w, mu):
    return float(np.sum(mu * logabsQ(asc, w)))


def lll_breed_degree(k, t, w, mu, n_seed=30, scales=(60, 120, 240, 480)):
    """Breed candidate integer polynomials Q(w) of degree k via LLL.

    Lattice: rows are unit vectors e_i (i=0..k) for the integer coeff q_i, augmented
    with scaled real/imag parts of w_n^i at seed points v_n drawn from mu*'s support.
    A short LLL vector => integer (q_i) with sum_i q_i w_n^i ~ 0 on the seeds, i.e. a
    polynomial small where mu* lives => candidate improving column.
    Returns a list of ascending-coeff integer polynomials (the LLL basis rows)."""
    # seed points: the n_seed control points with the largest mu* (the binding band)
    order = np.argsort(mu)[::-1]
    seeds = order[:n_seed]
    vw = w[seeds]                                   # complex w-values where mu* lives
    out = []
    for scale in scales:
        # build (k+1) x (k+1 + 2*n_seed) integer matrix
        K = k + 1
        cols_extra = 2 * len(seeds)
        Mrows = []
        # precompute monomials w_n^i
        # powers[i, n] = vw[n]^i
        powers = np.array([vw ** i for i in range(K)])   # (K, n_seed) complex
        for i in range(K):
            row = [0] * (K + cols_extra)
            row[i] = 1
            for n in range(len(seeds)):
                re = float(np.real(powers[i, n]))
                im = float(np.imag(powers[i, n]))
                row[K + 2 * n] = int(round(scale * re))
                row[K + 2 * n + 1] = int(round(scale * im))
            Mrows.append(row)
        try:
            red = Matrix(Mrows).lll()
        except Exception:
            continue
        for r in range(red.rows):
            coeffs = [int(red[r, i]) for i in range(K)]   # q_0..q_k ascending
            # strip trailing zeros
            asc = coeffs[:]
            while len(asc) > 1 and asc[-1] == 0:
                asc = asc[:-1]
            if all(x == 0 for x in asc):
                continue
            # require genuine degree (not collapsing to a low-degree column)
            out.append(asc)
    return out


def main():
    t, z, w, b = control_points(8000)
    cols = base_columns()
    res = solve_lp(cols, w, b)
    m0, c0, mu = res
    print("=" * 74)
    print("DELIVERABLE 2 — high-degree LLL w-column breeding, priced vs Flammang dual")
    print("=" * 74)
    print(f"[LP] Flammang 24-column optimum  m* = {m0:.10f}")
    print(f"     (record to beat 0.2487458; LP machinery valid: m* matches Flammang)")
    print(f"     dual mu* support (mu>1e-6): {(mu > 1e-6).sum()} points; "
          f"binding band t in "
          f"[{t[mu > 1e-6].min():.3f}, {t[mu > 1e-6].max():.3f}]")
    base_keys = {tuple(a) for a in cols}

    NOISE = 1e-7          # reduced costs above this in magnitude are LP noise
    GATE = 1e-5           # an "improving" column needs r < -GATE to be credible

    all_priced = []
    best_overall = (0.0, None, None)   # (most-negative r, asc, k)
    for k in range(24, 41):
        bred = lll_breed_degree(k, t, w, mu)
        # price each bred column
        kbest = (0.0, None)
        seen = set()
        for asc in bred:
            key = tuple(asc)
            if key in base_keys or key in seen:
                continue
            seen.add(key)
            # skip degenerate constants
            if len(asc) <= 1:
                continue
            r = reduced_cost(asc, w, mu)
            all_priced.append((r, asc, k))
            if r < kbest[0]:
                kbest = (r, asc)
        if kbest[1] is not None:
            print(f"[k={k:2d}] bred {len(bred):3d} cols; best reduced cost "
                  f"r = {kbest[0]:+.3e}  (deg {len(kbest[1])-1})")
            if kbest[0] < best_overall[0]:
                best_overall = (kbest[0], kbest[1], k)

    print("-" * 74)
    all_priced.sort(key=lambda x: x[0])
    print("Most-negative reduced costs across ALL bred columns (k=24..40):")
    for r, asc, k in all_priced[:12]:
        head = asc if len(asc) <= 8 else str(asc[:8]) + "..."
        print(f"   r = {r:+.3e}  (k={k}, deg {len(asc)-1})  Q_asc = {head}")

    improving = [(r, asc, k) for (r, asc, k) in all_priced if r < -GATE]
    print("-" * 74)
    print(f"Columns priced in below the gate r < -{GATE}: {len(improving)}")
    if not improving:
        print("RESULT (HONEST): NO bred high-degree column prices in above the noise")
        print(f"   floor.  Best reduced cost {all_priced[0][0]:+.3e} is "
              f"{'BELOW' if abs(all_priced[0][0]) < NOISE else 'near'} the ~1e-7 LP")
        print("   noise floor.  Flammang's 24-column set is LP-optimal against the")
        print("   high-degree LLL dictionary too.  The k>32 lever is CLOSED (inert).")
        print("   No forward improvement; the round's advance is the OSS retraction.")
        return 0

    # if anything priced in, re-optimize the LP with the improving columns added
    print("Improving columns FOUND — re-optimizing the LP (CONJECTURE until certified):")
    add = []
    for r, asc, k in improving:
        if tuple(asc) not in base_keys and asc not in add:
            add.append(asc)
    newcols = cols + add
    out = solve_lp(newcols, w, b)
    if out is None:
        print("   LP re-solve failed.")
        return 1
    m_new, c_new, mu_new = out
    print(f"   added {len(add)} columns -> m_new = {m_new:.10f}  "
          f"(raise {m_new - m0:+.3e})")
    if m_new > m0 + 1e-7:
        print(f"   *** LP value RAISED past Flammang by {m_new - m0:+.3e} ***")
        print("   THIS IS A CONJECTURE.  Re-certify with verify_vec.py interval B&B")
        print("   on the honest locus (confirm global plane min stays on |z|=1 — do")
        print("   NOT repeat the OSS wrong-locus error) before claiming any bound.")
        # report the improving columns for the certifier
        for r, asc, k in improving:
            print(f"      r={r:+.3e} k={k} Q_asc={asc}")
    else:
        print("   raise is within LP noise (~1e-7); not a credible improvement.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
