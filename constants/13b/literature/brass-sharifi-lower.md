# Brass–Sharifi 2005 lower bound for Lebesgue's universal cover (the soft target)

**Verified value to beat:** a ≥ 0.832 [BS2005] (Int. J. Comput. Geom. Appl. 15, 537–544).
Prior lower bounds: trivial π/4 = 0.7854 (disk); Elekes 1994 0.8257 (disk + equilateral
triangle), 0.8271 (disk + regular 3^j-gons).

**Method (finite computer-aided construction — reproducible).**
- A lower bound for a is obtained from a FINITE family of diameter-1 convex shapes:
  any universal cover must contain a congruent (rigid-motion + reflection) copy of EACH
  shape simultaneously. So
      a ≥ min over rigid placements of {S_1,...,S_k} of Area(conv(⋃ placed S_i)).
  i.e. place each shape by its own rigid motion to MINIMIZE the area of the convex hull of
  the union; that minimum is a valid lower bound.
- Brass–Sharifi used three shapes: a **circle (disk)**, an **equilateral triangle**, and a
  **regular pentagon**, all of diameter 1, "in a certain alignment," with a computer search
  over placements. Result a ≥ 0.832. (Confirmed in BBG2015 §intro.)

**Reproduction status (June 2026):** arXiv:2606.04458 (Xie, 2026) provides a *reproducible
certificate* for the 0.832 bound (adaptive ledger + terminal-route replay + local
lower-bound certificate families). It REPRODUCES, does NOT improve, 0.832. So 0.832 is the
verified bar; nothing newer beats it.

**Where the slack is (concrete openings prior work did not push):**
1. **More shapes.** Only 3 shapes were used. Adding diameter-1 shapes — Reuleaux triangle
   and other constant-width curves (Vrećica: it suffices to cover all constant-width-1 sets,
   so constant-width shapes are the *right* test family), regular heptagon/9-gon, "lens"
   sets, Cantor-set-of-breadth shapes (Elekes) — each can only raise the min-hull area.
   The bound is monotone non-decreasing in the shape set.
2. **Better joint placement / global optimization.** BS used "a certain alignment" + search.
   A modern global optimizer (basin-hopping / SLSQP over each shape's (x,y,θ) plus reflection
   flag, computing Area(conv(union)) via scipy ConvexHull) can both reproduce 0.832 and search
   richer configs. The objective is a min (over placements) of a max-type hull area — the
   *floor* of that min over a *larger* shape set is the lower bound.
3. **Rigor caveat:** a numerical min over placements is only a lower bound if you certify
   that the reported configuration is a true global *minimum* of the hull area (or you bound
   the hull area from below over ALL placements). The honest reviewer-grade route is: pick a
   small shape family, discretize/branch the placement space, and prove a verified floor
   (interval arithmetic or a covering argument over the placement grid). This is the load-
   bearing step.

**Gap:** lower 0.832 vs upper 0.8440936 — a 0.0121 gap, vs a 2.2e-5-scale frontier on the
upper side. The lower bound is the clearly softer, more tractable side.
