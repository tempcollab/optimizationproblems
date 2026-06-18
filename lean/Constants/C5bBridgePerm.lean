import Mathlib
import Constants.C5b
import Constants.C5bCap

/-!
# C_5b : the decidable bridge — permutation-invariance half

This file builds the **permutation-invariance** half of the decidable bridge that wires the
R8 structural cap lemma (`C5bCap.m_le_n_sub_2`, stated over the abstract `Is45 : Finset ℤ → Prop`)
into the concrete engine predicate `C5b.is45setB` (`lean/Constants/C5b.lean`).

The cap lemma takes the hypothesis `Is45 A`, which quantifies over **every ordering** of four
pairwise-distinct points of `A`:

```
Is45 A := ∀ a b c d, a ∈ A → … → (pairwise ≠) → diffs4B a b c d = true.
```

The engine, by contrast, checks `diffs4Bof` on each member of `combos l 4` — i.e. it tests
`diffs4B` on **one** index-order per 4-subset.  To lift the single-order check to the
all-orders quantification of `Is45`, the bridge needs two facts:

1. **`combos`-completeness** — every 4-subset of `l.toFinset` appears (in some order) as a
   member of `combos l 4`.  *(Proved separately, in `C5bCombos.lean`; here it is taken as an
   explicit named hypothesis `combos_complete`, in the trust-boundary style of `MTThm15`.)*
2. **`diffs4B` permutation-invariance** — `diffs4B` is invariant under reordering its four
   arguments, so the one combos-order witness lifts to the arbitrary order `Is45` quantifies
   over.  **This file proves (2) in full.**

## What is FORMALIZED here (no `sorry`, no `native_decide`, no axiom)

* `countDistinct_eq_dedup_length` / `countDistinct_perm` — `countDistinct` is invariant under
  list permutation (`l ~ l' → countDistinct l = countDistinct l'`), via `l.dedup.length`.
* `diffs6_perm_swap_ab/_bc/_cd` — under each adjacent transposition of the four arguments,
  `diffs6` is a `List.Perm` of the original 6-list (using `|x−y| = |y−x|`).  These three
  transpositions generate `S₄`.
* `diffs4B_swap_ab/_bc/_cd` and the full `diffs4B_perm` family — `diffs4B` is invariant under
  every reordering of its four arguments.
* `is45setB_to_Is45` — the assembled bridge `is45setB l = true → Is45 l.toFinset`, taking the
  `combos`-completeness fact as the single explicit named hypothesis `hcomplete`.

Source of the structural facts: Ma & Tang, arXiv:2602.23282 (**[MT26]**), Lemma 2.4 path.
-/

namespace C5bBridgePerm

open C5b C5bCap

/-! ### Part 1 — `countDistinct` is permutation-invariant. -/

/-- `countDistinct l` counts the distinct entries of `l`, which is exactly the length of the
deduplicated list `l.dedup`.  Proved by structural induction, matching `countDistinct`'s
`if xs.contains x …` branch against `List.dedup`'s `if x ∈ xs …` branch. -/
theorem countDistinct_eq_dedup_length : ∀ l : List ℤ, countDistinct l = l.dedup.length
  | [] => by simp [countDistinct]
  | x :: xs => by
      rw [countDistinct]
      by_cases hx : x ∈ xs
      · rw [List.dedup_cons_of_mem hx, if_pos (List.contains_iff_mem.mpr hx),
          Nat.zero_add, countDistinct_eq_dedup_length xs]
      · rw [List.dedup_cons_of_notMem hx, List.length_cons,
          if_neg (by simpa [List.contains_iff_mem] using hx),
          countDistinct_eq_dedup_length xs, Nat.add_comm]

/-- **`countDistinct` is invariant under list permutation.**  A permutation of `l` has the same
distinct values, so the same distinct-count.  Via `countDistinct l = l.dedup.length`,
`List.Perm.dedup`, and `List.Perm.length_eq`. -/
theorem countDistinct_perm {l l' : List ℤ} (h : l.Perm l') :
    countDistinct l = countDistinct l' := by
  rw [countDistinct_eq_dedup_length, countDistinct_eq_dedup_length]
  exact (h.dedup).length_eq

/-! ### Part 2 — `diffs6` is permutation-invariant under the `S₄` generators.

`diffs6 a b c d = [|a−b|, |a−c|, |a−d|, |b−c|, |b−d|, |c−d|]`.  The key tool is the symmetry
`|x−y| = |y−x|` (`diffSym`).  Under each adjacent transposition of `(a,b,c,d)` the six unordered
differences are the same multiset, so `diffs6` of the swapped tuple is a `List.Perm` of the
original. -/

/-- `|x − y| = |y − x|` cast back to `ℤ` (the entry shape used in `diffs6`). -/
theorem diffSym (x y : ℤ) : (((x - y).natAbs : ℤ)) = (((y - x).natAbs : ℤ)) := by
  rw [← Int.natAbs_neg, neg_sub]

/-- Swap the first two arguments.  `diffs6 b a c d ~ diffs6 a b c d`. -/
theorem diffs6_perm_swap_ab (a b c d : ℤ) :
    (diffs6 b a c d).Perm (diffs6 a b c d) := by
  unfold diffs6
  rw [diffSym b a]
  -- now: [|a−b|, |b−c|, |b−d|, |a−c|, |a−d|, |c−d|] ~ [|a−b|, |a−c|, |a−d|, |b−c|, |b−d|, |c−d|]
  refine List.Perm.cons _ ?_
  -- [|b−c|, |b−d|, |a−c|, |a−d|, |c−d|] ~ [|a−c|, |a−d|, |b−c|, |b−d|, |c−d|]
  -- this is the block move of [|b−c|, |b−d|] past [|a−c|, |a−d|]; append-comm-style.
  have h :
      ([((b - c).natAbs : ℤ), ((b - d).natAbs : ℤ), ((a - c).natAbs : ℤ),
        ((a - d).natAbs : ℤ), ((c - d).natAbs : ℤ)]).Perm
      ([((a - c).natAbs : ℤ), ((a - d).natAbs : ℤ), ((b - c).natAbs : ℤ),
        ((b - d).natAbs : ℤ), ((c - d).natAbs : ℤ)]) := by
    have :
        ([((b - c).natAbs : ℤ), ((b - d).natAbs : ℤ)] ++
          [((a - c).natAbs : ℤ), ((a - d).natAbs : ℤ), ((c - d).natAbs : ℤ)]).Perm
        ([((a - c).natAbs : ℤ), ((a - d).natAbs : ℤ), ((c - d).natAbs : ℤ)] ++
          [((b - c).natAbs : ℤ), ((b - d).natAbs : ℤ)]) := List.perm_append_comm
    -- reorder the right block back to the target via a second append-comm on its tail
    refine this.trans ?_
    -- [|a−c|,|a−d|,|c−d|,|b−c|,|b−d|] ~ [|a−c|,|a−d|,|b−c|,|b−d|,|c−d|]
    refine (List.Perm.cons _ (List.Perm.cons _ ?_))
    -- [|c−d|,|b−c|,|b−d|] ~ [|b−c|,|b−d|,|c−d|]
    exact (List.perm_append_comm (l₁ := [((c - d).natAbs : ℤ)])
      (l₂ := [((b - c).natAbs : ℤ), ((b - d).natAbs : ℤ)]))
  exact h

/-- Swap the middle two arguments.  `diffs6 a c b d ~ diffs6 a b c d`. -/
theorem diffs6_perm_swap_bc (a b c d : ℤ) :
    (diffs6 a c b d).Perm (diffs6 a b c d) := by
  unfold diffs6
  -- diffs6 a c b d = [|a−c|, |a−b|, |a−d|, |c−b|, |c−d|, |b−d|]
  -- target        = [|a−b|, |a−c|, |a−d|, |b−c|, |b−d|, |c−d|]
  rw [diffSym c b]
  -- now first list: [|a−c|, |a−b|, |a−d|, |b−c|, |c−d|, |b−d|]
  -- swap heads |a−c|, |a−b|
  refine (List.Perm.swap' _ _ ?_)
  -- [|a−d|, |b−c|, |c−d|, |b−d|] ~ [|a−d|, |b−c|, |b−d|, |c−d|]
  refine (List.Perm.cons _ (List.Perm.cons _ ?_))
  -- [|c−d|, |b−d|] ~ [|b−d|, |c−d|]
  exact List.Perm.swap _ _ _

/-- Swap the last two arguments.  `diffs6 a b d c ~ diffs6 a b c d`. -/
theorem diffs6_perm_swap_cd (a b c d : ℤ) :
    (diffs6 a b d c).Perm (diffs6 a b c d) := by
  unfold diffs6
  -- diffs6 a b d c = [|a−b|, |a−d|, |a−c|, |b−d|, |b−c|, |d−c|]
  -- target         = [|a−b|, |a−c|, |a−d|, |b−c|, |b−d|, |c−d|]
  rw [diffSym d c]
  -- now: [|a−b|, |a−d|, |a−c|, |b−d|, |b−c|, |c−d|]
  refine (List.Perm.cons _ ?_)
  -- [|a−d|, |a−c|, |b−d|, |b−c|, |c−d|] ~ [|a−c|, |a−d|, |b−c|, |b−d|, |c−d|]
  refine (List.Perm.swap' _ _ ?_)
  -- [|b−d|, |b−c|, |c−d|] ~ [|b−c|, |b−d|, |c−d|]
  exact (List.Perm.swap' _ _ (List.Perm.refl _))

/-! ### Part 3 — `diffs4B` is invariant under each generator swap, then under any reordering. -/

/-- `diffs4B` is invariant under swapping the first two arguments. -/
theorem diffs4B_swap_ab (a b c d : ℤ) : diffs4B b a c d = diffs4B a b c d := by
  unfold diffs4B
  rw [countDistinct_perm (diffs6_perm_swap_ab a b c d)]

/-- `diffs4B` is invariant under swapping the middle two arguments. -/
theorem diffs4B_swap_bc (a b c d : ℤ) : diffs4B a c b d = diffs4B a b c d := by
  unfold diffs4B
  rw [countDistinct_perm (diffs6_perm_swap_bc a b c d)]

/-- `diffs4B` is invariant under swapping the last two arguments. -/
theorem diffs4B_swap_cd (a b c d : ℤ) : diffs4B a b d c = diffs4B a b c d := by
  unfold diffs4B
  rw [countDistinct_perm (diffs6_perm_swap_cd a b c d)]

/-! ### Part 4 — full 4-argument permutation invariance via a compositional pairwise-diff list.

To lift the three generator swaps to **arbitrary** reorderings (the all-orders quantifier of
`Is45`) without enumerating the 24 orderings, we route through a *compositional* helper
`pdiffs : List ℤ → List ℤ` that builds the multiset of pairwise `|x−y|` by structural recursion
(`pdiffs (x :: xs) = xs.map (|x − ·|) ++ pdiffs xs`).  Compositionality makes it directly
amenable to `List.Perm` induction:

* `pdiffs_perm` — `l ~ l' → (pdiffs l).Perm (pdiffs l')`, by `Perm` induction (the `swap` case is
  exactly the `|x−y| = |y−x|` symmetry packaged through `List.perm_append_comm`).
* `pdiffs_four` — `pdiffs [a,b,c,d]` is a `List.Perm` of `diffs6 a b c d` (both list the same 6
  pairwise differences; the entry order differs, handled by `diffSym`).

Composing these with `countDistinct_perm` gives `diffs4B` invariance under any reordering of its
four arguments. -/

/-- Compositional list of pairwise absolute differences `|x − y|` of a list, by structural
recursion: each head contributes its difference to every later element. -/
def pdiffs : List ℤ → List ℤ
  | [] => []
  | x :: xs => xs.map (fun y => ((x - y).natAbs : ℤ)) ++ pdiffs xs

/-- A single head's contribution `xs.map |x − ·|` is `Perm`-stable when the tail permutes. -/
theorem map_diff_perm (x : ℤ) {l l' : List ℤ} (h : l.Perm l') :
    (l.map (fun y => ((x - y).natAbs : ℤ))).Perm (l'.map (fun y => ((x - y).natAbs : ℤ))) :=
  h.map _

/-- **`pdiffs` is permutation-invariant.**  Proved by `List.Perm` induction; the `swap` case
`x :: y :: l` is where the symmetry `|x−y| = |y−x|` (`diffSym`) feeds the head reorder. -/
theorem pdiffs_perm : ∀ {l l' : List ℤ}, l.Perm l' → (pdiffs l).Perm (pdiffs l') := by
  intro l l' h
  induction h with
  | nil => exact List.Perm.refl _
  | cons x h ih =>
      simp only [pdiffs]
      exact (map_diff_perm x h).append ih
  | swap x y l =>
      -- pdiffs (y :: x :: l)  ~  pdiffs (x :: y :: l)
      simp only [pdiffs, List.map_cons]
      -- after diffSym the two "cross" entries both become |x−y|
      rw [diffSym y x]
      -- abbreviations for the two map-blocks and the common tail
      set A := l.map (fun z => ((x - z).natAbs : ℤ)) with hA
      set B := l.map (fun z => ((y - z).natAbs : ℤ)) with hB
      set t := pdiffs l with ht
      set c := ((x - y).natAbs : ℤ) with hc
      -- Goal:  (c :: B) ++ (A ++ t)  ~  (c :: A) ++ (B ++ t)
      -- i.e.   c :: (B ++ (A ++ t))  ~  c :: (A ++ (B ++ t)).
      refine List.Perm.cons _ ?_
      -- B ++ (A ++ t)  ~  A ++ (B ++ t)
      simp only [List.append_eq, ← List.append_assoc]
      -- (B ++ A) ++ t  ~  (A ++ B) ++ t
      exact (List.perm_append_comm).append_right t
  | trans h₁ h₂ ih₁ ih₂ => exact ih₁.trans ih₂

/-- `pdiffs [a,b,c,d]` is a `List.Perm` of `diffs6 a b c d`:  both enumerate the six pairwise
`|x−y|` of `{a,b,c,d}`.  `pdiffs` lists them in head-order
`[|a−b|,|a−c|,|a−d|,|b−c|,|b−d|,|c−d|]`, which is *exactly* `diffs6`. -/
theorem pdiffs_four (a b c d : ℤ) :
    (pdiffs [a, b, c, d]).Perm (diffs6 a b c d) := by
  simp only [pdiffs, diffs6, List.map_cons, List.map_nil, List.nil_append,
    List.cons_append]
  -- both sides are literally the same 6-element list
  exact List.Perm.refl _

/-- **`diffs4B` permutation invariance (all 24 orderings).**  If `[a,b,c,d] ~ [a',b',c',d']`
then `diffs4B a b c d = diffs4B a' b' c' d'`.  This lifts the single-order engine check to the
all-orders quantifier of `C5bCap.Is45`. -/
theorem diffs4B_perm4 {a b c d a' b' c' d' : ℤ}
    (h : ([a, b, c, d] : List ℤ).Perm [a', b', c', d']) :
    diffs4B a b c d = diffs4B a' b' c' d' := by
  unfold diffs4B
  have hp : (diffs6 a b c d).Perm (diffs6 a' b' c' d') :=
    (pdiffs_four a b c d).symm.trans ((pdiffs_perm h).trans (pdiffs_four a' b' c' d'))
  rw [countDistinct_perm hp]

/-! ### Part 5 — the assembled bridge `is45setB l → Is45 l.toFinset`.

`is45setB l = true` means every member of `combos l 4` passes `diffs4Bof`.  Given four
**pairwise-distinct** points `a,b,c,d ∈ l.toFinset`, the `combos`-completeness fact
(`hcomplete`, taken here as an explicit named hypothesis — proved separately in `C5bCombos.lean`)
provides a member `[w,x,y,z] ∈ combos l 4` that is a permutation of `[a,b,c,d]`.  `is45setB`
gives `diffs4B w x y z = true`; `diffs4B_perm4` lifts it to `diffs4B a b c d = true`. -/

/-- The `combos`-completeness obligation, **as a `Prop`** (the single named trust boundary of this
half, in the `MTThm15` style).  It states: for a `Nodup` list `l` and four pairwise-distinct
points of `l.toFinset`, some member of `combos l 4` is a permutation of `[a,b,c,d]`.  *Proved
separately in `C5bCombos.lean`; left here as a hypothesis so the two halves compose next round.* -/
def CombosComplete (l : List ℤ) : Prop :=
  ∀ a b c d : ℤ, a ∈ l.toFinset → b ∈ l.toFinset → c ∈ l.toFinset → d ∈ l.toFinset →
    a ≠ b → a ≠ c → a ≠ d → b ≠ c → b ≠ d → c ≠ d →
    ∃ p ∈ combos l 4, p.Perm [a, b, c, d]

/-- **The bridge (permutation-invariance half).**  Granting the `combos`-completeness fact
(`hcomplete : CombosComplete l`), the engine check `is45setB l = true` implies the set-level
(4,5)-property `Is45 l.toFinset` that the cap lemma `C5bCap.m_le_n_sub_2` consumes.

The proof: completeness yields a `combos` member `p ~ [a,b,c,d]`; `is45setB` makes `diffs4Bof p`
true; `p` has length 4 (it permutes a 4-list) so `diffs4Bof p = diffs4B p₀ p₁ p₂ p₃`;
`diffs4B_perm4` transports that to `diffs4B a b c d`.  No `sorry`, no axiom — the single trusted
input is the visible hypothesis `hcomplete`. -/
theorem is45setB_to_Is45 {l : List ℤ}
    (hcomplete : CombosComplete l) (h45 : is45setB l = true) :
    Is45 l.toFinset := by
  intro a b c d ha hb hc hd hab hac had hbc hbd hcd
  obtain ⟨p, hpmem, hperm⟩ := hcomplete a b c d ha hb hc hd hab hac had hbc hbd hcd
  -- `is45setB l = true` ⇒ every combos member passes `diffs4Bof`.
  have hall : ∀ q ∈ combos l 4, diffs4Bof q = true := by
    have := h45
    unfold is45setB at this
    rwa [List.all_eq_true] at this
  have hpof : diffs4Bof p = true := hall p hpmem
  -- `p` permutes `[a,b,c,d]`, so it has length 4: write `p = [w,x,y,z]`.
  have hlen : p.length = 4 := by
    have := hperm.length_eq; simpa using this
  match p, hlen, hperm, hpof with
  | [w, x, y, z], _, hperm, hpof =>
      -- `diffs4Bof [w,x,y,z] = diffs4B w x y z`
      simp only [diffs4Bof] at hpof
      -- transport along the permutation `[w,x,y,z] ~ [a,b,c,d]`
      rw [diffs4B_perm4 hperm] at hpof
      exact hpof

end C5bBridgePerm
