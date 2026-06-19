#!/usr/bin/env python3
"""
Sketch: transfer-matrix-lower
Target (LOWER bound): gr(Av(1324)) > 10.271   [beats BBEPP2017 record 10.271]

Strategy (explorer angle C, cleanest Lean-fit certificate):
  Build a FINITE automaton / transfer matrix whose accepted language is a VERIFIED
  subclass S subset Av(1324). Then gr(S) = spectral radius rho(M) of the nonnegative
  integer transfer matrix M, and gr(Av(1324)) >= gr(S) = rho(M) since S subset Av(1324).
  A Collatz-Wielandt rational witness v > 0 with  M v >= lam v (entrywise) certifies
  rho(M) >= lam exactly, in rational linear algebra. If lam > 10.271 the record is beaten.

================================================================================
WHAT THIS ROUND (R1) DELIVERS -- a fully rigorous, end-to-end certified lower bound
via the cleanest provably-sound subclass found, the SKEW-SUM closure.
================================================================================

Sound subclass S_L (the transfer-matrix's accepted language)
------------------------------------------------------------
Every permutation skew-decomposes uniquely as a skew sum

        sigma = c_1 (-) c_2 (-) ... (-) c_t

of skew-INDECOMPOSABLE components c_i (the skew sum a(-)b places a in the top-left and
b in the bottom-right: every point of a is above-and-left of every point of b).

  S_L  :=  { sigma in Av(1324) : every skew-component c_i has length <= L }.

This is literally a SUBSET of Av(1324) (counted without repetition -- the skew
decomposition is unique), so |S_L,n| <= |Av_n(1324)| and gr(S_L) <= gr(Av(1324)).

SOUNDNESS  (obligation 1 -- proved, see prove_skew_sum_closure() below):
  LEMMA (skew-sum closure of Av(1324)).  a (-) b avoids 1324  <=>  a and b both avoid 1324.
  Proof of "<=" (the only direction we need): suppose a, b avoid 1324 and a(-)b contains
  a 1324 at positions q1<q2<q3<q4 with value-ranks (1,3,2,4).  In a(-)b the a-points occupy
  the LEFT positions and the HIGH values, the b-points the RIGHT positions and LOW values.
  Positions increase, so the chosen points lie in a as a position-prefix: the first t are in
  a, the last 4-t in b, for some t in {0,1,2,3,4}.  If t in {1,2,3} the occurrence "crosses".
  But then the t a-points -- having the HIGHEST values -- must carry the t LARGEST value-ranks
  among {1,2,3,4}.  Checking each t (done exactly in prove_skew_sum_closure):
      t=1: a-ranks must be {4}      but prefix-positions give ranks {1}        -- impossible
      t=2: a-ranks must be {3,4}    but prefix-positions give ranks {1,3}      -- impossible
      t=3: a-ranks must be {2,3,4}  but prefix-positions give ranks {1,2,3}    -- impossible
  (rank of position q1,q2,q3,q4 in pattern 1324 is 1,3,2,4 resp.)  So no crossing 1324
  exists; the occurrence is entirely in a or entirely in b, contradicting avoidance.   QED
  By induction over the number of components, every skew sum of avoiders avoids 1324, so
  S_L subset Av(1324) for every L.  (We also re-verify the lemma by brute force below.)

COUNT  (obligation: the matrix counts the subclass, no over/under-count):
  Let b_k = #{skew-indecomposable 1324-avoiders of length k}  (1 <= k <= L), computed
  EXACTLY by brute force here.  Because the skew decomposition is unique, the counting
  sequence f_n = |S_L,n| satisfies the LINEAR RECURRENCE
        f_n = sum_{k=1}^{L} b_k f_{n-k},   f_0 = 1,
  verified against brute-force enumeration of S_L (verify_recurrence()).  Hence
        gr(S_L) = lim f_n^{1/n} = (largest root of  x^L - sum_k b_k x^{L-k})
                = rho(M),  M = companion matrix of the recurrence (nonnegative integer).

CERTIFICATE  (obligation 2 -- exact rational Collatz-Wielandt):
  M's Perron eigenvector is geometric: v_i = q^{L-1-i}.  For the shift rows
  (M v)_i = v_{i-1} = q * v_i, so taking lam = q gives equality there.  For row 0,
  (M v)_0 / v_0 = sum_{k=1}^{L} b_k q^{1-k}, which EXCEEDS q for any rational q strictly
  below rho(M).  We pick such a rational q, set lam = q and v_i = q^{L-1-i} (exact Fractions),
  and re-check  M v >= lam v  componentwise in exact rational arithmetic.  This certifies
  rho(M) >= lam, hence gr(Av(1324)) >= lam.

HONEST STATUS -- THE RECORD IS *NOT* BEATEN THIS ROUND.
  The skew-sum truncation converges to gr(Av(1324)) ~ 11.6 only logarithmically slowly:
  L=8 gives ~3.773, and even L=16 (needing |Av_16(1324)|, an enormous enumeration) reaches
  only ~5.10.  No feasible L clears 10.271 by THIS construction.  We therefore CERTIFY the
  honest sub-record value and leave the record-beating step as an explicit hole H_BIG: find
  a *sound* automaton/transfer matrix (e.g. a staircase of Av(132)/Av(213) Catalan cells with
  rigorously bounded GF-weighted entries, BBEPP's actual engine) whose certified Perron root
  exceeds 10.271.  The Collatz-Wielandt machinery below is exactly what certifies it once the
  matrix exists -- so this round discharges H2 (soundness) + H3 (CW certificate) on a real
  machine and reshapes H1 to "a HIGHER-growth sound machine" (see approach doc).

Both load-bearing obligations are met for the value we CLAIM (a lower bound, just below the
record): (1) S_L subset Av(1324), proved + brute-checked; (2) exact rational CW inequality.
"""
from fractions import Fraction
from itertools import permutations, combinations

RECORD_LOWER = Fraction(10271, 1000)  # BBEPP2017 verified lower bound to strictly beat


# ----------------------------------------------------------------------------- #
#  Pattern machinery (1324 = value pattern (1,3,2,4) at increasing positions)    #
# ----------------------------------------------------------------------------- #
def contains_1324(p):
    """True iff permutation p (0-indexed tuple) contains the pattern 1324."""
    n = len(p)
    for a, b, c, d in combinations(range(n), 4):
        # positions a<b<c<d, need values p[a] < p[c] < p[b] < p[d]
        if p[a] < p[c] < p[b] < p[d]:
            return True
    return False


def is_skew_indecomposable(p):
    """True iff p cannot be written a (-) b with a,b nonempty.
    p is skew-DECOMPOSABLE iff some proper position-prefix 0..i holds exactly the TOP
    values {n-i-1, ..., n-1}.  (That prefix would be the top-left block a.)"""
    n = len(p)
    mn = n
    for i in range(n - 1):
        mn = min(mn, p[i])
        if mn == n - (i + 1):
            return False
    return True


def skew_components(p):
    """Return the list of skew-component lengths of p (unique skew decomposition)."""
    n = len(p)
    comps = []
    start = 0
    mn = n
    for i in range(n):
        mn = min(mn, p[i])
        if mn == n - (i + 1):
            comps.append(i - start + 1)
            start = i + 1
            mn = n
    return comps


# ----------------------------------------------------------------------------- #
#  Obligation 1: SOUNDNESS  --  skew-sum closure of Av(1324)                      #
# ----------------------------------------------------------------------------- #
def prove_skew_sum_closure():
    """Exact finite proof that a crossing 1324 is impossible in a skew sum a(-)b.

    Pattern 1324 has value-rank pattern (1,3,2,4) at positions (q1,q2,q3,q4) with
    q1<q2<q3<q4.  In a(-)b, a-points take the left positions and the high values.
    A crossing occurrence has the first t points (t in {1,2,3}) in a; those t points,
    carrying the highest values, must have the t LARGEST ranks of {1,2,3,4}.  We show the
    ranks actually sitting on the first t positions are never the t largest -> impossible.
    """
    # rank of pattern position q_i (1-indexed pos i -> rank), pattern 1324:
    posrank = {1: 1, 2: 3, 3: 2, 4: 4}
    for t in (1, 2, 3):
        a_ranks = sorted(posrank[i] for i in range(1, t + 1))        # ranks on prefix positions
        b_ranks = sorted(posrank[i] for i in range(t + 1, 5))        # ranks on suffix positions
        a_must_be_top = (min(a_ranks) > max(b_ranks))                # a needs the highest ranks
        assert not a_must_be_top, f"crossing 1324 NOT excluded for t={t}"
    return True


def brute_check_skew_closure(max_total=7):
    """Re-verify the lemma by brute force: for all a,b avoiders with |a|+|b|<=max_total,
    a(-)b avoids 1324.  (Direction we use: both avoid => sum avoids.)"""
    def skew_sum(a, b):
        n = len(a) + len(b)
        # a in top-left: values offset by len(b); b in bottom-right.
        return tuple([x + len(b) for x in a] + list(b))
    allp = {n: list(permutations(range(n))) for n in range(1, max_total)}
    for la in range(1, max_total):
        for lb in range(1, max_total - la + 1):
            for a in allp[la]:
                if contains_1324(a):
                    continue
                for b in allp[lb]:
                    if contains_1324(b):
                        continue
                    if contains_1324(skew_sum(a, b)):
                        raise AssertionError(f"skew closure FAILS: {a} (-) {b}")
    return True


# ----------------------------------------------------------------------------- #
#  Build the transfer (companion) matrix M of the sound subclass S_L            #
# ----------------------------------------------------------------------------- #
def skew_indec_counts(L):
    """b_k = #{skew-indecomposable 1324-avoiders of length k}, exact, 1<=k<=L."""
    b = [0] * (L + 1)
    for k in range(1, L + 1):
        b[k] = sum(
            1 for p in permutations(range(k))
            if (not contains_1324(p)) and is_skew_indecomposable(p)
        )
    return b


def build_subclass_automaton(L):
    """H1 (this round: the skew-sum machine) + H2 (soundness, discharged above).

    Returns (M, b) where M is the L x L nonnegative integer companion matrix of the
    recurrence  f_n = sum_{k=1}^L b_k f_{n-k}  counting S_L = { avoiders whose every
    skew-component has length <= L }.  rho(M) = gr(S_L) <= gr(Av(1324))."""
    b = skew_indec_counts(L)
    M = [[0] * L for _ in range(L)]
    for j in range(L):
        M[0][j] = b[j + 1]            # row 0 = [b_1, ..., b_L]
    for i in range(1, L):
        M[i][i - 1] = 1               # shift rows
    return M, b


def verify_recurrence(b, L, upto=7):
    """Confirm the matrix counts the subclass exactly: the recurrence f_n = sum b_k f_{n-k}
    reproduces the BRUTE-FORCE count of S_L (no over/under-counting)."""
    # recurrence values
    f = [1] + [0] * upto
    for n in range(1, upto + 1):
        f[n] = sum(b[k] * f[n - k] for k in range(1, min(L, n) + 1))
    # brute counts of S_L
    for n in range(1, upto + 1):
        brute = sum(
            1 for p in permutations(range(n))
            if (not contains_1324(p)) and max(skew_components(p)) <= L
        )
        assert f[n] == brute, f"recurrence != subclass count at n={n}: {f[n]} vs {brute}"
    return True


# ----------------------------------------------------------------------------- #
#  Obligation 2: Collatz-Wielandt rational witness  M v >= lam v                 #
# ----------------------------------------------------------------------------- #
def collatz_wielandt_witness(M, b, L):
    """H3 (discharged).  Geometric witness v_i = q^{L-1-i}, lam = q, with q a rational
    strictly below rho(M).  Returns (lam, v) with all entries exact Fractions, satisfying
    (M v)_i >= lam * v_i for every i.  Certifies rho(M) >= lam."""
    # Find rho(M) numerically only to pick a good rational q below it (the CHECK is exact).
    import numpy as np
    rho = max(np.linalg.eigvals(np.array(M, dtype=float)).real)
    # pick q = a rational just below rho such that  sum_k b_k q^{1-k} >= q  (verified exactly).
    # Walk q down from rho until the exact row-0 inequality holds.
    q = Fraction(int(rho * 10**6) - 1, 10**6)  # rational just below rho
    def row0_ge(q):
        # (M v)_0 / v_0 = sum_{k=1}^L b_k q^{1-k} >= q  <=>  sum_k b_k q^{L-k} >= q^L
        lhs = sum(b[k] * q ** (L - k) for k in range(1, L + 1))
        return lhs >= q ** L
    steps = 0
    while not row0_ge(q):
        q -= Fraction(1, 10**6)
        steps += 1
        if steps > 10**6:
            raise RuntimeError("could not find rational CW witness below rho")
    lam = q
    v = [q ** (L - 1 - i) for i in range(L)]   # exact Fractions, all > 0
    return lam, v


# ----------------------------------------------------------------------------- #
def certify(L=8):
    # Obligation 1 -- soundness (analytic finite proof + brute re-check).
    assert prove_skew_sum_closure(), "skew-sum closure proof failed"
    assert brute_check_skew_closure(max_total=7), "brute skew-closure check failed"

    # Build the sound transfer matrix and confirm it counts the subclass exactly.
    M, b = build_subclass_automaton(L)
    assert verify_recurrence(b, L, upto=7), "transfer matrix mis-counts the subclass"

    # Obligation 2 -- exact rational Collatz-Wielandt certificate.
    lam, v = collatz_wielandt_witness(M, b, L)
    assert all(x > 0 for x in v), "witness must be strictly positive"
    Mv = [sum(Fraction(int(M[i][j])) * v[j] for j in range(L)) for i in range(L)]
    assert all(Mv[i] >= lam * v[i] for i in range(L)), "CW inequality M v >= lam v fails"

    print(f"skew-indecomposable 1324-avoider counts b_1..b_{L} = {b[1:]}")
    print(f"transfer matrix M is {L}x{L}, nonnegative integer (companion of the recurrence)")
    print(f"CERTIFIED (exact rational Collatz-Wielandt):  gr(Av(1324)) >= rho(M) >= {lam}")
    print(f"            = {float(lam):.6f}")
    beats = lam > RECORD_LOWER
    print(f"record to beat (BBEPP2017): {float(RECORD_LOWER)}   --  beats record: {beats}")
    if not beats:
        print("HOLE H_BIG REMAINS: this sound skew-sum machine certifies a TRUE but "
              "SUB-RECORD lower bound; converges to ~11.6 only logarithmically. A "
              "higher-growth sound machine (staircase of Catalan cells) is needed to clear "
              "10.271 -- the CW machinery above certifies it the moment that matrix exists.")
    return lam


if __name__ == "__main__":
    certify(L=8)
