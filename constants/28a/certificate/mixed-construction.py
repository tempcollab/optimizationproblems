"""
Sketch D  --  mixed-construction  (constant 28a, 63 -> 62)

ATTACK LINE D (explorer): Gri's final set is NOT two-distance (the added p gives
a third distance 192 - 48t). The door is open to sets that are two-distance on a
clique-cover-5 CORE plus a few controlled extra points, engineered into 62 dims.

GENERAL FRAME. A Borsuk counterexample in R^62 needs a finite point set X, |X|>=316
(if max smaller-diameter part is 5) -- but the part-size cap need NOT come from a
single SRG clique number. We allow:
  - a CORE K of two-distance points whose smaller-diameter subsets are cliques of
    an SRG (cap c_K),
  - a PERTURBATION set P (general points) chosen so that every smaller-diameter
    subset of X = K u P still has size <= 5,
  - all of X inside a 62-dim subspace.
The cap-5 condition becomes: the DIAMETER GRAPH of X has clique number <= 5 (a
finite recomputation), and ceil(|X|/5) >= 64.

This relaxes the rigid "single SRG" requirement: P can break two-distance and yet
keep the clique cap, exactly as Gri's one point did, but now used to BUY a
dimension rather than a point. The freedom is choosing K (a sub-SRG with cap <=5
in <=62 dims is impossible alone -- that's lines A/B) so K should be a LOWER-dim
core (e.g. a sub-configuration genuinely in <=62 dims even if |K| < 316) and P
fills the count while staying cap-5 and in the same 62-dim subspace.

CANDIDATE CORES to try (each a HOLE to instantiate):
  - K = a 62-dim two-distance sub-configuration of a SMALLER SRG (from srg-sweep),
    cap c_K, |K| possibly < 316; P engineered to reach 316.
  - K = Gri's 63-dim set intersected with a 62-dim subspace (keeps the C-points on
    a hyperplane, a handful) + many perturbation points.
  - K = a tensor/section construction (Bondarenko's product corollaries) trimmed
    to 62 dims.
"""

import numpy as np
import math
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib
_g24 = importlib.import_module("g24")


def build_core():
    """
    HOLE 1: instantiate a core two-distance configuration K in a 62-dim subspace
    (from srg-sweep survivors, or a trimmed G_2(4) section). Returns X_core (m x f),
    f <= 62, plus its diameter graph.
    """
    raise NotImplementedError(
        "build_core: a <=62-dim two-distance core. Depends on srg-sweep output."
    )


def engineer_perturbation(X_core, target_n=316):
    """
    HOLE 2 (load-bearing): add perturbation points P (NOT necessarily two-distance)
    so that X = core u P satisfies:
       |X| >= target_n,
       X lies in a common 62-dim subspace,
       diameter-graph clique number of X <= 5.
    Mirrors Gri's single non-two-distance point, scaled up to buy a dimension.
    The hard part: each added point creates new diameter-graph edges; keeping the
    clique number capped at 5 while reaching 316 points in 62 dims is the open
    construction. Model as a constrained packing / SAT-style search.
    """
    raise NotImplementedError(
        "engineer_perturbation: reach >=316 pts in 62 dims with diameter-clique <=5."
    )


def verify(X):
    """
    CERTIFY (Lean-fit core): build the diameter graph of X, check
      (1) dim span(X) <= 62,
      (2) clique number of diameter graph <= 5  (g24.max_clique_le),
      (3) ceil(|X|/5) >= 64.
    Because X is NOT two-distance, the clique = smaller-diameter equivalence must
    be re-derived from the actual pairwise distances (handled by building the
    diameter graph directly), then the clique bound certifies the part count.
    """
    dim = _g24.subspace_dim(X)
    G = _diameter_graph(X)
    omega_le_5 = _g24.max_clique_le(G, 5)
    n = X.shape[0]
    parts = math.ceil(n / 5)
    return dict(dim=dim, omega_le_5=omega_le_5, n=n, parts_needed=parts,
                is_counterexample=(dim <= 62 and omega_le_5 and parts >= 64))


def _diameter_graph(X, tol=1e-6):
    D = np.add.outer((X * X).sum(1), (X * X).sum(1)) - 2 * X @ X.T
    dmax = D.max()
    return ((D < dmax - tol) & (D > tol)).astype(np.int64)


if __name__ == "__main__":
    print("mixed-construction (sketch D): two-distance core in <=62 dims + cap-5")
    print("perturbation to reach 316 pts.  Hard step: engineer_perturbation.")
    try:
        build_core()
    except NotImplementedError as e:
        print("HOLE pending:", e)
