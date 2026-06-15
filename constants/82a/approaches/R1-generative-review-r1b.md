# R1b re-review — sibling-generator gap-closure (82a)

Reviewer: proof-reviewer, R1b (2026-06-15). Re-review after CHANGES REQUESTED in R1.
Artifacts: `certificate/firstvar_08_sibling_generator.py`, `approaches/R1-generative-build.md`
(Gap-closure R1b note), `upper_bound_paper.tex` (lem:transfer ~l.763, thm:generator ~l.812).

## VERDICT: APPROVE

The R1 load-bearing gap is closed. The certificate now certifies the firing transfer with
`RHS = RHS_sharp` ALONE; the unjustified global cap is demoted to a non-certifying diagnostic;
R2 now clears the firing gap rigorously (the entire point of the fix). All four adversarial
checks pass, and I independently re-derived the per-cell sharp bound and both final margins.

This is a THEORY-PAPER round: no numeric bound changes. Held upper 0.2538893183 / lower
0.2524001332 UNCHANGED, Status stays `none`. The advance is the upgrade of the generative
sibling-generator milestone from minimal `*` (R1) to fully VERIFIED.

## Goal Progress
- Eval: `grep -rhE '^\s*-\s*R[0-9]+:' constants/*/current.md | wc -l`
- Previous: 20
- Current: 20
- Direction: IMPROVED (the milestone count was already 20 from R1; this round genuinely
  advances the frontier by UPGRADING that milestone's verification level minimal->verified
  via a closed certificate gap — a real advance, not a new countable line. The R1b line uses
  the `R1b:` tag which the eval regex `R[0-9]+:` does not count, by design: it is an upgrade
  of the existing R1 milestone, not a second milestone. No padding.)

## Adversarial checks — all PASS

1. **RHS is RHS_sharp ALONE, no min() picking the global cap.** Grep of the selection logic:
   line 432 `RHS = RHS_sharp` (direct assignment, no `min`); the verdict uses `res['RHS']`
   (= RHS_sharp). `RHS_global` (line 442) is computed only for the diagnostic print
   ("NOT used", line 572) and appears nowhere in the firing decision. The R1 bug
   `RHS = min(RHS_global, RHS_sharp)` is gone.

2. **Per-cell sharp bound is a rigorous outward-rounded upper bound, valid in both cases.**
   Re-derived from scratch: on a cell the interval machinery certifies |R|^2 in [r2_lo,r2_hi],
   |Q*|^2 in [q2_lo,q2_hi]. The integrand |log|R|-log|Q*|| = |1/2 log|R|^2 - 1/2 log|Q*|^2|.
   - case log|R| >= log|Q*|: <= 1/2 log(r2_hi/q2_lo) = up1;
   - case log|R| <  log|Q*|: <= 1/2 log(q2_hi/r2_lo) = up2.
   So <= max(up1,up2) = logRQ_abs_hi (line 271), with `log_up` outward rounding. All four
   constants come from `rho_full` interval enclosures (Taylor/mean-value model reused from
   bound_01), NOT measured. Valid in BOTH cases. The adaptive bisection (2nd criterion
   `well_contrib = w*|log|R/Q*||_hi > WELL_TOL=5e-4`, line 325-327) genuinely drives the
   CERTIFIED well integral down: refinement reaches depth 6-7 with frontier empty and
   `unresolved well cells = 0` for both siblings (every leaf well cell has |R|^2>0 certified;
   no measurement floor). Leaf/refine accounting is sound: a refined cell is NOT banked, only
   its two equal-total-width children are — no double-count, total width preserved.

3. **R2 clears the firing gap RIGOROUSLY; R0 still clears. Margins re-derived by hand.**
   log h = 0.2536331090204145 (Gri26 record, confirmed against literature/Gri26_digest.md).
   | sibling | r_Q*(Omega_F) | RHS_sharp | r_Q*+RHS_sharp | margin to log h | fires |
   |---|---|---|---|---|---|
   | R0 (Q1) | -0.033527 | 0.004814 | -0.028713 | +0.282346 | YES |
   | R2 (Q2) | -0.033008 | 0.006285 | -0.026723 | +0.280356 | YES |
   R2 was -0.029 (FAIL) under the sharp bound in R1; it now clears with margin +0.280.
   I independently confirmed at N=4e6 (own complex-Horner eval): true (1/28)int_W|log R/Q*|
   = 0.00174 (R0)/0.00285 (R2), and the CERTIFIED well_int_sharp/28 = 0.00291 (R0)/0.00428
   (R2) genuinely UPPER-bounds the true value (safe direction). True transfer r_R-r_Q* =
   +0.00066/+0.00082 matches identity (A) to ~1e-19. |W| fraction 0.077/0.085 <= certified
   delta 0.083/0.100. R0,R2 = pp(Q* -+ P1^5 P2^5 P4 . tail) re-confirmed via own sympy
   (content 1, deg 28 = deg Q*).

4. **Paper states firing claims at exactly the certified strength; generative scope intact.**
   lem:transfer (l.763) now writes the well term as the integral int_W|log|R/Q*|| ds with the
   per-cell bound max{L_R-l_Q*, L_Q*-l_R} "valid whether or not log|R|>log|Q*|", and demotes
   the L^inf cap log(1/m_R)+sup log|Q*| to "secures integrability but too crude to certify
   firing — hence the cell-wise treatment". thm:generator (l.812) quotes RHS<=0.0049/0.0063,
   both margins ~0.28, and states "no global cap on |log|R/Q*|| invoked". rem:gen-scope is
   honest and unweakened (criterion-alone does NOT predict R0,R2; bridge/tails not claimed
   optimal). No residual overclaim a referee would catch.

Tamper checks E1 (understated log h not cleared), E2 (false deg R_5=27 rejected), E3 (false
'a=6 preserves deg 28' rejected) all reject.

## Milestone logged

Appended an `R1b:` line to current.md upgrading the R1 generative-theory milestone from
minimal `*` to VERIFIED: both R0 AND R2 firing now certified under rigorously-justified
bounds (RHS_sharp alone, no global cap), R2 clears rigorously, the per-cell bound and margins
independently re-derived, the paper matched to the certificate. The eval count stays 20 (this
is an upgrade of the existing R1 milestone, not a new countable line).

Verification level: **verified** (raised from minimal `*` in R1).

## What was edited
- `constants/82a/current.md`: appended the `R1b:` progress-log line (level minimal->verified).
- Held upper/lower and `## Status: none` UNCHANGED (theory round, no numeric break).
- Canonical `constants/82a.md` NOT edited (no bound change).
