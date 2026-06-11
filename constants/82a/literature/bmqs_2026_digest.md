# Digest: BMQS [BMQS] "Closing the gap around the essential minimum of height functions with linear programming" (arXiv:2601.18978, 2026)

Authors: Burgos Gil, Menares, Qu, Sombra. PDF: constants/82a/literature/pdfs/bmqs2601.18978.pdf. Text /tmp/bmqs.txt.

## What it is
A THEORETICAL / structural paper. Main message: the two classical methods for the essential
minimum of a height h_g (with Green function g) are LP-DUAL to each other, and strong duality holds.

- LOWER-bound method (Smyth / dual problem D(g)):
    D(g) = sup over k, a_i>=0, P_i in Z[x]\{0} of  inf_{z in C} ( g(z) - sum_i a_i log|P_i(z)| ).
  This is exactly Smyth's auxiliary-function method (= Flammang's, with g = the ZZ Green function).
- UPPER-bound method (primal P(g)):
    P(g) = inf over conjugation-invariant prob. measures mu with int log|Q| dmu >= 0 for all Q in Z[x]\{0}
           of  int g dmu.
- Theorem D (Thm 6.5): D(g) = ess(h_g) = P(g). Strong duality "closes the gap from both ends."
- Theorem E (Thm 7.6): if g is a *computable* Green function, ess(h_g) is a computable real number
  (a theoretical algorithm: reduce D and P to countable subsets, generate converging upper/lower
  sequences, stop when within precision). Uses Smith-Orloski-Sardari (Thm 4.1): measures
  approximable by Galois orbits of algebraic integers are exactly those with int log|Q| dmu >= 0.

## CRUCIAL caveats for us
- BMQS reports the bounds as  0.248247 <= ess(h_ZZ) <= 0.254437  (Zagier/Doche). They do NOT cite
  Flammang's 0.24874 -- so the VERIFIED record in the registry (0.24874 [F18]) is BETTER than the
  number BMQS quote. The registry's bar stands.
- They explicitly state (intro, sec 1.7): "no practical algorithm is known to approximate them up
  to any arbitrary precision ... after a few iterations the methods reach a point where it is
  unclear how to continue, due to the enormous size of the search space and the lack of an
  efficient criterion to find the optimal direction."
- "The obtained algorithm is far from being practical" (their own words, sec ~7).
- They give NO new numerical bound, NO finite LP recipe, NO table, NO computation for ZZ.

## Value to us
- Confirms the lower-bound pipeline IS an LP (semi-infinite), so numpy/scipy linprog is the right
  tool to reproduce/re-optimize Flammang's auxiliary function.
- Confirms the upper-bound side is a measure-LP; an explicit good measure (atomic, supported on
  conjugate sets of low-measure polynomials) gives upper bounds -- this is Doche's perturbed-poly
  approach.
- Does NOT itself move any bound. Its contribution is conceptual (duality/computability), so it is
  NOT a ready-made route to a record break; but it validates the LP framing the builder will use.
