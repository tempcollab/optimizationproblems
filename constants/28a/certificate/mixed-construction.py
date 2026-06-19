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
    HOLE 1 (REVISED, round 2): instantiate a <=62-dim core configuration K.

    R1 PLAN (DEAD): "from a srg-sweep survivor" -- srg-sweep is now a CLOSED
    negative (0 of 564 feasible rows certify dim<=62), so the core can NOT come
    from a smaller-SRG survivor.  Re-planned core sources, in priority order:

      (a) A G_2(4) SECTION that already sits in <=62 dims by exact rank.  The C
          orbit spans exactly 63 (Gri wall), but a *sub-orbit* / hyperplane
          section of C (or of C u B1) of size m can have exact rank <=62 -- e.g.
          intersect the 320 C-points with a 62-dim coordinate window so the
          surviving K is genuinely two-distance in 62 dims (cap_dim ledger in
          fresh-orthogonal-dir.py gives the exact surviving rank for a window).
          This EVADES the wall differently from lines A/B: we do NOT need K to
          reach 316 -- only to be a <=62-dim two-distance seed.  |K| may be ~200.

      (b) A 3-DISTANCE core via Musin section 3.3 (s-distance theorem, digest
          literature/musin2025.md): color E(K_n) with s colors, B(L) governed by
          theta(Gbar_1) > dim_E2(L)+1.  Gri's record set is ALREADY 3-distance,
          so a 3-distance K with a small clique-cover-1 color and a low-rank
          realization is a legitimate <=62-dim core.  Returns the realization
          plus the partition by the min-distance color.

    Returns (X_core (m x f) with f<=62, diameter graph of K).  This hole only
    needs a CORRECT <=62-dim seed; the count is line D's perturbation hole.
    """
    raise NotImplementedError(
        "build_core (revised): a <=62-dim core -- either a G_2(4) hyperplane "
        "section of C/CuB1 with exact surviving rank <=62 (NOT a srg-sweep "
        "survivor -- that line is closed), or a 3-distance Musin-3.3 core."
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
