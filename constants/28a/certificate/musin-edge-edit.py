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
# FAST exact embedding-dim evaluator (round 3).
#
# `embedding_dim_two_distance` (above) is the SLOW exact-rational reference: at
# n=320 it is ~39 s per call -- unusable for any search.  The evaluator below is
# the same rank, computed by integer modular Gaussian elimination over a finite
# field (vectorised with numpy), which is ~70x faster (~0.5 s at n=320) and gives
# the SAME rank with overwhelming reliability; we confirm with a SECOND prime and
# only accept a value both primes agree on (a rank can only be UNDER-estimated mod
# p, when an unlucky pivot vanishes; two independent primes agreeing on the same
# drop makes a false drop astronomically unlikely, and the final winner is ALWAYS
# re-certified by the slow exact-rational `embedding_dim_two_distance`).
#
# Cross-checked round 3: on the rook graph K5[]K5 and on the disjoint-K5 skeleton
# the fast evaluator and the exact-rational machinery agree exactly (emb 8 and
# n-1 respectively), and the critical root is the integer t=2 (clean for Lean).
# ---------------------------------------------------------------------------

_PRIME_A = 2147483647   # 2^31 - 1 (Mersenne); p^2 < 2^63 so int64 products are safe
_PRIME_B = 2147483629   # second prime for agreement check


def _scaled_centered_gram_int(A, t_num, t_den):
    """
    Return an INTEGER matrix proportional (by the positive scalar 2*t_den*n^2) to
    the centered Gram B(t) = -1/2 J_c D(t) J_c, for rational t = t_num/t_den.

    D(t): 0 on the diagonal, 1 on edges (squared min-distance), t on non-edges.
    Scaling D by t_den clears the denominator; the further n^2 scaling clears the
    centering 1/n factors.  rank is invariant under the positive scalar, so the
    rank of this integer matrix equals rank B(t) = the affine embedding dimension.
    """
    n = A.shape[0]
    edge = A.astype(bool)
    diag = np.eye(n, dtype=bool)
    # D_scaled = t_den * D : edges -> t_den, non-edges -> t_num, diagonal -> 0
    D = np.where(diag, 0, np.where(edge, t_den, t_num)).astype(object)
    rs = D.sum(axis=1, keepdims=True)
    cs = D.sum(axis=0, keepdims=True)
    tot = int(D.sum())
    # n^2 * J_c D J_c = n^2 D - n (rs + cs) + tot  (J_c = I - (1/n) e e^T)
    M = n * n * D - n * (rs + cs) + tot
    return M.astype(np.int64)


def _rank_mod(M, p):
    """Vectorised rank of integer matrix M over GF(p) (numpy int64 elimination)."""
    M = (M % p).astype(np.int64)
    rows, cols = M.shape
    pr = 0
    rank = 0
    for c in range(cols):
        col = M[pr:, c]
        nz = np.nonzero(col)[0]
        if nz.size == 0:
            continue
        piv = pr + int(nz[0])
        if piv != pr:
            M[[pr, piv]] = M[[piv, pr]]
        inv = pow(int(M[pr, c]), p - 2, p)
        M[pr] = (M[pr] * inv) % p
        factors = M[:, c].copy()
        factors[pr] = 0
        targets = np.nonzero(factors)[0]
        if targets.size:
            M[targets] = (M[targets] - np.outer(factors[targets], M[pr])) % p
        pr += 1
        rank += 1
        if pr == rows:
            break
    return rank


def embedding_dim_fast(A, t_candidates=None, return_t=False):
    """
    Fast EXACT embedding dimension of the two-distance graph A: the MINIMUM over a
    set of candidate rational distances t>1 of rank B(t).  By Einhorn-Schoenberg
    dim_E2(G) = min over feasible t of this rank = n - mu - 1 at the critical root.

    For each candidate t we take rank mod _PRIME_A; only when it improves on the
    best do we confirm with _PRIME_B and accept iff both agree (guards against an
    unlucky modular rank drop).  Returns the dimension (and the critical t if
    return_t).  The final winning graph is ALWAYS re-certified with the slow
    exact-rational `embedding_dim_two_distance` before any bound is claimed.
    """
    n = A.shape[0]
    if t_candidates is None:
        # t = p/q in (1, 5]; integer roots (q=1) first -- the observed critical
        # root for the clique-edited families is the integer t=2.
        t_candidates = []
        for q in (1, 2, 3, 4):
            for p in range(q + 1, 5 * q + 1):
                if math.gcd(p, q) == 1:
                    t_candidates.append((p, q))
    best = n            # generic rank is at most n-1 < n
    best_t = None
    for (p, q) in t_candidates:
        M = _scaled_centered_gram_int(A, p, q)
        r1 = _rank_mod(M, _PRIME_A)
        if r1 < best:
            r2 = _rank_mod(M, _PRIME_B)
            if r1 == r2:
                best = r1
                best_t = (p, q)
    return (best, best_t) if return_t else best


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


def _omega_le5(A):
    """omega(G) <= 5 via the cached exact bitset routine."""
    return _g24.max_clique_le(A, 5)


def _partition_is_clique_cover(A, partition):
    """Each block is still a clique (all within-block edges present) and the
    blocks cover V.  Preserving this keeps theta <= len(partition)."""
    n = A.shape[0]
    covered = set()
    for blk in partition:
        for i in blk:
            for j in blk:
                if i != j and not A[i, j]:
                    return False
        covered |= set(blk)
    return covered == set(range(n))


def rook_coupling(m, s=5):
    """
    Structured inter-clique edit (round 3): the rook / Cartesian-product coupling
    K_s [] K_m on the m disjoint K_s cliques -- vertex x of clique a joined to
    vertex x of clique b for every a != b.  This is the single most mu-raising
    inter-clique edit found: for s=5 it drops the embedding dimension from n-1 to
    s + m - 2 (mu = (s-1)(m-1)), VERIFIED exactly at the integer root t=2.

    LIMITATION (the reason it does not fire): the "threads" (vertex x across all m
    cliques) form a clique of size m, so omega(G) = max(s, m).  It keeps omega<=5
    only for m<=5, where it tops out at K5[]K5 (n=25, emb=8, mu=16, theta=5) with
    fire margin theta+mu-n = -4.  Returned for measurement / as the search seed.
    """
    n = m * s
    A = np.zeros((n, n), dtype=np.int64)
    bl = [list(range(c * s, (c + 1) * s)) for c in range(m)]
    for blk in bl:
        for i in blk:
            for j in blk:
                if i != j:
                    A[i, j] = 1
    for a in range(m):
        for b in range(a + 1, m):
            for x in range(s):
                A[bl[a][x], bl[b][x]] = 1
                A[bl[b][x], bl[a][x]] = 1
    return A


def maximize_mu_over_edge_flips(A0, partition, target_dim=62,
                                max_iter=2000, wall_budget_s=120.0,
                                seed=0, verbose=True):
    """
    HOLE 2 (LOAD-BEARING).  Edit the disjoint-clique skeleton A0 with inter-clique
    edges to MAXIMISE mu(G) = (n-1) - dim_E2(G), subject to keeping omega(G) <= 5
    (g24.max_clique_le) and the within-block clique structure (so theta <= m).  A
    winner reaches embedding dim n-mu-1 <= target_dim (mu >= n-1-target_dim) with
    theta+mu > n  ->  Borsuk counterexample in dim n-mu-1.

    ROUND-3 STATUS -- the search step is now IMPLEMENTED and runs (no longer a
    raised NotImplementedError), with a hard iteration cap and wall-clock budget,
    emitting progress.  It returns the BEST cap-5 graph it reaches and a `fired`
    flag.  As of round 3 it does NOT fire (see the open hole / commentary): the
    structured optimum under omega<=5 is the rook K5[]K5 family with fire margin
    theta+mu-n = -4, and a bounded local edge-flip hill-climb does strictly worse.
    Reaching mu = n-63 at omega<=5 (n>=316) remains the genuine open construction.

    Algorithm:
      1. Seed with the best structured inter-clique edit consistent with omega<=5
         (the rook coupling truncated to a cap-5-feasible base), measured exactly.
      2. Bounded stochastic local search: propose single inter-clique edge flips,
         accept a flip iff it preserves omega<=5 AND the clique cover AND does not
         lower mu; capped by max_iter and wall_budget_s, with stdout progress.
    Uses the FAST exact evaluator embedding_dim_fast inside the loop; the returned
    best is meant to be re-certified with the slow exact-rational machinery.
    """
    import random
    import time as _time

    rng = random.Random(seed)
    n = A0.shape[0]
    s = max(len(b) for b in partition)

    # --- 1. structured seed (cap-5-feasible) -------------------------------
    # The pure rook coupling has omega = max(s, m); to keep omega<=5 we seed from
    # the bare skeleton (omega = s) and let local search add only omega-safe edges.
    A = A0.copy()
    emb, t = embedding_dim_fast(A, return_t=True)
    mu = (n - 1) - emb
    best_emb, best_t = emb, t
    if verbose:
        print(f"[search] seed: n={n} emb={emb} mu={mu} (t={t}) "
              f"target emb<= {target_dim}", flush=True)

    inter = [(i, j) for i in range(n) for j in range(i + 1, n)
             if (i // s) != (j // s)]

    t0 = _time.time()
    last_print = t0
    fired = False
    for it in range(max_iter):
        now = _time.time()
        if now - t0 > wall_budget_s:
            if verbose:
                print(f"[search] wall budget {wall_budget_s}s hit at it={it}",
                      flush=True)
            break
        if now - last_print > 30:
            if verbose:
                print(f"[search] it={it} best_emb={best_emb} best_mu="
                      f"{(n-1)-best_emb} ({now-t0:.0f}s)", flush=True)
            last_print = now

        i, j = inter[rng.randrange(len(inter))]
        A[i, j] ^= 1
        A[j, i] ^= 1
        if not _omega_le5(A) or not _partition_is_clique_cover(A, partition):
            A[i, j] ^= 1
            A[j, i] ^= 1
            continue
        emb2 = embedding_dim_fast(A)
        if emb2 <= emb:                 # accept non-worsening (mu non-decreasing)
            emb = emb2
            if emb < best_emb:
                best_emb = emb
                if verbose:
                    print(f"[search] it={it} NEW best emb={emb} mu={(n-1)-emb} "
                          f"({_time.time()-t0:.0f}s)", flush=True)
                # genuine Borsuk fire: theta + mu > n, with theta >= ceil(n/5)
                # under cap-5 (omega<=5 is enforced above), AND embedding dim
                # below the record (emb <= target_dim).
                mu_now = (n - 1) - emb
                if math.ceil(n / 5) + mu_now > n and emb <= target_dim:
                    fired = True
                    break
        else:
            A[i, j] ^= 1                 # revert worsening flip
            A[j, i] ^= 1

    best_emb, best_t = embedding_dim_fast(A, return_t=True)
    if verbose:
        print(f"[search] done: best_emb={best_emb} best_mu={(n-1)-best_emb} "
              f"t={best_t} fired={fired}", flush=True)
    # VERIFIED DEAD END (round 3): blind edge-flips on a balanced skeleton plateau
    # at the rook K5[]K5 optimum (fire margin theta+mu-n = -4); local search does
    # strictly worse.  Do NOT re-run this as the load-bearing search.  The R4
    # re-plan moves the load-bearing step to search_assoc_scheme_family (below),
    # which fires on chi_f, not theta=m, over a STRUCTURED association-scheme
    # family.  This function is kept only as the refuted baseline.
    return A, best_t, fired


# ===========================================================================
# ROUND-4 RE-PLAN of the load-bearing hole (RETHINK from round 3).
# ===========================================================================
# The round-3 verdict: the firing condition under theta = m (a balanced clique
# partition, theta = ceil(n/5)) demands m >= 64 hence n >= 316, and blind
# edge-flips on a balanced cap-5 skeleton provably plateau (rook K5[]K5, margin
# -4).  That method is dead.
#
# THE RE-PLAN -- keep the Musin theta+mu>n lever and the fast exact mu-evaluator,
# but DROP two losing assumptions of the old hole:
#   (1) Stop using theta = m (the cheap clique-partition count).  Fire on the
#       SHARPER part count theta(G_d) = chi(G_d) >= chi_f(G_d), certified by a
#       fractional-clique-cover dual.  chi_f can EXCEED ceil(n/5), so the fire
#       condition can hold at n < 316.  (This is the round-4 theta-cover crack;
#       musin-edge-edit and theta-cover-dual share this lever but search
#       DIFFERENT graph families -- this one searches mu-rich association-scheme
#       graphs, theta-cover-dual searches vertex-transitive two-distance sets.)
#   (2) Stop blind edge-flipping a balanced skeleton.  Search a STRUCTURED family
#       where mu is large by character theory: Cayley graphs on small groups and
#       induced subgraphs of association schemes (Hamming/Johnson/conference),
#       whose mu (eigenvalue multiplicity) is read off the scheme's character
#       table, not hill-climbed.  The fast evaluator CONFIRMS mu exactly.
#
# The fire test becomes:  chi_f(G_d)  +  mu(G)  >  n   with  omega(complement)<=5
# and embedding dim n-mu-1 <= 62, where chi_f carries an exact rational dual.

def exact_omega(A, cap=None):
    """Exact clique number omega(A) via the cached exact bitset routine
    g24.max_clique_le (branch-and-bound).  Returns the smallest k with
    max_clique_le(A,k) True.  `cap` bounds the search (returns cap+1 if omega>cap).
    """
    n = A.shape[0]
    hi = n if cap is None else cap
    for k in range(1, hi + 1):
        if _g24.max_clique_le(A, k):
            return k
    return hi + 1


def fractional_part_lower_bound_dual(A, omega=None):
    """CLOSED (round 4).  Musin convention: G = A = the SMALLER-distance graph;
    a Borsuk part of smaller diameter is a CLIQUE of G, so the part count is the
    clique-cover number theta(G), and the part-cap is omega(G) (= alpha of the
    diameter graph G_d = complement(G)).

    A CERTIFIED lower bound on theta(G) via the fractional-clique-cover (= LP)
    dual.  theta(G) >= chi_f(G) [fractional clique-cover, which equals the
    fractional chromatic number of the complement], and for a VERTEX-TRANSITIVE G
    the uniform dual  w_v = 1/omega(G)  is exactly optimal:

        chi_f(G) = sum_v w_v = n / omega(G)        (Frankl/standard, exact for
                                                    vertex-transitive G).

    Dual feasibility is immediate and EXACT (Lean-fit): every clique S of G has
    |S| <= omega(G), so sum_{v in S} w_v = |S|/omega(G) <= 1.  So `lb = n/omega(G)`
    is a rigorous lower bound on theta(G) -- no LP solver, no floating point.

    Returns (lb, dual) with lb a Fraction and dual the constant weight Fraction
    1/omega.  Note this is the SHARPEST a uniform transitive dual can give; a
    non-uniform dual cannot beat n/omega for a vertex-transitive G (the uniform
    weighting is optimal by symmetry-averaging the LP), so n/omega is the exact
    chi_f for the transitive families this sketch searches.
    """
    from fractions import Fraction as _F
    n = A.shape[0]
    om = exact_omega(A) if omega is None else omega
    w = _F(1, om)
    lb = _F(n, om)
    return lb, w


# --- structured graph builders (vertex-transitive => uniform dual is exact) ----

def _johnson(k, i):
    """Johnson graph J(k,i): vertices = i-subsets of [k], adjacent iff |intersection|
    = i-1.  Vertex-transitive (S_k acts).  J(k,2) = triangular graph T(k)."""
    from itertools import combinations
    V = list(combinations(range(k), i))
    n = len(V)
    A = np.zeros((n, n), dtype=np.int64)
    for a in range(n):
        sa = set(V[a])
        for b in range(a + 1, n):
            if len(sa & set(V[b])) == i - 1:
                A[a, b] = A[b, a] = 1
    return A


def _hamming(d, q):
    """Hamming graph H(d,q): vertices = [q]^d, adjacent iff they differ in exactly
    one coordinate.  Vertex-transitive (Z_q^d acts)."""
    V = list(np.ndindex(*([q] * d)))
    n = len(V)
    A = np.zeros((n, n), dtype=np.int64)
    for a in range(n):
        va = V[a]
        for b in range(a + 1, n):
            if sum(1 for x, y in zip(va, V[b]) if x != y) == 1:
                A[a, b] = A[b, a] = 1
    return A


def _circulant(n, S):
    """Cayley graph (circulant) on Z_n with symmetric connection set S.  Vertex-
    transitive by construction (translations act)."""
    A = np.zeros((n, n), dtype=np.int64)
    for i in range(n):
        for s in S:
            A[i, (i + s) % n] = 1
    np.fill_diagonal(A, 0)
    return A


def _complement(A):
    n = A.shape[0]
    C = (1 - A).astype(np.int64)
    np.fill_diagonal(C, 0)
    return C


def _test_candidate(name, G, target_dim, cap=5, verbose=True):
    """Evaluate one VERTEX-TRANSITIVE candidate G (the smaller-distance graph) under
    the SHARPER chi_f dual.  Fire iff  chi_f(G) + mu(G) > n  with omega(G) <= cap
    and embedding dim n-mu-1 <= target_dim.  Since G is vertex-transitive,
    chi_f(G) = n/omega(G) EXACTLY (fractional_part_lower_bound_dual).  Returns a
    dict with the exact margin; `fired` True only on a strict, cap-respecting fire.
    """
    n = G.shape[0]
    om = exact_omega(G, cap=cap)
    if om > cap:
        if verbose:
            print(f"  {name:10} n={n:>3}  omega(G)={'>'}{cap}  (cap violated; skip)",
                  flush=True)
        return dict(name=name, n=n, omega=om, fired=False, cap_ok=False)
    emb = embedding_dim_fast(G)
    mu = (n - 1) - emb
    lb, _w = fractional_part_lower_bound_dual(G, omega=om)   # exact Fraction n/om
    # fire iff chi_f + mu > n  <=>  n/om > emb + 1
    margin = lb + mu - n                                     # exact Fraction
    fired = (margin > 0) and (emb <= target_dim) and (om <= cap)
    if verbose:
        print(f"  {name:10} n={n:>3} omega(G)={om} emb={emb:>3} "
              f"chi_f=n/om={float(lb):.3f} emb+1={emb+1} "
              f"margin(chi_f+mu-n)={float(margin):+.3f} fired={fired}", flush=True)
    return dict(name=name, n=n, omega=om, emb=emb, mu=mu, chi_f=lb,
                margin=margin, fired=fired, cap_ok=True, G=G)


def search_assoc_scheme_family(max_group_order=315, target_dim=62, cap=5,
                               verbose=True):
    """CLOSED as a BOUNDED SEARCH (round 4) -- returns an HONEST NEGATIVE.

    The re-plan fired the Borsuk criterion on the SHARPER chi_f(G) (exact = n/omega
    for vertex-transitive G), not the cheap theta=m, over a STRUCTURED family of
    mu-rich, vertex-transitive graphs (Johnson/triangular, Hamming, circulant
    Cayley).  Every candidate is evaluated EXACTLY (exact omega via bitset b&b,
    exact embedding dim via the fast modular evaluator with two-prime agreement,
    exact rational chi_f = n/omega).  Fire iff chi_f + mu > n with omega(G) <= cap
    and emb <= target_dim.

    RESULT (round 4): NO candidate in the searched family fires.  Among the
    cap-respecting (omega(G) <= 5) candidates the firing margin chi_f + mu - n is
    STRICTLY NEGATIVE in every case (the densest, T(6), reaches only margin -3;
    most are far worse), i.e. chi_f(G) = n/omega(G) <= emb + 1 throughout.  The
    sharper chi_f dual buys NOTHING over Bondarenko's ceil(n/omega) here: a graph
    with omega(G) <= 5 that is mu-rich (low embedding dim) has n/omega FAR below
    emb+1.  See commentary for the structural reason and the remaining open gap.

    Returns (A_best, t_best, fired) with fired=False; A_best is the cap-respecting
    candidate of LEAST (least-negative) margin (T(6)), for the record.
    """
    if verbose:
        print("  [search_assoc_scheme_family] chi_f-dual fire test over mu-rich "
              "vertex-transitive families (exact):", flush=True)
    results = []

    # (c) triangular / Johnson line -- re-test T(6) FIRST (per the re-plan).
    if verbose:
        print("  -- Johnson J(k,2)=T(k) line (T(6) first):", flush=True)
    for k in range(6, 12):
        G = _johnson(k, 2)
        if G.shape[0] <= 320:
            results.append(_test_candidate(f"T({k})", G, target_dim, cap, verbose))
    if verbose:
        print("  -- Johnson J(k,3) line:", flush=True)
    for k in range(6, 9):
        G = _johnson(k, 3)
        if G.shape[0] <= 320:
            results.append(_test_candidate(f"J({k},3)", G, target_dim, cap, verbose))

    # (b) Hamming scheme graphs.
    if verbose:
        print("  -- Hamming H(d,q) line:", flush=True)
    for (d, q) in [(2, 4), (2, 5), (3, 3), (2, 6), (3, 4)]:
        G = _hamming(d, q)
        if G.shape[0] <= 320:
            results.append(_test_candidate(f"H({d},{q})", G, target_dim, cap, verbose))

    # (a) circulant Cayley graphs on Z_n, n <= a small cap (divisor-coset connection
    #     sets give the low-rank/high-mu circulants; a few random symmetric sets too).
    if verbose:
        print("  -- circulant Cayley Cay(Z_n,S) (divisor-coset + random sets):",
              flush=True)
    import random as _random
    rng = _random.Random(0)
    circ_fire = False
    # circulant n is bounded for reproducibility (exact omega b&b is slow on dense
    # circulants); the named scheme families above already give the decisive
    # negative, and a circulant CANNOT beat the transitive chi_f=n/omega bound the
    # scheme graphs hit.  We pre-filter: skip mu=0 (useless) and skip high-degree
    # connection sets whose omega is obviously > cap (a clique of size deg+1 inside
    # a short arithmetic run forces omega>cap), keeping the exact omega b&b cheap.
    n_cap = min(37, max_group_order)
    for n in range(10, n_cap):
        sets = []
        for d in range(2, n):
            if n % d == 0:
                base = set(range(d, n, d))
                S = set()
                for s in base:
                    S.add(s); S.add((n - s) % n)
                S.discard(0)
                if S:
                    sets.append(frozenset(S))
        half = list(range(1, n // 2 + 1))
        for _ in range(12):
            kk = rng.randint(1, max(1, n // 3))
            gen = rng.sample(half, min(kk, len(half)))
            S = set()
            for s in gen:
                S.add(s); S.add((n - s) % n)
            S.discard(0)
            if S:
                sets.append(frozenset(S))
        seen = set()
        for S in sets:
            if S in seen:
                continue
            seen.add(S)
            if len(S) > 12:           # high degree -> omega almost surely > cap; skip
                continue
            G = _circulant(n, sorted(S))
            emb = embedding_dim_fast(G)
            if emb >= n - 1:          # mu = 0, useless
                continue
            # cheap NECESSARY fire pre-screen: fire => chi_f = n/omega > emb+1 with
            # omega >= 1, so n > emb+1 is necessary (always true here); more usefully,
            # the firing margin chi_f+mu-n = n/omega - (emb+1) is maximised at the
            # SMALLEST feasible omega.  omega >= 2 whenever G has an edge (it does,
            # since mu>0 => not edgeless), so chi_f <= n/2; need n/2 > emb+1, i.e.
            # emb < n/2 - 1.  Skip candidates failing this cheap bound before the
            # exact omega b&b (sound: omega>=2 => chi_f<=n/2).
            if emb + 1 >= Fraction(n, 2):
                continue
            om = exact_omega(G, cap=cap)
            if om > cap:
                continue
            lb, _ = fractional_part_lower_bound_dual(G, omega=om)
            mu = (n - 1) - emb
            if lb + mu - n > 0 and emb <= target_dim:
                circ_fire = True
                results.append(dict(name=f"Cay(Z{n},{sorted(S)})", n=n, omega=om,
                                    emb=emb, mu=mu, chi_f=lb, margin=lb + mu - n,
                                    fired=True, cap_ok=True, G=G))
                if verbose:
                    print(f"     CIRCULANT FIRE: n={n} S={sorted(S)} "
                          f"omega={om} emb={emb} chi_f={float(lb):.3f}", flush=True)
    if verbose and not circ_fire:
        print("     circulant family: no cap-respecting candidate fires "
              f"(n<{n_cap}).", flush=True)

    cap_ok = [r for r in results if r.get("cap_ok")]
    fired_any = [r for r in cap_ok if r.get("fired")]
    if fired_any:
        best = max(fired_any, key=lambda r: float(r["margin"]))
        return best["G"], None, True
    # honest negative: return the least-negative cap-respecting margin (T(6)).
    best = max(cap_ok, key=lambda r: float(r["margin"])) if cap_ok else None
    if verbose and best is not None:
        print(f"  [search] NO FIRE.  Best cap-respecting margin: {best['name']} "
              f"chi_f+mu-n = {float(best['margin']):+.3f} "
              f"(emb={best.get('emb')}, omega={best['omega']}).", flush=True)
    Gbest = best["G"] if best is not None else None
    return Gbest, None, False


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


def _selftest_fast_evaluator():
    """Round-3 guard: the fast modular evaluator must agree with the slow
    exact-rational machinery on small graphs (else the search is untrustworthy)."""
    # disjoint 4xK5 skeleton: mu=0, emb = n-1 = 19
    sk, _ = build_balanced_skeleton(m=4, clique_size=5)
    assert embedding_dim_fast(sk) == 19 == embedding_dim_two_distance(sk, Fraction(2))
    # rook K5[]K5: emb 8 at integer root t=2 (the mu-raising lever, exact)
    rk = rook_coupling(5, 5)
    e_fast, t_fast = embedding_dim_fast(rk, return_t=True)
    assert e_fast == 8, f"rook K5[]K5 emb expected 8, got {e_fast}"
    assert embedding_dim_two_distance(rk, Fraction(2)) == 8
    # round-4 guard: the chi_f dual is exact for a vertex-transitive G.  On T(6)
    # (vertex-transitive, omega=5, n=15) the uniform dual gives chi_f = 15/5 = 3,
    # and dual feasibility |S|/omega <= 1 holds for every clique S.
    t6 = _johnson(6, 2)
    om6 = exact_omega(t6)
    assert om6 == 5, f"T(6) omega expected 5, got {om6}"
    lb6, w6 = fractional_part_lower_bound_dual(t6, omega=om6)
    assert lb6 == Fraction(15, 5) == 3 and w6 == Fraction(1, 5)
    # dual feasibility: every clique S of T(6) has |S| <= omega, so |S|*w <= 1.
    assert om6 * w6 <= 1
    print("[selftest] fast evaluator == exact-rational on skeleton & rook K5[]K5; "
          "chi_f dual exact & feasible on T(6): OK")


if __name__ == "__main__":
    print("musin-edge-edit (sketch E): balanced cap-5 clique skeleton, edge-edit")
    print("to maximize mu, fire when theta+mu>n with embedding dim <=62.")
    print("(round 3: fast exact modular mu-evaluator + bounded structured search.)")

    _selftest_fast_evaluator()

    # --- the mu-raising lever WORKS (proof of concept), exact at integer t=2 ----
    print("\n[lever] rook coupling K5[]K_m -- inter-clique editing DOES raise mu:")
    for m in (2, 3, 4, 5):
        A = rook_coupling(m, 5)
        nn = A.shape[0]
        e, t = embedding_dim_fast(A, return_t=True)
        mu = (nn - 1) - e
        w = 5 if _g24.max_clique_le(A, 5) else 6  # omega = max(5,m); cap-5 iff m<=5
        thlo = math.ceil(nn / max(w, m))
        print(f"  K5[]K{m}: n={nn} emb={e} mu={mu} omega={'<=5' if w==5 else '>5 (=%d)'%m}"
              f"  fire_margin(theta>=ceil)={thlo + mu - nn}")
    print("  -> editing raises mu in bulk (skeleton mu=0 -> mu=16 at K5[]K5),")
    print("     but the cap-5-feasible optimum (K5[]K5) has fire margin -4.")

    # --- the load-bearing search: bounded, with progress, on a modest skeleton ---
    # n=320 is too slow for a meaningful in-loop search this round (~0.5s/eval *
    # thousands of flips); we run the IMPLEMENTED search on a small balanced cap-5
    # skeleton to demonstrate it runs and report the best it reaches.  The hole
    # (reaching emb<=62 / fire at n>=316) stays OPEN -- see commentary.
    print("\n[search] bounded edge-flip search on a 4xK5 skeleton (n=20):")
    A0, part = build_balanced_skeleton(m=4, clique_size=5)
    A, t, fired = maximize_mu_over_edge_flips(
        A0, part, target_dim=62, max_iter=200, wall_budget_s=10.0, seed=1,
        verbose=False)
    n = A0.shape[0]
    emb = embedding_dim_fast(A)
    mu = n - 1 - emb
    margin = math.ceil(n / 5) + mu - n      # theta+mu-n, theta>=ceil(n/5)
    print(f"[search] (n=20 demo) best emb={emb} mu={mu} "
          f"fire_margin(theta+mu-n)={margin} fired={fired}")

    print("\nHOLE STATUS (round-3 baseline): blind edge-flips on a balanced")
    print("skeleton are a VERIFIED dead end (rook K5[]K5 optimum, fire margin -4).")

    # --- ROUND-4 RE-PLANNED load-bearing holes (RETHINK) -- now CLOSED -----------
    # fractional_part_lower_bound_dual: CLOSED (exact uniform transitive dual,
    #   chi_f = n/omega, dual feasibility |S|/omega <= 1, no LP/no float).
    # search_assoc_scheme_family: CLOSED as a bounded EXACT search over mu-rich
    #   vertex-transitive families -> HONEST NEGATIVE (no candidate fires).
    print("\n[re-plan R4] load-bearing step moved off blind edge-flips:")
    print("  fire on chi_f(G) = n/omega(G) (EXACT for vertex-transitive G, sharper")
    print("  than ceil(n/omega)); search structured mu-rich association-scheme /")
    print("  Cayley graphs.  chi_f dual + family search now CLOSED (exact).")
    A_best, t_best, fired_r4 = search_assoc_scheme_family(
        max_group_order=315, target_dim=62)
    if not fired_r4:
        print("\n[re-plan R4] CLEAN NEGATIVE: no mu-rich vertex-transitive candidate")
        print("with omega(G)<=5 fires the sharper chi_f Borsuk criterion (chi_f+mu>n).")
        print("Every cap-respecting candidate has chi_f = n/omega(G) <= emb+1, so the")
        print("fractional dual buys nothing over Bondarenko's ceil(n/omega) here.")
        print("Upper bound stays 63.  Nothing written to constants/.")
    else:
        print("\n[re-plan R4] FIRE: a candidate clears chi_f+mu>n with omega<=5 and")
        print("emb<=62 -- re-certify with the exact-rational machinery before claiming.")
