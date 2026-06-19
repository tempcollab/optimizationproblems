# ghr-lemma-lean — machine-checked certificate via the GHR single-set lemma (LEAN line)

**Direction:** lower bound on C_3a. **Record to beat:** 1.1740744 [G2026].
**Borrows:** the winning `(A,d,T)` and exact counts from `alphabet-search-dp`.

## Strategy
3a is **strongly Lean-fit** (explorer's headline reason to pick it): the load-bearing step is
exact integer counting of `|U+U|, |U−U|, max(U)` plus **one rational log inequality** — no
continuum estimate, SDP, or quadrature. Lean's arbitrary-precision `Nat` handles the
astronomical-but-exact counts; the inequality goes through Mathlib's `Real.log` lemmas. A bound
here becomes a `lake build`-green theorem (the gold-standard certificate per CLAUDE.md).

**Design — keep the heavy DP out of the kernel.** The three counts are produced and checked by
the trusted Python DP (`ghr_dp.py`, validated against the record). In Lean:
- **cheap path:** take the counts as `Nat` literals, prove only the final inequality
  `θ(s,diff,q) > 1.1740744`. Already a real machine-checked theorem about the inequality.
- **full path:** additionally re-derive the counts via a Lean `Decide`/computed DP.

Either way the **GHR single-set lemma** is the reusable core to certify into `lemmas/` — once
there, every future `(A,d,T)` sketch reduces to "compute three Nats + one log bound".

## Holes
- **H0 BOOTSTRAP (builder):** create the Lake project at `constants/3a/lean/` (math template),
  pin `lean-toolchain` + Mathlib rev, `lake exe cache get`, `lake build` green. (Heavy install;
  Lean/elan not yet present.)
- **H1 GHR LEMMA:** `C_3a ≥ 1 + log(|U−U|/|U+U|)/log(2 max U + 1)` for finite `U ∋ 0` (the
  projection construction, or imported as the cached lemma). The high-value `lemmas/` entry.
- **H2 EXACT COUNTS:** the winner's `|U+U|, |U−U|, 2 max U+1` as `Nat` (literals from `ghr_dp`,
  or Lean-internal computation).
- **H3 LOG INEQUALITY (load-bearing rigor):** `log(diff/s) − 0.1740744·log q > 0` via a rational
  lower bound (atanh series / extended `norm_num`).

## Hard step
H3 (the rational log inequality inside Lean) and, if taken, H0/H2 if the counts are re-derived
in-kernel (the DP is large). The construction/search itself is done by `alphabet-search-dp`;
this sketch *certifies* its winner.

## Certify
Lean `lake build` green + `#print axioms` showing no `sorryAx`. Depends on
`alphabet-search-dp` producing the winning counts first.
