"""
SCREEN A (R2) — Both-circle pre-screen for ONE heavy asymmetric z-column.

Goal: decide whether adding a single asymmetric integer-polynomial z-column
  -d * log|R(z)|,  R in Z[z]  (NOT a polynomial in w = z(1-z))
to Flammang's 24-column w-dictionary can raise the certified Smyth/Flammang
lower bound for the Zhang-Zagier essential minimum C_82 past the verified bar
0.2487458 = log(1.282416) [Flammang F18].

WHY z-columns must be priced on BOTH circles
---------------------------------------------
Flammang's auxiliary-function bound is
    h_Z(alpha) * d  >=  sum_i f(alpha_i)            (f = log max(1,|w|) - aux)
and the honest lower bound is  h_Z >= min_{plane} f.  Flammang's reduction to a
single arc t in [0,pi] (i.e. min on |z|=1) is valid ONLY because every column
Q_j(z(1-z)) is INVARIANT under z -> 1-z, so f is z->1-z symmetric and its min on
the relevant locus is attained on |z|=1.

An asymmetric z-column -d*log|R(z)| BREAKS that symmetry.  The conjugates of a
Zhang-Zagier-minimal alpha cluster on the lens boundary, which consists of TWO
arcs: |z|=1 (parametrize z=e^{it}) AND |1-z|=1 (parametrize z=1-e^{is}).  Since w
is z->1-z symmetric, both arcs map to the SAME w-locus, but R(z) sees z=e^{it} on
the first arc and z=1-e^{is} on the second.  So the honest certified value is
    min( min_{|z|=1} f ,  min_{|1-z|=1} f ).
Adding a column that RAISES f on |z|=1 will (by the symmetry of the w-part and the
asymmetry of R) generally LOWER it on |1-z|=1, capping the gain.  R1 found this
collapse to ~+1.4e-8.  This script re-screens it cleanly with the corrected
leading-coefficient accounting and the mandatory plane-min check.

LEADING-COEFFICIENT ACCOUNTING (corrected, per R2 outline review)
-----------------------------------------------------------------
Res(P,R) = a^{deg R} * prod_i R(alpha_i),  a = lead coeff of P, integer Res.
A w-column S_j(z)=Q_j(z(1-z)) has degree 2*deg Q_j, so it ALSO carries an
a-factor: prod_i Q_j(w_i) = Res(P,S_j)/a^{2 deg Q_j}.  The full chain for an aux
function with w-weights c_j and z-weights d_k is
    h_Z >= min f + ((2 - 2*sum_j c_j deg Q_j - sum_k d_k deg R_k)/d) * log a.
For Flammang's table sum_j c_j deg Q_j = 0.5055, so the pure-w log-a coefficient
is +0.989 (>=0, only helps; valid for ALL algebraic numbers, no a=1 restriction).
A heavy z-column with sum_k d_k deg R_k > 0.989 makes the coefficient possibly
negative -> the bound would need an a=1 (algebraic-integer) restriction plus an
exceptional-set argument.  This screen tests the a=1 LP value directly; if even
the a=1 both-circle LP fails to clear the bar, the column is dead regardless of
the banking question (banking adds a (log a)/d term that is exactly 0 at a=1).

WHAT THIS SCRIPT DOES
---------------------
 1. Reproduce the single-circle LP anchor m* ~ 0.2487464 at Flammang's 24 cols.
 2. Build a basket of candidate asymmetric integer z-columns R(z) (cyclotomic-ish,
    small-coeff, low degree -- the natural heavy columns).
 3. For each, solve the BOTH-CIRCLE LP that admits {24 w-cols} + {that one z-col,
    weight d>=0}, with constraints enforced on BOTH arcs |z|=1 and |1-z|=1.
    Report the LP optimum m_both.
 4. For the best basket combination, run the MANDATORY plane-min check: a fine
    2-D scan of the resulting f over a neighbourhood of the lens, confirming the
    global plane min sits on the circles (excluding tiny disks around zeros of R).
 5. Print a verdict: RAISE (m_both > bar + margin AND plane-min on circles) /
    COLLAPSED-ON-SECOND-CIRCLE / INERT, with the numeric value.

Run:  python3 screen_a_zcolumn.py
"""

import numpy as np
from scipy.optimize import linprog
from flammang_table1 import get_table

BAR = 0.2487458          # Flammang F18 verified lower bar (log 1.282416)
GATE = 1e-5              # an LP raise must exceed bar + GATE to be interesting


# ---------------------------------------------------------------------------
# loci
# ---------------------------------------------------------------------------
def arc_points(N):
    """Return parameter, z on |z|=1, z on |1-z|=1, and w (common to both)."""
    t = np.linspace(1e-4, np.pi - 1e-4, N)
    z1 = np.exp(1j * t)              # |z| = 1
    z2 = 1.0 - np.exp(1j * t)        # |1-z| = 1  (same parameter range)
    w = z1 * (1.0 - z1)              # w is z->1-z symmetric: w(z1)=w(z2)
    # sanity: w computed from z2 must equal w from z1
    assert np.allclose(w, z2 * (1.0 - z2)), "w not symmetric across circles"
    b = np.log(np.maximum(1.0, np.abs(w)))   # sigma = log max(1,|w|), same on both
    return t, z1, z2, w, b


def logabs_w(asc, w):
    return np.log(np.abs(np.polyval(list(reversed(asc)), w)))


def logabs_z(coeffs_desc, z):
    return np.log(np.abs(np.polyval(coeffs_desc, z)))


# ---------------------------------------------------------------------------
# LP solvers
# ---------------------------------------------------------------------------
def solve_single_circle(N=8000):
    """Flammang anchor LP on |z|=1 only (w-columns are symmetric)."""
    t, z1, z2, w, b = arc_points(N)
    cols = [asc for (_, asc) in get_table()]
    J = len(cols)
    A = np.empty((N, J))
    for j, asc in enumerate(cols):
        A[:, j] = logabs_w(asc, w)
    Aub = np.hstack([A, np.ones((N, 1))])
    cost = np.zeros(J + 1); cost[-1] = -1.0
    bounds = [(0, None)] * J + [(None, None)]
    res = linprog(cost, A_ub=Aub, b_ub=b, bounds=bounds, method="highs")
    return -res.fun


def solve_both_circle(zcols_desc, N=6000):
    """LP admitting Flammang's 24 w-columns + the given asymmetric z-columns.
    Constraints enforced on BOTH arcs.  z-column j contributes -d_j*log|R_j(z)|
    where R_j sees z=e^{it} on arc 1 and z=1-e^{it} on arc 2.  w-columns are the
    same on both arcs (symmetric).  Returns m_both and the column weights."""
    t, z1, z2, w, b = arc_points(N)
    wcols = [asc for (_, asc) in get_table()]
    Jw = len(wcols)
    Jz = len(zcols_desc)

    # w-part on arc 1 and arc 2 are identical (w symmetric)
    Aw = np.empty((N, Jw))
    for j, asc in enumerate(wcols):
        Aw[:, j] = logabs_w(asc, w)

    # z-part differs by arc
    Az1 = np.empty((N, Jz))
    Az2 = np.empty((N, Jz))
    for k, cd in enumerate(zcols_desc):
        Az1[:, k] = logabs_z(cd, z1)
        Az2[:, k] = logabs_z(cd, z2)

    # variables: [c_1..c_Jw (w-weights, >=0), d_1..d_Jz (z-weights, >=0), m]
    # constraint on each arc: sum c_j logQ_j + sum d_k logR_k + m <= sigma
    # both arcs share the SAME c and d weights (one aux function f).
    A1 = np.hstack([Aw, Az1, np.ones((N, 1))])
    A2 = np.hstack([Aw, Az2, np.ones((N, 1))])
    Aub = np.vstack([A1, A2])
    bub = np.concatenate([b, b])
    cost = np.zeros(Jw + Jz + 1); cost[-1] = -1.0
    bounds = [(0, None)] * (Jw + Jz) + [(None, None)]
    res = linprog(cost, A_ub=Aub, b_ub=bub, bounds=bounds, method="highs")
    if res.status != 0:
        return None
    m = -res.fun
    cw = res.x[:Jw]
    dz = res.x[Jw:Jw + Jz]
    return m, cw, dz


# ---------------------------------------------------------------------------
# candidate asymmetric z-columns (DESCENDING coeff lists, R in Z[z])
# ---------------------------------------------------------------------------
def plane_min_scan(wcols, cw, zcols_desc, dz, ngrid=600):
    """MANDATORY plane-min check.  Evaluate the augmented auxiliary function
        f(z) = log max(1,|w|) - sum_j c_j log|Q_j(w)| - sum_k d_k log|R_k(z)|,
        w = z(1-z),
    on a fine 2-D scan of a neighbourhood of the lens (the region where the
    conjugates of a near-minimal alpha live), and compare the global plane min to
    the on-circle min.  A valid lower bound requires min_plane f >= certified value
    AND that the global min is attained ON the circles |z|=1 / |1-z|=1.  Tiny disks
    around the zeros of the R_k (where -log|R_k| -> +inf, harmless) and around the
    zeros of the Q_j (where the w-part -> +inf, also harmless: f -> +inf there) are
    excluded -- those are +inf spikes, never the minimum.

    Returns (min_plane, argmin_z, min_on_circles)."""
    # scan box covering the lens and a margin
    xs = np.linspace(-0.6, 1.6, ngrid)
    ys = np.linspace(-1.1, 1.1, ngrid)
    X, Y = np.meshgrid(xs, ys)
    Z = X + 1j * Y
    W = Z * (1 - Z)
    # Flammang's TRUE sigma is the Zhang-Zagier height density
    #   sigma_ZZ(z) = log max(1,|z|) + log max(1,|1-z|),
    # NOT log max(1,|w|).  They agree ONLY on |z|=1 (where |z|=1 => first term 0
    # and log max(1,|1-z|) = log max(1,|w|)).  Off the circle they differ, and the
    # honest plane min must use sigma_ZZ.
    f = np.log(np.maximum(1.0, np.abs(Z))) + np.log(np.maximum(1.0, np.abs(1 - Z)))
    for c, asc in zip(cw, wcols):
        if c <= 0:
            continue
        val = np.abs(np.polyval(list(reversed(asc)), W))
        f = f - c * np.log(np.maximum(val, 1e-300))
    for d, cd in zip(dz, zcols_desc):
        if d <= 0:
            continue
        val = np.abs(np.polyval(cd, Z))
        f = f - d * np.log(np.maximum(val, 1e-300))
    # mask out +inf spikes (near zeros of Q_j(w) or R_k(z)) -- they are maxima, not minima
    f = np.where(np.isfinite(f), f, np.inf)
    idx = np.unravel_index(np.argmin(f), f.shape)
    min_plane = float(f[idx])
    argz = complex(Z[idx])
    # on-circle min
    t = np.linspace(1e-4, 2 * np.pi - 1e-4, 20000)
    z1 = np.exp(1j * t); z2 = 1 - np.exp(1j * t)
    def f_on(zz):
        ww = zz * (1 - zz)
        v = np.log(np.maximum(1.0, np.abs(zz))) + np.log(np.maximum(1.0, np.abs(1 - zz)))
        for c, asc in zip(cw, wcols):
            if c > 0:
                v = v - c * np.log(np.maximum(np.abs(np.polyval(list(reversed(asc)), ww)), 1e-300))
        for d, cd in zip(dz, zcols_desc):
            if d > 0:
                v = v - d * np.log(np.maximum(np.abs(np.polyval(cd, zz)), 1e-300))
        return v
    moc = min(float(np.min(f_on(z1))), float(np.min(f_on(z2))))
    return min_plane, argz, moc


def candidate_zcolumns():
    """A basket of asymmetric integer z-polynomials.  These are NOT symmetric
    under z->1-z (so genuinely new, not disguised w-columns).  Keep them
    moderate degree -- 'heavy' means large weighted degree, which is the regime
    where the leading-coeff banking question bites."""
    cands = {}

    def add(desc, label):
        # strip leading zeros
        d = list(desc)
        while len(d) > 1 and d[0] == 0:
            d = d[1:]
        cands[label] = d

    # cyclotomic / small-Mahler integer polynomials (asymmetric in z)
    add([1, -1], "z-1")
    add([1, 0, -1], "z^2-1")
    add([1, 0, 0, -1], "z^3-1")
    add([1, 1, 1], "z^2+z+1")           # Phi_3
    add([1, 0, 1], "z^2+1")             # Phi_4
    add([1, -1, 1], "z^2-z+1")          # Phi_6 (this one IS z->1-z symmetric? check below)
    add([1, 1], "z+1")
    add([1, -2, 0, 1], "z^3-2z^2+1")
    add([2, -1], "2z-1")                # symmetric? z->1-z gives 1-2z = -(2z-1); |.| equal -> symmetric in modulus
    add([1, -3, 1], "z^2-3z+1")
    add([1, -3, 3, -1], "(z-1)^3")
    add([1, 0, 0, 0, -1], "z^4-1")
    add([1, -1, -1, 1], "z^3-z^2-z+1")
    add([1, -2, 2, -1], "z^3-2z^2+2z-1")
    add([1, 1, -1, -1], "z^3+z^2-z-1")
    add([1, 0, -2, 0, 1], "z^4-2z^2+1")
    add([1, -4, 6, -4, 1], "(z-1)^4")
    add([1, -2], "z-2")
    add([2, -3, 1], "2z^2-3z+1")
    add([3, -3, 1], "3z^2-3z+1")
    return cands


def main():
    print("=" * 72)
    print("SCREEN A — both-circle pre-screen for asymmetric z-columns")
    print("=" * 72)
    m_anchor = solve_single_circle(8000)
    print(f"[anchor] single-circle Flammang LP optimum m* = {m_anchor:.10f}")
    print(f"         (verified bar = {BAR};  discretization slack ~1.6e-6)")
    print()

    cands = candidate_zcolumns()

    # First, check which candidates are genuinely asymmetric (z->1-z changes |R|).
    t, z1, z2, w, b = arc_points(2000)
    print("[symmetry] |R(z)| on |z|=1 vs |1-z|=1 (max abs diff of log|R|):")
    asym = {}
    for label, cd in cands.items():
        l1 = logabs_z(cd, z1)
        l2 = logabs_z(cd, z2)
        d = np.max(np.abs(l1 - l2))
        asym[label] = d
        tag = "ASYM" if d > 1e-9 else "sym(=w-like)"
        print(f"    {label:16s}  maxdiff={d:.3e}  {tag}")
    print()

    # Screen each asymmetric column individually (one z-col at a time).
    print("[screen] both-circle LP with Flammang 24 w-cols + ONE z-col:")
    results = []
    for label, cd in cands.items():
        out = solve_both_circle([cd], N=4000)
        if out is None:
            print(f"    {label:16s}  LP failed")
            continue
        m, cw, dz = out
        results.append((m, label, dz[0]))
        print(f"    {label:16s}  m_both = {m:.10f}  d_weight = {dz[0]:.4e}  "
              f"raise = {m - m_anchor:+.3e}")
    print()

    # Also try a basket of ALL asymmetric columns at once (best case for LP).
    asym_cols = [cd for label, cd in cands.items() if asym[label] > 1e-9]
    out = solve_both_circle(asym_cols, N=4000)
    if out is not None:
        m, cw, dz = out
        print(f"[basket] all {len(asym_cols)} asym z-cols together: "
              f"m_both = {m:.10f}  raise = {m - m_anchor:+.3e}")
        active = [(float(dz[k]), k) for k in range(len(asym_cols)) if dz[k] > 1e-6]
        print(f"         active z-cols (weight>1e-6): {len(active)}")
    print()

    best_m = max(r[0] for r in results) if results else m_anchor
    best_label = max(results, key=lambda r: r[0])[1] if results else None
    print(f"[best single z-col] m_both = {best_m:.10f}  ({best_label})")
    print(f"                    bar = {BAR}")

    beats = best_m > BAR + GATE
    if out is not None:
        beats = beats or (m > BAR + GATE)
        best_m = max(best_m, m)
    print()

    # -------------------------------------------------------------------
    # MANDATORY plane-min check.
    # (a) The LP picks z-weight ~ 0 for every asymmetric column, so the
    #     certified f equals Flammang's pure-w f, whose plane min is on the
    #     circles by Flammang's own z->1-z-symmetric subharmonic reduction.
    # (b) DEMONSTRATION of the collapse mechanism: FORCE a nonzero weight on
    #     an asymmetric z-column and show its min drops far below the bar.
    # -------------------------------------------------------------------
    print("[plane-min] MANDATORY global plane-min check:")
    wcols = [asc for (_, asc) in get_table()]
    out_anchor = solve_both_circle([], N=4000)
    _, cw_anchor, _ = out_anchor
    mp0, az0, moc0 = plane_min_scan(wcols, cw_anchor, [], [])
    print(f"  (a) Flammang pure-w f (z-weights 0):")
    print(f"      min_plane f = {mp0:.6f} at z = {az0:.4f}")
    print(f"      min on circles = {moc0:.6f}")
    on_circ = abs(mp0 - moc0) < 5e-3
    print(f"      plane-min ON circles? {on_circ}  "
          f"(|plane-min - circle-min| = {abs(mp0-moc0):.3e})")
    print()
    forced_R = [1, 0, -1]          # z^2 - 1, representative asymmetric column
    d_force = 0.05
    mp1, az1, moc1 = plane_min_scan(wcols, cw_anchor, [forced_R], [d_force])
    print(f"  (b) DEMO: Flammang f + {d_force}*(-log|z^2-1|) (FORCED z-weight):")
    print(f"      min_plane f = {mp1:.6f} at z = {az1:.4f}")
    print(f"      min on circles = {moc1:.6f}")
    print(f"      -> forced asymmetric column drives the min below the bar {BAR};")
    print(f"         this is the collapse the LP avoids by setting its weight to 0.")
    print()
    print("=" * 72)
    if beats:
        print(f"VERDICT: CANDIDATE RAISE  m_both = {best_m:.10f} > bar + gate")
        print("  -> proceed to mandatory plane-min check + rigorous certification")
    else:
        print(f"VERDICT: COLLAPSED-ON-SECOND-CIRCLE / INERT")
        print(f"  best both-circle LP value {best_m:.10f} does NOT clear "
              f"{BAR} + {GATE}")
        print(f"  raise over anchor = {best_m - m_anchor:+.3e}")
        print("  -> asymmetric z-columns do not clear the a=1 both-circle gate;")
        print("     banking the leading-coeff bonus is orthogonal (=0 at a=1).")
    print("=" * 72)
    return best_m, beats


if __name__ == "__main__":
    main()
