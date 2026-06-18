# C_5b cap lemma certificate — `m ≤ n − 2` (hardening [MT26] Lemma 2.4)

Machine-checked Lean theorem that, for any **(4,5)-set** `A` of size `n`, the number `m` of
**midpoint-distinct 3-term arithmetic progressions** in `A` satisfies `m ≤ n − 2`.  This replaces
the previously-trusted external citation ([MT26], Lemma 2.4) — on which the whole cap/τ/Henning–Yeo
analysis and any future record-beating N=30 gadget cert rests — with a `lake build`-checked theorem.

## Lean source

`lean/Constants/C5bCap.lean` (namespace `C5bCap`), imports `Constants.C5b` (reuses `diffs6`,
`diffs4B`, `countDistinct`, the engine's (4,5) difference machinery).

## Build target

```
cd lean
export PATH="$HOME/.elan/bin:$PATH"
lake build Constants.C5bCap        # ~40s incremental; the whole project: lake build
```

`Build completed successfully` ⇒ the theorems below type-check. (Mathlib pinned at `v4.31.0`.)

## Theorems (all no `sorry`, no `native_decide`)

- `diffs6_midpoint_countDistinct_le_four (p d1 d2)` — **FACT1 arithmetic core**: the 4-subset
  `{p−d₁, p−d₂, p+d₂, p+d₁}` has `countDistinct (diffs6 …) ≤ 4` for **all** `p, d₁, d₂ : ℤ`
  (universally quantified, no enumeration).  The crux is `diffs6_midpoint_repeats`: entries 4 and
  5 of `diffs6` literally equal entries 1 and 0 as integer differences, so two of the six pairwise
  `|·|`-differences are duplicates and at most 4 distinct values remain.
- `fact1_diffs4B_false (p d1 d2)` — hence `diffs4B (p−d₁) (p−d₂) (p+d₂) (p+d₁) = false`: this
  4-subset never satisfies the (4,5) difference condition (≥ 5 distinct `|x−y|`).
- `midpoint_degree_le_one` — **FACT1**: in any (4,5)-set `A` (`Is45 A`), a vertex `b` that is the
  midpoint of two proper 3-APs with gaps `d₁, d₂ > 0` has `d₁ = d₂` (midpoint degree ≤ 1).
- `midpoint_injOn` — the midpoint map `(b, z) ↦ b` is injective on `threeAPs A` (the **only** place
  `Is45` is used; this is what makes "count 3-APs by midpoint" exact).
- `m_le_n_sub_2 (hA : Is45 A) (hn : 2 ≤ A.card)` — **the cap lemma**:
  `(threeAPs A).card ≤ A.card − 2`.

Here `threeAPs A` encodes each 3-AP `{b−d, b, b+d}` (`d>0`) as the pair `(b, b+d)` with midpoint
`b ∈ A` and upper endpoint `b+d ∈ A`; `Is45 A` is the set-level (4,5)-property (every quadruple of
**pairwise-distinct** points of `A` passes `diffs4B`), exactly what the engine's decidable
`is45setB` discharges for a concrete `Nodup` list.

## Axiom check (reproduce)

```
cd lean
export PATH="$HOME/.elan/bin:$PATH"
printf 'import Constants.C5bCap\n#print axioms C5bCap.m_le_n_sub_2\n#print axioms C5bCap.fact1_diffs4B_false\n#print axioms C5bCap.midpoint_degree_le_one\n#print axioms C5bCap.midpoint_injOn\n' > AxProbeCap.lean
lake env lean AxProbeCap.lean ; rm AxProbeCap.lean
```

Recorded output:

```
'C5bCap.m_le_n_sub_2' depends on axioms: [propext, Classical.choice, Quot.sound]
'C5bCap.fact1_diffs4B_false' depends on axioms: [propext, Quot.sound]
'C5bCap.midpoint_degree_le_one' depends on axioms: [propext, Quot.sound]
'C5bCap.midpoint_injOn' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The standard clean set only — **no `sorryAx`, no `Lean.ofReduceBool` (`native_decide`), no added
axiom**.  The hard step (FACT1) is genuinely inside the formalization.

## What this is / is NOT

- It IS a machine-checked hardening of the structural lemma the cap analysis trusts.
- It does NOT move the bound (4/7 stands); it is verified machinery, recorded as such.
- The (4,5)→bound bridge (Thm 1.5) remains the cited trust boundary in `C5b.lean`'s `MTThm15`;
  this file hardens the *cap* lemma (2.4), a different and previously-untouched trusted input.

Source: Ma & Tang, arXiv:2602.23282 ("Largest Sidon subsets in weak Sidon sets"), **[MT26]**,
Lemma 2.4.
