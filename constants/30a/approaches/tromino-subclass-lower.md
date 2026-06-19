# tromino-subclass-lower — LOWER bound by a staircase-product subclass (domino now, tromino next)

**Side / target.** Lower bound. Top-level target: `gr(Av(1324)) > g > 10.271` from an explicit
gridded staircase subclass with computable algebraic growth `g`. Beats BBEPP2017's 10.271.

**Strategy (explorer angle C/D + outliner B1 — BBEPP's named open route).**
BBEPP (Thm 5.1) grid a subclass `P_k ⊆ Av(1324)` along the descending (Av(213),Av(132))
staircase, decomposed into **dominoes** (2-cell blocks) + single **connecting cells**, with an
exact closed-form count `|P_k| = |B_{14k}|^k · |C_{8k,7k}|^k · C(21k,14k)^{2k-1}` and an
**algebraic** growth-rate limit `81/8 = 10.125`. They flag (§7.4): a lower bound on the growth of
permutations gridded in three consecutive cells (**trominoes**) would, by decomposing the
staircase into trominoes, give a new bound > 10.271 — but "enumerating trominoes seems to require
some new ideas."

## What R2 closed (verified, sound, reproducible)

**Reproduce:** `python3 constants/30a/certificate/tromino-subclass-lower.py` (exit 0; prints the
verified sub-record bound, then the record-beating hole H1 raises as designed).

Reconstructed and certified the **domino Thm-5.1 product** end to end, giving the verified bound

> **gr(Av(1324)) ≥ 81/8 = 10.125** — sound, algebraic, no continuum, no conjecture.

This is `> R1 held 3.773326` (a +6.35 jump on the held axis) but `< record 10.271`.

Two load-bearing obligations discharged in the script:

- **(S2) exact count + growth limit — fully closed.** Component formulas verified: Catalan-forest
  `|C_{n,c}| = (c/n)C(2n-c-1,n-1)` (integer-valued, reduces to `Catalan(n-1)` at `c=1`); domino
  counts `|D_n|` = OEIS A000139 (cache lemma `domino_growth_constant`, gr 27/4). The total point
  count is `N(k) = 36k²` (Θ(k) cells × Θ(k) points). The growth-rate limit
  `lim_k |P_k|^{1/N(k)}` is computed **symbolically (sympy, exact)** and equals **exactly 81/8**;
  the two binomial entropy limits are independently re-checked in log-space at k=4000. The
  soundness chain `gr(Av(1324)) ≥ limsup_k |P_{N(k)}|^{1/N(k)} ≥ lim_k |P_k|^{1/N(k)} = 81/8`
  is spelled out (needs only a subsequence of subclass sizes — no Fekete).

- **(S1) containment — scoped honestly, mechanism shown genuine.** General containment
  `P_k ⊆ Av(1324)` is **BBEPP Thm 5.1 (peer-reviewed), cited** — not re-proved. The script
  replaces an earlier *vacuous* "descending-band" brute check (it avoided 1324 trivially by a
  global descending layout, exercising no interleave constraint — flagged and removed) with a
  **faithful, teeth-having** test: over all small gridded domino fillings, some column
  interleavings *create* a 1324 and some *avoid* it, so the cell-interleave constraint is a
  genuine, non-vacuous restriction (the containment claim is not trivially true).

## Holes remaining

- **H1 (record-beating, OPEN — the genuine new work).** The **tromino (3-cell) analogue**: a
  certified *lower* bound `g3` on the growth of permutations gridded in three consecutive
  staircase cells, then the tromino-decomposition product + ratio optimisation `> 10.271`.
  - *Mechanism (sound, not exact enumeration — sidesteps BBEPP's "new ideas"):* an explicit
    transfer-matrix **sub-subclass inside the tromino** — a finite automaton whose accepted
    gridded fillings are brute-verified 1324-avoiders, with nonnegative integer matrix `M_T`;
    `g3 ≥ ρ(M_T)` certified by the **same exact-rational Collatz–Wielandt witness** as
    `transfer-matrix-lower` / Walks2025 (`M_T v ≥ λ v`, λ rational).
  - *Blocker:* building `T` with `g3` large enough that the tromino product clears 10.271 is real
    work. The R1/R2 lesson (per-role memory) is that *plain integer automata cap logarithmically*
    — so `T` must capture the tromino's extra cross-cell freedom (the analogue of the 14k:8k:7k
    domino balance), not just a skew/insertion truncation, or it will stall like the skew-sum
    machine did at 3.77. The matrix must encode the **interleave freedom between three cells**,
    which is exactly the structure BBEPP couldn't enumerate.
  - *Restated intermediate statement (vs the skeleton).* The skeleton's H2 asked for the *exact*
    tromino count (BBEPP "new ideas"); H1 is reshaped to a **lower bound only** via the CW
    sub-subclass, which is what the strategy actually needs and is achievable in principle.
- **H2' (open, depends on H1).** Assemble the tromino-decomposition exact-count product as a
  function of `g3` and the per-cell point ratios; optimise ratios → growth `> 10.271`. Stubbed
  (`tromino_decomposition_growth`) until H1 supplies `g3`.

## Claim (clearly a claim until reviewer-verified)

Claimed verified lower bound this round: **gr(Av(1324)) ≥ 81/8 = 10.125** (sound subclass,
exact symbolic limit). **Does NOT beat the record 10.271** — it beats the R1 held 3.773326. The
record-beating tromino step (H1/H2') is an explicit open hole.

## What would push it further

1. **Discharge H1** with a CW-certified tromino sub-subclass whose `g3` lifts the product past
   10.271 (the principled lever: 3 cells > 2 cells ⇒ per-block growth > domino's).
2. Alternatively the **richer-single-cell** variant (explorer angle D): keep the 2-cell skeleton
   but replace the balanced-domino cell by a higher-growth *sound* gridded cell with an exact
   Catalan-forest count, then re-optimise the integer point-ratios — same Thm-5.1 product machinery,
   possibly past 81/8 without trominoes.
3. The §6/§7 leaf-relaxation (10.125→10.271) is the **continuum step** and is deliberately NOT the
   road here — it is Lean-hostile.

## Lean-fit

H1 (transfer matrix + exact-rational Collatz–Wielandt) is Lean-fit and shares machinery with
`transfer-matrix-lower`. (S2) is exact rational/algebraic arithmetic + a symbolic limit — Lean-fit
in shape; the one cited analytic input is `θ^{1/n}→1` for balanced dominoes (BBEPP Prop 3.6).

## Promotable lemmas

None new this round. (Reuses cached `domino_growth_constant` and `skew_sum_closure_Av1324`.) The
domino-product growth-limit computation is sketch glue, not a general reusable lemma; do not
promote.
