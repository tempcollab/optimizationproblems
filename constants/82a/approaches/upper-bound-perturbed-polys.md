# Approach: upper bound via low-Zhang-Zagier-measure polynomial families

Status: PROPOSED (round 1). Third-ranked / fallback. Higher risk, less reproducible.
Moves: UPPER bound. Target: strictly < 0.25444 = log(1.287527) [Doche Doc01b].

## Idea
The upper bound is a WITNESS: any single algebraic integer alpha with zeta(alpha) < 1.287527
gives C_82 <= log zeta(alpha) (essential minimum <= any spectrum value, modulo finiteness — more
precisely the ess min is <= any accumulation value; Doche's family construction is the rigorous
route). Doche's record is a degree-32 "perturbed" polynomial with measure 1.287527. BMQS frame
the upper side as the primal measure-LP P(g): minimize int g dmu over conjugation-invariant
probability measures mu with int log|Q| dmu >= 0 for all integer Q.
Find a better explicit family (lower measure) than Doche's degree-32 example.

## Skeleton
1. Reconstruct Doche's perturbed-polynomial construction (Doc01b): families built by perturbing
   coefficients of products related to x(1-x) to keep all roots clustered near 0 and 1, minimizing
   M(alpha)M(1-alpha)^{1/d}. (Need to fetch Doc01b — not yet digested; explorer flagged it as a
   one-off with no reproducible LP.)
2. Search a parameterized family (e.g. resultant/composition constructions, degree 32-64) for a
   minimal-polynomial whose Zhang-Zagier measure zeta = (M(alpha)M(1-alpha))^{1/d} is rigorously
   < 1.287527. Compute M via roots (Graeffe / high-precision root-finding) with a rigorous
   enclosure (interval root bounds) so the measure is a certified upper bound.
3. Verify alpha is an algebraic integer (integer minimal polynomial, leading coeff 1) and irreducible
   (so the measure formula applies cleanly), then C_82 <= log zeta(alpha).

## Artifact
`certificate/upper_witness.py` producing an explicit integer minimal polynomial P, a rigorous
upper enclosure of zeta(alpha), and the resulting upper bound < 0.25444.

## HARDEST step (named)
Producing an integer polynomial with rigorously certified Zhang-Zagier measure below 1.287527.
- Mechanism: zeta is minimized by polynomials whose roots and the roots of 1-x are both close to
  the unit circle / clustered to make max(1,|root|) products small. Doche found 1.287527 at degree
  32; the conjecture (Flammang) is this IS the next spectrum point, so beating it likely requires
  HIGHER degree and a genuinely new construction, not a perturbation of Doche's.
- Why hard: the explorer notes the upper side has "no reproducible LP recipe" and "less obvious
  slack"; if 1.287527 is the true next spectrum point the upper bound may already be essentially
  tight from above near there, leaving little room.
- Risk: HIGHEST of the three. No reproducible engine; pure search over a poorly-charted family;
  rigorous measure-enclosure adds work. Doc01b not yet digested.

## Check the builder runs
The integer polynomial P, a certified interval enclosure of each |root| and of zeta, and the
arithmetic giving log zeta < 0.25444. Reviewer recomputes the roots and the measure.

## Spec review: required
(No reproducible recipe, depends on un-digested Doc01b, unclear there is room below the conjectured
next spectrum point. Do NOT pursue unless Angles 1-2 stall.)
