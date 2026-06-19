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

R3 REVISION (re-plan of the load-bearing hole H3, + a new soundness-audit hole H0).
====================================================================================
The R3 explorer flagged a SOUNDNESS SUBTLETY that must be pinned before the
"diagonal n=k ALONE => unconditional 10.418" reduction can be claimed:

  The number 10.418 is the spectral radius of the weighted quotient graph computed
  at a FINITE CUTOFF n=220 (Walks2025 Cor 9). That finite-cutoff CW value is a sound
  lower bound only if the weighted walk counts it consumes are <= the true counts --
  i.e. one needs W~_{N,k} <= W_{N,k} for exactly the (N,k) pairs the n=220 witness
  ranges over, NOT merely the limiting diagonal n=k. Walks2025's wording "the
  corollary only needs the case n=k" is about the LIMIT; the finite computation that
  produces the number is what must be audited.  => NEW HOLE H0.

CONCRETE H3 MECHANISM (the explorer asked the outliner to supply one, not restate the
conjecture).  Per-walk WEIGHT-DECONSTRUCTION injection on the diagonal:
  A weighted diagonal walk's contribution is prod_e (E(e)/|A(source(e))|), where E(e)
  = #ungrouped edges from the source GROUP to the target GROUP. Expand the product over
  the walk: numerator = prod_e E(e) = the number of ways to choose, at each step, an
  ungrouped edge realising the group-to-group transition; denominator = prod_e
  |A(source(e))|. A true diagonal walk of weight W_{n,n} is a sequence of ungrouped
  vertices. Plan: build an injection from the numerator's "edge-choice sequences"
  (telescoping the denominators against the next group's size via the diagonal
  constraint n=k that ties |A(source)| to the realised vertex multiplicity) into true
  ungrouped walks, so the averaged product is dominated term-by-term. The diagonal
  constraint is load-bearing: it is what makes the telescoping cancel (off-diagonal it
  does not, which is why the full conjecture is harder).  This is a SPECIFIC injection
  to verify/refute at small n, not a flavour.

HOLES:
  H0 (NEW, soundness gate) audit_finite_cutoff_window(): enumerate EXACTLY which (N,k)
      weighted-vs-true inequalities the n=220 CW witness consumes. If they are all on
      the diagonal N=k, the diagonal proof (H3) suffices; if not, either H3 must be
      strengthened to cover them or the cutoff must be re-chosen. THIS GATES the whole
      reduction -- without it "diagonal => 10.418" is itself a hole.
  H1  weighted_walk_sum(n, k):  W~_{n,k}, the rational weighted walk-sum over the A(n,r)
      quotient graph (exact -- reproduce Walks2025's average-weight construction).
  H2  true_walk_count(n, k):    W_{n,k}, the TRUE integer count of length-n insertion
      walks with k short values (= 1324-avoiders with that statistic; brute/transfer).
  H3  prove_diagonal_domination(): the LOAD-BEARING hole. Prove W~_{n,n} <= W_{n,n} for
      ALL n (the diagonal case of Conjecture 8) via the weight-deconstruction injection
      above (term-by-term out-degree domination with diagonal telescoping) -- NOT just a
      finite check. Validate the injection at small n first (H3-base), then generalise.
  H4  assemble_unconditional_10418(): given H0 + H3, restate Walks2025 Cor 9's n=220
      rational CW value as an UNCONDITIONAL bound 10.418 and re-verify that witness.
"""
from fractions import Fraction

RECORD_LOWER = Fraction(10271, 1000)   # BBEPP2017 verified lower bound to strictly beat
TARGET = Fraction(10418, 1000)         # Walks2025 Cor 9 value, currently conditional


def audit_finite_cutoff_window():
    """HOLE H0 (NEW, soundness gate): enumerate EXACTLY which (N,k) weighted-vs-true
    inequalities W~_{N,k} <= W_{N,k} the Walks2025 n=220 CW witness actually consumes.

    The CW criterion Sum_{e: g->h} Q[g,h] w_h >= rho w_g is checked over the quotient
    graph truncated at size 220; the consumed inequalities are those edges' average
    weights. Determine whether they all lie on the diagonal N=k (so H3 suffices) or
    spill off-diagonal (so H3 must be extended / the cutoff re-chosen). MUST be settled
    before claiming 'diagonal => unconditional 10.418'."""
    raise NotImplementedError(
        "H0: audit which (N,k) inequalities the n=220 CW witness consumes "
        "(diagonal-only? off-diagonal spill?). Soundness gate for the reduction."
    )


def weighted_walk_sum(n, k):
    """HOLE H1: rational weighted walk-sum W~_{n,k} over the A(n,r) quotient graph."""
    raise NotImplementedError("H1: weighted walk-sum W~_{n,k} (average-weight quotient)")


def true_walk_count(n, k):
    """HOLE H2: TRUE integer count W_{n,k} of length-n insertion walks with k short values."""
    raise NotImplementedError("H2: true walk count W_{n,k}")


def prove_diagonal_domination():
    """HOLE H3 (LOAD-BEARING): prove W~_{n,n} <= W_{n,n} for ALL n (diagonal Conjecture 8).

    MECHANISM (R3 -- weight-deconstruction injection, see module docstring):
    expand the weighted diagonal walk's product prod_e E(e)/|A(source(e))|; the
    numerator counts ungrouped edge-choice sequences realising the group transitions,
    the denominator is prod_e |A(source(e))|. On the DIAGONAL n=k the group sizes
    telescope against the next step's edge multiplicity, giving a term-by-term
    domination -> an injection of weighted edge-choice sequences into true ungrouped
    walks. Validate the injection at small n (H3-base) before generalising.
    Walks2025 verified n<=50 numerically -- that is the sanity base, not the proof.
    """
    raise NotImplementedError(
        "H3: structural proof of diagonal W~_{n,n} <= W_{n,n} via weight-deconstruction "
        "injection with diagonal telescoping (validate at small n, then generalise)."
    )


def assemble_unconditional_10418():
    """HOLE H4: given H3, restate Walks2025 Cor 9's n=220 rational CW value 10.418 as an
    UNCONDITIONAL lower bound and re-verify the rational Collatz-Wielandt witness exactly."""
    raise NotImplementedError("H4: re-verify n=220 rational CW witness -> unconditional 10.418")


def lower_bound():
    audit_finite_cutoff_window()        # H0 -- soundness gate (must precede the rest)
    _ = weighted_walk_sum(1, 1)         # H1
    _ = true_walk_count(1, 1)           # H2
    assert prove_diagonal_domination()  # H3 -- the load-bearing soundness step
    lam = assemble_unconditional_10418()  # H4
    assert lam > RECORD_LOWER, f"{float(lam)} does not beat {float(RECORD_LOWER)}"
    print(f"CERTIFIED (unconditional, via diagonal Conjecture 8): "
          f"gr(Av(1324)) >= {lam} = {float(lam):.6f} > {float(RECORD_LOWER)}")
    return lam


if __name__ == "__main__":
    print("conjecture8-diagonal-lower -- skeleton (holes raise as designed)")
    print(f"  target {float(TARGET):.6f} > record {float(RECORD_LOWER):.6f}")
    print("  H0 (soundness gate): audit which (N,k) the n=220 CW witness consumes")
    print("  H3 (load-bearing): diagonal W~ <= W via weight-deconstruction injection")
    try:
        lower_bound()
    except NotImplementedError as e:
        print(f"\n[load-bearing hole raises, as expected]  {e}")
