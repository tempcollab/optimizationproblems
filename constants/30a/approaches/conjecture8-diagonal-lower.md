# conjecture8-diagonal-lower — UNCONDITIONAL 10.418 by proving the diagonal of Walks2025 Conjecture 8

**Side / target.** Lower bound. Top-level target: `gr(Av(1324)) >= 10.418 > 10.271`,
beating BBEPP2017's verified record 10.271. (10.418 is Walks2025 Corollary 9, currently
*conditional* on Conjecture 8.)

**Strategy (explorer Angle B).** Walks2025 forms the weighted quotient of the
insertion-encoding walk graph: states grouped by `A(n,r) = (size n, r short values)`, edge
`A(n,r)→A(m,s)` weighted by the **average** out-degree `E(n,r,m,s)/|A(n,r)|`. The weighted
spectral radius is a sound lower bound **iff** `W̃_{n,k} ≤ W_{n,k}` (weighted walk-sum ≤
true integer walk count) — their **Conjecture 8**, unproven. Their **Corollary 9** needs
only the **diagonal `n=k`**: granting it, the n=220 rational Collatz–Wielandt computation
(already done in the paper, the *number* is certified) yields `gr ≥ 10.418` unconditionally.

This sketch supplies the missing soundness step (the diagonal of Conj 8), turning the
already-computed 10.418 into an **unconditional** bound. We do not re-derive the spectral
value — Walks2025's rational CW witness at n=220 is reproducible; we re-verify it (H4) and
attach the now-proven inequality.

**Why borrow / what's new.** Borrows the CW-certificate shape from `transfer-matrix-lower`
(H4 is the same rational `Σ w_τ ≥ ρ w_π` check the R1 certifier implements). The new content
is purely H3 — a discrete monotonicity proof. Distinct from the sibling Angle-A re-pointing
inside `transfer-matrix-lower` (min-weighted *sound* quotient): Angle A avoids Conjecture 8
by replacing the average with a provable minimum and asks whether ρ still clears 10.271;
Angle B proves the average is sound and gets the named 10.418 directly. Higher payoff, higher
risk — they hedge each other.

**Holes.**
- **H1** `weighted_walk_sum(n,k)` — exact rational `W̃_{n,k}` from the average-weight quotient.
- **H2** `true_walk_count(n,k)` — true integer `W_{n,k}` (insertion walks with k short values).
- **H3 (load-bearing)** `prove_diagonal_domination()` — prove `W̃_{n,n} ≤ W_{n,n}` for **all**
  n by a structural argument (per-walk injection or term-by-term out-degree domination), not a
  finite check. Walks2025 verified n≤50 — that is the base/sanity range, the proof must be
  general. This is exactly the paper's stated open problem, restricted to the diagonal.
- **H4** `assemble_unconditional_10418()` — re-verify the n=220 rational CW witness and restate
  10.418 as unconditional once H3 holds.

**Hard step.** H3. The average out-degree `E/|A(n,r)|`, raised to a product over a walk, must
provably never exceed the true walk count. Figure 9 shows `W̃/W ∈ (0.998, 0.99997)` — razor-thin
below 1, so the domination is true but tight; any slack-free argument must track the product
structure exactly. Mechanism candidate: a measure-preserving injection of weighted walks into
true walks on the diagonal, or convexity/AM–GM on the per-group out-degree distribution.

**Lean-fit.** H1/H2/H4 are finite integer/rational computations + a rational CW check (maximally
Lean-fit). H3 is a combinatorial monotonicity — Lean-fit in shape (same flavour as CJS Conj 13),
genuinely hard in content.

**Sketch file.** `constants/30a/certificate/conjecture8-diagonal-lower.py` (runs; holes raise).
