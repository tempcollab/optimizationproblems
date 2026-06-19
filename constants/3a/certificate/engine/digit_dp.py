"""
Exact carry-free digit-DP count engine for the GHR / C_3a digit-set construction.

Constant C_3a (Gyarmati-Hennecart-Ruzsa). GHR2007 lemma: for any finite U subset of Z>=0
with 0 in U,
    C_3a >= 1 + log(|U-U| / |U+U|) / log(2*max(U)+1).

The record construction is the base-B digit set
    U(A,B,d,T) = { sum_{i=0}^{d-1} a_i * B^i : a_i in A, sum a_i <= T }.

When B > 2*max(A) the addition/subtraction of two U-elements is CARRY-FREE, so:
  * each u in U has a UNIQUE base-B digit vector (a_0..a_{d-1}), a_i in A;
  * u+v has digit vector (a_i+b_i) over the per-digit alphabet A+A (each entry < B, no carry);
  * u-v has signed digit vector (a_i-b_i) over A-A (each |entry| < B, unique signed rep);
  * the ONLY coupling across positions is the global digit-sum cap sum a_i <= T (and likewise
    for the other addend); without the cap |U+-U| would factor as |A+-A|^d exactly.

Hence |U+U| = number of distinct ACHIEVABLE output digit vectors (c_i), where c_i is achievable
position-wise as a_i (op) b_i with a_i,b_i in A, AND there exists a GLOBAL split with
sum a_i <= T and sum b_i <= T simultaneously.  This is computed by an exact DP that, for each
output prefix, tracks the SET of feasible partial-sum pairs (s1, s2) = (sum used a_i, sum used b_i)
and counts distinct output vectors whose final feasible set is non-empty.

ALL load-bearing arithmetic is Python big-int / exact rational (fractions.Fraction).  NO floats
appear in the counts; floats are used only to print a human-readable approximation of the value.

This is the search-immune machinery baseline (analogous to the 9a 367-set Lean baseline);
reproducing the record is gap 0, NOT a beat.
"""

from fractions import Fraction
from collections import defaultdict


# ----------------------------------------------------------------------------
# Per-position output alphabet -> set of (a, b) decompositions
# ----------------------------------------------------------------------------

def _decompositions(A, op):
    """
    Return dict: output_digit -> sorted list of (a, b) with a,b in A and
    (a+b == output) if op == '+', or (a-b == output) if op == '-'.
    """
    decomp = defaultdict(set)
    for a in A:
        for b in A:
            c = a + b if op == '+' else a - b
            decomp[c].add((a, b))
    return {c: sorted(pairs) for c, pairs in decomp.items()}


# ----------------------------------------------------------------------------
# Core DP: count distinct achievable output digit-vectors under the digit-sum cap
# ----------------------------------------------------------------------------

def count_opset(A, d, T, op):
    """
    Exact count of |U op U| in the carry-free regime, where
        U = { sum a_i B^i : a_i in A, sum a_i <= T }  (i = 0..d-1).
    op is '+' (sumset) or '-' (difference set).  B does NOT enter the count (carry-free):
    the cardinality depends only on (A, d, T, op).  Caller must ensure B > 2*max(A).

    Returns an exact Python int.

    KEY SIMPLIFICATION (the load-bearing observation).  For a FIXED output digit-vector c with
    c_i = a_i (op) b_i and Sa = sum a_i, Sb = sum b_i, Sc = sum c_i:
        op = '+' :  a_i + b_i = c_i  for all i  =>  Sa + Sb = Sc, so Sb = Sc - Sa.
        op = '-' :  a_i - b_i = c_i  for all i  =>  Sa - Sb = Sc, so Sb = Sa - Sc.
    In BOTH cases Sb is an AFFINE function of (Sa, Sc).  Hence an output vector c is achievable
    (i.e. admits a split with Sa <= T AND Sb <= T) iff there is a reachable a-sum value Sa, over
    the per-position decompositions consistent with c, satisfying
        '+' :  Sa <= T  and  Sc - Sa <= T   (Sb = Sc - Sa)
        '-' :  Sa <= T  and  Sa - Sc <= T   (Sb = Sa - Sc)
    So we only need to track the SET of reachable a-sums Sa in {0..T} (we may cap at T: Sa > T is
    infeasible and a-sums only grow), together with the running output digit-sum Sc.  This collapses
    the 2-D (Sa, Sb) lattice to a 1-D reachable-Sa set keyed by Sc -- a small, fast signature.

    DP state = (frozenset of reachable Sa values in {0..T}, Sc).  dp maps state -> number of
    distinct output prefixes with that state.  At the end an output vector is achievable iff some
    reachable Sa meets the affine Sb<=T condition above.
    """
    assert 0 in A  # 0 in U requires 0 in A
    decomp = _decompositions(A, op)
    out_digits = sorted(decomp.keys())
    # For each output digit c, the distinct a-values usable (b = c-a or a-c is then forced and in A).
    a_options = {c: sorted({a for (a, b) in pairs}) for c, pairs in decomp.items()}

    if op == '-':
        return _count_minus(out_digits, a_options, d, T)
    return _count_plus(out_digits, a_options, d, T)


def _count_plus(out_digits, a_options, d, T):
    """
    Sumset count.  An output vector c (Sc = sum c_i) is achievable iff there is a reachable a-sum
    Sa <= T with Sb = Sc - Sa <= T, i.e. iff MAX reachable Sa >= Sc - T.  We need the exact set of
    reachable a-sums (boundary gaps are real, e.g. Sa = 1 is unreachable), tracked as a bitmask:
    bit j <=> a-sum j reachable.  State = (mask, Sc) -> #output prefixes.
    """
    TMASK = (1 << (T + 1)) - 1
    dp = {(1, 0): 1}
    for _pos in range(d):
        new_dp = defaultdict(int)
        for (mask, sc), cnt in dp.items():
            for c in out_digits:
                nm = 0
                for a in a_options[c]:
                    nm |= mask << a
                nm &= TMASK
                if nm:
                    new_dp[(nm, sc + c)] += cnt
        dp = dict(new_dp)
    total = 0
    for (mask, sc), cnt in dp.items():
        if (mask.bit_length() - 1) >= (sc - T):  # max reachable Sa >= Sc - T
            total += cnt
    return total


def _count_minus(out_digits, a_options, d, T):
    """
    Difference-set count.  An output vector c (Sc = sum c_i) is achievable iff there is a reachable
    a-sum Sa with Sa <= T and Sb = Sa - Sc <= T, i.e. Sa <= T + Sc.  Both are UPPER bounds on Sa,
    so the SMALLEST reachable Sa is optimal: achievable iff MIN reachable Sa <= T + Sc (and <= T,
    which is the kept range).  The minimum reachable a-sum for an output prefix is exactly the sum
    of the per-digit minimum a-options (the all-min-a path is a single consistent decomposition,
    and gives Sb = minSa - Sc >= 0 automatically).  So min reachable Sa transitions deterministically:
    minSa_new = minSa_old + min(a_options[c]); the digit is infeasible (dropped) iff minSa_new > T.
    Hence state collapses to (minSa, Sc) -- no mask needed -- which keeps the difference DP small.
    """
    min_a = {c: a_options[c][0] for c in out_digits}  # a_options sorted ascending
    dp = {(0, 0): 1}  # (minSa, Sc)
    for _pos in range(d):
        new_dp = defaultdict(int)
        for (msa, sc), cnt in dp.items():
            for c in out_digits:
                nmsa = msa + min_a[c]
                if nmsa <= T:
                    new_dp[(nmsa, sc + c)] += cnt
        dp = dict(new_dp)
    total = 0
    for (msa, sc), cnt in dp.items():
        if msa <= (T + sc):  # min reachable Sa <= T + Sc  (and msa <= T by construction)
            total += cnt
    return total


def max_U(A, B, d, T):
    """
    Exact max(U) = max over digit vectors (a_i in A, sum a_i <= T) of sum a_i B^i.

    Greedy from the TOP position down: at each position use the LARGEST alphabet digit a in A
    with a <= remaining digit-sum budget.  Optimal because B is large (carry-free regime,
    B > 2*max(A) >= max(A)+1), so a unit of digit-sum is worth strictly more at a higher
    position than any amount it could buy at lower positions: B^i > sum_{j<i} max(A)*B^j when
    B > max(A)+1.  Hence top-heavy placement with the largest AFFORDABLE alphabet digit is
    optimal.  (Bug guard: only digits actually in A are used -- e.g. for A={0,2,3,4,5} the
    digit 1 is NOT available, so leftover budget 1 contributes 0, not 1.)  Returns exact int.
    """
    Aset = sorted(A)
    budget = T
    val = 0
    for pos in range(d - 1, -1, -1):
        if budget <= 0:
            break
        # largest alphabet digit <= budget
        dig = 0
        for a in Aset:
            if a <= budget:
                dig = a
            else:
                break
        val += dig * (B ** pos)
        budget -= dig
    return val


def ghr_bound_value(A, B, d, T):
    """
    Compute the exact integer counts N_plus=|U+U|, N_minus=|U-U|, M=max(U), and the
    GHR lower-bound value  1 + log(N_minus/N_plus)/log(2M+1)  (returned as a float for display,
    plus the exact integer ingredients).  B must satisfy B > 2*max(A) (carry-free regime).
    """
    Amax = max(A)
    if B <= 2 * Amax:
        raise ValueError(f"B={B} not > 2*max(A)={2*Amax}: carry-free DP does not apply")
    N_plus = count_opset(A, d, T, '+')
    N_minus = count_opset(A, d, T, '-')
    M = max_U(A, B, d, T)
    return N_plus, N_minus, M


def value_float(N_plus, N_minus, M):
    """Human-readable float approximation of 1 + log(N-/N+)/log(2M+1). Display only."""
    import math
    return 1.0 + (math.log(N_minus) - math.log(N_plus)) / math.log(2 * M + 1)


def value_str(N_plus, N_minus, M, digits=40):
    """
    High-precision decimal of the value, computed via mpmath-free big-int log ratio using
    the Decimal module's ln at high precision (display only; the bound itself is certified by
    the exact rational-power inequality, not this float).
    """
    from decimal import Decimal, getcontext
    getcontext().prec = digits + 30
    v = Decimal(1) + (Decimal(N_minus).ln() - Decimal(N_plus).ln()) / (Decimal(2 * M + 1)).ln()
    return str(v)[:digits + 2]


# ----------------------------------------------------------------------------
# Rational-power certificate:  value >= c  <=>  N-^q >= N+^q * (2M+1)^p   (c-1 = p/q)
# ----------------------------------------------------------------------------

def certifies_at_least(N_plus, N_minus, M, c):
    """
    Exact (no-float) check of  1 + log(N-/N+)/log(2M+1) >= c, for rational c = Fraction.
    Equivalent (all quantities > 1, log increasing) to:
        log(N-/N+) >= (c-1) * log(2M+1)
        (N-/N+) >= (2M+1)^(c-1)            [assuming N- >= N+, i.e. value >= 1]
        N-^q >= N+^q * (2M+1)^p            where c-1 = p/q in lowest terms, p,q >= 0.
    Returns True iff the GHR bound value is >= c, as an exact integer comparison.
    """
    c = Fraction(c)
    cm1 = c - 1
    p = cm1.numerator
    q = cm1.denominator
    assert q > 0
    if p < 0:
        # c < 1; the value is always >= 1 > c here, trivially true.
        return N_minus >= N_plus  # value>=1 iff N->=N+
    lhs = N_minus ** q
    rhs = (N_plus ** q) * ((2 * M + 1) ** p)
    return lhs >= rhs


def largest_certified_rational(N_plus, N_minus, M, denom):
    """
    For a fixed denominator `denom`, return the largest c = k/denom (>=1) such that
    certifies_at_least(...) is True.  Lets us report a clean rational lower bound exactly.
    """
    # value is between 1 and 2 in practice; scan k from denom upward.
    best = None
    k = denom  # c = 1
    while True:
        c = Fraction(k, denom)
        if certifies_at_least(N_plus, N_minus, M, c):
            best = c
            k += 1
        else:
            break
        if k > 2 * denom:  # safety bound (value < 2)
            break
    return best
