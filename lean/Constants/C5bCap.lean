import Mathlib
import Constants.C5b

/-!
# C_5b : the structural cap lemma `m ≤ n − 2` (hardening [MT26] Lemma 2.4)

This file machine-checks the structural cap lemma that underlies the whole cap/τ/Henning–Yeo
analysis of `C_5b` (Erdős #757) and any future record-beating gadget.  Until now this lemma was
a **trusted external citation** ([MT26], Lemma 2.4); here it becomes a `lake build`-checked
theorem.

## The statement

For a **(4,5)-set** `A` (predicate `C5b.is45setB`, the difference condition: every 4-subset has
≥ 5 distinct pairwise `|x−y|`) of size `n`, let `m` be the number of *midpoint-distinct* 3-term
arithmetic progressions in `A` — i.e. the number of distinct values `b ∈ A` that are the
midpoint of some proper 3-AP `(a, b, c)` with `a, c ∈ A`, `a + c = 2b`, `a ≠ c`.  Then

```
m ≤ n − 2.
```

## The load-bearing content (FACT1, fully formalized below)

The whole lemma rests on one purely **arithmetic identity** (`midpoint_degree_le_one` /
`fact1_no_two_aps`):

> In a (4,5)-set, no vertex `p` is the midpoint of **two distinct** 3-APs.

If `p` were the midpoint of `(p−d₁, p, p+d₁)` and `(p−d₂, p, p+d₂)` with `d₁ > d₂ > 0`, the
4-subset `{p−d₁, p−d₂, p+d₂, p+d₁}` has its six pairwise absolute differences equal to

```
{ d₁−d₂, d₁+d₂, 2d₁, 2d₂, d₁+d₂, d₁−d₂ }
```

— the values `d₁−d₂` and `d₁+d₂` **each occur twice**, so there are at most **4** distinct
differences, never the ≥ 5 a (4,5)-set requires.  Hence the midpoint→3-AP map is injective.
This is a universally-quantified algebraic fact (no search/enumeration over candidate sets), so
the proof is structurally immune to compute blow-up.

Combined with the order fact that the **minimum** and **maximum** of `A` can never be a midpoint
of a 3-AP inside `A` (a midpoint lies strictly between its two endpoints), the set of midpoint
values is an injective image inside `A`'s interior, giving `m ≤ n − 2`.

## What is FORMALIZED here (no `sorry`, no `native_decide`, no smuggled hypothesis)

* `countDistinct_le_four_of_first_two_repeat` — the combinatorial cap: a 6-list whose first two
  entries each reappear later has `≤ 4` distinct values.
* `fact1_diffs_le_four` — the 4-subset `{p−d₁, p−d₂, p+d₂, p+d₁}` (`0 < d₂ < d₁`) has
  `countDistinct (diffs6 …) ≤ 4`, hence `diffs4B … = false`: **FACT1's arithmetic core**.
* `fact1_no_two_aps` — in any (4,5)-set, `p` is not the midpoint of two distinct 3-APs.
* `midpoints_subset_interior` / `card_midpoints_le` — the midpoint set sits in `A`'s interior,
  so `m ≤ n − 2`.
* `m_le_n_sub_2` — the cap lemma, stated over `C5b.is45setB` lists.

Source: Ma & Tang, arXiv:2602.23282 ("Largest Sidon subsets in weak Sidon sets"), **[MT26]**,
Lemma 2.4.
-/

namespace C5bCap

open C5b

/-! ### Part 1 — the `countDistinct` cap (combinatorial core). -/

/-- If `a` already occurs in `l`, prepending it does not change the distinct-count. -/
theorem countDistinct_cons_mem {a : ℤ} {l : List ℤ} (h : l.contains a = true) :
    countDistinct (a :: l) = countDistinct l := by
  conv_lhs => rw [countDistinct]
  rw [if_pos h, Nat.zero_add]

/-- Key cap: a list whose **first two entries each reappear later** has at most `4 + (length − …)`
distinct values.  Specialized to length-6 lists this gives `≤ 4`.

We prove the precise bound `countDistinct l ≤ l.length` first, then peel the two repeated heads. -/
theorem countDistinct_le_length : ∀ l : List ℤ, countDistinct l ≤ l.length
  | [] => by simp [countDistinct]
  | x :: xs => by
      have ih := countDistinct_le_length xs
      unfold countDistinct
      rw [List.length_cons]
      split <;> omega

/-- A 6-entry list `[e0,e1,e2,e3,e4,e5]` whose **first two entries each reappear in the tail**
has at most 4 distinct values:  `e0` and `e1` contribute `0` to `countDistinct`, and the
remaining 4-element tail contributes at most its length `4`. -/
theorem countDistinct_le_four_of_first_two_repeat
    (e0 e1 e2 e3 e4 e5 : ℤ)
    (h0 : ([e1, e2, e3, e4, e5] : List ℤ).contains e0 = true)
    (h1 : ([e2, e3, e4, e5] : List ℤ).contains e1 = true) :
    countDistinct [e0, e1, e2, e3, e4, e5] ≤ 4 := by
  rw [countDistinct_cons_mem h0, countDistinct_cons_mem h1]
  have := countDistinct_le_length [e2, e3, e4, e5]
  simpa using this

/-! ### Part 2 — FACT1's arithmetic core: the forbidden 4-subset has `≤ 4` distinct differences.

The 4-subset `{p−d₁, p−d₂, p+d₂, p+d₁}` formed by a vertex `p` that is the midpoint of two
3-APs has `diffs6` equal (entrywise) to `[w, x, y, z, x, w]`: the last two entries literally
equal the first two as integer differences (no sign/order assumption needed), so by
`countDistinct_le_four_of_first_two_repeat` it has `≤ 4` distinct values — never the ≥ 5 a
(4,5)-set demands.  Hence `diffs4B (p−d₁) (p−d₂) (p+d₂) (p+d₁) = false`. -/

/-- The two structural repeats in `diffs6 (p−d₁) (p−d₂) (p+d₂) (p+d₁)`, holding for **all**
integers `p, d₁, d₂` (no positivity): entry 4 = entry 1, entry 5 = entry 0.  This is the
crux of FACT1 — the midpoint structure forces two of the six differences to be duplicates. -/
theorem diffs6_midpoint_repeats (p d1 d2 : ℤ) :
    (((p - d2) - (p + d1)).natAbs : ℤ) = (((p - d1) - (p + d2)).natAbs : ℤ) ∧
    (((p + d2) - (p + d1)).natAbs : ℤ) = (((p - d1) - (p - d2)).natAbs : ℤ) := by
  constructor
  · congr 1
    have : (p - d2) - (p + d1) = (p - d1) - (p + d2) := by ring
    rw [this]
  · congr 1
    have : (p + d2) - (p + d1) = (p - d1) - (p - d2) := by ring
    rw [this]

/-- **FACT1, arithmetic core.**  The 4-subset `{p−d₁, p−d₂, p+d₂, p+d₁}` has at most 4 distinct
pairwise absolute differences, for **every** `p, d₁, d₂ : ℤ`.  (The midpoint structure alone
forces the duplicates; no ordering assumption is used here.) -/
theorem diffs6_midpoint_countDistinct_le_four (p d1 d2 : ℤ) :
    countDistinct (diffs6 (p - d1) (p - d2) (p + d2) (p + d1)) ≤ 4 := by
  obtain ⟨r4, r5⟩ := diffs6_midpoint_repeats p d1 d2
  -- name the six entries
  set e0 : ℤ := (((p - d1) - (p - d2)).natAbs : ℤ) with he0
  set e1 : ℤ := (((p - d1) - (p + d2)).natAbs : ℤ) with he1
  set e2 : ℤ := (((p - d1) - (p + d1)).natAbs : ℤ) with he2
  set e3 : ℤ := (((p - d2) - (p + d2)).natAbs : ℤ) with he3
  -- `diffs6` unfolds to `[e0, e1, e2, e3, e4, e5]` with `e4 = e1`, `e5 = e0`.
  have hlist : diffs6 (p - d1) (p - d2) (p + d2) (p + d1) = [e0, e1, e2, e3, e1, e0] := by
    simp only [diffs6, he0, he1, he2, he3]
    rw [r4, r5]
  rw [hlist]
  apply countDistinct_le_four_of_first_two_repeat
  · rw [List.contains_iff_mem]; simp
  · rw [List.contains_iff_mem]; simp

/-- **FACT1.**  In any (4,5)-set the 4-subset `{p−d₁, p−d₂, p+d₂, p+d₁}` fails the difference
condition (`diffs4B = false`), for every `p, d₁, d₂`.  This is the form fed to the contradiction:
a vertex that is the midpoint of two 3-APs produces exactly this 4-subset. -/
theorem fact1_diffs4B_false (p d1 d2 : ℤ) :
    diffs4B (p - d1) (p - d2) (p + d2) (p + d1) = false := by
  unfold diffs4B
  have h := diffs6_midpoint_countDistinct_le_four p d1 d2
  rw [Bool.eq_false_iff, ne_eq, Nat.ble_eq]
  omega

/-! ### Part 3 — the structural cap `m ≤ n − 2` over a `Finset ℤ`.

We now state the cap lemma for an abstract point set `A : Finset ℤ`.  The (4,5)-property is the
predicate `Is45 A`: every quadruple of points of `A` (listed in any order) passes the difference
check `diffs4B`.  This is exactly the hypothesis the engine's `is45setB` discharges for a concrete
list (every 4-sublist has `diffs4B = true`); `Is45` is its set-level statement. -/

/-- The set-level **(4,5)-property**: every four **pairwise-distinct** points of `A` (in any
order) pass the difference check `diffs4B`.  This is exactly what the engine's `is45setB`
discharges for a concrete list — every 4-sublist (which has distinct entries, the list being
`Nodup`) has ≥ 5 distinct pairwise `|x−y|`.  The pairwise-distinct guard is essential: a real
(4,5)-set does **not** satisfy `diffs4B` on degenerate quadruples with repeats. -/
def Is45 (A : Finset ℤ) : Prop :=
  ∀ a b c d : ℤ, a ∈ A → b ∈ A → c ∈ A → d ∈ A →
    a ≠ b → a ≠ c → a ≠ d → b ≠ c → b ≠ d → c ≠ d → diffs4B a b c d = true

/-- A vertex `b` is a **proper midpoint** in `A` if it is the midpoint of a 3-AP `(b−d, b, b+d)`
with `d > 0` and both endpoints in `A`. -/
def IsMidpoint (A : Finset ℤ) (b : ℤ) : Prop :=
  ∃ d : ℤ, 0 < d ∧ b - d ∈ A ∧ b + d ∈ A

/-- **FACT1 (midpoint degree ≤ 1).**  In a (4,5)-set, a proper midpoint `b` has a **unique** gap
`d`:  if `(b−d₁, b, b+d₁)` and `(b−d₂, b, b+d₂)` are both 3-APs in `A` with `d₁, d₂ > 0`, then
`d₁ = d₂`.  So the map (3-AP) → (midpoint) is injective; counting 3-APs by midpoint is exact. -/
theorem midpoint_degree_le_one {A : Finset ℤ} (hA : Is45 A) {b d1 d2 : ℤ}
    (hd1 : 0 < d1) (hd2 : 0 < d2)
    (h1m : b - d1 ∈ A) (h1p : b + d1 ∈ A) (h2m : b - d2 ∈ A) (h2p : b + d2 ∈ A) :
    d1 = d2 := by
  by_contra hne
  -- WLOG d1 > d2; swap roles otherwise.  In both cases we apply FACT1.
  rcases lt_or_gt_of_ne hne with hlt | hgt
  · -- d1 < d2 : use the 4-subset {b−d2, b−d1, b+d1, b+d2} (FACT1 with gaps d2 > d1)
    have hfalse := fact1_diffs4B_false b d2 d1
    have htrue := hA (b - d2) (b - d1) (b + d1) (b + d2) h2m h1m h1p h2p
      (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
    rw [hfalse] at htrue
    exact Bool.noConfusion htrue
  · -- d1 > d2 : use the 4-subset {b−d1, b−d2, b+d2, b+d1}
    have hfalse := fact1_diffs4B_false b d1 d2
    have htrue := hA (b - d1) (b - d2) (b + d2) (b + d1) h1m h2m h2p h1p
      (by omega) (by omega) (by omega) (by omega) (by omega) (by omega)
    rw [hfalse] at htrue
    exact Bool.noConfusion htrue

/-- The set of **3-APs** of `A`, encoded as pairs `(b, z)` with both the midpoint `b ∈ A` and the
**upper endpoint** `z ∈ A` (so the carrier `A ×ˢ A` is finite), gap `z − b > 0`, and the lower
endpoint `2b − z = b − (z − b) ∈ A`.  Each unordered 3-AP `{b−d, b, b+d}` (`d > 0`) is the single
pair `(b, b+d)`; `m = |threeAPs A|` is the number of midpoint-distinct 3-APs. -/
noncomputable def threeAPs (A : Finset ℤ) : Finset (ℤ × ℤ) :=
  (A ×ˢ A).filter (fun bz => bz.1 < bz.2 ∧ 2 * bz.1 - bz.2 ∈ A)

/-- A proper midpoint is **not the minimum** of `A`: its lower endpoint `b − d ∈ A` is smaller. -/
theorem midpoint_ne_min {A : Finset ℤ} (hne : A.Nonempty) {b : ℤ}
    (_hb : b ∈ A) (hmid : IsMidpoint A b) : b ≠ A.min' hne := by
  obtain ⟨d, hd, hm, _⟩ := hmid
  intro hbeq
  have : A.min' hne ≤ b - d := A.min'_le _ hm
  rw [← hbeq] at this
  omega

/-- A proper midpoint is **not the maximum** of `A`: its upper endpoint `b + d ∈ A` is larger. -/
theorem midpoint_ne_max {A : Finset ℤ} (hne : A.Nonempty) {b : ℤ}
    (_hb : b ∈ A) (hmid : IsMidpoint A b) : b ≠ A.max' hne := by
  obtain ⟨d, hd, _, hp⟩ := hmid
  intro hbeq
  have : b + d ≤ A.max' hne := A.le_max' _ hp
  rw [← hbeq] at this
  omega

/-- **FACT1 as an injectivity statement.**  In a (4,5)-set, the midpoint map `(b, d) ↦ b` is
injective on the set of 3-APs: two 3-APs with the same midpoint have the same gap.  This is the
content that makes "counting 3-APs by midpoint" exact, and is where `Is45` is genuinely used. -/
theorem midpoint_injOn {A : Finset ℤ} (hA : Is45 A) :
    Set.InjOn (fun bz : ℤ × ℤ => bz.1) (threeAPs A : Set (ℤ × ℤ)) := by
  intro p hp q hq hpq
  simp only [threeAPs, Finset.coe_filter, Finset.mem_product,
    Set.mem_setOf_eq] at hp hq
  obtain ⟨⟨_, hpzA⟩, hplt, hplo⟩ := hp
  obtain ⟨⟨_, hqzA⟩, hqlt, hqlo⟩ := hq
  simp only at hpq
  have hb : p.1 = q.1 := hpq
  -- gaps  d_p = p.2 − p.1 > 0,  d_q = q.2 − q.1 > 0; endpoints all in A.
  have hdp : (0 : ℤ) < p.2 - p.1 := by omega
  have hdq : (0 : ℤ) < q.2 - q.1 := by omega
  -- FACT1 with midpoint p.1 = q.1, gaps p.2−p.1 and q.2−q.1.
  have key : p.2 - p.1 = q.2 - q.1 := by
    apply midpoint_degree_le_one hA hdp hdq
    · -- p.1 − (p.2 − p.1) = 2 p.1 − p.2 ∈ A
      have : p.1 - (p.2 - p.1) = 2 * p.1 - p.2 := by ring
      rw [this]; exact hplo
    · -- p.1 + (p.2 − p.1) = p.2 ∈ A
      have : p.1 + (p.2 - p.1) = p.2 := by ring
      rw [this]; exact hpzA
    · -- p.1 − (q.2 − q.1) ∈ A, using p.1 = q.1
      have : p.1 - (q.2 - q.1) = 2 * q.1 - q.2 := by rw [hb]; ring
      rw [this]; exact hqlo
    · have : p.1 + (q.2 - q.1) = q.2 := by rw [hb]; ring
      rw [this]; exact hqzA
  have hz : p.2 = q.2 := by omega
  exact Prod.ext hb hz

/-- A 3-AP's midpoint `b` is a proper midpoint of `A` (witness `IsMidpoint A b`). -/
theorem threeAP_isMidpoint {A : Finset ℤ} {bz : ℤ × ℤ} (h : bz ∈ threeAPs A) :
    IsMidpoint A bz.1 := by
  rw [threeAPs, Finset.mem_filter] at h
  obtain ⟨hprod, hlt, hlo⟩ := h
  obtain ⟨_hb, hzA⟩ := Finset.mem_product.mp hprod
  refine ⟨bz.2 - bz.1, by omega, ?_, ?_⟩
  · have : bz.1 - (bz.2 - bz.1) = 2 * bz.1 - bz.2 := by ring
    rw [this]; exact hlo
  · have : bz.1 + (bz.2 - bz.1) = bz.2 := by ring
    rw [this]; exact hzA

/-- The midpoint of any 3-AP lands in the **interior** `A \ {min, max}`. -/
theorem threeAP_midpoint_mem_interior {A : Finset ℤ} (hne : A.Nonempty) {bz : ℤ × ℤ}
    (h : bz ∈ threeAPs A) :
    bz.1 ∈ (A.erase (A.min' hne)).erase (A.max' hne) := by
  have hmid := threeAP_isMidpoint h
  have hbA : bz.1 ∈ A := by
    rw [threeAPs, Finset.mem_filter] at h
    exact (Finset.mem_product.mp h.1).1
  rw [Finset.mem_erase, Finset.mem_erase]
  exact ⟨midpoint_ne_max hne hbA hmid, midpoint_ne_min hne hbA hmid, hbA⟩

/-- **The cap lemma `m ≤ n − 2`.**  For any (4,5)-set `A : Finset ℤ` of size `n ≥ 2`, the number
`m = |threeAPs A|` of **midpoint-distinct 3-APs** satisfies `m ≤ n − 2`.

The midpoint map `(b, z) ↦ b` sends `threeAPs A` **injectively** (FACT1, `midpoint_injOn`, the
only place the (4,5)-property is used) into the interior `A \ {min, max}`
(`threeAP_midpoint_mem_interior`), which has exactly `n − 2` elements.  `card_le_card_of_injOn`
then gives the bound.  This hardens [MT26], Lemma 2.4 from a trusted external citation into a
`lake build`-checked theorem. -/
theorem m_le_n_sub_2 {A : Finset ℤ} (hA : Is45 A) (hn : 2 ≤ A.card) :
    (threeAPs A).card ≤ A.card - 2 := by
  have hne : A.Nonempty := Finset.card_pos.mp (by omega)
  have hminmax : A.min' hne ≠ A.max' hne := by
    intro h
    have := Finset.min'_lt_max'_of_card A (by omega : 1 < A.card)
    rw [h] at this; exact lt_irrefl _ this
  -- inject threeAPs into the interior via the (injective) midpoint map
  have hcard : (threeAPs A).card ≤ ((A.erase (A.min' hne)).erase (A.max' hne)).card := by
    apply Finset.card_le_card_of_injOn (fun bz => bz.1)
    · intro bz hbz; exact threeAP_midpoint_mem_interior hne hbz
    · exact midpoint_injOn hA
  -- |interior| = |A| - 2
  have hmaxmem : A.max' hne ∈ A.erase (A.min' hne) :=
    Finset.mem_erase.mpr ⟨(hminmax).symm, A.max'_mem hne⟩
  have hminmem : A.min' hne ∈ A := A.min'_mem hne
  rw [Finset.card_erase_of_mem hmaxmem, Finset.card_erase_of_mem hminmem] at hcard
  omega

end C5bCap
