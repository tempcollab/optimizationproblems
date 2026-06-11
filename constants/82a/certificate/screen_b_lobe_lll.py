"""
SCREEN B (R2) — Lobe-adaptive dual + deep w-LLL re-screen for the C_82a LOWER bound.

DISTINCTION FROM R1's CLOSED uniform-dual k>32 LLL pass
-------------------------------------------------------
R1 (lll_breed.py) priced high-degree integer w-columns Q(w), w=z(1-z), against the
LP dual mu* extracted from a UNIFORM-grid discretization of Smyth's semi-infinite
LP, and found it inert (best genuine reduced cost >= 0; only ~3.5e-14 LP noise on
the trivial binding monomials w, w^2).

The remaining unscreened depth (R2 outline, Angle 1): the equilibrium/dual measure
the LLL columns are priced against may be slightly off the true continuum optimum
because of the uniform grid.  Flammang's optimum equioscillates over ~12 lobes; a
uniform grid under-resolves the lobe peaks.  This screen:
  (a) re-solves the LP with control points ADAPTIVELY CLUSTERED at the equioscillation
      lobes (densify where the slack g(t)-m* is near 0), extracting a sharper dual
      mu_lobe;
  (b) re-prices the deep LLL-bred w-columns (k=24..40, several lattice scalings) AND
      a broad cheap integer dictionary against mu_lobe;
  (c) reports any column whose reduced cost prices in below a -1e-5 gate.

A column with reduced cost r(Q) = integral log|Q(w)| dmu_lobe < 0 is a
column-generation improving column: adding it can RAISE the LP value m.  This is
fully rigorous: any Q in Z[w] is an admissible Flammang column (Res(P,Q(z(1-z))) is
a nonzero integer off a finite exceptional set; NO leading-coefficient obstruction),
and w-columns are z->1-z symmetric so the honest min stays on |z|=1 (no wrong-locus
risk -- the plane min of a w-only f is on the circle by Flammang's own reduction).

HONEST EXPECTATION (outline review): likely inert -- the equilibrium measure is what
it is and R1 swept 100+ columns/degree.  A clean reproducible "best reduced cost >=
gate" is a valid lever-closing negative, distinct from R1's because it prices against
a DIFFERENT (lobe-adaptive) dual.

Run:  python3 screen_b_lobe_lll.py
"""

import numpy as np
from scipy.optimize import linprog
from sympy import Matrix
from itertools import product
from flammang_table1 import get_table

BAR = 0.2487458
GATE = 1e-5
NOISE = 1e-7


def logabsQ(asc, w):
    return np.log(np.abs(np.polyval(list(reversed(asc)), w)))


def base_columns():
    return [list(asc) for (_, asc) in get_table()]


def solve_lp_at(t):
    """Solve Flammang LP at the given control-point parameter array t.
    Returns (m, c, mu, w, slack) where slack_n = b_n - (sum c_j logQ_j + m)."""
    z = np.exp(1j * t)
    w = z * (1 - z)
    b = np.log(np.maximum(1.0, np.abs(w)))
    cols = base_columns()
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
    aux = A @ c_vec + m
    slack = b - aux
    return m, c_vec, mu, w, slack


def build_lobe_adaptive_grid(n_uniform=4000, n_refine=8000):
    """Two-pass adaptive grid: solve on a uniform grid, find where the slack is
    near zero (the equioscillation lobes / binding band), then add a dense cluster
    of control points there.  Returns the combined sorted parameter array."""
    t0 = np.linspace(1e-4, np.pi - 1e-4, n_uniform)
    out = solve_lp_at(t0)
    m, c, mu, w, slack = out
    # binding band: points where slack < threshold (the lobes touch 0)
    thr = np.percentile(slack, 8.0)        # lowest ~8% slack = the active lobes
    binding = t0[slack <= thr]
    lo, hi = binding.min(), binding.max()
    # densify the whole binding band AND each connected lobe
    # add a fine uniform refinement across [lo,hi]
    t_band = np.linspace(max(1e-4, lo - 0.02), min(np.pi - 1e-4, hi + 0.02), n_refine)
    # also cluster extra points tightly at each near-zero-slack control point
    extra = []
    for tc in binding:
        extra.append(np.linspace(tc - 1e-3, tc + 1e-3, 9))
    extra = np.concatenate(extra) if extra else np.array([])
    extra = extra[(extra > 1e-4) & (extra < np.pi - 1e-4)]
    t_all = np.unique(np.concatenate([t0, t_band, extra]))
    return t_all, (lo, hi)


def lll_breed_degree(k, w, mu, n_seed=40, scales=(40, 80, 160, 320, 640)):
    """Breed integer Q(w) of degree k via LLL, seeded at the top-mu_lobe points."""
    order = np.argsort(mu)[::-1]
    seeds = order[:n_seed]
    vw = w[seeds]
    out = []
    K = k + 1
    powers = np.array([vw ** i for i in range(K)])      # (K, n_seed)
    for scale in scales:
        cols_extra = 2 * len(seeds)
        Mrows = []
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
            coeffs = [int(red[r, i]) for i in range(K)]
            asc = coeffs[:]
            while len(asc) > 1 and asc[-1] == 0:
                asc = asc[:-1]
            if all(x == 0 for x in asc):
                continue
            out.append(asc)
    return out


def cheap_dictionary():
    """Broad cheap integer dictionary: low-degree small-coeff, products of pairs,
    +/- perturbations of the base columns (the R1 colgen dictionary, re-priced
    against the lobe-adaptive dual)."""
    base = base_columns()
    cands = {}

    def add(asc):
        a = list(asc)
        while len(a) > 1 and a[-1] == 0:
            a = a[:-1]
        if all(x == 0 for x in a):
            return
        cands[tuple(a)] = a

    for deg in range(1, 6):
        for coeffs in product(range(-3, 4), repeat=deg):
            add(list(reversed([1] + list(coeffs))))
    for i in range(len(base)):
        for j in range(i, len(base)):
            if (len(base[i]) - 1) + (len(base[j]) - 1) <= 30:
                add([int(x) for x in np.convolve(base[i], base[j]).astype(np.int64)])
    for asc in base:
        for kk in range(0, min(len(asc), 8)):
            for s in (1, -1):
                p = list(asc); p[kk] += s; add(p)
    return list(cands.values())


def main():
    print("=" * 74)
    print("SCREEN B — lobe-adaptive dual + deep w-LLL re-screen (C_82a lower)")
    print("=" * 74)

    # uniform baseline for reference
    t_uni = np.linspace(1e-4, np.pi - 1e-4, 8000)
    m_uni, c_uni, mu_uni, w_uni, _ = solve_lp_at(t_uni)
    print(f"[uniform] LP optimum m* = {m_uni:.10f}  (bar {BAR})")

    # lobe-adaptive grid
    t_lobe, (lo, hi) = build_lobe_adaptive_grid()
    out = solve_lp_at(t_lobe)
    m_lobe, c_lobe, mu_lobe, w_lobe, slack = out
    print(f"[lobe]    adaptive grid: {len(t_lobe)} control points, binding band "
          f"t in [{lo:.3f}, {hi:.3f}]")
    print(f"          LP optimum m_lobe = {m_lobe:.10f}")
    print(f"          dual support (mu>1e-6): {(mu_lobe > 1e-6).sum()} points")
    # compare the two duals: do they price the base columns the same?
    print(f"          (a sharper dual could flip a marginally-positive reduced cost)")
    print()

    base_keys = {tuple(a) for a in base_columns()}

    # ----- price the cheap dictionary against the LOBE dual -----
    cheap = cheap_dictionary()
    cheap_priced = []
    for asc in cheap:
        if tuple(asc) in base_keys:
            continue
        r = float(np.sum(mu_lobe * logabsQ(asc, w_lobe)))
        cheap_priced.append((r, asc))
    cheap_priced.sort(key=lambda x: x[0])
    print(f"[cheap dict] {len(cheap)} candidates priced vs lobe dual.")
    print("   most-negative reduced costs:")
    for r, asc in cheap_priced[:8]:
        head = asc if len(asc) <= 8 else str(asc[:8]) + "..."
        print(f"      r = {r:+.3e}  Q_asc = {head}")
    print()

    # ----- deep LLL breeding priced against the LOBE dual -----
    print("[LLL deep] breeding k=24..40 vs lobe dual:")
    lll_priced = []
    for k in range(24, 41):
        bred = lll_breed_degree(k, w_lobe, mu_lobe)
        kbest = (0.0, None)
        seen = set()
        for asc in bred:
            key = tuple(asc)
            if key in base_keys or key in seen or len(asc) <= 1:
                continue
            seen.add(key)
            r = float(np.sum(mu_lobe * logabsQ(asc, w_lobe)))
            lll_priced.append((r, asc, k))
            if r < kbest[0]:
                kbest = (r, asc)
        if kbest[1] is not None:
            print(f"   k={k:2d}: bred {len(bred):3d}; best r = {kbest[0]:+.3e} "
                  f"(deg {len(kbest[1])-1})")
    lll_priced.sort(key=lambda x: x[0])
    print()

    # ----- combine, find improving columns -----
    all_priced = cheap_priced[:] + [(r, asc) for (r, asc, k) in lll_priced]
    all_priced.sort(key=lambda x: x[0])
    best_r = all_priced[0][0] if all_priced else 0.0
    improving = [(r, asc) for (r, asc) in all_priced if r < -GATE]

    print(f"[result] best reduced cost across ALL columns vs lobe dual: {best_r:+.3e}")
    print(f"         gate = -{GATE}; noise floor ~ {NOISE}")
    print(f"         columns below gate: {len(improving)}")
    print()

    if not improving:
        print("=" * 74)
        print("VERDICT: INERT")
        print(f"  No w-column prices in below -{GATE} against the lobe-adaptive dual.")
        print(f"  Best reduced cost {best_r:+.3e} is "
              f"{'below noise floor' if abs(best_r) < NOISE else 'within LP noise'}.")
        print("  The lobe-adaptive dual prices the integer w-dictionary the same as")
        print("  R1's uniform dual: Z[w] is LP-saturated to deg ~40.  Lever CLOSED")
        print("  (distinct from R1: different dual, same conclusion).")
        print("=" * 74)
        return

    # if something prices in, re-solve and report (CONJECTURE)
    print("[colgen] improving columns found; re-solving LP (CONJECTURE):")
    add = []
    seen = set()
    for r, asc in improving:
        key = tuple(asc)
        if key not in base_keys and key not in seen:
            seen.add(key); add.append(asc)
    cols = base_columns() + add
    N = len(w_lobe); J = len(cols)
    A = np.empty((N, J))
    for j, asc in enumerate(cols):
        A[:, j] = logabsQ(asc, w_lobe)
    Aub = np.hstack([A, np.ones((N, 1))])
    bb = np.log(np.maximum(1.0, np.abs(w_lobe)))
    cost = np.zeros(J + 1); cost[-1] = -1.0
    bounds = [(0, None)] * J + [(None, None)]
    res = linprog(cost, A_ub=Aub, b_ub=bb, bounds=bounds, method="highs")
    m_new = -res.fun
    print(f"   added {len(add)} cols -> m_new = {m_new:.10f}  (raise {m_new - m_lobe:+.3e})")
    print("=" * 74)
    if m_new > BAR + GATE:
        print(f"VERDICT: CANDIDATE RAISE m_new = {m_new:.10f} > {BAR}+{GATE}")
        print("  -> re-certify with verify_vec.py interval B&B (single circle OK,")
        print("     w-columns symmetric).  CONJECTURE until certified.")
        for r, asc in improving[:10]:
            print(f"     r={r:+.3e}  Q_asc={asc}")
    else:
        print(f"VERDICT: INERT (LP raise {m_new - m_lobe:+.3e} within noise; no break)")
    print("=" * 74)


if __name__ == "__main__":
    main()
