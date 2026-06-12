# R9 outline — UNIFIED first-variation cross-term lemma (82a UPPER, structural)

Spec review: required
Target to beat: STRUCTURAL milestone (NO numeric break). The numeric UPPER lever is
reviewer-verified EXHAUSTED (A-base maximal-firing-set R7; B-branch maximal-firing-set
R8; BMQS recast = saturated Doche family R1). Held upper 0.2538893183 stays UNCHANGED,
Status:none. The "value to beat" is therefore a NEW reviewer-verifiable structural
advance not already banked — specifically, a single first-variation statement that does
NOT assume which arg attains D, generalizing the two separately-verified sub-cases
(R6/R8 A-base: D constant, no cross-term; R8 B-branch: D moves, cross-term
-(log h)deg/D) and supplying the missing TIE-case derivation.

Why this is a genuinely NEW milestone and not a re-bank: R8 proved the two endpoints
under DISJOINT hypotheses (H2: arg_A<arg_B for A-base; its mirror for B-branch). Neither
covers (a) an A-base block that ENTERS the D-attaining arg (the A-attaining cross-term,
which has NO on-disk FD because there is no live A-dominant family — see Scope), nor
(b) the boundary arg_A=arg_B where D is a max of two MOVING args. The unified lemma is
the envelope statement that contains both endpoints as corollaries and closes the tie.

================================================================================
## What is already on disk (INPUTS — cite, do NOT re-derive)

- A-base sub-case (R6 lemma, R8 rigorized): `approaches/R8-firstvar-rigorous.md`.
  Phi(q)=int_0^1 max(A_0+q log|Q.chi|, B) ds right-diff at 0 with
  Phi'(0+)=int_{A_0>B} log|Q.chi| ds, via DCT on the difference quotient
  psi_q=[G(.,q)-G(.,0)]/q (1-Lipschitz max => dominated by |log|Q.chi|| in L^1;
  a.e. limit = log|Q.chi|*1_{A_0>B}; kink set K={A_0=B} finite => measure 0).
  Under H2 (arg_A<arg_B => dD/dq=0) this gives d(log h)/dq = (1/D) r~_Q, NO cross-term.
  Engine: `certificate/verify_firstvar_lemma.py`, audit `audit_firstvar_rigor.py`.
- B-branch sub-case (R8 Angle A): `certificate/verify_Bbranch_marginal.py` header is the
  full derivation. When the block enters the D-ATTAINING arg, arg_B is affine in q with
  slope deg(Q), dD/dq=deg(Q), and the quotient rule gives
  m_B(Q)=(1/D)[int_{B>A} log|Q.chi| ds - (log h) deg(Q)]. FD MOVES D. Reviewer-reproduced.
- Both sub-cases use the SAME inner-max envelope (Danskin boundary cancellation because
  A-B=0 on the kink set) — the difference is ONLY whether the perturbed arg attains the
  OUTER max D. That observation is the whole content of the unification.

The unified lemma must INVOKE these two, not re-prove them. The only genuinely new
derivation is the outer-max Danskin + the tie case.

================================================================================
## The object

Let, for a perturbation direction (an integer block Q entering ONE of the two sides with
exponent q >= 0; sign/side fixed by which branch it joins):

  Phi(q) = int_0^1 max( A(s,q), B(s,q) ) ds,     log h(q) = Phi(q) / D(q),
  D(q)   = max( arg_A(q), arg_B(q) ),
  arg_A(q), arg_B(q) AFFINE in q (Doche §4 D-formula: each is base-value + q*deg(Q)
           on the side Q joins, constant on the other side).

At q=0 write a := arg_A(0), b := arg_B(0). Exactly one of three regimes holds:
  (I)  a > b  : A attains D.
  (II) a < b  : B attains D.   <- the held R4 family (b=72.00 > a=61.66).
  (III) a = b : TIE, D is a max of two args BOTH moving in q.  <- the HARD STEP.

================================================================================
## Angle 1 (top pick): direct quotient rule + one-sided Danskin on the OUTER max

Moves: nothing numeric — establishes the UNIFIED structural statement
  d^+ log h /dq |_0 = (1/D) [ Phi^+'(0) - log h * (dD/dq)^+ |_0 ],
with Phi^+'(0) = int_{active arc} log|Q.chi| ds (active arc = {A_0>B} or {B>A_0}
depending on the side Q joins; the inner-max envelope, already proved), and
(dD/dq)^+ = deg(Q) * 1{the joined arg is (one of) the D-attainer(s)} in regimes I/II,
and in the tie a one-sided value selected by which branch's arg-slope is larger.

Skeleton:
  1. log h = Phi/D, both factors functions of q; D(q)>0 bounded away from 0 (D >= 56).
     A one-sided product/quotient rule then needs ONLY that Phi and D each have a
     one-sided derivative at 0 — by tool: elementary calculus of one-sided derivatives,
     d^+(Phi/D) = (Phi^+' D - Phi (D)^+') / D^2.
  2. Phi has the stated one-sided derivative Phi^+'(0) = int_{active} log|Q.chi| ds.
     — by tool: the R8 DCT lemma (`R8-firstvar-rigorous.md`), applied to whichever side
     Q joins. (INPUT, already rigorized; the inner-max kink set is finite either way.)
     NOTE: Phi^+' is the SAME integral regardless of regime I/II/III — it depends on the
     inner max(A,B), not on which arg attains the OUTER D. This decoupling is the key.
  3. D(q)=max(arg_A(q),arg_B(q)) with arg_A,arg_B AFFINE => D is convex piecewise-linear,
     hence has a one-sided derivative at 0 equal to the max of the slopes of the args
     that ATTAIN the max at 0:
        (dD/dq)^+|_0 = max{ arg_A'(0) : a attains D } u { arg_B'(0) : b attains D }.
     — by tool: Danskin/Bertsekas for the max of finitely many affine (hence C^1)
       functions; the directional derivative of a finite max is the max of the
       derivatives over the ACTIVE index set. Citation, not dependency (D is an explicit
       2-term max of affine functions, so this is one line of convex calculus).
  4. Read off the three regimes:
     - (I) a>b: only arg_A active in D. If Q joins A-side, (dD/dq)^+=deg(Q) and
       cross-term = -(log h)deg(Q)/D (the A-ATTAINING cross-term — NEW, no on-disk FD,
       see Scope). If Q joins B-side, (dD/dq)^+=0, no cross-term.
     - (II) a<b: mirror image. Q on B-side => cross-term (recovers R8 m_B EXACTLY);
       Q on A-side => no cross-term (recovers R6/R8 r~_Q EXACTLY). This is the held
       family; both corollaries are the already-verified results.
     - (III) a=b: both active; (dD/dq)^+ = max over the two slopes of whichever args
       move. The one-sided derivative still EXISTS (convex pw-linear) and equals the
       larger slope; the quotient rule of step 1 then gives a one-sided d^+ log h /dq.
  5. State the unified marginal and list R6 (II,A-side) and R8 (II,B-side) as corollaries
     obtained by zeroing the inactive terms. — by inspection.

Hard step: STEP 3+4(III), the TIE case a=b. Load-bearing claim: at a tie, D(q) is the
max of two AFFINE functions agreeing at q=0, so D is convex and right-differentiable with
(dD/dq)^+|_0 = max(arg_A'(0), arg_B'(0)); consequently log h = Phi/D has a ONE-SIDED
directional derivative (not necessarily two-sided — a kink in q is allowed and expected).
Mechanism: a finite max of affine functions is convex piecewise-linear; convex functions
on R have one-sided derivatives everywhere, and for a finite max the right-derivative is
the max of the right-derivatives of the active pieces (Danskin/Rockafellar Thm 23.x).
Phi^+'(0) exists independently by the R8 DCT lemma. Quotient of two right-differentiable
functions with nonzero denominator is right-differentiable. So d^+ log h /dq exists and
equals the displayed envelope expression. The tie is NOT an open inequality — it is a
one-sided-Danskin/envelope identity on an explicit 2-term affine max.

What could go wrong (the review must check):
  (a) Two-sided vs one-sided. At a tie, log h need NOT be differentiable (only one-sided).
      The lemma MUST state d^+ (right derivative), and the "firing iff <0" corollary must
      use the right derivative. Claiming a two-sided derivative at a tie is FALSE.
  (b) Whether Phi^+'(0) and the int commute / are regime-independent. The R8 DCT lemma is
      stated under H2 (regime II). The unification must confirm its proof uses ONLY the
      inner-max finiteness of K={A_0=B} and the L^1 dominator — NEITHER depends on which
      arg attains the OUTER D. (It does not: D enters only as the q-constant or affine
      normalizer, never inside Phi.) This is the one place to re-read R8 carefully; it is
      a check, not a re-derivation.
  (c) Active-index set at the tie is the FULL {A,B} (both active), so Danskin gives the
      max of BOTH slopes — must not silently drop one. In regimes I/II the active index
      set is a singleton and the cross-term indicator is clean.
  (d) The arg_A, arg_B affineness in q is the Doc01a §4 D-formula (already used and
      PDF-verified R2/R4/R7); cite it, do not re-derive.

Check (what the builder runs/derives to certify it):
  - The two COROLLARIES are exercised by the EXISTING engines, unchanged:
    `verify_firstvar_lemma.py 4000000 1e-4` (regime II, A-side, no cross-term) and
    `verify_Bbranch_marginal.py 4000000 1e-4` (regime II, B-side, cross-term -(log h)deg/D).
    These re-PASS => the unified statement reduces correctly on the live family.
  - A SMALL NEW symbolic/numeric check for the OUTER-max one-sided derivative on a TIE:
    build a toy 2-term affine max D(q)=max(a0+ s_A q, a0 + s_B q) (a tie at q=0) and a
    toy Phi(q)=Phi0 + r q (r = int over active arc) and verify the right finite-difference
    of Phi/D matches (r D - Phi0 max(s_A,s_B))/D^2 to <0.1% while the LEFT FD differs
    (demonstrating the genuine one-sided kink). This isolates and exercises EXACTLY the
    tie-case formula without needing a live A-dominant family. ~seconds.
  - Reviewer re-derives step 3 (convex-max right-derivative) from Rockafellar/Danskin
    by hand and confirms (a)-(d) above.

================================================================================
## Angle 2: homogeneous f/D limit-point reparametrization

Moves: same structural statement, via Doche's homogeneous form. log h = 2b f(q)/D(q)
with f(q)=int_0^1 max(A,B) ds the limit-point functional; reparametrize so the
perturbation is a ray q*v in exponent-space and differentiate log h along the ray.
Because both f and D are positively-homogeneous-degree-1-PLUS-affine in the single new
exponent, the directional derivative along the ray is the Gateaux derivative, and the
tie becomes the statement "the support function of the active-arg set is the max of the
two arg-slopes." Recovers the same envelope expression.

  Hard step: showing the limit-point functional f is directionally differentiable along
  the ray and that the D-normalization commutes with the limit defining h (Doche Lemma 2,
  h(q)=exp(2b f(q)/D)). Risk: the limit-point construction's differentiability in q is
  NOT obviously the same as differentiating the finite-N integrand; one must argue the
  limit and d/dq interchange. This is STRICTLY harder than Angle 1 (it re-opens the
  limit-point convergence that Angle 1 sidesteps by working directly with Phi=int max).
  Check: same two corollary engines; plus confirm at v = e_Q (single new exponent) the
  Gateaux derivative reduces to Angle 1's d^+.

  Verdict: more elegant framing but adds a convergence-interchange obligation Angle 1
  does not have. Use ONLY if a reviewer objects that Angle 1's "log h = Phi/D" is not
  literally the Doche limit object (it is — D is the q-dependent normalizer, Phi=2b f).

================================================================================
## Angle 3: subdifferential / Clarke generalized gradient (cover the tie uniformly)

Moves: same statement, but instead of a one-sided derivative state the result as a
Clarke subdifferential: log h = Phi/D is locally Lipschitz in q (Phi Lipschitz by the
1-Lipschitz max + L^1 dominator; D convex pw-linear Lipschitz; ratio Lipschitz away from
D=0), so partial-Clarke d(log h) is a nonempty compact interval, and at a tie it is the
interval between the two branch marginals; firing iff max of the Clarke set < 0.

  Hard step: identifying the Clarke set at the tie with [min,max] of the two branch
  marginals — needs the chain/quotient rules for Clarke gradients (Clarke 1983 Thm 2.3.x)
  and that the two affine pieces are the only generators. Risk: Clarke calculus has
  INCLUSION (not equality) chain rules in general; equality needs regularity (here the
  functions are subdifferentially regular: convex D, and Phi is C^1-on-each-side with a
  measure-zero kink), which must be argued. Slightly heavier machinery than needed.
  Check: same two corollary engines; the toy tie check from Angle 1 confirms the Clarke
  interval endpoints.

  Verdict: most robust (handles the tie without committing to one-sidedness and gives the
  cleanest "firing" criterion as max of the set < 0), but invokes more theory than the
  problem needs. Good fallback if the one-sided statement of Angle 1 draws objections
  about which one-sided derivative is the "right" firing test.

================================================================================
## Ranking

Angle 1 first. It works DIRECTLY on Phi=int max(A,B) ds (no limit-point interchange,
unlike Angle 2; no Clarke-regularity obligation, unlike Angle 3), reuses the two
reviewer-verified sub-case engines UNCHANGED as corollaries, and isolates the one new
piece — the outer-max right-derivative at a tie — as a one-line convex-calculus fact
(max of affine functions) that is exercised by a seconds-long toy check. Its only genuine
subtlety, that the tie gives a ONE-SIDED (not two-sided) derivative, is a feature to state
correctly, not a gap.

Fall back to Angle 3 if the reviewer wants the tie handled without privileging a
direction (Clarke interval => firing iff max < 0 is unambiguous). Use Angle 2 only if the
"log h = Phi/D" object is challenged as not being literally Doche's limit point.

================================================================================
## Scope (HONEST — enforce in the write-up)

- This is a UNIFICATION + TIE-CASE argument. Regime II (both sides) is the held family
  and its two corollaries are FD-exercised on disk. Regime I (A attains D) and the
  A-ATTAINING cross-term -(log h)deg/D for an A-side block are established by the SAME
  envelope structure, NOT by a numeric FD check: there is NO live A-dominant family on
  disk to perturb (the held family has arg_A=61.66 < arg_B=72.00). Say so explicitly.
  Do NOT claim the A-attaining cross-term is numerically exercised.
- The TIE case (III) is the load-bearing new step; it is a one-sided Danskin/envelope
  identity on an explicit 2-term affine max, NOT an open inequality. Do NOT hand-wave it
  — write the convex-max right-derivative argument and the one-sided quotient rule out,
  and exercise the formula on the toy tie check.
- Do NOT re-bank: re-running verify_firstvar_lemma.py / verify_Bbranch_marginal.py alone
  logs no milestone. The milestone is the UNIFIED statement + tie proof; the engines are
  corollary checks, not the advance.
- Keep the prior HONESTY guardrails: dual loci scoped UPPER-INTERNAL ({A_0>B} vs {B>A_0});
  no "lower locus = complement of upper arc"; no inf_Q r~ = -log t_{Z,phi} overclaim.
