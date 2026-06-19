# Walks2025 — "Pattern avoiding permutations as walks" (arXiv:2512.19462, 2025)

PDF: `pdfs/walks2025.pdf`. Directly the H_BIG paper for the LOWER bound: it is the
most recent and most relevant attempt to push gr(Av(1324)) above 10.271 by a
transfer-matrix / spectral-radius method with a Collatz–Wielandt certificate.

## Method (the cleanest sound lower-bound template)

- Encode an avoider by **inserting a new maximum** one element at a time. State = an
  intermediate (suffix-reduced, standardised) permutation; an edge = one insertion.
  Building an avoider of length n = a length-n walk from the empty state. So
  #avoiders of length n = #length-n walks, and **gr(Av(π)) = spectral radius ρ(M)**
  of the (infinite) adjacency matrix M.
- **Cutoff N** truncates the graph to states of size ≤ N. Walks in the cutoff graph
  are a strict subset of all walks ⇒ ρ(M_N) is an **unconditional lower bound** on the
  growth rate, monotone increasing in N. (Removing states only loses walks — sound.)
- **Collatz–Wielandt certificate (line 678-687).** For ANY nonnegative weight vector
  `w` on the (exact, ungrouped) graph, if `Σ_{τ→π} (1/ρ) w_τ ≥ w_π` for every vertex π,
  then ρ is a valid lower bound on the Stanley–Wilf limit. This is exactly the
  rational CW witness our `transfer-matrix-lower` certifier already implements — it
  applies VERBATIM to the ungrouped insertion-encoding graph. The hard part is NOT the
  certificate; it is getting ρ(M_N) large at feasible N.

## THE decisive negative result for H_BIG (why pure integer machines cap below 10.271)

- For 1324 the exact (ungrouped) graph is "too large for direct computation"; the
  feasible cutoff is only **N = 17**, which yields ρ ≈ **8.18** (line 521-523) —
  *below* the record 10.271, and below even AERWZ's 9.47 / Bevan's 9.81 (those use
  cleverer subclass structure, not a raw cutoff). Vertex count is exponential in N, so
  pushing N high enough to clear 10.271 is computationally infeasible by brute force.
  CONFIRMS round-1's finding: a plain integer insertion/skew machine converges to the
  true ~11.6 too slowly to clear the record at any feasible size.

## The grouped/weighted graph — and why its 10.418 is ONLY conditional (Conjecture 8)

- To shrink the graph they **quotient** 1324-states by `A(n,r)` = (length n, r short
  values = non-right-to-left-maxima). For 132-avoiders this quotient is EXACT (Thm 5–7:
  a bijection of walks, `|A(n,k)| = T_{n-1,k}`, A009766). For **1324** the quotient is
  NOT exact — walks no longer correspond one-to-one (line 931-933).
- Fix: give the edge `A(n,r) → A(m,s)` the **weight `E(n,r,m,s)/|A(n,r)|`** = the
  *fraction* of source-group vertices that have an edge into the target group
  (line 935-942). A walk now contributes the PRODUCT of its edge weights, not 1. This
  is an **average over the group**, chosen to match the stationary distribution
  `w'_π = f(π)/|π|!` of the uniform random walk (f = #short values).
- **Why it is not sound (Conjecture 8, line 998-1000).** The needed inequality is
  `W̃_{n,k}(1324) ≤ W_{n,k}(1324)` (weighted walk-sum ≤ true walk count). It is
  UNPROVEN. Averaging the out-degree can OVERcount some path structures, breaking the
  lower-bound (sub-walk) property. Verified only for `k ≤ 15` (all n) and for the
  diagonal `n=k` up to n=50 against CGZ enumeration. Figure 9 shows `W̃/W` is `< 1` but
  razor-thin (0.998–0.99997) — so the average BARELY underestimates, which makes Conj 8
  plausible but means a SOUND replacement must preserve almost the entire value.
- **Corollary 9 (conditional):** if Conj 8 holds, gr(Av(1324)) ≥ **10.418** (computed at
  n=220 via a rational CW check, so the *number* is certified; only the
  weighted-≤-unweighted step is conjectural). Convergence ~ N^{-3/2}; the method does
  NOT approach the conjectured 11.6 — it plateaus, so even unconditionally it may not
  reach 11.6.

## What this tells the H_BIG hole — the sound-vs-average crux (core takeaway)

A machine's entries become "GF-weighted" precisely when a quotient collapses many
true states into one and the edge weight is an **average** of their out-degrees. An
average is NOT a sound lower bound (Conjecture 8 is exactly the unprovable claim that
this particular average happens to underestimate). To stay sound you must replace each
averaged weight by a **provable per-group MINIMUM** (or any value ≤ the true sub-walk
contribution): `weight(A(n,r)→A(m,s)) := min over π∈A(n,r) of (#edges π→A(m,s))`, or
more sharply a weight `w` satisfying the CW inequality on the EXACT ungrouped graph.
- min-weight quotient = sound but loses growth (how much is unmeasured here — an open,
  computable question; if the min-weighted ρ clears 10.271 it is an unconditional
  record, the single cleanest Lean-fit path).
- The exact ungrouped graph + any rational CW witness is fully sound but caps at ~8.18
  at feasible N.
- So H_BIG's real task = find a quotient/subclass that is BOTH (a) small enough to
  certify and (b) sound (exact, or min-weighted, not average-weighted) and whose ρ
  exceeds 10.271. Conjecture 8, if ever proved (even for the diagonal n=k), would
  immediately give the record 10.418 — that proof is itself a clean discrete target.

## Lean-fit assessment

- The CW certificate (rational witness `w`, check `Σ w_τ ≥ ρ w_π` entrywise) is
  maximally Lean-fit — finite, exact, rational; identical in shape to round-1's certifier.
- The OBSTRUCTION is discrete too: Conjecture 8 is a finite-flavoured inequality
  `W̃_{n,k} ≤ W_{n,k}` on integer/rational walk counts — a combinatorial monotonicity,
  the same SHAPE as CJS Conjecture 13. Proving it (or its diagonal n=k case) is Lean-fit
  in principle and would hand over 10.418 unconditionally.
