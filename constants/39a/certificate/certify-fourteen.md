# Certificate record — sketch D `certify-fourteen` (Lean)

**Lake project:** `constants/39a/lean/` (bootstrapped round 1; first Lean sketch of the run).
**Toolchain (pinned):** `leanprover/lean4:v4.31.0` (`lean/lean-toolchain`).
**Mathlib (pinned):** rev `fabf563a7c95a166b8d7b6efca11c8b4dc9d911f` (= tag `v4.31.0`), recorded in
`lean/lake-manifest.json`. Reproduce deps with `lake exe cache get` (cache hit for this rev).

## Build target
```
cd constants/39a/lean
lake build            # builds H3 (default) which imports Sketches.CertifyFourteen
```
Result: `Build completed successfully (2413 jobs).` (exit 0). The remaining diagnostics are
warnings only — the one `declaration uses 'sorry'` on `H3_le_14` (the intended open hole) plus
benign linter notes; `warningAsError = false` in `lakefile.toml` keeps a holed sketch green, per
CLAUDE.md (a `sorry` is a hole, not a build error).

## `#print axioms` (run via `lake env lean` on an importing file)
```
IsCoveredBy.mono_left        : [propext, Classical.choice, Quot.sound]
IsCoveredBy.union            : [propext, Classical.choice, Quot.sound]
coveringNumber_mono_left     : [propext, Classical.choice, Quot.sound]
icc_covered_by_two           : [propext, Classical.choice, Quot.sound]
H3_le_14                     : [propext, sorryAx, Classical.choice, Quot.sound]   <- HONEST open hole
```
The four infrastructure lemmas are **sorry-free and axiom-clean** (only the standard Mathlib
trio). `H3` is a genuine `def` (NOT an axiom) — no bound-smuggling. The lone `sorryAx` is on
`H3_le_14` itself, so nothing downstream silently depends on the unproved bound.

## What this certifies
NOT the bound (14 is already verified; D cannot beat it). It certifies, machine-checked:
the registry definition of `H3` and the reusable finite covering primitives (cover monotonicity,
cover-union assembly, and the 1-D interval-covering LP primitive) that record-break sketches A
and C reuse.
