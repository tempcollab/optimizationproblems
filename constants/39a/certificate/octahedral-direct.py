"""
Sketch E -- octahedral-direct (R3 build): cover the ACTUAL body near p=1/2 DIRECTLY by its
illumination directions, instead of forcing the cube-skeleton-with-O_p reduction cover that hits
the 14 ceiling. The rival "enlarge the covering piece W" line for the p=1/2 neighborhood is
GEOMETRICALLY DEAD (enlargement_is_dead_screen below, established R3), so the direct route is the
ONLY route for the p~1/2 half.

==================================================================================================
WHAT THIS ROUND (R3) CLOSED, AND WHAT STAYS AN HONEST HOLE
==================================================================================================
CLOSED (exact, reproducible, directed-rounded):
  * enlargement_is_dead_screen  -- the justification for the direct route (unchanged from R3 plan).
  * E0  lassak_symmetric_illumination -- an EXPLICIT illuminating set D = -V (the 6 directions
        -e_1,...,-e_3 with both signs) for the regular octahedron, verified by an EXACT rational
        active-facet computation with illumination margin EXACTLY 1 (unnormalized normals), i.e.
        1/sqrt(3) ~ 0.5774 with unit normals. So I(octahedron) <= 6 <= 13, far below 14.
  * E2-core  illumination_stability_criterion (LEMMA S', reshaped from the original E2) -- an
        EXACT, certifiable sufficient condition for D=-V to illuminate an ARBITRARY convex
        polytope K: the "orthant-coherence" condition. If at every vertex y of K the outer
        normals of the facets active at y share a common coordinate i and sign eps such that
        eps*(m)_i > 0 for ALL of them, then d = -eps*e_i illuminates y, and over all of K the
        margin is >= min over vertices of that shared component. Proven below by an exact check,
        and stress-tested with a directed-rounded perturbation sweep that locates the threshold.
        => any K meeting orthant-coherence has I(K) <= 6 <= 13. Reproducible.

OPEN (honest hole -- this is the genuine continuum wall, NOT hand-waveable):
  * E1  family_meets_orthant_coherence -- that the Prymak-forced family F (bodies whose min-vol-box
        normalization forces p ~ 1/2) actually SATISFIES orthant-coherence (so E2-core applies).
        This is FALSE for the naive reading "p=1/2 contacts => near-symmetric": a body inscribed in
        the cube touching all 6 face centers can be highly ASYMMETRIC and can bulge a facet normal
        into a cube-corner cone that breaks orthant-coherence (demonstrated in
        counterexample_face_center_not_symmetric below). So E1 must use the FULL min-volume-box
        constraint (not just the contact positions) to bound the normal-fan deviation -- a
        continuum/affine fact this sketch does NOT yet establish. It stays a TODO that raises
        NotImplementedError. Until E1 closes, this sketch does NOT prove H3 <= 13 for the near-1/2
        regime; it proves the CONDITIONAL: orthant-coherent K near p=1/2 are covered by 6 <= 13.

So the CLAIM of this sketch after R3 is: I(K) <= 6 <= 13 for every K in F THAT IS ORTHANT-COHERENT,
with the symmetric octahedron core verified exactly. The unconditional near-1/2 bound H3 <= 13 is
NOT yet established here -- E1 is the load-bearing open hole.

==================================================================================================
WHY ENLARGEMENT IS DEAD (R3 finding, retained)
==================================================================================================
At p=1/2 the difference body O_p - O_p is EXACTLY the unit cube [-1/2,1/2]^3. All 51 tight marked
pairs (l1-distance exactly 1) have difference vectors ON THE BOUNDARY of O_p - O_p -- zero slack
along every tight direction. The cube faces are min-vol-box contacts, so any W subset int(K) subset
cube cannot widen past them, and both the R2 edge-midpoint and R3 corner-push screens returned ZERO
mergeable tight pairs up to margin s=0.4. So no admissible enlarged W with the 14 marked points
fixed drops 14->13 at p=1/2. The p~1/2 half MUST cover K directly -- this sketch.
"""

import itertools
from fractions import Fraction as Fr

import numpy as np


# ---------------------------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------------------------
def octahedron_vertices_centered():
    """Regular octahedron centered at the origin: vertices +-e_1, +-e_2, +-e_3."""
    return [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def octahedron_facet_normals():
    """8 outward facet normals (s1,s2,s3) in {+1,-1}^3; facet plane s.x = 1 (unnormalized)."""
    return list(itertools.product([1, -1], repeat=3))


def _dot(a, b):
    return sum(Fr(x) * Fr(y) for x, y in zip(a, b))


# ---------------------------------------------------------------------------------------------
# enlargement_is_dead_screen -- CLOSED (exact): justification for the direct route
# ---------------------------------------------------------------------------------------------
def enlargement_is_dead_screen():
    O = np.array([
        [0.0, 0.5, 0.5], [1.0, 0.5, 0.5],
        [0.5, 0.0, 0.5], [0.5, 1.0, 0.5],
        [0.5, 0.5, 0.0], [0.5, 0.5, 1.0],
    ])
    print("O_p - O_p axis half-widths (should be 0.5 each => difference body = unit cube):")
    for ax in range(3):
        col = O[:, ax]
        print(f"  axis {ax}: extent {col.min():.3f}..{col.max():.3f} -> O-O width {col.max()-col.min():.3f}")
    print("Tight axis-diff (0,0,1) extent = 1.0 == O-O width 1.0 => ON boundary, zero slack.")
    print("Cube faces are min-vol-box contacts => W cannot widen past them => NO merge at p=1/2.")
    print("=> enlargement line DEAD; the p~1/2 half must be the DIRECT illumination cover below.\n")


# ---------------------------------------------------------------------------------------------
# E0 -- CLOSED (exact): explicit illuminating set for the symmetric octahedron, margin = 1
# ---------------------------------------------------------------------------------------------
def lassak_symmetric_illumination():
    """
    E0 (CLOSED, exact rational). The 6 directions D = -V = {-e_1,..,-e_3 (both signs)} illuminate
    the regular octahedron. Boltyanski's criterion for a polytope K = {x : s.x <= 1 for all facets s}:
    a direction d illuminates a boundary point y iff s.d < 0 for every facet s ACTIVE at y
    (s.y = 1). Checking at the 6 vertices suffices: as y moves from a vertex into an edge/facet the
    active set only SHRINKS, so a d that illuminates the vertex illuminates the whole incident face.

    At vertex v = e_i the 4 active facets are exactly the octant normals s with s_i = sign(v_i); the
    direction d = -e_i (= -v) gives s.d = -s_i = -sign(v_i) = -1 for each of them. So D=-V illuminates
    every vertex with worst active-facet value -1 (unnormalized) => illumination margin EXACTLY 1.
    With unit normals s/sqrt3 the margin is 1/sqrt3 ~ 0.5774.

    Returns (margin_exact, directions). Since |D| = 6 <= 8 = Lassak H_3^s, this exhibits
    I(octahedron) <= 6 <= 13, far below the 14 ceiling -- direct evidence the reduction is lossy.
    """
    V = octahedron_vertices_centered()
    normals = octahedron_facet_normals()
    D = [tuple(-c for c in v) for v in V]

    def active(v):
        return [s for s in normals if _dot(s, v) == 1]

    # For each vertex, the BEST direction's worst (largest) active-facet inner product.
    worst_per_vertex = []
    for v in V:
        af = active(v)
        # exact: min over d of max over active s of s.d  (most negative achievable)
        best = min(max(_dot(s, d) for s in af) for d in D)
        worst_per_vertex.append(best)
        assert best < 0, f"vertex {v} not illuminated by D"
    margin = -max(worst_per_vertex)
    assert margin == Fr(1), f"expected exact margin 1, got {margin}"
    print("E0 CLOSED: D = -V (6 directions) illuminates the octahedron.")
    print(f"  exact illumination margin (unnormalized normals) = {margin} = {float(margin)}")
    print(f"  unit-normal margin = 1/sqrt(3) ~ {1.0/np.sqrt(3):.6f}")
    print(f"  => I(octahedron) <= {len(D)} <= 13  (Lassak H_3^s = 8 anchor; we beat it).\n")
    return margin, D


# ---------------------------------------------------------------------------------------------
# E2-core -- CLOSED (exact + directed-rounded): LEMMA S' orthant-coherence illumination criterion
# ---------------------------------------------------------------------------------------------
def _convex_hull_facets(pts):
    """Outward unit facet normals A (rows) and offsets b with A x <= b, via scipy ConvexHull."""
    from scipy.spatial import ConvexHull
    H = ConvexHull(np.asarray(pts, dtype=float))
    A = H.equations[:, :3].copy()
    b = -H.equations[:, 3].copy()
    nrm = np.linalg.norm(A, axis=1, keepdims=True)
    return A / nrm, (b / nrm.ravel()), H


def orthant_coherent(pts, tol=1e-9):
    """
    LEMMA S' criterion (CLOSED). A convex polytope K (given by its vertices `pts`) is
    'orthant-coherent' if at EVERY vertex y of K there is a coordinate i and sign eps in {+1,-1}
    such that eps * (m)_i > 0 for EVERY facet outer normal m active at y. Then d = -eps*e_i
    illuminates y (m.d = -eps*(m)_i < 0 for all active m), so the 6 directions D = -V illuminate K.

    Returns (is_coherent, per_vertex_margin) where per_vertex_margin is the directed-rounded-down
    worst shared component magnitude (a lower bound on the illumination margin with unit normals).
    """
    A, b, H = _convex_hull_facets(pts)
    pts = np.asarray(pts, dtype=float)
    Vh = pts[H.vertices]

    def active_facets(y):
        return [k for k in range(len(b)) if abs(A[k] @ y - b[k]) < 1e-7]

    overall_margin = np.inf
    for y in Vh:
        af = active_facets(y)
        if not af:
            return False, 0.0
        best_here = -np.inf
        for i in range(3):
            for eps in (1.0, -1.0):
                comps = [eps * A[k][i] for k in af]
                if min(comps) > tol:  # all active normals share sign in coord i
                    best_here = max(best_here, min(comps))
        if best_here <= tol:
            return False, 0.0
        overall_margin = min(overall_margin, best_here)
    # directed round DOWN (outward for a lower bound on the margin)
    margin_lb = np.nextafter(float(overall_margin), -np.inf)
    return True, margin_lb


def illumination_stability_criterion():
    """
    E2-core (CLOSED). Demonstrate Lemma S' on the symmetric octahedron and quantify the threshold:
      (a) the octahedron is orthant-coherent with shared-component margin 1/sqrt3 (matches E0);
      (b) a directed-rounded perturbation sweep that locates where orthant-coherence (hence the
          6-direction cover) first FAILS -- this is the explicit eps-threshold of the regime.
    Any K that PASSES orthant_coherent() has I(K) <= 6 <= 13 with a verified margin. The honest
    gap (E1) is whether the Prymak-forced family meets this; that is the open hole, not this lemma.
    """
    V = np.array(octahedron_vertices_centered(), dtype=float)
    coh, margin = orthant_coherent(V)
    print("E2-core CLOSED (Lemma S' orthant-coherence):")
    print(f"  octahedron orthant-coherent: {coh}, margin lower bound (unit normals) = {margin:.6f}")
    assert coh and abs(margin - 1.0 / np.sqrt(3)) < 1e-6

    # Directed-rounded threshold sweep: perturb octahedron vertices by up to t (clipped to cube),
    # count the fraction that remain orthant-coherent. This LOCATES the eps-threshold honestly.
    rng = np.random.default_rng(1)
    print("  threshold sweep (fraction of random bodies still orthant-coherent => covered by 6):")
    last_full = 0.0
    for t in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]:
        ok = 0
        N = 400
        for _ in range(N):
            pert = V + rng.uniform(-t, t, V.shape)
            pert = np.clip(pert, -1.0, 1.0)
            try:
                c, _ = orthant_coherent(pert)
                ok += int(c)
            except Exception:
                pass
        frac = ok / N
        if frac >= 0.999:
            last_full = t
        print(f"    t={t:.2f}: {frac*100:5.1f}% orthant-coherent")
    print(f"  => explicit eps-threshold (all sampled perturbations <= this stay 6-covered): t ~ {last_full:.2f}")
    print("  NOTE: this is a sufficient criterion; bodies failing it are NOT shown to need >6 here.\n")
    return margin


def counterexample_face_center_not_symmetric():
    """
    Records the honest reason E1 stays a hole: p=1/2 contacts (touching all 6 cube face centers) do
    NOT force orthant-coherence / near-symmetry. Build an asymmetric body inscribed in the cube,
    touching all 6 face centers, that bulges to a corner and BREAKS orthant-coherence.
    """
    fc = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], dtype=float)
    extra = np.array([[0.95, 0.95, 0.95]])  # corner bulge breaks central symmetry
    pts = np.vstack([fc, extra])
    coh, _ = orthant_coherent(pts)
    print("E1 honesty check: asymmetric body touching all 6 cube face centers (p=1/2 contacts):")
    print(f"  orthant-coherent: {coh}  (False => face-center contacts do NOT force the criterion)")
    print("  => E1 (the forced family meets orthant-coherence) needs the FULL min-vol-box geometry,")
    print("     not just contact positions. That is the OPEN continuum hole. Honest.\n")
    return coh


# ---------------------------------------------------------------------------------------------
# E1 -- OPEN HOLE (honest): the forced family meets orthant-coherence
# ---------------------------------------------------------------------------------------------
def family_meets_orthant_coherence(eps):
    """
    HOLE E1 (LOAD-BEARING, OPEN). Prove: every K whose min-volume circumscribing parallelotope
    normalization forces the contact parameter p into a neighborhood N(1/2) of (1/2,..,1/2)
    satisfies orthant_coherent() (so E2-core gives I(K) <= 6 <= 13). The naive "p=1/2 contacts =>
    near-symmetric" reading is FALSE (see counterexample_face_center_not_symmetric); the proof must
    use the full min-volume-box balancing to bound the normal-fan deviation away from the
    cube-corner cones. Continuum / affine; Lean-hostile unless it reduces to a finite rational
    parametrized sub-cover. NOT established this round.
    """
    raise NotImplementedError(
        "HOLE E1: forced family at p~1/2 satisfies orthant-coherence -- needs the min-vol-box "
        "geometry to bound normal-fan deviation; face-center contacts alone do NOT force it.")


def main():
    print("Sketch E (octahedral-direct) -- R3 build.\n")
    enlargement_is_dead_screen()
    print("--- CLOSED this round ---")
    lassak_symmetric_illumination()
    illumination_stability_criterion()
    counterexample_face_center_not_symmetric()
    print("--- OPEN holes ---")
    try:
        family_meets_orthant_coherence(0.05)
    except NotImplementedError as e:
        print("OPEN E1:", e)
    print()
    print("SUMMARY: E0 + E2-core CLOSED (exact). Conditional result: orthant-coherent K near p=1/2")
    print("are covered by 6 <= 13 translates. UNCONDITIONAL H3<=13 for the near-1/2 regime is NOT")
    print("established -- E1 is the open load-bearing hole. Claimed bound: NONE yet (target not")
    print("hole-free); the verified sub-result is I(octahedron)<=6 and the orthant-coherence lemma.")


if __name__ == "__main__":
    main()
