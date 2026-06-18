import Mathlib
import Constants.C5b
import Constants.C5bCap
import Constants.C5bCombos
import Constants.C5bBridgePerm

/-!
# C_5b : the decidable bridge — unconditional assembly + the `Abase` cap corollary

This file is the **close-out** of the multi-round thread that wires the R8 structural cap
lemma (`C5bCap.m_le_n_sub_2`, stated over the abstract `Is45 : Finset ℤ → Prop`) into the
concrete engine predicate `C5b.is45setB` (`lean/Constants/C5b.lean`).

The two halves were built and verified separately in earlier rounds:

* **perm-invariance half** (`Constants/C5bBridgePerm.lean`):
  `C5bBridgePerm.is45setB_to_Is45 : CombosComplete l → is45setB l = true → Is45 l.toFinset`,
  i.e. the bridge **modulo** a single named hypothesis `CombosComplete l`.
* **combos-completeness half** (`Constants/C5bCombos.lean`):
  `C5bCombos.combos_complete : l.Nodup → … → ∃ t ∈ combos l 4, t ~ [a,b,c,d]`,
  the existential that `CombosComplete l` packages.

This file does the (trivial, load-bearing-free) assembly:

1. `CombosComplete_of_Nodup : l.Nodup → CombosComplete l` — discharges the named hypothesis
   of the perm half by feeding it `combos_complete`, converting each `· ∈ l.toFinset` to
   `· ∈ l` via `List.mem_toFinset` (the only non-trivial line, a single Mathlib lemma).
2. `is45setB_to_Is45 : is45setB l = true → l.Nodup → Is45 l.toFinset` — the **unconditional**
   bridge, with no remaining named hypothesis.
3. `Abase_Is45 : Is45 Abase.toFinset` and `Abase_threeAPs_card_le_12 :
   (threeAPs Abase.toFinset).card ≤ 12` — fire the cap lemma `C5bCap.m_le_n_sub_2` on the
   concrete engine gadget `Abase` (the genuine record 14-point (4,5)-set), instantiating the
   abstract `m ≤ n − 2` at `n = |Abase.toFinset| = 14` to the concrete `m ≤ 12`.

No `sorry`, no `native_decide`, no new axiom: every step is either a compiled theorem from an
earlier round or a single Mathlib rewrite.  `#print axioms` on the new top-level lemmas shows
only `propext` / `Classical.choice` / `Quot.sound`.

This does **not** move the bound (the run's record stays the verified upper `4/7` of [MT26]);
it is a verified machinery close-out that hardens the cap lemma's wiring into the engine.
-/

namespace C5bBridge

open C5b C5bCap C5bCombos C5bBridgePerm

/-- **Discharging the `CombosComplete` obligation.**  For a `Nodup` list `l`, the named
hypothesis `CombosComplete l` of the perm-invariance half holds: it is exactly the
existential produced by `C5bCombos.combos_complete`, after converting each membership
`· ∈ l.toFinset` to `· ∈ l` via `List.mem_toFinset`. -/
theorem CombosComplete_of_Nodup {l : List ℤ} (hl : l.Nodup) : CombosComplete l := by
  intro a b c d ha hb hc hd hab hac had hbc hbd hcd
  rw [List.mem_toFinset] at ha hb hc hd
  exact combos_complete hl ha hb hc hd hab hac had hbc hbd hcd

/-- **The unconditional decidable bridge.**  For a `Nodup` list `l`, the concrete engine check
`is45setB l = true` implies the set-level (4,5)-property `Is45 l.toFinset` that the cap lemma
`C5bCap.m_le_n_sub_2` consumes — with **no** remaining named hypothesis.

This is the assembly of the two verified halves: `CombosComplete_of_Nodup` discharges the
single trust boundary of `C5bBridgePerm.is45setB_to_Is45`. -/
theorem is45setB_to_Is45 {l : List ℤ} (h45 : is45setB l = true) (hl : l.Nodup) :
    Is45 l.toFinset :=
  C5bBridgePerm.is45setB_to_Is45 (CombosComplete_of_Nodup hl) h45

/-! ### The `Abase` cap corollary — firing `m_le_n_sub_2` on the concrete engine gadget. -/

/-- `Abase.toFinset` has exactly **14** elements (`Abase` is `Nodup` of length 14). -/
theorem Abase_toFinset_card : Abase.toFinset.card = 14 := by
  rw [List.toFinset_card_of_nodup Abase_nodup, Abase_length]

/-- **The concrete (4,5)-property of `Abase`.**  The record 14-point gadget `Abase` is a
genuine (4,5)-set at the set level: feeding the verified engine facts `Abase_is45set`
(`is45setB Abase = true`, R3 kernel `decide`) and `Abase_nodup` through the unconditional
bridge yields `Is45 Abase.toFinset`. -/
theorem Abase_Is45 : Is45 Abase.toFinset :=
  is45setB_to_Is45 Abase_is45set Abase_nodup

/-- **The cap lemma on the concrete engine gadget.**  Firing `C5bCap.m_le_n_sub_2` on
`Abase.toFinset` (a (4,5)-set of size `14 ≥ 2`) bounds the number of midpoint-distinct 3-APs:

`m = |threeAPs Abase.toFinset| ≤ n − 2 = 14 − 2 = 12`.

This is the concrete instantiation of the abstract `m ≤ n − 2` cap (R8 `C5bCap.m_le_n_sub_2`)
on the engine's record gadget — the close-out of the cap-lemma → concrete-engine wiring. -/
theorem Abase_threeAPs_card_le_12 : (threeAPs Abase.toFinset).card ≤ 12 := by
  have h := C5bCap.m_le_n_sub_2 Abase_Is45 (by rw [Abase_toFinset_card]; norm_num)
  rwa [Abase_toFinset_card] at h

end C5bBridge
