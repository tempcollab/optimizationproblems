#!/usr/bin/env python3
"""
Sketch: cjs-increasing-columns-upper
Target (UPPER bound): gr(Av(1324)) <= e^{pi sqrt(2/3)} ~ 13.001954 < 13.5
                      [beats BBEPP2017 record 13.5]

Strategy (explorer angle D, Lean-fit if provable):
  Let S^k_n(1324) = #{1324-avoiders of length n with exactly k inversions}.
  CJS12 Conjecture 13 ("increasing columns"): for all n,k, S^k_n <= S^k_{n+1}.
  CJS12 Theorem 17: Conjecture 13 => L(1324) <= rho := e^{pi sqrt(2/3)} ~ 13.002.
  The 132-analogue (each inversion column is weakly increasing in n and
  eventually equals p(k), the partition count, with p(k) < rho^sqrt(k)) is PROVEN;
  the open part for 1324 is the approach to the (already identified) limit value.

  Plan: prove Conjecture 13 (or a usable weakening: monotonicity for k <= K(n)
  plus an independent tail bound on sum_{k>K} S^k_n) and combine with the
  classical partition asymptotic to get the unconditional bound <= 13.002.

Load-bearing HARD step (H1): the monotonicity S^k_n <= S^k_{n+1}. Open since 2012,
verified numerically on small triangles. A clean discrete statement -- candidate
for an injective/inductive proof (exhibit an injection from length-n k-inversion
1324-avoiders to length-(n+1) ones). Risk: it has resisted since 2012; but it is a
finite-combinatorial monotonicity, the right SHAPE for a machine-checkable proof,
and even a weakening may suffice.

HOLES:
  H1  increasing_columns(): injection Av^{k}_n(1324) -> Av^{k}_{n+1}(1324)
      witnessing S^k_n <= S^k_{n+1} (or the weakened bounded-k + tail version).
  H2  column_limit_bound(): the eventual column value is bounded by p(k)
      (CJS Prop 15 / Lemma 16 analogue), with p(k) < rho^sqrt(k).
  H3  partition_asymptotic(): p(k) < e^{pi sqrt(2k/3)} (classical Hardy-Ramanujan
      upper bound) -- citable / provable; sum over k <= C(n,2) gives growth <= rho.

Lean-fit: YES if H1 is an explicit injection. H2/H3 are discrete + a standard
partition bound. The whole argument is combinatorial/algebraic.
"""
import math


RECORD_UPPER = 13.5
RHO = math.exp(math.pi * math.sqrt(2.0 / 3.0))  # ~ 13.001954


def increasing_columns(n, k):
    """HOLE H1: witness S^k_n(1324) <= S^k_{n+1}(1324).

    Ideal form: an injective map from length-n 1324-avoiders with k inversions
    into length-(n+1) 1324-avoiders with k inversions. Return that map (or the
    weakened bounded-k statement + tail bound).
    """
    raise NotImplementedError("H1: increasing-columns monotonicity (CJS Conjecture 13)")


def column_limit_bound(k):
    """HOLE H2: eventual value of inversion column k bounded by p(k)."""
    raise NotImplementedError("H2: column-limit <= p(k)")


def partition_asymptotic(k):
    """HOLE H3: p(k) < e^{pi sqrt(2k/3)} (classical, citable)."""
    raise NotImplementedError("H3: Hardy-Ramanujan partition upper bound")


def upper_bound():
    increasing_columns(None, None)  # H1
    column_limit_bound(None)        # H2
    partition_asymptotic(None)      # H3
    bound = RHO
    assert bound < RECORD_UPPER, f"bound {bound} does not beat {RECORD_UPPER}"
    print(f"CERTIFIED gr(Av(1324)) <= {bound} < {RECORD_UPPER}")
    return bound


if __name__ == "__main__":
    upper_bound()
