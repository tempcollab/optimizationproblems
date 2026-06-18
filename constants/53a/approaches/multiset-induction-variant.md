# Approach: multiset-induction-variant

**Constant:** 53a — Davenport constant of `C_n^3`,
`C_53 = sup_{n>=2} (D(C_n^3)-1)/(n-1)`, repo bounds `3 <= C_53 <= 4`.
**Moves:** upper bound (re-derives, does NOT beat, `C_53 <= 4`).
**Type:** Lean-fit certificate. INFRASTRUCTURE / faithfulness.

> **Body authored round 4 by the sibling slug `factors-bridge-max-extract`** (per the
> outline-reviewer dispatch). This slug was registered in round 3 as a ranker stub with no
> `.md` body and the summary word "Multiset". The realization actually landed via the
> **List / `Nat.primeFactorsList` route**, not `Multiset` — the List route is the lighter
> realization (the explorer and outline-reviewer both recommended it), and all its load-bearing
> Mathlib lemmas are confirmed present in the pinned rev. So this approach and
> `factors-bridge-max-extract` describe the SAME verified increment; see
> `factors-bridge-max-extract.md` for the full writeup.

## Idea

Tie the abstract factor list `ps` of `global_induction` / `c53_le_4_per_n` to the actual
prime factorization of a concrete `n`. The original framing imagined a `Multiset`
(`Nat.factors`/`Nat.factorization`) induction; the realized route is over the ORDERED list
`Nat.primeFactorsList n` (prime factors with multiplicity), extracting the maximum prime as
the modulus and erasing it to form `ps`.

## What COMPILED (round 4)

`lean/Constants/C53a.lean`, theorem **`factors_bridge_max`** — for `n >= 2`,
`D n - 1 <= 4 * ((n:ℤ) - 1)` with modulus `Q = largest prime factor of n`, read off
`Nat.primeFactorsList n`. `lake build Constants` green; axioms
`[propext, Classical.choice, Quot.sound]`, no `sorryAx`. Full mechanism, pitfalls, and the
largest-prime-vs-prime-power (`P(n)`) subtlety are documented in
`factors-bridge-max-extract.md` and `constants/53a/certificate/axioms.txt`.

## Why List, not Multiset

- `Nat.prod_primeFactorsList`, `Nat.prime_of_mem_primeFactorsList`,
  `Nat.primeFactorsList_ne_nil`, plus `List.perm_cons_erase` / `List.Perm.prod_eq` /
  `List.maximum_of_length_pos_mem` / `List.le_maximum_of_length_pos_of_mem` give the whole
  chain directly on the list, with no `Multiset.toList` / `Quotient` round-trips.
- The `global_induction` fold (round 3) already consumes a `List ℕ`, so the List route plugs
  in with zero adaptation.

## Does NOT beat 4

Same conditional-on-`hstep` situation as the rest of the scaffold; the record-break lever is
the open sub-`3p^2` `eta(C_p^3)` (`eta-coefficient-barrier.md`). `held` unchanged at 4.

## Further work

Same carry-forwards as `factors-bridge-max-extract.md`: Route P (prime-power `P(n)`), `iSup`
packaging, and a faithful in-Lean `hstep`. A genuine `Multiset`/`Finset.prod` reformulation
(if ever wanted for a cleaner statement) would re-prove `factors_bridge_max` over
`n.primeFactors` with `Finset.max'`; not needed for `C_53 <= 4` and lower priority than Route P.
