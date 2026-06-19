"""
Sketch B  --  gri-augment  (constant 28a, 63 -> 62)

ATTACK LINE B (explorer): Gri2026 added ONE projected point p = t*z_b to the
320-point C-set (already in the 63-dim subspace W), reaching ceil(321/5)=65.
We push further: engineer a set of >=316 points that ALSO admits a 4th
orthogonal direction, dropping to 62 dims while keeping max smaller-diameter
part (clique) <= 5.

Two sub-strategies inside W (dim 63):

(B1) DROP-IN-W. Inside the already-63-dim W, can we find a 62-dim subspace W'
     of W containing >= 316 of the points {x_c : c in C} (or C minus a few plus
     a couple of Gri-type projected points)? Equivalent: a vector r in W with
     x_c . r = 0 for >= 316 indices c. The explorer says no hyperplane holds
     more than a handful of C-points -- so this needs ADDED points engineered
     to lie in a common hyperplane of W with the retained C-points.

(B2) REPLACE-AND-DROP. Remove a small cluster C0 of C-points whose removal frees
     an orthogonal direction (their removal lowers the rank by 1), keeping
     |C \ C0| >= 316 only if |C0| <= 4 -- but C is general-position so removing
     4 points cannot drop the rank. Instead remove a structured ~k-point cluster
     and ADD back >= |C0| projected points that DO share a hyperplane. Net: stay
     >= 316, gain one codim, keep omega <= 5.

The clique cap is a FINITE recomputation on the augmented graph (Lean-fit), so
the only open part is producing the points + the common 62-dim subspace.
"""

import numpy as np
import math
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib
_g24 = importlib.import_module("g24")


def gri_W_and_Cpoints():
    """
    HOLE 1 (scaffold): build G_2(4), integer Gram, C-points {x_c} and the 63-dim
    subspace W = span(S1,S2,S3)^perp. Mirrors Gri Lemmas 1-3 (verified facts).
    Returns (A, X_C, W_basis, C_idx, B_parts, S_vectors).
    """
    A, verts = _g24.build_g24()
    raise NotImplementedError(
        "gri_W_and_Cpoints: build_g24 + W (dim 63) + C-points. Gri Lemmas 1-3."
    )


def projected_point(X, b_idx, S1, t):
    """
    Gri's construction of one added point in W: z_b = x_b - (1/32) S1,
    p = t * z_b, with t the positive root of 78 t^2 + 12 t = 102.
    Generalizable: different b in B1 (or B2,B3) give different z_b, all in W.
    """
    z_b = X[b_idx] - S1 / 32.0
    return t * z_b


def engineer_augment_in_codim1(A, X_C, W_basis, C_idx, S_vectors):
    """
    HOLE 2 (the load-bearing hole): produce a set P of added points (Gri-type
    projected points, or other points of W) and a subset C' of C such that
       P union {x_c : c in C'}  has >= 316 points,
       lies in a common 62-dim subspace of W (rank <= 62),
       and the induced diameter graph has clique number <= 5.

    The crux: the >=316 retained/added points must share a hyperplane of W.
    Since C is general-position, the added points must SUPPLY the codimension --
    i.e. choose r in W (the 4th orthogonal vector), keep only the C-points with
    x_c . r = 0 (a handful), and fill the rest to 316 with engineered points on
    {y : y . r = 0}. Feasibility unknown: too few C-points lie on any hyperplane,
    so the engineered points would have to number ~300 and individually preserve
    omega <= 5 -- a hard packing problem. State it, test small.
    """
    raise NotImplementedError(
        "engineer_augment_in_codim1: build >=316 points in a 62-dim subspace of W "
        "with omega <= 5. Sketch B's hard step."
    )


def verify(A_aug, X_aug):
    """
    CERTIFY (Lean-fit): recompute the diameter graph of the augmented point set,
    check (1) embedding dim <= 62, (2) max smaller-diameter clique <= 5,
    (3) ceil(n/5) >= 64. Clique recomputation uses g24.max_clique_le on the
    *augmented* diameter graph (added points create new edges -- must re-derive).
    """
    dim = _g24.subspace_dim(X_aug)
    n = X_aug.shape[0]
    # diameter graph: vertices at strictly-less-than-max distance are adjacent
    G = _build_diameter_graph(X_aug)
    omega_le_5 = _g24.max_clique_le(G, 5)
    parts = math.ceil(n / 5)
    return dict(dim=dim, omega_le_5=omega_le_5, n=n, parts_needed=parts,
                is_counterexample=(dim <= 62 and omega_le_5 and parts >= 64))


def _build_diameter_graph(X, tol=1e-6):
    """Adjacency: i~j iff ||xi-xj||^2 < max pairwise squared distance."""
    D = np.add.outer((X * X).sum(1), (X * X).sum(1)) - 2 * X @ X.T
    dmax = D.max()
    A = ((D < dmax - tol) & (D > tol)).astype(np.int64)
    return A


if __name__ == "__main__":
    print("gri-augment (sketch B): augment Gri's 63-dim W-set to >=316 pts in a")
    print("62-dim subspace, omega <= 5.  Hard step: engineer_augment_in_codim1.")
    try:
        gri_W_and_Cpoints()
    except NotImplementedError as e:
        print("HOLE pending:", e)
