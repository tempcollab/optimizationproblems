# C_5b — current verified bottom line

Constant: C_5b = c* (Sidon density in (4,5)-sets), Erdős #757. We attack the UPPER bound.

## Status
none

## Bounds
table: 4/7 ≈ 0.5714286 (upper, [MT26]) · held: 4/7 (record reproduced — Lean-certified finite content + cited Thm 1.5 bridge; NOT improved)

Verified lower bound for context: 9/17 ≈ 0.5294 ([MT26]).

## Progress log
- R1: Verified Lean reproduction of the record. `lake build Constants.C5b` passes; the two finite, load-bearing facts about the 14-pt record gadget A_base — `Abase_weakSidon` (it is a (4,5)-set / weak Sidon set, all 91 pair-sums distinct) and `Abase_hLe8` (all 2002 nine-subsets contain a 3-AP ⇒ h(A_base) ≤ 8) — `decide` with NO axiom dependence (kernel reduction only; no sorry, no native_decide). Witness `AbaseWitness8_no3AP` gives h ≥ 8, so h(A_base) = 8 and c* ≤ 8/14 = 4/7. The gadget→bound bridge ([MT26] Thm 1.5, c* = inf_n f(n)/n) is the single trusted-not-proved link, exposed as the explicit hypothesis `MTThm15`; `c5b_le_four_sevenths` rests only on it plus the 3 standard Mathlib axioms (propext, Classical.choice, Quot.sound). Independently re-derived all four finite facts in Python (combos count = 2002 confirmed in-kernel via #eval). This REPRODUCES the record; it does not beat it.
- R1: Verified obstruction window for the small-gadget upper-bound angle. From the PROVEN lower bound c* ≥ 9/17, every (4,5)-set of size N has h(A) ≥ ⌈9N/17⌉, so a size-N gadget beats 4/7 only if 7·⌈9N/17⌉ < 4N. Independently confirmed: N=14 and N=21 CANNOT beat 4/7 (floors 8 and 12 land exactly at 4/7). Smallest feasible N: 9, 11, 13, 15, 16, 17, 18, 20, 22, … Window-limited exact search found no beat at N=9,11 within the searched windows (suggestive, not a global non-existence proof).
