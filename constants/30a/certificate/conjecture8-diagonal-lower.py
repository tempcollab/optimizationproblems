#!/usr/bin/env python3
"""
Sketch: conjecture8-diagonal-lower
Target (LOWER bound): gr(Av(1324)) >= 10.418 > 10.271   [beats BBEPP2017 record 10.271]

Strategy (explorer Angle B -- prove Walks2025 Conjecture 8, even just the diagonal):
  Walks2025 builds the WEIGHTED quotient of the insertion-encoding graph: states are
  grouped by A(n,r) = (size n, r = #short values = non-right-to-left maxima), and the
  edge A(n,r)->A(m,s) carries the AVERAGE out-degree weight E(n,r,m,s)/|A(n,r)|. A walk
  contributes the PRODUCT of its edge weights. Let
        W_{n,k}      = TRUE number of length-n insertion-encoding walks ending with k
                       short values (= a genuine count of 1324-avoiders, integer),
        W~_{n,k}     = the WEIGHTED walk-sum over the quotient graph (rational).
  Their Corollary 9: IF W~_{n,k} <= W_{n,k} for all n,k (Conjecture 8), then the weighted
  spectral radius is a SOUND lower bound, and the n=220 rational Collatz-Wielandt value
  gives gr(Av(1324)) >= 10.418 UNCONDITIONALLY. Corollary 9 needs only the DIAGONAL n=k.

  This sketch's job: discharge the soundness step W~ <= W. We do NOT re-run the n=220 CW
  computation from scratch (Walks2025 already certified the NUMBER 10.418 via a rational
  CW witness -- that part is sound and reproducible); we supply the missing inequality so
  the number becomes an unconditional bound.

  Why this is Lean-fit in SHAPE: W~ and W are both finite integer/rational walk counts;
  the inequality is a discrete monotonicity (an average out-degree, raised to a product
  over a walk, never exceeds the true product count). Same flavour as CJS Conjecture 13.

  Risk: this is the paper's stated OPEN problem. We attack the DIAGONAL n=k only (suffices
  for Cor 9), which Walks2025 verified to n=50 -- so an induction or a structural
  domination argument has a concrete finite base. Higher payoff (named 10.418), higher
  risk than Angle A's min-weighted quotient.

HOLES:
  H1  weighted_walk_sum(n, k):  W~_{n,k}, the rational weighted walk-sum over the A(n,r)
      quotient graph (exact -- reproduce Walks2025's average-weight construction).
  H2  true_walk_count(n, k):    W_{n,k}, the TRUE integer count of length-n insertion
      walks with k short values (= 1324-avoiders with that statistic; brute/transfer).
  H3  prove_diagonal_domination(): the LOAD-BEARING hole. Prove W~_{n,n} <= W_{n,n} for
      ALL n (the diagonal case of Conjecture 8) by a structural argument -- e.g. exhibit
      a per-walk injection or a term-by-term out-degree domination -- NOT just a finite
      check. A finite check (n <= some bound) is a SANITY test, not the proof.
  H4  assemble_unconditional_10418(): given H3, restate Walks2025 Cor 9's n=220 rational
      CW value as an UNCONDITIONAL lower bound 10.418 and re-verify that rational witness.
"""
from fractions import Fraction

RECORD_LOWER = Fraction(10271, 1000)   # BBEPP2017 verified lower bound to strictly beat
TARGET = Fraction(10418, 1000)         # Walks2025 Cor 9 value, currently conditional


def weighted_walk_sum(n, k):
    """HOLE H1: rational weighted walk-sum W~_{n,k} over the A(n,r) quotient graph."""
    raise NotImplementedError("H1: weighted walk-sum W~_{n,k} (average-weight quotient)")


def true_walk_count(n, k):
    """HOLE H2: TRUE integer count W_{n,k} of length-n insertion walks with k short values."""
    raise NotImplementedError("H2: true walk count W_{n,k}")


def prove_diagonal_domination():
    """HOLE H3 (LOAD-BEARING): prove W~_{n,n} <= W_{n,n} for ALL n (diagonal Conjecture 8).

    Structural argument required (not a finite check): a per-walk injection or a
    term-by-term domination showing the product of average out-degrees along any diagonal
    walk never exceeds the true diagonal walk count. Walks2025 verified n<=50; that is the
    base/sanity range, not the proof.
    """
    raise NotImplementedError("H3: structural proof of diagonal W~_{n,n} <= W_{n,n}")


def assemble_unconditional_10418():
    """HOLE H4: given H3, restate Walks2025 Cor 9's n=220 rational CW value 10.418 as an
    UNCONDITIONAL lower bound and re-verify the rational Collatz-Wielandt witness exactly."""
    raise NotImplementedError("H4: re-verify n=220 rational CW witness -> unconditional 10.418")


def lower_bound():
    # H1/H2: the two walk-count quantities whose ordering is the conjecture.
    _ = weighted_walk_sum(1, 1)         # H1
    _ = true_walk_count(1, 1)           # H2
    assert prove_diagonal_domination()  # H3 -- the load-bearing soundness step
    lam = assemble_unconditional_10418()  # H4
    assert lam > RECORD_LOWER, f"{float(lam)} does not beat {float(RECORD_LOWER)}"
    print(f"CERTIFIED (unconditional, via diagonal Conjecture 8): "
          f"gr(Av(1324)) >= {lam} = {float(lam):.6f} > {float(RECORD_LOWER)}")
    return lam


if __name__ == "__main__":
    lower_bound()
