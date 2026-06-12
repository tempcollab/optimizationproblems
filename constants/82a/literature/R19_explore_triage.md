# R19 explore triage — 82a UPPER (Zhang-Zagier essential minimum)

Explorer: math-explorer, round 19. READ-ONLY start-of-round triage — no improvement
attempted, no new PDF fetches, no long/silent ops. On-disk material only (current.md,
R11–R18 triages, role memory, approaches/ + certificate/ + literature/ dir listings).

Held VERIFIED upper bound to STRICTLY beat: **0.2538893183** (R4 this campaign,
verify_upper_q8A.py; Doche Doc01a §4 family + j3 deg-3 + j9 deg-8 A-base blocks,
B-perturbers Q1*Q2*Q5^qE*Q6^qF). Best verified table value (run_state) = **0.2540419719** (R11);
campaign already sits 1.53e-4 below it, and 5.5e-3 below the original Doche bar 0.25444.

This is the **NINTH** consecutive round-start UPPER triage (R11–R18 all DRY, now R19).

## On-disk change check (verified, not on faith)
`ls -la` of certificate/, literature/, approaches/: the newest NON-triage artifact is still
`certificate/verify_dual_loci_decomposition.py` (R10). Every later file is a triage write-up
(R11–R18, literature/) or a prior-round artifact. NO new capacity/identity script, NO new
digest, NO new approach doc, NO new certificate since R10. The standing package is exactly as
banked through R10, re-confirmed dry R11–R18. The round-19 dispatch carries no new idea — it
restates the SAME THREE already-recorded-and-closed levers: (R1) BMQS Thm 4.5 density framing,
(R6) integer-transfinite-diameter thesis, (R7) design-principle "minimize r_Q over Z[X]". All
three are adversarially closed (R12–R18). Confirmed: nothing on disk changed since R10/R18.

================================================================================
## Q1 — Any concrete NEW computed artifact this round (new script -> new identity/number)
## that survives the WITD-independence objection and is NOT prose re-assembly of R6–R10?
## ANSWER: **NO.**  VERDICT: **DRY.**

Every artifact category collapses to a reviewer-verified dead end:

1. **Numeric upper (A-base or B-branch Doche enrichment).** DEAD by TWO reviewer-verified
   maximal-firing-set theorems. A-base (R7): cheapest coprime original monic factor costs
   r_tilde >= +0.0131 > |best firing margin 0.0052|; borrowed block j16 -> float drop 2.94e-6
   < 5e-6 gate. B-branch (R8): every firing block inadmissible; all 263 admissible atoms have
   int/deg >= 0.2631 > log h = 0.2539. Per-step gain decayed ~47x (j3 +1.49e-4 -> j9 +3.2e-6);
   next projects ~1e-7, at/below cert slack. Hard rule. Not an opening.

2. **A second fixed-q numerator identity (R10-style).** NONE LEFT. R10 banked the ONE clean
   fixed-q identity (active-arc partition 1_{A>B}+1_{B>A}=1 a.e. + numerator split). The R9
   unified one-sided first-variation theorem covers every derivative direction across all three
   D-regimes incl. the tie. Decomposition + engine jointly EXHAUST the splittable structure.

3. **Capacity / transfinite diameter / equilibrium measure of ACT(A)/ACT(B).** REFUTED — do NOT
   re-propose. New as a number but BACKS NOTHING: capacity is a property of the plane SET alone,
   independent of any Q; r_tilde/m_B are weighted log-norms of a FIXED integer Q. Tying them IS
   the open WITD equality inf_Q r_tilde_Q = -log d_inf(ACT(A)), which R7 PROVED FAILS in the
   load-bearing direction (firing integer roots strictly inside the unit disk, |zeta| in
   [0.43,0.79], away from the deepest U^nu wells, so the integer inf sits STRICTLY ABOVE the
   continuous -log d_inf). Also anchor/exponent dependent (|ACT(A)| = 0.428 at R4 vs 0.0686
   under R10 convention) — not one well-defined number. Exactly the trap the dispatch warns against.

4. **Second-order / Hessian first-variation expansion.** New arithmetic but load-bearing only
   for a numeric improvement the firing-set theorems prove cannot exist. Banks nothing.

5. **WITD equality as a real theorem.** OPEN, multi-round; R7 proved the obstruction. Not
   one-round reachable.

6. **Consolidate R6–R10 into one theorem.** Prose re-assembly of already-banked facts, no NEW
   identity/script — reviewer rejected this category R9–R18. Banks nothing.

No category yields a concrete, new, one-round, WITD-independent, non-re-run artifact.

================================================================================
## Q2 — Does BMQS Thm 4.5 density (the round-19 user framing), re-examined ONCE MORE, unlock
## any NON-Doche construction that is neither (a) bare-single-pair mu_{P,Q} (hopeless, R1)
## nor (b) the saturated weighted-product Doche recast (BMQS Thm 6.5 strong duality)?
## ANSWER: **NO.**  VERDICT: **DRY.**

The dispatch framing is the R1 framing already closed R12–R18. The dichotomy is exact
(re-checked against the §4 / §7.3 / Thm 6.5 digests):

(a) **Strong duality pins the optimum to the saturated cone.** BMQS Thm 6.5: P(g)=inf_mu int g
    dmu = ess(h_g) = D(g). The Doche weighted-product family IS the V=prod P_m^{q_m} interior
    cone direction (Rmk 4.6 / §1.4); BOTH branches proven saturated within reach (R7/R8). The
    pullback phi_{P,Q}=P^{deg Q+1}/Q^{deg P} defining mu_{P,Q} is exactly the weighted ratio
    whose log is the Doche auxiliary integrand — density says these APPROXIMATE the optimum, it
    does NOT supply a sub-Doche feasible point. No new reading.

(b) **Bare single-pair mu_{P,Q} is the ONLY genuinely-non-Doche member, and it is hopeless.**
    R1 numeric PoC: every valid coprime-irreducible low-degree pair gives 0.34–0.69 (best ~0.340)
    vs held 0.2539. Multi-pair/weighted mu' (Rmk 4.6) is NOT a new object — it IS the Doche
    V=prod P^q recast. No third kind. No new reading.

(c) **The density limit has no efficient compass and is high-degree.** Thm 4.5 promises
    convergence only via mu_{P_n,P_{n+1}} for a minimal-poly sequence equidistributing to the
    optimal measure — degrees in the tens, sequence known a priori. BMQS state their own wall
    (§1.7): "enormous size of the search space and the lack of an efficient criterion"; "far from
    being practical." A multi-round directed-search gamble, not a one-round construction; and if
    a sequence equidistributes, R7's geometric obstruction (firing roots strictly inside the disk
    vs the locus arc) says integer realizations cannot reach the deepest wells — the same wall
    that saturates the Doche family. No new reading.

No non-Doche mu_{P,Q} construction is feasible in one round. Definitively re-confirmed (NINE
times: R1 scope, R12, R13, R14, R15, R16, R17, R18, R19).

================================================================================
## Q3 — Is "minimize r_Q over Z[X]" (R7 design principle) anything other than the WITD primal
## problem already closed by both maximal-firing-set theorems (A-base R7, B-branch R8)?
## ANSWER: **NO — fully closed.**  VERDICT: **DRY.**

The R7 design problem (minimize the certified first-variation marginal r_tilde_Q over integer
polynomials Q) IS the construction (primal) side of the WITD problem. Exercised and refuted by
R7's A-base maximal-firing-set theorem (design_block*.py: 73845 originals -> 0 firing; cheapest
coprime original monic factor w^2-w+1 costs r_tilde=+0.01311 > |best reachable firing margin j16
-0.00521|). The B-branch analog (m_B firing iff <0) is closed by R8's B-branch maximal-firing-set
theorem (every firing block inadmissible; all 263 admissible atoms above the firing gate). Both
branches reviewer-verified saturated within reach (deg<=16, ~80k candidates, LLL/CVP/well-rounding,
R2+R4 anchors). No unexercised sub-case. The direction is closed.

================================================================================
## NET VERDICT: **DRY (PLATEAU).** No concrete artifact to name. No builder dispatch justified.

Adversarial self-check of every "PROCEED" I was tempted by — each collapses:
- "compute the locus capacity" -> secretly the open WITD equality; R7 proved it fails (Q1.3). DRY.
- "second numerator identity" -> none left; engine covers all directions (Q1.2). DRY.
- "new BMQS mu_{P,Q} from density" -> bare hopeless or saturated Doche recast (Q2). DRY.
- "add/swap one more block" -> both branches proven maximal firing sets (Q1.1, Q3). DRY.
- "second-order Hessian expansion" -> backs only an impossible numeric break (Q1.4). DRY.
- "consolidate R6–R10 into one theorem" -> prose re-assembly, banks nothing (Q1.6). DRY.

NINTH consecutive dry-well triage. The standing UPPER package is publication-complete:
R4 record 0.2538893183 + both-branch maximal-firing-set saturation (R7/R8) + fully unified +
rigorous first-variation engine (R6 DCT / R8 B-branch cross-term / R9 unified one-sided theorem)
+ R10 dual-loci numerator decomposition. Any further one-round UPPER milestone requires a
QUALITATIVELY NEW idea from the user (a genuinely non-Doche construction, or new machinery for
the OPEN multi-round WITD equality). The repeated identical BMQS Thm 4.5 / R6 thesis / R7
design-principle dispatch supplies no such idea.

Honest action: do NOT force a low-value structural artifact the reviewer will reject (rejected
prose re-assembly through R11–R18). No valid builder dispatch -> no build -> no reviewer. END
round PLATEAU. Strongly recommend the user either (1) pivot this campaign to WRITE-UP of the
verified UPPER package, or (2) re-target the LOWER side (live: R17 held lower 0.2524001332 via
the OSS log-energy certificate — a DIFFERENT dispatch, off-limits in THIS upper dispatch), or
(3) re-target a DIFFERENT registry constant with an open verifiable-advance well.

================================================================================
## Dead ends (carried forward, authoritative — do NOT retry)
- A-base enrichment (any block): PROVEN saturated, R7 maximal firing set. [hard rule]
- B-branch enrichment (any block): PROVEN saturated, R8 maximal firing set. [hard rule]
- Bare single-pair mu_{P,Q}: 0.34–0.69, hopeless. [R1]
- Weighted/multi-pair mu_{P,Q} / mu' (Rmk 4.6): = Doche V=prod P^q recast, saturated. [R1]
- Limit-of-mu_{P,Q} density object: multi-round, no compass, high-degree, same R7 wall. [R1/R7]
- Design-principle "minimize r_Q over Z[X]": = WITD primal side, refuted R7/R8. [R7/R8]
- Same-family q-only tuning: sub-cert-slack. [R6]
- Capacity / transfinite diameter / equilibrium measure of ACT(A)/ACT(B): un-theorem'd,
  anchor-dependent, geometrically mismatched with j3/j9 roots, IS the open WITD equality.
  Backs nothing. [R11–R18, decisive]
- Consolidate R6/R7/R8/R9/R10 into one theorem: prose re-assembly, banks nothing. [R9/R10]
- Second-order/Hessian expansion: backs only an impossible numeric break. [R11]
- WITD equality inf_Q r_tilde = -log d_inf as a full theorem: open, multi-round. [R7/R11]
- Lower side: OFF-LIMITS by user directive in THIS UPPER dispatch. [hard rule for UPPER]
- Re-running any existing verified script as a "milestone": banks nothing.

## Files read (no new artifacts fetched)
- constants/82a/current.md (held upper 0.2538893183 / Bounds / Progress log)
- constants/82a/literature/R18_explore_triage.md (full); R11–R17 referenced
- /tmp/memory/run_state.md (Goal / Eval History / Rules / State)
- /tmp/memory/math-explorer.md (role memory — corroborates every dead-end)
- approaches/ + certificate/ + literature/ dir listings (newest non-triage artifact =
  R10 verify_dual_loci_decomposition.py; nothing new since R18 triage)

VERDICT: DRY — no valid builder dispatch
