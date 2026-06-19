# Cached lemma — `C3a.log_bridge` (reviewer-certified, R7)

**Promoted by:** proof-reviewer, Round 7. **Bar:** full bound bar (Lean: `sorry`-free, axiom-clean, statement correct and no stronger than proved, `lake build` reproducible).

## Statement (Lean, exact)
```lean
theorem log_bridge (s d q A B : ℕ)
    (hs : 0 < s) (hq : 1 < q) (hB : 0 < B)
    (hint : s ^ B * q ^ A < d ^ B) :
    1 + (A : ℝ) / (B : ℝ) < 1 + Real.log ((d : ℝ) / (s : ℝ)) / Real.log (q : ℝ)
```
**Where proved:** `constants/3a/lean/Sketches/NativeDecideSmallMT.lean`, `namespace C3a` (lines ~125–155). Build target `lake build C3a` (EXIT 0). Mathlib pin: `leanprover/lean4:v4.31.0` (`lean/lake-manifest.json`).

## Reading
The cleared-denominator integer certificate `d^B > s^B·q^A` is exactly the cleared-denominator form of `log(d/s)/log q > A/B`. So for the GHR θ read-off `θ = 1 + log(d/s)/log q`, holding such an integer certificate proves `θ > 1 + A/B` for ANY rational target `1 + A/B` (with `0 < s`, `1 < q`, `0 < B`). The sketch instantiates `(A,B) = (7,40)` → `θ > 47/40 = 1.175`; the lemma is fully general in `(s,d,q,A,B)`.

## Certification (what the reviewer reproduced — R7)
- `lake build C3a` → EXIT 0, "Build completed successfully (2968 jobs)."
- `#print axioms C3a.log_bridge` → `[propext, Classical.choice, Quot.sound]` — Mathlib's standard axioms ONLY. NO `sorryAx`, NO `native_decide` axiom (the lemma is pure real arithmetic), NO custom `axiom`.
- Statement re-derived by hand and confirmed correct: `s^B·q^A < d^B` and `s^B>0` ⇒ `q^A < (d/s)^B`; `log` monotone (q^A>0) ⇒ `A·log q < B·log(d/s)`; `log q>0` (q>1), `B>0` ⇒ `A/B < log(d/s)/log q`; add 1. The conclusion is a strict `<` matching the strict hypothesis — **no stronger than proved**.

## Scope / caveat
A Lean theorem (the log-algebra half of the GHR θ-bridge), reusable by any C_3a / GHR sketch that holds a cleared-denominator integer certificate `d^B > s^B·q^A` and wants the real bound `θ > 1 + A/B`. It does NOT contain the GHR2007 read-off `θ ≤ C_3a` (that remains an assumed hypothesis `ghr` in the sketch's top theorem); this lemma only converts the integer inequality into the real θ-inequality.
