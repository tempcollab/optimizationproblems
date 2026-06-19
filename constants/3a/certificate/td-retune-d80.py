"""Sketch: td-retune-d80  (constant 3a, LOWER bound)  -- ROUND 2 BUILD

TARGET (top-level claim):
    For the record digit alphabet A = {0,2,3,4,5,6,7,8,9,10} (base b = 2*max(A)+1 = 21),
    digit count d = 80, there exists a global sum cap T (NOT necessarily Griego's T=150) such
    that the exactly-counted set
        U = { sum_i a_i b^i : a_i in A, sum_i a_i <= T }
    satisfies
        1 + log(|U-U| / |U+U|) / log(2*max(U)+1)  >  1.1740744.
    By the GHR2007 single-set lemma this is a valid lower bound on C_3a, strictly beating the
    record [G2026] = 1.1740744 (achieved at the SAME alphabet and d but T = 150).

RESULT THIS ROUND:  the winning cap is T = 154.  Exact-integer DP gives
        |U+U| = (see S154 below),  |U-U| = (see D154),  max(U) = (see M154).
    A directed-rounded RATIONAL lower bound on theta (all arithmetic exact Fraction, the only
    transcendental step bounded by a truncated atanh series with a signed tail) certifies
        theta_lb = 1.174171...  >  11740744/10000000 = 1.1740744 = record.
    The margin (theta_lb - record ~ 9.7e-5) survives the directed rounding.  HOLES H1/H2/H3
    are CLOSED below; the script reproduces the certificate end-to-end.

STRATEGY (cheapest concrete shot; borrows the engine from alphabet-search-dp and the atanh
log primitives from per-position-alphabet):
    The math-explorer (round 2) found that Griego's T/d ratio is mildly off-optimal: holding the
    record alphabet fixed, the theta-vs-T/d curve PEAKS near T/d = 1.90-1.95, ABOVE Griego's
    1.875 = 150/80.  At d=80 the analogue is T ~ 152-156.  The ONLY free knob is T: a
    one-parameter scan of exact DP runs at d=80 around T in {150,152,154,156,158}.  T=154 wins.

CERTIFICATE DESIGN (the load-bearing H3 fix, replacing the broken shared path):
    per-position-alphabet.certify_theta_lb ran the atanh log series DIRECTLY on q ~ 21^80 and on
    diff/s ~ 1e18.  For both, z = (x-1)/(x+1) ~ 1, so the series needs ~1e106 terms and silently
    returns a useless bound (theta_lb collapses to ~1.0).  THIS sketch fixes it with the
    base-b reduction Griego's template uses:  for any integer N >= 1, with k = floor(log_b N),
        log(N) = k * log(b) + log(N / b^k),   N / b^k in [1, b),
    so the residual ratio's z <= (b-1)/(b+1) = 20/22 ~ 0.909 and the atanh series converges in a
    few hundred terms.  log(b) = log(21) itself is bounded by the same atanh series (z = 10/11).
    Directed rounding:
        * numerator  log(diff) - log(s):  LOWER bound on log(diff) (k_d * logb_LB + atanh-LB of
          residual), UPPER bound on log(s) (k_s * logb_UB + atanh-UB of residual);
        * denominator log(q):             UPPER bound (k_q * logb_UB + atanh-UB of residual).
    Every term is exact Fraction; truncation/tail are in the safe (conservative) direction, so
    theta_lb is a rigorous lower bound on the true theta.  Validated on Griego's record instance
    (reproduces theta_lb = 1.17407444769 to 12 digits, matching float) before use here.

ENGINE (sped up this round): ghr_dp.diffset_fast (numpy 2D shift-add, <1 s) and
    ghr_dp.sumset_bitmask (big-int bitmask, ~170 s at d=80). Both validated exact-match vs the
    frozenset oracle (ghr_dp.__main__) and against Griego's literals. Every DP point prints a
    progress line with flush=True so a long run never looks like a hang.

USAGE:
    python td-retune-d80.py            # full pipeline: ~170 s sumset DP, then certify (default)
    python td-retune-d80.py --scan     # re-run the T-scan around 150-158 (one point at a time)
    python td-retune-d80.py --replay   # certify from the cached exact counts only (seconds)
"""

import sys
import os
import time
from math import log
from fractions import Fraction

sys.path.insert(0, os.path.dirname(__file__))
from ghr_dp import (  # noqa
    diffset_fast, sumset_bitmask, max_U, theta_floatbound_fast,
    sumset_size, diffset_size, carry_free_base,
)

# Reuse ONLY the well-conditioned atanh primitives from per-position-alphabet (NOT its broken
# certify_theta_lb, which feeds q/diff-over-s into the series at z~1).  We call them only on
# residual ratios in [1, b) and on b itself, where they converge.
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("_pp", os.path.join(os.path.dirname(__file__), "per-position-alphabet.py"))
_pp = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_pp)
_log_lb = _pp._log_lb   # rational LOWER bound on log(num/den), num>=den>=1, valid for any z<1
_log_ub = _pp._log_ub   # rational UPPER bound on log(num/den), num>=den>=1, valid for any z<1

RECORD = 1.1740744
RECORD_FRAC = Fraction(11740744, 10000000)  # exact rational floor we must strictly exceed
ARECORD = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
D = 80
B = carry_free_base(ARECORD)  # = 21
T_WINDOW = [150, 152, 154, 156, 158]  # the one-parameter scan
T_WIN = 154                            # the winner found by the scan (see H1 below)

# --- Cached exact-integer DP counts for the winning T=154 (reproduced by exact_confirm) -------
# These are EXACT integers from the validated fast DP (sumset_bitmask + diffset_fast), each
# cross-checked vs the frozenset oracle on small/medium cases in ghr_dp.__main__ and below.
S154 = 597130362133498688344900538759091221981599964605490705452812019502078419618406
D154 = 1583022697814754823730226433460816281662151877595631959725969360255416773109712840757177539870935
M154 = 2995805288150731620427416034073013045407712819639364547243511761614441608214402813704058986719974740854874


# =============================================================================================
# H1 -- T-SCAN (CLOSED): one-parameter scan at d=80, record alphabet.  T=154 wins on float-theta.
# =============================================================================================

def t_scan(window=None, verbose=True):
    """HOLE H1 -- CLOSED.  One-parameter T-scan at d=80, record alphabet, fast exact DP.

    Each point is ~170 s (sumset dominates) and prints a per-stage line; the loop is chunked one
    T at a time.  Reproduced this round:
        T=150 -> theta=1.1740744477  (= Griego's record literal, sanity)
        T=154 -> theta=1.1741713540  (+9.7e-5 over the record on float; the WINNER)
    Returns (best_T, best_theta, results).
    """
    window = window or T_WINDOW
    results = []
    for T in window:
        t0 = time.time()
        th, s, diff, q = theta_floatbound_fast(ARECORD, D, T, verbose=verbose)
        results.append((T, th, s, diff, q))
        if verbose:
            flag = "  <-- beats record" if th > RECORD else ""
            print(f"[H1] T={T} float-theta={th:.10f} ({time.time()-t0:.0f}s){flag}", flush=True)
    best_T, best_theta = max(((T, th) for T, th, *_ in results), key=lambda t: t[1])
    return best_T, best_theta, results


# =============================================================================================
# H2 -- EXACT CONFIRM (CLOSED): exact integer counts for the winning T, two independent fast
# paths, cross-checked vs the slow frozenset oracle on a medium case for added safety.
# =============================================================================================

def _oracle_crosscheck():
    """Belt-and-suspenders: confirm the fast routines == the frozenset/2D oracle on a medium
    d (where the oracle is still feasible) at the record alphabet.  The d=80 instance itself is
    cross-checked at small/medium d in ghr_dp.__main__; here we add a d=20 check at the live T/d
    ratio so the exact d=80 literals rest on agreement of THREE independent implementations.
    """
    A = ARECORD
    for d0, T0 in [(8, 15), (12, 23), (20, 39)]:
        assert sumset_bitmask(A, d0, T0) == sumset_size(A, d0, T0), (d0, T0)
        assert diffset_fast(A, d0, T0) == diffset_size(A, d0, T0), (d0, T0)
    return True


def exact_confirm(T=T_WIN, verbose=True):
    """HOLE H2 -- CLOSED.  Exact integer counts |U+U|, |U-U|, max(U), q = 2 max(U)+1 for T.

    Computes via the two fast routines; for the cached winner T=154 it also asserts they match
    the cached literals S154/D154/M154 (so --replay needs no DP).  Returns (s, diff, m, q).
    """
    if verbose:
        print(f"[H2] exact counts at d={D}, T={T} (fast DP, ~170 s) ...", flush=True)
    t0 = time.time()
    diff = diffset_fast(ARECORD, D, T)
    if verbose:
        print(f"[H2]   diffset done ({time.time()-t0:.0f}s)", flush=True)
    t1 = time.time()
    s = sumset_bitmask(ARECORD, D, T)
    if verbose:
        print(f"[H2]   sumset done ({time.time()-t1:.0f}s)", flush=True)
    m = max_U(ARECORD, D, T)
    q = 2 * m + 1
    if T == T_WIN:
        assert s == S154 and diff == D154 and m == M154, "fast DP disagrees with cached T=154 literals"
    return s, diff, m, q


# =============================================================================================
# H3 -- CERTIFY (CLOSED): directed-rounded rational lower bound on theta via base-b log reduction.
# =============================================================================================

def _round_down_decimal(frac, places):
    """Decimal string of `frac` truncated DOWN to `places` digits (so it stays a valid lower
    bound).  Avoids str()-ing the multi-thousand-digit exact Fraction."""
    scaled = (frac.numerator * 10 ** places) // frac.denominator  # floor
    ip, fp = divmod(scaled, 10 ** places)
    return f"{ip}.{fp:0{places}d}"


def _floor_log_b(N, b):
    """Largest integer k with b^k <= N  (N >= 1, b >= 2).  Exact integer arithmetic."""
    assert N >= 1 and b >= 2
    k = 0
    p = 1
    while p * b <= N:
        p *= b
        k += 1
    return k


def _log_big_lb(N, b, logb_lb, terms):
    """Rational LOWER bound on log(N), N >= 1.  log(N) = k*log(b) + log(N/b^k), residual in
    [1,b).  k >= 0 and logb_lb <= log(b), and _log_lb(N, b^k) <= log(N/b^k); both signs safe."""
    k = _floor_log_b(N, b)
    return k * logb_lb + _log_lb(N, b ** k, terms)


def _log_big_ub(N, b, logb_ub, terms):
    """Rational UPPER bound on log(N), N >= 1.  Same reduction; logb_ub >= log(b) and
    _log_ub(N, b^k) >= log(N/b^k); both signs safe."""
    k = _floor_log_b(N, b)
    return k * logb_ub + _log_ub(N, b ** k, terms)


def certify_theta_lb(s, diff, q, b=B, terms=400):
    """Directed-rounded rational LOWER bound on theta = 1 + log(diff/s)/log(q).

    Requires diff >= s >= 1 and q >= 2.  The fraction (log diff - log s)/log q is positive, so a
    lower bound on theta needs a LOWER bound on the numerator and an UPPER bound on the
    denominator:
        num_lb = log_big_lb(diff) - log_big_ub(s)   (<= log diff - log s)
        den_ub = log_big_ub(q)                       (>= log q)
        theta_lb = 1 + num_lb / den_ub               (<= true theta)
    All logs reduced to base b first so the atanh series runs only on residuals in [1,b) and on
    b itself (z <= 20/22), where it converges.  Returns (theta_lb : Fraction, beats : bool).
    """
    assert diff >= s >= 1 and q >= 2
    logb_lb = _log_lb(b, 1, terms)   # <= log(b)
    logb_ub = _log_ub(b, 1, terms)   # >= log(b)
    assert logb_lb > 0
    num_lb = _log_big_lb(diff, b, logb_lb, terms) - _log_big_ub(s, b, logb_ub, terms)
    den_ub = _log_big_ub(q, b, logb_ub, terms)
    assert num_lb >= 0 and den_ub > 0
    theta_lb = 1 + num_lb / den_ub
    return theta_lb, theta_lb > RECORD_FRAC


def _validate_certify_on_record(terms=400):
    """Before trusting the certificate on T=154, confirm it reproduces Griego's record theta to
    full precision and lands a LOWER bound (directed rounding in the safe direction)."""
    s = 75448362167176243488362019935078206851619643198150854886920234689186981134888
    diff = 195351744295266763842135520514417052287242446785296742323733058216909095059024572338564089814415
    m = max_U(ARECORD, D, 150)
    q = 2 * m + 1
    theta_lb, beats = certify_theta_lb(s, diff, q, terms=terms)
    theta_float = 1 + (log(diff) - log(s)) / log(q)
    flb = float(theta_lb)
    assert flb <= theta_float + 1e-12, (flb, theta_float)          # genuine lower bound
    assert theta_float - flb < 1e-9, (theta_float - flb)            # and tight
    assert beats  # record's own theta 1.17407444769 > 1.1740744
    print(f"[H3] certify validated on record: theta_lb={flb:.12f} (float {theta_float:.12f})", flush=True)
    return theta_lb


# =============================================================================================
# MAIN -- end-to-end certified bound at T=154
# =============================================================================================

def run_full(do_dp=True):
    print(f"[setup] A={ARECORD}, b={B}, d={D}; target to beat = {RECORD} [G2026]", flush=True)
    _oracle_crosscheck()
    print("[H2] fast routines == frozenset oracle on small/medium cases (3 impls agree)", flush=True)
    _validate_certify_on_record()
    if do_dp:
        s, diff, m, q = exact_confirm(T_WIN)
    else:
        print("[H2] --replay: using cached exact T=154 literals (no DP)", flush=True)
        s, diff, m, q = S154, D154, M154, 2 * M154 + 1
        # still re-derive max(U) cheaply (it is fast) to guard the cached literal
        assert max_U(ARECORD, D, T_WIN) == M154
    print(f"[H2] T={T_WIN}: |U+U|={s}", flush=True)
    print(f"[H2] T={T_WIN}: |U-U|={diff}", flush=True)
    print(f"[H2] T={T_WIN}: max(U)={m}", flush=True)
    theta_lb, beats = certify_theta_lb(s, diff, q)
    theta_float = 1 + (log(diff) - log(s)) / log(q)
    # theta_lb is an exact Fraction with ~thousands of digits (terms=400); show a directed-DOWN
    # decimal truncation (still a valid lower bound) and the float cross-check, never the raw ratio.
    dec_lb = _round_down_decimal(theta_lb, 15)
    print(f"[H3] CERTIFIED theta_lb >= {dec_lb}  (exact rational, shown round-DOWN to 15 places)", flush=True)
    print(f"[H3]            float check {theta_float:.12f}", flush=True)
    print(f"[H3] record = {RECORD}; beats strictly = {beats}", flush=True)
    margin = theta_lb - RECORD_FRAC
    print(f"[H3] rational margin over record = {float(margin):.3e}", flush=True)
    assert beats, "certificate did NOT clear the record -- do not claim a bound"
    print("[OK] verified lower bound on C_3a:", float(theta_lb), ">", RECORD, flush=True)
    return theta_lb, beats


if __name__ == "__main__":
    if "--scan" in sys.argv:
        bt, bth, _ = t_scan()
        print(f"[H1] best T={bt} float-theta={bth:.10f}", flush=True)
    elif "--replay" in sys.argv:
        run_full(do_dp=False)
    else:
        run_full(do_dp=True)
