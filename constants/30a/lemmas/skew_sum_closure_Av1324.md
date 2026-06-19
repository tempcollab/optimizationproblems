# Lemma `skew_sum_closure_Av1324`

**Statement.** For permutations `a, b`, the skew sum `a ⊖ b` avoids 1324 **iff** both
`a` and `b` avoid 1324. (Equivalently: `Av(1324)` is closed under skew sum, and a skew
sum is a 1324-avoider only when both summands are.)

Here `a ⊖ b` places `a`'s block above-and-left of `b`'s block: `a`-points take the left
positions and the high values, `b`-points the right positions and the low values.

**Status.** CERTIFIED (round 1, reviewer-verified). Source sketch:
`certificate/transfer-matrix-lower.py` (`prove_skew_sum_closure` + `brute_check_skew_closure`).

**Proof of the load-bearing direction (⇐).** Suppose `a, b` avoid 1324 and a 1324
occurrence sits at positions `q1<q2<q3<q4` of `a ⊖ b` with value-ranks `(1,3,2,4)`.
Positions increase left-to-right, so the chosen points are a position-prefix of length
`t` in `a` and the remaining `4−t` in `b`, some `t ∈ {0,1,2,3,4}`. `t=0` puts the
occurrence entirely in `b`; `t=4` entirely in `a`; both contradict avoidance. For a
crossing `t ∈ {1,2,3}`: the `a`-points carry the **highest** values, so they must carry
the `t` largest value-ranks among `{1,2,3,4}`. But the ranks on the first `t` pattern
positions of `1324=(1,3,2,4)` are `t=1→{1}`, `t=2→{1,3}`, `t=3→{1,2,3}` — never the `t`
largest (which would be `{4}`, `{3,4}`, `{2,3,4}`). Contradiction. So no crossing
occurrence exists; the occurrence must be local to one summand, contradicting avoidance.
By induction over the number of skew-components the closure extends to any finite skew sum.

The (⇒) direction is immediate: `a` and `b` each occur as order-isomorphic sub-permutations
of `a ⊖ b`, so a 1324 in either lifts to a 1324 in `a ⊖ b`; contrapositive gives ⇒.

**Reviewer verification (round 1).** The biconditional was reproduced independently by
exhaustive enumeration over all avoider/non-avoider pairs with `|a|+|b| ≤ 8` (zero
counterexamples to `contains_1324(a⊖b) ⇔ contains_1324(a) ∨ contains_1324(b)`). The
finite rank argument above is general (not length-bounded). Statement is correct and no
stronger than proved.

**Reusable for.** Any skew-sum / skew-component construction on `Av(1324)`
(e.g. the tromino-subclass sketch, and the unique-skew-decomposition recurrence in
`transfer-matrix-lower`).
