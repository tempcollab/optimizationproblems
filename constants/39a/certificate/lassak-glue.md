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
-- NEW R4 — the partition-validation lemmas, AXIOM-CLEAN (no sorryAx):
H3.LassakGlue.evenBox_mem_generic : [propext, Classical.choice, Quot.sound]
H3.LassakGlue.pStar_mem_near      : [propext, Classical.choice, Quot.sound]
H3.LassakGlue.coordSign_evenBox   : [propext, Classical.choice, Quot.sound]
H3.LassakGlue.coordSign_pStar     : [propext, Classical.choice, Quot.sound]
H3.LassakGlue.generic_or_near     : [propext, Classical.choice, Quot.sound]
```
No CUSTOM axiom anywhere. The R4 partition predicate (`coordSign`/`EvenParity`/`Near`) is now a
genuine sorry-free `def` (not the old opaque ball), so `generic_or_near` and the four new
validation lemmas are AXIOM-CLEAN — **no `sorryAx`**. The `sorryAx` on `H3_le_13` flows in only
through the five genuinely-open holes and the imported placeholder defs (`GenericThirteenLP.Generic`,
`CoverTarget`, `Piece`, and this file's `Body`), NOT through any smuggled hypothesis: `H3_le_13`'s
own proof term is `Nat.sInf_le every_body_cover_13` and the case-split glue `per_param_cover_13` /
`generic_or_near` carry no anonymous sorry.

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
- **NEW R4 — partition-validation lemmas (axiom-clean, no sorry of their own):**
  - `coordSign_evenBox` / `coordSign_pStar` — `coordSign` reads off the sign-vectors `(1,1,0,0,0,0)`
    / `(1,0,1,1,0,0)` of the sample even box / witness `p*` exactly (`fin_cases`+`norm_num`).
  - `evenBox_mem_generic : EvenParity evenBox` — the sample even-popcount box is in the generic
    region (popcount 2 even, `decide` on the unfolded sum).
  - `pStar_mem_near : Near pStar` — the proven `GenericThirteenLP` witness `p*` is ODD-popcount (3),
    so it lies in `Near`, NOT the clean even stratum. (In-Lean check that the witness geometry is as
    the certificate classified it.)
  These pin the partition predicate's combinatorial behaviour *in Lean*, so a wrong predicate cannot
  silently poison the glue. Backed by exact-rational certificate (`generic-thirteen-lp.py`,
  reproduced this round): all 32 even-popcount corner boxes 13-feasible (0 infeasible); all 24
  infeasible boxes odd-popcount (→ `Near`); 8 odd boxes feasible (bonus, incl. `p*`).

REMAINING HOLES (explicit `sorry`, honest — nothing downstream silently rests on them):
- `Body p` — opaque placeholder def for the normalized body family (instantiated with H_RED).
- `prymak_param` (H_RED) — Prymak Lemma 2.2 affine-normalization: every convex body is covering-
  equivalent to some `Body p`. Shared infra (= CertifyFourteen D1/D2/D5).
- `evenParity_generic` (H_PARITY_FIT) — `EvenParity p → GenericThirteenLP.Generic p`. NOT
  `id`-closable from this file: `GenericThirteenLP.Generic` is an opaque `sorry`-def, so it must
  first be instantiated by the sibling's atlas hole (`H_GEN_ATLAS`) over the even stratum. The
  *partition predicate's soundness* is already CLOSED (the validation lemmas above); what is open is
  the LP-region/atlas side owned by `GenericThirteenLP`.
- `generic_branch_cover` (H_GENERIC transport) — transports the `E ∪ V_p`-by-`int(O_p)` LP cover
  (`generic_cover_le_13'`) to a `Body p`-by-`int(Body p)` cover. Its LP content is GenericThirteenLP.
- `near_cover_le_13` (H_NEAR) — direct Lassak-stability cover of `Body p` for near-1/2 `p`
  (octahedral-direct E1/E2; Lean-hostile, numerical certificate).

## Status
This sketch states the genuine target and closes the final-glue + case-split assembly. It does NOT
yet establish `H3 ≤ 13` (three load-bearing holes remain). It is a building member of the
population, NOT a verified bound. Table value to beat: `H3 ≤ 14` (Prymak 2023). Claimed (unverified)
target: `H3 ≤ 13`, hole-free: NO.
