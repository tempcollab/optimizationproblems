# combos-completeness certificate (R9)

## Lean theorem (the deliverable)
File: `lean/Constants/C5bCombos.lean`.

Build target:
    cd lean && lake build Constants.C5bCombos        # PASS, Mathlib v4.31.0

Key lemma:
    C5bCombos.combos_complete {l : List ℤ} (hl : l.Nodup)
      {a b c d : ℤ} (ha hb hc hd : · ∈ l) (6 pairwise-ne) :
        ∃ t, t ∈ C5b.combos l 4 ∧ t ~ [a,b,c,d]

Supporting: `length_of_mem_combos`, `mem_combos_of_sublist` (the hard induction),
`four_distinct_perm_sublist`.

## Axioms (reproduce with `axioms_check.lean`)
    cd lean && lake env lean ../constants/5b/certificate/combos/axioms_check.lean
Output (R9):
    'C5bCombos.combos_complete' depends on axioms: [propext, Quot.sound]
    'C5bCombos.mem_combos_of_sublist' depends on axioms: [propext, Quot.sound]
    'C5bCombos.length_of_mem_combos' depends on axioms: [propext, Quot.sound]
    'C5bCombos.four_distinct_perm_sublist' depends on axioms: [propext, Quot.sound]
No sorryAx, no Classical.choice, no native_decide/ofReduceBool.

## Independent completeness cross-checks
1. In-kernel `#eval` (`eval_coverage_check.lean`): `(combos L 4).length = C(|L|,4)`
   on |L| = 6,7 (15, 35); every member length-4 + distinct; distinct underlying sets = C(|L|,4).
       cd lean && lake env lean ../constants/5b/certificate/combos/eval_coverage_check.lean
2. External Python (`python_coverage_check.py`): re-enumerates the recurrence and compares to
   itertools.combinations on n in {6,7,8}; cover_all_subsets = True, count = C(n,4).
       python3 python_coverage_check.py
