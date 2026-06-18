# Certificate — decidable-bridge-is45-full (R10)

The **unconditional** decidable bridge `is45setB l = true → l.Nodup → Is45 l.toFinset` plus
the concrete `Abase` cap corollary, closing out the cap-lemma → concrete-engine wiring thread.

This does **NOT** move the bound (record stays verified upper `4/7` of [MT26]); it is a
verified Lean-machinery close-out.

## File

`lean/Constants/C5bBridge.lean` (auto-included by the `Constants.+` lib glob in
`lean/lakefile.toml`; no lakefile edit needed).

## Build target + result

```
cd lean
lake build Constants.C5bBridge      # ✔ Built Constants.C5bBridge
lake build                          # ✔ Build completed successfully (8570 jobs).
```

Mathlib pinned at v4.31.0 (lean/lake-manifest.json), Lean toolchain v4.31.0.

## New top-level theorems (file/line)

- `C5bBridge.CombosComplete_of_Nodup`  (C5bBridge.lean:51) — `l.Nodup → CombosComplete l`,
  discharges the perm half's named hypothesis via `combos_complete` + `List.mem_toFinset`.
- `C5bBridge.is45setB_to_Is45`  (C5bBridge.lean:62) — the **unconditional** bridge
  `is45setB l = true → l.Nodup → Is45 l.toFinset` (no remaining named hypothesis).
- `C5bBridge.Abase_toFinset_card`  (C5bBridge.lean:69) — `Abase.toFinset.card = 14`.
- `C5bBridge.Abase_Is45`  (C5bBridge.lean:76) — `Is45 Abase.toFinset` (concrete (4,5)-property
  of the record gadget, via the bridge).
- `C5bBridge.Abase_threeAPs_card_le_12`  (C5bBridge.lean:86) —
  `(threeAPs Abase.toFinset).card ≤ 12`, the cap lemma `C5bCap.m_le_n_sub_2` fired on the
  concrete engine gadget (`m ≤ n − 2 = 14 − 2 = 12`).

## #print axioms (reproduce with `lake env lean` on an importing file)

```
'C5bBridge.is45setB_to_Is45'           depends on axioms: [propext, Classical.choice, Quot.sound]
'C5bBridge.Abase_Is45'                 depends on axioms: [propext, Classical.choice, Quot.sound]
'C5bBridge.Abase_threeAPs_card_le_12'  depends on axioms: [propext, Classical.choice, Quot.sound]
'C5bBridge.CombosComplete_of_Nodup'    depends on axioms: [propext, Classical.choice, Quot.sound]
'C5bBridge.Abase_toFinset_card'        depends on axioms: [propext, Classical.choice, Quot.sound]
```

No `sorryAx`, no `Lean.ofReduceBool` (native_decide), no new axiom — only the three standard
Mathlib axioms.

Importing file used:
```lean
import Constants.C5bBridge
open C5bBridge
#print axioms is45setB_to_Is45
#print axioms Abase_Is45
#print axioms Abase_threeAPs_card_le_12
#print axioms CombosComplete_of_Nodup
#print axioms Abase_toFinset_card
```

## Inputs consumed (all prior-round compiled theorems)

- `C5bBridgePerm.is45setB_to_Is45` (R9, perm half, modulo `CombosComplete l`).
- `C5bCombos.combos_complete` (R9, combos-completeness half, Perm form, under `l.Nodup`).
- `C5bCap.m_le_n_sub_2` (R8, abstract cap lemma `m ≤ n − 2` over `Is45`).
- `C5b.Abase_is45set`, `C5b.Abase_nodup`, `C5b.Abase_length` (R3/R1, kernel `decide`).
