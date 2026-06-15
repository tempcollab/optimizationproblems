# R3 — Bridge-support selection: the criterion SELECTS the deg-4 factor P4

Status: OUTLINE (round 3). Awaiting outline-reviewer, then proof-builder.
Spec review: REQUIRED (new finite-comparison frame, new certificate, new paper Prop +
table; non-trivial admissible-family definition that must be defensible to a referee).

## 82a
Spec review: required
Target to beat: NO numeric bound. This is a THEORY milestone (run goal already met at 21).
The "target" is a NEW reviewer-certifiable generative principle past `rem:gen-scope`:
the first-variation criterion SELECTS the bridge SUPPORT (the deg-4 multiplier P4),
the SUPPORT analogue of R2's EXPONENT-optimality (prop:restricted-opt). Held bounds stay
FROZEN (upper 0.2538893183, lower 0.2524001332); Status stays `none`.

## What the milestone claims (the new Proposition)

Fix the bridge CORE `P1^5 P2^5` (= chi^5, the contour coordinate to the 5th power, a clean
structural fact worth stating: P1=X, P2=1-X => P1·P2 = X(1-X) = chi) and the tail P8. Vary
ONLY the remaining degree-4 monic multiplier `d`, forming
    R(d) = pp(Q1 - P1^5 P2^5 · d · P8),  which stays deg-28 iff deg(core·d·P8)=26, i.e. deg d = 4.
Among a STATED FINITE admissible family of such `d`, the first-variation firing margin
r_{R(d)}(Omega_F) is MAXIMISED (most negative) at d = P4 = (1,-2,4,-3,1). I.e. P4 is the
firing-optimal admissible deg-4 bridge support. This is the bridge-SUPPORT half of
rem:gen-scope, leaving only the SEED choice (Angle 2 of the explorer, R7-blocked) as
future work.

NUMERICS (explorer's full sweep, anchor Omega_F = record\{Q1}, reproduces R0's margin
r_R0 = -0.03560 exactly):
    #1  d = P4 = (1,-2,4,-3,1)   r_R = -0.03560   UNIQUE maximizer over 1458 candidates
    #2  d = (1,-1,4,-3,1)        r_R = -0.03490   runner-up, gap +7.0e-4
    #3  d = (1,-3,4,-3,1)        r_R = -0.03442   gap +1.18e-3
The runner-ups are GENUINE admissible competitors (verified this round: each yields a
deg-28, content-1, squarefree, coprime-to-Q1 sibling with R(0)=R(1)=1 — same admissibility
filter as P4), so the optimality genuinely discriminates. Tightest cert gap ~7e-4 →
integrated difference D ~ e-4. R2 cleared D_4^hi = -3.12e-4 by the SAME machinery, so this
is feasible but the tightest near-miss sets the difficulty.

LITERATURE GROUNDING (do not invent the ansatz): cite Doche [Doc01b]'s own design
principle — the base set {P1,P2,P4,P6,P8} is "forced by the search of the minimum" and the
perturbing factors are chosen for small height AND because "a product of the P_i divides
Q1-Q2" (the resultant heuristic). So drawing the bridge support from the base factors
{P1,P2,P4,P6,P8} is DOCHE's principle, not ours. The admissible family below is the
deg-4 multipliers consistent with that principle and with degree preservation.

---

## Angle 1 (TOP PICK): finite signed-difference-enclosure comparison D(d) > 0

Moves: nothing numerically. Establishes RESTRICTED firing-optimality of P4 over the stated
finite admissible deg-4 family. Mirrors prop:restricted-opt exactly but for SUPPORT.

Skeleton:
  1. DEFINE the admissible family A (finite, explicit, exact sympy filter). The natural
     family: monic deg-4 integer multipliers
         d(X) = X^4 + c3 X^3 + c2 X^2 + c1 X + c0,
     with the admissibility constraints that (i) make R(d) admissible and (ii) keep it a
     genuine competitor of the same TYPE as P4. Proposed exact constraints:
         - monic, degree exactly 4 (preserves deg R = 28, by prop:degfloor count);
         - unit constant term c0 = +1 (so R(d)(0)=1 is forceable / Doche normalization;
           P4 has c0=+1);
         - |c1|,|c2|,|c3| <= 4 (the explorer's height box; P4=(c3,c2,c1,c0)=(-2,4,-3,1)
           sits strictly inside, so the box is not gerrymandered around P4);
         - R(d) = pp(Q1 - chi^5 d P8) is ADMISSIBLE: deg 28, content 1, squarefree,
           coprime to Q1, R(d)(0)=R(d)(1)=1  (exact sympy gcd/eval checks).
     This is a FINITE set: |c1|,|c2|,|c3| in {-4..4} (9 each), c0=+1, monic => 9^3 = 729
     raw candidates (the explorer's 1458 counts c0=±1; restrict to c0=+1, the
     Doche-normalized sign, halving it and matching R0). The admissibility filter then
     prunes to the genuine competitors. — by EXACT sympy enumeration (firstvar_10 setup).
  2. COARSE PRE-SCREEN: compute a CHEAP rigorous LOWER bound on each competitor's margin
     gap to P4 (e.g. a coarse-grid signed-difference enclosure, or a crude per-cell bound).
     Every competitor whose margin is provably > P4's margin + 3e-3 is CLEARED coarsely (it
     fires strictly weaker by a comfortable margin) and needs NO tight cert. The explorer's
     sweep shows only a handful (~the top few: #2 at +7e-4, #3 at +1.18e-3, and any others
     within ~3e-3) survive to the tight stage. — by coarse enclosure, batched.
  3. TIGHT CERT for each surviving near-miss d: certify
         D(d) := r_{R(d)}(Omega_F) - r_{R(P4)}(Omega_F)
               = (1/28) ∫_{Omega_F} log |R(d)/R(P4)| ds  > 0
     by the SAME outward-rounded asymmetric signed-difference enclosure as firstvar_09,
     with Q* := R(P4) the FIXED reference and R := R(d). Both deg 28 on the SAME anchor
     Omega_F, shared normalizer 1/28, so eq:diff-id transfers VERBATIM (just Q*:=R(P4)).
     Here we want D(d) > 0 (competitor fires WEAKER, larger/less-negative margin), so we
     certify a rigorous outward-rounded LOWER bound D(d)^lo > 0 — the SIGN-FLIPPED twin of
     firstvar_09's upper-bound D_a^hi < 0. The asymmetric accumulation flips: on a
     certainly-IN cell bank w·(int_lo); on a STRADDLE cell bank w·min(0,int_lo) (only the
     negative part of a could-be-out cell may reduce a lower bound); certainly-OUT cells
     contribute 0. Adaptive well bisection on the shared near-root cells (R(d), R(P4) share
     most roots — milder wells than R/Q1, already cleared in firstvar_08). — by the
     firstvar_09 machinery with the sign convention reversed.
  4. CHAIN: every admissible d != P4 has D(d) > 0 (coarsely or tightly), so r_{R(P4)} is
     strictly the most negative => P4 is firing-optimal over A. — by finite conjunction.
  5. PAPER: new subsection + Proposition prop:support-opt under sec:generator, mirroring
     prop:restricted-opt; a candidate-margin table (top few competitors with their certified
     D(d)^lo); a firstvar_10 row on tab:verify; a sentence citing Doche [Doc01b] for why
     the support is drawn from {P_i} and noting P1·P2 = chi. State the HONEST scope: optimal
     over the STATED FINITE admissible deg-4 family, NOT over all Z[X]. — paper edit.

Hard step: certifying D(d_#2)^lo > 0 for the tightest near-miss d_#2 = (1,-1,4,-3,1),
true gap ~7e-4 => integrated D ~ e-4, sign-changing integrand.
  Mechanism: eq:diff-id with Q*:=R(P4) is EXACT (equal degree, shared normalizer, same
  Omega_F), so the gap IS the signed integral; the sign-flipped asymmetric accumulation of
  firstvar_09 (banking negative help only on certainly-IN cells, positive-discarding the
  rest) gives a rigorous LOWER bound that converges to the true +e-4 under adaptive
  bisection because R(d)/R(P4) shares most roots => wells are mild (boundary band cancels
  ~3e-7, as in R2). R2 cleared the symmetric-sign version at -3.12e-4; +7e-4 is LOOSER, so
  feasible — but it is the binding cell and the cert must show D(d_#2)^lo comfortably > 0.

Check (builder runs / reviewer reproduces):
  - firstvar_10_support_optimality.py: (i) exact sympy enumeration of A and its admissibility
    filter (print |A|, list survivors of the coarse screen); (ii) coarse pre-screen clearing
    all but the near-misses; (iii) tight D(d)^lo > 0 for each near-miss (outward-rounded,
    adaptive bisection, m_R>0 root-freeness gate on BOTH R(d), R(P4), 0 unresolved cells);
    (iv) float cross-check reproducing the explorer's margin sweep and r_R0=-0.03560;
    (v) tamper checks: a fabricated D(d)^lo <= 0 must FAIL the PASS; perturbing the
    admissibility filter to admit a non-competitor must be rejected; the coarse screen must
    not silently skip a near-miss (assert every d with float-gap < 3e-3 reaches the tight
    stage).
  - Reviewer re-derives eq:diff-id with Q*:=R(P4) from scratch (sympy/Horner at high N),
    confirms the sign-flip is sound, reproduces D(d_#2)^lo > 0.

---

## Angle 2 (FALLBACK): per-competitor two-sided margin enclosures, ordered by non-overlap

Moves: same milestone, weaker frame. For each admissible d compute a rigorous two-sided
margin enclosure [r^lo(d), r^hi(d)] and certify r^hi(P4) < r^lo(d) (P4's whole interval
below the competitor's). Same conclusion via non-overlap instead of a difference.
Hard step: the half-width budget. The P4–#2 gap is ~7e-4; a two-sided per-margin enclosure
must resolve the Omega_F active-set boundary to ~3.5e-4 TWICE (P4 and #2 separately) — and
unlike the difference, the boundary straddle uncertainty does NOT cancel (R2 found ~3e-7
cancellation in the difference vs a fresh straddle budget per absolute margin). So this is
strictly more fragile than Angle 1 for the tight pair.
Check: a two-sided variant of firstvar_09's margin accumulation; PASS iff intervals
disjoint with P4 below. Use ONLY if Angle 1's coarse screen mis-sizes and the difference
cert is borderline on a near-miss.

---

## Angle 3 (BUNDLED FREE FIX, NOT a milestone): honest-numbers prose fix

Moves: nothing. Fixes a descriptive prose slip flagged in run_state NEXT and by the
explorer. paper l.923 (prop:restricted-opt proof) AND firstvar_09's docstring say "about
79% of the mass is negative" for a=4; the true figure is ~64% (35.7% positive). Non-load-
bearing, affects no bound, referee hygiene only. Fold into the Angle-1 round for free — it
touches the same Proposition family and certificate the builder is already editing. This
logs NO milestone on its own (the reviewer only logs genuinely new advances); it ships as a
correctness nit alongside the Angle-1 milestone.
Check: builder corrects both the .tex line and the firstvar_09 docstring; reviewer confirms
the corrected figure against a fresh sign-count of the a=4 integrand on Omega_F.

---

## Ranking

1. **Angle 1 (signed-difference-enclosure D(d) > 0)** — TOP. It reuses the EXACT machinery
   the reviewer already APPROVED in firstvar_09 (eq:diff-id, asymmetric outward-rounded
   accumulation, adaptive well bisection, m_R>0 gate), only with Q*:=R(P4) fixed as the
   reference and the sign of the bound flipped (lower-bound D > 0 instead of upper-bound
   D < 0). The boundary uncertainty CANCELS in the difference (the lesson of R2 / role
   memory), which is exactly why the difference frame beats the absolute-margin frame for
   the tight ~7e-4 near-miss. It mirrors the "restricted" framing the reviewer accepted in
   R2, so it is referee-defensible as stated.
2. **Angle 2 (non-overlapping margin intervals)** — FALLBACK only. Cleaner to state but the
   straddle budget does not cancel, so the tight pair is harder to certify. Switch to it
   only if Angle 1's near-miss cert comes out borderline AND the difference frame somehow
   fails (unlikely given R2 cleared a tighter gap).
3. **Angle 3 (prose fix)** — bundle into the Angle-1 round for free; not a standalone
   milestone.

## Key risks the builder/reviewer must watch (do NOT trip the recorded dead ends)
- NO pointwise subordination: |chi| > 1 on ~11% of Omega_F, the D(d) integrand is
  sign-changing. Ordering MUST use the asymmetric signed-difference enclosure outward-
  rounded through the subtraction (vv.rsub), never a subordination inequality or a per-d
  absolute margin for the tight pair (role memory + run_state Rules).
- NO unqualified optimality: state RESTRICTED to the stated finite admissible deg-4 family,
  never "P4 optimal over all Z[X]". Mirror the rem:a6 honest-scope framing.
- WITD/equilibrium reading is DEAD — do not invoke it as the "reason" P4 is selected.
- The admissible family A MUST be defined BEFORE seeing the margins (the height box
  |c_i|<=4, c0=+1, monic, R(d) admissible) so the family is not gerrymandered to make P4
  win — defensibility hinges on this. P4 sits strictly inside the box, which is the honest
  signal.
- Held bounds stay frozen; Status stays `none`. This is a theory-quality milestone.

## Pointers
- Machinery to fork: constants/82a/certificate/firstvar_09_restricted_optimality.py
  (certify_diff -> certify_diff_support with Q*:=R(P4), D^lo>0 sign flip).
- Firing harness / anchor Omega_F: firstvar_08_sibling_generator.py.
- Paper anchors: sec:generator, prop:restricted-opt (the model to mirror), eq:diff-id,
  lem:transfer, tab:degfloor, tab:verify, rem:gen-scope (the residual this shrinks).
- Prior frame: constants/82a/approaches/R2-restricted-firing-optimality.md.
