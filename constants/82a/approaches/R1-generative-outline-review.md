# Outline review — R1 generative sibling-generator theorem (82a)

Reviewer: outline-reviewer, R1 (2026-06-15). Outline under review:
`constants/82a/approaches/R1-generative-outline.md` (Angle 1 = coprime-sibling generator
theorem; Angle 2 = bridge-exponent / degree-optimality fallback).

## VERDICT: CHANGES REQUESTED

Angle 1 is the **right technique and is genuinely generative** (not secretly diagnostic),
its load-bearing analytic bound is real and I confirmed numerically that it **clears the
firing gap rigorously** for both R0 and R2. But three items must be nailed down while
building, and one scope claim must be re-worded. None is fatal; all are fixable in the
builder round. Angle 2 is a sound rigorous floor and should be produced first as the
outline recommends.

---

## 1. Is it generative or dressed-up diagnosis? — GENERATIVE (passes)

The criterion for "generative vs after-the-fact" is: **does the theorem need R0,R2 as
input, or only Q\* + Ω?** Verified it needs only Q\* + Ω + the bridge ansatz:

- Input is the distinguished block Q\* (=Q1,Q2) and the active set Ω. The output is the
  family R(a,tail) = pp(Q\* ∓ P1^a P2^a P4 · P_tail). R0 = R(5,P8), R2 (on Q2) = R(5,P7)
  are **instances produced by the recipe**, not inputs to it. This is the line that makes
  it a generator and not a screen — confirmed.
- It does NOT claim the criterion alone (no seed) predicts R0,R2, and the outline's scope
  line says so. That honesty is correct and necessary; with it, the contribution is real.

So the deliverable converts paper l.647 "explanatory, not generative" into a stated
construction recipe + the magnitude condition that makes it fire + the degree count that
forces a=5. That clears the referee bar **as a generator-from-seed theorem**. Do not let
the builder overstate it to "from the criterion alone" (see §5).

## 2. The hard step (marginal-transfer / magnitude-subordination bound) — HOLDS, with the
   flagged θ-fix, and CLEARS the gap. (re-derived numerically; the builder must make the
   constants rigorous.)

I reproduced the identity and the bound at N=4e6 (`/tmp/check_hardstep.py`, re-runnable):

- **The identity is EXACT.** `r_R - r_Q* = (1/deg) ∫_Ω log|R/Q*|` requires deg R = deg Q*
  (so the normalizer is shared) AND a single common Ω. Both hold: deg R0 = deg Q1 = 28,
  and scoring R0 and Q1 on the *same* mask gives r_R0 - r_Q1 = +0.001145, equal to
  (1/28)·mean_Ω log|R0/Q1| = +0.001145 to all digits. Identity confirmed.
- **The θ-split is necessary and the outline's fix (α) is correct.** Splitting Ω at a
  fixed θ = 1/2 on |g/Q*| (not at |g/Q*| ≤ 1) avoids the |u|/(1-|u|) blow-up. With θ=1/2:
  - bulk term ≤ (θ/(1-θ))·|Ω_0|/N = 0.441 (un-normalized)
  - well term = δ·(log(1/m_R) + M_Q*) = 2.952 (un-normalized), m_R0 ≈ 1.39e-6, M_Q1 ≈ 25.1
  - RHS/28 = 0.1212, so r_R0 ≤ r_Q1 + 0.1212 = -0.0699 + 0.1212 = **0.0513 < log h = 0.2536.**
  - R2: RHS/28 = 0.1329, r_R2 ≤ 0.0675 < 0.2536. **Both clear.** Risk γ resolved FAVORABLY:
    the rigorous bound (≈0.12) is two orders looser than the true gap (≈0.001) yet still
    leaves ~0.20 of slack to log h. The bound is crude but sufficient.

**Three things the builder MUST fix in this step (the reason for CHANGES not APPROVE):**

(a) **The δ in the outline is the WRONG number.** The outline and the explore doc quote
   "δ ≈ 0.02 (deepest 2% wells)". That 2% is the deepest-2%-of-the-full-contour figure
   from probe 3 — it is NOT the measure of the θ-split well region {|g/Q*| > θ} ∩ Ω that
   the bound actually uses. The real well fraction at θ=1/2 is **14.8% of Ω ≈ 7.6% of the
   full circle**, ~4× larger. The bound still clears (shown above) because m_R is only
   ~1e-6, but the builder must compute δ as the measure of {|g/Q*| > θ} (a rigorous upper
   bound via interval enclosure), not reuse the 0.02 figure. Quoting δ=0.02 in the proof
   would be a real error a referee re-running the integral would catch.

(b) **M_Q* (= max log|Q*| ≈ 25.1) and m_R (= min|R| ≈ 1.4e-6) dominate the well term and
   MUST be certified, not measured.** The well term 2.95 is dominated by M_Q* = 25.1, which
   is large; the bound's clearance depends on δ·M_Q* staying below the slack. The builder
   must produce M_Q* as a rigorous *upper* bound and m_R as a rigorous *lower* bound (>0,
   contour-root-free) by outward-rounded interval evaluation — the `verify_upper.py` /
   `bound_*` harness already does exactly this style. I checked min|R0| is stable under a
   1e-7 grid refinement (1.39217e-6 both), so it is a genuine bounded-away-from-zero
   minimum, not a missed contour root — but the rigorous lower bound still has to be
   stated, and δ must be a certified upper bound on the well measure.

(c) **Ω is anchor-dependent — fix ONE anchor and score both Q\* and R on it.** Ω = {B > A0}
   is computed at the candidate-free family, which differs depending on whether R or Q* is
   the removed candidate. I measured the two masks differ by only 0.4% symmetric difference
   and r_Q1 moves by 0.0003 between anchors, so this is small — but the identity is exact
   only on a *single* common Ω. The builder must state the theorem on a fixed anchor family
   F with a single Ω = Ω_F, read "Q\* fires" as r_{Q\*}(Ω_F) < log h, and score R on the
   same Ω_F. Stated that way the identity is clean and there is no circularity. Left
   implicit (as the outline currently leaves it), a referee will flag the Ω-ambiguity.

## 3. Admissibility, content, degree arithmetic — VERIFIED rigorous (passes)

Re-ran the sympy checks (`/tmp/` script) for a = 3..7:

- **Degree formula deg(bridge·P8) = 2a+16 is CORRECT** (deg bridge = 2a+4, × deg P8 = 12).
  The explore doc's "deg 14 / bridge·P8 deg 26" is the a=5 special case; the outline's
  general 2a+16 is right and supersedes it. The outline already notes it corrects the
  explorer's looser "2a+17".
- **The maximal-displacement rider is rigorous:** deg(Q* ∓ g_a) = 28 iff 2a+16 ≤ 27 iff
  **a ≤ 5**. Pure inequality, no analysis. Confirmed.
- **a=5 preserves the top two coefficients [1,-7] = Q1's** (deg(bridge·P8)=26 < 28); content
  = 1 for a=3,4,5; R coprime to Q1, squarefree, R(0)=R(1)=1 — all True. Admissibility
  follows, not assumed. The content factor (β) is 1 here, verified — but the builder must
  still print `.primitive()[0]` and state it = 1 rather than silently dropping it.
- **a=6 cancellation confirmed:** bridge·P8 at a=6 has LC = +1, deg 28 = deg Q1 (LC +1), so
  the X^28 terms cancel and deg R drops to 27 (top coeff jumps to 4). The "a=5 is the unique
  largest leading-coefficient-preserving exponent" claim is sound. **Caution on wording:**
  the *uniqueness* of a=5 rests only on the inequality 2a+16 < 28; the a=6 *cancellation*
  is a separate (data-specific, here-verified) bonus, not what forces a≤5. The builder
  should not conflate them — "largest a with deg(g·P8) < deg Q*" is the clean rigorous claim;
  the a=6 leading-term cancellation is an illustrative remark. (Also note a=7 gives deg 30,
  not a further degree drop — so "a=6 drops the degree" is true but is not a monotone trend;
  state it as the single boundary case.)

## 4. Avoids recorded dead ends — YES

The outline correctly excludes the three refuted lines (equilibrium/transfinite-diameter
generative rule per paper l.709 + R7; "R0 small on Ω" — R0 is the same size as Q1; global
r_Q-minimization as the principle — R7 sparse-lattice). The generator is correctly framed
as a subroutine-from-seed, not an unconstrained solver. Good.

## 5. Scope / honesty — one re-wording required

The outline's "Honest scope line" is mostly correct, but tighten two points so a referee
cannot read an overclaim:

- Keep "given the distinguished block as seed" attached to EVERY statement of the result.
  The contribution is a generator-from-seed; it is NOT "the criterion predicts R0,R2".
- Do not claim the bridge P1^5P2^5P4 or the tails P7,P8 are optimal among generators (the
  outline already disclaims this — keep it explicit; it is the open WITD residual).
- State the firing-transfer conclusion (c) as **proved** (the rigorous bound clears the
  gap — confirmed here), NOT "conditional on measured constants". Since the certified
  constants DO clear it, (c) is a theorem, not a diagnostic — but only once δ, M_Q*, m_R
  are the certified versions per §2(a,b). If the builder cannot certify those, (c) reverts
  to conditional and the result weakens to Angle 2.

## Angle 1 vs Angle 1+2 — both, in the order the outline gives

Angle 1 alone is a standalone contribution **provided §2(a,b,c) are closed** — the
generative recipe + the certified subordination bound + the degree count is enough. It is
not too thin. But the outline's plan to **produce Angle 2 (degree-count + per-a admissibility
table, fully rigorous, cheap) FIRST, then add the Angle-1 analytic bound on top** is the
right risk ordering: it guarantees a referee-acceptable rigorous floor (the family + its
degree boundary + admissibility-per-a) even in the unlikely event the certified constants
in §2(b) come out too loose. Build Angle 2's table, then Angle 1's bound; together they are
the milestone.

## What the builder must deliver (checklist)

1. `sibling_generator.py`: construct R from Q* + bridge ansatz; assert deg R = 28 + shared
   top two coeffs, content = 1, coprimality/squarefree/R(0)=R(1)=1 (sympy).
2. Rigorous (outward-rounded interval) evaluation of: δ = measure{|g/Q*| > θ} on a FIXED
   anchor Ω (NOT the 0.02 figure), M_Q* (upper), m_R (lower, > 0). Print RHS of the
   θ-split inequality and confirm r_Q* + RHS < log h for R0 AND R2.
3. State the theorem on a single fixed anchor family F / Ω_F; score Q* and R on the same Ω_F.
4. Angle-2 table: (deg R_a, admissible?, content, r_{R_a}) for a = 1..6, with the 2a+16
   degree-boundary as the rigorous optimality statement.
5. Scope paragraph with the seed-dependence and non-optimality disclaimers of §5.

Numerical confirmations re-runnable from `/tmp/check_hardstep.py` (identity exact; bound
clears for R0 and R2; Ω anchor-dependence ≈ 0.4%; min|R0| stable under refinement).
