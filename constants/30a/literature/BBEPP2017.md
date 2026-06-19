# BBEPP2017 — Bevan, Brignall, Elvey Price, Pantone

"A structural characterisation of Av(1324) and new bounds on its growth rate."
arXiv:1711.10325 (v3, 2019); Eur. J. Combin. 2020. PDF: `pdfs/bbepp2017.pdf`.

**The record on BOTH sides: 10.271 ≤ gr(Av(1324)) ≤ 13.5.**

## Core structural object (the foundation everything rests on)

- **Prop 2.1 (staircase containment).** Av(1324) ⊆ the descending (Av(213), Av(132))
  *staircase* grid class: an infinite anti-diagonal of cells alternating Av(213) (upper)
  and Av(132) (lower). Proof is a constructive **greedy gridding**: scan points, place
  row/column dividers by a deterministic 213/132 rule. This is an *exact* containment
  (one direction); the staircase itself has growth rate 16, so containment alone only
  re-proves CJS12's 16.
- **Dominoes** = a pair of vertically (or horizontally) adjacent cells, top avoiding 213,
  bottom avoiding 132, with the joint constraint that the gridded pair avoids 1324.
  Bijection (Prop 3.2–3.4) to **arch configurations** with no forbidden sub-arrangement.
- **Theorem 3.1 (exact domino count).** #{n-point dominoes} = 2(3n+3)! / ((n+2)!(2n+3)!),
  which is **OEIS A000139** (West-2-stack-sortable perms; rooted nonseparable planar maps).
  Hence **gr(D) = 27/4 = 6.75**. Algebraic GF, derived by resultant elimination on the
  arch functional equation; growth rate read off the dominant singularity.
- **Prop 3.6 (balanced dominoes).** Dominoes with equal points in each cell have the same
  growth rate 27/4 (pigeonhole + concatenation argument). Used by both lower-bound constructions.

## Upper bound 13.5 (Theorem 4.1) — METHOD AND SLACK

**Method.** Injection Av_n(1324) ↪ {◦,•}^n × D_n. Greedy-grid σ; record a binary word of
length n (◦ if point is in an upper/213 cell, • if lower/132 cell), and collapse all upper-cell
points into the domino's top cell, all lower-cell points into the bottom cell. σ is recoverable
from (word, domino), so the map is injective. Counting: 2^n binary words × (27/4)^n dominoes
⟹ growth rate **2 · 27/4 = 13.5**.

**Load-bearing step = the factor 2** (the 2^n free binary words encoding the vertical interleave).
**SLACK — stated verbatim by the authors (p.14):** "The use of an arbitrary binary word to
record the vertical interleaving of the points is very rudimentary. One would hope that the
approach could be refined by recording this information as decorations on the domino in such
a way as to yield a tighter upper bound, **but we have not been able to do so.**"
- The 2^n massively overcounts: not every binary word × domino is a valid 1324-avoider. Any
  rigorous restriction on which (word, domino) pairs are achievable drops the base below 13.5.
- Anything strictly between 27/4 (≈6.75, the no-interleave-freedom floor) and 13.5 is a new record.
  Even shaving the effective per-point interleave choice from 2 to, e.g., 1.9 gives 12.825.

## Lower bound — METHOD AND SLACK

**Initial (Theorem 5.1, gr ≥ 81/8 = 10.125).** Partition the staircase into alternating
*dominoes* and single *connecting cells* (period-6 cell pattern). Build a subclass: each
domino cell 14k points, each connecting cell 8k points with 7k skew-indecomposable
components; require every domino-cell point to sit *between* the components of adjacent
connecting cells (this rule guarantees no 1324). Count exactly:
|P_k| = |B_14k|^k · |C_8k,7k|^k · C(21k,14k)^{2k−1}, with |B_n| ~ (27/4)^{2n} and
|C_n,c| = (c/n)·C(2n−c−1, n−1) (Catalan-forest count). Optimise the ratios ⟹ 81/8.

**Refined (Theorem 7.1, gr ≥ 10.271012).** Section 6 proves two **concentration results**
(expected #leaves and #empty-strips in a random n-point domino cell are asymptotically
concentrated). Section 7 *relaxes* the interleaving rule for horizontal dominoes: only
*non-leaves* must sit between components; *leaves* may be placed arbitrarily. Re-derive the
generating function G(z), Hj(z,q); pick α=5/9−1e-8, β=5/27−1e-8, γ≈0.9515, κ≈0.4963 ⟹
z0≈0.097361383, 1/z0 ≈ **10.271012**. (Footnote: an alternative analysis gives an algebraic
number of min-poly degree 104 ≈ 10.27101292824530.)

**Load-bearing step = the interleaving count + the leaf/strip concentration estimates.**
**SLACK — stated verbatim by the authors (§7.4 "Improving the lower bound further"):**
1. "If we determined the expected proportion of k-leaf strips for k≥1, and established that
   their distribution was concentrated, that would affect the optimal distribution of points...
   leading to a better bound. It is possible to modify the functional equation for dominoes to
   record k-leaf strips for any k, but the result is complicated and it has not been possible to
   analyse the result, even for k=1." — **k=1 leaf-strip concentration is the explicit next step.**
2. "We could relax our construction to permit leaves in *vertically* adjacent domino cells to be
   positioned arbitrarily [as horizontal ones already are]. Due to the complex interaction
   between interleaving in two directions, we have not been able to determine a lower bound."
   — **2D interleaving freedom is unexploited.**
3. "If we established a lower bound on the growth rate of permutations gridded in the first
   THREE cells (**trominoes**), we could decompose the staircase into trominoes to yield a new
   bound. However, enumerating trominoes seems to require some new ideas." — **trominoes.**

## Open problems flagged
- Problem 3.5: find an explicit bijection dominoes ↔ A000139 structures (2-stack-sortable / planar maps).
- The exact value of gr(Av(1324)) remains open; numerical estimate (CGZ) ≈ 11.60 ± 0.003.

## Lean-fit assessment
- The **domino count 27/4 is exact and algebraic** (a hypergeometric ratio / algebraic-GF
  singularity) — discrete, certifiable.
- The **upper bound 13.5 = 2·(27/4)** is a *finite product of an exact algebraic constant and a
  counting factor*; a refined upper bound that replaces "2" with a smaller certified
  per-point multiplicity would be largely discrete/algebraic — plausibly Lean-fit.
- The lower bound's final number (10.271) bottoms out in a *continuum* optimisation of a
  multivariate generating function with concentration (probabilistic) inputs — Lean-hostile in
  its current form. BUT a lower bound from a finite explicit subclass with a rational/algebraic
  count (à la Theorem 5.1's exact |P_k| product, or a transfer-matrix spectral radius) is
  discrete and certifiable.
