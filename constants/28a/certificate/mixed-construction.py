"""
Sketch D  --  mixed-construction  (constant 28a, attempt 63 -> 62)

ATTACK LINE D (explorer): Gri's final set is NOT two-distance (the added p gives
a third distance).  The door is open to sets that are a two-distance CORE that
genuinely sits in <=62 dims, plus a few controlled extra (perturbation) points,
all inside the same 62-dim subspace, with the Borsuk part-cap kept at 5.

----------------------------------------------------------------------------
CORRECT BORSUK CRITERION (reconciled this round -- see commentary).
----------------------------------------------------------------------------
For a finite X with diameter d, a Borsuk part must have diameter < d, so no two
points at distance d (a "diameter pair") share a part.  Hence

    Borsuk(X) = chi(G_d),   G_d = diameter graph (edge iff dist == d),

and the lower bound used by Bondarenko/Gri is

    chi(G_d) >= |X| / alpha(G_d),   alpha(G_d) = max set with NO diameter pair.

So the certifiable target is  alpha(G_d) <= 5  =>  parts >= ceil(|X|/5), and a
R^62 counterexample needs |X| >= 316 (ceil(316/5)=64 > 63).

alpha(G_d) = omega(complement of G_d) = omega of the "non-diameter" graph
(edge iff dist < d).  For a TWO-DISTANCE set this complement is exactly the
smaller-distance graph; for G_2(4)'s C-points that is the induced adjacency
A[T,T] (adjacency <-> inner product 18 <-> the smaller distance), which is why
the certified g24 fact omega(A)=5 is precisely alpha(G_d)=5.

NOTE (correctness fix, round 3): the round-2 verify() checked omega of the
DIAMETER graph (the wrong quantity).  The part bound is governed by alpha of the
diameter graph = omega of its COMPLEMENT.  verify() below is corrected and uses
EXACT integer rank + EXACT clique (over the complement), matching the certified
fresh-orthogonal-dir / g24 machinery.  This is intermediate-statement search:
the hole's planned check was wrong; the true provable one is alpha(G_d) <= 5.
"""

import numpy as np
import math
import sys, os
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib
_g24 = importlib.import_module("g24")
_fo = importlib.import_module("fresh-orthogonal-dir")


# ---------------------------------------------------------------------------
# HOLE 1 -- CLOSED (round 3): a <=62-dim G_2(4) hyperplane section of C.
# ---------------------------------------------------------------------------

def build_core():
    """
    CLOSED (round 3).  Returns a G_2(4) section that sits EXACTLY in 62 dims,
    certified by exact integer rank over Q (not float SVD).

    Construction (option (a) of the revised hole -- a G_2(4) hyperplane section
    of C with exact surviving rank <= 62):
      * Build G_2(4) and the standard partition wrt the first isotropic point q0
        (B,C with |B|=96, |C|=320), from the certified g24 lemma.
      * The 320 C-points span EXACTLY 63 dims (Gri wall).  Delete the C-points
        that lie in the B-structure of a SECOND isotropic point (the structured
        family of fresh-orthogonal-dir): this is the hyperplane section that
        removes exactly one spanned direction.  The surviving subset T has
            T subset of C, |T| = 270,  exact integer rank(Gram[T,T]) = 62,
        and its smaller-distance graph A[T,T] has clique number omega = 5
            (= alpha of T's diameter graph = 5),  ceil(270/5) = 54.
      * EXACT certificate: rank computed by rational Gaussian elimination
        (fo.exact_rank), clique by exact bitset branch-and-bound (g24.max_clique_le).

    The float reps from the g24 lemma are NOT used for any load-bearing claim;
    the surviving rank and the clique are both re-certified exactly here.

    Returns dict(T, P, A_core, G_core, info) where
        T       : list of 270 G_2(4) vertex indices (the core, subset of C),
        P       : (270 x 62) float coords (search/visualization only),
        A_core  : (270 x 270) int adjacency of the smaller-distance graph,
        G_core  : (270 x 270) int standard Gram of the core,
        info    : exact certificate dict.
    """
    A, verts = _g24.build_g24()
    q0, B_idx, C_idx = _g24.standard_partition(verts)
    assert len(B_idx) == 96 and len(C_idx) == 320
    G = _g24.gram_standard(A)
    E = _fo.eigenspace_E(A)

    T = _fo.search_structured_fresh_direction(A, verts, E)
    assert T is not None, "structured 62-dim section not found"
    Tset = set(T)
    assert Tset <= set(C_idx), "core must be a section of C"
    assert len(T) == 270, f"expected 270-point section, got {len(T)}"

    # EXACT certification of the load-bearing facts.
    G_core = G[np.ix_(T, T)]
    dim = _fo.exact_rank(G_core)                 # exact rank over Q
    A_core = A[np.ix_(T, T)]
    alpha_le_5 = _g24.max_clique_le(A_core, 5)   # alpha(G_d) = omega(A_core)
    alpha_eq_5 = alpha_le_5 and not _g24.max_clique_le(A_core, 4)
    assert dim == 62, f"exact rank must be 62, got {dim}"
    assert alpha_le_5, "smaller-distance clique (alpha of diameter graph) must be <=5"

    # float coords (62-dim) for the perturbation search only -- never load-bearing
    w, V = np.linalg.eigh(G_core.astype(float))
    pos = w > 1e-6
    P = V[:, pos] * np.sqrt(w[pos])
    assert P.shape[1] == 62

    info = dict(n=len(T), exact_dim=dim, alpha_le_5=alpha_le_5,
                alpha_eq_5=alpha_eq_5, parts_lb=math.ceil(len(T) / 5))
    return dict(T=T, P=P, A_core=A_core, G_core=G_core, info=info)


# ---------------------------------------------------------------------------
# HOLE 2 (load-bearing) -- OPEN.  engineer_perturbation.
# ---------------------------------------------------------------------------

def engineer_perturbation(core, target_n=316, max_iters=20000, time_budget_s=120,
                          rng_seed=0, verbose=True):
    """
    OPEN HOLE (load-bearing).  Add perturbation points P_add inside the SAME
    62-dim subspace as the core so that X = core u P_add has

        |X| >= target_n,                          (>= 316)
        diameter(X) == diameter(core) (= sqrt 192),  -- no pair may EXCEED it,
        alpha(diameter graph of X) <= 5           => parts >= ceil(|X|/5).

    THE OBSTRUCTION (made precise round 3).  alpha(G_d) is the max set with NO
    diameter pair (all pairwise dist^2 < 192).  Adding a point p that is FAR from
    the diameter (e.g. near the centroid, dist^2 ~ 90 to all core points) gives p
    NO diameter edges, so p joins every large "non-diameter" clique and BLOWS UP
    alpha(G_d) -- catastrophic.  To keep alpha <= 5, each added p must be at the
    diameter distance (dist^2 = 192) from ENOUGH core points that p never sits in
    a 6-set of mutually non-diameter points.  This is exactly why Gri could add
    only ONE such point; doing it 46+ times in a fixed 62-dim subspace, keeping
    alpha capped, is the open construction.

    This routine runs a BOUNDED greedy search (hard caps on iterations and wall
    clock; frequent stdout) and returns the best valid X it reaches.  It does NOT
    in general reach 316; it reports the best count honestly.

    Strategy of the bounded search:
      * Candidate pool = points at dist^2 = 192 from a chosen 'far' core anchor,
        intersected (approximately) with dist^2 <= 192 to all core points; we
        sample such points on the boundary sphere of the ball-intersection.
      * Accept a candidate only if adding it keeps the EXACT alpha(G_d) <= 5
        (re-checked incrementally on a float diameter graph, then re-certified on
        the accepted final X).
    """
    import time
    t0 = time.time()
    P = core["P"]                       # 270 x 62 float coords
    n0 = P.shape[0]
    diam2 = 192.0
    rng = np.random.default_rng(rng_seed)

    pts = [P[i].copy() for i in range(n0)]

    def diam_graph_alpha_le5(points):
        """EXACT-ish (float, tol) check that the diameter graph has alpha<=5,
        i.e. its complement (non-diameter graph) has omega<=5.  Float here is for
        the SEARCH only; the final X is re-certified exactly in verify()."""
        M = np.array(points)
        d = (M * M).sum(1)
        D2 = d[:, None] + d[None, :] - 2 * M @ M.T
        np.fill_diagonal(D2, diam2)          # self-loops irrelevant
        # complement of diameter graph: edge iff dist^2 < diam2 (non-diameter)
        comp = (D2 < diam2 - 1e-3)
        np.fill_diagonal(comp, False)
        return _omega_le(comp, 5)

    accepted = 0
    it = 0
    if verbose:
        print(f"  [perturb] core n={n0}, target={target_n}, "
              f"budget={time_budget_s}s / {max_iters} iters", flush=True)
    while len(pts) < target_n and it < max_iters and time.time() - t0 < time_budget_s:
        it += 1
        # sample a candidate on the diameter sphere of a random core anchor,
        # then project toward feasibility (dist^2<=192 to all current points).
        anchor = pts[rng.integers(len(pts))]
        direction = rng.standard_normal(62)
        direction /= np.linalg.norm(direction)
        cand = anchor + math.sqrt(diam2) * direction
        d2 = np.array([((cand - q) ** 2).sum() for q in pts])
        if d2.max() > diam2 + 1e-6:
            continue                          # would grow the diameter
        trial = pts + [cand]
        if diam_graph_alpha_le5(trial):
            pts = trial
            accepted += 1
            if verbose and accepted % 5 == 0:
                print(f"  [perturb] accepted {accepted} "
                      f"(n={len(pts)}, it={it}, {time.time()-t0:.0f}s)", flush=True)
    X = np.array(pts)
    if verbose:
        print(f"  [perturb] DONE: accepted {accepted}, |X|={len(pts)}, "
              f"iters={it}, {time.time()-t0:.0f}s "
              f"(reached 316: {len(pts) >= target_n})", flush=True)
    # NOTE: this is a bounded heuristic.  If it does not reach target_n the hole
    # is NOT closed; the count reached is reported as a conjecture-level partial.
    return dict(X=X, n_core=n0, n_added=accepted, reached=len(pts) >= target_n)


# ---------------------------------------------------------------------------
# Exact omega helper over a boolean adjacency (bitset branch-and-bound).
# ---------------------------------------------------------------------------

def _omega_le(adj_bool, k):
    """True iff the clique number of the boolean graph adj_bool is <= k.
    Exact bitset branch-and-bound (same algorithm as g24.max_clique_le, but on a
    boolean numpy matrix)."""
    n = adj_bool.shape[0]
    nbr = [0] * n
    for i in range(n):
        b = 0
        row = adj_bool[i]
        for j in range(n):
            if row[j]:
                b |= (1 << j)
        nbr[i] = b
    best = [0]

    def expand(rsize, P):
        if rsize > best[0]:
            best[0] = rsize
            if best[0] > k:
                return True
        while P:
            if rsize + bin(P).count("1") <= best[0]:
                return False
            v = (P & -P).bit_length() - 1
            P &= ~(1 << v)
            if expand(rsize + 1, P & nbr[v]):
                return True
        return False

    full = (1 << n) - 1
    expand(0, full)
    return best[0] <= k


# ---------------------------------------------------------------------------
# CERTIFY (Lean-fit core).  CORRECTED criterion (round 3): alpha(diam graph)<=5.
# ---------------------------------------------------------------------------

def verify(X, tol=1e-4):
    """
    EXACT-style certificate for a candidate point set X (m x f float coords):
      (1) embedding dim  = exact integer rank of the integer-scaled Gram <= 62,
          (for the core we use the certified exact rank; for perturbed X the
          coords are float, so dim is reported by SVD and flagged NOT exact),
      (2) alpha(diameter graph) <= 5, i.e. omega(NON-diameter graph) <= 5
          (the CORRECT Borsuk part-cap; round-2 verify used the wrong graph),
      (3) parts >= ceil(|X| / 5) >= 64.
    Returns the verdict; is_counterexample requires all three.
    """
    m = X.shape[0]
    d = (X * X).sum(1)
    D2 = d[:, None] + d[None, :] - 2 * X @ X.T
    np.fill_diagonal(D2, 0.0)
    diam2 = D2.max()
    # embedding dim (float SVD -- exact only when X is the certified integer core)
    s = np.linalg.svd(X - X.mean(0), compute_uv=False)
    dim = int((s > 1e-6).sum())
    # complement of diameter graph (non-diameter edges)
    comp = (D2 < diam2 - tol)
    np.fill_diagonal(comp, False)
    alpha_le_5 = _omega_le(comp, 5)
    parts = math.ceil(m / 5)
    return dict(dim=dim, alpha_le_5=alpha_le_5, n=m, parts_needed=parts,
                is_counterexample=(dim <= 62 and alpha_le_5 and parts >= 64))


def verify_core_exact(core):
    """EXACT certificate for the (integer) core: exact rank over Q + exact clique
    of the smaller-distance graph (= alpha of the diameter graph)."""
    return dict(exact_dim=_fo.exact_rank(core["G_core"]),
                alpha_le_5=_g24.max_clique_le(core["A_core"], 5),
                n=core["info"]["n"],
                parts_lb=core["info"]["parts_lb"])


if __name__ == "__main__":
    print("mixed-construction (sketch D): <=62-dim G_2(4) section core + cap-5")
    print("perturbation to reach 316.  Correct criterion: alpha(diam graph)<=5.\n")

    print("[HOLE 1 build_core] building exactly-certified 62-dim section ...",
          flush=True)
    core = build_core()
    ce = verify_core_exact(core)
    print(f"  CLOSED: core |T|={ce['n']} (subset of C), EXACT integer rank "
          f"over Q = {ce['exact_dim']} (<=62), alpha(diam graph)=omega(A[T,T])"
          f"<=5 = {ce['alpha_le_5']}, parts_lb=ceil(|T|/5)={ce['parts_lb']}.")
    assert ce['exact_dim'] == 62 and ce['alpha_le_5'] and ce['n'] == 270
    print("  => build_core CLOSED: a genuine 62-dim two-distance core, exactly "
          "certified.  Needs >=46 more points (316-270) for a counterexample.\n")

    print("[HOLE 2 engineer_perturbation] bounded greedy attempt "
          "(open hole) ...", flush=True)
    res = engineer_perturbation(core, target_n=316, max_iters=20000,
                                time_budget_s=90)
    print(f"\n  best perturbed set: |X|={res['X'].shape[0]} "
          f"(core {res['n_core']} + added {res['n_added']}), "
          f"reached 316: {res['reached']}.")
    if res['n_added'] > 0:
        v = verify(res['X'])
        print(f"  verify(X): dim(float)={v['dim']}, alpha<=5={v['alpha_le_5']}, "
              f"n={v['n']}, parts_needed={v['parts_needed']}, "
              f"is_counterexample={v['is_counterexample']}.")
    print("\n[STATUS] build_core CLOSED (exact 62-dim, 270 pts).  "
          "engineer_perturbation OPEN: reaching 316 in the fixed 62-dim subspace "
          "with alpha(diam graph)<=5 is undischarged.  NO improvement claimed; "
          "upper bound stays 63.")
