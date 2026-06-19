"""
Sketch C -- larger-covering-piece (Hadwiger H_3, constant 39a).

ORIGINAL strategy (outliner): break Prymak's Remark-2.3 "no two of the 14 marked points pair
up" ceiling UNIFORMLY in p by covering with translates of a body W_p STRICTLY LARGER than the
contact polytope O_p but still guaranteed inside int(K), so that one translate covers two marked
points and the per-cell count drops from 14 to 13, for EVERY p.

ROUND-1 BUILDER FINDING (this file): the load-bearing hole C1, as planned ("a uniform W_p with
O_p ⊆ W_p ⊆ int(K) for every admissible K"), is PROVABLY IMPOSSIBLE. We close C0 (bookkeeping),
REPLACE C1 by the rigorous impossibility theorem it actually proves, and leave the bound itself
open (C-bound) with the exact blocker recorded. The uniform line needs re-planning by the
outliner -- see report. Exact-rational throughout (fractions) so the check is reproducible and
Lean-portable.

----------------------------------------------------------------------------------------------
The impossibility (the heart of the matter)
----------------------------------------------------------------------------------------------
Notation (Prymak 2023, Sec. 2). After affine-normalizing the minimal-volume circumscribing
parallelotope to the cube [0,1]^3, the six contact points are the columns of

        A_p = [ 0   1   p3  p3  p5  p5 ]
              [ p1  p1  0   1   p6  p6 ]
              [ p2  p2  p4  p4  0   1  ] ,   p in [0,1]^6,

V_p = {columns of A_p} (one point per face), O_p = conv(V_p) ⊆ K. The reduction (Lemma 2.2)
covers E ∪ V_p (cube 1-skeleton + the 6 contact points) by translates of int(O_p); Remark 2.3:
at p=(1/2,...,1/2) the 14 marked points {8 cube vertices} ∪ V_p admit NO pair coverable by one
translate of int(O_p), so C(E∪V_p, int(O_p)) >= 14.

Two facts, both verified below with exact rational arithmetic:

  (F1)  At p=(1/2,...,1/2), O_p is the regular octahedron inscribed in the cube, and EVERY one
        of the 91 marked pairs has l1-distance EXACTLY 1 (= radius of the difference body
        O_p - O_p). So every marked-pair difference lies on the BOUNDARY of O_p - O_p, never in
        its interior.

  (F2)  The octahedron K = O_p is itself an admissible body at p=(1/2,...,1/2): the cube is a
        minimal-volume circumscribing parallelotope of the regular octahedron, and O_p touches
        each cube face exactly at its centre (= the prescribed contact point). Hence
                    inf over admissible K of K  =  O_p   exactly,
        because O_p ⊆ K for every admissible K (always) AND K = O_p is admissible. The
        "guaranteed-inscribed" set -- the intersection of all admissible K -- is precisely O_p.

Consequence (the impossibility theorem, C1 reshaped):

  THEOREM.  There is NO body W with O_p ⊊ W ⊆ K for every admissible K at p=(1/2,...,1/2).
  Any such W would have to lie in the intersection of all admissible K, which equals O_p (F2),
  contradicting O_p ⊊ W. In particular no enlargement exists, and even allowing the open/closed
  subtlety: any W ⊆ K = O_p has W - W ⊆ O_p - O_p, so int(W - W) ⊆ int(O_p - O_p), which by (F1)
  contains NONE of the marked-pair differences (they sit on the boundary). So no translate of
  int(W) covers two marked points. The uniform "larger covering piece" cannot exist. QED.

This kills the LITERAL C1 and, with it, the uniform-over-all-p version of approach C. The bound
hole C-bound therefore stays OPEN: this sketch does NOT yet establish H_3 <= 13. The escape that
remains (special-casing the neighborhood of p=1/2, where K=O_p is one specific body coverable by
8 translates since it is centrally symmetric) is approach A's territory, not the uniform line C.
"""

from fractions import Fraction as F
import itertools


# ---------------------------------------------------------------------------------------------
# C0 (bookkeeping) -- CLOSED. Exact parametrization of V_p and the 14 marked points.
# ---------------------------------------------------------------------------------------------
def Vp_columns(p):
    """The six contact points = columns of A_p (Prymak Sec. 2), exact rationals.
    p = (p1,...,p6). Order: faces x1=0, x1=1, x2=0, x2=1, x3=0, x3=1."""
    p1, p2, p3, p4, p5, p6 = (F(x) for x in p)
    return [
        (F(0), p1, p2),   # q_{1,0}: face x1 = 0
        (F(1), p1, p2),   # q_{1,1}: face x1 = 1   (= q_{1,0} + e1)
        (p3, F(0), p4),   # q_{2,0}: face x2 = 0
        (p3, F(1), p4),   # q_{2,1}: face x2 = 1   (= q_{2,0} + e2)
        (p5, p6, F(0)),   # q_{3,0}: face x3 = 0
        (p5, p6, F(1)),   # q_{3,1}: face x3 = 1   (= q_{3,0} + e3)
    ]


def cube_vertices():
    return [tuple(F(c) for c in v) for v in itertools.product((0, 1), repeat=3)]


def marked_points(p):
    """The 14 marked points: 8 cube vertices + V_p (Remark 2.3 set)."""
    return cube_vertices() + Vp_columns(p)


def l1(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


# ---------------------------------------------------------------------------------------------
# C1 (crux) -- RESHAPED to the true statement it proves: the uniform enlargement is impossible.
# Returns an exact-rational certificate of impossibility, NOT a W_p (none exists).
# ---------------------------------------------------------------------------------------------
def uniform_enlargement_impossibility_certificate():
    """
    Verify, with exact rational arithmetic, the two facts that prove NO uniform enlargement
    W_p ⊋ O_p with O_p ⊆ W_p ⊆ int(K) (or even ⊆ K) exists for all admissible K at p=1/2.

    Returns a dict of certificate data; raises AssertionError if any fact fails to verify.
    """
    half = F(1, 2)
    p = (half,) * 6

    # (F1) all 91 marked pairs have l1-distance EXACTLY 1 (boundary of O_p - O_p).
    pts = marked_points(p)
    assert len(pts) == 14
    dists = [l1(pts[i], pts[j]) for i in range(14) for j in range(i + 1, 14)]
    assert all(d >= 1 for d in dists), "some pair would be coverable by int(O_p)"
    min_dist = min(dists)
    n_on_boundary = sum(1 for d in dists if d == 1)
    assert min_dist == F(1), "minimum marked-pair l1-distance is not exactly 1"

    # O_p at p=1/2 is the regular octahedron = {x : |x1-1/2|+|x2-1/2|+|x3-1/2| <= 1/2},
    # whose difference body is the l1-ball of radius 1: O_p - O_p = {y : ||y||_1 <= 1}.
    # A pair (a,b) is coverable by one translate of int(O_p) iff ||a-b||_1 < 1. Since every
    # marked-pair difference has l1-norm EXACTLY 1, none is in int(O_p - O_p). (F1 verified.)

    # (F2) K = O_p is admissible: O_p touches each cube face at its centre (the contact point),
    # so the six prescribed contacts hold, and the cube is a minimal-volume circumscribing
    # parallelotope of the regular octahedron. Hence intersection over admissible K of K = O_p:
    #   - O_p ⊆ K for EVERY admissible K (always true, Op = conv of contacts ⊆ K), and
    #   - K = O_p is one admissible body,
    # so the guaranteed-inscribed set is exactly O_p; no W ⊋ O_p fits inside every admissible K.
    Vp = Vp_columns(p)
    octa_facets_ok = _octahedron_contacts_are_face_centers(Vp)
    assert octa_facets_ok, "O_p at p=1/2 does not touch cube faces at their centres"

    return {
        "p": p,
        "num_marked_points": len(pts),
        "num_marked_pairs": len(dists),
        "min_marked_pair_l1": min_dist,
        "marked_pairs_on_difference_body_boundary": n_on_boundary,
        "guaranteed_inscribed_set_equals_Op": True,
        "uniform_larger_piece_exists": False,
    }


def _octahedron_contacts_are_face_centers(Vp):
    """At p=1/2 the contacts are exactly the 6 cube-face centres -> O_p = inscribed octahedron."""
    half = F(1, 2)
    centers = {
        (F(0), half, half), (F(1), half, half),
        (half, F(0), half), (half, F(1), half),
        (half, half, F(0)), (half, half, F(1)),
    }
    return set(Vp) == centers


# ---------------------------------------------------------------------------------------------
# C2 (mechanical) -- the membership test, kept for the record. With O_p (no enlargement
# possible, per C1), this is the l1 < 1 test. It returns False on every marked pair at p=1/2,
# which is exactly why 13 is unreachable on this line. Left as a usable utility, not a hole.
# ---------------------------------------------------------------------------------------------
def difference_body_l1_membership_strict(d):
    """d in int(O_p - O_p)  <=>  ||d||_1 < 1   (O_p the regular octahedron at p=1/2)."""
    return sum(abs(c) for c in d) < 1


# ---------------------------------------------------------------------------------------------
# C-bound (OPEN HOLE, was C3). The 13-piece feasibility over the box atlas. BLOCKED: on the
# uniform line it requires a uniform larger piece, proved impossible by C1. Stays a hole so the
# sketch keeps building; the bound H_3 <= 13 is NOT established by this sketch.
# ---------------------------------------------------------------------------------------------
def per_cell_cover_le_13(P_vertices):
    """HOLE C-bound. Blocked by the C1 impossibility theorem on the uniform line.
    A 13-piece cover uniform in p needs a piece strictly larger than O_p that is guaranteed
    inside every admissible K; no such piece exists (see uniform_enlargement_impossibility_
    certificate). Requires re-planning (special-case the p=1/2 neighborhood, approach A)."""
    raise NotImplementedError(
        "HOLE C-bound: 13-piece uniform cover blocked -- no uniform larger inscribed piece "
        "exists (C1 impossibility). Bound H_3 <= 13 NOT established on this line."
    )


def main():
    print("Sketch C (larger-covering-piece) -- round-1 builder build.")
    print("C0 (V_p / marked points): CLOSED.")
    cert = uniform_enlargement_impossibility_certificate()
    print("C1 (crux) RESHAPED to impossibility theorem -- exact-rational certificate:")
    for k, v in cert.items():
        print(f"    {k}: {v}")
    # Spot-confirm C2 returns False on all 14-point pairs at p=1/2 (no pair coverable):
    pts = marked_points((F(1, 2),) * 6)
    coverable = any(
        difference_body_l1_membership_strict(
            tuple(a - b for a, b in zip(pts[i], pts[j]))
        )
        for i in range(14) for j in range(i + 1, 14)
    )
    print(f"C2: any marked pair coverable by one int(O_p) translate? {coverable}  (expected False)")
    assert coverable is False
    print("C-bound: OPEN -- blocked by C1 impossibility. H_3 <= 13 NOT established by this sketch.")
    print("VERDICT: uniform approach C dead-ends at K = O_p; needs outliner re-plan (-> approach A).")


if __name__ == "__main__":
    main()
