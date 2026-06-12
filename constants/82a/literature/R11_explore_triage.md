# R11 explore triage — 82a UPPER (Zhang-Zagier essential minimum)

Explorer: math-explorer, round 11. Triage ONLY — no improvement attempted. On-disk
artifacts only (run_state, math-explorer role memory, current.md, approaches/,
literature/ digests, certificate headers) + three short (<60s) numeric probes of the
held family loci. No new PDFs, no long silent ops.

================================================================================
## (a) Number to beat + saturation status

**Held VERIFIED upper bound = 0.2538893183** (REVIEWER-VERIFIED, R4 this campaign;
verify_upper_q8A.py; j3 deg-3 + j9 deg-8 A-base blocks on Doche Doc01a §4 family,
perturbers Q1*Q2*Q5^qE*Q6^qF). Reconciled against run_state R4, current.md, and the
authoritative harness — consistent. Doche-conjectured upper limit ~0.25272. Best
verified lower (context only, do NOT touch) = Flammang 0.2487458; the repo's 0.2524 is
user-flagged WRONG.

**NUMERIC UPPER LEVER IS GENUINELY EXHAUSTED on the Doche family** — confirmed, do not
re-attack:
- A-base dictionary: PROVEN maximal firing set (R7, reviewer-verified, deg<=16 / ~80k
  candidates). Geometric obstruction: firing roots sit strictly inside the unit disk
  where no integer w^2-pw+q root can reach; every coprime original factor costs
  r_tilde >= +0.013 > |best firing margin -0.005|. Best reachable borrowed block (j16)
  converts to float drop 2.94e-6 < the 5e-6 gate.
- B-branch perturbers: PROVEN maximal firing set (R8, reviewer-verified). Every firing
  block inadmissible (Q(1)=0 / non-sqfree / contour roots); all 263 admissible atoms
  have int/deg >= 0.2631 > threshold (log h)=0.2539.
- BMQS mu_{P,Q} as a distinct lever: bare single-pair 0.34-0.69 hopeless (R1);
  weighted/multi-pair recast = the saturated Doche family (BMQS strong-duality Thm 6.5
  => same cone, no separate gap). NOT a one-to-few-round opening.
Per-step gain decayed j3 +1.49e-4 -> j9 +3.2e-6 (47x/step); next projects ~1e-7
at/below the ~1.2-2.0e-7 cert slack. Dead, not merely shrinking.

================================================================================
## (b) Named concrete new computed artifact for R11

The dispatch's standing candidate: COMPUTE the logarithmic capacity / transfinite
diameter (and/or equilibrium measure) of the two active loci ACT(A)={A0>B} and
ACT(B)={A0<B} of the held certificate, and relate it to the first-variation marginals
r_tilde (ACT(A)) and m_B (ACT(B)).

### Step 1 — Is it genuinely NEW content (not already on disk)? YES.
I grep-checked every certificate script. NO script computes an actual logarithmic
capacity / transfinite diameter / equilibrium measure of either locus:
- `verify_shared_pool.py` uses the *phrase* "weighted integer transfinite-diameter
  problem t_{Z,phi}" only as FRAMING/analogy in its header; it checks exact integer-
  poly identities + coprimality, no capacity number.
- `screen_conditional_capacity.py` "conditional-capacity" is a least-squares RESIDUAL
  ranking heuristic (regress log|Q| on the active dictionary's log-potentials), NOT a
  capacity of a set.
- `verify_dual_loci_decomposition.py` (R10) computes the active-arc PARTITION and the
  numerator split Phi=int_ACT(A)A0+int_ACT(B)B — a measure/integral identity, NOT a
  capacity.
So an honest cap(ACT(A)), cap(ACT(B)), and the equilibrium measures would be a NEW
computed quantity. The loci are well-posed: my probe (N=2e5, held family) shows each
is a SINGLE connected arc (2 sign changes of 1_{A0>B}), mapping under chi(s)=z(1-z) to
a connected curve segment in the plane (|w| in [0,1.25], Re in [0,1.125], Im in
[-0.55,0.53]) — so its 2D logarithmic capacity / transfinite diameter is computable by
the standard Leja-points / discretized-energy estimator in well under 60s.

### Step 2 — Would it genuinely BACK the integer-transfinite-diameter thesis? NO —
### this is the honest blocker, and it is decisive.

The thesis is "block selection on each locus is an INTEGER transfinite-diameter /
integer-Chebyshev problem." What a capacity computation would actually produce is the
ORDINARY (real/complex) transfinite diameter d_inf(ACT(A)) of the PLANE SET — a single
geometric number with NO integrality and NO polynomial attached. The quantities the
thesis is about, and that are already verified, are:
  - r_tilde_Q = (1/D) int_ACT(A) log|Q(chi)| ds  (A-base marginal, R6 lemma), and
  - m_B(Q)    = (1/D)[int_ACT(B) log|Q| - (log h)*deg(Q)]  (B-branch, R8),
i.e. WEIGHTED log-norms of a FIXED integer polynomial Q over the locus. The transfinite
diameter / equilibrium measure of the locus is a property of the SET ALONE, independent
of any Q. There is NO theorem on disk (or available in one round) that equates
inf over integer Q of r_tilde_Q with -log d_inf(ACT(A)) or with the equilibrium energy
— that equality is exactly the WITD inequality `inf_Q r_tilde ~ -log t_{Z,phi}`, which
the R10 triage and the role memory already flagged as the REAL OPEN lower-bound-side
problem, NOT one-round-tractable (dead end list, R10). A bare cap(ACT(A)) number sitting
next to the r_tilde table is a COINCIDENTAL juxtaposition, not a proof that ties the
thesis to a number — the reviewer (who has banked R6-R10 only on genuinely-new
CHECKABLE content that means something) would correctly judge an un-theorem'd capacity
number a non-load-bearing decoration and bank nothing, OR worse, the build would
overstate it into the unsupported WITD-equality claim.

Two further concrete problems make this artifact thin even as a number:
1. The locus partition is ANCHOR/EXPONENT dependent. My probe at the held R4 family
   gives |ACT(A)|=0.428 / |ACT(B)|=0.572; R10's decomposition reports 0.0686 / 0.9314
   (A0 taken WITHOUT the candidate blocks vs. with). So "the capacity of ACT(A)" is not
   even a single well-defined number — it depends on which A0 convention is used, and
   neither convention is privileged by a theorem. A number that moves with an arbitrary
   convention does not back a structural thesis.
2. The marginals r_tilde, m_B integrate a SPECIFIC integer Q, not the equilibrium
   measure. To "relate" cap to the marginals you would need the equilibrium measure of
   the locus to be (near) the root-counting measure of the firing blocks j3/j9 — but
   R7 already PROVED the firing roots sit strictly INSIDE the unit disk, geometrically
   away from the locus arc (which is why no integer block reaches the deepest wells).
   So the equilibrium measure of ACT(A) and the j3/j9 root measure are KNOWN to be
   geometrically mismatched — a capacity computation would, if anything, CONTRADICT the
   "blocks approximate the equilibrium distribution" slogan, not support it.

### VERDICT on the candidate: the capacity/transfinite-diameter artifact is NEW as a
### computation but DOES NOT back the thesis and is not a defensible milestone. Decline it.

================================================================================
## (b') VERDICT FOR THE ROUND — the verifiable-advance well is DRY

I find NO concrete new computed artifact that (i) is genuinely new, (ii) is verifiable
in one round, AND (iii) means something for the thesis. Specifically:
- Numeric upper: dead (both branches saturated, BMQS recast = Doche). [hard rule]
- The capacity/transfinite-diameter computation: new as a number but un-theorem'd and
  anchor-dependent; backs nothing and risks the unsupported WITD-equality overstatement
  (see (b) Step 2). Decline.
- R10 already banked the dual-loci PARTITION + numerator split — the only clean new
  identity that was on disk. There is no second such identity left.
- Consolidation of R6/R7/R8/R9 into one theorem: prose re-assembly, banks nothing
  (R9 + R10 triage, run_state hard rule).
- The WITD inequality inf_Q r_tilde ~ -log t_{Z,phi} as a real theorem: open lower-side
  problem, multi-round, NOT tractable. (This is the only direction a capacity number
  would matter, and it is exactly the thing that is hard.)

**RECOMMENDATION TO THE USER (honest):** the verifiable-advance well for 82a UPPER is
now exhausted on BOTH the numeric lever (saturated both branches, R7/R8) AND the
structural lever (engine fully unified+rigorous R6/R8/R9; both maximal-firing-set
theorems R7/R8; dual-loci numerator decomposition R10). The paper material is
essentially COMPLETE. The standing capacity-computation candidate, on close inspection,
does not tie the thesis to a meaningful number — it would either bank no milestone or
tempt an overstatement of the genuinely-open WITD equality. R11 should NOT be forced
into a milestone; recommend the user pivot to WRITE-UP of the existing verified package
(which is strong and publishable) rather than spend another agent round mining a dry
well. If the user insists on a round, the least-bad option is a clearly-scoped
EXPLORATORY capacity computation labelled CORROBORATION-only (NOT a thesis proof, NOT a
WITD-equality claim) — but flag up front it likely banks nothing and may even surface
the equilibrium/root-measure MISMATCH noted in (b) Step 2.2.

================================================================================
## (c) Single hardest step

**The one hard step is the one that does NOT exist in one round:** proving the WITD
EQUALITY that would make a capacity number load-bearing —
   inf over integer Q of r_tilde_Q  =  -log d_inf(ACT(A))  (and the B-branch analog),
i.e. that the integer transfinite diameter of the active locus equals the best
first-variation marginal. Without it, cap(ACT(A)) is a decoration. With it, it is a
theorem — but it is the real open problem (R7 already proved the obstruction: integer
roots cannot reach the deepest wells, so the integer inf is STRICTLY ABOVE the
real/complex -log d_inf, and the gap is exactly the unanalyzed quantity). This is a
multi-round research problem, not a one-round verifiable advance.

================================================================================
## Dead ends (do NOT retry) — carried forward, authoritative

- A-base enrichment (any block): PROVEN saturated, R7 maximal firing set. [hard rule]
- B-branch enrichment (any block): PROVEN saturated, R8 maximal firing set. [hard rule]
- BMQS mu_{P,Q} as a distinct lever: hopeless bare / = Doche recast. [R1]
- Same-family q-only tuning: sub-cert-slack, DEAD. [R6]
- Consolidation R6+R7+R8+R9 into one theorem: prose re-assembly, banks nothing. [R9/R10]
- Re-running any existing verified script as a "milestone": banks nothing.
- "lower locus = complement of upper active arc": UNSUPPORTED. [hard rule]
- The WITD inequality inf_Q r_tilde ~ -log t as a full theorem: open lower-side, multi-
  round, NOT one-round-tractable. (The capacity-computation candidate collapses to this.)
- Lower side: do NOT touch (repo 0.2524 user-flagged wrong; real lower Flammang 0.2487458).
- A live A-dominant Doche family to FD the regime-I cross-term: none on disk. [R7 memory]
- NEW THIS ROUND: the cap/transfinite-diameter computation of ACT(A)/ACT(B) as a THESIS-
  BACKING milestone — new as a number, but un-theorem'd, anchor-dependent, and the
  equilibrium measure is geometrically MISMATCHED with the j3/j9 root measure (R7), so it
  backs nothing and risks the WITD-equality overstatement. Decline as a milestone target.

## Files read (no new artifacts fetched)
- /tmp/memory/run_state.md, /tmp/memory/math-explorer.md
- constants/82a/current.md (held reconciled 0.2538893183)
- constants/82a/literature/R10_explore_triage.md
- certificate headers: verify_shared_pool.py, screen_conditional_capacity.py,
  verify_dual_loci_decomposition.py (grep for capacity/transfinite/equilibrium)
- 3 short probes via verify_dual_loci_decomposition.AB_arrays on the held family
  (loci are single connected arcs; |ACT(A)|=0.428/|ACT(B)|=0.572 at held R4 exponents,
  vs R10's 0.0686/0.9314 under the no-candidate A0 convention — anchor-dependent).
