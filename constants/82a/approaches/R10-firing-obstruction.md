# R10 — Base-marginal firing-OBSTRUCTION / root-localisation theorem (outline)

> **STATUS (R23): outline-reviewed & APPROVED-in-principle; cert PARTIALLY verified; NOT a
> milestone yet.** The outline-reviewer (constants/82a/approaches/R10-firing-obstruction-review.md)
> confirmed the angle clears the milestone bar (novelty orthogonal to thm:generator and
> prop:restricted-opt; upgrades the heuristic rem:wells to a proved root-localisation necessary
> condition), independently verified the X-root additivity identity (~1e-17), sup|chi|=2 exactly
> (so R0=3.5,M=2,R0-M=1.5>0; far-field c2 certified > 0), gap-free coverage of complement(K) by
> {Re<=-delta}∪{|α|>=R0}, true min U over box B = +9.5e-4>0, and the false imaginary-axis lemma
> (so delta=0.02 is forced). Cert firstvar_11_firing_obstruction.py: step 1 (additivity) PASS and
> step 2ii (far-field, c2=+6.99e-3 CERTIFIED at Ns=40000) run in ~30s. **BUT the load-bearing
> step 2i (box-B alpha-cover) did NOT complete in >40 min (R23, killed)** — each alpha-cell is
> O(Ns) and the well-boundary band needs deep refinement while straddle banking over ~12k
> unresolved-membership cells biases U_lo down. So the obstruction is NOT yet reviewer-verified.
> **Open next step:** make box B feasible — vectorise the per-cell loop, or certify U on box B by a
> coarse membership-INDEPENDENT lower bound that avoids straddle banking. Three reviewer must-fixes
> recorded: MF-A (the docstring's "inf_s|chi-α|>=0.47" was FALSE; true ~0.0075 near the grazing
> lobe — corrected in the cert docstring R23); MF-B (demonstrate a completed full run — OPEN);
> MF-C (state cert's Omega_F={A>B} is the paper's candidate-free {A_0>B} anchor).


## 82a
Spec review: **required** (new analytic result: a certified continuum lower bound on
the single-root potential U(alpha), plus a far-field tail lemma — it must be checked
that the chosen framing both certifies cleanly AND carries genuine predictive content
past rem:wells, rem:evidence, eq:additive).

Target to beat: this is a **THEORY milestone**, not a numeric bound. Held bounds stay
FROZEN (upper 0.2538893183, lower 0.2524001332), Status `none`. The bar is the
proof-reviewer's "genuinely new, independently re-derived, re-runnable" milestone bar:
turn the heuristic Remark `rem:wells` ("r~_Q is negative only when a root sits in a
deep well ... the statements above rest on the additivity and the reproduced marginals,
NOT on the geometry") into a PROVED Proposition with predictive content — a necessary
root-localisation condition every firing block must satisfy.

--------------------------------------------------------------------------------
## Setup common to all framings (verified this round, N up to 3.2e6)

Base branch of cor:criterion: an integer block Q enters profitably (fires on the base
side) iff its base marginal
    r~_Q = int_{Omega_F} log|Q(chi(s))| ds  <  0,   Omega_F = {A > B}  (the base active arc),
where chi(s) = z(1-z), z = e^{2 pi i s}, ds = the s-uniform measure (mean over s),
meas(Omega_F) = 0.068607 on the held R4 family.

Two structural facts, both verified this round:

(A) EXACT X-ROOT additivity (finer than the paper's factor-only eq:additive).
    Writing Q(X) = lc * prod_j (X - alpha_j) and using admissibility Q(0)=Q(1)=1 to
    fix the content, the base marginal is additive over the COMPLEX ROOTS:
        r~_Q = sum_j U(alpha_j),     U(alpha) := int_{Omega_F} log|chi(s) - alpha| ds.
    VERIFIED to 2.0e-18 on the degree-3 block j3 = X^3+X^2-2X+1 (roots
    {-2.14790, 0.57395 +/- 0.36899 i}): r~_direct = -4.0264505e-5 = sum_j U(alpha_j).
    [The leading-coefficient term contributes log|lc| * meas(Omega_F); for a monic Q
    it is 0. The builder must state the lc bookkeeping explicitly — see Hard step C.]

(B) The single-root potential U(alpha):
    - U(alpha) >= 0 OUTSIDE a compact well-region W = {U < 0}, and
      U(alpha) -> +infinity as |alpha| -> infinity (U(alpha) ~ meas * log|alpha|).
    - VERIFIED W geometry (held R4 anchor): W is contained in
      {-0.005 < Re(alpha) < 0.98} ∩ {|Im(alpha)| < 0.72}, min U = -0.0378.
    - The well TOUCHES / barely crosses Re = 0:  U(0) ~ -1.1e-5 (stable across
      N=8e5..3.2e6),  U(0.05) = -2.4e-3,  U(-0.005) min over Im = +2.3e-4,
      U(-0.02) min over Im = +9.5e-4,  U(-0.05) = +2.4e-3.
    - Far field (min over circle |alpha|=R):  R=1.5 -> +1.77e-2,  R=2 -> +4.14e-2,
      so W sits inside |alpha| < ~1.2.

THE OBSTRUCTION (the theorem skeleton, framing-independent): if every X-root alpha_j of
an admissible block Q lies in the certified U>=0 region (the complement of a certified
bounding set for W), then r~_Q = sum_j U(alpha_j) >= 0 and Q CANNOT FIRE. Equivalently:
a NECESSARY condition for Q to fire is that at least one X-root sits in the certified
compact well set. This is predictive root-localisation — it tells you WHERE a firing
block's roots must live, which rem:wells only asserts.

WHY this is the SAFE certification direction (and not the bridge-support killer): the
load-bearing inequality is U(alpha) >= 0, a LOWER bound on U on a region where U is
comfortably positive. The integrand log|chi(s) - alpha| is a smooth bounded function of
s for alpha held OFF the contour (alpha in Re <= -delta or |alpha| large; the contour
chi lives in a bounded region near Re in [0,0.25]), so inf_s |chi - alpha| > 0 with a
certified margin — NO singularity, NO deep well, NO straddle-cell banking, NO 729 boxes.
It is a 1-D smooth quadrature in s with a uniform-in-alpha interval bound. This is the
firstvar_09 orientation (a SAFE one-sided enclosure), NOT the firstvar_10 lower-bound-
on-a-near-cancellation orientation that banked -4e-4 of irreducible negative mass.

--------------------------------------------------------------------------------
## Hard-step fact decided this round (gates the framing choice)

The explorer flagged "well touches Re=0; use offset Re<=-delta OR an exact U(iy)>=0
imaginary-axis lemma." I PROBED the axis directly (N=2e6, 3.2e6):

    U(i*0.00) = -1.06e-5,  U(i*0.01) = -9.7e-6,  U(i*0.02) = -6.9e-6,
    U(i*0.05) = +1.3e-5,  U(i*0.10) = +8.7e-5,  U(i*0.30) = +1.3e-3.

=> **The imaginary-axis lemma U(iy) >= 0 is FALSE.** The well genuinely crosses Re=0 in
a small neighbourhood of the origin (U < 0 for |y| < ~0.04). The "exact axis lemma" is
not provable because the statement is not true. This DECISIVELY rules out the
symmetry/axis framing and forces the OFFSET half-plane (Re <= -delta, delta > 0). I have
removed it from the ranking below except as a recorded negative result to put in the doc.

The offset is cheap and robust: at Re = -0.01 already min U over Im = +4.7e-4; at
Re = -0.02, +9.5e-4. So delta = 0.02 gives a ~1e-3 margin with no near-cancellation.

--------------------------------------------------------------------------------
Angle 1 (top pick): OFFSET-HALF-PLANE obstruction + far-field tail + certified well box
  Moves: theory (no numeric bound). Milestone = upgrade rem:wells to a proved Prop.
  Proposition (statement to prove):
    Let delta = 0.02 and R0 = 1.3 (explicit). Then
      (i)  U(alpha) >= +c1 for all alpha with Re(alpha) <= -delta,
      (ii) U(alpha) >= +c2 for all alpha with |alpha| >= R0,
    with explicit certified c1, c2 > 0 (c1 ~ 9e-4, c2 ~ 1e-2). Hence the well set
      W = {U < 0} is contained in the certified compact box
      K = {-delta < Re(alpha) < 0.98} ∩ {|Im(alpha)| < 0.72} ∩ {|alpha| < R0}.
    Consequence (the obstruction): an admissible block Q whose every X-root alpha_j
    satisfies (Re(alpha_j) <= -delta) OR (|alpha_j| >= R0) has r~_Q = sum_j U(alpha_j)
    >= 0 and does not fire on the base branch. Equivalently, a firing admissible block
    must have at least one X-root in the compact set K.
  Skeleton:
    1. X-root additivity r~_Q = sum_j U(alpha_j) + log|lc|*meas — by direct factoring
       of log|Q| over roots and linearity of the integral; lc handled by admissibility.
       (One-line identity; numerically 2e-18, but PROVE it as an exact identity, the
       numerics only confirm.)
    2. (i) Certified LOWER bound U(alpha) >= c1 uniformly over the closed half-plane
       Re(alpha) <= -delta — by an outward-rounded interval quadrature in s with a
       uniform-in-alpha enclosure of log|chi(s) - alpha| on the half-plane. The
       half-plane is unbounded in Im and in |Re|, so split: a finite box
       {-R0 <= Re <= -delta, |Im| <= R0} done by interval arithmetic in BOTH s and
       alpha (2-D alpha-cover, adaptive only in alpha, NOT in s — no deep wells), and
       the unbounded part folded into step 3.
    3. (ii) Far-field tail U(alpha) >= meas*log|alpha| - C for |alpha| >= R0 — by a
       Jensen / sub-mean-value estimate: log|chi(s)-alpha| >= log(|alpha| - sup_s|chi|)
       pointwise once |alpha| > sup_s|chi| (= max |chi| on the unit circle, a clean
       constant), integrated over Omega_F gives meas*log(|alpha| - M). Choose R0 so the
       RHS is >= c2 > 0. This closes BOTH unbounded directions (large |Re| and large
       |Im|) analytically with one inequality — no interval cover at infinity.
    4. Assemble: (i)+(ii) => W ⊆ K (compact, explicit). Print K's certified box. The
       obstruction is then immediate from step 1.
  Hard step: **the uniform-in-alpha certified lower bound U(alpha) >= c1 on the finite
    box {-R0 <= Re <= -delta, |Im| <= R0} (step 2)** — because it requires a rigorous
    enclosure of int_s log|chi(s)-alpha| ds that is valid for a CONTINUUM of alpha, not
    a grid. The mechanism that makes it tractable and safe: for alpha in this box,
    inf_s |chi(s) - alpha| >= delta - (something) > 0 is bounded below by an explicit
    constant (the contour chi has Re(chi) >= 0 region structure; alpha has Re <= -delta,
    so |chi - alpha| >= |Re(chi) - Re(alpha)| >= delta where Re(chi) >= 0, and the
    finite Im range is handled by the box cover), so log|chi - alpha| is a BOUNDED
    Lipschitz function of alpha with NO singularity — its enclosure over an alpha-cell
    is controlled by the cell width times an explicit Lipschitz/derivative bound, and
    U is monotone-increasing as alpha moves left/up away from W, giving the lower bound
    at the cell's worst corner. (The off-contour separation is the whole game: it is why
    this is a smooth bounded quadrature and not the deep-well blow-up that killed
    firstvar_10.)
  Check (what the builder runs to certify): one new firstvar_11_obstruction.py that
    (a) reproduces X-root additivity on j3 (and 1-2 more blocks) to ~1e-15 [confirms
        step 1 numerically; the PROOF is the identity];
    (b) outward-rounded interval cover of {-1.3 <= Re <= -0.02, |Im| <= 1.3}, certifying
        U(alpha) >= c1 > 0 on every alpha-cell (adaptive bisection in alpha only, refine
        until the per-cell lower bound is > 0; report any unresolved cell as FAIL);
    (c) evaluates the far-field constant M = sup_s |chi(s)| (outward-rounded) and prints
        R0 with meas*log(R0 - M) >= c2 > 0;
    (d) prints the certified W bounding box K;
    (e) tamper mode: target c1 := some value above the true min -> FAIL with the
        violating cell resolved (rules out a grid fallback), exactly like firstvar_09.
    Cost: 1-D quadrature in s (fixed, no adaptive s-bisection) times a modest 2-D alpha
    cover — minutes, not the ~17h full-box regime. Feasible and reviewable.

Angle 2: RECTANGLE/STRIP obstruction (Re <= -delta only, drop the disk, keep tail)
  A leaner variant of Angle 1: state ONLY the half-plane obstruction "every root with
  Re(alpha_j) <= -delta contributes U >= 0" plus the far-field tail, and report the well
  box K as computational data (not the load-bearing claim). Predictive content: a firing
  block cannot have ALL roots in Re <= -delta or far out — weaker, but the certificate is
  smaller (the finite box in step 2 shrinks to {-M' <= Re <= -delta, |Im| <= bound}
  where the tail already covers |Im| large). Hard step: same as Angle 1 step 2 but on a
  smaller box. Check: same cert minus the disk cover. Use this as the FALLBACK if the
  full compact-box certification (Angle 1 step 4) proves loose at the W boundary near
  Re=0 (it should not — min U at Re=-0.005 is +2.3e-4 — but delta=0.02 is the safe choice).
  Note: by the X <-> 1-X near-symmetry of the construction the same obstruction should
  hold mirrored on Re >= 1+delta; the builder may add it cheaply (another box cover) to
  double the predictive reach, but must VERIFY the symmetry numerically first (do NOT
  assume it — the anchor family is not exactly X<->1-X symmetric).

Angle 3 (RECORDED NEGATIVE RESULT, not a milestone on its own): exact imaginary-axis
  lemma U(iy) >= 0. **REFUTED this round**: U(iy) < 0 for |y| < ~0.04 (U(0) = -1.1e-5).
  The well crosses the axis; the clean axis statement is false. Document this in the
  approach doc as the reason the offset framing is mandatory (it sharpens rem:wells:
  the wells are not confined to a half-plane, they straddle Re=0 in a tiny neighbourhood
  of the origin). Do NOT spend builder compute trying to prove a false statement.

--------------------------------------------------------------------------------
## Ranking

1. **Angle 1 (offset half-plane + far-field tail + certified compact well box).** Best
   balance of certifiability and predictive content. It is the SAFE direction (U >= 0
   lower bound on a region where U is comfortably positive, off-contour, smooth — no
   near-cancellation, no deep well, no 729 boxes), the hard step is a bounded
   analytic+interval task with the singularity held off-contour, and it delivers the
   full root-localisation statement (W ⊆ explicit compact K) that makes rem:wells a
   theorem. The far-field tail (step 3) is a one-inequality Jensen estimate that closes
   the unbounded part for free, which is what makes the compact-box claim affordable.

2. **Angle 2 (strip-only)** is the fallback if, against the probes, the compact-box
   assembly is loose near the W boundary; it sacrifices the "compact K" punch line but
   keeps a true, certified, predictive half-plane obstruction. Switch to it only if
   Angle 1's disk/box cover refuses to close.

3. **Angle 3** is not pursued — refuted numerically; record it as the negative result
   that motivates the offset.

## Honest scope / risk the outline-reviewer must weigh
- NOVELTY is MEDIUM: this upgrades an existing Remark (rem:wells) to a Proposition. The
  reviewer should confirm that "proved root-localisation necessary condition with an
  explicit certified compact well set + the exact X-root additivity identity" clears the
  genuinely-new bar (it is orthogonal to thm:generator and prop:restricted-opt, and adds
  the geometry the paper explicitly disclaims it has — "NOT on the geometry").
- The delicate boundary at Re=0 is HANDLED by the offset delta=0.02 (margin ~1e-3),
  decided after direct probing; the false axis-lemma is recorded, not attempted.
- The lc/content bookkeeping in step 1 must be stated exactly (admissibility Q(0)=Q(1)=1
  fixes it); a monic vs non-monic slip would void additivity.
- This is NOT a new bound; held bounds and Status stay frozen.
