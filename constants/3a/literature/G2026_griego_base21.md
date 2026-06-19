# [G2026] Griego — base-21 digit construction (RECORD, C_3a ≥ 1.1740744)

Source: GitHub PR teorth/optimizationproblems#71 (MERGED, approved by teorth). Full PR
body saved reasoning; verification script reproduces exactly (ran here in ~23s).

## The construction (this is the artifact to beat)

Single set U of non-negative integers containing 0, then GHR lemma:
  C_3a ≥ 1 + log(|U−U|/|U+U|) / log(2·max(U)+1).

Parameters: digit set A = {0,2,3,4,5,6,7,8,9,10} (NOTE: digit 1 is DROPPED), base B=21,
d=80 digits, digit-sum cap T=150.
  U = { Σ_{i=0}^{79} a_i·21^i : a_i ∈ A, Σ a_i ≤ 150 }.

Exact values (certified):
- max(U) = 10·Σ_{i=65}^{79} 21^i  (≈ 2.9958e105)
- |U+U| = 75448362167176243488362019935078206851619643198150854886920234689186981134888
- |U−U| = 195351744295266763842135520514417052287242446785296742323733058216909095059024572338564089814415
- value = 1.174074447693521163363531806658755676... (conservative bound 1.1740744)

## Why it is a VALID bound (injectivity / no carries)

- Sums: every digit-sum lies in [0,20] < base 21, so U+U has NO CARRIES → g injective on U+U.
- Differences: difference digits c_i ∈ [−20,20]; if Σ c_i 21^i = 0 then mod 21 forces c_0=0,
  induction gives all c_i=0 → g injective on U−U.
- CRITICAL VALIDITY CONSTRAINT: base must be > 2·max(A) = 20, i.e. base ≥ 21. Base 20 with
  this digit set is INVALID (verified by brute force: carries collide, DP overcounts |U+U|).

## The exact counting certificate (reproducible, fast)

Two DPs over digit positions (in Griego's verification script, reproduced here):
- sum_count: state = (running digit-sum total_y, bitset of achievable Σa_i values),
  transitions over sum-digits y∈A+A using P_y={a∈A: y−a∈A}; feasible iff one can pick
  a_i∈P_{y_i} with Σa_i≤T and Σ(y_i−a_i)≤T. Bitset shifts encode the Σa_i constraint.
- diff_count: state = (left=Σ q_{δ_i}, right=Σ(q_{δ_i}+δ_i)), where q_δ = min{b∈A: b+δ∈A};
  feasible iff left≤T and right≤T.
- Final log-ratio certified with directed-rounded ln via atanh series (ln_bounds, M=120 terms),
  margin > 0 proves 1.1740744 rigorously. Interval width ~2.35e-115.

## Lean-fit assessment

The counting step is FINITE EXACT INTEGER COUNTING (two DPs producing exact bignums) — discrete
and algebraic in spirit. The only continuum piece is the FINAL comparison
log(d/s) vs c·log(q), handled by a rational interval bound on ln (rigorous, finite series with
explicit remainder). So this is Lean-fit-ADJACENT: the DP counts are integers a Lean proof could
certify by evaluating/`decide`-style or by a reflected computation; the ln-comparison is a rational
inequality on truncated atanh series. In practice for round 1 the natural certificate is the
PYTHON exact-integer DP + directed-rounded ln (the existing reproducible certificate), and Lean is
optional/heavy. Keep as a Python exact certificate unless a later round wants the gold-standard.

## Key insight that makes this beat the asymptotic optimum

The simplex family W(m,L,B) with CONTIGUOUS digits {0..B} caps at θ0=1.173077 (Zheng's
asymptotic optimum, B=5). Griego beats it by SCULPTING the digit set — dropping the digit 1 from
{0,1,...,10} (and using a tight digit-sum cap T). Dropping digit 1 makes A−A "sparser near 0"
relative to A+A, raising |U−U|/|U+U|. This is OUTSIDE the W(m,L,B) family the asymptotic theory
covers, which is exactly why it exceeds 1.173077.
