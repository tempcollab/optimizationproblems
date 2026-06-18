# lean-cap-lemma-m-le-n-minus-2

**Class:** Lean-fit verified machinery (not a bound-mover this round).
**Status (R8):** BUILT — `lake build`-passing, axiom-clean. Claim awaiting reviewer verification.

## Idea

The whole C_5b cap/τ/Henning–Yeo analysis (and any future record-beating N=30 gadget certificate)
rests on **[MT26], Lemma 2.4**: for a (4,5)-set `A` of size `n`, the number `m` of
midpoint-distinct 3-term APs satisfies `m ≤ n − 2`. Until now this was a *trusted external
citation* in our Lean engine. This approach formalizes it into a `lake build`-checked theorem,
removing that trust.

The load-bearing content is one purely **arithmetic identity** (FACT1, midpoint degree ≤ 1):
if a vertex `p` were the midpoint of two distinct 3-APs `(p−d₁,p,p+d₁)` and `(p−d₂,p,p+d₂)`, the
4-subset `{p−d₁, p−d₂, p+d₂, p+d₁}` has its six pairwise `|·|`-differences equal to
`{d₁−d₂, d₁+d₂, 2d₁, 2d₂, d₁+d₂, d₁−d₂}` — `d₁−d₂` and `d₁+d₂` each appear **twice**, so there are
≤ 4 distinct differences, never the ≥ 5 a (4,5)-set demands. Hence the midpoint→3-AP map is
injective; combined with "min/max of `A` are never midpoints", the 3-APs inject into `A`'s
interior (`n − 2` points), giving `m ≤ n − 2`.

## What was built (R8)

New file `lean/Constants/C5bCap.lean` (namespace `C5bCap`), imports `Constants.C5b` and reuses the
engine's `diffs6` / `diffs4B` / `countDistinct` (4,5)-machinery. Theorems, all **no `sorry`, no
`native_decide`, clean axioms** (`propext`/`Classical.choice`/`Quot.sound`):

- `countDistinct_le_four_of_first_two_repeat` — combinatorial cap: a 6-list whose first two
  entries each reappear later has ≤ 4 distinct values. (The two repeated heads contribute 0; the
  4-element tail contributes ≤ its length.)
- `diffs6_midpoint_repeats` — the structural crux: in `diffs6 (p−d₁)(p−d₂)(p+d₂)(p+d₁)`, entry 4 =
  entry 1 and entry 5 = entry 0 **as integer differences, for all `p,d₁,d₂`** (the duplicates hold
  with NO positivity/order assumption — `(p−d₂)−(p+d₁) = (p−d₁)−(p+d₂)` and
  `(p+d₂)−(p+d₁) = (p−d₁)−(p−d₂)` by `ring`).
- `diffs6_midpoint_countDistinct_le_four`, `fact1_diffs4B_false` — FACT1's arithmetic core:
  `countDistinct ≤ 4`, hence `diffs4B … = false`, for every `p,d₁,d₂`.
- `midpoint_degree_le_one` — FACT1: in any (4,5)-set, two 3-APs with the same midpoint have the
  same gap. WLOG handled by `lt_or_gt_of_ne` (both orderings reduce to `fact1_diffs4B_false`); the
  four points' pairwise-distinctness is supplied by `omega`.
- `midpoint_injOn` — the midpoint map `(b,z) ↦ b` is injective on `threeAPs A` (the ONLY place the
  (4,5)-property `Is45` is genuinely used).
- `m_le_n_sub_2 (hA : Is45 A) (hn : 2 ≤ A.card) : (threeAPs A).card ≤ A.card − 2` — **the cap
  lemma**, via `Finset.card_le_card_of_injOn` into `(A.erase min').erase max'`.

Encoding choices (per repo Rules): `threeAPs A := (A ×ˢ A).filter (fun (b,z) => b < z ∧ 2b−z ∈ A)`
keeps the carrier finite (gap `z−b > 0`, lower endpoint `2b−z ∈ A`). `Is45 A` quantifies over
**pairwise-distinct** quadruples (the distinctness guard is essential — a real (4,5)-set does not
satisfy `diffs4B` on degenerate quads); this matches exactly what the decidable `is45setB`
discharges for a concrete `Nodup` list.

## Certificate

`constants/5b/certificate/cap/README.md` — build target `lake build Constants.C5bCap`, the
`#print axioms` lines, and reproduction steps.

## How to push further

1. **Bridge `is45setB` (list) → `Is45` (Finset).** Add a Lean lemma
   `is45setB l = true → Is45 l.toFinset` (every 4-sublist passing `diffs4B` ⇒ every distinct
   Finset quadruple passes it). This connects the cap lemma to the concrete decidable engine used
   on actual gadgets, fully closing the Lemma-2.4 trust path inside `C5b.lean`.
2. **Use the cap as an `h` lower-bound input.** With `m ≤ n−2` machine-checked, the
   Henning–Yeo τ-bound `17τ ≤ 5n + 3m` becomes a Lean-certifiable consequence once the HY
   inequality itself is formalized — that is the next structural lemma toward an N=30 beat
   certificate (target 17/30 ≈ 0.5667 < 4/7).
3. **Tight m = n−2 ⟺ bijection onto interior.** A converse/characterization lemma (FACT2's "=" case)
   would let a found gadget's `m` be read off structurally; useful to certify the stage-a search's
   m-frontier in Lean rather than numerically.

## Why it does not move the bound

It is verified machinery: it hardens a trusted lemma but the record 4/7 is unchanged. The bound
moves only when an indecomposable N≈30 (4,5)-set with the right τ-density is found and certified
(the stage-a / milp lines). This cap lemma is a prerequisite that any such certificate leans on.
