# Approach: Monte-Carlo beam search + concentration (probabilistic lower bound)

Spec review: required (reviewer must rule on acceptability of a probabilistic bound)
Status: proposed (round 1) — BACKUP / orthogonal road
Moves: LOWER bound. Numerically can reach ~0.799 (AA2026 claim 0.79970), past
**0.792665992** [H2024] — but the bound is probabilistic.

## Idea (this is the AA2026 road; reproduce + strengthen, do NOT cite their number)

For a sampled pair of length-n uniform binary strings, a **beam search** (width W)
constructs an *actual common subsequence*, whose length `Z` is a genuine (random)
lower bound on `λ_n` for that pair. Average over M Monte-Carlo trials → `Zbar`.

## Why the inequality direction is valid (CRITICAL — must be exactly right)

- LCS length is **superadditive** ⇒ `E[λ_n]/n` is increasing in n and converges
  *up* to `gamma_2`. Hence for every finite n: `E[λ_n]/n <= gamma_2`. So a lower
  bound on `E[λ_n]/n` is a lower bound on `gamma_2`. **This direction is the whole
  game**: a finite-n quantity bounds `gamma_2` from BELOW, never above. (The
  Monte-Carlo *estimate of the constant itself*, by contrast, would be an
  over-estimate via the upper-bound side — do NOT use that framing.)
- Beam search returns *a* common subsequence, so `Z <= λ_n` always, hence
  `E[Z] <= E[λ_n]`. Combined: `E[Z]/n <= E[λ_n]/n <= gamma_2`. A high-confidence
  lower bound on `E[Z]/n` is therefore a valid lower bound on `gamma_2`.
- **Concentration:** `Z in [0,n]`, so by Hoeffding,
  `P( Zbar < E[Z] - t ) <= exp(-2 M t^2 / n^2)`. Picking `t = n·sqrt(ln(1/δ)/(2M))`
  gives, w.p. `1-δ`, `E[Z]/n >= Zbar/n - sqrt(ln(1/δ)/(2M))`. Report
  `gamma_2 >= Zbar/n - sqrt(ln(1/δ)/(2M))` at, e.g., `δ=1e-12`.

## Skeleton

1. Implement beam search producing a valid common subsequence (verify validity:
   it IS a subsequence of both strings) — by tool: direct code + assertion.
2. Run M (≈1e6) trials at n≈1000, record `Zbar` and `min`/`max` — by tool: sampling.
3. Apply Hoeffding with the n-range [0,n]; report the high-prob lower bound — by tool:
   closed-form.
4. (Strengthen vs AA2026) use a *median-of-means* or empirical-Bernstein bound to
   tighten t given low variance, and larger n to lift `E[λ_n]/n` closer to gamma_2.

## Hard step

**Reviewer acceptance of a probabilistic certificate.** Mechanism: the bound holds
only w.p. `1-δ`; it is not a deterministic feasibility certificate. The repo's
rigor rule says "a numerical search result is a conjecture until certified" — a
Hoeffding bound is borderline. This is exactly why AA2026 is starred/unverified.
Secondary hard step: the *validity of the beam-search subsequence* (must truly be
a common subsequence — easy to check per trial) and using the correct range
[0,n] (not a smaller empirical range) in Hoeffding, else the bound is unsound.

## Check

Reviewer re-runs the sampler with a fixed seed, re-verifies each returned object
is a common subsequence, recomputes `Zbar` and the Hoeffding bound. Must decide
whether `1-δ` confidence qualifies as a verified milestone. RECOMMEND: only use
as a fallback, and present as an *independent corroboration* of the DP value, not
the headline certificate.
