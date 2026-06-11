"""
gap_diagnostic.py  --  C_82a (Zhang-Zagier essential minimum), LOWER bound.

ROOT-LOCATION DIAGNOSTIC CORRECTION  (reviewer-reproducible certificate).

PURPOSE
-------
This script CORRECTS the wrong "far lemniscate / mean_nu f ~ 0.44" diagnosis that the
loop has carried in its run_state Rules since R3, and replaces it with the honest
picture, computed reproducibly across MULTIPLE Flammang Table-1 polynomials.

It establishes, for each Table-1 polynomial Q_j(w), w = z(1-z):

  (1) the conjugate-root locations  z  (roots of  Q_j(z(1-z)) = 0 ),
  (2) their distances to the two circles  |z| = 1  and  |1 - z| = 1,
  (3) the mean of the Zhang-Zagier density  sigma_ZZ(z) = log+|z| + log+|1-z|
      over those roots,
  (4) the circle-min of Flammang's FULL auxiliary function f over |z| = 1
      (reproduces ~0.2487462),
  (5) the per-poly MIN gap and MEAN gap  ( root-value of f  -  circle-min f ),
      where f is evaluated with the principled "exclude the self term" convention
      (see NOTE below).

CORRECTED FINDINGS (re-run to verify):
  * Roots HUG the two circles -- mean distance ~0.013-0.034, max usually < 0.05.
    The |z| in [0.5, 2.0] spread is NOT an off-circle lemniscate: a root with
    |z| ~ 1.97 has |1 - z| ~ 1, i.e. it sits on the OTHER circle.
  * mean sigma_ZZ over the conjugates is ~0.24-0.27, NOT 0.44.
  * Explorer B's "0.44 / far lemniscate" is the FULL-f-WITH-SELF artifact (see NOTE)
    on the tiny deg-8 poly j=5 (full-f mean 0.432), over-generalized. Its honest
    mean sigma_ZZ is 0.2406, and its roots sit exactly ON the circles.
  * The genuine slack is the MIN-vs-MEAN gap on the cross-aux f, NOT an off-circle
    leak. The MEAN gap stays POSITIVE and persistent (+0.003 to +0.02) at the
    highest degrees, while the MIN gap collapses toward (and below) 0 -- so the
    obstruction is NOT "the gap shrinks to 0"; the mechanism uses the MEAN gap,
    which does not collapse.  (See R4-min-vs-mean-equidistribution.md.)

NOTE on the "exclude self term" convention.
  The roots z used as a proxy for ZZ-conjugate locations are, by construction,
  roots of  Q_j(z(1-z)) = 0, so  Q_j(w) = 0  there and the term  -c_j log|Q_j(w)|
  in the FULL f diverges to +inf at exactly those points. That +inf is a numerical
  artifact of using Q_j's own roots, NOT a property of genuine ZZ-minimal numbers:
  a genuine ZZ-minimal polynomial P is coprime to each Q_j, so log|Q_j(alpha(1-alpha))|
  is finite there. We therefore evaluate the min-vs-mean f with the SELF term j
  removed (sum over jj != j). This is the principled object; the FULL-f-with-self
  number is reported separately ONLY to expose that it is the source of the bogus
  "0.44". Both the circle-min (point 4) and the root distances (points 1-3) are
  self-term-free and unaffected.

The script is self-contained (numpy only) and emits gap_diagnostic.json.

USAGE
-----
  python3 gap_diagnostic.py            # full diagnostic + writes gap_diagnostic.json
  python3 gap_diagnostic.py selftest   # fast soundness checks (asserts the cores)

Source for the polynomials and aux function:
  V. Flammang, "On the Zhang-Zagier measure", Int. J. Number Theory 14 (2018),
  Table 1.  (transcribed verbatim in flammang_table1.py)
"""

import json
import os
import sys

import numpy as np

from flammang_table1 import get_table

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------------
# core helpers
# ---------------------------------------------------------------------------
def Qval(asc, w):
    """Horner evaluation of the integer polynomial (ascending coeffs) at w."""
    q = np.zeros_like(np.asarray(w, dtype=complex))
    for a in reversed(asc):
        q = q * w + a
    return q


def sigma_ZZ(z):
    """Honest Zhang-Zagier density (Flammang eq 2.1): log+|z| + log+|1-z|."""
    return (np.log(np.maximum(1.0, np.abs(z)))
            + np.log(np.maximum(1.0, np.abs(1.0 - z))))


def comp_roots(asc):
    """Roots z of Q_j(z(1-z)) = 0, where asc are the ascending w-coeffs of Q_j.

    Builds the composed polynomial in z by substituting w = z - z^2 and
    accumulating sum_k asc[k] * (z - z^2)^k, then calls numpy.roots.
    """
    wz = np.array([-1.0, 1.0, 0.0])      # z - z^2  in descending z-coeffs
    res = np.array([0.0])
    powk = np.array([1.0])               # (z - z^2)^0
    for a in asc:
        term = a * powk
        L = max(len(res), len(term))
        r = np.zeros(L)
        r[L - len(res):] += res
        r[L - len(term):] += term
        res = r
        powk = np.convolve(powk, wz)
    return np.roots(res)


def circle_min_full_f(table, n=2_000_001):
    """min over |z|=1 of the FULL Flammang aux f (reproduces Flammang 0.2487462)."""
    t = np.linspace(0.0, 2.0 * np.pi, n)
    z = np.exp(1j * t)
    w = z * (1.0 - z)
    val = sigma_ZZ(z)
    for c, asc in table:
        val = val - c * np.log(np.abs(Qval(asc, w)))
    return float(val.min())


def f_excl_self(z, table, skip):
    """Flammang aux f at z with the self term (index skip) removed.

    A genuine ZZ-minimal P is coprime to each Q_j, so this is the principled
    evaluation; removing skip avoids the +inf artifact at Q_skip's own roots.
    """
    w = z * (1.0 - z)
    val = sigma_ZZ(z)
    for jj, (c, asc) in enumerate(table):
        if jj == skip:
            continue
        val = val - c * np.log(np.abs(Qval(asc, w)))
    return val


def f_full(z, table):
    """FULL Flammang aux f at z (includes every term; diverges at any Q-zero).

    Used ONLY to expose the bogus-0.44 artifact; the +inf at a Q-zero is the
    expected divergence, so we silence the log(0) warning here.
    """
    w = z * (1.0 - z)
    val = sigma_ZZ(z)
    with np.errstate(divide="ignore"):
        for c, asc in table:
            val = val - c * np.log(np.abs(Qval(asc, w)))
    return val


# ---------------------------------------------------------------------------
# diagnostic
# ---------------------------------------------------------------------------
def run_diagnostic(verbose=True):
    table = get_table()
    cm = circle_min_full_f(table)

    rows = []
    for j in range(1, len(table) + 1):
        c, asc = table[j - 1]
        deg_w = len(asc) - 1
        rts = comp_roots(asc)

        dz = np.abs(np.abs(rts) - 1.0)            # dist to |z|=1
        d1 = np.abs(np.abs(1.0 - rts) - 1.0)      # dist to |1-z|=1
        dmin = np.minimum(dz, d1)

        s = sigma_ZZ(rts)

        fr = f_excl_self(rts, table, j - 1)       # principled min-vs-mean object
        full = f_full(rts, table)                 # artifact-inflated (with self)

        # |z| range to show the "spread is the OTHER circle" point explicitly
        absz = np.abs(rts)

        rows.append({
            "j": j,
            "deg_w": int(deg_w),
            "n_roots_z": int(len(rts)),
            "max_dist_to_2_circles": float(dmin.max()),
            "mean_dist_to_2_circles": float(dmin.mean()),
            "min_absz": float(absz.min()),
            "max_absz": float(absz.max()),
            "mean_sigma_ZZ": float(s.mean()),
            "circle_min_f": float(cm),
            "min_root_f_exclself": float(fr.min()),
            "mean_root_f_exclself": float(fr.mean()),
            "min_gap": float(fr.min() - cm),
            "mean_gap": float(fr.mean() - cm),
            "full_f_with_self_mean": float(full.mean()),  # the bogus-0.44 source
        })

    if verbose:
        print(f"circle-min of FULL Flammang aux f over |z|=1 = {cm:.7f}"
              f"   (Flammang record 0.2487458; +{cm - 0.2487458:.1e})")
        print()
        hdr = (" j  deg_w  n_z   maxd   meand   |z|range          "
               "meanSig   minGap    meanGap   fullSelfMean")
        print(hdr)
        print("-" * len(hdr))
        for r in rows:
            print(f"{r['j']:2d}   {r['deg_w']:2d}   {r['n_roots_z']:3d}  "
                  f"{r['max_dist_to_2_circles']:.3f}  "
                  f"{r['mean_dist_to_2_circles']:.3f}  "
                  f"[{r['min_absz']:.2f},{r['max_absz']:.2f}]   "
                  f"{r['mean_sigma_ZZ']:.4f}  "
                  f"{r['min_gap']:+.5f}  {r['mean_gap']:+.5f}   "
                  f"{r['full_f_with_self_mean']:.4f}")
        print()
        _print_trends(rows)

    return {"circle_min_f": cm, "rows": rows}


def _print_trends(rows):
    """Show: MIN gap collapses with degree, MEAN gap persists."""
    # use only the substantive polys (deg_w >= 8) for the trend read
    sub = [r for r in rows if r["deg_w"] >= 8]
    sub.sort(key=lambda r: r["deg_w"])
    print("Degree trend (deg_w >= 8):  MIN gap collapses, MEAN gap PERSISTS")
    print("  deg_w   min_gap    mean_gap")
    for r in sub:
        print(f"   {r['deg_w']:2d}    {r['min_gap']:+.5f}   {r['mean_gap']:+.5f}")
    hi = [r for r in sub if r["deg_w"] >= 16]
    if hi:
        mn_min = min(r["min_gap"] for r in hi)
        mx_min = max(r["min_gap"] for r in hi)
        mn_mean = min(r["mean_gap"] for r in hi)
        mx_mean = max(r["mean_gap"] for r in hi)
        print()
        print(f"  At deg_w >= 16:  min_gap in [{mn_min:+.5f}, {mx_min:+.5f}] "
              f"(collapses toward / below 0)")
        print(f"                   mean_gap in [{mn_mean:+.5f}, {mx_mean:+.5f}] "
              f"(stays >> 1.5e-4, the raise threshold)")
        print("  => The min-vs-mean MECHANISM (which uses the MEAN gap) is NOT killed")
        print("     by a shrinking gap. The MIN gap shrinking is a side observation.")


# ---------------------------------------------------------------------------
# selftest  (fast, asserts the load-bearing cores)
# ---------------------------------------------------------------------------
def selftest():
    table = get_table()
    ok = True

    # CORE A: circle-min reproduces Flammang to ~1e-5
    cm = circle_min_full_f(table, n=400_001)
    print(f"[A] circle-min f = {cm:.7f}  (target Flammang 0.2487458)")
    if not (0.24870 <= cm <= 0.24882):
        print("    FAIL: circle-min does not reproduce Flammang"); ok = False
    else:
        print("    PASS: reproduces Flammang record on |z|=1")

    # CORE B: roots hug the two circles (high-deg polys, mean dist < 0.05)
    print("[B] root hug-the-circles (deg_w >= 12):")
    for j in (13, 15, 17, 23):
        c, asc = table[j - 1]
        rts = comp_roots(asc)
        dmin = np.minimum(np.abs(np.abs(rts) - 1.0),
                          np.abs(np.abs(1.0 - rts) - 1.0))
        msg = f"    j={j:2d} mean_dist={dmin.mean():.4f} max_dist={dmin.max():.4f}"
        if dmin.mean() < 0.05:
            print(msg + "  PASS")
        else:
            print(msg + "  FAIL"); ok = False

    # CORE C: mean sigma_ZZ ~ 0.24-0.27, NOT 0.44
    print("[C] mean sigma_ZZ in [0.23, 0.28] (NOT 0.44):")
    for j in (8, 13, 15, 17, 24):
        c, asc = table[j - 1]
        rts = comp_roots(asc)
        ms = sigma_ZZ(rts).mean()
        if 0.23 <= ms <= 0.28:
            print(f"    j={j:2d} mean_sigma_ZZ={ms:.4f}  PASS")
        else:
            print(f"    j={j:2d} mean_sigma_ZZ={ms:.4f}  FAIL"); ok = False

    # CORE D: the bogus "0.44" is the FULL-f-with-self artifact on tiny j=5
    c, asc = table[5 - 1]
    rts = comp_roots(asc)
    full5 = f_full(rts, table).mean()
    sig5 = sigma_ZZ(rts).mean()
    print(f"[D] j=5 (deg_w=4): full-f-with-self mean = {full5:.4f} (the bogus '0.44');")
    print(f"    honest mean_sigma_ZZ = {sig5:.4f} (roots ON the circles).")
    if full5 > 0.40 and sig5 < 0.26:
        print("    PASS: '0.44' is the self-term artifact on the tiny poly, "
              "over-generalized.")
    else:
        print("    FAIL"); ok = False

    # CORE E: MEAN gap PERSISTS at high degree (does NOT collapse) -- the
    #         load-bearing correction to the wrong 'gap->0' verdict.
    print("[E] MEAN gap persists at deg_w >= 16 (>> 1.5e-4 raise threshold):")
    for j in (15, 16, 17, 23, 24):
        c, asc = table[j - 1]
        rts = comp_roots(asc)
        fr = f_excl_self(rts, table, j - 1)
        mg = fr.mean() - cm
        if mg > 1.5e-3:
            print(f"    j={j:2d} mean_gap={mg:+.5f}  PASS (persists)")
        else:
            print(f"    j={j:2d} mean_gap={mg:+.5f}  FAIL (collapsed)"); ok = False

    print()
    print("selftest:", "ALL PASS" if ok else "FAILURES PRESENT")
    return ok


# ---------------------------------------------------------------------------
def main():
    res = run_diagnostic(verbose=True)
    out = os.path.join(HERE, "gap_diagnostic.json")
    with open(out, "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"\n[written] {out}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        sys.exit(0 if selftest() else 1)
    sys.exit(main())
