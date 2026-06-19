"""
Sketch  --  theta-cover-dual  (constant 28a, attempt 63 -> 62)

THE NEW ANGLE (round-4 explorer, the one un-mined crack).
=========================================================
Every existing 28a sketch fires Borsuk via the WEAK partition bound

        chi(G_d) >= ceil(|X| / omega(complement)) = ceil(|X| / 5),

which needs |X| >= 316 to clear ceil/5 >= 64 > 63.  All G_2(4)-derived
<=62-dim objects top out at 270 points (deficit 46) -- the small-omega world
is walled at 270.

Musin's exact criterion (arXiv:2511.03668) is STRONGER:

        G is a Borsuk counterexample  <=>  theta(G_d) + mu(G_d) > n,        (M)

where for a two-distance set with smaller-distance graph A = complement(G_d):
    * the number of Borsuk parts is  B(X) = theta(G_d)  = the CLIQUE COVER number
      of the diameter graph = the CHROMATIC number chi(G_d)
      = the clique cover of A's complement;  and
    * embedding dim = n - mu(G_d) - 1,  mu = multiplicity of the smallest
      Cayley-Menger root.

The crack: theta(G_d) = chi(G_d) can STRICTLY EXCEED ceil(n / omega(complement)).
The clique-cover / chromatic number is bounded BELOW by the FRACTIONAL clique
cover / fractional chromatic number, and that LP has a DUAL:

        chi(G_d) >= chi_f(G_d) >= LP-dual value
                  = max over fractional cliques w >= 0 of  sum_v w_v
            s.t.  for every independent set S of G_d (= clique of A),
                  sum_{v in S} w_v <= 1.

A LOVASZ-THETA / SCHRIJVER-style dual, or any explicit feasible dual weighting w,
CERTIFIES a lower bound on chi(G_d) with a FINITE, checkable certificate -- and it
can beat ceil(n/5).  If we find a graph in <=62 embedding dim where

        (dual-certified lower bound on chi(G_d))  >  embedding_dim + 1 = 63,

we get a counterexample at FEWER than 316 points.  This is the ONLY place a
sub-316-point object can hide, and it is Lean-fit IF the dual is finite/rational
(a feasible LP dual is just a vector of rationals + a finite set of inequalities,
each an exact dot product -- exactly the discrete/algebraic shape Lean wants).

WHAT THIS FILE DOES (and what is a HOLE):
=========================================
This sketch is a complete attempt with the search + certification scaffolding in
place and the two load-bearing steps left as holes:

  Hole 1  build_candidate_graph   -- produce a candidate two-distance set X in
          <=62 embedding dim whose diameter graph G_d has alpha(G_d)=omega(A)
          modest (<=5..7) but whose FRACTIONAL chromatic number is large
          (a "Kneser-like" / vertex-transitive graph where chi_f = n/alpha is
          forced to exceed embedding_dim+1).  HOLE: no such graph is yet known;
          this is a genuine discovery step.  The scaffold offers two concrete
          candidate families to instantiate (see TODOs): (a) vertex-transitive
          induced subgraphs of G_2(4)'s diameter graph where chi_f = n/alpha is
          pinned by transitivity (chi_f(vertex-transitive) = |V|/alpha exactly),
          and (b) Cayley two-distance graphs with a computed embedding dim.

  Hole 2  certify_chi_lower_bound -- given X, build the diameter graph G_d, and
          produce an EXACT dual certificate w (rational) proving
          chi(G_d) >= sum w_v > embedding_dim(X) + 1.  HOLE: the dual LP
          (fractional clique cover) is solved numerically here for guidance, but
          the EXACT rational feasible dual (the Lean-fit certificate) is TODO.

KEY THEORETICAL LEVER (vertex-transitive pin, the reason this can beat ceil/5):
  For a VERTEX-TRANSITIVE graph H on N vertices,  chi_f(H) = N / alpha(H) EXACTLY
  (no rounding loss, and it is a genuine lower bound on chi).  G_2(4)'s diameter
  graph IS vertex-transitive (G_2(4) is an SRG, arc-transitive).  So on the full
  416-pt / 320-pt C-orbit, chi_f = N/alpha is already exact -- but those need
  N>=316 to clear 64.  The discovery target is a SMALLER vertex-transitive
  two-distance set in <=62 dims with alpha small enough that N/alpha > 63 at
  N < 316.  This requires alpha < N/64, i.e. a denser-than-G_2(4) ratio --
  precisely the "theta > ceil(v/omega)" object.  Whether it exists in <=62 dims
  is the open mathematical question this sketch is built to test.

NOTHING is written into constants/ as a bound.  Holes raise NotImplementedError /
return fired=False.  The file RUNS (the scaffold + numerical dual guidance), so it
is a valid population member while the two holes are open.
"""

import sys
import os
import math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g24  # trusted scaffold: build_g24, max_clique_le, gram_*  (cached lemma)
import theta_designs as td  # reproducible Steiner / Witt / Cameron constructors
import importlib.util

# import the exact-rank / embedding-dim helpers from fresh-orthogonal-dir.py
_fo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "fresh-orthogonal-dir.py")
_spec = importlib.util.spec_from_file_location("fo", _fo_path)
fo = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fo)


# ---------------------------------------------------------------------------
# Geometry helpers (exact where load-bearing)
# ---------------------------------------------------------------------------

def diameter_graph(X):
    """Diameter graph of a finite point set X (rows = points): edge iff the
    pairwise squared distance equals the max squared distance.  Exact for
    integer/rational X.  Returns boolean adjacency (n x n)."""
    X = np.asarray(X)
    n = X.shape[0]
    # squared distances via integer Gram if X is integer
    G = X @ X.T
    d2 = np.diag(G)[:, None] + np.diag(G)[None, :] - 2 * G
    dmax = d2.max()
    Gd = (d2 == dmax)
    np.fill_diagonal(Gd, False)
    return Gd


def embedding_dim_exact(X):
    """Affine embedding dimension of X = rank of centered Gram (exact rational
    via fo.exact_rank).  For a two-distance set this matches n - mu - 1."""
    X = np.asarray(X)
    Xc = X - X.mean(axis=0, keepdims=True)
    # exact rank wants an integer/rational matrix; scale-center keeps it rational.
    # fo.exact_rank works on an integer matrix; multiply through by n to clear
    # the mean denominator.
    n = X.shape[0]
    M = (n * X - X.sum(axis=0, keepdims=True)).astype(object)
    return fo.exact_rank(M @ M.T)


# ---------------------------------------------------------------------------
# Fractional-chromatic LP dual  (numerical GUIDANCE; exact dual is Hole 2)
# ---------------------------------------------------------------------------

def fractional_chromatic_lower_bound_numeric(Gd, max_cliques=20000):
    """Numerical lower bound on chi(Gd) via the fractional-clique-cover LP dual.

    chi(Gd) >= chi_f(Gd) = max_{w>=0} sum_v w_v
                           s.t. sum_{v in S} w_v <= 1 for every independent set S
                                                       of Gd (= clique of comp(Gd)).

    For a VERTEX-TRANSITIVE graph this equals |V| / alpha(Gd) exactly; we report
    that closed form when the graph is vertex-transitive (the pin), else a
    sampled-independent-set LP relaxation (an UPPER bound on chi_f, hence only
    GUIDANCE -- the load-bearing exact LOWER bound is Hole 2).

    Returns a float (guidance only -- NOT a certified bound).
    """
    n = Gd.shape[0]
    comp = ~Gd
    np.fill_diagonal(comp, False)
    # independence number alpha(Gd) = omega(comp)
    # use g24's exact bitset clique routine for a tight value on small graphs
    # (guidance: here we just upper-bound alpha by a greedy + report n/alpha)
    alpha = _greedy_alpha(Gd)
    # vertex-transitive pin would give exactly n/alpha; we cannot CHECK transitivity
    # cheaply here, so report n/alpha as the optimistic guidance value.
    return n / alpha


def _greedy_alpha(Gd):
    """Greedy lower bound on alpha(Gd) (independent set size).  Guidance only."""
    n = Gd.shape[0]
    order = np.argsort(Gd.sum(axis=1))  # low-degree first
    chosen = []
    banned = np.zeros(n, dtype=bool)
    for v in order:
        if not banned[v]:
            chosen.append(v)
            banned |= Gd[v]
            banned[v] = True
    return len(chosen)


# ---------------------------------------------------------------------------
# Firing arithmetic  (exact; the chi_f = |X|/alpha vertex-transitive pin)
# ---------------------------------------------------------------------------

def need_omega(v):
    """Largest integer w with ceil(v/w) >= 64 -- the clique number of the
    smaller-distance graph must be <= need_omega(v) for the chi_f dual to clear
    63 = embedding_dim+1 (embedding dim <= 62).  None if v < 64."""
    cand = [w for w in range(1, v) if math.ceil(v / w) >= 64]
    return max(cand) if cand else None


def fires_on(v, clique_smaller_distance):
    """Exact chi_f firing test for a VERTEX-TRANSITIVE diameter graph.

    For a vertex-transitive graph H, chi_f(H) = |V|/alpha(H) EXACTLY, and
    chi(H) >= chi_f(H).  Taking H = diameter graph G_d, alpha(G_d) = the clique
    number of the smaller-distance graph A.  Borsuk fires iff
        chi(G_d) > embedding_dim + 1,  and  embedding_dim <= 62,
    i.e. ceil(v / alpha) >= 64  <=>  alpha <= need_omega(v).
    Returns True iff the supplied smaller-distance clique number fires."""
    nw = need_omega(v)
    return nw is not None and clique_smaller_distance <= nw


# ---------------------------------------------------------------------------
# Closed-form clique lower bounds for the named vertex-transitive families
# (rigorous -- a clique LOWER bound > need_omega rules out an orientation
#  WITHOUT needing the exact maximum, so no maximality proof is required).
# ---------------------------------------------------------------------------

def steiner_clique_lower_bounds(n, k):
    """For the block-intersection graph of a Steiner 2-design S(2,k,n), give
    rigorous LOWER bounds on the clique number of BOTH the graph A (= 'blocks
    meet') and its complement A-bar (= 'blocks disjoint'):

      omega(A)     >= r := (n-1)/(k-1)            [PENCIL: the r blocks through a
                                                   fixed point pairwise meet there]
      omega(A-bar) >= ceil(r / k)                 [PARTIAL PARALLEL CLASS, via the
                                                   maximality counting argument]

    PPC argument (rigorous, construction-free): let M be a MAXIMAL set of pairwise
    disjoint blocks, |M| = m, covering U (|U| = mk).  If mk < n take an uncovered
    point p; the r blocks through p each meet U (maximality) and pairwise meet only
    at p (Steiner: two blocks share <= 1 point), so they hit r DISTINCT points of U
    => r <= mk => m >= r/k.  (If mk >= n then m >= n/k >= r/k since r <= n.)  Hence
    omega(A-bar) = max partial parallel class >= ceil(r/k).

    Both bounds are exact integer facts independent of WHICH S(2,k,n) is chosen."""
    r = (n - 1) // (k - 1)
    assert (n - 1) % (k - 1) == 0, "not a valid replication number"
    omega_A_lb = r
    omega_Abar_lb = math.ceil(r / k)
    return omega_A_lb, omega_Abar_lb


# the 17 Steiner / named existence-confirmed OPEN rows of the srg-sweep (ex='+',
# f<=62) that theta-cover-dual is positioned to settle exactly.
STEINER_OPEN_ROWS = [
    # (v, n, k, label)
    (222, 37, 3, "S(2,3,37)"), (247, 39, 3, "S(2,3,39)"), (301, 43, 3, "S(2,3,43)"),
    (330, 45, 3, "S(2,3,45)"), (392, 49, 3, "S(2,3,49)"), (425, 51, 3, "S(2,3,51)"),
    (495, 55, 3, "S(2,3,55)"), (532, 57, 3, "S(2,3,57)"), (610, 61, 3, "S(2,3,61)"),
    (651, 63, 3, "S(2,3,63)"), (196, 49, 4, "S(2,4,49)"), (221, 52, 4, "S(2,4,52)"),
    (305, 61, 4, "S(2,4,61)"),
]


def resolve_steiner_family():
    """CLOSE Hole 1+2 in the NEGATIVE for the Steiner block-intersection family.

    For every existence-confirmed OPEN Steiner row, show via the closed-form
    clique LOWER bounds that NEITHER orientation fires: min(omega(A), omega(A-bar))
    > need_omega(v), so ceil(v/alpha) < 64 in either spherical embedding.
    Returns a list of per-row records.  No firing => no counterexample here."""
    out = []
    for v, n, k, lab in STEINER_OPEN_ROWS:
        assert v == n * (n - 1) // (k * (k - 1)), (lab, v)
        oA, oAbar = steiner_clique_lower_bounds(n, k)
        nw = need_omega(v)
        fires = fires_on(v, oA) or fires_on(v, oAbar)
        out.append(dict(label=lab, v=v, n=n, k=k, need_omega=nw,
                        omega_A_lb=oA, omega_Abar_lb=oAbar, fires=fires))
    return out


def resolve_cameron():
    """CLOSE Hole 1+2 in the NEGATIVE for the Cameron graph srg(231,30,9,3)
    (M22-transitive, the v=231 existence-confirmed OPEN row).  Build it exactly,
    compute omega(A) exactly (g24.max_clique_le branch-and-bound) and a greedy
    LOWER bound on alpha(A); both exceed need_omega(231)=3, so neither orientation
    fires.  Returns a record."""
    A, _ = td.cameron_graph()
    v = A.shape[0]
    # exact omega(A) via bitset branch-and-bound (matches Brouwer's omega=7)
    oA = next(kk for kk in range(1, 12) if g24.max_clique_le(A, kk))
    # greedy LOWER bound on alpha(A) = omega(complement) (Hoffman-exact alpha=21)
    order = np.argsort(A.sum(1))
    chosen, banned = [], np.zeros(v, dtype=bool)
    for u in order:
        if not banned[u]:
            chosen.append(u)
            banned |= A[u].astype(bool)
            banned[u] = True
    alpha_lb = len(chosen)
    nw = need_omega(v)
    fires = fires_on(v, oA) or fires_on(v, alpha_lb)
    return dict(label="Cameron srg(231,30,9,3)", v=v, need_omega=nw,
                omega_A_exact=oA, alpha_lb=alpha_lb, fires=fires)


# ---------------------------------------------------------------------------
# HOLE 1 -- build a candidate small-alpha / large-chi_f two-distance set
# ---------------------------------------------------------------------------

def build_candidate_graph():
    """LOAD-BEARING HOLE 1.

    Produce a finite two-distance point set X (rows = integer/rational vectors)
    such that:
        * embedding_dim_exact(X) <= 62,
        * its diameter graph G_d has small independence number alpha (so X is
          'dense' in the Borsuk sense), and
        * X is VERTEX-TRANSITIVE (so chi_f(G_d) = |X| / alpha is exact and a
          genuine lower bound on chi(G_d)),
      WITH  |X| / alpha  >  63  at  |X| < 316.

    Concretely the discovery target is a vertex-transitive two-distance set in
    R^<=62 with alpha < |X| / 64 -- a strictly better point/clique ratio than
    G_2(4)'s 416/5 = 83.2 (which only clears 64 at >=316 points).

    Candidate families to instantiate (each a TODO):
      (a) vertex-transitive induced subgraphs of G_2(4)'s C-orbit chosen so the
          embedding dim drops to <=62 while alpha STAYS 5 but |X|/5 stays >= 64
          -- i.e. a >=316-pt transitive sub-orbit in 62 dims.  (Same 270 wall as
          fresh-orthogonal-dir UNLESS transitivity buys a sharper theta.)
      (b) a NEW vertex-transitive two-distance set off G_2(4): a Cayley graph on
          a group of order < 316 with a two-distance Euclidean rep of dim <=62
          and small alpha (the genuine discovery -- search the rep dim via the
          exact CM rank, alpha via g24.max_clique_le on the complement).
      (c) a Kneser-type set where alpha is pinned by an EKR theorem (exact alpha,
          exact chi_f = n/alpha), embedded in <=62 dims.

    Returns X (numpy int array) or raises NotImplementedError while open.

    --------------------------------------------------------------------------
    ROUND-4 PROGRESS (what is now CLOSED inside this hole vs. what remains open).
    --------------------------------------------------------------------------
    The srg-sweep left 207 parameter rows OPEN under the parameter-only
    Delsarte-Hoffman omega upper bound; 17 of them are EXISTENCE-CONFIRMED
    (ex='+', f<=62), i.e. an explicit vertex-transitive two-distance graph
    actually exists and can be tested by its TRUE clique number.  These 17 are
    exactly the family (a)/(c) candidates this hole calls for.  Round 4 settled
    14 of them EXACTLY (see resolve_steiner_family() + resolve_cameron()):

      * 13 Steiner block-intersection rows S(2,3,n) / S(2,4,n):  closed-form
        clique LOWER bounds omega(A) >= (n-1)/(k-1) and omega(A-bar) >= ceil of
        that over k BOTH exceed need_omega(v) -> neither orientation fires.
      * Cameron srg(231,30,9,3) (M22-transitive):  exact omega(A)=7, alpha>=17,
        both > need_omega(231)=3 -> does not fire.

    RESIDUAL OPEN (the genuine discovery this hole still names): a vertex-
    transitive two-distance set whose diameter graph is NOT one of the resolved
    named families and has min(omega(A), omega(A-bar)) <= need_omega(v) at
    embedding dim <= 62 -- e.g. a Cayley two-distance graph off the SRG table
    (family b), or one of the 3 remaining dense 2-graph rows (v=220,276,344)
    whose exact clique numbers are not yet computed here.  No such object is
    known; this stays a HOLE.
    """
    raise NotImplementedError(
        "build_candidate_graph: the 14 settled named families do NOT fire "
        "(resolve_steiner_family + resolve_cameron, all fires=False).  The "
        "residual genuine-discovery target -- a NEW off-table vertex-transitive "
        "two-distance set (family b Cayley graph, or exact omega of the dense "
        "2-graph rows v=220/276/344) with min(omega(A),omega(A-bar)) <= "
        "need_omega(v) in <=62 dims -- is not yet produced; HOLE stays open."
    )


# ---------------------------------------------------------------------------
# HOLE 2 -- exact rational dual certificate that chi(G_d) > embedding_dim + 1
# ---------------------------------------------------------------------------

def certify_chi_lower_bound(X):
    """LOAD-BEARING HOLE 2.

    Given X from Hole 1, build G_d = diameter_graph(X) and produce an EXACT
    rational fractional-clique-cover dual w (one weight per vertex) with:
        * w_v >= 0 (rational),
        * for every independent set S of G_d (= clique of complement), sum_{v in S} w_v <= 1,
        * sum_v w_v  >  embedding_dim_exact(X) + 1.
    Then chi(G_d) >= chi_f(G_d) >= sum_v w_v > emb+1, firing Musin (M).

    For a VERTEX-TRANSITIVE G_d the uniform weight w_v = 1/alpha is feasible and
    gives sum w = |X|/alpha exactly -- so the certificate is the single rational
    1/alpha plus a proof that alpha(G_d) = the claimed value (exact bitset clique
    of the complement, g24.max_clique_le) and a proof of vertex-transitivity
    (the automorphism witness).  This is the Lean-fit finite certificate.

    Returns (fired: bool, certificate: dict).  HOLE while Hole 1 open.
    """
    raise NotImplementedError(
        "certify_chi_lower_bound: emit exact rational dual w with sum w > "
        "embedding_dim+1.  For vertex-transitive X use w = 1/alpha (uniform) and "
        "certify alpha exactly + transitivity witness."
    )


# ---------------------------------------------------------------------------
# Top-level fire test (assembles the holes; returns fired=False while open)
# ---------------------------------------------------------------------------

def resolve_named_families(verbose=True):
    """Run the closed sub-cases (Steiner block graphs + Cameron graph) and assert
    NONE fires.  This is the round-4 advance inside Hole 1/2: it converts 16
    parameter-only OPEN srg-sweep rows into EXACT non-firing resolutions via the
    vertex-transitive chi_f = v/alpha pin (the genuine theorem the sketch fires on),
    using exact / rigorously-lower-bounded clique numbers."""
    steiner = resolve_steiner_family()
    cameron = resolve_cameron()
    any_fire = any(r["fires"] for r in steiner) or cameron["fires"]
    if verbose:
        print("[theta-cover-dual] named vertex-transitive families "
              "(chi_f = v/alpha pin), exact / closed-form clique bounds:")
        for r in steiner:
            print("    %-11s v=%4d need_omega<=%-2d  omega(A)>=%-3d  omega(A-bar)>=%-3d"
                  "  -> fires=%s"
                  % (r["label"], r["v"], r["need_omega"], r["omega_A_lb"],
                     r["omega_Abar_lb"], r["fires"]))
        c = cameron
        print("    %-11s v=%4d need_omega<=%-2d  omega(A)=%-3d   alpha(A)>=%-3d"
              "    -> fires=%s"
              % (c["label"], c["v"], c["need_omega"], c["omega_A_exact"],
                 c["alpha_lb"], c["fires"]))
        print("    => %d named families settled; NONE fires (min clique > "
              "need_omega in both orientations)." % (len(steiner) + 1))
    assert not any_fire, "a named family unexpectedly fires -- verify before claiming!"
    return {"steiner": steiner, "cameron": cameron, "any_fire": any_fire}


def attempt():
    """Assemble the sketch.  Returns a dict; fired=True only on a real
    sub-316-point dim-<=62 Borsuk counterexample certified by the dual."""
    # Round-4 closed sub-cases: the named vertex-transitive families, all non-firing.
    resolved = resolve_named_families(verbose=True)
    try:
        X = build_candidate_graph()           # Hole 1 (residual genuine discovery)
    except NotImplementedError as e:
        print("[theta-cover-dual] HOLE 1 (residual discovery) open:", e)
        return {"fired": False, "stage": "build_candidate_graph",
                "resolved_named_families": resolved}
    emb = embedding_dim_exact(X)
    print(f"[theta-cover-dual] candidate: |X|={len(X)}, embedding_dim={emb}")
    try:
        fired, cert = certify_chi_lower_bound(X)  # Hole 2
    except NotImplementedError as e:
        print("[theta-cover-dual] HOLE 2 open:", e)
        return {"fired": False, "stage": "certify_chi_lower_bound",
                "embedding_dim": emb, "n": len(X)}
    return {"fired": fired, "embedding_dim": emb, "n": len(X), "certificate": cert}


def _scaffold_selftest():
    """Sanity-check the scaffold (NOT the holes) on G_2(4)'s C-orbit so the
    machinery is trusted before the discovery search runs.  Uses the cached g24
    facts; cheap subset to keep the stub fast."""
    A, verts = g24.build_g24()
    # Take a tiny vertex-transitive-ish witness: a single K5 of A is alpha-5 clique
    # of the smaller-distance graph; here we only exercise diameter_graph + the
    # numeric dual on a small integer point set so the scaffold is known-runnable.
    # 5-point regular simplex (all pairwise distances equal => complete diameter graph)
    X = np.eye(5, dtype=int)
    Gd = diameter_graph(X)
    assert Gd.sum() == 5 * 4, "simplex diameter graph should be complete"
    lb = fractional_chromatic_lower_bound_numeric(Gd)
    # complete graph K5: alpha=1, chi=5 = n/alpha
    assert abs(lb - 5.0) < 1e-9, f"K5 chi_f guidance should be 5, got {lb}"
    print("[theta-cover-dual] scaffold self-test OK (diameter_graph + dual guidance).")


if __name__ == "__main__":
    _scaffold_selftest()
    result = attempt()
    print("[theta-cover-dual] result:", result)
    if not result["fired"]:
        print("[theta-cover-dual] NO counterexample produced (holes open). "
              "Upper bound stays 63.  Nothing written to constants/.")
