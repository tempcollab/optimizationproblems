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

## What is CLOSED this round (exact / directed-rounded)
- `enlargement_is_dead_screen` — exact: $O_p-O_p$ = unit cube, tight pairs on the boundary
  (justifies the direct route; carried over from R3 plan).
- `lassak_symmetric_illumination` (E0) — **exact rational**: the 6 directions $D=-V$
  illuminate the regular octahedron via Boltyanski's active-facet criterion (checking vertices
  suffices because the active set only shrinks off a vertex). Exact illumination margin **= 1**
  (unnormalized normals) $= 1/\sqrt3$ with unit normals. So $I(\text{octahedron})\le 6\le 13$.
- `illumination_stability_criterion` / `orthant_coherent` (E2-core, **Lemma S'**) — exact
  criterion + directed-rounded threshold sweep: if at every vertex of $K$ the active facet outer
  normals share a coordinate-sign, then $D=-V$ illuminates $K$ with verified margin, so
  $I(K)\le 6\le 13$. Sufficiency independently corroborated (1932 coherent bodies, 0 illumination
  failures over a full-boundary direct test). Explicit threshold located at perturbation
  $t\approx 0.30$.
- `counterexample_face_center_not_symmetric` — exact: an asymmetric body touching all 6 cube
  face centers ($p=1/2$ contacts) that **breaks** orthant-coherence — the honesty record for why
  E1 is genuinely open.

## Open hole (load-bearing)
- **E1** `family_meets_orthant_coherence` — `NotImplementedError`. That the Prymak-forced family
  at $p\approx1/2$ satisfies orthant-coherence. The naive "$p=1/2\Rightarrow$ near-symmetric"
  reading is **false** (counterexample above); E1 needs the full min-volume-box geometry to bound
  the normal-fan deviation. Continuum / Lean-hostile. NOT established.

## Claimed bound
**None unconditional yet.** Verified sub-results: $I(\text{octahedron})\le 6$ and the
orthant-coherence $\Rightarrow \le 6$ lemma. The unconditional near-$1/2$ bound $H_3\le 13$ is
**not** established — E1 is open. Target hole-free: **no**.
