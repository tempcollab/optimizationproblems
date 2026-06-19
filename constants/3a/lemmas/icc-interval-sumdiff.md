# Cached lemmas — integer-interval sumset/diffset identities

Certified by the proof-reviewer in Round 21 (sketch `lean-c3a-def`). Both are
sorry-free and axiom-clean (`#print axioms = [propext, Classical.choice, Quot.sound]`,
NO `sorryAx`), independently re-derived and `decide`-checked on concrete `n`
(`setSum (Icc 0 4)(Icc 0 4) = Icc 0 8`, `setDiff (Icc 0 4)(Icc 0 4) = Icc (-4) 4`).
General over the interval bound `n`; the `0 ≤ n` hypothesis is load-bearing.

Location: `lean/Sketches/C3aDef.lean` (with `setSum A B := image₂ (·+·) A B`,
`setDiff A B := image₂ (·-·) A B`).

## `icc_setSum_eq`
```lean
theorem icc_setSum_eq (n : ℤ) (hn : 0 ≤ n) :
    setSum (Finset.Icc (0:ℤ) n) (Finset.Icc (0:ℤ) n) = Finset.Icc 0 (2 * n)
```
The sumset of `[0,n]` with itself is exactly `[0,2n]`. The `⊇` half writes any
`z ∈ [0,2n]` as `min z n + (z − min z n)`, both summands in `[0,n]`.

Immediate corollary (also in the file): `icc_setSum_card`,
`(setSum (Icc 0 n)(Icc 0 n)).card = (2n+1).toNat` via `Int.card_Icc`.

## `icc_setDiff_eq`
```lean
theorem icc_setDiff_eq (n : ℤ) (hn : 0 ≤ n) :
    setDiff (Finset.Icc (0:ℤ) n) (Finset.Icc (0:ℤ) n) = Finset.Icc (-n) n
```
The diffset of `[0,n]` with itself is exactly the symmetric interval `[-n,n]`. The
`⊇` half writes any `z ∈ [-n,n]` as `max z 0 − max (-z) 0`, both in `[0,n]`.

Immediate corollary: `icc_setDiff_card`,
`(setDiff (Icc 0 n)(Icc 0 n)).card = (2n+1).toNat`.

Reusable for any growing-interval realizability witness (independent of all witness
data). Used in R21 to close `realizes_one : Realizes 1` via `A n = B n = Icc 0 n`.
