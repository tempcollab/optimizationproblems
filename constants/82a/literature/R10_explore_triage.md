# R10 explore triage — 82a UPPER (Zhang-Zagier essential minimum)

Explorer: math-explorer, round 10. Triage ONLY — no improvement attempted. On-disk
artifacts only (run_state, current.md, 82a.md, approaches/, literature/ digests,
certificate harness headers + a 30s re-run of verify_shared_pool.py). No new PDFs, no
long silent ops.

Authoritative held (run_state R4 / current.md / verify_upper_q8A.py):
**upper held = 0.2538893183** (REVIEWER-VERIFIED, R4 this campaign). Family = Doche
Doc01a §4 limit-point, j3 (deg 3) + j9 (deg 8) A-base blocks on prod-P^q side; perturbers
Q1*Q2*Q5^qE*Q6^qF (Q5=j13 deg12, Q6=j15 deg16). Best LOWER held = 0.2524001332 (R17,
repo-internal; user flags this WRONG — real lower is Flammang 0.2487458). Doche-conjectured
upper limit ~0.25272. Target to STRICTLY beat on UPPER: 0.2538893183.

State of the kernel after R9 (so we do not re-bank done work):
- First-variation ENGINE is FULLY UNIFIED & RIGOROUS. R6 (A-base DCT lemma), R8 (B-branch
  cross-term + DCT rigorization), R9 (UNIFIED one-sided theorem (T) across all three
  D-regimes incl. the TIE case, with regime-I A-attaining cross-term and regime-II
  corollaries). Candidate (ii)'s "tie + cross-term unification" was ALREADY DELIVERED in R9.
- Both branches PROVEN SATURATED (maximal firing sets): A-base R7, B-branch R8, both
  reviewer-verified. No single added block (original or borrowed) improves the held family.
- WITD shared-pool framing CORE is verified (R6 verify_shared_pool.py; I re-ran it R10,
  PASS 0/55 coprime, all 11 blocks squarefree, P4=j5/P6=j8/P8=j12/Q5=j13/Q6=j15/j3/j9 exact
  Table-1 identities). Re-running it banks NO milestone.

================================================================================
## Q1 — Highest-value GENUINELY-NEW verifiable advance for R10

Both run_state "Next" candidates, judged on whether they yield a NEW verifiable artifact
(a script checking a NEW identity, not a re-run) — because pure prose re-packaging banks
NO milestone:

### Candidate (ii): consolidate R7+R8+R9 into one "criterion explains+optimizes block
### selection AND proves the family saturated" theorem.
**VERDICT: LOW / likely banks NO milestone as a standalone round.** The three verified
components already exist and were each reviewer-banked: R7 A-base maximal-firing-set
(R7_structural_result.py), R8 B-branch maximal-firing-set (screen_Bbranch*.py) +
B-marginal (verify_Bbranch_marginal.py), R9 unified theorem (T)
(verify_unified_firstvar.py). A consolidation is PROSE assembly of already-verified facts;
its checkable core is the union of existing passing scripts. **No NEW identity, no new
script.** The eval counts only NEW verified content (R9 triage rule, repeated in
run_state). The reviewer will (correctly) decline to log a milestone for re-packaging.
NOT the R10 target on its own. (Valuable for the eventual paper, but it is a write-up task,
not a milestone-banking round.)

### Candidate (i): WITD UNIFICATION write-up of Doche-upper vs Flammang-lower as the
### paper thesis, scoped HONESTLY (upper-INTERNAL dual loci {A>B} vs {A<B} ONLY).
**VERDICT: this is the ONLY candidate that can produce a GENUINELY-NEW verifiable
artifact in R10, IF and ONLY IF it is scoped to a NEW IDENTITY, not the R6 shared-pool
re-run.** The framing prose alone rides verify_shared_pool.py (already banked R6) -> no
milestone. To bank a milestone it must produce a NEW checkable identity. The one
genuinely-new, self-contained, reviewer-verifiable identity available on disk is:

  **The UPPER-INTERNAL dual-loci decomposition as an EXACT measure/integral identity.**
  The first-variation marginals live on two DISJOINT, COMPLEMENTARY arcs of s in [0,1]:
  the A-base lever acts on ACT(A)={A_0>B}, the B-perturber lever on ACT(B)={B>A_0}, and
  (modulo the finite kink set K={A_0=B}, |K|=0, established R8) these PARTITION [0,1]:
  1_{A_0>B} + 1_{B>A_0} = 1 a.e. A NEW script can check, on the LIVE held R4 family
  (verify_upper_q8A modules, N=4M):
    (a) |ACT(A)| + |ACT(B)| = 1 to float tol, |K|=0 (kink count stable across N);
    (b) the partition identity feeds Phi(0) = int_{ACT(A)} A_0 + int_{ACT(B)} B  exactly
        (Phi = <max(A,B)> split by the active arc) -- a NEW decomposition of the held
        certificate's NUMERATOR into its two dual-locus contributions, never written
        as an identity before;
    (c) the two marginal families r~_Q (A-side, on ACT(A)) and m_B (B-side, on ACT(B))
        integrate over these COMPLEMENTARY loci -- making "upper-internal dual loci"
        a PROVEN exact statement, not a framing slogan.
  This is NEW verifiable content: no existing script checks the active-arc PARTITION or the
  numerator's dual-locus split; verify_shared_pool checks only poly identities/coprimality,
  verify_firstvar/Bbranch check the marginals on ONE arc each, never the partition.
  HONESTY GUARDRAIL (hard rule): this is UPPER-INTERNAL ({A>B} vs {A<B}). It does NOT touch
  Flammang's lower locus (the whole contour minimized to a point). The "lower = complement
  of upper arc" framing remains UNSUPPORTED -- do NOT revive it. The Doche-upper/
  Flammang-lower link that IS supported is ONLY the shared integer-poly POOL (R6, the
  w=z(1-z) small-Mahler-measure dictionary), not a locus duality.

**Honest caveat on (i):** the partition/decomposition identity is genuinely new and
checkable, but it is a MODEST advance (a clean structural identity, not a deep theorem).
Whether the reviewer banks it depends on the builder framing it as a NEW decomposition of
the held certificate (numerator split + active-arc partition), NOT as a re-statement of
the R6 framing. If the builder only re-narrates the shared-pool framing, it banks nothing.
This is the single risk and the outliner must steer the build to the NEW identity (a/b/c
above), not the framing prose.

### A THIRD option the run_state "Next" did not flag, surfaced here:
**Rigorize the regime-III TIE one-sidedness / kink as a LIVE-family-anchored statement is
NOT available** (no Doche family sits exactly on a tie; R9 already exercised it on a toy
and scoped it honestly). Do NOT try to "upgrade" the tie to a live family -- there is none.

================================================================================
## Q2 — Any remaining numeric upper lever NOT yet ruled out?

**VERDICT (one line): NO. The numeric upper lever is GENUINELY EXHAUSTED on the Doche
family; the only un-refuted numeric direction (a qualitatively different multi-pair BMQS
mu_{P,Q} configuration) has no compass and is a multi-round NEW-construction gamble, not a
tractable R10 opening.**

Skeptical detail (the user's original BMQS hope, re-checked against R1/R7 on disk):
- Bare single-pair mu_{P,Q}: 0.34-0.69 (R1, hopeless; no free real-exponent direction).
- Weighted-product / multi-pair recast: this IS the Doche family (R1, BMQS Rmk 4.6 + §1.4;
  strong duality Thm 6.5 => no separate gap between the mu_{P,Q} parametrization and the
  Doche parametrization -- both are points of the SAME cone). Not a distinct lever.
- A genuinely-DIFFERENT base-set/convex-combination point of the cone is, in principle, a
  different point -- BUT (i) BMQS §1.7 state the "enormous search space, no efficient
  direction" wall; (ii) the only sub-0.34 member ever found is the Doche weighted-product
  member = the held family = proven saturated both branches; (iii) any new combination must
  BEAT the optimized Doche member, which already sits in the favorable part of the cone.
- Is there a CONCRETE not-yet-tried mu_{P,Q} config (specific multi-pair / different P,Q
  degrees) that could plausibly clear cert slack? **No concrete one exists that is not the
  Doche recast.** The cert slack is ~1.2-2.0e-7; A-base per-step gain decayed j3 +1.49e-4 ->
  j9 +3.2e-6 (47x/step) -> next projects ~1e-7 AT/BELOW slack; the realized-drop/|r_tilde|
  conversion factor itself collapsed ~14x as the dictionary filled. This is genuine dryness
  (geometric obstruction: firing roots sit strictly inside the unit disk where no integer
  w^2-pw+q root can reach), not merely shrinking returns. A blind BMQS multi-pair search has
  no objective/compass and no guarantee -- NOT a one-to-few-round opening.

So: the numeric upper lever is dead for the round budget. Negative finding stated plainly.

================================================================================
## Q3 — Single softest, most-verifiable target for R10 + the ONE hard step

**Softest, most-verifiable NEW target: candidate (i) scoped to the NEW IDENTITY only --
the UPPER-INTERNAL dual-loci PARTITION + held-certificate NUMERATOR DECOMPOSITION**
(active-arc partition 1_{A_0>B}+1_{B>A_0}=1 a.e.; Phi(0) = int_{ACT(A)} A_0 + int_{ACT(B)} B
exact split; the two marginal families r~_Q, m_B integrate over these complementary loci).
This is the only remaining clean, genuinely-NEW, single-round, reviewer-verifiable advance,
and it makes "upper-internal dual loci" a PROVEN exact statement that the paper's WITD
thesis section can rest on -- distinct from the already-banked R6 shared-pool identities
and the R9 marginal theorem.

**THE ONE HARD STEP:** rigorously handling the kink set K={A_0=B} so the partition is an
EXACT a.e. identity, not just a numerical near-partition. Specifically: (1) show |K|=0
(A_0-B real-analytic, not identically 0 => finite zero set -- this is the R8 audit fact,
CITE it, do not re-derive); (2) confirm the float active-arc measures |ACT(A)|+|ACT(B)|
sum to 1 to tol on the LIVE held family (a NEW check, N>=4M, kink count stable across N --
the artifact); (3) state the numerator split Phi(0)=int_{ACT(A)}A_0+int_{ACT(B)}B as an
EXACT identity (G=max(A_0,B)=A_0 on ACT(A), =B on ACT(B), a.e.) and verify it numerically
reproduces the held Phi(0)/D = 0.2538893183 to cert precision. The risk is framing: the
builder MUST present this as a NEW decomposition of the held certificate, not a re-narration
of the R6 framing, or the reviewer banks nothing.

================================================================================
## Dead ends (do NOT retry) — authoritative lineage

- A-base dictionary enrichment (any block, original or borrowed): PROVEN saturated/DRY,
  reviewer-verified R7 maximal-firing-set, geometric obstruction. [run_state hard rule]
- B-branch perturber enrichment (any block): PROVEN saturated/DRY, reviewer-verified R8
  maximal-firing-set (firing blocks inadmissible; admissible atoms above threshold).
- BMQS mu_{P,Q} as a DISTINCT upper lever: bare single-pair 0.34-0.69 hopeless (R1);
  weighted/multi-pair recast = the saturated Doche family (strong duality => no separate
  gap). NOT a one-to-few-round numeric opening.
- Same-family q-only tuning: dry (R6 gained 1.8e-6, now sub-cert-slack). DEAD.
- Candidate (ii) consolidation as a STANDALONE milestone round: re-packaging of already-
  banked R7/R8/R9 facts; no new identity/script => reviewer banks nothing. (Fine for the
  eventual paper write-up, NOT a milestone round.)
- Re-running verify_firstvar_lemma.py / verify_Bbranch_marginal.py / verify_shared_pool.py
  / verify_unified_firstvar.py as a "milestone": already reviewer-verified; re-running
  banks NO new milestone.
- The R9 tie/cross-term unification: ALREADY DELIVERED (R9 theorem (T)). Do NOT re-bank it.
- "lower locus = complement of upper active arc" framing: UNSUPPORTED, hard rule. Flammang's
  lower locus is the whole contour minimized to a point. Do NOT revive.
- The WITD inequality inf_Q r_tilde ~ -log t_{Z,phi} as a full theorem: real open
  lower-bound side, NOT one-round-tractable. Framing/corollary only.
- Lower side: do NOT touch. Repo's 0.2524 is user-flagged WRONG; real lower is Flammang
  0.2487458 (analogy/shared-pool source only). [run_state, user R6]
- A live A-dominant Doche family (to FD-exercise the regime-I cross-term): none exists on
  disk (held family arg_A=61.66 < arg_B=72.00, regime II). Do NOT promise to build one;
  R9 correctly scoped regime I to a toy. [R7 role-memory]

## Files read (no new artifacts fetched)
- /tmp/memory/run_state.md, /tmp/memory/math-explorer.md
- constants/82a/current.md, constants/82a.md (README row reconciled: held upper
  0.2538893183, matches run_state R4)
- constants/82a/literature/{R9_explore_triage.md, flammang_F18_digest.md}
- constants/82a/approaches/R9-unified-firstvar.md
- re-ran constants/82a/certificate/verify_shared_pool.py (PASS, ~1.3s) to confirm WITD core
