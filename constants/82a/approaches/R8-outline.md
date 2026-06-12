# 82a UPPER — R8 outline (two angles, ranked)

Spec review: required

Target to beat (numeric headline, if reachable): **0.2538893183** = held VERIFIED upper
(R4, Doche Doc01a §4 family with j3 deg3 + j9 deg8 as A-base blocks; harness
`certificate/verify_upper_q8A.py`). Moving the UPPER bound DOWN.

Per the run_state R6/R7 user redirect, a verified STRUCTURAL milestone counts too; the
A-base numeric lever is PROVEN saturated (R7, reviewer-verified — do NOT add another
A-base block). The two genuinely-open R8 levers are (A) a HIGHER-degree B-branch
**perturber** addition — the only untested numeric lever — and (B) rigorizing the R6
first-variation lemma — a clean bankable structural milestone with outline + outline-review
already on disk.

================================================================================
## Angle A (numeric, the user's standing ask): higher-degree B-branch perturber block

  Moves: UPPER bound DOWN toward < 0.2538893183, IF a B-perturber fires AND clears the
  5e-6 float gate. Honest prior: THIN (cross-term shrinks the firing margin, conversion
  factor collapsing ~14x/fill). Treat a structural "corrected B-marginal + screen" as the
  fallback deliverable if the gate fails.

  --- WHY THIS IS OPEN (R7 did NOT close it) ---
  R7's maximal-firing-set proof was about **A-base** blocks — blocks entering the A-arg
  prod-P^q side (arg_A = 61.66, the LOSING arg of D = max(arg_A, arg_B)). The R6 lemma's
  clean marginal r̃_Q = (1/D)∫_{A>B} log|Q| ds relies on D-CONSTANCY: an A-base block enters
  the losing arg, so dD/dq_Q = 0, no quotient cross-term. A **B-branch perturber** enters
  arg_B = 72.00, which ATTAINS D. So dD/dq_Q = +deg(Q) ≠ 0 — the D-constancy linchpin
  FAILS, and the first-variation marginal acquires a cross-term. This regime is UNANALYZED.

  --- THE CORRECTED B-BRANCH MARGINAL (derive + verify FIRST; this is the spec-review item) ---
  With log h = ⟨G⟩/D, ⟨G⟩ = ∫_0^1 G ds, G = max(A, B), and a B-perturber sending
  B(s) → B(s) + q_Q·log|Q(χ(s))| and arg_B → arg_B + q_Q·deg(Q) (so D = arg_B grows):

      d(log h)/dq_Q|_0 = [ d⟨G⟩/dq_Q · D − ⟨G⟩·dD/dq_Q ] / D²
                       = (1/D)·∫_{B>A} log|Q(χ)| ds  −  ⟨G⟩·deg(Q)/D²
                       = (1/D)·[ ∫_{B>A} log|Q(χ)| ds  −  (log h)·deg(Q) ].

  Define **m_B(Q) := (1/D)[ ∫_{B>A} log|Q| ds − (log h)·deg(Q) ]**. FIRING ⟺ m_B(Q) < 0,
  i.e. ∫_{B>A} log|Q(χ)| ds < (log h)·deg(Q) ≈ 0.25389·deg(Q).

  Two sign facts the builder MUST pin (these are the load-bearing subtleties):
   - The active region for a B-perturber is {B>A} (B attains the max there) — the COMPLEMENT
     arc of the A-base active set {A>B}. Measure of {B>A} ≈ 1 − 0.0686 ≈ 0.931 (most of [0,1]).
   - The cross-term −(log h)·deg(Q)/D is NEGATIVE (firing-favorable, REWARDS high degree):
     growing D lowers log h = ⟨G⟩/D. So a high-deg B-perturber gets a deg-proportional
     firing bonus ≈ −0.25389·deg(Q)/D. The firing question is whether ∫_{B>A} log|Q| ds
     (which is POSITIVE on most of the contour since |Q|>1 there for an admissible block —
     this is the anti-firing term) stays below (log h)·deg(Q). This is a genuine
     transfinite-diameter condition on the COMPLEMENT arc, not yet screened.

  Skeleton:
    1. DERIVE m_B(Q) as above; CONFIRM the envelope step (d⟨G⟩/dq_Q = ∫_{B>A} log|Q|, since
       B is the active branch on {B>A}) and the D-growth step (dD/dq_Q = deg Q) — both clean
       calculus on max(A,B) with B attaining D. — by hand + sympy, ~minutes.
    2. VERIFY m_B against a central finite-difference of log h on the held R4 anchor, for a
       KNOWN admissible B-perturber already in the family (Q5=j13 deg12 or Q6=j15 deg16,
       evaluated as a marginal at its q_E/q_F by ±eps — NOT at 0; OR use a fresh small test
       perturber). The FD-vs-closed-form ratio must be 1.000 ± a few e-3, mirroring R6's
       check for the A-marginal. This certifies the cross-term SIGN AND MAGNITUDE before any
       search. — reuse `verify_firstvar_lemma.finite_diff_marginal`, retargeted to the B
       branch. ~1-2 min.
    3. STATE the design optimization: minimize m_B(Q) over admissible B-perturbers Q ∈ Z[X]:
         (c1) Q(0) = Q(1) = 1  (B-branch perturbers REQUIRE this — run_state Rule; A-base
              blocks were exempt, B-perturbers are NOT);
         (c2) coprime + squarefree (in w = z(1−z)) vs the active dictionary
              {P1,P2,P4,P6,P8,j3,j9, Q1,Q2,Q5,Q6} (Doc01a cond (4); sympy gcd);
         (c3) contour-root-free: min_s |Q∘χ| ≥ ~1e-2 (so log|Q∘χ| ∈ L¹);
         (c4) ORIGINAL preferred (∉ Flammang Table-1) but a borrowed firing block is a valid
              numeric break — the constraint here is firing + gate, not originality.
       Because the cross-term REWARDS degree, screen HIGHER-degree blocks (deg > 16, where
       run_state's "all low-deg B-perturbers dry, qG→0" does NOT apply — that was LOW deg).
    4. SCREEN candidates by m_B on the held R4 anchor (the q_Q=0 point for a NEW perturber);
       rank most-negative. Seed from: (a) Flammang Table-1 high-deg entries not in the dict
       (deg ≥ 18-24) that satisfy Q(0)=Q(1)=1; (b) the U^ν-well map RECOMPUTED for the {B>A}
       region (the complement arc — the existing well map in R6/R7 was for {A>B}; the
       B-branch needs the complement potential U^ν_B(ζ) = ⟨log|ζ−χ|·1_{B>A}⟩_s). The
       root-potential factorization still holds: m_B(Q) = Σ_ρ U^ν_B(ρ) + deg·(log|lead| −
       log h/... ) — re-derive the per-root form including the cross-term as a flat
       −(log h)/D per unit degree.
    5. CHEAP FLOAT PRE-GATE (mandatory, run_state Rule) on the top firing candidate BEFORE any
       certify: clone `verify_upper_q8A.float_value_q8A` to a q9 PERTURBER-slot path (new
       free B-exponent qJ, seed 0), joint Nelder-Mead re-opt of all exponents at N ≥ 4M.
       Require N-STABLE drop ≥ 5e-6 below 0.2538893183 (≥10x the ~2e-7 cert slack), stable
       across N = 400k and N = 4M. If drop < 5e-6 → STOP; record the corrected-B-marginal +
       screen as the STRUCTURAL deliverable. If ≥ 5e-6 → proceed to certify.
    6. CERTIFY (only if step 5 passes): branch-and-bound on a q9-perturber harness (clone of
       verify_upper_q8A with a third perturber block), HELD_CERT set to the TRUE held
       0.2538893183 (NOT a stale hardcoded value — run_state Rule), frontier = 0 required,
       ~8 min. Note the D-formula now has the new perturber in arg_B; re-verify which branch
       attains D after re-opt (a D-switch would re-break the marginal — flag it).

  Hard step (load-bearing): **getting the cross-term sign/magnitude of m_B right so the
  marginal actually predicts firing, AND finding a B-perturber whose joint-reopt drop clears
  the 5e-6 gate.** Mechanism: the marginal is d(log h)/dq_Q = (1/D)∫_{B>A}log|Q| − (log h)·
  deg(Q)/D; the cross-term −(log h)deg/D is the NEW, degree-rewarding term absent from the
  R6 A-base lemma. Firing requires the positive ∫_{B>A}log|Q| (anti-firing, since |Q|>1 on
  most of the complement arc) to be beaten by (log h)·deg(Q). Whether any admissible Q
  achieves this — and whether the realized joint-reopt drop survives the conversion-factor
  collapse to clear 5e-6 — is genuinely unknown and is exactly what step 2's FD check and
  step 5's gate decide. Risk: explorer warns this is THIN; the cross-term may not make any
  admissible block fire by a margin that converts above the gate.

  Check (what the builder runs/derives):
   - sympy derivation of m_B + the FD-vs-closed-form ratio check on a known B-perturber
     (step 2) — this is the SPEC-REVIEW-CRITICAL artifact; reviewer re-derives the cross-term
     and re-runs the FD match independently.
   - `screen_Bbranch.py` (new): computes U^ν_B on the {B>A} complement arc, scores candidates
     by exact m_B, gates (c1)-(c3) via sympy, prints firing originals/borrowed, most-negative
     first. Cross-checks against the root-potential identity to <1e-5.
   - THEN the N≥4M float pre-gate (step 5), and ONLY if it clears 5e-6, the ~8-min certify.

  CRASH-SAFETY NOTE: the builder MUST do the CHEAP steps first — (1) hand+sympy derivation of
  m_B, (2) the ~1-2 min FD verification, (3) the minutes-long `screen_Bbranch.py`, (4) the
  N≥4M float pre-gate — BEFORE any ~5-8 min certify. One silent multi-minute certify call
  trips the stuck watchdog (R1, R3). Emit progress between each step. Certify is the LAST
  step and only runs if the gate passes.

================================================================================
## Angle B (structural, bankable milestone): rigorize the R6 first-variation lemma

  Moves: NO numeric change to the bound; logs a verified STRUCTURAL milestone (the publishable
  KERNEL of the paper). Independent of Angle A — can be the round's deliverable on its own, or
  the fallback if Angle A's gate fails.

  --- THE LEMMA TO PROVE (statement; from R7_explore_nextstep Q2 + outline-review-firstvar) ---
  With χ(s) = z(1−z), z = e^{2πis}, s ∈ [0,1]; A_0, B finite sums of q_i·log|R_i∘χ| for integer
  polys R_i; Q an integer poly; G(s,q) = max(A_0(s) + q·log|Q(χ(s))|, B(s)); Φ(q) = ∫_0^1 G ds.
  CLAIM: Φ is right-differentiable at q = 0 and
        Φ'(0+) = ∫_{{A_0>B}} log|Q(χ(s))| ds =: r̃_Q.
  (Then d(log h)/dq_Q = (1/D)·Φ'(0+) by the D-constancy step, B-branch attains D.)

  Skeleton:
    1. (a) D-constancy / no cross-term: arg_A = 61.55 < arg_B = 71.99 on the R2 anchor; arg_A
       is affine in q_Q with slope deg Q, so D ≡ arg_B locally constant, dD/dq_Q = 0 on
       |q_Q| < δ with δ = (arg_B − arg_A)/deg Q ≈ 1.3 (deg 8). PIN δ; note the ±eps FD check
       (eps = 1e-4 ≪ δ) stays in the window. — verified on disk, the easy half.
    2. (b) Φ'(0+) = r̃_Q via DOMINATED CONVERGENCE on the difference quotient (the
       citation-free body; Danskin/Bertsekas as a corroborating citation, NOT a dependency):
         - difference quotient (G(s,q)−G(s,0))/q is 1-Lipschitz (max is 1-Lipschitz in any
           added term), DOMINATED by |log|Q∘χ|| ∈ L¹ (H1′: candidate Q contour-root-free →
           log|Q∘χ| bounded, audited min|Q∘χ|: j9 1.06e-2, j3 4.07e-2);
         - a.e. pointwise limit = log|Q∘χ|·1_{A_0>B} for s ∉ K (the kink set);
         - DCT ⇒ Φ'(0+) = ∫_{A_0>B} log|Q∘χ| ds.
    3. (c) K = {A_0 = B} has measure zero: A_0 − B is real-analytic OFF the finite contour-root
       set of its constituent blocks and ≢ 0 (max +2.52, min −194; 64 sign changes STABLE
       across N = 5e5, 2e6, 8e6), so K is finite. The moving-boundary term ∮_K (A_0−B)·
       (∂boundary/∂q) = 0 because A_0 − B = 0 ON K (continuity of the max across the kink) —
       NOT because the boundary is fixed. THIS IS THE LOAD-BEARING "2nd-order" line.
    4. Corollary (scoped HONESTLY): the SIGN of r̃_Q is a weighted-integer-Chebyshev condition
       on the active arc {A_0>B}. Do NOT claim the full inf_Q r̃_Q ≍ −log t_{Z,φ} equivalence
       (future work) nor "lower locus = complement of upper arc" (UNSUPPORTED — run_state Rule).

  Hard step (load-bearing): **the active-set boundary term vanishes at first order** — for
  G = max(A_0 + q·log|Q∘χ|, B), Φ'(0+) = ∫_{A_0>B} log|Q∘χ| ds. Mechanism: the kink set
  K = {A_0=B} is finite (A_0−B real-analytic, ≢0 on the arc), and the moving-boundary
  contribution is ∮_K (A_0−B)·(dboundary/dq) = 0 because A_0−B = 0 ON K (continuity of max
  across the kink), NOT because the boundary is fixed. DCT on the 1-Lipschitz difference
  quotient then needs only that K has measure zero.

  --- MANDATORY STATEMENT CORRECTIONS (from R7-outline-review-firstvar.md — the builder MUST
      apply these or the reviewer hits a contradiction at the first dictionary block) ---
   - **H1 is FALSE as originally stated** ("no block has a contour root"). P1 = X vanishes at
     χ(s=0)=0; A_0 has integrable −∞ log-singularities. REPLACE with:
       (H1′) only the CANDIDATE Q is contour-root-free (⇒ log|Q∘χ| bounded, L¹);
       (H1″) A_0, B real-analytic OFF the finite contour-root set of their blocks, with
             integrable −∞ log-singularities, A_0 → −∞ at each (so a neighborhood lies in
             {A_0<B}, never touching K or the active integrand).
   - **The active arc is NOT "[0, 0.8221]"** (a stale R6 number in a different convention). In
     the s ∈ [0,1] harness convention it is a UNION OF ~32 INTERVALS (K = 64 points), total
     measure ≈ 0.0685, and does NOT start at s=0 (s=0 is the DEEPEST inactive point). State ν's
     support on this finite union.
   - State the kink case as a.e. (s ∉ K), pin K finite from real-analyticity (not a hand-wave).
   - Keep the DCT body, the Danskin/Bertsekas citation-not-dependency framing, and the
     upper-internal dual-loci scoping verbatim.

  Check (what the builder runs/derives): reproduce `verify_firstvar_lemma.py` (N=4M: central-FD
  match <0.1% on j3/j6/j7/j9, root-potential identity 5.2e-17), the kink-count stability audit
  (64 crossings stable to N=8e6), and min|Q∘χ| audit (candidate contour-root-free). The lemma's
  proof body is re-derived by hand by the reviewer; the numerics back it.

  CRASH-SAFETY NOTE: this angle is a WRITE-UP + a re-run of the existing `verify_firstvar_lemma.py`
  (~54s at N=4M) and a cheap kink/contour audit — no ~8-min certify, no stall risk. Emit progress
  while writing. The expensive numeric is the single N=4M lemma re-run; everything else is prose.

================================================================================
## RANKING & RECOMMENDATION

**Build Angle A this round; carry Angle B as a bankable in-round fallback.**

1. **Angle A (B-branch perturber) — BUILD FIRST.** It is the ONLY genuinely-open NUMERIC lever
   and directly serves the user's standing ask (a numeric break / a constructed improving
   block). Its load-bearing cross-term derivation is NOVEL and must be checked (spec review).
   The cheap path (derive m_B → FD-verify the cross-term sign → screen → N≥4M float gate) is
   crash-safe and bounded; the ~8-min certify runs ONLY if the gate clears 5e-6. EITHER outcome
   is a deliverable: a numeric break if it fires through the gate, OR a verified
   corrected-B-marginal + screen (a NEW first-variation result for the D-attaining branch,
   structural) if the gate fails. The explorer warns the gate likely FAILS (cross-term shrinks
   the margin; conversion collapsing) — so plan for the structural-B outcome and keep Angle B
   ready.

2. **Angle B (rigorize the R6 lemma) — IN-ROUND FALLBACK / bankable milestone.** If Angle A's
   float gate fails AND the corrected-B-marginal screen does not itself rise to a clean
   milestone in the reviewer's eyes, the builder should ALSO write up Angle B (outline +
   outline-review already on disk; the only expensive step is one N=4M re-run of an existing
   harness). This is the cleanest single-round structural milestone with the lowest stall risk
   and is the publishable kernel. It is independent of Angle A, so it banks a milestone
   regardless of whether the B-branch fires.

   Builder order: do Angle A's CHEAP steps (m_B derivation + FD verify + screen + float gate)
   FIRST. If the gate clears → certify (Angle A numeric break, the headline). If the gate fails
   → the round still has (i) the verified corrected-B-marginal + screen from Angle A and (ii)
   Angle B's rigorized lemma. Deliver the strongest of these that the reviewer can verify.

3. (Angle C — different family / BMQS / base-swap: CLOSED as a distinct lever per the explorer;
   do NOT pursue. A-base enrichment: PROVEN saturated, run_state hard rule; do NOT pursue.)

Spec-review verdict: **REQUIRED** — Angle A's corrected B-branch cross-term marginal
m_B(Q) = (1/D)[∫_{B>A} log|Q| − (log h)·deg(Q)] is novel and load-bearing; its sign/magnitude
must be checked (against the FD on a known B-perturber) BEFORE the builder spends certify
compute on a block selected by it.
