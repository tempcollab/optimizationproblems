import Mathlib
import Constants.C5bTransversal

/-!
# C_5b : depth-bounded BRANCHING transversal certificate for `h(A) ≤ m` (tight)

This file closes the **integrality gap** left by the fractional-matching certificate of
`Constants.C5bTransversal`.  That lemma (`hLe_of_fracMatching`) bounds the minimum
transversal `τ` of the 3-AP hypergraph `H(A)` by an LP-duality (fractional matching) value
`ν*`, and on the record gadget `A_base` the gap `τ = 6 > ⌈ν*⌉ = 5` means the fractional cert
only proves `h(A_base) ≤ 9`, **not** the tight `h(A_base) ≤ 8`.

Here we replace the fractional lower bound on `τ` by an **exact branch-and-bound hitting-set
lower bound**, formalized as a structurally-recursive `Bool` predicate `noTransLe` plus a
clean soundness induction.  This reaches the integral `τ = 6` on `A_base` and so certifies the
**tight** `h(A_base) ≤ 8`.

## The certificate (branch-and-bound hitting-set lower bound, hand-auditable)

For a list `FW` of edges (3-term APs) and a budget `k : ℕ`, `noTransLe FW k = true` means:
**no vertex set of size `≤ k` hits every edge of `FW`** (equivalently `τ(FW) > k`).  It is the
standard hitting-set B&B:

* if `FW = []` there is nothing to hit, so the empty set (size `0 ≤ k`) is a transversal —
  a transversal of size `≤ k` *exists*, so return `false`;
* if `k = 0` and `FW ≠ []`, no set of size `0` hits a nonempty family — return `true`;
* otherwise any transversal must contain a vertex of the *first* edge `(a,b,c)`; branch on the
  three choices, removing that vertex (and every edge through it) from the family and
  decrementing the budget, and `AND` the three recursive verdicts.

`noTransLe (allAPs A) k = true` certifies `τ(H(A)) > k`, hence (the complement of any no-3-AP
set is a transversal) `h(A) ≤ N − k − 1`.  With `k = 5` on `A_base` this gives `h ≤ 8`.

## What is FORMALIZED here (no `sorry`, no smuggled axiom)

`noTransLe_sound` : the **soundness lemma** — `noTransLe FW k = true → every hitting list `H`
of `FW` has `k < H.length`.  Proof: strong induction on the recursion's fuel/budget, using
the residual-hitting lemma `hitsAll_removeVertex_erase` (erasing the chosen branch vertex from
a hitting set still hits every edge not through that vertex).

`hLe_of_branchCert` : the **bridge** — wraps `noTransLe_sound` with the SAME complement /
cardinality split proven in `C5bTransversal.hLe_of_fracMatching`, giving `h(A) ≤ N − k − 1`
for any `A` and any branching certificate `noTransLe FW k = true` (with `FW` a family of genuine
APs inside `A`).

## Validation on the record gadget `A_base` (zero added axioms, by `decide`)

`Abase_branch_tau` : `noTransLe Abase_APs 5 = true` by kernel `decide` (364-node search tree,
well within plain `decide`; worst case `3^5 = 243` leaves).  Via `hLe_of_branchCert` this
certifies the **tight** `h(A_base) ≤ 8` through the transversal route — closing the gap the
fractional lemma left open.

## TRUST BOUNDARY (honest scope)

This file is a **machinery** sub-goal.  By itself it does **not** beat the record `4/7`: it
re-derives the *known* `h(A_base) = 8` (the record value), now via a *tight, scalable*
transversal route rather than the `C(14,9)` enumeration.  Its value is that it removes the
integrality-gap blocker: a future indecomposable `N ≈ 30` gadget with `h = 17` can now be
Lean-certified `h ≤ 16` once it is found (the gadget search is a separate, off-Lean step, still
open).  The `MTThm15` bridge (Thm 1.5: `c* = inf f(n)/n`) certifying the actual constant lives
in `Constants.C5b` and is an explicit hypothesis there, not assumed here.

Source of the structural facts: Ma & Tang, arXiv:2602.23282 (Feb 2026), **[MT26]**
(Lemma 2.3: inside a weak Sidon set, Sidon ⟺ no 3-term AP).  The branch-and-bound hitting-set
lower bound is standard.
-/

namespace C5bBranch

open C5bTransversal

/-! ## The branching predicate -/

/-- Remove from the family every edge that passes through vertex `v`. -/
def removeVertex (v : ℤ) (FW : List ((ℤ × ℤ × ℤ) × ℕ)) : List ((ℤ × ℤ × ℤ) × ℕ) :=
  FW.filter (fun p => !memTriple v p.1)

/-- **The branch-and-bound hitting-set certificate.**

`noTransLe FW k = true` certifies that **no** vertex list of size `≤ k` hits every edge of
`FW`, i.e. `τ(FW) > k`.  Structurally recursive on `FW` and `k` (each branch strictly
decreases `k`, and at `k = 0` the recursion stops). -/
def noTransLe : List ((ℤ × ℤ × ℤ) × ℕ) → ℕ → Bool
  | [], _ => false
  | (_ :: _), 0 => true
  | (p :: rest), (k + 1) =>
      let a := p.1.1; let b := p.1.2.1; let c := p.1.2.2
      noTransLe (removeVertex a (p :: rest)) k
        && noTransLe (removeVertex b (p :: rest)) k
        && noTransLe (removeVertex c (p :: rest)) k

/-! ## Residual-hitting lemma

If `H` hits every edge of `FW` and `v ∈ H`, then `H.erase v` hits every edge of
`removeVertex v FW` (the edges that survive removal are exactly those NOT through `v`, so the
witness vertex in `H` for such an edge is `≠ v` and survives the erase). -/

/-- Every edge surviving `removeVertex v FW` does NOT contain `v`. -/
theorem mem_removeVertex {v : ℤ} {FW : List ((ℤ × ℤ × ℤ) × ℕ)} {p : (ℤ × ℤ × ℤ) × ℕ}
    (h : p ∈ removeVertex v FW) : p ∈ FW ∧ memTriple v p.1 = false := by
  unfold removeVertex at h
  rw [List.mem_filter] at h
  refine ⟨h.1, ?_⟩
  have := h.2
  simpa using this

/-- If `H` hits all of `FW` and `v ∈ H`, then `H.erase v` hits all of `removeVertex v FW`. -/
theorem hitsAll_removeVertex_erase {H : List ℤ} {v : ℤ}
    {FW : List ((ℤ × ℤ × ℤ) × ℕ)}
    (hhits : hitsAll H FW) :
    hitsAll (H.erase v) (removeVertex v FW) := by
  intro p hp
  obtain ⟨hpFW, hpv⟩ := mem_removeVertex hp
  -- a witness `w ∈ H` lies on `p`; since `p` avoids `v`, `w ≠ v`, so `w` survives the erase.
  obtain ⟨w, hwH, hwp⟩ := hhits p hpFW
  have hwv : w ≠ v := by
    rintro rfl
    rw [hwp] at hpv; exact absurd hpv (by simp)
  refine ⟨w, ?_, hwp⟩
  rw [List.mem_erase_of_ne hwv]; exact hwH

/-! ## Soundness of the branching certificate -/

/-- **Soundness lemma.**  If `noTransLe FW k = true`, then every list `H` that hits all of
`FW` (and is `Nodup`) has size strictly greater than `k`.  Equivalently `τ(FW) > k`.

Strong induction on `k`; the residual-hitting lemma feeds the IH on the chosen branch. -/
theorem noTransLe_sound :
    ∀ (k : ℕ) (FW : List ((ℤ × ℤ × ℤ) × ℕ)) (H : List ℤ),
      H.Nodup → noTransLe FW k = true → hitsAll H FW → k < H.length := by
  intro k
  induction k with
  | zero =>
    intro FW H _ hcert hhits
    -- `noTransLe FW 0 = true` forces `FW ≠ []`; a nonempty family needs a hitting vertex.
    cases FW with
    | nil => simp [noTransLe] at hcert
    | cons p rest =>
      -- the head edge `p` is hit by some `w ∈ H`, so `H ≠ []`, hence `0 < H.length`.
      obtain ⟨w, hwH, _⟩ := hhits p (by simp)
      have : H ≠ [] := by rintro rfl; simp at hwH
      exact Nat.pos_of_ne_zero (by simpa [List.length_eq_zero_iff] using this)
  | succ k ih =>
    intro FW H hH hcert hhits
    cases FW with
    | nil => simp [noTransLe] at hcert
    | cons p rest =>
      -- decode the three-way `AND`.
      have hcert3 :
          noTransLe (removeVertex p.1.1 (p :: rest)) k = true
          ∧ noTransLe (removeVertex p.1.2.1 (p :: rest)) k = true
          ∧ noTransLe (removeVertex p.1.2.2 (p :: rest)) k = true := by
        simp only [noTransLe, Bool.and_eq_true] at hcert
        exact ⟨hcert.1.1, hcert.1.2, hcert.2⟩
      -- `H` hits the head edge `p`: some witness `w ∈ H` lies on `(a,b,c)`.
      obtain ⟨w, hwH, hwp⟩ := hhits p (by simp)
      -- `w` is one of the three vertices of `p`.
      have hw3 : w = p.1.1 ∨ w = p.1.2.1 ∨ w = p.1.2.2 := by
        unfold memTriple at hwp
        simp only [Bool.or_eq_true, beq_iff_eq] at hwp
        tauto
      -- common facts about the erase
      have hlen : (H.erase w).length = H.length - 1 := by
        rw [List.length_erase_of_mem hwH]
      have hH' : (H.erase w).Nodup := hH.erase w
      have hres : hitsAll (H.erase w) (removeVertex w (p :: rest)) :=
        hitsAll_removeVertex_erase hhits
      -- in each case rewrite the chosen branch and feed the IH
      rcases hw3 with h | h | h
      · rw [h] at hres hlen hH'
        have := ih (removeVertex p.1.1 (p :: rest)) (H.erase p.1.1) hH' hcert3.1 hres
        omega
      · rw [h] at hres hlen hH'
        have := ih (removeVertex p.1.2.1 (p :: rest)) (H.erase p.1.2.1) hH' hcert3.2.1 hres
        omega
      · rw [h] at hres hlen hH'
        have := ih (removeVertex p.1.2.2 (p :: rest)) (H.erase p.1.2.2) hH' hcert3.2.2 hres
        omega

/-! ## The tight transversal bound (bridge)

We reuse the complement / cardinality split of `C5bTransversal.hLe_of_fracMatching` verbatim,
swapping the fractional `τ`-lower-bound for the branching one.  A no-3-AP set `S ⊆ A` has
complement `H = A \ S` a transversal of the AP family; `noTransLe_sound` gives `|H| > k`, and
`|S| + |H| = N` gives `|S| < N − k`, i.e. `|S| ≤ N − k − 1`. -/

/-- **Tight transversal soundness lemma (coordinate-free).**

Given a point list `A` (`Nodup`), an edge family `FW` with every edge a genuine 3-AP inside
`A` (`edgesOK A FW = true`), and a branching certificate `noTransLe FW k = true` (so
`τ(FW) > k`), every sublist `S ⊆ A` (`Nodup`) that **avoids every listed AP** has
`S.length ≤ A.length − k − 1`.

In the intended application `FW` lists exactly the 3-term APs of `A`, so a no-3-AP (Sidon, by
[MT26] Lemma 2.3) subset avoids them all; hence `h(A) ≤ N − k − 1`. -/
theorem hLe_of_branchCert
    {A : List ℤ} {FW : List ((ℤ × ℤ × ℤ) × ℕ)} {k : ℕ}
    (hA : A.Nodup)
    (hedges : edgesOK A FW = true)
    (hcert : noTransLe FW k = true)
    {S : List ℤ} (hS : S.Nodup) (hSsub : S ⊆ A)
    (hSavoid : avoidsAll S FW = true) :
    S.length ≤ A.length - k - 1 := by
  -- The complement `H = A \ S` hits every listed AP (identical construction to the fractional
  -- lemma).  We re-derive `hitsAll H FW` here.
  set H : List ℤ := A.filter (fun x => !S.contains x) with hHdef
  have hHmem : ∀ x, x ∈ H ↔ (x ∈ A ∧ x ∉ S) := by
    intro x
    rw [hHdef, List.mem_filter]
    simp [List.contains_eq_mem]
  have hhits : hitsAll H FW := by
    intro p hp
    have hpOK : (isAP p.1 && tripleInA A p.1) = true := by
      have := (List.all_eq_true.1 hedges) p hp
      simpa using this
    have htriA : tripleInA A p.1 = true := (Bool.and_eq_true _ _ ▸ hpOK).2
    obtain ⟨hAa, hAb, hAc⟩ := tripleInA_mem htriA
    have hcons : p.1.1 ∉ S ∨ p.1.2.1 ∉ S ∨ p.1.2.2 ∉ S := by
      have h0 := (List.all_eq_true.1 hSavoid) p hp
      simp only [Bool.not_eq_true', containsTriple, Bool.and_eq_false_iff,
        List.contains_eq_mem, decide_eq_false_iff_not] at h0
      tauto
    rcases hcons with h | h | h
    · exact ⟨p.1.1, (hHmem _).2 ⟨hAa, h⟩, by unfold memTriple; simp⟩
    · exact ⟨p.1.2.1, (hHmem _).2 ⟨hAb, h⟩, by unfold memTriple; simp⟩
    · exact ⟨p.1.2.2, (hHmem _).2 ⟨hAc, h⟩, by unfold memTriple; simp⟩
  -- `H` is `Nodup` (filter of a `Nodup` list).
  have hHnodup : H.Nodup := hA.filter _
  -- the branching certificate ⇒ `k < |H|`.
  have hHlen : k < H.length := noTransLe_sound k FW H hHnodup hcert hhits
  -- cardinality split `|S| + |H| = |A|` (identical to the fractional lemma).
  have hcard : S.length + H.length = A.length := by
    have hsplit := List.length_eq_length_filter_add (l := A) (fun x => S.contains x)
    have hfilterS : (A.filter (fun x => S.contains x)).length = S.length := by
      apply Nat.le_antisymm
      · have hsubF : (A.filter (fun x => S.contains x)) ⊆ S := by
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
    rw [hHdef]
    omega
  -- conclude:  |S| = N − |H| ≤ N − (k+1) = N − k − 1.
  omega

/-! ## Validation on the record gadget `A_base` (tight `h ≤ 8`) -/

namespace Validation

open C5bTransversal.Validation in
/-- The 14-point record set (re-export of `C5bTransversal.Validation.Abase`). -/
def Abase : List ℤ := C5bTransversal.Validation.Abase

/-- The twelve 3-term APs of `A_base`, as an unweighted (weight-0) edge family.  Only the
edge triples matter for the branching certificate; the weights are inert. -/
def Abase_APs : List ((ℤ × ℤ × ℤ) × ℕ) :=
  [ ((0, 136, 272), 0),
    ((0, 200, 400), 0),
    ((0, 298, 596), 0),
    ((0, 528, 1056), 0),
    ((136, 596, 1056), 0),
    ((200, 243, 286), 0),
    ((200, 249, 298), 0),
    ((243, 246, 249), 0),
    ((246, 272, 298), 0),
    ((246, 323, 400), 0),
    ((249, 286, 323), 0),
    ((272, 400, 528), 0) ]

/-- Every listed edge is a genuine 3-AP whose vertices lie in `A_base`. -/
theorem Abase_APs_edgesOK : edgesOK Abase Abase_APs = true := by decide

/-- **Branching certificate** : no transversal of size `≤ 5` hits all twelve APs, i.e.
`τ(A_base) > 5`, so `τ ≥ 6`.  Checked by kernel `decide` (364-node tree). -/
theorem Abase_branch_tau : noTransLe Abase_APs 5 = true := by decide

/-- `A_base` lists 14 distinct integers. -/
theorem Abase_nodup : Abase.Nodup := by decide

/-- `A_base` has length 14. -/
theorem Abase_length : Abase.length = 14 := by decide

/-- **Validation (tight).**  Via the branching transversal soundness lemma, the
`decide`-checked branching certificate forces every sublist of `A_base` that avoids all twelve
APs to have length `≤ 8`.  (For a genuinely no-3-AP — Sidon — subset this is automatic, since
it avoids every AP; so `h(A_base) ≤ 8` by the *tight* transversal route.)

This closes the integrality gap left by `C5bTransversal.Abase_avoiders_le_9` (`h ≤ 9`): the
branching cert reaches the integral `τ = 6`, matching the `C(14,9)` enumeration of
`Constants.C5b` but at `decide`-tractable `O(3^budget)` cost. -/
theorem Abase_avoiders_le_8
    {S : List ℤ} (hS : S.Nodup) (hSsub : S ⊆ Abase)
    (hSavoid : avoidsAll S Abase_APs = true) :
    S.length ≤ 8 := by
  have h := hLe_of_branchCert (A := Abase) (FW := Abase_APs) (k := 5)
    Abase_nodup Abase_APs_edgesOK Abase_branch_tau hS hSsub hSavoid
  -- `A_base.length - 5 - 1 = 14 - 6 = 8`.
  rw [Abase_length] at h
  simpa using h

end Validation

end C5bBranch
