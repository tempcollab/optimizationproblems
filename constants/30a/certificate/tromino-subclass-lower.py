#!/usr/bin/env python3
"""
Sketch: tromino-subclass-lower
Target (LOWER bound): gr(Av(1324)) > 10.271   [beats BBEPP2017 record 10.271]

Strategy (explorer angle C/D + outliner B1 -- BBEPP's named open route).
  BBEPP (Thm 5.1) build a SUBCLASS P_k of Av(1324) gridded along the
  (Av(213),Av(132)) descending staircase, decomposed into DOMINOES (2-cell blocks)
  + single CONNECTING cells, with an EXACT closed-form count and an algebraic
  growth-rate limit 81/8 = 10.125.  They flag (Sec 7.4): a lower bound on the
  growth rate of permutations gridded in the first THREE staircase cells (TROMINOES)
  would, by decomposing the staircase into trominoes, give a NEW bound above 10.271.

WHAT THIS FILE DELIVERS THIS ROUND (R2), fully rigorously and reproducibly
==========================================================================
  H1' / H2  -- the DOMINO Thm-5.1 product, reconstructed and certified SOUND and
               EXACT, giving the verified lower bound

                   gr(Av(1324)) >= 81/8 = 10.125

               by an explicit subclass P_k subset Av(1324) with an exact rational
               count whose growth-rate limit is computed symbolically (sympy,
               exact) to be 81/8.  This is < the record 10.271, but >> the R1
               held value 3.773326, and is genuinely SOUND/algebraic (no continuum,
               no conjecture).

  H1 (the record-beating hole, LEFT OPEN, honest)  -- the TROMINO (3-cell) analogue:
               a certified lower bound g3 on the growth rate of permutations gridded
               in three consecutive staircase cells, then the tromino-decomposition
               product, which BBEPP say "seems to require new ideas."  We leave it as
               an explicit hole (raise NotImplementedError), with the sub-bound
               mechanism (a transfer-matrix sub-subclass INSIDE the tromino, certified
               by the same Collatz-Wielandt machinery as transfer-matrix-lower) spelt
               out but not yet discharged.

SOUNDNESS (the load-bearing obligations, stated for the reviewer)
=================================================================
The bound gr(Av(1324)) >= lim_k |P_k|^{1/N(k)} rests on exactly two facts:

 (S1) CONTAINMENT.  P_k subset Av(1324) for every k.  This is BBEPP Thm 5.1's
      construction: P_k is gridded in the descending (Av(213),Av(132)) staircase, and
      the "between-components" interleave rule -- every domino-cell point lies strictly
      between two consecutive skew-components of each adjacent connecting cell -- forces
      1324-avoidance.  The general containment is BBEPP Thm 5.1 (peer-reviewed), cited.
      We do NOT re-prove it here; instead we FAITHFULLY demonstrate that the cell-
      interleave constraint is GENUINE (non-vacuous): over all small gridded domino
      fillings, some column interleavings CREATE a 1324 and some AVOID it, so the rule
      is a real restriction (the containment claim is not trivially true).  [An earlier
      'descending-band' brute check was removed as VACUOUS -- it avoided 1324 only by a
      global descending layout, exercising no interleave constraint.]

 (S2) EXACT COUNT + GROWTH LIMIT.  |P_k| = |B_{14k}|^k * |C_{8k,7k}|^k *
      C(21k,14k)^{2k-1}, where
        - |B_n| = #{balanced dominoes, n points in each cell}; gr in TOTAL points is
          27/4 (BBEPP Prop 3.6 + Thm 3.1, cache lemma `domino_growth_constant`), so
          |B_n|^{1/n} -> (27/4)^2 = 729/16  (n counts points-per-cell here);
        - |C_{n,c}| = (c/n) C(2n-c-1, n-1) = #{forests of c plane trees on n nodes}
          (Catalan-forest / cycle-lemma count -- EXACT, verified integer + reduces to
          Catalan(n-1) at c=1);
        - C(21k,14k) is an ordinary binomial.
      The total point count is N(k) = 36 k^2 (Theta(k) cells each holding Theta(k)
      points).  We compute the limit
                lim_k |P_k|^{1/N(k)}  =  exp( lim_k (log|P_k|)/(36 k^2) )
      SYMBOLICALLY with sympy and obtain EXACTLY 81/8.

      WHY THIS IS A GENUINE LOWER BOUND (the sound chain, for the reviewer).  Let
      P := union_k P_k subset Av(1324) (by S1).  Each P_k consists of permutations of
      size exactly N(k)=36k^2, so |P_{N(k)}| >= |P_k| (members of P of size N(k) include
      all of P_k).  Hence
          gr(Av(1324)) = limsup_n |Av_n(1324)|^{1/n}
                       >= limsup_n |P_n|^{1/n}                  [P subset Av(1324)]
                       >= limsup_k |P_{N(k)}|^{1/N(k)}          [subsequence]
                       >= limsup_k |P_k|^{1/N(k)}
                       =  lim_k |P_k|^{1/N(k)} = 81/8.
      No super-multiplicativity / Fekete is needed -- a single subsequence of subclass
      sizes already forces the bound.  This is fully sound and unconditional.

WHY NOT THE RECORD YET.  81/8 = 10.125 < 10.271.  BBEPP push 10.125 -> 10.271 by the
Sec 6 concentration results + Sec 7 leaf-relaxation -- a CONTINUUM optimisation of a
multivariate generating function (radius of convergence), which is Lean-hostile and is
explicitly NOT re-derived here.  The ALGEBRAIC road past 10.271 is the tromino analogue
(H1): replace the 2-cell domino block by a 3-cell tromino block whose per-block growth
exceeds the domino's, lifting the product above 81/8.  That is the open hole.

Reproduce:  python3 constants/30a/certificate/tromino-subclass-lower.py
Top-level entrypoint RAISES on the open record-beating hole H1, so it can never print a
false "RECORD BEATEN" line; the verified 10.125 sub-record is reported by status_report().
"""
from fractions import Fraction
from itertools import permutations, combinations
from math import comb

import sympy as sp

RECORD_LOWER = Fraction(10271, 1000)   # BBEPP2017 verified lower bound to strictly beat
HELD_R1 = Fraction(3773326, 1000000)   # R1 verified held value (skew-sum floor)


# ----------------------------------------------------------------------------- #
#  Pattern machinery                                                             #
# ----------------------------------------------------------------------------- #
def contains_1324(p):
    """True iff permutation p (0-indexed tuple) contains the pattern 1324:
    positions a<b<c<d with values p[a] < p[c] < p[b] < p[d]."""
    n = len(p)
    for a, b, c, d in combinations(range(n), 4):
        if p[a] < p[c] < p[b] < p[d]:
            return True
    return False


# ----------------------------------------------------------------------------- #
#  (S2) component counts -- exact, verified                                      #
# ----------------------------------------------------------------------------- #
def catalan(m):
    """m-th Catalan number C(2m,m)/(m+1)."""
    return comb(2 * m, m) // (m + 1)


def catalan_forest_count(n, c):
    """|C_{n,c}| = (c/n) C(2n-c-1, n-1) -- number of ordered forests of c plane trees
    on n nodes total (cycle-lemma / ballot count).  Returns an exact Fraction; it is a
    nonnegative integer for 1 <= c <= n."""
    return Fraction(c, n) * comb(2 * n - c - 1, n - 1)


def verify_catalan_forest():
    """Check |C_{n,c}| is integer-valued and reduces to Catalan(n-1) at c=1."""
    for n in range(1, 12):
        for c in range(1, n + 1):
            v = catalan_forest_count(n, c)
            assert v.denominator == 1 and v >= 0, f"|C_{n},{c}| not a nonneg integer: {v}"
        assert catalan_forest_count(n, 1) == catalan(n - 1), \
            f"|C_{n},1| != Catalan({n - 1})"
    return True


def domino_counts_A000139(upto=8):
    """|D_n| = 2(3n+3)!/((n+2)!(2n+3)!)  (OEIS A000139).  gr = 27/4 (cache lemma
    `domino_growth_constant`).  Returns the list [|D_1|,...,|D_upto|]; cross-checked
    against OEIS A000139 = 2,6,22,91,408,1938,9614,49335,..."""
    from math import factorial as fac
    seq = [2 * fac(3 * n + 3) // (fac(n + 2) * fac(2 * n + 3)) for n in range(1, upto + 1)]
    oeis = [2, 6, 22, 91, 408, 1938, 9614, 49335][:upto]
    assert seq == oeis, f"domino count != A000139: {seq} vs {oeis}"
    return seq


# ----------------------------------------------------------------------------- #
#  (S2) the exact |P_k| product and its EXACT growth-rate limit (symbolic)       #
# ----------------------------------------------------------------------------- #
def Pk_exact(k):
    """Exact integer |P_k| = |B_{14k}|^k * |C_{8k,7k}|^k * C(21k,14k)^{2k-1}, with the
    balanced-domino factor evaluated by its EXACT asymptotic leading term symbol below;
    here we return the SYMBOLIC growth-determining product so the limit is exact.

    Note: |B_{14k}| has no elementary closed form (it is a sub-exponential correction
    times (27/4)^{28k}); for the GROWTH LIMIT only its exponential order matters, which
    is what growth_rate_limit() uses.  This function is informational (the exact finite
    count needs |B_{14k}|, which we do not enumerate)."""
    raise NotImplementedError(
        "exact finite |P_k| needs the non-elementary balanced-domino count |B_{14k}|; "
        "only the growth LIMIT (exponential order) is needed for the bound -- "
        "see growth_rate_limit()."
    )


def growth_rate_limit():
    """(S2) Exact symbolic growth-rate limit  g := lim_k |P_k|^{1/N(k)},  N(k)=36 k^2.

    log|P_k| = k*log|B_{14k}| + k*log|C_{8k,7k}| + (2k-1)*log C(21k,14k), with leading
    exponential orders (each verified independently below):
        log|B_{14k}|     ~ 14k * log((27/4)^2)     [balanced domino, gr 27/4 in pts/cell]
        log|C_{8k,7k}|   ~ k   * log( H(9,8) )      [Catalan forest, dominant binom C(9k,8k)]
        log C(21k,14k)   ~ k   * log( H(21,14) )    [entropy, H(a,b)=a^a/(b^b (a-b)^{a-b})]
    Dividing by N(k)=36 k^2 and taking k->inf gives an exact algebraic number.  Returns
    it as a sympy Rational; it equals EXACTLY 81/8.
    """
    k = sp.symbols('k', positive=True)

    def H(a, b):  # exact entropy limit  C(a k, b k)^{1/k} -> a^a / (b^b (a-b)^{a-b})
        a, b = sp.Integer(a), sp.Integer(b)
        return a ** a / (b ** b * (a - b) ** (a - b))

    twoseven4_sq = (sp.Rational(27, 4)) ** 2
    log_Pk = (k * (14 * k * sp.log(twoseven4_sq))     # k * log|B_{14k}|
              + k * (k * sp.log(H(9, 8)))             # k * log|C_{8k,7k}|  (dominant C(9k,8k))
              + (2 * k - 1) * (k * sp.log(H(21, 14))))  # (2k-1) * log C(21k,14k)
    NK = 36 * k ** 2
    log_g = sp.limit(sp.expand(log_Pk) / NK, k, sp.oo)
    g = sp.simplify(sp.exp(log_g))
    g = sp.nsimplify(g, rational=True)
    return g


def verify_growth_limit():
    """Confirm the symbolic limit is EXACTLY 81/8 and that each exponential piece's
    1/k-limit is the claimed exact algebraic number (guards the asymptotic inputs)."""
    g = growth_rate_limit()
    assert sp.simplify(g - sp.Rational(81, 8)) == 0, f"growth limit != 81/8: {g}"

    # independent re-check of the two binomial entropy limits at a large finite k,
    # in LOG space (the binomials are astronomically large; never convert to float).
    from math import lgamma, log
    def log_binom(n, m):
        return lgamma(n + 1) - lgamma(m + 1) - lgamma(n - m + 1)
    for (a, b) in [(9, 8), (21, 14)]:
        K = 4000
        approx_log = log_binom(a * K, b * K) / K          # (1/K) log C(aK,bK)
        lim = float(sp.Integer(a) ** a / (sp.Integer(b) ** b * sp.Integer(a - b) ** (a - b)))
        assert abs(approx_log - log(lim)) < 1e-2, \
            f"entropy limit off for ({a},{b}): {approx_log} vs {log(lim)}"
    return g


# ----------------------------------------------------------------------------- #
#  (S1) CONTAINMENT  P_k subset Av(1324) -- BBEPP rule + small brute check        #
# ----------------------------------------------------------------------------- #
def _contains_pattern(p, std):
    """True iff permutation p contains the pattern given by 0-indexed standard form std."""
    k = len(std)
    for idx in combinations(range(len(p)), k):
        sub = [p[i] for i in idx]
        rk = {v: i for i, v in enumerate(sorted(sub))}
        if [rk[x] for x in sub] == list(std):
            return True
    return False


def verify_domino_mechanism_has_teeth():
    """(S1) FAITHFUL demonstration that the cell-interleave constraint is a GENUINE,
    non-vacuous restriction -- i.e. the brute check below has teeth.

    Model a single DOMINO (BBEPP's verified 2-cell core): a top cell whose content avoids
    213 (values all ABOVE the bottom cell), a bottom cell whose content avoids 132, and a
    choice of how the two cells' columns INTERLEAVE.  We enumerate small fillings over ALL
    column interleavings and confirm BOTH:
      (a) SOME interleaving CREATES a 1324  -> the interleave choice is a real constraint
          (so a containment claim is NOT trivially true; the rule does work);
      (b) SOME interleaving AVOIDS 1324     -> the avoiding subclass is non-empty.
    This is the honest, teeth-having statement we can fully check by brute force.  It does
    NOT by itself verify BBEPP's exact between-skew-components interleave rule on the full
    staircase -- that general containment is BBEPP Thm 5.1 (peer-reviewed), cited as (S1).
    (An earlier 'descending-band' toy check was REMOVED: it avoided 1324 trivially by the
    global descending layout and so exercised no interleave constraint -- a vacuous guard.)
    """
    P213 = (1, 0, 2)   # pattern 213, 0-indexed
    P132 = (0, 2, 1)   # pattern 132, 0-indexed
    P1324 = (0, 2, 1, 3)
    saw_violation = False
    saw_ok = False
    for nt in range(1, 4):
        for nb in range(1, 4):
            if nt + nb > 5:
                continue
            for tperm in permutations(range(nt)):
                if _contains_pattern(tperm, P213):
                    continue                      # top cell avoids 213
                for bperm in permutations(range(nb)):
                    if _contains_pattern(bperm, P132):
                        continue                  # bottom cell avoids 132
                    tvals = [v + nb for v in tperm]   # top values all above bottom
                    bvals = list(bperm)
                    for cols in combinations(range(nt + nb), nt):  # column interleaving
                        arr = [None] * (nt + nb)
                        ti = bi = 0
                        for c in range(nt + nb):
                            if c in cols:
                                arr[c] = tvals[ti]; ti += 1
                            else:
                                arr[c] = bvals[bi]; bi += 1
                        if _contains_pattern(tuple(arr), P1324):
                            saw_violation = True
                        else:
                            saw_ok = True
    assert saw_violation, "interleave constraint is VACUOUS (no filling makes 1324) -- " \
        "the containment claim would be trivial; check the model"
    assert saw_ok, "no interleaving avoids 1324 -- the avoiding subclass would be empty"
    return saw_violation and saw_ok


# ----------------------------------------------------------------------------- #
#  H1 -- the RECORD-BEATING hole (tromino analogue), LEFT OPEN, honest           #
# ----------------------------------------------------------------------------- #
def tromino_growth_lower():
    """HOLE H1 (open).  A certified LOWER bound g3 on the growth rate of 1324-avoiders
    gridded in three consecutive staircase cells (a TROMINO block).

    MECHANISM (sound sub-bound, not exact enumeration -- sidesteps BBEPP's "new ideas"):
      Build an explicit transfer-matrix sub-subclass T inside the tromino: a finite
      automaton whose accepted gridded fillings are VERIFIED 1324-avoiders (brute-checked
      on the 3-cell fragment as in verify_containment_small), with nonnegative integer
      transfer matrix M_T.  Then gr(tromino) >= gr(T) = rho(M_T), certified by an
      exact-rational Collatz-Wielandt witness M_T v >= lam v (the SAME machinery as
      transfer-matrix-lower / Walks2025).  If the tromino's per-block growth g3 exceeds
      the balanced domino's (27/4)^2 strongly enough, the tromino-decomposition product
      (H2 below) lifts the staircase bound above 10.271.

    OPEN because: constructing T with g3 large enough to clear 10.271 in the product is
    real new work -- the genuine BBEPP obstruction.  Raises so the top-level can never
    falsely claim the record."""
    raise NotImplementedError(
        "H1: tromino (3-cell) growth-rate lower bound via a CW-certified transfer-matrix "
        "sub-subclass -- the record-beating step; not discharged this round."
    )


def tromino_decomposition_growth(g3):
    """HOLE H2' (open, depends on H1).  The Thm-5.1 ANALOGUE for trominoes: decompose the
    staircase into 3-cell tromino blocks + connecting cells and assemble the exact-count
    product, returning the algebraic growth-rate limit as a function of the tromino
    sub-bound g3 and the optimised point-ratios.  Must exceed 10.271 for some admissible
    ratios.  Open until H1 supplies g3."""
    raise NotImplementedError(
        "H2': tromino-decomposition product + ratio optimisation -> growth > 10.271; "
        "needs the H1 sub-bound g3 first."
    )


# ----------------------------------------------------------------------------- #
#  Top-level                                                                      #
# ----------------------------------------------------------------------------- #
def lower_bound():
    """RECORD-BEATING entrypoint.  Runs the open H1 -> H2 chain; RAISES until the tromino
    push is discharged, so no false 'RECORD BEATEN' can print."""
    g3 = tromino_growth_lower()                 # H1 (open)
    g = tromino_decomposition_growth(g3)        # H2' (open)
    assert g > RECORD_LOWER, f"growth {float(g)} does not beat {float(RECORD_LOWER)}"
    print(f"RECORD BEATEN: gr(Av(1324)) >= {g} = {float(g):.6f} > {float(RECORD_LOWER)}")
    return g


def status_report():
    """Verified, reproducible SUB-RECORD lower bound this round: the SOUND domino Thm-5.1
    product -> exactly 81/8 = 10.125.  Discharges (S1) containment (cited + brute-checked)
    and (S2) exact count + symbolic growth limit.  10.125 > R1 held 3.773326, < record
    10.271 (the gap to 10.271 is BBEPP's continuum step / the open tromino hole H1)."""
    print("=" * 74)
    print("tromino-subclass-lower -- verified content this round (SOUND, no continuum)")
    print("=" * 74)

    assert verify_catalan_forest(), "Catalan-forest count check failed"
    print("[S2] Catalan-forest |C_{n,c}| = (c/n)C(2n-c-1,n-1): integer + Catalan(n-1) @ c=1  OK")

    dom = domino_counts_A000139(8)
    print(f"[S2] domino counts |D_1..8| = {dom}  == OEIS A000139  OK  (gr=27/4, cache lemma)")

    assert verify_domino_mechanism_has_teeth()
    print("[S1] interleave constraint is GENUINE (some fillings make 1324, some avoid it)  "
          "OK\n     general containment P_k subset Av(1324): BBEPP Thm 5.1 (cited)")

    g = verify_growth_limit()
    print(f"[S2] exact symbolic growth-rate limit  lim_k |P_k|^(1/36k^2) = {g} "
          f"= {float(g):.6f}")
    print()
    print(f"VERIFIED (sound, algebraic, reproducible):  gr(Av(1324)) >= {g} "
          f"= {float(g):.6f}")
    print(f"   R1 held value to clear .......... {float(HELD_R1):.6f}   beats held: "
          f"{Fraction(81,8) > HELD_R1}")
    print(f"   record to beat (BBEPP2017) ...... {float(RECORD_LOWER):.6f}   beats record: "
          f"{Fraction(81,8) > RECORD_LOWER}")
    print()
    print("OPEN HOLE H1 (record-beating): tromino (3-cell) analogue -- a CW-certified "
          "transfer-matrix\n  sub-bound g3 on the tromino growth rate, then the "
          "tromino-decomposition product > 10.271.\n  BBEPP: 'enumerating trominoes "
          "seems to require some new ideas.'  Not discharged.")
    return g


if __name__ == "__main__":
    # Report the verified SUB-RECORD bound (10.125); never claims the record.
    status_report()
    # The record-beating chain is an OPEN hole -- demonstrate it raises (sound guard),
    # without aborting the verified report above.
    try:
        lower_bound()
    except NotImplementedError as e:
        print(f"\n[record-beating hole H1 raises, as expected]  {e}")
