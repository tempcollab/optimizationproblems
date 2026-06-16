# R1 generative-build — the sibling-generator theorem (82a)

Builder: proof-builder, R1 (2026-06-15). Angle built: **Angle 1 (coprime-sibling
generator) + Angle 2 (degree floor)**, per `R1-generative-outline.md` and the
CHANGES-REQUESTED items of `R1-generative-outline-review.md`. THEORY-PAPER round —
no new numeric bound; the held upper 0.2538893183 / lower 0.2524001332 are untouched.

## What was built

1. **Certificate** `constants/82a/certificate/firstvar_08_sibling_generator.py` —
   a self-contained, rigorous (outward-rounded interval) script.
2. **Paper section** `constants/82a/upper_bound_paper.tex`, new
   `\section{The sibling generator: from diagnosis to construction}` (`sec:generator`),
   plus an intro consequence (`thm:gen-intro`), a verification-table row, and a
   rewritten Scope paragraph. The closing paragraph of `sec:record` now points
   forward: "diagnosis -> construction".

## What was PROVED (the load-bearing facts, all certified)

The construction is **generative from a seed**: input = a distinguished firing block
`Q*` (Q1 or Q2) + the bridge ansatz `g = P1^a P2^a P4 . P_tail`; output = the family
`R = pp(Q* -+ g)` of admissible firing siblings, of which Grinsztajn's R0,R2 are the
instances `a=5`, tail `P8`/`P7`.

### (Angle 2) Degree floor — fully rigorous, exact integer arithmetic
`deg(g_a . P8) = 2a+16`, hence `deg R_a = pp(Q1 - g_a P8) = 28 = deg Q1  iff  2a+16<28
iff a<=5`. For `a=1..5`: content `=1`, coprime to Q1, squarefree, `R_a(0)=R_a(1)=1`
(admissible by Lemma `lem:doche`). `a=5` is the maximal leading-coefficient-preserving
exponent → `R0 = R_5`. (`a=6`: deg(g_6 P8)=28 with LC `+1`=Q1's, leading terms cancel,
deg drops to 27 — an illustrative boundary, NOT what forces `a<=5`; the bound is the
inequality `2a+16<28` alone. Outline-review §3 wording caveat folded in.)

### (Angle 1) Marginal-transfer identity + theta-split firing-transfer bound
Fix ONE anchor `F` = record denominator with `Q*` removed, `Omega_F = {B_F > A_F}`
(must-fix item 3: a SINGLE fixed anchor, both `Q*` and `R` scored on it). Since
`deg R = deg Q* = 28`, the EXACT identity

    r_R - r_Q*  =  (1/28) int_{Omega_F} log|R/Q*| ds                              (I)

holds (script confirms it numerically to ~1e-18). The **load-bearing inequality** is
the theta-split bound (theta=1/2), Lemma `lem:transfer`:

    |r_R - r_Q*|  <=  (1/28)[ log c  +  (theta/(1-theta))|Omega_0|
                              +  delta (log(1/m_R) + M_Q*) ]  =: RHS              (II)

- bulk `Omega_0 = {|g/Q*|<=theta} ∩ Omega_F`:  `|log|1-+u|| <= -log(1-|u|) <=
  |u|/(1-|u|) <= theta/(1-theta)` for `|u|<=theta<1`.
- well `W = {|g/Q*|>theta} ∩ Omega_F`, `delta=|W|`:  `|log|R/Q*|| <= log(1/m_R)+M_Q*`,
  finite because `R` is contour-root-free (`m_R = inf_{Omega_F}|R| > 0`).

**Firing transfer:** `r_Q*(Omega_F) + RHS < log h  =>  r_R(Omega_F) < log h`, so `R`
fires (Cor. `cor:criterion`).

## The certified constants (must-fix items 1 + 2) and the verdict

Every constant in (II) is an **outward-rounded interval enclosure over `Omega_F`**, NOT
a grid measurement. Each `|P(chi)|^2` is enclosed `[lo,hi]` over each whole cell by the
2nd-order Taylor/mean-value model `rho_full()` reused VERBATIM from
`bound_01_doche_base.py` (the SAME machinery the certified upper bound uses). Cells are
classified against `Omega_F` by the certified branch gap (`B_lo>A_hi` in; `B_hi<A_lo`
out; else straddle, counted conservatively). **The cells near `R`'s deep wells are
ADAPTIVELY BISECTED until `|R|^2` is certified strictly positive** — so `m_R>0` is
*established*, not measured (this is what makes the well term finite rigorously).

At the documented `N=200000` (depth-4 refinement, 0 unresolved well cells):

| seed→sibling | content c | \|Omega_0\| | delta=\|W\| | M_Q* | m_R | r_Q*(Omega_F) | RHS | r_Q*+RHS | log h | fires |
|---|---|---|---|---|---|---|---|---|---|---|
| Q1→R0 (P8) | 1 | ≤0.4432 | ≤0.0837 | ≤12.125 | ≥2.4e-8 | ≤-0.0350 | ≤0.1046 | ≤0.0695 | 0.25363 | YES |
| Q2→R2 (P7) | 1 | ≤0.4434 | ≤0.0897 | ≤12.147 | ≥5.5e-8 | ≤-0.0340 | ≤0.1083 | ≤0.0743 | 0.25363 | YES |

Both clear with margin ≈0.18. (Corrections to the outline numbers: **(item 1)**
`delta` is the certified `{|g/Q*|>theta}∩Omega` measure ≈0.084 of the circle, NOT the
0.02 "deepest-2%" figure — matches the review's predicted ≈0.076. **(item 2)** `M_Q*`
and `m_R` are certified upper/lower bounds, not measured; here `M_Q*≈12.1` over
`Omega_F` (tighter than the review's full-contour 25.1) and `m_R≈2–6e-8` certified `>0`.
The bound (II) is crude — RHS≈0.10 vs the true shift `r_R-r_Q*≈1e-3` from (I) — but
clears comfortably. The script also reports a SHARP per-cell well-integral version as a
cross-check; the global-constant form (the clean paper statement) is the binding one.)

## Check command

```
cd constants/82a/certificate
python3 firstvar_08_sibling_generator.py            # N=200000, ~90-150s, prints PASS
python3 firstvar_08_sibling_generator.py 500000     # finer grid (~7min), same verdict
```
Prints `(D)` degree floor, `(A)` identity (I), `(B)` certified constants, `(C)` the
theta-split bound and firing verdict, `(E)` tamper checks. **PASS** iff (II) clears the
gap for both R0,R2 with certified constants, the degree floor is exact, admissibility
holds, AND the three tamper checks reject (understated log h not cleared; false
`deg R_5=27`; false `a=6 preserves deg 28`). Verdict stable across N: 200k and 500k
both PASS with margin ≈0.18; the certified constants shift slightly with the grid
(Q1→R0 RHS 0.1046@200k vs 0.0992@500k; Q2→R2 RHS 0.1083@200k vs 0.1091@500k), all four
clear comfortably. The paper quotes the N=200000 values.

## Honest scope (what stays conjectural)

PROVES (re-runnable): R0,R2 are degree-preserving (deg 28) coprime admissible firing
siblings of Q1,Q2, **generated** by the bridge ansatz given the seed; the firing is
transferred from the seed by the certified bound (II); `a=5` is the maximal
degree-preserving exponent. This converts paper l.647 "explanatory, not generative"
into a stated construction recipe with a certificate.

DOES NOT prove (kept heuristic, Remark `rem:gen-scope`): that the criterion ALONE (no
seed) predicts R0,R2; that the bridge `P1^5P2^5P4` or the tails `P7,P8` are OPTIMAL
among generators (the open WITD residual); that the recipe yields the BEST siblings.
The seed and bridge CHOICE remain heuristic — only the *consequence* (admissible firing
sibling) is certified.

## Spec concerns sent back to the outline

- Outline item (α): the `theta`-split fix is correct and used (`theta=1/2`); without it
  the `|u|/(1-|u|)` blows up at `|g/Q*|→1`. Confirmed.
- Outline item (β) content: content `c=1` for R0,R2 (printed via sympy `.primitive()`,
  carried exactly in (II), `log c = 0`). Confirmed; not dropped.
- Outline item (γ) clearance: the rigorous constants DO clear the gap (margin ≈0.18),
  so conclusion (c) is a THEOREM, not conditional — review §5 satisfied.
- The well term needed adaptive bisection of `R`'s deep-well cells to certify `m_R>0`;
  a uniform grid floors `r2_lo` to 1e-300 and the bound diverges. This is the one
  implementation subtlety beyond the outline; resolved with the certified-bound
  frontier-refinement pattern. No remaining gap.

## Status of `current.md`

Builder did NOT write to `held`/`Status`/`Progress log` (reviewer's job). Only the
`## Bounds` snapshot's held block is unchanged; this is a theory milestone, no new
numeric bound. The new certified facts (the generator theorem) are a STRUCTURAL
milestone for the reviewer to log if verified.

## Gap-closure (R1b) — the well bound is now rigorous, R0 AND R2 fire certified

The R1 proof-reviewer (`R1-generative-review.md`) returned CHANGES REQUESTED on ONE
load-bearing step: the **global well cap** `|log|R/Q*|| <= log(1/m_R)+M_Q*` (paper
Lemma `lem:transfer` l.788-791; cert `RHS_global`). It is NOT a consequence of the
certified constants in the case `log|R| > log|Q*|` (true on 63-73% of W, reaching
+3.2): that case needs a certified UPPER bound on `|R|` and LOWER bound on `|Q*|`,
which the cert never provided. The cert reported `RHS = min(RHS_global, RHS_sharp)`
and `RHS_global` was binding — so the R2 PASS rested on an unjustified bound. Under
the unconditionally-valid SHARP bound alone, the reviewer found R0 still cleared but
**R2 did not** (r_Q2 + RHS_sharp = 0.2823 > log h = 0.25363, margin -0.029).

**Verified the gap myself** (per-cell well-integral diagnostic, N=40000 Q2->R2):
the loose old `RHS_sharp` (well integral 16.69, unnorm ~104) is dominated by WIDE
well cells where `q2_lo` (and `r2_lo`) floor to 0 — at the shared deep wells of R
and Q*, the per-cell ratio enclosure `r2hi/q2lo` blows up to ~e^353 even though the
true integrand `|log|R/Q*||` is ~1e-3. 9860 of 10116 well cells have `q2_lo<1e-6`
and carry essentially all of the 533 (unnorm) integral.

**Closure taken: route (B) — tighten the SHARP bound; DROP the global cap.**

- The per-cell well bound `max(log r_hi - log q_lo, log q_hi - log r_lo)` is a
  rigorous upper bound on `|log|R| - log|Q*||` over the cell, valid in BOTH cases
  (`log|R|` ≷ `log|Q*|`) — it is the honest per-cell enclosure of the integrand,
  not a global cap. It is integrable: at a shared well the per-cell value grows like
  `log(1/width)`, so `width * value -> 0`. Hence **adaptive bisection of the heavy
  well cells drives the certified well integral to the true ~1e-3 shift.**
- Added a SECOND refinement criterion to the existing adaptive driver: a well cell is
  now bisected if EITHER `|R|^2` is not yet certified `>0` (the old m_R criterion)
  OR its per-cell sharp contribution `w * |log|R/Q*||_hi > WELL_TOL = 5e-4`
  (unnormalized ds), up to `MAX_DEPTH = 34`.
- The certified `RHS` is now `RHS_sharp` **alone**; `RHS_global` is computed and
  printed but explicitly labelled NON-CERTIFYING (used nowhere in the verdict).

**The exact inequality with constants (certified, N=40000):**

    |r_R - r_Q*| <= (1/28)[ log c + (theta/(1-theta))|Omega_0| + int_W |log|R/Q*|| ds ]
                 =: RHS_sharp,    theta = 1/2, c = 1 (log c = 0).

  | seed->R | r_Q*(Omega_F) | int_Omega0 |..| | int_W |log R/Q*| (refined) | RHS_sharp | r_Q*+RHS_sharp | < log h=0.25363 |
  |---|---|---|---|---|---|---|
  | Q1->R0 | <= -0.0335 | 0.05317 | 0.08161 | <= 0.004814 | -0.02871 | YES (margin +0.282) |
  | Q2->R2 | <= -0.0330 | 0.05618 | 0.11980 | <= 0.006285 | -0.02672 | YES (margin +0.280) |

  (Both well integrals were ~16-105 unnormalized BEFORE refinement; the frontier
  refinement collapses them by a factor ~85-100. R2 now clears with margin +0.28,
  vs the old sharp-only margin of -0.029.) Verdict stable at N=200000 too:
  RHS_sharp R0=0.00377, R2=0.00447, margins +0.285/+0.284 — the adaptive well
  frontier, not the base N, sets the tightness.

**Final status:**
- **R0 (Q1 seed): CERTIFIED-FIRES.** (Was already certified under sharp; unchanged.)
- **R2 (Q2 seed): CERTIFIED-FIRES.** (Was the gap; now cleared rigorously by the
  refined sharp well integral, no global cap.)

Tamper checks E1 (understated log h not cleared), E2 (false deg R_5=27 rejected),
E3 (false 'a=6 preserves deg 28' rejected) all still reject. m_R>0 still certified
(0 unresolved well cells). The certificate prints a FIRING CERTIFICATION summary
listing each block as CERTIFIED-FIRES / NOT certified.

**New check command** (unchanged invocation; the verdict now rests on RHS_sharp only):

    cd constants/82a/certificate
    python3 firstvar_08_sibling_generator.py            # N=200000, ~4-5min, PASS
    python3 firstvar_08_sibling_generator.py 40000      # coarser base, ~3min, same verdict

**Paper changes:** Lemma `lem:transfer` (eq `transfer-bound`) now states the well term
as the integral `int_W |log|R/Q*|| ds`, finite via `m_R>0` and `sup log|Q*|<inf`,
with the proof giving the rigorous per-cell bound `max(L_R - l_Q*, L_Q* - l_R)` and
noting the `L^infty` cap is "too crude to certify — hence the cell-wise treatment".
Theorem `thm:generator` proof updated to the certified numbers (RHS<=0.0049/0.0063,
margin ~0.28) and to state explicitly "no global cap on |log|R/Q*|| invoked".
Both firing claims in the theorem are now backed by the certificate.
