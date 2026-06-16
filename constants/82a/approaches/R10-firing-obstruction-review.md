# Outline review — R10/R11 base-marginal firing-OBSTRUCTION / root-localisation

Reviewed: `approaches/R10-firing-obstruction.md` (Angle 1, top pick) and the already-written
cert `certificate/firstvar_11_firing_obstruction.py`. The outline was marked
"Spec review: required" and the review had not been done before the builder proceeded; this is
that review, done now, after the build addressed the prior R10 must-fixes (MF1 R0/M, MF2
separation-not-from-half-plane, MF3 monic/lc bookkeeping).

VERDICT: **CHANGES REQUESTED** (technique is sound and verified; two cosmetic-but-misleading
prose defects and one feasibility/printed-margin item must be nailed down before the cert run
is handed to the proof-reviewer). The angle CLEARS the milestone bar — the builder may proceed
to a full cert run; no re-outline needed.

--------------------------------------------------------------------------------
## What I verified independently (N up to 2e6)

1. **X-root additivity (Step 1)** — `r~_Q = log|lc|*meas + sum_j U(alpha_j)`,
   `U(alpha)=int_{A>B} log|chi-alpha| ds`. Reproduced on three monic blocks (j3, X^4-X^3-X+1,
   X^2-X+1): |diff| = 2.4e-17, 1.4e-16, 1.2e-17. The identity is exact (log of a product +
   linearity of the integral); the numerics only confirm. **SOUND, no leap.** The lc bookkeeping
   (monic => log|lc|=0; a |lc|<1 fractional content would add negative mass and is excluded by
   hypothesis) is stated correctly in the cert docstring (MF3 satisfied).

2. **Far-field constant (Step 3 / MF1)** — sup|chi| = 2.0000 exactly on the full circle,
   1.9724 over Omega_F. With M=2, R0=3.5 gives R0-M = 1.5 > 0, c2 = meas*log(1.5) ≈ 0.0686*0.405
   ≈ 2.78e-2 > 0. **MF1 correctly fixed** — the old R0=1.3 (log arg negative) is gone; the cert
   uses R0=3.5. The pointwise Jensen floor log|chi-alpha| >= log(|alpha|-M) is valid for
   |alpha| >= R0 > M. **SOUND.**

3. **Coverage (boundary/gap question)** — {Re<=-delta} UNION {|alpha|>=R0} covers complement(K)
   where K = {Re>=-delta} INTERSECT {|alpha|<=R0}. The gap I worried about in R10
   (Re<=-delta but |Im|>R0) is closed: if |Im|>R0 then |alpha|>=|Im|>R0 -> far field; if
   Re<-R0 then |alpha|>=|Re|>R0 -> far field. Box B = {-R0<=Re<=-delta, |Im|<=R0} catches the
   rest. 2e6-point random check: **0 uncovered points.** complement(K) subset of certified
   region by inclusion. **NO GAP. SOUND.**

4. **Box-B positivity (Step 2(i), the load-bearing step)** — true min U over box B = **+9.50e-4**,
   attained at the well-boundary corner Re=-0.02, Im≈0 (the offset edge closest to the well).
   c1 > 0 holds with ~1e-3 margin (100x the E3 threshold 1e-5). **SOUND.**

5. **Imaginary-axis lemma is FALSE (recorded negative result, Angle 3)** — U(i*0)≈-1.1e-5, the
   well crosses Re=0. The offset delta=0.02 is therefore FORCED, not a free choice; at Re=-0.02
   min U over Im is +9.5e-4. Framing handled correctly; do not attempt to prove the false lemma.
   **Correct.**

--------------------------------------------------------------------------------
## MUST-FIX (close while finalising the cert; none require a re-outline)

**MF-A (load-bearing prose is FALSE — the "0.47" separation figure).**
The cert docstring line 89 and the outline (Hard-step paragraph, ~line 120-130) both claim
`inf_s|chi-alpha| is certified >= ~0.47 > 0` for alpha in box B. **This is wrong.** chi=z(1-z)
traces a lemniscate reaching Re(chi)≈-1.73, so alpha in box B near Re≈-1.6, Im≈1.1 sit very
close to the contour: I measured the WORST separation inf_{Omega_F}|chi-alpha| over box B =
**0.0075** (at alpha≈-1.626+1.108i), not 0.47. The bound is STILL VALID (separation > 0, no
actual singularity; U there = +0.051, comfortably positive because the grazing s-point is a
single bounded-negative integrand swamped by the far bulk) — but the explanatory number must be
corrected, or the proof-reviewer will (rightly) reject the docstring as not matching the printed
`min_sep`. **Fix:** replace "0.47" with the true certified value (the cert's printed
`min certified separation`, ~0.007) and note that small separation occurs at the contour-grazing
alpha (Re≈-1.6), which is FAR from the well, so U stays large there — the well-boundary corner
(Re=-0.02, sep≈0.02) is where U is actually minimised. This also dispels the false impression
that "separation 0.47 => trivially bounded"; the genuine point is that separation > 0 everywhere
(certified per-cell by the |chi-alpha|^2 enclosure, MF2) AND the small-separation region is
decoupled from the small-U region.

**MF-B (the "no straddle banking / minutes not 17h" claim must be demonstrated, not asserted).**
The outline (lines 57-63, 142-143) and docstring (lines 86-92) argue this is the SAFE firstvar_09
direction with "NO straddle banking, minutes not 17h". That is plausible (the integrand is
bounded since alpha is off-contour, unlike firstvar_10's on-contour blow-up), and I confirmed the
worst per-point integrand is a bounded ~-0.75 (not the -4e-4-banked irreducible mass of
firstvar_10). BUT: the cert DOES still bank negative half-log on s-straddle cells (lines 110-113,
295), and near the contour-grazing alpha (sep 0.007 => per-cell half-log floor ~ -4.9) the
alpha-cover must refine. Both my dev-resolution cert runs (Ns=20000, n0=6 and n0=8) produced NO
output after several minutes — slower than the outline's "minutes" promise. **Fix:** the builder
must (i) run the full cert to completion and confirm PASS with 0 unresolved alpha-cells and the
printed wall-time, (ii) confirm the contour-grazing band (Re≈-1.6, Im≈1.1) resolves without
hitting max_depth, and (iii) put the ACTUAL wall-time in the docstring/banner, not "minutes". If
the grazing band fails to resolve, fall back to Angle 2 (strip-only, smaller box) per the
outline's own ranking. NOTE per the run_state Rules: builders must NOT launch a blocking full
run (idle watchdog) — the ORCHESTRATOR runs the heavy cert via run_in_background and hands the
completed output to the builder.

**MF-C (state the membership region matches the paper's `{A_0 > B}`).**
The cert builds Omega_F = {A>B} from `firstvar_04.AB_arrays(R4,.)`, where A is the candidate-FREE
base value (P1..P8, j3=Q7, j9=Q8 at the fitted exponents — NO candidate block). This IS the
paper's candidate-free anchor `{A_0 > B}` (rem:evidence, eq:additive context). Confirm this
identification explicitly in the cert docstring and the paper statement so the proof-reviewer
sees the obstruction is scored at the same anchor as rem:wells/rem:evidence, not a different arc.
meas(Omega_F)=0.06861 reproduced — matches the outline. (Minor.)

--------------------------------------------------------------------------------
## Novelty / scope (clears the bar)

This upgrades the HEURISTIC rem:wells ("r~_Q negative only when a root sits in a deep well ...
the statements rest on additivity and reproduced marginals, NOT on the geometry") into a PROVED
necessary condition: a firing admissible monic block must have at least one X-root in an explicit
compact set K = {Re>=-delta} INTERSECT {|alpha|<=R0}. This is **genuinely new and orthogonal** to
the two existing verified results:
- thm:generator CONSTRUCTS the R0/R2 sibling family from a seed — a sufficiency/construction
  result on a specific family;
- prop:restricted-opt SELECTS the bridge exponent a=5 among degree-preserving siblings — an
  optimality result within that family;
- this OBSTRUCTION is a NECESSARY condition on ALL admissible monic blocks (root localisation),
  adding the geometry the paper explicitly disclaims ("NOT on the geometry"). It is a genuine
  predictive statement (WHERE roots must live), not a restatement of the remark.

The exact X-root additivity identity (finer than the paper's factor-only eq:additive) is itself
a small new contribution. Together this clears the "genuinely new, independently re-derived,
re-runnable" milestone bar. **Novelty: MEDIUM but real.** This is a THEORY milestone: held bounds
stay FROZEN (upper 0.2538893183, lower 0.2524001332), Status `none`.

--------------------------------------------------------------------------------
## Not blockers (noted)
- E1/E2/E3 tamper design mirrors firstvar_09 (alpha-on-contour -> sep~0 reject; false target ->
  cover fails; c1 margin > 1e-5). Reasonable; the proof-reviewer will re-run them.
- delta=0.02 with margin ~1e-3 is the correct conservative choice given the well grazes Re=0.
- The X<->1-X mirrored obstruction (Angle 2 note) is OPTIONAL and must be verified, not assumed
  (the anchor family is not exactly symmetric). Do not include it unless separately checked.

## One-line summary
Technique is correct and every load-bearing fact (additivity 1e-17, sup|chi|=2, min U over box B
= +9.5e-4 > 0, coverage gap-free, far-field floor +2.8e-2) is independently verified; the angle
clears the genuinely-new bar. CHANGES REQUESTED only to (A) fix the FALSE "0.47" separation
figure to the true ~0.007 in docstring+outline, (B) prove the feasibility/no-blow-up claim by a
completed full run with 0 unresolved cells and the real wall-time, (C) state the {A_0>B}
anchor identification. No re-outline; build/finalise on Angle 1.
