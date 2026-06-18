# C_5b certificate — Lean machine-checked (round 1, warm-up)

**Slug:** `lean-scaffold-and-warmup`
**Status:** warm-up — reproduces the record `c* ≤ 4/7`, does NOT beat it.
**Type:** Lean-fit. The check is `lake build` + `#print axioms` (type-checking IS the
reproduction).

## What is certified

Two finite, decidable combinatorial facts about the record 14-point set
`A_base = [0,136,200,243,246,249,272,286,298,323,400,528,596,1056]`, formalized in
`lean/Constants/C5b.lean` (namespace `C5b`):

- `Abase_weakSidon : weakSidonB Abase = true`
  — `A_base` is a weak Sidon set / (4,5)-set (all pairwise sums of distinct unordered
  pairs are distinct).
- `Abase_hLe8 : noSidonSubsetB Abase 9 = true`
  — every 9-element subset of `A_base` contains a 3-term AP, i.e. (by [MT26] Lemma 2.3,
  Sidon ⟺ no 3-AP inside a weak Sidon set) `h(A_base) ≤ 8`.
- `AbaseWitness8_no3AP : has3APB AbaseWitness8 = false` together with
  `AbaseWitness8_card` / `AbaseWitness8_subset` — the size-8 subset
  `[0,136,200,243,246,298,323,528]` is Sidon, so `h(A_base) ≥ 8`. Hence `h(A_base) = 8`.

`c5b_le_four_sevenths (c5b : ℝ) (hThm15 : MTThm15 c5b) : c5b ≤ 4/7` draws the bound from
those facts, granting [MT26] Theorem 1.5 (`c* = inf_n f(n)/n`) as the explicit hypothesis
`MTThm15`. Theorem 1.5 is CITED, not formalized; it is the single trusted-not-proved link
(see file header). The decidable facts — the part a finite certificate carries — are fully
proved by kernel `decide`, no `sorry`.

## How the reviewer re-establishes it

```
cd /home/agentuser/repo/lean
source $HOME/.elan/env
lake build                       # whole project, includes Constants.C5b  (gold-standard check)
# or just the module:
lake build Constants.C5b
```
Then check axioms (must show no `sorryAx`, no `Lean.ofReduceBool`/`native_decide`):
```
cat > AxCheck.lean <<'EOF'
import Constants.C5b
open C5b
#print axioms Abase_weakSidon
#print axioms Abase_hLe8
#print axioms AbaseWitness8_no3AP
#print axioms c5b_le_four_sevenths
EOF
lake env lean AxCheck.lean
rm AxCheck.lean
```

## Expected output (verified this round)

`lake build` → `Build completed successfully`.
`#print axioms`:
```
'C5b.Abase_weakSidon' does not depend on any axioms
'C5b.Abase_hLe8' does not depend on any axioms
'C5b.AbaseWitness8_no3AP' does not depend on any axioms
'C5b.c5b_le_four_sevenths' depends on axioms: [propext, Classical.choice, Quot.sound]
```
The two load-bearing facts depend on NO axioms (pure kernel reduction — no
`native_decide`, no `sorry`). `c5b_le_four_sevenths` uses only the three standard Mathlib
foundational axioms (from `norm_num`/`linarith`/ℝ) — no `sorryAx`, no `Lean.ofReduceBool`.

## Build/perf notes

- `decide` (kernel, NOT `native_decide`) is used throughout. To keep it tractable the
  predicates are `Bool`-valued computations over explicit `List ℤ` (structural recursion),
  not `Finset ℤ` + `powersetCard` (the latter OOMs the kernel on the 2002 nine-subsets).
- `set_option maxRecDepth 100000` is set for the `h ≤ 8` evaluation (deep but finite
  recursion); this is a kernel evaluation-depth knob only, it adds no axiom and weakens
  nothing.
- Module build time ≈ 40s.

## Source

Ma & Tang, "Largest Sidon subsets in weak Sidon sets", arXiv:2602.23282 (Feb 2026).
Digest: `constants/5b/literature/MT26-ma-tang-digest.md`.
