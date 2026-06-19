"""
Sketch E -- octahedral-direct: bypass the skeleton reduction at the worst case. Cover the
ACTUAL worst body near p=1/2 directly by 13 (or fewer) translates of its own interior, using
illumination, instead of forcing the cube-skeleton-with-O_p cover that hits the 14 ceiling.

Strategy
--------
The 14-ceiling at p=1/2 is an ARTIFACT of the reduction: it demands the full cube skeleton E
be covered by translates of the small octahedron int(O_p). But the body actually being bounded
at p=1/2 is (an affine image of) a near-octahedral / near-symmetric body, whose true
illumination number is much smaller -- a centrally symmetric body in R^3 has H <= 8 (Lassak
H_3^s = 8). The reduction throws this away.

Plan:
  (E1) Identify the family of bodies K that force p near (1/2,...,1/2) under Prymak's
       normalization -- they are the bodies whose minimal-volume box has all six contacts near
       face centers. Characterize this family (octahedron-like, possibly with small asymmetric
       perturbations).
  (E2) For this family directly: H(K) = C(K, int K) <= 13 via an explicit illumination /
       homothety cover -- e.g. 6 directions from the symmetric core (Lassak-type) + a bounded
       number of corrective translates for the asymmetry, total <= 13.
  (E3) Glue: for p OUTSIDE the p=1/2 family, Prymak's existing LP already gives <= 14, and
       in fact the obstruction only bites at p=1/2, so a 13-piece tau works there (cf. sketch A
       regime R1). Combine to a global <= 13.

This is the cleanest conceptual attack (treats the genuine extremal body on its own terms) but
the "characterize + directly cover the family" step is the hard, partly-continuum hole.

This file frames the family + direct cover; steps are TODO holes.
"""

import numpy as np
import itertools

def octahedron():
    """The p=1/2 contact polytope: regular octahedron = conv of cube-face midpoints."""
    return np.array([
        [0.0, 0.5, 0.5], [1.0, 0.5, 0.5],
        [0.5, 0.0, 0.5], [0.5, 1.0, 0.5],
        [0.5, 0.5, 0.0], [0.5, 0.5, 1.0],
    ])

def octahedron_symmetric_cover_count():
    """
    Sanity: the octahedron is centrally symmetric, so by Lassak H_3^s = 8 it is illuminated
    by <= 8 translates of its interior -- FAR below 14. Demonstrates the reduction's loss.
    HOLE E0 (mechanical): exhibit 8 explicit illumination directions for the octahedron.
    """
    raise NotImplementedError("HOLE E0: 8 explicit illumination directions for the octahedron")

def worst_case_family():
    """
    HOLE E1 (crux part 1). Characterize the family F of convex bodies K whose Prymak
    normalization forces p in a neighborhood of (1/2,...,1/2). Show F consists of
    octahedron-like bodies (symmetric core + controlled asymmetry), so each K in F is close
    to centrally symmetric.
    """
    raise NotImplementedError("HOLE E1: characterize the p~1/2 worst-case body family F")

def direct_cover_le_13(K_in_family):
    """
    HOLE E2 (crux part 2). For every K in F, exhibit an explicit cover of K by <= 13 translates
    of int(K): 6-8 symmetric-core directions (Lassak-type) plus a bounded number of corrective
    translates handling the asymmetry. Output the translate vectors and a coverage proof.
    """
    raise NotImplementedError("HOLE E2: <= 13 direct illumination/translate cover for K in F")

def glue_outside_family():
    """
    HOLE E3. For p outside the neighborhood of 1/2, a 13-piece tau is feasible in Prymak's LP
    (the obstruction is local to p=1/2). Combine with E2 for a global H_3 <= 13.
    """
    raise NotImplementedError("HOLE E3: 13-piece cover for p outside the worst-case family")

def main():
    print("Sketch E (octahedral-direct) -- building stub.")
    print("Insight: the 14-ceiling is a reduction artifact; the genuine p=1/2 body is")
    print("near-symmetric (H <= 8). Crux E1+E2: characterize and directly cover that family by <= 13.")

if __name__ == "__main__":
    main()
