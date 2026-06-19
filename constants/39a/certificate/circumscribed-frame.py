"""
Sketch B -- circumscribed-frame: change the normalization away from the minimal-volume
parallelotope so the worst case p=(1/2,...,1/2) is never forced, lowering the per-cell
covering count below 14.

Strategy
--------
Prymak normalizes K by its minimal-volume circumscribed parallelotope C, maps C=[0,1]^3.
This FORCES the cube skeleton E and admits the bad p=1/2 configuration. The reduction is
lossy precisely there. Two normalization changes to try:

  (B1) A different circumscribing FRAME -- e.g. a parallelotope chosen to *minimize the
       worst-case per-cell count* rather than volume, or a non-parallelotope frame (a prism
       over a hexagon / a frame adapted to K's contact directions) -- such that the analogue
       of Prymak's max over p has value <= 13.

  (B2) A two-frame / case split: if K's minimal-volume box is "cube-like" (near the bad
       symmetric case) use frame F1; otherwise use Prymak's box. Pick frames so each regime
       certifies <= 13.

The reduction lemmas (Prymak Lemma 2.1/2.2) must be re-derived for the new frame: the frame
must still contain a 6-point contact configuration whose contact polytope O' is inside K, and
covering E' cup V' with translates of int(O') must need <= 13.

This file frames the frame-selection + re-derived reduction; steps are TODO holes.
"""

import numpy as np

def minimal_volume_parallelotope(K_vertices):
    """Prymak's normalization (baseline, for comparison). HOLE B0 (bookkeeping):
    compute the minimal-volume circumscribed parallelotope of a polytope K."""
    raise NotImplementedError("HOLE B0: minimal-volume circumscribed parallelotope (baseline)")

def alternative_frame(K_vertices):
    """
    HOLE B1 (crux). Construct an alternative circumscribed frame F (parallelotope or other
    polytope) for K such that:
      (i)  F contains a 6-point (or k-point) contact configuration with contact polytope
           O' = conv(contacts) subseteq K, and
      (ii) the worst-case over the frame's parameter space of C(E' cup V', int(O')) is <= 13.
    Return F's facet/vertex description and the contact configuration. The frame must exist
    for EVERY convex body K (this is the load-bearing universality claim).
    """
    raise NotImplementedError("HOLE B1: alternative circumscribed frame with per-cell count <= 13")

def reduction_lemma(frame, K_vertices):
    """
    HOLE B2. Re-derive the Prymak Lemma 2.1/2.2 analogue for the new frame:
        C(K, int K) <= max over frame-params of C(E' cup V', int(O')).
    Continuum/affine step -- likely Lean-hostile; certify by an adversarial hand-rederivation.
    """
    raise NotImplementedError("HOLE B2: reduction lemma for the alternative frame")

def per_cell_le_13(frame_box):
    """HOLE B3. Per-cell covering count <= 13 over the new frame's parameter atlas
    (rational LP feasibility analogue)."""
    raise NotImplementedError("HOLE B3: per-cell <= 13 over the new frame's atlas")

def main():
    print("Sketch B (circumscribed-frame) -- building stub.")
    print("Crux hole B1: a circumscribed frame that avoids the p=1/2 worst case for ALL K,")
    print("with re-derived reduction (B2, likely Lean-hostile) and per-cell <= 13 (B3).")

if __name__ == "__main__":
    main()
