# bridge-perm-invariance-half

**Angle.** Build the permutation-invariance half of the decidable bridge
`is45setB l = true → Is45 l.toFinset`, which wires the R8 structural cap lemma
(`C5bCap.m_le_n_sub_2`, stated over the abstract `Is45 : Finset ℤ → Prop`) into the concrete
engine predicate `C5b.is45setB`. The cap lemma's hypothesis `Is45 A` quantifies over **every
ordering** of four pairwise-distinct points; the engine checks `diffs4B` on **one** index-order
per 4-subset (each member of `combos l 4`). The bridge needs (i) `combos`-completeness and (ii)
`diffs4B` permutation-invariance. **This slug delivers (ii) in full** plus the assembly modulo a
named (i).

**No bound move** — this is a search-immune Lean-machinery increment (all gadget-search levers
are walled; see run_state Rules). Value = a verified, axiom-clean compiled theorem advancing the
cap-lemma formalization.

## Status — R9: BUILT, claim = lake build PASS + axiom-clean (UNVERIFIED until reviewer confirms)

New file `lean/Constants/C5bBridgePerm.lean` (auto-included by the `Constants.+` lib glob; no
lakefile edit). `lake build Constants.C5bBridgePerm` PASS; full `lake build` PASS (8569 jobs).

Theorems proved (all sorry-free, axioms `[propext, Classical.choice, Quot.sound]` only — checked
by `#print axioms`, no `sorryAx`/`native_decide`/`ofReduceBool`):

1. `countDistinct_eq_dedup_length : countDistinct l = l.dedup.length` — by structural induction,
   matching `countDistinct`'s `if xs.contains x` branch to `List.dedup`'s `if x ∈ xs` branch.
2. `countDistinct_perm : l.Perm l' → countDistinct l = countDistinct l'` — via (1) +
   `List.Perm.dedup` + `List.Perm.length_eq`. (the outline's step 1, **fully proved**.)
3. `diffs6_perm_swap_ab/_bc/_cd` + `diffs4B_swap_ab/_bc/_cd` — the three adjacent transpositions
   (which generate S₄) leave `diffs6` Perm-stable and `diffs4B` invariant, using `diffSym`
   (`|x−y| = |y−x|`).
4. **`diffs4B_perm4` (the hard step, all 24 orderings, fully proved):**
   `[a,b,c,d].Perm [a',b',c',d'] → diffs4B a b c d = diffs4B a' b' c' d'`. Routed through a
   *compositional* pairwise-diff list `pdiffs` (`pdiffs (x::xs) = xs.map |x−·| ++ pdiffs xs`),
   whose Perm-invariance `pdiffs_perm` is provable by plain `List.Perm` induction (the `swap`
   case is `diffSym` + `List.perm_append_comm`); `pdiffs_four` ties `pdiffs [a,b,c,d]` back to
   `diffs6 a b c d`. This avoids enumerating 24 orderings or any group-theory S₄ machinery.
   (the outline's step 2 — **fully proved**, the named hard step.)
5. **`is45setB_to_Is45` (the assembly):** `CombosComplete l → is45setB l = true → Is45 l.toFinset`.
   The `combos`-completeness fact is `CombosComplete l : Prop` — an **explicit named hypothesis**
   (MTThm15-style trust boundary), NOT a `sorry`, NOT an axiom. The proof: completeness yields a
   `combos l 4` member `p ~ [a,b,c,d]`; `is45setB` gives `diffs4Bof p = true`; `p` has length 4
   (it permutes a 4-list) so `diffs4Bof p = diffs4B p₀ p₁ p₂ p₃`; `diffs4B_perm4` transports to
   `diffs4B a b c d`. (the outline's step 3 — **fully assembled**, modulo the named hypothesis.)

Independent cross-check: `constants/5b/certificate/bridgeperm/check_perm_invariance.py` brute-forces
`diffs4B` constant across all 24 orderings on anchors + 50 000 random quadruples (both True and
False outcomes covered); agrees with the Lean `#eval`s. Cert: `constants/5b/certificate/bridgeperm/`.

## Claimed (unverified) result

`is45setB l = true → Is45 l.toFinset` is now a compiled, axiom-clean Lean theorem **modulo the
single explicit named hypothesis `CombosComplete l`** (the `combos`-completeness fact). The full
perm-invariance content (`countDistinct_perm`, `diffs4B_perm4`) is unconditional and banked.

## How to push further

1. **Discharge `CombosComplete`** with the sibling slug `bridge-combos-completeness-half`'s
   `combos_complete` lemma (`C5bCombos.lean`). Then `is45setB_to_Is45` becomes unconditional —
   the full end-to-end bridge. One-line composition once both halves land (next round).
   - Watch the exact statement shape: this file's `CombosComplete` asks for `∃ p ∈ combos l 4,
     p.Perm [a,b,c,d]` for pairwise-distinct `a,b,c,d ∈ l.toFinset`. The combos-half lemma must
     produce exactly this `Perm`-to-`[a,b,c,d]` witness (or be adapted to it).
2. **Fire the `Abase` corollary.** With the unconditional bridge + `C5bCap.m_le_n_sub_2`, prove on
   `Abase` (a genuine (4,5)-set, `is45setB Abase = true` already `decide`-checked) that
   `(threeAPs Abase.toFinset).card ≤ 12 = 14 − 2`, demonstrating the wiring fires. This is the
   `decidable-bridge-is45-full` slug's remaining one-liner.
3. **Nodup note.** `Is45` quantifies over `l.toFinset` (a set), so the perm-half assembly never
   needs `l.Nodup` itself; the completeness hypothesis carries any Nodup obligation. Keep that
   boundary clean when composing.

This half is a near-certain APPROVE: bounded fixed-size reshuffles, no induction over `l`, math
already hand-verified in R8. The only open obligation is the visibly-named `CombosComplete`.
