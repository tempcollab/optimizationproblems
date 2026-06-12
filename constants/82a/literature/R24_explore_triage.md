# R24 explore triage — 82a UPPER (Zhang-Zagier essential minimum)

Explorer: math-explorer, round 24. READ-ONLY start-of-round RE-CONFIRMATION triage. No
improvement attempted, no new PDF fetches, no multi-minute computation. On-disk material only
(run_state.md, current.md, 82a.md + README row, R23/R22/R21 triages + R10/R11 skim, approaches/
+ certificate/ listings, git log, role memory /tmp/memory/math-explorer.md).

Held VERIFIED upper bound to STRICTLY beat: **0.2538893183** (R4 this campaign,
verify_upper_q8A.py; Doche Doc01a §4 limit-point family + j3 deg-3 + j9 deg-8 A-base blocks,
B-perturbers Q1*Q2*Q5^qE*Q6^qF). README and current.md agree (upper 0.25389). Two-sided gap to
held LOWER 0.2524001332 (R17) is ~0.00149.

This is the **FOURTEENTH** consecutive round-start UPPER triage (R11–R23 all DRY; now R24).

## On-disk change check (verified directly via git, not on faith)
- `git log 239b19b..HEAD -- constants/82a/certificate/` is EMPTY. The newest certificate artifact
  is still R10's `verify_dual_loci_decomposition.py` (commit 239b19b, 2026-06-12 02:21:57).
- Rounds 11–23 added ONLY triage write-ups in literature/ (R11–R23_explore_triage.md). The
  standing UPPER package is BIT-IDENTICAL to what R10 banked and R11–R23 adjudicated dry.
- The round-24 dispatch carries NO new idea: it restates the three standing levers verbatim —
  (Q2) R1 BMQS Thm 4.5 density family; (Q3) R7 "minimize r_Q over Z[X]" design principle;
  (Q1) the WITD-independent-artifact question — all three recorded as Goal Updates R1/R6/R7 and
  adversarially closed in R7–R23.

================================================================================
## Q1 — Any concrete NEW WITD-independent computed artifact a reviewer would BANK in one round?
## ANSWER: **NO.** VERDICT: **DRY.**

Every artifact category collapses to a reviewer-verified dead end (carried forward, re-confirmed
against current.md Progress log R6–R10 and the R21–R23 triages):

1. **Numeric upper (A-base or B-branch Doche enrichment): DEAD** by two reviewer-verified
   maximal-firing-set theorems. A-base (R7): cheapest coprime original w^2-w+1 costs
   r_tilde +0.0131 > |best firing margin -0.0052|, so every original product flips non-firing
   (73845 originals -> 0 firing). B-branch (R8): all 263 admissible atoms have int/deg >= 0.2631 >
   logh 0.2539; every firing block is inadmissible. Per-step gain decayed ~47x (j3 +1.49e-4 ->
   j9 +3.2e-6); next same-kind step projects ~1e-7 <= cert slack 1.2–2.0e-7. Hard rule in run_state.

2. **Second fixed-q numerator identity (R10-style): NONE LEFT.** R10 banked the one clean fixed-q
   numerator split Phi(0)=int_{A>B}A0+int_{B>A}B; the R9 unified one-sided first-variation theorem
   (T) covers every derivative direction. No second clean identity remains.

3. **Capacity / transfinite diameter / equilibrium measure of ACT(A)/ACT(B): REFUTED** — the trap
   the dispatch warns against. NEW as a number (no on-disk script computes it) but BACKS NOTHING:
   capacity is a property of the plane SET alone, independent of any Q; tying it to the verified
   Q-weighted marginals r_tilde/m_B IS exactly the open WITD equality
   inf_Q r_tilde_Q = -log d_inf(ACT(A)), which R7 PROVED FAILS in the load-bearing direction
   (firing integer roots sit |zeta| in [0.43,0.79] strictly inside the unit disk, away from the
   deepest U^nu wells, so the integer inf sits STRICTLY ABOVE the continuous -log d_inf). It is also
   anchor-dependent (|ACT(A)|=0.428 at R4 exponents vs 0.0686 under R10 convention) — not one
   well-defined number. This is the WITD-INDEPENDENCE objection in full: it secretly ties a
   Q-independent set property to the verified Q-weighted marginals. Banks nothing.

4. **Second-order / Hessian first-variation expansion:** backs only a numeric break that the two
   maximal-firing-set theorems prove cannot exist within reach. No banked advance.

5. **WITD equality as a real theorem:** OPEN, multi-round. Not one-round reachable.

6. **Consolidate R6–R10 into one theorem:** prose re-assembly of already-banked facts; no NEW
   identity/script. The reviewer rejected this in R9–R23. Banks nothing.

No category yields a concrete, new, one-round, WITD-independent, non-re-run artifact.

================================================================================
## Q2 — Does BMQS Thm 4.5 density unlock any non-Doche mu_{P,Q} construction?
## ANSWER: **NO.** VERDICT: **DRY.**

The dichotomy is exact (re-checked against bmqs_2026_digest.md + R21–R23 triages):
- (a) BMQS Thm 6.5 strong duality (P(g)=ess(h_g)=D(g)) pins the optimum to the saturated cone; the
  Doche weighted-product family IS the V=prod P^q interior direction (Rmk 4.6 / §1.4), and BOTH
  branches are proven saturated (R7/R8). Density says the mu_{P,Q} APPROXIMATE the optimum, not that
  any of them is a sub-Doche feasible point a one-round build could certify below 0.2538893183.
- (b) The bare single-pair mu_{P,Q} is the ONLY genuinely-non-Doche member, and it is hopeless
  (R1 numeric: every valid coprime-irreducible low-degree pair gives 0.34–0.69 vs held 0.2539).
  Multi-pair / weighted mu' (Rmk 4.6) IS the Doche recast — there is no third kind.
- (c) BMQS state their own wall (§1.7: "far from being practical," "no efficient criterion"). Any
  equidistributing minimal-poly sequence hits R7's geometric obstruction (firing roots strictly
  inside the disk). A multi-round directed-search gamble, NOT a one-round construction.

So Q2 is neither (a) the hopeless bare single-pair nor (b) anything but the strong-duality-pinned
Doche recast. DRY.

================================================================================
## Q3 — Is "minimize r_Q over Z[X]" anything beyond the WITD primal, already closed?
## ANSWER: **NO — fully closed.** VERDICT: **DRY.**

The R7 design problem (minimize the certified first-variation marginal r_tilde_Q over integer Q) IS
the construction (primal) side of the WITD problem. It is refuted by BOTH maximal-firing-set
theorems: A-base (R7, 73845 originals -> 0 firing; cheapest coprime original r_tilde +0.01311 >
|best firing margin -0.00521|) and B-branch (R8, every firing block inadmissible; all 263 admissible
atoms above the firing gate). Both branches reviewer-verified saturated within reach (deg <= 16,
~80k candidates, LLL/CVP/well-rounding). No unexercised sub-case. Closed.

================================================================================
## Adversarial self-attack: name ONE concrete builder dispatch, then break it
Per the dispatch instruction, I tried hard to manufacture a PROCEED:

- "Dispatch builder to compute log capacity of ACT(A) and equate to the firing infimum." -> This is
  precisely the WITD equality R7 proved FAILS (integer inf strictly above continuous -log d_inf).
  The reviewer would reject the equality as false in the load-bearing direction; the bare capacity
  number backs no marginal. FAILS Q1.3.
- "Dispatch builder to search deg 17–24 A-base / B-branch blocks (beyond R7/R8 reach)." -> The
  maximal-firing-set obstructions are GEOMETRIC (firing roots must sit inside the lemniscate where
  no integer w^2-pw+q root reaches; firing products inadmissible), not a reach artifact; higher
  degree also risks a D-switch and duplicates Q6 (deg 16). Realized-drop conversion already
  collapsed ~14x j3->j9, so even a firing-sign block projects below the 5e-6 gate. Multi-round
  gamble with no compass, not a one-round bankable artifact. FAILS Q1.1 + role-memory R7.
- "Dispatch builder to certify a bare single-pair mu_{P,Q} from BMQS density." -> 0.34–0.69, far
  ABOVE held; not an upper-bound improvement at all. FAILS Q2(b).
- "Dispatch builder to write the second-order expansion / consolidated theorem." -> backs an
  impossible numeric break / prose re-assembly; reviewer banks neither. FAILS Q1.4/Q1.6.

Every PROCEED temptation collapses identically to R21–R23. No valid builder dispatch exists.

================================================================================
## NET VERDICT: **DRY (PLATEAU).** Fourteenth consecutive dry-well triage.

The standing UPPER package is publication-complete: R4 record 0.2538893183 + both-branch
maximal-firing-set saturation (R7/R8) + fully unified rigorous first-variation engine (R6/R8/R9) +
R10 dual-loci numerator decomposition. Any further one-round UPPER milestone requires a
QUALITATIVELY NEW idea from the user (a non-Doche construction, or a technique for the OPEN
multi-round WITD equality). The repeated identical BMQS Thm 4.5 / R6 thesis / R7 design-principle
dispatch supplies no such idea.

Honest action: no valid builder dispatch -> no build -> no reviewer. END round PLATEAU.
Recommend the user (1) pivot this campaign to WRITE-UP of the verified UPPER package, or (2)
re-target the LOWER side (OFF-LIMITS in this UPPER dispatch; the live frontier — gap now ~0.00149),
or (3) re-target a DIFFERENT registry constant with an open verifiable-advance well.

## Files read (no new artifacts fetched)
- /tmp/memory/run_state.md (held upper 0.2538893183; eval history R2–R23; Rules; role levers)
- /tmp/memory/math-explorer.md (role memory — corroborates every dead end, incl. R11 capacity refutation)
- constants/82a/current.md + 82a.md + README row 82a
- constants/82a/literature/R23_explore_triage.md (+ R22/R21 referenced)
- constants/82a/approaches/ + literature/ + certificate/ dir listings
- git log 239b19b..HEAD -- constants/82a/certificate/ (EMPTY; bit-identical since R10)

VERDICT: DRY — no valid builder dispatch (14th consecutive)
