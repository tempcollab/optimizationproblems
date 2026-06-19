# Lower-bound side: proving Borsuk holds in dim 4..62 (= raising LOWER bound above 4)

The LOWER bound `C_28 >= 4` means Borsuk's conjecture is *true* for `n<=3` (Borsuk n=2, Eggleston/Grünbaum n=3). Raising it to `>=5` means **proving b(4) <= 5** (every bounded `X⊂R^4` partitions into 5 smaller-diameter parts), and so on up the line to 62.

## Why this is conjecture-hard (flag: do NOT target)
- **n=4 is wide open.** Best known is `b(4) <= 9` (Lassak 1982), with later small improvements (e.g. arXiv:1007.2518 "On the Borsuk number of four-dimensional sets" narrows it for restricted classes; WX2022 arXiv:2206.15277 does the `ℓ_p` analogue). The *conjectured* value is 5; nobody has closed the gap from 9 down to 5 for general 4-dim sets in ~90 years.
- Proving `b(n) <= n+1` for a *general* bounded set in any fixed `n in {4,...,62}` is a **major open problem** — it is the Borsuk conjecture itself in that dimension. There is no known finite/discrete reduction: the adversary set `X` ranges over *all* bounded subsets of `R^n` (a continuum optimization over infinitely many configurations), not a finite graph. This is the opposite of Lean-fit.
- CLAUDE.md guidance: skip the conjecture-hard side. This side qualifies.

## Verdict
The lower-bound side is **not a viable target** this run. All tractable motion is on the UPPER bound (explicit finite counterexample constructions). Direct effort to the upper-bound / Gri2026 line.
