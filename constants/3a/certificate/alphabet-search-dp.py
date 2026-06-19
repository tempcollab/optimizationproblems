"""Sketch: alphabet-search-dp  (constant 3a, LOWER bound)

TARGET (top-level claim):
    There exist a finite digit alphabet A (0 in A), digit count d, global sum cap T, with
    carry-free base b = 2*max(A)+1, such that the exactly-counted set
        U = { sum_i a_i b^i : a_i in A, sum a_i <= T }
    satisfies
        1 + log(|U-U| / |U+U|) / log(2*max(U)+1)  >  1.1740744.
    By the GHR2007 single-set lemma this is a valid lower bound on C_3a, strictly beating
    the record [G2026] = 1.1740744.

STRATEGY (re-scoped, round 2):
    The HOMOGENEOUS record alphabet A={0,2..10} is SATURATED (explorer Finding A: Griego's
    {0,2..10} wins every omission variant at d=40).  So drop blind alphabet edits and re-aim
    at LONGER d at a RE-TUNED cap ratio: theta rises with d toward the asymptote, and the
    optimal T/d sits ABOVE Griego's 1.875 (the d=40 scan peaks near c=1.95-1.975, interior).
    The length gain compounds with the T/d gain.  Re-optimize (d, T) on the SAME validated
    exact-integer DP, then certify the winner with a directed-rounded RATIONAL log bound.

LOAD-BEARING FIX THIS ROUND (H3, certify path):
    The shared per-position `certify_theta_lb` bounded log(q) by running the atanh series
    DIRECTLY on q ~ 21^80.  There z=(q-1)/(q+1)=1-3.3e-106 so the series needs ~1e106 terms
    and returns garbage (theta_lb collapses).  The SAME flaw afflicts the numerator: diff/s
    ~ 1e18 also has z=1, so log(diff/s) diverged too.  FIXED here with a SCALED base-2
    expansion (Griego's base-b template, instantiated at b=2): for any integer N>=1,
        log N = k*log 2 + log(N / 2^k),   k = floor(log2 N) = N.bit_length()-1,
    where N/2^k in [1,2) so z=(N/2^k - 1)/(N/2^k + 1) in [0,1/3] and the atanh series
    converges in a few hundred terms.  log 2 itself is bounded by atanh at z=1/3 (fast).
    All arithmetic is exact `Fraction`; truncation directions are chosen so the certified
    theta_lb is a true LOWER bound on theta (validated against float on the record).

HOLES (status):
  (H1) SEARCH -- CLOSED (round 2).  The longer-d + retuned-T/d scan FOUND d=84, T=162.
  (H1') LONGER-d FRONTIER (d=88, d=96) -- CLOSED this round (round 3).  Scanned d=88 and
       d=96 at the re-tuned T/d grid, ONE point per invocation (sumset bitmask ~267 s/pt at
       d=88, ~400 s/pt at d=96, diffset <2 s; all under the silent-run ceiling, flush=True
       progress).  Both d have an INTERIOR peak; ALL scanned points beat HELD:
         d=88: T=167->1.17475046, 168->1.17476379, *169->1.17476434 (peak)*,
               170->1.17475214, 171->1.17472719   (c_peak = 1.9205)
         d=96: T=182->1.17526075, 183->1.17527164, *184->1.17527174 (peak)*,
               185->1.17526106, 186->1.17523960   (c_peak = 1.9167)
       The optimum c keeps drifting down with d (d=84:1.929 -> d=88:1.921 -> d=96:1.917) and
       theta keeps rising toward the asymptote.  Winners cached in WINNERS with exact counts.
  (H2) EXACT CONFIRM -- CLOSED.  exact_confirm() recomputes |U+U|,|U-U|,max(U) as exact ints
       with the fast routines (validated vs the oracle on small cases + vs Griego's literals);
       the winning counts are cached in WINNERS and re-derivable with VERIFY_DP=1.  The d=96,
       T=184 winner's q was independently re-derived (max_U) and matches the cached literal.
  (H3) CERTIFY -- CLOSED (round 2): directed-rounded rational theta_lb via scaled base-2
       log bounds (certify_theta_lb_scaled below; identical to the reviewer-certified
       lemmas/log_bounds.py).  Validated on the record (matches float, beats with margin
       4.77e-8); applied to the d=96, T=184 winner -> certified theta_lb = 1.1752717416788478
       (terms=300 already saturated; terms in {300,350,400,500} all give the same safe value).

>>> RESULT (round 3): certified LOWER bound C_3a >= 1.1752717416788478, the NEW BEST, strictly
    above the prior held 1.1744750903655619 (+7.97e-4) and the record 1.1740744 [G2026]
    (+1.20e-3).  Construction: A={0,2,3,4,5,6,7,8,9,10}, d=96, T=184, base 21 (c=T/d=1.9167).
    All steps are exact-integer DP + directed-rounded rational log bounds; no hole on the path.

Running this file (<1 s from cached literals): validates the engine + the fixed certifier on
the record, then certifies the stored winners.  Set VERIFY_DP=1 to re-run the ~230 s DP and
assert the cached counts.
"""

import sys
import os
from fractions import Fraction

sys.path.insert(0, os.path.dirname(__file__))
from ghr_dp import (  # noqa
    sumset_size, diffset_size, max_U, theta_floatbound, carry_free_base,
    diffset_fast, sumset_bitmask, theta_floatbound_fast,
)

RECORD = 1.1740744
RECORD_FRAC = Fraction(11740744, 10000000)  # exact rational floor we must strictly exceed


# ---------------------------------------------------------------------------
# H3 CERTIFY (CLOSED): directed-rounded rational LOWER bound on theta
# ---------------------------------------------------------------------------
#
# atanh series:  log(x) = 2 * sum_{k>=0} z^(2k+1)/(2k+1),  z = (x-1)/(x+1) in [0,1).
# Every term is nonnegative => any finite partial sum is a LOWER bound on log(x).
# Tail after N terms:  2*sum_{k>=N} z^(2k+1)/(2k+1) <= (2/(2N+1)) * z^(2N+1)/(1-z^2)
# (1/(2k+1) <= 1/(2N+1), then geometric sum) => partial+tail is an UPPER bound.
# We only ever call these with x in [1,2) (so z <= 1/3), where convergence is fast.

def _log_small_lb(num, den, terms):
    """LOWER bound on log(num/den) for 1 <= num/den < 2 (exact Fraction, truncated)."""
    x = Fraction(num, den)
    z = (x - 1) / (x + 1)
    z2 = z * z
    s = Fraction(0)
    zk = z
    for k in range(terms):
        s += zk / (2 * k + 1)
        zk *= z2
    return 2 * s


def _log_small_ub(num, den, terms):
    """UPPER bound on log(num/den) for 1 <= num/den < 2 (partial sum + geometric tail)."""
    x = Fraction(num, den)
    z = (x - 1) / (x + 1)
    z2 = z * z
    s = Fraction(0)
    zk = z
    for k in range(terms):
        s += zk / (2 * k + 1)
        zk *= z2
    tail = zk / (2 * terms + 1) / (1 - z2)   # zk == z^(2*terms+1) here
    return 2 * (s + tail)


def _floor_log2(N):
    """k, 2^k with 2^k <= N < 2^(k+1) for N >= 1 (exact, no float)."""
    k = N.bit_length() - 1
    return k, 1 << k


_LOG2_LB_CACHE = {}
_LOG2_UB_CACHE = {}


def _log2_lb(terms):
    if terms not in _LOG2_LB_CACHE:
        _LOG2_LB_CACHE[terms] = _log_small_lb(2, 1, terms)  # log 2, z=1/3
    return _LOG2_LB_CACHE[terms]


def _log2_ub(terms):
    if terms not in _LOG2_UB_CACHE:
        _LOG2_UB_CACHE[terms] = _log_small_ub(2, 1, terms)
    return _LOG2_UB_CACHE[terms]


def logN_lb(N, terms=300):
    """LOWER bound on log(N), N >= 1, via scaled base-2 expansion.
        log N = k*log 2 + log(N / 2^k),   N/2^k in [1,2).
    Lower-bound both pieces (each >= 0)."""
    assert N >= 1
    k, bk = _floor_log2(N)
    return k * _log2_lb(terms) + _log_small_lb(N, bk, terms)


def logN_ub(N, terms=300):
    """UPPER bound on log(N), N >= 1, via scaled base-2 expansion."""
    assert N >= 1
    k, bk = _floor_log2(N)
    return k * _log2_ub(terms) + _log_small_ub(N, bk, terms)


def certify_theta_lb_scaled(s, diff, q, terms=300):
    """Directed-rounded rational LOWER bound on
        theta = 1 + log(diff/s) / log(q),   diff >= s >= 1, q >= 2.
    Lower-bound the numerator (log diff lower, log s upper) and UPPER-bound the
    denominator log q, so the quotient -- hence theta -- is under-estimated.

    This REPLACES the shared per-position certify_theta_lb, whose atanh-on-huge-q
    (and on huge diff/s) diverged.  Returns (theta_lb : Fraction, beats : bool).
    """
    assert diff >= s >= 1 and q >= 2
    num_lb = logN_lb(diff, terms) - logN_ub(s, terms)   # <= log(diff/s)
    den_ub = logN_ub(q, terms)                          # >= log q
    assert num_lb >= 0 and den_ub > 0
    theta_lb = 1 + num_lb / den_ub                      # <= theta
    return theta_lb, theta_lb > RECORD_FRAC


def _check_certify_on_record():
    """The fixed certifier must reproduce the record's theta as a true (slightly conservative)
    LOWER bound, and report beats=True.  This is the H3 self-test (cheap: uses the known
    record literals, no DP)."""
    from math import log
    s = 75448362167176243488362019935078206851619643198150854886920234689186981134888
    diff = 195351744295266763842135520514417052287242446785296742323733058216909095059024572338564089814415
    q = 2 * (10 * sum(21 ** i for i in range(65, 80))) + 1
    theta_lb, beats = certify_theta_lb_scaled(s, diff, q, terms=300)
    theta_float = 1 + (log(diff) - log(s)) / log(q)
    flb = float(theta_lb)
    assert flb <= theta_float + 1e-12, (flb, theta_float)      # safe direction
    assert theta_float - flb < 1e-9, (theta_float - flb)        # tight
    assert beats, theta_lb
    print(f"[H3] fixed certifier validated on record: theta_lb={flb:.12f} "
          f"(float {theta_float:.12f}); beats RECORD={beats}; "
          f"margin={float(theta_lb - RECORD_FRAC):.3e}", flush=True)
    return theta_lb


# ---------------------------------------------------------------------------
# Engine sanity (cheap; full-scale fast routines validated in ghr_dp.__main__)
# ---------------------------------------------------------------------------

def sanity_record():
    A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for d0, T0 in [(8, 15), (10, 18)]:
        assert sumset_bitmask(A, d0, T0) == sumset_size(A, d0, T0)
        assert diffset_fast(A, d0, T0) == diffset_size(A, d0, T0)
    th, s, diff, q = theta_floatbound_fast(A, 12, 22)
    print(f"[engine check] fast routines match oracle; d=12,T=22 theta={th:.6f}", flush=True)
    return th


# ---------------------------------------------------------------------------
# H1 SEARCH (longer d, retuned T/d) + H2 exact confirm
# ---------------------------------------------------------------------------

A_REC = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Winning triples found by the longer-d retuned-T/d search (round 2), with their EXACT
# integer counts (s=|U+U|, diff=|U-U|, q=2*max(U)+1) cached so the certificate reproduces
# in <1 s without re-running the ~230 s DP.  Each was computed by the FAST routines
# (diffset_fast/sumset_bitmask, validated exact-match vs the frozenset/2D oracle on small
# cases and vs Griego's record literals at full scale).  Recompute with VERIFY_DP=1 (slow).
#
# Best certified: d=84, T=162 -> theta_lb = 1.1744750903655619  (margin +4.01e-4 over record).
# This sketch owns the LONGER-d frontier (d > 80); the d=80 retune is td-retune-d80's lane.
WINNERS = {
    (84, 162): dict(
        s=6097708534951589347439183607038270910158216193597072358058994024712092458076766270,
        diff=145710369635805984294872090934229656671521875518799257570738793680742528284363557961708618559623567675,
        q=1165254416489684872554618217361872378435684345652187969599710464819025051454571621932090673372945921527696090485,
        float_theta=1.1744750903655619,
    ),
    (84, 164): dict(
        s=16777722616407479187147504571629992614689318525575983076108586880851554003065008694,
        diff=395408260987655412181207585916583184388551911069273615252881628449017521960376630791972773544057686111,
        q=1165254416489684872554773367704321832783618869900619554858691396740867998558326013724405243400764220064810193449,
        float_theta=1.174420968969189,
    ),
    # --- ROUND 3 (hole H1' closed): the d=88 / d=96 frontier scan -----------------------
    # d=88 interior peak at T=169 (c=1.9205); float scan T in {167..171} all beat HELD,
    # peak at T=169 (167->1.17475046, 168->1.17476379, 169->1.17476434 PEAK,
    #                170->1.17475214, 171->1.17472719).
    (88, 169): dict(
        s=37426702858728646432282756452279923211302451814423993558049713846305746450715225147721,
        diff=8089822321128549482175445108898615340129429952564150606760178195018521495093392976519143508642843850587135,
        q=226619844173330403699400313808878995189192616963040449480352838082290594716834946150538880875774352576915570878314699,
        float_theta=1.1747643448523182,
    ),
    # d=96 interior peak at T=184 (c=1.9167); float scan T in {182..186}:
    #   182->1.17526075, 183->1.17527164, 184->1.17527174 PEAK, 185->1.17526106, 186->1.17523960.
    # This is the BEST construction this run: certified theta_lb = 1.1752717416788478,
    # +7.97e-4 over the HELD bound 1.1744750903655619, +1.20e-3 over the record 1.1740744.
    (96, 184): dict(
        s=2354612726795560198637539626081323633677464536763944205611915446610439936255355430057651233079,
        diff=41657829615040226466508207079583713163528747660407140693727914721760094182467298116869474627721404780883597620670119,
        q=8571410494579611166108619722960490736204749562145503217128903617006442204626527584995605100800210570065634413170633869420430689,
        float_theta=1.1752717416788478,
    ),
}


def search_for_better(d_list=(84, 88), c_list=(1.95, 1.975, 2.0), cap_T=200, verbose=True):
    """HOLE H1: longer-d + retuned-T/d float scan.  Fix A=A_REC (saturated alphabet).
    For each d in d_list, T = round(c*d) for c in c_list (capped at cap_T), compute the FAST
    float-theta one point at a time with progress printed.  Return the list of (d,T,theta)
    that strictly beat RECORD, sorted best-first.

    CHUNKED + progress-printed (flush=True) so a long run is never a silent hang.  The bitmask
    cost grows ~T^2; cap_T bounds per-point cost.  RUN THIS ROUND (round 2): d=84 with
    T in {160,162,164,166} all beat the record on float; the peak is interior at T=162
    (theta=1.17447509, c=1.929).  Each point's diffset is ~1 s; the sumset bitmask is the cost
    (~210-235 s at d=84).  The certified results are cached in WINNERS; this function is kept
    so the scan is re-runnable and extensible to d in {88,96}.
    """
    return _scan(d_list, c_list, cap_T, verbose)


# -- ROUND 3 EXTENSION (open hole H1'): the d=88 / d=96 frontier scan -----------------------
# The d=84 optimum sat at c=1.929 (interior; T=162).  The optimal c drifts DOWN slightly as d
# grows (d=40 peak ~1.95-1.975 -> d=84 peak ~1.92-1.93), so the d=88/96 optima are expected at
# c ~ 1.91-1.93.  PLAN for the builder (one point at a time, flush=True progress, never a single
# silent >600s call -- see per-role NEVER): scan the SMALL grid below, find the interior peak on
# float-theta, then cache its exact counts in WINNERS and certify with certify_theta_lb_scaled
# (the H3 path is already closed/reused).  Cost: sumset bitmask is ~T^2; at d=88,c~1.92 (T~169)
# expect ~250-280 s/point; at d=96,c~1.92 (T~184) expect ~300-340 s/point -- so run d=88 first,
# ONE T per invocation, and checkpoint.  Expected further gain: a further small +~1-2e-4 (the
# asymptote is still above 1.17448), diminishing per d-step.
D88_GRID = (87, 168, 169, 170, 171)   # d=88, T near c in [1.909, 1.943]
D96_GRID = (183, 184, 185, 186, 187)  # d=96, T near c in [1.906, 1.948]


def scan_d88(T_list=D88_GRID[1:], verbose=True):
    """HOLE H1' (OPEN, round 3): scan d=88 at the planned T-grid, ONE point at a time.
    The first element of D88_GRID is d=88; pass an explicit single T to do exactly one point
    (recommended -- keeps each invocation well under the silent-run ceiling)."""
    return _scan((88,), tuple(T / 88 for T in T_list), cap_T=max(T_list), verbose=verbose)


def scan_d96(T_list=D96_GRID, verbose=True):
    """HOLE H1' (OPEN, round 3): scan d=96 at the planned T-grid, ONE point at a time.
    Each d=96 point is ~300-340 s -- ALWAYS run exactly one T per invocation."""
    return _scan((96,), tuple(T / 96 for T in T_list), cap_T=max(T_list), verbose=verbose)


def _scan(d_list, c_list, cap_T, verbose):
    from math import log
    hits = []
    for d in d_list:
        Ts = sorted({min(round(c * d), cap_T) for c in c_list})
        for T in Ts:
            if verbose:
                print(f"  [H1] d={d} T={T} (c={T/d:.3f}) ...", flush=True)
            diff = diffset_fast(A_REC, d, T)
            s = sumset_bitmask(A_REC, d, T)
            q = 2 * max_U(A_REC, d, T) + 1
            th = 1 + (log(diff) - log(s)) / log(q)
            beats = th > RECORD
            if verbose:
                print(f"  [H1] d={d} T={T} theta={th:.10f}"
                      f"{'  <-- BEATS RECORD' if beats else ''}", flush=True)
            if beats:
                hits.append((d, T, th))
    hits.sort(key=lambda t: -t[2])
    return hits


def exact_confirm(A, d, T):
    """HOLE H2 (CLOSED for the stored winners): exact integer recomputation of the three counts.
    At d>=80 the frozenset oracle is too slow to run inline; the fast routines are validated
    exact-match vs the oracle on small cases (ghr_dp.__main__) and vs Griego's record literals
    at full scale, so we trust the fast routines and skip the inline oracle recompute for large
    d.  Returns (s, diff, q)."""
    s = sumset_bitmask(A, d, T)
    diff = diffset_fast(A, d, T)
    if d <= 12:  # only cross-check the slow oracle where it is cheap
        assert s == sumset_size(A, d, T) and diff == diffset_size(A, d, T), "fast/oracle mismatch"
    q = 2 * max_U(A, d, T) + 1
    return s, diff, q


def certify_winner(d, T, verify_dp=False, terms=300):
    """Certify a stored winning (d, T) from its cached exact counts.  If verify_dp, RE-RUN the
    fast DP (~230 s at d=84) and assert it matches the cached literals before certifying."""
    w = WINNERS[(d, T)]
    s, diff, q = w["s"], w["diff"], w["q"]
    if verify_dp:
        print(f"  [H2] re-running DP at d={d} T={T} to confirm cached counts ...", flush=True)
        s2, diff2, q2 = exact_confirm(A_REC, d, T)
        assert (s2, diff2, q2) == (s, diff, q), "cached counts disagree with DP recompute!"
        print("  [H2] DP recompute matches cached counts", flush=True)
    theta_lb, beats = certify_theta_lb_scaled(s, diff, q, terms=terms)
    return theta_lb, beats


if __name__ == "__main__":
    sanity_record()
    _check_certify_on_record()
    print()
    verify = os.environ.get("VERIFY_DP") == "1"  # set VERIFY_DP=1 to re-run the slow DP
    # Best certified winner: d=84, T=162.
    best = max(WINNERS, key=lambda dt: WINNERS[dt]["float_theta"])
    for (d, T) in sorted(WINNERS):
        theta_lb, beats = certify_winner(d, T, verify_dp=verify)
        tag = "  <== BEST" if (d, T) == best else ""
        print(f"WINNER A={A_REC} d={d} T={T}  certified theta_lb={float(theta_lb):.16f} "
              f"beats={beats}  margin={float(theta_lb - RECORD_FRAC):.3e}{tag}", flush=True)
    bd, bT = best
    btheta, _ = certify_winner(bd, bT)
    print(f"\nCERTIFIED LOWER BOUND on C_3a: {float(btheta):.13f}  "
          f"(d={bd}, T={bT}, A={A_REC}, base=21) > record 1.1740744 [G2026].", flush=True)
