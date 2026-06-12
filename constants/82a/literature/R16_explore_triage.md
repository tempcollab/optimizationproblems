# R16 explore triage — 82a UPPER (Zhang-Zagier essential minimum)

Explorer: math-explorer, round 16. READ-ONLY triage — no improvement attempted, no new
PDF downloads, no long/silent ops. On-disk material only (current.md, R11–R15 triages,
role memory, approaches/ + literature/ dir listings).

Held VERIFIED upper bound to STRICTLY beat: **0.2538893183** (R4 this campaign,
verify_upper_q8A.py; Doche Doc01a §4 family + j3 deg-3 + j9 deg-8 A-base blocks,
B-perturbers Q1*Q2*Q5^qE*Q6^qF). Best verified table value to beat = 0.2540419719 (the
campaign already sits 1.53e-4 below it). README/82a.md bar 0.25444 = log(1.289735) is the
original Doche bar; the campaign sits 5.5e-3 below it.

This is the SIXTH consecutive round-start triage (R11, R12, R13, R14, R15, now R16). The
round-16 dispatch is a VERBATIM restatement of the R1 BMQS Thm 4.5 density framing
(mu_{P,Q} = pullback of unit-circle Haar measure under phi_{P,Q}=P^{deg Q+1}/Q^{deg P};
mu_{P,Q} dense in the valid measure cone). On-disk verification: the newest files under
constants/82a/ are the R14/R15 triage docs themselves (find -newermt confirms NO new file
since 2026-06-12 02:37). The certificate/, approaches/, and literature/ directories are
UNCHANGED in content since R13. NO new capacity/identity script, NO new digest, NO new
approach doc, NO new user idea. The standing package is exactly as banked through R10,
re-confirmed dry R11–R15.

================================================================================
## Q1 — Any concrete new computed artifact this round could produce that SURVIVES the
## WITD-independence objection?  ANSWER: **NO.**

The dispatch names the trap precisely: a quantity tying a Q-INDEPENDENT set property
(capacity / transfinite diameter / equilibrium measure) to the verified Q-WEIGHTED
marginals r_tilde / m_B IS the open WITD equality inf_Q r_tilde_Q = -log d_inf(ACT(A)),
which R7 PROVED FAILS in the load-bearing direction (firing integer roots sit strictly
inside the unit disk, geometrically away from the deepest U^nu wells, so the integer inf
sits STRICTLY ABOVE the continuous -log d_inf). Do NOT bank it. Re-enumerated every
artifact category against four gates: (i) genuinely-new checkable content, (ii) one-round
reachable, (iii) survives the WITD-independence objection, (iv) not a re-run / prose
re-assembly. Every category collapses to a known dead end:

1. **Numeric upper (enrich Doche family, A-base or B-branch).** DEAD by two
   reviewer-verified maximal-firing-set theorems. A-base (R7): every coprime original
   monic factor costs r_tilde >= +0.013 > |best firing margin -0.005|; best reachable
   borrowed block j16 -> float drop 2.94e-6 < 5e-6 gate. B-branch (R8): every firing block
   inadmissible; all 263 admissible atoms have int/deg >= 0.2631 > log h = 0.2539.
   Per-step gain decayed 47x (j3 +1.49e-4 -> j9 +3.2e-6); next projects ~1e-7 at/below cert
   slack. Hard rule. NOT an opening.

2. **A second fixed-q numerator identity (R10-style).** NONE LEFT. R10 banked the ONE clean
   fixed-q identity (active-arc partition + numerator split). The R9 unified one-sided
   first-variation theorem covers every derivative direction across all three D-regimes incl.
   the tie. Decomposition + engine jointly EXHAUST the splittable structure of the held cert.

3. **Capacity / transfinite diameter / equilibrium measure of ACT(A)/ACT(B).** REFUTED, do
   NOT re-propose. New AS A NUMBER but BACKS NOTHING: capacity is a property of the PLANE SET
   alone, independent of any Q; r_tilde/m_B are weighted log-norms of a FIXED integer Q.
   Tying them IS the open WITD equality R7 proved fails. Partition is also anchor/exponent
   dependent (|ACT(A)|=0.428 at R4 vs 0.0686 under R10 convention) — not one well-defined
   number. The exact trap the dispatch warns against. Declined R11–R15; I concur.

4. **Second-order/Hessian first-variation expansion.** New arithmetic but load-bearing only
   for a numeric improvement the firing-set theorems prove cannot exist — banks nothing.

5. **WITD equality as a real theorem.** OPEN lower-side problem, multi-round, NOT one-round
   tractable; R7 proved the obstruction. Not reachable this round.

No category yields a concrete, new, one-round, WITD-independent, non-re-run artifact.

================================================================================
## Q2 — Does the restated BMQS Thm 4.5 density claim unlock anything NOT already refuted in
## R12–R15? Is there a NEW reading of it?  ANSWER: **NO. No new reading exists.**

The dispatch's framing is bit-for-bit the R1 framing already adversarially closed R12–R15.
The dichotomy is exact and was re-verified against the full §4 (Thm 4.1/Prop 4.4/Thm
4.5/Rmk 4.6) + §7.3 + Thm 6.5 digests. Nothing on disk changed. Three independent reasons,
and I specifically checked each for any NEW reading:

(a) **Strong duality pins the optimum to the saturated cone.** BMQS Thm 6.5:
    P(g)=inf_mu int g dmu = ess(h_g)=D(g). The Doche weighted-product family is the
    V=prod P_m^{q_m} interior cone direction (Rmk 4.6 / §1.4); BOTH branches proven
    saturated within reach (R7/R8). No separate primal construction with slack below the
    saturated Doche cone exists at held precision. NEW READING? None — the pullback
    phi_{P,Q}=P^{deg Q+1}/Q^{deg P} that defines mu_{P,Q} is exactly the weighted ratio
    whose log is the Doche auxiliary integrand; the density theorem says these APPROXIMATE
    the optimum, it does NOT supply a sub-Doche feasible point.

(b) **Bare single-pair mu_{P,Q} is the ONLY genuinely-non-Doche member, and it is hopeless.**
    R1 numeric PoC: every valid coprime-irreducible low-degree pair gives 0.34-0.69 (best
    ~0.340) vs held 0.2539. Multi-pair/weighted mu' (Rmk 4.6) is NOT a new object — it IS the
    Doche V=prod P^q recast. No third kind. NEW READING? None.

(c) **The density limit has no efficient compass and is high-degree.** Thm 4.5 promises
    convergence only via mu_{P_n,P_{n+1}} for a minimal-poly sequence equidistributing to the
    optimal measure — degree in the tens, and you must already KNOW the sequence. BMQS state
    their own wall (§1.7): "enormous size of the search space and the lack of an efficient
    criterion"; "the obtained algorithm is far from being practical." A limit-of-mu_{P,Q}
    object is a multi-round directed-search gamble, not a one-round construction. And if such
    a sequence equidistributes to the optimal measure, R7's geometric obstruction (firing
    roots strictly inside the unit disk vs the locus arc) says the integer realizations cannot
    reach the deepest wells — the same wall that saturates the Doche family. NEW READING? None.

No non-Doche mu_{P,Q} construction is feasible in one round. Definitively re-confirmed (now
SIX times: R1 scope, R12, R13, R14, R15, R16). The restatement supplies no new idea.

================================================================================
## Q3 — NET VERDICT: **DRY (PLATEAU).** No concrete artifact to name.

I cannot name a single artifact simultaneously (i) new, (ii) one-round reachable,
(iii) WITD-independent, (iv) not a re-run / prose re-assembly. The dispatch's BMQS Thm 4.5
direction is a restatement of a closed lever: it splits into bare-hopeless (Q2.b) OR the
saturated Doche recast pinned by Thm 6.5 strong duality (Q2.a), with the density limit
multi-round + no compass + same R7 wall (Q2.c). DRY.

Adversarial self-check of every "PROCEED" I was tempted by — each collapses to a known
dead end:
- "compute the locus capacity" -> secretly the open WITD equality, R7 proved it fails (Q1.3). DRY.
- "second numerator identity" -> none left; engine covers all directions (Q1.2). DRY.
- "new BMQS mu_{P,Q} from the density theorem" -> bare hopeless or saturated Doche recast (Q2). DRY.
- "add/swap one more block" -> both branches proven maximal firing sets (Q1.1). DRY.
- "second-order Hessian expansion" -> backs only an impossible numeric break (Q1.4). DRY.
- "consolidate R6-R10 into one theorem" -> prose re-assembly, banks nothing. DRY.

This is the SIXTH consecutive dry-well triage (R11 explorer+outliner; R12; R13; R14; R15;
now R16). The standing UPPER package is publication-complete: R4 record 0.2538893183 +
both-branch maximal-firing-set saturation (R7/R8) + fully unified+rigorous first-variation
engine (R6 DCT / R8 B-branch cross-term / R9 unified one-sided theorem) + R10 dual-loci
numerator decomposition. Any further one-round UPPER milestone requires a QUALITATIVELY NEW
idea from the user (a genuinely non-Doche construction, or a new technique for the OPEN
multi-round WITD equality inf_Q r_tilde = -log d_inf(ACT(A))). The repeated identical BMQS
Thm 4.5 dispatch does NOT supply such an idea.

Honest action: do NOT force a low-value structural artifact the reviewer will reject (the
reviewer has rejected prose re-assembly through R11–R15). No valid builder dispatch -> no
build -> no reviewer (nothing to verify). END round PLATEAU. Strongly recommend the user
either (1) pivot this campaign to WRITE-UP of the verified UPPER package, or (2) re-target
the LOWER side (live: R17 held lower 0.2524001332 via the OSS log-energy certificate, gap to
upper now ~0.00149 — the well is NOT dry there, but it is a DIFFERENT dispatch), or (3)
re-target a DIFFERENT constant from the registry where a verifiable-advance well is open.

================================================================================
## Dead ends (carried forward, authoritative — do NOT retry)
- A-base enrichment (any block): PROVEN saturated, R7 maximal firing set. [hard rule]
- B-branch enrichment (any block): PROVEN saturated, R8 maximal firing set. [hard rule]
- Bare single-pair mu_{P,Q}: 0.34-0.69, hopeless. [R1]
- Weighted/multi-pair mu_{P,Q} / mu' (Rmk 4.6): = Doche V=prod P^q recast, saturated. [R1]
- Limit-of-mu_{P,Q} density object: multi-round, no compass, high-degree, same R7 wall. [R1/R7]
- Design-principle "minimize r_Q over Z[X]" original block: = WITD primal side, exercised +
  refuted by R7 maximal firing set (design_block*.py all above gate). [R7]
- Same-family q-only tuning: sub-cert-slack. [R6]
- Capacity / transfinite diameter / equilibrium measure of ACT(A)/ACT(B): un-theorem'd,
  anchor-dependent, equilibrium measure geometrically mismatched with j3/j9 roots (R7), IS
  the open WITD equality. Backs nothing; risks overstatement. [R11–R15, decisive]
- Consolidate R6/R7/R8/R9 into one theorem: prose re-assembly, banks nothing. [R9/R10]
- Second-order/Hessian first-variation expansion: backs only a numeric break the firing-set
  theorems prove impossible -> banks nothing. [R11 outline]
- WITD equality inf_Q r_tilde = -log d_inf as a full theorem: open, multi-round. [R7/R11]
- Lower side: OFF-LIMITS by user directive in THIS UPPER dispatch; live well for a separate
  LOWER dispatch. [hard rule for UPPER]
- Re-running any existing verified script as a "milestone": banks nothing.

## Files read (no new artifacts fetched)
- constants/82a/current.md (held reconciled 0.2538893183; table bar 0.2540419719)
- constants/82a/literature/R15_explore_triage.md (full); R11–R14 triages referenced
- /tmp/memory/math-explorer.md (role memory — corroborates every dead-end)
- approaches/ + literature/ dir listings (find -newermt: UNCHANGED since R15 triage written)
