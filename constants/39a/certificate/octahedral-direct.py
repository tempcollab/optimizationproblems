"""
Sketch E -- octahedral-direct: cover the ACTUAL body near p=1/2 DIRECTLY by its illumination
directions, instead of forcing the cube-skeleton-with-O_p reduction cover that hits the 14
ceiling. The rival "enlarge the covering piece W" line for the p=1/2 neighborhood is GEOMETRICALLY
DEAD (enlargement_is_dead_screen below, established R3), so the direct route is the ONLY route for
the p~1/2 half. This sketch is the run's LOAD-BEARING open problem: the near-1/2 regime gates the
global H3<=13 bound.

==================================================================================================
R4 STATUS -- WHAT IS CLOSED (CHECKED IN CODE), WHAT STAYS AN HONEST HOLE
==================================================================================================
CLOSED (exact / directed-rounded, reproducible -- the checked core):
  * enlargement_is_dead_screen  -- the justification for the direct route (R3, retained).
  * E0  lassak_symmetric_illumination -- EXPLICIT illuminating set D = -V = {+-e_i} (6 dirs) for the
        regular octahedron, by an EXACT rational active-facet computation, illumination margin
        EXACTLY 1 (unnormalized) = 1/sqrt(3) with unit normals. So I(octahedron) <= 6 <= 13.
  * E2-core  illumination_stability_criterion (LEMMA S') -- an EXACT sufficient criterion
        (orthant-coherence) for D=-V to illuminate an arbitrary polytope; CLOSED, sweep-located
        threshold ~0.30. (A SUFFICIENT condition only; the forced family need not meet it.)

R4 NEW (the E1b STRUCTURE, checked in code with exact rationals on the load-bearing predicate):
  * E1b-PREDICATE (EXACT, illumination_predicate_exact) -- the per-vertex illumination predicate
        via Boltyanski's active-facet criterion, computed in EXACT Fractions from integer-cross-
        product facet normals: direction d illuminates vertex y iff d.m < 0 for every facet normal
        m active at y. As a corollary the CORNER direction -s (s in {+-1}^3, the inward octant
        diagonal) illuminates y iff s.m > 0 for all active m. Verified exactly on a rational body.
  * E1b-FINITENESS (EXACT, corner_cover_is_finite_hitting_set) -- *conditional on* every broken
        vertex being corner-coverable, covering the broken set B(K) by corner directions is a
        FINITE HITTING-SET problem over the 8 corner directions, solved exactly. So the corrective
        budget = min hitting-set size <= 8 whenever B(K) is corner-coverable. This finitizes E1b's
        cover (a step toward Lean-fit) -- the cover is a finite rational object once coverability holds.
  * E1b-BUDGET SCREEN (directed search, broken_set_budget_screen) -- an adversarial search over a
        broad forced-family proxy (6 face-center contacts + arbitrary cube-interior vertices, incl.
        all-8-corners-bulged): in 12000+ bodies the broken set was ALWAYS corner-coverable and the
        min hitting-set never exceeded 5 (<= 7). Recorded as a CONJECTURE WITH A REPRODUCIBLE SCREEN,
        not a proof (the continuum gap is below).
  * E1b-HONEST LIMIT (EXACT, corner_coverability_is_not_generic) -- the abstract statement
        "pointed + broken => corner-coverable" is FALSE: an explicit pointed broken normal config
        has NO covering corner direction. So corner-coverability is a genuine FORCED-FAMILY fact
        (it uses the cube / min-vol-box structure), NOT a generic one. This pins EXACTLY where the
        open continuum content lives -- it is the link from the box geometry to the normal cones,
        not a generic combinatorial truth.

OPEN (honest holes -- the genuine continuum wall, NOT hand-waveable):
  * E1a  broken_set_bounded_by_min_vol_box -- bound |B(K)| from the min-vol-box tilt. OPEN.
  * E1b-COVERABILITY  every_broken_vertex_corner_coverable -- that EVERY broken vertex of a
        forced-family body is corner-coverable (extensively screened, never refuted, but UNPROVED:
        the abstract version is false, so the proof must use the cube structure). OPEN.
  * E1b-BUDGET<=7  corner_budget_at_most_7 -- that <= 7 distinct corner directions always suffice
        (the 8th excluded by volume balancing). Screened (never > 5 observed), UNPROVED. OPEN.
  * E1   near_one_half_illuminated_by_13 -- assembly: I(K) <= 6 + 7 = 13. Rests on E1a + E1b above.

So the R4 CLAIM of this sketch: the E1b *cover mechanism* is now a FINITE, exact, rational object
(corner hitting-set over 8 directions) whenever its coverability hypothesis holds; coverability and
the <=7 budget are SCREENED (never refuted, max 5 corners) but remain CONJECTURAL because the
abstract version is provably false -- they need the cube/min-vol-box geometry (E1a's content).
The unconditional near-1/2 bound H3 <= 13 is NOT established. Claimed bound: NONE (beat-14: no).

==================================================================================================
WHY ENLARGEMENT IS DEAD (R3 finding, retained)
==================================================================================================
At p=1/2 the difference body O_p - O_p is EXACTLY the unit cube [-1/2,1/2]^3. All 51 tight marked
pairs (l1-distance exactly 1) have difference vectors ON THE BOUNDARY of O_p - O_p -- zero slack
along every tight direction. The cube faces are min-vol-box contacts, so any W subset int(K) subset
cube cannot widen past them, and both screens returned ZERO mergeable tight pairs up to margin
s=0.4. So no admissible enlarged W with the 14 marked points fixed drops 14->13 at p=1/2. The p~1/2
half MUST cover K directly -- this sketch.
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


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _sub(a, b):
    return tuple(Fr(x) - Fr(y) for x, y in zip(a, b))


# Core illumination directions (the symmetric 6) and the 8 corner sign vectors.
CORE_DIRECTIONS = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
CORNER_SIGNS = list(itertools.product([1, -1], repeat=3))  # s; corner direction is -s


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
    """E0 (CLOSED, exact rational). D = -V = {-e_i (both signs)} illuminates the regular
    octahedron. Boltyanski: d illuminates boundary point y iff s.d < 0 for every facet s active at
    y; checking vertices suffices (active set only shrinks off a vertex). At v = e_i the 4 active
    facets are the octant normals s with s_i = sign(v_i); d = -e_i gives s.d = -1 for each.
    So margin EXACTLY 1 (unnormalized), 1/sqrt3 with unit normals. |D| = 6 <= 8 = Lassak H_3^s."""
    V = octahedron_vertices_centered()
    normals = octahedron_facet_normals()
    D = [tuple(-c for c in v) for v in V]

    def active(v):
        return [s for s in normals if _dot(s, v) == 1]

    worst_per_vertex = []
    for v in V:
        af = active(v)
        best = min(max(_dot(s, d) for s in af) for d in D)
        worst_per_vertex.append(best)
        assert best < 0, f"vertex {v} not illuminated by D"
    margin = -max(worst_per_vertex)
    assert margin == Fr(1), f"expected exact margin 1, got {margin}"
    print("E0 CLOSED: D = -V (6 directions) illuminates the octahedron.")
    print(f"  exact illumination margin (unnormalized normals) = {margin} = {float(margin)}")
    print(f"  unit-normal margin = 1/sqrt(3) ~ {1.0/np.sqrt(3):.6f}")
    print(f"  => I(octahedron) <= {len(D)} <= 13.\n")
    return margin, D


# ---------------------------------------------------------------------------------------------
# E2-core -- CLOSED (exact + directed-rounded): LEMMA S' orthant-coherence (SUFFICIENT criterion)
# ---------------------------------------------------------------------------------------------
def _convex_hull_facets(pts):
    """Outward unit facet normals A (rows) and offsets b with A x <= b, via scipy ConvexHull
    (used for face COMBINATORICS only; the load-bearing exact tests recompute normals in Fractions)."""
    from scipy.spatial import ConvexHull
    H = ConvexHull(np.asarray(pts, dtype=float))
    A = H.equations[:, :3].copy()
    b = -H.equations[:, 3].copy()
    nrm = np.linalg.norm(A, axis=1, keepdims=True)
    return A / nrm, (b / nrm.ravel()), H


def orthant_coherent(pts, tol=1e-9):
    """LEMMA S' criterion (CLOSED, SUFFICIENT). K is 'orthant-coherent' if at EVERY vertex y there
    is a coordinate i and sign eps with eps*(m)_i > 0 for EVERY active outer normal m; then
    d = -eps*e_i illuminates y, so D = -V illuminates K. Returns (is_coherent, margin_lb)."""
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
                if min(comps) > tol:
                    best_here = max(best_here, min(comps))
        if best_here <= tol:
            return False, 0.0
        overall_margin = min(overall_margin, best_here)
    margin_lb = np.nextafter(float(overall_margin), -np.inf)  # directed round DOWN
    return True, margin_lb


def illumination_stability_criterion():
    """E2-core (CLOSED). Lemma S' on the octahedron + a directed-rounded threshold sweep. A
    SUFFICIENT condition only; the forced family need NOT meet it (that is why E1 is re-planned to
    the asymmetry-tolerant budget below, not a <=6 coherence claim)."""
    V = np.array(octahedron_vertices_centered(), dtype=float)
    coh, margin = orthant_coherent(V)
    print("E2-core CLOSED (Lemma S' orthant-coherence, SUFFICIENT only):")
    print(f"  octahedron orthant-coherent: {coh}, margin lower bound (unit normals) = {margin:.6f}")
    assert coh and abs(margin - 1.0 / np.sqrt(3)) < 1e-6

    rng = np.random.default_rng(1)
    print("  threshold sweep (fraction of random bodies still orthant-coherent => covered by 6):")
    last_full = 0.0
    for t in [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]:
        ok = 0
        N = 400
        for _ in range(N):
            pert = np.clip(V + rng.uniform(-t, t, V.shape), -1.0, 1.0)
            try:
                c, _ = orthant_coherent(pert)
                ok += int(c)
            except Exception:
                pass
        frac = ok / N
        if frac >= 0.999:
            last_full = t
        print(f"    t={t:.2f}: {frac*100:5.1f}% orthant-coherent")
    print(f"  => explicit eps-threshold (all sampled <= this stay 6-covered): t ~ {last_full:.2f}")
    print("  NOTE: SUFFICIENT criterion; bodies failing it are NOT shown to need >6 here.\n")
    return margin


def counterexample_face_center_not_symmetric():
    """Records why E1 was re-planned: p=1/2 contacts do NOT force orthant-coherence. An asymmetric
    body touching all 6 cube face centers bulges to a corner and breaks the criterion."""
    fc = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], dtype=float)
    pts = np.vstack([fc, np.array([[0.95, 0.95, 0.95]])])
    coh, _ = orthant_coherent(pts)
    print("E1 re-plan reason: asymmetric body touching all 6 cube face centers (p=1/2 contacts):")
    print(f"  orthant-coherent: {coh}  (False => face-center contacts do NOT force the <=6 criterion)")
    print("  => the <=6 target is too strong; E1 re-planned to the asymmetry-tolerant <=13 budget.\n")
    return coh


# =============================================================================================
# E1 -- RE-PLANNED R4: asymmetry-tolerant <=13 = 6 core + <=7 perturbed corrective directions.
# The corrective directions are the 8 CORNER (inward octant-diagonal) directions; the budget claim
# is that <=7 of them ever suffice. R4 builds the EXACT, FINITE structure of this cover and screens
# the two continuum hypotheses it rests on (coverability, <=7 budget).
# =============================================================================================

def broken_vertices_under_core(pts, tol=1e-9):
    """Vertices of conv(pts) NOT illuminated by ANY core direction D0 = -V (Boltyanski: d
    illuminates y iff d.m < 0 for every active outer normal m). Returns the broken vertices."""
    A, b, H = _convex_hull_facets(pts)
    pts = np.asarray(pts, dtype=float)
    Vh = pts[H.vertices]

    def active_normals(y):
        return [A[k] for k in range(len(b)) if abs(A[k] @ y - b[k]) < 1e-7]

    broken = []
    for y in Vh:
        act = active_normals(y)
        if not act:
            continue
        if not any(all(float(np.dot(d, m)) < -tol for m in act) for d in CORE_DIRECTIONS):
            broken.append(y)
    return broken


def core_handles_octahedron():
    """SANITY / base case (re-uses E0): the 6 core directions illuminate the symmetric octahedron
    with ZERO broken vertices -- 0 corrections needed, total 6 <= 13."""
    broken = broken_vertices_under_core(octahedron_vertices_centered())
    print("E1 base case: core 6 directions on the symmetric octahedron ->",
          f"{len(broken)} broken vertices (expect 0).")
    assert len(broken) == 0, "core must fully illuminate the symmetric octahedron"
    return len(broken)


# ---------------------------------------------------------------------------------------------
# E1b-PREDICATE -- CLOSED (EXACT): Boltyanski illumination & corner-cover predicate in Fractions
# ---------------------------------------------------------------------------------------------
def _exact_facets(Vrat):
    """Exact outward facet normals (integer-cross-product) + a representative vertex per facet, for
    a polytope with rational vertices Vrat. scipy gives the COMBINATORICS; normals are recomputed in
    Fractions so the load-bearing illumination test is exact (proof-builder memory rule)."""
    from scipy.spatial import ConvexHull
    H = ConvexHull(np.array([[float(c) for c in v] for v in Vrat], dtype=float))
    n = len(Vrat)
    cen = tuple(Fr(sum(Vrat[i][k] for i in range(n)), n) for k in range(3))
    facets = []
    for simp in H.simplices:
        i, j, k = (int(x) for x in simp)
        nrm = _cross(_sub(Vrat[j], Vrat[i]), _sub(Vrat[k], Vrat[i]))
        if _dot(nrm, _sub(Vrat[i], cen)) < 0:
            nrm = tuple(-x for x in nrm)
        facets.append((nrm, Vrat[i]))
    return facets, [Vrat[v] for v in set(int(x) for x in H.vertices.tolist())]


def illumination_predicate_exact():
    """E1b-PREDICATE (CLOSED, EXACT). The per-vertex illumination predicate, computed in EXACT
    Fractions: direction d illuminates vertex y iff d.m < 0 for every facet normal m active at y
    (m.y == m.p for that facet's representative p). Corollary: corner direction -s (s in {+-1}^3)
    illuminates y iff s.m > 0 for all active m. Verified on a rational forced-family body; the
    broken set and its corner-cover are exact rational objects (no float on the load-bearing step)."""
    Vrat = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1),
            (Fr(9, 10), Fr(9, 10), Fr(9, 10))]
    facets, verts = _exact_facets(Vrat)

    def active(v):
        return [n for (n, p) in facets if _dot(n, v) == _dot(n, p)]

    broken = []
    for v in verts:
        act = active(v)
        if not act:
            continue
        if any(all(_dot(d, m) < 0 for m in act) for d in CORE_DIRECTIONS):
            continue  # illuminated by a core/axis direction => not broken
        cc = [s for s in CORNER_SIGNS if all(_dot(s, m) > 0 for m in act)]  # -s illuminates
        broken.append((v, cc))
    print("E1b-PREDICATE CLOSED (EXACT rational illumination via integer-cross-product normals):")
    for v, cc in broken:
        print(f"  broken vertex {tuple(str(c) for c in v)} illuminated by corner dirs -s, s in {cc}")
    # the (9/10)^3 corner bulge must be broken and illuminated exactly by corner -(1,1,1)
    assert len(broken) == 1 and broken[0][1] == [(1, 1, 1)], "exact corner-cover predicate failed"
    print("  => Boltyanski illumination + corner-cover predicate verified EXACTLY (Fractions).\n")
    return broken


# ---------------------------------------------------------------------------------------------
# E1b-FINITENESS -- CLOSED (EXACT): the corner cover is a finite hitting-set over 8 directions
# ---------------------------------------------------------------------------------------------
def _corner_cover_sets(pts, tol=1e-9):
    """For each broken vertex, the set of corner-sign indices j whose direction -CORNER_SIGNS[j]
    illuminates it. Float geometry for the screen (the EXACT version is illumination_predicate_exact)."""
    A, b, H = _convex_hull_facets(pts)
    pts = np.asarray(pts, dtype=float)
    Vh = pts[H.vertices]
    cov = []
    for y in Vh:
        act = [A[k] for k in range(len(b)) if abs(A[k] @ y - b[k]) < 1e-7]
        if not act:
            continue
        if any(all(float(np.dot(d, m)) < -tol for m in act) for d in CORE_DIRECTIONS):
            continue  # not broken
        hits = frozenset(j for j, s in enumerate(CORNER_SIGNS)
                         if all(float(np.dot(s, m)) > tol for m in act))
        cov.append(hits)
    return cov


def _min_hitting_set(cov):
    """Exact min number of corner directions hitting every broken vertex's cover set. None if some
    broken vertex has empty cover (NOT corner-coverable). <=8 by construction when coverable."""
    if any(len(h) == 0 for h in cov):
        return None
    universe = sorted(set().union(*cov)) if cov else []
    for r in range(0, len(universe) + 1):
        for S in itertools.combinations(universe, r):
            Ss = set(S)
            if all(Ss & h for h in cov):
                return r
    return 0


def corner_cover_is_finite_hitting_set():
    """E1b-FINITENESS (CLOSED, conditional). Covering the broken set by corner directions is, when
    every broken vertex is corner-coverable, a FINITE HITTING-SET over the 8 corner directions --
    so the corrective budget = min hitting-set size <= 8 (a finite rational object, a step toward
    Lean-fit). Demonstrated on a rational body: the broken set is covered by exactly its minimal
    corner subset, computed exactly."""
    Vrat = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1),
            (Fr(9, 10), Fr(9, 10), Fr(9, 10)), (Fr(-9, 10), Fr(-9, 10), Fr(9, 10))]
    facets, verts = _exact_facets(Vrat)

    def active(v):
        return [n for (n, p) in facets if _dot(n, v) == _dot(n, p)]

    cov = []
    for v in verts:
        act = active(v)
        if not act:
            continue
        if any(all(_dot(d, m) < 0 for m in act) for d in CORE_DIRECTIONS):
            continue
        cov.append(frozenset(j for j, s in enumerate(CORNER_SIGNS)
                             if all(_dot(s, m) > 0 for m in act)))
    k = _min_hitting_set(cov)
    print("E1b-FINITENESS CLOSED (EXACT, conditional on coverability):")
    print(f"  rational body with 2 opposite corner bulges -> {len(cov)} broken vertices,")
    print(f"  corner cover sets {[tuple(h) for h in cov]}; min hitting set = {k} corner directions.")
    assert k is not None and k == 2, "two opposite corner bulges need exactly 2 corner directions"
    print("  => the corrective cover is a FINITE rational hitting-set over 8 corners (<=8 always,")
    print("     and the screen below never needs > 5). Coverability is the open hypothesis.\n")
    return k


# ---------------------------------------------------------------------------------------------
# E1b-BUDGET SCREEN -- directed search (CONJECTURE with reproducible screen, NOT a proof)
# ---------------------------------------------------------------------------------------------
def broken_set_budget_screen():
    """E1b-BUDGET SCREEN (CONJECTURE). Adversarial directed search over a broad forced-family proxy
    (6 face-center contacts + arbitrary cube-interior vertices, incl. all-8-corners-bulged): record
    (a) whether the broken set is ALWAYS corner-coverable, (b) the max distinct corner directions
    needed. RESULT this round: always coverable; max hitting-set never > 5 (<= 7). This SUPPORTS the
    6+7=13 budget but is a SCREEN, not a proof -- the abstract version is false (see next function)."""
    FC = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], float)
    rng = np.random.default_rng(2024)
    maxk = 0
    maxbroken = 0
    uncoverable = 0
    hist = {}
    N = 12000
    for trial in range(N):
        mode = trial % 3
        if mode == 0:  # all 8 corners bulged (maximal asymmetry)
            extra = np.array([np.array(s, float) * rng.uniform(0.55, 0.99) for s in CORNER_SIGNS])
        elif mode == 1:  # random subset of corners
            idx = rng.choice(8, size=int(rng.integers(4, 9)), replace=False)
            extra = np.array([np.array(CORNER_SIGNS[i], float) * rng.uniform(0.55, 0.99) for i in idx])
        else:  # arbitrary interior vertices
            extra = rng.uniform(-0.98, 0.98, size=(int(rng.integers(4, 10)), 3))
        pts = np.vstack([FC, extra])
        try:
            cov = _corner_cover_sets(pts)
        except Exception:
            continue
        maxbroken = max(maxbroken, len(cov))
        k = _min_hitting_set(cov)
        if k is None:
            uncoverable += 1
            continue
        hist[k] = hist.get(k, 0) + 1
        maxk = max(maxk, k)
    print("E1b-BUDGET SCREEN (CONJECTURE -- reproducible directed search, NOT a proof):")
    print(f"  {N} forced-family-proxy bodies (incl. all-8-corners-bulged):")
    print(f"  broken set NOT corner-coverable in {uncoverable} bodies (0 => coverability screen holds)")
    print(f"  max broken vertices = {maxbroken}; max distinct corner directions needed = {maxk}")
    print(f"  histogram of corrective-direction counts: {dict(sorted(hist.items()))}")
    print(f"  => budget <= {maxk} observed (<= 7 target met with slack). CONJECTURAL: see below.\n")
    return maxk, uncoverable


def corner_coverability_is_not_generic():
    """E1b-HONEST LIMIT (CLOSED, EXACT). The abstract claim 'a pointed (=> illuminable) broken
    normal cone is corner-coverable' is FALSE. Exhibit a pointed broken normal set with NO covering
    corner direction. So corner-coverability is a genuine FORCED-FAMILY fact (it uses the cube /
    min-vol-box structure), NOT a generic combinatorial truth -- this pins where the open continuum
    content lives (E1a/E1b-COVERABILITY), and is why those holes are NOT hand-waveable."""
    # An explicit pointed (illuminable by a single d) broken normal set with no covering corner.
    # Found by exact integer search; verified here exactly. d = (-2,-4,3) gives d.m < 0 for all four
    # (so the cone is POINTED / vertex illuminable), yet NO corner sign s has s.m > 0 for all four.
    normals = [(3, 0, -3), (-1, 1, 0), (0, 3, 3), (-1, 0, -1)]
    illum_d = [dd for dd in [(-2, -4, 3)] if all(_dot(dd, m) < 0 for m in normals)]
    # broken: no axis direction illuminates
    axis_ok = any(all(_dot(ax, m) < 0 for m in normals) for ax in CORE_DIRECTIONS)
    # corner cover: any s with s.m>0 for all m?
    corner_ok = any(all(_dot(s, m) > 0 for m in normals) for s in CORNER_SIGNS)
    print("E1b-HONEST LIMIT CLOSED (EXACT): abstract 'pointed+broken => corner-coverable' is FALSE.")
    print(f"  normal set {normals}")
    print(f"  illuminable by a single direction (pointed): {len(illum_d) > 0} (e.g. d={illum_d[0] if illum_d else None})")
    print(f"  illuminated by some AXIS direction (=> not broken): {axis_ok}")
    print(f"  illuminated by some CORNER direction: {corner_ok}")
    assert len(illum_d) > 0 and not axis_ok and not corner_ok, "honest-limit witness failed"
    print("  => pointed + broken does NOT force corner-coverability. So coverability for the FORCED")
    print("     family is a real geometric fact needing the cube structure -- the open hole, honest.\n")
    return True


# ---------------------------------------------------------------------------------------------
# E1a -- OPEN HOLE: bound the size of the broken set from the min-vol-box geometry
# ---------------------------------------------------------------------------------------------
def broken_set_bounded_by_min_vol_box(eps):
    """HOLE E1a (LOAD-BEARING, OPEN). Bound |B(K)| for every K whose min-volume circumscribing
    parallelotope normalization forces p into N(1/2), from the min-vol-box optimality conditions
    (six face-center contacts + volume balancing bound the normal-fan tilt, hence how many vertices
    fall into a corner cone). Continuum/affine; UNPROVED. The screen shows |B(K)| <= 5 in practice
    but that is not a proof. This is the same continuum content E1b-COVERABILITY needs."""
    raise NotImplementedError(
        "HOLE E1a: |broken set| bounded by min-vol-box tilt -- needs the quantitative normal-fan "
        "deviation bound from the box optimality conditions (screened |B(K)|<=5, UNPROVED).")


# ---------------------------------------------------------------------------------------------
# E1b -- OPEN HOLE: every broken vertex corner-coverable + <=7 corner directions suffice
# ---------------------------------------------------------------------------------------------
def perturbed_directions_cover_broken_set(eps):
    """HOLE E1b (LOAD-BEARING, OPEN). Two sub-claims, both SCREENED (never refuted) but UNPROVED
    because the abstract version is provably FALSE (corner_coverability_is_not_generic):
      (E1b-COVERABILITY) every broken vertex of a forced-family body is corner-coverable -- needs
        the cube/min-vol-box structure to rule out the frustrated (non-corner-coverable) cones;
      (E1b-BUDGET<=7) the corner hitting-set has size <= 7 (volume balancing excludes the 8th).
    R4 CLOSED the FINITE structure conditional on coverability (corner_cover_is_finite_hitting_set)
    and screened both (broken_set_budget_screen: coverable, max 5). The proofs remain open."""
    raise NotImplementedError(
        "HOLE E1b: (coverability) every forced-family broken vertex corner-coverable -- NOT generic "
        "(see corner_coverability_is_not_generic), needs cube structure; (budget<=7) screened max 5, "
        "UNPROVED. The finite hitting-set structure is CLOSED conditional on coverability.")


def near_one_half_illuminated_by_13(eps):
    """HOLE E1 (LOAD-BEARING, OPEN -- ASSEMBLY). For every K in the Prymak-forced family at p~1/2,
    I(K) <= 13 = 6 core (E0, CLOSED) + <=7 corrective corner directions (E1a |broken| bound +
    E1b coverability & <=7 budget). NOT established -- rests on the honest holes E1a, E1b."""
    broken_set_bounded_by_min_vol_box(eps)      # E1a
    perturbed_directions_cover_broken_set(eps)  # E1b
    return 13


def main():
    print("Sketch E (octahedral-direct) -- R4: E1b structure CLOSED (exact, finite); E1a + E1b")
    print("coverability/budget honestly OPEN (continuum).\n")
    enlargement_is_dead_screen()
    print("--- CLOSED (E0, E2-core SUFFICIENT criterion) ---")
    lassak_symmetric_illumination()
    illumination_stability_criterion()
    counterexample_face_center_not_symmetric()
    print("--- E1 RE-PLANNED: asymmetry-tolerant <=13 = 6 core + <=7 corner corrective ---")
    core_handles_octahedron()
    print()
    print("--- R4 NEW: E1b structure (CHECKED IN CODE) ---")
    illumination_predicate_exact()          # EXACT predicate
    corner_cover_is_finite_hitting_set()    # EXACT finite cover (conditional on coverability)
    broken_set_budget_screen()              # directed screen (conjecture)
    corner_coverability_is_not_generic()    # EXACT honest limit
    print("--- OPEN holes (the continuum wall) ---")
    for fn, name in ((broken_set_bounded_by_min_vol_box, "E1a"),
                     (perturbed_directions_cover_broken_set, "E1b"),
                     (near_one_half_illuminated_by_13, "E1")):
        try:
            fn(0.05)
        except NotImplementedError as e:
            print(f"OPEN {name}:", e)
    print()
    print("SUMMARY: E0 + E2-core CLOSED. R4 NEW (CHECKED IN CODE): the E1b corrective cover is an")
    print("EXACT FINITE hitting-set over the 8 corner directions (<=8 always; screen never > 5), with")
    print("the Boltyanski illumination predicate verified EXACTLY in Fractions. The two hypotheses it")
    print("rests on -- (coverability) every forced-family broken vertex is corner-coverable, and")
    print("(budget) <=7 corners suffice -- are SCREENED (never refuted) but CONJECTURAL: the abstract")
    print("version is provably FALSE, so they need the cube/min-vol-box geometry (E1a). E1a + E1b stay")
    print("honest open holes. UNCONDITIONAL H3<=13 near-1/2 NOT established. Claimed bound: NONE.")


if __name__ == "__main__":
    main()
