# 82a UPPER — R6 outline: integer transfinite diameter as a STRUCTURAL result

Spec review: **REQUIRED** (the top deliverable rests on a non-obvious first-variation /
equilibrium-measure identity that is genuinely new analysis, not on disk; the
load-bearing weight-identification step must be checked before the builder commits a
round to it).

Target to beat: this round is **NOT a numeric break** (held upper 0.2538893183 is
near-saturated: A-base gains decay ~47x/step, next block < cert slack). The deliverable
is a **reviewer-verifiable LEMMA + structural characterization**. The "value to beat"
is therefore a verified milestone of the form: a closed-form first-variation identity
whose prediction matches the campaign's empirical fired/dry table (a falsifiable,
reproducible numerical check), PLUS the rigorously-checked shared-pool unifying
statement. A bonus numeric break is welcome but the round must NOT depend on one.

The round's deliverable composes **Angle 3 (anchor) + Angle 1 (headline) + Angle 2
(corollary)**. Angle 4 is opportunistic only.

================================================================================

## KEY STRUCTURAL FACT THE WHOLE OUTLINE RESTS ON (verified, on disk)

In the held R4 family the **perturber B-branch attains D**: D = max(A-arg 61.65784,
B-arg 72.00176) = 72.00176. So adding a new A-base block Q with small exponent q_Q
**adds q_Q·deg(Q) to the LOSING A-arg of D** — i.e. **D is locally constant in q_Q**
(its derivative is 0 until the A-arg catches up to 72.00, far away). Therefore, to
first order in q_Q at q_Q=0:

  d(log h)/dq_Q = d( (∫G ds)/D )/dq_Q = (1/D)·d(∫G ds)/dq_Q   (D-derivative term vanishes)

This is what makes the first-variation lemma CLEAN — no quotient-rule cross term from D.
The builder must FIRST re-confirm this (cheap: recompute the two D-args at the held
optimum; A-arg 61.66 < B-arg 72.00, gap 10.34, so q_Q·deg(Q) stays in the losing branch
for q_Q up to ~1.3 for deg 8). If a candidate block's exponent ever pushes the A-arg
past 72.00 the D-term re-enters — flag and handle (Angle 1, hard-step note).

================================================================================

Angle 1 (top pick, HEADLINE): The first-variation lemma — marginal ∫G-gain = weighted
conditional log-capacity on the active arc.
  Moves: structural (explains UPPER firing); no numeric claim required.
  Spec review: REQUIRED.

  Skeleton:
    1. Set A(t) = (1/2)Σ q_i log|P_i(w(t))|² + Σ_active q·log|base|² etc., B(t) =
       log|Q1Q2| + Σ qE,qF log|perturber|², G(t)=max(A,B), the contour w(t)=z(1-z),
       z=e^{it}, t∈[0,π]. Objective log h = (∫_0^π G dt)/D (in the harness's ds
       normalization). — by the Doc01a §4 D-formula (already verified R2/R4/R7/R9).
    2. Add a new A-base block Q with exponent q_Q: A(t) ↦ A(t) + q_Q·log|Q(w(t))|²·(1/2).
       (Use the harness's exact A-integrand convention: it adds q_Q·log|Q|, match it.)
       — by the construction definition.
    3. First variation of the max-integral. Because G=max(A,B) and only A carries q_Q:
         d(∫G dt)/dq_Q |_{q_Q=0} = ∫_{A>B} (∂A/∂q_Q) dt = ∫_{A>B} log|Q(w(t))| dt
       (the {A=B} kink set has measure zero; on {A<B}, G=B is q_Q-independent ⇒ 0). This
       is the directional derivative of an integral of a pointwise max — standard
       Danskin / envelope theorem: the derivative of max(A,B) wrt a parameter only in A
       equals ∂A·1[A>B] a.e. — by Danskin's theorem (envelope theorem for max of two
       smooth functions; the active-index set is {A>B}).
    4. Combine with the D-fact above:
         d(log h)/dq_Q |_0 = (1/D)·∫_{A>B} log|Q(w(t))| dt.
       Define the **active-arc log-functional** r̃_Q := ∫_{A>B} log|Q(w(t))| dt (NOT
       normalized by deg — the deg shows up only if D's branch switches). Then
       **Q FIRES (q_Q>0 lowers log h) ⟺ d(log h)/dq_Q|_0 < 0 ⟺ ∫_{A>B} log|Q| dt < 0**,
       i.e. Q is, on average over the active arc, INSIDE the unit lemniscate |Q|<1. — by
       step 3 + step (D-fact).
    5. Identify the weight as an equilibrium/balayage density (the "capacity" framing,
       the publishable upgrade). The active arc {A>B} = [0, 0.8221] (verified). The
       functional ∫_{A>B} log|Q(w(t))| dt = ∫ log|Q| dν where ν = pushforward of arc
       Lebesgue measure under t↦w(t) restricted to {A>B}. Writing it via the logarithmic
       potential U^ν(ζ)=∫log|ζ-w|dν(w): ∫log|Q|dν = Σ_{roots ρ of Q} U^ν(ρ) + deg(Q)·
       (log lead). So **the marginal gain is the sum of the arc-potential U^ν evaluated at
       Q's roots** — Q fires iff its roots sit where U^ν is most negative, i.e. near the
       arc's support / its equilibrium-type measure. THIS is "roots approximate the
       equilibrium distribution of the active locus" made precise. — by the standard
       potential-theoretic identity ∫log|Q|dν = ΣU^ν(ρ_i)+deg·log|lead|.
    6. CONDITIONAL correction (the j9>j6 falsifier resolution). The naive r_Q
       (unconditioned, deg-normalized) FAILS because firing is set RELATIVE to the
       already-active dictionary. The honest object is the residual after the *finite*
       parameter rebalance: when q_Q turns on, the other exponents re-optimize, so the
       true second-order test is whether log|Q| has a component on {A>B} ORTHOGONAL (in
       L²(active arc)) to span{log|P_m|, log|perturbers|} — the active dictionary's
       potentials. The first-order term (steps 3-4) is necessary; the CONDITIONAL residual
       explains why j9 (notch in a sub-band j3 leaves thin) beats redundant j6. — frame as:
       first-order screen = r̃_Q; the predictive screen = conditional residual capacity.

  Hard step (load-bearing): **step 3 — the directional derivative of ∫max(A,B)
  equals ∫_{A>B} ∂A.** Mechanism: Danskin/envelope theorem — for G(t,q)=max(A(t,q),B(t)),
  ∂_q ∫G dt = ∫ ∂_q A · 1[A>B] dt because the kink contributes zero (A=B there, measure
  zero, and the one-sided derivatives agree off it). The subtlety the reviewer will probe:
  the active set {A>B} ITSELF moves with q (its boundary shifts), but by the envelope
  theorem that boundary motion is a SECOND-order effect (G is continuous across the kink,
  so moving the integration limit where the two branches are equal contributes 0 to first
  order) — this is exactly the explorer's "lowering A shrinks the {A>B} support
  nonlinearly" observation, correctly relegated to second order. So the FIRST-order
  formula is exact and clean; the support-shrink is the second-order / conditional term
  (step 6). The reviewer must confirm the boundary-motion term vanishes to first order.

  Check (what the builder runs to certify — CHEAP, no 8-min certify):
    (a) Closed-form vs finite-difference. Compute r̃_Q = ∫_{[0,0.8221]} log|Q(w(t))| dt
        (high-N quadrature, the explorer already has 400k samples) for Q ∈ {j3, j9 (FIRED),
        j6, j7 (DRY)}. Independently compute the EMPIRICAL marginal Δ(∫G)/Δq_Q by finite
        difference: certify-free, just evaluate ∫G at q_Q=0 and q_Q=ε on the held family
        (Riemann sum, N≥4M, the harness's float_value path). The lemma PASSES iff
        Δ(∫G)/Δq_Q /D ≈ r̃_Q/D to the quadrature tolerance for ALL FOUR blocks, AND the
        SIGN matches the fired/dry table: r̃_Q < 0 (gain) for j3,j9; r̃_Q ≥ 0 or the
        re-optimized exponent collapsing for j6,j7. This is a falsifiable, reproducible,
        ~seconds-to-minutes numerical check — NO branch-and-bound certify needed.
    (b) Root-potential cross-check (step 5): verify ∫log|Q|dν = Σ U^ν(ρ_i)+deg·log|lead|
        numerically for j3 (3 roots) — confirms the equilibrium-measure identification.
    (c) D-constancy: re-confirm A-arg(q_Q=ε) < 72.00 so the D-derivative is 0 (step 4).

  Risk: MEDIUM. The first-order lemma is almost certainly true (it's Danskin). The RISK
  is that the first-order screen r̃_Q does NOT by itself reproduce the fired/dry ordering
  (the explorer already found r̃_Q is one-directional: j3 smallest fires, j7 largest dry,
  but j9>j6 inverts). MITIGATION: the lemma is still PUBLISHABLE as the exact first-order
  identity (it correctly predicts SIGN ⇒ whether a block can fire at all), and the j9>j6
  inversion is then EXPLAINED as the second-order/conditional effect (step 6), turning a
  weakness into the paper's main subtlety. So the lemma stands even if r̃_Q alone is not a
  perfect screen — the check (a) on SIGN is the must-pass; the magnitude-ordering is the
  corollary's job (Angle 2). Worst case (lemma's sign prediction itself fails a block):
  fall back to Angle 3 as the round's milestone.

================================================================================

Angle 2 (corollary / methods contribution): The conditional-capacity SCREEN.
  Moves: structural — converts brute multistart into a principled block-selection rule.
  Spec review: not required (it is the operationalization of Angle 1; rides its review).

  Idea: project log|Q(w(t))| onto the orthogonal complement, in L²([0,0.8221], dt) (or
  weighted by the equilibrium density dν of Angle-1 step 5), of the span of the active
  dictionary's log-potentials {log|P_m(w)|, log|j3(w)|, log|j9(w)|, log|perturbers|};
  rank candidate admissible blocks by the residual r̃^⊥_Q (the conditional capacity).
  Predict: fired blocks have large-magnitude-NEGATIVE residual; dry blocks ≈ 0 residual.

  Skeleton:
    1. Build the Gram matrix G_mn = ⟨log|D_m|, log|D_n|⟩_{L²(active arc)} over the active
       dictionary; sample at N points on [0,0.8221]. — linear algebra.
    2. For each candidate Q: residual r̃^⊥_Q = ⟨log|Q|, log|Q|⟩ − g^T G^{-1} g, where
       g_m=⟨log|Q|,log|D_m|⟩ (the L² projection residual norm), AND the signed projected
       mean (the part that moves ∫G). — projection.
    3. Verify the ranking reproduces the KNOWN fired/dry table: j3, j9 rank above j6, j7;
       and the live j9>dry j6 inversion (which raw r_Q got BACKWARDS) is RECOVERED by the
       conditional residual. — numerical check against R2/R4 campaign data.

  Hard step: showing the conditional residual ORDERING matches the campaign's fired/dry
  ordering INCLUDING the j9>j6 inversion. Mechanism: j6's log-potential is largely
  redundant with j3's coverage of the arc (small residual after projection ⇒ dry), while
  j9's notch falls in a sub-band j3 leaves thin (large residual ⇒ fires). This is the
  precise, defensible form of the user's thesis.

  Check (CHEAP): the Gram/projection computation is pure numpy on the explorer's existing
  samples — seconds. PASS iff residual-rank(j9) > residual-rank(j6) (the falsifier the raw
  r_Q got wrong) AND fired blocks {j3,j9} top the ranking. PRE-CHECK before any spec: run
  the Gram projection on the 4 blocks first; if it does NOT recover j9>j6, the screen is
  not the right object and Angle 2 is downgraded to "future work" (Angle 3 still carries
  the round).

  Risk: MEDIUM-LOW for the qualitative claim; the screen is a HEURISTIC tool, not a
  theorem, so it cannot fail "rigor" — it either reproduces the ordering (a real methods
  result) or it doesn't (logged as a negative result). Cheap to settle.

================================================================================

Angle 3 (LOW-RISK ANCHOR — the safe backbone the round can stand on alone): The
shared-pool / weighted integer transfinite diameter unifying statement.
  Moves: structural — rigorously establishes that both sides draw from ONE pool.
  Spec review: not required (it is a verification of already-found facts).

  Idea: State and rigorously verify the unifying observation the explorer already found
  with verbatim evidence: the integer polynomials in BOTH the Doche upper construction and
  the Flammang lower construction are entries of Flammang [F18] Table 1 — ONE pool of
  small-Mahler-measure integer polynomials in w=z(1-z) — and both selection problems are
  instances of WEIGHTED INTEGER TRANSFINITE DIAMETER t_{Z,φ} on the lemniscate.

  Skeleton (all CHEAP, all sympy/numpy — no certify):
    1. Exact identification, rigorously checked: P4=j5, P6=j8, P8=j12 (Doche base polys =
       Flammang Table-1 entries; descending coeffs of j_k reverse to ascending base coeffs)
       and Q5=j13, Q6=j15, plus the A-base blocks j3, j9 — list the EXACT Table-1 indices
       on each side. — by sympy polynomial equality (reverse-coeff match), already partly
       done by explorer; make it a clean assertion table.
    2. Admissibility / coprimality audit of the FULL active dictionary {P1,P2,P4,P6,P8,
       j3,j9} ∪ {Q1,Q2,Q5,Q6}: pairwise coprime, squarefree, Doc01a condition (4). — by
       sympy gcd (already verified R2/R4; consolidate).
    3. The unifying frame: Flammang's lower-side dictionary enlargement is the weighted
       integer transfinite diameter t_{Z,φ}(C) with φ=(max(1,|z|)max(1,|1−z|))^{−1} on
       control points near the least minima of f, solved via LLL (from
       flammang_F18_digest.md). The Doche upper-side block selection picks integer polys
       of small ∫_{arc}log|Q| — the SAME small-weighted-norm integer-Chebyshev problem on
       the SAME lemniscate w=z(1−z); the active arc {A>B} is the upper-side analogue of
       Flammang's "control points near the least minima of f". — by citing Flammang's own
       t_{Z,φ}+LLL machinery + the shared pool (steps 1-2).
    4. State the DEFENSIBLE dual-loci structure (HONESTY GUARDRAIL): the genuine dual loci
       are UPPER-INTERNAL — the A-branch active arc {A>B}=[0,0.8221] (A-base lever) vs its
       complement {A<B}=[0.8221,π] (B-perturber lever). Explicitly DO NOT claim
       "lower locus = set-complement of upper active arc" — the explorer found NO on-disk
       support for it; that version is overstated and must not be written as proved.

  Hard step: NONE that is novel — this is verification of established facts. The only
  care needed is the HONEST scoping in step 4 (state the upper-internal dual-loci, not the
  unsupported upper-vs-lower complement).

  Check: sympy coprimality + reverse-coeff equality (deterministic, reproducible,
  seconds). This is the certainly-true backbone; even if Angles 1-2 stall, this is a real
  verified structural milestone.

  Risk: LOW. Facts are already on disk and verbatim. The only risk is OVERCLAIMING the
  dual-loci — explicitly guarded against in step 4.

================================================================================

Angle 4 (opportunistic bonus, round must NOT depend on it): Screen-surfaced untried block.
  Moves: upper bound — a small numeric drop IF Angle 2's screen surfaces a block with a
  real first-order gain. Spec review: not required (rides the held certify harness).

  Idea: if the conditional-capacity screen (Angle 2) ranks an UNTRIED admissible block
  (e.g. j11 deg 11, or any Table-1 block with lemniscate-near roots) above the dry blocks
  with a genuinely negative residual, run the existing joint FLOAT gate (N≥4M, margin
  ≥5e-6) on it; certify ONLY if it clears the held 0.2538893183 by >10x cert slack.

  Hard step: the float gate clearing ≥5e-6 — explorer flags A-base is saturated (next
  block likely <1e-6, at/below the ~1.2-2.0e-7 cert slack), so this is a LONG SHOT.

  Check: the mandatory joint FLOAT pre-gate (per the anti-stall rule) BEFORE any certify.
  If the float drop < 5e-6, STOP — do not certify (per round-4 saturation rule).

  Risk: HIGH for a numeric break (saturation). Treat strictly as a bonus; the round's
  verified milestone is Angles 3+1(+2), independent of Angle 4.

================================================================================

## RANKING (publishability-per-effort)

1. **Angle 3 (anchor) — do FIRST, certain milestone, ~minutes.** Low risk, already-found
   facts, rigorously checkable with sympy. Guarantees the round logs a verified structural
   milestone even if the lemma is hard. This is the floor.
2. **Angle 1 (headline) — the publishable theorem, MEDIUM risk.** The first-order Danskin
   identity is near-certain and is the paper's centerpiece (it EXPLAINS firing via the SIGN
   of ∫_{A>B}log|Q|, and the j9>j6 falsifier becomes its second-order subtlety). Its CHEAP
   finite-difference check (a) is decisive and needs NO branch-and-bound certify. Do this
   second; it is where the "elevate above a computation" value lives.
3. **Angle 2 (corollary) — rides Angle 1, MEDIUM-LOW risk, CHEAP.** Run the Gram-projection
   pre-check early (seconds); if it recovers the j9>j6 inversion it is a clean methods
   contribution, if not it is logged as future work. Settle it cheaply alongside Angle 1.
4. **Angle 4 (bonus) — only if Angle 2's screen surfaces a live block; HIGH risk numeric,
   do NOT let the round depend on it.**

The builder runs ONE composed line: **Angle 3 (anchor) → Angle 1 (headline lemma with the
finite-difference + sign check on j3/j9/j6/j7) → Angle 2 (Gram-projection corollary)**,
producing a `R6-integer-transfinite-diameter.md` deliverable = the lemma statement + its
proof sketch (Danskin + envelope) + the reproducible numerical fired/dry check + the
shared-pool table. Spec-review the Angle-1 weight-identification / envelope-boundary step
BEFORE the builder commits, per the REQUIRED flag.

## Anti-stall / cheap-checks-first ordering (per Rules)
- CHEAPEST first: Angle 3 sympy coprimality (seconds) → Angle 1 finite-difference sign
  check on 4 blocks (minutes, NO certify) → Angle 2 Gram projection (seconds).
- NO branch-and-bound certify is needed for the headline deliverable (it is a lemma +
  finite-difference + projection check). The only certify is the OPTIONAL Angle-4 bonus,
  gated by the mandatory ≥5e-6 FLOAT pre-gate.
- Re-confirm the D-constancy fact (A-arg 61.66 < B-arg 72.00) FIRST — it is the linchpin
  that kills the quotient-rule cross term and makes the lemma clean.

================================================================================
================================================================================

# R6 BUILD RESULT — the verified structural deliverable

Status: BUILT (R6), AWAITING REVIEW. Composes Angle 3 (anchor) + Angle 1 (headline
lemma) + Angle 2 (corollary screen). This round is **NOT a numeric record-break**
(the held upper 0.2538893183 is near-saturated). The headline VALUE is a
reviewer-verifiable LEMMA whose sign prediction reproduces the campaign's empirical
fired/dry table, plus the rigorously-checked shared-pool unifying statement.

All three scripts are self-contained in `constants/82a/certificate/`, reuse the
held harness's exact A,B,D,contour conventions (`verify_upper.py` /
`verify_upper_q8A.py`), and run in seconds-to-≈1min — NO branch-and-bound certify
is needed for the deliverable.

--------------------------------------------------------------------------------
## THE REQUIRED ANCHOR FIX (from the outline review) — implemented

The lemma is a FIRST VARIATION AT q_Q = 0, so r̃_Q must be measured on the anchor
family that does NOT yet contain the candidate block (recomputing {A>B} there):

  candidate j3  → anchor **R11** family (perturbers Q5,Q6 only; NO A-base; qG=qH=0)
  candidate j9  → anchor **R2**  family (has j3 A-base, NOT j9; qG=0.8935, qH=0)
  dry j6, j7    → anchor **R2**  family (the family they were screened against)

Exact anchor exponent vectors are hard-coded in `verify_firstvar_lemma.py`
(R11/R2/R4 dicts), taken verbatim from the R11 and R2 record rows of
`constants/82a.md`. The SATURATED **R4** family (j3 AND j9 both on) is included only
as a NEGATIVE CONTROL: evaluating r̃(j9) there gives r̃ = +0.00012 > 0 and FD =
+1.6e-6 > 0 — the documented mispredict (j9 looks dry because it is already active).
This is the trap the review flagged; with the correct R2 anchor every sign is right.

Numbering trap also obeyed: campaign jk = `flammang_table1._TABLE_DESCENDING[k-1]`
(the `screen_swap_R5._TAB` map). j3=[1,1,-2,1] (deg3), j9=[1,-1,0,-3,15,-22,16,-6,1]
(deg8), j6=[2,-5,6,2,-11,11,-5,1] (deg7), j7=[1,-2,4,-7,13,-16,12,-5,1] (deg8). Each
candidate polynomial is written explicitly in the script, not read by raw table[k].

--------------------------------------------------------------------------------
## ANGLE 3 — shared-pool anchor (LOW-RISK MILESTONE) — PASS

`verify_shared_pool.py` (sympy, ~1.3s). Checks, by EXACT integer-polynomial identity
(no floats), as polynomials in w = z(1−z):

  Doche base   P4 == Flammang j5 (deg 4),  P6 == j8 (deg 8),  P8 == j12 (deg 12)
  A-base       campaign j3 == Flammang j3 (deg 3),  j9 == Flammang j9 (deg 8)
  perturbers   Q5 == Flammang j13 (deg 12),  Q6 == Flammang j15 (deg 16)

all PASS (exact equality). The full active dictionary {P1,P2,P4,P6,P8,j3,j9} ∪
{Q1,Q2,Q5,Q6} (11 blocks) is verified squarefree and pairwise coprime (all 55 pairs)
— Doc01a condition (4) non-degeneracy.

UNIFYING FRAME (honestly scoped): both the Doche upper construction and the Flammang
[F18] lower construction draw their integer polynomials from ONE pool — Flammang
Table 1 — of small-Mahler-measure integer polys in w = z(1−z). Both selection
problems are instances of the SAME weighted integer transfinite-diameter problem
t_{Z,φ} on the lemniscate w = z(1−z): pick integer polys of small weighted log-norm
on a sub-locus of that curve.

HONESTY GUARDRAIL (asserted in the script, step 5): the genuine dual loci are
UPPER-INTERNAL — the A-base lever acts on the active arc {A>B}, the B-perturber lever
on its complement {A<B} of the SAME contour. We DO NOT claim "lower-bound locus =
set-complement of the upper active arc"; there is no on-disk support for it and it is
not asserted.

--------------------------------------------------------------------------------
## ANGLE 1 — the HEADLINE first-variation lemma — PASS

### Lemma (first variation of the upper objective)

Held family: log h = (1/D)·⟨G⟩_s, G(s)=max(A(s),B(s)), s∈[0,1], chi(s)=z(1−z),
z=e^{2πi s}, with A = Σ q_i log|P_i(chi)| + (A-base terms), B = log|Q1Q2| +
(perturber terms), and D = max(arg_A, arg_B), arg_A = Σ q_i deg P_i + (A-base degs),
arg_B = 56 + (perturber degs) — exactly `verify_upper_q8A.float_value_q8A`/`_Dval`.

Introduce a new A-base block Q (integer poly) with exponent q_Q ≥ 0:
A(s) ↦ A(s) + q_Q·log|Q(chi(s))|. Suppose at the base family (q_Q=0) the B-branch
attains D, i.e. **arg_A < arg_B = D**. Then

    d(log h)/dq_Q |_{q_Q=0}  =  (1/D)·r̃_Q,
    r̃_Q := ⟨ log|Q(chi)|·1_{A_0>B} ⟩_s   (the BASE-family active arc),

and the firing criterion: **Q fires (small q_Q>0 lowers log h) ⟺ r̃_Q < 0** ⟺ Q is,
on average over the active arc, inside the unit lemniscate |Q|<1.

### Proof (two clean steps)

1. **D-constancy (kills the quotient cross-term).** d(log h)/dq_Q =
   [d⟨G⟩/dq_Q·D − ⟨G⟩·dD/dq_Q]/D². Since arg_A < arg_B, raising q_Q only grows the
   LOSING arg_A; D = arg_B stays fixed until arg_A catches up (needs q_Q·deg(Q) >
   arg_B − arg_A). So dD/dq_Q = 0 in a neighbourhood of q_Q=0 and
   d(log h)/dq_Q = (1/D)·d⟨G⟩/dq_Q. Verified: at every test anchor arg_A < arg_B with
   gap ≈10.3–11.4, and the eps-perturbed arg_A stays below arg_B (D-const-OK in all
   rows of the table below).

2. **Danskin / envelope.** G(s,q_Q)=max(A(s,q_Q),B(s)) with only A depending on q_Q,
   ∂A/∂q_Q = log|Q(chi(s))|. For s off the kink set {A_0=B} (measure zero, A_0−B
   real-analytic and not ≡0): if A_0(s)>B(s) then G=A near q_Q=0 so ∂G/∂q_Q =
   log|Q(chi(s))|; if A_0(s)<B(s) then G=B so ∂G/∂q_Q = 0. Differentiating under the
   integral (G is Lipschitz in q_Q, uniformly bounded a.e. gradient log|Q| ∈ L¹)
   gives d⟨G⟩/dq_Q|_0 = ⟨log|Q(chi)|·1_{A_0>B}⟩_s = r̃_Q. The active-set BOUNDARY
   moves with q_Q, but at the boundary A_0=B the two branches are EQUAL, so moving the
   integration limit there changes the integrand by 0 to first order — the standard
   envelope-theorem boundary-cancellation. Hence r̃_Q is exact to first order and the
   support-shrink (the explorer's "lowering A shrinks {A>B}") enters only at O(q_Q²).

Combine: d(log h)/dq_Q|_0 = (1/D)·r̃_Q. ∎

### Potential-theoretic identification (the "transfinite diameter" upgrade)

Let ν = pushforward of arc-Lebesgue measure (restricted to {A_0>B}) under
s↦chi(s). Then r̃_Q = ∫ log|Q| dν factors over Q's roots:

    r̃_Q = Σ_{ρ: Q(ρ)=0} U^ν(ρ) + deg(Q)·log|lead(Q)|,
    U^ν(ζ) = ∫ log|ζ−chi| dν = ⟨ log|ζ−chi|·1_{A_0>B} ⟩_s   (the arc log-potential).

So the marginal gain is the SUM OF THE ARC-POTENTIAL at Q's roots: Q fires iff its
roots sit where U^ν is most negative — near the equilibrium-type measure of the
active locus. This is "the firing blocks' roots approximate the equilibrium
distribution of the active locus" made precise. Verified numerically for j3 to
machine precision (|LHS−RHS| = 5.2e-17, `verify_firstvar_lemma.py roots`): j3's
complex-conjugate root pair 0.574±0.369i has U^ν = −0.041 each (near the arc), the
real root −2.148 has U^ν = +0.058; the pair dominates, r̃(j3) = −0.0228 < 0 ⇒ fires.

### Verification table (`verify_firstvar_lemma.py`, N=4M, eps=1e-4, central diff, 54s)

| blk | anchor | arg_A | arg_B | D | r̃_Q | (1/D)r̃ | FD d(logh)/dq | ratio | pred | exp |
|-----|--------|------:|------:|------:|---------:|----------:|--------------:|------:|------|-----|
| j3  | R11    | 59.198| 70.641| 70.641| −0.02285 | −3.234e-4 | −3.235e-4     | 0.9998| FIRED| FIRED|
| j9  | R2     | 61.546| 71.987| 71.987| −0.00677 | −9.407e-5 | −9.415e-5     | 0.9992| FIRED| FIRED|
| j6  | R2     | 61.546| 71.987| 71.987| +0.00954 | +1.325e-4 | +1.324e-4     | 1.0004| DRY  | DRY |
| j7  | R2     | 61.546| 71.987| 71.987| +0.00729 | +1.013e-4 | +1.012e-4     | 1.0006| DRY  | DRY |
| j9  | R4*    | 61.658| 72.002| 72.002| +0.00012 | +1.656e-6 | +1.627e-6     | 1.0180| TRAP+| (neg ctrl)|

Closed-form (1/D)r̃ matches the independent central finite difference to <0.1% on the
clean rows; the SIGN predicts fired (r̃<0) vs dry (r̃>0) for all four test blocks,
INCLUDING the j9-vs-j6 inversion on the SAME R2 anchor (j9 r̃=−0.0068 fires, j6
r̃=+0.0095 dry). The R4* row is the negative control: on the saturated family
r̃(j9)>0 (the documented anchor trap) — NOT a test of the lemma. D-constancy holds in
every row (arg_A < arg_B; the eps-perturbed arg_A stays below arg_B).

NOTE per the outline review: the un-normalized r̃_Q already separates j9 from j6 — the
explorer's earlier j9>j6 "inversion" was an artifact of his degree-NORMALIZED r_Q,
NOT a defect of the first-order lemma. The lemma alone is the predictor.

--------------------------------------------------------------------------------
## ANGLE 2 — conditional-capacity SELECTION HEURISTIC — PASS

`screen_conditional_capacity.py` (numpy, ~30s, N=2M). Since the lemma already
separates fired/dry, this is positioned (per the review) as a RANKING TOOL, not a
fix for a non-existent lemma defect. Two diagnostics per candidate, on the active arc
{A_0>B} of its anchor:

  (1) raw first-order marginal r̃_Q (the lemma's exact predictor); rank by
      most-negative.
  (2) CONDITIONAL residual: least-squares regression of log|Q| on the active-side
      dictionary potentials {log|P_m|, log|j3|} over the active arc WITHOUT an
      intercept (the construction re-weights q_m but has no free additive constant),
      reporting the signed residual mean m⊥_Q = ⟨e_Q·1_arc⟩ — the part of Q's marginal
      the joint re-optimization CANNOT reproduce by re-weighting active blocks — plus
      the residual rms (redundancy diagnostic).

Result (R2 anchor, directly comparable): j9 r̃=−0.0068 / m⊥=−0.0068 / rms=0.96
(FIRED); j6 +0.0095 / +0.0095 / rms=0.47 (DRY); j7 +0.0073 / +0.0073 / rms=0.26
(DRY). The screen RECOVERS the empirical fired/dry ordering incl. the j9>j6
inversion. The rms exposes WHY: j9's active-arc profile carries much structure NOT
spanned by the dictionary (rms 0.96), whereas j6/j7 are largely redundant (rms
0.47/0.26) — so re-weighting the dictionary nearly replicates them ⇒ dry.

--------------------------------------------------------------------------------
## ANGLE 4 — forward note (NO certify this round)

The screen ranks three UNTRIED admissible Table-1 blocks with NEGATIVE first-order
marginal on the R2 anchor: **j16 (deg16, r̃=−0.0073)**, **j17 (deg16, r̃=−0.0060)**,
**j20 (deg20, r̃=−0.0050)** — all verified squarefree and coprime to the active
dictionary. These clear the >5e-3 first-order pre-screen and are logged as candidates
for a FUTURE certify. CAVEATS (why no certify now): (i) the screen is a first-order
marginal at q_Q=0 — it does not account for the D-switch a high-degree block triggers
(deg 16–20 pushes arg_A toward arg_B≈72 faster) nor for saturation when the other
exponents rebalance; (ii) the held A-base lever is near-saturated (R4 gain 3.2e-6 ≈
cert slack); (iii) per the anti-stall rule, any certify must first clear the joint
FLOAT pre-gate (N≥4M, drop ≥5e-6). The deliverable does NOT depend on Angle 4.

--------------------------------------------------------------------------------
## What would push this further

- Angle 4 float gate: run the joint N≥4M Nelder-Mead with j16/j17/j20 in a new A-base
  slot (seed exponent=0), per the ≥5e-6 N-stable drop gate, before any certify. If a
  drop clears the gate, clone verify_upper_q*A.py with the block as a new A-base and
  certify. (Expectation: thin, given saturation — but j16/j17 are the screen's top
  untried picks.)
- Sharpen the potential-theoretic statement into a clean transfinite-diameter
  inequality: relate inf over admissible integer Q of r̃_Q to the weighted integer
  transfinite diameter t_{Z,φ}(active arc), making the "upper-side selection =
  integer-Chebyshev on the active arc" thesis a theorem rather than a framing.
- Quantify the second-order (active-set-shift) term to predict the SATURATED firing
  magnitude (the R4 row), turning the screen into a magnitude predictor not just a
  sign/sieve.

--------------------------------------------------------------------------------
## Reproduce (all fast, no certify)

    cd constants/82a/certificate
    python3 verify_shared_pool.py                         # Angle 3, ~1.3s, PASS
    python3 verify_firstvar_lemma.py 4000000 1e-4         # Angle 1, ~54s, PASS
    python3 verify_firstvar_lemma.py roots 2000000        # step-5 potential id, ~4s, PASS
    python3 screen_conditional_capacity.py 2000000        # Angle 2, ~30s, PASS

A coarser/faster lemma run: `python3 verify_firstvar_lemma.py 1000000 1e-4` (~10s;
signs + inversion still correct, ratios slightly off at lower N — use N=4M for the
quantitative match).
