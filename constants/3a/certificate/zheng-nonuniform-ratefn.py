"""Sketch: zheng-nonuniform-ratefn  (constant 3a, LOWER bound -- THEORY/GUIDE line)

TARGET (top-level claim):
    Extend Zheng's Cramer large-deviation asymptotic from the UNIFORM digit alphabet
    {0..B} to a GENERAL digit weight distribution p on a finite alphabet A, yielding a
    closed-form limiting exponent  theta_inf(A, p, c)  as #digits -> infinity with cap
    T = c*d.  Maximize over (A, p, c) to predict the optimal alphabet shape, then realize
    the predicted optimum as a FINITE construction whose exact-DP-certified theta beats
    the HELD bound 1.1744750903655619.

WHY THIS EXISTS (highest NEW leverage, explorer lever B):
    Zheng's framework ASSUMES the full uniform interval {0..B} (mean B/2, uniform mgf), so
    his formula does NOT cover Griego's non-uniform set ({0..10} minus {1}).  Nobody has
    written the limiting theta for a general digit distribution.  Doing so (a) tells us
    WHICH alphabet shape + cap ratio c maximizes the exponent -- guiding/replacing the brute
    search of alphabet-search-dp and telling us how much of the 1.17448->1.25 corridor this
    single-set family can even reach -- and (b) any (A,p,c) it points to is realized FINITELY
    and exact-DP-certified, feeding the leader.

REVISED THIS ROUND (round 3): H1 is now a CONCRETE RUNNABLE skeleton, not a bare raise.
    The rate function I_p(c) (Legendre transform via scipy) and the constrained-entropy
    assembly are implemented; the builder's H1 job is to (i) get the sumset/diffset joint-cap
    exponents right and (ii) VALIDATE against Zheng's uniform table (the anchor below).
    H2 (variational optimization over A,p,c) and H3 (finite realization + exact certificate)
    remain the two hard holes.

THE ENGINE (H1 -- skeleton implemented below, joint-cap exponents are the open piece):
    With each digit drawn iid from distribution p on A and cap sum a_i <= c*d, Cramer gives
        lim (1/d) log |U|        = H(p) - I_p(c)            (constrained entropy / count),
    where I_p(c) = sup_t ( t c - log E_p[e^{t a}] ) is the Legendre transform (rate fn) of p
    and H(p) is the Shannon entropy (the unconstrained log-count rate).  The cap is binding
    only when c < mean(p); for c >= mean the constraint is slack and the rate is H(p).
    Analogous limits for log|U+U| (digit distribution of a+a', i.e. p*p convolution, under the
    joint cap that BOTH digit-sums <= c*d) and log|U-U| (a-a').  Denominator log q -> d*log(b)
    with b = 2*max(A)+1.  Assemble theta_inf = 1 + (rate|U-U| - rate|U+U|) / log(b).

VALIDATION ANCHOR (the correctness gate H1 must pass before H2/H3 are trusted):
    plugging the UNIFORM p on {0..B} must reproduce Zheng's table: B=5 -> theta-1 = 0.1730773
    (Z2025).  ZHENG_UNIFORM_B5 below is that target; validate_uniform() is the harness.

Running this file now: runs the uniform-rate-function self-checks (I_p(mean)=0; the single-set
count exponent), then STOPS at the joint-cap sumset/diffset hole with a clear [hole] message.
"""

import numpy as np

try:
    from scipy.optimize import minimize_scalar
except Exception:  # pragma: no cover - scipy expected present per CLAUDE.md toolchain
    minimize_scalar = None

RECORD = 1.1740744
HELD = 1.1744750903655619          # value to beat (R2 verified)
ZHENG_UNIFORM_B5 = 0.1730773       # theta-1 target for uniform p on {0..5} (Z2025)


# ---------------------------------------------------------------------------
# H1 (skeleton implemented): single-digit rate function and constrained count rate
# ---------------------------------------------------------------------------

def _as_dist(p):
    """Normalize p (dict a->weight, a in A) into (support array, prob array)."""
    A = np.array(sorted(p), dtype=float)
    w = np.array([p[a] for a in sorted(p)], dtype=float)
    return A, w / w.sum()


def logmgf(p, t):
    """log E_p[e^{t a}] for distribution p on alphabet A (numerically stable)."""
    A, w = _as_dist(p)
    m = (t * A).max()
    return m + np.log(np.sum(w * np.exp(t * A - m)))


def rate_function(p, c):
    """I_p(c) = sup_t ( t c - log E_p[e^{t a}] ), the Cramer rate function of p at level c.
    Implemented via 1-D Legendre transform (scipy bounded maximization).  I_p(mean(p)) = 0;
    I_p is convex and >= 0.  Used for the cap-binding correction to the count rate."""
    if minimize_scalar is None:
        raise NotImplementedError("H1: scipy required for the Legendre transform")
    A, w = _as_dist(p)
    mean = float((A * w).sum())
    if abs(c - mean) < 1e-12:
        return 0.0
    f = lambda t: -(t * c - logmgf(p, t))
    r = minimize_scalar(f, bounds=(-200.0, 200.0), method="bounded",
                        options={"xatol": 1e-10})
    return max(0.0, -r.fun)


def shannon_entropy(p):
    """H(p) = -sum p log p (nats) -- the unconstrained per-digit log-count rate."""
    _, w = _as_dist(p)
    w = w[w > 0]
    return float(-(w * np.log(w)).sum())


def count_rate(p, c):
    """lim (1/d) log |U| for iid digits ~ p under cap (sum a_i)/d <= c.
    Cramer constrained-entropy: H(p) if the cap is slack (c >= mean), else H(p) - I_p(c)
    measured at the binding tilt.  (Standard tilted-measure argument: the constrained log-count
    rate equals the entropy of the tilted distribution that puts mean exactly at c.)"""
    A, w = _as_dist(p)
    mean = float((A * w).sum())
    if c >= mean:
        return shannon_entropy(p)
    return shannon_entropy(p) - rate_function(p, c)


# ---------------------------------------------------------------------------
# H1 (OPEN): joint-cap sumset / diffset exponents
# ---------------------------------------------------------------------------

def sumset_rate(p, c):
    """HOLE H1 (open): lim (1/d) log |U+U| for iid digits ~ p, cap c on BOTH summands.
    The y-digit is a+a' (support A+A, distribution p*p convolution); the count is over
    distinct feasible y-strings with a JOINT cap (both sum a_i and sum a'_i <= c*d).  The
    exponent is NOT simply count_rate(p*p, ...) because the two caps couple -- needs the
    2-D rate function I_{p,p}(c,c) of the pair (a, a') restricted to the y-marginal.  Derive
    the 2-D Legendre transform and reduce to the y-marginal count rate."""
    raise NotImplementedError("H1: joint-cap sumset exponent not implemented")


def diffset_rate(p, c):
    """HOLE H1 (open): lim (1/d) log |U-U| for iid digits ~ p, cap c on both terms.
    delta-digit is a-a' (support A-A); same joint-cap 2-D rate-function reduction as sumset,
    on the delta-marginal.  This is the dominant numerator term -- Zheng's own lever (2) notes
    his d(U) lower bound uses a CRUDE single-k term, so the tight delta-marginal count here may
    itself exceed his asymptotic (a possible standalone lift)."""
    raise NotImplementedError("H1: joint-cap diffset exponent not implemented")


def theta_inf(A_support, p, c):
    """HOLE H1 (assembly, open until sumset/diffset rates land): limiting theta for general p.
        theta_inf = 1 + (diffset_rate(p,c) - sumset_rate(p,c)) / log(2*max(A)+1).
    Must reproduce Zheng's uniform table (validate_uniform)."""
    b = 2 * max(A_support) + 1
    return 1.0 + (diffset_rate(p, c) - sumset_rate(p, c)) / np.log(b)


# ---------------------------------------------------------------------------
# H2 / H3 (hard holes, unchanged)
# ---------------------------------------------------------------------------

def optimize_shape():
    """HOLE H2 (hard): maximize theta_inf over (A, p, c) -- variational problem over alphabet
    support and weights.  Expected to point near / beyond Griego's {0,2..10} shape and to give
    the asymptotic ceiling of the single-set family.  Gated on H1 (the joint-cap rates)."""
    raise NotImplementedError("H2: variational optimization not implemented")


def realize_finite(A, p, c):
    """HOLE H3 (hard): convert the optimal (A,p,c) into a finite (A_finite, d, T) -- p encoded
    via digit MULTIPLICITY or per-position frequency -- and exact-DP-certify (ghr_dp /
    alphabet-search-dp machinery + lemmas/log_bounds.py) that the finite theta strictly beats
    HELD = 1.1744750903655619.  Tying the asymptotic optimum to a VALID finite construction is
    the second hard step; the asymptotic alone is NOT a bound."""
    raise NotImplementedError("H3: finite realization + certificate not implemented")


# ---------------------------------------------------------------------------
# H1 validation harness (the correctness gate)
# ---------------------------------------------------------------------------

def validate_uniform(B=5, tol=1e-3):
    """The H1 correctness gate: uniform p on {0..B} must reproduce Zheng's table.
    Currently exercises the single-digit pieces (rate_function, count_rate); the full
    theta check is gated on the open sumset/diffset rates."""
    p = {a: 1.0 for a in range(B + 1)}
    A, w = _as_dist(p)
    mean = float((A * w).sum())
    assert abs(rate_function(p, mean)) < 1e-6, "I_p(mean) must be 0"
    assert count_rate(p, mean + 1.0) == shannon_entropy(p), "slack cap -> entropy"
    print(f"[H1] single-digit rate pieces OK: mean={mean}, H(p)={shannon_entropy(p):.6f}",
          flush=True)
    try:
        tm1 = theta_inf(list(range(B + 1)), p, c=mean) - 1.0
        ok = abs(tm1 - ZHENG_UNIFORM_B5) < tol
        print(f"[H1] uniform theta-1={tm1:.7f} vs Zheng {ZHENG_UNIFORM_B5} -> {'OK' if ok else 'MISMATCH'}",
              flush=True)
        return ok
    except NotImplementedError as e:
        print(f"[hole] {e}", flush=True)
        return None


if __name__ == "__main__":
    validate_uniform()
    try:
        A, p, c = optimize_shape()
        print("predicted optimal shape:", A, p, c)
    except NotImplementedError as e:
        print(f"[hole] {e}", flush=True)
