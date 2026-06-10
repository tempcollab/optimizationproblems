# C_31a — Chvátal–Sankoff constant (binary alphabet)

$C_{31a} = \lim_{n\to\infty} \mathbb{E}[\lambda_{n,2}]/n$, the normalized expected
length of the longest common subsequence of two uniform random binary strings.

## Status
none

## Bounds
- table: lower = 0.792665992 [H2024, verified] · upper = 0.826280 [L2009]
  (a starred/unverified lower bound 0.79970 [AA2026] exists but is NOT the record to beat)
- held: lower = 0.792665992 · upper = 0.826280   (no independent verification by us yet)

Softer target: **lower bound** (0.792665992). It is a compute-limited finite-window
DP/LP certificate, not an analytic barrier; the numerical estimate of $\gamma_2$ is
$\approx 0.81$, so there is real room above the record.

## Progress log
(none yet)

## Notes
- Lower-bound machinery: Lueker [L2009] finite-window DP + LP-feasibility certificate;
  [H2024] pushed it to 0.792665992 by heavier compute (deeper window, parallel, memory).
- LCS is superadditive ⇒ E[λ_n]/n increases to γ_2, so finite-n averages are valid
  lower bounds (relevant to the Monte-Carlo + Hoeffding route, [AA2026]).
- Two reproducible roads to beat 0.792665992: (A) deeper Lueker/Heineman DP certificate
  (deterministic, gold-standard for the reviewer); (B) Monte-Carlo beam search +
  concentration (cheaper, but probabilistic — reviewer may not accept).
- Literature digests in constants/31a/literature/.
