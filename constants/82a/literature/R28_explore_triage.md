# R28 explore triage — 82a UPPER (read-only, fast, adversarially scoped)

Held verified upper = **0.2538893183** (j3/j9 Doche A-base, verify_upper_q8A.py), UNCHANGED since R4.
Best verified value to beat: anything strictly below 0.2538893183.

On-disk state git-verified bit-identical since R10: `git log --oneline 239b19b..HEAD -- constants/82a/certificate/`
returns EMPTY (no cert-dir commit since the R10 dual-loci decomposition). Newest non-triage artifact is
still `certificate/verify_dual_loci_decomposition.py`. Only R11–R27 triage docs + R11-outline.md committed
afterward. Milestone count = 19 (eval grep), matching run_state. No new user idea — the round-28 prompt is
bit-for-bit the R1 BMQS Thm 4.5 density framing + R6 integer-transfinite-diameter thesis + R7 "minimize
r_Q over Z[X]" design principle (all three user messages timestamped 2026-06-11, already recorded as Goal
Updates R1/R6/R7 and refuted R12–R27).

## Q1 — any NEW WITD-independent computed artifact a builder could bank in one round?  **DRY**
Both Doche branches are reviewer-verified MAXIMAL FIRING SETS within reach (A-base R7: 73845 originals -> 0
firing; B-branch R8: all 263 admissible atoms above the firing gate). R10 banked the one clean fixed-q
numerator identity (the upper-internal dual-loci partition 1_{A>B}+1_{B>A}=1 a.e. + numerator split
Phi=int_{A>B}A + int_{B>A}B); the R9 unified one-sided first-variation theorem covers EVERY derivative
direction, so no second R10-style fixed-q identity remains to bank. The only un-computed candidate "new
number" — logarithmic capacity / transfinite diameter / equilibrium measure of ACT(A)/ACT(B) — is
Q-INDEPENDENT set data; tying it to the verified Q-weighted marginals r_tilde/m_B IS the open WITD equality
inf_Q r_tilde = -log d_inf, which R7 PROVED FAILS in the load-bearing direction (firing/integer roots sit
strictly inside the unit disk |zeta| in [0.43,0.79], cannot reach the deepest U^nu wells; integer inf sits
strictly ABOVE the continuous -log d_inf). It would back nothing, and the partition is anchor/exponent
dependent (|ACT(A)|=0.428 at held exponents vs 0.0686 under R10's no-candidate convention — not one
well-defined number). Adversarial probe for a SECOND clean identity: any new fixed-q numerator split would
have to partition the locus differently than R10's max(A,B) split, but the cert numerator is exactly
int_0^1 max(A,B) ds — the R10 split is the unique a.e. decomposition of that integrand, and every derivative
direction is the R9 theorem. No new checkable, meaningful artifact exists. DRY.

## Q2 — BMQS Thm 4.5 density: any non-Doche mu_{P,Q} upper construction?  **DRY**
Exact dichotomy (R1, re-attacked R12–R27): a non-Doche mu_{P,Q} = (phi_{P,Q})_* lambda object is either a
bare single pair P,Q (value 0.34–0.69 numerically — hopeless, well above held) or the weighted/multi-pair
recast, which IS the saturated Doche V = prod P^m family. BMQS Thm 6.5 STRONG DUALITY pins the primal
optimum to that saturated cone, so density gives no separate reachable upper construction. The density LIMIT
needs high-degree minimal-poly sequences with no efficient one-round compass (BMQS §1.7 wall) and still hits
R7's geometric obstruction (firing roots strictly inside the disk). Adversarial probe: could one pick a
mu_{P,Q} that is NEITHER bare-single-pair NOR the product recast? No — the BMQS family is parameterized by
coprime monic irreducible (P,Q); every member of the dense family is a single phi-pullback (the "bare" case)
and the only way to approach the optimum is the convex-combination / product structure that recasts to the
Doche cone (Thm 6.5). The dichotomy is complete. A multi-round high-degree gamble, not a one-round feasible
construction. DRY.

## Q3 — "minimize r_Q over Z[X]" (R7 design principle): anything not already closed?  **DRY**
This IS the WITD primal from the construction side. Fully closed by BOTH maximal-firing-set theorems:
A-base (R7, 73845 originals -> 0 firing across deg<=16, 3 methods LLL/CVP/well-rounding, R2+R4 anchors;
cheapest coprime original factor w^2-w+1 has r_tilde=+0.01311 > best reachable firing margin j16 -0.00521,
so every original product flips non-firing) and B-branch (R8, all 263 admissible atoms have int/deg>=0.2631
> firing threshold (log h)=0.2539; products only ADD per-degree integrals). The realized-drop/|r_tilde|
conversion factor itself collapsed ~14x from j3->j9, so even the borrowed firing blocks j16/j17/j20 project
~3e-6, at/below the 5e-6 float gate (R7 float pre-gate RUN+FAILED at 2.94e-6). No reachable original block
fires. Adversarial probe: is there an unexplored sub-region of Z[X] (e.g. non-monic, or higher degree
deg 17–24)? Non-monic scales r_tilde by +log|lead|>0 (strictly worse); higher degree risks a D-switch and is
redundant with Q6 (deg16) — and the projected drop is already below cert slack. DRY.

## Adversarial self-check on the DRY verdict
The reviewer banks ONLY genuinely new checkable content that means something — not prose re-assembly of
R6–R10, not re-runs, not a number that backs nothing. Every candidate one-round artifact reduces to one of:
(a) a numeric firing block (both branches saturated, projected drop below cert slack); (b) a new fixed-q
identity (R10 banked the unique one; R9 covers all derivatives); (c) the locus capacity (= the refuted
open WITD equality). No new user idea has arrived (prompt identical to R1/R6/R7). The watchdog-safe
conclusion holds: no valid builder dispatch.

## Overall verdict: DRY (18th consecutive). No valid builder dispatch.
82a UPPER is PUBLICATION-COMPLETE (R4 record 0.2538893183 + both-branch saturation R7/R8 + full
first-variation engine R6/R8/R9 + R10 dual-loci decomposition). Recommend: pivot to write-up of the
verified UPPER package, the LOWER side (separate dispatch — forbidden here by user R6 directive), or a
different registry constant with an open well. Only a qualitatively new (non-Doche) user idea, or a
technique for the open multi-round WITD equality, unlocks further UPPER work.
