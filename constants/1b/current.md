# C_1b — Erdős minimum overlap constant

µ = largest C s.t. sup_{x∈[-2,2]} ∫_{-1}^1 f(t)g(x+t)dt ≥ C for all f,g:[-1,1]->[0,1],
f+g=1, ∫f=1. Equivalent to Erdős problem #36 (discrete minimum overlap).

## Status
none

## Bounds
table: lower = 0.379005 [W2022], upper = 0.380868 [SimpleTES 2026]   (gap ≈ 0.0019, 0.49%)
held: (none verified by us yet)

Both README and 1b.md agree on these. Bar to beat:
- LOWER bound: 0.379005 (verified, untouched since 2022) <- softer target.
- UPPER bound: 0.380868 (4 ML teams ground it from 0.380927 -> 0.380868 in 2025-26; ~6e-5
  improvements per paper; extremely hard, explicit-construction side).

## Triage summary (R1, math-explorer)
Continuous optimization constant — tractable, AlphaEvolve-style. NOT pinned, NOT tied to a
famous open problem. Lower bound is the softer target: it is a single 2022 paper using a
convex-program + dual-certificate method, untouched since, while the upper side is saturated
by ML competition.

W2022 lower-bound method = derive necessary properties of M (mass; 2nd-moment identity;
even-cosine Fourier coeffs of M nonpositive; exact f<->M coeff identities) -> minimize ||M||_∞
as a convex QCQP/SOCP over interval-averages w_j,v_j and Fourier coeffs c_k,d_k -> certify by a
verified-feasible DUAL point. Divide-and-conquer over E(M), c_1, d_1 boxes; min over pieces.

Named slack (author's own concluding remarks):
- (a) larger N,T,R / higher precision: near-exhausted ("limit not much larger than 0.379";
  could certify 0.37905 but not 0.3791).
- (b) STRUCTURAL: prove optimal f* is even -> can set h1=h2=q1=q2=0, collapsing nuisance
  dimensions and raising the achievable bound. Conjectured, unproven.
Orthogonal slack: f∈[0,1] used only as ‖f‖_1=1,‖f‖_2^2≤1 — higher-moment/SDP tightening of the
f-coefficient feasible set, and more even-cosine-sign constraints (R>10), are unexploited.

Tractability for a verified milestone THIS run: 6/10. Reproducing/strengthening the W2022
SOCP+dual pipeline (the certificate is NOT public) is itself a logged milestone even short of a
record-break; a record-break is harder and likely needs the symmetry reduction or an SDP.

## Progress log
(none yet — reviewer appends `- R<n>:` lines for verified advances)
