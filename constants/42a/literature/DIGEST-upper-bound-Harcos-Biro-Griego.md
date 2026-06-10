# Upper-bound method for C_42 (Harcos 0.69368; Griego 0.6906538*)

## The constant
C_42 = limsup_n R_n,  R_n = min_{max_i|z_i|=1} max_{1<=k<=n} |sum_i z_i^k|.
Equivalent to Erdős problem #519. README & 42a.md agree: verified lower 0.5, verified upper 0.69368.

## The construction behind every modern upper bound (Biró [Bir00], Harcos, Griego)
All upper bounds since Biró [Bir00] use the SAME generating-function / Newton-identity
machinery. The full mechanism is laid out (and reproduced) in the Griego note
`griego-repo/notes/turan_42a_improved_upper_bound.md`. Skeleton:

1. **Prescribe the power sums S_k = Q_k = sum_j y_j^k** (k=1..n) instead of the roots.
   This is legal: given target power sums S_1..S_n there is a monic degree-(n-1)
   polynomial p_n(Z)=Z^{n-1}+b_1 Z^{n-2}+...+b_{n-1} with roots y_2..y_n, plus a forced
   root y_1=1, whose power sums (with y_1) equal S_k for 1<=k<=n. The b_l satisfy a
   triangular Newton recursion in the S_l, and Q_k=S_k holds for 1<=k<=n PROVIDED b_n=0.
2. **Rescale** z_j = y_j / Λ_n with Λ_n = max_j |y_j| >= 1 (since y_1=1). Then
   max|z_j|=1 and sum_j (z_j)^k = Λ_n^{-k} S_k, so |sum z_j^k| <= |S_k| <= C if every
   |S_k|<=C. Hence R_n <= C. This is the load-bearing inequality: **if you can choose
   power sums S_1..S_n with all |S_k|<=C AND b_n=0, then R_n<=C.**
3. **Two-block (now three-region) choice of the S_k.** Generating function
   B(z)=sum b_l z^l = (1-z)^{-1} exp(-sum_{m>=1} S_m z^m/m). Choosing S_m equal to a
   constant s=1-α on an initial block B_n={1..A_n} makes B(z)=(1-z)^{-α}·(corrections),
   so b_l ≈ β_l = (α)_l/l! (rising factorial). Middle block J_n uses S_m=η; final block
   F_n={n-A_n..n} carries free values used to enforce b_n=0 with |S_m|<=C.
4. **The b_n=0 condition becomes an analytic inequality.** With A_n=⌊τn⌋ and τ>1/3,
   correction terms of order >= 3 cannot reach degree n, so b_n is linear+quadratic in
   the corrections. After normalizing by Γ(α)n^{1-α}, the discrete sums converge to
   integrals:
     K = I_α(τ) = ∫_0^τ u^{α-1}/(1-u) du,
     D = I_{Re α}(τ)  (the |·| version, real),
     A1 = ∫_τ^{1-τ} u^{α-1}/(1-u) du,
     A2 = 2∫_0^{1-2τ} u^{α-1}/(1-u) log((1-τ-u)/τ) du.
   Set Y = 1 - w·A1 + (w^2/2)·A2 + s·K, where s=1-α, w=η-s. The free final block can
   realize b_n=0 with all |S_m|<=C **iff** the limiting feasibility inequality
     **|Y| <= C·D**
   holds. So the whole problem reduces to: minimize C subject to existence of
   (α, η, τ) with |1-α|<C, |η|<C, and |Y(α,η,τ)| <= C·D(α,τ).

## What Harcos got: C = 0.69368
Harcos (reported in Biró [Bir00]) optimized this construction to C ≈ 0.69368. This is the
**verified record upper bound** (the bar). The 5/6 in the table is Biró's earlier weaker
version of the same idea.

## What Griego claims: C = 0.6906538* (NOT verified — not the bar)
Griego re-optimizes the SAME inequality with explicit rational
τ=0.36988243, α=(61927309+57623741i)/1e8, η=(59839764-34485185i)/1e8, C=3453269/5000000.
The repo's exact rational-interval verifier (`scripts/verify_42a_certificate.py`) PASSES
(I ran it: all checks PASS, certified gap |Y|^2 < C^2 D^2 with exact rational margin
3875.../25e132 > 0; comparison gap to 0.69368 ≈ 1.55e-7). BUT:
- **It is asymptotic only**: "no explicit finite threshold N is provided." The verifier
  checks the *limiting* inequality |Y|<CD, not R_n<=C for any concrete n. The asymptotic
  reduction (coefficient asymptotics β_l = l^{α-1}/Γ(α)(1+O(1/l)), Riemann-sum limits,
  floor-error lemma, termwise integration tail bounds) is argued in prose in the note,
  NOT machine-verified.
- Listed as `0.6906538*` (starred/unverified) in 42a.md. Per run_state rules this is NOT
  the value to beat; the bar is Harcos 0.69368.

## Where the slack is on the upper side
- The reduction min C s.t. |Y(α,η,τ)|<=C·D(α,τ) is a smooth 5-real-parameter optimization
  (α∈C, η∈C, τ∈R). Harcos found 0.69368; Griego pushed to ~0.69065 — only ~1.55e-7 from
  the bar after optimization, suggesting this two/three-block ansatz is near its floor.
- Genuine slack would need a RICHER ansatz: more than two interior blocks (piecewise-
  constant S_m with k pieces → k complex params), or a continuously varying S_m profile
  S(t) for t=m/n giving a calculus-of-variations problem for the optimal profile. Cheer-
  Goldston numerics suggest the true value is ~0.7, so the optimal limsup may be ABOVE
  0.69065 — i.e. the upper bound cannot drop much further and a too-aggressive C is simply
  infeasible. The construction's own floor likely sits near 0.69.
