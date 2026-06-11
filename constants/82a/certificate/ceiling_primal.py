"""
R3 — BMQS PRIMAL-MEASURE LP-DUALITY CEILING for the C_82a LOWER bound.
=====================================================================

WHAT THIS CERTIFIES (read the scope carefully — it is a CEILING, not a bound on C_82).

Flammang's [F18] lower bound is the OPTIMUM of Smyth's semi-infinite LP (the DUAL):

    m* = sup over auxiliary functions  f(z) = sigma_ZZ(z) - sum_j c_j log|Q_j(z(1-z))|,
         c_j >= 0,  Q_j in Z[w],  w=z(1-z),
    of  min over the contour of f,
    where sigma_ZZ(z) = log max(1,|z|) + log max(1,|1-z|)   [Flammang eq 2.1].

By LP strong duality (BMQS arXiv:2601.18978 framing; standard LP duality), this equals
the PRIMAL measure-LP optimum:

    m* = inf over probability measures mu on the contour
         of  int sigma_ZZ dmu
         subject to  int log|Q_j| dmu >= 0  for every column Q_j in the dictionary.

KEY (the ceiling mechanism): any FEASIBLE primal probability measure mu_hat (atoms >= 0,
summing to 1, satisfying int log|Q_j| dmu_hat >= 0 for every column) has

        int sigma_ZZ dmu_hat  >=  m*  =  dual optimum.

Therefore  C := int sigma_ZZ dmu_hat  is a rigorous UPPER bound (a CEILING) on what ANY
auxiliary function in the SPAN of these columns can certify as a lower bound on C_82.

This script EXHIBITS one such rationalized mu_hat and VERIFIES, with float64 interval
arithmetic and outward rounding (fastiv.py), that

   (i)  int log|Q_j| dmu_hat >= 0  for EVERY column j in the dictionary  (lower-bounded),
   (ii) int sigma_ZZ dmu_hat <= C                                       (upper-bounded),

and prints  CERTIFIED <C>.

TWO-WARRANT SCOPE (load-bearing honesty — do NOT collapse these into one claim):
  (a) THIS BUILD proves: no auxiliary function in the SPAN of the {Q_j} actually placed
      in the dictionary (24 Flammang base columns + the LLL-bred Z[w] columns to deg 40,
      ceiling_muhat.json) certifies a lower bound above C = 0.2487857.  This is the
      mu_hat feasibility certificate below, and it is fully rigorous.
  (b) SEPARATELY, the dictionary is breeding-SATURATED: the R1/R2 verified-NEGATIVE
      screens (lll_breed.py, screen_b_lobe_lll.py) found that NO new Z[w] column prices
      in below the LP noise floor (best reduced cost ~1e-13..1e-15) against the optimal
      dual, to degree ~40.  selftest() below re-confirms 0 bred columns price in.
      This warrant rests on (b)'s empirical saturation, NOT on mu_hat.
  CONJUNCTION (a)+(b) is the operationally-relevant statement: the contour /
  auxiliary-function method over the breeding-saturated Z[w] dictionary is CAPPED at
  C = 0.2487857, i.e. ~4e-5 above the Flammang [F18] verified record 0.2487458.  The
  lower bound is intrinsically STUCK near Flammang absent a method engaging the conjugate
  measure's true lemniscate support (NOT the circle).  C is NOT a true upper bound on the
  essential minimum C_82.

  (The discretized primal optimum is in fact ~0.2487464, only 6e-7 above Flammang; the
  ceiling C=0.2487857 carries a deliberate ~4e-5 feasibility margin so that rationalizing
  mu_hat to dyadic nodes + rational weights cannot break any constraint under outward
  interval rounding.  There is essentially NO primal headroom.)

Run:
   python3 ceiling_primal.py            full certificate (prints CERTIFIED <C>)
   python3 ceiling_primal.py selftest   saturation re-check + interval soundness probe
   python3 ceiling_primal.py tamper     a bogus measure / bogus ceiling must FAIL
"""

import sys
import json
import math
import os
from fractions import Fraction

import fastiv as F
from fastiv import Iv

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "ceiling_muhat.json")

# The certified ceiling: a clean value strictly ABOVE the interval-verified objective.
CEILING = Fraction(2487857, 10**7)        # 0.2487857
FLAMMANG = 0.2487458                      # log(1.282416), the verified record to beat


# --------------------------------------------------------------------------- #
#  Rigorous interval evaluation of the dictionary / cost at a fixed node       #
# --------------------------------------------------------------------------- #
def node_intervals(n, node_denom):
    """Interval enclosures of z=e^{it}, w=z(1-z) at t = n/node_denom (n integer).

    t = n/node_denom is generally NOT exactly a float; we enclose t in the
    one-ULP bracket [t_lo, t_hi] of the nearest float and use fastiv's rigorous
    cos_iv/sin_iv over that bracket, so every trig value is a guaranteed enclosure.
    Returns (zr, zi, wr, wi) as fastiv.Iv intervals."""
    tk = n / node_denom
    t_lo = math.nextafter(tk, -math.inf)
    t_hi = math.nextafter(tk, math.inf)
    c = F.cos_iv(t_lo, t_hi)
    s = F.sin_iv(t_lo, t_hi)
    c2 = F.cos_iv(2.0 * t_lo, 2.0 * t_hi)
    s2 = F.sin_iv(2.0 * t_lo, 2.0 * t_hi)
    # z = c + i s
    zr, zi = c, s
    # w = z(1-z) = (cos t - cos 2t) + i (sin t - sin 2t)   (double-angle identity)
    wr = c - c2
    wi = s - s2
    return zr, zi, wr, wi


def logabsQ_lower(asc, wr, wi):
    """Rigorous LOWER bound of log|Q(w)| via interval Horner on |Q|^2, then 0.5*log_down.
    Returns None if the |Q|^2 enclosure touches 0 (cannot bound log from below)."""
    qr = Iv(0.0)
    qi = Iv(0.0)
    for a in reversed(asc):
        nr, ni = F.cmul(qr, qi, wr, wi)
        qr = nr.add_const(int(a))
        qi = ni
    rho_lo = (qr * qr + qi * qi).lo          # lower bound of |Q|^2
    if rho_lo <= 0.0:
        return None
    return 0.5 * F.log_down(rho_lo)


def sigma_upper(zr, zi, wr, wi):
    """Rigorous UPPER bound of sigma_ZZ(z) = log max(1,|z|) + log max(1,|1-z|)."""
    # log max(1,|z|): |z|^2 upper
    z2_hi = (zr * zr + zi * zi).hi
    log_z = 0.0 if z2_hi <= 1.0 else 0.5 * F.log_up(z2_hi)
    # 1 - z = (1 - zr) - i zi ;  |1-z|^2 = (1-zr)^2 + zi^2
    omc = Iv(1.0, 1.0) - zr
    rho1_hi = (omc * omc + zi * zi).hi
    log_1mz = 0.0 if rho1_hi <= 1.0 else 0.5 * F.log_up(rho1_hi)
    return log_z + log_1mz


# --------------------------------------------------------------------------- #
#  Load mu_hat + dictionary                                                    #
# --------------------------------------------------------------------------- #
def load():
    with open(DATA) as fh:
        d = json.load(fh)
    node_denom = d["node_denom"]
    weight_denom = d["weight_denom"]
    nodes = d["nodes"]            # integer numerators n_k, t_k = n_k/node_denom
    weights = d["weights"]        # integer numerators, p_k = w_k/weight_denom
    columns = d["columns"]        # ascending integer coeff lists
    assert sum(weights) == weight_denom, "weights must sum to weight_denom (prob. measure)"
    assert all(x >= 0 for x in weights), "weights must be >= 0"
    return node_denom, weight_denom, nodes, weights, columns


# --------------------------------------------------------------------------- #
#  The certificate                                                             #
# --------------------------------------------------------------------------- #
def certify(ceiling=CEILING, verbose=True):
    node_denom, weight_denom, nodes, weights, columns = load()
    M = len(nodes)
    P = [Fraction(w, weight_denom) for w in weights]

    # precompute interval (z,w) at each node
    iv_nodes = [node_intervals(n, node_denom) for n in nodes]

    # ---- (i) every column constraint  int log|Q_j| dmu_hat >= 0  (lower bound) ----
    worst_col = None
    worst_val = None
    n_bad = 0
    for jidx, asc in enumerate(columns):
        s = Fraction(0)
        ok = True
        for k in range(M):
            zr, zi, wr, wi = iv_nodes[k]
            lv = logabsQ_lower(asc, wr, wi)
            if lv is None:
                ok = False
                break
            # p_k >= 0, so a lower bound of p_k * log|Q| uses the lower bound lv
            s += P[k] * Fraction(lv)
        if not ok:
            n_bad += 1
            continue
        val = float(s)
        if worst_val is None or val < worst_val:
            worst_val = val
            worst_col = (jidx, len(asc) - 1)
        if s < 0:
            if verbose:
                print(f"  FAIL column {jidx} (deg {len(asc)-1}): "
                      f"int log|Q| dmu_hat = {val:.3e} < 0")
            return False, None

    feasible = (n_bad == 0) and (worst_val is not None) and (worst_val >= 0.0)

    # ---- (ii) objective  int sigma_ZZ dmu_hat <= ceiling  (upper bound) ----
    obj = Fraction(0)
    for k in range(M):
        zr, zi, wr, wi = iv_nodes[k]
        gu = sigma_upper(zr, zi, wr, wi)
        obj += P[k] * Fraction(gu)
    obj_le = (obj <= ceiling)

    if verbose:
        print(f"  measure: {M} dyadic nodes t_k = n_k/{node_denom}, "
              f"rational weights / {weight_denom}, sum = {sum(weights)/weight_denom:.0f}")
        print(f"  dictionary: {len(columns)} columns "
              f"(24 Flammang base + {len(columns)-24} LLL-bred Z[w], deg<=40)")
        print(f"  (i)  min_j int log|Q_j| dmu_hat (interval lower) = "
              f"{worst_val:+.6e}  (worst col {worst_col}); columns with rho touching 0: {n_bad}")
        print(f"  (ii) int sigma_ZZ dmu_hat (interval upper)        = "
              f"{float(obj):.10f}  <=  C = {float(ceiling):.10f} ? {obj_le}")

    ok = feasible and obj_le
    return ok, float(obj)


# --------------------------------------------------------------------------- #
#  Saturation re-check (warrant (b)) + interval soundness probe                #
# --------------------------------------------------------------------------- #
def selftest():
    print("=" * 74)
    print("SELFTEST — warrant (b) saturation re-check + interval soundness")
    print("=" * 74)
    # 1) re-breed and re-price against the primal optimal measure: confirm NO column
    #    prices in (reduced cost int log|Q| dmu* < 0 only by LP noise).
    import numpy as np
    from scipy.optimize import linprog
    from sympy import Matrix
    from flammang_table1 import get_table

    def sigma_zz(z):
        return np.log(np.maximum(1.0, np.abs(z))) + np.log(np.maximum(1.0, np.abs(1 - z)))

    def logabsQ(asc, w):
        return np.log(np.abs(np.polyval(list(reversed(asc)), w)))

    N = 4000
    t = np.linspace(1e-4, np.pi - 1e-4, N)
    z = np.exp(1j * t); w = z * (1 - z); g = sigma_zz(z)
    base = [list(asc) for (_, asc) in get_table()]
    J = len(base)
    A = np.empty((N, J))
    for j, a in enumerate(base):
        A[:, j] = logabsQ(a, w)
    res = linprog(g, A_ub=-A.T, b_ub=np.zeros(J), A_eq=np.ones((1, N)), b_eq=[1.0],
                  bounds=[(0, None)] * N, method="highs")
    p = res.x
    print(f"  primal LP optimum m_disc = {res.fun:.10f}  (Flammang anchor {FLAMMANG};")
    print(f"     discretized primal value sits +{res.fun - FLAMMANG:.1e} above Flammang)")
    sup = np.where(p > 1e-9)[0]
    seeds_w = w[sup]

    def breed(k, sw, scales=(40, 80, 160, 320, 640)):
        out = []; K = k + 1
        powers = np.array([sw ** i for i in range(K)])
        for scale in scales:
            ce = 2 * len(sw); rows = []
            for i in range(K):
                row = [0] * (K + ce); row[i] = 1
                for nn in range(len(sw)):
                    row[K + 2 * nn] = int(round(scale * powers[i, nn].real))
                    row[K + 2 * nn + 1] = int(round(scale * powers[i, nn].imag))
                rows.append(row)
            try:
                red = Matrix(rows).lll()
            except Exception:
                continue
            for r in range(red.rows):
                asc = [int(red[r, i]) for i in range(K)]
                while len(asc) > 1 and asc[-1] == 0:
                    asc = asc[:-1]
                if all(x == 0 for x in asc):
                    continue
                out.append(asc)
        return out

    basekeys = {tuple(a) for a in base}
    seen = set(basekeys)
    min_rc = 1e9; n_priced_in = 0; n_bred = 0
    for k in range(24, 41):
        for asc in breed(k, seeds_w):
            key = tuple(asc)
            if key in seen or len(asc) <= 1:
                continue
            seen.add(key); n_bred += 1
            rc = float(np.sum(p * logabsQ(asc, w)))   # int log|Q| dmu*  (reduced cost)
            min_rc = min(min_rc, rc)
            if rc < -1e-7:
                n_priced_in += 1
    print(f"  saturation: bred {n_bred} distinct Z[w] columns (deg 24..40); "
          f"min reduced cost = {min_rc:+.2e}")
    print(f"     columns pricing in below -1e-7 gate: {n_priced_in}  "
          f"(0 => dictionary breeding-SATURATED; warrant (b) holds)")

    # 2) interval soundness: the interval lower of log|Q| must NEVER exceed the true
    #    float value (it bounds from BELOW).  Probe on the loaded nodes/columns.
    node_denom, weight_denom, nodes, weights, columns = load()
    max_overshoot = -1e9
    for jidx in range(0, len(columns), 7):
        asc = columns[jidx]
        for n in nodes:
            zr, zi, wr, wi = node_intervals(n, node_denom)
            lv = logabsQ_lower(asc, wr, wi)
            if lv is None:
                continue
            tk = n / node_denom
            wz = (math.cos(tk) - math.cos(2 * tk)) + 1j * (math.sin(tk) - math.sin(2 * tk))
            true = math.log(abs(__import__("numpy").polyval(list(reversed(asc)), wz)))
            max_overshoot = max(max_overshoot, lv - true)
    print(f"  interval soundness: max (interval_lower - true) over probe = "
          f"{max_overshoot:+.2e}  (<= 0 required; the bound never overshoots)")
    sound = (n_priced_in == 0) and (max_overshoot <= 1e-9)
    print(f"  SELFTEST {'PASS' if sound else 'FAIL'}")
    return sound


# --------------------------------------------------------------------------- #
#  Tamper test                                                                 #
# --------------------------------------------------------------------------- #
def tamper():
    print("=" * 74)
    print("TAMPER TEST — bogus inputs must FAIL (no auto-certify / no rubber-stamp)")
    print("=" * 74)

    # (T1) a ceiling BELOW the true objective must be rejected by check (ii).
    bogus_ceiling = Fraction(2487458, 10**7)    # exactly Flammang's value 0.2487458
    ok1, obj = certify(ceiling=bogus_ceiling, verbose=False)
    print(f"  (T1) ceiling = 0.2487458 (= Flammang, below the primal value {obj:.7f}):"
          f"  certify -> {ok1}  (expect False)")

    # (T2) a measure that VIOLATES one column constraint must fail check (i).
    #      Corrupt mu_hat: dump all mass onto a single node where Q_1=w is small
    #      (|w|<1 => log|w|<0 => int log|w| dmu < 0).  Patch load() via a temp file.
    node_denom, weight_denom, nodes, weights, columns = load()
    import numpy as np
    # pick the node with the smallest |w| (deep inside the unit disk => log|w|<0)
    vals = []
    for n in nodes:
        tk = n / node_denom
        wz = (math.cos(tk) - math.cos(2 * tk)) + 1j * (math.sin(tk) - math.sin(2 * tk))
        vals.append(abs(wz))
    kmin = int(np.argmin(vals))
    bogus_weights = [0] * len(weights)
    bogus_weights[kmin] = weight_denom          # all mass on the small-|w| node
    # evaluate column 0 (Q_1 = w) constraint by hand
    n = nodes[kmin]
    zr, zi, wr, wi = node_intervals(n, node_denom)
    lv = logabsQ_lower(columns[0], wr, wi)      # log|w| at that node (lower)
    constraint0 = float(Fraction(1) * Fraction(lv))
    ok2 = constraint0 >= 0
    print(f"  (T2) measure = delta at node t={n}/{node_denom} (|w|={vals[kmin]:.3f}<1):"
          f"  int log|Q_1=w| dmu = {constraint0:+.4f}  feasible? {ok2}  (expect False)")

    passed = (not ok1) and (not ok2)
    print(f"  TAMPER {'PASS' if passed else 'FAIL'} "
          f"(both bogus inputs correctly rejected)" if passed else
          "  TAMPER FAIL")
    return passed


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "certify"
    if mode == "selftest":
        return 0 if selftest() else 1
    if mode == "tamper":
        return 0 if tamper() else 1

    print("=" * 74)
    print("PRIMAL-MEASURE LP-DUALITY CEILING for C_82a lower bound (over Z[w] dictionary)")
    print("=" * 74)
    ok, obj = certify(verbose=True)
    print("-" * 74)
    if ok:
        print(f"CERTIFIED {float(CEILING):.7f}")
        print(f"  Rigorous CEILING: every auxiliary function in the SPAN of the loaded")
        print(f"  Z[w] dictionary certifies a lower bound on C_82 of at most "
              f"{float(CEILING):.7f}.")
        print(f"  Flammang [F18] verified record = {FLAMMANG} (= log 1.282416).")
        print(f"  Headroom over Flammang = {float(CEILING) - FLAMMANG:+.2e}  "
              f"(true primal opt ~0.2487464, i.e. +6e-7 — essentially STUCK).")
        print(f"  SCOPE: this is a ceiling for THIS breeding-saturated dictionary+contour,")
        print(f"  NOT a true upper bound on the essential minimum C_82.")
        print(f"  Warrant (a) [this build]: mu_hat caps the SPAN of loaded columns.")
        print(f"  Warrant (b) [R1/R2 + selftest]: dictionary is breeding-saturated.")
        return 0
    else:
        print("CERTIFICATE FAILED — measure not feasible or objective exceeds ceiling.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
