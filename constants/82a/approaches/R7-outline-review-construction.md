# R7 outline review — DESIGN-PRINCIPLE construction of an original A-base block (82a UPPER)

Reviewed: `constants/82a/approaches/R7-design-principle-construction.md` (Angles 1–3).
Re-run against the on-disk harness: `verify_firstvar_lemma.py` (objective + root-potential
factorization), `flammang_table1.py` (the 24-entry originality dictionary), a fresh U^ν-well
+ objective-boundedness probe (below). All four functions the outline names
(`closed_form_rtilde`, `finite_diff_marginal`, `root_potential_check`, `float_value_q8A`)
exist and behave as the outline claims.

**Verdict: APPROVE (with two build-time guardrails to nail down, neither blocking).**

The design problem is well-posed, the optimization is bounded below (no scaling escape),
the objective IS the certified quantity, originality/admissibility are well-defined and
checkable, and the float-pre-gate-before-certify ordering is correctly placed so the builder
cannot trip the ~8-min silent-certify stall. The honest framing — structural deliverable
primary, certify a gated bonus — is exactly right and matches the audited saturation. Build it.

---

## 1. TECHNIQUE — is LLL/enumeration the right tool, and is the optimization well-posed? PASS

**Well-posedness (the user's hidden-obstruction worry — checked, no obstruction).** The
objective `r̃_Q = Σ_ρ U^ν(ρ) + deg·log|lead|` is NOT unbounded below by scaling the leading
coefficient. I confirmed on the R2 anchor (N=1M):

- `log|lead|` enters with weight = the active-arc measure `arcfrac = 0.06854 ≥ 0`. For an
  integer block `|lead| ≥ 1`, so `log|lead| ≥ 0` ⇒ a non-monic integer block PAYS
  `+0.0685·log|lead| > 0`. Scaling the leading coeff HURTS; the minimizer is monic. No
  scaling escape.
- `U^ν(ρ)` is the log-potential of a compactly-supported finite measure (mass `arcfrac`),
  bounded below by its deepest well, measured at **U_min ≈ −0.0382 at ρ ≈ 0.579 + 0.347i**
  (matches the audited cluster). Each root contributes `≥ U_min`, so for a degree-capped
  search (`d ≤ 10`) the objective is bounded: `r̃_Q ≥ d·U_min ≈ −0.38`. Well-posed per
  degree budget.

So the deg-cap `d ≤ 10` in the outline is load-bearing for boundedness — keep it.

**Is the lattice the right tool given sparsity?** Yes. The realized `r̃(j9) = −0.0068` comes
from 8 roots averaging only `−0.00085` each — two orders of magnitude above the `−0.038`
floor. The contour-root-free constraint (c1) forces most roots AWAY from the well (j9's
deepest-hugging pair sits 0.008 from the locus; the rest are positive contributors). This is
exactly why blind coeff enumeration is dry and `±1` perturbations of j9 flip the sign: the
firing lattice points are where integer roots happen to land near the well while the poly
stays root-free. Root-placement + LLL (find the nearest integer poly to a real well-targeting
target in the ν-Gram metric) is the principled tool for that; seeded enumeration (Angle 2) is
the cheap first pass. The U^ν-well precompute making the search targeted is sound — I
reproduced the deepest well it relies on.

**One caveat to state, not a blocker:** boundedness holds *per fixed degree*. Across degree,
each extra well-seated root lowers `r̃` further, so the objective is NOT coercive in `deg` —
but the contour-root-free + integer constraints make the realizable firing set sparse
(audited), so there is no "push degree up to drive r̃ → −∞" free lunch. The builder should NOT
claim a global minimizer; the deliverable is "the most-negative original admissible block
found within the deg ≤ 10 / height budget," which is honest and sufficient.

## 2. ORIGINALITY / ADMISSIBILITY — well-defined and checkable? PASS

- **Originality is well-defined.** `flammang_table1._TABLE_DESCENDING` is a list of exactly
  **24** `(mahler, descending-coeffs)` tuples. "Q ∉ Table-1" = Q's descending integer coeff
  list (normalized to leading sign) equals none of the 24 — a deterministic sympy/list
  equality, fully verifiable. The outline's "(24 entries)" is correct. Also require
  `Q ∉ {dictionary blocks}` — same check. Good.
- **(c1) contour-root-free, threshold `min_s|Q∘χ| ≥ 1e−2`.** Correctly the ONLY block that
  must be contour-root-free (it is the candidate whose `log|Q∘χ|` enters the difference-
  quotient dominator — see the R7-firstvar review's H1′). The threshold matches the audited
  witness margins (j9 1.06e−2, j6 8.21e−3). Note j6 at 8.2e−3 would FAIL a strict `≥1e−2`
  gate — that is fine (j6 is dry anyway), but the builder should treat `1e−2` as a SCREEN for
  L¹-safety, and the true requirement is only `min|Q∘χ| > 0` (strictly no contour root). Do
  not reject an otherwise-firing original block solely for landing at, say, 7e−3; re-check it
  is genuinely root-free and accept. State this so a good block is not discarded on a soft
  threshold.
- **No `Q(0)=Q(1)=1` needed for an A-base block — CORRECT** (run_state Rule; A-base needs only
  Doc01a cond (4) non-degeneracy + coprimality). Confirmed against the run_state rule.
- **(c2) coprime + squarefree vs the active dictionary
  `{P1,P2,P4,P6,P8,j3,j9,Q1,Q2,Q5,Q6}`.** This is the correct 11-block dictionary
  (`BASE=[P1,P2,P4,P6,P8]` in verify_upper.py + j3,j9 A-base + Q1,Q2 + perturbers Q5,Q6).
  Coprimality is in `w = z(1−z)`, the shared variable (per R6 verify_shared_pool). The builder
  must run the gcd in `w`, not in raw `X` — flag, since the blocks are written as polys in the
  contour variable.

## 3. FEASIBILITY HONESTY + anti-stall ordering — PASS, correctly placed

- The FEASIBILITY HONESTY section is unambiguous: the numeric lever is probably dry, the
  STRUCTURAL outcome (original admissible Q* with reviewer-reproducible `r̃_Q* < 0`) is the
  PRIMARY deliverable, the certify is an opportunistic bonus. This matches the audited
  saturation (j3 +1.49e−4 → j9 +3.2e−6, and j16/j17/j20 project ~3e−6 < the 5e−6 gate). Honest
  and correct — do not let the builder soften it into "we expect a break."
- **Anti-stall ordering is correctly placed.** Step order: cheap design+score (`design_block.py`,
  1–3 min) → finite-diff r̃ confirmation (1 min) → **float pre-gate at N≥4M requiring N-stable
  drop ≥ 5e−6** (step 5) → certify ONLY if the gate passes (step 6). The ≥5e−6 float gate sits
  strictly BEFORE the ~8-min branch-and-bound, so the builder never enters the silent certify
  unless a real margin exists. This is exactly the run_state anti-stall + round-4 saturation
  rule. Per my role memory the empirical cert slack is ~1.2e−7..2.0e−7, so the 5e−6 gate is
  ~25–40× slack — safe, not knife-edge.
- **HELD_CERT guardrail — restate forcefully.** Step 6 correctly says set HELD_CERT to the TRUE
  held **0.2538893183**. Per my role memory, cloned q-harnesses ship a STALE hardcoded target
  (q7A has 0.2540419719, q8A has 0.2538925359 — both superseded). The builder MUST overwrite
  HELD_CERT to 0.2538893183 in any q9A clone, else certify rubber-stamps an easy target and
  emits a FALSE break. This is the single most dangerous footgun in the certify path. The
  outline names it; make it the first edit in the clone.

## 4. Circularity / missing-case / void-the-result checks

- **No circularity.** The objective `r̃_Q` scored by `design_block.py` IS the certified
  first-variation quantity (`closed_form_rtilde`), cross-checked against the root-potential
  identity (verified to 5.2e−17) and against `finite_diff_marginal` — so "r̃ < 0" is the R6
  lemma APPLIED, not a fresh assertion. The design problem and the verification close on the
  same object. Clean.
- **Anchor trap — the one place the builder could void the structural milestone.** A NEW
  (third) A-base block is a first variation at q_Q=0, so r̃ MUST be measured on a family WITHOUT
  it. The outline says R2 — but R2 has j3 ON, j9 OFF. The new block Q* would sit ALONGSIDE BOTH
  j3 and j9 in the certify family, so the correct q_Q=0 anchor for Q* is the **R4 family (j3 AND
  j9 both on, Q* off)**, NOT R2. The outline's "anchor = R2" is the anchor j9 was screened on;
  for an ORIGINAL THIRD block the anchor is R4 (the family it is being added to, at its own
  exponent 0). The builder must measure `r̃_Q*` on R4, recomputing {A>B} there. Measuring on R2
  (which lacks j9) evaluates the derivative at the wrong base point and can mis-sign. THIS IS
  THE LOAD-BEARING CORRECTION — pin it before building. (For the U^ν-well *map* used only to
  SEED the search, R2 vs R4 barely matters; for the FINAL `r̃_Q* < 0` claim that is the
  milestone, it must be R4.) Note the R4 active arc differs slightly from R2 (arcfrac 0.0685
  vs the R4 value) — recompute, don't transplant.
- **Squarefree/coprime self-check:** an original block built by root-placement could
  accidentally share a factor with j3 or j9 (the seeds). The sympy gcd gate (c2) catches it;
  ensure it runs in `w` and includes j3, j9 explicitly (the dictionary the seeds come from).
- **Don't overclaim "global minimum of the integer-transfinite-diameter problem."** The
  deliverable is a CONSTRUCTED original firing block + the method, not a proof of optimality.
  The write-up must say "an original admissible block the design principle produces," not "the
  optimal integer block" — else a reviewer rejects an unproven optimality claim.

---

## Required build-time guardrails (none blocking the round)

1. **ANCHOR = R4, not R2, for the final `r̃_Q* < 0` milestone claim** (a third A-base block's
   q_Q=0 base family has BOTH j3 and j9 on). R2 is fine only for seeding the U^ν well-map.
   Recompute {A>B} on R4. (Load-bearing — gets the sign right.)
2. **HELD_CERT = 0.2538893183** in any q9A certify clone (overwrite the stale hardcoded
   superseded value FIRST). Gate certify on frontier=0 below 0.2538893183.
3. **Keep deg ≤ 10** (boundedness of the objective rests on the degree cap) and the monic
   preference (non-monic integer lead pays `+0.0685·log|lead| > 0`).
4. **(c1) is an L¹ SCREEN, true requirement is strictly-no-contour-root** (`min|Q∘χ| > 0`); do
   not discard a firing original block that lands just under 1e−2 if it is genuinely root-free.
5. **gcd/squarefree in `w = z(1−z)`** against the full 11-block dictionary incl. j3, j9.
6. **Frame the deliverable as "an original admissible firing block the method produces,"** not
   a global optimum; keep the FEASIBILITY HONESTY (structural primary, certify gated bonus)
   verbatim. Do not write any unverified search value into constants/ as `held`.

With guardrail 1 (the R4 anchor) and guardrail 2 (HELD_CERT), the structural milestone is
clean and reproducible and the certify path is safe. Build Angle 2 (cheap seeded enumeration)
→ Angle 1 (LLL) → Angle 3 (well-tiling), scoring on R4, stopping at the structural deliverable
unless the ≥5e−6 float gate clears.
