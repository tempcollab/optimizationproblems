# Cached lemma — `C3a.setSum_card_decompose` / `setDiff_card_decompose` (reviewer-certified, R14)

**Promoted by:** proof-reviewer, Round 14. **Bar:** full bound bar (Lean: `sorry`-free, axiom-clean, statement correct and no stronger than proved, `lake build` reproducible).

**Source file:** `constants/3a/lean/Sketches/C3aDef.lean` (lines ~271–296, with supports ~186–264).

## What it is
The GHR composite-dilution disjoint-union additive count, at the Finset cardinality level:
for `mₙ = |shifts|` pairwise sum/diff-disjoint translates `aᵢ+B` plus a disjoint interval piece `I`,

    |(I ∪ ⋃ᵢ (aᵢ + B)) ± B| = mₙ · |B ± B| + |I ± B|.

Both disjointness conditions are EXPLICIT load-bearing hypotheses (`hpair` pairwise, `hint`
interval-vs-union) — neither is assumed away. This is the reusable heart of any GHR composite count
(the `Aₙ = [1,Lₙ] ∪ ⋃(aᵢ+Bₙ)` dilution).

## Statements (Lean, exact)
```lean
def setSum (A B : Finset ℤ) : Finset ℤ := Finset.image₂ (· + ·) A B
def setDiff (A B : Finset ℤ) : Finset ℤ := Finset.image₂ (· - ·) A B
def tr (c : ℤ) (A : Finset ℤ) : Finset ℤ := A.image (c + ·)
-- (sumset/diffset from TensorMultiplicativity: sumset S = setSum S S, diffset S = setDiff S S)

theorem setSum_card_decompose
    {ι : Type*} [DecidableEq ι] (shifts : Finset ι) (a : ι → ℤ) (I B : Finset ℤ)
    (hpair : ∀ i ∈ shifts, ∀ j ∈ shifts, i ≠ j →
        Disjoint (setSum (tr (a i) B) B) (setSum (tr (a j) B) B))
    (hint : Disjoint (setSum I B) (shifts.biUnion (fun i => setSum (tr (a i) B) B))) :
    (setSum (I ∪ shifts.biUnion (fun i => tr (a i) B)) B).card
      = shifts.card * (sumset B).card + (setSum I B).card

theorem setDiff_card_decompose
    {ι : Type*} [DecidableEq ι] (shifts : Finset ι) (a : ι → ℤ) (I B : Finset ℤ)
    (hpair : ∀ i ∈ shifts, ∀ j ∈ shifts, i ≠ j →
        Disjoint (setDiff (tr (a i) B) B) (setDiff (tr (a j) B) B))
    (hint : Disjoint (setDiff I B) (shifts.biUnion (fun i => setDiff (tr (a i) B) B))) :
    (setDiff (I ∪ shifts.biUnion (fun i => tr (a i) B)) B).card
      = shifts.card * (diffset B).card + (setDiff I B).card
```

## Supporting lemmas (also sorry-free, axiom-clean, available for reuse)
- `setSum_tr` / `setDiff_tr` — sum/diff of a one-coordinate translate = translate of the sum/diff (ring algebra).
- `setSum_tr_card` / `setDiff_tr_card` — a translate's sum/diff has the SAME cardinality (translation injective).
- `setSum_union` / `setDiff_union` — distributivity over `∪` in the first argument.
- `setSum_biUnion` / `setDiff_biUnion` — distributivity over `Finset.biUnion`.

## Certification (R14)
- `lake build C3a` EXIT 0 (2970 jobs), reproduced by the reviewer.
- `#print axioms` on all 10 lemmas above = `[propext, Classical.choice, Quot.sound]` — NO `sorryAx`.
- Proof mechanism re-derived: `setSum_union` → `setSum_biUnion` → `card_union_of_disjoint hint`
  → `card_biUnion hpair`, then each translate sumset card = `|sumset B|` via `setSum_tr_card`
  (with `setSum B B = sumset B` definitionally), `sum_const`, `smul_eq_mul`. Faithful, no hidden step.
- Statement correct and not stronger than proved: both disjointness hypotheses are required arguments.

**Build target:** `C3a` · **axioms:** `[propext, Classical.choice, Quot.sound]` (no sorryAx).
