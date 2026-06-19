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
    # TODO(load-bearing, OPEN): fired is False -- no cap-5 edit reaches emb<=62
    # (mu>=n-63) at n>=316.  The structured optimum under omega<=5 is the rook
    # K5[]K5 (fire margin -4) and local search does worse.  Landing the fire
    # condition needs a genuinely new omega<=5 construction (an exceptional
    # association-scheme graph outside the swept SRG table), not blind editing.
    return A, best_t, fired


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
    print("[selftest] fast evaluator == exact-rational on skeleton & rook K5[]K5: OK")


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
        A0, part, target_dim=62, max_iter=600, wall_budget_s=60.0, seed=1)
    n = A0.shape[0]
    emb = embedding_dim_fast(A)
    mu = n - 1 - emb
    margin = math.ceil(n / 5) + mu - n      # theta+mu-n, theta>=ceil(n/5)
    print(f"[search] (n=20 demo) best emb={emb} mu={mu} "
          f"fire_margin(theta+mu-n)={margin} fired={fired}")

    print("\nHOLE STATUS: maximize_mu_over_edge_flips is implemented and runs, but")
    print("does NOT fire (no cap-5 graph reaching emb<=62 at n>=316 found).  The")
    print("structured optimum under omega<=5 is rook K5[]K5 (fire margin -4); a")
    print("winner needs a new omega<=5 construction outside the swept SRG table.")
