"""
Sketch E  --  musin-edge-edit  (constant 28a, 63 -> 62)   [NEW, round 2]

ATTACK LINE A (explorer round-2 §6): Musin 2025 (arXiv:2511.03668) reformulation.
For a two-distance set with min-distance graph G on n vertices:

    dim_E2(G) = n - mu(G) - 1        (mu = multiplicity of the smallest root t>1
                                      of the Cayley-Menger polynomial C_G(t))
    B(S)      = theta(G)             (Borsuk number = clique COVER number)

  => G is a Borsuk counterexample  iff  theta(G) + mu(G) > n.

This is STRICTLY MORE GENERAL than Bondarenko's SRG criterion ceil(v/omega)>f+1,
and -- crucially -- it gives a *generative* search method that lives OUTSIDE
G_2(4), so it evades the named Gri2026 codim wall (the 320 C-points span exactly
63 dims, no spare direction). We do NOT drop a dimension inside G_2(4); we BUILD a
graph whose embedding dimension is <=62 by construction.

THE TARGET in mu/theta language (Musin digest, derived):
  cap-5 cliques => theta(G) >= ceil(n/5).  Want embedding dim n-mu-1 <= 62, i.e.
  mu >= n-63, AND theta + mu > n.  With a balanced clique partition into m cliques
  of size <=5: theta = m (when the minimal clique partition IS that partition and
  omega<=5).  Fire condition: m + mu > n with n-mu-1 <= 62  <=>  m >= 64  (>= 316
  vertices in <=64 cliques of <=5) AND mu = n-63 (embedding dim exactly 62).

THE STRATEGY (Musin section 3.2, Einhorn-Schoenberg):
  (i)  mu(G)=0  iff  G is a disjoint union of cliques (embedding dim n-1).
  (ii) each edge added/removed BETWEEN cliques can RAISE mu.
  So: fix a balanced skeleton C0 = m disjoint cliques of size <=5 (m>=64, n>=316),
  then HILL-CLIMB on inter-clique edge-flips to maximize mu(G), subject to keeping
  the minimal clique partition = C0 (preserve omega<=5 AND theta=m).  A winner is
  any G reaching mu >= n-63 while theta stays = m >= 64.

WHY THIS IS A DIFFERENT LEVER (explorer): R1 sought a single integer orthogonal
vector inside a fixed graph (rank-1 drop). mu is a *multiplicity* -- edge-editing
raises it in bulk. Cardinality headroom is huge (c2(62)=1953 >> 316), so dense
cap-5 graphs at dim 62 are not ruled out by any counting bound.

LEAN-FIT of a winner: (1) clique partition into m cliques of size<=5 (finite) =>
theta<=m and the part-cap; (2) omega(G)<=5 by exact bitset search (g24.max_clique_le)
=> theta>=ceil(n/5)>=64 for cap-5; (3) mu(G) = multiplicity of an integer/rational
root of the Cayley-Menger polynomial => embedding dim is an EXACT rank fact.  All
finite/discrete/algebraic, same certification core as the g24 scaffold.

HARD STEP (the load-bearing hole): maximize_mu_over_edge_flips -- find a cap-5,
theta=m>=64 graph with mu = n-63.  Whether the edge-flip landscape on a balanced
cap-5 skeleton even REACHES mu=n-63 is the open question (it may plateau below).
"""

import numpy as np
import math
import sys, os
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib
_g24 = importlib.import_module("g24")


# ---------------------------------------------------------------------------
# The Cayley-Menger / embedding-dimension machinery (the certifiable core).
# For a two-distance graph G with distances 1 (edge) and b>1 (non-edge), the
# Euclidean representability and embedding dimension are governed by the matrix
# M(t) = (entries 1 on edges, t=b^2 on non-edges, 0 diagonal) via the rank of
# the bordered Cayley-Menger matrix.  dim_E2(G) = n - mu - 1 where mu is the
# multiplicity of the smallest feasible root t>1.
# This helper computes embedding dim of a CONCRETE two-distance realization once
# the distance value t is fixed -- exact rational rank, Lean-fit.
# ---------------------------------------------------------------------------

def embedding_dim_two_distance(A, t):
    """
    Given adjacency A (edge = distance^2 = 1) and a non-edge squared distance t
    (a Fraction), build the squared-distance matrix D (D_ij = 0, 1 on edges,
    t on non-edges) and return the affine embedding dimension via the rank of
    the Cayley-Menger / centered Gram matrix, computed EXACTLY over Q.

    Affine embedding dim = rank of the centered matrix  -1/2 * J_c D J_c
    (Schoenberg).  Equals n-1-mu when t is the critical root.  This is the
    exact rank fact a Lean proof certifies.
    """
    n = A.shape[0]
    # squared-distance matrix as Fractions
    D = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                D[i][j] = Fraction(0)
            elif A[i, j]:
                D[i][j] = Fraction(1)
            else:
                D[i][j] = Fraction(t)
    # centered Gram B = -1/2 J_c D J_c, J_c = I - (1/n) ee^T
    # B_ij = -1/2 ( D_ij - row_i - col_j + total )
    rowmean = [sum(D[i]) / n for i in range(n)]
    total = sum(rowmean) / n
    B = [[-(Fraction(1, 2)) * (D[i][j] - rowmean[i] - rowmean[j] + total)
          for j in range(n)] for i in range(n)]
    return _exact_rank(B)


def _exact_rank(M):
    """Fraction-free / exact Gaussian elimination rank over Q."""
    m = [row[:] for row in M]
    rows = len(m)
    cols = len(m[0]) if rows else 0
    rank = 0
    pr = 0
    for c in range(cols):
        piv = None
        for r in range(pr, rows):
            if m[r][c] != 0:
                piv = r
                break
        if piv is None:
            continue
        m[pr], m[piv] = m[piv], m[pr]
        inv = m[pr][c]
        for r in range(rows):
            if r != pr and m[r][c] != 0:
                f = m[r][c] / inv
                m[r] = [m[r][k] - f * m[pr][k] for k in range(cols)]
        pr += 1
        rank += 1
        if pr == rows:
            break
    return rank


# ---------------------------------------------------------------------------
# The holes.
# ---------------------------------------------------------------------------

def build_balanced_skeleton(m=64, clique_size=5):
    """
    HOLE 1 (scaffold): build the balanced clique skeleton C0 = m disjoint cliques
    of size `clique_size` (so n = m*clique_size >= 316 when m>=64,size=5).  This
    is a disjoint union of K_5's -- mu(G)=0, embedding dim n-1 (Einhorn-Schoenberg
    fact (i)).  Returns adjacency A0 (n x n) and the partition (list of cliques).

    This part is trivial and certifiable directly; the WORK is editing it.
    """
    n = m * clique_size
    A0 = np.zeros((n, n), dtype=np.int64)
    partition = []
    for c in range(m):
        idx = list(range(c * clique_size, (c + 1) * clique_size))
        partition.append(idx)
        for i in idx:
            for j in idx:
                if i != j:
                    A0[i, j] = 1
    return A0, partition


def maximize_mu_over_edge_flips(A0, partition, target_dim=62):
    """
    HOLE 2 (LOAD-BEARING): starting from the disjoint-clique skeleton A0, add/remove
    edges BETWEEN cliques to MAXIMIZE mu(G), subject to:
       - the minimal clique partition of G stays = `partition` (so theta = m, and
         omega(G) <= clique_size = 5),
       - G remains two-distance-representable (Einhorn-Schoenberg conditions),
    until embedding dim n-mu-1 <= target_dim (i.e. mu >= n-1-target_dim).

    Whenever theta(G) + mu(G) > n we have a counterexample in dim n-mu-1.
    For cap-5, theta = m = n/5; need n - mu - 1 <= 62  <=>  mu >= n-63, AND
    m >= 64.  Returns the edited adjacency A (and the critical distance t).

    THE OPEN QUESTION: does the inter-clique edge-flip landscape on a balanced
    cap-5 skeleton ever REACH mu = n-63 while keeping the minimal clique partition
    fixed?  This is a finite discrete optimization (hill-climb / SAT / ML over the
    edge-flip space).  Plan:
      (a) implement a single-flip delta-mu evaluator (recompute embedding dim via
          embedding_dim_two_distance at the critical t after each candidate flip),
      (b) greedy / simulated-annealing hill-climb raising mu,
      (c) keep only flips that preserve omega<=5 (g24.max_clique_le) and the
          minimal clique partition (so theta stays m).
    """
    raise NotImplementedError(
        "maximize_mu_over_edge_flips: edit a balanced cap-5 skeleton to reach "
        "embedding dim <=62 (mu>=n-63) with theta=m>=64.  Finite edge-flip search."
    )


def verify(A, t, partition):
    """
    CERTIFY (Lean-fit core).  Given the edited two-distance graph A, critical
    squared-distance t, and a clique partition, check:
       (1) omega(G) <= 5            (exact bitset, g24.max_clique_le)
       (2) the partition is a valid clique partition into m cliques of size<=5,
           so theta <= m and >= ceil(n/5)  =>  theta = m if m = ceil(n/5)
       (3) embedding dim = n - mu - 1 = embedding_dim_two_distance(A, t) <= 62
       (4) m + mu > n   <=>   ceil(n/5) > 62+1 = 63   <=>   m >= 64
    is_counterexample iff all hold.
    """
    n = A.shape[0]
    m = len(partition)
    # (2) partition validity: each block a clique of size<=5, blocks cover V
    covered = set()
    ok_part = True
    for blk in partition:
        if len(blk) > 5:
            ok_part = False
        for i in blk:
            for j in blk:
                if i != j and not A[i, j]:
                    ok_part = False
        covered |= set(blk)
    ok_part = ok_part and (covered == set(range(n)))
    omega_le_5 = _g24.max_clique_le(A, 5)
    emb = embedding_dim_two_distance(A, t)
    theta_eq_m = ok_part and (m == math.ceil(n / 5))
    fire = theta_eq_m and (m + (n - emb - 1) > n)  # theta + mu > n
    return dict(n=n, m=m, omega_le_5=omega_le_5, embedding_dim=emb,
                theta_eq_m=theta_eq_m,
                is_counterexample=(omega_le_5 and emb <= 62 and m >= 64
                                   and ok_part and fire))


if __name__ == "__main__":
    print("musin-edge-edit (sketch E): balanced cap-5 clique skeleton, edge-flip")
    print("to maximize mu, fire when theta+mu>n with embedding dim <=62.")
    # The scaffold + the exact embedding-dim machinery RUN green; the hole raises.
    A0, part = build_balanced_skeleton(m=64, clique_size=5)
    n = A0.shape[0]
    print(f"skeleton: n={n}, m={len(part)} cliques of 5, theta=ceil(n/5)={math.ceil(n/5)}")
    # disjoint union of K5: mu=0, embedding dim = n-1 (sanity of the exact core)
    emb0 = embedding_dim_two_distance(A0, Fraction(2))  # any t>1 for disjoint cliques
    print(f"disjoint-K5 embedding dim (should be n-1={n-1} since mu=0): {emb0}")
    assert _g24.max_clique_le(A0, 5), "skeleton omega must be 5"
    print("scaffold + exact embedding-dim machinery: OK")
    try:
        maximize_mu_over_edge_flips(A0, part)
    except NotImplementedError as e:
        print("HOLE pending:", e)
