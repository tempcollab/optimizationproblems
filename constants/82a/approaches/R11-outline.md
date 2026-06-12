# R11 — UPPER outline: CONCURRENCE with the dry-well verdict

## 82a (UPPER)
Spec review: skip (no angle proposed worth an outline-reviewer pass)
Target to beat: 0.2538893183 = held VERIFIED upper (verify_upper_q8A.py, R4 this campaign).

================================================================================
## VERDICT: CONCUR — the verifiable-advance well for 82a UPPER is DRY.

After an INDEPENDENT survey (not a re-read of the explorer's report), I find NO angle
that is simultaneously (i) genuinely new on disk, (ii) one-round verifiable, and
(iii) a thing a skeptical reviewer would bank as advancing the frontier. I concur with
the R11 explorer's dry verdict and recommend the orchestrator END the round reporting
the verifiable-advance well exhausted and the upper-side paper material essentially
complete. I did NOT manufacture an angle to avoid concurring.

================================================================================
## What I independently checked (the survey, not a re-narration)

### 1. A genuinely DIFFERENT upper construction (not the Doche family). DEAD.
The only upper-bound machinery for the ZZ essential minimum in the literature reduces
to "infinite sets of points / atomic measures of bounded height" = Doche's small-measure
perturbed-polynomial family. I web-searched (June 2026) for any 2024-2026 upper
construction: the live hits are BMQS arXiv:2601.18978 (already digested) and Morales
2022 (families of lines / Fekete-Szego-BPRS refinement). The BMQS digest (line 35-36)
states explicitly the upper side is a measure-LP whose explicit good measures ARE
Doche's perturbed-poly families; Thm 6.5 (strong duality) means the saturated Doche
cone is the BMQS primal optimum within reach — NO separate upper gap. No new escape.

### 2. Numeric lever (add/swap a block). DEAD by hard rule.
A-base maximal-firing-set (R7) + B-branch maximal-firing-set (R8), both reviewer-
verified. Per-step gain decayed ~47x/step (j3 +1.49e-4 -> j9 +3.2e-6); next projects
~1e-7 at/below the ~1.2-2.0e-7 cert slack. Not merely shrinking — proven saturated.
Do NOT re-attack. BMQS mu_{P,Q} bare = 0.34-0.69 hopeless (R1); weighted recast = the
same saturated Doche cone.

### 3. The standing capacity / transfinite-diameter computation. DECLINE.
A cap(ACT(A)), cap(ACT(B)) or equilibrium-measure number IS new as a computation, but
it is the ORDINARY (real/complex) transfinite diameter of a PLANE SET — a property of
the locus ALONE, with no integer polynomial and no integrality attached. The verified
quantities (r~_Q, m_B) are WEIGHTED log-norms of a FIXED integer Q. Tying cap to the
marginals requires the WITD EQUALITY inf_Q r~_Q = -log d_inf(ACT(A)) — which R7 already
PROVED FALSE-in-the-direction-that-matters: integer roots cannot reach the deepest wells
(firing roots sit strictly inside the unit disk, geometrically away from the locus arc),
so the integer inf sits STRICTLY ABOVE the continuous -log d_inf, and the gap is the
unanalyzed open quantity. Worse, the locus partition is anchor/exponent dependent
(|ACT(A)| = 0.428 at the held family vs 0.0686 under R10's no-candidate-A0 convention),
so "the capacity of ACT(A)" is not even a single well-defined number. A bare cap number
next to the r~ table is a coincidental juxtaposition — the reviewer banks nothing, or the
build overstates it into the unsupported WITD-equality claim. DECLINE (concur with
explorer (b) Step 2).

### 4. A second NEW exact identity (like R10's numerator split). NONE LEFT.
R10 banked the only clean fixed-q identity available: the dual-loci PARTITION (P) +
numerator split (N), Phi(0) = int_ACT(A) A0 + int_ACT(B) B. The first-variation engine
already covers every DERIVATIVE direction: R6 (A-base r~), R8 (B-branch m_B + DCT
rigorization), R9 (unified one-sided theorem incl. tie case). There is no third
distinct exact identity on the held certificate that is not a relabeling of these. A
"second-order / Hessian" first-variation expansion would be new arithmetic, but it is
load-bearing only for a numeric improvement the firing-set theorems already prove cannot
exist (no firing block within reach), so it backs nothing the reviewer would bank.

### 5. Prose consolidation of R6-R10 into "one theorem." BANKS NOTHING.
Explorer-judged + hard rule (R9/R10): re-narration of banked facts banks no milestone.

================================================================================
## Single hardest step (the one that does NOT exist in one round)

Proving the WITD EQUALITY that would make any capacity number load-bearing:

    inf over integer Q of r~_Q  =  -log d_inf(ACT(A))   (and the B-branch analog),

i.e. that the integer transfinite diameter of the active locus equals the best
first-variation marginal. Without it, cap(ACT(A)) is a decoration; with it, it is a
theorem. But R7 already proved the obstruction (integer roots cannot reach the deepest
wells), so the integer inf is STRICTLY above the real -log d_inf and the gap is the
unanalyzed open quantity. This is a multi-round research problem, NOT a one-round
verifiable advance.

================================================================================
## Recommendation to the orchestrator

END the round on the upper side reporting the verifiable-advance well exhausted.
The upper-side package is strong and essentially publication-complete:
  - numeric record 0.2538893183 (R4), tightening Doche 0.25444 by ~5.4e-4;
  - both branches proven maximal-firing-set saturated (R7/R8);
  - the first-variation engine fully unified + rigorous (R6 DCT, R8 B-branch cross-term,
    R9 unified one-sided theorem);
  - the dual-loci numerator decomposition (R10).
R11 should NOT be forced into a milestone. The honest move is WRITE-UP of the existing
verified package. If the orchestrator insists on activity, the least-bad option is a
clearly-scoped EXPLORATORY capacity computation labelled CORROBORATION-ONLY (NOT a
thesis proof, NOT a WITD-equality claim) — but flag up front it likely banks nothing and
may surface the equilibrium/root-measure mismatch (R7), so it is not recommended.

NOTE: the LOWER side is live and improving (R17 held 0.2524001332, gap to upper now
~0.00165) — if the orchestrator wants verified progress this run, the LOWER-side OSS
log-energy certificate is where the well is NOT dry. That is a different dispatch
(this dispatch is UPPER-only), but it is the honest place to point the campaign.
