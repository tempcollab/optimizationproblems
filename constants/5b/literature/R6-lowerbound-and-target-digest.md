# R6 digest — MT26 lower-bound machinery + the sharp R6 gadget target

Source: Ma & Tang, arXiv:2602.23282 (HTML body, fetched R6), cross-checked numerically.

## The lower-bound chain (verbatim lemma numbers)
- **Lemma 2.4** (midpoint map injective): for an edge e={x−d,x,x+d}, μ(e):=x is injective
  on a weak-Sidon set and misses min A, max A ⇒ **m_H ≤ n_H − 2**.
- **Theorem 5.3** (Henning–Yeo): for a 3-uniform **linear** **F₇-free** hypergraph,
  **17·τ(H) ≤ 5·n_H + 3·m_H**.
- **Definition 1.7 / Fig 1:** F₇ = 3-uniform on {0..6}, edges {012},{034},{056},{135},{246}.
  A (4,5)-set's H(A) is linear (edges meet in ≤1 vertex) and F₇-free.
- Combine: 17τ ≤ 5n + 3(n−2) ≤ 8n ⇒ τ ≤ (8/17)n ⇒ **α = h(A) ≥ (9/17)n**.

## The key R6 finding: HENNING–YEO IS TIGHT ON A_base
At N=14, m=12 (=n−2, **saturated**): HY gives τ ≤ (70+36)/17 = 6.235 ⇒ τ ≤ 6, and the
actual τ(A_base)=6. So **A_base is a Henning–Yeo-extremal configuration**: it saturates
BOTH m=n−2 and the HY transversal cap simultaneously. That is why 4/7 is hard to beat and
why 9/17 is hard to push.

## Consequence for option (b) — lower bound f(30) ≥ 18
To get f(30) ≥ 18 we need τ ≤ 12 forced on every size-30 (4,5)-set. HY gives
τ ≤ (150+3m)/17; at the max m=n−2=28 this is τ ≤ 13.76 ⇒ τ ≤ 13 ⇒ only **α ≥ 17**, NOT 18.
So the EXISTING machinery cannot prove f(30)≥18 — it would need a *sharpened* Henning–Yeo
for this restricted class (or a forced m≤18 at N=30). That is a genuine extremal-hypergraph
theorem, the SAME difficulty as improving 9/17, and **Lean-hostile** (no finite case core).
Option (b) is therefore NOT a soft target.

## Consequence for option (a) — the sharp gadget target
HY does NOT forbid α=17 at N=30 (allowed for m≥13). The beat target is exact:
**an indecomposable (4,5)-set, N=30, with m = n−2 = 28 edges (3-APs) and τ=13 ⇒ α=17 ⇒ 17/30 < 4/7.**
- Need τ-density 13/30 = 0.4333, just above A_base's 6/14 = 0.4286.
- A_base SATURATES m=n−2=12; the Fibonacci subsequence family (best found R5) has only
  m=26 < n−2=28 at N=30 — it is **2 edges short of the cap**, and its 3-AP hypergraph is a
  near-path (each triple is (i,i+2,i+3), max degree 3), giving α=19=floor+3. The τ-deficit of
  2 = the edge-deficit of 2 in disguise.
- So the R6 search target sharpens to: **maximize m toward n−2 with an indecomposable,
  non-path 3-AP arrangement** (A_base's hypergraph has a degree-4 vertex and is not a path).

## Why the general 3-AP-maximization literature does NOT help
Unrestricted n-sets reach ⌈n²/2⌉ 3-APs (Green–Sisask), but the weak-Sidon/midpoint-injective
condition collapses that to the LINEAR cap m≤n−2. So dense-3-AP constructions (which are full
APs, not weak-Sidon) are irrelevant; the binding constraint is the linear cap, and the game is
arranging n−2 midpoint-distinct 3-APs into a transversal-efficient (τ-dense) hypergraph that is
still a (4,5)-set and indecomposable.

## Construction families, triaged against the m=n−2 lens
- **Fibonacci subsequence** (GL95 lineage, best R5): m=n−2 minus 2, near-path, α=floor+3. WALL.
- **B₂[g] / Singer / CRT modular:** the (4,5) difference filter kills most points (R5: keeps
  7–9 of 30). These are SIDON-like (FEW 3-APs) ⇒ high α ⇒ wrong direction.
- **Geometric 3^k:** 3-AP-free, α=N. Wrong direction (extreme).
- **The right direction is the OPPOSITE of Sidon:** pack the midpoint-injective 3-APs as
  densely as the cap allows while keeping the difference condition. A_base is the only known
  m=n−2 saturator; the open question is whether an indecomposable m=n−2 saturator EXISTS at
  N=30 with τ=13 (i.e. whether A_base's extremal structure extends past N=14).
