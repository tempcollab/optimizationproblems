# R14 explore triage — 82a UPPER (Zhang-Zagier essential minimum)

Explorer: math-explorer, round 14. READ-ONLY triage — no improvement attempted, no
new PDF downloads, no long/silent ops. On-disk material only (current.md, R11/R12/R13
triages, role memory, certificate/ + approaches/ + literature/ dir listings).

Held VERIFIED upper bound to STRICTLY beat: **0.2538893183** (R4 this campaign,
verify_upper_q8A.py; Doche Doc01a §4 family + j3 deg-3 + j9 deg-8 A-base blocks,
perturbers Q1*Q2*Q5^qE*Q6^qF). Reconciled vs current.md and the authoritative harness —
consistent. (README/82a.md table value 0.25444 = log(1.289735) is the original Doche bar;
the campaign already sits 5.5e-3 below it.)

This is the FOURTH consecutive round-start triage (R11, R12, R13, now R14). The round-14
dispatch restates the SAME BMQS Thm 4.5 density framing verbatim — no qualitatively new
user idea arrived. The certificate/, approaches/, and literature/ directories are
UNCHANGED since R13 (no new capacity/identity script, no new digest). The standing package
is exactly as banked through R13.

================================================================================
## Q1 — Any concrete, ONE-ROUND, reviewer-verifiable NEW computed artifact (NEW script
## / NEW exact identity, NOT prose re-assembly of R6-R10) that advances 82a UPPER?
## ANSWER: **NO.**

I re-enumerated every artifact category against four gates: (i) genuinely-new checkable
content, (ii) one-round reachable, (iii) survives the WITD-independence objection,
(iv) not a re-run / prose re-assembly. Every category collapses to a known dead end.

1. **Numeric upper (enrich the Doche family, A-base or B-branch).** DEAD by two
   reviewer-verified maximal-firing-set theorems. A-base (R7, deg<=16/~80k cands: every
   coprime original monic factor costs r_tilde>=+0.013 > |best firing margin -0.005|;
   best reachable borrowed block j16 -> float drop 2.94e-6 < 5e-6 gate). B-branch (R8:
   every firing block inadmissible; all 263 admissible atoms have int/deg>=0.2631 >
   threshold log h=0.2539). Per-step gain decayed 47x (j3 +1.49e-4 -> j9 +3.2e-6); next
   projects ~1e-7 at/below cert slack. Hard rule. NOT an opening.

2. **A second fixed-q numerator identity (an R10-style decomposition).** NONE LEFT.
   R10 banked the ONE clean fixed-q identity (active-arc partition 1_{A0>B}+1_{B>A0}=1
   a.e. + numerator split Phi(0)=int_{ACT(A)}A0 + int_{ACT(B)}B). The R9 unified one-sided
   first-variation theorem already covers EVERY derivative direction across all three
   D-regimes incl. the tie; the per-locus marginals (r_tilde on ACT(A), m_B on ACT(B)) are
   R6/R8. Decomposition + engine jointly EXHAUST the splittable structure of the held
   certificate. A second-order/Hessian expansion would be new arithmetic but is load-
   bearing only for a numeric improvement the firing-set theorems prove cannot exist — it
   banks nothing.

3. **Capacity / transfinite diameter / equilibrium measure of ACT(A), ACT(B).** REFUTED,
   do NOT re-propose. New AS A NUMBER (no on-disk script computes it) but BACKS NOTHING:
   capacity is a property of the PLANE SET alone, independent of any Q, whereas r_tilde/m_B
   are weighted log-norms of a FIXED integer Q. Tying them IS the open equality
   inf_Q r_tilde_Q = -log d_inf(ACT(A)), which R7 PROVED FAILS in the load-bearing
   direction (firing integer roots sit strictly inside the unit disk, geometrically away
   from the deepest U^nu wells, so the integer inf sits STRICTLY ABOVE the continuous
   -log d_inf). The partition is also anchor/exponent dependent (|ACT(A)|=0.428 at held R4
   exponents vs 0.0686 under R10's no-candidate convention) — not one well-defined number.
   The "secretly the WITD equality" trap the dispatch explicitly warns against. Declined by
   both R11 agents, re-declined R12 and R13; I concur.

4. **Consolidate R6/R7/R8/R9 into one theorem.** Prose re-assembly of already-banked
   facts, no new identity/script. Banks nothing (hard rule, role memory).

5. **The WITD equality as a real theorem.** OPEN lower-side problem, multi-round, NOT
   one-round tractable; R7 proved the obstruction. Not reachable this round.

No category yields a concrete, new, one-round, WITD-independent, non-re-run artifact.

================================================================================
## Q2 — BMQS Thm 4.5 density (re-stated verbatim in the R14 task): any non-Doche
## mu_{P,Q} upper construction that is NOT (a) bare single-pair hopeless or (b) the
## saturated weighted-product recast?  ANSWER: **NO.**

The dichotomy is exact and was re-verified adversarially in R12 and R13 against the full
§4 (Thm 4.1/Prop 4.4/Thm 4.5/Rmk 4.6) + §7.3 + Thm 6.5 digests. Nothing on disk has
changed; the framing is identical to the one already closed. The three independent reasons:

(a) **Strong duality pins the optimum to the saturated cone.** BMQS Thm 6.5:
    P(g)=inf_{mu} int g dmu = ess(h_g)=D(g). The Doche weighted-product family is the
    V=prod P_m^{q_m} interior cone direction (Rmk 4.6 / §1.4); BOTH branches proven
    saturated within reach (R7/R8). No separate primal construction with slack below the
    saturated Doche cone exists at held precision.

(b) **Bare single-pair mu_{P,Q} is the ONLY genuinely-non-Doche member, and it is
    hopeless.** R1 numeric PoC: every valid coprime-irreducible low-degree pair gives
    0.34-0.69 (best ~0.340) vs held 0.2539. Multi-pair/weighted mu' (Rmk 4.6) is NOT a new
    object — it IS the Doche V=prod P^q recast. So a non-Doche mu_{P,Q} object is either
    bare single-pair (hopeless) or the weighted recast (= saturated Doche). No third kind
    exists.

(c) **The density limit has no efficient compass and is high-degree.** Thm 4.5 promises
    convergence only via mu_{P_n,P_{n+1}} for a minimal-polynomial sequence equidistributing
    to the optimal measure — degree in the tens, and you must already KNOW the sequence.
    BMQS state their own wall (§1.7): "enormous size of the search space and the lack of an
    efficient criterion"; "the obtained algorithm is far from being practical." A
    limit-of-mu_{P,Q} object is a multi-round directed-search gamble, not a one-round
    feasible construction. And if such a sequence equidistributes to the optimal measure,
    R7's geometric obstruction (firing roots strictly inside the unit disk vs the locus arc)
    says the integer realizations cannot reach the deepest wells — the same wall that
    saturates the Doche family.

No non-Doche mu_{P,Q} construction is feasible in one round. Definitively re-confirmed
(now FOUR times: R1 scope, R12, R13, R14).

================================================================================
## Q3 — VERDICT: **DRY.** Publication-complete; no reachable one-round milestone.

The 82a UPPER verifiable-advance well is genuinely exhausted. No honest builder dispatch
exists. I cannot name a single artifact that is simultaneously (i) new, (ii) one-round
reachable, (iii) WITD-independent, (iv) not a re-run / prose re-assembly.

Adversarial self-check of every "PROCEED" I was tempted by — each collapses to a known
dead end:
- "compute the locus capacity" -> secretly the open WITD equality (Q1.3). DRY.
- "second numerator identity" -> none left; engine covers all directions (Q1.2). DRY.
- "consolidate R6-R10 into one theorem" -> prose re-assembly, banks nothing (Q1.4). DRY.
- "new BMQS mu_{P,Q}" -> bare hopeless or saturated Doche recast (Q2). DRY.
- "add/swap one more block" -> both branches proven maximal firing sets (Q1.1). DRY.

This is the FOURTH consecutive dry-well triage (R11 explorer+outliner; R12; R13; now R14).
The standing UPPER package is publication-complete: R4 record 0.2538893183 + both-branch
maximal-firing-set saturation (R7/R8) + fully unified+rigorous first-variation engine
(R6 DCT / R8 B-branch cross-term / R9 unified one-sided theorem) + R10 dual-loci numerator
decomposition. Any further one-round UPPER milestone requires a QUALITATIVELY NEW idea from
the user (a genuinely non-Doche construction, or a new technique to attack the OPEN
multi-round WITD equality inf_Q r_tilde = -log d_inf(ACT(A))). The repeated identical
BMQS-density dispatch does NOT supply such an idea.

Honest action: do NOT force a low-value structural artifact the reviewer will reject (the
reviewer has rejected prose re-assembly through R11-R13). No valid builder dispatch -> no
build -> no reviewer (nothing to verify). END round PLATEAU. Strongly recommend the user
either (1) pivot the campaign to WRITE-UP of the verified UPPER package, or (2) re-target a
DIFFERENT constant from the registry where a verifiable-advance well is open.

================================================================================
## Dead ends (carried forward, authoritative — do NOT retry)
- A-base enrichment (any block): PROVEN saturated, R7 maximal firing set. [hard rule]
- B-branch enrichment (any block): PROVEN saturated, R8 maximal firing set. [hard rule]
- Bare single-pair mu_{P,Q}: 0.34-0.69, hopeless. [R1]
- Weighted/multi-pair mu_{P,Q} / mu' (Rmk 4.6): = Doche V=prod P^q recast, saturated. [R1]
- Limit-of-mu_{P,Q} density object: multi-round, no compass, high-degree, same R7 wall. [R1/R7]
- Same-family q-only tuning: sub-cert-slack. [R6]
- Capacity / transfinite diameter / equilibrium measure of ACT(A)/ACT(B): un-theorem'd,
  anchor-dependent, equilibrium measure geometrically mismatched with j3/j9 roots (R7),
  IS the open WITD equality. Backs nothing; risks overstatement. [R11/R12/R13, decisive]
- Consolidate R6/R7/R8/R9 into one theorem: prose re-assembly, banks nothing. [R9/R10]
- Second-order/Hessian first-variation expansion: backs only a numeric break the firing-set
  theorems prove impossible -> banks nothing. [R11 outline]
- WITD equality inf_Q r_tilde = -log d_inf as a full theorem: open, multi-round. [R7/R11]
- Lower side: OFF-LIMITS by user R6 directive (repo 0.2524 user-flagged wrong). [hard rule]
- Re-running any existing verified script as a "milestone": banks nothing.

## Files read (no new artifacts fetched)
- constants/82a/current.md (held reconciled 0.2538893183)
- constants/82a/literature/{R13,R12,R11}_explore_triage.md
- /tmp/memory/math-explorer.md
- certificate/ + approaches/ + literature/ dir listings (UNCHANGED since R13; no new
  capacity/identity script, no new digest)
