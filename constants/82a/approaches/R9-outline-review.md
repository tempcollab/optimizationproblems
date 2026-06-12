# R9 outline review — UNIFIED first-variation cross-term lemma (82a UPPER, structural)

Reviewer: outline-reviewer, Round 9. Target: STRUCTURAL milestone (no numeric break).
Outline under review: `approaches/R9-unified-firstvar-outline.md`, Angle 1.

## Verdict: CHANGES REQUESTED

The angle is sound and certifiable. The hard step (the tie case) has a correct,
explicitly-stated mechanism, and I reproduced it numerically (toy tie-case: right-FD of
Phi/D matches `(r D - Phi0*max(sA,sB))/D^2` to 1e-8 while the left-FD genuinely differs —
the one-sided kink is real). Two issues must be nailed down in the write-up before the
milestone is bankable; neither blocks the builder from starting. Details below, keyed to
the four spec-review checks.

---

## CHECK 1 — the TIE case (one-sided Danskin on the outer max). PASS, with a caveat.

The outline states the tie correctly and as ONE-SIDED. Step 3 invokes: a finite max of
affine functions is convex piecewise-linear; convex functions on R have one-sided
derivatives everywhere; for a finite max the right-derivative is the max of the
right-derivatives over the ACTIVE index set (Rockafellar Thm 23.x / Danskin). At a tie
both args are active, so `(dD/dq)^+ = max(arg_A'(0), arg_B'(0))`. This is exactly right and
I verified it numerically (toy: tie at q=0, slopes sA=8 > sB=3; right-deriv of D = sA,
left = sB; the quotient Phi/D inherits a one-sided kink). The outline is honest that
`log h` need NOT be two-sided differentiable at a tie (point (a)) — good, this is the
single most common way such a lemma goes wrong and the outline pre-empts it.

CAVEAT to enforce in the build: the "active index set" reasoning is for the RIGHT
derivative `q -> 0+` ONLY because the perturbation is `q >= 0` (block enters with
nonnegative exponent — stated in §The object). The builder must NOT silently quote a
two-sided value. At the tie the LEFT derivative would pick `min(arg_A', arg_B')` (the
other branch becomes active for q<0), so the kink is real and the firing test is the RIGHT
derivative. Since admissible perturbations are `q >= 0`, the right derivative is the only
physically meaningful one and the "firing iff d+ < 0" criterion is the correct test —
state this explicitly so no reader infers differentiability.

## CHECK 2 — quotient rule composing one-sided Danskin(Phi) with one-sided D'. PASS.

`d+(Phi/D) = (Phi+' D - Phi D+')/D^2` is valid because: (i) D >= 56 > 0 bounded away from
zero, so 1/D is right-differentiable wherever D is; (ii) Phi is right-differentiable at 0
by the R8 DCT lemma (INPUT, already verified — I did not re-check it); (iii) the product of
two right-differentiable functions is right-differentiable, and the standard one-sided
quotient rule holds with no extra hypothesis beyond nonzero denominator. Phi+'(0) and
D+'(0) are both established (Phi+' via R8 DCT; D+' via the affine args + convex-max fact).
No regime where the composition fails: Phi+' exists in ALL regimes (it depends only on the
inner max(A,B), not on which arg attains the outer D — the "decoupling" the outline names
in Step 2 is correct and is the actual content of the unification). I reproduced the
composition on the toy and it matched to 1e-8.

One thing the builder MUST confirm while building (the outline flags it as point (b) but it
is load-bearing, not optional): re-read the R8 DCT proof and confirm it uses ONLY (a) the
inner-max 1-Lipschitz domination by |log|Q.chi|| in L^1 and (b) finiteness of the kink set
K={A_0=B} — NEITHER of which references which arg attains the OUTER D. From
`R8-firstvar-rigorous.md` Steps 2-5 this is plainly true (D enters only as the q-constant
or affine normalizer, never inside Phi=int max). This is a 5-minute read-and-confirm, but
it is the hinge of the whole unification, so it must appear in the write-up as an explicit
"the R8 lemma's hypotheses are regime-independent" paragraph, not be assumed.

## CHECK 3 — the A-attaining cross-term has NO live family. THIS IS THE ISSUE TO FIX.

This is where the outline is weakest and the write-up must be disciplined.

The held family has arg_A=61.66 < arg_B=72.00 (regime II). So regime I (A attains D) and
in particular the A-ATTAINING cross-term `-(log h)deg(Q)/D` for an A-side block have NO
on-disk family to finite-difference. The outline (Step 4(I), Scope bullet 1) is HONEST that
this case is "established by the SAME envelope structure, NOT by a numeric FD check." That
honesty is the right instinct — but as written it risks reading as "asserted by analogy,"
which is an unproven leap dressed as a corollary.

It is in fact NOT a leap, and the fix is to make the derivation self-contained rather than
lean on "same structure":

- The A-attaining cross-term is NOT a separate empirical fact needing its own FD. It is the
  MECHANICAL output of the SAME quotient rule (Check 2) with the SAME convex-max
  right-derivative (Check 1), under the index swap "A active in D instead of B." Concretely:
  in regime I with an A-side block, `(dD/dq)^+ = deg(Q)` (arg_A affine, slope deg(Q),
  attains D), Phi+'(0) = int_{A_0>B} log|Q.chi| ds (R8 DCT, A-side), and the quotient rule
  gives `(1/D)[int_{A_0>B} log|Q| - (log h)deg(Q)]`. This is the B-branch m_B with A<->B
  swapped — it is the SAME one derivation specialized, not a new claim.

- REQUIRED FIX: the builder must DERIVE the A-attaining cross-term as a line of the unified
  quotient-rule statement (zeroing/activating the indicator), and the toy tie-check
  (proposed in the outline) must be EXTENDED to also exercise a NON-tie regime-I config
  (a0_A > a0_B, A-side slope on D) so the A-attaining cross-term formula is numerically
  isolated and confirmed on a toy — exactly as the tie is. The toy needs no live A-dominant
  family; it just needs `D(q)=max(a0_A + deg*q, a0_B)` with a0_A > a0_B. This converts "same
  envelope structure" from an assertion into a checked corollary of the unified rule. Do NOT
  ship the A-attaining branch backed only by prose.

- The Scope must continue to state plainly that the A-attaining cross-term is NOT exercised
  on a LIVE Doche family (no A-dominant family exists on disk); the toy check certifies the
  FORMULA, the live engines certify the two regime-II corollaries. Keep that distinction
  sharp — it is the difference between an honest milestone and an overclaim.

## CHECK 4 — wrong technique / circularity / missing cases.

- No circularity: the unified lemma INVOKES the R8 DCT lemma and the B-branch derivation as
  cited inputs and does not re-prove them. The only new derivation is the outer-max
  right-derivative + tie, which rests on convex analysis (Rockafellar), independent of the
  inputs. Clean.
- Both one-sided directions: the outline covers `q -> 0+` (the admissible direction) and is
  explicit that the tie is one-sided. It does NOT need `q -> 0-` since exponents are >= 0,
  but the write-up should SAY so (one sentence: "admissible perturbations have q >= 0, so
  only the right derivative is needed; the left derivative differs at a tie, confirming the
  kink"). Otherwise a reader wonders whether the omitted direction hides a gap.
- a.e.-differentiability of arg_A, arg_B in q: arg_A, arg_B are AFFINE in q (Doche §4
  D-formula, PDF-verified R2/R4/R7), hence everywhere differentiable in q; D is their max,
  hence everywhere right-differentiable. No a.e. subtlety — the affineness is exact, cite
  Doc01a §4 and do not re-derive (outline point (d), correct).
- Active-index set at the tie is the FULL {A,B} (outline point (c)) — correct, must not drop
  one. In regimes I/II the active set is a singleton. The toy extension (Check 3) should
  cover all three: singleton-A (regime I), singleton-B (regime II), and tie (both).

## What the builder runs to certify (sufficient, with the Check-3 addition):

1. Re-run the two existing engines UNCHANGED as corollary checks (NOT as the milestone):
   `verify_firstvar_lemma.py 4000000 1e-4` (regime II A-side, no cross-term) and
   `verify_Bbranch_marginal.py 4000000 1e-4` (regime II B-side, cross-term). These re-PASS
   => the unified statement reduces correctly on the live family. Per run_state, re-running
   these ALONE banks no milestone — the milestone is the unified statement + tie proof.
2. The toy outer-max one-sided-derivative check, EXTENDED to all three regimes (Check 3 /
   Check 4): tie (both slopes active, right != left kink), regime-I singleton-A (A-attaining
   cross-term), regime-II singleton-B (recovers m_B). Each: right-FD of Phi/D matches the
   closed form to <0.1%, and at the tie the LEFT-FD differs (demonstrating the kink). I ran
   the tie and the A-attaining toy and both match to ~1e-8 — the formula is correct, the
   builder just needs to package it.

## Summary of required changes (all fixable while building, none re-route to outliner):

1. (Check 3, load-bearing) DERIVE the A-attaining cross-term as a specialization of the
   unified quotient rule and EXERCISE it on a regime-I toy — do not back it by "same envelope
   structure" prose alone.
2. (Check 2) Add an explicit paragraph confirming the R8 DCT lemma's hypotheses
   (1-Lipschitz L^1 domination + finite K) are regime-independent of the outer D.
3. (Check 1 / Check 4) State explicitly that the result is the RIGHT derivative (q >= 0),
   that the tie gives a genuine one-sided kink (left != right), and that the firing test is
   `d+ log h /dq < 0`.
4. Extend the toy check to all three regimes (singleton-A, singleton-B, tie).

These are write-up discipline + one extra toy regime, not a new angle. Angle 1 is the right
pick (Angle 2 adds a limit-interchange obligation; Angle 3 adds a Clarke-regularity
obligation — both heavier than needed). Build it.
