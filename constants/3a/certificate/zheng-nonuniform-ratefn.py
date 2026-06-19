"""Sketch: zheng-nonuniform-ratefn  (constant 3a, LOWER bound -- THEORY/GUIDE line)

TARGET (top-level claim):
    Extend Zheng's Cramer large-deviation asymptotic from the UNIFORM digit alphabet
    {0..B} to a GENERAL digit weight distribution p on a finite alphabet A, yielding a
    closed-form limiting exponent  theta_inf(A, p, c)  as #digits -> infinity with cap
    T = c*d.  Maximize over (A, p, c) to predict the optimal alphabet shape, then realize
    the predicted optimum as a FINITE construction whose exact-DP-certified theta beats
    1.1740744.

WHY THIS EXISTS:
    Zheng's framework ASSUMES the full uniform interval {0..B} (mean B/2, uniform mgf), so
    his formula does NOT cover Griego's non-uniform set ({0..10} minus {1}).  Nobody has written
    the limiting theta for a general digit distribution.  Doing so (a) tells us WHICH
    alphabet shape maximizes the exponent -- guiding/replacing the brute search of
    alphabet-search-dp -- and (b) upper-bounds what any finite construction in this family
    can reach.  This is the principled version of explorer levers #2 and #3.

THE ENGINE (to derive in H1): With each digit drawn iid from distribution p on A and cap
    sum a_i <= c*d, Cramer gives
        lim (1/d) log |U|        = H(p) - I_p(c)            (constrained entropy),
    where I_p(c) = sup_t ( t c - log E_p[e^{t a}] ) is the Legendre transform (rate fn) of p.
    Analogous limits for log|U+U| (distribution of a+a', i.e. p*p convolution under joint cap)
    and log|U-U| (distribution of a-a').  Denominator log q -> log(b) * d with b=2max(A)+1.
    Assemble theta_inf as a ratio of these exponents.  (Zheng eq. for uniform p is the
    special case -- USE IT AS THE VALIDATION TARGET: plugging uniform p must reproduce his
    table, e.g. B=5 -> theta-1 = 0.1730773.)

HOLES:
  (H1) RATE FUNCTION: implement I_p(c) and the joint-cap convolution exponents for sumset and
       diffset under a general p on A. Validate against Zheng's uniform table.
  (H2) OPTIMIZE: maximize theta_inf over (A, p, c). HARD STEP -- the variational problem
       (Legendre transform of the chosen digit mgf, jointly over alphabet support and
       weights). Expected to point near / beyond Griego's shape.
  (H3) REALIZE + CERTIFY: convert the optimal (A, p, c) into a finite (A, d, T) -- p encoded
       via digit MULTIPLICITY or per-position frequency -- and exact-DP-certify (ghr_dp /
       alphabet-search-dp machinery) that the finite theta strictly beats 1.1740744. Tying
       the asymptotic optimum to a VALID finite construction is the second hard step.

Running this file now: STOPS at the rate-function hole.
"""

RECORD = 1.1740744
ZHENG_UNIFORM_B5 = 1.1730773  # validation target for H1 (uniform p on {0..5})


def rate_function(p, c):
    """HOLE H1: I_p(c) = sup_t (t c - log E_p[e^{t a}]) for distribution p (dict a->prob)."""
    raise NotImplementedError("H1: general-alphabet rate function not implemented")


def theta_inf(A, p, c):
    """HOLE H1: limiting exponent for general digit distribution p on alphabet A, cap ratio c.
    Must reproduce Zheng's table when p is uniform on {0..B}."""
    raise NotImplementedError("H1: non-uniform asymptotic exponent not implemented")


def optimize_shape():
    """HOLE H2: maximize theta_inf over (A, p, c). Returns the predicted optimal shape."""
    raise NotImplementedError("H2: variational optimization not implemented")


def realize_finite(A, p, c):
    """HOLE H3: build a finite (A_finite, d, T) realizing the optimal shape and exact-DP
    certify theta > RECORD."""
    raise NotImplementedError("H3: finite realization + certificate not implemented")


if __name__ == "__main__":
    try:
        A, p, c = optimize_shape()
        print("predicted optimal shape:", A, p, c)
    except NotImplementedError as e:
        print(f"[hole] {e}")
