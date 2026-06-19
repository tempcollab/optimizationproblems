# gri-augment — augment Gri's 63-dim W-set, then drop a dimension

**Attack line B** (explorer §5). A refinement of the record construction.

## Target
Engineer a `>= 316`-point set inside (or extending) Gri's 63-dim subspace `W`
that lies in a common **62-dim** subspace, with smaller-diameter parts (cliques)
`<= 5`, so `ceil(n/5) >= 64 > 63`.

## Mechanism
Gri added **one** projected point `p = t·z_b` (`z_b = x_b − S1/32 ∈ W`,
`78t²+12t=102`) to the 320-pt C-set to reach `ceil(321/5)=65` at dim 63. We add a
*controlled set* of such points and simultaneously force a 4th orthogonal
direction, dropping to dim 62.

Two sub-strategies:
- **B1 drop-in-W:** find `r ∈ W` orthogonal to ≥316 of the (C-points + added
  points). Obstruction: no hyperplane of `W` holds more than a handful of C-points
  (explorer §4), so added points must supply the codimension.
- **B2 replace-and-drop:** remove a structured cluster `C0` whose removal frees a
  direction, add back `≥|C0|` projected points sharing a hyperplane; net stay
  `≥316`, gain one codim, keep `omega ≤ 5`.

## Holes
1. **`gri_W_and_Cpoints`** — build_g24 + W (dim 63) + C-points (scaffold, Gri
   Lemmas 1–3).
2. **`engineer_augment_in_codim1` (load-bearing)** — produce ≥316 points in a
   common 62-dim subspace of `W` with `omega ≤ 5`. Crux: since C is general
   position, ~300 *added* engineered points on a hyperplane `{y·r=0}` must each
   preserve `omega ≤ 5` — a hard packing problem. State precisely, test small
   cases (can we add 2, 3, 5 points and keep clique cap?).
3. **`verify`** — Lean-fit: recompute the *augmented* diameter graph (added points
   create NEW edges, must re-derive), check dim≤62 + omega≤5 + ceil(n/5)≥64.

## What would push it
Start by reproducing Gri's single-point check, then test whether *two* projected
points `t·z_b, t·z_{b'}` (`b,b'∈B1`) can be co-engineered into a 62-dim subspace.
The diameter-graph recomputation on the augmented set is the reusable Lean-fit
core; the packing feasibility is the real unknown.

## Self-assessment
Builds directly on the verified record, so the certification path is the most
trustworthy. But it inherits the same wall (C has no spare direction), pushing all
the burden onto the added points — likely infeasible to reach 316 added points
with omega 5. Medium-low feasibility; high value because it reuses Gri's verified
machinery and any partial result tightens the margin understanding.
