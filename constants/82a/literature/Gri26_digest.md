# Gri26 digest — Grinsztajn's Zhang–Zagier C82 upper-bound record

**Source.** NOT an arXiv paper. It is a GitHub repository:
`github.com/maaxgrin/zhang-zagier-c82-bound` (commit cb88f92, year 2026), cited in
`references.bib` as `@misc{Gri26}` (Max Grinsztajn). It is code + certification data,
not an exposition. Certifies `mu^ess(h_Z) <= 0.2536331090204145`, the current upper
record (Doche's longstanding 0.25443677 was the previous; our held in-repo cert is
0.2538893183, between the two).

**What it computes.** A DENOMINATOR-FIRST search on the Doche functional written in
complementary coordinates. Value reported as
`(log M(Q) + ∫_0^1 (A−B)^+ ds) / deg Q`, with `A = Σ_i q_i log|P_i(χ)|` (numerator,
LP-tuned over P1..P6,P8) and `B = log|Q(χ)|` (denominator). By Jensen `∫ B = log M(Q)`,
so this equals Doche's `Φ/D = ∫ max(A,B) ds / deg Q` exactly (paper eq.
(samefunctional)). Same surface as Doche; just descended denominator-first.

**The record denominator (deg 140):** `Q = Q1 · Q2 · R0 · R2 · P7 · P9`, where
- Q1,Q2 = the two deg-28 factors of Doche's distinguished block,
- P7 = Flammang j13 (deg 12, = our Q5), P9 = Flammang j15 (deg 16, = our Q6),
- **R0, R2** = two NEW deg-28 "near-cancellation" factors:
  ```
  R0 = primitive_part( Q1 − P1^5 P2^5 P4 · P8 )
  R2 = primitive_part( Q2 + P1^5 P2^5 P4 · P7 )
  ```
  (taken to positive leading coefficient). Full coefficient vectors in the paper's
  Appendix A.

**LP-tuned numerator exponents at the record** (their `targeted_refined` run):
P1 26.5119, P2 23.7828, P3 0.9707, P4 4.5261, P5 0.0383, P6 4.1738, P8 1.6858.

**The search heuristic (how R0,R2 entered).** The repo README does **NOT derive** R0,R2.
It calls them "perturbative factors" with no theoretical justification. The search is a
**finite-family heuristic**: enumerate squarefree denominator products over {Q1,Q2
required; optional R0,R2,P1,…,P9}, subject to deg(Q) ≤ 220 — 2048 candidate denominators
— LP-optimize the numerator for each, rank, and report the best. The README explicitly
warns this is "a heuristic and finite-family check, not a proof that the displayed
denominator is globally optimal." So **R0,R2 were posited by hand** (the near-cancellation
ansatz Q1 − integer-product) and then validated by the LP — exactly the "found by search,
not predicted by theory" gap the generative task targets.

**WHY the ansatz works (this run's finding; see R1-generative-explore.md §1).** R0 is a
degree-preserving COPRIME SIBLING of Q1: same Mahler measure (mean log|R0|=7.11 ≈
log|Q1|=7.09), same root-cloud hugging the active locus, gcd(R0,Q1)=0, irreducible,
R0(0)=R0(1)=1 (admissible). The bridge P1^5 P2^5 P4 is engineered to be exponentially
small on the active bulk of Ω (|Q1|/|bridge·P8| ~ 23× there) yet comparable in Q1's
deepest wells (ratio ~3.65), so R0 ≈ Q1 on the bulk (inherits Q1's firing reduced cost
r_Q ≈ −0.069) while its deep-well roots are displaced enough to make it a fresh,
independent admissible block. Exponent a=5 is the largest keeping deg = 28 (bridge·P8
has deg 26 < 28). R2 = same on Q2 with sign flip + tail P7 (so R2 ⊥ R0). The criterion
fires on R0,R2 because they copy Q1,Q2's reduced cost — NOT because |R0| is small on Ω
(it is not; the "best small-on-Ω approximation" reading is wrong).

**Status vs our work.** The paper's Prop. 6 diagnoses (after the fact, on a fine grid)
that all six denominator blocks fire by `r_Q < log h`, R0,R2 included, while controls
stay inert — explanatory, not generative. A rigorous interval certificate of the Gri26
deg-140 bound IN OUR harness is a separate open milestone (would upgrade the diagnostic
to a certified statement). No in-repo bound depends on the Gri26 numbers.

**Reproduce.** `python3 constants/82a/certificate/firstvar_07_record_blocks.py`
(reproduces the functional identity, firing margins Table 2, and stationarity cluster);
`scratch/probe{1,2,3,4}_R0R2.py` (the sibling-generator mechanism).
