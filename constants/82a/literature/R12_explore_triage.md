# R12 explore triage — 82a UPPER (Zhang-Zagier essential minimum)

Explorer: math-explorer, round 12. Triage ONLY — no improvement attempted. On-disk
material only (run_state, role memory, current.md, approaches/, literature/ digests,
certificate dir listing). No new PDF downloads, no long silent ops. Scope honored.

Held VERIFIED upper bound to STRICTLY beat: **0.2538893183** (R4 this campaign,
verify_upper_q8A.py; Doche Doc01a §4 family + j3 deg-3 + j9 deg-8 A-base blocks,
perturbers Q1*Q2*Q5^qE*Q6^qF). Reconciled vs run_state R4, current.md, and the
authoritative harness — consistent.

================================================================================
## Q1 — Is there a CONCRETE new computed artifact reachable in ONE round on UPPER
## that a reviewer could bank as a genuine advance (NOT prose re-assembly, NOT the
## refuted WITD/capacity direction)?  ANSWER: NO.

I enumerated every category of artifact that could in principle be new and checked
each against (i) genuinely-new checkable content, (ii) one-round reachability,
(iii) survives the WITD-independence objection, (iv) not a re-run.

1. **Numeric upper (enrich the Doche family, A-base or B-branch).** DEAD by two
   reviewer-verified theorems: A-base is a maximal firing set (R7, deg<=16/~80k cands;
   every coprime original monic factor costs r_tilde >= +0.013 > |best firing margin
   -0.005|; best reachable borrowed block j16 -> float drop 2.94e-6 < 5e-6 gate);
   B-branch is a maximal firing set (R8; every firing block inadmissible, all 263
   admissible atoms have int/deg >= 0.2631 > threshold log h = 0.2539). Per-step gain
   decayed 47x (j3 +1.49e-4 -> j9 +3.2e-6), next projects ~1e-7 at/below cert slack.
   Hard rule in run_state. NOT an opening.

2. **A second fixed-q numerator identity (an R10-style decomposition).** NONE LEFT.
   R10 already banked the ONE clean fixed-q identity: the active-arc partition
   1_{A0>B}+1_{B>A0}=1 a.e. plus the numerator split Phi(0)=int_{ACT(A)}A0+int_{ACT(B)}B.
   The first-variation engine (R9 unified one-sided theorem) already covers EVERY
   derivative direction across all three D-regimes incl. the tie; the marginals on the
   complementary loci (r_tilde on ACT(A), m_B on ACT(B)) are R6/R8. There is no
   orthogonal fixed-q or derivative-direction identity of the R10 kind remaining to
   compute — the decomposition + the engine jointly exhaust the splittable structure of
   the held certificate. Confirmed by reading R10-dual-loci-decomposition.md (the
   identity is stated as (P)/(N)/(M) and (M) is exactly the already-banked R6/R8 marginal
   pair).

3. **Capacity / transfinite diameter / equilibrium measure of ACT(A), ACT(B).**
   REFUTED — do not re-propose (this is the standing dry-well candidate). It is new AS A
   NUMBER (no on-disk script computes it) but it BACKS NOTHING: capacity is a property of
   the PLANE SET alone, independent of any Q, whereas r_tilde/m_B are weighted log-norms
   of a FIXED integer Q. Tying them IS the open equality inf_Q r_tilde_Q = -log d_inf(ACT(A)),
   which R7 already PROVED FAILS in the load-bearing direction (firing integer roots sit
   strictly INSIDE the unit disk, geometrically away from the deepest U^nu wells, so the
   integer inf is STRICTLY ABOVE the continuous -log d_inf). The partition is also
   anchor/exponent dependent (|ACT(A)|=0.428 at held R4 exponents vs 0.0686 under R10's
   no-candidate-A0 convention) — not one well-defined number. A bare capacity number is a
   non-load-bearing decoration the reviewer banks nothing for, OR it tempts the unsupported
   WITD-equality overstatement. Declined R11 by two independent agents; I concur.

4. **Consolidate R6/R7/R8/R9 into one theorem.** Prose re-assembly of already-banked
   facts, no new identity/script. Banks nothing (R9/R10 triage + run_state hard rule).

5. **The WITD equality as a real theorem.** Open lower-side problem, multi-round, NOT
   one-round tractable. R7 already proved the obstruction (integer inf strictly above
   continuous -log d_inf). This is the single remaining hard step and it is not reachable
   this round.

No category yields a concrete, new, one-round, WITD-independent, non-re-run artifact.

================================================================================
## Q2 — Re-examine BMQS Thm 4.5 density ONE more time: any weighted-product /
## multi-pair mu_{P,Q} or limit-of-mu_{P,Q} object that is NOT the saturated Doche
## recast and could yield a reachable feasible UPPER construction?  ANSWER: NO.

Re-read R1_explore_bmqs_thm45.md (full §4 Thm 4.1/Prop 4.4/Thm 4.5/Rmk 4.6 + §7.3
Prop 7.8 digest) and bmqs_2026_digest.md (Thm 6.5 strong duality, §1.7 wall). The
density claim is real but offers no one-round upper construction, for three independent
reasons:

(a) **Strong duality pins the optimum to the saturated cone.** BMQS Thm 6.5:
    P(g) = inf_{mu in P^Z_log} int g dmu = ess(h_g) = D(g). Every valid mu gives an upper
    bound; the Doche weighted-product family is the V = prod P_m^{q_m} interior cone
    direction (BMQS Rmk 4.6 / §1.4), and BOTH its branches are now proven saturated within
    reach (R7/R8). There is no SEPARATE primal construction with slack below the saturated
    Doche cone that strong duality would permit at the held precision.

(b) **Bare single-pair mu_{P,Q} is hopeless and is the ONLY genuinely-non-Doche member.**
    R1's numeric PoC: every valid coprime-irreducible low-degree pair gives 0.34-0.69
    (best ~0.340), vs held 0.2539. The single-integer-pair family trades Doche's free-real-
    exponent product freedom (the lever that drove R2-R11) for "any irreducible pair," which
    is strictly worse at low degree. Multi-pair / weighted-product mu' (Rmk 4.6) is NOT a new
    object — it IS the Doche V=prod P^q recast (R1 §2: "the record family already lives in
    this picture"). So the dichotomy is exact: a non-Doche mu_{P,Q} object is either bare
    single-pair (0.34-0.69, hopeless) or the weighted recast (= saturated Doche). No third
    kind exists.

(c) **The density limit has no efficient compass and is high-degree.** Thm 4.5 density only
    promises convergence via mu_{P_n,P_{n+1}} for a sequence of minimal polynomials of
    algebraic integers equidistributing to the OPTIMAL measure — degree in the tens, and you
    must already KNOW the sequence. BMQS state their own wall (§1.7): "enormous size of the
    search space and the lack of an efficient criterion to find the optimal direction"; "the
    obtained algorithm is far from being practical." A limit-of-mu_{P,Q} object is therefore a
    multi-round directed-search gamble with no guarantee, NOT a one-round feasible construction.
    And if such a sequence equidistributes to the optimal measure, R7's geometric obstruction
    (firing roots strictly inside the unit disk vs the locus arc) says the integer realizations
    cannot reach the deepest wells — the same wall that saturates the Doche family.

Conclusion: the BMQS Thm 4.5 family offers NO new one-round feasible UPPER construction
distinct from the already-saturated Doche recast. Definitively re-confirmed.

================================================================================
## Q3 — VERDICT: DRY.

The 82a UPPER verifiable-advance well is genuinely exhausted this round. No honest
builder dispatch exists. I cannot name a single concrete checkable artifact that is
(i) genuinely new, (ii) one-round reachable, (iii) survives the WITD-independence
objection, and (iv) is not a re-run or prose re-assembly. This is the THIRD consecutive
round (R11 dry-well; R10 was the last structural bank) to reach this conclusion, now via
an independent adversarial re-check of the two specific levers the dispatch flagged
(R10-style second identity; BMQS Thm 4.5 density). Both are closed.

The honest action: do NOT force a low-value structural artifact. Report the well dry.
The standing package (R4 record 0.2538893183 + both-branch maximal-firing-set saturation
R7/R8 + fully unified+rigorous first-variation engine R6/R8/R9 + R10 dual-loci numerator
decomposition) is publication-complete on UPPER. Any further one-round UPPER milestone
requires a QUALITATIVELY NEW idea from the user (a genuinely non-Doche construction, or a
new technique to attack the OPEN multi-round WITD equality inf_Q r_tilde = -log d_inf(ACT(A))).

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
  IS the open WITD equality. Backs nothing; risks overstatement. [R11, decisive]
- Consolidate R6/R7/R8/R9 into one theorem: prose re-assembly, banks nothing. [R9/R10]
- WITD equality inf_Q r_tilde = -log d_inf as a full theorem: open, multi-round. [R7/R11]
- Lower side: OFF-LIMITS by user R6 directive (repo 0.2524 user-flagged wrong). [hard rule]
- Re-running any existing verified script as a "milestone": banks nothing.

## Files read (no new artifacts fetched)
- /tmp/memory/run_state.md, /tmp/memory/math-explorer.md
- constants/82a/current.md (held reconciled 0.2538893183)
- constants/82a/literature/{R11_explore_triage.md, R1_explore_bmqs_thm45.md, bmqs_2026_digest.md}
- constants/82a/approaches/R10-dual-loci-decomposition.md
- certificate/ + approaches/ + literature/ dir listings (no new capacity/identity script exists)
