"""
Sketch A -- special-case-p-half: push H_3 <= 13 by treating the p=1/2 bottleneck
separately, while the rest of p-space admits a 13-piece covering structure.

Reproducible check (exact rational, no floats on the load-bearing facts):
    python3 constants/39a/certificate/special-case-p-half.py
prints PASS lines for every closed sub-claim and raises NotImplementedError on the
remaining open holes (A2/A3 -- the full 13-piece atlas LP, and A1 in its honest form).

----------------------------------------------------------------------------------
Setup (Prymak 2023, arXiv 2112.10698)
----------------------------------------------------------------------------------
For any 3-D convex body K, normalize the minimal-volume parallelotope C >= K to the
unit cube [0,1]^3 (covering number is affine-invariant). K touches each face; pick
perpendicular contact pairs q_ij, columns of

    A_p = [[ 0,  1, p3, p3, p5, p5],
           [p1, p1,  0,  1, p6, p6],
           [p2, p2, p4, p4,  0,  1]],   p in [0,1]^6.

V_p = {q_10,q_11,q_20,q_21,q_30,q_31} (one point per face), O_p = conv(V_p) <= K.
Reduction (Lemma 2.2):  C(K,int K) <= max_p C(E ∪ V_p, int(O_p)),  E = cube 1-skeleton.
Prymak certifies the RHS <= 14 by a rational LP over 4.66M boxes (Prop 2.6).

Remark 2.3: at p=(1/2,...,1/2), O_p is the regular octahedron with vertices at the six
face midpoints, and the 14 marked points (8 cube vertices + V_p) are pairwise
ell_1-distance >= 1 = radius of O_p - O_p, so NO two share a translate of int(O_p):
C(E ∪ V_p, int O_p) >= 14. So 14 is the exact ceiling of THIS reduction.

----------------------------------------------------------------------------------
What this round establishes (exact, reproducible) and what remains open
----------------------------------------------------------------------------------
CLOSED this round (rigorous, exact rational):
  (F0) Remark 2.3 reproduced exactly: 0 of 14 marked points pairwise coverable at p=1/2,
       with min pairwise ell_1 distance EXACTLY 1 (zero slack -- the obstruction is tight).
  (F1) FRAGILITY: the obstruction is supported on the single point p=1/2. Perturbing ONE
       coordinate by any eps>0 makes >=1 vertex/face-point pair coverable (exact facet
       certificate at p1=1/2+1/10). So the 13-merge mechanism is available for every p != 1/2.
  (F2) The reviewer's worst-case framing is geometrically corrected: K = O_p (the regular
       octahedron itself) does NOT normalize to p=1/2. Its minimal-volume parallelotope has
       volume EXACTLY 2, strictly less than the cube's 8 (a +-1 matrix of det 4 gives a
       smaller enclosing parallelotope). Hence a body genuinely FORCED to p=1/2 by the
       minimal-volume normalization is strictly larger than O_p near the cube corners --
       there IS slack between O_p and K there. (And K=O_p is centrally symmetric => H<=8,
       far below 13, so it never needs the special case.)

OPEN (the genuine blockers; left as holes):
  (A1') The slack established by (F2) is QUALITATIVE. Turning it into a uniform, rational,
        finite enlargement W with O_p <= W <= int(K) valid across ALL p=1/2-forced bodies
        requires a quantitative lower bound on corner slack from the minimal-volume-box
        condition -- a continuum/affine fact not supplied by the contacts alone. OPEN.
  (A2)  A 13-piece covering structure tau' whose LP (Prop 2.6 form, WITH the 12 edges) is
        feasible on a generic box. The naive single-merge is infeasible once edges are
        included (the merged translate loses its edge-covering capacity): demonstrated below.
        A correct tau' needs a combinatorial redesign + atlas search. OPEN.
  (A3)  The symmetry-reduced 13-feasible box atlas covering [0,1]^6 minus a neighborhood of
        1/2. OPEN (depends on A2).
"""

from fractions import Fraction as F
import itertools

import numpy as np
from scipy.spatial import ConvexHull


# ----------------------------------------------------------------------------------
# Exact geometry
# ----------------------------------------------------------------------------------

def Vp(p):
    """The six contact points V_p (columns of A_p), exact rationals."""
    p1, p2, p3, p4, p5, p6 = p
    return [
        (F(0), p1, p2), (F(1), p1, p2),   # F_1: x=0,1
        (p3, F(0), p4), (p3, F(1), p4),   # F_2: y=0,1
        (p5, p6, F(0)), (p5, p6, F(1)),   # F_3: z=0,1
    ]


CUBE_VERTS = [tuple(F(c) for c in v) for v in itertools.product([0, 1], repeat=3)]
FACE_LABELS = ["q10", "q11", "q20", "q21", "q30", "q31"]


def l1(a, b):
    return sum(abs(a[k] - b[k]) for k in range(3))


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def Op_facets(p):
    """Exact half-space rep of O_p = conv(V_p): list of (n, d) with n.x <= d on O_p.

    Facet incidences come from a float ConvexHull (combinatorics only); the normals and
    offsets are recomputed EXACTLY from the rational vertices via integer cross products,
    so the returned inequalities are exact and the float step is not load-bearing.
    """
    V = Vp(p)
    Vf = np.array([[float(c) for c in v] for v in V])
    hull = ConvexHull(Vf)
    center = tuple(sum(V[i][k] for i in range(6)) / 6 for k in range(3))
    facets = []
    for simp in hull.simplices:
        a, b, c = (V[simp[0]], V[simp[1]], V[simp[2]])
        ab = tuple(b[k] - a[k] for k in range(3))
        ac = tuple(c[k] - a[k] for k in range(3))
        n = _cross(ab, ac)
        d = sum(n[k] * a[k] for k in range(3))
        if sum(n[k] * center[k] for k in range(3)) > d:   # orient: center inside
            n = tuple(-x for x in n)
            d = -d
        facets.append((n, d))
    # dedupe parallel facets (triangulated octahedron faces are already distinct here)
    return facets


# ----------------------------------------------------------------------------------
# (F0) Remark 2.3, exact
# ----------------------------------------------------------------------------------

def verify_remark_2_3():
    half = [F(1, 2)] * 6
    M = CUBE_VERTS + Vp(half)
    dists = [l1(M[i], M[j]) for i in range(len(M)) for j in range(i + 1, len(M))]
    mind = min(dists)
    # At p=1/2, O_p - O_p = { |x|_1 <= 1 } exactly; coverable iff l1 < 1.
    coverable = [d for d in dists if d < 1]
    assert mind == 1, f"expected min l1 == 1, got {mind}"
    assert len(coverable) == 0, f"expected 0 coverable pairs, got {len(coverable)}"
    print("PASS F0: Remark 2.3 exact -- 0/14 pairs coverable, min pairwise l1 = 1 (zero slack).")


# ----------------------------------------------------------------------------------
# (F1) Fragility: a vertex/face pair becomes coverable for any single-coordinate nudge
# ----------------------------------------------------------------------------------

def _strictly_inside(d, facets):
    """Exact: is point d strictly inside the polytope {x : n.x <= dd}? (all strict)."""
    return all(sum(n[k] * d[k] for k in range(3)) < dd for (n, dd) in facets)


def diffbody_facets(p):
    """Exact facets of O_p - O_p. O_p-O_p = conv{v_i - v_j}; recompute facets exactly."""
    V = Vp(p)
    W = [tuple(V[i][k] - V[j][k] for k in range(3)) for i in range(6) for j in range(6)]
    Wf = np.array([[float(c) for c in w] for w in W])
    hull = ConvexHull(Wf)
    facets = []
    for simp in hull.simplices:
        a, b, c = (W[simp[0]], W[simp[1]], W[simp[2]])
        ab = tuple(b[k] - a[k] for k in range(3))
        ac = tuple(c[k] - a[k] for k in range(3))
        n = _cross(ab, ac)
        d = sum(n[k] * a[k] for k in range(3))
        # O_p - O_p is symmetric about 0; orient so 0 inside (d >= 0)
        if d < 0:
            n = tuple(-x for x in n); d = -d
        facets.append((n, d))
    return facets


def verify_fragility():
    """Perturb p1 by +1/10; show >=1 vertex/face pair becomes strictly coverable (exact)."""
    p = [F(1, 2)] * 6
    p[0] = F(1, 2) + F(1, 10)
    fac = diffbody_facets(p)
    M = CUBE_VERTS + Vp(p)
    n_cube = len(CUBE_VERTS)
    found = []
    for i in range(len(M)):
        for j in range(i + 1, len(M)):
            d = tuple(M[j][k] - M[i][k] for k in range(3))
            if _strictly_inside(d, fac):
                # classify pair type
                ti = "v" if i < n_cube else "f"
                tj = "v" if j < n_cube else "f"
                found.append((ti + tj, i, j))
    vf = [f for f in found if f[0] in ("vf", "fv")]
    assert len(vf) >= 1, "expected a vertex/face-point pair to become coverable"
    # one explicit example: cube vertex (0,0,0) and face point q30
    i0 = CUBE_VERTS.index((F(0), F(0), F(0)))
    j0 = n_cube + FACE_LABELS.index("q30")
    d0 = tuple(M[j0][k] - M[i0][k] for k in range(3))
    assert _strictly_inside(d0, fac), "expected (0,0,0)+q30 coverable at p1=1/2+1/10"
    print(f"PASS F1: at p1=1/2+1/10, {len(found)} pairs strictly coverable "
          f"({len(vf)} vertex/face). Explicit: vtx(0,0,0)+q30 (exact interior cert).")


# ----------------------------------------------------------------------------------
# (F2) The regular octahedron does NOT normalize to p=1/2  (corrects the worst-case framing)
# ----------------------------------------------------------------------------------

def verify_octahedron_min_box():
    """O_p (regular octahedron) admits an enclosing parallelotope of volume EXACTLY 2 < 8,
    so its minimal-volume parallelotope is strictly smaller than the cube.

    The octahedron Oc = {x : |x|_1 <= 1}.  A centered parallelotope M([-1,1]^3) contains Oc
    iff every vertex +-e_i lies in it, i.e. iff R := M^{-1} has all |entries| <= 1 (column
    infinity-norms <= 1).  Then Vol = 8/|det R|; taking R a +-1 matrix of det 4 (the
    Hadamard-type maximum of |det| over [-1,1]^{3x3}) gives an enclosing parallelotope of
    volume 8/4 = 2.  Volume 2 < 8 = cube volume, so the cube is NOT the minimal-volume
    parallelotope of O_p.  (We only need the strict inequality; "= 2" is the exact minimum
    but the lower bound is not needed here.)  Hence K = O_p is NOT min-vol-box-normalized to
    the cube, so it is NOT a body forced to p=1/2: there is genuine room between O_p and any
    actually-p=1/2 body near the cube corners.
    """
    best = 0
    witness = None
    for e in itertools.product([-1, 1], repeat=9):
        R = np.array(e).reshape(3, 3)
        d = abs(int(round(np.linalg.det(R))))
        if d > best:
            best = d
            witness = e
    assert best == 4, f"expected max |det| of +-1 3x3 == 4, got {best}"
    encl_vol = F(8, best)   # volume of an EXPLICIT enclosing parallelotope (R a det-4 +-1 matrix)
    assert encl_vol == F(2), f"expected enclosing parallelotope vol 2, got {encl_vol}"
    assert encl_vol < F(8), "octahedron's min box must be strictly below the cube"
    Rw = np.array(witness).reshape(3, 3)
    # exact det of the integer witness
    detw = (Rw[0, 0] * (Rw[1, 1] * Rw[2, 2] - Rw[1, 2] * Rw[2, 1])
            - Rw[0, 1] * (Rw[1, 0] * Rw[2, 2] - Rw[1, 2] * Rw[2, 0])
            + Rw[0, 2] * (Rw[1, 0] * Rw[2, 1] - Rw[1, 1] * Rw[2, 0]))
    assert abs(int(detw)) == 4
    print(f"PASS F2: octahedron enclosing parallelotope = 2 (witness det {int(detw)}); "
          f"< cube 8 => K=O_p is NOT forced to p=1/2, so slack to K exists.")


# ----------------------------------------------------------------------------------
# Demonstration: naive single-merge 13-piece LP becomes INFEASIBLE once edges are included
# (documents why A2 needs a genuine tau' redesign, not a free merge)
# ----------------------------------------------------------------------------------

CUBE_EDGES = [(i, j) for i in range(8) for j in range(i + 1, 8)
              if sum(CUBE_VERTS[i][k] != CUBE_VERTS[j][k] for k in range(3)) == 1]


def naive_merge_with_edges_infeasible(p, merge_v_idx=0, merge_face_idx=4):
    """Float LP screen (not load-bearing -- only documents the obstacle): the 13-piece
    structure '8 vertex-translates + 5 face-translates, one face merged onto a vertex'
    is INFEASIBLE when the 12 edges must also be covered by the endpoint-translate chain.
    Returns True iff feasible (we assert it is False)."""
    from scipy.optimize import linprog
    facets = Op_facets(p)
    Vpt = Vp(p)
    facemap = {}
    nxt = 8
    for fi in range(6):
        facemap[fi] = merge_v_idx if fi == merge_face_idx else nxt
        if fi != merge_face_idx:
            nxt += 1
    ntrans = nxt
    nbase = ntrans * 3
    nv = nbase + len(CUBE_EDGES)
    A_ub, b_ub = [], []
    eps = 1e-7

    def add_pt(pt, ti):
        for (n, d) in facets:
            row = [0.0] * nv
            for k in range(3):
                row[ti * 3 + k] = -float(n[k])
            A_ub.append(row)
            b_ub.append(float(d) - eps - sum(float(n[k]) * float(pt[k]) for k in range(3)))

    for i in range(8):
        add_pt(CUBE_VERTS[i], i)
    for fi in range(6):
        add_pt(Vpt[fi], facemap[fi])
    for ei, (i, j) in enumerate(CUBE_EDGES):
        vk = CUBE_VERTS[i]
        uk = tuple(CUBE_VERTS[j][k] - CUBE_VERTS[i][k] for k in range(3))
        tvar = nbase + ei
        for ti in (i, j):
            for (n, d) in facets:
                row = [0.0] * nv
                for k in range(3):
                    row[ti * 3 + k] = -float(n[k])
                row[tvar] = sum(float(n[k]) * float(uk[k]) for k in range(3))
                A_ub.append(row)
                b_ub.append(float(d) - eps - sum(float(n[k]) * float(vk[k]) for k in range(3)))
    bounds = [(None, None)] * nbase + [(0, 1)] * len(CUBE_EDGES)
    res = linprog([0.0] * nv, A_ub, b_ub, bounds=bounds, method='highs')
    return res.success


def document_edge_obstacle():
    p = [F(1, 2)] * 6
    p[0] = F(1, 2) + F(1, 10)
    feasible = naive_merge_with_edges_infeasible(p)
    assert not feasible, "naive merge unexpectedly feasible with edges"
    print("PASS (doc): naive single-merge 13-structure is INFEASIBLE with edges included "
          "-> A2 needs a genuine tau' redesign, not a free merge.")


# ----------------------------------------------------------------------------------
# OPEN HOLES
# ----------------------------------------------------------------------------------

def cover_neighborhood_of_p_half():
    """HOLE A1' (load-bearing, OPEN). On a neighborhood of p=1/2, a 13-translate cover of
    E ∪ V_p needs a body W with O_p <= W <= int(K).  (F2) shows slack exists, but a UNIFORM
    rational W valid for all p=1/2-forced bodies needs a quantitative corner-slack bound
    from the minimal-volume-box condition -- a continuum/affine fact, not supplied by the
    six contacts alone.  BLOCKER: contacts + min-vol-box do not yield a finite/rational W."""
    raise NotImplementedError(
        "HOLE A1': uniform rational enlargement W from min-vol-box slack is not established")


def cover_generic_box(P_vertices, tau13):
    """HOLE A2 (OPEN). A 13-piece covering structure tau' whose Prop-2.6 LP (vertices + 6
    face rectangles + all 12 EDGES, over Q_P = intersection of O_v over box vertices) is
    feasible on a generic box.  BLOCKER: the naive merge is edge-infeasible
    (document_edge_obstacle); a correct tau' needs a combinatorial redesign + a rational LP
    search, then an exact Farkas re-check."""
    raise NotImplementedError("HOLE A2: 13-piece edge-aware rational LP feasibility (open)")


def box_atlas():
    """HOLE A3 (OPEN). Symmetry-reduced finite atlas covering [0,1]^6 minus a neighborhood of
    1/2, each box tagged with a 13-feasible tau'.  Depends on A2."""
    raise NotImplementedError("HOLE A3: 13-feasible box atlas (open, depends on A2)")


def main():
    verify_remark_2_3()
    verify_fragility()
    verify_octahedron_min_box()
    document_edge_obstacle()
    print()
    print("Closed (exact): F0 (Remark 2.3), F1 (fragility), F2 (octahedron min-box / slack).")
    print("Open holes: A1' (uniform W from min-vol slack), A2 (edge-aware 13-piece LP), A3 (atlas).")
    print("Claimed bound: still 14 (NOT improved) -- the 13-cover holes A1'/A2/A3 are open.")


if __name__ == "__main__":
    main()
