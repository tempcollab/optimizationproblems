# R8 outline review (outline-reviewer)

Reviewing `constants/82a/approaches/R8-outline.md` (two angles: A = B-branch perturber
with the novel m_B cross-term marginal; B = rigorize the R6 first-variation lemma).

## VERDICT: OUTLINE SOUND — builder may proceed (with the corrections in §"Required" below)

The load-bearing novel claim (the B-branch cross-term marginal m_B) is **derived
correctly in form and verified numerically by me** against the actual harness. Angle A
identifies a GENUINELY OPEN lever (unlike the proven-saturated A-base), and Angle B is a
sound bankable fallback with the R7 corrections correctly folded in. Build Angle A's cheap
path first; carry Angle B.

================================================================================
## The load-bearing m_B claim — VERIFIED CORRECT (I re-derived and FD-tested it)

The outline's marginal
  **m_B(Q) = (1/D)[ ∫_{B>A} log|Q∘χ| ds − (log h)·deg(Q) ]**,  firing ⟺ m_B < 0.

I confirmed all four scrutiny points from the dispatch against the live R4 held family
(q8A harness, N=4M):

1. **Cross-term form is correct (quotient rule).** With log h = ⟨G⟩/D and a B-perturber
   sending B → B + q_Q·log|Q| AND arg_B → arg_B + q_Q·deg(Q) (B attains D, so D moves):
   d(log h)/dq_Q = [d⟨G⟩/dq_Q·D − ⟨G⟩·dD/dq_Q]/D² = (1/D)∫_{B>A}log|Q| − (log h)·deg(Q)/D.
   **FD test:** test block Q = X²−X+1 (deg 2, Q(0)=Q(1)=1) on R4, central FD eps=1e-4:
     FD d(log h)/dq_Q = +3.14568e-4 ; closed-form m_B = +3.14560e-4 ; ratio = **0.99997**.
   The cross-term derivation is right to <3e-5 relative. The dispatch's term-by-term
   reading is correct: term1 = (1/D)∫_{B>A}log|Q|, term2 = −⟨G⟩·deg(Q)/D² =
   −(log h)·deg(Q)/D since ⟨G⟩/D = log h.

2. **Region {B>A} is the correct integration region (Danskin/envelope).** Confirmed: on
   {B>A} the B-branch is active so ∂G/∂q_Q = ∂B/∂q_Q = log|Q|; on {A>B}, G=A is
   q_Q-independent. Measure{B>A} = **0.9314**, measure{A>B} = 0.0686 (the complement of
   the A-base active arc, as claimed). Using the WRONG region {A>B} would give
   ∫_{A>B}log|Q| = +0.0131 instead of the correct ∫_{B>A}log|Q| = +0.5304 — a gross error.
   The outline correctly evaluates on the held family recomputing {B>A} there (the
   q_Q=0 anchor for a NEW perturber is the held R4 family — see anchor note below).

3. **The moving-boundary subtlety (dispatch Q3) is genuinely 2nd order — B attaining D
   does NOT break it.** Two distinct "boundaries", both handled:
   (a) The D-max branch boundary: D(q_Q) = max(arg_A, arg_B0 + q_Q·deg Q). At q_Q=0,
       arg_B0 = 72.00 > arg_A = 61.66 with **gap 10.34**, so for |q_Q| < 10.34/deg(Q)
       (= 2.59 for deg 4) D is AFFINE in q_Q (slope deg Q), NOT kinked at 0. So
       dD/dq_Q = deg(Q) is a clean exact derivative, not a one-sided kink. This is the
       NEW term the A-base lemma did not have, and it is well-defined precisely because
       the gap is wide.
   (b) The pointwise integrand kink set {A=B}: same as the A-base case — the integrand of
       max(A,B) is continuous across {A=B}, so the moving-limit term is 0 to first order;
       {A=B} has measure zero. B being the dominant branch on {B>A} does not change this:
       Danskin only needs ∂G/∂q_Q = (∂B/∂q_Q)·1_{B>A} a.e., which the FD ratio 0.99997
       confirms. **The B-branch case does NOT break the 2nd-order boundary step.**

4. **Sign of the cross-term is firing-favorable (degree-rewarding), as claimed.** The
   cross-term −(log h)·deg(Q)/D = −0.00705 per deg-2 block (negative). The anti-firing
   term (1/D)∫_{B>A}log|Q| is positive (|Q|>1 on most of the complement arc). FIRING ⟺
   ∫_{B>A}log|Q| < (log h)·deg(Q), i.e. average log|Q| over the 0.931-measure arc <
   **0.2726 per unit degree**.

**LEVER IS GENUINELY OPEN (the key positive finding).** I tested B-perturbers and FOUND a
FIRING one at first order: Q = X⁴−X³−X+1 (deg 4, Q(0)=Q(1)=1) gives ∫_{B>A}log|Q| = +0.807
< (log h)·4 = +1.016, so **m_B·D = −0.209 < 0 — IT FIRES.** This is unlike the A-base
regime (R7 proved saturated). The cross-term genuinely makes B-perturber firing reachable.
So Angle A is NOT a dead end at first order — the marginal admits firing blocks, and the
real question (correctly flagged "THIN" by the outline) is whether the realized
joint-reopt drop clears the 5e-6 float gate. That is exactly what step 5 decides.

================================================================================
## REQUIRED corrections / clarifications before/while building Angle A

These are CHANGES-while-building, not blockers — none invalidates the angle.

R1. **Do NOT blindly reuse `verify_firstvar_lemma.finite_diff_marginal` for the B branch.**
    That function (line 150) was written for the A-base regime where dD/dq_Q = 0 (D
    constant). For a B-perturber dD/dq_Q = deg(Q) ≠ 0, so a correct FD-vs-closed-form
    check MUST move D in the perturbed evaluation: D(±eps) = arg_B0 ± eps·deg(Q). My test
    above did this and matched to 0.99997; a copy of the A-base FD path that holds D fixed
    will MISMATCH and falsely reject the formula. Step 2 says "retargeted to the B branch"
    — make explicit that "retargeted" means **recompute D at q_Q=±eps with the new
    perturber degree added to arg_B**. This is the spec-critical FD gate (dispatch Q4);
    it IS present in the outline (step 2) — just ensure the D-movement is in it.

R2. **Anchor for a NEW B-perturber = the held R4 family (j3 AND j9 on, all current
    perturbers Q5,Q6 on), candidate q_Q = 0.** A fresh B-perturber sits ALONGSIDE the
    existing perturbers, so its first variation is at the R4 base, recomputing {B>A}
    there. (This mirrors the R7 rule that a third A-base block anchors on R4, not R2.)
    The outline's step 2 says "on the held R4 anchor" — correct; step 4 also says R4 —
    correct. Do NOT drift to the R2 anchor for the final m_B firing claim. (R2 is fine
    only as a U^ν-well seed source.) My verification above used R4 throughout.

R3. **The U^ν_B well-map must use the {B>A} COMPLEMENT region, not {A>B}.** Step 4(b)
    says this — confirm the builder rebuilds U^ν_B(ζ) = ⟨log|ζ−χ|·1_{B>A}⟩_s (measure
    0.931), NOT the R6/R7 A-base U^ν on {A>B} (measure 0.069). These are different
    measures; reusing the A-base well map would screen the wrong arc. The root-potential
    factorization m_B = Σ_ρ U^ν_B(ρ) + deg·log|lead| − (log h)·deg/D must include the
    FLAT per-degree cross-term −(log h)/D = −0.003526 per unit degree (this is the
    degree-reward; the outline's step 4 mentions it — pin the numeric value so the
    screen's per-root scoring is right).

R4. **B-perturber admissibility is STRICTER than A-base: Q(0)=Q(1)=1 IS required**
    (run_state Rule — perturber blocks need it, A-base were exempt). The outline's step
    3(c1) has this. Good. Also coprime+squarefree in w vs the full dictionary
    {P1,P2,P4,P6,P8,j3,j9, Q1,Q2,Q5,Q6} and contour-root-free (step 3 c2,c3). My firing
    test block X⁴−X³−X+1 satisfies Q(0)=Q(1)=1 — confirm the builder's screen enforces
    this gate (a block failing it is inadmissible however negative its m_B).

R5. **The certify (step 6) needs a fresh harness with the perturber in arg_B, and
    HELD_CERT = the true held 0.2538893183** (NOT the stale 0.2540419719 baked into
    q7A, NOT the superseded 0.2538925359 — run_state Rule, my per-role memory). After
    re-opt, re-verify which branch attains D: a high-degree perturber pushes arg_B up
    AND a re-optimized perturber-exponent set could in principle let arg_A catch up — if
    a D-switch happens at the optimum the marginal form changes; flag it. (Cert slack on
    this machinery is empirically ~1.2–2.0e-7, so the 5e-6 gate = ~25–40x slack, SAFE —
    not knife-edge.)

R6. **Honest framing of the likely outcome.** My FD shows firing IS reachable at first
    order, but the outline's prior — the realized joint-reopt drop likely fails the
    5e-6 gate (conversion-factor collapse, as for A-base j16 → 2.94e-6) — is well-founded
    and the builder should PLAN for the structural-B outcome (the verified corrected-B
    marginal + screen is itself a NEW first-variation result for the D-ATTAINING branch,
    which the R6 lemma did not cover — a clean milestone). Either outcome banks.

================================================================================
## Angle B (rigorize the R6 lemma) — SOUND fallback, R7 corrections correctly folded

Checked against the R7-outline-review corrections (and my per-role memory):
- **H1 corrected:** the outline replaces the false "no block has a contour root" with
  H1′ (candidate-Q-only contour-root-free → L¹) + H1″ (A_0,B real-analytic off integrable
  log-sings, A_0→−∞ there putting a nbhd in {A_0<B}). CORRECT — P1=X vanishes at χ(0)=0,
  the original H1 was false (my memory rule, R7). ✓
- **Active arc geometry corrected:** outline states "union of ~32 intervals, K=64 points,
  measure ≈ 0.0685, does NOT start at s=0", replacing the stale "[0,0.8221]" single
  interval. CORRECT. ✓ (My N=4M run confirms measure{A>B}=0.0686.)
- **Load-bearing boundary-term-vanishing argument is sound:** Φ'(0+) = ∫_{A_0>B}log|Q|
  via DCT on the 1-Lipschitz difference quotient (dominated by |log|Q∘χ|| ∈ L¹), with
  the moving-boundary term = ∮_K(A_0−B)·(∂boundary/∂q) = 0 because A_0−B = 0 ON K
  (continuity of max), K finite from real-analyticity. This is the correct mechanism
  (NOT "boundary fixed"). ✓
- **Scoping guardrails kept:** no "inf_Q r̃_Q ≍ −log t_{Z,φ}" overclaim, no "lower locus =
  complement of upper arc" (run_state HONESTY rule). ✓

Angle B is a low-stall-risk bankable milestone (one N=4M re-run + prose). Keep it ready.

================================================================================
## What to watch (no action needed, just flags)
- D-switch after re-opt (R5) — the only way the m_B form could break post-certify.
- The B-branch FD gate MUST move D (R1) — the single most likely builder error.
- Float gate likely fails (R6) — plan structural-B deliverable; do NOT certify on a
  sub-5e-6 float drop (anti-stall + saturation rule).

Builder order (crash-safe): derive m_B (hand+sympy) → FD-verify with D MOVED (R1) →
build U^ν_B well-map on {B>A} (R3) → screen admissible high-deg B-perturbers by exact
m_B (R4 gates) → N≥4M float pre-gate → certify ONLY if ≥5e-6 (R5). Cheap steps first;
the ~8-min certify is last and conditional.
