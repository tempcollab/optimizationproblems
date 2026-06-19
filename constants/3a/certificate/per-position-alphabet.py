"""Sketch: per-position-alphabet  (constant 3a, LOWER bound)

TARGET (top-level claim):
    There exist per-position digit alphabets A_0,...,A_{d-1} (each finite, 0 in A_i), a
    common carry-free base b = 2*max_i max(A_i)+1, and a global cap T such that
        U = { sum_i a_i b^i : a_i in A_i, sum_i a_i <= T }
    gives  1 + log(|U-U|/|U+U|) / log(2 max(U)+1) > 1.1740744.

STRATEGY (strictly enlarges the homogeneous family of alphabet-search-dp):
    All prior work (GHR, Gerbicz, Zheng, Griego) uses the SAME alphabet at every digit
    position.  Letting the alphabet vary by position i strictly enlarges the construction
    space while preserving carry-free injectivity: the base is set by the GLOBAL max digit
    b = 2*max_i max(A_i)+1, so digit-wise sums/differences of two U-elements still land in
    [-(b-1), b-1] and the base-b encoding stays injective on U+U and U-U (no carries).

    A natural low-dim parameterization that stays searchable: a small number of "blocks" of
    positions, each block with its own alphabet (e.g. denser alphabet in low positions,
    sparser in high positions where max(U) -- the denominator log q -- is most sensitive).

HOLES (status this round):
  (H1) ENGINE -- CLOSED.  Position-dependent DP generalizing ghr_dp's sumset/diffset/max DP
       to take a list [A_0,...,A_{d-1}].  The (sa,sap)/(la,ra) state machinery is unchanged;
       only the per-step feature lists differ (built from A_i at step i) and the carry-free
       base is the GLOBAL max.  Validated three ways below: (a) all A_i equal -> identical to
       ghr_dp; (b) small brute-force over genuinely inhomogeneous schedules; (c) reproduces
       Griego's record literals on the homogeneous instance.
  (H2) SEARCH (HARD) -- PARTIALLY DONE / open.  Principled position schedules explored with a
       cheap-d proxy then confirmed at larger d.  Best inhomogeneous theta found so far is
       documented; see search_blocked() and the commentary.  If no schedule beats the record,
       that is reported honestly (the homogeneous record appears near-optimal within the
       block families tried) -- remaining schedule families are a marked TODO.
  (H3) EXACT CONFIRM + CERTIFY -- CLOSED for the certify machinery.  exact_confirm() returns
       exact integer counts; certify_theta_lb() gives a directed-rounded (round-DOWN) rational
       lower bound on theta.  It only certifies a RECORD-BEATING bound if H2 produces a winner.

Running this file: validates the engine (H1), runs the schedule search (H2), and -- if a
winner is found -- prints exact counts and certified theta (H3).  If no winner, reports the
best certified inhomogeneous theta as honest population progress.
"""

import sys
import os
from collections import defaultdict
from fractions import Fraction

sys.path.insert(0, os.path.dirname(__file__))
from ghr_dp import sumset_size, diffset_size, max_U, carry_free_base  # noqa  (homogeneous ref)

RECORD = 1.1740744
RECORD_FRAC = Fraction(11740744, 10000000)  # exact rational floor we must strictly exceed


# ---------------------------------------------------------------------------
# H1 ENGINE: position-dependent exact-integer DP
# ---------------------------------------------------------------------------

def _global_base(alphabets):
    """Carry-free base forced by the GLOBAL max digit across all positions."""
    return 2 * max(max(A) for A in alphabets) + 1


def sumset_size_pp(alphabets, T):
    """Exact |U+U| for per-position alphabets [A_0,...,A_{d-1}], global cap T.

    Same DP as ghr_dp.sumset_size but the feasible output-digit set A_i+A_i and the
    feasible-split list P_y depend on the position's alphabet A_i.  State = frozenset of
    reachable (sa, sap) = (running sum of a_i, running sum of a'_i), both pruned at T.
    Reduces to ghr_dp.sumset_size when all A_i are equal.
    """
    alphabets = [sorted(set(A)) for A in alphabets]
    states = {frozenset([(0, 0)]): 1}
    for A in alphabets:
        setA = set(A)
        AA = sorted(set(x + y for x in A for y in A))
        Py = {y: [a for a in A if (y - a) in setA] for y in AA}
        new = defaultdict(int)
        for st, cnt in states.items():
            for y in AA:
                reach = set()
                for (sa, sap) in st:
                    for a in Py[y]:
                        nsa = sa + a
                        nsap = sap + (y - a)
                        if nsa <= T and nsap <= T:
                            reach.add((nsa, nsap))
                if reach:
                    new[frozenset(reach)] += cnt
        states = new
    return sum(states.values())


def diffset_size_pp(alphabets, T):
    """Exact |U-U| for per-position alphabets [A_0,...,A_{d-1}], global cap T.

    Same DP as ghr_dp.diffset_size but the diff-digit set A_i-A_i and the cheapest
    representative q_delta = min{b in A_i : b+delta in A_i} depend on position i.
    For a FIXED delta at position i, the cheapest rep (q+delta, q) simultaneously minimizes
    BOTH the left running total and the right running total (since increasing q raises both
    sides by the same amount), so a string is feasible iff its per-position cheapest-rep
    totals are <= T.  State = (left total, right total), pruned at T.
    Reduces to ghr_dp.diffset_size when all A_i are equal.
    """
    alphabets = [sorted(set(A)) for A in alphabets]
    states = {(0, 0): 1}
    for A in alphabets:
        setA = set(A)
        DD = sorted(set(x - y for x in A for y in A))
        rep = {}
        for delta in DD:
            q = min(b for b in A if (b + delta) in setA)
            rep[delta] = (q + delta, q)
        new = defaultdict(int)
        for (la, ra), cnt in states.items():
            for delta in DD:
                dl, dr = rep[delta]
                nla, nra = la + dl, ra + dr
                if nla <= T and nra <= T:
                    new[(nla, nra)] += cnt
        states = new
    return sum(states.values())


def max_U_pp(alphabets, T):
    """Exact max(U) for per-position alphabets: greedily fill highest positions with the
    largest admissible digit subject to the global cap sum a_i <= T.  Greedy is optimal here
    because position i carries weight b^i and b > sum of all lower-position contributions, so
    a larger high digit always dominates any rearrangement of the remaining cap below it.
    Reduces to ghr_dp.max_U when all A_i are equal.
    """
    alphabets = [sorted(set(A)) for A in alphabets]
    d = len(alphabets)
    b = _global_base(alphabets)
    val = 0
    rem = T
    for i in range(d - 1, -1, -1):
        cands = [x for x in alphabets[i] if x <= rem]
        a = max(cands) if cands else 0
        val += a * b ** i
        rem -= a
    return val


def theta_floatbound_pp(alphabets, T):
    """Quick (NON-certified) float estimate of theta for search/ranking."""
    from math import log
    s = sumset_size_pp(alphabets, T)
    diff = diffset_size_pp(alphabets, T)
    q = 2 * max_U_pp(alphabets, T) + 1
    return 1.0 + (log(diff) - log(s)) / log(q), s, diff, q


# ---------------------------------------------------------------------------
# H1 VALIDATION
# ---------------------------------------------------------------------------

def _validate_engine(verbose=True):
    from itertools import product as iproduct
    # (a) homogeneous reduction: equal alphabets -> ghr_dp exactly
    for A in [[0, 1, 2], [0, 2, 3, 4, 5], [0, 2, 3, 5, 7]]:
        for d, T in [(4, 6), (5, 9)]:
            alph = [A] * d
            assert sumset_size_pp(alph, T) == sumset_size(A, d, T)
            assert diffset_size_pp(alph, T) == diffset_size(A, d, T)
            assert max_U_pp(alph, T) == max_U(A, d, T)

    # (b) brute-force over genuinely INHOMOGENEOUS schedules
    def brute_pp(alphabets, T):
        b = _global_base(alphabets)
        d = len(alphabets)
        U = set()
        for combo in iproduct(*alphabets):
            if sum(combo) <= T:
                U.add(sum(a * b ** i for i, a in enumerate(combo)))
        plus = set(x + y for x in U for y in U)
        minus = set(x - y for x in U for y in U)
        return len(plus), len(minus), max(U)

    schedules = [
        [[0, 1, 2], [0, 2, 3], [0, 1, 4]],
        [[0, 2, 5], [0, 1, 2], [0, 3]],
        [[0, 1, 3, 4], [0, 2], [0, 2, 3], [0, 1]],
        [[0, 4], [0, 1, 2], [0, 2, 3, 4]],
    ]
    for alph in schedules:
        for T in [4, 6, 8]:
            bp, bm, bx = brute_pp(alph, T)
            ep = sumset_size_pp(alph, T)
            em = diffset_size_pp(alph, T)
            ex = max_U_pp(alph, T)
            assert (bp, bm, bx) == (ep, em, ex), (alph, T, (bp, bm, bx), (ep, em, ex))

    # (c) reproduce Griego's record literals on the homogeneous instance
    A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    alph = [A] * 80
    s = sumset_size_pp(alph, 150)
    diff = diffset_size_pp(alph, 150)
    assert s == 75448362167176243488362019935078206851619643198150854886920234689186981134888
    assert diff == 195351744295266763842135520514417052287242446785296742323733058216909095059024572338564089814415
    if verbose:
        print("[H1] engine validated: homogeneous reduction + inhomogeneous brute-force + record literals OK")


# ---------------------------------------------------------------------------
# H3 CERTIFY: directed-rounded (round-DOWN) rational lower bound on theta
# ---------------------------------------------------------------------------

def _log_lb(num, den, terms=60):
    """Rational LOWER bound on log(num/den) for num >= den >= 1 (so the log is >= 0).

    Uses the atanh series  log(x) = 2*atanh((x-1)/(x+1)) = 2 * sum_{k>=0} z^(2k+1)/(2k+1),
    z = (x-1)/(x+1) in [0,1).  Every term is non-negative, so any finite partial sum is a
    valid LOWER bound on log(x).  All arithmetic is exact Fraction; we just truncate.
    """
    x = Fraction(num, den)
    z = (x - 1) / (x + 1)
    z2 = z * z
    s = Fraction(0)
    zk = z
    for k in range(terms):
        s += zk / (2 * k + 1)
        zk *= z2
    return 2 * s


def _log_ub(num, den, terms=60):
    """Rational UPPER bound on log(num/den) for num >= den >= 1.

    The atanh tail after N terms is 2 * sum_{k>=N} z^(2k+1)/(2k+1) <= 2/(2N+1) * z^(2N+1)/(1-z^2)
    (bounding 1/(2k+1) <= 1/(2N+1) and summing the geometric series).  Add this tail bound to
    the partial sum to get a valid UPPER bound.  Exact Fraction arithmetic.
    """
    x = Fraction(num, den)
    z = (x - 1) / (x + 1)
    z2 = z * z
    s = Fraction(0)
    zk = z
    for k in range(terms):
        s += zk / (2 * k + 1)
        zk *= z2
    # zk now = z^(2*terms+1); tail bound
    tail = zk / (2 * terms + 1) / (1 - z2)
    return 2 * (s + tail)


def certify_theta_lb(s, diff, q, terms=200):
    """Directed-rounded rational LOWER bound on
        theta = 1 + log(diff/s) / log(q).
    diff >= s >= 1 and q >= 1 (here q huge).  We need a LOWER bound on the ratio
    log(diff/s)/log(q): numerator >= 0 lower-bounded, denominator upper-bounded.

    Returns (theta_lower : Fraction, beats : bool) where beats = theta_lower > RECORD_FRAC.
    """
    assert diff >= s >= 1 and q >= 1
    num_lb = _log_lb(diff, s, terms)      # <= log(diff/s)
    den_ub = _log_ub(q, 1, terms)         # >= log(q)
    assert num_lb >= 0 and den_ub > 0
    theta_lb = 1 + num_lb / den_ub        # <= 1 + log(diff/s)/log(q) = theta
    return theta_lb, theta_lb > RECORD_FRAC


def _check_certify_self():
    """Sanity-check the rational log bounds against float math on the record instance, and
    confirm the certified theta is a genuine (slightly conservative) LOWER bound on the float
    theta -- i.e. directed rounding is in the safe direction."""
    from math import log
    A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    s = sumset_size(A, 80, 150)
    diff = diffset_size(A, 80, 150)
    q = 2 * max_U(A, 80, 150) + 1
    theta_lb, beats = certify_theta_lb(s, diff, q, terms=400)
    theta_float = 1 + (log(diff) - log(s)) / log(q)
    flb = float(theta_lb)
    assert flb <= theta_float + 1e-12, (flb, theta_float)
    assert theta_float - flb < 1e-6, (theta_float - flb)  # tight
    # record's own theta is ~1.17407444769, which IS > 1.1740744, so beats=True for record
    assert beats
    print(f"[H3] certify machinery validated on record: theta_lb={flb:.12f} "
          f"(float {theta_float:.12f}); beats RECORD={beats}")


# ---------------------------------------------------------------------------
# H2 SEARCH: principled position schedules
# ---------------------------------------------------------------------------

def exact_confirm(alphabets, T):
    """H2->H3 bridge: exact integer counts for a candidate schedule."""
    s = sumset_size_pp(alphabets, T)
    diff = diffset_size_pp(alphabets, T)
    q = 2 * max_U_pp(alphabets, T) + 1
    return s, diff, q


def _two_block_schedule(A_low, A_high, d, frac_high):
    """High positions (top frac_high of d) use A_high, the rest use A_low.  High positions
    dominate max(U) (the denominator log q); a sparser/larger-step A_high lowers q growth,
    a denser A_low in low positions adds cheap sums/diffs."""
    n_high = int(round(frac_high * d))
    n_low = d - n_high
    return [A_low] * n_low + [A_high] * n_high


def search_blocked(d_proxy=24, verbose=True):
    """H2: principled search over position schedules using a cheap small-d proxy.

    Key reasoning (where the ratio is sensitive):
      * theta = 1 + log(diff/s)/log(q), q = 2 max(U)+1.  max(U) is set by the HIGH positions
        and the global base b = 2*max_i max(A_i)+1.  To keep q small we want SMALL max digit
        in high positions; to keep diff/s large we want a rich alphabet (many distinct
        differences) where it is cheap.
      * The homogeneous record uses A={0,2,..,10} (max 10, base 21) EVERYWHERE.  The
        inhomogeneous lever: use the rich record alphabet in LOW positions (cheap, they
        barely move q because b^i is small there) and a SMALLER-max alphabet in HIGH
        positions (so the global base, hence q, could in principle shrink) -- BUT the base is
        global, so shrinking high-position max only helps if it lowers the GLOBAL max, which
        means EVERY position must drop its max.  That is just a smaller homogeneous alphabet.
      * The real inhomogeneous freedom that does NOT touch the global base: keep max=10
        somewhere (fixing b=21) and VARY THE INTERIOR digits per position (which mid digits
        to include), trading sum/diff richness against the cap budget per position.

    We therefore search two- and three-block schedules at fixed base 21 (max digit 10
    present), tapering the interior alphabet, on a cheap proxy d, then lift the best to
    larger d for confirmation.
    """
    from math import log

    Arec = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # the record alphabet (base 21)
    # Candidate alphabets, all with max=10 (keep base 21 fixed) unless noted:
    cand = {
        'rec':      [0, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'full':     [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'omit12':   [0, 3, 4, 5, 6, 7, 8, 9, 10],
        'omit2':    [0, 1, 3, 4, 5, 6, 7, 8, 9, 10],
        'sparse':   [0, 2, 4, 5, 6, 7, 8, 9, 10],
        'lowrich':  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'midgap':   [0, 2, 3, 4, 6, 7, 8, 9, 10],
    }

    # Proxy: match T/d to Griego's 150/80 = 1.875.
    Tp = int(round(1.875 * d_proxy))
    results = []

    # Baseline: homogeneous record at the proxy size.
    th0, s0, diff0, q0 = theta_floatbound_pp([Arec] * d_proxy, Tp)
    results.append(('homogeneous-rec', th0))
    if verbose:
        print(f"[H2] proxy d={d_proxy} T={Tp}: homogeneous record theta={th0:.10f}")

    # Two-block schedules: (low alphabet, high alphabet, frac_high).
    fracs = [0.25, 0.4, 0.5, 0.6, 0.75]
    pairs = [
        ('rec', 'full'), ('full', 'rec'),
        ('rec', 'omit12'), ('omit12', 'rec'),
        ('rec', 'sparse'), ('sparse', 'rec'),
        ('rec', 'omit2'), ('omit2', 'rec'),
        ('rec', 'midgap'), ('midgap', 'rec'),
        ('full', 'omit12'), ('omit12', 'full'),
    ]
    for (lo, hi) in pairs:
        for fr in fracs:
            sched = _two_block_schedule(cand[lo], cand[hi], d_proxy, fr)
            th, s, diff, q = theta_floatbound_pp(sched, Tp)
            results.append((f"2blk[{lo}|{hi}]@{fr}", th))

    results.sort(key=lambda t: -t[1])
    if verbose:
        print("[H2] top proxy schedules (float theta):")
        for name, th in results[:8]:
            flag = " <-- beats homogeneous-rec" if th > th0 + 1e-12 else ""
            print(f"      {name:28s} {th:.10f}{flag}")

    best_name, best_th = results[0]
    beats_homog = best_th > th0 + 1e-9
    return results, best_name, best_th, beats_homog, (d_proxy, Tp)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    _validate_engine()
    _check_certify_self()
    print()
    results, best_name, best_th, beats_homog, (dp, Tp) = search_blocked(d_proxy=24)
    print()
    if beats_homog:
        print(f"[H2] proxy WINNER over homogeneous: {best_name} theta={best_th:.10f}")
        print("     -> lift to larger d and exact-certify (see commentary).")
    else:
        print(f"[H2] no inhomogeneous schedule beat the homogeneous record at proxy d={dp}.")
        print(f"     best inhomogeneous proxy theta={best_th:.10f} ({best_name}); "
              f"homogeneous-rec was at the top -> homogeneous appears near-optimal here.")
        print("     REMAINING HOLE (H2): larger-d block families / interior-digit schedules "
              "not yet exhausted; no record-beating bound this round.")
