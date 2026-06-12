# R8 explore triage v2 — 82a UPPER (Zhang-Zagier essential minimum)

Explorer: math-explorer, round 8. Triage ONLY — no improvement attempted. On-disk
artifacts only (no new PDFs, no long silent ops).

Authoritative held (run_state R4 / current.md / verify_upper_q8A.py header):
**upper held = 0.2538893183**, family = Doche Doc01a §4 with **j3 (deg 3) + j9 (deg 8)
as A-base blocks** on the prod-P^q side; perturbers Q1*Q2*Q5^qE*Q6^qF (Q5=j13 deg12,
Q6=j15 deg16). Harness: `certificate/verify_upper_q8A.py`. Best LOWER held = 0.2524001332
(R17, OSS energy cert). Two-sided gap ~0.00149.

================================================================================
## (a) VERDICT on R8_explore_triage.md: DISCARD — stale / mismatched-lineage.

`R8_explore_triage.md` is **unreliable and must be discarded**. It does NOT describe a
lever on our held family. Concrete proof from on-disk artifacts:

1. **Wrong held value.** It states "upper held = 0.2543185491 [this repo R7]." Per
   current.md line 98, 0.2543185491 is the **PRIOR-campaign R7** value — the old
   `verify_upper_q3.py` ell=1 single-Qa-block family. The AUTHORITATIVE held is
   0.2538893183 (R4 this campaign, j3/j9 A-base, `verify_upper_q8A.py`). 0.2543185491
   is WORSE than the real held by +4.29e-4 — it is a superseded record, not the bar.

2. **Wrong lineage.** It builds on "Qa/Qb deg-24 perturber blocks" via `verify_upper_q3.py`.
   That Qa/Qb path is the OLD R7->R9 lineage (h=Q1*Q2*Qa^qB*Qb^qC). It was ABANDONED at
   R10/R11 (Qa,Qb DROPPED, replaced by Q5=j13, Q6=j15) and the entire family was then
   superseded by the R2/R4 A-base j3/j9 construction. The held harness is
   `verify_upper_q8A.py`, NOT `verify_upper_q3.py`. The git history (R2 j3, R4 j9) confirms
   the j3/j9 A-base lineage; "Qa/Qb" matches nothing in the held family.

3. **The 5.3e-5 probe is anchored to a mismatched baseline => MEANINGLESS for us.** Its
   probe reads "R7 6-exp float (Qa only) = 0.2543184416 ... + Qb 2nd free block = 0.2542655469,
   DROP 5.29e-5." That drop is measured DOWN FROM 0.25431844 — a family that is itself
   +4.3e-4 WORSE than our held 0.2538893183. The probed endpoint ~0.2542655 is still far
   ABOVE (worse than) the authoritative held. So the "5.3e-5 structural gain, well not
   drying up" claim is an artifact of standing on a superseded baseline. On the REAL held
   family the Qa/Qb deg-24 blocks are not even present (dropped at R11). **Discard the
   probe; it is not a lever on our held family.**

4. **Internal staleness corroborates.** The file's PATH B says "lower 0.24874 [F18], only
   REPRODUCED, never beaten" — but current.md shows the lower has been beaten four times
   this campaign (R14->R15->R17, held 0.2524001332). The file pre-dates the entire
   R10-R17 work; it is an OLD draft mis-named "R8" (file mtime 17:44, before this round).

CONCLUSION: `R8_explore_triage.md` is stale/alternate-lineage. Its recommendation
(PATH A = add Qb), its held value, and its 5.3e-5 probe are ALL anchored to the
abandoned Qa/Qb deg-24 ell=1 family and have no bearing on the authoritative j3/j9 held.
Do not act on it. Authoritative guidance: run_state.md + this file.

================================================================================
## (b) RANKED upper-side levers GENUINELY open on the held j3/j9 family.

### Lever 1 (RANK 1, but a NEGATIVE/structural lever): the R6 first-variation-LEMMA RIGORIZATION.
- Type: WRITE-UP / proof rigor, not a numeric break. Milestone-grade (the reviewer logs
  structural milestones; R6 and R7 each scored one this way).
- Softness: SOFTEST genuinely-open step. The object already exists and is numerically
  verified (R6: closed-form (1/D)*r_tilde matches central finite-diff of log h to <0.1%
  on j9/j6/j7; potential-theoretic identity to 5.2e-17 on j3). Converting it to a written
  rigorous lemma is a write-up + proof-tightening task, NOT a search. Outline ALREADY
  drafted: `approaches/R7-firstvar-rigorous.md` + `R7-outline-review-firstvar.md`, and the
  detailed statement/hard-step is in `literature/R7_explore_nextstep.md` Q2.
- Single named hard step: show the active-set boundary term vanishes at first order — for
  G(s,q)=max(A0(s)+q*log|Q(chi(s))|, B(s)), Phi(q)=int G ds, prove Phi'(0+)=int_{A0>B} log|Q| ds.
  Load-bearing line: the kink set K={A0=B} is finite (A0-B real-analytic, not identically 0
  on the arc) and the moving-boundary contribution is int_K (A0-B)*(dboundary/dq)=0 because
  A0-B=0 ON K (continuity of the max across the kink), NOT because the boundary is fixed.
  Routes: (route 2, self-contained, NO external ref) elementary Reynolds/Leibniz with the
  vanishing boundary term + L1-dominated convergence; (route 1, cleaner) cite Danskin's
  theorem (Bertsekas, Nonlinear Programming) for the directional derivative of a max of two
  C^1 functions. Outline-review flagged H1 needs correction (candidate-Q contour-root-free;
  active locus = union of ~32 intervals, measure ~0.0685, no s=0) — already noted on disk.
- Why rank 1 despite being non-numeric: it is the only CLEAN single-round milestone with
  an outline+outline-review already on disk, it is the publishable KERNEL of the paper, and
  the user's R6/R7 redirect explicitly elevated structural results over number-shaving.

### Lever 2 (RANK 2, the only plausibly-open NUMERIC lever): the B-branch PERTURBER addition.
- Type: numeric break candidate. Status: OPEN but with a CAVEAT that must be checked first.
- Why it is NOT closed by R7: the R7 maximal-firing-set proof was specifically about
  **A-base** blocks (blocks entering prod-P^q, the LOSING D-arg argA=61.66). A B-branch
  perturber enters the WINNING D-arg argB=72.00 (which ATTAINS D). The R6 first-variation
  lemma's clean form d(log h)/dq_Q=(1/D)*r_tilde relies on D-CONSTANCY (dD/dq_Q=0), which
  holds ONLY because an A-base block enters the losing arg. **A B-branch block enters the
  arg that ATTAINS D, so dD/dq_Q = +deg(Q) != 0 — the D-constancy linchpin FAILS and the
  marginal acquires a quotient cross-term:**
      d(log h)/dq_Q|_0 = (1/D)*[ int_{B>A} log|Q| ds ]  -  <G>*deg(Q)/D^2 .
  This is a DIFFERENT marginal than the A-base r_tilde; the R7 saturation analysis (which
  evaluated int_{A>B}, the A-base region) does NOT cover it. So the question "is a B-branch
  perturber firing?" is genuinely UNANSWERED on the held family.
- Softness assessment: MEDIUM-LOW. Two headwinds. (i) The cross-term -<G>*deg(Q)/D^2 is a
  RAISING (anti-firing) contribution proportional to deg(Q): with <G>=log(h)*D ~ 18.28 and
  D ~ 72, the cross-term is ~ -18.28*deg(Q)/72^2 ~ -0.00353*deg(Q) on the (1/D)-scaled
  marginal... [SIGN CHECK NEEDED by the outliner: the cross-term reduces log h as q grows
  the larger deg pushes D up, which LOWERS log h=<G>/D — so a high-deg B-perturber gets a
  bonus from the D-growth, but its int_{B>A} log|Q| firing region is the COMPLEMENT arc].
  This sign interplay is exactly what makes it un-pre-judged and worth a float probe. (ii)
  run_state says "all LOW-DEG B-perturbers are dry" (R2 Angle 1: qG->0; R7 note) — but that
  was LOW degree. A HIGHER-degree B-branch block (deg > 16, original or borrowed) has NOT
  been screened with the corrected cross-term marginal. **This is the single genuinely-open
  numeric lever.**
- Single named hard step: compute the corrected B-branch first-variation marginal
  m_B(Q) = (1/D) int_{B>A} log|Q(chi)| ds  -  <G>*deg(Q)/D^2  on the held R4 anchor
  (the B>A region is the COMPLEMENT of the A-base active arc, t in (0.8221,1] roughly), and
  find a coprime admissible Q (Q(0)=Q(1)=1, squarefree, coprime to {P1,P2,P4,P6,P8,j3,j9,
  Q1,Q2,Q5,Q6}) with m_B(Q) < 0 AND a joint-reopt float drop clearing the 5e-6 gate. Must
  re-derive the cross-term sign carefully (the R6 lemma does NOT apply verbatim — D is no
  longer constant) and re-check for a D-switch.
- Honest caveat: the cross-term makes the firing margin SMALLER in magnitude (the -<G>*deg/D^2
  works against int_{B>A}log|Q| if log|Q|<0 on the firing arc), and the realized-drop/
  marginal conversion factor has been collapsing ~14x per dictionary fill (j3->j9). So even
  if a B-perturber fires, expect the realized drop to be sub-1e-5; it may not clear the
  5e-6 float gate. The lever is OPEN but THIN. Worth ONE float pre-gate, not a blind certify.

### Lever 3 (RANK 3): a qualitatively DIFFERENT family (BMQS mu_{P,Q} weighted-product / different base set).
- Type: structural / exploratory. Status: largely CLOSED as a *distinct* lever.
- Why mostly closed: R1 already scoped BMQS Thm 4.5 mu_{P,Q}. Verdict on disk
  (R1_explore_bmqs_thm45.md, R7_explore_polya.md, role-memory): the bare single-pair
  mu_{P,Q} gives 0.34-0.69 (hopeless), and the only live value is the weighted-product
  recast — which IS the Doche family already in use. BMQS strong duality => no separate gap
  to harvest; it only relabels the same LP. So "switch to BMQS" is NOT a distinct lever.
- The one un-exhausted sub-angle: a STRUCTURALLY different BASE-set choice (different P_i,
  not the Doche {P1=X,P2,P4,P6,P8}) or a BLOCK-SWAP (replace, not add, a base block). R7
  proved the A-base ADD lever saturated, but did NOT exhaustively prove no swap helps;
  `screen_swap_R5.py` exists on disk and could be re-pointed. Softness: LOW (high search
  cost, no targeted objective, stall risk), payoff uncertain. Not recommended for R8.

================================================================================
## (c) RECOMMENDATION.

**Honestly report the A-base numeric lever is saturated, and pivot to the
structural/rigor milestone (Lever 1: the R6 first-variation-lemma rigorization).**

Reasoning:
- The A-base lever is PROVEN saturated (R7, reviewer-verified, deg<=16 / ~80k candidates):
  every coprime original monic factor costs r_tilde >= +0.013 > |best firing margin -0.005|,
  and the best reachable block (j16) converts to a float drop 2.94e-6 < the 5e-6 gate. Do
  NOT spend R8 on another A-base block (run_state hard rule).
- The B-branch perturber (Lever 2) is the only genuinely-open NUMERIC lever, but it is THIN
  (cross-term shrinks the margin; conversion factor collapsing; low-deg already dry) and the
  realistic upside is sub-1e-5, possibly below the gate. It is worth at most ONE float
  pre-gate as a BONUS probe — NOT a full round's bet, and NOT a certify on raw sign.
- Lever 1 (rigorize the R6 lemma) is the CLEAN single-round milestone: outline +
  outline-review already on disk (`R7-firstvar-rigorous.md`, `R7-outline-review-firstvar.md`),
  numerics already verified and reproducible (`verify_firstvar_lemma.py`), one named hard
  step (the Danskin/boundary-cancellation lemma), and it is the publishable kernel the user's
  R6/R7 redirect asked for. It scores a verified milestone with low stall risk.

PRIMARY plan for R8 (hand to outliner): rigorize the R6 first-variation lemma (Lever 1).
OPTIONAL bonus (only if time + a crash-safe atomic float probe): screen ONE higher-degree
B-branch perturber with the CORRECTED cross-term marginal m_B(Q) (Lever 2) at N>=4M float;
certify ONLY if it clears 5e-6 — expect it to fail, in which case the round still logs the
Lever-1 rigorization milestone. Do NOT pursue Lever 3 or any A-base addition.

================================================================================
## Dead ends (do NOT retry) — corrected for the AUTHORITATIVE lineage.
- A-base dictionary enrichment (add any block, original or borrowed) to the held j3/j9
  family: PROVEN saturated/DRY (R7, reviewer-verified). [run_state hard rule]
- Same-family q-tuning of the held family: gain ~3.6e-9 / sub-1e-6, DEAD.
- The Qa/Qb deg-24 ell=1 family and its "add Qb 5.3e-5" probe (R8_explore_triage.md):
  STALE LINEAGE, abandoned at R11, baseline +4.3e-4 worse than held. DISCARD.
- "BMQS mu_{P,Q} as a distinct upper lever": NOT distinct (bare hopeless; weighted recast =
  Doche family). [R1, R7_explore_polya]
- Low-degree B-branch perturbers: DRY (qG->0, R2 Angle 1). [Only HIGHER-deg B-perturbers
  with the corrected cross-term marginal remain untested — see Lever 2.]
- The "A-attains-D cross-term generalization" as a standalone exercise: no live A-dominant
  family on disk to finite-difference-verify against (held D attained by B-branch). The
  cross-term is, however, exactly the math NEEDED for Lever 2's B-branch marginal — use it
  there, where there IS a live config (B attains D), not as an A-dominant generalization.

## Files read (no new artifacts fetched)
- run_state.md, math-explorer role memory; current.md; R8_explore_triage.md (the suspect);
  verify_upper_q8A.py header (authoritative held harness); R7_explore_nextstep.md
  (Lever-1 hard-step detail). Certificate dir listing confirms verify_upper_q8A.py is the
  held harness and verify_upper_q3/q4 (Qa/Qb) are the abandoned prior lineage.
