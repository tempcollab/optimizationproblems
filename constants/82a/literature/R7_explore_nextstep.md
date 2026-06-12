# 82a UPPER — R7 explorer: which Next step is the softest single-round milestone?

Scope: read-only triage of the three R6 "Next" candidates + the Angle-4 numeric lever.
Sources on disk ONLY: current.md, R6-integer-transfinite-diameter.md (approach +
build), /tmp/round-6/{build,proof-reviewer}.md. No new PDFs, no certify run.

State recap (authoritative, run_state R4): held UPPER = **0.2538893183** (verified R4,
A-base j3+j9 on Doche Doc01a §4 family). R6 logged a STRUCTURAL milestone (14 total),
NO numeric break. The held A-base lever is near-saturated (R2 j3 +1.49e-4 -> R4 j9
+3.2e-6, ~47x/step decay; next same-kind step projects ~1e-7 = at/below cert slack).

================================================================================
## Q1 — Rank the three Next candidates by tractability for ONE round

The three candidates (run_state "Next"): (i) fully rigorize the Danskin
moving-boundary directional-derivative identity; (ii) generalize the lemma off the
special D-config (cross-term when A attains D); (iii) write up the weighted-integer-
transfinite-diameter (WITD) unification (Doche-upper vs Flammang-lower) as the paper
thesis.

**Ranking (softest first):**

**#1 — (i) Rigorize the Danskin/envelope directional-derivative identity. SOFTEST.**
  - Why softest: the object already EXISTS and is verified numerically — R6 matched the
    closed-form (1/D)·r̃_Q to a central finite-difference of log h to <0.1% on j9/j6/j7,
    and the potential-theoretic factorization r̃_Q = Σ_ρ U^ν(ρ)+deg·log|lead| to 5.2e-17
    for j3. So the round is converting a numerically-verified identity into a written
    rigorous lemma with hypotheses — a WRITE-UP + proof-tightening task, not a search.
  - Single reviewer-verifiable deliverable: a self-contained lemma statement + proof
    where the load-bearing line (the moving-boundary term is O(q_Q²)) is established by
    a named, citable theorem rather than "by Danskin, numerically confirmed."
  - Hard step (named): the active-set boundary {A_0=B} moves with q_Q; one must show
    the boundary-motion contribution to d⟨G⟩/dq_Q vanishes at first order. This is the
    Reynolds-transport / Leibniz boundary term ∮_{∂{A>B}} (A−B)·(∂boundary/∂q_Q); it
    vanishes because A−B = 0 ON the boundary (continuity of the max across the kink),
    NOT because the boundary doesn't move. The proof must (a) confirm {A_0=B} is a
    finite point set (A_0−B real-analytic, ≢0 on the arc), (b) confirm G(·,q_Q) is
    Lipschitz in q_Q with a.e. derivative log|Q|·1_{A>B} ∈ L¹, (c) invoke
    differentiation-under-the-integral / Danskin for the max of two C¹ functions.

**#2 — (iii) Write up the WITD unification as the paper thesis. SECOND, LOW RISK but
LOW HEADLINE.**
  - Why not #1: the rigorously-checkable CORE of this is ALREADY DONE and verified in
    R6 (verify_shared_pool.py: exact identities P4=j5,P6=j8,P8=j12,Q5=j13,Q6=j15,j3,j9
    all Flammang Table-1; 11-block dict squarefree + all 55 pairs coprime; dual loci
    scoped UPPER-INTERNAL). Re-running it logs no NEW milestone (eval counts only new
    verified advances). The genuinely-new part — turning "both sides draw from one
    pool" into a THEOREM (inf over admissible integer Q of r̃_Q relates to the weighted
    integer transfinite diameter t_{Z,φ} on the active arc) — is the hard, open part and
    is NOT a single-round task. As a write-up it is real but it leans on (i): the
    "upper-side selection = integer-Chebyshev on the active arc" statement is only
    rigorous once the first-variation identity (i) is a proved lemma.
  - Hard step: the WITD inequality itself (inf_Q r̃_Q ≍ −log t_{Z,φ}(active arc)) is a
    genuine new theorem with a real lower-bound side — too big for one round. Honestly
    scoped, this round's (iii) deliverable would only be a FRAMING section, which the
    reviewer may decline to log as a fresh milestone since the checkable facts are R6's.

**#3 — (ii) Generalize the lemma off the special D-config (A-attains-D cross-term).
HARDEST / lowest payoff this round.**
  - Why hardest: when arg_A attains D (A-branch wins), dD/dq_Q = deg(Q) ≠ 0, so the
    clean identity d(log h)/dq_Q = (1/D)·r̃_Q acquires a quotient cross-term
    −⟨G⟩·deg(Q)/D². Deriving the cross-term form is straightforward algebra, BUT it is
    not reviewer-VERIFIABLE on the held family: the held family's D is attained by the
    B-perturber branch (arg_A 61.66 < arg_B 72.00, gap ~10.3), so there is NO on-disk
    configuration where A attains D to finite-difference-check the cross-term against.
    The builder would have to CONSTRUCT a new A-dominant family first (a numeric search,
    against the anti-stall rule and likely a worse held), then verify — two hard steps,
    high stall risk, and the result is a generalization nobody can exercise on the live
    family. Lowest milestone-per-round.

================================================================================
## Q2 — The Danskin/envelope step: what exactly must be proven, and is on-disk
       machinery enough or is one external reference needed?

**Precise statement to prove.** With chi(s)=z(1−z), z=e^{2πis}, s∈[0,1], A_0,B real-
analytic on [0,1], Q an integer poly with no root on the contour chi([0,1]) (so log|Q∘chi|
is bounded and real-analytic where A_0>B), define G(s,q)=max(A_0(s)+q·log|Q(chi(s))|, B(s))
and Φ(q)=∫_0^1 G(s,q) ds. Then Φ is right-differentiable at q=0 and
        Φ'(0+) = ∫_{{A_0>B}} log|Q(chi(s))| ds  =: r̃_Q.

**The two pieces and their justification:**
1. **Differentiation under the integral / a.e. pointwise derivative.** Off the kink set
   K={s: A_0(s)=B(s)}, ∂_q G = log|Q∘chi|·1_{A_0>B} pointwise; |G(s,q)−G(s,0)| ≤
   |q|·|log|Q∘chi(s)|| (1-Lipschitz max), and log|Q∘chi| ∈ L¹([0,1]) (integrable log-
   singularities only at the finitely many s where chi(s) hits a root of Q, none on the
   contour for the active dict). Dominated convergence gives Φ'(0)=∫ ∂_q G.
2. **K has measure zero / boundary term vanishes.** A_0−B is real-analytic and ≢0 on
   [0,1] (it changes sign — the held active arc is [0,0.8221]), so K is finite; the
   integration-limit motion contributes ∮_K (A_0−B)·(dboundary/dq) = 0 because A_0−B=0
   on K. This is the load-bearing "2nd-order" line.

**Is the on-disk machinery sufficient?** The NUMERICS are fully on disk and reviewed
(R6 FD match <0.1%, ratio 1.000±0.001 central; potential-id 5.2e-17). The MISSING piece
is a citable theorem name for the max-of-two-smooth-functions envelope so the reviewer
re-derives a *theorem*, not a numerical coincidence. Two acceptable routes, BOTH already
present in spirit on disk:
  - **Danskin's theorem** (Danskin 1967 / Bertsekas, *Nonlinear Programming*, Prop. on
    directional derivatives of max-functions): for f(q)=max_i g_i(q) with g_i C¹, the
    directional derivative is the max over the ACTIVE index set of the directional
    derivatives. Here the index set is {A,B} and the active branch a.e. is the one
    achieving the max — directly gives ∂_q G = ∂_q(active branch). This is the cleanest
    single external citation.
  - Equivalently, **Reynolds/Leibniz with vanishing boundary term**, fully elementary
    given K finite and A_0−B=0 on K — needs NO external reference, just the real-
    analyticity of A_0−B (provable on disk: A,B are finite sums of log|integer poly∘chi|,
    real-analytic off contour-roots, which the active dict avoids).

**Verdict for Q2:** the on-disk machinery is sufficient for a SELF-CONTAINED elementary
proof (route 2) — no external reference is strictly required, because every ingredient
(real-analyticity of A−B, K finite, L¹ domination, the central-FD numerical
corroboration) is on disk. ONE external citation (Danskin/Bertsekas) makes it cleaner
and more obviously correct to the reviewer, and is the recommended single reference to
name. The builder should NOT need to download anything: state Danskin's theorem from the
standard reference and give the elementary boundary-cancellation argument as the proof
body.

================================================================================
## Q3 — Bonus numeric lever: any UNTRIED admissible block with a marginal that could
       give a drop >5e-6, or is the A-base lever saturated?

**Reconciliation of sign convention (CRITICAL — the dispatch phrasing is inverted).**
The R6 lemma's firing criterion is: **Q FIRES (q_Q>0 LOWERS log h, i.e. IMPROVES the
upper bound) ⟺ r̃_Q < 0.** So a NEGATIVE first-order marginal r̃_Q is exactly the
FIRING / improving sign. The dispatch's "j16/j17/j20 have NEGATIVE first-order marginal
(won't fire)" is BACKWARDS on the sign: the R6 screen reports

    j16 (deg16): r̃ = −0.0073   (NEGATIVE => predicted to FIRE)
    j17 (deg16): r̃ = −0.0060   (NEGATIVE => predicted to FIRE)
    j20 (deg20): r̃ = −0.0050   (NEGATIVE => predicted to FIRE)

all squarefree and coprime to the active dictionary. So per the first-order lemma these
three DO have firing-sign marginals — they are NOT dead on sign. The dispatch likely
mis-summarized the build's Angle-4 note (which lists them as untried CANDIDATES, not as
dry blocks). **Corrected finding: there ARE untried admissible blocks with firing-sign
(negative) first-order marginal.**

**But will any clear the >5e-6 float gate? Almost certainly NOT — the A-base lever is
saturated. Magnitude calibration from the on-disk verified anchors:**
  - j3 fired with r̃ = −0.0229  -> realized drop +1.49e-4 (R2).
  - j9 fired with r̃ = −0.0068  -> realized drop +3.2e-6  (R4).
  Ratio realized-drop/|r̃|: j3 ~6.5e-3, j9 ~4.7e-4 — the conversion factor itself
  collapses ~14x as the dictionary fills (the realized drop is the CONDITIONAL residual
  after the other 8 exponents re-optimize, far smaller than the raw r̃).
  - j16 has r̃ = −0.0073, ~ the SAME magnitude as already-fired j9 (−0.0068). Applying
    j9's (already-shrunk) conversion gives a projected realized drop ~3e-6 — i.e.
    SAME ORDER as j9's +3.2e-6, which is BELOW the 5e-6 float gate and only ~15x the
    ~2e-7 cert slack. And j16/j17/j20 are deg 16/16/20 — HIGHER degree than j9 (deg 8),
    so (a) they push arg_A toward arg_B=72 faster (D-switch risk: arg_A 61.66 + q·deg
    can cross 72 and re-introduce the dD/dq cross-term, breaking the clean regime), and
    (b) they are MORE redundant with the now-larger active dict {…,j3,j9,Q5(deg12),
    Q6(deg16)} — j16/Q6 are both deg16, so j16's conditional residual after Q6 is in the
    dict is likely far below its raw r̃.

**Q3 verdict: the A-base lever is SATURATED for a >5e-6 nudge.** The untried blocks have
the right (negative/firing) SIGN but their projected realized drop is ~3e-6 or less —
below the mandatory 5e-6 float pre-gate and not safely above cert slack. No bonus
certify is warranted in R7. (If a future round still wants to try, the ONLY admissible
path is the mandatory joint N≥4M float pre-gate on j16 first; expect it to FAIL the gate.
Do not certify on the raw-marginal sign alone — the conversion-factor collapse and
deg16/Q6 redundancy will eat it.)

================================================================================
## RECOMMENDATION — single best plan target for Round 7

Target **(i): turn the R6 first-variation lemma into a fully rigorous, self-contained
written lemma** — state hypotheses (A,B real-analytic finite sums of log|integer poly∘chi|;
Q with no contour root; B-branch attains D so dD/dq_Q=0 locally), prove Φ'(0+)=r̃_Q via
the Danskin/envelope route with the boundary term vanishing because A−B=0 on the finite
kink set K, and cite Danskin (Bertsekas, *Nonlinear Programming*) as the one external
reference for the max-function directional derivative. The numerical corroboration
(central-FD match <0.1%, potential-id 5.2e-17) is already on disk and reproducible via
verify_firstvar_lemma.py, so the reviewer can re-derive the proof AND re-run the check —
a clean, falsifiable, single-round milestone that elevates the campaign above number-
shaving (the user's R6 redirect). Fold the shared-pool/WITD framing in only as a short
corollary section (it rides the already-verified verify_shared_pool.py), and do NOT
spend the round on (ii) (no live A-dominant family to verify the cross-term against) or
on an Angle-4 certify (the A-base lever is saturated; projected drop ~3e-6 < the 5e-6
gate). Do NOT touch the lower side (run_state: repo's 0.2524 lower is user-flagged WRONG;
real lower is Flammang 0.2487458 — analogy source only).
