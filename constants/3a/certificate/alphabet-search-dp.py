"""Sketch: alphabet-search-dp  (constant 3a, LOWER bound)

TARGET (top-level claim):
    There exist a finite digit alphabet A (0 in A), digit count d, global sum cap T, with
    carry-free base b = 2*max(A)+1, such that the exactly-counted set
        U = { sum_i a_i b^i : a_i in A, sum a_i <= T }
    satisfies
        1 + log(|U-U| / |U+U|) / log(2*max(U)+1)  >  1.1740744.
    By the GHR2007 single-set lemma this is a valid lower bound on C_3a, strictly beating
    the record [G2026] = 1.1740744.

STRATEGY:
    Griego beat Zheng's uniform-digit limit (1.173077) by ONE alphabet tweak
    ({0..10} minus {1}, base 21, d=80, T=150) -> 1.17407444769.  The alphabet space is large and
    barely explored.  Re-optimize (A, d, T) using the SAME validated exact-integer DP
    (certificate/ghr_dp.py, already reproduces the record exactly), then certify the winner
    with a directed-rounded rational log bound.

HOLES:
  (H1) SEARCH: find a triple (A, d, T) with ghr_dp float-theta strictly above the record.
       Candidate moves (cheap float DP, then exact confirm):
         - omit different / multiple small digits ({0,3,4,..,M}, {0,2,3,..,M} minus {k}, ...);
         - vary max digit M (-> base 2M+1) and T/d ratio around Griego's T/d = 150/80;
         - longer d at matched T/d (asymptotics sharpen).
  (H2) EXACT CONFIRM: recompute |U+U|, |U-U|, max(U) as exact ints (ghr_dp) for the winner.
  (H3) CERTIFY: rational lower bound on log(|U-U|/|U+U|) - 0.1740744*log(2max U+1) > 0 with
       directed rounding (atanh series + explicit remainder, as in Griego's certificate).
       This is the load-bearing rigor step; deliver as a re-runnable margin.

Running this file now: validates the engine on the record, then STOPS at the search hole.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from ghr_dp import sumset_size, diffset_size, max_U, theta_floatbound, carry_free_base  # noqa

RECORD = 1.1740744


def sanity_record():
    A = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    th, s, diff, q = theta_floatbound(A, 80, 150)
    print(f"[engine check] record alphabet -> theta={th:.17f}  (must be ~1.17407444769)")
    assert abs(th - 1.17407444769352116) < 1e-12
    return th


def search_for_better():
    """HOLE H1: search alphabet/cap/length space for a triple beating the record.

    Returns (A, d, T) with float-theta > RECORD.  The search is cheap (DP is seconds to a
    couple minutes per point); the HARD part is finding the right neighborhood, not running
    the DP.  Implement: a structured sweep over (which small digits to omit, max digit M,
    T/d ratio, d), shortlisting on theta_floatbound, then exact-confirming the top few.
    """
    raise NotImplementedError("H1: alphabet/cap/length search not yet implemented")


def exact_confirm(A, d, T):
    """HOLE H2: exact integer recomputation of the three counts for the winning triple."""
    s = sumset_size(A, d, T)
    diff = diffset_size(A, d, T)
    q = 2 * max_U(A, d, T) + 1
    return s, diff, q


def certify_rational(s, diff, q):
    """HOLE H3: directed-rounded rational certificate that
       log(diff/s) - RECORD*log(q) > 0, i.e. theta > 1.1740744, with a re-runnable margin.
    """
    raise NotImplementedError("H3: rational directed-rounded log certificate not implemented")


if __name__ == "__main__":
    sanity_record()
    try:
        A, d, T = search_for_better()
        s, diff, q = exact_confirm(A, d, T)
        margin = certify_rational(s, diff, q)
        print(f"WINNER A={A} d={d} T={T}  certified margin={margin}")
    except NotImplementedError as e:
        print(f"[hole] {e}")
