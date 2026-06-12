# R9 explore triage — 82a UPPER (Zhang-Zagier essential minimum)

Explorer: math-explorer, round 9. Triage ONLY — no improvement attempted. On-disk
artifacts only (run_state, current.md, approaches/, literature/ digests, certificate/
headers). No new PDFs, no long silent ops.

Authoritative held (run_state R4 / current.md / verify_upper_q8A.py):
**upper held = 0.2538893183** (REVIEWER-VERIFIED, R4 this campaign). Family = Doche
Doc01a §4 limit-point, with **j3 (deg 3) + j9 (deg 8) A-base blocks** on the prod-P^q
side; perturbers Q1*Q2*Q5^qE*Q6^qF (Q5=j13 deg12, Q6=j15 deg16). Harness
`certificate/verify_upper_q8A.py`. Best LOWER held = 0.2524001332 (R17). Two-sided gap
~0.00149. Target to STRICTLY beat: 0.2538893183 (NOT the stale 0.2540419719 / 0.2543185491).

================================================================================
## Q1 — Is there a QUALITATIVELY DIFFERENT upper-side construction with a real
##      numeric opening below 0.2538893183? (BMQS mu_{P,Q} multi-pair / weighted-product)

**Answer: NO tractable one-to-few-round numeric opening. R1's "weighted recast = Doche"
conclusion forecloses the BMQS lever as a DISTINCT family. Verified from on disk
(R1_explore_bmqs_thm45.md, R7_explore_polya.md, role-memory):**

1. **Bare single-pair mu_{P,Q} is hopeless.** R1 ran the Prop-7.8 objective
   integral(g dmu_{P,Q}) on the simplest coprime monic-irreducible pairs: values
   0.34–0.69 (best ~0.340), vs the (then) record 0.25404. Far above held 0.25389.
   This is not a low-degree slack problem — it is structural: a single integer pair
   has NO free real-exponent direction, the very direction that drove R5–R11.

2. **Multi-pair / weighted-product is NOT a new family — it IS the Doche family.**
   BMQS's own Remark 4.6 (mu' via P^{deg Q}/Q^{deg P}) and §1.4's V=prod P^q direction
   are exactly the weighted-product / real-exponent generalization, which R1 identified
   as the Doche perturbed-polynomial limit measure already in use (h(q)=exp int g dmu_q,
   mu_q the equidistribution measure on {|prod P_m(chi)^{q_m}|=|Q1(chi)|}, chi=z(1-z),
   FREE REAL exponents). BMQS strong duality (Thm 6.5: P(g)=inf int g dmu = C_82) means
   there is NO separate gap between the mu_{P,Q} parametrization and the Doche
   parametrization — both are points of the SAME cone P^Z_log(C). A re-coordinatization,
   not new slack.

3. **A genuinely-different "finite convex combination of mu_{P,Q}" / different BASE-set
   configuration is, in principle, a different POINT of the cone, but:** (i) it has no
   targeted objective / efficient search compass — BMQS §1.7 explicitly state the
   "enormous search space, no efficient direction" wall; (ii) the only member ever found
   below ~0.34 is the Doche weighted-product member, which is the held family and is now
   proven SATURATED on both branches (R7 A-base, R8 B-branch); (iii) any new convex
   combination would have to BEAT the optimized Doche member, and Doche already sits in
   the favorable weighted-product part of the cone. The honest read: a multi-pair /
   finite-convex-combination BMQS campaign is a multi-round NEW-construction search with
   NO guarantee and no compass — NOT a one-to-few-round tractable opening below 0.25389.

**Verdict Q1: numeric upper lever via BMQS mu_{P,Q} (single-pair, multi-pair, or
weighted-product) is foreclosed / intractable in the round budget. The weighted recast
= Doche, and Doche is saturated.**

================================================================================
## Q2 — Is there ANY admissible CONSTRUCTION route left where the design principle
##      (minimize first-variation marginal over Z[X]) still produces a numeric
##      improvement? Or is the numeric upper lever EXHAUSTED?

**Answer: the numeric upper lever is EXHAUSTED. No admissible construction route remains
on the held family. The honest conclusion is STRUCTURAL.** Verified chain:

- **A-base (prod-P^q side):** R7 reviewer-verified MAXIMAL-FIRING-SET (deg<=16, ~80k
  candidates, LLL/CVP/well-rounding). Every coprime ORIGINAL monic factor costs
  r_tilde >= +0.013 > |best reachable firing margin j16 = -0.005|, so EVERY original
  product flips non-firing. Best reachable borrowed block (j16) -> joint 10-exp re-opt
  drop 2.94e-6 < the 5e-6 float gate => DRY. The deepest U^nu wells (|zeta| in [0.43,0.79])
  sit strictly INSIDE the unit disk where no integer w^2-pw+q (q>=1) root can reach —
  a GEOMETRIC obstruction, not just a search-budget limit. FORBIDDEN to retry (run_state
  hard rule).

- **B-branch (perturber side):** R8 reviewer-verified MAXIMAL-FIRING-SET. Corrected
  marginal m_B(Q)=(1/D)[int_{B>A}log|Q| - (log h)*deg], fires iff m_B<0. Every firing
  block is INADMISSIBLE (X^4-X^3-X+1=(X-1)^2(X^2+X+1): Q(1)=0/non-sqfree; etc.); all 263
  admissible squarefree atoms have int/deg >= 0.2631 > threshold (log h)=0.2539, and
  products only ADD per-degree integrals so cannot fire. Least-dry admissible block
  (X^2-X+1): float drop 1.98e-7 << 5e-6 gate => DRY. FORBIDDEN to retry (run_state).

- **The design principle, run as an optimizer, PROVES the opposite of the user's ask.**
  The R7 redirect asked the method to CONSTRUCT an original improving block. The method,
  applied rigorously, instead proved that NO original block fires on either branch —
  i.e. it EXPLAINS why j3/j9 were near-optimal and the family is saturated. The verified,
  publishable content is "the criterion EXPLAINS and OPTIMIZES block selection and proves
  this family saturated", NOT "the criterion DESIGNS new record-breaking blocks" (refuted
  both branches). This is the honest thesis the paper must adopt.

- **Decay corroborates exhaustion:** A-base per-step gains j3 (+1.49e-4) -> j9 (+3.2e-6),
  ~47x/step; next same-kind step projects ~1e-7 = at/below the ~1.2-2.0e-7 cert slack.
  The realized-drop/|r_tilde| conversion factor itself collapsed ~14x (j3 6.5e-3 -> j9
  4.7e-4) as the dictionary filled. The lever is genuinely dry, not merely shrinking.

**Verdict Q2: the numeric upper lever is exhausted. Do NOT spend R9 on any block
(A-base, B-branch, original or borrowed) on the held family, nor on a blind BMQS search.
The round's value must be STRUCTURAL.**

================================================================================
## Q3 — Rank the remaining structural / write-up steps by value x tractability;
##      name the single highest-value one-round-tractable target.

State of the structural kernel (so we do not re-bank done work):
- The R6 first-variation lemma is ALREADY RIGORIZED for BOTH branches:
  * A-base (LOSING arg, D constant): R8-firstvar-rigorous.md, full DCT-on-difference-
    quotient proof, Danskin boundary-cancellation written out, hypotheses H1'/H1''/H2
    corrected and audited. Reviewer-verified R8.
  * B-branch (D-ATTAINING arg, D moves): R8 Angle A, cross-term -(log h)*deg/D derived
    and reviewer-reproduced from scratch (FD that moves D). Reviewer-verified R8.
  => Re-deriving / re-running EITHER logs NO new milestone (eval counts only new advances).
- Shared-pool / WITD framing core is verified (R6 verify_shared_pool.py): exact identities
  P4=j5,P6=j8,P8=j12,Q5=j13,Q6=j15 + j3,j9 all Flammang Table-1; 11-block dict squarefree,
  all 55 pairs coprime; dual loci scoped UPPER-INTERNAL. Re-running logs no new milestone.

Remaining candidate structural steps, ranked (value x one-round tractability):

**#1 (HIGHEST VALUE, but NOT one-round-tractable as a THEOREM): the WITD inequality
   inf_Q r_tilde_Q ~ -log t_{Z,phi} on the active arc.** This is the genuine new theorem
   that would turn "block selection = integer-Chebyshev on the active locus" from a framing
   into a result. Its LOWER-BOUND side (that no integer Q can beat the transfinite-diameter
   floor) is a real open inequality — too big for one round, flagged in R7_explore_nextstep
   Q1 #2 and R8-firstvar-rigorous Scope as future work. NOT the R9 target.

**#2 (HIGHEST one-round-tractable VALUE): generalize the first-variation cross-term off
   the special held-family D-config — i.e. state and prove the marginal in the FULL regime
   where EITHER arg can attain D (the unified d(log h)/dq = (1/D)int_{active} log|Q| -
   (log h)*deg(Q)*1_{q enters D-arg}/D).** R8 already has BOTH endpoints proved (A-base:
   D constant, no cross-term; B-branch: D moves, cross-term -(log h)*deg/D). The remaining
   step is the UNIFICATION into one statement covering the boundary case (a tie arg_A=arg_B,
   where D becomes a max of two moving args and the directional derivative is itself a max
   of the two branch marginals — a clean Danskin-on-two-active-indices statement). This is
   NOW tractable in a way it was NOT in R7/R8: R7 role-memory flagged it as un-exercisable
   because "no live A-dominant config on disk to FD-verify against" — but R9 does NOT need
   a live A-dominant family for the UNIFIED-STATEMENT write-up, because the proof is the
   same Danskin envelope (directional derivative of max of two C^1 functions = max over the
   ACTIVE index set of branch derivatives) that R8 already proved for each branch separately;
   the unified statement just removes the H2 (B-attains-D) hypothesis and reads off both
   sub-cases as corollaries, each ALREADY numerically exercised on disk (A-base via
   verify_firstvar_lemma.py, B-branch via verify_Bbranch_marginal.py). HARD STEP: the tie
   case (arg_A=arg_B, both active in D) — show the directional derivative of log h=Phi/D
   exists as a one-sided derivative and equals the appropriate max/min over the two branch
   marginals (Danskin for the OUTER max D(q)=max(arg_A(q),arg_B(q)) combined with the
   quotient rule). This is a self-contained envelope-calculus lemma, no new family search,
   both sub-case numerics already on disk. CAVEAT: must NOT overclaim it is "exercised" on
   an A-dominant family — it is the unification of two separately-verified sub-cases plus
   the tie-case envelope argument; scope it as such or the reviewer logs no milestone.

**#3 (LOW headline, LOW risk): write up the WITD UNIFICATION FRAMING section** (Doche-upper
   and Flammang-lower both draw from one pool of small-Mahler-measure integer polys in
   w=z(1-z), block selection = integer-transfinite-diameter on the active locus, dual loci
   scoped UPPER-INTERNAL). The checkable core is R6's verify_shared_pool.py (already
   verified), so as a STANDALONE round it likely banks NO new milestone — the reviewer
   already logged the verifiable facts. Only valuable as a corollary section riding #2.
   NOT the R9 target on its own.

**Single highest-value, one-round-tractable target: #2 — the UNIFIED first-variation
   cross-term lemma (remove the B-attains-D hypothesis; state the marginal for either/both
   arg attaining D via Danskin-on-the-outer-max + quotient rule; the two saturating
   sub-cases drop out as already-verified corollaries).** It is the only remaining clean,
   genuinely-NEW, single-round, reviewer-verifiable structural advance that strengthens
   the "engine is a theorem" kernel without a numeric search, and it is the missing piece
   that lets the WITD framing (#1, #3) be stated for the general construction rather than
   only the special held D-config. Its hard step (the tie case) is a standard
   Danskin/envelope argument, not an open inequality.

================================================================================
## RECOMMENDATION (R9)

**Softest target: STRUCTURAL, not numeric. The numeric upper lever is exhausted
(A-base R7 + B-branch R8 both reviewer-verified maximal-firing-sets; BMQS recast = the
same saturated Doche family). Do NOT attempt a numeric break.**

**Target: prove the UNIFIED first-variation cross-term lemma — generalize R6/R8 off the
special B-attains-D config to a single statement valid when EITHER arg (or both, at a tie)
attains D, via Danskin on the outer max D(q)=max(arg_A,arg_B) plus the quotient rule;
recover the A-base (no cross-term) and B-branch (-(log h)deg/D cross-term) results as
already-verified corollaries.**

**Hard step:** the tie case arg_A(q)=arg_B(q) where D is itself a max of two moving args —
show log h = Phi(q)/D(q) has a one-sided directional derivative equal to the appropriate
extremum over the two active-branch marginals (Danskin for the outer max combined with the
inner max(A,B) envelope already handled in R8). No new family search; both sub-case
numerics (verify_firstvar_lemma.py, verify_Bbranch_marginal.py) already on disk and
reproducible. Scope HONESTLY: this is a unification + tie-case argument, NOT a claim that
the cross-term is FD-exercised on a live A-dominant family (no such family on disk — do
not overclaim, R7 role-memory).

================================================================================
## Dead ends (do NOT retry) — authoritative lineage

- A-base dictionary enrichment (any block, original or borrowed): PROVEN saturated/DRY,
  reviewer-verified R7 maximal-firing-set, geometric obstruction (firing roots inside the
  unit disk). [run_state hard rule]
- B-branch perturber enrichment (any block): PROVEN saturated/DRY, reviewer-verified R8
  maximal-firing-set (firing blocks inadmissible; admissible atoms above threshold). [run_state]
- BMQS mu_{P,Q} as a DISTINCT upper lever: bare single-pair 0.34-0.69 (hopeless, R1);
  weighted/multi-pair recast = the saturated Doche family (R1, R7_explore_polya, strong
  duality => no separate gap). NOT a one-to-few-round numeric opening.
- Same-family q-only tuning: well dry (R6 gained 1.8e-6, sub-cert-slack now). DEAD.
- The Qa/Qb deg-24 ell=1 lineage + its "5.3e-5 probe" (R8_explore_triage.md, NOT _v2):
  STALE / abandoned at R11, baseline +4.3e-4 WORSE than held. DISCARD. [R8 explore v2]
- Re-running verify_firstvar_lemma.py / verify_Bbranch_marginal.py / verify_shared_pool.py
  as a "milestone": already reviewer-verified (R6/R8); re-running logs NO new milestone.
- The WITD inequality inf_Q r_tilde ~ -log t_{Z,phi} as a full theorem: real open
  lower-bound side, NOT one-round-tractable. Framing/corollary only.
- Lower side: do NOT touch. Repo's 0.2524 is user-flagged WRONG; real lower is Flammang
  0.2487458 (analogy source only). [run_state, user R6]

## Files read (no new artifacts fetched)
- /tmp/memory/run_state.md, /tmp/memory/math-explorer.md (role memory)
- constants/82a/current.md
- constants/82a/literature/{R1_explore_bmqs_thm45.md, R8_explore_triage_v2.md,
  R7_explore_nextstep.md}
- constants/82a/approaches/R8-firstvar-rigorous.md
- (certificate harness verify_upper_q8A.py confirmed as authoritative held via run_state/current.md)
