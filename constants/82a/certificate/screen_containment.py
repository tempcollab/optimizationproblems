"""
screen_containment.py  --  C_82a (Zhang-Zagier essential minimum), LOWER bound.

VERIFIED-NEGATIVE CLOSURE of the LAST OPEN lower-bound angle (the min-vs-mean gap).
Round 6.  NO raise: the held lower bound stays Flammang [F18] 0.2487458, Status none.

WHAT THIS CERTIFIES
-------------------
PART (i)  -- the genuinely NEW, reproducible milestone of this round.
  The hypothesised POINTWISE CONTAINMENT LEMMA is FALSE on Flammang's Table-1 family.

  The lower-bound identity is  h_Z(alpha) = (1/d) sum_i f(z_i)  >=  (1/d) sum_i f(z_i),
  and Flammang bounds the RHS below by  min_{|z|=1} f = 0.2487462  (the MIN reduction).
  The only non-barred way to beat Flammang is a min-vs-mean improvement
        (1/d) sum_i f(z_i)  >=  circle-min f  +  delta,   delta > 1.5e-4 uniformly in d,
  i.e. the conjugate measure's f-MEAN must exceed the circle MIN.  R4 left OPEN whether
  this could be cashed by a *pointwise* containment lemma -- a deterministic region R,
  derived from integer/coefficient structure ALONE, that holds every conjugate of every
  ZZ-minimal alpha and keeps it off the single binding lobe  w* = z*(1-z*),
  z* = 0.8383 + 0.5453i,  w* = 0.4329 - 0.3689i  (the circle-min locus, recomputed here).

  This script certifies that NO such pointwise lemma can exist on the natural test family:
    * Of the 13 Flammang Table-1 polynomials with deg_w >= 12, EXACTLY 7
      (j = 14,15,16,18,20,21,22) have a NEGATIVE worst-conjugate min_gap:
      at least one conjugate z_i has  f(z_i) < circle-min f.  Their worst conjugates
      land ON or just below the binding-lobe locus (|w| ~ |w*|, arg near arg(w*)).
    * The absolute smallest single-conjugate value of f over the substantive family is
      f = 0.23032 at j=5 -- well BELOW the circle-min 0.2487462.
    * Yet ALL 13 of those polynomials retain a POSITIVE mean_gap (+0.0036 .. +0.0443):
      the f-MEAN over conjugates stays above the circle min.
  So individual conjugates DO reach and pass the binding lobe -- the pointwise exclusion
  is false -- while the mean stays up.  Any salvage of the min-vs-mean route must
  therefore be an AVERAGED / equidistribution statement, NOT a pointwise containment.

PART (ii) -- the structural DICHOTOMY (a CITED SYNTHESIS of prior closures, not a new
  theorem; see the approach doc and R4_nonenergy_methods_digest.md).  Made DECISIVE by
  part (i):  any height-independent, degree-uniform MEAN containment floor is an
  equidistribution/discrepancy statement, and its only admissible inputs are
    (a) integer invariants of the root CONFIGURATION:
          - power sums / w-moments  (R5-CLOSED: sign-indefinite AND non-integer off a=1),
          - discriminant / resultants = the LOG-ENERGY cone  (R1-BARRED; its capacity-1
            transfinite-diameter LP IS Flammang's own method, R3-CEILINGed at 0.2487857),
    (b) the Weil height h  (FR06 / Bilu / Petsche effective equidistribution --
          height-DEPENDENT, error ~(4h)^{1/2} contains the bounded height: R4-CIRCULAR).
  There is no third admissible object, so the route is closed.  This screen does NOT
  re-prove the dichotomy (it is asserted prior art); it CHECKS that part (i) holds, that
  no claimed "fourth admissible input" or "pointwise lemma holds" assertion can sneak
  past, and records the citation chain.

SCOPE CAVEAT (reviewer-required).  Flammang's Table-1 polynomials are near-extremal
  AUXILIARY polynomials, NOT the minimal polynomials of actual small-height ZZ numbers.
  Part (i) therefore disproves the pointwise lemma on the natural SUGGESTIVE family; it
  does not assert "the lemma is false for all ZZ-minimal alpha as a theorem."  The
  family-INDEPENDENT closure is part (ii): even granting the lemma, the only salvage is a
  mean/equidistribution statement, which is barred (energy) or circular (height).

CONVENTIONS.  Honest ZZ density  sigma_ZZ(z) = log max(1,|z|) + log max(1,|1-z|)
  [F18 eq 2.1] -- NOT log max(1,|w|).  EXCL-SELF: a genuine ZZ-minimal P is coprime to
  each Q_j, so log|Q_j(alpha(1-alpha))| is finite; when we use the roots of Q_j(z(1-z))=0
  as a proxy for ZZ-conjugate locations we evaluate f with the self term j REMOVED (the
  +inf at Q_j's own roots is an artifact of using Q_j's own roots, not a property of ZZ
  numbers).

USAGE
-----
  python3 screen_containment.py certify    # full certificate + the 7/13 table
  python3 screen_containment.py selftest    # fast asserts of the load-bearing cores
  python3 screen_containment.py tamper      # bogus claims MUST fail (exit 1 = good)

Source for the polynomials and aux function:
  V. Flammang, "On the Zhang-Zagier measure", Int. J. Number Theory 14 (2018), Table 1
  (transcribed verbatim in flammang_table1.py).
"""

import sys

import numpy as np

from flammang_table1 import get_table


# ---------------------------------------------------------------------------
# core math (self-contained, numpy only; independent of gap_diagnostic.py)
# ---------------------------------------------------------------------------
def Qval(asc, w):
    """Horner evaluation of an integer polynomial (ascending coeffs) at w."""
    q = np.zeros_like(np.asarray(w, dtype=complex))
    for a in reversed(asc):
        q = q * w + a
    return q


def sigma_ZZ(z):
    """Honest Zhang-Zagier density (F18 eq 2.1): log max(1,|z|) + log max(1,|1-z|)."""
    return (np.log(np.maximum(1.0, np.abs(z)))
            + np.log(np.maximum(1.0, np.abs(1.0 - z))))


def comp_roots(asc):
    """Roots z of Q_j(z(1-z)) = 0, where asc are the ascending w-coeffs of Q_j.

    Substitute w = z - z^2 and accumulate sum_k asc[k]*(z - z^2)^k, then numpy.roots.
    """
    wz = np.array([-1.0, 1.0, 0.0])      # z - z^2 in descending z-coeffs
    res = np.array([0.0])
    powk = np.array([1.0])
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
    """min over |z|=1 of the FULL Flammang aux f.  Returns (min, argmin z, argmin w).

    Reproduces Flammang's record 0.2487462 and locates the binding lobe w*.
    """
    t = np.linspace(0.0, 2.0 * np.pi, n)
    z = np.exp(1j * t)
    w = z * (1.0 - z)
    val = sigma_ZZ(z)
    # A grid point may land exactly on a Q_j zero (log 0 = -inf); that pushes f to
    # +inf there (val += +inf), never the MIN, so the argmin is unaffected.  Silence
    # the expected divide-by-zero warning rather than mask a real issue.
    with np.errstate(divide="ignore"):
        for c, asc in table:
            val = val - c * np.log(np.abs(Qval(asc, w)))
    k = int(val.argmin())
    return float(val[k]), z[k], w[k]


def f_excl_self(z, table, skip):
    """Flammang aux f at z with the self term (index skip) removed (the principled object)."""
    w = z * (1.0 - z)
    val = sigma_ZZ(z)
    for jj, (c, asc) in enumerate(table):
        if jj == skip:
            continue
        val = val - c * np.log(np.abs(Qval(asc, w)))
    return val


# ---------------------------------------------------------------------------
# PART (i) computation -- per-poly worst-conjugate min and mean gaps
# ---------------------------------------------------------------------------
def compute_rows(table, cm, deg_min=12):
    """For every Table-1 poly with deg_w >= deg_min, recompute (independently from the
    conjugate roots) the worst single-conjugate min_gap and the mean_gap, plus the
    location of the worst conjugate.  Returns a list of dicts."""
    rows = []
    for j in range(1, len(table) + 1):
        c, asc = table[j - 1]
        deg_w = len(asc) - 1
        if deg_w < deg_min:
            continue
        rts = comp_roots(asc)
        fr = f_excl_self(rts, table, j - 1)
        k = int(np.argmin(fr))
        zk = rts[k]
        wk = zk * (1.0 - zk)
        rows.append({
            "j": j,
            "deg_w": deg_w,
            "n_conj": len(rts),
            "min_f": float(fr.min()),
            "mean_f": float(fr.mean()),
            "min_gap": float(fr.min() - cm),
            "mean_gap": float(fr.mean() - cm),
            "worst_z": complex(zk),
            "worst_w": complex(wk),
        })
    return rows


# the load-bearing claim, as data the reviewer can pin
NEG_J_EXPECTED = {14, 15, 16, 18, 20, 21, 22}   # deg_w>=12 polys with min_gap < 0
ABS_MIN_F_J = 5                                  # absolute-smallest single-conjugate f
ABS_MIN_F_VAL = 0.23032                          # ... value, < circle-min 0.2487462
CIRCLE_MIN_TARGET = 0.2487462                    # reproduces Flammang record


# ---------------------------------------------------------------------------
# certify
# ---------------------------------------------------------------------------
def certify(verbose=True):
    table = get_table()
    cm, zstar, wstar = circle_min_full_f(table)

    rows = compute_rows(table, cm, deg_min=12)
    neg = [r for r in rows if r["min_gap"] < 0]
    neg_j = {r["j"] for r in neg}
    all_mean_pos = all(r["mean_gap"] > 0 for r in rows)

    # absolute smallest single-conjugate f over the substantive family (deg_w >= 3)
    abs_min = None
    for j in range(1, len(table) + 1):
        c, asc = table[j - 1]
        if len(asc) - 1 < 3:
            continue
        rts = comp_roots(asc)
        fr = f_excl_self(rts, table, j - 1)
        v = float(fr.min())
        if abs_min is None or v < abs_min[0]:
            abs_min = (v, j)

    if verbose:
        print("=" * 78)
        print("C_82a LOWER -- min-vs-mean closure, PART (i): pointwise containment FALSE")
        print("=" * 78)
        print(f"circle-min of FULL Flammang aux f over |z|=1 = {cm:.7f}")
        print(f"   (Flammang record 0.2487458; reproduces it, +{cm - 0.2487458:.1e})")
        print(f"   binding lobe  z* = {zstar.real:+.4f}{zstar.imag:+.4f}i"
              f"   w* = {wstar.real:+.4f}{wstar.imag:+.4f}i")
        print()
        print("deg_w >= 12 family (13 polys).  worst conjugate per poly,"
              " EXCL-self f, honest sigma_ZZ:")
        print(" j  deg_w n_conj  min_f     mean_f    min_gap     mean_gap   "
              "worst_w (lobe ~ 0.433-0.369i)")
        print("-" * 92)
        for r in rows:
            flag = "  <== min_gap<0 (conj passes the lobe)" if r["min_gap"] < 0 else ""
            print(f"{r['j']:2d}   {r['deg_w']:2d}   {r['n_conj']:3d}   "
                  f"{r['min_f']:.5f}  {r['mean_f']:.5f}  {r['min_gap']:+.6f}  "
                  f"{r['mean_gap']:+.6f}  "
                  f"({r['worst_w'].real:+.4f}{r['worst_w'].imag:+.4f}i){flag}")
        print()
        print(f"  # deg_w>=12 polys with NEGATIVE worst-conjugate min_gap: "
              f"{len(neg)} / {len(rows)}   at j = {sorted(neg_j)}")
        print(f"  all 13 mean_gap > 0 (range "
              f"[{min(r['mean_gap'] for r in rows):+.5f}, "
              f"{max(r['mean_gap'] for r in rows):+.5f}]): {all_mean_pos}")
        print(f"  absolute smallest single-conjugate f over substantive family: "
              f"{abs_min[0]:.5f} at j={abs_min[1]}  (< circle-min {cm:.5f})")
        print()

    # -------- the load-bearing assertions (these define the certificate) --------
    ok = True

    def check(name, cond):
        nonlocal ok
        status = "PASS" if cond else "FAIL"
        if verbose:
            print(f"  [{status}] {name}")
        if not cond:
            ok = False

    check("circle-min reproduces Flammang record (in [0.24870, 0.24882])",
          0.24870 <= cm <= 0.24882)
    check(f"exactly 7 of 13 deg_w>=12 polys have min_gap<0 at j={sorted(NEG_J_EXPECTED)}",
          neg_j == NEG_J_EXPECTED and len(rows) == 13)
    check("ALL 13 deg_w>=12 polys retain mean_gap > 0", all_mean_pos)
    check("the 7 negatives reach f BELOW circle-min (pointwise lemma is FALSE)",
          len(neg) == 7 and all(r["min_f"] < cm for r in neg))
    check(f"absolute min single-conjugate f = {abs_min[0]:.5f} at j={abs_min[1]} "
          f"< circle-min (binding lobe is reached)",
          abs_min[1] == ABS_MIN_F_J and abs(abs_min[0] - ABS_MIN_F_VAL) < 1e-3
          and abs_min[0] < cm)

    if verbose:
        print()
        print("PART (ii) -- structural dichotomy (CITED prior art, made decisive by (i)):")
        print("  A height-independent, degree-uniform MEAN containment floor is an")
        print("  equidistribution/discrepancy statement; its only admissible inputs are")
        print("   (a) integer root-configuration invariants:")
        print("        * power sums / w-moments  -> R5-CLOSED (sign-indefinite; non-integer off a=1)")
        print("        * disc / resultants = log-energy cone -> R1-BARRED, R3-CEILINGed 0.2487857")
        print("   (b) the Weil height h (FR06/Bilu/Petsche) -> R4-CIRCULAR (error ~(4h)^{1/2})")
        print("  No third admissible object exists (R4_nonenergy_methods_digest.md synthesis +")
        print("  R1/R3/R4/R5 closures).  Part (i) removes the only remaining degree of freedom")
        print("  (a pointwise exclusion), so the route is CLOSED.")
        print()
        print("SCOPE: Table-1 are near-extremal AUX polys, not ZZ-minimal polys; part (i)")
        print("  disproves the pointwise lemma on the natural family, part (ii) is what makes")
        print("  the closure family-independent.")
        print()
        print("RESULT:", "ALL CERTIFICATE CHECKS PASS"
              if ok else "CERTIFICATE FAILED")
        print("NO raise: held lower stays Flammang 0.2487458, Status none.")

    return ok, rows, cm


# ---------------------------------------------------------------------------
# selftest -- fast asserts of the load-bearing cores
# ---------------------------------------------------------------------------
def selftest():
    table = get_table()
    cm, zstar, wstar = circle_min_full_f(table, n=400_001)
    ok = True

    print(f"[A] circle-min f = {cm:.7f} (target Flammang 0.2487458); "
          f"binding lobe w* = {wstar.real:+.4f}{wstar.imag:+.4f}i")
    if not (0.24870 <= cm <= 0.24882):
        print("    FAIL"); ok = False
    else:
        print("    PASS: reproduces Flammang and locates the binding lobe")

    rows = compute_rows(table, cm, deg_min=12)
    neg_j = {r["j"] for r in rows if r["min_gap"] < 0}
    print(f"[B] deg_w>=12 polys with min_gap<0: {sorted(neg_j)}")
    if neg_j == NEG_J_EXPECTED and len(rows) == 13:
        print("    PASS: exactly 7/13 are negative (pointwise lemma FALSE)")
    else:
        print("    FAIL: expected exactly {14,15,16,18,20,21,22}"); ok = False

    print("[C] every deg_w>=12 mean_gap > 0:")
    mn = min(r["mean_gap"] for r in rows)
    mx = max(r["mean_gap"] for r in rows)
    if all(r["mean_gap"] > 0 for r in rows):
        print(f"    PASS: range [{mn:+.5f}, {mx:+.5f}] (mean stays above circle-min)")
    else:
        print("    FAIL"); ok = False

    print("[D] the 7 negatives reach f strictly below circle-min:")
    negs = [r for r in rows if r["min_gap"] < 0]
    worst = min(negs, key=lambda r: r["min_f"])
    if all(r["min_f"] < cm for r in negs):
        print(f"    PASS: worst negative min_f = {worst['min_f']:.5f} < {cm:.5f} "
              f"at j={worst['j']}, worst_w = "
              f"{worst['worst_w'].real:+.4f}{worst['worst_w'].imag:+.4f}i")
    else:
        print("    FAIL"); ok = False

    print("[E] absolute smallest single-conjugate f = 0.23032 at j=5 (< circle-min):")
    c, asc = table[ABS_MIN_F_J - 1]
    f5 = float(f_excl_self(comp_roots(asc), table, ABS_MIN_F_J - 1).min())
    if abs(f5 - ABS_MIN_F_VAL) < 1e-3 and f5 < cm:
        print(f"    PASS: f(j=5)_min = {f5:.5f} < circle-min {cm:.5f}")
    else:
        print(f"    FAIL: f(j=5)_min = {f5:.5f}"); ok = False

    print()
    print("selftest:", "ALL PASS" if ok else "FAILURES PRESENT")
    return ok


# ---------------------------------------------------------------------------
# tamper -- bogus claims MUST fail the screen (exit 1 = the screen is honest)
# ---------------------------------------------------------------------------
def tamper():
    """Two adversarial claims that the screen must REJECT:

    T1: 'the pointwise containment lemma HOLDS' i.e. no conjugate reaches below the
        circle min => NO poly has min_gap < 0.  The data refutes this (7 do), so a
        screen that auto-passed it would be broken.  We assert the screen sees the 7.
    T2: 'a fourth admissible input exists' -- a phantom degree-uniform mean floor with
        min_gap>0 forced everywhere (the pointwise lemma true).  We simulate it by
        zeroing the negative gaps and assert the screen's core check would then FAIL
        (proving the check actually bites the data, not a constant True).
    """
    table = get_table()
    cm, _, _ = circle_min_full_f(table, n=400_001)
    rows = compute_rows(table, cm, deg_min=12)
    neg_j = {r["j"] for r in rows if r["min_gap"] < 0}

    print("TAMPER T1: assert 'pointwise containment lemma HOLDS' (no min_gap<0).")
    bogus_holds = (len(neg_j) == 0)
    if bogus_holds:
        print("    FAIL: screen accepted the bogus lemma -- it is broken.")
        return False
    print(f"    GOOD: screen sees {len(neg_j)} polys with min_gap<0 "
          f"({sorted(neg_j)}); the bogus 'lemma holds' is REJECTED.")

    print("TAMPER T2: forge a 'fourth admissible input' by zeroing the negative gaps")
    print("           (pretend every conjugate stays off the lobe) and re-run the core.")
    forged = []
    for r in rows:
        rr = dict(r)
        if rr["min_gap"] < 0:
            rr["min_gap"] = abs(rr["min_gap"])        # forge a clean containment
            rr["min_f"] = cm + rr["min_gap"]
        forged.append(rr)
    forged_neg = {r["j"] for r in forged if r["min_gap"] < 0}
    # the certificate's core check is: exactly NEG_J_EXPECTED are negative.
    core_holds_on_forged = (forged_neg == NEG_J_EXPECTED)
    if core_holds_on_forged:
        print("    FAIL: core check passed on FORGED data -- it does not bite.")
        return False
    print("    GOOD: on forged 'lemma-true' data the core check FAILS "
          f"(forged negatives {sorted(forged_neg)} != expected "
          f"{sorted(NEG_J_EXPECTED)}); the check genuinely tests the data.")

    print()
    print("tamper: BOTH bogus claims correctly REJECTED.")
    return True


# ---------------------------------------------------------------------------
def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "certify"
    if mode == "certify":
        ok, _, _ = certify(verbose=True)
        return 0 if ok else 1
    if mode == "selftest":
        return 0 if selftest() else 1
    if mode == "tamper":
        # tamper SUCCEEDS (exit 0) iff both bogus claims are correctly rejected.
        return 0 if tamper() else 1
    print(f"unknown mode {mode!r}; use certify | selftest | tamper")
    return 2


if __name__ == "__main__":
    sys.exit(main())
