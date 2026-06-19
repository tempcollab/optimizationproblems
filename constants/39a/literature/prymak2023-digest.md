# Digest: Prymak 2023 — "A new bound for Hadwiger's covering problem in E^3" (arXiv 2112.10698, SIAM J. Discrete Math 37(1):17-24)

**Result.** $H_3 \le 14$. Every 3-dim convex body is covered by 14 translates of its interior.
Previous best 16 (Papadoperakis 1999). Hadwiger conjecture: 8.

PDF: `constants/39a/literature/pdfs/prymak2023.pdf`; text `prymak2023.txt`.
Code/data: https://github.com/andriyprm/h3atmost14/releases/tag/v1 (SageMath scripts + output).

## The method (this is the load-bearing structure)

Builds on Papadoperakis [Pap1999]. Steps:

1. **Reduce to a normalized box.** For any convex body $K$, take the minimal-volume
   parallelotope $C \supset K$; affinely map $C = [0,1]^3$ (the unit cube). Covering number
   $C(K,\mathrm{int}(K))$ is affine-invariant.
2. **Six contact points -> a configuration $A_p$.** On each pair of opposite faces $F_{ij}$
   choose contact points $q_{ij}\in F_{ij}\cap K$ with $q_{i0}+e_i = q_{i1}$ (perpendicular
   pairs). These six points are the columns of a matrix $A_p$, parametrized by
   $p\in[0,1]^6$. $V_p = A_p(\{e_1,\dots,e_6\})$ (the 6 points); $O_p = A_p(S)$ = their convex
   hull (a polytope inside $K$), where $S$ is the simplex.
3. **Key reduction (Papadoperakis Lemma 4, sharpened to Lemma 2.2).**
   $C(K,\mathrm{int}(K)) \le \max\{ C(E\cup V_p, \mathrm{int}(O_p)) : p\in[0,1]^6\}$
   where $E$ = the 1-skeleton (12 edges) of the cube. The general body is replaced by a
   **6-parameter family of covering problems** on the cube's skeleton + 6 face points,
   covering with translates of the (larger) polytope $O_p$ rather than a parallelotope.
   Using $O_p$ (vs. the inscribed parallelotope $P$ of Papadoperakis) is exactly the
   improvement 16 -> 14.
4. **Discretize $p$-space; open -> closed.** Partition the configuration space into small
   boxes $P$. For each box define $Q_P = \bigcap_{v\in U_P} O_v$ (intersection over the 64
   vertices of $P$). Lemma 2.4: $Q_P \subset O_p$ for all $p\in P$, and a translate of $Q_P$
   sits in $\mathrm{int}(O_p)$ — converts the open-cover requirement into a closed-polytope LP.
   Corollary 2.5: $\max_{p\in P} C(E\cup V_p,\mathrm{int}(O_p)) \le C(E\cup R_P, Q_P)$ where
   $R_P=\bigcup_{p\in P}V_p$ (six rectangles on the facets).
5. **Fix the covering combinatorics, reduce to an LP.** Use a fixed covering structure: 8
   translates of $Q_P$ for the 8 cube vertices (each covering a vertex + parts of 3 adjacent
   edges), plus 6 translates each covering one face-rectangle $R_P\cap F_{ij}$ + a "middle"
   portion of one edge — selected by an injective map
   $\tau:\{1,2,3\}\times\{0,1\}\to\{0,\dots,11\}$. Total 14. Edges are 1-D so coverage by two
   (or three) closed translates is an LP feasibility on the translate vectors. **60 variables,
   $68q$ linear constraints** ($q$ = #facets of $Q_P$), all rational coefficients
   (Proposition 2.6). Feasibility => $C(E\cup R_P,Q_P)\le 14$.
6. **Computer proof (Proposition 3.1).** Symmetry-reduce $p$-space to a fundamental domain
   $D$ (cube symmetries, ~1/48). Cover $D$ by $U_{20}$ grid boxes; adaptively subdivide.
   **4,660,035 boxes**, each with a feasible $(P_j,\tau_j)$. Float LP first, then exact
   rational re-check. ~2 weeks on 10 i7 threads.

## The obstruction — why 14 and not less (CRITICAL for upper-bound angles)

**Remark 2.3 (sharpness of THIS approach).** With $p=(1/2,\dots,1/2)$, the 14-point set
{8 cube vertices} $\cup\,V_p$ has the property that **no single translate of $\mathrm{int}(O_p)$
can cover two of these 14 points**. Hence $C(E\cup V_p,\mathrm{int}(O_p))\ge 14$, so
$\max_p \ge 14$. **14 is exactly the best the $O_p$-on-the-cube approach can do.**

Consequence: to beat 14 via this lineage, the **minimal-volume-parallelotope reduction
itself** must be replaced or refined — e.g. a body for which $p=(1/2,\dots,1/2)$ is forced
is essentially the affine-regular octahedron / a body whose 14 marked points are mutually
"far"; one must either (a) not normalize to a single cube, (b) use a different family of
covering pieces (not $O_p$), or (c) treat the worst $p=(1/2,\dots)$ case separately with a
smarter cover. The $p=1/2$ case is the genuine bottleneck.

## Lean fit

The certifying step is **LP feasibility over $\mathbb{Q}$ for 4.66M boxes** — a finite,
exact-rational, discrete computation. This is *Lean-formalizable in principle* (Farkas
certificates / rational LP feasibility witnesses are checkable in `Mathlib`), but the scale
(millions of boxes, the box-subdivision search) makes a full Lean replay heavy. The
load-bearing inequalities are rational and finite, NOT continuum — so the bound is closer to
Lean-fit than to the 82a (Mahler integral) kind, but a *new* improvement would want a much
smaller certificate to be Lean-practical.
