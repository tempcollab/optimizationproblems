"""
Sketch — minvol-corner-slack: the QUANTITATIVE corner-slack certificate that unlocks the
near-p=1/2 half of H_3 <= 13. This is the single missing lemma the explorer (R2) named as the
load-bearing open problem of the run. Numerical (Lean-hostile: a continuum/affine estimate).

----------------------------------------------------------------------------------------------
THE GAP THIS CLOSES
----------------------------------------------------------------------------------------------
At and near p=(1/2,...,1/2), the covering piece O_p (the regular octahedron, conv of the 6 face
contacts) CANNOT give a 13-cover: the 14 marked points are pairwise l1-uncoverable by int(O_p)
(Remark 2.3, VERIFIED R1 as F0 -- a hard 14-floor with piece O_p). The ONLY escape at/near p=1/2
is a STRICTLY LARGER admissible piece W with O_p ⊆ W ⊆ int(K), where the slack comes from F2
(VERIFIED R1): a body K forced to the cube as its MINIMAL-VOLUME circumscribing parallelotope,
with face-center contacts, is strictly larger than O_p -- vol(O_p)=1/6 while K must have volume
near 1 to keep the cube minimal. So there IS room; the open problem is making it QUANTITATIVE and
DIRECTIONAL.

R2-outliner screen sharpened the DIRECTION (this is the crux the prior 'enlarge toward corners'
framing got wrong): the 51 tight marked pairs decompose as 12 VV (cube-edge, diff e.g. (0,0,1)),
24 Vq (vertex-facecenter, diff e.g. (0,1/2,1/2)), 15 qq (facecenter-facecenter). To merge ANY
tight pair, W-W must contain that difference in its interior. The Vq differences point along
FACE-DIAGONAL / EDGE-MIDPOINT directions (0,1,1), NOT toward cube corners. So W must enlarge O_p
toward the cube EDGE-MIDPOINTS, and the min-vol-box condition must guarantee room THERE.

----------------------------------------------------------------------------------------------
THE LOAD-BEARING HOLE (H_SLACK)
----------------------------------------------------------------------------------------------
LEMMA (to prove): There is an explicit rational margin s* > 0 such that EVERY convex body K whose
minimal-volume circumscribing parallelotope is the cube and whose Prymak contacts force
p in N(1/2) (the rational neighborhood the generic regime excludes) contains the enlarged piece
    W = conv(O_p ∪ { edge-midpoint-pushed points at margin s* }) ,
and W-W contains at least one tight marked-pair difference in its interior -- so one translate of
int(W) covers two marked points, dropping the local count 14 -> 13.

The bound s* must come from the MINIMAL-VOLUME-BOX OPTIMALITY condition, NOT from the contacts
(the cube corners/edge-midpoints carry no contact). Min-vol-box optimality (classical: the
minimal-volume enclosing parallelepiped touches each facet, and the contact configuration is
'balanced' so no shear/scaling shrinks it) forces K to occupy a quantifiable fraction of the cube
near each edge -- otherwise a smaller sheared box exists. Turning that into an explicit rational s*
valid across all such K is the continuum estimate (Lean-hostile; directed-rounded numerical
certificate, adversarially re-derivable).

----------------------------------------------------------------------------------------------
WHAT THIS SCRIPT DOES NOW (the screen) vs. the open hole
----------------------------------------------------------------------------------------------
Closed/screened (exact rational where possible):
  * the tight-pair direction analysis (which marked-pair differences are reachable by enlarging O_p
    toward edge-midpoints) -- exact.
Open (the genuine blocker, raises NotImplementedError):
  * H_SLACK: the min-vol-box lower bound s* itself, valid uniformly over the forced family. This is
    a continuum optimization (min volume sheared box >= cube => K fat near edges). NOT closed.
"""
from fractions import Fraction as F
import itertools
import numpy as np
from scipy.spatial import ConvexHull


def Vp(p):
    p1, p2, p3, p4, p5, p6 = p
    return [(F(0), p1, p2), (F(1), p1, p2),
            (p3, F(0), p4), (p3, F(1), p4),
            (p5, p6, F(0)), (p5, p6, F(1))]


def marked_points():
    verts = [tuple(F(c) for c in v) for v in itertools.product([0, 1], repeat=3)]
    return verts + Vp([F(1, 2)] * 6)


def l1(a, b):
    return sum(abs(a[k] - b[k]) for k in range(3))


def tight_pairs():
    """Exact: the marked pairs at l1-distance exactly 1, with their difference vectors."""
    M = marked_points()
    out = []
    for i, j in itertools.combinations(range(14), 2):
        if l1(M[i], M[j]) == 1:
            diff = tuple(M[i][k] - M[j][k] for k in range(3))
            out.append((i, j, diff))
    return out


def edge_midpoint_directions():
    """Unit (face-diagonal) directions from cube center toward the 12 edge-midpoints."""
    dirs = []
    for axis in range(3):
        for s1 in (-1, 1):
            for s2 in (-1, 1):
                d = [0, 0, 0]
                others = [k for k in range(3) if k != axis]
                d[others[0]] = s1
                d[others[1]] = s2
                dirs.append(tuple(F(x) for x in d))
    return dirs


def enlarged_piece_W(s):
    """W = conv(O_p face centers ∪ points pushed from center toward each edge-midpoint by margin s).
       Returns the vertex list (floats) for hull/difference-body tests."""
    fc = Vp([F(1, 2)] * 6)
    extra = []
    center = (F(1, 2), F(1, 2), F(1, 2))
    for d in edge_midpoint_directions():
        # edge midpoint is center + (1/2)*d (normalized along the 2 nonzero coords);
        # push O_p toward it by fraction s of the way to the edge midpoint
        em = tuple(center[k] + F(1, 2) * d[k] for k in range(3))
        extra.append(tuple(center[k] + s * (em[k] - center[k]) for k in range(3)))
    return [tuple(float(c) for c in v) for v in fc + extra]


def diffbody_covers(Wverts, diff, eps=1e-9):
    """Does `diff` lie in the interior of W - W? (Necessary support-width test.)"""
    W = np.array(Wverts)
    h = ConvexHull(W)
    A = h.equations[:, :3]
    d = np.array([float(x) for x in diff])
    for j in range(len(A)):
        n = A[j]
        width = (W @ n).max() - (W @ n).min()
        if abs(n @ d) >= width - eps:
            return False
    return True


def screen():
    print("=== minvol-corner-slack: direction screen (exact + numeric) ===\n")
    tp = tight_pairs()
    from collections import Counter
    by_type = Counter()
    M = marked_points()
    for i, j, diff in tp:
        ti = 'V' if i < 8 else 'q'
        tj = 'V' if j < 8 else 'q'
        by_type[''.join(sorted(ti + tj))] += 1
    print(f"tight marked pairs (l1=1 exactly): {len(tp)}  by type {dict(by_type)}")
    print("To beat 14 at p=1/2, W-W must contain >=1 of these differences in its interior.\n")

    print("Enlarging O_p toward EDGE-MIDPOINTS (face-diagonal dirs) by margin s:")
    found_at = None
    for s in [F(1, 20), F(1, 10), F(3, 20), F(1, 5), F(1, 4), F(3, 10), F(7, 20), F(2, 5)]:
        W = enlarged_piece_W(s)
        covered = [(i, j) for (i, j, d) in tp if diffbody_covers(W, d)]
        print(f"  s={float(s):.3f}: tight pairs now coverable by int(W-W): {len(covered)}"
              + (f"  e.g. {covered[0]}" if covered else ""))
        if covered and found_at is None:
            found_at = s
    print()
    if found_at is not None:
        print(f"SCREEN POSITIVE: enlargement margin s>={float(found_at):.3f} toward edge-midpoints"
              f" merges a tight pair -> a 13-cover becomes geometrically possible IF K guarantees"
              f" that much room. The open hole is whether the min-vol-box condition forces s*>=that.")
    else:
        print("SCREEN NEGATIVE at tested margins: edge-midpoint enlargement alone does not merge a"
              " tight pair; W must enlarge along the actual tight-difference directions -- builder"
              " to search the correct W shape.")


def minvol_box_lower_bound():
    """H_SLACK -- THE OPEN HOLE.
    Prove: every K with min-vol box = cube and face-center contacts contains W at margin s*.
    Needs the continuum min-volume-parallelepiped optimality estimate. NOT closed."""
    raise NotImplementedError(
        "H_SLACK (load-bearing): explicit rational s* from the minimal-volume-box optimality "
        "condition, valid uniformly over the family of bodies forced to p in N(1/2). Continuum "
        "estimate (Lean-hostile); to be a directed-rounded, adversarially re-derivable certificate."
    )


if __name__ == "__main__":
    screen()
    print("\n--- open hole H_SLACK ---")
    try:
        minvol_box_lower_bound()
    except NotImplementedError as e:
        print("OPEN:", e)
