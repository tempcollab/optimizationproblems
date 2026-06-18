# Approach: lean-scaffold-and-warmup

**Constant:** C_5b (Sidon density in (4,5)-sets, Erdős #757).
**Direction:** upper bound. Record to beat: `c* ≤ 4/7 ≈ 0.5714286` ([MT26], verified).
**This approach does NOT beat the record** — it builds the reusable, machine-checked Lean
certificate engine and proves it works by certifying the record value `4/7`.

## Idea

By [MT26] Theorem 1.5, `c* = inf_n f(n)/n`, so a single finite (4,5)-set `A` (weak Sidon)
with `h(A) ≤ m` and `|A| = N` rigorously gives `c* ≤ m/N`. Certification of such a gadget
is two finite decidable facts:
1. `A` is weak Sidon — all pairwise sums of distinct unordered pairs are distinct.
2. `h(A) ≤ m` — every `(m+1)`-subset of `A` contains a 3-term AP (by [MT26] Lemma 2.3,
   Sidon ⟺ no 3-AP inside a weak Sidon set).

Build these as `decide`-checkable Lean predicates once; then every future strict beat is a
one-line gadget swap + re-`decide`.

## What is proven this round (in `lean/Constants/C5b.lean`, no `sorry`)

For the record set `A_base` (14 points):
- `Abase_weakSidon : weakSidonB Abase = true` — `A_base` is a (4,5)-set. **No axioms.**
- `Abase_hLe8 : noSidonSubsetB Abase 9 = true` — `h(A_base) ≤ 8`. **No axioms.**
- `AbaseWitness8_no3AP`, `AbaseWitness8_card`, `AbaseWitness8_subset` — the size-8 subset
  `[0,136,200,243,246,298,323,528]` is Sidon, so `h(A_base) ≥ 8`. Hence `h(A_base) = 8`.
- `c5b_le_four_sevenths (c5b) (hThm15 : MTThm15 c5b) : c5b ≤ 4/7` — the bound, granting
  [MT26] Thm 1.5 as the explicit hypothesis `MTThm15`. Uses only the 3 standard Mathlib
  axioms (`propext`, `Classical.choice`, `Quot.sound`); no `sorryAx`, no `native_decide`.

`#print axioms` confirms the two load-bearing facts depend on NO axioms (pure kernel
`decide`). See `constants/5b/certificate/`.

## Claim

**Claimed (warm-up, matches record — NOT a beat): `c* ≤ 4/7`**, machine-checked in Lean
modulo the cited [MT26] Theorem 1.5 (the gadget→bound bridge, stated as hypothesis
`MTThm15`, not formalized). The finite load-bearing content (`A_base` is weak Sidon, no
Sidon 9-subset) is fully proved with no axioms.

## What is reusable (the engine)

All in namespace `C5b`, gadget-agnostic:
- `weakSidonB (l : List ℤ) : Bool` — the (4,5)/weak-Sidon check.
- `has3APB (s : List ℤ) : Bool` — "contains a 3-term AP".
- `combos (l : List ℤ) (k : ℕ) : List (List ℤ)` — all `k`-subsets (subsequences).
- `noSidonSubsetB (l : List ℤ) (k : ℕ) : Bool` — "no Sidon `k`-subset" ⟺ `h ≤ k-1`.
- `MTThm15 (c5b : ℝ) : Prop` — the cited bridge as an explicit hypothesis.

Encoding choice: `Bool`-over-`List ℤ` (structural recursion), NOT `Finset ℤ` +
`powersetCard` — the latter OOMs the kernel `decide` on the 2002 nine-subsets. The List
version `decide`s in ~40s with `set_option maxRecDepth 100000`.

## How to push to a strict beat next round

1. Find a finite (4,5)-set `A` (list of distinct ℤ) with `h(A)/|A| < 4/7` — e.g. N=21 with
   `h ≤ 11` (11/21 ≈ 0.5238), N=28 with `h ≤ 15` (0.5357), or any `m/N < 8/14`. (See the
   `guided-search-N21` approach.)
2. Drop it in as `Abase`, set `noSidonSubsetB A (m+1)` and re-`decide`. Add a theorem
   `c5b_le_<m>_<N>` mirroring `c5b_le_four_sevenths`.
3. **Scaling caveat:** `combos A k` has `C(N, k)` entries; at N=21, `C(21,12) ≈ 293k`
   — kernel `decide` may OOM/time out. If so, fall back to (a) `native_decide` (heavier
   trust — document; adds `Lean.ofReduceBool` axiom), or (b) an explicit transversal
   certificate: a small family of 3-APs proven to hit every `(m+1)`-subset, so the kernel
   checks a finite witness instead of enumerating all subsets. The transversal route keeps
   the no-axiom property and is the recommended path for large N.

## Status

DONE this round (warm-up): engine built, record `4/7` certified, `lake build` + clean
`#print axioms` confirmed. Reusable for every future beat.
