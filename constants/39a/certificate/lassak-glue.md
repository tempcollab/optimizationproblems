# Certificate record — sketch `lassak-glue` (Lean)

**Lake project:** `constants/39a/lean/` (bootstrapped round 1; shared by all Lean sketches).
**Toolchain (pinned):** `leanprover/lean4:v4.31.0` (`lean/lean-toolchain`).
**Mathlib (pinned):** rev `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f` (= tag `v4.31.0`),
recorded in `lean/lake-manifest.json`. Reproduce deps with `lake exe cache get`.

## Build target
```
cd constants/39a/lean
lake build Sketches.LassakGlue
```
Result: `Build completed successfully (2413 jobs).` (exit 0). Remaining diagnostics are
warnings only: four `declaration uses 'sorry'` (the explicit open holes — see below) plus benign
linter notes inherited from imports. `warningAsError = false` in `lakefile.toml` keeps a holed
sketch green per CLAUDE.md.

## `#print axioms` (run via an importing probe file)
```
H3.LassakGlue.H3_le_13           : [propext, sorryAx, Classical.choice, Quot.sound]
H3.LassakGlue.per_param_cover_13 : [propext, sorryAx, Classical.choice, Quot.sound]
H3.LassakGlue.generic_or_near    : [propext, sorryAx, Classical.choice, Quot.sound]
```
No CUSTOM axiom anywhere — only the standard Mathlib trio plus `sorryAx`. The `sorryAx` on
`H3_le_13` flows in through the four genuinely-open holes and the imported placeholder defs
(`Generic`, `CoverTarget`, `Piece`, `Body`), NOT through any smuggled hypothesis: `H3_le_13`'s own
proof term is `Nat.sInf_le every_body_cover_13` and the case-split glue `per_param_cover_13` /
`generic_or_near` carry no anonymous sorry. (`generic_or_near = em (Generic p)` inherits `sorryAx`
only because the imported `Generic` def is itself a placeholder `sorry`.)

## What this certifies (and what is still a hole)

CLOSED this round (no sorry of their own):
- `H3_le_13 : H3 ≤ 13` — the TOP-LEVEL TARGET, stated against the genuine registry `H3`
  (`sInf {N | ∀ K, IsConvexBody3 K → IsCoveredBy N K (interior K)}`), correct strict direction
  (13 < 14 = Prymak record), NO value smuggled. Closed by `Nat.sInf_le`: `every_body_cover_13` is
  literally the membership of `13` in the registry set.
- `every_body_cover_13` — reduces the arbitrary-body cover to the per-parameter cover through
  `prymak_param` (the only sorry on its path).
- `per_param_cover_13` — the GLUE: the total case split `generic_or_near` routes each `p` to the
  generic branch or the near branch; no anonymous sorry, both branches are named interface holes.
- `generic_or_near : Generic p ∨ Near p` — total partition (`Near := ¬ Generic`, `em`).
- `generic_cover_le_13'` — re-export of `GenericThirteenLP.generic_regime_thirteen` (records the
  imported LP content the generic transport rests on).

REMAINING HOLES (explicit `sorry`, honest — nothing downstream silently rests on them):
- `Body p` — opaque placeholder def for the normalized body family (instantiated with H_RED).
- `prymak_param` (H_RED) — Prymak Lemma 2.2 affine-normalization: every convex body is covering-
  equivalent to some `Body p`. Shared infra (= CertifyFourteen D1/D2/D5).
- `generic_branch_cover` (H_GENERIC transport) — transports the `E ∪ V_p`-by-`int(O_p)` LP cover
  (`generic_cover_le_13'`) to a `Body p`-by-`int(Body p)` cover. Its LP content is GenericThirteenLP.
- `near_cover_le_13` (H_NEAR) — direct Lassak-stability cover of `Body p` for near-1/2 `p`
  (octahedral-direct E1/E2; Lean-hostile, numerical certificate).

## Status
This sketch states the genuine target and closes the final-glue + case-split assembly. It does NOT
yet establish `H3 ≤ 13` (three load-bearing holes remain). It is a building member of the
population, NOT a verified bound. Table value to beat: `H3 ≤ 14` (Prymak 2023). Claimed (unverified)
target: `H3 ≤ 13`, hole-free: NO.
