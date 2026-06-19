"""Shared goal-cache lemma (constant 3a) — directed-rounded rational bounds on log(N).

REVIEWER-CERTIFIED (round 2). Any 3a sketch may import these instead of re-deriving the
log-bound primitive. This is the correct replacement for the broken shared
`per-position-alphabet.certify_theta_lb` (which fed the atanh series the full q ~ b^d and
diff/s, where z=(x-1)/(x+1) ~ 1, so the series could not converge and theta_lb collapsed
to ~1.0).

CERTIFICATION (what the reviewer established, R2):
  * atanh identity: log(x) = 2*atanh(z) = 2*sum_{k>=0} z^(2k+1)/(2k+1), z=(x-1)/(x+1),
    convergent for x>0 (z in (-1,1)). For x>=1 every term is >= 0.
  * LOWER bound: any finite partial sum of nonnegative terms is <= log(x).  (_log_small_lb)
  * UPPER bound: tail after N terms = 2*sum_{k>=N} z^(2k+1)/(2k+1)
       <= (2/(2N+1)) * sum_{k>=N} z^(2k+1) = (2/(2N+1)) * z^(2N+1)/(1-z^2),
    so partial + this tail >= log(x).  (_log_small_ub)
  * Scaled reduction: log N = k*log2 + log(N/2^k) with 2^k <= N < 2^(k+1), N/2^k in [1,2),
    so the atanh argument has z <= 1/3 and converges in a few hundred terms. log2 is bounded
    once at z=1/3. logN_lb under-estimates both pieces, logN_ub over-estimates both.
  * Verified: brackets true log(N) (logN_lb(N) <= log N <= logN_ub(N)) across random N up to
    ~300 bits and at the winner scale q ~ 1e105 (checked vs mpmath @150-200 dps).

This file is verbatim the certify primitives from `certificate/alphabet-search-dp.py`
(functions `_log_small_lb/_ub`, `_floor_log2`, `logN_lb`, `logN_ub`, `certify_theta_lb`),
which produced the verified R2 record C_3a >= 1.1744750903655619.
"""

from fractions import Fraction


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


def certify_theta_lb(s, diff, q, terms=300):
    """Directed-rounded rational LOWER bound on
        theta = 1 + log(diff/s) / log(q),   diff >= s >= 1, q >= 2.
    Lower-bound the numerator (log diff lower, log s upper) and UPPER-bound the
    denominator log q, so the quotient -- hence theta -- is under-estimated.
    Returns the Fraction theta_lb (<= true theta).
    """
    assert diff >= s >= 1 and q >= 2
    num_lb = logN_lb(diff, terms) - logN_ub(s, terms)   # <= log(diff/s)
    den_ub = logN_ub(q, terms)                          # >= log q
    assert num_lb >= 0 and den_ub > 0
    return 1 + num_lb / den_ub                          # <= theta
