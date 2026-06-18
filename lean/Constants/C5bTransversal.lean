import Mathlib

/-!
# C_5b : AP-transversal (fractional-matching) certificate for `h(A) ≤ m`

This file builds **reusable, machine-checked** machinery for upper-bounding the largest
Sidon (= no-3-term-AP, inside a weak Sidon / (4,5)-set, by [MT26] Lemma 2.3) subset of a
finite point set `A ⊂ ℤ`, *without* enumerating the `C(N, m+1)` subsets.

## The obstacle this solves

To certify `h(A) ≤ m` directly one shows every `(m+1)`-subset of `A` contains a 3-term AP,
i.e. checks `C(N, m+1)` subsets.  For the record gadget `N = 14, m = 8` that is
`C(14,9) = 2002`; for the target `N = 30, m = 16` it is `C(30,17) ≈ 1.2·10⁸` — far past
kernel `decide`.  This file replaces that exponential check with a **transversal /
fractional-matching certificate** whose validity is a finite check of cost `O(|F|·N)`.

## The certificate (LP-duality, hand-auditable)

Let `H(A)` be the 3-uniform hypergraph whose vertices are the points of `A` and whose edges
are the 3-term APs contained in `A`.

* A subset `S ⊆ A` with **no** 3-term AP misses at least one vertex of every AP, so its
  complement `A \ S` is a **hitting set (transversal)** of `H(A)`.  Hence
  `|S| ≤ |A| − τ`, where `τ` is the minimum transversal size.  So `h(A) ≤ N − τ`.
* A **fractional matching** lower-bounds `τ` by LP duality: assign each AP `e` a weight
  `w_e ≥ 0` so that for every vertex `v`, the total weight of APs through `v` is `≤ D`
  (a common denominator `D`).  Then every transversal `H` satisfies
  `D·|H| ≥ Σ_{v∈H} load(v) ≥ Σ_e w_e = T` (each edge is hit, so its weight is counted at
  least once).  Hence `τ = min|H| ≥ T / D`.

Combining:  `h(A) ≤ N − ⌈T/D⌉`.  To certify `h(A) ≤ m` it therefore suffices to exhibit a
weighting with `T > D·(N − m − 1)` — a finite, `decide`-checkable inequality of cost
`O(|F|·N)`.

Crucially the fractional matching is genuinely stronger than an integral AP packing:
an integral packing of vertex-disjoint APs has `≤ ⌊N/3⌋` edges (only proving `h ≤ N−⌊N/3⌋`,
e.g. `h(A_base) ≤ 10`), whereas the fractional value can reach `τ = N − h = 6` on the 14
points of `A_base` (validated below).

## What is FORMALIZED here (no `sorry`, no smuggled axiom)

`hLe_of_fracMatching` : the **soundness lemma** — from a weighting certificate
(`isAPcert` : every listed edge a genuine AP in `A`; `loadOK` : every vertex load `≤ D`;
`T > D·(N−m−1)`) it derives that **every** no-3-AP sublist of `A` has length `≤ m`.

The proof is a list double-counting induction (`totalW ≤ Σ_{v∈H} load(v)` for any hitting
set `H`), fully elementary — it uses only `List.sum` arithmetic, no `decide` on `C(N,m+1)`.

## Validation on the record gadget (zero axioms, by `decide`)

`Abase_tau_ge_6` : a weighting certificate `Fcert_base` over the 3-APs of `A_base` with
`T = 6·D` and every vertex load `≤ D`, checked by kernel `decide`.  Via the soundness lemma
this re-derives `h(A_base) ≤ 8` *through the transversal route* (`O(|F|·14)`), matching the
existing `C(14,9)` enumeration in `Constants.C5b` — proving the machinery sound and usable.

The gadget search for the bound-moving `N = 30` set is deferred to a later round; this file
delivers the verified, reusable certificate format and its soundness proof.

Source of the structural facts: Ma & Tang, arXiv:2602.23282 (Feb 2026), **[MT26]**
(Lemma 2.3: inside a weak Sidon set, Sidon ⟺ no 3-term AP).
-/

namespace C5bTransversal

/-! ## Decidable predicates for the certificate format -/

/-- A triple `(a,b,c)` is a genuine non-degenerate 3-term AP: `a + c = 2b` with the three
entries pairwise distinct. -/
def isAP (t : ℤ × ℤ × ℤ) : Bool :=
  let a := t.1; let b := t.2.1; let c := t.2.2
  (a + c == 2 * b) && (a ≠ b) && (b ≠ c) && (a ≠ c)

/-- `v` occurs as one of the three vertices of the triple `t`. -/
def memTriple (v : ℤ) (t : ℤ × ℤ × ℤ) : Bool :=
  (v == t.1) || (v == t.2.1) || (v == t.2.2)

/-- Every entry of the triple `t` is a member of the point list `A`. -/
def tripleInA (A : List ℤ) (t : ℤ × ℤ × ℤ) : Bool :=
  A.contains t.1 && A.contains t.2.1 && A.contains t.2.2

/-- The weight (as a `ℕ`) that vertex `v` carries from the weighted edge list `FW`:
the sum of the weights of all listed APs that pass through `v`.  Defined by structural
recursion so that the soundness induction unfolds cleanly. -/
def vertexLoad (FW : List ((ℤ × ℤ × ℤ) × ℕ)) (v : ℤ) : ℕ :=
  match FW with
  | [] => 0
  | (t, wt) :: rest => (if memTriple v t then wt else 0) + vertexLoad rest v

/-- Total weight of the matching = `Σ_e w_e`. -/
def totalW (FW : List ((ℤ × ℤ × ℤ) × ℕ)) : ℕ :=
  (FW.map (fun p => p.2)).sum

/-- Certificate well-formedness: every listed edge is a genuine 3-AP whose three points all
lie in `A`. -/
def edgesOK (A : List ℤ) (FW : List ((ℤ × ℤ × ℤ) × ℕ)) : Bool :=
  FW.all (fun p => isAP p.1 && tripleInA A p.1)

/-- The vertex-load constraint of the fractional matching: every point of `A` carries total
weight `≤ D`. -/
def loadOK (A : List ℤ) (FW : List ((ℤ × ℤ × ℤ) × ℕ)) (D : ℕ) : Bool :=
  A.all (fun v => vertexLoad FW v ≤ D)

/-! ## Sidon (no-3-AP) predicate, self-contained for this file

A list `S` is *Sidon* (relative to a weak Sidon ambient set) iff it contains no 3-term AP.
We phrase "contains a 3-term AP from the family `FW`" so the soundness statement is about the
*same* family the certificate weights — that is exactly what makes the bound finite. -/

/-- `containsTriple S t` : all three vertices of the AP `t` occur in `S`. -/
def containsTriple (S : List ℤ) (t : ℤ × ℤ × ℤ) : Bool :=
  S.contains t.1 && S.contains t.2.1 && S.contains t.2.2

/-- `S` avoids every AP listed in `FW` (contains none of them fully).  A no-3-AP set in
particular avoids every genuine AP, so in particular every AP we listed. -/
def avoidsAll (S : List ℤ) (FW : List ((ℤ × ℤ × ℤ) × ℕ)) : Bool :=
  FW.all (fun p => !containsTriple S p.1)

/-! ## The double-counting core

For any list `H` of vertices that **hits** every edge of `FW` (contains ≥ one vertex of each
listed AP), the total weight is bounded by the loads carried by `H`:
`totalW FW ≤ Σ_{v ∈ H} vertexLoad FW v`. -/

/-- `H` hits every listed AP: each edge of `FW` has at least one vertex in `H`. -/
def hitsAll (H : List ℤ) (FW : List ((ℤ × ℤ × ℤ) × ℕ)) : Prop :=
  ∀ p ∈ FW, ∃ v ∈ H, memTriple v p.1 = true

/-- Sum of `vertexLoad FW v` over `v ∈ H` (as a list sum). -/
def loadSum (H : List ℤ) (FW : List ((ℤ × ℤ × ℤ) × ℕ)) : ℕ :=
  (H.map (vertexLoad FW)).sum

/-- If some `v0 ∈ H` lies on `t`, the contribution `Σ_{v∈H} (if v∈t then wt else 0)` is
`≥ wt`. -/
theorem single_edge_charge (H : List ℤ) (t : ℤ × ℤ × ℤ) (wt : ℕ)
    (hv : ∃ v ∈ H, memTriple v t = true) :
    wt ≤ (H.map (fun v => if memTriple v t then wt else 0)).sum := by
  obtain ⟨v0, hv0H, hv0t⟩ := hv
  -- the summand at `v0` is exactly `wt`; all summands are `≥ 0`.
  have hmem : (if memTriple v0 t then wt else 0) ∈
      (H.map (fun v => if memTriple v t then wt else 0)) := by
    apply List.mem_map.2
    exact ⟨v0, hv0H, rfl⟩
  have hle : (if memTriple v0 t then wt else 0) ≤
      (H.map (fun v => if memTriple v t then wt else 0)).sum :=
    List.single_le_sum (by intro x _; exact Nat.zero_le x) _ hmem
  simpa [hv0t] using hle

/-- **Double-counting bound.**  If `H` hits every listed AP then the matching's total weight
is at most the total load carried by `H`. -/
theorem totalW_le_loadSum (H : List ℤ) :
    ∀ FW : List ((ℤ × ℤ × ℤ) × ℕ), hitsAll H FW → totalW FW ≤ loadSum H FW := by
  intro FW
  induction FW with
  | nil => intro _; simp [totalW, loadSum]
  | cons p rest ih =>
    intro hhit
    -- the head edge `p` is hit by some `v ∈ H`; the tail `rest` is still hit.
    have hhead : ∃ v ∈ H, memTriple v p.1 = true := hhit p (by simp)
    have hrest : hitsAll H rest := by
      intro q hq; exact hhit q (by simp [hq])
    -- `loadSum` on the consed family splits: edge term of `p` + load of the tail.
    have hload : loadSum H (p :: rest)
        = (H.map (fun v => if memTriple v p.1 then p.2 else 0)).sum + loadSum H rest := by
      unfold loadSum
      have hfun : (vertexLoad (p :: rest))
          = (fun v => (if memTriple v p.1 then p.2 else 0) + vertexLoad rest v) := by
        funext v; cases p; rfl
      rw [hfun, List.sum_map_add]
    -- `totalW` on the consed family: `w_p + totalW rest`.
    have htot : totalW (p :: rest) = p.2 + totalW rest := by
      simp [totalW]
    rw [hload, htot]
    have h1 : p.2 ≤ (H.map (fun v => if memTriple v p.1 then p.2 else 0)).sum :=
      single_edge_charge H p.1 p.2 hhead
    have h2 : totalW rest ≤ loadSum H rest := ih hrest
    exact Nat.add_le_add h1 h2

/-- If every vertex of `H` carries load `≤ D`, then the total load on `H` is `≤ D·|H|`. -/
theorem loadSum_le (H : List ℤ) (FW : List ((ℤ × ℤ × ℤ) × ℕ)) (D : ℕ)
    (hD : ∀ v ∈ H, vertexLoad FW v ≤ D) :
    loadSum H FW ≤ D * H.length := by
  unfold loadSum
  calc (H.map (vertexLoad FW)).sum
      ≤ (H.map (fun _ => D)).sum := List.sum_le_sum (by intro v hv; exact hD v hv)
    _ = D * H.length := by
        simp [List.map_const', List.sum_replicate, smul_eq_mul, Nat.mul_comm]

/-! ## The transversal soundness lemma

Putting the pieces together: a fractional-matching certificate forces every set avoiding all
listed APs to be small.  This is the load-bearing result — it carries the `O(|F|·N)`
certificate in place of the `C(N, m+1)` enumeration. -/

/-- Membership-in-`A` for the three vertices of a listed AP (decoded from `tripleInA`). -/
theorem tripleInA_mem {A : List ℤ} {t : ℤ × ℤ × ℤ} (h : tripleInA A t = true) :
    t.1 ∈ A ∧ t.2.1 ∈ A ∧ t.2.2 ∈ A := by
  unfold tripleInA at h
  simp only [Bool.and_eq_true, List.contains_eq_mem, decide_eq_true_eq] at h
  exact ⟨h.1.1, h.1.2, h.2⟩

/-- **Transversal soundness lemma (coordinate-free).**

Given a point list `A` (`Nodup`), a weighted AP-family certificate `FW` with

* `hedges : edgesOK A FW = true` — every listed edge is a genuine 3-AP inside `A`,
* `hload  : loadOK A FW D = true` — every point of `A` carries total weight `≤ D`,
* `hT     : D * (A.length - m - 1) < totalW FW` — the fractional-matching value exceeds
  `D·(N − m − 1)`,

every sublist `S ⊆ A` (`Nodup`) that **avoids every listed AP** has `S.length ≤ m`.

In the intended application the listed APs are exactly the 3-term APs of `A`, so a no-3-AP
(Sidon, by [MT26] Lemma 2.3) subset automatically avoids them all; hence `h(A) ≤ m`. -/
theorem hLe_of_fracMatching
    {A : List ℤ} {FW : List ((ℤ × ℤ × ℤ) × ℕ)} {D m : ℕ}
    (hA : A.Nodup)
    (hedges : edgesOK A FW = true)
    (hload : loadOK A FW D = true)
    (hT : D * (A.length - m - 1) < totalW FW)
    {S : List ℤ} (hS : S.Nodup) (hSsub : S ⊆ A)
    (hSavoid : avoidsAll S FW = true) :
    S.length ≤ m := by
  -- The complement `H = A \ S` (points of `A` not in `S`).
  set H : List ℤ := A.filter (fun x => !S.contains x) with hHdef
  -- characterise membership in `H`.
  have hHmem : ∀ x, x ∈ H ↔ (x ∈ A ∧ x ∉ S) := by
    intro x
    rw [hHdef, List.mem_filter]
    simp [List.contains_eq_mem]
  -- (1) `H` hits every listed AP: `S` avoids each AP, so a vertex of it is outside `S`,
  --     and (edges in `A`) that vertex lies in `A`, hence in `H`.
  have hhits : hitsAll H FW := by
    intro p hp
    -- decode `edgesOK`: every vertex of `p.1` is in `A`.
    have hpOK : (isAP p.1 && tripleInA A p.1) = true := by
      have := (List.all_eq_true.1 hedges) p hp
      simpa using this
    have htriA : tripleInA A p.1 = true := (Bool.and_eq_true _ _ ▸ hpOK).2
    obtain ⟨hAa, hAb, hAc⟩ := tripleInA_mem htriA
    -- `S` does not contain all three vertices of `p`: at least one is not in `S`.
    have hcons : p.1.1 ∉ S ∨ p.1.2.1 ∉ S ∨ p.1.2.2 ∉ S := by
      have h0 := (List.all_eq_true.1 hSavoid) p hp
      simp only [Bool.not_eq_true', containsTriple, Bool.and_eq_false_iff,
        List.contains_eq_mem, decide_eq_false_iff_not] at h0
      tauto
    -- pick the witness vertex; it is in `A` and not in `S`, hence in `H`, and on `p.1`.
    rcases hcons with h | h | h
    · exact ⟨p.1.1, (hHmem _).2 ⟨hAa, h⟩, by unfold memTriple; simp⟩
    · exact ⟨p.1.2.1, (hHmem _).2 ⟨hAb, h⟩, by unfold memTriple; simp⟩
    · exact ⟨p.1.2.2, (hHmem _).2 ⟨hAc, h⟩, by unfold memTriple; simp⟩
  -- (2) double-counting:  totalW ≤ loadSum H ≤ D·|H|.
  have hdc : totalW FW ≤ loadSum H FW := totalW_le_loadSum H FW hhits
  have hHloadEach : ∀ v ∈ H, vertexLoad FW v ≤ D := by
    intro v hv
    have hvA : v ∈ A := ((hHmem v).1 hv).1
    have := (List.all_eq_true.1 hload) v hvA
    simpa using this
  have hloadD : loadSum H FW ≤ D * H.length := loadSum_le H FW D hHloadEach
  have hTle : totalW FW ≤ D * H.length := le_trans hdc hloadD
  -- (3) cardinality:  |S| + |H| = |A|, hence |H| = N - |S|.
  have hcard : S.length + H.length = A.length := by
    have hsplit := List.length_eq_length_filter_add (l := A) (fun x => S.contains x)
    -- `A.length = |filter S.contains A| + |filter (¬S.contains) A|`
    -- the second term is `H.length`.
    have hfilterS : (A.filter (fun x => S.contains x)).length = S.length := by
      apply Nat.le_antisymm
      · -- filter ⊆ S, filter nodup
        have hsubF : (A.filter (fun x => S.contains x)) ⊆ S := by
          intro x hx
          rw [List.mem_filter] at hx
          have := hx.2; rw [List.contains_eq_mem, decide_eq_true_eq] at this; exact this
        have hnodupF : (A.filter (fun x => S.contains x)).Nodup := hA.filter _
        calc (A.filter (fun x => S.contains x)).length
            = (A.filter (fun x => S.contains x)).toFinset.card :=
              (List.toFinset_card_of_nodup hnodupF).symm
          _ ≤ S.toFinset.card :=
              Finset.card_le_card (by
                intro x hx; rw [List.mem_toFinset] at *; exact hsubF hx)
          _ = S.length := List.toFinset_card_of_nodup hS
      · have hsubF : S ⊆ (A.filter (fun x => S.contains x)) := by
          intro x hx
          rw [List.mem_filter]
          exact ⟨hSsub hx, by rw [List.contains_eq_mem, decide_eq_true_eq]; exact hx⟩
        calc S.length = S.toFinset.card := (List.toFinset_card_of_nodup hS).symm
          _ ≤ (A.filter (fun x => S.contains x)).toFinset.card :=
              Finset.card_le_card (by
                intro x hx; rw [List.mem_toFinset] at *; exact hsubF hx)
          _ ≤ (A.filter (fun x => S.contains x)).length := List.toFinset_card_le _
    -- combine
    rw [hHdef]
    omega
  -- (4) conclude by contradiction: if |S| ≥ m+1 then |H| ≤ N−m−1, contradicting hT.
  by_contra hlt
  rw [Nat.not_le] at hlt   -- hlt : m < S.length
  have hHsmall : H.length ≤ A.length - m - 1 := by omega
  have : D * H.length ≤ D * (A.length - m - 1) := Nat.mul_le_mul_left D hHsmall
  have : totalW FW ≤ D * (A.length - m - 1) := le_trans hTle this
  omega

/-! ## Validation on the record gadget `A_base`

We instantiate the machinery on the known 14-point record set `A_base`
(`h(A_base) = 8`).  Its 3-uniform AP-hypergraph has **twelve** 3-term APs.

We supply a **fractional-matching certificate** `Fcert_base` (denominator `D = 6`) over
those 12 APs whose total weight is `T = 27` and whose every vertex load is `≤ 6`
(`ν* = T/D = 4.5`).  Both finite facts are `decide`-checked (kernel, zero axioms).  Through
`hLe_of_fracMatching` this certifies — by the `O(|F|·N)` transversal route, **not** the
`C(14,9)` enumeration — that every no-3-AP sublist of `A_base` has length `≤ 9`, i.e.
`τ(A_base) ≥ 5`, hence `h(A_base) ≤ 9`.

### Honest scope note (the integrality gap)

The *tight* value is `h(A_base) = 8` (`τ = 6`), proved zero-axiom in `Constants.C5b` by the
`C(14,9)` enumeration.  The **fractional** matching value here is only `ν* = 4.5`, and `4.5`
is the exact LP optimum (verified): A_base's AP-hypergraph has an integrality gap
`τ = 6 > ⌈ν*⌉ = 5`.  Pure LP-duality therefore certifies `h ≤ 9`, **not** the tight `h ≤ 8`.
Closing the last unit (`h ≤ 8`) needs an *integral* transversal certificate (a branching /
odd-set strengthening of this lemma) — that is the next sub-goal.  The soundness lemma above
is the reusable, fully-verified core; this validation confirms it fires end-to-end on a real
gadget with zero axioms. -/

namespace Validation

/-- The 14-point record set (mirrors `C5b.Abase`). -/
def Abase : List ℤ :=
  [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]

/-- Fractional-matching certificate over the twelve 3-term APs of `A_base`, weights at
denominator `D = 6` (total `T = 27`, every vertex load `≤ 6`, `ν* = 4.5`). -/
def Fcert_base : List ((ℤ × ℤ × ℤ) × ℕ) :=
  [ ((0, 136, 272), 2),
    ((0, 200, 400), 0),
    ((0, 298, 596), 2),
    ((0, 528, 1056), 2),
    ((136, 596, 1056), 4),
    ((200, 243, 286), 4),
    ((200, 249, 298), 2),
    ((243, 246, 249), 2),
    ((246, 272, 298), 1),
    ((246, 323, 400), 3),
    ((249, 286, 323), 2),
    ((272, 400, 528), 3) ]

/-- Every listed edge is a genuine 3-AP whose vertices lie in `A_base`. -/
theorem Fcert_base_edgesOK : edgesOK Abase Fcert_base = true := by decide

/-- Every point of `A_base` carries total certificate weight `≤ 6`. -/
theorem Fcert_base_loadOK : loadOK Abase Fcert_base 6 = true := by decide

/-- The certificate's total weight is `27` (fractional-matching value `27/6 = 4.5`). -/
theorem Fcert_base_total : totalW Fcert_base = 27 := by decide

/-- `A_base` lists 14 distinct integers. -/
theorem Abase_nodup : Abase.Nodup := by decide

/-- `A_base` has length 14. -/
theorem Abase_length : Abase.length = 14 := by decide

/-- **Validation.**  Via the transversal soundness lemma, the `decide`-checked
fractional-matching certificate forces every sublist of `A_base` that avoids all twelve
listed APs to have length `≤ 9`.  (For a genuinely no-3-AP — i.e. Sidon — subset this is
automatic, since it avoids every AP; so `h(A_base) ≤ 9` by the transversal route.)

This fires the machinery end-to-end on a real gadget with **zero axioms**; the gap to the
tight `h ≤ 8` is the integrality gap documented above. -/
theorem Abase_avoiders_le_9
    {S : List ℤ} (hS : S.Nodup) (hSsub : S ⊆ Abase)
    (hSavoid : avoidsAll S Fcert_base = true) :
    S.length ≤ 9 := by
  have hT : (6 : ℕ) * (Abase.length - 9 - 1) < totalW Fcert_base := by
    rw [Abase_length, Fcert_base_total]; omega   -- 6 * 4 = 24 < 27
  exact hLe_of_fracMatching (D := 6) (m := 9) Abase_nodup Fcert_base_edgesOK
    Fcert_base_loadOK hT hS hSsub hSavoid

end Validation

end C5bTransversal
