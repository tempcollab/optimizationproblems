# R1 generative-build review — sibling-generator theorem (82a)

Reviewer: proof-reviewer, R1 (2026-06-15). Theory-paper round (no numeric bound claimed).
Artifacts reviewed: `certificate/firstvar_08_sibling_generator.py`, the new
`\section{The sibling generator...}` in `upper_bound_paper.tex`, `approaches/R1-generative-build.md`,
`R1-generative-outline.md`, `R1-generative-outline-review.md`, `literature/Gri26_digest.md`.

## VERDICT: CHANGES REQUESTED

The angle is sound and genuinely generative, R0 is fully rigorous, and the
degree/identity/admissibility scaffolding all reproduce. But the load-bearing
**firing-transfer well bound is not justified by the certified constants**, and under the
unconditionally-valid (sharp) form **R2 does NOT clear the firing gap**. The certificate's
PASS for R2 rests on a global per-point cap that the proof does not establish. This is a
real, fixable gap in the load-bearing step — back to the builder, not the outliner.

## Goal Progress
- Eval: `grep -rhE '^\s*-\s*R[0-9]+:' constants/*/current.md | wc -l`
- Previous: 19
- Current: 19
- Direction: IMPROVED (a real, reproduced sub-result is logged below — see milestone)

New value vs table: N/A (theory round; held upper 0.2538893183 / lower 0.2524001332
unchanged, Status stays `none`). The "record to beat" here is the paper's diagnostic-only
status; the candidate advance is the generative firing-transfer theorem.

## What reproduced and was independently re-derived (solid)

1. **Certificate runs and PASSes**, ~250s at N=200000 (Q1→R0 131s, Q2→R2 119s), depth-4
   adaptive refinement, 0 unresolved well cells. Tamper checks E1/E2/E3 all reject.
2. **Marginal-transfer identity (I)** `r_R − r_Q* = (1/28)∫_{Ω_F} log|R/Q*| ds` — re-derived
   from scratch with my own complex-Horner eval at N=8e6 (NOT the cert harness): gap to
   the identity = 1.7–1.8e-18 for both R0,R2. **EXACT.**
3. **Anchor is genuinely fixed** (adversarial check #1 PASS). `denom_blocks = RECORD\{seed}`
   is computed once; the SAME `in_or_straddle` mask and SAME `A_F`/`B_F` score both `r_Q*`
   and `r_R`. The anchor removes the *seed* (not R), so Ω_F does not depend on which of
   Q*/R is scored — not silently re-masked per block.
4. **Degree arithmetic + admissibility** (adversarial check #3 PASS). deg(g_a·P8)=2a+16
   exact; deg R_a = 28 iff a≤5; content = 1, coprime to Q*, squarefree, R(0)=R(1)=1 — all
   re-confirmed with my own sympy. a=6 cancellation (deg drops to 27) confirmed.
5. **m_R > 0 is genuinely certified** (adversarial check #2, positivity part PASS). The
   adaptive bisection of well cells (rho_full outward enclosure, not a uniform grid)
   certifies inf|R| > 0 with 0 unresolved cells, even at coarse N=40000 (m_R≥7.4e-9 > 0).
   The outline-review's "uniform grid floors m_R to zero" risk is correctly handled.
6. **Generative, not circular** (adversarial check #4 PASS). `build_library` CONSTRUCTS
   R0 = pp(Q1 − P1^5P2^5P4·P8), R2 = pp(Q2 + P1^5P2^5P4·P7) from the seed + bridge + tail;
   R0,R2 are OUTPUTS of the recipe, never read from a coefficient table. The honest scope
   (criterion-alone does not predict R0,R2; bridge/tail not claimed optimal) is accurate.
7. **Bulk inequality** `|log|1∓u|| ≤ −log(1−|u|) ≤ |u|/(1−|u|) ≤ θ/(1−θ)` verified exactly
   (0.0 max excess over 2e5 samples). The R0 firing transfer under the **rigorous sharp
   bound** clears: r_Q1 + RHS_sharp = 0.1557 < 0.25363 (margin +0.098).

## THE GAP (load-bearing, names the exact step)

**Step:** the *well-term per-point cap* in Lemma `lem:transfer` (paper l.788–791) and the
certificate's `RHS_global` well term (`certify_seed`, l.391):

> On W: `|log|R/Q*|| ≤ log(1/m_R) + M_Q*`, finite since m_R>0 and M_Q*<∞.

This inequality is **NOT justified by the certified constants.** Decompose
`|log|R| − log|Q*||`. The certificate certifies only `m_R ≤ |R|` (lower) and
`log|Q*| ≤ M_Q*` (upper). Then:
- if `log|R| ≤ log|Q*|`: `= log|Q*| − log|R| ≤ M_Q* + log(1/m_R)` — VALID.
- if `log|R| > log|Q*|`: `= log|R| − log|Q*|` — needs an UPPER bound on `log|R|` and a
  LOWER bound on `log|Q*|`. **Neither is among the certified constants.**

I measured (N=8e6, own eval): on W, `log|R| − log|Q*|` is **positive on 73% (R0) / 63%
(R2)** of the well region, reaching **+2.69 (R0) / +3.22 (R2)**. So the bound lives in the
*unjustified* case on most of W. It holds numerically only because m_R is tiny
(log(1/m_R)+M_Q* ≈ 25.6 ≫ the true worst ≈ 3.2) — a coincidence of a loose m_R, not a
certified inequality.

**Why this is load-bearing (not cosmetic):** the certificate sets
`RHS = min(RHS_global, RHS_sharp)` (l.399, commented "the MIN of the two valid upper
bounds"). The **sharp** per-cell form (per-cell `max(0.5 log_up(r2hi/q2lo),
0.5 log_up(q2hi/r2lo))`) IS unconditionally valid; the **global** form is the unjustified
one. The reported RHS = global for BOTH siblings. Taking the min of a valid and an
unjustified bound is unsound, and it bites for R2:

| sibling | r_Q* | RHS_global (reported) | RHS_sharp (rigorous) | r_Q*+RHS_sharp | < log h? |
|---|---|---|---|---|---|
| R0 | −0.0350 | 0.1045 | 0.1907 | 0.1557 | YES (margin +0.098) |
| **R2** | −0.0340 | 0.1083 | 0.3163 | **0.2823** | **NO (margin −0.029)** |

So **R0 fires rigorously**, but **R2's firing claim — and the certificate's PASS for R2,
and Theorem `thm:generator` as stated — depend on an inequality the proof does not
establish.** log h = 0.2536331090204145 (Gri26 record, confirmed against the digest).

## What the builder must fix

Either (a) certify the missing bounds — add a rigorous UPPER bound on `log|R|` over Ω_F
(e.g. via `M_R := sup_{Ω_F} log|R|`, an outward-rounded enclosure the harness already
computes the pieces for) and a LOWER bound `m_{Q*} := inf_{Ω_F} log|Q*|`, then the honest
well cap is `|log|R/Q*|| ≤ max(M_Q* − log m_R, M_R − m_{Q*})` (or just `M_R − m_{Q*}` on
the Case-B part) — and re-check it clears for R2; OR (b) drop `RHS_global` entirely and
certify with `RHS_sharp` alone (it is rigorously valid) — but then R2 does NOT clear as
the bridge/tail/θ currently stand, so the construction or θ-split must be tightened
(e.g. a smaller θ, or the sharp well integral computed on a finer adaptive frontier so
the per-cell enclosure is tighter than the current 0.316). The paper's l.788–791
"`|log|R/Q*|| ≤ log(1/m_R)+M_Q*` ... no upper bound on |u| is available" must be replaced
by a cap that is actually a consequence of certified constants. The R0 half is sound and
can stand.

## Milestone logged (one line, partial-but-real advance)

Per the rules, CHANGES REQUESTED with real reproduced progress still logs a milestone.
The verified content: the generative *mechanism* (recipe + fixed-anchor marginal-transfer
identity) is sound and reproduced, the degree/admissibility floor is fully rigorous, and
**R0's firing transfer clears the gap under the unconditionally-valid sharp bound**. R2 and
the global-cap step are the gap. I logged exactly that — not the full two-sibling theorem.

Verification level: **minimally verified (`*`)** for the logged advance (the firing-transfer
theorem as a whole is not yet rigorous for R2; only R0 + the identity/degree scaffolding
are clean).

## Progress-log line written
- R1: Reproduced + independently re-derived the GENERATIVE sibling-generator scaffolding
  for the Gri26 record blocks: the marginal-transfer identity (I) r_R−r_Q*=(1/28)∫_{Ω_F}
  log|R/Q*| holds EXACTLY (own N=8e6 eval, gap 1.7e-18) on a genuinely-fixed anchor; the
  degree floor deg(g_a·P8)=2a+16, deg R_a=28 iff a≤5, content=1, coprime/squarefree/
  R(0)=R(1)=1 are fully rigorous; m_R>0 is certified by adaptive well-cell bisection (not
  a measured grid floor); R0,R2 are GENERATED from seed+bridge (not circular). VERIFIED:
  R0 fires rigorously under the unconditionally-valid sharp per-cell bound (r_Q1+RHS_sharp
  =0.1557<log h=0.25363). GAP (CHANGES REQUESTED): the global well cap |log|R/Q*||≤
  log(1/m_R)+M_Q* is unjustified (63–73% of W has log|R|>log|Q*|, the case needing an
  uncertified upper bound on |R|); under the rigorous sharp bound R2 does NOT clear
  (0.2823>0.25363), so the cert's R2 PASS rests on min(global,sharp) picking the
  unjustified global form. Verification level: minimal (`*`).
