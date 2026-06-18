# decidable-bridge-is45-full

**Angle.** Assemble the two R9-verified halves of the decidable bridge into the
**unconditional** `is45setB l = true → l.Nodup → Is45 l.toFinset`, then fire the R8 structural
cap lemma `C5bCap.m_le_n_sub_2` on the concrete engine gadget `Abase`. This wires the abstract
cap lemma (over `Is45 : Finset ℤ → Prop`) into the concrete `is45setB`-keyed engine, closing out
the multi-round cap-lemma → concrete-engine thread (R8 cap lemma → R9 two halves → R10 assembly).

**No bound move — and honestly so.** The record stays the verified upper `4/7` of [MT26].
`c5b_le_four_sevenths` already rests on `is45setB` + `MTThm15` directly, and the cap lemma lives
on the `m` / lower side, not the `4/7` upper path. This is a search-immune Lean-machinery
close-out; value = a compiled, axiom-clean theorem hardening the formalization, not a beat.

## Status — R10: BUILT, claim = lake build PASS + axiom-clean (UNVERIFIED until reviewer confirms)

New file `lean/Constants/C5bBridge.lean` (auto-included by the `Constants.+` lib glob; no
lakefile edit). `lake build Constants.C5bBridge` PASS; full `lake build` PASS (8570 jobs).

New top-level theorems (all sorry-free; `#print axioms` = `[propext, Classical.choice,
Quot.sound]` only — no `sorryAx`/`native_decide`/`ofReduceBool`):

1. `CombosComplete_of_Nodup : l.Nodup → CombosComplete l` (C5bBridge.lean:51). Discharges the
   single named trust boundary of the perm half: `intro` the four points + distinctness, rewrite
   each `· ∈ l.toFinset` to `· ∈ l` via `List.mem_toFinset` (the only non-trivial line), then apply
   `C5bCombos.combos_complete hl`. The `combos_complete` output is *exactly* the
   `∃ p ∈ combos l 4, p.Perm [a,b,c,d]` that `CombosComplete` demands (verified R9).
2. **`is45setB_to_Is45 : is45setB l = true → l.Nodup → Is45 l.toFinset`** (C5bBridge.lean:62) —
   the **unconditional** bridge. One-line composition: feed `CombosComplete_of_Nodup hl` into
   `C5bBridgePerm.is45setB_to_Is45`. No remaining named hypothesis, no sorry, no new axiom.
3. `Abase_toFinset_card : Abase.toFinset.card = 14` (C5bBridge.lean:69) — via
   `List.toFinset_card_of_nodup Abase_nodup` + `Abase_length`.
4. `Abase_Is45 : Is45 Abase.toFinset` (C5bBridge.lean:76) — the concrete (4,5)-property of the
   record gadget, fed `Abase_is45set` (`is45setB Abase = true`, R3 kernel `decide`) + `Abase_nodup`
   through the unconditional bridge.
5. **`Abase_threeAPs_card_le_12 : (threeAPs Abase.toFinset).card ≤ 12`** (C5bBridge.lean:86) —
   the cap lemma `C5bCap.m_le_n_sub_2` fired on `Abase.toFinset` (a (4,5)-set of size `14 ≥ 2`),
   instantiating the abstract `m ≤ n − 2` to the concrete `m ≤ 14 − 2 = 12` on the engine gadget.

Cert: `constants/5b/certificate/bridge/README.md` (build target + `#print axioms` line).

## Claimed (unverified) result

The decidable bridge `is45setB l = true → l.Nodup → Is45 l.toFinset` is now a compiled,
axiom-clean Lean theorem with **no remaining named hypothesis** (both R9 halves discharged), and
the R8 cap lemma fires concretely on `Abase` to give `(threeAPs Abase.toFinset).card ≤ 12`. The
cap-lemma → concrete-engine wiring thread is fully closed in Lean. **No bound move.**

## How to push further

The cap-lemma formalization thread is now closed; this slug is terminal for that thread. The
concrete cap `m ≤ 12` on `Abase` is the lower-side machinery — it does NOT touch the `4/7` upper
path. Remaining in-5b verifiable directions (per run_state):

1. **Bound-move roads all walled** — gadget search exhausted (blind-α floor+3, max-m 26 vs cap 28,
   τ-deficit 2); pushing `9/17` / `f(30)≥18` is the same Lean-hostile sharpened-Henning–Yeo
   theorem with no finite core. No new bound-move lever has appeared in nine rounds.
2. If a future N≈30 gadget with a partially-integral cover LP is ever found, the unconditional
   bridge here feeds it straight into `Is45`, and `C5bInterleaved.hLe_of_interleaved` could then
   shrink the transversal budget — but that needs the gadget first (the verified wall).
3. The bridge is fully general (`l.Nodup` only), so it certifies the `Is45` set-property of ANY
   future engine gadget with one `decide` of `is45setB` — reusable beyond `Abase`.
