import Mathlib
import Constants.C5b

/-!
# C_5b : completeness of the custom `combos` enumerator (the bridge's hard half)

This file proves the **`combos`-completeness** lemma that is the load-bearing half of the
decidable bridge `is45setB l = true → C5bCap.Is45 l.toFinset` (the wiring of the R8 cap
lemma `C5bCap.m_le_n_sub_2` into the concrete engine).  The OTHER half — `diffs4B`
permutation-invariance + the final assembly *modulo* this lemma — is built in
`Constants/C5bBridgePerm.lean`; this file authors only `combos_complete`.

## What `combos` is, and why no Mathlib lemma applies directly

`C5b.combos` (`lean/Constants/C5b.lean:122`) is the repo's CUSTOM `k`-sublist enumerator:

```
combos _        0       = [[]]
combos []       (k+1)   = []
combos (x::xs)  (k+1)   = (combos xs k).map (x :: ·) ++ combos xs (k+1)
```

This is the include-`x` / exclude-`x` recurrence.  It enumerates exactly the **length-`k`
subsequences** (`List.Sublist`) of `l`, but it is a hand-rolled `def`, so no Mathlib
`sublistsLen`/`Sublist` membership lemma fires on it — completeness is proved from the
recurrence by induction.

## The completeness statement (the form the bridge needs)

`C5bCap.Is45 A` quantifies over every four **pairwise-distinct** points `a,b,c,d ∈ A` in
ANY order.  `is45setB l` checks `diffs4Bof` on every member of `combos l 4` — i.e. on every
4-subsequence, in its single `l`-induced index order.  To close the bridge we must show that
the four arbitrary distinct points `a,b,c,d` of `l.toFinset` arise as SOME member of
`combos l 4` (in some order), so that the engine's per-`combos`-member check covers them.

The cleanest bridge-ready form is via `List.Perm`:

> `combos_complete` : if `l.Nodup` and `a,b,c,d ∈ l` are pairwise distinct, then there is a
> `t ∈ combos l 4` with `t ~ [a,b,c,d]` (a permutation).

The perm half then reads off `diffs4Bof t = diffs4B w x y z = true` (`t` has length 4) and
lifts it along `t ~ [a,b,c,d]` to `diffs4B a b c d = true` by `diffs4B`-perm-invariance.

We prove it from the **general** fact `mem_combos_of_sublist` (every length-`k` subsequence of
`l` is a `combos l k` member), then realize the four distinct points as a length-4 subsequence
of `l` (in `l`-order), which is a permutation of `[a,b,c,d]`.

## What is FORMALIZED here (no `sorry`, no `native_decide`, no smuggled hypothesis)

* `length_of_mem_combos` — every member of `combos l k` has length `k`.
* `mem_combos_of_sublist` — every length-`k` subsequence (`<+`) of `l` is in `combos l k`
  (the include/exclude induction on the recurrence).
* `combos_complete` — the bridge-ready completeness lemma above.

Source of the construction: the repo engine `C5b.combos` (R1/R3).  No external citation.
-/

namespace C5bCombos

open C5b
open List

/-! ### Length of every enumerated combo. -/

/-- Every member of `combos l k` is a list of length exactly `k`. -/
theorem length_of_mem_combos :
    ∀ (l : List ℤ) (k : ℕ) (t : List ℤ), t ∈ combos l k → t.length = k
  | _, 0, t, ht => by
      simp only [combos, List.mem_singleton] at ht
      subst ht; rfl
  | [], k + 1, t, ht => by
      simp only [combos, List.not_mem_nil] at ht
  | x :: xs, k + 1, t, ht => by
      rw [combos, List.mem_append] at ht
      rcases ht with ht | ht
      · -- include branch: t = x :: t' with t' ∈ combos xs k
        rw [List.mem_map] at ht
        obtain ⟨t', ht', rfl⟩ := ht
        have := length_of_mem_combos xs k t' ht'
        simp [this]
      · -- exclude branch: t ∈ combos xs (k+1)
        exact length_of_mem_combos xs (k + 1) t ht

/-! ### Completeness: every length-`k` subsequence is enumerated. -/

/-- **Core completeness.**  Every subsequence `t <+ l` of length `k` occurs as a member of
`combos l k`.  Proved by induction on the `List.Sublist` derivation, matching `combos`'s
include/exclude recurrence:

* `.slnil` (`[] <+ []`): only `k = 0`, and `combos [] 0 = [[]]`.
* `.cons x h` (`t <+ x :: xs` with `t <+ xs`, `x` dropped): `t` lands in the exclude branch
  `combos xs k` (length `k`), hence in the `++` right side.
* `.cons₂ x h` (`a :: t' <+ x :: xs` with `t' <+ xs`): the head is `x`, `t'` has length
  `k - 1`, so `t' ∈ combos xs (k-1)` and `x :: t'` is in the `map (x :: ·)` left side. -/
theorem mem_combos_of_sublist :
    ∀ {t l : List ℤ}, t <+ l → t ∈ combos l t.length := by
  intro t l h
  induction h with
  | slnil => simp [combos]
  | @cons l₁ l₂ x hsub ih =>
      -- t = l₁ <+ l₂, dropping x.  goal: l₁ ∈ combos (x :: l₂) l₁.length
      rcases hl : l₁ with _ | ⟨a, l₁'⟩
      · -- l₁ = [] : combos _ 0 = [[]]
        simp [combos]
      · -- l₁ = a :: l₁' has length (k+1); land in the exclude (right) branch
        rw [List.length_cons, combos, List.mem_append]
        right
        -- ih : l₁ ∈ combos l₂ l₁.length = combos l₂ (l₁'.length + 1)
        rw [hl, List.length_cons] at ih
        exact ih
  | @cons_cons l₁ l₂ x hsub ih =>
      -- t = x :: l₁ <+ x :: l₂ with l₁ <+ l₂; land in the include (map) branch
      rw [List.length_cons, combos, List.mem_append]
      left
      rw [List.mem_map]
      exact ⟨l₁, ih, rfl⟩

/-! ### Realizing four distinct points as a subsequence in `l`-order. -/

/-- Helper: from four pairwise-distinct members of a `Nodup` list `l`, the `l`-ordered
sublist `l.filter (· ∈ ([a,b,c,d] : List ℤ))` is a subsequence of `l` that, as a multiset,
equals `{a,b,c,d}`.  We package the perm directly. -/
theorem four_distinct_perm_sublist {l : List ℤ} (hl : l.Nodup)
    {a b c d : ℤ}
    (ha : a ∈ l) (hb : b ∈ l) (hc : c ∈ l) (hd : d ∈ l)
    (hab : a ≠ b) (hac : a ≠ c) (had : a ≠ d)
    (hbc : b ≠ c) (hbd : b ≠ d) (hcd : c ≠ d) :
    ∃ t : List ℤ, t <+ l ∧ t ~ [a, b, c, d] := by
  classical
  -- The filtered sublist keeps exactly the entries equal to one of a,b,c,d.
  set S : List ℤ := [a, b, c, d] with hS
  refine ⟨l.filter (fun y => decide (y ∈ S)), List.filter_sublist, ?_⟩
  -- It is a permutation of S = [a,b,c,d].  Both are Nodup with the same element set.
  have hNodupF : (l.filter (fun y => decide (y ∈ S))).Nodup := hl.filter _
  have hNodupS : S.Nodup := by
    rw [hS]
    simp only [List.nodup_cons, List.mem_cons, List.not_mem_nil, or_false,
      List.nodup_nil, and_true, not_or, not_false_eq_true]
    exact ⟨⟨hab, hac, had⟩, ⟨hbc, hbd⟩, hcd⟩
  -- same membership
  apply (List.perm_ext_iff_of_nodup hNodupF hNodupS).mpr
  intro y
  rw [List.mem_filter]
  constructor
  · rintro ⟨_, hy⟩; exact of_decide_eq_true hy
  · intro hy
    refine ⟨?_, by simp [hy]⟩
    -- y ∈ S = {a,b,c,d} ⊆ l
    simp only [hS, List.mem_cons, List.not_mem_nil, or_false] at hy
    rcases hy with rfl | rfl | rfl | rfl
    · exact ha
    · exact hb
    · exact hc
    · exact hd

/-! ### The bridge-ready completeness lemma. -/

/-- **`combos_complete` (bridge-ready).**  For a `Nodup` list `l` and four pairwise-distinct
members `a,b,c,d ∈ l`, there is a list `t ∈ combos l 4` with `t ~ [a,b,c,d]`.

This is the half the bridge needs: it places the four arbitrary distinct points (which `Is45`
quantifies over in any order) as SOME member of `combos l 4`, up to a permutation that the
perm-invariance half discharges. -/
theorem combos_complete {l : List ℤ} (hl : l.Nodup)
    {a b c d : ℤ}
    (ha : a ∈ l) (hb : b ∈ l) (hc : c ∈ l) (hd : d ∈ l)
    (hab : a ≠ b) (hac : a ≠ c) (had : a ≠ d)
    (hbc : b ≠ c) (hbd : b ≠ d) (hcd : c ≠ d) :
    ∃ t : List ℤ, t ∈ combos l 4 ∧ t ~ [a, b, c, d] := by
  obtain ⟨t, hsub, hperm⟩ :=
    four_distinct_perm_sublist hl ha hb hc hd hab hac had hbc hbd hcd
  have hlen : t.length = 4 := by
    have := hperm.length_eq
    simpa using this
  refine ⟨t, ?_, hperm⟩
  have hmem := mem_combos_of_sublist hsub
  rwa [hlen] at hmem

end C5bCombos
