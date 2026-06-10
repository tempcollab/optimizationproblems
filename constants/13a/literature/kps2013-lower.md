# KPS 2013 (Khandhawit–Pagonakis–Sriswasdi) Moser worm lower bound (arXiv:1101.5638)

**Verified value to beat:** a ≥ 0.232239 [KPS2013]. Prior: Wetzel 0.2194 (broadworms);
KS2009 0.227498 (V-worms = equilateral-triangle hull, U-worms = square hull).
Upper bound for 13a: π/12 = 0.2617993878 (Wetzel's 30° sector, PW2021). Gap ~0.0296.

**Method (analytic min–max, NOT a clean construction).**
- The convex cover must contain a congruent copy of every unit-length arc. KPS force a
  configuration of specific worms (the unit **broadworm** plus parametrized worms) and
  bound the area of the convex hull of forced point sets ABCDEFPQ from below by summing
  areas of disjoint sub-triangles (BEC, AP B, DF A, CQD), handling all intersection cases.
- Final step: minimize a max of four explicit functions F(α,β)=max{p(α),q(β),f(α,β),g(α)}
  over a 2-parameter domain; proven F ≥ 0.232239 by a 4-case piecewise analysis.
- The paper notes section 3's variation "does not improve" the bound (line ~1841).

**Where the slack is:** the bound is a min–max over a chosen finite worm family; richer
forced families / more sub-triangles could raise it. But this is an ANALYTIC proof
(piecewise estimates + case analysis), not a numpy/scipy construction — improving it means
a sharper inequality, not a search. Less tractable for a single construction-focused run
than the Lebesgue (13b) lower bound, which is a clean finite placement optimization.
