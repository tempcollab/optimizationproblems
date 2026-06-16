# R10 explorer triage — 82a generative/predictive residual

Scope: triage whether ANY tractable, certifiable, genuinely-new generative/predictive
angle remains on the first-variation theory paper (`upper_bound_paper.tex`) that the
campaign has NOT already killed. NOT a new-bound campaign. Held bounds FROZEN
(upper 0.2538893183, lower 0.2524001332). Status `none`.

I read: run_state.md (Rules + Eval History), math-explorer role memory (esp. the R7
obstruction note, line 12), current.md, upper_bound_paper.tex (intro scope, sec:generator
scope, sec:saturation rem:evidence/rem:wells/rem:noteq, eq:additive), the bridge-support
dead-end doc (R3-bridge-support-selection.md), R7-structural-angles.md, R7_explore_structure.md,
firstvar_04/08/09/10. I re-ran numerical probes on the load-bearing facts (results below).

================================================================================
## TRIAGE VERDICT (one line)

ONE genuinely-new, SAFE-DIRECTION, deep-well-free candidate survives: a **base-marginal
sign / firing-obstruction theorem** that PROVES the paper's currently-heuristic
`rem:wells` geometric claim. It is the only residual angle that is not already a
documented dead end AND avoids the deep-well interval blow-up that killed bridge-support.
Everything else (bridge SUPPORT, SEED-Q* derivation, WITD, full-box certs, lower-side
energy) is dead or out-of-scope for a theory milestone. Honest caveat: the obstruction
theorem is a milestone of MEDIUM novelty (it upgrades an existing Remark from "evidence"
to "proof"), and its clean form has a delicate boundary at Re(X)=0 — see Hard step.

================================================================================
## A. WHAT IS ALREADY DEAD (do NOT re-propose — verified this round)

1. **Bridge SUPPORT selection** (Angle 1/2, firstvar_10, D(d)^lo>0 vs Q*=R0).
   VERIFIED STRUCTURAL DEAD END (R6, run_state Rules, R3-bridge-support-selection.md).
   The discriminating +e-4 firing signal lives in R0's near-cancellation deep-well
   STRADDLE cells, where a rigorous LOWER bound banks ~-4.1e-4 of irreducible negative
   mass (sublinear in N, D_lo<0 even at N=60000). The sign-flip of the working
   firstvar_09 UPPER-bound cert is FATAL. Also ~17h infeasible. Do not retry.

2. **SEED-Q* derivation from the criterion.** Doche's seed (the small-height +
   "product of P_i divides Q1-Q2" resultant heuristic) is the only known answer; a
   criterion-derived integer optimality runs into R7's sparse-knife-edge dead end
   (firing integer roots sit strictly inside |z|<1, cannot reach the continuous wells).
   Role-memory NEVER rule (round 3). Future-work remark only.

3. **WITD / transfinite-diameter / equilibrium reading of seed choice.** Refuted by
   paper rem:noteq (equilibrium potential ~0.524 >> log h=0.254) AND R7 (integer roots
   strictly inside disk). Paper already records the obstruction. Dead.

4. **Full-box certs over 729 boxes without precomputed shared geometry.** ~17h,
   infeasible/unreviewable (run_state Rules, round 6).

5. **Lower-side OSS log-energy column** (R7 Angle 2). Genuine upside but (a) it is a
   NEW-BOUND attempt, not a theory milestone, and (b) its certificate is multi-stage
   self-coupled potential-theory machinery the reviewer flagged as the unsolved part.
   Out of scope for this theory-paper task; not a near-term milestone.

================================================================================
## B. THE ONE SURVIVING CANDIDATE — base-marginal firing-obstruction theorem

### The precise claim
Work with the BASE branch of Corollary cor:criterion: a block Q fires (enters the bound
profitably on the base side) iff its base marginal
    r~_Q = int_{Omega_F} log|Q(chi)| ds  <  0,   Omega_F = {A>B} (the active base arc).
Two structural facts make this analysable root-by-root:

  (i) EXACT additivity over X-ROOTS (finer than the paper's eq:additive, which is
      factor-only). Writing Q(X) = prod_j (X - alpha_j) (monic; constant absorbed by
      admissibility Q(0)=Q(1)=1), r~_Q = sum_j U(alpha_j) where
          U(alpha) := int_{Omega_F} log|chi(s) - alpha| ds.
      VERIFIED this round to 1.7e-17 on j3 (X^3+X^2-2X+1): r~ direct = sum U(alpha_j).

  (ii) The single-root potential U(alpha) is >= 0 OUTSIDE a COMPACT well-region W
       strictly inside the X-plane, and U(alpha) -> +infinity as |alpha| -> infinity
       (U(alpha) ~ meas(Omega_F)*log|alpha|, meas=0.0686; VERIFIED: U(2)=0.043,
       U(5)=0.108, U(10)=0.157).

THE OBSTRUCTION (the theorem): if EVERY X-root alpha_j of an admissible block Q lies in
the half-plane Re(alpha) <= 0 (equivalently, by the X<->1-X near-symmetry, Re(alpha)>=1),
then r~_Q >= 0 and Q CANNOT FIRE. More usefully: a NECESSARY condition for Q to fire is
that at least one X-root lies in the compact well-region W = {U<0}, and the firing margin
is bounded below by sum over roots OUTSIDE W of their (positive) U plus the W-root
contributions. This is a PREDICTIVE necessary condition a firing block must satisfy —
genuine generative/diagnostic content, NOT a construction.

### Why it might be CERTIFIABLE in feasible time (avoids the deep-well blow-up)
- The load-bearing inequality is U(alpha) >= 0 on a CLOSED region (Re<=0, |alpha| large),
  the SAFE direction — exactly the orientation that made firstvar_09 (UPPER<0) work and
  is the OPPOSITE of the bridge-support killer (which needed a positive LOWER bound on a
  near-cancelling integral). U(alpha) >= 0 needs only an OUTWARD-rounded UPPER... no: it
  needs a rigorous LOWER bound on U, but on a region where U is comfortably positive
  (>= +1e-3 once Re <= -0.05; VERIFIED U(-0.05)=+0.0024), with NO near-cancellation and
  NO deep well — log|chi - alpha| has no singularity because alpha is held OFF the contour
  (alpha in Re<=0, the contour chi lives near Re in [0,0.25]). There is no straddle-cell
  banking problem at all: the integrand is a smooth bounded function of s for fixed alpha,
  integrated over a FIXED arc. This is a 1-D quadrature, not a 729-box deep-well cert.
- VERIFIED structure of W (this round, N=8e5, R4 anchor): {U<0} occupies
  0 <= Re <= 0.95, |Im| <= 0.70, min U = -0.035. U over the entire half-plane Re in
  [-3,0] dips only to -1e-5 (the Re=0 boundary), and U over Re in [1,4] is >= +1e-5.
  So the well is genuinely compact and the half-planes are (essentially) clean.

### The hard step (single, gating) — and an honest delicacy
HARD STEP: the well-region W touches the line Re(X)=0 EXACTLY (min Re of {U<0} = 0.0 at
the finest scan; U(0) ~ -1e-5, U(0+/-0.1i) ~ +9e-5). The earlier role-memory figure
"min Re of {U<0} = +0.016" does NOT reproduce on this anchor — the well reaches Re=0.
Consequences for the theorem:
  - The clean statement "Re(alpha) <= 0 => U >= 0" is borderline AT the axis (U ~ -1e-5),
    so it must be stated with a STRICT open half-plane Re(alpha) < -delta for an explicit
    small delta (e.g. Re <= -0.02, where U >= +1e-3 with margin), OR the boundary U(iy)>=0
    must be proved exactly (it likely IS >= 0 on the imaginary axis by a symmetrization of
    log|chi - iy|, but that is a genuine analytic lemma, not a quadrature).
  - To make it a THEOREM (not "computational evidence") the load-bearing U(alpha) >= 0
    must be certified for a CONTINUUM of alpha in the closed half-plane, not a grid. The
    feasible route: (a) a rigorous outward-rounded LOWER bound on U(alpha) uniform over
    alpha in a box via interval arithmetic in BOTH s and alpha (the integrand
    log|chi(s)-alpha| is monotone-controllable in alpha away from the contour); plus
    (b) the far-field tail U(alpha) >= meas*log|alpha| - C for |alpha| > R0 closing the
    unbounded part analytically (one clean Jensen/sub-mean-value estimate). This is a
    real but BOUNDED analytic+interval task — no deep-well blow-up, no 729 boxes.

### Is it a genuinely-new milestone, or re-dressing the existing two?
GENUINELY NEW, but adjacent. The paper ALREADY has rem:wells, which ASSERTS exactly this
geometry ("r~_Q is negative only when a root sits in a deep well ... strictly inside the
lemniscate, where an admissible integer block cannot place a root without a conjugate
elsewhere that pays for it") but explicitly disclaims it: "the statements above rest on
the additivity and the reproduced marginals, NOT on the geometry," and the whole
sec:saturation is flagged "computational evidence, not a non-existence theorem." Turning
rem:wells into a PROVED root-localisation necessary condition (with the X-root additivity
identity, the certified U>=0 half-plane, and the compact well) is a NEW structural theorem
with predictive content — it tells you WHERE a firing block's roots must sit, which is the
diagnostic/generative direction the user wants and which the paper currently only asserts.
It is NOT the sibling generator (thm:generator) and NOT the exponent optimality
(prop:restricted-opt); it is orthogonal to both. It is medium-novelty: it upgrades an
existing Remark to a Proposition, not a brand-new phenomenon.

### Smallest atomic build (for the outliner, NOT to attempt here)
State Prop: "exact X-root additivity r~_Q = sum_j U(alpha_j)" (one-line, already 1e-17
verified) + Prop: "U(alpha) >= 0 for Re(alpha) <= -delta and for |alpha| >= R0, hence an
admissible block all of whose X-roots avoid the certified compact well W={U<0} cannot
fire" + a certificate that (i) reproduces additivity, (ii) outward-rounded LOWER-bounds U
on a box-cover of {Re <= -delta, |alpha| <= R0} and closes |alpha|>R0 by the tail
estimate, (iii) prints the certified W bounding box. One new firstvar_11_obstruction.py;
fork the firstvar_04 AB_arrays anchor (Omega_F = {A>B} on the held R4 family).

================================================================================
## C. ANGLES CONSIDERED AND REJECTED THIS ROUND (besides A's dead ends)

- **A WELL-LOCALISATION strengthening of the sibling generator** (predict R0,R2's roots
  from the seed's roots via the bridge as a root-displacement map): the displacement is
  genuine (R1 explore (M2): R0's roots COPY Q1's roots), but quantifying it into a
  certifiable optimality runs back into the SEED-derivation dead end (you'd need the seed
  roots' optimality, which is heuristic). No new certifiable claim.

- **Monotonicity / closed-form lower bound on the firing margin in the bridge exponent a**
  (extend prop:restricted-opt to a continuous a, or a closed-form for D_a): the consecutive
  differences D_a are already certified monotone (-2.06e-3 -> -3.12e-4); a closed form would
  be nicer but (i) a is an integer (exponent), continuous a is not admissible, and (ii) the
  D_a integrand is sign-changing with |chi|>1 on ~11% of Omega_F, so no clean closed form is
  in reach. Re-dressing prop:restricted-opt, not a new milestone.

- **A second-variation / convexity statement** (is r~_Q convex in some block parameter):
  no anchor in the existing machinery; the marginal is a first-variation object and the
  paper's Scope explicitly limits to the local first variation. Speculative, no feasible
  cert in hand.

================================================================================
## D. NUMERICAL FACTS ESTABLISHED THIS ROUND (reproducible)
Anchor: held R4 family, Omega_F = {A>B}, meas(Omega_F) = 0.06861 (fork firstvar_04).
- X-root additivity r~_Q = sum_j U(alpha_j): exact to 1.7e-17 (block j3, roots
  {-2.148, 0.574+/-0.369i}; r~_j3 = -1.3e-5 < 0, j3 fires as the paper states).
- {U<0} compact well-region: 0 <= Re <= 0.95, |Im| <= 0.70, min U = -0.035.
- min Re of {U<0} = 0.0 (well TOUCHES the imaginary axis; role-memory "+0.016" does NOT
  reproduce here — boundary is delicate, U(0) ~ -1e-5, U(0+/-0.1i) ~ +9e-5).
- U >= -1e-5 over Re in [-3,0]; U >= +1e-5 over Re in [1,4]; U(-0.05)=+0.0024,
  U(0.05)=-0.0024.
- Far field: U(2)=0.043, U(5)=0.108, U(10)=0.157 (~ meas*log|alpha|), so {U<0} is bounded
  and the obstruction half-planes close at infinity.

================================================================================
## E. BOTTOM LINE FOR THE OUTLINER

There IS one tractable, certifiable, genuinely-new angle: the base-marginal
firing-OBSTRUCTION theorem (Section B) — it proves the paper's heuristic rem:wells,
is SAFE-direction (U>=0, no near-cancellation), is a smooth 1-D quadrature with the
singularity held OFF-contour (NO deep-well blow-up, NO 729 boxes, NO straddle-cell
banking), and gives predictive content (a necessary root-localisation condition a firing
block must satisfy). Its single hard step is honest: the well touches Re=0, so the clean
half-plane statement needs either a strict offset Re <= -delta (cheap, certifiable) or an
exact imaginary-axis lemma U(iy) >= 0 (a real analytic step). Recommend the outliner take
the OFFSET form first (Re <= -delta with explicit delta, plus far-field tail) as the
atomic, certifiable milestone, and treat the sharp-axis version as optional polish.

If the outliner judges "upgrade a Remark to a Proposition" too incremental to clear the
proof-reviewer's genuinely-new bar, then the honest conclusion is: the tractable
deepenings of this paper are essentially mined out, and a further milestone would require
either the lower-side OSS energy program (multi-round, new-bound, out of this task's
scope) or moving to a different constant.
