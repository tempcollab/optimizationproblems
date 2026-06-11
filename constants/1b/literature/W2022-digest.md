# Digest: [W2022] Ethan P. White, "Erdős' minimum overlap problem" (arXiv:2201.05704)

PDF: `constants/1b/literature/pdfs/w2022.pdf`; text: `pdfs/w2022.txt`.

## What it proves
**Theorem 1: µ = C_1b ≥ 0.379005.** This is the current verified record lower bound
(README and 1b.md agree). Previous lower record was Moser's sqrt(4-sqrt15) ≈ 0.356394
[M1959]. So W2022 jumped the lower bound by ~0.0226 in one paper.

Definition used (Swinnerton-Dyer / Haugland equivalence): µ = largest C s.t. ||M||_∞ ≥ C
for every M(x) = ∫_{-1}^1 f(t) g(x+t) dt, with f:[-1,1]->[0,1], ∫f=1, g=1-f.

## Method — a RIGOROUS lower bound via convex programming + dual certificate
This is NOT a single construction. A lower bound here is a "for all f,g" statement, so the
method derives **necessary properties** every valid M must satisfy, then **minimizes ||M||_∞
subject to those properties** as a convex program. Any feasible dual point of that program is
a rigorous lower bound on µ. Structure:

1. **Necessary properties of M (the constraints).** All derived analytically:
   - (2.2) ∫_{-2}^2 M = 1   (mass) -> gives µ ≥ 1/4.
   - (2.3)/Lemma 6: ∫ x^2 M dx = 2/3 + E(M)^2/2  (second-moment identity) -> gives µ ≥ 1/sqrt8.
   - **(2.4) KEY new property: all EVEN cosine Fourier coeffs of M are ≤ 0**, i.e.
     ∫ cos(πkx) M dx ≤ 0 for all k≥1. This is the paper's main analytic insight.
   - Lemma 2/3: exact identities linking the sine-cosine Fourier coeffs of f on [-1,1]
     (variables c_k, d_k) to those of M on [-2,2] (A_m, B_m). Crucially A_2m ≤ 0 and the
     quadratic A_m = (4 sin(mπ/2)/mπ) a_m − 2(a_m^2 + b_m^2) couples M's coeffs to |f-hat|^2.

2. **Discretization into LP/convex variables.**
   - Variables: Ω (= target ||M||_∞), interval-averages w_j, v_j of M over N equal cells
     (L=2/N), the first T Fourier coeffs c_k,d_k of f, and tail-slack variables ε,δ.
   - Lemma 5/7: turn the moment and Fourier-coeff constraints into linear inequalities in
     w_j, v_j using rigorous per-cell min/max bounds α±, β± on cos/sin (with a +πmL/4
     Lipschitz safety margin) — so discretization is an *over/under-estimate*, never an
     approximation. This keeps the bound valid.
   - Lemma 4: the truncated Fourier tails (k>T) are rigorously bounded via Parseval
     (Σ(c_k^2+d_k^2) ≤ 1/2) + Cauchy–Schwarz, absorbed into ε,δ. So truncation is rigorous too.
   - Constraint (5.5) is QUADRATIC in (a_m,b_m) -> the program is a convex QCQP, reformulated
     as an SOCP (Appendix I).

3. **Divide-and-conquer over 3 nuisance parameters.** The program also takes box bounds on
   E(M)∈[h1,h2], c_1∈[p1,p2], d_1∈[q1,q2]. With the full boxes (0,2),(0,1),(-1,1) the optimum
   is only ~0.25. The bound is obtained by partitioning these boxes into many small pieces and
   taking the **min of the optimum over all pieces** (Tables 2,3, Fig 1). Most pieces give ≥0.38;
   the binding region is E(M)∈[0,0.06], c_1∈[0.33,0.45], d_1∈[-0.02,0.02], giving 0.379005.

4. **Rigor of the certificate (Appendix II).** They solve the dual SOCP numerically (CPLEX,
   N up to 25000, T up to 7000, R=10), then post-process: verify every dual inequality holds
   with a margin exceeding worst-case floating-point error (Higham summation bounds). A clever
   reuse trick: h1,h2,p1,p2 don't enter the dual constraints, only the dual objective, so one
   dual point certifies an *ellipse* of (h,p) values — 7 feasible points cover the binding region.

## Where the author SAYS the slack is (Concluding remarks, lines 2425–2441)
Two explicitly named sources:
- **(a) Pure computation** — larger N, T, R and higher-precision arithmetic improve the bound.
  BUT the author cautions: with N,T,R=25000,7000,10 he could certify 0.37905 but **NOT 0.3791**,
  and "this seems to indicate the limit of this method is not much larger than 0.379." So brute
  scaling of the SAME constraint set is near-exhausted — do not expect a record from scale alone.
- **(b) STRUCTURAL: prove the optimal f* is even.** "We also expect that the optimal f*(x) is
  even. A proof of this would also improve the lower bound on µ, since we could always take
  h1=h2=q1=q2=0 in the input." Symmetry would (i) kill the d_k (sine) variables and the whole
  divide-and-conquer over d_1=q, and (ii) pin E(M) and the odd structure — collapsing nuisance
  dimensions and letting the program reach higher. This is a CONJECTURE in the paper, unproven.

## Un-exploited analytic slack (not in the paper's remarks but visible in the construction)
- Only constraints used: mass (k=0 / 2.2), 2nd-moment identity (Lemma 6), even-cosine-coeff
  sign (2.4), the exact f<->M coefficient identities (Lemma 3), Parseval ℓ2 bound (3.7), and
  pointwise 0≤f≤1. **The f∈[0,1] box constraint is used only weakly** — via ‖f‖_1=1 and
  ‖f‖_2^2 ≤ 1 (Parseval, eq 3.7, since f∈[0,1] => f^2≤f). Higher-moment / higher-order
  pointwise consequences of 0≤f≤1 (e.g. f^2 ≤ f as a *distributional* constraint giving
  Σ richer than just ‖f‖_2^2≤1, or ∫f^k relations) are NOT exploited. A 4th-moment / higher
  even-coefficient family, or an SDP (not just SOCP) tightening the f-coefficient feasible set,
  is a genuinely orthogonal angle.
- R (number of cosine-sign constraints used as A_2m≤0) is only 10. The even-coeff-nonpositivity
  family is infinite; the author truncates at R=10 cosine constraints. Adding more, with proper
  tail control, costs only solver time, not validity.

## Reproducibility note
Full variable assignments are "available upon request to the author" — NOT in the paper. So the
exact certificate is not public; a re-implementation of the SOCP+dual pipeline would be needed
to reproduce 0.379005 or push it. The method is fully specified, though (Sections 3–5 + appendices).
