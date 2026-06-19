# cjs-increasing-columns-upper — UPPER bound by proving CJS Conjecture 13

**Side / target.** Upper bound. Top-level target: `gr(Av(1324)) <= e^{pi·sqrt(2/3)} ≈
13.001954 < 13.5`. Beats BBEPP2017's record 13.5.

**Strategy (explorer angle D — Lean-fit if the discrete monotonicity is provable).**
Let `S^k_n(1324)` = #{1324-avoiders of length n with exactly k inversions}. CJS12 **Conjecture
13** ("increasing columns"): for all n,k, `S^k_n <= S^k_{n+1}`. CJS12 **Theorem 17**:
Conjecture 13 => `L(1324) <= rho := e^{pi·sqrt(2/3)} ≈ 13.002`. The 132-analogue is *proven*
(each column weakly increasing in n, eventually `p(k)`, with `p(k) < rho^sqrt(k)`); the open
part for 1324 is the approach to the (already identified) limit, not the limit itself.

Plan: prove Conjecture 13 — ideally as an **explicit injection** `Av^k_n(1324) ↪
Av^k_{n+1}(1324)` (append/insert a point preserving inversion count and 1324-avoidance) — or a
usable weakening (monotonicity for `k <= K(n)` plus an independent tail bound on
`sum_{k>K} S^k_n`). Combine with the partition asymptotic => unconditional <= 13.002.

**Holes.**
- **H1 (the hard step)** the increasing-columns monotonicity, as an injection (or weakening).
  Open since 2012, verified numerically — but a clean finite-combinatorial statement, the right
  shape for a machine-checkable injective proof.
- **H2** eventual column value bounded by `p(k)` (CJS Prop 15 / Lemma 16 analogue).
- **H3** `p(k) < e^{pi·sqrt(2k/3)}` (classical Hardy-Ramanujan upper bound) — citable; sum over
  `k <= C(n,2)` gives growth <= rho.

**Lean-fit.** Yes if H1 is an explicit injection; H2/H3 are discrete + a standard partition
bound. Whole argument is combinatorial/algebraic.

**Honest estimate.** Highest-quality landing (a clean conceptual bound at 13.002, and Lean-fit),
but H1 has resisted since 2012 — the riskiest of the upper-bound sketches. Worth fielding for
breadth: an injective proof, even of a weakened bounded-k form, would be a major result. A good
intermediate target for the builder: verify H1 numerically on the triangle to bounded n (cheap,
already known to hold) and search for the injection's combinatorial rule.

**Sketch file.** `constants/30a/certificate/cjs-increasing-columns-upper.py` (runs; holes raise).
