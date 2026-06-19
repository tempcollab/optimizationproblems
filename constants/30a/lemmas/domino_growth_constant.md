# Lemma `domino_growth_constant`

**Statement.** The number of `n`-point dominoes is
`|D_n| = 2·(3n+3)! / ((n+2)!·(2n+3)!)` (OEIS A000139), and its growth rate is
`gr(D) = lim_n |D_n|^{1/n} = 27/4` exactly.

**Status.** CERTIFIED (round 1, reviewer-verified). Source: BBEPP2017 Theorem 3.1
(cited literature constant); realized in `certificate/decorated-domino-upper.py`
(`A000139`, `domino_growth_constant`).

**Reviewer verification (round 1).**
- Closed form reproduced and cross-checked against OEIS A000139 small terms
  (`1,2,6,22,91,408,1938,…`).
- Growth rate re-derived independently and exactly: the consecutive ratio is
  `|D_{n+1}|/|D_n| = (27n²+81n+60)/(4n²+22n+30)`, whose limit as `n→∞` is `27/4`
  (verified symbolically with sympy). So `gr(D) = 27/4` rigorously, not merely cited.

Statement is correct and no stronger than proved.

**Reusable for.** Any 30a domino-skeleton upper-bound sketch (e.g.
`decorated-domino-upper`, `bona-forbidden-factor-upper`), where the final bound is
`gr(Av(1324)) ≤ β · gr(D) = β · 27/4` for a word-multiplicity factor `β`.
