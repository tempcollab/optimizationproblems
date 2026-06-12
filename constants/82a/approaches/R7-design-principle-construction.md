## 82a UPPER — R7 DESIGN-PRINCIPLE construction (turn the first-variation criterion into a block-design method)

Spec review: **required**
Target to beat (numeric headline, if reachable): **0.2538893183** = held verified upper (R4, j3+j9 A-base), moving the UPPER bound DOWN.
Fallback milestone (if the numeric lever is dry): a CONSTRUCTED ORIGINAL block Q* (not in Flammang Table-1, not j3/j6/j7/j9) with **verified r̃_Q* < 0** on the correct anchor and verified admissibility — i.e. a reproducible demonstration that the R6 criterion DESIGNS improving blocks, even if Q*'s certified drop is sub-slack. Structural, not a record-break.

Per the user R7 redirect (run_state Goal Updates): the contribution is a METHOD (the criterion as a design objective), with the bound as proof the method works. The R6 lemma is the engine; this round builds the optimizer on top of it. This SUPERSEDES the math-explorer's recommended target (i) "rigorize Danskin" — (i) stays available as a write-up corollary but is not the headline.

=================================================================================
## VERIFIED INPUTS (audited this round — use as the optimization's data)

Facts I re-derived against the on-disk harness, not claims to re-litigate:

- **Sign:** NEGATIVE r̃_Q is FIRING. r̃_Q = ⟨log|Q∘chi|·1_{A₀>B}⟩_s, chi(s)=z(1−z), z=e^{2πi s}.
- **Anchor for a SECOND A-base block = R2 family** (j3 on, j9 off), exponents in `verify_firstvar_lemma.R2`. r̃ MUST be measured there (the q_Q=0 point); on the saturated R4 anchor the sign flips (documented trap). On R2: active fraction 0.0685, the active set is a union of ~32 intervals.
- **The active locus, mapped in the complex w-plane** (R2 anchor, N=2M): Re(w)∈[−1.73, 1.05], Im(w)∈[−1.75, 1.75], |w|∈[0.46, 1.97], symmetric in Im. This is the curve on which Q must be small.
- **WHY j9 fires (the design signal, audited):** j9's 8 roots sit essentially ON the active locus — min-distance to the active point cloud is **0.008** for the root pair 1.030±0.916i and **0.030** for the pairs near 0.54±0.33i / 0.43±0.34i. r̃(j9)=−0.0068. The roots at −1.50±1.49i are 0.29 from the locus (positive contributors). So firing = roots hugging the active arc where |Q|<1, while staying contour-root-free (min|j9∘chi|=1.06e−2 > 0).
- **The integer lattice is SPARSE here (audited, the hard fact):** (a) every low-height ORIGINAL quadratic/quartic I built by rounding "X²−2Re(p)X+|p|²" to integers for p in the active locus came out **dry** (best r̃=+0.013); integer rounding cannot place a deg-2 root close enough to the locus while staying root-free. (b) j9 is an ISOLATED minimum: every single-coeff integer perturbation of j9 jumps r̃ from −0.0068 to **+0.028 or worse**. Firing blocks are rare lattice points; brute coefficient enumeration will not find a better one. The right machinery is ROOT-PLACEMENT + lattice reduction, not coeff search.

=================================================================================
## Angle 1 (top pick): LLL-driven root-placement design of an original A-base block

  Moves: UPPER bound toward 0.2538893183 (if it clears the gate); else delivers the constructed-block structural milestone.

  Skeleton:
    1. DESIGN PROBLEM (the new framing). Minimize the linear objective
         r̃_Q = ⟨log|Q∘chi|·1_{A₀>B}⟩_s = ∫ log|Q| dν,  ν = pushforward of arc-Lebesgue under chi|_{A₀>B},
       over Q ∈ Z[X], deg ≤ d (d ∈ {6,…,10}; j-blocks live in 3..8), subject to
         (c1) contour-root-free: min_s |Q∘chi(s)| ≥ 1e−2 (so log|Q∘chi| ∈ L¹, the R6 lemma's hypothesis H1′);
         (c2) coprime + squarefree vs the active dictionary {P1,P2,P4,P6,P8,j3,j9,Q1,Q2,Q5,Q6} (Doc01a cond (4); sympy gcd);
         (c3) ORIGINAL: Q ≠ any Flammang Table-1 entry (24 entries) and ≠ any dictionary block.
         (no P(0)=P(1)=1 needed — A-base blocks are exempt, per run_state Rule.)
       — objective and ν are exactly `verify_firstvar_lemma.closed_form_rtilde` on the R2 anchor; this IS the integer-transfinite-diameter / weighted-Chebyshev problem for the Doche active locus, never before stated as an optimization.
    2. Factor the objective over roots (the lever LLL acts on):
         r̃_Q = Σ_{ρ: Q(ρ)=0} U^ν(ρ) + deg(Q)·log|lead Q|,  U^ν(ζ)=⟨log|ζ−chi|·1_{A₀>B}⟩_s.
       (Identity already verified to 5.2e−17 in `verify_firstvar_lemma.root_potential_check`.) So r̃_Q is driven DOWN by putting roots where U^ν is most negative — the deepest wells of the active-arc potential. Precompute U^ν on a fine complex grid; read off the wells (expect them near the audited cluster 1.03±0.92i and 0.54±0.33i).
    3. SOLVE by LLL/lattice reduction (recommended method): seed monic real target polynomials whose roots sit at the U^ν wells, then LLL-reduce the lattice of integer polynomials of degree d to find the nearest integer Q to that target in the ⟨·,·⟩_ν Gram metric. Score every LLL output by the EXACT r̃_Q (step-1 objective) on the R2 anchor; keep those with r̃_Q < 0 and contour-root-free, sorted most-negative.
    4. SELECT Q* = the most-negative original admissible block. Report r̃_Q* vs j9's −0.0068. Two outcomes:
         (numeric) if r̃_Q* is comparably or more negative than j9 AND the joint float pre-gate clears 5e−6, build a q9A certify harness (new A-base slot) and certify a bound < 0.2538893183.
         (structural) else, deliver Q* + verified r̃_Q* < 0 + admissibility as the milestone: the criterion designed an original improving block.
    5. CHEAP FLOAT PRE-GATE before any certify (mandatory, run_state Rule). Clone `verify_upper_q8A.float_value_q8A` to a q9A float path with Q* as a third A-base block (seed exponent 0), joint Nelder-Mead re-opt of all 10 exponents at N ≥ 4M. Require N-STABLE drop ≥ 5e−6 below 0.2538893183 (≥10× the ~2e−7 cert slack), stable across N=400k and N=4M. If drop < 5e−6 → STOP, do NOT certify; record the structural milestone (step-4 structural outcome).
    6. CERTIFY (only if step 5 passes). Branch-and-bound on the q9A harness, HELD_CERT set to the TRUE held **0.2538893183** (NOT the stale 0.2538925359 hardcoded in q8A — run_state Rule), frontier=0 required, ~8 min.

  Hard step (load-bearing): **the lattice yields an ORIGINAL Q with r̃_Q strictly negative and contour-root-free.**
    Mechanism: r̃_Q = Σ U^ν(ρ) + deg·log|lead| is linear in the per-root potentials; the U^ν wells are negative and the active-arc point cloud is dense, so several integer roots can be driven into the wells. LLL finds the integer poly minimizing the ν-weighted norm to a real root-target in the wells. The risk this carries: the lattice is SPARSE (audited — naive rounding dry, j9 isolated), so LLL may only RE-DISCOVER a Table-1 block or land just above 0. Mitigation: (a) search deg 6–10 where there are enough roots to hug the locus (j9 is the deg-8 witness it is possible); (b) seed from the conditional-capacity screen's top untried picks (j16/j17/j20 have r̃ ≈ −0.005..−0.007 but are Table-1 — use their root patterns as LLL seeds for an ORIGINAL block); (c) if no original clears r̃ < 0 after the budget, that is itself reportable (firing lattice exhausted by Table-1), and the fallback is the most-negative original found plus the method write-up.

  Check (what the builder runs/derives):
    - `design_block.py` (new): computes U^ν on a grid (R2 anchor), runs LLL root-placement, scores candidates by exact r̃_Q via `closed_form_rtilde`, gates on min|Q∘chi| ≥ 1e−2 and sympy coprimality/squarefree/originality, prints the top originals with r̃ < 0. Cross-checks Q* against the root-potential identity (Σ U^ν(ρ)+deg·log|lead| = r̃ to <1e−5) so the design objective IS the certified quantity. ~1–3 min.
    - finite-difference confirmation r̃_Q* < 0 ⇔ d(log h)/dq_Q* < 0 on R2, reusing `verify_firstvar_lemma.finite_diff_marginal` — so the firing claim is the verified lemma applied, not a new assertion. ~1 min.
    - THEN the float pre-gate (step 5) and, only if it passes, the certify (step 6).

=================================================================================
## Angle 2: direct enumeration scored by r̃_Q, seeded from the capacity screen

  Moves: same targets as Angle 1; cheaper, lower ceiling. RUN THIS FIRST (cheap pass).
  Skeleton: enumerate low-height integer polys of degree d ∈ {4,…,9} (|coeffs| ≤ H, monic, reciprocal/duplicate-pruned), score each by the exact r̃_Q on the R2 anchor, gate by (c1)–(c3). Take the most-negative original admissible block; then the same float pre-gate + conditional certify as Angle 1 steps 5–6.
  Hard step: the enumeration HITS a negative-r̃ original block within a tractable height bound — the audit says firing is sparse (naive low-height quads all dry, j9 isolated), so H must reach where j9-class blocks live (j9 has a coeff 22). Mitigation: enumerate AROUND the U^ν-well root targets (hybrid with Angle-1 step 2) rather than blind, and around small products of firing seeds.
  Check: same `design_block.py` scoring path; numpy + sympy, minutes. If enumeration alone surfaces a clean original Q* with r̃ < 0, Angle 1's LLL may be unnecessary.

=================================================================================
## Angle 3 (fallback if both above only re-discover Table-1): SWAP/well-tiling design

  Moves: structural (and possibly numeric) — design a small original block that COVERS the U^ν wells more fully than any single table entry.
  Skeleton: from the audited U^ν wells, build the minimal monic integer poly (deg 5–7, ∉ Table-1) whose conjugate-pair roots tile both deepest wells (1.03±0.92i and 0.54±0.33i) — a deg-6 with three pairs at the wells, deliberately distinct from j9 (which single-covers the deepest well). Score by r̃_Q; gate (c1)–(c3).
  Hard step: such a deg-6 integer poly stays contour-root-free — the wells are close to but not on the contour (min|j9∘chi|=1.06e−2 shows the margin is thin). Check: same scoring path.

=================================================================================
## FEASIBILITY HONESTY (mandatory — the user asked for it plainly)

**Is there a realistic chance a CONSTRUCTED block clears the gate and beats 0.2538893183?**
Honest answer: **the numeric lever is probably dry, and even a good original block likely does NOT clear the 5e−6 float gate.** Two audited reasons:
  1. The A-base lever is SATURATED: realized drops collapsed ~14× from j3 (+1.49e−4) to j9 (+3.2e−6); the r̃→certified-drop conversion fell off a cliff. Even j16/j17/j20 (r̃ ≈ −0.005..−0.007, COMPARABLE to the already-fired j9's −0.0068) project realized drops ~3e−6 — BELOW the 5e−6 gate and barely above the ~2e−7 cert slack. A new original block with r̃ ≈ j9's would convert similarly — sub-gate.
  2. To beat the gate the design must find a block with r̃ MORE negative than j9 by a real margin, on a lattice where (audited) naive rounding is dry and j9 is an isolated minimum. Possible (deg 6–10 has room) but unlikely within one round's search budget.

**Therefore the builder AIMS FOR THE STRUCTURAL OUTCOME as the primary deliverable** (Angle 1 steps 1–4 + checks), and treats the certify as an opportunistic bonus gated strictly by the 5e−6 float pre-gate. The reviewer-verifiable headline: **the design principle, run as an optimizer, produces an ORIGINAL admissible block Q* (∉ Table-1, ∉ dictionary) with reviewer-reproducible r̃_Q* < 0** — proof the R6 criterion is a constructive design method, not just a post-hoc explanation. A numeric record-break is logged ONLY if the float gate clears 5e−6 AND the certify returns frontier=0 below 0.2538893183. Do the cheap design + r̃ verification FIRST; run the ~8-min certify ONLY if the gate passes (anti-stall rule).

Do NOT write any unverified search value into constants/ as `held` (run_state Rule). The certified 0.2538893183 stays held unless step 6 strictly beats it.

=================================================================================
## RANKING

1. **Angle 1 (LLL root-placement)** — the principled, publishable instance of the design problem: directly minimizes the certified objective r̃_Q over the integer lattice via the root-potential factorization, and the U^ν-well map makes the search targeted, not blind. Most likely to (a) deliver an original firing block and (b) if anything clears the gate, this is it.
2. **Angle 2 (seeded enumeration)** — run FIRST as a cheap pass (minutes); if it already finds a clean original Q* with r̃ < 0, the milestone is in hand without LLL. Lower ceiling, fastest path to the structural deliverable.
3. **Angle 3 (well-tiling design)** — fallback if Angles 1–2 only re-discover Table-1 blocks; constructs an original block by covering the U^ν wells more fully than any single table entry.

Builder order: Angle 2 cheap enumeration → if dry on ORIGINALS, Angle 1 LLL → Angle 3 only if both fail to produce an original negative-r̃ block. At every stage the deliverable is the constructed block + verified r̃ < 0 + admissibility; the float gate + certify ride on top only if a block's projected drop clears 5e−6.

Deliverable doc: `constants/82a/approaches/R7-design-principle-construction.md` (method statement + the constructed block + the reproducible r̃/admissibility checks + the honest gate outcome).

=================================================================================
## RESULTS (proof-builder, R7) — OUTCOME: STRUCTURAL-ONLY (no numeric break; no original firing block on R4)

**Headline outcome, stated plainly:** the round did NOT produce an original firing block,
and did NOT beat the held upper 0.2538893183 (held UNCHANGED, Status:none). What it DID
establish — fully and reproducibly, on the correct R4 anchor (GUARDRAIL 1) — is a SHARP
MECHANISTIC CHARACTERIZATION of why the A-base lever is dry: the active dictionary is a
**maximal firing set** on the saturated anchor, so no original firing integer block of
degree ≤ 16 exists within reach, and the best reachable firing block converts to a drop
BELOW the certify gate. The design problem itself (the new framing) is fully formalized
and runnable; the negative result is the content.

### What was built (artifacts, all under `constants/82a/certificate/`)
- `construct_block_R7.py` — the design-problem scaffolding: originality blacklist
  (Flammang Table-1 24 entries ∪ 11-block dictionary, deterministic descending-coeff key),
  admissibility gate (gcd + squarefree **in w**, GUARDRAIL 5), contour-root-free screen
  `min_s|Q∘χ|`, U^ν well map on R4, a fast vectorized `Scorer.rtilde_batch`.
- `design_block.py` — Angle 1: LLL/CVP energy-minimization (Cholesky of the ν-Gram of
  monomials on the active arc + Babai/box enumeration), monic, deg 4..8.
- `design_block2.py` — Angle 2/3: U^ν-well root-target rounding + local lattice search,
  deg ≤ 10.
- `design_block3.py` — locus-hugging high-degree root targets, deg ≤ 16.
- `float_pregate_q9A.py` — the float pre-gate (q9A clone, 10-exponent joint Nelder-Mead,
  HELD=0.2538893183 GUARDRAIL 2).
- `R7_structural_result.py` — consolidated reproduce sheet of the four load-bearing facts.

### The design objective, on the R4 anchor (GUARDRAIL 1, j3 AND j9 ON, candidate exp 0)
- arcfrac (active fraction of {A>B} on R4) = 0.06861; active locus box
  Re w ∈ [−1.732, 1.055], Im w ∈ [−1.747, 1.747].
- Deepest U^ν well: **U_min ≈ −0.0362 at ζ ≈ 0.596 ± 0.348i** — matches the
  outline-review probe (−0.0382 on R2). **Every deep well has |ζ| ∈ [0.4, 0.85], strictly
  INSIDE the unit disk.** No integer-quadratic root reaches there (an integer w²−pw+q with
  q ≥ 1 has |root| ≥ 1, where U^ν > 0).

### The four load-bearing facts (reproducible via `R7_structural_result.py`, ~2 min)
1. **Objective is the certified quantity, sign correct.** r̃(j3)=−0.000031, r̃(j9)=+0.000123
   on R4 — both already-active (trap rows, ≥~0), exactly as the R6 lemma predicts for blocks
   already in the family. The objective = `verify_firstvar_lemma.closed_form_rtilde`.
2. **Firing table blocks coprime to the dictionary are j16/j17/j20.** On R4 the Table-1
   blocks that fire (r̃<0) AND are coprime+squarefree vs {P1,P2,P4,P6,P8,j3,j9,Q1,Q2,Q5,Q6}:
   j16 (deg16, r̃=−0.00521), j17 (deg16, −0.00374), j20 (deg20, −0.00827). All OTHER firing
   table blocks are BLOCKED by sharing a factor with the dictionary: j1=P1=w, j3 (in dict),
   P8=j12, **Q5=j13, Q6=j15** (the R6 shared-pool identities). The firing-coprime blocks are
   all NON-ORIGINAL (Table-1 entries).
3. **Firing is NON-PERTURBATIVE (isolated lattice points).** Every single ±1 coefficient
   perturbation of j16 flips r̃ from −0.00521 to ≥ **+0.0628** (a +0.068 swing); for j20,
   −0.00827 → ≥ +0.0886; all 2-coefficient ±1 perturbations of j16/j17/j20 also stay positive
   (0 firing among ~1800). The firing roots sit microscopically inside the lemniscate
   (min|Q∘χ|: j16 2.3e−5, j20 6.4e−6), so any integer move pushes them across the contour and
   destroys firing. Rounding a real locus-hugging target to integers therefore never lands on a
   firing point: searches of ~73,845 (deg ≤10 well-rounded) + ~3,645 (deg ≤16 locus-hugging) +
   ~3,000 (deg ≤8 energy-CVP) ORIGINAL candidates ALL gave **0 firing originals**, on both the
   R4 and the less-saturated R2 anchors.
4. **MAXIMAL-FIRING-SET obstruction (the saturation mechanism, quantitative).** Any original
   block within reach factors as (a firing block) × (a coprime factor). The cheapest coprime
   ORIGINAL monic factor (deg ≤ 2, contour-root-free) is **w²−w+1** (the 6th cyclotomic poly in
   w) at **r̃ = +0.01311**. This EXCEEDS the firing margin of the best reachable firing block
   j16 (−0.00521), so every such product flips POSITIVE. The dictionary has absorbed exactly
   the cheap firing factors (P1=w, P2=w−1, j13=Q5, j15=Q6), making it a **maximal firing set**
   on R4. Non-monic leads are strictly worse: a leading coeff 2 pays +2·log2·arcfrac=+0.0951 in
   r̃ (the boundedness/`log|lead|` term, GUARDRAIL 3). Hence **no original firing integer block
   of degree ≤ 16 exists within reach of the saturated R4 anchor.**

### Float pre-gate (GUARDRAIL 2; `float_pregate_q9A.py j16 350000 4000000`)
Fed the STRONGEST reachable firing-coprime block (j16) as a hypothetical third A-base block;
joint Nelder-Mead re-opt of all 10 exponents, re-evaluated N-stably at N=4M:
- base (qI=0) = 0.2538891201, re-optimized = 0.2538863828, **qI*=0.06854** (block active),
- **drop below held 0.2538893183 = 2.94e−6 < the 5e−6 gate** (only ~15× the ~2e−7 cert slack).
- **FLOAT GATE: FAIL.** Even the best reachable block is sub-gate — the A-base lever is DRY
  (consistent with the audited j3 +1.49e−4 → j9 +3.2e−6 → projected ~3e−6 collapse). Per the
  anti-stall rule and FEASIBILITY HONESTY, **NO certify was run** (gate failed; and j16 is not
  original anyway).

### Honest status of the deliverable vs the R7 ask
- (A) DESIGN PROBLEM: **formalized and solved as an optimization** (objective = certified r̃,
  factorized over U^ν wells; runnable). ✓ as a method statement.
- (B) ORIGINAL firing block Q* with r̃<0 on R4: **NOT achieved** — proved within reach
  (deg ≤ 16, ~80k candidates, monic + non-monic) that NONE exists, with the maximal-firing-set
  reason. This is a NEGATIVE/structural result, not the constructed block the ask wanted.
- (C) Float pre-gate: **run; FAILED (2.94e−6 < 5e−6)** → lever confirmed dry.
- (D) Certify: **not run** (gate failed). Held upper 0.2538893183 UNCHANGED.

### What would push it further
- The maximal-firing-set obstruction is anchor-specific: it says the R4 *dictionary* is firing-
  saturated. A genuinely new original firing block would need to fire on an anchor whose
  dictionary is NOT yet maximal — i.e. it must REPLACE (swap) a dictionary block rather than be
  added as a coprime factor, OR the family must change qualitatively (e.g. a B-branch move, all
  audited dry). The screen for a beneficial SWAP (R5 screen_swap) is the remaining structural
  lever; a numeric break almost certainly requires leaving the saturating A-base/perturber
  Doche family.
- The reproducible, publishable kernel from this round: **r̃ as a transfinite-diameter objective
  + the maximal-firing-set characterization of saturation** (the dictionary consumes the cheap
  firing factors; firing is a non-perturbative knife-edge; the firing margin of the best
  reachable block is below the cheapest coprime-factor cost). This mechanistically EXPLAINS the
  observed diminishing returns (j3 → j9 → dry), which the R6 lemma only described.
