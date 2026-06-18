# engine-is45set-difference-fix

**Angle:** correctness prerequisite — re-key the Lean certification engine from the wrong
(weaker) weak-Sidon *sum* predicate to the correct (4,5)-set *difference* predicate.
**Moves a bound?** No new bound by itself. It RE-VERIFIES the held `c* ≤ 4/7` zero-axiom on
the *correct* definition, and is a hard prerequisite for trusting any future gadget.
**Status (R3): BUILT, claim = held 4/7 re-certified on the correct predicate, `lake build`
PASS, axioms clean.** (Claim — unverified until the reviewer re-runs.)

## The problem this fixes

The R1/R2 engine (`lean/Constants/C5b.lean`) certified the gadget property via
`weakSidonB` = distinct pairwise SUMS (weak Sidon). That is WRONG for the (4,5)-set
definition, which is the *difference* condition: every 4-element subset has ≥ 5 distinct
pairwise absolute differences `|x−y|`. (4,5)-set ⊊ weak Sidon strictly — `{0,2,5,8,14,21,28}`
is weak Sidon but NOT a (4,5)-set (4-subset `{0,14,21,28}` has only 4 distinct diffs
`{7,14,21,28}`). So `MTThm15`, with antecedent `weakSidonB l = true`, is a FALSE proposition
for new gadgets and could falsely certify a bound from a weak-Sidon-non-(4,5) set.

## What was done (R3)

1. Added decidable `Bool` machinery over explicit `List ℤ` (same `combos` engine, plain
   kernel `decide`, no `Finset.powersetCard`):
   - `countDistinct : List ℤ → ℕ` — distinct-value count by structural recursion.
   - `diffs6 a b c d : List ℤ` — the 6 pairwise `|x−y|` of a 4-set (`Int.natAbs`).
   - `diffs4B a b c d : Bool` = `Nat.ble 5 (countDistinct (diffs6 …))` — "this 4-subset has
     ≥ 5 distinct differences".
   - `diffs4Bof : List ℤ → Bool` — applies `diffs4B` to a length-4 list.
   - `is45setB l : Bool = (combos l 4).all diffs4Bof` — every `C(N,4)` four-sublist passes.
2. Re-keyed the bridge: `MTThm15`'s antecedent is now `is45setB l = true` (was
   `weakSidonB l = true`); `c5b_le_four_sevenths` now feeds `Abase_is45set` (was
   `Abase_weakSidon`). `weakSidonB`/`Abase_weakSidon` kept for reference only, with docstrings
   stating they are the strictly-weaker property and do NOT certify.
3. Re-verified A_base by pure kernel `decide`:
   `theorem Abase_is45set : is45setB Abase = true := by decide` (C(14,4)=1001 four-subsets).
4. `#eval` sanity (verified): `is45setB Abase = true`; `is45setB [0,2,5,8,14,21,28] = false`
   (separating set correctly rejected); `weakSidonB [0,2,5,8,14,21,28] = true` (it IS weak
   Sidon — confirms the predicates genuinely differ); `diffs4Bof [0,14,21,28] = false`.

## Verification (claim — reviewer re-runs)

- `lake build` → PASS. Module `Constants.C5b` cold build 85–87s; full project 8563 jobs,
  31s incremental. Mathlib pinned at v4.31.0. `lean/.lake` not committed.
- `#print axioms`:
  ```
  'C5b.Abase_is45set' depends on axioms: [propext]
  'C5b.Abase_hLe8' does not depend on any axioms
  'C5b.AbaseWitness8_no3AP' does not depend on any axioms
  'C5b.c5b_le_four_sevenths' depends on axioms: [propext, Classical.choice, Quot.sound]
  ```
  No `sorryAx`, no `Lean.ofReduceBool`/`native_decide`, no added axiom. `propext` is one of
  the three standard foundational axioms (enters via the `Nat.ble`/`if` reduction); the only
  trusted-not-proved link is the explicit named hypothesis `MTThm15` ([MT26] Thm 1.5).
- Independent Python cross-check: A_base has 0 violations across all 1001 four-subsets;
  separating example fails on `{0,14,21,28}`.

## Claim

The held record `c* ≤ 4/7` is re-certified on the CORRECT (4,5)-set difference definition,
zero-axiom (modulo the explicit MTThm15 bridge). The 4/7 record SURVIVES — A_base is a
genuine (4,5)-set. No bound improvement (this is a correctness/soundness step).

## What would push it further

- The engine is now sound for any NEW gadget at the (4,5)-property step: a candidate
  beating 4/7 needs only `Abase`-swap + `is45setB`/`noSidonSubsetB` re-`decide`.
- The h-side at N ≥ 21 still needs the transversal-certificate machinery
  (`floorplus1-transversal-N30`) — `noSidonSubsetB` raw `decide` over `C(30,18) ≈ 86M` is
  hopeless; the difference predicate `C(N,4)` stays cheap (≤ 27405 at N=30).
- Source: Ma & Tang, arXiv:2602.23282 (Feb 2026), §Definitions + Lemma 2.3 + Theorem 1.5.
