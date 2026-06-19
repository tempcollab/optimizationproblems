#!/usr/bin/env python3
"""
Sketch: bona-forbidden-factor-upper
Target (UPPER bound): gr(Av(1324)) < 13.5   [beats BBEPP2017 record 13.5]

Strategy (explorer angle A2, Lean-fit):
  Bona's (w,z) word-pair coloring (B14a/B14b) injects Av_n(1324) into pairs of
  length-n words over {A,B,C,D} satisfying local forbidden factors (no CB-factor;
  CAB^k => k B's in the z-segment). The admissible count has an EXPLICIT RATIONAL
  generating function; its smallest-modulus denominator root alpha gives
  beta = 1/alpha and L(1324) <= beta^2. Known: CB only -> 13.7595; +CAB^2 -> 13.73977.
  The method SATURATES ~13.7 with the local factors used so far.

  Plan: add ONE more certified forbidden factor (a local consequence of
  1324-avoidance beyond CB / CAB^k that Bona did not use), recompute the rational
  GF root, and drive beta^2 below 13.5.

Load-bearing HARD step (H1): find a NEW forbidden factor in the (w,z) image that
(a) is provably forced by 1324-avoidance and (b) when added, drops the rational-GF
root enough to cross from ~13.7 to <13.5 -- a 0.24 gap. This is precisely where
Bona stalled (local factors saturate); capturing more *global* structure while
staying a regular/rational language is the risk. Honest: 13.7 -> 13.5 is a large
ask for one local factor; may need several or a structural insight. Multi-round.

HOLES:
  H1  new_forbidden_factor(): the additional certified local constraint on (w,z).
  H2  admissible_gf(): the rational GF of word-pairs satisfying {CB, CAB^k, H1}.
  H3  smallest_root_bound(): certified lower bound on |alpha| (smallest-modulus
      root of the GF denominator) via Sturm/interval arithmetic on an integer
      polynomial -> beta = 1/alpha, bound = beta^2.

Lean-fit: HIGH. Root-of-integer-polynomial bound is a finite Sturm certificate;
the forbidden-factor injection is a finite word argument.
"""
from fractions import Fraction


RECORD_UPPER = 13.5  # BBEPP2017 verified upper bound to strictly beat


def new_forbidden_factor():
    """HOLE H1: new certified forbidden factor in Bona's (w,z) encoding."""
    raise NotImplementedError("H1: new forbidden factor forced by 1324-avoidance")


def admissible_gf():
    """HOLE H2: rational GF of (w,z) word-pairs satisfying all forbidden factors.

    Return the integer-coefficient denominator polynomial P(x); beta = 1/alpha
    where alpha = smallest-modulus real root of P, and L(1324) <= beta^2.
    """
    raise NotImplementedError("H2: rational GF / denominator polynomial")


def smallest_root_bound():
    """HOLE H3: certified lower bound on |alpha| -> beta^2 < 13.5 via Sturm."""
    raise NotImplementedError("H3: Sturm/interval root bound -> beta^2")


def upper_bound():
    new_forbidden_factor()      # H1
    admissible_gf()             # H2
    bound = smallest_root_bound()  # H3 (Fraction or float, must be < 13.5)
    assert bound < RECORD_UPPER, f"bound {float(bound)} does not beat {RECORD_UPPER}"
    print(f"CERTIFIED gr(Av(1324)) <= {float(bound)} < {RECORD_UPPER}")
    return bound


if __name__ == "__main__":
    upper_bound()
