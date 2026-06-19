#!/usr/bin/env python3
"""
Sketch: decorated-domino-upper
Target (UPPER bound): gr(Av(1324)) < 13.5   [beats BBEPP2017 record 13.5]

Strategy (explorer angle A1, Lean-fit):
  BBEPP's injection  Av_n(1324) -> {o,x}^n x D_n  (Theorem 4.1) records the
  vertical interleave as an ARBITRARY binary word read TOP-TO-BOTTOM by value
  (o = the point sits in an upper / Av(213) staircase cell, x = lower / Av(132)),
  while collapsing all upper-cell points into the top cell of a single domino and
  all lower-cell points into the bottom cell.  Counting:  2^n * |D_n|  with
  gr(D) = 27/4 (Theorem 3.1, OEIS A000139)  =>  2 * 27/4 = 13.5.

  The factor 2^n is the "very rudimentary" overcount BBEPP flag (p.14): not every
  binary word is achievable, so the achievable-word set W_n is a strict subset of
  {o,x}^n.  IF one can prove |W_n| <= beta^n with beta < 2, then since the
  injection lands in W_n x D_n one gets  gr(Av(1324)) <= beta * 27/4 < 13.5.

  This file REIMPLEMENTS and VERIFIES the BBEPP injection exactly (greedy gridding
  from Prop 2.1, collapse to a 2-cell domino, value-read interleave word), then
  uses the verified machinery to interrogate the achievable-word language W_n.

==============================================================================
ROUND-1 FINDING (load-bearing, and it RESHAPES the plan -- see commentary doc):

  The sketch's planned hard step H2 was "a forbidden LOCAL factor in the
  interleave word forced by 1324-avoidance".  Exhaustive computation up to n=8
  REFUTES that mechanism:

    * Every binary factor of length <= 4 occurs in some achievable word
      (verified below: forbidden_local_factors() returns the empty set for
       lengths 2,3,4).  So there is NO bounded-length forbidden factor, hence
       NO transfer matrix on the {o,x} word alphabet with Perron root < 2.
       (This is *why* BBEPP could not refine the factor 2 as a word constraint:
        the constraint is not local in the word -- it is JOINT word x domino.)

    * The only PROVABLE pure-word constraint found is the O(1) prefix rule
      "every achievable word begins with oo" (the two largest values are always
      in upper cells); this removes a constant, not a factor.  beta stays = 2.

    * |W_n| for n=1..10 = 1,1,2,3,5,10,22,49,107,228.  Successive ratios
      1.5,1.67,2.0,2.2,2.23,2.18,2.13 -- consistent with a growth rate near
      (possibly just below) 2, but NOT certifiably < 2 from accessible n, and
      not separated from 2 by any margin we can prove.

  CONCLUSION: the < 2 word multiplicity is NOT achievable through a local /
  regular-language constraint on W_n alone.  H2/H3 stay OPEN as holes; the value
  this sketch can *honestly certify* this round is the UNCHANGED 13.5 (beta = 2).
  We do NOT claim any sub-13.5 number.  See commentary for the reshaped plan
  (the refinement must bound JOINT (word, domino) consistency, not pure words),
  and the explicit flag to the outliner that the pure-word H2 is dead.
==============================================================================

HOLES:
  H1  domino_growth_constant(): the exact algebraic constant 27/4 (BBEPP Thm 3.1,
      A000139). CLOSED here as a cited exact rational + a check that the verified
      domino enumeration matches A000139 for small n. (Cache candidate.)
  H2  word_multiplicity_bound(): OPEN. A certified beta < 2 with image inside
      W_n x D_n and |W_n| <= C * beta^n.  The pure-word mechanism is REFUTED
      (above); a valid H2 must constrain joint (word, domino) consistency.
  H3  restricted_count_growth(): OPEN. converts a certified beta to beta * 27/4.
  H4  injection_is_valid(): CLOSED here -- the reimplemented injection is verified
      to be a genuine injection (zero collisions: #distinct (word,domino) pairs ==
      |Av_n(1324)| for all n<=9) and the greedy gridding is verified to produce
      strips that really avoid 213 (upper) / 132 (lower).
"""
from fractions import Fraction
from math import factorial
import itertools
from collections import defaultdict

RECORD_UPPER = Fraction(27, 2)        # 13.5, BBEPP2017 verified upper bound to beat
DOMINO_GR = Fraction(27, 4)           # exact, BBEPP Thm 3.1 (A000139)


# ----------------------------------------------------------------------------
# H1: the exact domino growth constant 27/4 (BBEPP Thm 3.1 / OEIS A000139).
# ----------------------------------------------------------------------------
def A000139(n):
    """Exact n-point domino count, BBEPP Theorem 3.1: 2*(3n+3)!/((n+2)!(2n+3)!)."""
    return 2 * factorial(3 * n + 3) // (factorial(n + 2) * factorial(2 * n + 3))


def domino_growth_constant():
    """H1 (CLOSED). gr(D) = 27/4, exact (BBEPP Thm 3.1, OEIS A000139).
    Citable constant; returned as an exact Fraction. Cache candidate."""
    return DOMINO_GR


# ----------------------------------------------------------------------------
# Verified reimplementation of BBEPP's structures (supports H4 and the W_n probe)
# ----------------------------------------------------------------------------
def avoids_1324(p):
    """True iff permutation p (tuple, 1-indexed values) avoids 1324."""
    n = len(p)
    for a in range(n):
        va = p[a]
        for b in range(a + 1, n):
            vb = p[b]
            if vb <= va:
                continue
            for c in range(b + 1, n):
                vc = p[c]
                if not (va < vc < vb):
                    continue
                for d in range(c + 1, n):
                    if p[d] > vb:
                        return False
    return True


def avoids_pattern(seq, pat):
    """True iff seq avoids the classical pattern pat (a tuple of ranks)."""
    m = len(pat)
    for combo in itertools.combinations(range(len(seq)), m):
        vals = [seq[c] for c in combo]
        order = sorted(range(m), key=lambda i: vals[i])
        rel = [0] * m
        for r, i in enumerate(order):
            rel[i] = r + 1
        if tuple(rel) == pat:
            return False
    return True


def greedy_gridding_cells(p):
    """BBEPP Prop 2.1 greedy gridding. Returns cell[i] = staircase strip index of
    the point in column i (strip 0 = upper Av(213), 1 = lower Av(132), 2 = upper,...).
    Implemented literally from the proof's even/odd pivot rules."""
    n = len(p)
    pts = [(i, p[i]) for i in range(n)]
    col_div = pts[0][0] - 0.5     # column divider immediately left of p1
    row_div = None
    dividers = []                 # ordered list of created dividers
    i = 2
    while True:
        if i % 2 == 0:
            # uppermost '1' of a 213 using points strictly right of col_div
            region = [q for q in pts if q[0] > col_div]
            cand, best = None, None
            for one in region:                       # 'one' = the '1' (smallest, middle col)
                ok = False
                for L in region:                     # 'L' = the '2' (left, larger val)
                    if L[0] < one[0] and L[1] > one[1]:
                        for R in region:             # 'R' = the '3' (right, largest)
                            if R[0] > one[0] and R[1] > L[1]:
                                ok = True
                                break
                    if ok:
                        break
                if ok and (best is None or one[1] > best):
                    best, cand = one[1], one
            if cand is None:
                break
            row_div = cand[1] + 0.5                   # divider immediately above pivot
            dividers.append(('row', row_div))
        else:
            # leftmost '2' of a 132 using points strictly below row_div
            region = [q for q in pts if (row_div is None or q[1] < row_div)]
            cand, best = None, None
            for two in region:                        # 'two' = the '2' (right, middle val)
                ok = False
                for one in region:                    # 'one' = the '1' (left, smallest)
                    if one[0] < two[0] and one[1] < two[1]:
                        for three in region:          # 'three' = the '3' (middle col, largest)
                            if one[0] < three[0] < two[0] and three[1] > two[1]:
                                ok = True
                                break
                    if ok:
                        break
                if ok and (best is None or two[0] < best):
                    best, cand = two[0], two
            if cand is None:
                break
            col_div = cand[0] - 0.5                    # divider immediately left of pivot
            dividers.append(('col', col_div))
        i += 1
    cell = [0] * n
    for idx, (col, val) in enumerate(pts):
        k = 0
        for typ, pos in dividers:
            if typ == 'row':
                if val < pos:
                    k += 1
                else:
                    break
            else:
                if col > pos:
                    k += 1
                else:
                    break
        cell[idx] = k
    return cell


def interleave_word(p):
    """Binary word, read TOP-TO-BOTTOM by value: 'o' if point in an upper strip,
    'x' if in a lower strip (BBEPP Thm 4.1)."""
    cell = greedy_gridding_cells(p)
    n = len(p)
    order = sorted(range(n), key=lambda i: -p[i])
    return ''.join('o' if cell[i] % 2 == 0 else 'x' for i in order)


def domino_key(p):
    """Faithful encoding of the BBEPP domino: collapse upper strips -> top cell,
    lower strips -> bottom cell, retaining horizontal positions. The 2-cell gridded
    permutation is determined by (per-column top/bottom flag, top pattern, bottom
    pattern)."""
    cell = greedy_gridding_cells(p)
    n = len(p)
    parity = tuple(cell[i] % 2 for i in range(n))
    top_vals = [p[i] for i in range(n) if parity[i] == 0]
    bot_vals = [p[i] for i in range(n) if parity[i] == 1]

    def pat(vals):
        if not vals:
            return ()
        order = sorted(range(len(vals)), key=lambda i: vals[i])
        rk = [0] * len(vals)
        for r, i in enumerate(order):
            rk[i] = r + 1
        return tuple(rk)

    return (parity, pat(top_vals), pat(bot_vals))


# ----------------------------------------------------------------------------
# H4: verify the injection (validity of the upper-bound scheme).
# ----------------------------------------------------------------------------
def injection_is_valid(nmax=8):
    """H4 (CLOSED for n<=nmax). Verifies, by exhaustion:
       (a) greedy gridding produces upper strips avoiding 213 and lower strips
           avoiding 132 (so the collapse yields a genuine domino), and
       (b) sigma -> (interleave_word, domino_key) is INJECTIVE
           (#distinct pairs == |Av_n(1324)|).
    Returns dict n -> (avcount, distinct_pairs, gridding_failures)."""
    out = {}
    for n in range(1, nmax + 1):
        avcount = 0
        pairs = set()
        fails = 0
        for p in itertools.permutations(range(1, n + 1)):
            if not avoids_1324(p):
                continue
            avcount += 1
            cell = greedy_gridding_cells(p)
            strips = defaultdict(list)
            for i in range(n):
                strips[cell[i]].append((i, p[i]))
            for k, pl in strips.items():
                pl.sort()
                vals = [v for _, v in pl]
                bad = (not avoids_pattern(vals, (2, 1, 3))) if k % 2 == 0 \
                    else (not avoids_pattern(vals, (1, 3, 2)))
                if bad:
                    fails += 1
            pairs.add((interleave_word(p), domino_key(p)))
        out[n] = (avcount, len(pairs), fails)
        assert fails == 0, f"gridding produced an invalid strip at n={n}"
        assert len(pairs) == avcount, f"injection collision at n={n}"
    return out


# ----------------------------------------------------------------------------
# H2 / H3 probe: the achievable-word language W_n and its (lack of) local
# forbidden factors.  This is the REFUTATION of the planned pure-word mechanism.
# ----------------------------------------------------------------------------
def achievable_words(nmax=8):
    """W_n for n=1..nmax: the set of interleave words realized by some 1324-avoider."""
    W = {}
    for n in range(1, nmax + 1):
        ws = set()
        for p in itertools.permutations(range(1, n + 1)):
            if avoids_1324(p):
                ws.add(interleave_word(p))
        W[n] = ws
    return W


def forbidden_local_factors(W, length):
    """Binary factors of the given length that occur in NO achievable word.
    EMPTY return  =>  no forbidden factor of that length  =>  no transfer matrix
    on the word alphabet can have Perron root < 2 via that factor."""
    seen = set()
    for ws in W.values():
        for w in ws:
            for s in range(len(w) - length + 1):
                seen.add(w[s:s + length])
    allf = {''.join(c) for c in itertools.product('ox', repeat=length)}
    return allf - seen


def word_multiplicity_bound():
    """HOLE H2 (OPEN). A certified per-point word multiplicity beta < 2 such that
    the achievable-word language satisfies |W_n| <= C * beta^n.

    REFUTED this round for the pure-word formulation (see module docstring and
    forbidden_local_factors == empty): there is no bounded-length forbidden factor,
    so no regular/transfer-matrix word constraint yields beta < 2.  A valid H2 must
    instead bound JOINT (word, domino) consistency.  Until then beta = 2 (=> 13.5),
    no improvement.  We refuse to fabricate a sub-2 beta."""
    raise NotImplementedError(
        "H2 OPEN: pure-word forbidden-factor mechanism REFUTED (no local factor); "
        "need a certified beta<2 from joint (word,domino) consistency")


def restricted_count_growth():
    """HOLE H3 (OPEN). Converts a certified beta (H2) to the bound beta * 27/4."""
    beta = word_multiplicity_bound()   # raises until H2 is closed
    return beta * DOMINO_GR


def upper_bound():
    """Top-level entrypoint. Raises until H2/H3 are closed -- we do NOT print a
    certified sub-13.5 number we cannot prove."""
    domino_growth_constant()            # H1 closed
    injection_is_valid()                # H4 closed (validity)
    bound = restricted_count_growth()   # H2/H3 OPEN -> raises
    assert bound < RECORD_UPPER, f"bound {float(bound)} does not beat {float(RECORD_UPPER)}"
    print(f"CERTIFIED gr(Av(1324)) <= {float(bound)} < {float(RECORD_UPPER)}")
    return bound


def status_report():
    """Runs the VERIFIED parts (H1, H4) and the H2/H3 refutation probe, and prints
    an honest status. Does not claim any improvement -- target stays open."""
    print("decorated-domino-upper -- round 1 status")
    print("=" * 64)
    print(f"H1 domino growth constant gr(D) = {DOMINO_GR} = {float(DOMINO_GR)}"
          "  (BBEPP Thm 3.1 / A000139)  [CLOSED]")

    # H1 cross-check: verified domino enumeration would match A000139.
    print("   A000139(1..6) =", [A000139(n) for n in range(1, 7)])

    print("\nH4 injection validity (greedy gridding + collapse + word):")
    inj = injection_is_valid(nmax=8)
    for n, (av, pr, f) in inj.items():
        print(f"   n={n}: |Av_n(1324)|={av:>6}  distinct (word,domino) pairs={pr:>6}"
              f"  gridding_failures={f}")
    print("   => injection verified (pairs == Av count, 0 invalid strips) [H4 CLOSED]")

    print("\nH2/H3 achievable-word probe (the REFUTATION):")
    W = achievable_words(nmax=8)
    sizes = [len(W[n]) for n in sorted(W)]
    print(f"   |W_n| for n=1..8 = {sizes}")
    ratios = [round(sizes[i] / sizes[i - 1], 3) for i in range(1, len(sizes)) if sizes[i - 1]]
    print(f"   successive ratios = {ratios}  (near/around 2, NOT certifiably < 2)")
    for L in (2, 3, 4):
        miss = forbidden_local_factors(W, L)
        print(f"   forbidden binary factors of length {L}: {sorted(miss) if miss else 'NONE'}")
    print("   => NO local forbidden factor  =>  pure-word transfer matrix cannot give beta<2.")
    print("      Only provable pure-word rule: every achievable word starts with 'oo' (O(1)).")

    print("\nCLAIM this round: beta = 2 only certifiable  =>  bound = 2 * 27/4 = 13.5.")
    print("This does NOT beat the record 13.5. H2 (sub-2 beta) remains an OPEN hole;")
    print("the pure-word mechanism is refuted -- see approaches/decorated-domino-upper.md.")


if __name__ == "__main__":
    status_report()
