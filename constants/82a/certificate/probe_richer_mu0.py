"""
R16 DE-RISK PROBE (math-explorer, read-only measurement; NO cert written).

For each candidate reference measure mu0 (varying the freeze bin count B -> arc
count K and arc width L), measure BOTH:
  (1) the LP conjecture m_cut (re-freeze, read the dual);
  (2) the ACTUAL fine-grid certifiable ceiling under the verifier's per-cell
      Clausen arc-average potential UPPER bound -- i.e. the largest value the
      rigorous interval B&B could ever certify on this mu0.

The certifiable ceiling is min over a fine grid of `lower_bound_batch(a,b)` from
verify_vec_energy.py (the SAME outward-rounded per-cell lower bound on f the B&B
uses; its grid-min is an UPPER estimate of the true B&B ceiling, which converges
to it from above as the grid refines -- so a fine grid is a tight, slightly-
optimistic estimate of the verified ceiling, exact to grid-cell slack).

We do this by re-freezing into a temp dict and MONKEYPATCHING the verifier's
module-level frozen globals (CJ, LAM0, CENTERS, MASSES, LBIN, IHAT, MCUT_LP),
then calling its real lower_bound_batch -- so the ceiling is computed by the
GROUND-TRUTH machinery, not a re-implementation.
"""
import sys, time
import numpy as np
import freeze_energy as fe
import verify_vec_energy as vve

HELD = 0.2511300035          # R15 verified held lower bound
ANCHOR = 0.2487458


def patch_globals(d):
    vve.CJ = np.asarray(d["cj"])
    vve.LAM0 = float(d["lambda0"])
    vve.CENTERS = np.asarray(d["centers"])
    vve.MASSES = np.asarray(d["masses"])
    vve.LBIN = float(d["L"])
    vve.IHAT = float(d["Ihat"])
    vve.MCUT_LP = float(d["m_cut"])


def fine_grid_ceiling(ncells=400000):
    """min over a fine uniform grid of lower_bound_batch -> the certifiable ceiling
    estimate for the currently-patched frozen mu0."""
    a = np.linspace(0.0, np.pi, ncells + 1)
    A = a[:-1]; B = a[1:]
    L = vve.lower_bound_batch(A, B)
    i = int(np.argmin(L))
    return float(L[i]), 0.5 * (A[i] + B[i])


def probe(B, ncells=400000):
    d = fe.freeze(N=2000, B=B, verbose=False)
    patch_globals(d)
    t0 = time.time()
    ceil, t_at = fine_grid_ceiling(ncells)
    dt = time.time() - t0
    K = len(d["centers"])
    return dict(B=B, K=K, L=d["L"], m_cut=d["m_cut"], m0=d["m0"],
                lam0=d["lambda0"], Ihat=d["Ihat"], ceil=ceil, t_at=t_at, dt=dt)


if __name__ == "__main__":
    Bs = [int(x) for x in sys.argv[1:]] or [50, 60, 80, 40, 45, 55, 65, 70]
    print(f"{'B':>4} {'K':>3} {'L':>8} {'m_cut':>11} {'fineceil':>11} "
          f"{'haircut':>9} {'netVsHeld':>11} {'t@':>7} {'s':>5}")
    rows = []
    for B in Bs:
        r = probe(B)
        haircut = r["m_cut"] - r["ceil"]
        net = r["ceil"] - HELD
        rows.append(r)
        print(f"{r['B']:>4} {r['K']:>3} {r['L']:>8.5f} {r['m_cut']:>11.7f} "
              f"{r['ceil']:>11.7f} {haircut:>9.6f} {net:>+11.7f} "
              f"{r['t_at']:>7.4f} {r['dt']:>5.1f}")
    print(f"\nHELD (R15 verified) = {HELD}")
    best = max(rows, key=lambda r: r["ceil"])
    print(f"BEST certifiable ceiling: B={best['B']} K={best['K']} L={best['L']:.5f} "
          f"ceil={best['ceil']:.7f}  net vs held {best['ceil']-HELD:+.7f}")
