# Approach: Exact / certified Lueker–Heineman DP feasibility certificate

Spec review: required
Status: proposed (round 1)
Moves: LOWER bound. Aiming strictly past **0.792665992** [H2024].

## The machinery (verified against L2009 + H2024 arXiv:2407.10925 html)

Lueker's lower-bounding method (binary, d=2) is a value iteration on a vector
**w** indexed by pairs of length-ℓ suffix windows over {0,1} (so `2^(2ℓ)`
coordinates). The Bellman recurrence (H2024 eq. 2.4) is

```
w_n[A] >= b(A) + max_{z in {0,1}} F_z(w_{n-1}, w_{n-2}, A)
```

where `b(A)=1` if both strings of the pair `A` start with the same character,
else 0; `F_z` removes leading characters from the strings not starting with `z`
and averages the appended uniform random characters.

**The certificate (the load-bearing object).** A *feasible triplet* `(u, r, eps)`
— a potential vector `u` and scalars `r, eps` — satisfying the componentwise
inequality

```
F( u + r·1 , u )  >=  u + (2r - eps)·1            (feasibility, "(2.4)-type")
```

By **Lemma 2.1** (monotonicity + translation-invariance of `F`), feasibility
forces `v_n >= u_0 + n(r - eps)·1` for every n. Combined with
`gamma_2 = lim_n W_{2n}/n` (existence by Fekete/superadditivity, [CS1975]),
this yields

```
gamma_2 >= 2(r - eps).
```

**Inequality direction — why this is a LOWER bound on the LIMIT (not finite n).**
The chain is: (feasibility inequality, one-sided) ⇒ (Lemma 2.1: the true
expected-LCS iterate `v_n` grows at least linearly at rate `r-eps` *for all n*)
⇒ (the per-step rate of `v_n` is a lower bound on the asymptotic rate, because
the limit `gamma_2 = lim W_{2n}/n` exists and the linear lower envelope persists
to the limit). It is NOT "a finite-n average ≤ gamma" — that is the *Monte-Carlo*
direction (superadditivity: `E[λ_n]/n ↑ gamma_2`, so a finite-n estimate is a
lower bound on gamma_2 but an *over*-estimate is impossible by that route). Here
the DP certificate bounds the limit *from below* directly via the feasible
potential, with no probabilistic content. Getting this backwards voids the bound.

## Why H2024 left exploitable slack

From the H2024 html: they run value iteration in **floating-point (fp32/fp64),
no exact arithmetic, no interval/rounding certificate**, and the reported number
is "rounded down to the 6th decimal." Two consequences:

1. The reported `0.792665992` is a *float* read off iteration, not a verified
   feasible triplet. Re-deriving an exact feasible `(u,r,eps)` is itself a
   reviewer-grade contribution (gold-standard reproducible certificate).
2. Rounding the rate down to 6 decimals discards slack — the true feasible value
   at their depth may be slightly higher; but capturing that requires their ℓ=20
   vector, which is ~4.4 TB and **out of one-round reach** (see memory table).

## Skeleton

1. Implement the binary d=2 recurrence `F` and value iteration at a window depth
   ℓ that fits in RAM — by tool: direct numpy implementation; verify convergence
   `v_{n+1}-v_n -> r·1` and that the recovered rate matches Lueker's published
   value at that ℓ (cross-check, e.g. ℓ small reproduces ~0.77–0.79 range).
2. Apply complementation + pair-swap symmetry to halve/quarter the state space
   — by tool: index canonicalization, confirm identical fixed point.
3. Extract a near-optimal potential `u` (the converged iterate), snap to rationals
   with a small denominator, and **recompute `eps` exactly** so the feasibility
   inequality holds componentwise in exact rational arithmetic — by tool:
   Python `fractions`/`gmpy2`, single pass over all coordinates.
4. Report `gamma_2 >= 2(r - eps)` as an EXACT rational lower bound and a
   reviewer script that re-checks the componentwise inequality.

## Hard step

**Reaching a depth ℓ whose certified value exceeds 0.792665992 while the state
space still fits in RAM.** Mechanism/obstruction: the certified rate is monotone
increasing in ℓ but H2024 needed ℓ=20 (≈4.4 TB, HPC external memory) to hit
0.7927; depths that fit in this container's RAM (ℓ≤~15–16, ≤~17 GB even with
2× symmetry) cap the *certified* bound BELOW the record. So on its own this
angle yields a **fully verified reproduction at a sub-record value** (a
verified-progress milestone) — NOT a record-break — unless paired with the
compression in the companion doc to push ℓ to ~17–18 in RAM.

## Check the builder runs

A standalone script that loads `(u, r, eps)` (exact rationals), recomputes
`F(u+r·1, u)` componentwise, asserts `>= u + (2r-eps)·1` everywhere, and prints
`2(r-eps)` as an exact fraction and a rigorous decimal lower bound. The reviewer
re-runs it; no float trust required.
