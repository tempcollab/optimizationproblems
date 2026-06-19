# Cached lemma — `C3a.setSum_tr_pair_disjoint` / `setDiff_tr_pair_disjoint` (reviewer-certified, R15)

**Promoted by:** proof-reviewer, Round 15. **Bar:** full bound bar (Lean: `sorry`-free, axiom-clean, statement correct and no stronger than proved, `lake build` reproducible).

**Source file:** `constants/3a/lean/Sketches/C3aDef.lean` (lines ~365–394, with supports `tr`/`setSum`/`setDiff`/`setSum_tr`/`setDiff_tr` at ~102/187/191/202).

## What it is
The general translate-spacing disjointness lemma underlying the GHR composite-dilution separation:
if every element of the sumset/diffset `B ± B` lies in a window `[lo, lo + diam]`, and the shift gap
`|c − c'|` strictly exceeds `diam`, then the two translated sum/diff sets are disjoint:

    WithinDiam (B ± B) lo diam ∧ diam < |c − c'|  ⟹  Disjoint ((c + B) ± B) ((c' + B) ± B).

This is the reusable, cached-lemma-shaped half of B1a (`griego_ak_disjoint`): pairwise disjointness of
the `mₙ` AP-shifted translates follows by applying it with the diameters and shift-spacing of the
composite. The diameter window and the strict gap are both EXPLICIT load-bearing hypotheses — nothing
is assumed away, and the conclusion is exactly pairwise disjointness (not a stronger structural claim).

## Statements (Lean, exact)
```lean
def WithinDiam (S : Finset ℤ) (lo diam : ℤ) : Prop := ∀ z ∈ S, lo ≤ z ∧ z ≤ lo + diam

theorem setSum_tr_pair_disjoint (c c' : ℤ) (B : Finset ℤ) (lo diam : ℤ)
    (hwd : WithinDiam (setSum B B) lo diam) (hgap : diam < |c - c'|) :
    Disjoint (setSum (tr c B) B) (setSum (tr c' B) B)

theorem setDiff_tr_pair_disjoint (c c' : ℤ) (B : Finset ℤ) (lo diam : ℤ)
    (hwd : WithinDiam (setDiff B B) lo diam) (hgap : diam < |c - c'|) :
    Disjoint (setDiff (tr c B) B) (setDiff (tr c' B) B)
```

## Proof (sorry-free)
`setSum_tr`/`setDiff_tr` rewrite each translate image to `image (c + ·) (B ± B)`; `Finset.disjoint_left`
extracts a common element `c + w = c' + w'` with `w, w' ∈ [lo, lo + diam]` from the two `WithinDiam`
hypotheses; `abs_le` + `omega` (using the membership equality and the window bounds) gives
`|c − c'| ≤ diam`, which `linarith` contradicts against `diam < |c − c'|`. Pure ℤ interval arithmetic.

## Certification (R15 reviewer, reproduced independently)
- `lake build C3a` → EXIT 0 (2970 jobs); lines 365/380 carry NO `sorry` warning (proof-term sorry-free).
- `#print axioms` (independent throwaway `Sketches/AxCheck.lean`, since deleted):
  - `C3a.setSum_tr_pair_disjoint` → `[propext, Classical.choice, Quot.sound]` — NO `sorryAx`.
  - `C3a.setDiff_tr_pair_disjoint` → `[propext, Classical.choice, Quot.sound]` — NO `sorryAx`.
- Statement re-derived by hand: requires a genuine diameter window AND a strict shift gap to conclude
  disjointness; correct and not over-strong. No smuggled `axiom`/`admit`/`native_decide` in the file.
