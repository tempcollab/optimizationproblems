import Mathlib
import Constants.C5bTransversal
import Constants.C5bBranch

/-!
# C_5b : INTERLEAVED (fix-then-branch) transversal certificate for `h(A) ≤ m`

This file builds the genuinely **budget-shrinking** transversal lower bound that the R4
`max`-composition `hLe_of_hybrid` did NOT deliver.  The composition there took the *minimum*
of the fractional and branching `|S|`-bounds — sound, but the branching certificate still had
to certify the **full** `τ` on its own (full budget).  Here we **interleave**: the fractional
certificate carries part `a` of the transversal lower bound on a chosen **support** `P`, and
the branch-and-bound certifies the rest only on the **residual** family (the listed APs that
avoid `P`), with budget `g`.  The two parts are vertex-disjoint by construction, so they add
with **no double counting**:
`τ(FW_frac ∪ FW_res) ≥ a + (g + 1)`, hence `h(A) ≤ N − a − g − 1`.

This is the standard LP-fix-then-branch rule for `d`-Hitting-Set (`d = 3`): cover the LP
support with the fractional charge, contract it out, branch the bounded residual
(Nemhauser–Trotter half-integrality; refs arXiv:2308.05974, arXiv:2506.24114,
arXiv:1811.09429).  At `N ≈ 30`, when the LP has an **integral** component, `a` is large and
the residual budget `g = τ − a` is tiny, so the `3^g` branch tree stays `decide`-tractable —
which the plain `max`-hybrid never achieved.

## What is FORMALIZED here (no `sorry`, no smuggled axiom, no `native_decide`)

`hLe_of_interleaved` : the **interleaved soundness lemma**.  Its load-bearing new content is
the *disjoint residual attribution*: an arbitrary hitting set `H` of the combined family is
split as `(H ∩ P) ⊎ (H \ P)`, the fractional load lemma forces `|H ∩ P| ≥ a` (only `P`-vertices
carry the listed charge), and the residual-hitting argument (`H \ P` hits every residual edge,
because residual edges avoid `P`) feeds `noTransLe_sound` to force `|H \ P| ≥ g + 1`.  The two
parts are a genuine partition of the `Nodup` list `H`, so `|H| ≥ a + (g + 1)` with no double
counting.  Every step is inside the formalization.

The fractional half reuses `C5bTransversal.totalW_le_loadSum` (the load-bearing double-counting
lemma, already proven for any hitting set); the residual half reuses
`C5bBranch.noTransLe_sound` and `C5bBranch.hitsAll_removeVertex_erase`.

## HONEST scope note — the A_base validation (read this)

We validate `hLe_of_interleaved` end-to-end with **zero added axioms** on two instances:

* `A_syn` — a synthetic 4-AP instance (two vertex-disjoint APs charged fractionally, `a = 2`;
  two vertex-disjoint APs in the residual, branch budget `g = 1`, `3^1 = 3` leaves) reaching
  `τ = 4`.  This **exhibits the budget-shrink mechanism**: `τ = 4` is certified branching only
  `g = 1` (vs the pure branch budget `3`), with the fractional cert carrying the other `2`.

* `A_base` — the record 14-point gadget.  Here the interleaving **degenerates**: `A_base`'s
  3-AP hypergraph is a *fully half-integral* instance (the cover LP is `0/½`-valued with value
  `ν* = 4.5`, no integral component, **no forced vertex**, 143 distinct minimum covers).  An
  exhaustive check (`certificate/interleaved/check_interleaved_cert.py`) proves
  `max_{P ⊆ A} ( ⌈ν*(FW_frac⊆P)⌉ + τ(residual avoiding P) ) = 6`, attained **only** at
  `P = ∅` (`a = 0`, full branch budget `g = 5`).  So on `A_base` the interleaved cert cannot
  beat the pure branch budget — the proposed `g ≈ τ − ⌈ν*⌉ = 1` budget is **not achievable**
  for this half-integral instance.  We therefore validate `hLe_of_interleaved` on `A_base` in
  the degenerate `P = ∅` form (`a = 0`, `g = 5`), re-deriving the tight `h(A_base) ≤ 8`, which
  confirms the lemma is *sound* (it never claims more than the truth) even though the
  budget-shrink it is built for does not fire on this particular pathological gadget.  The
  mechanism's value is for the `N ≈ 30` target, where an integral LP component is expected.

Source of the structural facts: Ma & Tang, arXiv:2602.23282 (Feb 2026), **[MT26]**
(Lemma 2.3: inside a weak Sidon set, Sidon ⟺ no 3-term AP).  LP-fix-then-branch for
`d`-Hitting-Set is standard (Nemhauser–Trotter; refs above).
-/

namespace C5bInterleaved

open C5bTransversal C5bBranch

/-! ## Support membership and the residual family -/

/-- `v` is in the support list `P` (decidable membership of an integer in a list). -/
def inP (P : List ℤ) (v : ℤ) : Bool := P.contains v

/-- An edge `t` **avoids** the support `P` : none of its three vertices is in `P`. -/
def edgeAvoidsP (P : List ℤ) (t : ℤ × ℤ × ℤ) : Bool :=
  !(P.contains t.1) && !(P.contains t.2.1) && !(P.contains t.2.2)

/-- The fractional family's support lies in `P` : every vertex of every listed edge is in `P`. -/
def suppInP (P : List ℤ) (FW : List ((ℤ × ℤ × ℤ) × ℕ)) : Bool :=
  FW.all (fun p => P.contains p.1.1 && P.contains p.1.2.1 && P.contains p.1.2.2)

/-- Every residual edge avoids `P`. -/
def resAvoidsP (P : List ℤ) (FW : List ((ℤ × ℤ × ℤ) × ℕ)) : Bool :=
  FW.all (fun p => edgeAvoidsP P p.1)

/-! ## The fractional half : `a ≤ |H ∩ P|`

If the fractional family's support is inside `P`, a vertex `v ∉ P` carries **zero** load, so
the load is concentrated on `H ∩ P`.  Hence `totalW ≤ loadSum (H ∩ P) ≤ D·|H ∩ P|`. -/

/-- A vertex outside the support of `FW` carries zero load (when `suppInP P FW` and `v ∉ P`). -/
theorem vertexLoad_zero_of_notInP
    {P : List ℤ} {FW : List ((ℤ × ℤ × ℤ) × ℕ)} (hsupp : suppInP P FW = true)
    {v : ℤ} (hv : P.contains v = false) :
    vertexLoad FW v = 0 := by
  induction FW with
  | nil => simp [vertexLoad]
  | cons p rest ih =>
    have hsupp' : suppInP P rest = true := by
      have := (List.all_eq_true.1 hsupp)
      apply List.all_eq_true.2
      intro q hq; exact this q (by simp [hq])
    have hpsupp : (P.contains p.1.1 && P.contains p.1.2.1 && P.contains p.1.2.2) = true := by
      have := (List.all_eq_true.1 hsupp) p (by simp)
      simpa using this
    have hmem_false : memTriple v p.1 = false := by
      simp only [Bool.and_eq_true] at hpsupp
      -- each vertex of `p` is in `P`, but `v ∉ P`, so `v` is none of them
      have ha : P.contains p.1.1 = true := hpsupp.1.1
      have hb : P.contains p.1.2.1 = true := hpsupp.1.2
      have hc : P.contains p.1.2.2 = true := hpsupp.2
      unfold memTriple
      have hva : (v == p.1.1) = false := by
        by_contra hh
        simp only [Bool.not_eq_false, beq_iff_eq] at hh
        rw [hh] at hv; rw [hv] at ha; exact absurd ha (by simp)
      have hvb : (v == p.1.2.1) = false := by
        by_contra hh
        simp only [Bool.not_eq_false, beq_iff_eq] at hh
        rw [hh] at hv; rw [hv] at hb; exact absurd hb (by simp)
      have hvc : (v == p.1.2.2) = false := by
        by_contra hh
        simp only [Bool.not_eq_false, beq_iff_eq] at hh
        rw [hh] at hv; rw [hv] at hc; exact absurd hc (by simp)
      rw [hva, hvb, hvc]; rfl
    unfold vertexLoad
    simp only [hmem_false, Bool.false_eq_true, if_false, Nat.zero_add]
    exact ih hsupp'

/-- `loadSum H FW = loadSum (H ∩ P) FW` when `suppInP P FW`: the off-`P` vertices contribute 0.
We phrase `H ∩ P` as `H.filter (P.contains ·)`. -/
theorem loadSum_filterP
    {P : List ℤ} {FW : List ((ℤ × ℤ × ℤ) × ℕ)} (hsupp : suppInP P FW = true)
    (H : List ℤ) :
    loadSum H FW = loadSum (H.filter (fun x => P.contains x)) FW := by
  unfold loadSum
  induction H with
  | nil => simp
  | cons h rest ih =>
    by_cases hh : P.contains h = true
    · rw [List.filter_cons_of_pos (by simpa using hh)]
      simp only [List.map_cons, List.sum_cons]
      rw [ih]
    · have hhf : P.contains h = false := by simpa using hh
      rw [List.filter_cons_of_neg (by rw [hhf]; decide)]
      simp only [List.map_cons, List.sum_cons]
      rw [vertexLoad_zero_of_notInP hsupp hhf, Nat.zero_add]
      exact ih

/-- **Fractional half.**  If `H` hits `FW_frac`, whose support lies in `P`, and every vertex
of `A` carries load `≤ D`, then `totalW FW_frac ≤ D · |H ∩ P|`, hence (with the threshold)
`a ≤ |H ∩ P|`. -/
theorem frac_lb_on_P
    {A P : List ℤ} {FW : List ((ℤ × ℤ × ℤ) × ℕ)} {D a : ℕ}
    (hD : 0 < D)
    (hsupp : suppInP P FW = true)
    (hload : loadOK A FW D = true)
    (hHsub : ∀ v ∈ H, v ∈ A)
    (hhits : hitsAll H FW)
    (hTa : D * a ≤ totalW FW) :
    a ≤ (H.filter (fun x => P.contains x)).length := by
  -- double counting on `H`, then concentrate on `H ∩ P`.
  have hdc : totalW FW ≤ loadSum H FW := totalW_le_loadSum H FW hhits
  rw [loadSum_filterP hsupp H] at hdc
  -- every vertex of the filtered list is in `A`, so carries load ≤ D
  set HP := H.filter (fun x => P.contains x) with hHPdef
  have hHPload : ∀ v ∈ HP, vertexLoad FW v ≤ D := by
    intro v hv
    rw [hHPdef, List.mem_filter] at hv
    have hvA : v ∈ A := hHsub v hv.1
    have := (List.all_eq_true.1 hload) v hvA
    simpa using this
  have hloadD : loadSum HP FW ≤ D * HP.length := loadSum_le HP FW D hHPload
  -- `D*a ≤ totalW ≤ D*|HP|` ⇒ `a ≤ |HP|` (since `0 < D`).
  have hTle : D * a ≤ D * HP.length := le_trans hTa (le_trans hdc hloadD)
  exact Nat.le_of_mul_le_mul_left hTle hD

/-! ## The residual half : `g < |H \ P|`

The residual family's edges avoid `P`, so for each residual edge a hitting witness in `H` is
`∉ P`; hence `H` restricted to `¬P` (i.e. `H \ P`) still hits the whole residual family.
`noTransLe_sound` then forces `g < |H \ P|`. -/

/-- `H.filter (¬ P.contains ·)` (= `H \ P`) hits every residual edge, when those edges avoid
`P` and `H` hits them. -/
theorem res_hitsAll_filter
    {P : List ℤ} {FW : List ((ℤ × ℤ × ℤ) × ℕ)}
    (hres : resAvoidsP P FW = true)
    {H : List ℤ} (hhits : hitsAll H FW) :
    hitsAll (H.filter (fun x => !P.contains x)) FW := by
  intro p hp
  obtain ⟨w, hwH, hwp⟩ := hhits p hp
  -- the edge `p` avoids `P`, so its witness `w` (a vertex of `p`) is `∉ P`.
  have hpAvoid : edgeAvoidsP P p.1 = true := by
    have := (List.all_eq_true.1 hres) p hp
    simpa using this
  have hwnotP : P.contains w = false := by
    unfold edgeAvoidsP at hpAvoid
    simp only [Bool.and_eq_true, Bool.not_eq_eq_eq_not, Bool.not_true] at hpAvoid
    -- each of the three vertices of `p` is not in `P`.
    obtain ⟨⟨ha, hb⟩, hc⟩ := hpAvoid
    -- `w` is one of the three vertices of `p`.
    have hw3 : w = p.1.1 ∨ w = p.1.2.1 ∨ w = p.1.2.2 := by
      unfold memTriple at hwp
      simp only [Bool.or_eq_true, beq_iff_eq] at hwp
      tauto
    rcases hw3 with h | h | h
    · rw [h]; exact ha
    · rw [h]; exact hb
    · rw [h]; exact hc
  refine ⟨w, ?_, hwp⟩
  rw [List.mem_filter]
  refine ⟨hwH, ?_⟩
  simp only [Bool.not_eq_true']
  rw [hwnotP]

/-! ## The interleaved soundness lemma -/

/-- **Interleaved transversal soundness lemma (fix-then-branch).**

Given a point list `A` (`Nodup`), a support list `P`, a **fractional** certificate `FW_frac`
with

* `hsupp  : suppInP P FW_frac = true` — its support lies in `P`,
* `hload  : loadOK A FW_frac D = true` — every point of `A` carries load `≤ D`,
* `hTa    : D * (a - 1) < totalW FW_frac` — the fractional value is `≥ a` (an integer lower
  bound on the number of `P`-vertices any transversal must use),

and a **residual** branching certificate `FW_res` with

* `hres   : resAvoidsP P FW_res = true` — every residual edge avoids `P`,
* `hbranch: noTransLe FW_res g = true` — `τ(FW_res) > g`,

every sublist `S ⊆ A` (`Nodup`) that **avoids both** listed families has
`S.length ≤ A.length − a − g − 1`.

In the intended application both families are sub-families of the full 3-AP family of `A`, so
a genuinely no-3-AP (Sidon, [MT26] Lemma 2.3) subset avoids them all; hence
`h(A) ≤ N − a − g − 1` with branch budget only `g` (the residual gap), not the full `τ`. -/
theorem hLe_of_interleaved
    {A P : List ℤ}
    {FW_frac FW_res : List ((ℤ × ℤ × ℤ) × ℕ)}
    {D a g : ℕ}
    (hA : A.Nodup)
    (hD : 0 < D)
    (hedges_f : edgesOK A FW_frac = true)
    (hsupp : suppInP P FW_frac = true)
    (hload : loadOK A FW_frac D = true)
    (hTa : D * a ≤ totalW FW_frac)
    (hedges_r : edgesOK A FW_res = true)
    (hres : resAvoidsP P FW_res = true)
    (hbranch : noTransLe FW_res g = true)
    {S : List ℤ} (hS : S.Nodup) (hSsub : S ⊆ A)
    (hSavoid_f : avoidsAll S FW_frac = true)
    (hSavoid_r : avoidsAll S FW_res = true) :
    S.length ≤ A.length - a - g - 1 := by
  -- The complement `H = A \ S`.
  set H : List ℤ := A.filter (fun x => !S.contains x) with hHdef
  have hHmem : ∀ x, x ∈ H ↔ (x ∈ A ∧ x ∉ S) := by
    intro x; rw [hHdef, List.mem_filter]; simp [List.contains_eq_mem]
  have hHnodup : H.Nodup := hA.filter _
  have hHsubA : ∀ v ∈ H, v ∈ A := fun v hv => ((hHmem v).1 hv).1
  -- `H` hits any sub-family `FW` of genuine APs in `A` that `S` avoids (same construction as
  -- in the fractional / branching lemmas).
  have hits_of : ∀ FW : List ((ℤ × ℤ × ℤ) × ℕ),
      edgesOK A FW = true → avoidsAll S FW = true → hitsAll H FW := by
    intro FW hedges havoid p hp
    have hpOK : (isAP p.1 && tripleInA A p.1) = true := by
      have := (List.all_eq_true.1 hedges) p hp; simpa using this
    have htriA : tripleInA A p.1 = true := (Bool.and_eq_true _ _ ▸ hpOK).2
    obtain ⟨hAa, hAb, hAc⟩ := tripleInA_mem htriA
    have hcons : p.1.1 ∉ S ∨ p.1.2.1 ∉ S ∨ p.1.2.2 ∉ S := by
      have h0 := (List.all_eq_true.1 havoid) p hp
      simp only [Bool.not_eq_true', containsTriple, Bool.and_eq_false_iff,
        List.contains_eq_mem, decide_eq_false_iff_not] at h0
      tauto
    rcases hcons with h | h | h
    · exact ⟨p.1.1, (hHmem _).2 ⟨hAa, h⟩, by unfold memTriple; simp⟩
    · exact ⟨p.1.2.1, (hHmem _).2 ⟨hAb, h⟩, by unfold memTriple; simp⟩
    · exact ⟨p.1.2.2, (hHmem _).2 ⟨hAc, h⟩, by unfold memTriple; simp⟩
  have hhits_f : hitsAll H FW_frac := hits_of FW_frac hedges_f hSavoid_f
  have hhits_r : hitsAll H FW_res := hits_of FW_res hedges_r hSavoid_r
  -- Fractional half:  `a ≤ |H ∩ P|`.
  have hfrac : a ≤ (H.filter (fun x => P.contains x)).length :=
    frac_lb_on_P (A := A) hD hsupp hload hHsubA hhits_f hTa
  -- Residual half:  `g < |H \ P|`.
  have hHresHits : hitsAll (H.filter (fun x => !P.contains x)) FW_res :=
    res_hitsAll_filter hres hhits_r
  have hHresNodup : (H.filter (fun x => !P.contains x)).Nodup := hHnodup.filter _
  have hbr : g < (H.filter (fun x => !P.contains x)).length :=
    noTransLe_sound g FW_res _ hHresNodup hbranch hHresHits
  -- The two filtered parts partition `H`:  `|H ∩ P| + |H \ P| = |H|`.
  have hpart : (H.filter (fun x => P.contains x)).length
      + (H.filter (fun x => !P.contains x)).length = H.length := by
    have := List.length_eq_length_filter_add (l := H) (fun x => P.contains x)
    -- `H.length = |filter P| + |filter ¬P|`
    simpa [Nat.add_comm] using this.symm
  -- Hence `|H| ≥ a + (g+1)`.
  have hHlen : a + g + 1 ≤ H.length := by omega
  -- Cardinality split `|S| + |H| = |A|` (identical construction to the other lemmas).
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
    rw [hHdef]; omega
  -- conclude: `|S| = N − |H| ≤ N − (a+g+1) = N − a − g − 1`.
  omega

/-! ## Validation 1 — synthetic instance (the budget-shrink mechanism fires)

`A_syn` has four vertex-disjoint 3-APs: two charged fractionally (`a = 2`, `D = 1`, each edge
weight 1) and two left in the residual (branch budget `g = 1`, `3^1 = 3` leaves).  The combined
transversal number is `τ = 4`; the interleaved cert certifies it branching **only** `g = 1`,
the fractional cert carrying the other `2`.  This is the budget-shrink that the `max`-hybrid
could not do (it would have needed the full branch budget `3`). -/

namespace SynValidation

/-- Twelve distinct integers forming four vertex-disjoint 3-APs. -/
def Asyn : List ℤ := [0, 1, 2, 10, 11, 12, 100, 101, 102, 200, 201, 202]

/-- Support `P` of the fractional part : the two APs `(100,101,102)`, `(200,201,202)`. -/
def Psyn : List ℤ := [100, 101, 102, 200, 201, 202]

/-- Fractional family : two disjoint APs, each weight 1 (so `ν* = 2`, `totalW = 2`, `D = 1`). -/
def FWfrac_syn : List ((ℤ × ℤ × ℤ) × ℕ) :=
  [ ((100, 101, 102), 1), ((200, 201, 202), 1) ]

/-- Residual family : two disjoint APs avoiding `P`. -/
def FWres_syn : List ((ℤ × ℤ × ℤ) × ℕ) :=
  [ ((0, 1, 2), 0), ((10, 11, 12), 0) ]

theorem Asyn_nodup : Asyn.Nodup := by decide
theorem Asyn_length : Asyn.length = 12 := by decide
theorem FWfrac_edgesOK : edgesOK Asyn FWfrac_syn = true := by decide
theorem FWfrac_suppInP : suppInP Psyn FWfrac_syn = true := by decide
theorem FWfrac_loadOK : loadOK Asyn FWfrac_syn 1 = true := by decide
theorem FWfrac_total : totalW FWfrac_syn = 2 := by decide
theorem FWres_edgesOK : edgesOK Asyn FWres_syn = true := by decide
theorem FWres_avoidsP : resAvoidsP Psyn FWres_syn = true := by decide
/-- Residual branch certificate : `τ(FWres) > 1`, certified with budget `g = 1` (3 leaves). -/
theorem FWres_branch : noTransLe FWres_syn 1 = true := by decide

/-- **Synthetic validation (the mechanism fires).**  Via the interleaved lemma, with
fractional value `a = 2` and residual branch budget `g = 1`, every sublist of `A_syn` avoiding
both families has length `≤ 12 − 2 − 1 − 1 = 8`, i.e. `τ ≥ 4`.  The fractional cert supplied
`2` of the `4`, the branch supplied the rest with budget only `g = 1`. -/
theorem Asyn_avoiders_le_8
    {S : List ℤ} (hS : S.Nodup) (hSsub : S ⊆ Asyn)
    (hSavoid_f : avoidsAll S FWfrac_syn = true)
    (hSavoid_r : avoidsAll S FWres_syn = true) :
    S.length ≤ 8 := by
  have hTa : (1 : ℕ) * 2 ≤ totalW FWfrac_syn := by rw [FWfrac_total]
  have h := hLe_of_interleaved (A := Asyn) (P := Psyn)
    (FW_frac := FWfrac_syn) (FW_res := FWres_syn) (D := 1) (a := 2) (g := 1)
    Asyn_nodup (by decide) FWfrac_edgesOK FWfrac_suppInP FWfrac_loadOK hTa
    FWres_edgesOK FWres_avoidsP FWres_branch hS hSsub hSavoid_f hSavoid_r
  -- `12 - 2 - 1 - 1 = 8`
  rw [Asyn_length] at h
  simpa using h

end SynValidation

/-! ## Validation 2 — `A_base` (degenerate `P = ∅`, sound but no budget shrink)

`A_base` is a fully half-integral instance (see the module docstring and
`certificate/interleaved/check_interleaved_cert.py`): no choice of support `P` beats the pure
branch budget.  We validate `hLe_of_interleaved` in the **degenerate** form `P = ∅`
(`a = 0`, `g = 5`), confirming it soundly re-derives the tight `h(A_base) ≤ 8`.  With `P = ∅`
the fractional half is vacuous (`a = 0`) and the residual is the full AP family, so the budget
is the full `g = 5` — i.e. the interleaved cert never claims more than the truth, even when its
budget-shrink does not apply. -/

namespace BaseValidation

open C5bTransversal.Validation C5bBranch.Validation

/-- Empty support : `P = ∅`, so the residual is the full AP family and `a = 0`. -/
def Pempty : List ℤ := []

/-- With `P = ∅`, the empty fractional family trivially has its (empty) support in `P`. -/
def FWfrac_base : List ((ℤ × ℤ × ℤ) × ℕ) := []

theorem FWfrac_base_edgesOK : edgesOK C5bTransversal.Validation.Abase FWfrac_base = true := by
  decide
theorem FWfrac_base_suppInP : suppInP Pempty FWfrac_base = true := by decide
theorem FWfrac_base_loadOK : loadOK C5bTransversal.Validation.Abase FWfrac_base 1 = true := by
  decide
theorem FWfrac_base_total : totalW FWfrac_base = 0 := by decide
/-- With `P = ∅`, every edge avoids `P`, so the full AP family is a valid residual. -/
theorem Abase_APs_resAvoidsP : resAvoidsP Pempty Abase_APs = true := by decide
/-- `Abase_APs` is a genuine AP family inside `Abase` (re-export defeq to `C5bTransversal`'s). -/
theorem Abase_APs_edgesOK' : edgesOK C5bTransversal.Validation.Abase Abase_APs = true :=
  C5bBranch.Validation.Abase_APs_edgesOK

/-- **`A_base` validation (degenerate, sound).**  With `P = ∅` (`a = 0`) and the full residual
family branched at budget `g = 5`, the interleaved lemma re-derives every sublist of `A_base`
avoiding the family has length `≤ 14 − 0 − 5 − 1 = 8`.  This confirms `hLe_of_interleaved` is
sound; the budget here is the full `5` because `A_base` is half-integral (no shrink possible). -/
theorem Abase_avoiders_le_8_interleaved
    {S : List ℤ} (hS : S.Nodup) (hSsub : S ⊆ C5bTransversal.Validation.Abase)
    (hSavoid_r : avoidsAll S Abase_APs = true) :
    S.length ≤ 8 := by
  have hTa : (1 : ℕ) * 0 ≤ totalW FWfrac_base := by rw [FWfrac_base_total]
  -- `S` trivially avoids the empty fractional family.
  have hSavoid_f : avoidsAll S FWfrac_base = true := by
    unfold FWfrac_base avoidsAll; rfl
  have h := hLe_of_interleaved
    (A := C5bTransversal.Validation.Abase) (P := Pempty)
    (FW_frac := FWfrac_base) (FW_res := Abase_APs) (D := 1) (a := 0) (g := 5)
    C5bTransversal.Validation.Abase_nodup (by decide)
    FWfrac_base_edgesOK FWfrac_base_suppInP FWfrac_base_loadOK hTa
    Abase_APs_edgesOK' Abase_APs_resAvoidsP Abase_branch_tau
    hS hSsub hSavoid_f hSavoid_r
  -- `14 - 0 - 5 - 1 = 8`
  rw [C5bTransversal.Validation.Abase_length] at h
  simpa using h

end BaseValidation

end C5bInterleaved
