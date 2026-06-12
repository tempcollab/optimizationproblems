# R23 explore triage — 82a UPPER (Zhang-Zagier essential minimum)

Explorer: math-explorer, round 23. READ-ONLY start-of-round RE-CONFIRMATION triage — no
improvement attempted, no new PDF fetches, no multi-minute computation. On-disk material only
(current.md, 82a.md + README row, R22/R21 triages + R10/R11 skim, approaches/ + certificate/ +
literature/ listings, git log, role memory).

Held VERIFIED upper bound to STRICTLY beat: **0.2538893183** (R4 this campaign,
verify_upper_q8A.py; Doche Doc01a §4 limit-point family + j3 deg-3 + j9 deg-8 A-base blocks,
B-perturbers Q1*Q2*Q5^qE*Q6^qF). README row for 82a confirms upper 0.25389. Campaign sits
~5.5e-3 below the original Doche bar 0.25444; two-sided gap to held LOWER 0.2524001332 (R17, OSS
log-energy cert) is ~0.00149.

This is the **THIRTEENTH** consecutive round-start UPPER triage (R11–R22 all DRY; now R23).

## On-disk change check (verified, not on faith)
`git log -1 -- constants/82a/certificate/verify_dual_loci_decomposition.py` = [Round 10] commit
239b19b (2026-06-12 02:21:57). `git log 239b19b..HEAD -- constants/82a/certificate/` is EMPTY:
NO new certificate, identity script, or capacity artifact has been committed since R10. Rounds
11–22 added ONLY triage write-ups in literature/. The standing UPPER package is bit-identical to
what R10 banked and R11–R22 adjudicated dry. verify_upper_q8A.py header re-confirms the held
family h = Q1*Q2 * Q5^qE * Q6^qF * (prod P_i^q_i) * j3^qG * j9^qH.

The round-23 dispatch carries NO new idea — it is verbatim the R1 BMQS Thm 4.5 density framing
(Q2) + R6 integer-transfinite-diameter thesis + R7 "minimize r_Q over Z[X]" design principle
(Q3) + the WITD-independent-artifact question (Q1), all three already recorded and adversarially
closed in R7–R22. Role memory (/tmp/memory/math-explorer.md) corroborates every closed lever.

================================================================================
## Q1 — Any concrete NEW WITD-independent computed artifact a proof-reviewer would BANK?
## ANSWER: **NO.**  VERDICT: **DRY.**

Every artifact category collapses to a reviewer-verified dead end (carried forward authoritative,
re-confirmed against current.md Progress log R6–R10 + R21/R22 triages):
1. Numeric upper (A-base or B-branch Doche enrichment): DEAD by TWO reviewer-verified maximal-
   firing-set theorems. A-base (R7): cheapest coprime original w^2-w+1 costs r_tilde +0.0131 >
   |best firing margin 0.0052|. B-branch (R8): all 263 admissible atoms have int/deg >= 0.2631 >
   logh 0.2539. Per-step gain decayed ~47x (j3 +1.49e-4 -> j9 +3.2e-6); next projects ~1e-7 <=
   cert slack. Hard rule.
2. Second fixed-q numerator identity (R10-style): NONE LEFT. R10 banked the one clean fixed-q
   identity; the R9 unified one-sided first-variation theorem covers every derivative direction.
3. Capacity / transfinite diameter / equilibrium measure of ACT(A)/ACT(B): REFUTED — the trap the
   dispatch explicitly warns against. NEW as a number but BACKS NOTHING: capacity is a property of
   the plane SET alone, independent of any Q; tying it to r_tilde/m_B IS the open WITD equality
   inf_Q r_tilde_Q = -log d_inf(ACT(A)), which R7 PROVED FAILS in the load-bearing direction
   (firing integer roots |zeta| in [0.43,0.79] strictly inside the disk, away from the deepest
   U^nu wells, so the integer inf sits STRICTLY ABOVE the continuous -log d_inf). Also anchor-
   dependent (|ACT(A)|=0.428 at R4 vs 0.0686 under R10 convention) — not one well-defined number.
4. Second-order / Hessian first-variation expansion: backs only a numeric break the firing-set
   theorems prove cannot exist.
5. WITD equality as a real theorem: OPEN, multi-round; not one-round reachable.
6. Consolidate R6–R10 into one theorem: prose re-assembly, banks nothing (reviewer rejected R9–R22).

No category yields a concrete, new, one-round, WITD-independent, non-re-run artifact.

================================================================================
## Q2 — Does BMQS Thm 4.5 density unlock any non-Doche mu_{P,Q} construction?
## ANSWER: **NO.**  VERDICT: **DRY.**

The dichotomy is exact (re-checked against R21/R22 triages + bmqs_2026_digest.md):
(a) Strong duality (BMQS Thm 6.5: P(g)=ess(h_g)=D(g)) pins the optimum to the saturated cone; the
    Doche weighted-product family IS the V=prod P^q interior direction (Rmk 4.6/§1.4), BOTH branches
    proven saturated (R7/R8). Density says these APPROXIMATE the optimum, not supply a sub-Doche point.
(b) Bare single-pair mu_{P,Q} is the ONLY genuinely-non-Doche member, and it is hopeless (R1
    numeric: every valid coprime-irreducible low-degree pair gives 0.34–0.69 vs held 0.2539).
    Multi-pair/weighted mu' (Rmk 4.6) IS the Doche recast — no third kind.
(c) BMQS state their own wall (§1.7): "far from being practical," "no efficient criterion." A
    multi-round directed-search gamble, not a one-round construction; and any equidistributing
    sequence hits R7's geometric obstruction. No non-Doche mu_{P,Q} feasible in one round.

================================================================================
## Q3 — Is "minimize r_Q over Z[X]" anything beyond the WITD primal, already closed?
## ANSWER: **NO — fully closed.**  VERDICT: **DRY.**

The R7 design problem IS the construction (primal) side of the WITD problem. Refuted by R7's
A-base maximal-firing-set theorem (73845 originals -> 0 firing; cheapest coprime original costs
r_tilde +0.01311 > |best firing margin -0.00521|) and R8's B-branch analog (every firing block
inadmissible; all 263 admissible atoms above the firing gate). Both branches reviewer-verified
saturated within reach (deg<=16, ~80k candidates, LLL/CVP). No unexercised sub-case. Closed.

================================================================================
## NET VERDICT: **DRY (PLATEAU).** No concrete artifact to name. No builder dispatch justified.

Adversarial self-check of every "PROCEED" temptation — each collapses identically to R21/R22:
- "compute the locus capacity" -> secretly the open WITD equality; R7 proved it fails (Q1.3). DRY.
- "second numerator identity" -> none left; engine covers all directions (Q1.2). DRY.
- "new BMQS mu_{P,Q} from density" -> bare hopeless or saturated Doche recast (Q2). DRY.
- "add/swap one more block" -> both branches proven maximal firing sets (Q1.1, Q3). DRY.
- "second-order Hessian expansion" -> backs only an impossible numeric break (Q1.4). DRY.
- "consolidate R6–R10 into one theorem" -> prose re-assembly, banks nothing (Q1.6). DRY.

THIRTEENTH consecutive dry-well triage. The standing UPPER package is publication-complete:
R4 record 0.2538893183 + both-branch maximal-firing-set saturation (R7/R8) + fully unified rigorous
first-variation engine (R6/R8/R9) + R10 dual-loci numerator decomposition. Any further one-round
UPPER milestone requires a QUALITATIVELY NEW idea from the user. The repeated identical BMQS Thm 4.5
/ R6 thesis / R7 design-principle dispatch supplies no such idea.

Honest action: no valid builder dispatch -> no build -> no reviewer. END round PLATEAU. Strongly
recommend the user (1) pivot this campaign to WRITE-UP of the verified UPPER package, or (2) re-target
the LOWER side (live: R17 held lower 0.2524001332 — OFF-LIMITS in THIS upper dispatch; gap to held
upper now only ~0.00149, so the lower side is the live frontier), or (3) re-target a DIFFERENT
registry constant with an open verifiable-advance well.

## Files read (no new artifacts fetched)
- constants/82a/current.md (held upper 0.2538893183 / Bounds / Progress log R1–R17)
- constants/82a.md + README row 82a (upper 0.25389)
- constants/82a/literature/R22_explore_triage.md + R21_explore_triage.md (full); R10/R11 referenced
- /tmp/memory/math-explorer.md (role memory — corroborates every dead end)
- git log -- constants/82a/certificate/ (newest = R10 verify_dual_loci_decomposition.py, 239b19b;
  239b19b..HEAD empty — nothing new since R10) + verify_upper_q8A.py header + dir listings

VERDICT: DRY — no valid builder dispatch (13th consecutive)
