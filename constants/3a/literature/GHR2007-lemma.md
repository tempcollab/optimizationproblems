# [GHR2007] Gyarmati–Hennecart–Ruzsa, *Sums and differences of finite sets* (Funct. Approx. 37(1):175–186, 2007)

Source PDF: https://gyarmatikati.web.elte.hu/publ/sumdiffv.pdf

## The load-bearing lemma for the C_3a LOWER bound

For a finite nonempty set `U ⊂ ℤ_{≥0}` containing `0`, set
- `s = |U+U|`
- `d = |U−U|`
- `q = 2·max(U) + 1`
- `θ = 1 + log(d/s) / log(q)`

Then `C_3a ≥ θ`. (In the repo ledger this is the "lemma from [GHR2007]" remark.)

**Why one finite set suffices.** The constant C_3a is the largest exponent such that there
exist arbitrarily large `A,B` with `|A+B| ≪ |A|` and `|A−B| ≫ |A+B|^{C_3a}`. The GHR lemma
turns a single finite `U` into an infinite family by a base/tensor power: working in base
`q = 2·max(U)+1`, the `k`-fold "digit" product of `U` has sumset/diffset cardinalities `s^k`,
`d^k` and max `≈ q^k`, so the ratio `log(d/s)/log q` is preserved in the limit and yields the
exponent. Thus **any single finite U gives a valid lower bound** — no asymptotics needed in the
certificate, only in the *interpretation*.

## Caveat noted in the ledger
The naive "any U" route (treating U directly, U−U vs U+U) caps out below 1.25; the strong bounds
come from the structured digit constructions below, which are still single finite sets U but with
`max(U)` astronomically large (so `q` huge) chosen to push `log(d/s)/log q` up.

## Certificate shape (Lean-fit)
The bound for a given U is **finite integer arithmetic**: enumerate U, compute the two
cardinalities and the max, evaluate one logarithmic inequality. To beat a rational target
`p/q`, the inequality `log(d/s)/log(q_base) ≥ p/q − 1` is equivalent to the integer inequality
`d^{q'} ≥ s^{q'}·q_base^{p'}` (clear denominators) — a pure integer comparison, no floating point,
no continuum estimate. This is the Lean-fit core: `decide`/`native_decide` or rational interval
arithmetic over explicit big integers.
