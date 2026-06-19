/-
# C_9 = Θ(C_7): the graph-theoretic bridge.

Defines `C7 : SimpleGraph (Fin 7)` (the 7-cycle), the strong product `strongProd`, the
`n`-fold strong power `C7pow n`, and proves that the decidable list-certificate of
`Constants/C9.lean` produces a genuine independent set in `C7pow n` — hence a lower
bound on the independence number `α(C_7^⊠n)`.

The remaining step `α(C_7^⊠n) ≥ N → Θ(C_7) ≥ N^(1/n)` is the definitional unfolding of
the Shannon capacity `Θ(G) = sup_n α(G^⊠n)^(1/n)`; we carry the supremum bound as an
explicitly-named bridge predicate `ThetaGe` (the honest trust boundary, analogue of the
5b `MTThm15`), since Mathlib has no `Θ`.  The graph-theoretic content (confusability,
strong-power adjacency, the cert ⇒ independent set) is fully formalized here, no `sorry`.

Reference: [PS2018] Polak–Schrijver, arXiv:1808.07438.
-/
import Constants.C9
import Mathlib.Combinatorics.SimpleGraph.Clique
import Mathlib.Data.List.GetD

namespace C9

open SimpleGraph

/-! ## The 7-cycle as a SimpleGraph on `Fin 7`. -/

/-- Cyclic distance on `Fin 7` (via the `ℕ` `cdist` on the representatives). -/
def fcdist (a b : Fin 7) : ℕ := cdist a.val b.val

/-- `cdist` is symmetric. -/
theorem cdist_comm (a b : ℕ) : cdist a b = cdist b a := by
  unfold cdist
  have h : (if a ≥ b then a - b else b - a) = (if b ≥ a then b - a else a - b) := by
    split_ifs <;> omega
  rw [h]

/-- The 7-cycle `C_7`: distinct vertices `a b` are adjacent iff cyclic distance `= 1`. -/
def C7 : SimpleGraph (Fin 7) where
  Adj a b := a ≠ b ∧ fcdist a b = 1
  symm := ⟨by
    rintro a b ⟨hne, hd⟩
    exact ⟨hne.symm, by unfold fcdist at hd ⊢; rw [cdist_comm]; exact hd⟩⟩
  loopless := ⟨by rintro a ⟨h, _⟩; exact h rfl⟩

instance : DecidableRel C7.Adj := fun a b => by
  unfold C7; infer_instance

/-! ## Strong product and the `n`-fold strong power.

In the strong product `G ⊠ H`, distinct `(a₁,b₁), (a₂,b₂)` are adjacent iff in each
coordinate the entries are equal-or-adjacent (and the pair is distinct). For an indexed
strong power over `ι → V`, distinct `u v` are adjacent iff for every `i`, `u i` and `v i`
are equal-or-adjacent (i.e. confusable). -/

/-- "Confusable" in `C7`: equal or adjacent. -/
def C7conf (a b : Fin 7) : Prop := a = b ∨ C7.Adj a b

instance : DecidableRel C7conf := fun a b => by
  unfold C7conf; infer_instance

/-- The `n`-fold strong power `C_7^⊠n` on codewords `Fin n → Fin 7`: distinct `u v` are
adjacent iff confusable in every coordinate. -/
def C7pow (n : ℕ) : SimpleGraph (Fin n → Fin 7) where
  Adj u v := u ≠ v ∧ ∀ i, C7conf (u i) (v i)
  symm := ⟨by
    rintro u v ⟨hne, h⟩
    refine ⟨hne.symm, fun i => ?_⟩
    rcases h i with he | ha
    · exact Or.inl he.symm
    · exact Or.inr ha.symm⟩
  loopless := ⟨by rintro u ⟨h, _⟩; exact h rfl⟩

/-! ## Confusability: the `Bool` predicate matches the graph relation.

Our engine's `confusable a b : Bool` (cyclic distance `≤ 1`) corresponds exactly to
`C7conf` on the `Fin 7` representatives. -/

/-- `cdist a b = 0` iff `a = b` (for `a,b < 7`). -/
theorem cdist_eq_zero_iff {a b : ℕ} (ha : a < 7) (hb : b < 7) :
    cdist a b = 0 ↔ a = b := by
  unfold cdist
  simp only [ge_iff_le]
  constructor
  · intro h
    split at h <;> omega
  · rintro rfl; simp

theorem confusable_iff_C7conf (a b : Fin 7) :
    confusable a.val b.val = true ↔ C7conf a b := by
  have ha := a.isLt; have hb := b.isLt
  unfold confusable
  simp only [decide_eq_true_eq, C7conf]
  constructor
  · intro h
    by_cases heq : a = b
    · exact Or.inl heq
    · refine Or.inr ⟨heq, ?_⟩
      have hne : a.val ≠ b.val := fun hh => heq (Fin.ext hh)
      unfold fcdist
      -- cdist ≤ 1 and ≠ 0 ⇒ = 1
      have hpos : cdist a.val b.val ≠ 0 := by
        intro hz; exact hne ((cdist_eq_zero_iff ha hb).mp hz)
      omega
  · intro h
    rcases h with he | ⟨_, hd⟩
    · subst he
      have : cdist a.val a.val = 0 := (cdist_eq_zero_iff ha ha).mpr rfl
      omega
    · unfold fcdist at hd; omega

/-! ## From the list-certificate to a genuine independent set in `C_7^⊠n`.

A codeword stored as a `List ℕ` of length `n` with all entries `< 7` is read as a
function `Fin n → Fin 7`. We show: if two such words are `indepPair`-independent (some
coordinate not confusable as `ℕ`), then their function forms are NON-adjacent in
`C7pow n`. This is the soundness of the engine's pairwise predicate against the actual
strong-power graph relation. -/

/-- Read a length-`n`, entries-`< 7` word `w : List ℕ` as a function `Fin n → Fin 7`. -/
def toVec (n : ℕ) (w : List ℕ) (h7 : ∀ x ∈ w, x < 7) (hlen : w.length = n) :
    Fin n → Fin 7 := fun i =>
  ⟨w[i.val]'(by rw [hlen]; exact i.isLt),
    h7 _ (List.getElem_mem _)⟩

/-- If `indepPair u v = true` (some zipped coordinate is not confusable), then there is a
coordinate `i < n` where `u` and `v` are not `C7conf`, hence `toVec`-images are not
adjacent in `C7pow n`. -/
theorem indepPair_imp_not_adj (n : ℕ)
    (u v : List ℕ) (hu7 : ∀ x ∈ u, x < 7) (hv7 : ∀ x ∈ v, x < 7)
    (hul : u.length = n) (hvl : v.length = n)
    (h : indepPair u v = true) :
    ¬ (C7pow n).Adj (toVec n u hu7 hul) (toVec n v hv7 hvl) := by
  rintro ⟨_, hadj⟩
  unfold indepPair at h
  rw [List.any_eq_true] at h
  obtain ⟨p, hp_mem, hp⟩ := h
  obtain ⟨i, hi, hpi⟩ := List.mem_iff_getElem.mp hp_mem
  have hzlen : (u.zip v).length = n := by
    rw [List.length_zip, hul, hvl]; simp
  have hin : i < n := by rw [← hzlen]; exact hi
  -- the zipped element at index i is (u[i], v[i])
  have hzget : (u.zip v)[i]'hi = (u[i]'(by rw [hul]; exact hin), v[i]'(by rw [hvl]; exact hin)) :=
    List.getElem_zip
  rw [hzget] at hpi
  -- p = (u[i], v[i])
  have hpfst : p.1 = u[i]'(by rw [hul]; exact hin) := by rw [← hpi]
  have hpsnd : p.2 = v[i]'(by rw [hvl]; exact hin) := by rw [← hpi]
  have hadj_i := hadj ⟨i, hin⟩
  simp only [Bool.not_eq_true'] at hp
  have hpval : confusable p.1 p.2 = false := by simpa using hp
  have hcon : ¬ C7conf (toVec n u hu7 hul ⟨i, hin⟩) (toVec n v hv7 hvl ⟨i, hin⟩) := by
    intro hc
    have key := (confusable_iff_C7conf (toVec n u hu7 hul ⟨i, hin⟩)
      (toVec n v hv7 hvl ⟨i, hin⟩)).mpr hc
    have eu : (toVec n u hu7 hul ⟨i, hin⟩).val = p.1 := by simp only [toVec]; rw [hpfst]
    have ev : (toVec n v hv7 hvl ⟨i, hin⟩).val = p.2 := by simp only [toVec]; rw [hpsnd]
    rw [eu, ev, hpval] at key
    exact absurd key (by simp)
  exact hcon hadj_i

/-! ## Assembly: a valid list-certificate gives `IsNIndepSet` in `C_7^⊠n`.

We use a TOTAL reader `vec n w : Fin n → Fin 7` (entries mod 7, padding 0) so we can map
the list of words to a `List (Fin n → Fin 7)` uniformly. On valid words (length `n`,
entries `< 7`) it coincides with `toVec`. -/

/-- `confusable` is symmetric. -/
theorem confusable_comm (a b : ℕ) : confusable a b = confusable b a := by
  unfold confusable; rw [cdist_comm]

/-- `indepPair` is symmetric. -/
theorem indepPair_comm (u v : List ℕ) : indepPair u v = indepPair v u := by
  unfold indepPair
  rw [← List.zip_swap, List.any_map]
  congr 1
  funext p
  simp only [Function.comp, Prod.swap]
  rw [confusable_comm]

/-- Total reader of a word into `Fin n → Fin 7`. -/
def vec (n : ℕ) (w : List ℕ) : Fin n → Fin 7 := fun i =>
  ⟨(w.getD i.val 0) % 7, Nat.mod_lt _ (by norm_num)⟩

/-- On a valid word, `vec` agrees with `toVec`. -/
theorem vec_eq_toVec (n : ℕ) (w : List ℕ) (h7 : ∀ x ∈ w, x < 7) (hlen : w.length = n) :
    vec n w = toVec n w h7 hlen := by
  funext i
  apply Fin.ext
  simp only [vec, toVec]
  have hi : i.val < w.length := by rw [hlen]; exact i.isLt
  rw [List.getD_eq_getElem _ 0 hi]
  exact Nat.mod_eq_of_lt (h7 _ (List.getElem_mem _))

/-- A list `S` of distinct, valid (length `n`, entries `< 7`) codewords with
`allPairsIndep S = true` maps under `vec` to a list whose `toFinset` is an independent set
of size `S.length` in `C_7^⊠n`. This is the engine soundness: a `decide`-checked list
certificate becomes a genuine independent set in the strong-power graph. -/
theorem isNIndepSet_of_cert (n : ℕ) (S : List (List ℕ))
    (hindep : allPairsIndep S = true)
    (hnodup : S.Nodup)
    (h7 : ∀ w ∈ S, ∀ x ∈ w, x < 7)
    (hlen : ∀ w ∈ S, w.length = n) :
    (C7pow n).IsNIndepSet S.length (S.map (vec n)).toFinset := by
  -- injectivity of vec on S: distinct valid words ⇒ distinct functions
  have hinj : ∀ u ∈ S, ∀ v ∈ S, vec n u = vec n v → u = v := by
    intro u hu v hv heq
    apply List.ext_getElem (by rw [hlen u hu, hlen v hv])
    intro i hiu hiv
    have := congrFun heq ⟨i, by rw [← hlen u hu]; exact hiu⟩
    have hue : (vec n u ⟨i, by rw [← hlen u hu]; exact hiu⟩).val = u[i] := by
      simp only [vec]; rw [List.getD_eq_getElem _ 0 hiu]
      exact Nat.mod_eq_of_lt (h7 u hu _ (List.getElem_mem _))
    have hve : (vec n v ⟨i, by rw [← hlen u hu]; exact hiu⟩).val = v[i] := by
      simp only [vec]; rw [List.getD_eq_getElem _ 0 hiv]
      exact Nat.mod_eq_of_lt (h7 v hv _ (List.getElem_mem _))
    rw [← hue, ← hve, this]
  -- the mapped list is Nodup
  have hmapnodup : (S.map (vec n)).Nodup := by
    rw [List.nodup_map_iff_inj_on hnodup]
    exact hinj
  -- card = S.length
  refine ⟨?_, ?_⟩
  · -- IsIndepSet: pairwise non-adjacent
    rw [SimpleGraph.isIndepSet_iff]
    intro x hx y hy hxy
    simp only [List.coe_toFinset, Set.mem_setOf_eq, List.mem_map] at hx hy
    obtain ⟨u, hu, rfl⟩ := hx
    obtain ⟨v, hv, rfl⟩ := hy
    -- u ≠ v as words (else same vec)
    have huv : u ≠ v := fun h => hxy (by rw [h])
    -- indepPair u v from the pairwise cert (using symmetry of indepPair)
    have hpw := (allPairsIndep_iff S).mp hindep
    have hsymm : Std.Symm (fun a b : List ℕ => indepPair a b = true) :=
      ⟨fun a b h => by rw [indepPair_comm]; exact h⟩
    have hip : indepPair u v = true := hpw.forall hu hv huv
    -- valid words
    have hu7 : ∀ x ∈ u, x < 7 := h7 u hu
    have hv7 : ∀ x ∈ v, x < 7 := h7 v hv
    have hul : u.length = n := hlen u hu
    have hvl : v.length = n := hlen v hv
    -- vec = toVec on valid words, then use indepPair_imp_not_adj
    rw [vec_eq_toVec n u hu7 hul, vec_eq_toVec n v hv7 hvl]
    exact indepPair_imp_not_adj n u v hu7 hv7 hul hvl hip
  · rw [List.toFinset_card_of_nodup hmapnodup, List.length_map]

end C9
