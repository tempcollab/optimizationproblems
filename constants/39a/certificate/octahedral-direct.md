# Certificate record — sketch E `octahedral-direct` (numerical, Lean-hostile)

This is the near-$p\approx1/2$ direct-illumination route. Its load-bearing estimate is
continuum/affine (illumination stability under perturbation), so the check is a numerical
certificate (directed-rounded / exact-rational), not `lake build`.

## Reproduction command
```
python3 constants/39a/certificate/octahedral-direct.py
```
Runs clean (exit 0). Closed steps print their exact/directed-rounded verifications; the open
hole E1 prints `OPEN E1:` and the script ends with an honest SUMMARY (no unconditional bound
yet — the target is NOT hole-free).

## What is CLOSED (exact / directed-rounded)
Carried from R3:
- `enlargement_is_dead_screen` — exact: $O_p-O_p$ = unit cube, tight pairs on the boundary.
- `lassak_symmetric_illumination` (E0) — **exact rational**: $D=-V$ illuminates the octahedron,
  margin **= 1** (unnormalized) $=1/\sqrt3$. So $I(\text{octahedron})\le 6\le 13$.
- `illumination_stability_criterion` / `orthant_coherent` (E2-core, **Lemma S'**) — exact
  **SUFFICIENT** criterion + directed-rounded sweep (threshold $t\approx0.30$). The forced family
  need NOT meet it, so E1 was re-planned away from this $\le6$ target.
- `counterexample_face_center_not_symmetric` — exact: $p=1/2$ contacts do NOT force coherence
  (why E1 is the asymmetry-tolerant $\le13$ budget now).

**R4 NEW — the E1b corrective-cover STRUCTURE (checked in code):**
- `illumination_predicate_exact` (E1b-PREDICATE) — **exact rational** Boltyanski illumination
  predicate from integer-cross-product facet normals: $d$ illuminates vertex $y$ iff $d\cdot m<0$
  for every active normal $m$; corollary, corner $-s$ ($s\in\{\pm1\}^3$) illuminates iff
  $s\cdot m>0$ for all active $m$. Verified exactly on a rational body (corner bulge $(9/10)^3$
  broken, illuminated by exactly $-(1,1,1)$). The load-bearing predicate is exact — no float.
- `corner_cover_is_finite_hitting_set` (E1b-FINITENESS) — **exact**, *conditional on coverability*:
  covering the broken set $B(K)$ by corner directions is a FINITE HITTING-SET over the 8 corner
  directions, so the corrective budget $=$ min hitting-set $\le 8$. Demonstrated exactly (two
  opposite corner bulges → 2 broken vertices → min hitting-set 2). This **finitizes** the E1b
  cover (a step toward Lean-fit: once coverability holds the cover is a finite rational object).
- `broken_set_budget_screen` (E1b-BUDGET SCREEN) — **directed search, CONJECTURE not proof**:
  12000 forced-family-proxy bodies (6 face-center contacts + arbitrary cube-interior vertices,
  incl. all-8-corners-bulged). Broken set ALWAYS corner-coverable; min hitting-set **never $>5$**
  ($\le7$). Strong support for the $6+7=13$ budget with slack.
- `corner_coverability_is_not_generic` (E1b-HONEST LIMIT) — **exact**: the abstract
  "pointed $+$ broken $\Rightarrow$ corner-coverable" is **FALSE** (explicit integer witness
  normals $\{(3,0,-3),(-1,1,0),(0,3,3),(-1,0,-1)\}$: pointed via $d=(-2,-4,3)$, broken, no corner
  covers). So forced-family coverability is a genuine cube-geometry fact — pins exactly where the
  open continuum content lives, and is why E1b is NOT hand-waveable.

## Open holes (the continuum wall)
- **E1a** `broken_set_bounded_by_min_vol_box` — `NotImplementedError`. Bound $|B(K)|$ from the
  min-vol-box tilt. Screened $|B(K)|\le5$ but UNPROVED. Continuum/affine.
- **E1b** `perturbed_directions_cover_broken_set` — `NotImplementedError`. Two sub-claims, both
  SCREENED (never refuted) but UNPROVED because the abstract version is provably false:
  (coverability) every forced-family broken vertex is corner-coverable — needs the cube structure;
  (budget$\le7$) the corner hitting-set has size $\le7$. The finite-hitting-set structure is
  CLOSED *conditional* on coverability.
- **E1** `near_one_half_illuminated_by_13` — assembly $I(K)\le 6+7=13$; rests on E1a + E1b.

## Claimed bound
**None unconditional yet.** The unconditional near-$1/2$ bound $H_3\le13$ is **not** established
— E1a, E1b open. Target hole-free: **no**. Table value to beat: $H_3\le14$.
