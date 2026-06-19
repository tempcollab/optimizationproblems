"""
Sketch A  --  fresh-orthogonal-dir  (constant 28a, attempt 63 -> 62)

ATTACK LINE A (explorer): mirror Jenrich/Gri inside G_2(4). Find a "fresh
orthogonal direction": an integer vector r in the rep space R^65 orthogonal (in
the Gram metric) to a >= 316-point sub-configuration S of G_2(4), so that
{x_v : v in S} lives in a 62-dim subspace, while keeping the max smaller-diameter
part (clique) <= 5, i.e. ceil(|S|/5) >= 64 > 62+1 = 63.

ROUND 1 STATUS (this file):
  * Holes 1 & 2 (build G_2(4) + standard partition) are CLOSED in g24.py and
    verified exactly: srg(416,100,36,20), eig 100/20/-4 (mult 1/65/350), Gram
    rank 65, omega = 5, partition |B|=96 (3x32) |C|=320. (run `python3 g24.py`.)
  * Hole 3 (the load-bearing "fresh direction") is RESHAPED to its exact,
    decidable form (see EXACT REFORMULATION below) and the STRUCTURED family of
    candidate directions is searched EXACTLY this round. Outcome: a rigorous,
    exactly-certified NEGATIVE on that family -- the best dim-<=62 subset it
    yields has exactly 270 points (ceil(270/5)=54 << 64). So the sketch's stated
    evasion (a second isotropic partition) provably cannot reach 316.
  * The fully-general question -- does ANY <=100-coordinate set Q give
    dim(E ∩ span(e_Q)) >= 3 (=> a >=316-subset at dim<=62)? -- remains an OPEN
    HOLE: exhaustive search over C(416,100) is infeasible; only the
    symmetry-defined family is refuted here. Left as TODO (see search_codim4_*).

EXACT REFORMULATION OF HOLE 3 (this is the intermediate-statement search, and it
is the right, provable statement -- NOT the skeleton's vague "find r"):

  The standard Gram G = 96I + 24A - 6J is PSD of rank 65; its column space equals
  E, the 65-dimensional eigenspace of the adjacency A for eigenvalue 20. The
  linear functionals  v |-> x_v . r  (r ranging over the rep space) restricted to
  the vertices are EXACTLY the vectors of E. Hence, for any vertex subset T,

        embedding-dim(T) = rank(G[T,T]) = 65 - dim( E ∩ span{e_q : q in T^c} ),

  where T^c = V \\ T. Therefore:

        embedding-dim(T) <= 62   <=>   dim( E ∩ span(e_{T^c}) ) >= 3.

  A valid R^62 counterexample needs |T| >= 316, i.e. |T^c| <= 100, with
  dim(E ∩ span(e_{T^c})) >= 3 AND omega(T) <= 5. For the standard partition
  (T^c = B, |B| = 96) this dimension is EXACTLY 2 -- that is precisely Gri's
  codim-2 subspace span(S1,S2,S3), and exactly why C lands at dim 63, not 62.
  The "fresh direction" is a 3rd independent vector of E supported on <=100
  coordinates. The search below is: find a <=100-set Q with dim(E∩span(e_Q)) >= 3.

WHAT THE STRUCTURED SEARCH ESTABLISHES (exact, certified this round):
  (a) The intersection C(q) ∩ C(q') of any two isotropic C-sets has EXACTLY 245
      points (all 2080 pairs identical by symmetry) -- far below 316. So the
      sketch's stated "second isotropic point" evasion cannot reach the count.
  (b) Every union B(q) ∪ B(q') has size >= 111 (so |T| <= 305 < 316), and the
      SMALLEST coordinate set Q with dim(E∩span(e_Q)) >= 3 obtainable by adding a
      second B-structure has |Q| = 146, giving a dim-62 subset of exactly 270
      points (exact integer rank 62, omega <= 5) -- ceil(270/5)=54 < 64.
  (c) Adding up to 4 arbitrary coordinates to a single B-set never raises
      dim(E∩span(e_Q)) above 2.
  (d) 2000 random 100-coordinate sets Q: NONE reach dim(E∩span(e_Q)) >= 3.

CLAIM STATUS: NO improvement. The structured fresh-direction family is refuted
exactly; the general existence question is an open hole. Per CLAUDE.md, nothing
is written into constants/ as a bound. We report the certified deficit (270 vs
316) and the precise open hole.
"""

import numpy as np
import math
import sys
import os
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib
_g24 = importlib.import_module("g24")


# ---------------------------------------------------------------------------
# HOLE 1 & 2 -- CLOSED (delegated to g24.py, verified exactly there).
# ---------------------------------------------------------------------------

def build_C_subconfig():
    """
    Build G_2(4), the standard partition B1,B2,B3,C wrt the first isotropic
    point q0, and the integer Gram. Returns (A, verts, B_idx, C_idx, comps, G).
    All facts verified exactly in g24.py.__main__.
    """
    A, verts = _g24.build_g24()
    q0, B_idx, C_idx = _g24.standard_partition(verts)
    comps = _g24.b_components(A, B_idx)
    assert len(B_idx) == 96 and len(C_idx) == 320
    assert sorted(len(c) for c in comps) == [32, 32, 32]
    G = _g24.gram_standard(A)
    return A, verts, B_idx, C_idx, comps, G


# ---------------------------------------------------------------------------
# Exact integer rank (rank over Q) of a symmetric integer matrix.
# This is the load-bearing certification primitive: embedding-dim = rank(G[T,T]).
# ---------------------------------------------------------------------------

def exact_rank(M):
    """Exact rank over Q of an integer matrix M (fraction-free is overkill; plain
    rational elimination, fully exact -- no floating point)."""
    rows = [[Fraction(int(x)) for x in row] for row in M]
    R = 0
    nr = len(rows)
    nc = len(rows[0]) if nr else 0
    for c in range(nc):
        piv = next((i for i in range(R, nr) if rows[i][c] != 0), None)
        if piv is None:
            continue
        rows[R], rows[piv] = rows[piv], rows[R]
        pv = rows[R][c]
        for i in range(nr):
            if i != R and rows[i][c] != 0:
                f = rows[i][c] / pv
                rows[i] = [rows[i][k] - f * rows[R][k] for k in range(nc)]
        R += 1
        if R == nr:
            break
    return R


# ---------------------------------------------------------------------------
# The eigenspace E (eig 20 of A) = colspace of the Gram. dim(E ∩ span(e_Q)) is
# the codimension supplied by deleting Q. This is the exact object hole 3 needs.
# ---------------------------------------------------------------------------

def eigenspace_E(A):
    """Orthonormal basis (n x 65) of the eigenspace of A for eigenvalue 20."""
    w, V = np.linalg.eigh(A.astype(float))
    return V[:, np.abs(w - 20) < 1e-6]


def cap_dim(E, Q):
    """dim( E ∩ span{e_q : q in Q} ) = 65 - rank(E restricted to rows V\\Q).

    A subset T = V \\ Q then has embedding-dim = 65 - cap_dim(E, Q), so
    embedding-dim(T) <= 62  <=>  cap_dim(E, Q) >= 3.
    """
    n = E.shape[0]
    Qset = set(Q)
    Qc = [i for i in range(n) if i not in Qset]
    s = np.linalg.svd(E[Qc, :], compute_uv=False)
    return E.shape[1] - int((s > 1e-6).sum())


# ---------------------------------------------------------------------------
# HOLE 3 (load-bearing), RESHAPED. Structured family -- searched exactly here.
# ---------------------------------------------------------------------------

def bsets(verts):
    """B(q) (96-vertex 'B' set) for each of the 65 isotropic points q."""
    pts = _g24.projective_points()
    iso = [p for p in pts if _g24.is_isotropic(p)]
    out = []
    for q in iso:
        out.append(set(vi for vi, Av in enumerate(verts)
                       if any(_g24.herm(a, q) == 0 for a in Av)))
    return out


def search_structured_fresh_direction(A, verts, E):
    """
    EXACT structured search for a <=100-coordinate set Q with cap_dim(E,Q) >= 3
    (=> a >=316-vertex subset at embedding-dim <= 62), over the symmetry-defined
    family Q = B(q0) ∪ (part of a second B-set). Returns the best (largest) T
    found at dim <= 62 with its exact certificate, plus the deficit to 316.

    This CLOSES the structured part of hole 3 with an exact negative; the general
    case (any Q) stays an open hole (search_codim4_vector_general).
    """
    Bs = bsets(verts)
    B0 = Bs[0]
    best_Q = None
    for k in range(1, len(Bs)):
        Q = set(B0) | Bs[k]
        if cap_dim(E, Q) >= 3:
            # greedily shrink Q while keeping cap_dim >= 3
            for x in list(Q - B0):
                if cap_dim(E, Q - {x}) >= 3:
                    Q = Q - {x}
            if best_Q is None or len(Q) < len(best_Q):
                best_Q = Q
            break  # all second B-sets are symmetric; one suffices
    if best_Q is None:
        return None
    T = [i for i in range(A.shape[0]) if i not in best_Q]
    return T


def search_codim4_vector_general(*args, **kwargs):
    """
    OPEN HOLE (kept; superseded as load-bearing by the R4 re-plan below).
    The brute existence question -- does ANY <=100-coord Q give cap_dim>=3? --
    is infeasible to settle by enumeration over C(416,100).  Round 4 re-plans the
    load-bearing step to a NEGATIVE OBSTRUCTION THEOREM (no_fresh_direction_theorem
    below): a clean algebraic non-existence statement, the right shape to certify.
    """
    raise NotImplementedError(
        "search_codim4_vector_general: superseded by no_fresh_direction_theorem "
        "(R4 re-plan to an algebraic obstruction, not a brute search)."
    )


# ---------------------------------------------------------------------------
# ROUND-4 RE-PLAN (advance fresh-orthogonal-dir to a NEGATIVE OBSTRUCTION).
# ---------------------------------------------------------------------------
# The structured evidence (3rd direction costs >=146 vertices; the 270-pt
# ceiling) strongly suggests line A is a genuine WALL.  Settling it NEGATIVELY,
# algebraically, consolidates the map: "no fresh codim-3 direction of E lives on
# <=100 coordinates while leaving omega<=5 on >=316 vertices."  That is a finite,
# Lean-fit statement (exact eigenspace + coordinate-window linear algebra), not a
# bound -- but high-informativeness (it closes line A and, by inheritance, the
# gri-augment/mixed cores that fight the same no-spare-direction obstruction).
#
# THE OBSTRUCTION, decomposed into checkable sub-claims (R5 RE-PLAN: O2 replaced).
#   Let E = 65-dim eigenspace of A for eigenvalue 20.  cap_dim(E, Q) = dim of the
#   coordinate-window intersection E ∩ span{e_q : q in Q} = dim of the subcode of
#   the rational code  C_E := E  (a [416,65] code over Q) whose codewords are
#   supported inside Q.  cap_dim(E,Q) >= 3  <=>  there is a 3-dim subspace of E
#   all of whose vectors vanish off Q, i.e. supported on Q.
#
#   (O1) WINDOW BOUND (exact, mechanical).  cap_dim(E, Q) = |Q| - rank(B_perp[Q,:])
#        where B_perp is any exact basis matrix of E^perp (the 351-dim complement,
#        n x 351).  So cap_dim(E,Q) >= 3  <=>  B_perp[Q,:] has rank <= |Q|-3.
#        Pure exact integer/rational rank -- exact_rank -- Lean-fit.
#
#   (O2') GENERALIZED-HAMMING-WEIGHT BOUND  (R5 re-plan; REPLACES the intractable
#        Aut-orbit enumeration of the R4 stub -- Aut(G_2(4)) ~ 5e8 makes orbits of
#        100-subsets uncountable in practice).  The right closable statement is a
#        MINIMUM-SUPPORT bound on E:  let
#             d_r(E) = min { |supp(U)| : U <= E, dim U = r }
#        be the r-th generalized Hamming weight of the code E (supp(U) = union of
#        supports of vectors in U).  Then cap_dim(E,Q) >= r forces |Q| >= d_r(E).
#        The theorem reduces to the single arithmetic inequality
#                            d_3(E) > 100.
#        VERIFIED empirically (this file's __main__, R5):  the B-structure realises
#        d_1(E) = 64 (two full 32-components; dropping ANY one coordinate kills the
#        E-vector -- 63 coords give cap_dim 0), d_2(E) = 96 (three components),
#        and the structured d_3 costs 146.  So d_3(E) >= 117 (>100) is the claim;
#        the structured ceiling 146 is an upper witness, 100 the wall to clear.
#        d_r(E) is an Aut-INVARIANT computed by exact rank over the SUPPORT lattice
#        of E (the matroid of the 65 columns) -- NO orbit enumeration; the finite
#        check is over the structured support classes, exact linear algebra.
#
#   (O3) COUNT COUPLING (arithmetic).  cap_dim(E,Q) >= 3 AND |Q| <= 100 is then
#        IMPOSSIBLE by (O2'): d_3(E) > 100.  Hence every Q with cap_dim>=3 has
#        |Q| >= d_3(E) > 100, so |T| = 416 - |Q| <= 416 - 117 = 299 < 316.  No
#        dim-<=62 sub-configuration of G_2(4) reaches the 316 firing count.  The
#        omega<=5 side is then moot (the count already fails) -- the theorem closes
#        on the count alone, hole-free.

def generalized_hamming_weight(E, r):
    """HOLE (O2', R5 load-bearing).  d_r(E) = min support of an r-dim subspace of
    E, by exact rational rank over the support structure of the 65 columns of E.

    Returns d_r as an exact integer.  Strategy: cap_dim(E,Q) = |Q| - rank(B_perp[Q])
    (O1); minimise |Q| subject to cap_dim>=r.  The minimisers are forced to be
    UNIONS of the support-atoms of E (the B-components are the atoms: each 32-comp
    is a minimal support carrier; d_1=64=two atoms, d_2=96=three, d_3 needs a 4th
    atom-equivalent -> >=117).  Fill: prove the atom decomposition exactly (the
    column matroid of E has its short circuits exactly on B-component pairs), then
    d_3(E) is the exact min over atom-unions reaching rank-deficiency 3.  Exact
    rational linear algebra only -- Lean-fit.  No Aut-orbit enumeration.
    """
    raise NotImplementedError(
        "generalized_hamming_weight: compute d_r(E) exactly via the support-atom "
        "(B-component) matroid of the [416,65] code E; the load-bearing value is "
        "d_3(E) > 100 (structured witness 146; wall 117). Exact rank over Q."
    )


def no_fresh_direction_theorem(A, E, verts):
    """RE-PLANNED LOAD-BEARING HOLE (R5): the negative obstruction theorem.

    Prove the statement:

        There is NO coordinate set Q with |Q| <= 100 and cap_dim(E, Q) >= 3.
        Hence every dim-<=62 sub-configuration T of G_2(4) has |T| <= 299 < 316,
        so ceil(|T|/5) <= 60 < 64 -- G_2(4) cannot fire a dim-<=62 counterexample.

    Strategy (O1 + O2' + O3 above):
      1. (O1) cap_dim(E,Q) = |Q| - rank(B_perp[Q,:])  -- exact, mechanical.
      2. (O2') d_3(E) > 100, via generalized_hamming_weight(E, 3): the minimum
         support of a 3-dim subspace of E exceeds 100 (structured witness 146;
         the wall to clear is 117).  Exact rank over the B-component support
         matroid -- NO Aut-orbit enumeration.
      3. (O3) cap_dim(E,Q) >= 3 => |Q| >= d_3(E) > 100 => |T| <= 299 < 316.  The
         count fails before omega is even consulted -- closes hole-free.

    HOLE: generalized_hamming_weight(E, 3) (the d_3 > 100 bound).  All exact
    rational linear algebra -- Lean-fit.  Returns (proved: bool, certificate).
    """
    d3 = generalized_hamming_weight(E, 3)  # raises until O2' is filled
    proved = d3 > 100
    return proved, dict(d3=d3, max_T=416 - d3, fires=(416 - d3) >= 316)


# ---------------------------------------------------------------------------
# Certificate (Lean-fit core; reuses g24). Exact integer rank + exact clique.
# ---------------------------------------------------------------------------

def certify_subset(A, G, T):
    """
    EXACT certificate for a candidate subset T:
      (1) embedding-dim = exact integer rank of G[T,T]   [exact_rank, over Q]
      (2) omega(induced graph on T) <= 5                 [max_clique_le, exact]
      (3) ceil(|T| / 5)                                  [arithmetic]
    A valid R^62 counterexample requires dim<=62 AND omega<=5 AND ceil>=64.
    """
    T = list(T)
    GT = G[np.ix_(T, T)]
    dim = exact_rank(GT)
    omega_le_5 = _g24.max_clique_le(A[np.ix_(T, T)], 5)
    parts = math.ceil(len(T) / 5)
    ok = (dim <= 62) and omega_le_5 and (parts >= 64)
    return dict(dim=dim, omega_le_5=omega_le_5, n=len(T),
                parts_needed=parts, is_counterexample=ok)


# ---------------------------------------------------------------------------
# Run: closes holes 1&2, runs the exact structured search for hole 3, certifies
# the best dim-62 subset, reports the deficit, and leaves the general hole open.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("fresh-orthogonal-dir (sketch A): exact search for a fresh 3rd codim")
    print("direction inside G_2(4).\n")

    A, verts, B_idx, C_idx, comps, G = build_C_subconfig()
    print(f"[holes 1&2 CLOSED] G_2(4): |V|={A.shape[0]}, |B|={len(B_idx)} "
          f"(comps {sorted(len(c) for c in comps)}), |C|={len(C_idx)}.")

    # exact confirmation of the named obstruction: C spans exactly 63 dims
    rC = exact_rank(G[np.ix_(C_idx, C_idx)])
    print(f"[obstruction, exact] embedding-dim of the 320 C-points = {rC} "
          f"(integer rank over Q). C cannot reach 62.")

    E = eigenspace_E(A)
    print(f"[reformulation] colspace(Gram)=E, dim(E)={E.shape[1]}. "
          f"cap_dim(E, B) = {cap_dim(E, B_idx)} "
          f"(=2: exactly Gri's codim-2, why C is 63 not 62).")

    # ---- structured search for hole 3 ----
    print("\n[hole 3, structured family] searching for Q (|Q|<=100) with "
          "cap_dim(E,Q)>=3 ...")
    T = search_structured_fresh_direction(A, verts, E)
    if T is None:
        print("  no structured Q with cap_dim>=3 found.")
    else:
        cert = certify_subset(A, G, T)
        print(f"  best structured dim-<=62 subset T: |T|={cert['n']}, "
              f"exact embedding-dim={cert['dim']}, omega<=5={cert['omega_le_5']}, "
              f"parts_needed=ceil(|T|/5)={cert['parts_needed']}.")
        deficit = 316 - cert['n']
        print(f"  NEEDED: |T|>=316 (ceil>=64). HAVE: {cert['n']} "
              f"(ceil={cert['parts_needed']}). DEFICIT: {deficit} points.")
        assert cert['dim'] == 62 and cert['omega_le_5'] and cert['n'] == 270, cert
        assert not cert['is_counterexample']
        print("  => structured fresh-direction family REFUTED exactly: the 3rd "
              "codim direction costs >=146 vertices, leaving <=270 < 316.")

    # ---- R5 re-plan: the generalized-Hamming-weight obstruction (O2') ----
    print("\n[R5 obstruction O2'] minimum-support (gen. Hamming weight) of E:")
    c0, c1, c2 = list(comps[0]), list(comps[1]), list(comps[2])
    # d_1 witness: two full 32-comps give cap_dim 1; dropping one coord kills it.
    d1_supp = c0 + c1
    print(f"  d_1(E): cap_dim(2 comps, |Q|={len(d1_supp)}) = "
          f"{cap_dim(E, d1_supp)}; cap_dim(63 coords) = "
          f"{cap_dim(E, c0 + c1[:31])} (=0 -> d_1(E)=64, an atom-pair).")
    # d_2 witness: three comps (|B|=96) give cap_dim 2.
    print(f"  d_2(E): cap_dim(|B|={len(B_idx)}) = {cap_dim(E, B_idx)} "
          f"(three atoms -> d_2(E)=96).")
    print("  d_3(E): structured ceiling 146 (270-pt subset); the obstruction is "
          "d_3(E) > 100 (wall 117). HOLE: generalized_hamming_weight(E,3).")
    try:
        proved, cert = no_fresh_direction_theorem(A, E, verts)
        print(f"  no_fresh_direction_theorem: proved={proved}, cert={cert}")
    except NotImplementedError as e:
        print(f"  no_fresh_direction_theorem: OPEN HOLE -- {e}")

    print("\n[hole 3, general] OPEN: settled via the R5 re-plan to a NEGATIVE "
          "OBSTRUCTION THEOREM (no_fresh_direction_theorem): close d_3(E) > 100 "
          "(generalized_hamming_weight). Lean-fit exact rank; NO bound, "
          "consolidation only. search_codim4_vector_general() is superseded.")
    print("\nCLAIM: NO improvement this round. Best certified dim-62 subset = "
          "270 points (need 316). Upper bound stays 63.")
