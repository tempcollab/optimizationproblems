# mixed-construction — clique-cap-5 core + non-two-distance perturbation in 62 dims

**Attack line D** (explorer §5). The speculative wildcard.

## Target
A finite point set `X` in `R^62`, `|X| >= 316`, whose **diameter graph** has clique
number `<= 5`, giving `ceil(|X|/5) >= 64 > 63`. `X` need NOT be two-distance.

## Mechanism / the relaxation
Gri's record set is already non-two-distance (the added `p` makes a third
distance) — proving the part-cap can come from the *diameter graph's* clique
number, not from a single SRG. We exploit this: take a two-distance **core** `K`
that genuinely sits in `<= 62` dims (even if `|K| < 316`), then add a
**perturbation** set `P` of general points so that `X = K ∪ P` keeps
diameter-clique `<= 5`, reaches `>= 316` points, and stays in the same 62-dim
subspace. Gri used one non-two-distance point to buy a *point*; we use a
controlled set to buy a *dimension*.

## Holes
1. **`build_core`** — a `<=62`-dim two-distance core (from a `srg-sweep` survivor,
   a trimmed `G_2(4)` section, or a Bondarenko product/section trimmed to 62 dims).
2. **`engineer_perturbation` (load-bearing)** — add points to reach `>=316` in a
   common 62-dim subspace with diameter-clique `<= 5`. Each added point creates new
   diameter edges; capping the clique at 5 while hitting 316 is the open
   construction. Model as constrained packing / SAT search over candidate points.
3. **`verify`** — Lean-fit: build the diameter graph directly from pairwise
   distances (so the clique = smaller-diameter equivalence is re-derived, not
   assumed), check dim≤62 + omega≤5 + ceil(n/5)≥64.

## Dependency / how it evades the obstruction
Unlike A/B it does NOT require `C` (or any single SRG) to drop to 62 dims; the
dimension is satisfied by `K` from the start, and the count is made up by general
points whose only constraint is the finite clique cap. This sidesteps the
"general position, no 4th direction" wall — at the cost of a much larger,
less-structured search. Feeds on `srg-sweep` for the core.

## Self-assessment
Most flexible, least constrained by the named obstruction, but also the least
structured — the cap-5 packing of ~300 perturbation points is a large search with
no guarantee. High informativeness as a relaxation; if even a partial mixed set
reaches `n` in 62 dims with omega 5, it reframes the whole frontier. Lowest
near-term feasibility, highest conceptual upside. Run after srg-sweep seeds a core.
